# Critic-panel verdicts

## Loop 1 (candidate v1 — audit-first / gate-deferred)

| Lens | Verdict | One-line |
|---|---|---|
| architecture | `rework` | Audit script's grep schema *is* the per-state transition schema, smuggled in as Phase 0 with no source-of-truth coupling to README. |
| operations | `rework` | Phase 1's six-week "observation window" has no measurement instrument; without hand-labeled ground-truth, script's output becomes its own validation. |
| product | `reject` | Candidate answers "should we build a gate?" when operator asked "design the gate." Day 1 ships zero gate-shaped affordance. |

**Aggregate: minority-veto. Replan to step 8 (re-frame), Revision 2 to frame.md.**

## Loop 2 (candidate v2 — warning gate, day-1, schema-in-README)

| Lens | Verdict | One-line |
|---|---|---|
| architecture | `approve` | All three loop-1 conditions met; remaining concerns are soft and improvable in implementation. |
| operations | `approve` (with one pre-merge condition) | Honestly addresses measurement-instrument and rollback objections. Pre-merge: specify `--apply` safety behavior. |
| product | `approve` | Day-1 gate-shaped affordance; contract preserved; `--apply` correctly opt-in. |

**Aggregate: all three approve. Proceed to synthesis (step 12).**

## Pre-merge conditions (operations) and watch-fors

- `--apply`: must refuse on dirty working tree OR show `git diff --stat` before writing.
- Future-revision watch-fors: do not default `--apply` to true; do not rewrite README's "manual act" sentence.
- Cheap (non-blocking) operations enhancement: log each `/upgrade advance` invocation to `.claude/session-artifacts/upgrade-gate-runs.log` so silent-disuse becomes detectable.
- Soft-improve before merge: HTML-comment marker in the README's new schema section; one-sentence acknowledgement of schema-as-types alternative; one-sentence acknowledgement of cross-directory coupling.
