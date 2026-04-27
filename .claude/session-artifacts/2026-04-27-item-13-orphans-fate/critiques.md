# critiques.md — item 13 (orphans fate), aggregate

| lens | verdict | frame-level objection (one line) |
|------|---------|----------------------------------|
| [architecture](critiques/architecture.md) | **rework** | Candidate denies it introduces a new primitive while paying the full cost of one (session-artifact-as-deletion-log). A nameless primitive is the worst kind. |
| [operations](critiques/operations.md) | **rework** | This is a change-management op on a cross-referenced corpus, not a per-orphan disposal: should be sequenced (rename first, then deletes after one sweep cycle); CLAUDE.md amendment must be its own commit with a rollback criterion. |
| [product](critiques/product.md) | **rework** | "No new policy primitive" is measured by artifact count, not contract count — candidate ships three unannounced contract changes (step-9 requirement, `plans/` parsing convention, session-artifact-as-discoverability). |

## Minority-veto: triggered (3-of-3)

All three lenses returned `rework`; none returned `reject` or `approve`. Per CLAUDE.md step 11, route to step 11 (replan-vs-rewrite).

## Convergent objections (all three lenses)

1. **The session-artifact-as-discoverability claim is undefended.** Architecture calls it a nameless primitive; product calls it a circular discoverability claim ("future session reads the synthesis, but the synthesis is only discoverable to a session that already knows item 13 happened"); operations calls it a structurally impossible rollback ("you cannot revert what you do not remember to revert"). Three independent framings, same load-bearing weakness.

2. **The CLAUDE.md step-9 amendment is the wrong shape and rides on the wrong cart.** Architecture: volatile→stable inversion (lifting from a deleted file with zero live consumers into the most-stable doc). Operations: no enforcement mechanism, no rollback criterion, will decay into ceremony. Product: bait-and-switch — slipping a workflow contract change into a janitorial sweep PR.

3. **The O3 rename ships without an inbound link audit.** Architecture, operations, and product all flag the un-grepped link graph. Operations is most explicit: rename first, observe, then deletes.

## Divergent emphases

- **Architecture** is most concerned with the *naming* of the new primitive (explicit > implicit; if you're going to do it, name it).
- **Operations** is most concerned with *sequencing and rollback criteria* (atomicity is a bug, not a feature, here).
- **Product** is most concerned with *contract surfaces invisible to the next user* (empty `prompts/` reads as forgotten cleanup, not as signal).

## Routing decision (step 11)

The veto pattern is **frame-level** for architecture and product (both name a frame error: "no new primitive" is a false frame; "disposal decision" is a false frame), but **design-level** for operations (sequencing and rollback are specific actionable changes, not frame errors).

Two of three lenses raise frame-level objections. Per CLAUDE.md step 11: when veto is frame-level, route back to step 7 or 8. Architecture and product's objections converge on the same frame error: the candidate measured "no new primitive" by artifact count rather than by *contract count* / *load-bearingness*. The honest re-frame is "implicit primitive vs. explicit primitive," and the explicit-primitive frame should be evaluated.

**Decision:** route to step 9 (rewrite, not replan). Rationale: the frame-error all three lenses identified is correctable inside the generator step without re-running scope-mapper or frame-challenger — the alternative frame ("explicit primitive vs. implicit primitive") was *already named* by the architecture critic and the product critic; what the generator must do is accept it and re-derive the candidate. Re-running scope-mapper would produce the same map; re-running frame-challenger would produce the same challenges. The generator simply did not metabolize them.

Cap: this is loop 1 of 2 permitted by step 11. If loop 2 also vetoes, escalate to synthesis with the disagreements named.

---

## Loop 2 — candidate-v2 review

| lens | verdict | one-line |
|------|---------|----------|
| [architecture v2](critiques/v2/architecture.md) | **approve** | All loop-1 objections cleanly resolved; named primitive (`prompts/RETIRED.md`); rename dropped; CLAUDE.md amendment dropped; inbound-link audit documented. Frame-level "primitive vs precedent" flagged for synthesis, not blocking. |
| [operations v2](critiques/v2/operations.md) | **approve** | Atomicity now defensible (rename-driven asymmetry gone); rollback trigger named (sibling-session test); falsifier memory-independent; inbound-link audit performed. Single nit: promote item-07 coordination edit to a row in the action table. |
| [product v2](critiques/v2/product.md) | **approve unambiguously** | Bait-and-switch gone; self-explanatory sentinel replaces empty-dir; path-keyed discoverability breaks v1's circularity; falsifier runnable at commit time. |

## Minority-veto: cleared (3-of-3 approve)

Per CLAUDE.md step 10, all three lenses approve → proceed to step 12 (synthesis). Loop counter: 2 of 2 permitted.

## Convergent residual flags (carry into synthesis, not blocking)

1. **Primitive vs precedent.** Architecture flagged: `RETIRED.md` is shipped as a one-shot precedent but written up as a primitive with a contract. Pick one. Synthesis should name this as an open question, not silently resolve.
2. **Item-07 coordination edit.** Operations flagged: lives only in narrative; promote to a row in the action table to reduce the "forgot it on the way to commit" risk.
3. **Sibling-session test is itself a contract.** Product flagged: ships untested if not actually run. Cheap mitigation; named.
