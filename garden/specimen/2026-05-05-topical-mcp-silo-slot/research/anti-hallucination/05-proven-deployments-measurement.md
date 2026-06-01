# Anti-Hallucination — Proven Deployments, Expert Consensus & Measurement (2025–2026)

_Researched 2026-06-01 - axis: proven deployments & measurement_

This document triangulates **what the field's named leaders actually do to prevent and measure hallucination** in high-stakes topical retrieval, **what named experts and vendors concretely recommend**, **how hallucination is measured in production**, and **how regulated-domain products handle the liability of a wrong-but-grounded-looking answer**. It names companies and people, quotes concrete guidance with dates, and surfaces the strongest contrarian camp prominently before stating a single convergent default.

Scope note: a sibling document ([06-proven-deployments-experts.md] in this research set) covers the *retrieval pipeline shape* (hybrid + rerank + contextual chunking, Jason Liu / Chroma / Vespa / Anthropic Contextual Retrieval). This document does **not** re-litigate the pipeline; it owns the **anti-hallucination and measurement** layer that sits on top of it.

---

## Table of Contents

1. [What leading products actually do](#1-what-leading-products-actually-do)
2. [What named experts and vendors recommend](#2-what-named-experts-and-vendors-recommend)
3. [How hallucination is measured in production](#3-how-hallucination-is-measured-in-production)
4. [Building a gold eval set (the concrete recipe)](#4-building-a-gold-eval-set-the-concrete-recipe)
5. [Regulated-domain precedent (legal / financial / medical)](#5-regulated-domain-precedent-legal--financial--medical)
6. [Where the field converges — the de-facto default stack](#6-where-the-field-converges--the-de-facto-default-stack)
7. [The loudest contrarian views (surfaced)](#7-the-loudest-contrarian-views-surfaced)
8. [Verdict](#verdict)
9. [Sources](#sources)

---

## 1. What leading products actually do

The striking convergence: every credible product in high-stakes retrieval ships the **same three-part anti-hallucination contract** — (a) ground every claim in retrieved source text, (b) attach a verifiable inline citation to each claim, (c) abstain ("I don't know" / escalate) when grounding is absent. The differentiation is in *enforcement rigor* and *measurement*, not in the contract itself.

### Anthropic — Citations API (the grounding primitive, productized)

Anthropic shipped **Citations** to GA on the Anthropic API and Vertex AI in early 2025, with Amazon Bedrock support following ([Anthropic, "Introducing Citations," 2025](https://claude.com/blog/introducing-citations-api); [AWS, 2025-06](https://aws.amazon.com/about-aws/whats-new/2025/06/citations-api-pdf-claude-models-amazon-bedrock/)). The mechanism is the load-bearing detail for a retrieval tool: the API **chunks source documents into sentences**, and when Claude generates output it returns **exact references to the specific sentences and passages** it used. This is grounding enforced at the API surface rather than coaxed by prompt.

Concrete measured impact, quoted from Anthropic's launch customers:
- **Endex** (financial intelligence): reduced "source hallucinations and formatting issues **from 10% to 0%**" and saw a "**20% increase in references per response**" ([Anthropic, 2025](https://claude.com/blog/introducing-citations-api)).
- **Thomson Reuters / CoCounsel**: Jake Heller (Head of Product) said the feature "helps minimize hallucination risk but also strengthens trust in AI-generated content" ([Anthropic, 2025](https://claude.com/blog/introducing-citations-api)).
- Anthropic's internal evals reported "up to **15%** improvement in recall accuracy" vs. customer-built citation prompting ([Anthropic, 2025](https://claude.com/blog/introducing-citations-api)).

Simon Willison's contemporaneous analysis underscores *why this matters for a RAG tool*: citations are computed by the API against the supplied documents, so "the model can't cite a document it wasn't given" — the citation is mechanically tied to provided context, not to parametric memory ([Willison, 2025-01-24](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/)).

### Harvey (legal) — claim-decomposition + verify, with a measured rate

Harvey publishes the most rigorous public anti-hallucination methodology of any vertical product. From **"BigLaw Bench: Hallucinations"** (Harvey, 2024-10-07):
- **Definition:** a hallucination is "a factual claim made by an LLM that can be **demonstrably disproven by reference to a source of truth**."
- **Detection methodology (two-step):** the system first "break[s] down an answer into all of its relevant factual claims," then "consider[s] whether each factual claim made in the answer is true based on the information in the source-of-truth documents." This is **claim-level decomposition + per-claim verification**, validated against human review.
- **Measured rate:** Harvey's Assistant hallucinated on **~0.2% of claims (≈1 in 500)** on BigLaw Bench, vs. foundation models at 0.7% (Claude) and 1.9% (Gemini) in the same harness ([Harvey, 2024-10-07](https://www.harvey.ai/blog/biglaw-bench-hallucinations)).
- **Grounding:** RAG over authoritative sources, with real-time **Shepardization via LexisNexis** to verify cited cases remain good law — a domain-specific freshness/validity check layered on top of citation.

The transferable pattern: **decompose → verify each claim against source → report a per-claim rate**, not a per-answer pass/fail.

### kapa.ai — "answer with sources, or say I don't know"

kapa.ai (technical-docs Q&A, used by OpenAI, Docker, Mapbox docs) is the clearest productization of **mandatory abstention**. Their stated contract: "every answer is grounded in sources before reaching customers, and when it isn't sure, it says **'I don't know.'**" The system is "designed to provide answers based **solely** on documentation" and runs continuous evals against test sets to catch hallucination drift ([kapa.ai, "What Are AI Hallucinations," 2025](https://www.kapa.ai/blog/ai-hallucination); [kapa.ai product, 2025](https://www.kapa.ai/product/answering-engine)). This is the answer-or-refuse pattern the regulated-domain section below treats as the liability control.

### Perplexity — inline citations as the default UX

Perplexity grounds answers in retrieved web pages via RAG and attaches **clickable inline citations** to spans of the answer. Independent 2025 testing found it "hallucinates ~10% less on complex topics" than non-grounded chat and that inline citation "minimiz[es] hallucinations" relative to Google's AI summaries — while explicitly noting the reduction is "**not absolute**" ([DataStudios, 2025](https://www.datastudios.org/post/does-perplexity-hallucinate-less-than-chatgpt-when-searching-the-web-reliability-and-fact-checking)). Perplexity is the proof that **citation-as-default-UX** is commercially viable at scale; it is *not* proof that citations eliminate error (see §7).

### Glean (enterprise search) — permission-aware grounding + citations

Glean grounds answers in the customer's own indexed corpus, **surfaces citations (deep links) on every answer** so users can verify, and crucially enforces **permission-aware retrieval** — "users only see content they already have access to" ([Glean, "Grounding," 2025](https://www.glean.com/ai-glossary/grounding); [Glean product, 2025](https://www.glean.com/product/system-of-context)). For a regulated knowledge tool, permission-scoped retrieval is itself an anti-hallucination control: it prevents the model from grounding on documents it should never have surfaced.

### Common denominator across the products

| Product | Grounding | Citation | Abstention | Published measurement |
|---|---|---|---|---|
| Anthropic Citations | sentence-chunk, API-enforced | exact sentence refs | (caller policy) | customer 10%→0%; +15% recall |
| Harvey | RAG + Shepardize | citation + reasoning | (review gate) | 0.2% claim-level rate |
| kapa.ai | docs-only | sourced answers | **explicit "I don't know"** | continuous eval vs. test set |
| Perplexity | web RAG | inline clickable | partial | ~10% fewer on complex |
| Glean | corpus, permission-scoped | deep-link citations | rare-miss claim | 1.9× preferred vs ChatGPT |

---

## 2. What named experts and vendors recommend

### OpenAI — Kalai et al., "Why Language Models Hallucinate" (the abstention argument)

The single most influential 2025 paper on *why* grounding+citations is necessary but insufficient. Adam Tauman Kalai, Ofir Nachum, Santosh Vempala, Edwin Zhang (OpenAI), arXiv 2509.04664, **2025-09-04**:
- Core claim: hallucinations arise because "language models are **optimized to be good test-takers, and guessing when uncertain improves test performance**." Most benchmarks reward a confident guess over an honest "I don't know" ([arXiv 2509.04664, 2025-09-04](https://arxiv.org/abs/2509.04664); [OpenAI, 2025](https://openai.com/index/why-language-models-hallucinate/)).
- The fix they recommend is **not another hallucination eval**. It is "modifying the scoring of existing benchmarks" so they "**reward expressions of uncertainty rather than penalizing them**." A lone hallucination eval "has little effect against hundreds of traditional accuracy-based evals that penalize humility and reward guessing."
- **Directly load-bearing for an MCP retrieval tool:** the abstention behavior must be *rewarded in your own gold eval*, or the model will optimize toward confident-but-wrong. Measuring only accuracy on answerable questions trains the tool to never abstain.

### Vectara (Amr Awadallah) — HHEM as a deployable factual-consistency scorer

Vectara's **Hughes Hallucination Evaluation Model (HHEM)** is the de-facto industry reference for measuring grounding. It "compares AI-generated responses to the specific source documents they were based on" and emits a **factual-consistency score**; it is the #1 hallucination-detection model on Hugging Face (100k+ downloads) and drives the widely-cited Hallucination Leaderboard ([Vectara docs, 2025](https://docs.vectara.com/docs/hallucination-and-evaluation/hallucination-evaluation); [HuggingFace, vectara/HHEM](https://huggingface.co/vectara/hallucination_evaluation_model)). The leaderboard methodology is instructive for building your own metric: it forces "**Summarize using only the information in the given passage. Do not infer. Do not use your internal knowledge**," then scores whether the output stays factually consistent with the source ([Vectara leaderboard, 2026](https://github.com/vectara/hallucination-leaderboard)). As of mid-2026 the best models score ~1.8–3.3% summarization hallucination — i.e. even SOTA models hallucinate on grounded summarization a few percent of the time.

Awadallah's standing position (May 2025, on launching the Hallucination Corrector): LLMs "still fall distressingly short of the standards for accuracy required in highly-regulated industries like financial services, healthcare, law" ([SiliconANGLE, 2025-05-13](https://siliconangle.com/2025/05/13/vectara-launches-hallucination-corrector-increase-reliability-enterprise-ai/)). Vectara's recommended stack is grounding → HHEM factual-consistency score → a **guardian/corrector agent** that catches and rewrites unsupported spans before they reach the user.

### Patronus AI — Lynx + HaluBench (deployable detector + benchmark)

Patronus open-sourced **Lynx** (a fine-tuned hallucination-detection model that outperformed GPT-4 as a judge) and **HaluBench**, a 15k-sample benchmark "sourced from real-world domains" **including Finance and Medicine** — explicitly the domains earlier datasets omitted ([Patronus, "Lynx," 2024](https://www.patronus.ai/blog/lynx-state-of-the-art-open-source-hallucination-detection-model); [PR Newswire, 2024](https://www.prnewswire.com/news-releases/patronus-ai-launches-lynx-state-of-the-art-open-source-hallucination-detection-model-302194659.html)). Recommendation in practice: run a **reference-free, real-time hallucination detector** (Lynx-style) as an online guardrail, not just an offline eval. Lynx detects 8 hallucination types (coreference errors, calculation errors, CoT hallucinations, etc.) and emits a reasoned score.

### Galileo — Context Adherence / Luna (cheap online groundedness)

Galileo's **Context Adherence** metric (built on the ChainPoll method) measures "**closed-domain hallucinations: cases where your model said things that were not provided in the context**" ([Galileo docs, 2025](https://docs.galileo.ai/galileo/gen-ai-studio-products/galileo-guardrail-metrics/context-adherence)). The key 2025 move is **Luna-2**: small distilled evaluation models (a 440M DeBERTa-class encoder) that "replace the LLM-as-a-judge pattern with distilled small models at a fraction of the cost" ([Luna paper, arXiv 2406.00975](https://arxiv.org/html/2406.00975v2)). Recommendation: groundedness scoring can run **online on every response cheaply**, not just in batch eval — which makes a real-time abstention/escalation gate affordable.

### Jason Liu — measurement-first, synthetic-eval-before-traffic

Liu's anti-hallucination contribution is procedural: **you cannot fix what you don't measure, and you can bootstrap the measurement synthetically.** "Generate 5 questions that can be answered by each chunk" to create a measurable eval set before you have real traffic; track **recall** as the load-bearing retrieval metric because "models can handle irrelevant information, they cannot work with information that wasn't retrieved" ([jxnl.co, 2025-01-24](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/)). For anti-hallucination this means: most "hallucinations" in RAG are actually **retrieval failures** (the right chunk wasn't returned, so the model improvised) — so measure passage-level recall *first*.

### Hamel Husain — evals are the product, look at your data

Hamel's thesis (hamel.dev, 2024-03-29, reinforced through his 2025 "Field Guide" and AI Evals course): "Unsuccessful products almost always share a common root cause: **a failure to create robust evaluation systems.**" Concretely: "You must **remove all friction from the process of looking at data**," do **error analysis** by reading traces, and layer **unit-test-style assertions → human/model grading → A/B** ([hamel.dev, 2024](https://hamel.dev/blog/posts/evals/); ["A Field Guide to Rapidly Improving AI Products," O'Reilly, 2025-04](https://www.oreilly.com/radar/a-field-guide-to-rapidly-improving-ai-products/)). The anti-hallucination implication: **manual trace review of grounded answers** is non-negotiable; automated groundedness scores are a complement, not a replacement.

### Eugene Yan — factual-consistency as a bootstrappable guardrail

Yan frames hallucination control as a **guardrail mediating backend and UX**, and gives a concrete data threshold: with "a few hundred task-specific samples, models can identify obvious factual inconsistencies," and "with a thousand samples or more, it becomes a solid factual-consistency eval... good enough as a hallucination guardrail." He recommends bootstrapping from permissive open data (FIB, USB) to lift a detector's ROC-AUC "from 0.56 (practically random) to 0.85" ([Eugene Yan, "Task-Specific LLM Evals," 2024–2025](https://eugeneyan.com/writing/evals/)). This sets a **build-target**: ~1k labeled grounded/ungrounded examples gets you a usable in-domain detector.

---

## 3. How hallucination is measured in production

The field has converged on a **two-layer measurement model**: an **offline gold-set eval** (regression gate before ship) and an **online groundedness/citation telemetry** (continuous production signal). Both decompose the answer to **claim level** rather than scoring whole answers.

### The core metric: faithfulness / groundedness / context-adherence

These three names describe the same quantity — *does every claim in the answer trace to retrieved context?* The dominant operational definition is **RAGAS Faithfulness**:

> Faithfulness = 1 − (unsupported claims / total claims) — the answer is decomposed into atomic claims, each verified against the retrieved context ([RAGAS docs, 2025](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)).

This claim-decomposition approach is identical in spirit to Harvey's two-step method and Anthropic's sentence-level citation — **the entire field measures hallucination at claim granularity.**

### LLM-as-judge vs. distilled detectors

- **LLM-as-judge** (RAGAS, DeepEval) scales human-quality grading to production volume, achieving "15–20% higher correlation with human judgments than ROUGE/BLEU." But 2025 research on **judge bias** (verbosity inflation, self-preference, position effects) means you **must validate your judge against human labels before trusting it** ([Maxim, "RAG Evaluation," 2025](https://www.getmaxim.ai/articles/rag-evaluation-a-complete-guide-for-2025/); [Cohorte, 2025](https://cohorte.co/blog/evaluating-rag-systems-in-2025-ragas-deep-dive-giskard-showdown-and-the-future-of-context)).
- **Distilled detectors** (Vectara HHEM, Galileo Luna-2, Patronus Lynx) trade a little accuracy for **cost low enough to score every production response online**. This is what makes a real-time abstention gate economically viable.

### The benchmark substrate

- **RAGTruth** (arXiv 2401.00396) — ~18,000 RAG responses with **word-level and span-level** hallucination annotations; the reference corpus for training/evaluating RAG hallucination detectors. Span-level detection remains hard (fine-tuned Llama-2-13B reached only ~52.7% F1), confirming that **fine-grained hallucination detection is unsolved** ([RAGTruth, ACL 2024](https://aclanthology.org/2024.acl-long.585/)).
- **HaluBench** (Patronus) — 15k samples across real domains incl. Finance/Medicine.
- **FaithBench / FaithJudge** — human-annotated summarization hallucinations; FaithJudge automates evaluation with "notably higher agreement with human judgments" ([arXiv 2505.04847, 2025](https://arxiv.org/html/2505.04847v2)).
- **Vectara Hallucination Leaderboard** — the public summarization-grounding leaderboard (HHEM-2.x).

### Online production telemetry (what you actually dashboard)

The convergent production dashboard tracks, per query segment:
1. **Groundedness / faithfulness score** (HHEM / Luna / RAGAS-style) on every answer.
2. **Citation coverage** — fraction of claims with a supporting citation; and **citation-click / citation-verification rate** as a user-trust signal.
3. **Abstention / refusal rate** — and critically, **calibrated abstention**: refuse-when-should-refuse vs. refuse-when-answerable (over-refusal is a real failure mode).
4. **Retrieval recall** on the gold set (because most "hallucinations" are retrieval misses — per Liu).

---

## 4. Building a gold eval set (the concrete recipe)

Synthesizing Liu, Yan, Hamel, Chroma, and the benchmark designers into one buildable procedure for the AU-banking-regulation instance:

1. **Bootstrap synthetically (Liu).** For each chunk in the AU-banking corpus, generate ~5 questions answerable *only* from that chunk. Gives an immediate retrieval-recall + answerable-question set with known gold passages.
2. **Add unanswerable / out-of-corpus questions (OpenAI/Kalai).** Deliberately include questions the corpus *cannot* answer. The correct behavior is **abstain**. Score abstention explicitly — otherwise you train confident guessing. This is the single most-skipped step and the most important for a regulated tool.
3. **Label at claim level (Harvey/RAGAS).** For each gold answer, decompose into atomic claims and mark each supported / unsupported. Faithfulness = supported/total.
4. **Get to ~1k labeled examples (Yan).** Below a few hundred you get only obvious-error detection; ~1k makes an in-domain detector usable (ROC-AUC ~0.85). Use HaluBench/RAGTruth as a structural template; re-annotate in-domain.
5. **Validate the judge (2025 judge-bias research).** Before trusting an LLM-as-judge or HHEM/Luna detector, correlate its scores against a human-labeled subset; report the correlation as a property of your eval, not a given.
6. **Read the data (Hamel).** Have a domain expert (here: someone who knows AU banking regulation) read a sample of traces every cycle. Automated scores miss domain-specific subtleties (e.g., a citation that is *real* but to a *superseded* regulation — exactly the Harvey "is it still good law" problem).
7. **Gate + dashboard.** Offline gold set is a **regression gate** (block ship on faithfulness/abstention regressions); online HHEM/Luna scoring + citation-coverage + calibrated-abstention is the **continuous production signal**.

---

## 5. Regulated-domain precedent (legal / financial / medical)

This is where the "grounded-looking but wrong" liability is most studied — and the most important evidence for a banking-regulation tool.

### The cautionary empirical result — Stanford RegLab

The defining study: **"Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools"** (Stanford RegLab + HAI; preprint 2024-05, peer-reviewed in *Journal of Empirical Legal Studies*, 2025). Across 202 expert-scored queries, **commercial RAG legal tools hallucinated 17%–33% of the time**: Lexis+ AI >17%, Westlaw AI-Assisted Research ~33% ([Stanford HAI, 2024](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries); [RegLab PDF, 2024](https://law.stanford.edu/wp-content/uploads/2024/05/Legal_RAG_Hallucinations.pdf)). The vendors had claimed "**100% hallucination-free linked legal citations**" (LexisNexis) and "avoid hallucinations by relying on trusted content" (Thomson Reuters); RegLab's conclusion was that **"providers' claims are overstated."**

The load-bearing lesson for this project: **RAG + citations measurably reduces but does not eliminate hallucination, and vendor "hallucination-free" claims are empirically false.** A banking-regulation tool must publish a *measured* rate, not a marketing claim.

### How regulated products actually manage the liability

The convergent controls across 2025–2026 financial-services guidance:
- **Mandatory abstention / escalation, not parametric fallback.** "When no relevant source content exists, does the agent escalate to a human or clearly state it cannot answer? The wrong behavior is attempting to generate a plausible response from parametric knowledge" ([fin.ai, "AI Agent Compliance for Financial Services," 2026](https://fin.ai/learn/evaluate-ai-agent-compliance-financial-services)).
- **Human-in-the-loop as the liability backstop.** "There must always be a human in the loop, a responsible owner who validates and approves model behavior" ([Moody's, "Agentic AI in financial services," 2025](https://www.moodys.com/web/en/us/creditview/blog/agentic-ai-in-financial-services.html)).
- **Traceability / reproducibility for audit.** "AI-driven decisions must be traceable and testable. Institutions need to document inputs, outputs and human overrides so they can reproduce results for auditors and regulators" ([fin.ai, 2026](https://fin.ai/learn/evaluate-ai-agent-compliance-financial-services)). Citations are not just trust UX — they are the **audit trail**.
- **Citation-mandatory + freshness/validity check.** Harvey's Shepardization is the template: a citation to a *real* source is insufficient if the source is *superseded* — directly analogous to a banking tool citing a repealed regulation or a pre-amendment APRA standard.

The regulated pattern, stated as a contract: **answer only from cited sources; abstain/escalate when uncited; log everything for audit; verify the cited source is still current.**

---

## 6. Where the field converges — the de-facto default stack

Independent of vendor, vertical, and expert, the 2026 anti-hallucination default for high-stakes retrieval is a **four-layer contract**:

1. **Grounding** — answer strictly from retrieved context; permission-scoped retrieval (Anthropic Citations, Glean, kapa). Disable or heavily penalize parametric fallback.
2. **Claim-level citation** — every claim carries an inline, verifiable reference to a source span (Anthropic sentence-level, Harvey claim-level, Perplexity inline). Citations double as the **audit trail**.
3. **Calibrated abstention** — say "I don't know" / escalate when grounding is absent; reward this behavior in the eval (kapa, OpenAI/Kalai, financial-services HITL).
4. **Continuous measurement** — claim-level **faithfulness/groundedness** scored offline on a gold set (regression gate) and online on live traffic via a cheap distilled detector (HHEM / Luna-2 / Lynx), plus citation-coverage and calibrated-abstention dashboards (Vectara, Galileo, Patronus, RAGAS, Hamel, Yan).

The disagreement among experts is about *emphasis* (retrieval recall vs. detector accuracy vs. eval discipline), **not about the shape of the contract.**

---

## 7. The loudest contrarian views (surfaced)

### Contrarian #1 (strongest): "Hallucination is inherent — it cannot be eliminated, only bounded."

This is now the *mainstream-among-researchers* position, and it is the most important caveat to the convergent stack.
- **OpenAI/Kalai et al. (2025-09-04):** hallucinations "arise through **natural statistical pressures**" in pretraining and are reinforced by evaluation incentives. The framing is that hallucination is a structural property, mitigable via incentive redesign and abstention — **not eliminable** ([arXiv 2509.04664](https://arxiv.org/abs/2509.04664)).
- **Vectara leaderboard (2026):** even the best models hallucinate ~1.8–3.3% on *grounded summarization* — the easiest possible grounding task ([Vectara, 2026](https://github.com/vectara/hallucination-leaderboard)).
- **RAGTruth span-detection F1 ~52.7%** — fine-grained detection is itself unreliable ([RAGTruth, 2024](https://aclanthology.org/2024.acl-long.585/)).

Implication: the deliverable cannot promise zero hallucination. It must promise a **measured, bounded, audited rate with mandatory abstention** — and the marketing-claim trap (LexisNexis's "100% hallucination-free", debunked by Stanford) is the failure to avoid.

### Contrarian #2: "Citations create false confidence."

Citations make wrong answers *look* more trustworthy, and citations themselves can be fabricated or mis-supporting.
- The **Stanford RegLab** finding that "hallucination-free linked legal citations" claims were overstated is the direct empirical rebuttal to citation-as-guarantee ([Stanford, 2024](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries)).
- **Fabricated-citation epidemic:** a study documented **100 hallucinated citations** that passed NeurIPS 2025 peer review (3–5 expert reviewers each); fabricated-reference rates in papers rose from 1 in 2,828 (2023) to 1 in 458 (2025) to 1 in 277 (early 2026) ([arXiv 2602.05930, 2026](https://arxiv.org/html/2602.05930v1)). The lesson: a citation that *exists* is not a citation that *supports the claim* — you must verify the link, not just its presence (Harvey's claim-to-source binding, not citation-count).

Mitigation that survives this critique: **citation must be mechanically bound to provided context** (Anthropic-style: the model can only cite documents it was given) **and verified at claim level** (does the cited span actually support the claim?), plus a **freshness check** (is the source still current?).

### Contrarian #3 (weakest): "Just use a bigger / better model."

The Vectara leaderboard trend shows newer/larger models *do* hallucinate less on summarization, so model choice matters — but the same data shows the rate **plateaus at a few percent and never reaches zero**, and Stanford's regulated-domain study used vendor RAG systems on top of frontier models and still found 17–33%. Bigger models reduce the base rate; they do not remove the need for grounding, abstention, and measurement. This is the contrarian view the evidence least supports.

---

## Verdict

**The convergent, expert-recommended anti-hallucination default for a high-stakes topical retrieval tool in mid-2026 is a four-layer grounding contract, measured at claim level:**

> **Answer strictly from permission-scoped retrieved context; attach a verifiable inline citation to every claim (mechanically bound to provided sources, not parametric memory); abstain or escalate to a human when grounding is absent; and continuously measure claim-level faithfulness, citation coverage, and calibrated abstention — offline on a gold set as a release gate, online on live traffic via a cheap distilled detector.**

**How to measure it (concrete):**
- **Offline gold set:** ~1k in-domain examples (synthetically bootstrapped per Liu, ~5 questions/chunk), *including deliberately unanswerable questions whose gold answer is "abstain"* (per OpenAI/Kalai). Score **RAGAS-style faithfulness = 1 − unsupported_claims/total_claims**, plus retrieval recall and a calibrated-abstention metric. Validate the judge against a human-labeled subset (2025 judge-bias research). Gate releases on regression.
- **Online:** score every response with a distilled groundedness detector (**Vectara HHEM-2.x**, **Galileo Luna-2**, or **Patronus Lynx**); dashboard groundedness, citation coverage, citation-verification rate, and refuse-when-should vs. refuse-when-answerable. Have a domain expert read traces each cycle (Hamel).
- **Regulated add-on:** verify every cited source is *current* (Harvey-style Shepardization analog — e.g., the cited APRA/ASIC instrument is not superseded), and log inputs/outputs/overrides for audit (financial-services HITL guidance).

**Strongest dissent to keep visible:** hallucination is **inherent and not eliminable** (OpenAI/Kalai 2025; Vectara leaderboard shows ~2–3% even on the easiest grounded task), and **citations can create false confidence** (Stanford RegLab debunked "100% hallucination-free"; fabricated-citation rates are rising). Therefore the tool must publish a **measured, bounded rate with mandatory abstention** — never a "hallucination-free" claim, which the evidence shows is both false and a liability.

---

## Sources

- [Anthropic — Introducing Citations on the Anthropic API](https://claude.com/blog/introducing-citations-api) — Anthropic, 2025 (GA early 2025; Endex 10%→0%, +20% references, +15% recall; Thomson Reuters/CoCounsel quote).
- [Citations API and PDF support for Claude in Amazon Bedrock](https://aws.amazon.com/about-aws/whats-new/2025/06/citations-api-pdf-claude-models-amazon-bedrock/) — AWS, 2025-06.
- [Anthropic's new Citations API](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/) — Simon Willison, 2025-01-24.
- [BigLaw Bench: Hallucinations](https://www.harvey.ai/blog/biglaw-bench-hallucinations) — Harvey, 2024-10-07 (hallucination definition; claim-decomposition method; 0.2% rate; Shepardization).
- [What Are AI Hallucinations? Causes, Examples & How to Prevent Them](https://www.kapa.ai/blog/ai-hallucination) — kapa.ai, 2025 ("I don't know" abstention; docs-only grounding).
- [kapa.ai — Answering Engine](https://www.kapa.ai/product/answering-engine) — kapa.ai, 2025.
- [Does Perplexity Hallucinate Less Than ChatGPT?](https://www.datastudios.org/post/does-perplexity-hallucinate-less-than-chatgpt-when-searching-the-web-reliability-and-fact-checking) — DataStudios, 2025 (inline citation; ~10% fewer; "not absolute").
- [Glean — Grounding (AI glossary)](https://www.glean.com/ai-glossary/grounding) — Glean, 2025 (citations on every answer; permission-aware).
- [Glean — System of Context](https://www.glean.com/product/system-of-context) — Glean, 2025.
- [Why Language Models Hallucinate](https://arxiv.org/abs/2509.04664) — Kalai, Nachum, Vempala, Zhang (OpenAI), arXiv 2509.04664, 2025-09-04 (statistical pressure; rework evals to reward uncertainty/abstention).
- [Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/) — OpenAI, 2025.
- [Hallucination evaluation (HHEM)](https://docs.vectara.com/docs/hallucination-and-evaluation/hallucination-evaluation) — Vectara Docs, 2025.
- [vectara/hallucination_evaluation_model](https://huggingface.co/vectara/hallucination_evaluation_model) — Vectara on Hugging Face (HHEM; #1 detection model, 100k+ downloads).
- [Vectara Hallucination Leaderboard](https://github.com/vectara/hallucination-leaderboard) — Vectara, leaderboard read 2026 (HHEM-2.3 methodology; best models ~1.8–3.3%).
- [Vectara launches Hallucination Corrector](https://siliconangle.com/2025/05/13/vectara-launches-hallucination-corrector-increase-reliability-enterprise-ai/) — SiliconANGLE, 2025-05-13 (Amr Awadallah quote on regulated industries).
- [Patronus AI Launches Lynx (blog)](https://www.patronus.ai/blog/lynx-state-of-the-art-open-source-hallucination-detection-model) — Patronus AI, 2024 (Lynx; HaluBench incl. Finance/Medicine; 8 hallucination types).
- [Patronus AI Launches Lynx (press release)](https://www.prnewswire.com/news-releases/patronus-ai-launches-lynx-state-of-the-art-open-source-hallucination-detection-model-302194659.html) — PR Newswire, 2024.
- [Context Adherence](https://docs.galileo.ai/galileo/gen-ai-studio-products/galileo-guardrail-metrics/context-adherence) — Galileo Docs, 2025 (ChainPoll; closed-domain hallucination).
- [Luna: An Evaluation Foundation Model to Catch Hallucinations with High Accuracy and Low Cost](https://arxiv.org/html/2406.00975v2) — Galileo, arXiv 2406.00975 (Luna/Luna-2 distilled detectors).
- [Systematically Improving RAG Applications](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/) — Jason Liu, 2025-01-24 (synthetic evals; recall as load-bearing metric).
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — Hamel Husain, 2024-03-29 (evals as root cause; look at data; error analysis).
- [A Field Guide to Rapidly Improving AI Products](https://www.oreilly.com/radar/a-field-guide-to-rapidly-improving-ai-products/) — Hamel Husain, O'Reilly, 2025-04.
- [Task-Specific LLM Evals that Do & Don't Work](https://eugeneyan.com/writing/evals/) — Eugene Yan, 2024–2025 (factual-consistency guardrail; ~1k samples; ROC-AUC 0.56→0.85).
- [Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) — RAGAS Docs, 2025 (claim-decomposition faithfulness formula).
- [RAG Evaluation: A Complete Guide for 2025](https://www.getmaxim.ai/articles/rag-evaluation-a-complete-guide-for-2025/) — Maxim AI, 2025 (LLM-as-judge correlation; judge bias).
- [Evaluating RAG Systems in 2025: RAGAS Deep Dive](https://cohorte.co/blog/evaluating-rag-systems-in-2025-ragas-deep-dive-giskard-showdown-and-the-future-of-context) — Cohorte, 2025.
- [RAGTruth: A Hallucination Corpus for Trustworthy RAG](https://aclanthology.org/2024.acl-long.585/) — Niu et al., ACL 2024 (18k responses; word/span-level annotations; ~52.7% span F1).
- [Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards (FaithBench/FaithJudge)](https://arxiv.org/html/2505.04847v2) — arXiv 2505.04847, 2025.
- [AI on Trial: Legal Models Hallucinate in 1 out of 6 (or More) Queries](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries) — Stanford HAI / RegLab, 2024 (17%–33%; "providers' claims overstated").
- [Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools (PDF)](https://law.stanford.edu/wp-content/uploads/2024/05/Legal_RAG_Hallucinations.pdf) — Magesh, Surani, Dahl, Suzgun, Manning, Ho (Stanford RegLab), 2024 preprint; J. Empirical Legal Studies 2025.
- [AI Agent Compliance for Financial Services](https://fin.ai/learn/evaluate-ai-agent-compliance-financial-services) — fin.ai, 2026 (escalate/refuse vs. parametric fallback; traceability for audit).
- [Agentic AI in financial services](https://www.moodys.com/web/en/us/creditview/blog/agentic-ai-in-financial-services.html) — Moody's, 2025 (human-in-the-loop as backstop).
- [Compound Deception in Elite Peer Review: 100 Fabricated Citations at NeurIPS 2025](https://arxiv.org/html/2602.05930v1) — arXiv 2602.05930, 2026 (citations can be fabricated and pass expert review; rising rates).
