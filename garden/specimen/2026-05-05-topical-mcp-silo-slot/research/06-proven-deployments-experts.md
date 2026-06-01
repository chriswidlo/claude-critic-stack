# Proven Deployments & Expert Consensus — Topical Knowledge Retrieval (2025–2026)

_Researched 2026-06-01 - axis: proven deployments & expert consensus_

This document triangulates **what the field's named leaders actually do and recommend** for accurate topical document/website/database retrieval consumed by an AI agent. It names companies and people, quotes concrete recommendations with dates, and surfaces the strongest contrarian camps before stating a single convergent SOTA default.

---

## Table of Contents

1. [What named experts recommend](#1-what-named-experts-recommend)
2. [What leading products actually run](#2-what-leading-products-actually-run)
3. [Cloud/vendor reference architectures (the shipped defaults)](#3-cloudvendor-reference-architectures-the-shipped-defaults)
4. [The convergence point — de-facto SOTA default](#4-the-convergence-point--de-facto-sota-default)
5. [The contrarian camps (dissent, surfaced)](#5-the-contrarian-camps-dissent-surfaced)
6. [Verdict](#verdict)
7. [Sources](#sources)

---

## 1. What named experts recommend

The striking thing across 2025–2026 expert writing is how little daylight there is on the **shape** of the pipeline. The disagreements are about emphasis (eval discipline vs. embedding choice vs. reranking), not about the architecture.

### Jason Liu (RAG consultant; creator of `instructor`; "Systematically Improving RAG" / Maven)

Liu is the loudest voice on **measurement-first** retrieval. His January 2025 flagship post and 2025 RAG Master Series make concrete, quotable claims:

- **Recall is the load-bearing metric.** "Of all relevant snippets, how many did we return?" — retrieval failure cascades, because "models can handle irrelevant information, they cannot work with information that wasn't retrieved" ([jxnl.co, 2025-01-24](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/)). Focus on **passage-level recall**, not document-level.
- **Synthetic evals before real traffic.** "Generate 5 questions that can be answered by each chunk" to jumpstart a measurable eval set ([jxnl.co, 2025-01-24](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/)).
- **Two-stage retrieve-then-rerank.** "Do a quick vector search, then run re-ranking on the top K results" using cross-encoders for precision.
- **Hybrid + fine-tuned embeddings.** "You can see a 10–30% recall boost just by ensuring your embedding space aligns with how you define 'relevance.'" His widely quoted line: "If you're not fine-tuning your embeddings, you're more like a Blockbuster than a Netflix."
- **Query routing as tools.** Treat each index as a tool and classify the query to route it; monitor tool-selection precision/recall separately ([jxnl.co, 2025-01-24](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/)).
- **Keep structured data structured** — don't force tables/metadata through a text-embedding bottleneck.

### Kelly Hong, Anton Troynikov, Jeff Huber, Morgan McGuire (Chroma)

Chroma's **Generative Benchmarking** technical report (April 2025) attacks the practice of picking embedding models off public leaderboards: **"Stop Trusting MTEB Rankings."** The recommendation is to generate domain-representative query/chunk pairs from *your own* corpus and benchmark retrieval on that, because public benchmarks don't predict in-domain performance ([trychroma.com research, 2025-04](https://research.trychroma.com/generative-benchmarking); summarized by [jxnl.co, 2025-09-11](https://jxnl.co/writing/2025/09/11/stop-trusting-mteb-rankings-kelly-hong-chroma/)). This is the same "build a golden set for *your* data" discipline Liu preaches — convergent.

Chroma is also the source of the loudest **contrarian framing** (see §5).

### Jo Kristian Bergum (Vespa; the search-relevance authority)

Bergum is the most credible voice on the *ranking* side, and he is emphatically **pro-hybrid, pro-BM25**:

- **BM25 is a strong, generalizable baseline** that many dense single-vector models trained on MS MARCO *underperform* out-of-domain ([Vespa blog, "Improving Zero-Shot Ranking with Vespa Hybrid Search"](https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/)).
- A **hybrid neural + BM25** method outperformed alternatives on **12 of 13 BEIR datasets**.
- Architecturally he advocates **phased (multi-stage) ranking**: a cheap first-phase function over all matches, an expensive re-ranking expression only over the top-N. This is exactly the production pattern everyone else describes.

His out-of-domain warning is directly relevant to a *new domain like AU banking regulation*: do not assume a leaderboard-topping dense model beats BM25 on your specialized corpus without measuring.

### Anthropic — Contextual Retrieval (official guidance)

Anthropic's September 2024 **Contextual Retrieval** cookbook is arguably the single most-cited reference architecture of the period. Its concrete, measured recommendations:

- **Prepend LLM-generated chunk-specific context** to each chunk before embedding *and* before BM25 indexing.
- **Combine contextual embeddings + BM25 (hybrid).** Hybrid alone cut retrieval failures **~49%**; **adding reranking cut them ~67%** (top-20 failure rate 5.7% → 1.9%) ([analyticsvidhya summary, 2024-11](https://www.analyticsvidhya.com/blog/2024/11/anthropics-contextual-rag/); [AWS implementation, 2025](https://aws.amazon.com/blogs/machine-learning/contextual-retrieval-in-anthropic-using-amazon-bedrock-knowledge-bases/)).
- **Voyage and Gemini embeddings performed best** in their tests; **passing the top-20 chunks** to the model beat passing fewer.

This is the canonical "embeddings + BM25 + reranking" stack, with a domain-context augmentation step layered on.

### Cohere & Voyage AI (reranker/embedding vendors — official guidance)

The vendor-recommended production pattern, stated almost identically across docs: **Query → Dense + Sparse retrieval → RRF fusion → top 50–200 candidates → cross-encoder reranker → top 5–10 chunks → LLM** ([Cohere Rerank docs](https://docs.cohere.com/docs/rerank); [Cohere RAG example](https://docs.cohere.com/docs/rag-complete-example)). As of late 2025 the current models are **Cohere Rerank 4** (shipped Dec 2025) and **Voyage rerank-2.5 / rerank-2.5-lite**. Voyage also ships *domain-specialized* embeddings (e.g. `voyage-law-2`), the relevance of which to a vertical like AU banking is direct.

### kapa.ai (production RAG over technical docs, 100+ teams)

kapa.ai's "RAG Best Practices: Lessons from 100+ Technical Teams" is one of the best *deployed-at-scale* expert sources. Their numbers reinforce Anthropic's: **hybrid + contextual retrieval together drop error rates ~69%**; cross-encoders (BGE, Cohere Rerank, Voyage rerank-2.5) are standard; **"naive RAG fails in production"** ([kapa.ai blog](https://www.kapa.ai/blog/rag-best-practices); [kapa.ai 2026 pipeline guide](https://www.kapa.ai/blog/how-to-build-a-rag-pipeline-from-scratch-in-2026)).

---

## 2. What leading products actually run

### Perplexity — Vespa-powered hybrid + multi-stage ML ranking

The most documented production retrieval stack of the period. Perplexity runs on **Vespa**, indexing **200B+ URLs / 400PB hot storage**, combining:

- **Dense vector search** (semantic) + **BM25 lexical** (precision on rare terms/identifiers),
- **Three reranking layers (L1–L3)** with a **~0.7 quality threshold** and a fail-safe that *discards all results and re-queries* rather than serve weak citations,
- **Chunk-level retrieval** (ranks individual paragraphs, not whole docs), with citation-coupled generation
([ByteByteGo, "How Perplexity Built an AI Google"](https://blog.bytebytego.com/p/how-perplexity-built-an-ai-google); [ZipTie, "How Perplexity AI Answers Work"](https://ziptie.dev/blog/how-perplexity-ai-answers-work/)).

### Glean — classical IR + LLMs + personalization (hybrid)

Glean explicitly **combines traditional information retrieval with embeddings and LLMs**, emphasizing rigorous ranking, personalization, and hybrid classical-IR + vector search across 100+ connected apps ([ZenML LLMOps DB case study](https://www.zenml.io/llmops-database/building-robust-enterprise-search-with-llms-and-traditional-ir)). It is the "discovery" layer; Hebbia is the "do work over it" layer.

### Harvey (legal) — domain-specialized embeddings + multi-model orchestration

Harvey's underappreciated moat is a **custom legal embedding model, `voyage-law-2-harvey`, trained with Voyage AI on 20B+ tokens of legal text**, reporting a **25% reduction in irrelevant results** vs. off-the-shelf embeddings. Since May 2025 Harvey is **model-agnostic**, routing tasks across OpenAI, Anthropic Claude (via Azure), and Google models ([Contrary Research report](https://research.contrary.com/company/harvey); [Harvey blog, "Expanding Harvey's Model Offerings"](https://www.harvey.ai/blog/expanding-harveys-model-offerings)). The lesson for AU banking regulation: **domain-tuned embeddings are a real, deployed differentiator in regulated verticals.**

### Hebbia — "retrieval + reasoning" (Matrix)

Hebbia pairs "world-class retrieval with top-tier models" and an agentic orchestration layer (Matrix), positioning as a *system of record for reasoning over documents* — IR-plus-reasoning rather than single-shot RAG ([Sacra interview with Danny Wheller](https://sacra.com/research/danny-wheller-hebbia-vertical-vs-horizontal-enterprise-ai/); [Takafumi Endo on Hebbia](https://medium.com/@takafumi.endo/hebbias-edge-building-a-system-of-record-for-enterprise-reasoning-1264ab76ec6b)).

### Cursor / Claude Code / Devin — the agentic-grep camp (code, not docs)

For *code* retrieval, leading coding agents lean on **grep/AST/filesystem tools rather than vector RAG**, because code is a dependency graph that embeddings flatten. This is a real, deployed contrarian data point — but its proponents scope it to code (see §5).

---

## 3. Cloud/vendor reference architectures (the shipped defaults)

Every major cloud now ships the **same default**: hybrid (vector + BM25) + RRF fusion + cross-encoder rerank.

- **Anthropic / AWS Bedrock Knowledge Bases** — managed RAG with native connectors (S3, Confluence, SharePoint, Salesforce), **hybrid search (semantic + BM25)**, and Contextual Retrieval support; **multimodal retrieval GA Nov 2025** ([AWS Bedrock KB](https://aws.amazon.com/bedrock/knowledge-bases/); [multimodal GA announcement, 2025-11](https://aws.amazon.com/about-aws/whats-new/2025/11/multimodal-retrieval-bedrock-knowledge-bases/)).
- **Azure AI Search** — the Microsoft Ignite 2025 reference design is explicit: "start from classic keyword search, add vector search…, combine them using **hybrid retrieval with Reciprocal Rank Fusion**, and apply a **cross-encoder re-ranker**" ([itnext / Ignite 2025 writeup](https://itnext.io/next-level-rag-on-azure-building-knowledge-bases-with-azure-ai-search-and-foundry-6d88d60e7202)). Azure also shipped **Agentic Retrieval** ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)).
- **Google Vertex AI** — **RAG Engine** on **Vector Search 2.0** (early-2026 redesign: one Collection holds vectors + metadata + chunk text, one API call, scales to billions) ([Google Cloud RAG reference architecture](https://docs.cloud.google.com/architecture/gen-ai-rag-vertex-ai-vector-search); [GCP RAG spectrum](https://medium.com/google-cloud/the-gcp-rag-spectrum-vertex-ai-search-rag-engine-and-vector-search-which-one-should-you-use-f56d50720d5a)).
- **OpenAI** — File Search / Vector Stores: "automatically parses and chunks documents, creates and stores embeddings, and uses **both vector and keyword search**" via a single Responses-API call ([OpenAI File Search docs](https://developers.openai.com/api/docs/assistants/tools/file-search)).
- **Databricks** — Mosaic AI Vector Search (managed indexing/retrieval) + Mosaic AI Gateway (OpenAI-compatible unified model access) ([Databricks RAG docs](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation)).

**The vendors have standardized.** A 2026 platform comparison summarizes the managed tier bluntly: "AWS Bedrock Knowledge Bases, Azure AI Search, and GCP Vertex AI Search offer zero-ops RAG inside each cloud's ecosystem" ([Atlan comparison, 2026](https://atlan.com/know/enterprise-rag-platforms-comparison/)).

---

## 4. The convergence point — de-facto SOTA default

Independent of vendor, independent of expert, the **same pipeline** appears:

> **Hybrid first-stage retrieval (dense embeddings + BM25/lexical) → RRF fusion → retrieve broad (top 20–200 candidates) → cross-encoder reranker → top 5–10 chunks → LLM**, wrapped in an **eval/golden-dataset loop** built on your *own* domain data.

Convergent add-ons that the leaders agree raise accuracy:
1. **Contextual augmentation** of chunks before indexing (Anthropic; kapa.ai measured ~67–69% failure reduction with rerank/contextual combined).
2. **Domain-specialized embeddings** for verticals (Harvey/Voyage in legal — directly analogous to AU banking).
3. **Reranking is now baseline, not optional** (Cohere, Voyage, kapa.ai, Azure, Perplexity L1–L3, Bergum's phased ranking).
4. **Evaluate on representative in-domain queries, not MTEB** (Chroma, Liu).

There is essentially no credible 2025–2026 expert advocating *naive single-vector RAG* as SOTA. "Naive RAG fails in production" is the consensus floor.

---

## 5. The contrarian camps (dissent, surfaced)

Three distinct dissenting camps. None of them argues "no retrieval" — they argue against *specific* defaults.

### Camp A — "RAG is dead, context engineering is king" (Chroma / Jeff Huber)

The strongest *named* contrarian. In the Latent Space interview (2025), **Jeff Huber (Chroma CEO)** argues:

- The term "RAG" is "really confusing" — it conflates retrieval, augmentation, and generation. He rejects the reduction of RAG to "single dense vector search."
- **Context Rot** (Chroma technical report, ~Aug 2025): "the performance of LLMs is not invariant to how many tokens you use. As you use more and more tokens, the model can pay attention to less" — directly attacking the "just stuff a 1M-token window" narrative ([Latent Space, "RAG is Dead, Context Engineering is King"](https://www.latent.space/p/chroma)).
- His prescription is *not* "stop retrieving" — it's: **name the primitives** (dense, lexical, filters, rerank, assembly, eval), win first-stage retrieval with hybrid (200–300 candidates), **always rerank**, and prefer "tight, structured contexts over maximal windows."

Net: a *terminology and emphasis* dissent that, on substance, **reinforces** the convergent stack. The real target is lazy long-context maximalism.

### Camp B — long-context replaces RAG

The headline-grabbing dissent. Evidence (2025–2026) is mixed and the camp has *lost* its strong form: the LaRA study and year-end reviews conclude **"no silver bullet"** — choice depends on model, context size, task type, and retrieval characteristics; long context can win on quality for some QA but RAG remains far cheaper per token and indispensable in enterprise ([arXiv LaRA, 2025-01](https://arxiv.org/html/2501.01880v1); [RAGFlow 2025 year-end review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context); [TianPan decision framework, 2026-04](https://tianpan.co/blog/2026-04-09-long-context-vs-rag-production-decision-framework)). Chroma's Context Rot finding actively undercuts the strong form. **Mature consensus: route between them** (simple → retrieval, complex multi-hop → long context), not replace.

### Camp C — agentic tool-use / grep beats vector search (especially for code)

The freshest and most provocative. Cursor, Claude Code, and Devin reportedly favor **grep/AST/filesystem tools over vectors for code**, because "code isn't prose…a function call won't necessarily retrieve its definition" and grep is "fast, exact, deterministic" while RAG's failure mode is "silent and compounding" ([MindStudio, "Why Cursor, Claude Code, and Devin Use grep, Not Vectors"](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead)). A Feb-2026 paper claims **keyword search via agentic tool use attains >90% of vector-RAG performance with no vector DB** ([arXiv 2602.23368](https://arxiv.org/pdf/2602.23368)); a LlamaIndex 2026 benchmark found a filesystem agent beat traditional RAG on correctness and relevance ([LlamaIndex, "Did Filesystem Tools Kill Vector Search?"](https://www.llamaindex.ai/blog/did-filesystem-tools-kill-vector-search)).

**Important scoping for *this* tool's axis (topical docs / websites / databases, not a codebase):** these proponents explicitly carve out where vectors still win — "large-scale document retrieval over millions of documents," "unstructured text at scale," "multi-tenant knowledge bases with filtering," and they concede **hybrid search now outperforms pure vector RAG**. AU banking regulation is unstructured prose at scale, not a dependency graph — squarely in the territory the grep camp itself concedes to hybrid retrieval. The relevant *transferable* lesson is the **agentic wrapper**: let the agent decide what/whether to retrieve and iterate (the "Agentic RAG reasoning loop"), layered on top of the hybrid+rerank stack — which is exactly what Azure Agentic Retrieval and Hebbia's Matrix ship.

---

## Verdict

**The convergent expert-recommended SOTA default as of mid-2026 is a hybrid, reranked, eval-driven retrieval pipeline — *not* naive vector RAG, and *not* long-context-replaces-everything.** Stated as one concrete stack:

> **Ingest with contextual chunk augmentation** (Anthropic Contextual Retrieval-style) → **hybrid first-stage retrieval = dense embeddings + BM25/lexical** → **RRF fusion** → retrieve broad (**top ~50–200 candidates**) → **cross-encoder reranker** (Cohere Rerank 4 or Voyage rerank-2.5) → **top 5–10 chunks → LLM**. Wrap the whole thing in an **agentic retrieval loop** (let the agent decide what/whether to retrieve and re-query on low confidence), and **gate everything on a golden eval set built from your own domain queries, not MTEB**. For a specialized vertical like AU banking regulation, **strongly consider domain-tuned embeddings** (the Harvey/Voyage legal precedent).

This is corroborated independently by Anthropic, Cohere, Voyage, kapa.ai, Perplexity (Vespa), Glean, Azure/AWS/GCP/OpenAI/Databricks reference architectures, and named experts Jason Liu and Jo Kristian Bergum. Every major cloud now *ships this as the default*, which is the strongest possible signal of de-facto SOTA.

**Dissent to keep prominent:** The strongest contrarian voice is **Jeff Huber / Chroma — "RAG is dead, context engineering is king."** On inspection it is a *reframing*, not a refutation: name the primitives, win first-stage hybrid retrieval, *always rerank*, and beware **Context Rot** (more tokens ≠ better attention) — which actively rebuts the rival long-context-maximalist camp. The genuinely live, unresolved dissent for an agent-consumed tool is **agentic tool-use vs. embedding retrieval** (Camp C): for *structured* corpora (code, databases) deterministic tools can match or beat vectors, and that lesson transfers as an **agentic wrapper** over — not a replacement for — the hybrid+rerank core. For unstructured regulatory prose specifically, even the grep camp concedes hybrid retrieval wins.

---

## Sources

- [Systematically Improving RAG Applications](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/) — Jason Liu — 2025-01-24
- [Text Chunking Strategies for RAG Applications](https://jxnl.co/writing/2025/09/11/text-chunking-strategies-for-rag-applications/) — Jason Liu — 2025-09-11
- [Stop Trusting MTEB Rankings (Kelly Hong, Chroma)](https://jxnl.co/writing/2025/09/11/stop-trusting-mteb-rankings-kelly-hong-chroma/) — Jason Liu (summarizing Kelly Hong) — 2025-09-11
- [Generative Benchmarking (technical report)](https://research.trychroma.com/generative-benchmarking) — Kelly Hong, Anton Troynikov, Jeff Huber, Morgan McGuire (Chroma) — 2025-04
- ["RAG is Dead, Context Engineering is King" — with Jeff Huber of Chroma](https://www.latent.space/p/chroma) — Latent Space / Jeff Huber — 2025
- [Improving Zero-Shot Ranking with Vespa Hybrid Search — part two](https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/) — Jo Kristian Bergum (Vespa) — 2023 (canonical hybrid/BM25 reference, still cited 2025)
- [Redefining Hybrid Search Possibilities with Vespa — part one](https://blog.vespa.ai/redefining-hybrid-search-possibilities-with-vespa/) — Vespa / Jo Kristian Bergum
- [Anthropic's Contextual RAG (summary of Anthropic cookbook)](https://www.analyticsvidhya.com/blog/2024/11/anthropics-contextual-rag/) — Analytics Vidhya (summarizing Anthropic) — 2024-11
- [Contextual retrieval in Anthropic using Amazon Bedrock Knowledge Bases](https://aws.amazon.com/blogs/machine-learning/contextual-retrieval-in-anthropic-using-amazon-bedrock-knowledge-bases/) — AWS — 2025
- [Cohere's Rerank Model (docs)](https://docs.cohere.com/docs/rerank) — Cohere
- [End-to-end RAG with Chat, Embed, and Rerank](https://docs.cohere.com/docs/rag-complete-example) — Cohere
- [RAG Best Practices: Lessons from 100+ Technical Teams](https://www.kapa.ai/blog/rag-best-practices) — kapa.ai
- [How to Build a RAG Pipeline from Scratch in 2026](https://www.kapa.ai/blog/how-to-build-a-rag-pipeline-from-scratch-in-2026) — kapa.ai — 2026
- [How Perplexity Built an AI Google](https://blog.bytebytego.com/p/how-perplexity-built-an-ai-google) — ByteByteGo
- [How Perplexity AI Answers Work: Retrieval, Ranking, and Citation Pipeline](https://ziptie.dev/blog/how-perplexity-ai-answers-work/) — ZipTie
- [Glean: Building Robust Enterprise Search with LLMs and Traditional IR](https://www.zenml.io/llmops-database/building-robust-enterprise-search-with-llms-and-traditional-ir) — ZenML LLMOps Database
- [Danny Wheller, VP of Business & Strategy at Hebbia, on vertical vs horizontal enterprise AI](https://sacra.com/research/danny-wheller-hebbia-vertical-vs-horizontal-enterprise-ai/) — Sacra
- [Hebbia's Edge: Building a System of Record for Enterprise Reasoning](https://medium.com/@takafumi.endo/hebbias-edge-building-a-system-of-record-for-enterprise-reasoning-1264ab76ec6b) — Takafumi Endo
- [Report: Harvey Business Breakdown & Founding Story](https://research.contrary.com/company/harvey) — Contrary Research
- [Expanding Harvey's Model Offerings](https://www.harvey.ai/blog/expanding-harveys-model-offerings) — Harvey — 2025-05
- [Foundation Models for RAG — Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/) — AWS
- [Multimodal retrieval for Bedrock Knowledge Bases now GA](https://aws.amazon.com/about-aws/whats-new/2025/11/multimodal-retrieval-bedrock-knowledge-bases/) — AWS — 2025-11
- [Next-Level RAG on Azure: Building Knowledge Bases with Azure AI Search and Foundry](https://itnext.io/next-level-rag-on-azure-building-knowledge-bases-with-azure-ai-search-and-foundry-6d88d60e7202) — itnext (Microsoft Ignite 2025) — 2025
- [Agentic Retrieval Overview — Azure AI Search](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview) — Microsoft Learn
- [RAG infrastructure for generative AI using Vertex AI and Vector Search](https://docs.cloud.google.com/architecture/gen-ai-rag-vertex-ai-vector-search) — Google Cloud
- [The GCP RAG Spectrum: Vertex AI Search, RAG Engine, and Vector Search](https://medium.com/google-cloud/the-gcp-rag-spectrum-vertex-ai-search-rag-engine-and-vector-search-which-one-should-you-use-f56d50720d5a) — Saurabh Pandey (Google Cloud Community)
- [Assistants File Search](https://developers.openai.com/api/docs/assistants/tools/file-search) — OpenAI
- [RAG on Databricks](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation) — Databricks
- [Enterprise RAG Platforms Comparison 2026](https://atlan.com/know/enterprise-rag-platforms-comparison/) — Atlan — 2026
- [Long Context vs. RAG for LLMs: An Evaluation and Revisits (LaRA)](https://arxiv.org/html/2501.01880v1) — arXiv — 2025-01
- [From RAG to Context — A 2025 year-end review of RAG](https://ragflow.io/blog/rag-review-2025-from-rag-to-context) — RAGFlow
- [Long-Context Models vs. RAG: production decision framework](https://tianpan.co/blog/2026-04-09-long-context-vs-rag-production-decision-framework) — TianPan — 2026-04
- [Why Cursor, Claude Code, and Devin Use grep, Not Vectors](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead) — MindStudio
- [Vector Search Vs. Filesystem Tools: 2026 Benchmarks](https://www.llamaindex.ai/blog/did-filesystem-tools-kill-vector-search) — LlamaIndex — 2026
- [Keyword search is all you need: RAG-level performance without vector DBs via agentic tool use](https://arxiv.org/pdf/2602.23368) — arXiv — 2026-02
