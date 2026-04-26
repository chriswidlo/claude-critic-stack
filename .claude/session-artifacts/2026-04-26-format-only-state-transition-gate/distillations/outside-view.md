## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on adoption/durability of a self-imposed format-only state-transition validator over a ~22-entry, 8-state personal R&D notes corpus. Subagent returned a 15–30% sustained-adoption base rate, a verdict of "within tolerance, conditional on integration surface," and a modal failure mode of lifecycle spec drift.

## Bias flags (preserved verbatim from source)
- Canon corpus folder is gitignored on this machine; methodology stubs (Kahneman/Lovallo 1993, Flyvbjerg 2006, Tetlock 2015) consulted only by reference. **No canon coverage of the specific reference class.**
- All numeric base rates and adoption rates below derive from **web sources flagged as gap-fill, not promoted to canon**. See Sources at end.
- Team-CI reference class explicitly excluded per user constraint.

## Direct facts
1. [Forte Labs / PKM, web gap-fill] "~68% of PKM-tool adopters abandon within six months." (confidence: direct — quoted statistic, but source is web gap-fill, not canon)
2. [jyn.dev / Thoughtworks / dev.to / BigGo, web gap-fill] Pre-commit hooks have a documented `--no-verify` escape when hooks add friction >1–2s or produce false positives. (confidence: direct from web sources, gap-fill)
3. [outside-view, self-report] Canon does not cover personal-tooling validator adoption, pre-commit hook abandonment, or single-operator content-convention enforcement. (confidence: direct)

## Inferred claims
1. [outside-view] Estimated base rate of sustained adoption past 6 months for self-imposed personal-workflow validators: **15–30%**, flagged as a soft estimate. (confidence: inferred)
2. [outside-view] Modal outcome (~50–60%): "built, used briefly, then bypassed or removed." Meaningful minority (~15–25%): "built but never integrated into actual edit loop." (confidence: inferred)
3. [outside-view] Format-only gates have a much better track record than quality gates on personal R&D notes because they answer a yes/no the operator agrees with in advance. (confidence: inferred)
4. [outside-view] 8 states is on the high end for personal lifecycle; most surviving personal workflows collapse to 3–5 states within a year. (confidence: inferred)
5. [outside-view] "Required body elements per state" is a moving spec; validator will lag operator's actual template, producing false positives. (confidence: inferred)
6. [outside-view] Net design position: mildly favorable on design, mildly unfavorable on enforcement surface — roughly at base rate, perhaps slightly above if integration question is solved. (confidence: inferred)

## Modal failure mode (preserved)
**#1 — Lifecycle spec drift (modal).** Operator changes how a "spiked" entry is written but doesn't update the validator. Validator produces false positives; after 2–3 the operator stops trusting it; validator becomes vestigial.

Subsequent failure modes (rough order of likelihood):
2. State collapse (3 of 8 states unused within 2–3 months; validator enforces lifecycle operator no longer believes in).
3. Bypass-by-default (validator only runs on explicit invocation; operator drifts to editing without invoking).
4. Scope creep into quality judgment (gate becomes adversarial; abandoned within weeks).
5. One-off "first run" success then disuse.

## Lift conditions (preserved verbatim)
- Pin validator to a specific invocation surface that does not depend on operator memory.
- Co-locate lifecycle spec and validator in one file, so spec drift forces validator update.
- Pre-commit to a state-collapse review at the 6-week mark; treat collapse as expected, not as failure.

Non-failure path (preserved): validator runs automatically on every save or commit, takes <500ms, false-positive rate <5%, and the lifecycle spec is revised in lockstep with the validator (i.e., validator *is* the lifecycle spec).

## Authority-framed claims
None. The subagent did not attribute claims to named authors. Canon stubs (Kahneman & Lovallo, Flyvbjerg, Tetlock) were named only as methodology references consulted, with no claim ventriloquized from them.

## Contradictions surfaced
- **Adjacent reference class (low-code/CMS workflow validators) over-predicts adoption** because of multi-user pressure and platform lock-in absent here. Subagent flagged the class as a weaker fit and discounted it rather than averaging it in.
- **Favorable vs unfavorable factors** held in tension rather than collapsed: format-only + small corpus + self-authored spec (favorable) vs single-operator enforcement + 8-state spec on the high end + moving body-element spec + no forcing invocation surface (unfavorable). Net stated as "roughly at base rate."

## Subagent's own verdict (verbatim)
**"Within tolerance, conditional on integration surface."**
At or slightly above base rate *if and only if* the enforcement-surface problem is solved before building features. If invocation is "I'll run it manually" or "the agent will probably remember," forecast drops to bottom of range (~15%) — modal outcome is failure mode #3 (bypass-by-default).

## Gaps the subagent missed
- No estimate of cost-of-failure: if the validator is abandoned in 3 months, what is lost vs. not having built it? Asymmetry between "validator becomes vestigial" and "validator actively misleads" not analyzed.
- No discussion of whether agent-mediated edits (LLM doing the writes) change the reference class — agents do not have "operator memory" failure mode #3 in the same way; this could materially shift base rate but was only mentioned in passing.
- No quantification of how much the lift conditions actually lift the forecast (15–30% becomes what, exactly, if all three are met?).
- Reference class is web-sourced; no triangulation against canon methodology on how to weight a single-source base rate.

## Token budget
~720 tokens.
