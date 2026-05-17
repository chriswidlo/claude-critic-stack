#!/usr/bin/env python3
"""render-html-report.py — self-contained HTML report per session.

Pure-stdlib renderer. Reads diagnostics/metrics.json (and optionally
events.jsonl for the event timeline) and writes a single self-contained
report.html into the session directory.

No external CSS/JS, no fonts, no images — single file, browser-openable
offline, copy-pasteable to a viewer.

Runs from session-end.sh after aggregate-session.py.

Usage:
    render-html-report.py <workflow-id> [project-root]
"""
from __future__ import annotations

import html
import json
import os
import pathlib
import sys
from datetime import datetime


CSS = """
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
       max-width: 1100px; margin: 1rem auto; padding: 0 1rem; color: #1a1a1a; line-height: 1.5; }
h1 { font-size: 1.6rem; margin: 0.5rem 0 0.2rem; }
h2 { font-size: 1.2rem; margin: 1.8rem 0 0.4rem; padding-bottom: 0.2rem; border-bottom: 1px solid #ddd; }
h3 { font-size: 1.0rem; margin: 1.2rem 0 0.3rem; color: #555; }
.meta { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 0.5rem; margin: 1rem 0; }
.kpi { padding: 0.7rem 0.9rem; background: #f5f5f7; border-radius: 6px; border-left: 3px solid #4a90e2; }
.kpi-label { color: #666; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-value { font-size: 1.3rem; font-weight: 600; margin-top: 0.1rem; }
.kpi-warn { border-left-color: #d97706; background: #fef3c7; }
.kpi-good { border-left-color: #059669; }
.kpi-bad  { border-left-color: #dc2626; background: #fee2e2; }
table { width: 100%; border-collapse: collapse; margin: 0.4rem 0 1rem; font-size: 0.9rem; }
th, td { padding: 0.35rem 0.55rem; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f5f5f7; font-weight: 600; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
.verdict-approve { color: #059669; font-weight: 600; }
.verdict-rework  { color: #d97706; font-weight: 600; }
.verdict-reject  { color: #dc2626; font-weight: 600; }
.verdict-refused { color: #6b21a8; font-weight: 600; }
.verdict-unavailable { color: #6b7280; font-style: italic; }
.agree { color: #059669; }
.partial-agree { color: #d97706; }
.disagree { color: #dc2626; }
.unavailable { color: #6b7280; font-style: italic; }
details { margin: 0.5rem 0; }
summary { cursor: pointer; padding: 0.3rem 0; font-weight: 500; color: #444; }
pre { background: #f5f5f7; padding: 0.7rem; border-radius: 4px; overflow-x: auto; font-size: 0.85rem; }
.footer { color: #999; font-size: 0.8rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; }
"""


def kpi(label: str, value: str, kind: str = "") -> str:
    cls = f"kpi {kind}" if kind else "kpi"
    return f'<div class="{cls}"><div class="kpi-label">{html.escape(label)}</div><div class="kpi-value">{html.escape(value)}</div></div>'


def format_duration(seconds: int | None) -> str:
    if seconds is None:
        return "—"
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    h = seconds // 3600
    m = (seconds % 3600) // 60
    return f"{h}h {m}m"


def format_int(n: int) -> str:
    return f"{n:,}"


def render_token_table(by_agent: dict) -> str:
    if not by_agent:
        return "<p><em>No token data.</em></p>"
    rows = []
    for agent, vals in sorted(by_agent.items(), key=lambda kv: -(kv[1].get("input", 0) + kv[1].get("output", 0))):
        inp = vals.get("input", 0)
        out = vals.get("output", 0)
        cache_r = vals.get("cache_read", 0)
        cache_c = vals.get("cache_creation", 0)
        calls = vals.get("calls", 0)
        total = inp + out
        cache_hit_pct = (cache_r / (cache_r + inp) * 100) if (cache_r + inp) > 0 else 0
        rows.append(
            f"<tr><td>{html.escape(agent)}</td>"
            f"<td class='num'>{calls}</td>"
            f"<td class='num'>{format_int(inp)}</td>"
            f"<td class='num'>{format_int(out)}</td>"
            f"<td class='num'>{format_int(cache_r)}</td>"
            f"<td class='num'>{format_int(cache_c)}</td>"
            f"<td class='num'>{cache_hit_pct:.1f}%</td>"
            f"<td class='num'>{format_int(total)}</td></tr>"
        )
    return (
        "<table><thead><tr>"
        "<th>Agent</th><th>Calls</th><th>Input</th><th>Output</th>"
        "<th>Cache read</th><th>Cache create</th><th>Cache hit</th><th>Total</th>"
        "</tr></thead><tbody>"
        + "".join(rows) + "</tbody></table>"
    )


