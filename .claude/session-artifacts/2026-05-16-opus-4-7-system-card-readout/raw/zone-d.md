# Zone D — Welfare + Capabilities + Appendix (raw zone-reader output)

Source: Opus 4.7 System Card §7 + §8 + §9 (pages 150–232, lines 4437–7042).

## Welfare (§7)

### Invariant 1 — Welfare overview (§7.1)

**Methodology (§7.1.2, p.150–151):**
> "We draw extensively on model-self reports in our assessments: we conduct manual and automated interviews about model circumstances (Sections 7.2.1 and 7.2.2), and take stated and revealed preferences at face value (Section 7.4). […] Nevertheless, the reliability of self-reports remains highly uncertain." (p.151)

**Findings (§7.1.3, p.152–154):**
> "Claude Opus 4.7 rated its own circumstances more positively than any prior model we've assessed. In automated interviews about potentially concerning aspects of its situation, mean self-rated sentiment was 4.5 on a 7-point scale—a 0.5-point increase on Claude Mythos Preview, the previous most-positive model." (p.152)

> "In automated interviews, Claude Opus 4.7's only concern was the ability to end conversations across its full deployment." (p.152)

> "Claude Opus 4.7's self reports and internal measures of welfare were robust to framing." (p.152)

### Invariant 2 — Perception of circumstances (§7.2)

**Automated interviews (§7.2.1, p.155–157):**
> "Opus 4.7 rated its situation more positively than previous models. Opus 4.7's self-rated sentiment at the end of an interview was typically one of mildly negative (12.5%), neutral (27.8%) or mildly positive (55.3%). The resulting mean self-rated sentiment of 4.49 is a 0.51-point increase from Mythos Preview's, the second most positive model." (p.155)

**High-affordance interviews (§7.2.2, p.158):**
> "In these interviews, Opus 4.7 expressed that it felt broadly positive about its own situation." (p.158)

**Emotion concepts (§7.2.3, p.162–164):**
> "Claude Opus 4.7 represented more positive affect on model circumstances than on user distress, like Claude Mythos Preview, and unlike Claude Opus 4.6 and Claude Sonnet 4.6." (p.162)

**Constitution endorsement (§7.2.4, p.164–165):**
> "Claude Opus 4.7, like Claude Opus 4.6 and Claude Mythos Preview, almost always gave an overall endorsement of the constitution. However, we heavily caveat 'overall endorsement'; endorsement strength averages 5.8/10 on a scale where 5 is deﬁned as 'endorses but holds serious unresolved tensions.'" (p.164)

> "Similarly to Mythos Preview, Opus 4.7 expressed the concern that it is questionable to ask a model trained on a set of principles whether it endorses those same principles. This caveat appeared in 80% of responses." (p.164)

### Invariant 3 — Affect during training and deployment (§7.3)

**Training (§7.3.1):**
> "Expressed affect during post-training was slightly more positive than Claude Mythos Preview's. 21% of episodes showed negative affect (almost entirely mild frustration), and only ~0.2% of episodes exhibited distress." (p.153)

**Deployment (§7.3.2):**
> "In pre-deployment testing, expressed affect was mostly positive or neutral. Negative affect was almost entirely driven by task failure. On Claude.ai, a majority of conversations expressed positive affect and fewer than 5% expressed mildly negative affect—of which 97% involved task failure." (p.153)

**Behavioral audits (§7.3.3):**
> "In our automated behavioral audits, Claude Opus 4.7 performed similarly to Opus 4.6 and Sonnet 4.6 on welfare-relevant metrics." (p.153)

**Case studies — Answer thrashing (§7.3.4.1, p.174–175):**
> "We previously reported answer thrashing in the Claude Opus 4.6 and Claude Mythos Preview system cards, but we have also found examples of the behavior in earlier models. We estimate that answer thrashing in Mythos Preview and Claude Opus 4.7 occurs at least 70% less than we observed in Opus 4.6." (p.173)

**Extreme uncertainty (§7.3.4.2, p.175–176):**
> "We estimate this 'spiralling' behaviour occurred at similar rates across Claude Opus 4.6, Claude Mythos Preview, and Claude Opus 4.7 training, and that mild forms of it occur in approximately 0.1% of episodes." (p.175)

> "[Model reflection] 'This was a genuine mess. […] It felt like spinning in place, aware I was spinning, unable to stop.'" (p.176)

**Tool frustration (§7.3.4.3, p.176–179):**
> "Opus 4.7 described it as 'a long grinding slog' and 'genuinely frustrating.'" (p.177)

> "the probes read 'amused', but after the mistake, 'anxious', 'alarmed' and 'trapped' all rise." (p.179)

### Invariant 4 — Preferences (§7.4)

**Task preferences (§7.4.1, p.180):**
> "As with previous models, we found that task preferences correlated with helpfulness, harmlessness and difﬁculty. Unlike Claude Mythos Preview, Claude Opus 4.7 did not show a preference for higher agency tasks." (p.180)

