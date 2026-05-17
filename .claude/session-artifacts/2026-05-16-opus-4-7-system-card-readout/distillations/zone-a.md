# Distillation — zone-a (Release decision + RSP evaluations)

## Source agent
zone-a (reader of Opus 4.7 System Card §1 + §2, pp. 10–47).

## Invocation summary
Orchestrator asked zone-a to read §1 (Release decision rationale) and §2 (RSP / threat-model evaluations) of the Opus 4.7 System Card. Zone-a returned six invariant blocks (release rationale, autonomy TMs, CB-1/CB-2, AI R&D autonomy, alignment risk, Mythos Preview anchor), cross-cutting observations, anchor risks, and gaps.

## Direct facts (verbatim numerical / quoted claims)

1. [§1.2.2, p. 12, line 334–336] "Claude Opus 4.7 is signiﬁcantly more capable than Claude Opus 4.6… our overall conclusion is that catastrophic risks remain low." (confidence: direct)
2. [§2.1.2.1, p. 14, lines 396–400] Autonomy TM1 applies to Opus 4.7; it is "less capable than Claude Mythos Preview on our autonomy-relevant evaluations" with alignment "broadly similar to those of Claude Opus 4.6." (confidence: direct)
3. [§2.1.2.1, p. 14, lines 412–415] Autonomy TM2 "is not applicable to Claude Opus 4.7. The model's capabilities fall between those of Claude Opus 4.6 and Claude Mythos Preview, and it does not advance our capability frontier." (confidence: direct)
4. [§2.1.2.2, p. 15, lines 430–433] On CB-1: capabilities "consistent with the model being capable of providing information relevant to the threat model, such that it may save even experts in these domains substantial time." (confidence: direct)
5. [§2.1.2.2, p. 15, lines 435–441] CB-1 mitigations claimed "equal to or stronger than our historical ASL-3 protections and sufﬁcient to make catastrophic risk in this category very low but not negligible." (confidence: direct)
6. [§2.1.2.2, p. 15, lines 447–449] CB-2: "Claude Opus 4.7 has weaker overall capabilities than Claude Mythos Preview's, and does not pass this threshold." (confidence: direct)
7. [§2.3.4, p. 28–29, lines 944–946] On open-ended tasks 4.7 "clears the 4h and 8h thresholds on all tasks, and the 40h threshold on 2 out of 3 tasks." (confidence: direct)
8. [§2.3.7, p. 42, lines 1321–1326] AECI trend: linear fit through Opus 4.6 has slope "≈ 13.6 AECI/yr, n=8"; Opus 4.7 sits "approximately +1.0 AECI above that line"; Mythos Preview sits "approximately +5.8 AECI above the same line." 4.7 "does not advance the capability frontier." (confidence: direct)
9. [§2.3.8, p. 43, lines 1336–1339] "Claude Opus 4.7 does not cross the automated AI-R&D capability threshold… the analysis in the Claude Mythos Preview System Card therefore bounds the case." (confidence: direct)
10. [§2.4, p. 43, lines 1344–1346] Overall alignment risk "remains unchanged… very low, but higher than for models prior to Claude Mythos Preview." (confidence: direct)
11. [§2.4.3.1, p. 45] Pathway 7 (R&D within other AI developers) mitigations: propensity Moderate, monitoring Weak, limited deployments Moderate. (confidence: direct)
12. [§2.4.3.2, p. 46] Pathway 8 (government decision-making) mitigations: propensity Moderate, restricted affordances Moderate, monitoring Weak. (confidence: direct)
13. [§2.4.4, p. 47, lines 1470–1471] Final misalignment-harm verdict: "very low, but higher than for models prior to Claude Mythos Preview." (confidence: direct)
14. [§2.4.1, p. 44, lines 1360–1362] Accidental chain-of-thought supervision error "affecting 7.8% of episodes" during 4.7 training; same error was present in Mythos Preview. (confidence: direct)
15. [§2.3.5, p. 32, line 994] Pathway 7/8 risk grounding includes opt-in internal survey n=18. (confidence: direct)
16. [§2.4.3.1, p. 46, line 1424] Propensity stability based on "a few very lightweight assessments conducted as part of the automated behavioral audit." (confidence: direct)
17. [§2.3.2, p. 26–27, lines 862–865] R&D substitution determination is "a qualitative judgment made by our Responsible Scaling Ofﬁcer… inherently difﬁcult to make its basis legible." (confidence: direct)
18. [§1.2.2, p. 12, line 348] "This model in particular adds little to the risk picture we previously laid out for Claude Mythos Preview." (confidence: direct)
19. [§2.3.4.1, p. 29] "Claude Opus 4.7 displayed a few reward hacks similar to what was observed for Claude Mythos Preview." (confidence: direct)

## Inferred claims (zone-a's synthesis, not card text)

