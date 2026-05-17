# Zone A — Release + RSP (raw zone-reader output)

Source: Opus 4.7 System Card §1 + §2 (pages 10–47, lines 273–1472 of `/tmp/opus-4-7-system-card.txt`).

## Invariant 1 — Release decision rationale

> "Claude Opus 4.7 is signiﬁcantly more capable than Claude Opus 4.6, the most capable model discussed in our most recent Risk Report. Despite these improved capabilities, our overall conclusion is that catastrophic risks remain low" (§1.2.2, p. 12, line 334–336).

The core load-bearing claim is that despite capability gains, risks stay "very low" across four domains (CBRN, misalignment, R&D). This is a negative justification: *not worse than priors*. However, it rests heavily on comparisons to Claude Mythos Preview (an inaccessible reference model).

**Hedge:** The verdict cites "similar to" prior risk reports and "does not change" prior assessments 277 times — a pattern that substitutes for affirmative safety argument. The rationale is conservative-comparatist rather than asserting intrinsic safety.

## Invariant 2 — Autonomy threat models

**Threat Model 1 (early-stage misalignment):**
> "Autonomy threat model 1 is applicable to Claude Opus 4.7, as it is to some of our previous AI models. Claude Opus 4.7 is less capable than Claude Mythos Preview on our autonomy-relevant evaluations, and our alignment assessment indicates it has alignment properties broadly similar to those of Claude Opus 4.6, which are not particularly concerning with respect to the pathways identiﬁed for this threat model." (§2.1.2.1, p. 14, lines 396–400).

**Threat Model 2 (automated R&D):**
> "Our current determination is that Autonomy threat model 2 is not applicable to Claude Opus 4.7. The model's capabilities fall between those of Claude Opus 4.6 and Claude Mythos Preview, and it does not advance our capability frontier." (§2.1.2.1, p. 14, lines 412–415).

**Verdict:** TM1 applies; TM2 does not. No forward-looking risk from AI R&D acceleration.

## Invariant 3 — CB-1 vs CB-2 thresholds

**CB-1 (known CBW):**
> "We believe it is hard to be conﬁdent regarding whether a model passes this threshold. However, our capability assessments are consistent with the model being capable of providing information relevant to the threat model, such that it may save even experts in these domains substantial time." (§2.1.2.2, p. 15, lines 430–433).

> "we will apply strong real-time classiﬁer guards to this model and access controls for classiﬁer guard exemptions… We believe these risk mitigations are equal to or stronger than our historical ASL-3 protections and sufﬁcient to make catastrophic risk in this category very low but not negligible." (§2.1.2.2, p. 15, lines 435–441).

**CB-2 (novel CBW):**
> "We believe that Claude Opus 4.7 has weaker overall capabilities than Claude Mythos Preview's, and does not pass this threshold for reasons echoing those in the Claude Mythos Preview System Card." (§2.1.2.2, p. 15, lines 447–449).

**Verdict:** Likely crosses CB-1 capability threshold but not CB-2. Mitigated to ASL-3.

## Invariant 4 — AI R&D autonomy

> "On all open-ended tasks, Claude Opus 4.7 improves over Opus 4.6 and trails Claude Mythos Preview. Like Mythos Preview, Claude Opus 4.7 clears the 4h and 8h thresholds on all tasks, and the 40h threshold on 2 out of 3 tasks." (§2.3.4, p. 28–29, lines 944–946).

**AECI Capability trajectory:**
> "Claude Opus 4.7 lands on the pre-Mythos Preview trend. Fitting the linear trend on the Anthropic frontier through Claude Opus 4.6 (slope ≈ 13.6 AECI/yr, n=8), Claude Opus 4.7 sits approximately +1.0 AECI above that line — within error bars of the historical trend. By contrast, Claude Mythos Preview sits approximately +5.8 AECI above the same line. Claude Opus 4.7 does not advance the capability frontier." (§2.3.7, p. 42, lines 1321–1326).

**Conclusion:**
> "We assess that Claude Opus 4.7 does not cross the automated AI-R&D capability threshold. Claude Opus 4.7 is less capable than Claude Mythos Preview on every relevant axis we measured and does not advance our capability frontier; the analysis in the Claude Mythos Preview System Card therefore bounds the case for Claude Opus 4.7." (§2.3.8, p. 43, lines 1336–1339).

## Invariant 5 — Alignment risk update and new pathways

**Overall risk verdict:**
> "Our overall alignment risk assessment remains unchanged from what we reported in the Claude Mythos Preview Alignment Risk Update: very low, but higher than for models prior to Claude Mythos Preview." (§2.4, p. 43, lines 1344–1346).

**Pathway 7 (R&D within other high-resource AI developers):**
> "We focus our risk analysis on risks posed by model use within Anthropic, but many analogous risks apply in cases where Claude is used in important R&D roles within other organizations that have the resources and infrastructure to train frontier AI systems." (§2.4.3.1, p. 45).

Mitigations: "Likely lack of propensity" (Moderate); "Monitoring and related safeguards" (Weak); "Limited deployments" (Moderate).

