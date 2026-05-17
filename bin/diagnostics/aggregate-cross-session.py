#!/usr/bin/env python3
"""aggregate-cross-session.py — cross-session diagnostics aggregator.

Walks every session's diagnostics/metrics.json (across the main repo + any
git worktrees attached to it) and produces:
  - .claude/.metrics/cross-session.json         (always; stdlib-only)
  - .claude/.metrics/cross-session.duckdb       (if duckdb is installed)
  - .claude/.metrics/cross-session-report.html  (always; stdlib-only)

DuckDB is OPTIONAL. If absent, the script logs a hint to stderr and continues
with stdlib aggregation — the workflow never breaks for missing deps.

Worktree-aware: discovers worktree paths via `git worktree list` and globs
each one's session-artifacts dir.

Usage:
    aggregate-cross-session.py [project-root]
"""
from __future__ import annotations

import json
import os
import pathlib
import statistics
import subprocess
import sys
from collections import defaultdict
from datetime import datetime


def discover_session_dirs(project_root: pathlib.Path) -> list[pathlib.Path]:
    """Return every session-artifacts dir reachable from this repo, including
    worktree-mounted ones. Falls back to the main repo only if `git worktree
    list` fails."""
    roots = [project_root]
    try:
        out = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=project_root, capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            for line in out.stdout.splitlines():
                if line.startswith("worktree "):
                    wt = pathlib.Path(line[len("worktree "):].strip())
                    if wt != project_root and wt.is_dir():
                        roots.append(wt)
    except (subprocess.SubprocessError, OSError, FileNotFoundError):
        pass

    session_dirs = []
    for root in roots:
        sa = root / ".claude" / "session-artifacts"
        if not sa.is_dir():
            continue
        for child in sa.iterdir():
            if child.is_dir() and not child.name.startswith(("exemplars", ".")):
                session_dirs.append(child)
    return session_dirs


