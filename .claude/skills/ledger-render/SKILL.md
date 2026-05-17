---
name: ledger-render
description: Compute and write the workflow-cost ledger.md for a 13-step session in claude-critic-stack. Derives counts and ratios from diagnostics/metrics.json (the deterministic source produced by the SessionEnd hook), evaluates threshold warnings per the load-bearing schema in .claude/session-artifacts/README.md, and emits the synthesis citation line. Falls back to hand-tally only when metrics.json is missing (which is a workflow defect — the binding step in session-bootstrap was skipped). Use at step 13 — after synthesis.md is otherwise complete. SKIP for quick-take invocations and pure factual questions answered by canon-librarian.
argument-hint: <session-id — e.g. 2026-05-07-some-slug>
allowed-tools: Bash(find:*) Bash(grep:*) Bash(wc:*) Bash(ls:*) Bash(cat:*) Bash(python3:*) Read Write
---

You are the ledger renderer for the 13-step workflow. The user (or orchestrator) has invoked `/ledger-render` with a session id. Your job is to compute the ledger from the on-disk session state and write `ledger.md` per the load-bearing schema.

**Primacy rule.** `diagnostics/metrics.json` is the deterministic, machine-generated source of truth produced by the SessionEnd hook. If it exists, you derive everything from it — no hand-tally, no interpretation. The hand-tally path below exists only as a fallback for sessions where the binding step in [.claude/skills/session-bootstrap/SKILL.md](.claude/skills/session-bootstrap/SKILL.md) was skipped (a workflow defect that must be flagged loudly in `## Notes`).

The session id: $ARGUMENTS

(If `$ARGUMENTS` is empty, list current session directories under [.claude/session-artifacts/](.claude/session-artifacts/) and ask which one to render.)

## Your task

1. **Read the schema.** Read [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md), specifically the *Ledger schema (load-bearing)* section. Threshold values may have been retuned; trust the README, not memory.

2. **Confirm session exists and is non-bypassed.**
   - `ls .claude/session-artifacts/<session-id>/` — fail with a clear error if missing.
   - Bypass check: if the session has only `question.md` + a single direct answer (no `requirement.md`, no `synthesis.md`), it is a `quick take` or pure-factual session and **must not** get a ledger. Report and stop.
   - If `synthesis.md` is missing, the session is incomplete; render a `decisions = 0`, `ratios = N/A` ledger per the schema's veto-stopped clause and note the incompleteness.

3. **Choose the source-of-truth path.**

   - **Path A — `diagnostics/metrics.json` exists.** Read it. All counts come from it. Skip step 4's hand-tally entirely. Proceed to step 5.

   - **Path B — `diagnostics/metrics.json` is missing.** The diagnostics pipeline was not bound (the SessionStart→workflow-id→Stop chain produced no metrics.json). This is a **workflow defect**: the `session-bootstrap` skill's step 4b binding either was not run or failed silently. Fall back to hand-tally per step 4 below. Render a loud warning in `## Notes` naming the defect and the remediation (re-run a future session through `session-bootstrap` after verifying `.claude/.metrics/current-session-uuid` exists).

4. **(Path B only — fallback hand-tally.)**

   - **Agent calls.** Count manually:
     - 1 for `requirement-classifier` (always, on non-bypassed).
     - 1 for `outside-view` (if `distillations/outside-view.md` exists).
     - 1 for `canon-librarian` (if `distillations/canon-librarian.md` exists).
     - 1 per zone-reader (count `distillations/zone-*.md`).
     - 1 per distiller invocation (one per non-`zone-` distillation file: outside-view, canon-librarian).
     - 1 for `scope-mapper` (if `scope-map.md` exists).
     - 1 for `frame-challenger` (if `challenges.md` exists).
     - 3 per critic-panel loop (architecture + operations + product). +3 each if `SHADOW_PANEL=1` ran (look for `critiques/<lens>.shadow.md`). +1 for `critic-comparator` per shadow run.
     - Loops are recorded in `decision-log.md`; multiply the per-loop count.

     Show your math in the ledger's `## Counts` table cell in the same style as [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md) ("classifier (1) + outside-view (1) + ..."). **Mark the row `source: hand-tally (metrics.json missing — workflow defect)`.**

   - **Artifacts.** Run literally:
     ```
     find .claude/session-artifacts/<session-id> -name '*.md' -not -name 'ledger.md' | wc -l
     ```

   - **Loops used.** Read `decision-log.md`. Look for an explicit `Loops used: N/2` line or count `## Loop N` entries.

   - **Loop cap reached.** `true` iff loops used == 2.

   - **Decisions.** Open `synthesis.md`. Count bulleted items under `## Recommendation`, `## Post-critique recommendation`, or `## Uncertainties` (or the equivalent CLAUDE.md step-12 heading). If `synthesis.md` is missing, decisions = 0.

