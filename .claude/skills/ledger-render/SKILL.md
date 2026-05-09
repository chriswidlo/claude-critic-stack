---
name: ledger-render
description: Compute and write the workflow-cost ledger.md for a 12-step session in claude-critic-stack. Counts artifacts, parses decision-log.md for loop count, derives ratios, evaluates threshold warnings per the load-bearing schema in .claude/session-artifacts/README.md, and emits the synthesis citation line. Use at step 13 — after synthesis.md is otherwise complete and before the orchestrator commits the session. SKIP for quick-take invocations and pure factual questions answered by canon-librarian (per the schema's bypass section).
argument-hint: <session-id — e.g. 2026-05-07-some-slug>
allowed-tools: Bash(find:*) Bash(grep:*) Bash(wc:*) Bash(ls:*) Bash(cat:*) Bash(python3:*) Read Write
---

You are the ledger renderer for the 12-step workflow. The user (or orchestrator) has invoked `/ledger-render` with a session id. Your job is to compute the ledger from the on-disk session state and write `ledger.md` per the load-bearing schema.

The session id: $ARGUMENTS

(If `$ARGUMENTS` is empty, list current session directories under [.claude/session-artifacts/](.claude/session-artifacts/) and ask which one to render.)

## Your task

1. **Read the schema.** Read [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md), specifically the *Ledger schema (load-bearing)* section. Reread it every time — it is the single source of truth, and threshold values may have been retuned. Do not paraphrase from memory.

2. **Confirm session exists and is non-bypassed.**
   - `ls .claude/session-artifacts/<session-id>/` — fail with a clear error if missing.
   - Bypass check: if the session has only `question.md` + a single direct answer (no `requirement.md`, no `synthesis.md`), it is likely a `quick take` or pure-factual session and **must not** get a ledger. Report this and stop.
   - If `synthesis.md` is missing, the session is incomplete; render a `decisions = 0`, `ratios = N/A` ledger per the schema's veto-stopped clause and note the incompleteness.

3. **Count.** Use the schema's source-of-truth commands literally — do not invent shortcuts.

   - **Agent calls.** There is no one-line counter; count manually:
     - 1 for `requirement-classifier` (always, on non-bypassed).
     - 1 for `outside-view`.
     - 1 for `canon-librarian`.
     - 1 for `Explore` if and only if `distillations/explore.md` exists.
     - 1 per file under `distillations/` (each subagent that ran got distilled).
     - 1 for `scope-mapper` (if `scope-map.md` exists).
     - 1 for `frame-challenger` (if `challenges.md` exists).
     - 3 per critic-panel loop (architecture + operations + product). +3 each if `SHADOW_PANEL=1` ran (look for `critiques/<lens>.shadow.md`). +1 for `critic-comparator` per shadow run.
     - Loops are recorded in `decision-log.md`; multiply the per-loop count.

     Show your math in the ledger's `## Counts` table cell, in the same style as [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md) ("classifier (1) + outside-view (1) + ...").

   - **Artifacts.** Run literally:
     ```
     find .claude/session-artifacts/<session-id> -name '*.md' -not -name 'ledger.md' | wc -l
     ```
     Report the number. Do not exclude any other file pattern; subdirectories like `distillations/` and `critiques/` count, per the schema.

   - **Loops used.** Read `decision-log.md`. Look for the line `Loops used: N/2` or count entries that begin `## Loop N`. Take whichever is explicitly written; if both exist and disagree, prefer the explicit summary line and note the discrepancy in `## Notes`.

   - **Loop cap reached.** `true` iff loops used == 2.

   - **Decisions.** Open `synthesis.md`. Count bulleted items under either `## Recommendation`, `## Post-critique recommendation`, or `## Uncertainties` (or the equivalent named heading per CLAUDE.md step 12 — confirm by reading the heading text in the file). The exemplar counted `1 explicit recommendation + 5 named uncertainties = 6`. If `synthesis.md` is missing, decisions = 0.

4. **Derive ratios.** Per the schema:
   - Agent-calls per decision = `<agent-calls> / <decisions>`. If decisions = 0, render `N/A`.
   - Artifacts per decision = `<artifacts> / <decisions>`. If decisions = 0, render `N/A`.
   - Loops to convergence = `<loops>/2`.

5. **Evaluate warnings.** Per the schema:
   - `agent-calls / decisions > 10` → ⚠️ "consider whether the workflow produced more analysis than action"
   - `artifacts / decisions > 8` → ⚠️ "consider whether documentation is exceeding decisions"
   - loop cap reached → ⚠️ "candidate needed maximum rework; first-pass framing was off"
   - Zero warnings → render the literal line `warnings: none`.

6. **Write `ledger.md`.** Paste the schema's template, fill it. Use the four load-bearing headings exactly: `## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`. Do not rename, reorder, or merge them.

7. **Append the synthesis citation line.**
   - Read `synthesis.md`'s last line.
   - The required form is exactly: `Ledger: agent-calls=<N>, artifacts=<N>, loops=<N>/2; warnings: <list or "none">.`
   - If the line is absent, append it. If it is present but stale (numbers don't match the ledger you just computed), update it.
   - **Edit `synthesis.md`'s final line; do not rewrite the whole file.**

8. **Append the `## Metrics` block (optional, additive).**
   - If `.claude/session-artifacts/<session-id>/diagnostics/metrics.json` exists, read it and append a `## Metrics` block to `ledger.md` *after* `## Notes`. The block is YAML inside a fenced code block.
   - If `metrics.json` is missing (older session, or hooks were not enabled), **silently skip** — do not write a placeholder, do not error. The four load-bearing headings (`## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`) are untouched.
   - The block content is the YAML rendering of the JSON, preserving keys: `duration_seconds`, `tokens.{total, by_agent, source}`, `tool_calls.{total, by_type}`, `verdicts`, `loops`. Use `python3 -c "import json,yaml,sys; print(yaml.safe_dump(json.load(sys.stdin), default_flow_style=False))"` if available; otherwise fall back to a simple key:value dump that preserves the schema. The block heading must be exactly `## Metrics` (additive, not load-bearing — older renders without it remain valid).

9. **Report back.** In under 100 words:
   - The session id and ledger path you wrote (repo-root-relative markdown link).
   - A one-line summary: counts, ratios, warning count.
   - If a warning fired, name which one and a single sentence on what it likely means in this session's context (e.g., "loop cap reached → first-pass frame was off; check `decision-log.md` to confirm").
   - If `synthesis.md` was updated, say so explicitly.
   - If a `## Metrics` block was appended (because `diagnostics/metrics.json` existed), mention duration and the largest token-by-agent in one sentence (e.g., "metrics inlined: 562s total; critic-architecture used 25k tokens, 3× the others").

## Constraints

- **Counts are taken just before `ledger.md` is written. `ledger.md` does not count itself.** This is the schema's load-bearing rule — the `find ... -not -name 'ledger.md'` exclusion in the artifacts count enforces it.
- **Do not invent threshold values.** If the schema's thresholds (currently 10 / 8 / 2-loop) have been retuned in the README since this skill body was last updated, the README wins.
- **Do not write a ledger for a bypassed session.** Quick-take and pure-factual sessions get no ledger. Per the schema, "absence of `ledger.md` from a non-bypassed session is a workflow defect" — so being conservative on bypass is correct, but being wrong about a non-bypassed session and skipping the ledger is a defect.
- **Do not modify `decision-log.md` or any other session artifact** beyond `ledger.md` and the final line of `synthesis.md`. The session is the workflow's audit trail; the ledger is a derived view, not a rewrite license.
- **Do not anchor on a remembered ratio threshold.** The schema names "after 5 real ledgers exist, review the distribution" — thresholds may legitimately move; trust the README at read time.

## When the session state is incomplete

- **No `synthesis.md`:** veto-stopped session per the schema. Render with `decisions = 0`, ratios = `N/A`, and note this in `## Notes`. Do not refuse to render.
- **No `decision-log.md`:** loops used = 0 (the file is created on the first replan/rewrite decision; absence means no loops happened). Note this; do not error.
- **No `distillations/` directory:** subagent gathering (steps 3–5) was skipped — possibly a quick-take that the user later promoted. Confirm bypass status with the user before rendering.
- **Non-standard heading names in `synthesis.md`:** read [CLAUDE.md](CLAUDE.md) step 12 to learn the canonical heading text; if the file uses different headings, count what looks like the equivalent and note the deviation in `## Notes` so a future schema-tuning pass can decide whether to normalize.