def render_tool_table(tool_counts: dict, latency_summary: dict, errors_by_tool: dict) -> str:
    if not tool_counts:
        return "<p><em>No tool call data.</em></p>"
    rows = []
    for tool, count in sorted(tool_counts.items(), key=lambda kv: -kv[1]):
        lat = latency_summary.get(tool, {})
        errors = errors_by_tool.get(tool, 0)
        err_cell = f"<td class='num'>{errors}</td>" if errors else "<td class='num' style='color:#999'>0</td>"
        if lat:
            rows.append(
                f"<tr><td>{html.escape(tool)}</td>"
                f"<td class='num'>{count}</td>"
                f"<td class='num'>{lat.get('p50_ms', '—')}</td>"
                f"<td class='num'>{lat.get('p95_ms', '—')}</td>"
                f"<td class='num'>{lat.get('max_ms', '—')}</td>"
                f"<td class='num'>{lat.get('total_ms', '—')}</td>"
                f"{err_cell}</tr>"
            )
        else:
            rows.append(
                f"<tr><td>{html.escape(tool)}</td>"
                f"<td class='num'>{count}</td>"
                f"<td colspan='4' class='num' style='color:#999'>—</td>"
                f"{err_cell}</tr>"
            )
    return (
        "<table><thead><tr>"
        "<th>Tool</th><th>Calls</th>"
        "<th>p50 ms</th><th>p95 ms</th><th>max ms</th><th>total ms</th><th>Errors</th>"
        "</tr></thead><tbody>"
        + "".join(rows) + "</tbody></table>"
    )


def render_verdicts(opus_verdicts: dict, shadow_verdicts: dict, comparator: dict) -> str:
    lenses = set(opus_verdicts.keys()) | set(shadow_verdicts.keys()) | set(comparator.keys())
    if not lenses:
        return "<p><em>No critic-panel verdicts recorded for this session.</em></p>"
    rows = []
    for lens in sorted(lenses):
        opus = opus_verdicts.get(lens, {})
        shadow = shadow_verdicts.get(lens, {})
        agree = comparator.get(lens, "—")
        opus_v = opus.get("verdict", "—")
        opus_conf = opus.get("confidence")
        shadow_v = shadow.get("verdict", "—")
        shadow_conf = shadow.get("confidence")
        opus_cell = f"<span class='verdict-{opus_v}'>{html.escape(opus_v)}</span>"
        if opus_conf is not None:
            opus_cell += f" <span style='color:#999'>({opus_conf:.2f})</span>"
        shadow_cell = f"<span class='verdict-{shadow_v}'>{html.escape(shadow_v)}</span>"
        if shadow_conf is not None:
            shadow_cell += f" <span style='color:#999'>({shadow_conf:.2f})</span>"
        agree_cell = f"<span class='{agree}'>{html.escape(agree)}</span>" if agree != "—" else "—"
        rows.append(
            f"<tr><td>{html.escape(lens)}</td>"
            f"<td>{opus_cell}</td><td>{shadow_cell}</td><td>{agree_cell}</td></tr>"
        )
    return (
        "<table><thead><tr>"
        "<th>Lens</th><th>Opus verdict</th><th>Sonnet shadow verdict</th><th>Comparator agreement</th>"
        "</tr></thead><tbody>"
        + "".join(rows) + "</tbody></table>"
    )


