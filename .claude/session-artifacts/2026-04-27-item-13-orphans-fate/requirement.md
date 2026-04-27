# requirement.md — item 13 (orphans fate)

## Primary label
`new`

## Default frame (from label)
What shape should the lifecycle-for-expired-docs policy take, and what's the cheapest experiment (e.g., applying any draft policy to the four orphans and seeing where it breaks) that distinguishes shapes? Treat the per-orphan calls as the first application of the policy, not as four independent disposals.

## Known frame bias
Over-designing the policy before evidence — inventing lifecycle tags, archive folders, and promotion paths when the four orphans could be resolved with a one-line rule. The `new` frame tempts a policy more elaborate than the four data points justify.

## Secondary label
`investigation` — the per-orphan layer asks "what is each one's right disposition," which is a what-exists / what-belongs question; if the policy layer collapses ("no policy needed, just decide each"), the residual ask is investigation-shaped.

## Alternative classification
`refactor` — would become primary if the user concedes that no new lifecycle primitive is needed and the task reduces to "move/delete four files without changing what the repo can do." The approach plan's own guess was `refactor`/`investigation`; reject `refactor` here because the punch-list explicitly invites a *standing policy*, which is capability addition, not structural rearrangement preserving behavior.

## User's framing words (flagged)
- "standing policy for 'documents whose immediate utility has expired'" — presumes a policy will be built (`new`).
- "delete-by-default? archive-folder? lifecycle tags?" — three pre-shaped solution sketches; flagged as solution anchors, not requirements. Reframe must consider whether *no* policy is the right answer.
- "fate of these four orphans" / "wired in or archived/deleted" — done-when language is disposal-shaped, which biases toward `refactor`; the two-layer ask overrides that bias.
- Approach plan pre-guessed `refactor` or `investigation`. Noted and rejected: the policy layer is a new primitive.

## Gaps
- Is the policy expected to be load-bearing (referenced from CLAUDE.md / README) or a one-paragraph note in the punch-list? Load-bearing → `new`; appended clause → `extend`.
- Does "archive" mean a new top-level folder, a git-only archive (delete + rely on history), or a tag/state marker on the doc in place? Each is a different primitive.
- Is `exemplars/` in scope here or deferred to item 5? If item 5 owns the call, orphan #4 drops out and the policy only needs to cover three heterogeneous docs, which weakens the case for any policy at all.
- Does an existing primitive (deleted `temporary/`, [upgrades/LEDGER.md](../../upgrades/LEDGER.md) states, session-artifact immutability) already encode a lifecycle the orphans could be retrofitted into? Scope-mapper will resolve.
