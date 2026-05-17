# Distillation — outside-view

## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on whether the Opus 4.7 system-card's top-line safety claims will hold up post-deployment. Subagent returned a three-class reference framing, qualitative base-rate estimates, a positional read of the 4.7 card vs. that base rate, a gradient-erosion failure-mode narrative, and the verdict "below base rate."

## Canon-first disclosure (preserved verbatim in substance)
- Canon read first: [canon/sources.yaml](canon/sources.yaml). Confirmed coverage: Kahneman/Lovallo 1993, Flyvbjerg 2006, Tetlock 2015, Anthropic *Core Views on AI Safety* (2023).
- **Declared canon gaps:** system-card track records, RSP/PF audit history, eval-awareness literature, METR/Apollo evaluations, any post-2023 lab safety report. All numbers below come from web sources (named in raw) and are not promoted to canon.

## Direct facts
1. [outside-view, raw §Reference class] Class A is self-evaluated frontier-AI system cards 2023–2026, N≈20–30, with single-digit independent audits in the public record. (confidence: direct)
2. [outside-view, raw §Reference class] Class B (vendor self-attested safety claims in regulated-ish software) has measured optimism factors typically 1.3–3× vs. independent re-test. (confidence: direct; figure asserted without primary citation — see authority section)
3. [outside-view, raw §Reference class] Epic Sepsis Model: vendor-reported AUC vs. external-validation AUC 0.63, missed 67% of cases. (confidence: direct)
4. [outside-view, raw §Base rate] No clean published base rate exists for "system-card claim held up in deployment"; nobody has built the counterfactual harness. (confidence: direct)
5. [outside-view, raw §Position] Opus 4.5 system card disclosed a vulnerability that materialized in production two weeks before 4.6 shipped (VentureBeat, Promptfoo cited). (confidence: direct)
6. [outside-view, raw §Position] The 4.7 card publishes both white-box findings and discloses a 12% → 33% AI-safety-R&D refusal-rate regression. (confidence: direct)

## Inferred claims (all flagged by subagent as estimates, not measured rates)
1. [outside-view] Qualitative base rate: vendor top-line safety claim survives 12 months of real-world deployment without a high-profile incident the framing didn't anticipate **~30–50%, degrading as capability grows**. Explicitly labeled "Estimate, not a measured rate." (confidence: inferred)
2. [outside-view] Verdict: **"below base rate"** for the 4.7 card. Drivers: inaccessible Mythos comparator (worst-performing analog pattern), under-powered single white-box probe, asymmetric failure domain for the disclosed regression. (confidence: inferred)
3. [outside-view, §Typical failure mode] Failure shape is **gradient erosion**, not a single incident: (a) eval-distribution mismatch surfaces in 2–6 weeks moving safety metrics 1.5–3× in harmful direction; (b) comparator collapse; (c) disclosed regression expands rather than contracts; (d) eval-awareness becomes the headline within 6–9 months. (confidence: inferred; each numeric is an estimate)
4. [outside-view] Class-wide invalidation of eval → deployment inference is now underway (eval-awareness literature), not a single-vendor issue. (confidence: inferred)

## Authority-framed claims (percentages without primary citation flagged)
1. "FLI AI Safety Index (Winter 2025, Summer 2025): scores labs C-range and below on safety-claim verification; no lab scores above B." — underlying claim as stated. Quote present in output: no. Confidence: **unsupported** (source URL given but no quoted figure).
2. "FAS analysis of preparedness frameworks (2024–2025): independent reproduction of dangerous-capability evaluations is currently a single-digit-percent fraction of published evals." — Quote present: no. Confidence: **unsupported**.
3. "Pharma sponsor-trial efficacy claims revised downward in roughly **50–70%** of independent meta-analyses." — Quote present: no; no meta-analysis cited. Confidence: **unsupported**.
4. "Safety signals not present in trials emerge in **~30%** of approved drugs within 5 years (FDA post-market label changes)." — Quote present: no. Confidence: **unsupported**.
5. "In pharma, 'non-inferior to our prior internal formulation' claims fail external validation roughly **2 out of 3 times**." — Subagent self-labels "rough industry figure; estimate." Quote present: no. Confidence: **unsupported**.
6. "In Class C, shadow-environment generalization to production correct **40–60%** of the time, lower for ML." — Quote present: no. Confidence: **unsupported**.
7. "Apollo: in-context scheming behavior not present in original system-card framing." — Apollo URL cited; specific behavior not quoted. Confidence: **inferred** (citation exists, content not quoted).
8. "IAPS 2025: eval contexts are now behavioral inputs; any single white-box probe is under-powered." — IAPS URL cited; no direct quote. Confidence: **inferred** (citation exists, paraphrased).
9. "Disclosed eval regressions **expand** under deployment in ~70% of measured cases" (broader software-safety literature). — No citation. Confidence: **unsupported**.
10. "Base rate of inaccessible-comparator claim surviving external scrutiny: **<40%**, qualitative." — Subagent self-labels "qualitative." No citation. Confidence: **unsupported**.

## Contradictions surfaced
- **Strengths vs. weaknesses of the 4.7 card itself** (subagent preserved both, did not collapse):
  - Above class average: explicit regression disclosure (12% → 33%); white-box eval-awareness finding published rather than buried.
  - Below class average: inaccessible Mythos comparator (worst analog pattern); single under-powered white-box probe; asymmetric-failure domain for the regression.
- No within-source contradicting passages on the verdict itself; subagent did not surface a counter-reference-class that would yield "at or above base rate."

## Subagent's own verdict (verbatim)
**Below base rate.**

## Remediation list — "what would lift it toward base rate" (decision-bearing, preserved verbatim in substance)
1. An externally-runnable version of the Mythos comparator, **or** a third party reproducing the Mythos-vs-4.7 risk inequality on a held-out eval suite.
2. A second independent white-box probe of the deception-representation finding, ideally from a non-Anthropic group.
3. A pre-registered post-deployment monitoring commitment with thresholds at which the 12% → 33% claim is considered falsified.

## Gaps the subagent missed
- No attempt to construct a counter-reference-class (e.g., open-source model release track records, or pre-2023 ML safety reports) that might place 4.7 *at* base rate. The verdict rests entirely on the chosen three classes.
- No engagement with the *content* of canon entries it consulted (Kahneman/Lovallo, Flyvbjerg, Tetlock) — only confirmation of coverage. Reference-class forecasting heuristics from those sources are not cited against the case.
- Numeric estimates throughout are uncited; remediation list does not include "produce a citable base-rate study" even though the subagent itself declared one does not exist.
- No quantification of how much each remediation item would shift the verdict (i.e., which is the cheapest move).

## Token budget
~870 tokens.
