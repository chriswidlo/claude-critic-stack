# frame.md — item 13 (orphans fate)

## Revision 1

### User's framing (as posed)
"Decide the fate of four orphans. Either wire each into a load-bearing doc, or archive/delete with a one-line note in git history."

This framing presupposes the unit of analysis is *individual files*, and the choices are *keep-in-place / archive / delete*. The approach plan adds a layer: "is there a missing lifecycle for non-canonical docs?" — which presupposes the right output is a *policy* the four orphans then instantiate.

### What the user is implicitly optimizing for
**Tidy repo + low future maintenance.** The punch-list is a janitorial sweep; the implied goal is a state where a future audit pass finds no orphans. Optimizing for *tidiness*: orphans are bad because they are visible cruft.

### Alternative optimization
**Cheap reversibility of past judgment.** Orphans are also a record of what the repo *tried* and either shipped or abandoned. The warm-balloon plan is documentation of the Phase-2 design decision; the ultraplan brief is documentation of the meta-decision to commission an external planning pass; five-pressures was an early structural compensator that 12-step partly subsumed. Deleting them prioritizes tidy-now over the ability to ask "why did we do it this way?" six months from now.

Under this optimization, the orphans are not cruft but **frozen evidence** — and the right primitive is not an archive folder but git itself (where they already live, even after deletion). The question is not "where do they go" but "what's the minimum-friction way to let them rest somewhere a reader doesn't trip over them while still being recoverable in two `git log` commands?"

### Reframe (orchestrator's restatement)

The user asked: *"Wire-in, archive, or delete each of these four?"*

Reframe to: *"Are these four orphans the same kind of thing? If yes, what minimum primitive lets the repo distinguish 'live reference' from 'frozen evidence' without inventing a new lifecycle? If no, on what axis do they differ — and does that axis already have a venue?"*

Sub-questions:
1. **Categorization.** Is each orphan (a) a *reusable artifact* the repo could cite if wired in (five-pressures has the shape of a checklist), (b) *frozen evidence of a past decision* (warm-balloon, ultraplan brief), or (c) *a primitive that didn't take* (exemplars/ — the promotion mechanism produced zero entries in 3 days)?
2. **Venue check.** Do existing primitives already absorb each category? `upgrades/LEDGER.md` has a `state` column (idea/draft/verified/committed/etc.); `.claude/session-artifacts/` has *de facto* immutability already; canon has a curated-reference shape; git history has frozen-evidence shape for free.
3. **Policy necessity.** Does the repo need a *new* category (an `archive/` folder, a `prompts/` lifecycle, a "shipped-plans" state), or do the existing categories cover it once orphans are routed correctly?

### Frame bias acknowledged (carried from classifier)
The classifier's `new` label nudges toward inventing a policy. The reframe deliberately re-opens whether *no policy* is correct. The frame is biased toward `new` but the alternative answer "the existing primitives already cover this; the orphans are just mis-routed; no new policy needed" is on the table and must be defended against, not against.

### What this reframe does NOT do
It does not pre-decide any orphan's disposition. It does not commit to a policy shape. It commits only to: *categorize first, then check whether each category already has a venue, then design only the gap.*

### Honest friction with the user's framing
The user's "wire-in or archive/delete" binary is too coarse. Wiring `five-pressures` into a load-bearing doc is a different operation from deleting an empty `exemplars/` directory; treating them as parallel choices in a 2-column matrix loses the structural difference between "this artifact has shape that could be re-used" and "this is a primitive that failed to bootstrap." The pipeline should produce four *non-parallel* recommendations, not a single policy applied four times.
