# Operations lens — loop 2

**Verdict:** `approve` with one named pre-merge condition

**One-line:** v2 honestly addresses measurement-instrument and rollback-honesty objections; remaining risks are real but bounded and acknowledged.

## Loop-1 objections, addressed

- "No measurement instrument": warning fires *at advancement time*, in the operator's attention. The warning IS the instrument. Acceptable.
- "Phase 2 rollback dishonest": no Phase 2. Rollback is "delete subcommand block + delete README table." Honest.
- "No non-bypassable surface for solo operator": acknowledged in candidate's "ways this could be wrong" #3.

## Most likely incident
At T+10 weeks, operator/agent edits state-table date directly, bypassing `/upgrade advance` for 8 consecutive advancements. **Gate dies of disuse with no liveness signal.** Candidate accepts this fate (assumption #1) which is intellectually honest but operationally has no detection mechanism beyond "operator notices."

## Cheap mitigation (not gating on this)
When `/upgrade advance` runs, append one line to `.claude/session-artifacts/upgrade-gate-runs.log`. Operator can `wc -l` once a month and compare to `git log` count of state-table changes. Closes the silent-disuse gap without violating the "no new artifact" constraint (it's a log, not a contract).

## Pre-merge condition (the one thing I'd want fixed)
Specify `--apply`'s safety behavior: either (a) refuse to run on a dirty working tree, OR (b) show `git diff --stat` before writing. Currently v2 doesn't say. Mutation is small and git-tracked, so this is bounded — but explicit behavior beats implicit.

## Frame note
Soft frame objection: for a tool whose only invocation surface is operator/agent memory, the durability question is "does the invocation happen," not "does the warning work." v2 correctly names this in assumption #1 but conflates "warning ignored" with "gate not invoked" in "ways this could be wrong" #3 — they are different failure modes, deserve a one-line split.

## Symmetry worth naming
Blast radius of the gate failing = blast radius of not having built the gate. This is a "fails to safe" change. Worth saying out loud in the synthesis.
