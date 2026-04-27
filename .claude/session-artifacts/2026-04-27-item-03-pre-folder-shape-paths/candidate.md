# Candidate recommendation — item 3 (pre-folder-shape `.md` references)

**Loop:** 1 (pre-critic-panel).
**Authoring frame:** *honest collapse* — the split frame is fictional per [challenges.md §"Challenge to the split frame itself"](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/challenges.md). This candidate either commits the policy or removes the policy from the commit; it does not pretend the policy can ride along quietly.

## Position

**Ship the 4 active-surface edits as a single commit. Strip the implicit policy declaration out of that commit entirely. Queue the session-artifact policy as a separate question — but answer it cheaply now, not later, by amending [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md):45-51 in a *separate* commit *only if* the operator confirms the strict reading.**

Concretely:

- **Commit A (this session, low risk).** Apply edits 1–4 from the original [plan](plans/2026-04-27-item-03-pre-folder-shape-paths.md) (the 5 path-suffix substitutions in the 2 active-surface READMEs). Ship as a child of `c2fe604` per the alternative frame ([challenges.md §"Alternative frame"](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/challenges.md)) — name `c2fe604` in the commit message as the parent migration this completes. Do **not** include a Done-when condition that asserts session-artifact non-modification; that is what makes the policy ride along silently.
- **Commit B (operator decision required, separate session, optional).** If operator confirms the strict reading: append one sentence to [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md):45-51 stating that broken cross-references are a known consequence of the immutability rule and are not to be repaired retroactively. If operator confirms the permissive reading: instead, fix the 4 broken links inside session artifacts (leave the 3 prose mentions alone — those are content, not navigation), and explicitly note the precedent.
- **Commit C (deferred to item 1 or its successor, not this session).** When item 1 lands, restyle the 4 lines of commit A to whichever path style is chosen.

This is *not* the split frame. This is the split *commits* — the policy decision is genuinely deferred because it has its own commit envelope, not because Done-when #5 hides it inside this one.

## Revisions to the original plan

1. **Delete Done-when #5** ("No session-artifact file is modified by this commit") from the plan's stop-conditions. Replace with: *"This commit touches no session-artifact files. That is a property of the edit set, not a policy assertion."* The change is one of provenance, not behavior — same files untouched, but the act of not touching them does not establish a rule.
2. **Reframe the plan's "Two surfaces, two policies" section** as "Two surfaces, one set of edits this commit." The 7 untouched references are noted as out-of-scope-for-this-commit, with a pointer to commit B (operator-decision-pending) — not as policy-fenced.
3. **Address line 138 explicitly.** Per [challenges.md §"Self-quoting occurrence"](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/challenges.md), the preservation reason was weak. Adopt the challenger's suggestion: leave the prose unchanged but **append a parenthetical** so the line reads `Migrate `upgrades/no-brainer/2026-04-26-upgrade-entries-as-folders.md` (this entry — the dogfood — now at [`.../README.md`](upgrades/no-brainer/2026-04-26-upgrade-entries-as-folders/README.md))`. Cost: 60 seconds. Benefit: the historical record is preserved *and* a future reader following the path is forwarded to the live file. This is a 5th edit, not a deferred policy question.
4. **Rename "Edits 1–4" to "Edits 1–5"** in the plan body to reflect the line-138 addition.
5. **Add a `Done when` condition that addresses the outside-view's modal failure** — but with the frame-challenger's correction in hand. The outside-view's "fence leaks in 6–12 months" prediction is below base rate for this repo specifically (per [challenges.md §"Challenge to the outside-view"](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/challenges.md)). The mitigation is therefore lighter than outside-view recommends: append a single sentence to the commit message naming the 7 untouched references and the commit `5108ed3` rationale. No new tooling, no new file, no freeze-test. The repo's existing structural pressure (workflow routing + the README rule already in place) carries the rest.

## Named tradeoffs

| Choice | Wins | Loses |
|---|---|---|
| Three commits (A, B, C) instead of one | Clean stop-conditions, separate operator decisions get separate review surfaces, no silent policy bake | More commit overhead; risk that B and C never happen and the system sits half-done |
| Add 5th edit (line 138 forwarding parenthetical) | Preserves authoring context *and* forwards a future reader; honest answer to the challenger's preservation challenge | Touches a file the original plan said was off-limits; a tiny amount of "dogfood entry" semantic load is altered |
| No new tooling (no link checker, no freeze test) | Honors the frame-challenger's pushback on the outside-view's fence-leak forecast; no scope creep | Accepts ~20% rule-erosion risk if routing degrades; the prediction may turn out right |
| Defer style restyle to commit C / item 1 | Keeps each item's stop-condition clean; doesn't pre-commit to file-relative or repo-root | Known re-touch on the same 4 lines; if item 1 takes a month, edits stay in the "old style" until then |

