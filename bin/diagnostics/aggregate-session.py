#!/usr/bin/env python3
"""aggregate-session.py — per-session diagnostics aggregator.

Reads the Claude Code transcript JSONL for a session, attributes tokens to
specific agents (via isSidechain + Agent tool_use boundaries), aggregates tool
counts, computes per-tool latency from pre/post events, parses critique verdicts
and loops, and emits diagnostics/metrics.json.

Schema-aware: handles both the legacy `{ts, tool}` event format and the
OpenTelemetry-aligned `{ts_ns, event, gen_ai.*}` format introduced 2026-05-17.

Runs synchronously from session-end.sh once per session (was: per-turn from
stop.sh). AI-blind: no chat output, errors swallowed silently.

Usage:
    aggregate-session.py <workflow-id> <claude-session-uuid> [project-root]
"""
from __future__ import annotations

import glob
import json
import os
import pathlib
import re
import sys
from collections import defaultdict


# -----------------------------------------------------------------------------
# Transcript discovery + token attribution (unchanged from parse-session-metrics)
# -----------------------------------------------------------------------------

def find_transcript(claude_uuid: str) -> pathlib.Path | None:
    """Find the main transcript JSONL matching this Claude session UUID."""
    home = pathlib.Path.home()
    pattern = str(home / ".claude" / "projects" / "*" / f"{claude_uuid}.jsonl")
    matches = glob.glob(pattern)
    return pathlib.Path(matches[0]) if matches else None


def find_subagents_dir(transcript_path: pathlib.Path) -> pathlib.Path | None:
    """Subagent transcripts live in `<project>/<claude-uuid>/subagents/`."""
    candidate = transcript_path.with_suffix("") / "subagents"
    return candidate if candidate.is_dir() else None


