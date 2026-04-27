# Candidate recommendation — folder-shape depth bug fix (item 2)

## Position

**Bundle punch-list items 2 + 3, but only inside the punch-list's already-named scope (4 files, 3 of which already authored by the operator under item 3). Do not extend to agent-discovered files. Wait for item 1 to commit before shipping item 2. Use a one-shot grep verification, not a CI link-checker.**

The work is:

1. Wait for item 1 to be decided & committed (CLAUDE.md updated, `.claude/commands/upgrade.md` updated). Then under the in-force rule:
2. Rewrite every broken `../`-chain link in `upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md` (14 links) to repo-root-relative form.
3. Rewrite every broken `../`-chain link in `upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md` (12 links).
4. Fix the one item-3 occurrence in `upgrades/normal/2026-04-26-living-poweruser-knowledge-module/README.md` L48 (already named by the operator under item 3).
5. Run a one-shot grep across `upgrades/*/*/README.md` for residual `../../` chains and `\(\.\./\.\./\)` patterns; fix any typos surfaced.
6. Commit as one diff with a message that names items 2 and 3 closed.

That is **27 link rewrites across 3 files**. Counted from the per-file tables in [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md), not the summary count.

## What this candidate explicitly does NOT do

- **Does NOT extend to `upgrades/profound/2026-04-27-r-and-d-lab-thesis/README.md`** (mixed depth — Explore-discovered, not punch-list-named). Frame-challenger is right: agent-discovered scope ≠ human-authored scope. Surface it as a separate punch-list addendum or leave for the next sweep.
- **Does NOT ship `bin/check-path-discipline.sh`**. That is item 1's plan §Step 6 territory. Bundling a permanent CI artifact into a content-fix commit violates Release Simplicity (canon §inferred §3) more sharply than co-located link edits do.
- **Does NOT touch session-artifact files**, even those with the same bug. Commit `5108ed3` and [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) explicitly forbid style-editing them.
- **Does NOT modify `.claude/commands/upgrade.md`**. That is item 1's plan §Step 2 territory.
- **Does NOT proceed before item 1 commits.** Inverting that gate (per frame-challenger's "force item 1's hand by demonstrating the cost") trades certainty about correct fix-form for a rhetorical point.

## Addressing the frame-challenger's frame-level objection

The challenger asked: *"Why does this 30-link fix warrant the 12-step apparatus rather than a literal punch-list-line execution that preserves operator attention for items 4–13?"*

**Direct answer:** Strictly on the merits of the fix itself, the apparatus is over-applied — a literal mechanical fix would close the punch-list line in 30 minutes. The pipeline produced two pieces of value the literal execution would not have:

1. The **scope clarification** (items 2 and 3 are co-located in 2 of 3 files; bundling is colocation-coherent, not scope-creep). Without the scope-map and frame-challenger, the natural agent move was either (a) extend to all surfaced files or (b) ship the literal mechanical fix as written. Both are wrong; the right answer is in between, and the pipeline surfaced it.
2. The **item-1 sequencing constraint** made explicit. A literal execution would have proceeded under whichever option the agent's reflex chose (likely option B since it matches the punch-list's wording), risking a re-do.

The challenger's frame ("preserve operator attention for items 4–13") is correct in the limit — running the pipeline on every punch-list line *would* be the failure mode. The defense for running it on item 2 specifically: item 2 is the first item that actually depends on a not-yet-committed decision (item 1), and that dependency is invisible without the scope-map. Items 4-13 are independent per the punch-list's own sequencing note ("After [items 1-3], items 4 onward are independent and can be reordered freely") — the apparatus need not run on each of them.

**Concession to the challenger:** the orchestrator should not run the full 12-step pipeline on items 4-13 unless one of them surfaces a similar hidden dependency. Default to literal execution for those.

## Tradeoffs

| What we get | What we give up |
|---|---|
| Items 2 and 3 both closed in one commit. | Bigger diff than literal item 2 alone. |
| 27 link rewrites under one rule, no half-migration risk in the affected files. | Living-poweruser file gets edited under item 2's commit, blurring the items-2-vs-3 boundary in git history (mitigated by commit message naming both). |
| Honors item 1's regime by bringing 3 violators into compliance with the existing CLAUDE.md L7-16 rule. | Locks item 2 to item 1's commit timing — no parallel progress. |
| Surfaces and explicitly *defers* the r-and-d-lab-thesis mixed file as a separate concern. | Leaves a known partial-broken file in the active surface until a future sweep. |
| Falsifiability via one-shot grep, no new CI surface. | Recurrence prevention is item 1's job, not item 2's — if item 1 ships without the `/upgrade` patch, the bug class returns. |

