# Research — RAG / knowledge-tool patterns for AI over huge corpora

**Author:** orchestrator (research mode, not workflow run)
**Date:** 2026-04-27
**Scope:** survey of retrieval architectures, vector / reranker / embedding component landscape, and MCP knowledge-tool patterns — sized for **huge** knowledge bases (tens of thousands to millions of pages). Output is a literature/landscape map plus a single recommendation shape for this repo.
**Method:** canon-librarian (returned a structural gap — see §10), then WebSearch breadth across eight queries on retrieval patterns, components, and MCP surfaces. Currency: April 2026.

This document extends `synthesis.md` from this same session. The synthesis was the AU-banking-as-stress-test answer; this is the underlying landscape map a future kapa-style silo for this repo (or any topic) would draw on.

---

## Table of contents

- [1. The pattern taxonomy](#1-the-pattern-taxonomy)
- [2. The composed architecture — how the patterns layer](#2-the-composed-architecture--how-the-patterns-layer)
- [3. Component landscape — vector DBs](#3-component-landscape--vector-dbs)
- [4. Component landscape — embedding models](#4-component-landscape--embedding-models)
- [5. Component landscape — rerankers](#5-component-landscape--rerankers)
- [6. The MCP knowledge-tool surface](#6-the-mcp-knowledge-tool-surface)
- [7. Cost and scale envelope](#7-cost-and-scale-envelope)
- [8. Build-vs-buy decision tree](#8-build-vs-buy-decision-tree)
- [9. Recommendation shape for this repo](#9-recommendation-shape-for-this-repo)
- [10. Canon gap and proposed canon additions](#10-canon-gap-and-proposed-canon-additions)
- [11. Sources](#11-sources)

---

## 1. The pattern taxonomy

Eight patterns the field has converged on or is debating in 2026. Listed in rough order of how settled they are.

### 1.1 Naive vector RAG (single-stage dense retrieval)

Embed chunks, store in a vector DB, embed query, return top-k by cosine. **Settled as the floor**, not the ceiling. Anthropic's own benchmarks put naive top-20 failure rate at **5.7%** as the baseline against which all other techniques are measured. Acceptable for prototypes; rarely optimal in production.

### 1.2 Hybrid retrieval (BM25 + dense + RRF)

Run BM25 (sparse, exact-token) and dense (semantic) in parallel, fuse rankings via Reciprocal Rank Fusion. **The mandatory production baseline.** Rationale: dense embeddings miss exact-token queries (acronyms, IDs, defined terms); BM25 misses paraphrase. RRF requires no training. Native hybrid support is now a first-class feature in Weaviate (BlockMax WAND + RSF), Milvus 2.5+ (Sparse-BM25), Qdrant v1.9+, LanceDB, Pinecone, and Turbopuffer. **If you build a 2026 retrieval system without hybrid, you are starting below the floor.**

### 1.3 Anthropic Contextual Retrieval (Sep 2024)

Before embedding each chunk, prepend a 50–100 token LLM-generated context describing where the chunk sits in the document. Index the *contextualized* chunk. The same trick is applied to the BM25 side. Numbers from Anthropic's own benchmark on diverse domains (code, fiction, ArXiv, science):

| Configuration | Top-20 failure rate | Reduction vs naive |
|---|---|---|
| Naive embeddings | 5.7% | baseline |
| Contextual embeddings only | 3.7% | −35% |
| Contextual embeddings + Contextual BM25 | 2.9% | −49% |
| Above + reranking | **1.9%** | **−67%** |

Cost: one Claude Haiku call per chunk at index time (one-shot, with prompt caching the context-document is cached across all chunks of that doc). **Largest single quality lever in current literature** for the "improve retrieval quality" axis. Voyage and Gemini embeddings benchmarked best.

### 1.4 Cross-encoder reranking

After hybrid returns top-k (say, k=50–100), run a cross-encoder (or LLM-as-judge) over each (query, chunk) pair and re-score. Take final top-N (typically 5–10). Adds latency (one rerank per kept chunk) and cost, but quality lift is consistently 15–40% precision in benchmarks. **Settled as a near-mandatory second stage** for any production system where answer quality matters more than latency.

Best models in April 2026 by ELO/Hit@1 (per AIMultiple, ZeroEntropy, Voyage benchmarks):

| Reranker | Notes | Latency |
|---|---|---|
| Zerank-2 | 1638 ELO; top quality | mid |
| Cohere Rerank v4.0 Pro | 1629 ELO; managed; 595–603ms | sub-second |
| Voyage rerank-2.5 | Best for code/legal/finance domains | sub-second |
| Jina Reranker v3 | Only top-tier model under 200ms total | <200ms |
| BGE Reranker v2-m3 | Open-weights option | depends on host |
| gte-reranker-modernbert-base | 149M params matches 1.2B nemotron at Hit@1 | depends |

Latency-quality-cost is a Pareto front. Pick by which knee matters.

### 1.5 ColBERT / late interaction

Instead of one vector per chunk, store one vector per *token*. At query time, compute MaxSim between query tokens and each chunk's token-embeddings. **Better recall than single-vector dense, especially for novel domains and low-resource languages.** Also: token-level explainability (you can see *which tokens* matched).

The cost: storage. For 10M passages, OpenAI text-embedding-3-small needs **61 GB**; ColBERT needs **~768 GB** (~12× more). Production-feasible via RAGatouille (compresses indexes on disk), JinaColBERT-v2 (~90% RAM reduction vs naive ColBERTv2), or Qdrant's late-interaction support. **Not a default. A specific lever** for cases where (a) the corpus is novel-domain or multilingual and (b) you can absorb the storage cost.

### 1.6 GraphRAG

Extract entities and relations from chunks (LLM-as-extractor), build a knowledge graph, optionally cluster into community summaries. At query time, retrieve via graph traversal in addition to or instead of vector search. **Strong on multi-hop reasoning and global summarization. Weaker than vanilla RAG on single-hop factoid queries.**

The 2026 ICLR paper *"When to Use Graphs in RAG"* (arXiv 2506.05690 → GraphRAG-Bench) is the corrective: **don't default to GraphRAG**. Use it when the query distribution is multi-hop or "give me the big picture across these documents." Hybrid Selection strategies (route per-query between RAG and GraphRAG) gain ~6 points on MultiHop-RAG over either alone, and keep cost lower than always-GraphRAG. GraphRAG also performs **16.6% worse than RAG on time-sensitive queries** — a real concern for live-data corpora.

Verdict: **conditional, not default.** Build a query sample first; flip GraphRAG on if ≥20% of queries are multi-hop or community-summary shape.

### 1.7 RAPTOR / hierarchical

Recursive Abstractive Processing for Tree-Organized Retrieval. Cluster chunks, summarize each cluster, repeat to build a hierarchical tree of summaries. Retrieve from any tree level, so a query can hit either fine-grained chunks or document-level summaries.

Reports 15–30% precision improvement on multi-step QA (Stanford CS224N report). Integrated into RAGFlow as a one-toggle preprocessing step. 2026 enhancements use Leiden community detection and adaptive clustering. **Useful when queries straddle "tell me the overview" and "give me the specific clause"** — common in legal/financial/regulated corpora. Cost: index-time LLM summarization (one pass per cluster level).

### 1.8 Agentic retrieval

Agent calls a `search` tool one or more times, optionally rewriting the query, expanding it (HyDE), or decomposing it (Self-RAG, CRAG). Anthropic's multi-agent research system positions this as the alternative to single-shot top-k → generate. Token cost is the headline objection: **~15× chat tokens** in Anthropic's own report. Justified for high-value agentic workflows (research, compliance review); over-spec for retail Q&A.

### 1.9 Long-context-as-replacement (the rejected baseline)

Stuff everything into the context window, skip retrieval. Multi-fact recall ~60% even at million-token windows, "context rot" is real, and at $15/query at corpus scale it doesn't pencil. **Debunked for production at huge-corpus scale by mid-2026.**

---

## 2. The composed architecture — how the patterns layer

These patterns aren't alternatives — they stack. The 2026 SOTA shape for a **huge knowledge base** is roughly:

```
                    ┌──────────────────────────────────────────┐
                    │  AGENT (LLM with tool-use)               │
                    └───────────────────┬──────────────────────┘
                                        │ search_<TOPIC>(query)
                                        ▼
                    ┌──────────────────────────────────────────┐
                    │  4. AGENT SURFACE                        │
                    │     Narrow typed tool, returns           │
                    │     {source_url, content} chunks.        │
                    │     Often via MCP-over-HTTP.             │
                    └───────────────────┬──────────────────────┘
                                        │
                                        ▼
                    ┌──────────────────────────────────────────┐
                    │  3b. RERANK (stage 2)                    │
                    │      Cross-encoder over top-k.           │
                    │      Cohere v4 / Voyage 2.5 / Jina v3.   │
                    └───────────────────┬──────────────────────┘
                                        │ top-50..100
                                        ▲
                    ┌──────────────────────────────────────────┐
                    │  3a. HYBRID RETRIEVAL (stage 1)          │
                    │      BM25 + dense, fused via RRF.        │
                    │      + Anthropic Contextual at index time│
                    │      + optional GraphRAG branch          │
                    │      + optional RAPTOR tree levels       │
                    └───────────────────┬──────────────────────┘
                                        ▲
                    ┌──────────────────────────────────────────┐
                    │  2. INDEX  (vector DB + sparse index)    │
                    │      Pinecone / Qdrant / Turbopuffer /   │
                    │      Weaviate / pgvector / LanceDB       │
                    └───────────────────┬──────────────────────┘
                                        ▲
                    ┌──────────────────────────────────────────┐
                    │  1. INGEST + REFRESH PIPELINE            │
                    │      Source registry, chunkers,          │
                    │      contextualizer (LLM call/chunk),    │
                    │      embedder, refresh cadence.          │
                    └──────────────────────────────────────────┘
```

**Two non-negotiables for huge corpora:**

1. **Hybrid + rerank is the floor.** Anthropic's own numbers show contextual + hybrid + rerank together give a **67% failure-rate reduction** (5.7% → 1.9%). Skipping any of the three loses meaningful quality.
2. **The agent surface is a typed narrow tool returning chunks.** Not a generic `search()` endpoint, not a generated answer — chunks the agent reasons over with `source_url` for citation. This is the lesson kapa.ai productized.

Three conditional add-ons, each gated on query-sample evidence:

- **GraphRAG branch** — turn on if multi-hop ≥20% of queries.
- **RAPTOR hierarchy** — turn on if queries straddle overview/detail levels.
- **Agentic loop** — turn on if quality-per-query > cost-per-query for the use case.

---

## 3. Component landscape — vector DBs

Picking by axis matters more than picking the "best." All major DBs ship hybrid in 2026.

| DB | Type | Hybrid | Strength | Weakness | Pick when |
|---|---|---|---|---|---|
| **Pinecone** | Managed | Yes (proprietary sparse) | Scale, ops-free, mature | Lock-in, cost at scale | You want zero infra and budget isn't the constraint |
| **Qdrant** | OSS / Cloud | Yes (named vectors v1.9+) | Rust performance, ACORN solved filtered HNSW, rich payload filtering | Operational footprint if self-hosted | Complex metadata filtering matters (legal, finance) |
| **Weaviate** | OSS / Cloud | Yes (BlockMax WAND + RSF) | Built-in vectorizer modules (insert raw text) | Heavier than embedded options | You want the DB to handle embedding too |
| **pgvector** | Postgres extension | Yes (with extensions) | Already-have-Postgres simplicity, SQL filter, transactional | Underperforms purpose-built at >10M vectors | You're a Postgres shop and corpus < ~10M chunks |
| **LanceDB** | Embedded / OSS | Yes | In-process, zero-copy, no server, columnar (Lance format) | New ecosystem | Self-hosted single-node, frequent data updates |
| **Turbopuffer** | Serverless | Yes (BM25 + vector native) | Pay-per-use, cheap at low query rate | Newer, less battle-tested | Bursty workloads, cost-sensitive |
| **Chroma** | OSS / embedded | Limited | Easy local dev, MCP server exists | Not the production-scale leader | Prototyping or small corpora |
| **Milvus 2.5+** | OSS / Cloud | Yes (Sparse-BM25) | Scale, GPU support | Operational complexity | Very large scale (>100M vectors), GPU available |

**Default recommendation for a huge-corpus repo (≥1M chunks):** Qdrant if self-hosting, Turbopuffer if you want serverless economics, Pinecone if managed-and-mature is the priority. pgvector if and only if you already run Postgres and the corpus is in the low millions.

**Storage math for sizing:** with OpenAI text-embedding-3-small (1536 dims, float32), **10M chunks = ~61 GB**. With ColBERT-style late interaction, **~768 GB**. With Matryoshka-truncated 256-dim embeddings, **~10 GB**. Pick embedding dimension with storage in mind — Matryoshka-trained models (Cohere v4, OpenAI v3, Voyage) let you truncate without retraining.

---

## 4. Component landscape — embedding models

April 2026 MTEB-relevant top picks:

| Model | MTEB | Context | Pricing | Best for |
|---|---|---|---|---|
| **OpenAI text-embedding-3-large** | 64.6 | 8K | $0.13/1M tok | Default high-quality managed |
| **Cohere embed-v4** | 65.2 | **128K** | competitive | Long single-chunk documents (full contracts, papers) |
| **Voyage-3-large** | high (domain) | 32K | competitive | **Code, legal, medical, financial** — beats general models by 4–6 MTEB points on domain retrieval |
| **Gemini Embedding 2 (Mar 2026)** | top-tier | 8K, 3072d | $0.006/1M (cheapest) | Multimodal (text/image/video/audio/PDF), 100+ languages |
| **Jina Embeddings v3** | strong | 8K, late chunking | open-weights | Long documents, multilingual, cost-controlled |
| **BGE-M3** | 63.0 | 8K | open-weights | Self-host, multilingual, multi-functional (dense+sparse+colbert) |

**Decision rule:** Voyage if domain is code/legal/finance/medical (this includes AU banking → Voyage). OpenAI text-embedding-3 as the safe default. Cohere if your chunks are long. Gemini Embedding 2 if multimodal or cost-extreme. BGE-M3 if you must self-host without an API.

For AU banking specifically: **Voyage-3-large is the right embedding model**, by stated benchmark advantage on financial text.

---

## 5. Component landscape — rerankers

Restated from §1.4 with the picking dimensions made explicit.

| Reranker | Quality | Latency | Cost | Pick when |
|---|---|---|---|---|
| Cohere Rerank v4.0 Pro | top-3 quality | ~600ms | managed $ | Default managed pick |
| Voyage rerank-2.5 | top in code/legal/finance | ~600ms | managed $ | Domain match (incl. AU banking) |
| Zerank-2 | #1 ELO | mid | managed $ | Quality is the only axis |
| Jina Reranker v3 | top-tier among <200ms | <200ms | managed/self | Latency budget < 200ms |
| BGE Reranker v2-m3 | strong open-weights | depends | self-host | Air-gapped or no-API requirement |
| gte-reranker-modernbert-base | matches 1.2B at 149M | fast | self-host | Small footprint matters |

**Universally true:** reranking provides **15–40% precision lift** over hybrid alone. Skipping it is a quality-cost-budget choice, not a default-correct one.

---

## 6. The MCP knowledge-tool surface

Three patterns observed in the wild as of 2026, with tradeoffs:

### 6.1 Managed: kapa.ai pattern

A vendor (kapa) runs the full stack — connectors, ingest, chunking, embeddings, hybrid retrieval, rerank, refresh — and exposes one MCP server per customer at `<subdomain>.mcp.kapa.ai`. The server exposes **one tool** (`search_<PRODUCT>_knowledge_sources`) returning `{source_url, content}` chunks. Auth: OAuth or API key. Rate-limited (300/day per OAuth user, 60/min per team). The Temporal MCP at `temporal.mcp.kapa.ai` is the worked example. Setup time: ~60 seconds.

**Tradeoff:** zero infra, opaque pipeline, vendor risk, vendor cost. The pipeline internals (chunking strategy, embedding model, reranker choice) are not consumer-controllable.

### 6.2 Self-hosted official MCP servers

Both Qdrant and Chroma ship official MCP servers as wrappers over their respective vector DBs:

- **`qdrant/mcp-server-qdrant`** — exposes two tools: `qdrant-store` and `qdrant-find`. Acts as a "semantic memory layer." Customer brings the embedding model, ingest, refresh.
- **`chroma-core/chroma-mcp`** — exposes vector + full-text + metadata-filter retrieval. HTTP client points at self-hosted Chroma instance.

**Tradeoff:** you control everything (embedding model, chunker, refresh, rerank — though rerank is bring-your-own). You also operate everything. The MCP server is just the protocol surface; it does not give you the architecture.

### 6.3 Build-your-own MCP wrapping a custom pipeline

Stand up your own MCP server (any HTTP framework — FastMCP, MCP SDK, Netlify Edge Function in kapa's case). Behind it, run whatever retrieval pipeline you want: hybrid + contextual + rerank, GraphRAG, RAPTOR, agentic loop. Expose a single tool with the kapa-style chunk contract.

**Tradeoff:** total control, total responsibility. Months of work. Right answer for high-value durable corpora; wrong answer for one-off prototypes.

### 6.4 The MCP-vs-RAG framing trap

Several 2026 essays frame "MCP vs RAG" as competing approaches. **They are not.** MCP is the *protocol* for how an LLM reaches a tool. RAG is the *technique* for what the tool does. A kapa-style server is "MCP carrying RAG." The InfraNodus MCP carries GraphRAG. Anthropic's reference Memory MCP server carries a knowledge-graph-backed memory store. The interface (MCP) and the backend (RAG / GraphRAG / grep / vector DB / SQL) are orthogonal — choose each independently.

### 6.5 Anthropic's "Skills" / Tool Search direction (newer, watch)

Anthropic's 2025–2026 Skills pattern treats *tools themselves* as indexed knowledge — load only the tool schemas the agent needs for the current sub-task. Reduces initial-context overhead by ~85% in their reports for large tool libraries. **Adjacent to RAG but operates one level up:** RAG retrieves *content*; Skills/Tool-Search retrieves *tool affordances*. Likely to influence MCP design over the next 12 months. Not yet a stable production pattern; flag and watch.

---

## 7. Cost and scale envelope

Rough order-of-magnitude figures for a 1M-chunk corpus (≈10K average-size documents). Numbers vary 2–5× by provider and choice, but the *shape* is stable.

| Phase | Item | Cost range |
|---|---|---|
| **Index (one-time)** | Embedding 1M chunks @ ~500 tok | $50–$300 (depending on model) |
| | Anthropic Contextual Retrieval (1 Haiku call/chunk, w/ prompt caching) | **$300–$2,000** |
| | Vector DB storage (1M × 1536d float32) | ~6 GB → trivial cost |
| | ColBERT alternative storage | ~75 GB → $$/month if cloud |
| **Refresh (steady)** | 5% chunk delta/week × embedding | $5–$30/week |
| | + contextualization for changed chunks | $20–$100/week |
| **Query (steady)** | Embedding query | sub-cent |
| | Vector DB query | sub-cent (managed) to ~$0 (self-host) |
| | Rerank top-50 | $0.001–$0.01 per query |
| | Agentic loop (~15× tokens) | 15× the above |

**Headline:** indexing a 1M-chunk corpus with contextual retrieval is a **few-hundred-to-low-thousand-dollar one-time spend**, not a five-figure event. A 10M-chunk corpus is order-of-magnitude $5K–$20K to index with contextualization. Per-query cost is dominated by reranking and agentic loops, not retrieval itself.

**Where cost actually bites:** opex on the vector DB at scale (managed Pinecone for 10M+ vectors is recurring $$$), plus contextualization re-runs every time you change your chunking strategy.

---

## 8. Build-vs-buy decision tree

```
Is your corpus < ~50 markdown files (canon-scale)?
  → Use grep / file-based. Skip RAG. Don't over-engineer.

Is your corpus single-vendor doc-shaped, < ~10K pages, freshness needs are vendor-cadence?
  → Use kapa.ai or equivalent managed service. Saves months.

Is your corpus huge (>10K pages) AND single-vendor / vendor-controlled / consistent?
  → Managed (kapa) is still viable; self-host MCP-over-Qdrant works if you want pipeline control.

Is your corpus huge AND multi-source AND/OR you need pipeline control (specific chunker, custom rerank, audit context, version anchoring)?
  → Self-host: MCP server + Qdrant (or Turbopuffer) + hybrid + contextual retrieval at index time + Voyage/Cohere reranker. Build the eval harness FIRST.

Is your corpus huge AND queries are predominantly multi-hop reasoning?
  → Add GraphRAG as a parallel branch (not replacement). Microsoft GraphRAG or LightRAG.

Do you need "give me the big picture" + "give me the specific clause" in the same surface?
  → Add RAPTOR hierarchical summarization at index time.
```

The kapa-style managed shape is the right answer for **more cases than people expect**, because it eats months of work in 60 seconds of setup. Self-host only when you need control the managed service can't give you.

---

## 9. Recommendation shape for this repo

Anchor: this repo currently has the canon (markdown + grep, in-stack Agent invocation). The user wants to introduce a knowledge-tool pattern. The answer is two distinct silos with a shared interface contract:

### 9.1 The pattern (replicable slot)

```
ONE MCP SERVER PER TOPICAL KNOWLEDGE SILO
  - exposes ONE tool: search_<TOPIC>_knowledge(query)
  - returns: list of {source_url, content} chunks (kapa contract)
  - backed by: source registry → ingest pipeline → INDEX → retrieval pipeline
  - refreshed on a topic-appropriate cadence
  - audited via source URLs (provenance is structural, not optional)
```

This is the kapa-shape generalized. The slot multiplies cleanly: one MCP per topic. Other Claude instances `claude mcp add --transport http <topic> <url>` and immediately benefit.

### 9.2 Two instances, two backends, same interface

| Silo | Corpus size | Backend | Interface |
|---|---|---|---|
| **Canon** (existing) | ~dozens of files | grep over markdown | currently in-stack Agent; could later expose MCP if needed externally |
| **AU banking** (new) | ~tens of thousands of pages | Hybrid (BM25+dense via Qdrant or Turbopuffer) + Anthropic Contextual Retrieval at index + Voyage rerank-2.5 | MCP-over-HTTP, kapa-style chunk contract |

**Don't change the canon.** Grep is correct for that corpus size. Adding embeddings would be over-engineering. The canon's interface could *eventually* wear an MCP wrapper if external Claude instances need it, but the backend stays grep.

**For AU banking:** the SOTA shape is hybrid + contextual + rerank, exposed as MCP. Backed by Voyage-3-large embeddings (domain-justified). Vector DB: Qdrant (rich filtering for `(instrument, section, version, effective_date)` metadata) or Turbopuffer (cheaper if query rate is bursty). Reranker: Voyage rerank-2.5 (domain-justified).

### 9.3 What you actually have to build

Ordered by sequence:

1. **Eval harness first.** ~50–200 hand-written gold Q/A pairs. Without this, "SOTA" is a literature reflex, not an answerable claim about your corpus.
2. **Source registry.** YAML or similar — listing APRA standards, ASIC RGs, Federal Register instruments, AUSTRAC rules, RBA. With per-source refresh cadence and content type.
3. **Ingest pipeline.** Fetch → parse (PDF + HTML) → chunk (table-aware) → contextualize (Haiku call per chunk, with prompt caching) → embed (Voyage) → index (Qdrant).
4. **Retrieval pipeline.** Hybrid (BM25 + dense via RRF) → top-50 → Voyage rerank → top-5–10.
5. **MCP server.** Single tool, kapa contract, returns `{source_url, content}` chunks. Auth: API key. Rate-limit.
6. **Refresh worker.** Per-source cadence; diff-aware; tags chunks with `{instrument_id, version, effective_date, retrieved_at}`.

Optional, gated on eval evidence:
- GraphRAG branch (only if eval shows ≥20% multi-hop queries)
- RAPTOR (only if eval shows overview-vs-detail straddle)
- Agentic loop (only if quality > cost for the consumer)

### 9.4 What this repo gains, beyond the AU banking instance

The slot itself is the upgrade. Once the kapa-shape MCP scaffold exists in this repo, building the next topical silo (claude-code-internals, temporal-style topics, anything) becomes a configuration exercise, not a months-long project. **The real value is the slot, not any single instance.**

---

## 10. Canon gap and proposed canon additions

The canon-librarian returned an honest empty hand: **zero of the 19 corpus entries cover RAG, retrieval, embeddings, vector DBs, reranking, GraphRAG, ColBERT, contextual retrieval, agentic retrieval, or MCP-as-knowledge-surface.** The closest tangents are three Anthropic essays already known.

The librarian also flagged a **data-integrity issue**: `citation.yaml` files for the three Anthropic entries declare `body_completeness: full` but the corpus directories contain only `citation.yaml` + provenance `README.md` — no `body.md` or `source.txt` is on disk. The ingester recorded a sha256 but did not persist the body. This is a separate bug from the survey topic and worth fixing independently.

**Proposed canon additions** (open-access, fetchable URLs):

1. Lewis et al. 2020 — original RAG paper
2. Karpukhin et al. 2020 — DPR (dense passage retrieval)
3. Khattab & Zaharia 2020 — ColBERT
4. Robertson & Zaragoza — BM25 reference
5. Edge et al. 2024 — Microsoft GraphRAG
6. Anthropic Sep 2024 — Contextual Retrieval (notable miss; three other Anthropic essays are in-corpus)
7. arXiv 2506.05690 (ICLR'26) — *When to use Graphs in RAG* (the GraphRAG corrective)
8. RAPTOR paper (Sarthi et al. 2024)
9. Model Context Protocol spec (Anthropic, 2024) — absent from `sources.yaml`, `sources.ingest.yaml`, and `refresh-feeds.yaml` entirely
10. Ragas or BEIR — retrieval evaluation harness reference

The `refresh-feeds.yaml` keyword filter (line 25) already includes `retrieval` and `tool-use`, so the `canon-refresher` is configured to surface RAG papers from RSS — but nothing has been accepted into the corpus yet.

**Filing as upgrade entry**: this gap (curator-side, not the AI's call) should be captured as an upgrade entry — a no-brainer sized at one curator session.

---

## 11. Sources

### Anthropic primary

- [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — Anthropic, Sep 2024 — primary source for the 5.7% → 1.9% benchmark numbers.
- [Enhancing RAG with contextual retrieval (Cookbook)](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) — Anthropic — implementation guide.
- [Model Context Protocol servers](https://github.com/modelcontextprotocol/servers) — Anthropic + community — reference MCP servers including Memory (knowledge-graph-backed).

### Pattern surveys & benchmarks

- [Advanced RAG Techniques for High-Performance LLM Applications](https://neo4j.com/blog/genai/advanced-rag-techniques/) — Neo4j.
- [Building Contextual RAG Systems with Hybrid Search and Reranking](https://www.analyticsvidhya.com/blog/2024/12/contextual-rag-systems-with-hybrid-search-and-reranking/) — Analytics Vidhya.
- [RAG in 2026 — practical blueprint](https://dev.to/suraj_khaitan_f893c243958/-rag-in-2026-a-practical-blueprint-for-retrieval-augmented-generation-16pp).
- [The Next Frontier of RAG (2026–2030)](https://nstarxinc.com/blog/the-next-frontier-of-rag-how-enterprise-knowledge-systems-will-evolve-2026-2030/) — NStarX.
- [From RAG to Context — 2025 year-end review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context) — RAGFlow.

### GraphRAG

- [When to use Graphs in RAG (ICLR'26)](https://arxiv.org/abs/2506.05690) — the corrective paper.
- [GraphRAG-Bench (ICLR'26 official repo)](https://github.com/GraphRAG-Bench/GraphRAG-Benchmark).
- [RAG vs. GraphRAG: A Systematic Evaluation](https://arxiv.org/html/2502.11371v2).
- [Knowledge Graphs vs RAG (Atlan)](https://atlan.com/know/knowledge-graphs-vs-rag-for-ai/).

### ColBERT / late interaction

- [Late Interaction Retrieval Models (Weaviate)](https://weaviate.io/blog/late-interaction-overview).
- [RAGatouille (AnswerDotAI)](https://github.com/AnswerDotAI/RAGatouille) — production ColBERT toolkit.
- [Late interaction at Qdrant](https://qdrant.tech/articles/late-interaction-models/).

### Vector DB landscape

- [Best Vector Databases 2026 (Encore)](https://encore.dev/articles/best-vector-databases).
- [Vector Database Comparison 2026 (4xxi)](https://4xxi.com/articles/vector-database-comparison/).
- [Vector Database Performance Compared (Vecstore)](https://vecstore.app/blog/vector-database-performance-compared).

### Reranker landscape

- [Reranker Benchmark — Top 8 Models (AIMultiple)](https://aimultiple.com/rerankers).
- [Ultimate Guide to Choosing the Best Reranking Model (ZeroEntropy)](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/).
- [Voyage rerank-2 release](https://blog.voyageai.com/2024/09/30/rerank-2/).
- [Top Rerankers for RAG (Analytics Vidhya)](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/).

### Embedding models

- [Best Embedding Models 2026 (PE Collective)](https://pecollective.com/tools/best-embedding-models/).
- [Embedding Models Comparison 2026 (Reintech)](https://reintech.io/blog/embedding-models-comparison-2026-openai-cohere-voyage-bge).
- [Best Embedding Models for RAG 2026 (PremAI)](https://blog.premai.io/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/).

### MCP knowledge servers

- [Hosted MCP server (kapa docs)](https://docs.kapa.ai/integrations/mcp/overview) — managed reference.
- [Launch a Docs MCP Server with kapa](https://www.kapa.ai/blog/build-an-mcp-server-with-kapa-ai).
- [Official Qdrant MCP server](https://github.com/qdrant/mcp-server-qdrant) — self-host reference.
- [Chroma MCP server](https://github.com/chroma-core/chroma-mcp) — alternative self-host.
- [Knowledge MCP servers directory (Glama)](https://glama.ai/mcp/servers?query=Knowledge).

### RAPTOR / hierarchical

- [RAPTOR overview (VectorHub Superlinked)](https://superlinked.com/vectorhub/articles/improve-rag-with-raptor).
- [Enhancing RAPTOR with semantic chunking and adaptive graph clustering (Frontiers, 2026)](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1710121/full).
- [Long-context RAG based on RAPTOR (RAGFlow)](https://ragflow.io/blog/long-context-rag-raptor).

### MCP-vs-RAG framing

- [MCP vs RAG vs AI Agents (InfraNodus)](https://infranodus.com/docs/mcp-vs-rag-vs-ai-agents).
- [MCP vs RAG for Production Teams (Portkey)](https://portkey.ai/blog/mcp-vs-rag/).
- [Rethinking MCP — Skills, RAG-MCP](https://medium.com/@adityajani7270/rethinking-mcp-skills-rag-mcp-and-making-agents-that-scale-day-1-7c1e26e41ecd).
