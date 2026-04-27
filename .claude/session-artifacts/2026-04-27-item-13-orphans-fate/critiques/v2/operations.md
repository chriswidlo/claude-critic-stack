# Operations critique — item 13 (orphans fate), v2

Target: [candidate-v2.md](../../candidate-v2.md)

## 1. Most likely incident

At T+~commit time, the operator runs the five-action commit; the `prompts/RETIRED.md` sentinel is created and the two deletes land, but the in-scope coordination edit to [item-07's plan](../../../../../plans/2026-04-27-item-07-residual-agents-md-refs.md) (lines 26, 57) is forgotten in the rush to ship "one commit, five actions." Root cause: v2 names the item-07 update as in-scope but does not put it in the action table — it lives only in the audit narrative, so it is the action most likely to fall off the checklist.

## 2. Blast radius

- **Deletion blast (O1, O2):** bounded. Live inbound count is now known and named (zero load-bearing for O1; one for O2 = item-07 plan). Historical session-artifacts link-rot is explicitly accepted.
- **O3 header-only edit:** zero rename, zero broken links.
- **`prompts/RETIRED.md` introduction:** five-line file in a single directory; failure mode (file goes stale) is observable via `ls prompts/`.
- **Forgotten item-07 coordination edit:** one stale data-point reference. ~5 min single-investigation cost.

Order of magnitude smaller than v1.

## 3. Rollout / rollback

- **Rollout:** one commit, five named actions. Atomicity defensible because the rename (only reversibility-asymmetric action) is dropped.
- **Rollback path:** `git revert` on the single commit restores all five states.
- **Two-systems-running period:** none.
- **Rollback trigger:** named — failure of the commit-time sibling-session test. The operations-meaningful improvement: rollback now has a *trigger*, not just a mechanism.

## 4. Observability gap

- **`RETIRED.md` staleness:** `ls <dir>/` mismatch is the observable, but not automated. Acceptable for a five-line breadcrumb; flagged as "human eyeballs at next visit."
- **Item-07 coordination edit landing:** no automated check.
- **Commit-time sibling-session test:** named, runnable, produces observable pass/fail signal pre-merge. Real win over v1's 6-month memory test.

## 5. Cost at failure

- **Sibling-session test fails:** one extra commit (CLAUDE.md note). Cheap.
- **`RETIRED.md` itself goes orphan:** visual noise in `ls`. Bounded.
- **Item-07 edit forgotten:** ~5 min next-reader investigation. Bounded.
- **Compounding failure (v1's worst-case):** closed. `RETIRED.md` lives where the deleted file lived, so an inbound 404 from a session-artifact leads the reader to `ls prompts/` → `RETIRED.md` → answer in <30s. Unbounded cost is bounded.

No retry storms, no fan-out, no on-call surface.

## 6. Frame-level objection

I had one in loop 1 (this is a change-management op on a cross-referenced corpus). v2 metabolizes it: inbound-link audit performed and named; rename dropped; CLAUDE.md amendment dropped. Operations frame is satisfied — unit of work in v2 *is* an atomic tree-delta with a named link-graph audit and a named rollback criterion.

Residual frame note, not blocking: v2 still treats item-07 coordination edit as narrative rather than as a row in the action table. Checklist-design gripe, not frame error. Recommend the operator promote it to a sixth row before committing.

## 7. Verdict

**`approve`.**

What would change the verdict: nothing. v2 addresses every operations-lens objection from loop 1. Single residual nit (promote item-07 coordination to a row in the action table) is pre-commit checklist polish, not a rework trigger.
