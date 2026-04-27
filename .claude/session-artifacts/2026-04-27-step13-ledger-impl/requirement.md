# Requirement classification — Step-13 session ledger format

## Primary label
**extend** — adds a 13th step to the existing 12-step CLAUDE.md workflow. Does not replace synthesis (step 12); appends a new artifact-writing step after it. The 8-state lab lifecycle, the 12-step workflow, the [.claude/session-artifacts/](.claude/session-artifacts/) tree, and the orchestrator's role are all preserved.

## Default frame (carried by `extend`)
Bias: *fit-into-existing-shape*. The label nudges the recommendation toward "use existing artifacts and existing surfaces; minimize new files; the orchestrator already has the data, just write it down." This is mostly correct here — every count the ledger needs is recoverable from on-disk artifacts the workflow already produces.

## Frame bias to watch
The `extend` label can mask the alternative: this could also be classified as `new` (a new observability primitive, the first metrics artifact the lab produces). Treating it as `new` would push toward thinking about the **schema** (what counts as a "decision," what counts as an "agent call") with more rigor — because schemas in observability tend to outlive their authors and are expensive to change later.

## Alternative classification
**new** — first quantitative observability primitive. If we accept this label, we should:
- Treat the schema as load-bearing (consider versioning, naming stability, ratio-as-derived-not-stored).
- Anticipate cross-session aggregation (a future entry that diffs ledgers across sessions).
- Be wary of premature optimization — observability that nobody reads becomes dead weight.

The synthesis below adopts a **mixed posture**: extend in surface (a single new file per session, written by the orchestrator), new in schema-discipline (counts and derived ratios are committed-to with a stability rationale).

## What the user is implicitly optimizing for
A mechanical signal of "did this session over-elaborate?" without inventing money/time estimates that don't carry meaning in AI-native units.

## What the workflow should NOT optimize for
- Workflow self-justification ("look, we ran 14 agents, value!") — the ledger is a *warning surface*, not a brag.
- Cross-session leaderboards, gamification, or ranking sessions by efficiency.
- Replacing operator judgment about whether the synthesis is good.