def sum_tokens(jsonl_path: pathlib.Path) -> tuple[int, int, int, int]:
    """Sum input/output + cache_read/cache_creation tokens across assistant entries."""
    total_in = total_out = cache_read = cache_create = 0
    try:
        with open(jsonl_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "assistant":
                    continue
                usage = (entry.get("message") or {}).get("usage") or {}
                total_in += int(usage.get("input_tokens") or 0)
                total_out += int(usage.get("output_tokens") or 0)
                cache_read += int(usage.get("cache_read_input_tokens") or 0)
                cache_create += int(usage.get("cache_creation_input_tokens") or 0)
    except OSError:
        pass
    return total_in, total_out, cache_read, cache_create


def parse_main_transcript(transcript_path: pathlib.Path) -> dict:
    """Walk the main transcript: main-thread tokens, tool counts."""
    main_in = main_out = main_cache_read = main_cache_create = 0
    tool_counts: dict[str, int] = defaultdict(int)
    total_tools = 0
    response_models: dict[str, int] = defaultdict(int)

    with open(transcript_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "assistant":
                continue
            if entry.get("isSidechain"):
                continue

            msg = entry.get("message") or {}
            usage = msg.get("usage") or {}
            main_in += int(usage.get("input_tokens") or 0)
            main_out += int(usage.get("output_tokens") or 0)
            main_cache_read += int(usage.get("cache_read_input_tokens") or 0)
            main_cache_create += int(usage.get("cache_creation_input_tokens") or 0)

            model = msg.get("model")
            if model:
                response_models[model] += 1

            for content in (msg.get("content") or []):
                if not isinstance(content, dict):
                    continue
                if content.get("type") != "tool_use":
                    continue
                tool_name = content.get("name", "unknown")
                tool_counts[tool_name] += 1
                total_tools += 1

    return {
        "main_input": main_in,
        "main_output": main_out,
        "main_cache_read": main_cache_read,
        "main_cache_creation": main_cache_create,
        "tool_counts": dict(tool_counts),
        "total_tools": total_tools,
        "response_models": dict(response_models),
    }


def parse_subagents(subagents_dir: pathlib.Path) -> dict:
    """For each subagent transcript, read sibling .meta.json for agentType,
    sum tokens, group by agentType."""
    by_agent_input: dict[str, int] = defaultdict(int)
    by_agent_output: dict[str, int] = defaultdict(int)
    by_agent_cache_read: dict[str, int] = defaultdict(int)
    by_agent_cache_create: dict[str, int] = defaultdict(int)
    by_agent_calls: dict[str, int] = defaultdict(int)

    for meta_path in subagents_dir.glob("agent-*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        agent_type = meta.get("agentType") or "unknown"
        jsonl_path = meta_path.parent / meta_path.name.replace(".meta.json", ".jsonl")
        if not jsonl_path.is_file():
            continue
        ti, to, cr, cc = sum_tokens(jsonl_path)
        by_agent_input[agent_type] += ti
        by_agent_output[agent_type] += to
        by_agent_cache_read[agent_type] += cr
        by_agent_cache_create[agent_type] += cc
        by_agent_calls[agent_type] += 1

    return {
        "by_agent_input": dict(by_agent_input),
        "by_agent_output": dict(by_agent_output),
        "by_agent_cache_read": dict(by_agent_cache_read),
        "by_agent_cache_creation": dict(by_agent_cache_create),
        "by_agent_calls": dict(by_agent_calls),
    }


def build_token_block(transcript_path: pathlib.Path) -> dict:
    """Combine main-thread + per-subagent token attribution."""
    main = parse_main_transcript(transcript_path)
    subagents_dir = find_subagents_dir(transcript_path)
    sub = (
        parse_subagents(subagents_dir)
        if subagents_dir
        else {
            "by_agent_input": {}, "by_agent_output": {},
            "by_agent_cache_read": {}, "by_agent_cache_creation": {},
            "by_agent_calls": {},
        }
    )

    by_agent: dict[str, dict] = {}
    by_agent["main"] = {
        "input": main["main_input"],
        "output": main["main_output"],
        "cache_read": main["main_cache_read"],
        "cache_creation": main["main_cache_creation"],
        "calls": 0,
    }
    keys = (
        set(sub["by_agent_input"])
        | set(sub["by_agent_output"])
        | set(sub["by_agent_calls"])
    )
    for agent in sorted(keys):
        by_agent[agent] = {
            "input": sub["by_agent_input"].get(agent, 0),
            "output": sub["by_agent_output"].get(agent, 0),
            "cache_read": sub["by_agent_cache_read"].get(agent, 0),
            "cache_creation": sub["by_agent_cache_creation"].get(agent, 0),
            "calls": sub["by_agent_calls"].get(agent, 0),
        }

    total_in = sum(v["input"] for v in by_agent.values())
    total_out = sum(v["output"] for v in by_agent.values())
    total_cache_read = sum(v["cache_read"] for v in by_agent.values())
    total_cache_create = sum(v["cache_creation"] for v in by_agent.values())

    return {
        "tokens": {
            "total": {
                "input": total_in,
                "output": total_out,
                "cache_read": total_cache_read,
                "cache_creation": total_cache_create,
            },
            "by_agent": by_agent,
            "source": "transcript-parsed",
        },
        "tool_calls": {
            "total": main["total_tools"],
            "by_type": main["tool_counts"],
        },
        "models_seen": main["response_models"],
    }


# -----------------------------------------------------------------------------
# Hook-event aggregation: latency, errors, agent-end events
# -----------------------------------------------------------------------------

def parse_hook_events(events_path: pathlib.Path) -> dict:
    """Aggregate hook-emitted events.jsonl.

    Handles both schemas:
        legacy: {"ts": <unix>, "tool": "<name>"}
        new:    {"ts_ns": <ns>, "event": "tool_start|tool_end|tool_error|...", "gen_ai.tool.name": "...", "gen_ai.tool.call.id": "..."}

    Returns aggregated latency, error counts, and per-event-type counts.
    """
    result = {
        "events_by_type": defaultdict(int),
        "tools_by_status": defaultdict(int),
        "latency_ms_by_tool": defaultdict(list),
        "errors_by_tool": defaultdict(int),
        "error_types": defaultdict(int),
        "schema_version": "unknown",
    }
    if not events_path.is_file():
        return _finalize_event_result(result)

    starts: dict[str, int] = {}  # tool_use_id → ts_ns
    legacy = new = 0

    try:
        with open(events_path) as f:
            for line in f:
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Detect schema
                if "event" in e and "ts_ns" in e:
                    new += 1
                    _handle_new_event(e, starts, result)
                elif "tool" in e and "ts" in e:
                    legacy += 1
                    # legacy schema only counts tools, no latency available
                    result["tools_by_status"][e.get("tool", "unknown")] += 1
                    result["events_by_type"]["tool_end_legacy"] += 1
    except OSError:
        pass

    if new and not legacy:
        result["schema_version"] = "otel-aligned-2026-05"
    elif legacy and not new:
        result["schema_version"] = "legacy-ts-tool"
    elif new and legacy:
        result["schema_version"] = "mixed"
    return _finalize_event_result(result)


def _handle_new_event(e: dict, starts: dict, result: dict) -> None:
    ev = e.get("event", "")
    result["events_by_type"][ev] += 1
    tool_id = e.get("gen_ai.tool.call.id", "")
    tool_name = e.get("gen_ai.tool.name", "unknown")
    ts_ns = e.get("ts_ns")

    if ev == "tool_start" and tool_id and isinstance(ts_ns, int):
        starts[tool_id] = ts_ns
    elif ev == "tool_end" and tool_id:
        start_ns = starts.pop(tool_id, None)
        status = e.get("tool.status", "ok")
        result["tools_by_status"][f"{tool_name}:{status}"] += 1
        if start_ns and isinstance(ts_ns, int):
            latency_ms = (ts_ns - start_ns) / 1_000_000
            result["latency_ms_by_tool"][tool_name].append(latency_ms)
    elif ev == "tool_error" and tool_id:
        # Match against prior start; also count the error
        starts.pop(tool_id, None)
        result["errors_by_tool"][tool_name] += 1
        err = e.get("_err") or {}
        err_type = err.get("error.type", "unknown") if isinstance(err, dict) else "unknown"
        result["error_types"][err_type] += 1


def _finalize_event_result(r: dict) -> dict:
    # Compute latency summaries (p50, p95, count) per tool
    latency_summary = {}
    for tool, samples in r["latency_ms_by_tool"].items():
        if not samples:
            continue
        s = sorted(samples)
        n = len(s)
        latency_summary[tool] = {
            "n": n,
            "p50_ms": round(s[n // 2], 2),
            "p95_ms": round(s[min(n - 1, int(n * 0.95))], 2),
            "max_ms": round(s[-1], 2),
            "total_ms": round(sum(s), 2),
        }
    return {
        "schema_version": r["schema_version"],
        "events_by_type": dict(r["events_by_type"]),
        "tools_by_status": dict(r["tools_by_status"]),
        "latency_summary": latency_summary,
        "errors_by_tool": dict(r["errors_by_tool"]),
        "error_types": dict(r["error_types"]),
    }


# -----------------------------------------------------------------------------
# Critique / verdict parsing
# -----------------------------------------------------------------------------

def parse_verdicts(critiques_dir: pathlib.Path) -> dict:
    """Extract verdict + (optional) confidence from each non-shadow, non-comparison critique."""
    out: dict[str, dict] = {}
    if not critiques_dir.is_dir():
        return out
    for crit_file in critiques_dir.glob("*.md"):
        stem = crit_file.stem
        if "shadow" in stem or "comparison" in stem:
            continue
        try:
            txt = crit_file.read_text(errors="replace")
        except OSError:
            continue
        v = re.search(r"(?:^|\n)\s*Verdict\s*[:=]\s*(\w+)", txt, re.IGNORECASE)
        if not v:
            # Loose match anywhere
            v = re.search(r"verdict\s*[:=]\s*(\w+)", txt, re.IGNORECASE)
        if v:
            entry = {"verdict": v.group(1).lower()}
            c = re.search(r"(?:^|\n)\s*Confidence\s*[:=]\s*([\d.]+)", txt, re.IGNORECASE)
            if c:
                try:
                    entry["confidence"] = float(c.group(1))
                except ValueError:
                    pass
            out[stem] = entry
    return out


def parse_shadow_verdicts(critiques_dir: pathlib.Path) -> dict:
    """Same shape as parse_verdicts but for .shadow.md files."""
    out: dict[str, dict] = {}
    if not critiques_dir.is_dir():
        return out
    for crit_file in critiques_dir.glob("*.shadow.md"):
        stem = crit_file.stem.replace(".shadow", "")
        try:
            txt = crit_file.read_text(errors="replace")
        except OSError:
            continue
        v = re.search(r"(?:^|\n)\s*Verdict\s*[:=]\s*(\w+)", txt, re.IGNORECASE)
        if not v:
            v = re.search(r"verdict\s*[:=]\s*(\w+)", txt, re.IGNORECASE)
        if v:
            entry = {"verdict": v.group(1).lower()}
            c = re.search(r"(?:^|\n)\s*Confidence\s*[:=]\s*([\d.]+)", txt, re.IGNORECASE)
            if c:
                try:
                    entry["confidence"] = float(c.group(1))
                except ValueError:
                    pass
            out[stem] = entry
    return out


def parse_comparator_agreements(critiques_dir: pathlib.Path) -> dict:
    """Extract agreement-class from each <lens>.comparison.md."""
    out: dict[str, str] = {}
    if not critiques_dir.is_dir():
        return out
    for cmp_file in critiques_dir.glob("*.comparison.md"):
        lens = cmp_file.stem.replace(".comparison", "")
        try:
            txt = cmp_file.read_text(errors="replace")
        except OSError:
            continue
        # Look for explicit agreement class (agree | partial-agree | disagree | unavailable)
        m = re.search(r"\b(agree|partial-agree|disagree|unavailable)\b", txt, re.IGNORECASE)
        if m:
            out[lens] = m.group(1).lower()
    return out


def parse_loops(decision_log: pathlib.Path) -> int:
    """Best-effort: count `rewrite | replan` decisions in the log."""
    if not decision_log.is_file():
        return 0
    try:
        txt = decision_log.read_text(errors="replace")
    except OSError:
        return 0
    # Prefer explicit "Loop count: N/2" line if present
    m = re.search(r"Loop count[:\s]+(\d+)\s*/\s*\d", txt, re.IGNORECASE)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            pass
    return len(re.findall(r"\b(rewrite|replan)\b", txt, re.IGNORECASE))


def count_decisions(synthesis: pathlib.Path) -> int:
    """Count bulleted/numbered items under Recommendation + Uncertainties headings."""
    if not synthesis.is_file():
        return 0
    try:
        txt = synthesis.read_text(errors="replace")
    except OSError:
        return 0
    # Split on headings; grab sections that look like recommendation or uncertainties
    sections = re.split(r"\n##\s+", "\n" + txt)
    decisions = 0
    for sec in sections:
        head = sec.splitlines()[0].lower() if sec.strip() else ""
        if any(
            kw in head
            for kw in ("recommendation", "uncertaint", "post-critique")
        ):
            # Count list items (both - and 1.)
            decisions += len(re.findall(r"(?m)^\s*(?:[-*]|\d+\.)\s+\S", sec))
    return decisions


def count_artifacts(session_dir: pathlib.Path) -> int:
    """Count .md files in session dir, excluding ledger.md."""
    return sum(1 for p in session_dir.rglob("*.md") if p.name != "ledger.md")


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def read_int(path: pathlib.Path) -> int | None:
    try:
        return int(path.read_text().strip())
    except (OSError, ValueError):
        return None


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 3:
        print(
            f"usage: {sys.argv[0]} <workflow-id> <claude-session-uuid> [project-root]",
            file=sys.stderr,
        )
        return 2

    workflow_id = sys.argv[1]
    claude_uuid = sys.argv[2]
    project_root = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else os.getcwd())

    session_dir = project_root / ".claude" / "session-artifacts" / workflow_id
    diag_dir = session_dir / "diagnostics"
    if not diag_dir.is_dir():
        return 0  # nothing to do

    start_ts = read_int(diag_dir / "start.ts")
    end_ts = read_int(diag_dir / "end.ts")
    duration = (end_ts - start_ts) if (start_ts is not None and end_ts is not None) else None

    metrics: dict = {
        "workflow_id": workflow_id,
        "claude_session_uuid": claude_uuid,
        "duration_seconds": duration,
        "schema": "diagnostics-2026-05",
    }

    # Transcript-derived token + tool block
    transcript = find_transcript(claude_uuid)
    if transcript:
        try:
            metrics.update(build_token_block(transcript))
        except Exception as e:  # noqa: BLE001 — fail open
            metrics["tokens"] = {
                "total": {"input": 0, "output": 0},
                "by_agent": {},
                "source": f"parse-error: {type(e).__name__}",
            }
            metrics["tool_calls"] = {"total": 0, "by_type": {}}
    else:
        metrics["tokens"] = {
            "total": {"input": 0, "output": 0},
            "by_agent": {},
            "source": "transcript-missing",
        }
        metrics["tool_calls"] = {"total": 0, "by_type": {}}

    # Hook-event aggregation (latency, errors)
    metrics["events"] = parse_hook_events(diag_dir / "events.jsonl")

    # Critique parsing
    crit_dir = session_dir / "critiques"
    metrics["verdicts"] = parse_verdicts(crit_dir)
    metrics["shadow_verdicts"] = parse_shadow_verdicts(crit_dir)
    metrics["comparator_agreements"] = parse_comparator_agreements(crit_dir)

    # Workflow counts
    metrics["loops"] = parse_loops(session_dir / "decision-log.md")
    metrics["counts"] = {
        "artifacts": count_artifacts(session_dir),
        "decisions": count_decisions(session_dir / "synthesis.md"),
    }

    # Write
    out_path = diag_dir / "metrics.json"
    try:
        out_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    except OSError:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
