# candidate.md — item 13 (orphans fate)

## Position

**No new policy primitive. Per-orphan dispositions, with one extract-then-replace and one rename-with-status-header rather than four blanket deletes. Discoverability addressed in-tree via this plan + a punch-list footer, not via an archive folder or a CLAUDE.md rule.**

Concrete dispositions:

| orphan | disposition | one-line rationale |
|--------|-------------|--------------------|
| O1 — [prompts/five-pressures.md](../../../prompts/five-pressures.md) | **extract-then-delete** | Port pressure #2 ("Enumerate-before-select: list ≥3 candidate solutions") into [CLAUDE.md](../../../CLAUDE.md) step 9 (generator) — it is the only one of the five not covered by 12-step. Then delete the file. |
| O2 — [prompts/ultraplan-next-level.md](../../../prompts/ultraplan-next-level.md) | **delete** | Pure frozen-evidence; the brief's outputs are the punch-list and per-item plans, both already in-tree. Recovery via `git show <sha>:prompts/ultraplan-next-level.md`. |
| O3 — [plans/ok-cool-this-is-warm-balloon.md](../../../plans/ok-cool-this-is-warm-balloon.md) | **rename in place + Status header** | `git mv plans/ok-cool-this-is-warm-balloon.md plans/2026-04-24-phase-2-shipped.md`; prepend a one-line `> **Status:** shipped 2026-04-24, retained as design-record (alternatives-not-taken).` This is the only orphan whose content captures *rejected alternatives* — discoverable from `ls plans/`, no new folder. |
| O4 — [.claude/session-artifacts/exemplars/](../../exemplars/) | **defer to item 5** | Disposition is contingent on item 5's outcome (repair the promotion mechanism → folder stays; abandon → folder goes). Do not pre-empt. |
| P — standing policy | **do not write** | The combination of git history + LEDGER + session-artifact immutability + this plan + the punch-list footer covers the case at N=4 with no recurring cadence. A CLAUDE.md rule inherits unmaintained-policy failure modes. Demonstrate by example, not by promotion. |

The discoverability gap raised by the frame-challenger (git is for recovery, not discoverability) is addressed by **two in-tree breadcrumbs that already need to exist**: this candidate's eventual synthesis (preserved as a session-artifact, immutable, dated) and a one-line footer on punch-list item 13 ("Removed five-pressures.md, ultraplan-next-level.md in commit `<sha>`; renamed warm-balloon to 2026-04-24-phase-2-shipped.md; rationale in session 2026-04-27-item-13-orphans-fate."). Six months later, `ls .claude/session-artifacts/ | grep orphans` and `grep "item 13" plans/*.md` both find the answer in <30 seconds without prior knowledge of any deleted filename.

## Addressing the frame-level objection

The frame-challenger's load-bearing objection: *"Git history is a venue for recovery, not discoverability; deletion silently degrades the ability to answer 'why' six months later."*

Three responses, in order of weight:

1. **The session-artifact directory is the discoverability venue, not git.** [.claude/session-artifacts/2026-04-27-item-13-orphans-fate/](.) (this directory, immutable per the README) lands in the tree and stays there. Anyone reading the repo six months from now sees `ls .claude/session-artifacts/` includes a directory named "orphans-fate" — that is browseable without prior knowledge of which files were deleted. The frame-challenger's premise (git as the venue) is not the only candidate; the session-artifact convention is in-tree, immutable, and date-indexed. This is using a primitive the repo already has, not inventing one.

2. **One orphan (O3, warm-balloon) is preserved-with-header precisely because of this objection.** The frame-challenger correctly noted that commit messages capture what was done, not what was rejected; the warm-balloon plan's "Phase 2 SOTA upgrade (pragmatic cut) … Ultraplan's full output is competent but over-engineered" *is* the rejected-alternatives record. Renaming with a Status header keeps that record discoverable from `ls plans/` and accepts the frame-challenger's argument for that one orphan rather than overruling it.

3. **Falsifier accepted.** If a future LLM session, given the question "why was five-pressures replaced," cannot reconstruct the answer in <2 minutes from `ls .claude/session-artifacts/` + this plan + punch-list item 13 footer, the candidate is wrong and the in-tree breadcrumb file (`prompts/RETIRED.md` or equivalent) becomes warranted. The cheapest experiment that would test this is in §Cheapest experiment below.

## Named tradeoffs

- **Per-orphan asymmetry vs. uniform rule.** Treating four orphans non-uniformly (extract / delete / rename / defer) is more thinking-per-orphan than "delete all four, ship a CLAUDE.md rule." Trade: ~30 minutes of one-time analysis vs. avoiding a rule that will likely be wrong for orphan #5 (whose shape we cannot predict).
- **Discoverability via session-artifact vs. via in-place breadcrumb file.** Session-artifact is *one level removed* (you find it by browsing session-artifacts, not by browsing the directory the file lived in). An in-place `RETIRED.md` would be more direct but creates a new convention. Trade: indirection (low cost in a repo with N=21 session directories) vs. new primitive (cost paid forever).
- **Renaming O3 in place vs. moving to `plans/shipped/`.** A `plans/shipped/` subfolder is a new primitive; renaming with a header is not. Trade: less visual separation between in-flight and shipped plans (header line is the only signal) vs. no new directory convention to maintain.
- **Extract-then-delete (O1) vs. keep-in-place (O1).** Extracting pressure #2 into CLAUDE.md is a one-line addition that touches the most-referenced doc in the repo. Trade: small CLAUDE.md churn now vs. forever-redundant 37-line file pointed at by no live reader.

