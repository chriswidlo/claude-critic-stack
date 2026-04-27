# Requirement classification — item 3 (pre-folder-shape `.md` references)

## The question (orchestrator-condensed)

Item 3 of the repo cleanup punch-list ([`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md):55-77) catalogues 11 locations referencing upgrade entries by their pre-migration flat-file path (`upgrades/<tier>/<slug>.md`). All entries migrated to folder shape on commit `c2fe604`; the flat files no longer exist.

Draft plan ([`plans/2026-04-27-item-03-pre-folder-shape-paths.md`](plans/2026-04-27-item-03-pre-folder-shape-paths.md)) splits the 11 into:
- **4 active-surface locations** (under `upgrades/`) → fix mechanically; don't touch link style (item 1's job).
- **7 session-artifact locations** → leave alone, citing commit `5108ed3`.
- **1 self-quoting historical entry** → leave (path is the subject of the sentence, not a navigational link).

Plan deliberately stays narrow: doesn't bundle with item 2 (depth bugs in same files), doesn't fix link style. Each item gets its own commit with its own stop-condition.

## Primary label

**refactor**

## Default frame (from label)

What observable check confirms the post-edit links resolve to the *same conceptual targets* the pre-edit links *intended* to reach, not just to files that happen to exist? Refactor with a behavioral check (link resolution + target-identity grep), not just "the markdown still parses."

## Known frame bias

Calling a behavior change a refactor. The plan describes itself as a small mechanical fix, but it's also implicitly *deciding policy* on session-artifact immutability — making the strict reading of commit `5108ed3` binding. That's a normative act (it constrains all future cleanup sweeps), not a mechanical edit. The refactor frame will encourage waving past that policy decision because "we're only changing 4 link targets."

## Secondary label

**replace** — not for the link edits themselves, but for the implicit primitive being replaced: the *interpretation* of `5108ed3`'s "privacy redaction only" rule. The plan replaces a permissive reading (mechanical fixes OK) with a strict reading (don't touch session artifacts at all) and bakes that into precedent via Done-when condition #5.

## Alternative classification

**investigation** would become primary if the operator hasn't decided between strict and permissive readings of `5108ed3` and the real ask is *"which reading governs?"* rather than *"apply the strict reading."* The plan's "Single biggest uncertainty" section explicitly poses this as an open question with a "cheapest experiment: ask the operator" — the tell that an investigation is hiding inside a refactor wrapper.

## User's framing words (and what they presume)

- *"small mechanical fix (4 link-target edits)"* — presumes refactor.
- *"splits the 11 locations into… → fix mechanically"* — presumes work is already classified and only execution remains.
- *"Plan deliberately stays narrow: doesn't bundle with item 2… doesn't fix link style"* — presumes scope is settled; invites pipeline to validate rather than question.
- *"refactor with a hidden replace inside it"* — operator has pre-labeled this; classifier should not rubber-stamp. The hidden replace is the policy-binding move on session artifacts; deserves scope-mapper attention in step 7.

What would change the classification: if operator says "I want a ruling on the session-artifact policy first, then the edits follow" → `investigation` primary. If operator says "the policy is already settled by `5108ed3`; just execute" → `refactor` stays primary, `replace` collapses.

## Gaps for downstream steps to address

1. **Is the strict reading of `5108ed3` actually settled, or is this plan the first time it's being made binding?** The commit text is one sentence; the plan extrapolates a categorical rule. Downstream (esp. step 7, step 8) needs to know whether the policy is being *established* here or *applied* here.
2. **Does "session artifact immutability" cover only prose, or also broken markdown link syntax?** The punch list itself draws a line at "click-broken markdown link syntax" being fixable; the plan moves the line to "don't touch at all." Which line governs is unspecified.
3. **What is the cost of a click-broken link in an immutable artifact, in operator-time?** Plan asserts it's "one click that doesn't navigate" — no measurement. If artifacts are read often, the cost compounds; if write-only diagnostic data, near zero. Frame depends on this.
4. **Does the "don't bundle with item 2" stance survive contact with item 2's actual scope?** Both touch `2026-04-26-critics-get-write-tool/README.md`. Two commits to same file in sequence is fine; parallel branches editing same lines is not. Sequencing constraint unstated.
5. **Edit 4's coordination with item 6** (supersession of `agentic-engineering-reference-library`). Plan accepts "wasted 30 seconds" as worst case. If item 6 *renames* or *moves* the target, edit 4 may need a third revision. Coupling acknowledged but not bounded.
6. **Is there a 12th instance?** Plan's risk #4 names this and proposes "a final pass with a broader regex" — but doesn't specify the regex. Downstream critic-operations should name the exact grep.