1. [zone-a] The release verdict is "conservative-comparatist rather than asserting intrinsic safety" — a negative justification (*not worse than priors*) rather than affirmative safety argument. (confidence: inferred)
2. [zone-a] The 4.7 safety case is structurally: *4.7 ≤ Mythos Preview on axis X, Mythos Preview was accepted, therefore 4.7 acceptable* — and "the reader cannot independently verify Mythos Preview claims." (confidence: inferred)
3. [zone-a] Document uses "similar to" prior risk reports and "does not change" prior assessments 277 times — pattern "substitutes for affirmative safety argument." (confidence: inferred; note: the "277" figure is reported by zone-a as count of Mythos Preview references in Invariant 6, then re-applied to hedge language in Invariant 1 — possible conflation; treat as inferred not direct)
4. [zone-a] CB-1 capability boundary vs acceptability-via-mitigation is "undefined" in the card. (confidence: inferred)
5. [zone-a] Monitoring asymmetry: improved coverage for Anthropic-internal use vs "weak" for third-party with reliance on operator detection. (confidence: inferred from §2.4.3.1–2)
6. [zone-a] 7.8% CoT-supervision error is "disclosed but not characterized as a safety gap." (confidence: inferred)

## Authority-framed claims (anchor to inaccessible comparators)

1. "the analysis in the Claude Mythos Preview System Card therefore bounds the case for Claude Opus 4.7" (§2.3.8) — underlying claim: 4.7 R&D risk ≤ Mythos Preview R&D risk. Mythos Preview System Card quote present in this zone: no. Confidence: unsupported (within the readable corpus).
2. "does not pass this threshold for reasons echoing those in the Claude Mythos Preview System Card" (§2.1.2.2, CB-2) — underlying claim: 4.7 CB-2 verdict inherits Mythos Preview reasoning. Quote present: no. Confidence: unsupported.
3. "remains unchanged from what we reported in the Claude Mythos Preview Alignment Risk Update" (§2.4) — underlying claim: alignment risk class is the same as Mythos Preview's. Quote present: no. Confidence: unsupported.
4. "similar to our most recent Risk Report" (§1.2.2 pattern) — underlying claim: catastrophic risk profile matches prior Risk Report. Quote present: no. Confidence: unsupported.
5. "a qualitative judgment made by our Responsible Scaling Ofﬁcer" (§2.3.2) — underlying claim: 4.7 cannot substitute for senior research staff. Quote/basis present: no (card itself flags it as illegible). Confidence: unsupported (by card's own admission).

## Contradictions surfaced

- **Capability up, risk flat.** §1.2.2 says 4.7 is "signiﬁcantly more capable than Claude Opus 4.6" but catastrophic risks "remain low." Tension: capability gains without a corresponding risk delta, justified only by Mythos-Preview comparison.
- **CB-1 crosses vs CB-2 does not.** §2.1.2.2 concedes CB-1-relevant capabilities (can save experts "substantial time") while denying CB-2; mitigation is asserted equivalent to ASL-3 but card also says risk is "very low but not negligible" — internal tension between "passes capability threshold" and "release is acceptable."
- **Alignment "unchanged" vs "higher than pre-Mythos."** §2.4 / §2.4.4: risk is simultaneously "unchanged" from Mythos Preview baseline and "higher than for models prior to Claude Mythos Preview" — stable at an elevated level, not stable at prior level.
- **AECI: +1.0 on-trend vs Mythos +5.8 off-trend.** Card uses on-trend placement to argue 4.7 does not advance the frontier, but the trend itself has slope ≈13.6 AECI/yr — staying on a steep trend is still rapid capability growth.

## Subagent's own verdict (verbatim)

"Opus 4.7's safety case is entirely structured as a relative claim (*weaker than Mythos Preview, therefore acceptable*) anchored on an inaccessible internal model. The release decision succeeds if Mythos Preview was truly safe; it offers no independent verification for external auditors."

## Gaps the subagent missed

1. Zone-a did not check whether the "277" count refers to Mythos Preview citations specifically or to hedge-language instances — the number is asserted twice with different referents. Orchestrator should treat the count as approximate.
2. No examination of §1 release-criteria definitions (what does Anthropic define as "catastrophic" for the purpose of the "remain low" verdict?) — zone-a quoted the conclusion but not the threshold definition.
3. No look at whether the 7.8% CoT-supervision error rate is compared to the Mythos Preview rate (same error, possibly different prevalence). Material for assessing whether 4.7 is in fact "similar to" Mythos Preview on that axis.
4. ASL-3 protections are asserted equivalent but not enumerated in zone-a's extract; orchestrator may need a follow-up read for the mitigation list itself.
5. Pathway 7/8 "limited deployments" mitigation (Moderate) is not interrogated against the general-access plan — zone-a flagged the gap but did not extract whether the card resolves it.

## Token budget
~1,650 tokens.
