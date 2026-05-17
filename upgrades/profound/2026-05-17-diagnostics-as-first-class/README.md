# Diagnostics as a first-class workflow surface

| Field | Value |
|---|---|
| 📌 **title** | Diagnostics as a first-class workflow surface |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | session-traceable conversation, 2026-05-17 |
| 📅 **created** | 2026-05-17 |
| ⚡ **catalyst** | The 2026-05-16 Opus 4.7 system-card readout session produced a ledger.md by *hand-tally* — the orchestrator counted its own agent calls, artifacts, and decisions from memory. The infrastructure to do this deterministically existed (SessionStart / PostToolUse / Stop hooks → `bin/parse-session-metrics.py` → `diagnostics/metrics.json`) but the orchestrator never wrote the `workflow-id.txt` binding file, so every session orphaned into `.claude/.metrics/orphan/`. The diagnostic surface was *built and unused*. |
| 💡 **essence** | Diagnostics must be deterministic, automated, structured, side-effect-only, and **rendered into a surface the operator actually opens** (HTML, not just JSON). The hand-tally pattern is itself the bug. Bind the workflow-id at step 1 of session-bootstrap; expand the hook surface to capture per-tool latency / per-agent token usage / refusals / errors; align the event schema to OpenTelemetry GenAI semantic conventions so future OTLP export is free; promote critic verdicts and comparator agreement classes to first-class events; render a self-contained HTML report at session-end; aggregate across sessions (and worktrees) via DuckDB-when-available + stdlib-fallback. |
| 🚀 **upgrade** | Six-move migration, landed 2026-05-17. (1) `session-bootstrap` skill writes `workflow-id.txt` at step 4b — fixes the binding defect. (2) `ledger-render` skill rewritten to derive from `metrics.json`; falls back to hand-tally only when binding was skipped (loudly flagged). (3) Four new hooks: `pre-tool-use.sh` (latency pairs), `subagent-stop.sh` (per-agent usage), `session-end.sh` (canonical aggregation hook, replaces per-turn `stop.sh` parser invocation), `post-tool-use-failure.sh` (error events). (4) `events.jsonl` schema migrated to OpenTelemetry `gen_ai.*` field names with app-namespaced extensions (`tool.status`, `agent.outcome`, `workflow.{step,loop}`). (5) Critic agents (6 lenses + comparator) get a structured `Verdict: ... / Confidence: 0.0–1.0` block parsed into `judge_score` events. (6) Self-contained HTML report rendered at session-end into `<session-id>/report.html`. Plus: DuckDB-powered cross-session aggregator at `bin/diagnostics/aggregate-cross-session.py` that walks all worktrees, with stdlib-only fallback when DuckDB is absent. |
| 🏷️ **tags** | diagnostics, observability, hooks, opentelemetry, claude-code, judge-events, calibration, html-report, duckdb, worktree-aware |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-17 | 2026-05-17 | 2026-05-17 | 2026-05-17 | — | 2026-05-17 | — | — | — | — |

## Table of contents

