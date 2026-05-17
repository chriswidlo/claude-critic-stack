# OTel real sink — wire when a backend is chosen

| Field | Value |
|---|---|
| 📌 **title** | OTel real sink — wire when a backend is chosen |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-17 |
| ⚡ **catalyst** | V2 research §1.9 + §2 top-20 #16 recommend `CLAUDE_CODE_ENABLE_TELEMETRY=1` with OTel export for cost / latency / cache-hit-rate per session. The flag is now on in [.claude/settings.json](.claude/settings.json), but both exporters are set to `none` — Claude Code's OTel pipeline initializes and emits nothing. The reason: OTel's design requires a receiver process listening on a port; for solo-on-one-laptop use, that process is a babysitting cost without a payoff. The existing diagnostics pipeline ([bin/diagnostics/aggregate-session.py](bin/diagnostics/aggregate-session.py) + the 7 hooks under [.claude/hooks/](.claude/hooks/)) already captures per-session tool/agent/cost/latency data in our own schema. Adding OTel today would mean a second telemetry stream nobody reads. |
| 💡 **essence** | Defer the OTel sink wiring until one of three triggers fires: (a) a hosted backend is chosen (Honeycomb / Grafana Cloud / etc. — direct OTLP push, no local collector needed), (b) the operator runs ≥3 sessions in parallel and the per-session-file diagnostics view becomes harder to navigate than a unified dashboard, or (c) cross-session metrics from [bin/diagnostics/aggregate-cross-session.py](bin/diagnostics/aggregate-cross-session.py) outgrow what `metrics.json` rollups can carry. The flag stays warm so the eventual flip is a settings-only change. |
| 🚀 **upgrade** | When a backend lands, flip `OTEL_*_EXPORTER` from `none` to `otlp`, set `OTEL_EXPORTER_OTLP_ENDPOINT` to the backend's URL, add auth headers — typically a 5-minute settings.json edit, no code change. The OTel pipeline starts emitting standard GenAI-conventions metrics + logs immediately. Until that day, the diagnostics pipeline we already shipped is the actual telemetry: per-session `events.jsonl`, `metrics.json`, `report.html`. **Fails to safe:** if the trigger never fires, the stack runs exactly as it does today, with `bin/diagnostics/` carrying the telemetry weight. |
| 🏷️ **tags** | telemetry, otel, observability, deferred, scaffolding |
| 🔗 **relates_to** | 2026-05-17-diagnostics-as-first-class |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-05-17 | — | — | — | — | — | — | — |

## Why this is deferred, not skipped

The V2 research is right that OTel matters at scale. The specific reasoning behind deferring:

1. **OTel is push-based with no built-in file sink.** Claude Code supports `otlp` (network), `prometheus` (network pull), `console` (stderr), `none`. There is no `file` exporter in the emitter. Storage requires a separate receiver process.
2. **The receiver has to be running.** If the process dies between sessions and you don't notice, events drop silently. For solo use that's a non-trivial babysitting cost.
3. **Our diagnostics pipeline covers the same data in our own schema.** Tool calls, agent invocations, latencies, errors, verdicts, loop counts — all on disk via [.claude/hooks/](.claude/hooks/) + [bin/diagnostics/](bin/diagnostics/). Schema is ours, not OTel's, but the *coverage* is equivalent for our queries.
4. **Hosted backends solve the receiver problem.** Honeycomb / Grafana Cloud / Uptrace all expose a direct OTLP endpoint with auth. When we pick one, we skip the local-collector step entirely. That's the natural "switch on OTel" moment.

## What's already in place

- `CLAUDE_CODE_ENABLE_TELEMETRY=1` set in [.claude/settings.json](.claude/settings.json) — the master flag is on, so the OTel pipeline initializes; only the sinks are `none`.
- Exporters explicitly set to `none` rather than left unset — makes the deferral visible to anyone reading the settings.

## What flips when a trigger fires

```jsonc
// .claude/settings.json env block — current
"OTEL_METRICS_EXPORTER": "none",
"OTEL_LOGS_EXPORTER": "none",

// .claude/settings.json env block — when backend chosen
"OTEL_METRICS_EXPORTER": "otlp",
"OTEL_LOGS_EXPORTER": "otlp",
"OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
"OTEL_EXPORTER_OTLP_ENDPOINT": "https://<backend>/v1/otlp",
"OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer <token>"
```

No agent edits, no hook edits, no code changes. The deferral is structurally invertible.

## What was considered and rejected

Two cheaper-but-fiddlier paths were considered:

- **20-line Python OTLP sink.** A stdlib `http.server` script catching POST bodies into a file. Works, but introduces a process to babysit; if it dies, events drop. Rejected because the diagnostics pipeline already produces equivalent data with no extra process.
- **Hook-level OTel-format emission.** Modify our existing hooks to ALSO write OTel-schema JSON alongside `events.jsonl`. Doable in ~2 hours, but doubles the schema surface for no near-term consumer. Rejected for the same reason.

Both options remain on the table if conditions change.

## Trigger conditions (open this entry again when)

- A specific backend has been chosen (name it in `upgrade` field above when known).
- The operator finds themselves running cross-session rollups frequently enough that a hosted dashboard would be cheaper than the file-walking loop in `bin/diagnostics/aggregate-cross-session.py`.
- Parallel-worktree runs land (separately filed under V1 §1.3 work) and per-session-file diagnostics become navigation-heavy.

## Open questions

- Which backend? Grafana Cloud free tier (50GB/mo) vs Honeycomb free tier (20M events/mo) vs Uptrace vs self-hosted Jaeger. Decision-cost is real but small once we know we want OTel ingestion at all.
- If we go OTel: do we deprecate the diagnostics pipeline, run both in parallel, or convert one to feed the other? Not answered today; will surface when the trigger fires.