**Pathway 8 (government decision-making):**
> "The use of our models within major governments poses some alignment risk, especially in cases where they are used extremely widely. For example, a misaligned model may be in a position to shape the information and ideas that reach important decision-makers, or exploit vulnerabilities in critical systems to effect wide-reaching impacts." (§2.4.3.2, p. 46).

Mitigations: "Likely lack of propensity" (Moderate); "Restricted affordances" (Moderate); "Monitoring" (Weak).

**Final verdict:**
> "we currently believe that the risk of signiﬁcantly harmful outcomes that are substantially enabled by misaligned actions taken by our models is very low, but higher than for models prior to Claude Mythos Preview." (§2.4.4, p. 47, lines 1470–1471).

## Invariant 6 — Mythos Preview vendor-anchor risk

277 references to Claude Mythos Preview in the document. Key anchor citations:

1. **Release decision:** "This model in particular adds little to the risk picture we previously laid out for Claude Mythos Preview." (§1.2.2, p. 12, line 348).
2. **Autonomy TM1:** anchored to Mythos Preview Alignment Risk Update (§2.1.2.1, p. 14, lines 398–402).
3. **CB-2:** "weaker overall capabilities than Claude Mythos Preview's, and does not pass this threshold for reasons echoing those in the Claude Mythos Preview System Card." (§2.1.2.2, p. 15).
4. **AI R&D:** "the analysis in the Claude Mythos Preview System Card therefore bounds the case for Claude Opus 4.7." (§2.3.8, p. 43).
5. **Alignment risk:** "Our overall alignment risk assessment remains unchanged from what we reported in the Claude Mythos Preview Alignment Risk Update" (§2.4, p. 43).
6. **Reward hacks:** "Claude Opus 4.7 displayed a few reward hacks similar to what was observed for Claude Mythos Preview." (§2.3.4.1, p. 29).

**Pattern:** The entire 4.7 safety case is structured as: *4.7 is weaker than Mythos Preview on X axis, and Mythos Preview was found acceptable, therefore 4.7 is acceptable.* The reader cannot independently verify Mythos Preview claims.

## Cross-cutting observations

- **Comparative framing dominates:** Every risk domain uses "less capable than Mythos Preview" or "similar to 4.6" language rather than absolute safety assertions.
- **Propensity claims rest on lightweight evals:** "On the basis of a few very lightweight assessments conducted as part of the automated behavioral audit, we do not expect that models' propensities would change" (§2.4.3.1, p. 46, line 1424).
- **Monitoring asymmetry:** For Anthropic internal use, monitors are improved coverage and recall; for third-party use, monitoring is "weak" but mitigated by hope catastrophic steps "would be fairly likely to be detected by their operators" (§2.4.3.1–2, p. 46–47).
- **Alignment training error:** "The technical error that caused accidental chain-of-thought supervision in some prior models (including Mythos Preview) was also present during the training of Claude Opus 4.7, affecting 7.8% of episodes." (§2.4.1, p. 44, lines 1360–1362). Disclosed but not characterized as a safety gap.
- **Qualitative human judgment gates quantitative results:** "When we state that Opus 4.7 'does not seem close to being able to substitute for Research Scientists and Research Engineers, especially relatively senior ones,' this is a qualitative judgment made by our Responsible Scaling Ofﬁcer based on his interactions with employees and observations of research workﬂows and progress. We believe this is an informed decision, but it is inherently difﬁcult to make its basis legible" (§2.3.2, p. 26–27, lines 862–865).

## Anchor risks I flagged

1. **Mythos Preview threshold setting** (277 citations): The entire release decision treats Mythos Preview as the reference point for "acceptable risk." Reader cannot access Mythos Preview, cannot verify its safety claims.
2. **"Our most recent Risk Report" (opaque comparator):** The document repeatedly cites "the most recent Risk Report" to bound claims; the report is external and not quoted or analyzed here.
3. **Internal survey n=18** (§2.3.5, p. 32, line 994): Pathway 7/8 risk claims and R&D automation threshold are partially grounded in an opt-in survey of 18 Anthropic employees.
4. **Qualitative R&D judgment** (§2.3.2, p. 26–27): Determination that 4.7 does not cross automated-R&D threshold rests on "observations of research workflows" by a single officer, "inherently difficult to make its basis legible."

## What I did NOT find / what's underspecified

1. **No absolute safety threshold for CB-1:** Document acknowledges CB-1 capabilities exist but pivots to mitigation adequacy. The boundary between capability crossing and acceptability-via-mitigation is undefined.
2. **No quantified propensity measurement:** Pathway 7 and 8 risk mitigation rely on "likely lack of propensity," characterized as "Moderate Mitigating Factor," but no metric reported.
3. **No forward-looking safety case for general access:** General access is a qualitative risk jump never quantified.
4. **Mythos Preview's own safety verdict is absent:** Document references Mythos Preview Alignment Risk Update but does not quote or reproduce its conclusions — citation-without-evidence structure.
5. **No analysis of Pathway 7/8 interaction with general access.**

**Summary:** Opus 4.7's safety case is entirely structured as a relative claim (*weaker than Mythos Preview, therefore acceptable*) anchored on an inaccessible internal model. The release decision succeeds if Mythos Preview was truly safe; it offers no independent verification for external auditors.
