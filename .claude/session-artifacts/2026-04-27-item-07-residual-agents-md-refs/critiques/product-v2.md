# Product-lens critique v2 — item 7 (tombstone alternative)

## 1. User-visible consequence

A new operator running `ls` at repo root sees `AGENTS.md` and `CLAUDE.md` side by side. The directory listing carries a *signal that contradicts the truth* — "two constitutional docs, presumed co-equal" vs. the truth ("one constitutional doc, plus a tombstone"). Operators who grep, who feed the repo to a tool, who skim a tree view, or who use file-pickers showing only filenames are not protected by the body-first-sentence mitigation.

This is a **smaller harm than the loop-1 lifecycle-row violation, but it is a new harm v1 did not have.** v1 left `AGENTS.md` non-existent; the `ls` lie did not exist under v1.

## 2. Commitments implied

- **A "tombstone-recreates-deleted-primitives" pattern.** Once shipped, the next time a constitutional doc is retired, the cheapest path will be to leave a tombstone rather than fix references. The lab is committing to *file-system-as-reference-graph* over *prose-as-reference-graph*.
- **A populated-AGENTS.md migration path.** The tombstone body invites a future author to *"replace the tombstone with the new content."* The lab now has an *implicit TODO* sitting at repo root.
- **The supersede-don't-edit question stays open.** v2 punts the convention question to a separate upgrade entry and declares it not load-bearing — a commitment to *operate without an answer to that question* until the entry is filed and installed.

## 3. Migration burden

- **Orchestrator agent loading CLAUDE.md:** zero burden. Path-discipline rule's enumeration now names a real file again.
- **Future critic-panel agents performing supersession analysis** on the parity-claim entries: burden *unchanged from today*. Their cells still describe parity between two existing files. Whether the parity is substantive (CLAUDE.md vs. real co-equal) or vacuous (CLAUDE.md vs. tombstone) is a question those critics decide on merits. v2 does not poison their input as v1 would have.
- **Future operators searching `git log`** for "why does AGENTS.md exist": small new burden — three-stop archaeology where today is one.

## 4. Affordances better/worse

**Better than v1:**
- No upgrade-entry body edits; the entry-as-contract surface is preserved. **All three loop-1 objections moot.**
- Original-claim affordance preserved unchanged.
- `grep -r AGENTS.md` returns hits that all resolve.

**Worse than the no-AGENTS.md baseline:**
- **The `ls` lie.** A new product surface created: a file pair that *looks* co-equal in the listing but is not.
- **Ambient TODO at repo root.** Every future author who notices the tombstone has to decide whether to populate it.
- **A precedent that future-deleted constitutional docs should also be tombstoned.**

**Discoverability of retirement event:** the tombstone trades grep-opacity for ls-opacity. Different shape, not strictly better.

## 5. Frame-level objection

**The frame treats this as a reference-resolution problem; from a product lens, the decision is about what the repo's directory listing says about its own constitutional structure.**

The eight references are a *symptom*. The underlying product surface is "what does this repo claim its constitutional layer is, when read at the highest possible level (filenames at root)?" v1: inconsistent. v2: misleading. Alternative B (full symmetric supersede-don't-edit pass): consistent and honest.

v2 is cheaper than B and resolves the loop-1 critiques. **It does not resolve the underlying product surface question** — it just relocates the inconsistency from "broken references" to "misleading directory listing."

## 6. Weakest link

The `ls AGENTS.md` first-impression surface combined with the unmarked filename. The body-first-sentence mitigation is necessary but not sufficient. A reader who never opens the file gets the wrong impression and never corrects it.

## 7. Verdict

`rework`.

**Smallest change to approve.** Make the tombstone legible at the filename layer, not just inside the body. Two acceptable options:

1. **Rename the file `AGENTS.md.tombstone`** and update the seven existing references to point at the new filename. Breaks the "zero edits" property but only mechanically — references resolve, no benefit cell reworded. The `ls` surface tells the truth without anyone opening anything.
2. **Keep filename `AGENTS.md` but prefix the H1 with `[RETIRED] `** and add a top-of-file HTML comment readable by tools that strip markdown but render comments. Weaker than option 1 but preserves v2's "zero edits to existing files" property.

**Punch-list cross-link:** the punch-list `✅ done` line for item 7 should explicitly link to the (yet-to-be-filed) follow-up upgrade entry as an "open dependency" so the gap is legible.

Verdict flips to `approve` with option 2 plus the punch-list cross-link.
