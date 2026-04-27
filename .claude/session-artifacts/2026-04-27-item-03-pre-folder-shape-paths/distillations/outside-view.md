## Source agent
outside-view

## Invocation summary
Orchestrator asked for reference-class forecast on Item 03 (pre-folder-shape paths cleanup): mechanical fixup of 4 active-surface path references, with a policy fence leaving 7 historical references broken in session artifacts. Subagent returned a split verdict: within tolerance for the 4 edits, below base rate for the policy fence.

## Direct facts
1. [outside-view §0] Canon manifest covers forecasting methodology (Kahneman/Lovallo 1993; Flyvbjerg 2006; Tetlock 2015) and migration/refactoring (Fowler 2018; Fowler 2004 StranglerFig; Feathers 2004). (confidence: direct)
2. [outside-view §0] Corpus directory is gitignored; subagent cited from manifest, not full-text passages (canon-stub citation only). (confidence: direct)
3. [outside-view §0] Declared canon gaps: no entry on post-rename cleanup of doc-graph references; no "broken windows" entry; no entry on referential integrity in document graphs / wiki link rot; no entry on "immutable historical record" policies for engineering artifacts. (confidence: direct)
4. [outside-view §1] Reference class settled: mechanical post-rename cross-reference fixup in a small (single-operator) doc repository with a self-imposed "don't rewrite history" rule and cleanup sequenced behind an unrelated style-policy decision. (confidence: direct)
5. [outside-view §1] Rejected reference classes: wiki link rot at scale, code rename refactoring, DB schema migration with deferred backfill. (confidence: direct)

## Inferred claims
1. [outside-view §2] Base rate for 4-edit bounded substance executed by single operator: ~80% clean within one commit, ~15% leave latent debt, ~5% fail outright. ±15pt uncertainty. (confidence: inferred)
2. [outside-view §2] Base rate for full system over 6–12 months: ~30–40% reach stable steady state, ~40% leave latent debt indefinitely, ~20% drift back via the immutability rule eroding one exception at a time. (confidence: inferred)
3. [outside-view §3] Above base rate for the 4-edit substance because: enumerated catalogue with line numbers (strongest predictor of clean completion), grep verification step, tiny reversible diffs, adversarial-review routing. (confidence: inferred)
4. [outside-view §3] At or slightly below base rate for systemic question because: immutability rule stated but not tooling-enforced; sequencing behind item 1 introduces known re-touch; decision not to bundle with item 2 doubles sweep cost. (confidence: inferred)
5. [outside-view §4] Modal failure mode is fence leakage: future agent edits a session artifact for unrelated reason and "helpfully" fixes the click-broken link too, eroding the immutability rule one quiet commit at a time; six months later, half artifacts silently modernized. (confidence: inferred)
6. [outside-view §4] Secondary failure mode: deferred restyle never lands, leaving permanent style mix because item 1's decision sits unmade and the restyle pass migrates to a punch-list-of-punch-lists. (confidence: inferred)
7. [outside-view §4] Plan partially avoids modal failure (policy is named and written) but lacks: pre-commit/CI hook on session-artifact edits, in-file LOCKED markers, or a "freeze test" asserting the 7 references remain broken. Without one of these, plan relies on operator memory. (confidence: inferred)
8. [outside-view §5] Mitigation that would lift systemic part above class: tooling-level guard on session-artifact edits, or at minimum a `.claude/session-artifacts/README.md` stating the immutability rule in the directory it governs. (confidence: inferred)

## Authority-framed claims
1. "anchored on rename-refactor literature (very high completion when scoped) and maintenance-debt literature (low rate of bounded TODOs being fully closed in single-operator repos)" — underlying claim: bounded scoped renames complete cleanly; bounded TODOs in solo repos rarely close fully. Quote present in output: no (no passage cited; canon corpus is gitignored). Confidence: unsupported.

## Contradictions surfaced
- 4-edit substance forecast (above base rate, ~80% clean) vs systemic forecast (at/below base rate, ~40% latent-debt outcome). Same plan, two different verdicts; subagent does not collapse them.
- "Plan names policy clearly and writes it down" (positive signal) vs "stated rules in single-operator repos drift" / "rule erodes one quiet commit at a time" (the writing-down is insufficient). Both held simultaneously.

## Subagent's own verdict (verbatim)
"Within tolerance for the 4-edit substance. Below base rate for the policy fence."

## Gaps the subagent missed
- No quantification of the cost of the proposed mitigations (pre-commit hook, LOCKED markers, freeze test) versus the expected cost of the modal failure. Forecaster names the mitigation but does not say which is cheapest.
- No discussion of whether the immutability rule itself is the right policy — only whether it will hold. Frame question (should historical session artifacts be immutable at all?) is left to frame-challenger.
- No reference-class data on how often "README-in-the-governed-directory" patterns actually prevent rule erosion versus how often they are also ignored. The recommended cheapest mitigation is itself ungrounded in base rate.
- Did not address the interaction between item 03 and item 01's deferred decision in terms of optionality cost (locking in file-relative style now vs. waiting).

## Token budget
~720 tokens.