5. **(Path A — derive from metrics.json.)**

   - **Agent calls** = `metrics.json` → sum of `tokens.by_agent[*].calls` for non-`main` entries, plus the per-loop critic-panel count from `loops` (the parser may not yet record critic invocations as Agent calls if they were direct subagent transcripts; fall back to `tool_calls.by_type.Agent` if non-zero).
   - **Artifacts** = `metrics.json` → if a `counts.artifacts` field exists (newer parser), use it; otherwise run the `find ... wc -l` command as in Path B and document the source.
   - **Loops used** = `metrics.json.loops`.
   - **Loop cap reached** = `loops == 2`.
   - **Decisions** = `metrics.json` → if a `counts.decisions` field exists (newer parser), use it; otherwise count manually from `synthesis.md` and document the source.
   - **Mark each row with `source: metrics.json` (or `source: derived` when computed at render time).**

6. **Derive ratios.** Per the schema:
   - Agent-calls per decision = `<agent-calls> / <decisions>`. If decisions = 0, render `N/A`.
   - Artifacts per decision = `<artifacts> / <decisions>`. If decisions = 0, render `N/A`.
   - Loops to convergence = `<loops>/2`.

7. **Evaluate warnings.** Per the schema:
   - `agent-calls / decisions > 10` → ⚠️ "consider whether the workflow produced more analysis than action"
   - `artifacts / decisions > 8` → ⚠️ "consider whether documentation is exceeding decisions"
   - loop cap reached → ⚠️ "candidate needed maximum rework; first-pass framing was off"
   - **metrics.json missing → ⚠️ "diagnostics pipeline was not bound — workflow defect; see step 4b of session-bootstrap"** (Path B only)
   - Zero warnings → render the literal line `warnings: none`.

8. **Write `ledger.md`.** Paste the schema's template, fill it. Use the four load-bearing headings exactly: `## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`. Do not rename, reorder, or merge them.

9. **Append the synthesis citation line.**
   - Read `synthesis.md`'s last line.
   - The required form is exactly: `Ledger: agent-calls=<N>, artifacts=<N>, loops=<N>/2; warnings: <list or "none">.`
   - If absent, append it. If present but stale (numbers don't match what you computed), update it.
   - **Edit `synthesis.md`'s final line; do not rewrite the whole file.**

10. **Append the `## Metrics` block (Path A only — additive).**
    - Read `diagnostics/metrics.json` and append a `## Metrics` block to `ledger.md` *after* `## Notes`. The block is YAML inside a fenced code block.
    - Path B: silently skip (the metrics.json is missing by definition).
    - The block preserves keys: `duration_seconds`, `tokens.{total, by_agent, source}`, `tool_calls.{total, by_type}`, `verdicts`, `loops`, plus any newer fields the parser added (`judge_scores`, `refusals`, etc. once Move 5 lands). Use `python3 -c "import json,yaml,sys; print(yaml.safe_dump(json.load(sys.stdin), default_flow_style=False))"` if PyYAML is available; otherwise a stable key:value dump.
    - The block heading must be exactly `## Metrics` (additive, not load-bearing — older renders without it remain valid).

11. **Report back.** In under 100 words:
    - The session id and ledger path you wrote (repo-root-relative markdown link).
    - **Which path you took** (A: metrics.json derived; B: hand-tally fallback).
    - A one-line summary: counts, ratios, warning count.
    - If a warning fired, name which one and a single sentence on what it means.
    - If `synthesis.md` was updated, say so explicitly.
    - If a `## Metrics` block was appended, mention duration and the largest token-by-agent in one sentence.

## Constraints

- **Counts are taken just before `ledger.md` is written. `ledger.md` does not count itself.**
- **Path A is the default. Path B is a defect-recovery mode.** Never silently fall back to hand-tally; always flag it loudly in `## Notes` and `## Warnings` so future sessions don't inherit the defect.
- **Do not invent threshold values.** Trust the README at read time.
- **Do not write a ledger for a bypassed session.** Quick-take and pure-factual sessions get no ledger.
- **Do not modify `decision-log.md` or any other session artifact** beyond `ledger.md` and the final line of `synthesis.md`.
- **Do not anchor on a remembered ratio threshold.** Schema may legitimately move.

## When the session state is incomplete

- **No `synthesis.md`:** veto-stopped session. Render with `decisions = 0`, ratios = `N/A`, note in `## Notes`. Do not refuse to render.
- **No `decision-log.md`:** loops used = 0. Note this; do not error.
- **No `distillations/` directory:** subagent gathering was skipped. Confirm bypass status with the user before rendering.
- **No `diagnostics/metrics.json`:** Path B fallback per step 3 — flag as workflow defect, run hand-tally.
- **Non-standard heading names in `synthesis.md`:** read [CLAUDE.md](CLAUDE.md) step 12 for canonical heading text; count what looks like the equivalent and note the deviation in `## Notes`.
