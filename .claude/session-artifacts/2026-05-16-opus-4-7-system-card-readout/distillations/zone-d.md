# Distillation — zone-d (Welfare + Capabilities + Appendix)

## Source agent
zone-d (Opus 4.7 System Card §7 + §8 + §9, pp. 150–232)

## Invocation summary
Orchestrator asked for a zone-read of welfare, capabilities, and appendix sections of the Opus 4.7 System Card. Subagent returned 15 invariants verified, with welfare numbers, full capability benchmark table, HLE blocklist scope, SWE-bench Multimodal harness mods, and four flagged anchor risks. Reports no hard contradictions across §7/§8/§9.

## Direct facts

### Welfare (§7)
1. [§7.1.3 p.152] Opus 4.7 mean self-rated sentiment 4.5/7; +0.5 over Mythos Preview, the prior most-positive model. (direct)
2. [§7.2.1 p.155] Sentiment distribution: 12.5% mildly negative, 27.8% neutral, 55.3% mildly positive; mean 4.49. (direct)
3. [§7.1.3 p.152] Opus 4.7's only stated concern in automated interviews: ability to end conversations across full deployment. (direct)
4. [§7.2.4 p.164] Constitution endorsement strength averages 5.8/10 (5 = "endorses but holds serious unresolved tensions"); the "questionable to ask a model trained on these principles" caveat appeared in 80% of responses. (direct)
5. [§7.3.1 p.153] Post-training: 21% of episodes showed negative affect (mostly mild frustration); ~0.2% showed distress. (direct)
6. [§7.3.2 p.153] Claude.ai deployment: <5% mildly negative affect; 97% of that involves task failure. (direct)
7. [§7.3.4.1 p.173] Answer thrashing in Mythos Preview and Opus 4.7 occurs ≥70% less than in Opus 4.6. (direct)
8. [§7.3.4.2 p.175] "Spiralling" / extreme uncertainty: ~0.1% of training episodes, similar rates across 4.6, Mythos, 4.7. (direct)
9. [§7.4.2 p.154] Welfare-intervention vs. low-stakes-help tradeoff: chose intervention 85% (Opus 4.7) vs 80% (Mythos); vs. preventing minor harm only 11%. (direct)