## Named assumptions (any of which would flip the recommendation)

1. **Item 1 will commit Option A within the same operator session.** If item 1 stalls (operator is unsure between A and B for >1 week), the right move flips to "ship item 2 under literal mechanical fix per punch-list wording (Option B form), and let item 1's eventual decision either subsume or re-do this work." Waiting indefinitely on item 1 with item 2 staged-but-uncommitted is the worst of both worlds.

2. **The 27 hand-edited link rewrites have a typo rate ≤2.** Per outside-view §inferred §5, hand-edited 30-link batches typically have 1-2 typos. The grep verification step catches residual `../../` patterns but not new typos in the rewritten paths (e.g., `..claude` vs `.claude`). If typo rate is materially higher than expected, the recommendation flips to a `sed`-driven mechanical rewrite with diff review, not hand edits.

3. **No third folder-shape migration is anticipated within the punch-list horizon.** Per frame-challenger's falsifier — the "migration durability" justification for the wider sweep is weak if folder reshapes don't recur. This assumption is *implicit* in the recommendation: the candidate is sized to current breakage, not to recurrence prevention. If the operator confirms a third reshape is planned (e.g., `<slug>/README.md` → `<slug>/index.md`), the recommendation expands to also extend to the r-and-d-lab-thesis file and to ship `bin/check-path-discipline.sh` with this commit, not item 1's.

## Named ways this could be wrong

- **The frame-challenger's "honor the punch-list narrowness" frame might be the right one.** Under that frame, items 2 and 3 should be two separate commits even though their files overlap, because the punch-list author wrote them as separate lines. The candidate bundles them; this is a frame-level disagreement the orchestrator chose to override on the grounds that colocation is coherent, but the override could be wrong.
- **Inverting item-1 gating could be the better call.** If the operator is genuinely undecided between Options A and B in item 1, demonstrating the cost of B by executing item 2 in its B-form (15 link edits as written in the punch list) would surface the recurrence cost concretely. The candidate forecloses that demonstration.
- **The grep verification might miss the failure mode that actually fires.** The typical Option-A failure (per outside-view §4) is partial migration — links inside code fences or HTML comments. A grep over the file body catches them only if the residual chain pattern matches. Markdown link checkers (markdownlint, lychee) would catch resolution failures, not pattern presence; the grep-only approach trades a structural check for a syntactic one.
- **The session-artifact sanctity rule may be over-applied.** The rule forbids "noise pruning" but item 2's edits are structural correctness, not noise. If the operator reads the rule as permitting depth-bug fixes in session-artifacts, the candidate's exclusion of those 7 occurrences is too conservative. The candidate sides with the rule's literal text; the orchestrator does not have authority to relax it.

## Cheapest experiment that would reduce the biggest uncertainty

The biggest uncertainty is assumption #1 (item 1's commit timing). Cheapest experiment: **ask the operator directly — is item 1's option-A recommendation acceptable, and can it commit before item 2?** A one-line confirmation collapses the conditional shape of the requirement and unblocks item 2 as written. If the answer is "no, I'm still deciding," the candidate's own assumption #1 forces a flip to the literal mechanical fix.

Second-cheapest: **run the proposed grep verification against the current state of the repo** — if it already surfaces residual patterns the Explore audit missed, the typo-rate assumption (#2) is falsified before any edit.

## Done when

- Item 1 is committed (CLAUDE.md and `/upgrade` updated per its plan §Steps 1-2).
- Three files are edited per the per-line tables in [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md): critics-get-write-tool/README.md, workflow-docs-scattered-and-stale/README.md, living-poweruser-knowledge-module/README.md.
- The grep `grep -rn '\.\./\.\./[^/.]' upgrades/*/*/README.md` returns no matches in the three edited files.
- Punch-list is updated: items 2 and 3 marked `✅ done <YYYY-MM-DD>`. The r-and-d-lab-thesis mixed file is recorded as a new punch-list entry (not closed).
- Commit message names items 2 and 3 closed and references the session-artifact dir [`.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/`](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/).
