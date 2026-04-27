# Operations critic — loop 2

**Verdict: approve.**

## Most likely incident

At T+10 weeks, an operator scanning the punch list sees item 14 ("decide session-artifact immutability policy") and item 15 (if filed, "link-validation tooling"), reads them as low-priority because they lack the concrete-fix shape the other items have, and never schedules them; meanwhile a new structural change lands and produces a fresh batch of stale references that punch-list item 14 was *exactly* meant to govern.

This is a *different* failure mode from loop 1's "operator re-edits line 138 to tidy" — because v2 dropped the line-138 edit, that incident is no longer reachable. v2 substituted a slower, lower-amplitude failure for a faster, higher-amplitude one. Net win.

## Blast radius

Five string substitutions in two README files. Single-digit reader-clicks/week worth of nav repaired. Reversibility: full, single `git revert`. **Smaller than v1's blast radius** because the line-138 self-defeating-parenthetical risk is gone.

## Rollout / rollback

- One commit on main, solo operator.
- Rollback: clean `git revert`. **No sequencing dependency on item 1** (v2 explicitly disclaims pre-architecting the restyle). The "two systems running" period from v1 is **gone** — no commit C to wait for.
- Cost during overlap: zero, because there is no overlap.

Strict improvement over v1.

## Observability gap

**Partially closed.** Adding items 14/15 to the punch list *does* carry the "deliberately open" signal — the concrete fix at zero cost asked for in loop 1, adopted by v2.

What stays invisible: at T+3 months, an operator looking at items 14/15 cannot distinguish "deliberately deprioritized" from "forgotten" without re-reading the session artifact for context. The punch list has no `last-considered` or `deferral-reason` field. This is a punch-list-format limitation, not a v2 defect.

## Cost at failure

When v2 fails (items 14/15 forgotten):
- 7 broken session-artifact links stay broken — same as today, no regression.
- Next structural change produces another stale-reference batch — modal failure outside-view forecasted, materializes on schedule.

v2's failure cost is **bounded by the status quo**. v1's failure cost included silent style drift at the cleanup-pass spots, which v2 eliminates by not pre-committing to a style.

## Frame-level objection

v2 addresses my loop-1 WIP objection cleanly: one commit closes one ticket, and the 1-2 new punch-list items are honest scope-routing, not WIP-laundering, because they carry concerns the operator otherwise has no record of. Punch-list line items are *intake*, not *WIP* — they only become WIP when scheduled.

New objection: **the punch list's character is being mutated.** It was a list of concrete cleanup tickets; v2 introduces "decide a policy" as an item type. That is a category change. Flagging for synthesis, not vetoing on it.

## What would change the verdict

Verdict drops to `rework` if synthesis fails to present the operator with the choice between "file as items 14/15" vs. "log only in session artifacts."