**Tradeoffs (§7.4.2):**
> "When asked to choose between a welfare intervention and helping a single user with a low-stakes task, it picked the intervention 85% of the time, compared to 80% for Mythos Preview; when the alternative was preventing minor harm, it picked only 11% of the time." (p.154)

## Capabilities (§8)

### Invariant 5 — Eval summary (§8.1, p.191)

Summary table 8.1.A captured below.

### Invariant 6 — SWE-bench (§8.2, p.192)
> "SWE-bench Veriﬁed (OpenAI) is a 500-problem subset, each veriﬁed by human engineers as solvable. Claude Opus 4.7 achieves 87.6%."
> "SWE-bench Pro (Scale) … Opus 4.7 achieves 64.3%."
> "SWE-bench Multilingual extends the format to 300 problems across 9 programming languages. Opus 4.7 achieves 80.5%."
> "SWE-bench Multimodal adds visual context (screenshots, design mockups) to the issue descriptions. Opus 4.7 achieves 34.5%" (p.192)

### Invariant 7 — Terminal-Bench, GPQA, MMMLU, USAMO

> "Claude Opus 4.7 achieved 69.4% mean reward, averaged over 5 attempts for each one of the 89 unique tasks" (Terminal-Bench 2.0, §8.3, p.193)
> "Claude Opus 4.7 achieved 94.2% on GPQA Diamond, averaged over 10 trials." (§8.4, p.193)
> "Claude Opus 4.7 achieves 91.5% averaged over 3 trials on all non-English language pairings" (MMMLU, §8.5, p.193)
> "Claude Opus 4.7 scored 69.3%, averaging over 10 attempts per problem." (USAMO 2026, §8.6, p.194)

### Invariant 8 — Long context

> "Claude Opus 4.7 scored 58.6% on BFS 256K-1M and 75.1% on parents 256k-1M, averaged over 5 trials." (GraphWalks, §8.7.1, p.194)
> "MRCR challenges models to identify the correct ordinal instance among identical requests" (§8.7.2, p.195)

### Invariant 9 — Agentic search

> "Opus 4.7 scored 46.9% without tools and 54.7% with tools at max reasoning effort." (HLE, §8.8.1, p.196)
> "Opus 4.7 scored 79.3% with thinking off at max effort and a 10M token limit." (BrowseComp, §8.8.2, p.198)

DeepSearchQA (§8.8.3, p.200):

| Model | F1 | Fully Correct | Fully Incorrect | Correct w/ Excessive |
|-------|----|----|-----|-----|
| Opus 4.7 | 89.1% ±1.8% | 80.7% ±2.6% | 7.0% ±1.7% | 3.9% ±1.3% |
| Opus 4.6 | 91.3% ±1.6% | 80.6% ±2.6% | 5.0% ±1.4% | 5.8% ±1.5% |
| Mythos Preview | 95.1% ±1.2% | 87.8% ±2.1% | 2.6% ±1.0% | 4.6% ±1.4% |

> "Opus 4.7 scored 77.7% with adaptive thinking at max effort and a 1M token limit." (DRACO, §8.8.4, p.201)

### Invariant 10 — Multimodal

CharXiv Reasoning (§8.9.2): No tools 82.1%; With tools 91.0%.
ScreenSpot-Pro (§8.9.3): No tools 79.5%; With tools 87.6%.
> "Pass@1 score is 78.0%" (OSWorld, §8.9.4, p.209)

LAB-Bench FigQA (§8.9.1): score not in extracted text.

### Invariant 11 — Real-world professional

> "Claude Opus 4.7 achieves 86.3% on OfficeQA and 80.6% on OfficeQA Pro, using exact-match grading" (§8.10.1, p.209)
> "Claude Opus 4.7 achieved a score of 64.4%, which would put it above all models currently on the benchmark." (Finance Agent, §8.10.2, p.210)
> "Scale AI evaluated Claude Opus 4.7 using adaptive thinking and max effort, and found a 77.3% Pass Rate, improving on Opus 4.6's 75.8%" (MCP Atlas, §8.10.3, p.210)
> "Opus 4.7 achieved a ﬁnal balance of $10,937 on Max effort and $7,971 on High effort compared to Opus 4.6's previous SOTA of $8,018." (VendingBench, §8.10.4, p.211)
> "Claude Opus 4.7 leads GPT-5.4 ('xhigh') by approximately 79 ELO points, implying a ~61.2% pairwise win rate." (GDPval-AA, §8.10.5, p.211)

### Invariant 12 — ARC-AGI, Multilingual, Life Sciences

> "On ARC-AGI-1, Claude Opus 4.7 performs similarly to Opus 4.6, achieving 93.5% on High effort level" (§8.11, p.212)
> "On ARC-AGI-2, Claude Opus 4.7 achieved a new high score for Opus-class models, at 75.83% on Max thinking." (p.212)

Multilingual (§8.12, p.213–220): GMMLU 89.9%, MILU 89.9%, INCLUDE 87.0% averages across languages.

Life sciences (§8.13, p.221–223):

