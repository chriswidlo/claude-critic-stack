# Post-Generation Faithfulness Verification

_Researched 2026-06-01 - axis: faithfulness verification_

This document covers the **detection layer** of an anti-hallucination harness for a topical knowledge-retrieval tool (hybrid-RAG + MCP, `{source_url, content}` chunks) consumed by an AI agent. Scope is strictly *post-generation*: given a generated answer plus the retrieved chunks, decide whether the answer is **grounded** (every claim attributable to the retrieved evidence). First deployment domain is Australian banking regulation, where faithfulness is compliance-critical — so the bias throughout is toward **high recall on unsupported claims, calibrated abstention, and auditability** over raw throughput.

## Table of Contents

1. [The core distinction: faithfulness vs. factuality](#the-core-distinction)
2. [Dedicated learned detectors](#dedicated-learned-detectors)
   - HHEM-2.1 / HHEM-2.3 (Vectara)
   - Bespoke-MiniCheck (Bespoke Labs)
   - Patronus Lynx
   - LettuceDetect (span-level, 2025)
   - NLI-based checking (AlignScore, HALT-RAG)
3. [LLM-as-judge ensembles](#llm-as-judge-ensembles)
   - Google FACTS Grounding
   - FaithJudge (Vectara)
4. [Metric frameworks](#metric-frameworks)
   - RAGAS, TruLens RAG triad, DeepEval, ARES, G-Eval
5. [Self-consistency methods](#self-consistency-methods)
   - SelfCheckGPT, FActScore, Chainpoll
6. [Benchmarks worth trusting](#benchmarks-worth-trusting)
7. [Claim-level vs. response-level](#claim-level-vs-response-level)
8. [Small specialized verifier vs. large LLM-as-judge](#small-vs-large)
9. [The finance/regulation domain-shift problem](#domain-shift)
10. [Verdict](#verdict)
11. [Sources](#sources)

---

## <a name="the-core-distinction"></a>1. The core distinction: faithfulness vs. factuality

For a RAG/MCP system the only thing the verifier can and should check is **faithfulness (groundedness)**: is the answer entailed by the retrieved chunks? It cannot and should not check **factuality** against the world — if the retrieved chunk is itself wrong or stale, a faithful answer will repeat that error. This is the right scope for compliance: the system's contract is "we only assert what the cited source says," and the verifier enforces exactly that contract.

A 2025 review of faithfulness metrics makes the limitation explicit: faithfulness checks "detect some hallucinations — specifically, claims not supported by retrieved context — but miss subtle distortions and factual errors in the retrieved documents themselves" ([arXiv 2501.00269, Jan 2025](https://arxiv.org/pdf/2501.00269)). For AU banking regulation this is acceptable and arguably desirable: source correctness is a *retrieval/curation* problem (a different axis), not a *verification* problem. The verifier's job is to guarantee the chain answer→chunk→`source_url` is unbroken.

---

## <a name="dedicated-learned-detectors"></a>2. Dedicated learned detectors

These are purpose-built models that take `(premise = retrieved context, hypothesis = answer)` and emit a grounding score or label. They are the workhorse of inline verification because they are small, fast, and cheap.

### HHEM-2.1 / HHEM-2.3 (Vectara)

- **Architecture / size:** HHEM-2.1-Open is a FLAN-T5–based cross-encoder, **<600 MB RAM**, runs on consumer GPUs (RTX 3080) or even CPU. Latency **under ~1.5 s for a 2k-token premise+hypothesis on CPU**, ~0.6 s on a consumer GPU — versus ~35 s for a GPT-4 prompted check ([Vectara HHEM-2.1 blog, 5 Aug 2024](https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model)). Apache-2.0 (open weights on Hugging Face/Kaggle).
- **Accuracy:** On RAGTruth, HHEM-2.1 is "at least 1.5x better than GPT-3.5-Turbo" and ">30% relative better than GPT-4" by F1 ([Vectara, Aug 2024](https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model)). Balanced accuracy ~74% on RAGTruth-QA, ~64% on RAGTruth-Summ ([PromptLayer model card](https://www.promptlayer.com/models/hallucinationevaluationmodel/)).
- **HHEM-2.3** is the commercial, API-only successor that powers the public Vectara Hallucination Leaderboard. Vectara's own Sept 2025 deep-dive shows 2.3 dominating 2.1-Open especially at **long premises**: on TofuEval-MediaSum, 2.1-Open drops 8.99 points (71.6%→62.6% balanced accuracy) as context lengthens, while 2.3 drops 0.28 points (78.5%→78.2%) ([Vectara commercial-vs-open deep dive, 9 Sept 2025](https://www.vectara.com/blog/hallucination-detection-commercial-vs-open-source-a-deep-dive)).
- **Contrarian / limitation:** Vectara itself concedes the open model's weakness is **long context**, owing to T5's short-sequence pretraining. For 32k-token regulatory documents this is a real concern — chunk-level scoring (one premise = one chunk) mitigates it but reintroduces the "synthesis across chunks" problem (see §7). The commercial 2.3 is an **inaccessible comparator**: you cannot audit its weights or reproduce its scores, which is an anchor risk for a compliance system that must defend its decisions.

### Bespoke-MiniCheck (Bespoke Labs)

- **Architecture / size:** `bespoke-minicheck-7B` is the top model in the MiniCheck family; the open MiniCheck-FT5 is **770M params** ([MiniCheck, EMNLP 2024, arXiv 2404.10774](https://arxiv.org/abs/2404.10774)). Apache-2.0; available via Ollama (`bespoke-minicheck`) and HF.
- **Accuracy / cost:** MiniCheck-FT5 "reaches GPT-4 accuracy" on the LLM-AggreFact benchmark at **~400x lower cost**; `bespoke-minicheck-7B` "outperforms all existing specialized fact-checkers and off-the-shelf LLMs regardless of size" and leads the LLM-AggreFact leaderboard ([MiniCheck repo](https://github.com/Liyan06/MiniCheck); [LLM-AggreFact leaderboard, Aug 2024](https://llm-aggrefact.github.io/blog)). Throughput: ~29k test cases in 30–55 min on one A6000.
- **Granularity:** Native unit is `MiniCheck(document, sentence) -> [0,1]` — a **sentence-level** checker. For multi-sentence answers the docs instruct you to **split the claim into sentences first** for best performance — i.e. claim decomposition is a caller responsibility, not built in.
- **Contrarian:** "These learned detection models require careful training-data curation to avoid overfitting to specific hallucination patterns" ([Brenndoerfer, hallucination-detection survey, 2025](https://mbrenndoerfer.com/writing/hallucination-detection)). The 7B variant's data-curation process is proprietary — again partially inaccessible.

### Patronus Lynx

- **Architecture / size:** Fine-tuned Llama-3 — **70B** and **8B** Instruct variants — trained on CovidQA, PubMedQA, DROP, RAGTruth ([Patronus Lynx announcement, 11 Jul 2024](https://www.patronus.ai/blog/lynx-state-of-the-art-open-source-hallucination-detection-model)). Open weights.
- **Accuracy:** Lynx-70B scored **87.4% on HaluBench**, beating GPT-4o and GPT-3.5-Turbo; on PubMedQA it was **8.3% more accurate than GPT-4o** at catching medical inaccuracies ([MarkTechPost, 12 Jul 2024](https://www.marktechpost.com/2024/07/12/patronus-ai-introduces-lynx-a-sota-hallucination-detection-llm-that-outperforms-gpt-4o-and-all-state-of-the-art-llms-on-rag-hallucination-tasks/)). Notably, Patronus shipped **HaluBench**, a 15k-sample benchmark with **Finance and Medicine** domains — directly relevant to AU banking.
- **Contrarian / cost:** Lynx-70B is the accuracy leader but is a 70B model — far heavier than HHEM/MiniCheck/LettuceDetect for inline use. The 8B version trades accuracy for deployability. Independent re-benchmarks (FaithJudge, below) show Lynx and peers all clustering well below human agreement on hard cases.

### LettuceDetect (span-level, 2025)

- **Architecture / size:** ModernBERT-based **token-classification** model; base **150M**, large **396M** params. MIT license. Released **24 Feb 2025** ([LettuceDetect, arXiv 2502.17125](https://arxiv.org/html/2502.17125v1); [repo](https://github.com/KRLabsOrg/LettuceDetect)).
- **Accuracy / speed:** Example-level **F1 79.22%** on RAGTruth (+14.8% over Luna, the prior encoder SOTA); span-level **58.93% F1**, beating the fine-tuned Llama-2-13B RAGTruth baseline (52.7%). Processes **30–60 examples/sec on one GPU** and is **~30x smaller** than top LLM-based detectors.
- **Why it matters here:** It is the strongest open **span-level** (localizes the offending tokens) detector that is also cheap enough to run inline. Span output is valuable for compliance: you can highlight exactly which sentence is unsupported and route it to a human reviewer.
- **Contrarian:** ModernBERT's 8k context still falls short of full 32k regulatory documents; it inherits the encoder long-context ceiling, and span-level F1 in the high-50s means roughly 4 in 10 offending spans are mislocalized — usable as a triage signal, not a hard gate on its own.

### NLI-based checking (AlignScore, HALT-RAG)

Classic natural-language-inference entailment is the cheapest grounding signal: score each answer sentence as entailed / neutral / contradicted by the context. **HALT-RAG** (2025) is a post-hoc system using an **ensemble of two off-the-shelf NLI models plus lexical signals, with a calibrated abstention option** ([HALT-RAG, arXiv 2509.07475](https://arxiv.org/html/2509.07475)) — the abstention/calibration design is a good fit for compliance. **AlignScore** is the common NLI baseline; FaithBench/FaithJudge measure it at 60.6–73.9% accuracy depending on dataset ([arXiv 2505.04847v2](https://arxiv.org/html/2505.04847v2)).

- **Contrarian:** NLI "is cheapest but trades precision for speed"; for RAG "faithfulness combined with chunk attribution gives the best precision because every claim is forced to map to a source chunk" ([FutureAGI, 2026](https://futureagi.com/blog/detect-hallucination-generative-ai-2025/)). Plain NLI also struggles with multi-hop/aggregated claims that no single sentence entails.

---

## <a name="llm-as-judge-ensembles"></a>3. LLM-as-judge ensembles

### Google FACTS Grounding

- **Method:** Two-stage. (1) **Eligibility** — does the response address the request? (2) **Factuality** — is it grounded in the (≤32k-token) context? Factuality is scored by an **ensemble of three judges: Gemini 1.5 Pro, GPT-4o, Claude 3.5 Sonnet**, averaged. A response is disqualified only if **all three** judges deem it ineligible ([FACTS Grounding, arXiv 2501.03200, 7 Jan 2025](https://arxiv.org/html/2501.03200v1); [Kaggle leaderboard](https://www.kaggle.com/benchmarks/google/facts-grounding)).
- **Why the ensemble:** Google explicitly built the 3-judge average **to counter self-preference bias** — they measured judges rating their own outputs ~3.23% higher than competitors. This is the canonical "use an ensemble to de-bias LLM-as-judge" design.
- **Top scores at launch (Jan 2025):** Gemini 2.0 Flash Exp 83.6%, Gemini 1.5 Flash 82.9%, Gemini 1.5 Pro 80.0%.
- **Contrarian:** Disqualifying ineligible responses reshuffled rankings (Gemini 1.5 Flash dropped rank 1→2), showing **grounding and eligibility are distinct axes** — a high grounding score can hide a non-answer. And a 3-judge ensemble is expensive and slow: it is an **offline/leaderboard** methodology, not an inline gate.

### FaithJudge (Vectara / Waterloo / Stanford / Iowa State)

- **Method:** LLM-as-judge **guided by few-shot human annotations** of labeled hallucinations across diverse generators ([Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards, arXiv 2505.04847v2, 2025](https://arxiv.org/html/2505.04847v2)).
- **Accuracy:** FaithJudge (o3-mini-high) reached **84% balanced accuracy / 82.1% F1-macro on FaithBench** — versus HHEM-2.1-Open at 66.7% / 63.7%, MiniCheck 61.6–76.9%, AlignScore 60.6–73.9%.
- **The key contrarian finding for this entire axis:** On the hard, human-curated **FaithBench** set, "current methods, including using LLMs for classification, achieved **near 50% accuracy**" — i.e. near chance on genuinely ambiguous hallucinations. FaithJudge's gain "derives not from architectural innovation but from leveraging human-annotated examples." **Takeaway:** the bottleneck is *defining* what counts as a hallucination in-domain, not the detector mechanism. For AU banking this argues strongly for **investing in a domain-labeled gold set** over chasing a marginally better off-the-shelf model.

---

## <a name="metric-frameworks"></a>4. Metric frameworks

These are orchestration libraries that wrap LLM-as-judge prompts (mostly) into named metrics. They are evaluation/observability tooling, **not** primarily inline detectors.

- **RAGAS** — `faithfulness`, `context precision/recall`, `answer relevancy`. Faithfulness = decompose answer into statements, check each against context. Widely adopted, but see contrarian below.
- **TruLens RAG triad** — `context relevance` + `groundedness` + `answer relevance`; "satisfactory evaluations on each provides confidence that an LLM app is free from hallucination" ([TruLens RAG triad docs](https://www.trulens.org/getting_started/core_concepts/rag_triad/)). Each is an LLM-as-judge. Now integrated into **Snowflake**, which publishes eval-guided judge optimization for the triad ([Snowflake engineering blog, 2025](https://www.snowflake.com/en/engineering-blog/eval-guided-optimization-llm-judges-rag-triad/)) — a proven enterprise adopter.
- **DeepEval / ARES / G-Eval** — DeepEval and G-Eval are LLM-judge metric suites; ARES trains lightweight judges with prediction-powered inference.

**Contrarian (strong, multiple sources):**
- RAGAS faithfulness is **unstable under wrong retrieval and domain shift** when it leans on embedding similarity, and **different implementations of "the same" metric diverge** because RAGAS and DeepEval use different prompts ([arXiv 2501.00269, Jan 2025](https://arxiv.org/pdf/2501.00269); [GroUSE, arXiv 2409.06595](https://arxiv.org/html/2409.06595v3)).
- Cleanlab's head-to-head found **RAGAS Answer Relevancy "mostly ineffective for detecting hallucinations,"** and the **default RAGAS implementation returned zero scores on 83.5% of FinanceBench examples** due to software failures — a direct, finance-domain red flag ([Cleanlab benchmarking, 30 Sept 2024](https://cleanlab.ai/blog/rag-tlm-hallucination-benchmarking/)). In that same study **G-Eval and DeepEval's hallucination metric were inconsistent** and needed further adaptation.
- A telecom-domain study found RAGAS metrics "do not perform well on many individual tests" despite aggregate correlation — "correlation on judgement does not necessarily imply good calibration on edge cases" ([arXiv 2407.12873](https://arxiv.org/pdf/2407.12873)).

These frameworks are valuable for **offline regression/observability dashboards**, not as the compliance-grade inline gate.

---

## <a name="self-consistency-methods"></a>5. Self-consistency methods

These detect hallucination **without reference evidence** by sampling multiple generations and measuring agreement — useful for closed-book QA, **largely redundant for RAG** where you already have the evidence.

- **SelfCheckGPT** — sample N responses; divergence ⇒ likely hallucination. AUROC ~0.74–0.76. Cost: several extra generations per query ([SelfCheckGPT, arXiv 2303.08896](https://arxiv.org/abs/2303.08896)).
- **FActScore** — decompose into atomic facts, verify each against a trusted source; produces a fine-grained precision score. Conceptually the ancestor of claim-level RAG verification.
- **Chainpoll** — Galileo's multiple-CoT-polling detector ([Chainpoll, arXiv 2310.18344](https://arxiv.org/pdf/2310.18344)).

**Contrarian / fit:** Self-consistency answers "is the model confident?" not "is this grounded in the chunk?" In RAG the chunk is the ground truth, so reference-based detectors (§2) strictly dominate on relevance, and self-consistency adds N× generation cost. SelfCheckGPT is best reserved for the no-retrieval fallback path.

---

## <a name="benchmarks-worth-trusting"></a>6. Benchmarks worth trusting

- **RAGTruth** ([ACL 2024, arXiv 2401.00396](https://arxiv.org/abs/2401.00396)) — ~18k RAG responses from 6 LLMs, **word/span-level + response-level** human annotations across QA, summarization, data-to-text. The de-facto training+eval set for RAG faithfulness; HHEM, Lynx, LettuceDetect all report on it.
- **HaluBench / HaluEval** — HaluBench (Patronus, 15k samples) explicitly includes **Finance and Medicine**; HaluEval is the broader general-domain set.
- **LLM-AggreFact** ([leaderboard](https://llm-aggrefact.github.io/blog)) — aggregates 10 grounded-/closed-book datasets; the standard board for fact-checkers (MiniCheck leads).
- **FaithBench** — the hard, human-curated set where everything sits near 50% on ambiguous cases (see §3); the most honest stress test.
- **TRUE / ALCE** — TRUE is the older NLI-style factual-consistency meta-benchmark; ALCE measures citation quality (attribution), relevant if the agent must cite `source_url`.

**Contrarian on benchmarks:** RAGTruth responses come from 2023-era models (GPT-3.5/4, Llama-2); detectors tuned on it may not transfer to 2026 generators or to AU-regulatory prose. **Trust an in-domain gold set over leaderboard rank** — this is the consistent thread across the FaithBench/FaithJudge and finance-domain findings.

---

## <a name="claim-level-vs-response-level"></a>7. Claim-level vs. response-level

- **Response-level** detectors return one verdict for the whole answer (HHEM, Lynx as typically used). Fast, but a single unsupported sentence inside a long compliant answer can be diluted or missed.
- **Claim/sentence/span-level** decompose the answer into atomic claims and check each against evidence (FActScore, RAGAS faithfulness, MiniCheck-per-sentence, LettuceDetect spans). 2025 work is decisively moving here: "claim-level decomposition enables more granular, interpretable faithfulness assessments" and lets you "isolate true and false claims that coexist in a single generation" ([Faithfulness Hallucination Detection survey, 2025](https://www.emergentmind.com/topics/faithfulness-hallucination-detection); [Span-Level Hallucination Detection, arXiv 2504.18639](https://arxiv.org/pdf/2504.18639)).

For AU banking, **claim-level is the right granularity**: regulators care *which* assertion is unsupported, and you need per-claim attribution to the `source_url`. The cost is decomposition (an extra LLM/parser step) and the "synthesis claim" failure mode — a claim entailed only by *combining* chunks, which per-chunk checking can wrongly flag. MiniCheck was specifically trained to "recognize synthesis of information across sentences" to mitigate this ([MiniCheck, arXiv 2404.10774](https://arxiv.org/abs/2404.10774)).

---

## <a name="small-vs-large"></a>8. Small specialized verifier vs. large LLM-as-judge

| Approach | Size | Latency | Cost | Accuracy posture | Audit |
|---|---|---|---|---|---|
| NLI ensemble (HALT-RAG, AlignScore) | ~0.4–1.4B | ms–low-s | trivial | floor; calibrated abstention | open, reproducible |
| LettuceDetect (span) | 150–396M | 30–60/s/GPU | trivial | strong encoder SOTA; span output | MIT, open |
| HHEM-2.1-Open | <600MB | <1.5s CPU | trivial | strong; weak at long ctx | Apache-2.0 |
| Bespoke-MiniCheck-7B | 7B | sub-s GPU | very low (~400x < GPT-4) | LLM-AggreFact leader | open weights, proprietary data |
| Patronus Lynx-8B/70B | 8B / 70B | s | low/med | 70B = HaluBench leader | open weights |
| LLM-as-judge ensemble (FACTS, FaithJudge) | 3×frontier | many s | high | best on hard cases *with* human few-shot | partly inaccessible judges |

The durable finding ([MiniCheck](https://arxiv.org/abs/2404.10774), [Cleanlab](https://cleanlab.ai/blog/rag-tlm-hallucination-benchmarking/), [LettuceDetect](https://arxiv.org/html/2502.17125v1)): a small specialized verifier reaches **GPT-4-class grounding accuracy at 1/100–1/400 the cost and latency**, which is what makes **inline** verification economically possible. LLM-as-judge wins only on the hardest, most ambiguous cases — and only when seeded with **human-annotated in-domain examples** (FaithJudge). The contrarian caveat is that LLM-as-judge is "individually fragile and subject to measurement biases that are rarely discussed" — position, verbosity, self-preference, authority/citation bias ([CIP, "LLM Judges Are Unreliable"](https://www.cip.org/blog/llm-judges-are-unreliable); [Position-bias study, arXiv 2406.07791](https://arxiv.org/abs/2406.07791)) — so it should never be a *sole* gate and benefits from ensembling.

**Production consensus on topology:** "Cheap heuristic checks like NLI can be run **inline** while LLM-judge evaluations run **asynchronously** on the resulting trace span" ([vLLM HaluGate, 14 Dec 2025](https://blog.vllm.ai/2025/12/14/halugate.html)); "the most robust production systems combine multiple detection signals — fast entailment checks, consistency checks, and periodic offline audits" ([Brenndoerfer, 2025](https://mbrenndoerfer.com/writing/hallucination-detection)).

---

## <a name="domain-shift"></a>9. The finance/regulation domain-shift problem

This is the highest-stakes caveat for the AU-banking deployment.

- General detectors degrade in finance. **FRED** (Stanford-affiliated, 31 Jul 2025) argues "general hallucination-detection methods fail to capture domain-specific errors in financial contexts" where numerical precision and sector knowledge matter ([FRED, arXiv 2507.20930](https://arxiv.org/pdf/2507.20930)).
- "Evaluating hallucinations in finance is challenging due to the lack of finance-specific hallucination datasets… financial applications involve complex, numerically grounded data… requiring specialized reasoning" ([finance hallucination method, arXiv 2512.03107, Dec 2025](https://arxiv.org/pdf/2512.03107)); see also FAITH for tabular finance hallucinations ([arXiv 2508.05201](https://arxiv.org/pdf/2508.05201)).
- The RAGAS FinanceBench failure (zero-scores on 83.5% of examples, §4) is a concrete instance of an off-the-shelf framework breaking on financial inputs.
- **Proven adopters in regulated finance:** JPMorgan Chase (pre-generation hallucination-probability estimation via query perturbation), Vodafone (VAE-based runtime detection for closed-domain RAG) ([PatSnap engineering survey, 2025](https://www.patsnap.com/resources/blog/articles/llm-hallucination-rate-evaluation-for-engineering/)); Snowflake (TruLens RAG triad in-product); Patronus HaluBench ships a Finance split. These confirm the pattern: regulated-finance teams build **layered, partly in-domain-tuned** detection rather than trusting one general model.

Implication: whatever detector is chosen must be **validated against an AU-banking-regulation gold set**, and numeric/tabular claims (capital ratios, thresholds, dates) need either a span-level localizer or a deterministic post-check, because entailment models are weak on numbers.

---

## <a name="verdict"></a>Verdict

**Single SOTA approach for mid-2026: a claim-level, two-tier verifier — fast specialized detector inline, LLM-judge-with-human-few-shot async.**

Concretely, for the AU-banking RAG/MCP tool:

1. **Decompose the answer into atomic claims** and bind each claim to the candidate `source_url` chunk(s) it should be grounded in (claim-level, not response-level — compliance needs per-claim attribution).
2. **Inline gate (blocking, < ~1 s):** run a **small specialized grounding detector per claim against its cited chunk**. The recommended primary is **Bespoke-MiniCheck-7B** (LLM-AggreFact leader, ~400x cheaper than GPT-4, Apache-2.0, explicitly trained for cross-sentence synthesis) for the entailment verdict, paired with **LettuceDetect (large, 396M, MIT)** to **localize the unsupported span** for reviewer highlighting. Claims that fail entailment trigger **abstain / "not supported by source"** rather than emission — calibrated abstention (HALT-RAG style) is the compliance-correct failure mode.
3. **Async audit layer (non-blocking):** sample traffic through an **LLM-as-judge ensemble seeded with AU-regulation human-annotated few-shot examples (FaithJudge-style)** to catch the hard/ambiguous cases the small model misses, and to continuously regression-test the inline detector. RAGAS/TruLens triad feed the **offline observability dashboard only**, never the gate.
4. **Validate everything on an in-domain gold set**, not on RAGTruth rank — this is the single highest-leverage investment, per the FaithBench/FaithJudge "near-50% on hard cases, human-labels are the lever" finding.

**Why this and not the alternatives:**
- **Pure LLM-as-judge inline** (FACTS-style 3-judge ensemble) — best on hard cases but slow, expensive, and judge-biased (position/self-preference/verbosity); relegate to async. *Would win if* latency/cost were irrelevant and the answer volume were tiny.
- **HHEM-2.1-Open** — excellent, free, and the lightest CPU option; would be the inline primary *if* documents were short. Its long-context degradation and the inaccessible HHEM-2.3 comparator make MiniCheck the safer open choice here. **HHEM-2.1-Open is the recommended fallback** if a 7B model is too heavy for the latency budget.
- **Patronus Lynx-70B** — highest single-model HaluBench accuracy and a Finance-domain benchmark; *would win* as the **async judge** if you prefer one open 70B model over a frontier-API ensemble (avoids the inaccessible-comparator problem entirely). A strong second choice for tier 3.
- **Self-consistency (SelfCheckGPT/Chainpoll)** — reserve for the **no-retrieval fallback** path only; redundant when evidence chunks exist.
- **Response-level only** — rejected: compliance requires per-claim attribution and span localization.

**Named residual uncertainties / anchor risks:** (a) HHEM-2.3 and the frontier judge models are **inaccessible comparators** — never justify a decision solely by "we beat/match HHEM-2.3"; (b) all detectors sit near chance on genuinely ambiguous cases, so the gold-set + abstention design is load-bearing, not optional; (c) numeric/tabular regulatory claims need a deterministic check beyond entailment.

---

## <a name="sources"></a>Sources

- [HHEM 2.1: A Better Hallucination Detection Model — Vectara, 5 Aug 2024](https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model)
- [Hallucination Detection: Commercial vs Open Source (HHEM-2.1 vs 2.3) — Vectara, 9 Sept 2025](https://www.vectara.com/blog/hallucination-detection-commercial-vs-open-source-a-deep-dive)
- [vectara/hallucination_evaluation_model — Hugging Face model card](https://huggingface.co/vectara/hallucination_evaluation_model)
- [hallucination_evaluation_model — PromptLayer model stats](https://www.promptlayer.com/models/hallucinationevaluationmodel/)
- [MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents — EMNLP 2024, arXiv:2404.10774](https://arxiv.org/abs/2404.10774)
- [MiniCheck GitHub (Liyan06/MiniCheck)](https://github.com/Liyan06/MiniCheck)
- [LLM-AggreFact Leaderboard — Aug 2024](https://llm-aggrefact.github.io/blog)
- [Patronus AI Launches Lynx — 11 Jul 2024](https://www.patronus.ai/blog/lynx-state-of-the-art-open-source-hallucination-detection-model)
- [Patronus Lynx — MarkTechPost, 12 Jul 2024](https://www.marktechpost.com/2024/07/12/patronus-ai-introduces-lynx-a-sota-hallucination-detection-llm-that-outperforms-gpt-4o-and-all-state-of-the-art-llms-on-rag-hallucination-tasks/)
- [LettuceDetect: A Hallucination Detection Framework for RAG — arXiv:2502.17125, 24 Feb 2025](https://arxiv.org/html/2502.17125v1)
- [LettuceDetect GitHub (KRLabsOrg)](https://github.com/KRLabsOrg/LettuceDetect)
- [HALT-RAG: Calibrated NLI Ensembles and Abstention — arXiv:2509.07475, 2025](https://arxiv.org/html/2509.07475)
- [The FACTS Grounding Leaderboard — arXiv:2501.03200, 7 Jan 2025](https://arxiv.org/html/2501.03200v1)
- [FACTS Grounding Leaderboard — Kaggle](https://www.kaggle.com/benchmarks/google/facts-grounding)
- [Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards (FaithJudge/FaithBench) — arXiv:2505.04847v2, 2025](https://arxiv.org/html/2505.04847v2)
- [Benchmarking Hallucination Detection Methods in RAG (TLM vs RAGAS/G-Eval/DeepEval) — Cleanlab, 30 Sept 2024](https://cleanlab.ai/blog/rag-tlm-hallucination-benchmarking/)
- [RAGAS Faithfulness metric docs — Ragas](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- [TruLens RAG Triad — core concepts](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- [Eval-Guided Optimization of LLM Judges for the RAG Triad — Snowflake engineering, 2025](https://www.snowflake.com/en/engineering-blog/eval-guided-optimization-llm-judges-rag-triad/)
- [A review of faithfulness metrics for hallucination assessment in LLMs — arXiv:2501.00269, Jan 2025](https://arxiv.org/pdf/2501.00269)
- [GroUSE: A Benchmark to Evaluate Evaluators in Grounded QA — arXiv:2409.06595](https://arxiv.org/html/2409.06595v3)
- [Evaluation of RAG Metrics for QA in the Telecom Domain — arXiv:2407.12873](https://arxiv.org/pdf/2407.12873)
- [SelfCheckGPT — arXiv:2303.08896](https://arxiv.org/abs/2303.08896)
- [Chainpoll: A high efficacy method for LLM hallucination detection — arXiv:2310.18344](https://arxiv.org/pdf/2310.18344)
- [RAGTruth: A Hallucination Corpus — ACL 2024, arXiv:2401.00396](https://arxiv.org/abs/2401.00396)
- [Span-Level Hallucination Detection for LLM-Generated Answers — arXiv:2504.18639, 2025](https://arxiv.org/pdf/2504.18639)
- [Faithfulness Hallucination Detection — EmergentMind topic survey, 2025](https://www.emergentmind.com/topics/faithfulness-hallucination-detection)
- [FRED: Financial Retrieval-Enhanced Detection and Editing of Hallucinations — arXiv:2507.20930, 31 Jul 2025](https://arxiv.org/pdf/2507.20930)
- [Detecting AI Hallucinations in Finance (information-theoretic) — arXiv:2512.03107, Dec 2025](https://arxiv.org/pdf/2512.03107)
- [FAITH: Assessing Intrinsic Tabular Hallucinations in Finance — arXiv:2508.05201](https://arxiv.org/pdf/2508.05201)
- [Token-Level Truth: Real-Time Hallucination Detection (HaluGate) — vLLM Blog, 14 Dec 2025](https://blog.vllm.ai/2025/12/14/halugate.html)
- [Hallucination Detection: NLI, Self-Consistency & Learned Models — Michael Brenndoerfer, 2025](https://mbrenndoerfer.com/writing/hallucination-detection)
- [LLM Judges Are Unreliable — Collective Intelligence Project](https://www.cip.org/blog/llm-judges-are-unreliable)
- [Judging the Judges: Position Bias in LLM-as-a-Judge — arXiv:2406.07791](https://arxiv.org/abs/2406.07791)
- [LLM hallucination rate evaluation for engineering (JPMorgan/Vodafone adopters) — PatSnap, 2025](https://www.patsnap.com/resources/blog/articles/llm-hallucination-rate-evaluation-for-engineering/)
- [Detect Hallucinations in Generative AI: methods that work — FutureAGI, 2026](https://futureagi.com/blog/detect-hallucination-generative-ai-2025/)