def load_session_metrics(session_dir: pathlib.Path) -> dict | None:
    """Load metrics.json + augment with the session id."""
    metrics_path = session_dir / "diagnostics" / "metrics.json"
    if not metrics_path.is_file():
        return None
    try:
        m = json.loads(metrics_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    m["_session_id"] = session_dir.name
    m["_session_dir"] = str(session_dir)
    return m


def stdlib_aggregate(sessions: list[dict]) -> dict:
    """Pure-stdlib aggregation: per-lens verdict counts, per-agent token totals,
    loop distribution, refusal rate (when judge_score events land in v2).
    """
    if not sessions:
        return {"session_count": 0}

    durations = [s.get("duration_seconds") for s in sessions if isinstance(s.get("duration_seconds"), int)]
    loops = [s.get("loops", 0) for s in sessions]
    loop_distribution: dict[int, int] = defaultdict(int)
    for n in loops:
        loop_distribution[n] += 1

    verdict_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for s in sessions:
        for lens, entry in (s.get("verdicts") or {}).items():
            if isinstance(entry, dict):
                v = entry.get("verdict", "unknown")
            else:
                # Older parser stored a bare string
                v = str(entry)
            verdict_counts[lens][v] += 1

    agreement_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for s in sessions:
        for lens, agreement in (s.get("comparator_agreements") or {}).items():
            agreement_counts[lens][str(agreement)] += 1

    token_by_agent_total: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for s in sessions:
        for agent, vals in (s.get("tokens", {}).get("by_agent") or {}).items():
            if not isinstance(vals, dict):
                continue
            for k in ("input", "output", "cache_read", "cache_creation", "calls"):
                token_by_agent_total[agent][k] += int(vals.get(k, 0) or 0)

    error_totals: dict[str, int] = defaultdict(int)
    for s in sessions:
        for tool, n in (s.get("events", {}).get("errors_by_tool") or {}).items():
            error_totals[tool] += int(n)

    summary = {
        "session_count": len(sessions),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "duration_summary": {
            "count": len(durations),
            "total_s": sum(durations) if durations else 0,
            "mean_s": round(statistics.mean(durations), 1) if durations else None,
            "median_s": int(statistics.median(durations)) if durations else None,
            "max_s": max(durations) if durations else None,
        },
        "loop_distribution": dict(loop_distribution),
        "loop_cap_reached_rate": (sum(1 for n in loops if n >= 2) / len(loops)) if loops else 0,
        "verdict_counts_by_lens": {k: dict(v) for k, v in verdict_counts.items()},
        "agreement_counts_by_lens": {k: dict(v) for k, v in agreement_counts.items()},
        "token_totals_by_agent": {k: dict(v) for k, v in token_by_agent_total.items()},
        "tool_error_totals": dict(error_totals),
    }
    return summary


def duckdb_aggregate(project_root: pathlib.Path, sessions: list[dict]) -> dict | None:
    """Optional DuckDB-powered aggregation. Returns None if DuckDB missing."""
    try:
        import duckdb  # type: ignore
    except ImportError:
        return None

    # Persist a DuckDB file under .metrics/ for query reuse.
    db_path = project_root / ".claude" / ".metrics" / "cross-session.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Build a single Parquet/JSON view from all events.jsonl files (worktree-aware).
    event_globs = []
    for s in sessions:
        events_path = pathlib.Path(s["_session_dir"]) / "diagnostics" / "events.jsonl"
        if events_path.is_file():
            event_globs.append(str(events_path))

    if not event_globs:
        return {"duckdb": "ok", "events_loaded": 0, "note": "no events.jsonl files found"}

    con = duckdb.connect(str(db_path))
    try:
        # Create / refresh the events view from all per-session JSONL files.
        # union_by_name handles schema drift across sessions.
        con.execute("CREATE OR REPLACE TABLE events AS SELECT * FROM read_json_auto(?, union_by_name=true)",
                    [event_globs])
        n = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]

        # Inspect available columns so the query is schema-aware
        cols = {row[0] for row in con.execute("DESCRIBE events").fetchall()}

        # Build a defensive tool-name expression: prefer new schema (gen_ai.tool.name),
        # fall back to legacy (tool). All columns are nullable thanks to union_by_name.
        tool_expr_parts = []
        if "gen_ai.tool.name" in cols:
            tool_expr_parts.append('"gen_ai.tool.name"')
        if "tool" in cols:
            tool_expr_parts.append("tool")
        if not tool_expr_parts:
            return {
                "duckdb": "ok",
                "db_path": str(db_path),
                "events_loaded": n,
                "note": "no tool-name columns in events; nothing to summarize",
            }
        tool_expr = "COALESCE(" + ", ".join(tool_expr_parts) + ")" if len(tool_expr_parts) > 1 else tool_expr_parts[0]

        tool_summary = con.execute(f"""
            SELECT {tool_expr} AS tool, COUNT(*) AS calls
            FROM events
            WHERE {tool_expr} IS NOT NULL
            GROUP BY 1 ORDER BY calls DESC LIMIT 20
        """).fetchall()
        return {
            "duckdb": "ok",
            "db_path": str(db_path),
            "events_loaded": n,
            "columns_seen": sorted(cols),
            "tool_top20": [{"tool": t, "calls": c} for (t, c) in tool_summary],
        }
    except Exception as e:  # noqa: BLE001
        return {"duckdb": "error", "message": str(e)}
    finally:
        con.close()


