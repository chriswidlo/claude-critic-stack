# Candidate v2 — item 3 (pre-folder-shape `.md` references)

**Loop:** 2 (post-replan).
**Frame:** collapsed (per [`frame.md` Revision 2](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/frame.md)).
**Authoring posture:** *honest minimum.* Ship the 4 edits; surface workflow-generated concerns as new punch-list items; do not bill the operator for findings the workflow generated.

## Position

**One commit. 4 edits. Done.**

- **Apply edits 1–4** from [`plans/2026-04-27-item-03-pre-folder-shape-paths.md`](plans/2026-04-27-item-03-pre-folder-shape-paths.md): the 5 path-suffix substitutions in [`upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md`](upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md) (lines 20, 158, 190) and [`upgrades/normal/2026-04-26-living-poweruser-knowledge-module/README.md`](upgrades/normal/2026-04-26-living-poweruser-knowledge-module/README.md) (lines 40, 48). Use the existing file-relative link style in each file (item 1 will restyle uniformly when it lands; do not pre-decide).
- **Edit the plan**: delete Done-when #5 ("No session-artifact file is modified by this commit"); replace with one sentence: *"This commit happens not to modify session-artifact files. Whether it ever should is the open question filed as new punch-list item 14."*
- **Mark item 3 done** in [`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md) per the punch list's own ritual ("append `✅ done <YYYY-MM-DD>` to the item heading, do not delete").
- **Add new punch-list item 14**: *"Decide session-artifact immutability policy (strict vs. permissive reading of commit `5108ed3`). Surfaced by item 3's workflow run; deferred because the policy is broader than item 3 and the operator chose the punch list as the intake surface."* Include 2-3 lines of context, not a multi-page brief.

That's the entire commit.

## What is dropped from candidate v1

- ❌ "Commit B" (the conditional commit envelope) — workflow-generated artifact class; collapsed.
- ❌ "Commit C" (the deferred restyle choreography) — item 1's domain; not item 3's job to pre-architect.
- ❌ The 5th edit at line 138 (the forwarding parenthetical) — operator did not ask; touches a file the original plan said was off-limits; architectural critique flagged the parenthetical as not idempotent under future migrations.
- ❌ "Child of `c2fe604`" commit message framing — load-bearing only if the operator endorses the convention; not endorsed.
- ❌ The `redirects.md` primitive — surfaced by architecture lens as a real alternative; *also* workflow-generated scope; if it's worth doing, it's a separate punch-list item.
- ❌ Any new tooling (link checker, freeze test, hook) — accepts outside-view's modal-failure forecast as a known risk; mitigation, if needed, will arrive as a new punch-list item triggered by actual erosion, not by anticipated erosion.
- ❌ Any policy declaration about session-artifact immutability — explicit non-action.

## What this commit's blast radius actually is

Five string substitutions in two README files. Reversibility: full, single `git revert`. Worst case: a fifth string-substitution typo, caught immediately by a `ls`-the-target verification before commit (the plan's existing Done-when #2-3 cover this).

## Named tradeoffs

| Choice | Wins | Loses |
|---|---|---|
| Collapse to one commit | Honest response to operator's actual ask; no manufactured WIP | The 7 session-artifact references stay broken; no policy declaration |
| Drop the 5th line-138 edit | Doesn't touch an off-limits file; doesn't introduce a parenthetical that may stale-out | The dogfood entry continues to name an old path inline; future readers must follow the migration table to find it |
| Drop the `redirects.md` proposal | Doesn't add an architectural primitive on the back of a 4-edit cleanup | Misses an opportunity to prevent the next round of stale-reference accumulation; punch list takes the hit instead |
| Use existing file-relative style | Doesn't pre-decide item 1; matches surrounding lines | Known re-touch when item 1 lands; ~5 minutes of restyle work later |
| New punch-list item 14 instead of inline policy declaration | Respects the operator's chosen intake surface; surfaces the question without forcing it | Introduces a new line on a list that's already 13 long; risk that item 14 is never addressed |

## Named assumptions (any one wrong flips the recommendation)

1. **The operator's "best you think to approach this item" was permissive of restructuring the *plan*, but not of restructuring the *deliverable*.** Evidence supports: the operator routed the plan through the pipeline rather than asking me to ship; that signals "improve the plan, then we ship." If wrong (operator wanted the workflow to autonomously *make* the policy decision), commit A is incomplete and a v3 candidate with explicit policy ownership is needed.
2. **Adding an item to the punch list is a lower-friction surface for the policy question than committing a one-line policy declaration.** Evidence supports: the operator authored the punch list as their planning surface and is using it sequentially. If wrong (operator considers the punch list cluttered and would prefer an in-line decision), the policy should be settled in a commit message instead.
3. **The 5th edit at line 138 is *not* in the operator's mental scope for item 3.** Evidence supports: the original plan explicitly placed it out of scope; the operator did not contradict that placement when asking me to "pick up" item 3. If wrong (operator expects all 11 references addressed), candidate v2 underdelivers and the line-138 parenthetical should return.
4. **No new tooling within item 3's commit is the right call.** Evidence supports: scope-map flagged the absence of tooling as a `conflict`, but converting that into a new tooling primitive in this commit is exactly the workflow-generated scope the critics rejected. If wrong (the absence is acutely painful), the same fix can be filed as new punch-list item 15 ("link-validation tooling for active surfaces").

## Named ways this could be wrong

1. **Wrong on the operator's frame.** If the operator wanted a 5-edit comprehensive sweep and the workflow under-delivers because critics over-corrected against loop 1's scope, candidate v2 has whiplashed too far. Mitigation: synthesis (step 12) presents both candidate v1 and v2 explicitly and lets the operator choose, rather than presenting v2 as "the answer."
2. **Wrong on the punch list as venue for the policy question.** The punch list is currently a list of *concrete cleanup tickets*. Adding a "decide a policy" item changes its character. If that change is unwelcome, item 14 sits awkwardly forever.
3. **Wrong to drop the redirects-file alternative entirely.** Architecture lens specifically named it as the alternative most directly motivated by the symptom class. Filing it as a new punch-list item (15? 16?) is honest scope-routing; *not filing it at all* is the failure mode.

## How this candidate addresses the original frame-level objection

[Loop-1 critiques](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/critiques.md) converged on: *"the candidate over-engineered a small operator ask into a multi-commit choreography that bills the operator for findings the workflow surfaced."*

This v2 collapses to one commit. The findings (policy, redirects, tooling) are surfaced as **new punch-list line items**, not as deliverables in commit A. The operator can scan the new items and ignore, defer, or schedule them — same as for any other punch-list item. The workflow has done its job (find the concerns) without claiming authority over the operator's worklist.

This is the "responsive shape" product lens named at the end of its critique: *"4 edits + delete Done-when #5 is the responsive shape; everything beyond that is the workflow billing the operator for its own findings."* Plus the punch-list filing for surfaced concerns, which is operations lens's "concrete fix at zero cost."

## Single biggest uncertainty

Whether the operator wants the surfaced concerns (policy, redirects, tooling) **filed as new punch-list items** (this candidate) or **left entirely unfiled** (a more aggressive collapse where the workflow's findings live only in the session artifacts under [`.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/`](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/) and never enter the punch list).

**Cheapest experiment:** the synthesis (step 12) shows the operator both shapes — "file as items 14, 15" vs. "log only in session artifacts" — and lets them pick at presentation time. Both options are 30-second decisions; whichever they pick, candidate v2 ships in under 5 minutes.
