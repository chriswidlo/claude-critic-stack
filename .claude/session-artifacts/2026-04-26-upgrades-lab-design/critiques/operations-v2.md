# Operations critique v2 — verdict: approve

Persisted from inline return.

## Verdict
approve

## Were the v1 deltas addressed?

- **Delta 1 (instrument falsifier):** Yes. `bin/upgrades-ratio.sh` named, classification rules explicit, edge case (`bin/upgrades-*.sh` itself) called out, trigger procedure specified, pre-commit hook named.
- **Delta 2 (rollback semantics + break-glass):** Yes, with one residual gap (break-glass bound is operator-honored, not script-enforced).
- **Delta 3 (curator-bootstrap path):** Yes. Lint script as bootstrap; curator agent demoted from locking dimension to future capability.

All three deltas landed as actually-runnable artifacts on day-7 critical path, **contingent on assumption 3** ("the four scripts are actually written by day 7"). Candidate names this contingency: "the day-7 freeze does not land if the four scripts are not on disk." Right gate.

## New concerns introduced by v2

1. **3-hour estimate is plausible but optimistic.** Ratio-script classification logic has edge cases (commit touches both meta+content; inbox-entry-documenting-structural-change; pure-rename via `git mv`). Realistic build estimate: **3.5–4.5 hours**.
2. **Break-glass bound is enforceable in spirit but not in code.** Operator-honored, not script-detected. Candidate slightly over-claims.
3. **Inbox-then-promote two-step is genuine improvement.** Asymmetry: entries that never earn promotion cost only 10s; entries that do, cost capture+promotion at moment of structural intent. Net friction reduction at write-time.
4. **Discipline-tag transition when MODULES.md lands** is a content rewrite v2 doesn't acknowledge in worked examples. Frontmatter only, but real.
5. **Lint is "well-formed" not "useful."** Doesn't judge body-vs-type fit, justifications for `matured`, suggest missed cross-references. Acceptable as bootstrap; gap should be explicit.

## Operational cost at steady-state (revised)

- Day-1 setup: 3.5–4.5 hours (slightly over candidate's 3-hour estimate; not invalidating)
- Per inbox entry: 10 seconds (realistic)
- Per matured entry: 5–10 minutes (down from v1's 10–20 minutes — real friction reduction)
- Day-60 audit: ~10 minutes
- Quarterly review: half-day to full-day, still un-budgeted (minor concern, not blocking)

## Operational cost at failure (revised)

- Mode A: inbox surface is meaningful mitigation; recovery low-cost
- Mode B: essentially eliminated (worked examples carry load); residual = discipline mass-update, one-shot mechanical
- Mode C (curator never built): dissolved (lint is bootstrap; curator now optional layered capability)
- New Mode D (script written but never run): pre-commit hook opt-in; if operator never opts in nor runs ad-hoc, day-60 audit fails silently. Candidate names honestly in assumption 6.

## Frame-level objection

Load-bearing claim partially demonstrated; discipline-tag case is counter-example v2 skips. Operationally honest framing: "additive metadata layer is rewrite-free for body content and rewrite-cheap for frontmatter, with one named exception (first taxonomy commitment) that costs one batch operation." Phrasing objection, not structural; doesn't block approval.

## What would make this approve

This *is* approvable. Three v1 deltas landed as runnable controls. Candidate honestly names contingencies. Two-step capture-promote is operational improvement. Remaining concerns are real but not approve-blocking — deltas for hypothetical v3 if operator wants tightening. v2 is operationally sound.

Verdict that would be `reject`: any of four scripts not on disk by day 7. Verdict that would be `rework`: discovered edge case in ratio-script classification logic. Neither has fired.

**Approve, with four named lens-specific concerns recorded for visibility but not as veto conditions.**
