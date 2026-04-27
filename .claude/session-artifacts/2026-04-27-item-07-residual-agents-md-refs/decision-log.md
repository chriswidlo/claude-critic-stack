# Decision log — item 7

## Step 10 verdict

- Architecture: `reject` (frame-level)
- Operations: `rework`
- Product: `rework`

## Step 11 routing

**Decision: rewrite, not replan.**

The architecture lens issued a frame-level objection but its smallest-change-to-approve (the *tombstone alternative*) is a concrete generator-step rewrite, not a frame change. Adopting the tombstone simultaneously addresses operations' "no observability, scope-shrink risk" objection (no rewrites = no scope-shrink) and product's "lifecycle-row contract violation" objection (no body edits = no contract violation). One rewrite resolves three vetoes — strictly cheaper than reframing the question.

Routed to step 9 (generator) with: tombstone approach as the new candidate; preserve the live-doc edits (CLAUDE.md path-discipline rule, but in a different way — see v2); confine all changes to additive moves where possible.

Loop counter: 1 of 2 (cap per CLAUDE.md).

## Step 10 verdict — loop 2 (v2: tombstone)

- Architecture: `rework` (improvement from `reject`)
- Operations: `rework`
- Product: `rework`

## Step 11 routing — loop 2

**Decision: escalate to synthesis.** Cap reached (loop 2 of 2). All three lenses returned `rework` rather than `reject`. The reworks are not contradictory — they converge on minor refinements (architecture: codify upstream convention OR Alternative 2 minimal-edit-without-tombstone; operations: tombstone marker + rollback-consequence sentence; product: filename-or-heading-level marker + punch-list cross-link). Each rework names a small, concrete delta.

The pipeline cannot ratify a single approach within its loop budget. Per CLAUDE.md, escalate to synthesis with the disagreements named. The user (operator) chooses among the surfaced options.

Loop counter: 2 of 2.