## Named assumptions (any one wrong flips the recommendation)

1. **The operator's instruction "best you think to approach this item" was permissive of restructuring the plan, not just of executing it.** Evidence supports: explicit "best you think" wording. If wrong (operator wanted execution-only), the right move is to ship the original plan's 4 edits and note the workflow output as advisory rather than acting on it.
2. **The session-artifact immutability rule's reading is genuinely unsettled and not "obviously the strict one" to the operator.** Evidence supports: the punch list itself uses the permissive framing ("click-broken markdown link syntax" is fixable per [item 3, last bullet](plans/2026-04-27-repo-cleanup-punch-list.md):75); the plan moved the line; the operator has not signed off on either. If wrong (operator already considers it settled), commit B becomes irrelevant and Done-when #5 can stay; the candidate collapses to the original plan with line-138 addition.
3. **The frame-challenger's pushback on the outside-view ("fence leaks" is below base rate for this repo) is correct.** Evidence supports: the workflow structure exists, the README has the rule, agents route through pipelines. If wrong (the routing does not in fact suppress freelance edits as much as I'm assuming), the no-tooling decision is wrong and a freeze-test or hook should be added even at the cost of scope creep.
4. **Three small commits over a few days are not significantly costlier than one larger commit, in this repo's review process.** Evidence supports: solo-operator repo, no PR review overhead, git log already shows tight commit cadence. If wrong (e.g., commit-cost is non-trivial because each commit needs its own pipeline run), the candidate over-fragments and the original 1-commit plan is preferable.

## Named ways this could be wrong

1. **Wrong on the alternative frame.** If `c2fe604` is genuinely complete in the operator's mind and item 3 is just punch-list cleanup of orthogonal stale references, framing the commit as "child of c2fe604" misnames it. The cost is small (a slightly weird commit message), but the framing is doing real work — losing it loses the cleanest argument for skipping the policy declaration.
2. **Wrong on the line-138 fix.** If the dogfood entry's authoring context is *more* important than the challenger acknowledged (e.g., the entry is itself a teaching artifact about migration discipline, and modifying it teaches the wrong lesson), the 5th edit is a small unforced error. Mitigation: the parenthetical is additive; the original sentence reads identically before the parenthesis.
3. **Wrong on the cost of three commits.** Per assumption 4. If the operator experiences "commit B was never opened" as a hanging thread that bothers them more than "Done-when #5 silently set policy I'd already set anyway," the original collapsed-into-one approach is more honest *to the operator's actual preference structure*, even if structurally less clean.
4. **Wrong on the "no new tooling" stance.** Per assumption 3. Even with the frame-challenger's correction, if a single hook or check would be cheap (e.g., one bash line in `bin/`), the cost-benefit may favor adding it. The candidate punts; punting may be lazy.
5. **Wrong on routing.** If the operator's actual ask was just "do item 3, the workflow is overkill for this small a thing," all of this is over-built and a 5-line shell sed+verify would have been the right answer. The 12-step pass on a 4-line edit is itself a finding: small items may not need the full routing.

## How this candidate addresses the frame-level objection

The frame-level objection from [challenges.md §"Frame-level objection"](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/challenges.md):

> The split frame is fictional — the plan's Done-when #5 quietly ships the strict policy while the frame claims the policy is still open; the generator must either delete Done-when #5 (making the split real) or own the policy declaration explicitly (collapsing the split honestly), but cannot continue to do both.

This candidate **deletes Done-when #5** (revision 1 above) and explicitly **routes the policy decision to a separate commit B** (position §, bullet 2). The split frame becomes the split *commit envelope*. The policy is genuinely open after commit A; commit B happens only if the operator answers the question; absence of commit B means absence of declaration, not silent strict-reading bake.

This is the "delete Done-when #5 (split is real)" branch the challenger named. Not the "own the declaration" branch — because that requires an operator decision the orchestrator cannot make for them.

## Single biggest uncertainty

Whether the operator will read the three-commit structure as **"clean separation of concerns"** (the candidate's bet) or as **"unnecessary fragmentation of a 4-line cleanup"** (the candidate's risk). If the former, the structure pays for itself by keeping each decision auditable. If the latter, the operator wanted closure on item 3 and got an open thread (commit B) instead.

**Cheapest experiment to reduce this uncertainty:** ask the operator one binary question after presenting the synthesis — *"do you want commit B opened as a separate question, or do you want me to silently apply the strict reading and close item 3 in one commit?"* — and let the answer settle the candidate's structural choice without re-running any of the workflow.