def render_html(workflow_id: str, metrics: dict) -> str:
    duration = metrics.get("duration_seconds")
    tokens = metrics.get("tokens", {})
    total_tokens = tokens.get("total", {})
    by_agent = tokens.get("by_agent", {})
    tool_calls = metrics.get("tool_calls", {})
    events = metrics.get("events", {})
    counts = metrics.get("counts", {})
    loops = metrics.get("loops", 0)
    verdicts = metrics.get("verdicts", {})
    shadow_verdicts = metrics.get("shadow_verdicts", {})
    comparator_agreements = metrics.get("comparator_agreements", {})
    models = metrics.get("models_seen", {})

    total_input = total_tokens.get("input", 0)
    total_output = total_tokens.get("output", 0)
    total_cache_read = total_tokens.get("cache_read", 0)
    total_cache_create = total_tokens.get("cache_creation", 0)
    cache_hit_pct = (total_cache_read / (total_cache_read + total_input) * 100) if (total_cache_read + total_input) > 0 else 0

    loop_kind = "kpi-bad" if loops >= 2 else ("kpi-warn" if loops == 1 else "kpi-good")

    kpi_html = "".join([
        kpi("Duration", format_duration(duration)),
        kpi("Loops", f"{loops}/2", loop_kind),
        kpi("Total input tokens", format_int(total_input)),
        kpi("Total output tokens", format_int(total_output)),
        kpi("Cache hit", f"{cache_hit_pct:.1f}%", "kpi-good" if cache_hit_pct > 50 else ""),
        kpi("Artifacts", str(counts.get("artifacts", "—"))),
        kpi("Decisions", str(counts.get("decisions", "—"))),
        kpi("Tool calls", str(tool_calls.get("total", "—"))),
    ])

    models_str = ", ".join(f"{m}×{c}" for m, c in sorted(models.items(), key=lambda kv: -kv[1])) if models else "—"

    raw_metrics_pretty = html.escape(json.dumps(metrics, indent=2, sort_keys=True))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Session report — {html.escape(workflow_id)}</title>
<style>{CSS}</style>
</head>
<body>
<h1>{html.escape(workflow_id)}</h1>
<div class="meta">
  Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ·
  Schema version: <code>{html.escape(metrics.get('schema', '—'))}</code> ·
  Event schema: <code>{html.escape(events.get('schema_version', '—'))}</code>
</div>

<div class="kpi-grid">{kpi_html}</div>

<h2>Tokens by agent</h2>
{render_token_table(by_agent)}

<h2>Tool calls</h2>
{render_tool_table(tool_calls.get('by_type', {}), events.get('latency_summary', {}), events.get('errors_by_tool', {}))}

<h2>Critic panel verdicts</h2>
{render_verdicts(verdicts, shadow_verdicts, comparator_agreements)}

<h3>Models seen (response models)</h3>
<p style="font-family: monospace; font-size: 0.85rem;">{html.escape(models_str)}</p>

<h3>Error summary</h3>
{f"<p>{sum(events.get('error_types', {}).values())} errors recorded across {len(events.get('errors_by_tool', {}))} tools.</p>" if events.get('errors_by_tool') else "<p><em>No tool errors recorded.</em></p>"}

<details>
<summary>Raw metrics.json</summary>
<pre>{raw_metrics_pretty}</pre>
</details>

<div class="footer">
Rendered by <code>bin/diagnostics/render-html-report.py</code> · session-end hook ·
data from <code>diagnostics/metrics.json</code> + <code>diagnostics/events.jsonl</code>
</div>
</body>
</html>
"""


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <workflow-id> [project-root]", file=sys.stderr)
        return 2
    workflow_id = sys.argv[1]
    project_root = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else os.getcwd())

    session_dir = project_root / ".claude" / "session-artifacts" / workflow_id
    metrics_path = session_dir / "diagnostics" / "metrics.json"
    if not metrics_path.is_file():
        # No metrics — silently skip (session-end may have run before aggregate-session)
        return 0
    try:
        metrics = json.loads(metrics_path.read_text())
    except (OSError, json.JSONDecodeError):
        return 1

    html_out = render_html(workflow_id, metrics)
    report_path = session_dir / "report.html"
    try:
        report_path.write_text(html_out)
    except OSError:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
