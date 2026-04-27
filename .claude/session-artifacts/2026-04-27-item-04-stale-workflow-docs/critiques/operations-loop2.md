# Operations-lens critique (Loop 2) — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Lens.** Operations.
**Loop.** 2.

## 1. Most likely incident

At time T (≈ 4–8 months after this PR lands), the maintainer adds a fifth critic lens or restructures the workflow to 13 steps; the pre-commit hook does not fire because the README's categorical prose contains no count tokens to match, and the calendar reminder on 2026-07-27 was acknowledged-and-snoozed once already. Root cause: the hook is a count-drift detector but the actual drift mode after move #2 is *concept drift*, which the hook is structurally blind to.

## 2. Blast radius

- **Hook coverage:** narrow but appropriate for *count-drift*. Catches roughly 4 token shapes; misses `four lenses`, `2-step`, `eleven agents`, `panel of critics`, etc. Estimate: catches ≥80% of *naive* count drift; catches ≈0% of *categorical* drift.
- **Calendar reminder:** fires once on 2026-07-27. After that date, blast radius reverts to pre-control state unless re-armed. Single-shot.

## 3. Rollout / rollback

PR is now ~1-2h vs v1's 30 min, candidate names this honestly. Rollback for moves #1–#5 and #8–#9 is `git revert`. Rollback for move #6's pre-commit hook is `git revert` plus `git config --unset core.hooksPath`. Acceptable.

The non-reversible move (audience declaration shaping 3–6 months of subsequent doc decisions) is unchanged in v2 — it is still a frame commitment with multi-month consequences if wrong.

## 4. Observability gap

**Closed:**
- v1 had zero controls; v2 ships the pre-commit hook. Real, mechanical, falsifiable observation mechanism. Meets approve-condition (a).
- Assumption 1 marked untestable, cost absorbed (move #7). Honest. Meets approve-condition (b).

**Remaining (named by candidate, not closed):**
- Hook is blind to concept drift. Given that move #2 *removes counts entirely* from the README, the hook partly defends a vector that move #2 already structurally eliminated. Not useless — prevents *re-introduction* — but coverage of post-rewrite failure modes is narrow.
- Calendar reminder is single-shot. Better than v1's nothing; weaker than recurring quarterly.

**Net:** v2 has roughly one and a half controls where v1 had zero.

## 5. Cost at failure

- Hook false positive on legitimate edit: one `--no-verify` plus a few seconds. Cheap. Accepted.
- Concept drift slips past both controls: same as v1's failure mode — re-explanation cost amortised across future readers, plus a fresh stale-doc punch-list item in 6–12 months. v2 has not reduced *worst-case* cost; it has reduced *probability* of count-drift subset.

## 6. Frame-level objection

v1's frame objection was *"this is a control-design problem and the candidate ships zero controls."* v2 ships one mechanical control and one calendar commitment. The control-design frame is now *engaged with*, not bypassed. Bar met.

**Residual operational seam, not a veto:** the pre-commit hook is *opt-in* (`core.hooksPath = .githooks` must be registered in the local clone's config). Git does not commit `.git/config` — `core.hooksPath` is per-clone unless wrapped in a setup script. v2 says "registered in repo config" but should either ship a `make setup` / one-line installer, or acknowledge this is a single-machine control.

## 7. Verdict

**approve.**

Verdict would change to `reject` only if the pre-commit hook turns out to be uninstalled on the maintainer's actual clone (in which case the control is decorative and v2 collapses to v1). Maintainer should verify `git config core.hooksPath` returns `.githooks` on their working clone before merging.
