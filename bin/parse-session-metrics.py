#!/usr/bin/env python3
"""parse-session-metrics.py — post-session diagnostics parser.

Reads the Claude Code transcript JSONL for a session, attributes tokens to
specific agents (via isSidechain + Agent tool_use boundaries), aggregates tool
counts, parses critique verdicts and loops, and emits diagnostics/metrics.json.

Runs as a backgrounded process spawned by the Stop hook. AI-blind: no chat
output, errors are swallowed silently.

Usage:
    parse-session-metrics.py <workflow-id> <claude-session-uuid> [project-root]
"""
from __future__ import annotations

import glob
import json
import os
import pathlib
import re
import sys
from collections import defaultdict


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


def sum_tokens(jsonl_path: pathlib.Path) -> tuple[int, int]:
    """Sum input/output tokens across all assistant entries in a JSONL."""
    total_in = total_out = 0
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
    except OSError:
        pass
    return total_in, total_out


def parse_main_transcript(transcript_path: pathlib.Path) -> dict:
    """Walk the main transcript: main-thread tokens, tool counts."""
    main_in = main_out = 0
    tool_counts: dict[str, int] = defaultdict(int)
    total_tools = 0

    with open(transcript_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "assistant":
                continue
            # Skip sidechain entries (current Claude Code stores subagents in
            # separate files; older transcripts may have inline sidechains)
            if entry.get("isSidechain"):
                continue

            msg = entry.get("message") or {}
            usage = msg.get("usage") or {}
            main_in += int(usage.get("input_tokens") or 0)
            main_out += int(usage.get("output_tokens") or 0)

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
        "tool_counts": dict(tool_counts),
        "total_tools": total_tools,
    }


def parse_subagents(subagents_dir: pathlib.Path) -> dict:
    """For each subagent transcript, read sibling .meta.json for agentType,
    sum tokens, group by agentType."""
    by_agent_input: dict[str, int] = defaultdict(int)
    by_agent_output: dict[str, int] = defaultdict(int)
    by_agent_calls: dict[str, int] = defaultdict(int)

    for meta_path in subagents_dir.glob("agent-*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        agent_type = meta.get("agentType") or "unknown"
        jsonl_path = meta_path.with_suffix("")  # strips ".json", leaves "...meta"
        # Actually .meta.json → strip last two suffixes to get the .jsonl
        jsonl_path = meta_path.parent / meta_path.name.replace(".meta.json", ".jsonl")
        if not jsonl_path.is_file():
            continue
        ti, to = sum_tokens(jsonl_path)
        by_agent_input[agent_type] += ti
        by_agent_output[agent_type] += to
        by_agent_calls[agent_type] += 1

    return {
        "by_agent_input": dict(by_agent_input),
        "by_agent_output": dict(by_agent_output),
        "by_agent_calls": dict(by_agent_calls),
    }


def build_token_block(transcript_path: pathlib.Path) -> dict:
    """Combine main-thread + per-subagent token attribution."""
    main = parse_main_transcript(transcript_path)
    subagents_dir = find_subagents_dir(transcript_path)
    sub = (
        parse_subagents(subagents_dir)
        if subagents_dir
        else {"by_agent_input": {}, "by_agent_output": {}, "by_agent_calls": {}}
    )

    by_agent: dict[str, dict] = {}
    by_agent["main"] = {
        "input": main["main_input"],
        "output": main["main_output"],
        "calls": 0,
    }
    keys = set(sub["by_agent_input"]) | set(sub["by_agent_output"]) | set(sub["by_agent_calls"])
    for agent in sorted(keys):
        by_agent[agent] = {
            "input": sub["by_agent_input"].get(agent, 0),
            "output": sub["by_agent_output"].get(agent, 0),
            "calls": sub["by_agent_calls"].get(agent, 0),
        }

    total_in = sum(v["input"] for v in by_agent.values())
    total_out = sum(v["output"] for v in by_agent.values())

    return {
        "tokens": {
            "total": {"input": total_in, "output": total_out},
            "by_agent": by_agent,
            "source": "transcript-parsed",
        },
        "tool_calls": {
            "total": main["total_tools"],
            "by_type": main["tool_counts"],
        },
    }


def parse_verdicts(critiques_dir: pathlib.Path) -> dict:
    """Best-effort: extract `verdict: <X>` lines from each critique markdown."""
    verdicts = {}
    if not critiques_dir.is_dir():
        return verdicts
    for crit_file in critiques_dir.glob("*.md"):
        if "shadow" in crit_file.stem or "comparison" in crit_file.stem:
            continue
        try:
            txt = crit_file.read_text(errors="replace")
        except OSError:
            continue
        m = re.search(r"verdict\s*[:=]\s*(\w+)", txt, re.IGNORECASE)
        if m:
            verdicts[crit_file.stem] = m.group(1).lower()
    return verdicts


def parse_loops(decision_log: pathlib.Path) -> int:
    """Best-effort: count `rewrite | replan` decisions in the log."""
    if not decision_log.is_file():
        return 0
    try:
        txt = decision_log.read_text(errors="replace")
    except OSError:
        return 0
    return len(re.findall(r"\b(rewrite|replan)\b", txt, re.IGNORECASE))


def read_int(path: pathlib.Path) -> int | None:
    try:
        return int(path.read_text().strip())
    except (OSError, ValueError):
        return None


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

    metrics: dict = {"duration_seconds": duration}

    transcript = find_transcript(claude_uuid)
    if transcript:
        try:
            metrics.update(build_token_block(transcript))
        except Exception as e:  # noqa: BLE001 — fail open; never crash the hook chain
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

    metrics["verdicts"] = parse_verdicts(session_dir / "critiques")
    metrics["loops"] = parse_loops(session_dir / "decision-log.md")

    (diag_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
