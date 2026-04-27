# Product critique — folder-shape depth bug fix (item 2)

## Verdict
**rework**

## User-visible consequence
The operator opens [`upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md`](upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md) tomorrow and finds that **clicking a link no longer works** — where today (under broken `../../`) some links happen to resolve to the wrong-but-existent target, post-fix every in-repo reference is a repo-root path that the markdown previewer treats as a non-clickable text address. Three of the most-trafficked active-surface entries flip from "links sometimes click into a wrong place" to "links never click; they are addresses you copy." This is *intended* under Option A but the operator has not yet experienced it on entries they read regularly.

A second visible change: the punch-list itself ([`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md)) gets two lines marked done by one commit, AND a *new* line added (the deferred r-and-d-lab-thesis mixed file). Net −1 but the operator sees a new entry where they expected only deletions.

## Commitments implied
- **Bundling-by-colocation as precedent.** Once items 2+3 ship together "because two of three occurrences share files with item 2's targets," every future punch-list pair with file overlap pulls on this precedent. Items 6 and 7 both touch overlapping file sets. The candidate's disclaimer lives in a session-artifact, not in the punch-list. Operator memory is the only enforcement.
- **Option A as ratified-by-action.** Shipping item 2 in repo-root form with item 1 still uncommitted is a soft pre-commitment. Item 1 becomes harder to resolve to Option B because doing so invalidates the just-landed ship. Candidate gates on item 1 *committing* before item 2 ships, but the order is "item 1 first, then item 2, same session" — operator signs item 1 under pressure of an already-staged item 2 diff.
- **The "deferred punch-list addendum" pattern.** Recording r-and-d-lab-thesis as a new punch-list entry instead of fixing it commits the operator to a punch-list-as-living-document model where agent-discovered work appends to the human-authored list. **Model change** for the punch-list as a product surface (it was a pre-committed, finite scope contract; it becomes an open backlog).

## Migration burden
- Operator: read item 1's plan → decide A vs B → commit item 1 (CLAUDE.md + `.claude/commands/upgrade.md`) → review item-2 diff (3 files, 27 rewrites) → update punch-list (2 done-marks, 1 new entry) → commit. Five distinct review/decision contexts in one session.
- Future agents reading the three edited entries see repo-root paths and must not "helpfully" rewrite them to clickable form. Three files become highest-density exemplars of the rule applied to entry bodies.
- Punch-list edits: items 2 and 3 done-marks per "How to use this list" L257-265 template; r-and-d-lab-thesis appended in a format not specified.

## Product affordances better / worse
**Better:**
- Three highest-traffic entries become grep-stable.
- Diff-bisectability for these three files improves: future moves do not invalidate their links.
- Three concrete proof-points in active-surface entries that the rule is in force.

**Worse:**
- Click-to-navigate from inside these three entries dies. If operator's workflow relies on click-through, three files lose that affordance while the rest of the repo retains it. **Repo becomes inconsistent in click-affordance** in a way it currently is not (today: most things click or are obviously broken; post-ship: three files are deliberately non-clicking by policy).
- Operator loses ability to use these three entries as "click around to understand" surfaces. Read-only address sheets.
- "Deferred to a new punch-list entry" pattern prunes the affordance "the punch-list is a finite, completable contract."

## Frame-level objection
The candidate frames its defense around "item 2 has a hidden dependency on item 1, so the apparatus was warranted." From a product lens, that defense is beside the point. **The product surface here is the operator's attention budget across the full 13-item list, and the candidate's own concession ("don't run the apparatus on items 4-13") concedes the apparatus is not the right tool for the surface.** What the operator experiences on ship-day is not "the apparatus surfaced a hidden dependency"; it is "three entry bodies I read regularly now behave differently from the rest of the repo, and my punch-list grew." The frame-challenger's frame ("operator attention is the product") is the correct product frame, and the candidate's response — "we ran it for item 2, we won't for items 4-13" — accepts the frame in principle while violating it in this commit. **Product question the candidate does not answer:** *what does the operator gain on ship-day, in their reading workflow, that justifies the asymmetry between these three files and the rest?*

Second objection: candidate treats the punch-list as a process artifact (something to mark done) rather than as a product surface (something the operator reads to know what's left). Adding r-and-d-lab-thesis as a new line is process-coherent ("don't lose the finding") and product-incoherent ("the list the operator pre-committed to is no longer the list").

## Flip-to-approve conditions
(a) Drop the r-and-d-lab-thesis "new punch-list entry" — either include it in this sweep (uniformity over fidelity is the right call when the alternative is appending to a contract) or genuinely defer it without modifying the punch-list, AND (b) state in the commit message and in the punch-list line itself that bundling-by-colocation is a one-time exception for items 2+3, not precedent for items 6 or 7. The link-rewrite work itself is fine; the punch-list-as-product mutation is what needs rework.

## v2 review

**Verdict: approve**

### Flip-condition (a) — r-and-d-lab-thesis disposition
Partially addressed. v2 picks "genuinely defer without mutating the punch-list" and routes the finding through the commit message. Right *direction* — punch-list-as-finite-contract preserved, no agent appending to a human-authored list. v2 itself names the weakness: the operator may not see it weeks later when triaging. The commit message is a write-once, search-only surface; punch-list triage will not encounter it. *Strictly weaker* tracking surface than the punch-list, but the *correct* surface given the alternative violates a stronger product invariant. Net: I accept this trade.

### Flip-condition (b) — bundling-by-colocation as one-time exception
Addressed. §Position step 7 commits the disclaimer to the commit message. Text, not enforcement (v2 names this). Items 6/7 cannot pull on the precedent without an operator who chooses to ignore both sites.

### New product risks introduced by v2
1. **`bin/check-path-discipline.sh` is a sixth review context.** My v1 burden listed five; v2 adds review-the-script + accept-as-committed-code-that-future-agents-modify. Ships *new executable surface* on a session supposed to close two punch-list items.
2. **Script-class failure replaces line-class failure.** A hand-edit typo produces one broken link found on next read; a script bug produces 27 consistently-wrong links that may all pass the resolution check (existence, not intent). v2's mitigation puts human judgment back in via the per-link table — but the operator now reviews that table too. Seventh review context arguably.
3. **Ship-day operator experience unchanged in the dimension I cared about.** Same three files behave differently from the rest of the repo, plus a new `bin/` script, plus a one-line out-of-scope finding in commit message no surface tracks. Asymmetry is unchanged; v2 adds tooling without changing what the operator *reads*.

### Verdict sentence
Approve. The two flip conditions are met (one cleanly, one with acknowledged-weak deferral surface that is nonetheless the right trade). New risks live in architecture/operations lenses — script-as-shipped-artifact and script-class failure are not product-surface harms to the operator's reading workflow. Reverts to `rework` if operator's stated workflow excludes git-log review during punch-list triage.
