# Architecture critic — loop 2

**Verdict: approve.**

## Weakest structural link

The weakest link in v2 is the **forward dependency from item 3's edits to item 1's not-yet-decided link style**. v2 acknowledges this honestly ("known re-touch when item 1 lands; ~5 minutes") and routes it correctly: do not pre-architect against an undecided primitive. The coupling exists, but it is now *visible, bounded, and cheap to repair*. Loop 1's structure tried to absorb the coupling into Commit C choreography, which made the coupling structural; v2 leaves it as an in-flight string match across two files, which makes the coupling lexical. Lexical coupling on five lines is the right answer when the alternative is architecting against an unknown.

## Invariants at risk

1. **Punch-list-as-flat-cleanup-tickets invariant.** Item 14 is a "decide a policy" item, structurally unlike items 1–13 which are concrete edits. The punch list's *type* changes when it acquires policy items.
2. **Done-when minimality invariant.** Replacing Done-when #5 with a one-sentence note that points outward to item 14 means the plan now contains a forward reference to a not-yet-existing item.
3. **Single-commit reversibility invariant.** v2 promises "full, single `git revert`," but the commit also creates punch-list item 14. A revert undoes the edits *and* the new punch-list line; the surfaced concern is then lost unless re-filed.

## Coupling and direction

Direction is now correct on the policy axis: v2 declines to ship a policy primitive on the back of a 4-edit cleanup. Volatile (string substitutions) ships first; stable (policy) is deferred to its own carrier.

The remaining coupling — item 3's commit creates item 14 — is **author-time coupling**, not run-time. Acceptable. No cycles introduced.

## Frame-level objection

v2 collapses to "ship the 4 edits, surface concerns as punch-list items." This is the right collapse — but it embeds an assumption that **the punch list is the correct intake surface for *workflow-generated* findings**. The punch list was authored by the operator from operator-noticed problems. Adding agent-noticed findings to the same list silently changes its provenance mix. A future reader cannot distinguish operator-originated items from workflow-originated ones unless the items are tagged.

This is frame-level because it asks: *is the punch list a single-author worklist or a shared queue?* v2 picks "shared queue" without naming the choice.

## What would change the verdict

Evidence that the operator's punch list is a single-author surface, in which case item 14 should move to a commit-message note instead.
