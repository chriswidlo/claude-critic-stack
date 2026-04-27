# Critic — Product lens v2 — item 06 (loop 2)

## 1. User-visible consequence

Reader sees Group E grown from 1 row to 3. Both former-#18b and former-#18g now read `🌱 / —` in State / `Implement as` cells, sitting under "Observations (no immediate action)." **State column and implement column agree at the row level.** Clicking into either entry lands on a `## Status` paragraph that names the dead migration plan, the worktree branch, and the commit, then yields to the parent-shape narrative. **No phantom `git mv` blocks.** No blockquote-demoted imperatives. Migration text is gone from disk, not gone-but-still-grep-able.

State-cell-vs-`Implement as`-cell disagreement (loop 1) resolved at the schema level, not at the prose level.

## 2. Commitments implied

Two product-surface contracts; both weaker than (b′)'s and easier to live with:

1. **Group E is a destination, not just an origin.** Entries that originated as Group D ideas can be relocated when their action becomes non-executable.
2. **`## Status` is an entry-body section name with semantic load** ("the entry's actionability has changed since creation; here is what it now means"). One precedent, not yet a written rule.

Both recoverable: Group E entries can re-graduate to Group D with a fresh migration plan; `Status` section can be renamed at low cost (grep-unique today).

## 3. Migration burden

- **Future operator advancing either entry past `🌱`** still reads `Status`, but now the row's metadata (`—` in `Implement as`, Group E membership) tells them *not to advance* without re-graduation. Real load reduction vs. (b′).
- **`canon-librarian` and ranking subagents** need no new logic. State token meaning stable; group membership carries the actionability signal.
- **Reader of sister entry chasing cross-reference** lands on entry whose `Status` is first in the TOC. Authority of parent-shape sections preserved cleanly.
- **Group D row-number consumers** named honestly in candidate's "ways this could be wrong" section.

## 4. Affordances better / worse

**Better:**
- State and `Implement as` cells agree. Both rows communicate "non-actionable" through schema-level signals.
- Phantom imperative text is *gone*, not blockquoted. Honest negation applied with full force.
- **`## Status` is more legible than `## Update history`** for the use case (state-of-the-entry, not advancement-history audit). Different jobs, different sections — candidate's choice not to borrow 18f's shape is the right call.
- Punch-list rhythm matches items 1–5: mechanical edit with named files. Crisp.

**Worse:**
- Group E's affordance shifts mildly. At 1 row it reads as a singleton curiosity; at 3 rows it begins to read as a small bucket. Mild category drift. Mitigation ("split Group E later") fine.
- `Implement as` = `—` is partly internal jargon — decoded by reading row #19, not by any rule in [`upgrades/README.md`](../../../../upgrades/README.md) or LEDGER's "How to read this." After (e), convention is load-bearing on three rows. **A one-line addition to LEDGER's "How to read this" — "`—` in `Implement as` means the entry is observational; no action against `main` is prescribed" — would close this gap and cost nothing.** Recommended additive cleanup, not blocker.
- 18b/18g were a "parent + first instance" Group D pair. After (e) they become a Group E pair. Net-neutral but anyone citing them as evidence of a Group D shape needs to re-read.

## 5. Frame-level note

No frame-level objection. The loop-1 objection ("preserves vocabulary by overloading it") is fully retired. Partition-correction is the correct frame.

Smaller frame note: candidate frames Group E membership as a *correction*, not a *demotion*. Correct for these two entries but should not become a general escape hatch. The right rule: "an entry whose substantive narrative survives but whose action is no longer executable belongs in Group E; an entry whose substantive narrative depended on the action belongs in entry-level supersession or eviction." Worth one sentence in [`upgrades/README.md`](../../../../upgrades/README.md) at some point — not blocking.

## 6. Verdict

`approve`

What flips back to `rework`: if the operator finds either narrative substantively depends on the migration plan having been *executed* (rather than merely described), parent narrative is also stale and (e) leaves dead thinking on `main`. Candidate's assumption #2 names this risk; verification is a 10-minute re-read.
