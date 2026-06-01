# Recommendation — the single SOTA architecture for the topical knowledge-retrieval tool

_Synthesised 2026-06-01 from the six research axes in this folder ([01](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/01-interface-surface.md)–[06](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/06-proven-deployments-experts.md)) and cross-checked against the prior session [2026-04-25-au-banking-kb-sota](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/synthesis.md)._

This is the decisive document for the phase. The six axis files are the evidence base; this file is the converged answer to the question *"what is the proven, expert-recommended SOTA way to build this tool, MCP or otherwise."*

## Table of contents

- [The one-paragraph answer](#the-one-paragraph-answer)
- [Why one answer and not a menu](#why-one-answer-and-not-a-menu)
- [The architecture, stage by stage](#the-architecture-stage-by-stage)
- [The interface: MCP, but thin and owned](#the-interface-mcp-but-thin-and-owned)
- [What is OFF by default — and the switch that turns it on](#what-is-off-by-default--and-the-switch-that-turns-it-on)
- [Build, don't buy — with one exception](#build-dont-buy--with-one-exception)
- [Why this *is* the slot](#why-this-is-the-slot)
- [The real SOTA lever is the eval loop, not the stack](#the-real-sota-lever-is-the-eval-loop-not-the-stack)
- [Rejected alternatives and their flip conditions](#rejected-alternatives-and-their-flip-conditions)
- [Honest uncertainties and anchor risks](#honest-uncertainties-and-anchor-risks)

## The one-paragraph answer

The SOTA architecture as of mid-2026 is **an owned, thin, eval-driven hybrid-retrieval core — dense embeddings + BM25 fused with Reciprocal Rank Fusion, Anthropic-style contextual chunk augmentation at index time, and a cross-encoder reranker — exposed to agents as an MCP server with a single provenance-returning search tool, with graph and agentic layers gated OFF by default and switched on only by measured demand.** This is the "kapa.ai shape, built thin and owned." It is not novel and that is the point: every major cloud (AWS Bedrock Knowledge Bases, Azure AI Search, GCP Vertex, Databricks) now ships this exact pipeline as the *default*, and Anthropic, Cohere, Voyage, Perplexity, kapa.ai, and named practitioners (Jason Liu, Jo Kristian Bergum) all independently recommend it. Six independent research axes converged on it this session, and so did the prior AU-banking session five weeks ago. The convergence is the signal.

## Why one answer and not a menu

You asked for *one* approach that is SOTA, proven, and expert-recommended — not a survey. The honest finding is that the field has **converged hard**, so a single answer is defensible rather than arbitrary. The disagreements that remain are at the edges (which reranker; pgvector vs Qdrant; when graphs turn on) — not at the core, which is settled. Where genuine dissent exists (Chroma's "RAG is dead / context engineering"; the agentic-grep camp) it turns out to *reframe* the convergent stack rather than refute it — see [06](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/06-proven-deployments-experts.md). The one place the convergence is loud and unanimous: **the accuracy is won in the hybrid+rerank+eval layer, not in the choice of tool or vendor.**

## The architecture, stage by stage

```
                         ┌──────────────────────────────────────────────┐
   sources               │            INDEX-TIME (ingest)               │
   ───────               │                                              │
   local docs ─────────► │  parse → structure-aware ~512-tok chunks     │
   websites   ─────────► │  → CONTEXTUAL PREPEND (Anthropic, 1 LLM call │
   databases  ─────────► │     per chunk) → embed → store dense + BM25  │
   federated APIs ─────► │  (parent-doc + version/provenance metadata)  │
                         └──────────────────────────────────────────────┘
                                              │
   agent ──MCP search(query)──►  ┌────────────▼─────────────────────────┐
                                 │          QUERY-TIME (retrieve)        │
                                 │  metadata pre-filter                  │
                                 │  → hybrid: dense + BM25               │
                                 │  → RRF fusion (k=60), top ~50–100     │
                                 │  → cross-encoder RERANK → top 5–10    │
                                 │  → return [{source_url, content}]     │
                                 └───────────────────────────────────────┘
```

| Stage | SOTA choice (mid-2026) | Why | Proven by | Evidence (see axis file) |
|---|---|---|---|---|
| **Chunking** | Structure-aware + recursive ~512-token, **contextual prepend** (Anthropic Contextual Retrieval), return parent doc | Contextual prepend is the single largest cheap lever; fixed/recursive matches or beats "semantic" chunking | Anthropic; corroborated NAACL-2025/Vectara | [02](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/02-core-retrieval.md) |
| **Embeddings** | `voyage-3.5` (managed) **or** `Qwen3-Embedding-8B` (self-host, Apache-2.0, data sovereignty), stored MRL 1024-dim + int8 | Top of MTEB-class; MRL+int8 cuts store cost with negligible recall loss | Voyage; Qwen | [02](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/02-core-retrieval.md) |
| **Lexical channel** | **BM25 (mandatory, not legacy)** | Regulatory text is identifier-dense (section/standard codes); dense embeddings have a *provable* dimensional ceiling (DeepMind LIMIT) where BM25 still scores 85–94% | Perplexity (Vespa), Vespa/Bergum | [02](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/02-core-retrieval.md), [06](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/06-proven-deployments-experts.md) |
| **Fusion** | Reciprocal Rank Fusion, k=60, retrieve broad (top 50–100) | The only near-universal "query transformation" that always helps | de-facto default everywhere | [03](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/03-reranking-advanced.md) |
| **Rerank** | Cross-encoder: **Cohere Rerank 4 / Voyage rerank-2.5** (API) or **BGE-reranker-v2-m3 / answerai-colbert-small** (self-host) → top 5–10 | Largest precision lift on the candidate set; can make end-to-end RAG *faster* by shrinking LLM context 50→5 | Anthropic, Cohere, Voyage; everyone | [03](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/03-reranking-advanced.md) |
| **Store** | **pgvector** (if Postgres already present) or **Qdrant** + a BM25/sparse channel | At this corpus size vector search is 5–50ms vs 500ms–3s generation — scale is a non-issue; accuracy lives in the hybrid+rerank layer | Cursor, Qdrant production users | [05](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/05-infrastructure-buildvsbuy.md) |
| **Framework** | **None / thin in-house** behind one swappable `retrieve(query)` interface | Frameworks hide the levers that matter (chunking, embedding, hybrid weighting); winning teams "barely talk about tools" | Hamel Husain (30+ companies) | [05](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/05-infrastructure-buildvsbuy.md) |

## The interface: MCP, but thin and owned

**Yes, MCP — but as a thin wrapper over a retrieval core you own, not as the architecture itself.** The recommended surface is an **MCP server exposing a single semantic-search tool that returns `{source_url, content}` chunks** (the kapa shape). Rationale:

- MCP is now the de-facto integration standard: Anthropic donated it to the Linux Foundation in December 2025 with OpenAI, Google, and Microsoft as co-sponsors — it is neutral, foundation-governed infrastructure, which makes betting the interface on it **low-regret**. It is natively consumable by Claude, ChatGPT, Gemini, Copilot, Cursor, and Replit without per-client glue. ([01](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/01-interface-surface.md))
- The **single-tool, chunk-with-provenance** shape neutralises MCP's worst documented failure mode (tool-count context bloat) and gives the per-chunk provenance a regulated domain needs.
- **Keep a plain HTTP `/search` core underneath the MCP wrapper.** The contrarian (Glean, Mar 2026) is right that MCP's value only materialises at multi-consumer scale; with one local consumer a REST endpoint wins. Owning the core means the MCP layer is a 50-line adapter, and you are never locked to the protocol.

This directly answers *"it does not have to be MCP"*: the **load-bearing artifact is the owned retrieval core + the chunk contract**; MCP is the recommended-but-swappable delivery surface.

## What is OFF by default — and the switch that turns it on

The strongest finding from [04](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/04-graph-agentic-rag.md): the impressive-sounding advanced techniques are **conditional opt-ins, not defaults.** Defaulting them in is the most common way these systems waste money and accuracy.

| Layer | Default | Switch-on condition (must be *measured*, not assumed) |
|---|---|---|
| **GraphRAG** | OFF | Corpus is entity-dense **AND** ≥15–20% of real queries are multi-hop/global **AND** you use a *lazy* variant (LazyGraphRAG / LightRAG) so index cost ≈ vector RAG. The paper *When to use Graphs in RAG* (arXiv 2506.05690) states graphs "frequently underperform vanilla RAG" on single-hop/factoid. |
| **Agentic retrieval loop** | Lives in the **caller**, not the tool | The consumer is already an agent — keep the tool "smart about retrieval, dumb about goals." Well-built non-agentic RAG matches agentic at ~3.3× lower token cost (Ferrazzi et al., 2026). |
| **Query transforms (HyDE, multi-query, decomposition)** | OFF, router-gated | HyDE is *actively harmful* on precise fact-bound lookups (query drift + 25–60% latency). Gate any transform behind a lightweight router on hard queries only. |
| **Late-interaction (ColBERT/ColPali)** | OFF | Only for visually-complex PDFs (ColPali) or when first-stage recall is the proven bottleneck; carries 6–10× index-size cost. |

The `multi_hop` ratio in the **gold Q/A set (S2b)** is exactly what decides the GraphRAG switch. This is why the eval set is built before the retrieval choices are frozen.

## Build, don't buy — with one exception

**Build the core thin and in-house.** Managed RAG-as-a-service (kapa.ai, Vectara, Glean, Ragie) hides precisely the levers that determine citation accuracy — chunking, embedding choice, hybrid weighting — which is unacceptable when answers must cite an exact instrument/section/version. ([05](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/05-infrastructure-buildvsbuy.md))

**The one exception:** for a specialised regulated vertical, *buy the embeddings, not the pipeline* — i.e. **strongly consider domain-tuned embeddings**. Harvey's `voyage-law-2` cut irrelevant results ~25% for legal; the same precedent transfers to AU banking (a `voyage-finance`-class or fine-tuned embedding). This is the highest-leverage place to spend money. ([06](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/06-proven-deployments-experts.md))

## Why this *is* the slot

The architecture is **domain-agnostic by construction**: the chunk contract (`{source_url, content}`) and the `retrieve(query)` interface are invariant; the corpus, the embedding choice, and the source registry are per-topic configuration. That is exactly the "slot, not instance" thesis of the parent entry ([../README.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/README.md)). AU banking is the first instance; its source strategy is in [00-source-map-au-banking.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/00-source-map-au-banking.md) — **federate the law, build-and-version the guidance.**

## The real SOTA lever is the eval loop, not the stack

The single most-repeated expert message (Hamel Husain across 30+ companies; kapa.ai across 100+ deployments; Jason Liu): **the teams that win obsess over a golden eval set built from their own domain queries — not MTEB, not the vendor's benchmark — and iterate against it.** Tool/store/framework choice "barely correlates with success."

This is why Phase 1's deliverable is the **eval harness + gold Q/A set**, and why no retrieval code is written until the harness can grade it. The architecture above is the *starting point* the eval loop then tunes; it is not the finish line. "SOTA" is only answerable against our own eval set.

## Rejected alternatives and their flip conditions

| Alternative | Rejected because | Would win if |
|---|---|---|
| Naive single-vector RAG | 5.7% top-20 failure floor; dominated by hybrid+rerank | never (strictly dominated) |
| Long-context replaces retrieval | Context Rot: more tokens ≠ better attention; cost prohibitive at corpus scale | corpus fits in-context AND recall needs are shallow |
| Managed RAG-as-a-service | Hides chunking/embedding/weighting levers; corpus leaves your control | you'd rather buy ingestion+permissions+citation and the accuracy bar is moderate |
| GraphRAG as default | Underperforms vanilla RAG on factoid/single-hop; heavy index cost | entity-dense corpus + ≥15–20% multi-hop (use lazy variant) |
| Full agentic retrieval in the tool | ~3.3× token cost, agents don't iterate productively (53% identical re-retrievals) | the caller is *not* itself an agent |
| Plain REST instead of MCP | Loses multi-client reuse and the foundation-standard surface | exactly one known consumer forever, latency-critical |
| Heavy framework (LangChain etc.) | Net-negative; hides levers; winning teams avoid them | large team needing standardised abstractions over many pipelines |

## Honest uncertainties and anchor risks

Surfaced per the repo's anti-anchoring discipline — these are the assumptions that would flip the recommendation, and they are **not yet validated on our corpus**:

1. **Vendor-reported numbers.** Anthropic's 35/49/67% Contextual Retrieval lifts, Voyage's rerank deltas, and the Agentset reranker leaderboard are all vendor-published on vendor-chosen data with comparators we cannot independently exercise. Treat them as *directional ordering*, not portable magnitudes. The flip-condition is the **AU-regulation eval set** (S2b) — re-validate there before freezing any component.
2. **The entity-density assumption for the GraphRAG switch is asserted, not measured.** The gold set's `multi_hop` ratio resolves it.
3. **The FRL API's terms/SLA are undocumented** (see [00-source-map-au-banking.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/00-source-map-au-banking.md)) — a federation dependency to confirm with the Office of Parliamentary Counsel before production (S3 concern).
4. **2026 citations in the axis files** include several recent arXiv IDs the agents surfaced via web search; the *recommendation does not hinge on any single one* — it rests on the convergence across many independent sources plus the cloud-default signal.

---

**Bottom line for the phase:** the architecture is settled and low-regret. The remaining work is not "choose a stack" — it is "build the eval set that proves the stack on AU banking," then instantiate the thin owned core against it. Proceed to S2b (gold Q/A set), then S1 (build the slice).
