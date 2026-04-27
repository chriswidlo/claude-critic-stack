# Architecture critique — item 13 (orphans fate)

Target: [candidate.md](../candidate.md)

## 1. Weakest structural link

The candidate elevates `.claude/session-artifacts/<id>/` from a **session record** to a **deletion log / discoverability index**. Load-bearing primitive overload: the directory was designed to hold the immutable trace of one design session, addressed by session id and consumable in-order; the candidate now expects future maintainers to perform a reverse lookup — *"given a deleted file path I do not know, find the session that disposed of it"* — by globbing session-id slugs (`grep orphans`). That is a search pattern the primitive was not shaped for. The directory has no path-keyed index, no cross-reference back to the deleted artifact's former location, and grows monotonically with every future session unrelated to deletions. At N=21 sessions today the grep is fast; at N=200 it becomes a cross-cutting concern with no schema. The candidate is taking an implicit dependency on a property (path-addressable discoverability) that the session-artifact primitive does not provide and was not designed to provide.

## 2. Invariants at risk (not named by the candidate)

1. **Session-artifact monotonicity / single-purpose.** The directory's invariant is "one session, one immutable record, addressed by session id." Candidate does not state — and therefore does not preserve — the invariant that session-artifacts are *not* indexed by the artifacts they affect outside the session.
2. **`prompts/` single-occupant convention.** Candidate leaves `prompts/` empty post-deletion "as a passive signal." Empty dir in git is either uncommitted (signal lost) or sentinel-tracked (new primitive, contradicting the no-new-primitive stance).
3. **`plans/` semantic uniformity.** The other six occupants are *in-flight* punch-list items dated 2026-04-27. A Status header is *content-level* and does not survive `ls` or glob; readers/tools that filter on directory membership treat the shipped plan as in-flight.
4. **CLAUDE.md step 9 atomicity.** Adding "≥3 candidate solutions enumerated" is not additive — it changes the *shape* of the generator. Every downstream agent that reads step 9 inherits this shape change.
5. **Cross-orphan reference graph.** Candidate explicitly flags un-grepped: "the dependency-direction question … was not exhaustively grepped before deciding to rename." Renaming O3 with `git mv` will break any link that resolves by path.

## 3. Coupling and direction

- **Volatile → stable inversion (CLAUDE.md amendment).** CLAUDE.md is the most-stable, most-referenced doc. Pressure-#2 is being lifted from a 37-line orphan whose track record is *zero live consumers*. Stable should depend on stable, not on a deleted volatile.
- **Item 13 → item 5 dependency cycle risk.** Deferring O4 makes item 13's done-state depend on item 5. Direction unspecified. If item 5 also defers, item 13 is permanently open.
- **Layering violation (`plans/` ↔ `session-artifacts/`).** The footer adds a content-level link from work-tracking layer into session-record layer. Today `plans/` does not depend on session-artifacts; with this footer it does. New edge, not named.

## 4. Ignored architectural alternatives

1. **`prompts/RETIRED.md` (in-place breadcrumb).** 5-line file in `prompts/` listing each removed prompt with one-line rationale + commit SHA. Preserves path-keyed discoverability invariant. *Less* of a new primitive than session-artifact-as-deletion-log because it stays where the artifacts were.
2. **Header-only retention with no rename for O3.** Keep filename; prepend Status header. Zero link-breakage; "in-flight items get dated names; legacy items keep legacy names" is a less invasive convention.
3. **Promote O1 into a `critic-prelude` agent rather than into CLAUDE.md.** Preserves shape (checklist-shaped stays checklist-shaped) instead of forcing into prose-instruction shape.
4. **`.claude/session-artifacts/INDEX.md` (path-keyed index).** If candidate genuinely intends session-artifacts as a discoverability venue, the architecturally honest move is an index addressed by *deleted-artifact path*.

## 5. Frame-level objection

The candidate's frame is "no new primitive" — but the candidate **does** introduce a new primitive; it just refuses to name it. The new primitive is *"session-artifact directories are now path-addressable deletion logs, queryable by grep on session-id slugs."* This is a primitive in the strict sense: load-bearing convention with required reader behavior (look in session-artifacts before concluding a file never existed) and required writer behavior (slug session ids with terms a future grepper would guess). The candidate pays the full cost of a new primitive while denying that it is one and therefore declining to *document, enforce, or maintain* it. **A nameless primitive is the worst kind of primitive** — all the failure modes of a maintained convention plus the failure mode of being invisible to the people who must follow it. The honest frame is "implicit primitive vs. explicit primitive," and once stated that way, explicit wins on every architectural axis except the rhetorical one.

Second, narrower: the candidate accepts the frame-challenger's *premise* (git is not a discoverability venue) but rejects the *consequence* (an in-tree breadcrumb is needed) by substituting session-artifacts for git. If the premise is right, the consequence follows; the candidate's substitution only works if session-artifacts have the discoverability property git lacks. The candidate has asserted, not demonstrated. The cheapest experiment defers demonstration by 6 months — shipping on an undemonstrated load-bearing claim.

## 6. Verdict

**`rework`.**

What would change the verdict: name the new primitive explicitly (either "session-artifact-as-deletion-log, with these naming rules and this index" or "in-place `RETIRED.md` breadcrumb in directories that lose all occupants"), enumerate the link graph affected by the O3 rename before committing to `git mv`, and either justify the CLAUDE.md step 9 amendment on its own merits (not as an extraction from a deleted file) or drop it.