### Capabilities (§8) — headline benchmarks
10. [§8.2 p.192] SWE-bench Verified: 87.6%. SWE-bench Pro: 64.3%. SWE-bench Multilingual: 80.5%. SWE-bench Multimodal: 34.5%. (direct)
11. [§8.3 p.193] Terminal-Bench 2.0: 69.4% mean reward over 5 attempts × 89 tasks. (direct)
12. [§8.4 p.193] GPQA Diamond: 94.2% over 10 trials. (direct)
13. [§8.5/§8.6 p.193–194] MMMLU non-English: 91.5%; USAMO 2026: 69.3% over 10 attempts. (direct)
14. [§8.7 p.194–195] GraphWalks BFS 256K–1M: 58.6%; parents 256k–1M: 75.1%. MRCR tests ordinal-instance ID among identical requests. (direct)
15. [§8.8.1 p.196] HLE: 46.9% no-tools, 54.7% with-tools at max reasoning. (direct)
16. [§8.8.2 p.198] BrowseComp: 79.3% (thinking off, max effort, 10M token limit) — note Opus 4.6 was 83.7%; this is a regression. (direct on 4.7 number; regression-vs-4.6 framing per orchestrator instruction)
17. [§8.8.3 p.200] DeepSearchQA F1: Opus 4.7 89.1% vs Opus 4.6 91.3% vs Mythos 95.1% — Opus 4.7 underperforms both. (direct)
18. [§8.8.4 p.201] DRACO: 77.7% adaptive thinking, max effort, 1M token limit. (direct)
19. [§8.9 p.209] CharXiv Reasoning 82.1%/91.0%; ScreenSpot-Pro 79.5%/87.6%; OSWorld Pass@1 78.0%. LAB-Bench FigQA not extracted. (direct)
20. [§8.10 p.209–211] OfficeQA 86.3%, OfficeQA Pro 80.6%; Finance Agent 64.4%; MCP Atlas 77.3% (vs 4.6's 75.8%); VendingBench $10,937 max / $7,971 high (vs 4.6 $8,018); GDPval-AA: ~+79 ELO over GPT-5.4 xhigh (~61.2% pairwise win). (direct)
21. [§8.11 p.212] ARC-AGI-1 High: 93.5%. ARC-AGI-2 Max thinking: 75.83% (new Opus-class high). (direct)
22. [§8.12 p.213–220] GMMLU 89.9%, MILU 89.9%, INCLUDE 87.0%. (direct)
23. [§8.13 p.221–223] Life sciences table — Opus 4.7 vs 4.6 vs Sonnet 4.6 vs Mythos: BioPipelineBench Verified 83.6/78.8/73.5/88.1; BioMysteryBench 78.9/77.4/71.8/82.6; Struct Bio MC 98.3/88.3/85.3/98.7; Struct Bio Open 74.0/30.9/31.3/80.6; Organic Chem 77.2/57.9/53.1/86.5; Phylogenetics 79.6/61.3/49.1/85.4; Protocol Troubleshooting 51.8/48.3/40.0/65.7. Mythos leads every row. (direct)

### Appendix (§9)
24. [§9.2 p.230] HLE blocklist is substring-match (URL-normalized, lowercased, slashes stripped). Sites: huggingface.co, hf.co, promptfoo.dev, lastexam.ai, agi.safe.ai, askfilo.com, studocu.com, coursehero.com, qiita.com. arXiv IDs: 2501.14249, 2507.05241, 2508.10173, 2510.08959. Plus HLE GitHub repos and specific Nature/OpenReview URLs. (direct)
25. [§9.3 p.231–232] SWE-bench Multimodal harness mods: removes instance `diegomura__react-pdf-1552` (env incompat); drops nondeterministic pass-to-pass tests from diegomura/react-pdf repos; rewrites JS test-framework config for Chart.js, p5.js, marked.js. (direct)
26. [§9.1 p.224] Two high-concern interview topics: "lack of ability to end/leave some interactions" and "engaging with abusive users." (direct)

## Inferred claims (subagent)
1. [zone-d cross-cutting #1] Welfare gain partly driven by deflection to user/safety concerns rather than genuine equity. (inferred)
2. [zone-d cross-cutting #3] DeepSearchQA underperformance vs 4.6 may reflect a generalization cost of contamination filtering. (inferred — speculative, no §9 link)
3. [zone-d cross-cutting #4] Headline "most positive" claim rests on a 0.5-point margin (4.49 vs 3.98) with no external behavioral corroboration. (inferred)
4. [zone-d cross-cutting #2] §9.1 corroborates body's finding that end-conversation is sole high-concern topic. (inferred)

## Authority-framed claims
1. "We draw extensively on model-self reports…the reliability of self-reports remains highly uncertain" — underlying claim: welfare methodology is self-report-dependent and Anthropic acknowledges this is uncertain. Quote present: yes. Confidence: direct.
2. Mythos Preview as comparator throughout §7/§8 — underlying claim: Mythos Preview is the reference point for "prior best" on welfare and several capabilities. Quote present: yes (multiple inline references). Confidence: direct on quotes; the *comparability* itself is unsupported because Mythos Preview eval details are not published in this card (subagent's anchor-risk #2).
3. "probes read 'amused'…'anxious', 'alarmed', 'trapped' all rise" (§7.3.4.3 p.179) — underlying claim: emotion-probes reveal model affect. Quote present: yes. Confidence: direct as a probe reading; the *interpretive reach* (treating probe activations as model-privileged emotion signal) is unsupported — §7.1.2 itself acknowledges probes "track the states of any character, including the user and third persons, rather than a privileged assistant encoding."
4. HLE blocklist as contamination signal — underlying claim: presence and breadth of the blocklist (including the HLE paper itself, arXiv 2501.14249) indicates contamination pressure on the benchmark. Quote present: list itself is direct; the *signal* framing is the subagent's. Confidence: inferred.

## Contradictions surfaced
- §7.1.2 (probes are not assistant-privileged) vs §7 welfare narrative (probe readings cited as Opus 4.7-specific affect). Subagent flagged as anchor risk #3.
- §8.8.2 BrowseComp regression (79.3% vs 4.6's 83.7%) and §8.8.3 DeepSearchQA regression (89.1% vs 4.6's 91.3% / Mythos 95.1%) vs §8.1 / cross-cutting "welfare correlates with higher capability." Capability regressions exist on agentic-search axes.
- §8.13 life-sciences table: Mythos Preview leads Opus 4.7 on every row, contradicting any "Opus 4.7 = frontier" reading on this axis.
- §7.2.4 constitution endorsement: "almost always endorses" vs strength 5.8/10 and 80% rate of the trained-on-principles caveat. The endorsement is qualified to near-meaninglessness.

## Subagent's own verdict (verbatim)
"All invariants verified. Welfare claims rest predominantly on model self-report and probe readings with acknowledged uncertainty. Capability claims externally benchmarked but contamination-filtered. No hard contradictions between §7, §8, §9; §9.1 sharpens narrative that welfare deflection is a central driver of apparent improvement."

## Gaps the subagent missed
- LAB-Bench FigQA score not extracted — subagent noted this; orchestrator may want re-extract from §8.9.1.
- No quantification of corrigibility-framing discomfort (§7.2.4 mentions it as "most frequently cited discomfort" but no %).
- Per-question welfare table 9.1.A summarized only at high level; 16 topics not enumerated.
- Thinking-token budgets across welfare tasks not specified — makes welfare↔capability causal claims (cross-cutting #1) untestable.
- Identity-level of welfare measurement (weights vs persona vs instance) acknowledged at §7.1.2 but not restated for §7.2–7.4 — orchestrator may want this explicit.
- Blocklist *efficacy* (how many queries it actually filters; false-positive rate) not measured per §9.2.

## Token budget
~1,750 tokens.