def render_cross_session_html(summary: dict, duck: dict | None, out_path: pathlib.Path) -> None:
    """Tiny cross-session dashboard (single-file HTML)."""
    sessions_n = summary.get("session_count", 0)
    dur = summary.get("duration_summary", {})
    loops = summary.get("loop_distribution", {})
    loops_str = ", ".join(f"loops={k}: {v}" for k, v in sorted(loops.items()))
    verdicts = summary.get("verdict_counts_by_lens", {})
    agreements = summary.get("agreement_counts_by_lens", {})

    verdict_rows = []
    for lens in sorted(verdicts):
        counts = verdicts[lens]
        verdict_rows.append(
            f"<tr><td>{lens}</td>"
            + "".join(f"<td>{v}: {n}</td>" for v, n in sorted(counts.items()))
            + "</tr>"
        )
    agreement_rows = []
    for lens in sorted(agreements):
        counts = agreements[lens]
        agreement_rows.append(
            f"<tr><td>{lens}</td>"
            + "".join(f"<td>{v}: {n}</td>" for v, n in sorted(counts.items()))
            + "</tr>"
        )
    duck_block = ""
    if duck:
        duck_block = f"<h2>DuckDB</h2><pre>{json.dumps(duck, indent=2)}</pre>"
    else:
        duck_block = "<h2>DuckDB</h2><p><em>Not installed (optional). <code>pip install duckdb</code> to enable cross-session SQL queries.</em></p>"

    style = (
        "body{font-family:-apple-system,system-ui,sans-serif;max-width:1000px;margin:1rem auto;padding:0 1rem;color:#1a1a1a}"
        "h1{font-size:1.4rem}h2{font-size:1.1rem;margin-top:1.5rem;border-bottom:1px solid #ddd;padding-bottom:0.2rem}"
        "table{border-collapse:collapse;width:100%;margin:0.5rem 0;font-size:0.9rem}"
        "td,th{padding:0.3rem 0.5rem;border-bottom:1px solid #eee;text-align:left}"
        "pre{background:#f5f5f7;padding:0.5rem;border-radius:4px;font-size:0.85rem;overflow-x:auto}"
        ".meta{color:#666;font-size:0.85rem}"
    )

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Cross-session diagnostics</title>
<style>{style}</style></head><body>
<h1>Cross-session diagnostics</h1>
<p class="meta">Generated {summary.get('generated_at', '')} from {sessions_n} sessions (including worktrees).</p>

<h2>Duration</h2>
<p>total: {dur.get('total_s', 0)}s · mean: {dur.get('mean_s', '—')}s · median: {dur.get('median_s', '—')}s · max: {dur.get('max_s', '—')}s</p>

<h2>Loop distribution</h2>
<p>{loops_str or '—'}</p>
<p>Loop-cap-reached rate: {summary.get('loop_cap_reached_rate', 0):.1%}</p>

<h2>Verdict counts by lens</h2>
<table>{''.join(verdict_rows) if verdict_rows else '<tr><td><em>none</em></td></tr>'}</table>

<h2>Comparator agreement counts by lens</h2>
<table>{''.join(agreement_rows) if agreement_rows else '<tr><td><em>none</em></td></tr>'}</table>

<h2>Tool error totals</h2>
<pre>{json.dumps(summary.get('tool_error_totals', {}), indent=2)}</pre>

{duck_block}

<details><summary>Full stdlib summary</summary><pre>{json.dumps(summary, indent=2, sort_keys=True)}</pre></details>
</body></html>"""
    out_path.write_text(html)


def main() -> int:
    project_root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
    metrics_dir = project_root / ".claude" / ".metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    session_dirs = discover_session_dirs(project_root)
    sessions: list[dict] = []
    for sd in session_dirs:
        m = load_session_metrics(sd)
        if m:
            sessions.append(m)

    # stdlib aggregation always runs
    summary = stdlib_aggregate(sessions)
    (metrics_dir / "cross-session.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    # DuckDB best-effort
    duck = duckdb_aggregate(project_root, sessions)
    if duck is None:
        # Hint to stderr only — never block.
        try:
            sys.stderr.write(
                "[aggregate-cross-session] DuckDB not installed; SQL cross-cuts skipped. "
                "Install: pip install duckdb\n"
            )
        except OSError:
            pass

    render_cross_session_html(summary, duck, metrics_dir / "cross-session-report.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