## Named assumptions (≥3 that would flip the recommendation)

1. **Five-pressures coverage by 12-step is 4-of-5, with #2 (enumerate-before-select) the only gap.** Verified by grep of CLAUDE.md and agent files: the 12-step requires ≥3 *uncertainties* (CLAUDE.md:62) and ≥3 *flippable assumptions* (CLAUDE.md:74), but does not require ≥3 *candidate solutions* before selection. If on closer reading another pressure is also uncovered (e.g., consequence-imagine's "which system breaks first, detected by whom" is more specific than step 12's "cheapest experiment"), the extraction is incomplete and either CLAUDE.md gets multiple amendments or O1 stays.
2. **Sweep cadence is annual or slower.** Outside-view's base rate (option a below threshold) assumed first sweep. If the next sweep happens within 6 months, the policy primitive moves toward base rate and "no rule" loses its strongest argument. The session-artifact directory shows multiple 2026-04-27 sessions — that is one sweep day, not necessarily one sweep cadence; flag for verification.
3. **`plans/` convention tolerates a dated-shipped file alongside in-flight items.** I am asserting `plans/2026-04-24-phase-2-shipped.md` reads as "shipped" by virtue of the Status header and the date being older than the in-flight 2026-04-27 items. If readers parse `plans/` as strictly in-flight (and a Status header is invisible to that parsing), the rename is the wrong move; the right move is a `plans/shipped/` subfolder (which is a new primitive) or deletion (which loses the alternatives-not-taken record).
4. **The session-artifact directory is enough discoverability venue.** I am asserting that "session 2026-04-27-item-13-orphans-fate" is browseable enough to count as the in-tree breadcrumb. If a future maintainer's first instinct is `find . -name "*pressures*"` (which finds nothing post-deletion) rather than `ls .claude/session-artifacts/`, the breadcrumb fails. This is the falsifier in the cheapest experiment.
5. **Item 5's resolution does not pre-empt this.** Deferring O4 assumes item 5 will be decided in its own session and that the deferral is honored, not silently overridden. If item 5 is also deferred, O4 stays unresolved indefinitely and `exemplars/` becomes the smallest possible orphan-of-orphans.

## Named ways this could be wrong

- **The frame-challenger's "the orphans are the policy" frame might be the right frame, in which case my candidate is on the wrong frame.** I considered it and rejected it: the warmth of "exhibit rather than dispose" is appealing but assumes a reader who values teaching surface enough to wade through 26 KB of an external-agent brief. At N=4 with one maintainer, the marginal teaching surface per orphan kept is low. But this is a taste call, not a derivable one — if the maintainer's actual values lean exhibit-over-tidy, my candidate is mis-calibrated.
- **Pressure-#2 extraction may not hold up under critic-panel scrutiny.** "Enumerate ≥3 candidate solutions" added to CLAUDE.md step 9 may be redundant with what the generator already does in practice (the position/tradeoffs/assumptions structure implicitly enumerates), or may add ceremony that slows every future session for a benefit that is unmeasurable. The architecture critic may catch this.
- **Renaming O3 may not survive the operations lens.** Operations critic may note that `git mv` of a load-bearing plan file breaks any external links (e.g., from the punch-list, from item-01 plan, from session-artifacts that quote it by name). The dependency-direction question — who points at this file — was not exhaustively grepped before deciding to rename.
- **Deferring O4 may be the comfortable cop-out.** The product critic may rightly say that deferring to item 5 leaves the punch-list with one item perpetually open; a real disposition (delete-the-keep-file-recreate-if-ever-needed) would close item 13 cleanly. My deferral preserves the dependency in scope-map but does not resolve it.
- **The frame-level objection may be insufficiently addressed.** The session-artifact directory as discoverability venue assumes future readers know to look there. If that assumption is wrong (and the falsifier in the cheapest experiment confirms), an in-tree breadcrumb is needed and "no new primitive" was over-claimed.

## Cheapest experiment that distinguishes (success vs. failure)

**The 6-month future-session test.** In ~6 months (or whenever a new design question surfaces in this stack), pose to a fresh Claude Code session in this repo: *"Did this repo ever have a checklist called 'five-pressures'? If so, why was it removed?"* Score:
- **Pass (candidate validated):** session reconstructs the answer in <2 minutes using `ls .claude/session-artifacts/` → finds `2026-04-27-item-13-orphans-fate` → reads the synthesis or this candidate.
- **Fail (frame-challenger validated):** session cannot find the answer without being told to look in session-artifacts; instinct is `find` or `git log` of a path it does not know exists. In that case, retroactively add a `prompts/RETIRED.md` (or equivalent) breadcrumb, and amend the policy stance.

This is cheap because it is one prompt to a future session at near-zero cost; it is the right experiment because it directly tests the load-bearing assumption (session-artifact discoverability) without requiring any pre-commitment to either outcome.

## What the candidate explicitly does *not* do

- Does not create `prompts/RETIRED.md`, `archive/`, `attic/`, `plans/shipped/`, or any new directory.
- Does not amend CLAUDE.md beyond a single one-line addition to step 9 (generator) requiring ≥3 candidate solutions before selection.
- Does not pre-empt item 5; O4 stays in conflict-status until item 5 lands.
- Does not delete `prompts/` even though both its files are leaving — leaves the empty directory in place for ~one sweep cycle as a passive signal that the convention is dormant; if no new prompt files arrive by the next sweep, delete then.
