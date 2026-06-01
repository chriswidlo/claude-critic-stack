# Second-Stage Retrieval: Reranking, Late Interaction, and Query Transformation

_Researched 2026-06-01 - axis: reranking & advanced retrieval_

This is one axis of a multi-axis investigation into the SOTA architecture for a topical knowledge retrieval tool (accurate retrieval over local docs, websites, and databases, consumed by an AI agent; first instance: AU banking regulation). This document owns the **second stage** of the pipeline: what happens *after* a first-stage retriever has produced candidates. It covers reranking, late-interaction / multi-vector retrieval, query transformation, and the proven ordering of the full pipeline. First-stage embeddings, chunking, and ingestion are out of scope here and belong to sibling axes.

## Table of Contents

1. [Executive framing](#executive-framing)
2. [Rerankers: the SOTA landscape mid-2026](#rerankers-the-sota-landscape-mid-2026)
3. [Reranking: measured impact, latency, and the contrarian case](#reranking-measured-impact-latency-and-the-contrarian-case)
4. [Late interaction / multi-vector retrieval](#late-interaction--multi-vector-retrieval)
5. [ColPali and visual document retrieval](#colpali-and-visual-document-retrieval)
6. [Query transformation: what helps, what is theatre](#query-transformation-what-helps-what-is-theatre)
7. [Query routing and adaptive retrieval](#query-routing-and-adaptive-retrieval)
8. [The proven pipeline ordering](#the-proven-pipeline-ordering)
9. [Verdict](#verdict)
10. [Sources](#sources)

---

## Executive framing

By mid-2026 the field has converged on a strong consensus default for the second stage: **a two-stage pipeline** where stage 1 is hybrid retrieval (dense + sparse / BM25) fused with Reciprocal Rank Fusion (RRF), and stage 2 is a **cross-encoder reranker** that compresses a broad, noisy candidate pool (top ~50-100) down to a small, precise set (top ~5-10) for the agent's context. This ordering is documented as the recommended default across vendor guides, practitioner posts, and academic benchmarks for 2025-2026 ([digitalapplied, 2026](https://www.digitalapplied.com/blog/hybrid-search-bm25-vector-reranking-reference-2026); [arXiv 2604.01733](https://arxiv.org/pdf/2604.01733)).

The more advanced techniques on this axis — late interaction (ColBERT family), ColPali for visual documents, and query transformations (HyDE, multi-query, RAG-fusion, decomposition, routing) — are *situational upgrades*, not universal defaults. Each carries a real cost (index size, latency, operational complexity) that is only repaid under specific conditions. The body of this document is largely about identifying those conditions.

---

## Rerankers: the SOTA landscape mid-2026

A reranker is a **cross-encoder**: it takes the query and a candidate document *together* and scores their relevance jointly, rather than embedding them independently and comparing vectors. This joint attention is what makes rerankers far more precise than a first-stage bi-encoder — and also why they cannot be used for first-stage retrieval over millions of documents (you would have to run the model once per candidate).

### The leaderboard (Agentset, snapshot 2026-02-15)

The Agentset reranker leaderboard ([agentset.ai/rerankers](https://agentset.ai/rerankers), snapshot 2026-02-15) ranks models by ELO from head-to-head matchups, with measured latency and price. Top entries:

| Rank | Model | ELO | Latency (ms) | Price/1M | License |
|------|-------|-----|--------------|----------|---------|
| 1 | Zerank 2 | 1638 | 265 | $0.025 | cc-by-nc-4.0 |
| 2 | Cohere Rerank 4 Pro | 1629 | 614 | $0.050 | Proprietary |
| 3 | Zerank 1 | 1573 | 266 | $0.025 | cc-by-nc-4.0 |
| 4 | Voyage Rerank 2.5 | 1544 | 613 | $0.050 | Proprietary |
| 5 | Zerank 1 Small | 1539 | 248 | $0.025 | Apache 2.0 |
| 6 | Voyage Rerank 2.5 Lite | 1520 | 616 | $0.020 | Proprietary |
| 7 | Cohere Rerank 4 Fast | 1510 | 447 | $0.050 | Proprietary |
| 8 | Qwen3 Reranker 8B | 1473 | 4687 | $0.050 | Apache 2.0 |
| 9 | Contextual AI Rerank v2 | 1469 | 3333 | $0.050 | cc-by-nc-4.0 |
| 10 | Cohere Rerank 3.5 | 1451 | 392 | $0.050 | Proprietary |

Two things jump out. First, the **proprietary API leaders (Cohere Rerank 4 Pro, Voyage Rerank 2.5) and the open/cheap challenger Zerank 2 cluster within ~100 ELO** — a meaningful but not enormous quality gap. Second, **latency varies by an order of magnitude or more**: the API leaders sit at ~600ms, the Zerank family at ~250ms, while large LLM-style rerankers (Qwen3-Reranker-8B at 4.7s, Contextual AI Rerank v2 at 3.3s) are far too slow for interactive use without heavy optimization.

> **Caveat on the leaderboard as comparator.** Agentset is itself a RAG vendor; its leaderboard is a useful but vendor-published artifact, and its top pick (Zerank 2) is its own ecosystem's preferred model. The nDCG@10 column in the snapshot is also implausibly small in absolute terms (likely a delta or mis-scaled figure), so treat the *ordering* as informative and the absolute numbers as suspect. This is exactly the kind of "X is best because it beats Y" claim that should be cross-checked against an independently runnable benchmark on your own corpus before adoption.

### The named contenders

**Cohere Rerank** is the incumbent default and the most widely adopted reranker in production. **Rerank 4** was announced December 2025, with multilingual coverage across 100+ languages, Pro and Fast variants, and Cohere's first "self-learning" reranker capability ([Cohere, Dec 2025](https://cohere.com/blog/rerank-4)). It is available in Microsoft Foundry ([Microsoft, 2026](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-cohere-rerank-4-0-in-microsoft-foundry/4477076)). The prior **Rerank 3.5** remains widely deployed; it is the one most third-party benchmarks compare against.

**Voyage rerank-2.5 / rerank-2.5-lite** (released 2025-08-11) is the strongest documented challenger on quality-per-token. Voyage's own evaluation across 93 retrieval datasets, 9 domains, and 31 languages reports rerank-2.5 beating Cohere Rerank v3.5 by **7.94%** on standard evaluation and **12.70%** on the MAIR instruction-following benchmark; it offers a **32K token context (8x Cohere v3.5)** at no pricing change, and adds natural-language instruction-following to steer relevance ([Voyage AI, Aug 2025](https://blog.voyageai.com/2025/08/11/rerank-2-5/)). Notably Voyage claims rerank-2.5 exceeds Qwen3-Reranker-8B "despite being over an order of magnitude smaller." (These are *vendor-reported* gains against an older Cohere version; the head-to-head ELO leaderboard above, which post-dates Cohere Rerank 4, places Cohere 4 Pro slightly ahead of Voyage 2.5.) Voyage is now part of MongoDB, which matters for adopters already on Atlas.

**Zerank (ZeroEntropy)** is the 2026 open/cheap disruptor: roughly half the price of the API incumbents, ~250ms latency, top-of-leaderboard ELO, with a small Apache-2.0 variant. ZeroEntropy also publishes the most credible vendor-neutral-ish guide to open-source alternatives ([ZeroEntropy, 2026](https://zeroentropy.dev/articles/open-source-alternatives-to-cohere-rerank/)).

**Jina Reranker v2 / v3** — multilingual (100+ languages), function-calling and code-search support, ~6x speedup over v1 ([Jina, 2024](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual)). The open weights are **CC-BY-NC-4.0 (research only)**; commercial use requires Jina's API, AWS SageMaker, or Azure Marketplace. This licensing wrinkle is a real adoption constraint.

**BGE reranker v2-m3** — the de facto open-source / self-hostable default. Under 600M parameters, runs on consumer GPUs, **OSI-approved open license** ([analyticsvidhya, 2025](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/)). This is the model most data-sovereignty-constrained teams (including regulated finance) reach for when an external API is unacceptable. AU banking regulation data may well fall in this category.

**LLM-as-reranker** (e.g. Qwen3-Reranker-8B, or prompting a general LLM) gives top-tier quality and free-text instruction-following but at 3-5s latency per batch before optimization ([fin.ai, 2026](https://fin.ai/research/using-llms-as-a-reranker-for-rag-a-practical-guide/)). With thresholding, prompt caching, and parallelized calls, fin.ai drove added latency below 1s and cost down ~8x — but this is bespoke engineering, not a drop-in.

**Who uses what.** Cohere Rerank is the broad enterprise default and is embedded in Microsoft Foundry. Voyage is the choice for MongoDB Atlas shops and long-context / instruction-steered reranking. BGE-v2-m3 dominates self-hosted, privacy-constrained deployments. Jina is common in multilingual and code-search contexts (subject to its license).

---

## Reranking: measured impact, latency, and the contrarian case

### Measured impact

Adding a reranker to a two-stage pipeline reliably improves answer quality, and the two-stage (hybrid retrieval + neural reranker) design "outperforms all single-stage methods by a large margin" in the text-and-table benchmark ([arXiv 2604.01733](https://arxiv.org/pdf/2604.01733)). The mechanism is precision: the reranker takes a large noisy candidate set and compresses it to a small precise set, which is exactly what an LLM context window wants.

On most English RAG corpora the three dominant API rerankers land within **1-3 nDCG@10 points of each other**, so the practical choice hinges on latency, cost, language coverage, and deployment model rather than raw quality ([ZeroEntropy guide, 2026](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/)).

### Latency — and the counterintuitive result

The naive worry is that a reranker only adds latency. The more careful 2025-2026 finding is the opposite at the system level: **because LLM generation dominates end-to-end RAG latency, cutting context from ~50 chunks to ~5 chunks reduces generation time by 75-90%, so a reranker can make the whole pipeline faster while also improving quality and cost** ([BSWEN, 2026](https://docs.bswen.com/blog/2026-02-25-reranker-latency-impact/)). Decagon reports similar system-level wins from reranker optimization for low-latency agents ([Decagon, 2026](https://decagon.ai/blog/designing-low-latency-ai-agents-through-reranker-optimization)).

The honest counterweights:
- **API rerankers add ~100-400ms p50 and can spike under load**; at millions of queries/day the per-call cost compounds ([BSWEN, 2026](https://docs.bswen.com/blog/2026-02-25-reranker-latency-impact/)).
- **Self-hosted cross-encoders add ~100ms on GPU** — usually worth it, but it is real infra.

### The contrarian view: when reranking is *not* worth it

The sharpest contrarian point: **reranking only pays off when the candidate set is large and noisy.** If your first-stage retriever already returns a small, high-quality set (e.g. N=10 candidates, K=5 kept), reranking "adds latency but provides limited benefit, as the power of reranking comes from having a large, noisy candidate set and dramatically compressing it" ([BSWEN, 2026](https://docs.bswen.com/blog/2026-02-25-reranker-latency-impact/)). The corollary for the AU-banking instance: if the corpus is small and the first-stage retriever is already strong, a reranker may be net-negative latency for marginal quality. **Measure on your own query set before committing.**

---

## Late interaction / multi-vector retrieval

Late interaction (the ColBERT family) sits between single-vector retrieval and cross-encoder reranking. Instead of one vector per document, it stores **one vector per token** and scores via the MaxSim operator (each query token finds its best-matching document token, then sums). This captures fine-grained term-level matching that single-vector embeddings blur away, while still being precomputable (unlike a cross-encoder) so it can serve first-stage retrieval *or* reranking.

### The cost: index size

This is the central tradeoff. Late-interaction systems impose "an order-of-magnitude larger space footprint than single-vector models" because they store billions of small vectors ([arXiv 2112.01488, ColBERTv2](https://arxiv.org/pdf/2112.01488)). The illustrative figure circulated in 2025: ~10M documents of ~200 tokens needs roughly **6TB of index for naive ColBERT vs ~30GB for a bi-encoder**. ColBERTv2's residual compression cuts the per-token footprint ~6-10x (quantizing each vector from 256 bytes down to ~36 bytes at 2-bit, or ~20 bytes at 1-bit), bringing the index "to a level comparable to sparse + dense hybrid indexes" ([ColBERTv2 paper](https://arxiv.org/pdf/2112.01488); [Weaviate, 2025](https://weaviate.io/blog/late-interaction-overview)). Engines like **Vespa** and **WARP** ([arXiv 2501.17788](https://arxiv.org/pdf/2501.17788)) exist specifically to serve multi-vector retrieval efficiently in production.

### Production-feasible models mid-2026

- **ColBERTv2** — the reference architecture; residual compression made it production-viable.
- **answerai-colbert-small-v1** (Answer.AI, Aug 2024) — a 33M-parameter proof-of-concept that *vastly outperforms the original 110M ColBERTv2 on all benchmarks*, including unseen LoTTE, and beats e5-large-v2 and bge-base-en-v1.5 despite its size ([Answer.AI, 2024](https://www.answer.ai/posts/2024-08-13-small-but-mighty-colbert.html)). Available via PyLate, RAGatouille, Stanford ColBERT, and the `rerankers` library. This is the model that makes "ColBERT as a cheap, high-quality second-stage reranker over a small candidate set" practical.
- **Jina-ColBERT-v2** — general-purpose multilingual late interaction ([arXiv 2408.16672](https://arxiv.org/pdf/2408.16672)).
- **mxbai-edge-colbert-v0** (Oct 2025) — the frontier of small late-interaction: a 17M-parameter variant reportedly outperforms the current <1B single-vector SOTA by almost 20 nDCG@10 points ([arXiv 2510.14880](https://arxiv.org/html/2510.14880v1)).

### When late interaction beats single-vector + rerank

The 2025-2026 consensus: **use late interaction as a precise *second-stage reranker over a candidate set*, not as a first-stage retriever over the whole corpus** ([Zilliz, 2025](https://zilliz.com/learn/explore-colbert-token-level-embedding-and-ranking-model-for-similarity-search)). It shines where term-level matching matters — long technical documents, jargon-dense or entity-heavy text (regulation, legal, code) — and where the index-size cost is acceptable. A small ColBERT (answerai-colbert-small, mxbai-edge) over a top-100 candidate set can rival a cross-encoder at lower latency and self-hostable.

### The contrarian view: ColBERT is too heavy for most

"ColBERT's advantage comes at the cost of increased resource consumption … both in terms of speed and memory," and its speed/footprint "might make it less suitable for large-scale retrieval"; if a fast first retriever already gives a high-quality candidate set of <10 docs, ColBERT's added complexity "might offer diminishing returns compared to a full cross-encoder" ([Zilliz, 2025](https://zilliz.com/learn/explore-colbert-token-level-embedding-and-ranking-model-for-similarity-search)). In other words: for many teams, **single-vector hybrid + a cross-encoder reranker is simpler and good enough**, and the multi-vector index is operational overhead they will regret. The counter-counterpoint is the rise of tiny ColBERTs (17-33M params) that erode the speed/footprint objection — but those are still newer and less battle-tested than Cohere/Voyage rerank APIs.

---

## ColPali and visual document retrieval

ColPali extends late interaction to **document images**: a Vision-Language Model produces multi-vector embeddings directly from the rendered page, skipping OCR/layout parsing entirely ([arXiv 2407.01449](https://arxiv.org/abs/2407.01449), ICLR 2025). On the **ViDoRe** benchmark (Vision Document Retrieval) ColPali outperforms all evaluated systems and is the overall best document-retrieval model. **ColQwen2-VL** (a 2B VLM trained with the ColPali recipe) improves a further +5.3 nDCG@5 over ColPali. **Light-ColPali/ColQwen2** clusters patch vectors to cut the (large) memory footprint.

**Proven adopters.** Map-RAS embeds 100K+ Library of Congress maps with ColQwen2 (text/image queries, <<1s search over 25K images); a biomedical MM-RAG system does direct PDF-image retrieval in glycobiology backed by Qdrant GPU HNSW indices ([Weaviate, 2025](https://weaviate.io/blog/late-interaction-overview)).

**Relevance to AU banking regulation.** Regulatory PDFs are visually complex (tables, forms, multi-column layouts, figures) and OCR pipelines lose structure. ColPali is the strongest answer *if* the source documents are image/PDF-heavy and layout-bearing. **Contrarian / cost note:** ColPali inherits ColBERT's multi-vector index-size problem *and* adds VLM inference cost at index time; if your regulatory text is available as clean machine-readable text (HTML, well-structured PDF text layer), a text pipeline is far cheaper and you should not reach for ColPali. This is a "visual docs only" specialization, not a default.

---

## Query transformation: what helps, what is theatre

Query transformation rewrites or expands the user query *before* retrieval to close the query-document vocabulary gap. The 2025-2026 evidence is mixed and strongly *conditional* — this is the area with the most cargo-cult adoption.

### HyDE (Hypothetical Document Embeddings)

Generate a fake answer with an LLM, embed *that*, and retrieve against it. Reported gains of **25-50% nDCG@10 on hypothetical / ambiguous / conceptually deep queries** ([emergentmind, 2025](https://www.emergentmind.com/topics/hypothetical-document-embeddings-hyde)); used in TREC 2025 RAG submissions to enhance sparse retrieval ([UTokyo TREC 2025](https://trec.nist.gov/pubs/trec34/papers/UTokyo.rag.pdf)).

**Contrarian / cost:** HyDE adds **25-60% latency** (an LLM call on every query) and is "prone to hallucination" with **query drift** on "well-specified, fact-bound domains," where it "should be replaced by direct retrieval-based RAG" ([apxml, 2025](https://apxml.com/courses/optimizing-rag-for-production/chapter-2-advanced-retrieval-optimization/query-augmentation-rag); [emergentmind, 2025](https://www.emergentmind.com/topics/hypothetical-document-embeddings-hyde)). **For precise numerical/fact-bound queries — which describes a lot of banking-regulation lookup — HyDE provides limited benefit and risks drift.** The recommended mitigation is to invoke HyDE *only* when first-stage query-document confidence is low, and to post-validate with a cross-encoder.

### Multi-query and RAG-Fusion

Multi-query generates several paraphrases and unions their results; **RAG-Fusion** adds RRF merging on top. RRF-based hybrid/fusion typically shows **15-30% better retrieval accuracy than pure vector search** ([dmflow, 2025](https://www.dmflow.chat/en/blog/rag-query-transformation-guide-6-advanced-architectures)). A 2025 markov-decision-process multi-query variant (MQRF-RAG) beat HyDE by ~7% on HotPotQA multi-hop and edged RAG-Fusion by 2.55% ([ACM, 2025](https://dl.acm.org/doi/10.1145/3728199.3728221)). Cost: each extra query is an extra retrieval round trip plus the LLM generation of the variants.

### Query decomposition

Break a complex/multi-hop question into sub-questions, retrieve for each, then synthesize. Clear wins on multi-hop QA (HotPotQA-style); unnecessary overhead on simple lookups.

### What measurably helps vs. adds latency for no gain

- **Helps:** RRF fusion (cheap, reliable 15-30% gain — and it is barely "transformation," it is just hybrid retrieval done right); decomposition on genuinely multi-hop questions; HyDE on ambiguous/conceptual queries.
- **No gain / harmful:** HyDE and broad query expansion on precise, fact-bound, numerical queries (drift + latency for nothing — "contextual retrieval yields consistent gains" where expansion does not, per [arXiv 2604.01733](https://arxiv.org/pdf/2604.01733)); multi-query when the user query is already specific (you pay N× retrieval for redundant results).

The honest summary: **the only query transformation that is a near-universal win is RRF fusion of hybrid retrievers. Everything else should be gated by a query classifier, not applied to every query.**

---

## Query routing and adaptive retrieval

The unifying 2025-2026 idea is **don't apply the expensive techniques uniformly — route per query.** A small classifier (e.g. a T5-large in Adaptive-RAG) predicts query difficulty — no retrieval / single-step / multi-step — at **~5-15ms/query, far cheaper than the 3-8s it saves on the easy path** ([letsdatascience, 2026](https://letsdatascience.com/blog/agentic-rag-self-correcting-retrieval)). SELF-RAG uses reflection tokens to decide whether to retrieve at all.

A typical product corpus is **60-80% simple lookups, 20-40% reasoning queries; adaptive routing cuts average cost 30-50%** ([letsdatascience, 2026](https://letsdatascience.com/blog/agentic-rag-self-correcting-retrieval)). The critical UX caveat: with a sub-3s budget you cannot run a full agent loop on every query — route easy queries to single-pass and only hard ones to the agent. RAGRouter-Bench and tier-based routing frameworks for financial/legal/medical documents formalize this ([arXiv 2604.03455](https://arxiv.org/pdf/2604.03455); [arXiv 2604.14222](https://arxiv.org/html/2604.14222v1)).

**Relevance to the agent-consumed, domain-agnostic tool:** since the consumer is an AI agent, the agent itself can play the router (decide when to call the retrieval tool, with what transformed query, and whether to escalate to multi-hop). This argues for exposing retrieval as a capable but *simple-default* tool, with the expensive transformations available but not forced.

**Contrarian:** routing adds a failure mode — a mis-routed hard query that gets the cheap path returns a confidently wrong answer. The classifier must be tuned on your distribution, and the safe default for a regulated domain is to bias toward over-retrieval.

---

## The proven pipeline ordering

The documented default ordering for 2025-2026 production RAG ([digitalapplied, 2026](https://www.digitalapplied.com/blog/hybrid-search-bm25-vector-reranking-reference-2026); [glaforge, 2026](https://glaforge.dev/posts/2026/02/10/advanced-rag-understanding-reciprocal-rank-fusion-in-hybrid-search/); [arXiv 2604.01733](https://arxiv.org/pdf/2604.01733)):

```
(0. optional) Query routing/classification  -> decide retrieval depth & whether to transform
(1. optional) Query transformation           -> HyDE / multi-query / decomposition, GATED by router
 2. Stage-1 retrieval (parallel)             -> dense (vector) + sparse (BM25)
 3. Fusion                                    -> Reciprocal Rank Fusion (RRF, k=60) -> top ~50-100
 4. Stage-2 rerank                            -> cross-encoder (or small ColBERT) -> top ~5-10
 5. Context assembly                          -> hand top-K to the LLM/agent
```

Key proven parameters and notes:
- **RRF with k=60** is the near-universal fusion default; it is rank-only, sidestepping the score-incompatibility problem of naive weighted fusion, and "rewards agreement across retrievers" ([glaforge, 2026](https://glaforge.dev/posts/2026/02/10/advanced-rag-understanding-reciprocal-rank-fusion-in-hybrid-search/)).
- **Retrieve broad (~50-100), rerank to narrow (~5-10).** The compression ratio is where reranking earns its keep; if N≈K, drop the reranker.
- **Anthropic Contextual Retrieval** (Sept 2024) is an *ingestion-time* complement that prepends LLM-generated context to each chunk before embedding; "Contextual hybrid outperforms vanilla hybrid RRF" ([analyticsvidhya, 2024](https://www.analyticsvidhya.com/blog/2024/12/contextual-rag-systems-with-hybrid-search-and-reranking/)). It lives upstream of this axis but pairs directly with the rerank stage.
- "The real work … is not in the fusion algorithm — RRF is three lines of code — but in embedding model evaluation against your corpus, chunking, metadata filtering, and the evaluation harness" ([digitalapplied, 2026](https://www.digitalapplied.com/blog/hybrid-search-bm25-vector-reranking-reference-2026)). The second stage is necessary but not where most teams' marginal effort should go first.

---

## Verdict

**The single SOTA second-stage recipe for mid-2026:**

> **Hybrid retrieve (dense + BM25) → RRF fusion (k=60) → cross-encoder reranker, retrieving broad (~top 50-100) and compressing to ~top 5-10.** Query transformation and multi-hop should be *gated by a lightweight query router*, not applied to every query — the only near-universal transformation is the RRF hybrid fusion itself.

**Reranker choice (the one knob that matters most), by deployment constraint:**
- **External API acceptable:** Cohere Rerank 4 (Pro for quality, Fast for ~450ms latency) or Voyage rerank-2.5 (best long-context / instruction-following; default if on MongoDB Atlas). These are the proven enterprise defaults and within 1-3 nDCG@10 of each other.
- **Self-hosted / data-sovereignty required (likely for AU banking regulation):** **BGE reranker v2-m3** (OSI license, runs on consumer GPUs) as the safe default, or a small late-interaction model (**answerai-colbert-small-v1**) where term-level matching on dense regulatory text justifies the multi-vector index.
- **Cost-sensitive at scale:** Zerank 2 (~half the price, ~250ms) — but validate its quality on your own corpus first, since the supporting leaderboard is vendor-published.

**Alternatives and their winning conditions:**
- **Late interaction (ColBERT family) as the reranker** instead of a cross-encoder — wins when documents are long, jargon/entity-dense, and the ~6-10x index-size cost is acceptable; the new tiny ColBERTs (answerai-colbert-small 33M, mxbai-edge-colbert 17M) make this newly practical and self-hostable.
- **ColPali / ColQwen2** — wins *only* if source documents are image/PDF-heavy and layout-bearing (visually complex regulatory PDFs that lose meaning under OCR). Skip it entirely if clean machine-readable text exists.
- **HyDE** — wins on ambiguous / conceptual queries; **actively harmful** (drift + 25-60% latency) on precise, fact-bound, numerical queries, which describes much of banking-regulation lookup. Gate it on low first-stage confidence; never apply it unconditionally.
- **Query decomposition** — wins on genuine multi-hop questions; pure overhead on simple lookups.
- **Adaptive query routing** — wins at scale (30-50% cost reduction when 60-80% of traffic is simple lookups); since the consumer here is an AI agent, the agent can serve as the router. Bias toward over-retrieval in a regulated domain to avoid confidently-wrong cheap-path answers.

**Strongest contrarian to the whole recipe:** reranking and late interaction only pay off when the first-stage candidate set is *large and noisy*. For a small, well-curated corpus with a strong first-stage retriever, a reranker can be net-negative latency for marginal quality gain. The entire second stage must be validated against the actual query distribution and corpus — the recipe above is the right *starting point*, not a substitute for measurement.

---

## Sources

- [Voyage AI — rerank-2.5 and rerank-2.5-lite: instruction-following rerankers](https://blog.voyageai.com/2025/08/11/rerank-2-5/) — 2025-08-11
- [Cohere — Introducing Rerank 4: Cohere's most powerful reranker yet](https://cohere.com/blog/rerank-4) — Dec 2025
- [Microsoft — Introducing Cohere Rerank 4.0 in Microsoft Foundry](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-cohere-rerank-4-0-in-microsoft-foundry/4477076) — 2026
- [Agentset — Best Rerankers for RAG (Leaderboard)](https://agentset.ai/rerankers) — snapshot 2026-02-15
- [ZeroEntropy — Ultimate Guide to Choosing the Best Reranking Model](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/) — 2026
- [ZeroEntropy — Open-source alternatives to Cohere Rerank in 2026](https://zeroentropy.dev/articles/open-source-alternatives-to-cohere-rerank/) — 2026
- [Jina — jina-reranker-v2-base-multilingual (Hugging Face)](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual) — 2024-06-25
- [Analytics Vidhya — Top 7 Rerankers for RAG](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/) — Jun 2025
- [fin.ai — Using LLMs as a Reranker for RAG: A Practical Guide](https://fin.ai/research/using-llms-as-a-reranker-for-rag-a-practical-guide/) — 2026
- [BSWEN — Does Adding a Reranker to RAG Increase Latency? The Counterintuitive Truth](https://docs.bswen.com/blog/2026-02-25-reranker-latency-impact/) — 2026-02-25
- [Decagon — Designing low-latency AI agents through reranker optimization](https://decagon.ai/blog/designing-low-latency-ai-agents-through-reranker-optimization) — 2026
- [arXiv 2112.01488 — ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://arxiv.org/pdf/2112.01488) — 2021/2022
- [Weaviate — An Overview of Late Interaction Retrieval Models: ColBERT, ColPali, and ColQwen](https://weaviate.io/blog/late-interaction-overview) — 2025
- [arXiv 2501.17788 — WARP: An Efficient Engine for Multi-Vector Retrieval](https://arxiv.org/pdf/2501.17788) — 2025
- [Answer.AI — Small but Mighty: Introducing answerai-colbert-small](https://www.answer.ai/posts/2024-08-13-small-but-mighty-colbert.html) — 2024-08-13
- [arXiv 2408.16672 — Jina-ColBERT-v2: A General-Purpose Multilingual Late Interaction Retriever](https://arxiv.org/pdf/2408.16672) — 2024
- [arXiv 2510.14880 — Fantastic (small) Retrievers and How to Train Them: mxbai-edge-colbert-v0](https://arxiv.org/html/2510.14880v1) — 2025-10
- [Zilliz — Explore ColBERT: Token-Level Embedding and Ranking Model](https://zilliz.com/learn/explore-colbert-token-level-embedding-and-ranking-model-for-similarity-search) — 2025
- [arXiv 2407.01449 — ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449) — 2024 (ICLR 2025)
- [GitHub illuin-tech/vidore-benchmark — Vision Document Retrieval (ViDoRe) Benchmark](https://github.com/illuin-tech/vidore-benchmark) — 2024/2025
- [EmergentMind — HyDE: Hypothetical Document Embeddings](https://www.emergentmind.com/topics/hypothetical-document-embeddings-hyde) — 2025
- [apxml — Query Augmentation: Expansion and Transformation](https://apxml.com/courses/optimizing-rag-for-production/chapter-2-advanced-retrieval-optimization/query-augmentation-rag) — 2025
- [dmflow — Six Advanced Query Transformation Architectures](https://www.dmflow.chat/en/blog/rag-query-transformation-guide-6-advanced-architectures) — 2025
- [ACM — Optimization of RAG multi-query rewrite generation via Markov decision process](https://dl.acm.org/doi/10.1145/3728199.3728221) — 2025
- [UTokyo-HitU at TREC 2025 RAG Track: HyDE-Enhanced Sparse Retrieval](https://trec.nist.gov/pubs/trec34/papers/UTokyo.rag.pdf) — 2025
- [arXiv 2604.01733 — From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents](https://arxiv.org/pdf/2604.01733) — 2026
- [digitalapplied — Hybrid Search: BM25, Vector & Reranking Reference 2026](https://www.digitalapplied.com/blog/hybrid-search-bm25-vector-reranking-reference-2026) — 2026
- [glaforge — Advanced RAG: Understanding Reciprocal Rank Fusion in Hybrid Search](https://glaforge.dev/posts/2026/02/10/advanced-rag-understanding-reciprocal-rank-fusion-in-hybrid-search/) — 2026-02-10
- [Analytics Vidhya — Building Contextual RAG Systems with Hybrid Search and Reranking](https://www.analyticsvidhya.com/blog/2024/12/contextual-rag-systems-with-hybrid-search-and-reranking/) — Dec 2024
- [letsdatascience — Agentic RAG Explained: Self-Correcting Retrieval](https://letsdatascience.com/blog/agentic-rag-self-correcting-retrieval) — 2026
- [arXiv 2604.03455 — Lightweight Query Routing for Adaptive RAG: RAGRouter-Bench](https://arxiv.org/pdf/2604.03455) — 2026
- [arXiv 2604.14222 — Adaptive Query Routing: A Tier-Based Framework for Hybrid Retrieval](https://arxiv.org/html/2604.14222v1) — 2026
