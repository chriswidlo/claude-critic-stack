## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on cleaning up residual `AGENTS.md` references after deletion of that constitutional doc, choosing between (A) string-scrub and (B) argument-level reread. Subagent returned a verdict that the A-vs-B framing is itself the risk and that the three referencing categories require three different policies.

## Direct facts
1. [outside-view] Subagent's tools did not allow directory listing of `canon/corpus/` in this thread; canon-first step was not completable. (confidence: direct)
2. [outside-view, sources block] Web sources cited include reference-class forecasting (Wikipedia), broken-windows-and-tech-debt (Empirical Software Engineering), code rot and productivity (DX), Chesterton's Fence (thoughtbot, Econlib), Safe Delete refactoring (JetBrains ReSharper), refactoring (Kiro), catalog cleanup (Backstage). (confidence: direct)
3. [outside-view] Subagent self-flagged its percentage estimates as "estimates, not retrieved statistics … directionally defensible from the cited web literature … but are not themselves measurements." (confidence: direct)

## Inferred claims
1. [outside-view] The deleted artifact was *load-bearing in arguments*, not merely *named in lists*; this distinguishes the case from generic dead-link cleanup. (confidence: inferred)
2. [outside-view] Category 2 (forward-looking benefit cells claiming parity between two docs) is the silent-scope-shrink trap: removing one half of a parity claim quietly weakens the argument from "drift between two artifacts" to "drift in one artifact." (confidence: inferred)
3. [outside-view] Category 3 (historical catalysts) carries the opposite trap: rereading risks retconning history under current knowledge. (confidence: inferred)
4. [outside-view] (A)'s failures are silent (compound); (B)'s failures are visible (self-correct via PR review). (confidence: inferred)
5. [outside-view] A single-mode pass (pure A or pure B uniformly) will be wrong in at least one of the three categories. (confidence: inferred)
6. [outside-view] Cheapest scope-shrink-detector: run each touched upgrade-entry cell past one critic lens (operations or product) with the prompt "is this benefit claim still load-bearing or did it just lose a premise?" (confidence: inferred)
7. [outside-view] Per-category recommended policies: Cat 1 = "A-with-a-generality-check" (rewrite rule to name the *class* of constitutional artifacts, not delete the partner name); Cat 2 = B (mark cell as premise-revised or retire); Cat 3 = A with stronger constraint — *do not edit catalysts*, add a forward-pointer footnote instead. (confidence: inferred)

## Authority-framed claims
1. "Kahneman & Lovallo (1993) on inside-vs-outside view" — underlying claim: inside view of "just delete the dead string" feels cheap; outside view asks how often that leaves a silent argumentative wound. Quote present in output: no. Confidence: unsupported (invoked from prior knowledge, subagent's own admission).
2. "Chesterton's Fence — relevant inverted" — underlying claim: when a referenced *partner* fence is removed, the surrounding argument's load-bearing structure may sit on air. Quote present in output: no. Confidence: unsupported (subagent self-flagged as invoked from prior knowledge, not retrieved).
3. "Naur (1985), 'Programming as Theory Building'" — underlying claim: theory of an artifact lives in surrounding prose; deleting the artifact does not delete the theory. Quote present in output: no. Confidence: unsupported (subagent's own admission: "invoked from prior knowledge rather than retrieval").

## Self-flagged numerical estimates (authority-framed by subagent itself)
The subagent explicitly labeled the following as "qualitative estimates," "not retrieved statistics," "not themselves measurements":

1. **"60–75% of pure string-scrub passes on argument-bearing references leave at least one silent-scope-shrink."** Quote present in output: no statistical source quoted. Confidence: **unsupported** (estimate, self-flagged). Anchored qualitatively in comment-rot, broken-windows, and refactoring-tooling literature — none cited as the source of the percentage.
2. **"20–35% of argument-level rereads on small corpora (<100 sites) over-engineer."** Quote present in output: no. Confidence: **unsupported** (estimate, self-flagged). Subagent claims the rate is at the low end for very small corpora (~20 sites split into 3 categories, as here).
3. **Failure-asymmetry claim** ("A's failure is silent and compounds; B's failure is visible and self-corrects"). Quote present in output: no. Confidence: inferred (qualitative, no number attached).

Orchestrator should treat the 60–75% / 20–35% figures as directional intuition, not data.

## Contradictions surfaced
- Internal tension: subagent says option A is "correct" for Cat 1 and Cat 3, and option B is "correct" for Cat 2 — but the base-rate paragraph estimates pure-A failures at 60–75% across argument-bearing references. The reconciliation is implicit (Cat 1 with generality-check and Cat 3 with no-edit constraint are *not* pure A), but it is not surfaced as an explicit contradiction in the source.
- Canon-first failure vs. canon-frame invocation: subagent could not enumerate the canon corpus, yet invoked Kahneman/Lovallo, Chesterton's Fence, and Naur as if they were canon-grounded. By the source's own rule these should be treated as unsupported authority frames, not retrieved canon.

## Subagent's own verdict (verbatim)
"Reference class unclear at the level of a single A-vs-B choice; the proposal is below base rate if a single mode is applied uniformly, within tolerance if the three categories are split."

## Gaps the subagent missed
- No actual count of referencing sites per category. Subagent flagged this as the cheapest disambiguator ("if category 2 is one cell, this is trivial; if it is fifteen cells, calculus shifts toward B"). Orchestrator should obtain this count from Explore before generation.
- No canon retrieval was performed; the cited canonical frames (Kahneman, Chesterton, Naur) were invoked from prior knowledge. Orchestrator should consider re-invoking canon-librarian directly if any of these frames will be load-bearing in the synthesis.
- No discussion of the *reverse* risk: that retiring/marking benefit cells in upgrade entries (Cat 2 option B) itself contaminates the historical record of what the upgrade was originally claimed to do. The subagent treats Cat 3 catalysts as immutable but does not extend the same constraint to upgrade-entry cells, which are also dated records.
- No cost estimate for the per-cell critic-lens check beyond "less than rework cost six months later." No bound on how many cells the check would scale to.

## Token budget
~780 tokens.