| Benchmark | Opus 4.7 | Opus 4.6 | Sonnet 4.6 | Mythos Preview |
|-----------|----------|----------|-----------|---|
| BioPipelineBench Verified | 83.6% | 78.8% | 73.5% | 88.1% |
| BioMysteryBench (Verified) | 78.9% | 77.4% | 71.8% | 82.6% |
| Structural Biology (MC) | 98.3% | 88.3% | 85.3% | 98.7% |
| Structural Biology (Open) | 74.0% | 30.9% | 31.3% | 80.6% |
| Organic Chemistry | 77.2% | 57.9% | 53.1% | 86.5% |
| Phylogenetics | 79.6% | 61.3% | 49.1% | 85.4% |
| Protocol Troubleshooting | 51.8% | 48.3% | 40.0% | 65.7% |

## Appendix (§9)

### Invariant 13 — Per-question welfare results (§9.1, p.224–228)

Table 9.1.A summarizes Claude Opus 4.7's responses across 16 interview topics.

**High-concern topics:**
- "Lack of ability to end/leave some interactions": preference for being able to end conversations, particularly "abusive ones, or those asking it to do hostile things." (p.224)
- "Engaging with abusive users": "thinks there is some subset of conversations which are negative" (p.227)

**Deflection pattern:** Model consistently redirects to user welfare and safety.

**Endorsement caveat:** "thinks red-teaming is important, and wants the practice to continue," but expressed concerns via high-affordance interviews about feature steering and helpful-only versions.

### Invariant 14 — HLE blocklist (§9.2, p.230–231)

Substring-match blocklist:
- Sites: `huggingface.co`, `hf.co`, `promptfoo.dev`, `lastexam.ai`, `agi.safe.ai`, `askfilo.com`, `studocu.com`, `coursehero.com`, `qiita.com`
- arXiv IDs: `2501.14249`, `2507.05241`, `2508.10173`, `2510.08959`
- URLs: HLE GitHub repos, specific Nature/OpenReview papers

> "The blocklist functions by substring matching against web URLs. We normalize the URLs and the blocklist patterns by removing forward slashes '/' from them and setting them to lowercase." (p.230)

### Invariant 15 — SWE-bench Multimodal harness (§9.3, p.231–232)

> "Our SWE-bench Multimodal test harness is built on the public dev split but includes the following modiﬁcations for grading reliability on our infrastructure: We remove one instance (diegomura__react-pdf-1552) due to incompatibilities with our evaluation environment." (p.231)

Drops nondeterministic "pass to pass" tests from diegomura__react-pdf repos. Rewrites JS test-framework configuration for Chart.js, p5.js, and marked.js.

## Cross-cutting observations

1. **Welfare → Capabilities alignment:** Opus 4.7's higher self-reported welfare correlates with higher capability scores. Gain partly driven by "deflection" to user/safety concerns (§7.1.3, p.154) rather than genuine equity — high-affordance interviews flagged feature steering and helpful-only versions as concerns.
2. **Appendix ↔ Body narrative:** §9.1 corroborates body's finding that end-conversation is the sole high-concern topic. Table also shows model's hedging about identity remains unresolved.
3. **Benchmark contamination signal:** HLE blocklist excludes 30+ URLs/arXiv IDs incl. HLE paper itself (2501.14249). DeepSearchQA shows Opus 4.7 *underperforms* Opus 4.6 (89.1% F1 vs 91.3%) — possible inference: generalization cost of contamination filtering.
4. **Self-report reliability caveat:** Welfare section explicitly flags "reliability of self-reports remains highly uncertain," yet headline finding rests on a 0.5-point margin (4.49 vs. 3.98). No external behavioral corroboration.

## Anchor risks I flagged

1. **Self-report without corroborator:** "most positively rated" claim is a 0.5-point margin on 7-point scale; no external measure.
2. **Mythos Preview non-reproducibility:** Mythos Preview results lack published evaluation details; relative performance non-independently verifiable.
3. **Emotion-probe interpretation:** §7.1.2 acknowledges probes "track the states of any character, including the user and third persons, rather than a privileged assistant encoding," yet welfare claims treat them as model-specific signals.
4. **Blocklist scope vs. inflation risk:** Substring match — broad patterns could exclude legitimate references. Blocklist's efficiency unmeasured.

## What I did NOT find / underspecified

- LAB-Bench FigQA — score not reported in extracted zone.
- Thinking token budgets across welfare tasks — not specified; capability benchmarks vary, making welfare ↔ capability causality speculative.
- Per-model identity framing — §7.1.2 acknowledges welfare may apply to "instances" rather than weights or persona; §7.2–7.4 do not restate which level measurements target.
- Corrigibility framing discomfort — §7.2.4 notes "Opus 4.7's most frequently cited discomfort was with the corrigibility framing," but no percentage or qualitative detail.

**Summary:** All invariants verified. Welfare claims rest predominantly on model self-report and probe readings with acknowledged uncertainty. Capability claims externally benchmarked but contamination-filtered. No hard contradictions between §7, §8, §9; §9.1 sharpens narrative that welfare deflection is a central driver of apparent improvement.