- [The problem](#the-problem)
- [The infrastructure that already existed](#the-infrastructure-that-already-existed)
- [The six moves](#the-six-moves)
- [What is captured now](#what-is-captured-now)
- [Schema](#schema)
- [Worktree behaviour](#worktree-behaviour)
- [DuckDB — optional, opt-in, never blocking](#duckdb--optional-opt-in-never-blocking)
- [What stays out of scope](#what-stays-out-of-scope)
- [Validation](#validation)
- [Falsifier](#falsifier)

## The problem

The 2026-05-16 Opus 4.7 system-card readout session ([.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/)) produced a complete 12-step workflow output — `requirement.md`, `frame.md`, `scope-map.md`, `challenges.md`, six critique files, `synthesis.md`, `ledger.md` — but the ledger numbers were authored by the orchestrator from memory ("classifier (1) + outside-view (1) + ..."). No automated capture. No per-tool duration. No cache hit rate. No refusal-vs-unavailable distinction (the very gap the operations-shadow critic flagged in that session). No way to answer the question "what's the median loop count for safety-flavored sessions in the last 30 days."

The user's response: *"so there is no record of agents recording their metadata?... we need to seriously step up our diagnostic game here."* This R&D entry tracks the response.

## The infrastructure that already existed

The repo already had `.claude/hooks/{session-start,post-tool-use,stop}.sh` writing to `.claude/.metrics/staging/<UUID>/` plus a `bin/parse-session-metrics.py` that read Claude Code's transcript JSONL files (`~/.claude/projects/<project>/<uuid>/...`) to attribute tokens per subagent. The `Stop` hook would move staging into a session directory **if** the orchestrator had written `workflow-id.txt` linking the UUID to the workflow-id — and that one binding step was never documented or implemented in CLAUDE.md or the session-bootstrap skill. Result: every session orphaned, the parser never produced a non-trivial `metrics.json`, and the only existing example metrics.json (`.claude/session-artifacts/2026-05-09-review-diagnostics-impl/diagnostics/metrics.json`) was built specifically for the diagnostics-implementation feature itself.

The infrastructure was 70% in place and 100% unused. This entry brings it across the line and extends it.

## The six moves

| # | Move | Files touched |
|---|---|---|
| 1 | Fix workflow-id binding | [.claude/skills/session-bootstrap/SKILL.md](.claude/skills/session-bootstrap/SKILL.md) |
| 2 | `ledger-render` derives from `metrics.json` | [.claude/skills/ledger-render/SKILL.md](.claude/skills/ledger-render/SKILL.md) |
| 3 | Four new hooks + lighten `stop.sh` | [.claude/hooks/{pre-tool-use,subagent-stop,session-end,post-tool-use-failure}.sh](.claude/hooks/), [.claude/hooks/{session-start,post-tool-use,stop}.sh](.claude/hooks/) (refactor), [.claude/settings.json](.claude/settings.json) |
| 4 | OpenTelemetry `gen_ai.*` schema upgrade | All hooks (emit new format); [bin/diagnostics/aggregate-session.py](bin/diagnostics/aggregate-session.py) (handles both old + new) |
| 5 | Critic `Verdict:` + `Confidence:` contract | All 6 critic agents + [.claude/agents/critic-comparator.md](.claude/agents/critic-comparator.md) |
| 6 | Self-contained HTML report per session | [bin/diagnostics/render-html-report.py](bin/diagnostics/render-html-report.py), wired into `session-end.sh` |
| + | Cross-session DuckDB aggregator | [bin/diagnostics/aggregate-cross-session.py](bin/diagnostics/aggregate-cross-session.py) |

## What is captured now

Per session, the SessionEnd hook produces:

- **`<session-id>/diagnostics/events.jsonl`** — OpenTelemetry-aligned per-event log: `tool_start`, `tool_end`, `tool_error`, `agent_end`, `turn_end`, `session_start`. Fields: `gen_ai.tool.name`, `gen_ai.tool.call.id`, `gen_ai.agent.id`, `gen_ai.agent.name`, `tool.status`, `error.type`, `error.message`, plus nanosecond timestamps.
- **`<session-id>/diagnostics/metrics.json`** — aggregated per-session view: per-agent tokens (input / output / cache_read / cache_creation / calls), per-tool counts + p50/p95/max/total latency, error totals, models seen (response_models for drift detection), per-lens verdicts + confidence, comparator agreement classes, loop count, decision count, artifact count, duration.
- **`<session-id>/diagnostics/start.ts`**, **`end.ts`** — Unix-time bookends.
- **`<session-id>/report.html`** — self-contained HTML report, single file, no external assets, browser-openable offline.
- **`<session-id>/ledger.md`** — now a derived view of `metrics.json` (Path A) rather than a hand-tally (Path B — flagged as workflow defect when triggered).

Across sessions (run on demand by the user, or by SessionEnd as a backgrounded task):

- **`.claude/.metrics/cross-session.json`** — stdlib-only summary: loop distribution, verdict counts by lens, comparator agreement counts by lens, token totals by agent, tool error totals, duration distribution.
- **`.claude/.metrics/cross-session.duckdb`** — DuckDB-backed columnar query layer (only if `pip install duckdb` is present; the workflow never depends on this).
- **`.claude/.metrics/cross-session-report.html`** — dashboard rendering of the same.

## Schema

The events.jsonl event envelope (post-migration):

```json
{
  "ts_ns": 1747443163123456789,
  "event": "tool_start | tool_end | tool_error | agent_end | turn_end | session_start",
  "session_id": "uuid",
  "gen_ai.operation.name": "execute_tool | invoke_agent",
  "gen_ai.tool.name": "Read",
  "gen_ai.tool.call.id": "toolu_...",
  "gen_ai.agent.id": "...",
  "gen_ai.agent.name": "critic-architecture",
  "tool.status": "ok | error | timeout",
  "_err": {"error.type": "...", "error.message": "..."},
  "_usage": {"gen_ai.usage.input_tokens": 12034, "gen_ai.usage.output_tokens": 891, "gen_ai.usage.cache_read.input_tokens": 10500, "gen_ai.usage.cache_creation.input_tokens": 0, "duration_ms": 1430}
}
```

Field names align to the OpenTelemetry GenAI Special Interest Group's `gen_ai.*` semantic conventions ([opentelemetry.io/docs/specs/semconv/gen-ai/](https://opentelemetry.io/docs/specs/semconv/gen-ai/)). When Anthropic's native `CLAUDE_CODE_ENABLE_TELEMETRY=1` exporter is eventually flipped on, the OTLP spans will speak the same field names — no rename migration, just a field-map.

App-namespaced extensions (`tool.status`, `agent.outcome`, `workflow.{step,loop}`, `prompt.template.sha`, `judge.confidence`) cover what the OTel spec demurs on. They are explicitly separated from the OTel surface so future spec adoption doesn't collide.

## Worktree behaviour

The cross-session aggregator discovers worktrees via `git worktree list --porcelain` and globs each one's `.claude/session-artifacts/` independently. A session running in `worktrees/foo/` writes its own `events.jsonl` into `worktrees/foo/.claude/session-artifacts/<id>/diagnostics/`; the aggregator's discovery finds all of them in a single pass.

This is the load-bearing property for the user's planned **"10 upgrades in worktrees at the same time"** workflow: each worktree's hook chain operates on its own staging dir (keyed by Claude session UUID, which is per-Claude-Code-instance, so no collisions), each worktree produces its own per-session diagnostics, and the cross-session view stitches them all together when invoked.

## DuckDB — optional, opt-in, never blocking

The cross-session aggregator probes for `duckdb` at startup:

```python
try:
    import duckdb
except ImportError:
    sys.stderr.write("[aggregate-cross-session] DuckDB not installed; SQL cross-cuts skipped. Install: pip install duckdb\n")
    # ...continues with stdlib aggregation
```

Without DuckDB, the script still produces `cross-session.json` and `cross-session-report.html` from pure stdlib aggregation. The DuckDB layer is purely a convenience for ad-hoc SQL queries against `events.jsonl` files across sessions. **No part of the workflow capture or per-session diagnostics path depends on DuckDB.** If a collaborator clones this repo and never installs it, every session still produces full diagnostics; they just can't run cross-session SQL.

## What stays out of scope

- **OTLP backend (Grafana / Tempo / Honeycomb).** No external service. Field names are OTel-compatible so flipping the switch later is one env-var change.
- **Daemon-based aggregation (the Agent-Monitor pattern).** Adds operational complexity for a single-developer stack. JSONL append + DuckDB-on-demand is the right shape at this scale.
- **Wrapping the Claude binary (claude-trace pattern).** Brittle vector; broke once with native installs (lemmy issue #48). Native hooks + OTel-compatible field names get the same data without binary patching.

## Validation

Smoke tests at landing time:

- `python3 bin/diagnostics/aggregate-session.py 2026-05-09-review-diagnostics-impl junk-uuid` → exit 0, produces metrics.json with `events.schema_version = "legacy-ts-tool"`, counts.artifacts and counts.decisions populated.
- `python3 bin/diagnostics/render-html-report.py 2026-05-09-review-diagnostics-impl` → exit 0, produces `report.html` (5.5 KB) with KPIs, token table, tool table, verdict table.
- `python3 bin/diagnostics/aggregate-cross-session.py` (without DuckDB installed) → exit 0, produces `cross-session.json` + `cross-session-report.html`, stderr hint to install DuckDB.
- Same command (with DuckDB) → exit 0, produces additional `cross-session.duckdb` (~500 KB), report includes DuckDB block with `events_loaded` and `tool_top20`.

End-to-end validation requires a fresh session that actually exercises the binding step at session-bootstrap step 4b — pending.

## Falsifier

This R&D entry is **retired** if:
- Anthropic ships native subagent / workflow diagnostics that supersede this (would absorb Moves 3-6 into upstream tooling).
- The OpenTelemetry GenAI semantic conventions land a final / stable spec that materially diverges from the current 2026-05 draft — would require schema migration.
- A future session demonstrates that hand-tally is sufficient and the binding-step ergonomics aren't worth the schema surface — unlikely given the user's stated need for parallel-worktree diagnostics, but recorded here for honesty.

## Related session artifacts

- Catalyst: [.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/ledger.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/ledger.md) (the hand-tally that triggered this R&D entry)
- Research (4-agent parallel pass, 2026-05-17): Claude Code native telemetry, OpenTelemetry GenAI semconv, multi-agent critic-panel metrics literature (Petri, Apollo, IAPS), GitHub patterns survey
