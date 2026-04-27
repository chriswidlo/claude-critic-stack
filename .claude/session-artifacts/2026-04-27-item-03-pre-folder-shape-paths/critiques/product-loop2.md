# Product critic — loop 2

**Verdict: approve.**

## User-visible consequence

Day-of-ship under v2, the operator opens git log expecting `item 3 ✅ done` and finds **exactly that**: one commit, 5 string substitutions, item marked done in the punch list, two new punch-list entries (14 and possibly 15) appended at the end of the list they themselves authored. Most-noticed surface change: the punch list grew by 1–2 lines in a section the operator already scans regularly. No frame revisions are pushed back. No "commit B" deferred-slot artifact appears. No conditional commit choreography. **This is the shape a five-word ask deserves.**

## Commitments implied

Three, all materially smaller than v1's:

- "Workflow-surfaced concerns get filed to the operator's existing intake surface (the punch list), not invented as new artifact classes."
- "Done-when conditions that do hidden policy work get deleted with a one-sentence note, not preserved with a wrapper."
- "The synthesis step may legitimately present the operator with two candidate shapes." **This is new and the most load-bearing of the three** — see frame-level objection.

## Migration burden

- Operator: ~30 seconds scanning 1–2 new punch-list entries.
- Item 1's session/successor: same known re-touch as v1.
- Future readers of line 138: *no* new parenthetical (burden removed relative to v1).
- Future cleanup items 4–13: inherit a smaller precedent ("responsive minimum + punch-list filing for surfaced concerns") instead of v1's "ship + spawn 1–3 commits + a question."

## Affordances better / worse

**Better than v1:**
- "Item 3 is done in one commit" restored.
- "Plan = ship" coupling restored.
- Commit messages about what the commit does, period.
- Operator's intake surface respected.

**Worse / pruned:**
- 7 stale session-artifact references stay stale (acknowledged tradeoff).
- Line 138's dogfood entry continues to name an old path inline.
- The redirects-file alternative is filed rather than evaluated.

## Frame-level objection

The candidate's "synthesis presents both shapes" line (assumption 1's mitigation, restated in the cheapest experiment) is a frame-level concession that **the workflow doesn't trust its own convergence**. If the loop-1 veto was correctly read as "v1 over-generated scope" and v2 is the correctly-collapsed response, then v2 *is* the answer and synthesis says so. Offering v1 alongside is the workflow asking the operator to retroactively legitimize the over-generation. **Drop it. Pick.**

## What would change the verdict

Verdict drops to `rework` if synthesis presents both v1 and v2 as a choice rather than presenting v2 as the recommendation with v1 named only as an audit-trail artifact.
