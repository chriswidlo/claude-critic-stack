# Memory, Retrieval, and Long-Context for AI Workflows — 2026 Canonical Reference

*Reference report, May 2026. Audience: any practitioner building production AI systems that need to remember, retrieve, or reason over more than a single prompt's worth of material. Stack-agnostic; current as of model releases through Q2 2026 (Opus 4.7, Gemini 2.5 Pro, GPT-5).*

---

## 1. The 2026 memory taxonomy

The word "memory" has fractured into six distinct technical primitives. Conflating them is the single most reliable way to ship a broken agent. The taxonomy below maps loosely onto cognitive psychology — but the *failure modes* are what make the distinction load-bearing.

### 1.1 Context-window memory

**What it is.** Ephemeral, per-turn. Tokens the model literally attends to during decoding.

**State of the art (May 2026).** Opus 4.7 ships a 1M-token window with a 90% prompt-cache discount on cached prefixes. Gemini 2.5 Pro ships 2M. GPT-5 advertises 1M but most production deployments treat ~400k as the practical ceiling for multi-needle workloads.

**Failure mode.** Attention degradation past the headline number. Single-needle retrieval at 1M is now ~89% (Opus 4.7 NIAH-style evals), but **multi-needle 8-needle retrieval drops to ~56% at the same depth**, and the U-shaped "lost in the middle" curve (Liu et al. 2023, TACL) still produces 5–15 point drops in the middle 30–70% of the window for tasks that require synthesizing across positions. The headline matters less than the effective context.

**Implementation note.** Treat context window as a *budget*, not a *bucket*. Filling it linearly increases per-turn cost (and the cache discount only applies to *stable prefixes*, which most multi-turn agents fail to maintain).

### 1.2 Working memory

**What it is.** Scratchpad state inside a single agent turn — chain-of-thought, extended thinking blocks, intermediate tool results.

**Implementations.** Anthropic's extended thinking blocks (with optional summary mode for token economics); OpenAI's reasoning summaries; agent scratchpads in LangGraph and CrewAI; the "thinking" budget tokens that Claude allocates before answer generation.

**Failure mode.** The model commits to a wrong intermediate (e.g., a hallucinated function signature in step 2 of a 5-step reasoning chain) and downstream steps inherit the error. Working memory is invisible to the user and unaccountable to the orchestrator unless explicitly inspected.

### 1.3 Episodic memory

**What it is.** Per-session state that persists across turns within a single session and dies with it.

**Implementations.** The conversation array; session-scoped KV stores; **file-as-memory** patterns (writing `requirement.md` in turn 2 and reading it in turn 7). The `.claude/session-artifacts/<id>/` directory in this repo is precisely episodic memory rendered as files.

**Failure mode.** Dies with the session unless explicitly promoted to long-term storage. Cheap and clean while alive. The orchestrator pattern of "write artifact → read artifact in next step" is now the recommended Anthropic pattern (cf. *Building Effective Agents*, Dec 2024).

### 1.4 Long-term memory

**What it is.** State persisting across sessions, days to months.

**Implementations.** ChatGPT memory (rolled out 2024, expanded 2025); Claude project memory (late 2025); Claude Code auto-memory (`memory/MEMORY.md` index + leaf files); Anthropic's memory tool for Managed Agents (Sept 2025); LangGraph `BaseStore`; Mem0; Letta archival memory.

**Failure mode.** Long-term memory fails by **lying**. There is no automatic invalidation primitive in any shipping product as of mid-2026 — stale facts persist until manually overwritten or contradicted by a write. The most common production bug: user changes job in March, but the agent keeps referring to their old role through August because no contradicting write occurred.

### 1.5 Procedural memory

**What it is.** "I learned how to do X." Stored as routines — code, playbooks, prompts, skill files — not as facts.

**Implementations.** Claude Code skills (`~/.claude/skills/`); Claude Code's slash-commands and CLAUDE.md instructions; OpenAI GPTs and Custom Actions; LangGraph subgraphs registered as named tools; agent SDK "playbooks."

**2026 trend.** Procedural memory is increasingly **written as code or markdown rather than embedded**. The agent needs to read and reason about the procedure (apply it deterministically), not retrieve fuzzy nearest-neighbors of it. Embedding-based skill retrieval was popular in 2023 and has largely been abandoned for first-class skill listings.

### 1.6 Semantic memory

**What it is.** Factual knowledge as embeddings + retrieval. The traditional RAG corpus.

**Implementations.** Vector store + chunked documents + reranker. Increasingly augmented with BM25 (hybrid search) and graph structures (GraphRAG).

**Failure mode.** Missing the right chunk. Retrieval quality is bounded by chunk boundaries and embedding-model recall, neither of which the agent can fix at query time without architectural support (query rewriting, iterative retrieval, fallback to web).

### 1.7 Why the taxonomy is load-bearing

The four ways memory fails:

- **Episodic** dies.
- **Long-term** lies.
- **Semantic** misses.
- **Procedural** drifts out of date.

A single "agent memory" abstraction that blurs these — the early-LangChain `ConversationBufferMemory` lineage — reliably produces systems that fail in all four ways at once and offer no architectural handle to debug *which*. The 2026 best practice: maintain at least four named substrates and choose deliberately per write.

---

## 2. Anthropic's memory primitives

Anthropic shipped four distinct memory primitives between 2024 and early 2026, each addressing a different layer.

### 2.1 The memory tool (Agent SDK, beta Sept 2025)

A client-side filesystem-backed scratchpad. The model issues tool calls (`view`, `create`, `str_replace`, `insert`, `delete`, `rename`) scoped to a `/memories` directory; the SDK executes them against whatever backend the client wires up (local disk, S3, encrypted blob, Postgres). Documented at [Memory tool — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).

The API surface is deliberately filesystem-shaped — Claude has been trained extensively on Bash, so it generalizes well from "edit a file" rather than from a bespoke memory grammar. The beta header is `context-management-2025-06-27`. The tool ships in API, Bedrock, and Vertex.

**Use for:** working memory that needs to survive **compaction** within a session; coordination state between sub-agents; structured notes a long-running agent rebuilds on every wake (the "ASSUME INTERRUPTION" pattern Anthropic recommends in the tool's auto-injected system instruction).

**Don't use for:** large corpora (no semantic retrieval — it's flat read); long-term user memory if you have no decay or invalidation strategy; anything requiring cross-tenant isolation without a hardened path-traversal guard (Anthropic explicitly warns: validate paths, reject `../`, watch for URL-encoded traversal).

### 2.2 Claude Code's auto-memory pattern

The pattern visible on most Claude Code installs: `memory/MEMORY.md` is an index, leaf files like `feedback_reframe_after_subagents.md` carry the actual facts, and the taxonomy is `{user_, feedback_, project_, reference_}`. `user_*` is durable facts about the user; `feedback_*` is corrections from past sessions; `project_*` is project-specific; `reference_*` is durable lookup content.

The genius: it's grep-able, version-control-friendly, human-auditable, and uses **no embeddings**. The cost: the model has to re-read the index every session and decide what's relevant — there is no semantic retrieval. Anthropic's bet (correct, in 2026): with 1M context, you can just put the whole index in the prompt and let attention do the routing.

The user-facing write primitive is the `# memorize` prefix (the user types `# I prefer X over Y` and Claude routes it to the right leaf file). This is the cheapest known UX for procedural-memory accumulation.

### 2.3 File-as-memory

Broader than auto-memory: any time an agent writes a file and a later turn (or session) reads it, that is memory. The claude-critic-stack uses this everywhere — `requirement.md`, `frame.md`, `distillations/`, `challenges.md`, `critiques.md`, `synthesis.md`, `ledger.md` are all episodic-memory primitives. The orchestrator explicitly reads them between steps rather than relying on the conversation transcript.

This is the canonical Anthropic recommendation (*Building Effective Agents*, Schluntz & Zaharia, Dec 2024): files as the memory substrate, not in-memory state. The reasoning: conversation transcripts are subject to compaction (lossy); files survive intact; files are grep-able and auditable; files compose with version control.

### 2.4 Conversation compaction

Claude Code ships `PreCompact` and `PostCompact` hooks. When the context window approaches its budget, the harness summarizes older turns and replaces them with the summary; `PreCompact` lets the project inject preservation material before summarization, and `PostCompact` lets it re-bootstrap state after.

This is the bridge between context-window memory and episodic memory. Without it, long sessions either OOM or silently lose early-turn context. The 2026 best practice: **keep important decisions on disk** (file-as-memory) and let compaction be lossy for the conversation transcript itself. The memory tool was designed in part to pair with compaction — the memory directory persists across compaction boundaries by construction.

### 2.5 Long context as an alternative to RAG

Opus 4.7 at 1M tokens fundamentally changes what counts as RAG. For corpora under ~500K tokens (roughly a 300-page book, or 200 typical markdown files), it is now defensible to put the whole corpus in the prompt with prompt caching to amortize cost across queries. Anthropic's prompt-caching discount (90% on cached prefixes) makes corpus-in-prompt economically competitive with vector search for read-heavy, low-write corpora. The `canon-librarian` agent in this stack bets on exactly this: it grep-loads canon entries into Claude's context rather than vector-retrieving them.

---

## 3. RAG patterns in 2026

The 2023 naive RAG pipeline (chunk by char count → embed with `ada-002` → cosine similarity → top-k → stuff into prompt) is the baseline to beat, not a target. Modern RAG has stratified into five patterns.

### 3.1 Advanced RAG

**Chunking.** Semantic chunking (sentence transformers detect topic boundaries); recursive chunking that respects markdown/code structure; **parent-document retrieval** (the chunk is the search unit, but the parent document is what's returned to the model — recovers context the embedding lost). The 500-token-with-50-overlap default is now an anti-pattern for any corpus where chunk boundaries cut across logical units.

**Query rewriting.** HyDE (Hypothetical Document Embeddings, Gao et al. 2022) generates a fake answer and embeds *that* — closer to the corpus's distribution than the question. Multi-query expansion generates N paraphrases and unions retrieval. Step-back prompting generalizes the query before retrieval ("What kind of question is this?") and reduces over-specific matches.

**Hybrid search.** BM25 + dense via Reciprocal Rank Fusion. BM25 catches the exact-token cases dense embeddings miss — codenames, error strings, function names, SKU numbers, regulatory citations. **Production rule of thumb**: if your corpus contains any literal identifiers, you need BM25.

**Reranking.** Slower, more accurate model picks the top-K from the top-N candidates. Single highest-ROI addition to any RAG system as of 2026. See §6.

### 3.2 The "RAG is dead" debate (2024–2026)

Started in earnest when Gemini 1.5 shipped 1M context (Feb 2024) and Google's research team published "RAG vs Long Context" results showing long context winning on most QA benchmarks. The 2026 consensus, after 18 more months of evidence: **both, with the dividing line at corpus size and cost.**

Long context wins when:
- Corpus < ~500K tokens.
- Queries are diverse (per-query retrieval cost dominates).
- Freshness matters per-turn (no time to re-index).
- The corpus benefits from cross-document attention (synthesis questions).

RAG wins when:
- Corpus > 1M tokens (doesn't fit, period).
- Cost-per-query matters more than recall ceiling.
- **Citation provenance is required** (compliance, regulated industries).
- The corpus updates faster than prompt caches can amortize.
- Multi-tenant isolation is a requirement.

The Anthropic Contextual Retrieval post (Sept 2024) split the difference: small corpora → context + caching; large corpora → contextual chunking + hybrid retrieval. That pattern remains the strongest single recommendation in mid-2026.

### 3.3 GraphRAG (Microsoft, Edge et al. 2024)

Builds a knowledge graph from the corpus at index time using an LLM, then retrieves **subgraphs** rather than chunks. The Leiden community-detection algorithm is run hierarchically — level 0 detects fine-grained communities, level 1 aggregates them into super-communities, and so on until partitioning stops improving structure. Each community gets an LLM-generated summary.

Two query modes:
- **Local search** answers entity-specific questions by traversing nearby graph neighborhoods.
- **Global search** answers corpus-wide "sensemaking" questions ("what are the main themes?") by map-reducing across community summaries.

Reported improvement: 50–70% better comprehensiveness on global questions vs. naive RAG, on corpora in the 1M-token range. Expensive to build (LLM calls per entity at index time) and the graph-staleness problem is unsolved — incremental graph updates are an active research area. Open-sourced as [microsoft/graphrag](https://github.com/microsoft/graphrag).

### 3.4 Self-RAG (Asai et al. 2023)

The model emits special reflection tokens — `[Retrieve]`, `[No Retrieve]`, `[Relevant]`, `[Irrelevant]`, `[Supported]`, `[Useful]` — that gate retrieval and self-critique. Effectively turns retrieval from a pre-pass into a model decision exercised during generation. Trained via supervised fine-tuning on traces that include the tokens. Outperforms ChatGPT and retrieval-augmented Llama2-chat on open-domain QA, reasoning, fact verification, and long-form generation in the original eval.

### 3.5 Corrective RAG / CRAG (Yan et al. 2024)

A lightweight retrieval evaluator classifies retrieved documents into three confidence buckets — correct, incorrect, ambiguous. **Correct** docs are passed through a decompose-recompose step that filters them to only the relevant strips. **Incorrect** triggers a fallback to web search. **Ambiguous** combines both. Plug-and-play with existing RAG stacks; the pattern is now baked into LangGraph templates and LlamaIndex's `CorrectiveRAGPack`.

### 3.6 Agent-native RAG (the 2025–2026 architectural shift)

The most consequential change: retrieval is no longer a pre-pass that runs before the LLM sees the question. It is a **tool the agent calls**, often multiple times, with refined queries. Cursor's codebase search, Claude Code's `Grep` + `Read` combo, Devin's repo navigation, and the `canon-librarian` agent in this stack all share this shape: the agent reasons about what to retrieve, retrieves, reads, and decides whether to retrieve again.

The pre-pass RAG architecture is now considered a special case (single-shot retrieval at turn 0). See *Building Effective Agents* (Dec 2024) and the agentic-search literature (Search-o1, Li et al. 2025) for the canonical framing.

---

## 4. Vector store landscape (2026)

Vector-store choice is dominated more by **where the data already lives** than by raw retrieval performance. Latency and recall differences between the top five products are within the noise of chunking and reranking choices.

### 4.1 Managed / hosted

**Pinecone.** Serverless tier scales to zero; the default greenfield choice when ops headcount is the binding constraint. ~$70/mo at 10M vectors, but the cost gap widens sharply past 100M (~$700/mo) where self-hosted alternatives flatten.

**Weaviate.** Hybrid search champion — native BM25 + dense + metadata filtering in a single query, GraphQL surface. Strongest single product if you need both modalities without orchestrating two systems.

**Qdrant.** Rust-native, exceptional filtering and payload performance, p50 latency ~8ms in independent 2026 benchmarks (vs Pinecone ~20ms, Weaviate ~15ms, Milvus ~12ms). Best self-hosted-or-cloud option for filter-heavy workloads.

**Milvus.** Designed for 10B+ vector scale, strong GPU support, enterprise feature set. Operational complexity exceeds the others; choose when you genuinely have billion-scale vectors and a platform team.

### 4.2 Embedded

**Chroma.** Developer-experience leader. The simplest API, ideal for prototypes. Production-ready on a single 4–8GB VPS up to ~few million records; community guidance in 2026 is to plan a migration path to Qdrant or pgvector when filtering grows complex or scale crosses ~10M.

**LanceDB.** Apache-Arrow-based, columnar, near in-memory performance from disk, exceptional multimodal support (text + image + video in one store). Mindshare growth from 6.7% to 9.6% YoY in 2026 is the steepest in the category — serverless and multimodal architectures are pulling it forward.

**FAISS.** In-process benchmark; Meta's reference implementation. Not a database — a library. Use as the embedded engine inside something else, or for benchmarking other stores.

### 4.3 Co-located (vectors live next to operational data)

**pgvector.** The default for any team already on Postgres. **0.8.0 (Oct 2024)** added iterative index scans for HNSW — the long-standing "overfiltering" problem (where a tight `WHERE` clause leaves the index unable to return enough candidates) is now solved via `hnsw.iterative_scan` (`strict_order` or `relaxed_order` modes) and a `hnsw.max_scan_tuples` budget. With iterative scans on, pgvector is competitive with dedicated vector DBs for most production workloads up to ~50M vectors.

**sqlite-vec.** Edge / desktop / single-tenant deployments. Surprisingly capable for its weight class.

**DuckDB vss extension.** Analytical workloads where vector search is one column of a larger query — the columnar engine matters more than the vector index.

### 4.4 Selection criteria (ranked by 2026 leverage)

1. **Where the data already lives.** Postgres team → pgvector. Snowflake/Databricks → native vector functions. Greenfield → managed.
2. **Hybrid search need.** If yes → Weaviate, Qdrant, or pgvector + tsvector.
3. **Scale.** <10M vectors: any. 10M–1B: Qdrant, Milvus, Pinecone, pgvector with tuning. >1B: Milvus or sharded Pinecone.
4. **Filtering complexity.** Qdrant if filters dominate; pgvector if filters are SQL-shaped.
5. **Deployment surface.** Edge → sqlite-vec/LanceDB. Cloud-only → managed. Self-hosted → Qdrant/Milvus.

---

## 5. Embedding models 2026

### 5.1 Voyage AI (Anthropic-recommended, acquired 2025)

- **voyage-3-large** — top MTEB at 65.1 (Jan 2025 release), state-of-the-art across 8 domains (law, finance, code, technical, web reviews, multilingual, long-context, conversation). Outperforms OpenAI text-embedding-3-large by ~9.74% average, Cohere embed-v3 by ~20.71%. Matryoshka-trained: supports 2048/1024/512/256-dim truncation. Quantization-aware: int8 at 1024 dim is only 0.31% below float at 2048 dim, with 8× storage reduction. **Binary at 512 dim outperforms OpenAI float at 3072 dim by 1.16% with 200× less storage.** 32K context.
- **voyage-3** — smaller default, strong general-purpose.
- **voyage-code-3** — code-specialized; strongest single embedding model for code search in mid-2026.
- **voyage-finance-2**, **voyage-law-2** — domain-specialized.
- **voyage-multimodal-3** — text + image joint embedding.
- **voyage-rerank-2.5** — cross-encoder reranker. Recommended pairing with voyage embeddings for any production stack.

First 200M tokens are free.

### 5.2 OpenAI

- **text-embedding-3-small** / **text-embedding-3-large** (Jan 2024, still current in May 2026). Matryoshka-truncatable. text-embedding-3-large at full 3072 dim is competitive but no longer SOTA; small is the default cost-leader for non-specialized retrieval.

### 5.3 Cohere

- **embed-v3** family (English, multilingual, light variants). Strong enterprise distribution, particularly inside Bedrock and the Cohere managed RAG product.
- **Cohere Rerank 3** — long-standing reranker default; still competitive, particularly in multilingual scenarios.

### 5.4 Open weights

- **BGE-M3** (BAAI) — strong multilingual, multi-function (dense + sparse + multi-vector from one model).
- **E5** family (Microsoft) — solid open default.
- **nomic-embed-text-v1.5** — open weights *and* open training data; the cleanest provenance story among open models.

### 5.5 Specialized

- **Code:** voyage-code-3, jina-embeddings-v2-code, nomic-embed-code.
- **Multimodal:** voyage-multimodal-3, jina-clip-v2, Cohere embed-v4 (preview).
- **Long-context:** jina-embeddings-v3 (8192 tokens), voyage-3-large (32K).

---

## 6. Chunking and retrieval patterns

### 6.1 Chunking

Default of 500 tokens with 50 overlap is now a documented anti-pattern for any corpus with structure. Modern options:

- **Semantic chunking** — embed sentence-by-sentence, cut at embedding-space discontinuities.
- **Recursive chunking** — respect document structure (markdown headers, code blocks, paragraph boundaries).
- **Parent-document retrieval** — embed small (sentence-level) chunks for retrieval precision, return the parent paragraph or section for generation context.
- **Contextual retrieval (Anthropic, Sept 2024)** — the strongest single chunking improvement of the past two years. An LLM generates a 50–100-token chunk-specific prefix that situates the chunk in the document; the prefix is prepended before both embedding and BM25 indexing.

### 6.2 Contextual retrieval — the numbers

From the [Anthropic Contextual Retrieval post](https://www.anthropic.com/news/contextual-retrieval):

| Configuration | Top-20 retrieval failure rate | Reduction |
|---|---|---|
| Baseline (chunks alone) | 5.7% | — |
| Contextual Embeddings | 3.7% | 35% |
| Contextual Embeddings + Contextual BM25 | 2.9% | **49%** |
| + Reranking | 1.9% | **67%** |

The hybrid combines via **Reciprocal Rank Fusion**, default 80% semantic / 20% BM25, tunable per corpus. The one-time contextualization cost is ~$1.02 per million document tokens with prompt caching (cache hits the document once, generates prefixes for each chunk).

### 6.3 Hybrid search

BM25 + dense + RRF. Catches the exact-string cases embeddings systematically miss — error codes, function names, regulatory citations, product SKUs. The 80/20 RRF weighting is a defensible default; tune toward BM25 for high-jargon corpora (legal, finance, code), toward dense for natural-language corpora.

### 6.4 Reranking — the highest-ROI single addition

A slower, more accurate cross-encoder model rescores the top-N candidates from initial retrieval and picks top-K. Typical configuration: retrieve top-150 with fast hybrid, rerank to top-20.

| Reranker | Notes |
|---|---|
| **Voyage Rerank 2.5** | Current top recommendation for Anthropic stacks; pairs cleanly with voyage embeddings. |
| **Cohere Rerank 3** | Long-standing default; strong multilingual; available in Bedrock. |
| **ColBERTv2** | Late-interaction architecture; open weights. PLAID-optimized inference is 7× faster on GPU, 45× on CPU vs vanilla. Jina ColBERT v2 adds multilingual + compact embeddings. Sub-60ms total query+rerank latency on ModernBERT+ColBERTv2 in production benchmarks. |

Reranking is the single highest-leverage addition to a baseline RAG stack — typically 2–4× recall@5 improvement for one extra model call.

### 6.5 Query rewriting

- **HyDE** — generate a hypothetical answer, embed it, retrieve against that.
- **Multi-query** — generate N paraphrases, union retrieval.
- **Step-back prompting** — generalize the query before retrieval ("what kind of question is this?").

Cheap to add (one LLM call), substantial recall improvement on under-specified queries.

### 6.6 Citation tracking

Provenance is no longer optional in 2026 — compliance, audit, and user-trust requirements all demand it. Every retrieved span should carry the tuple:

```
(doc_id, chunk_id, char_offset_start, char_offset_end,
 retrieval_score, rerank_score, indexed_at_version)
```

Surfacing this in the generated answer (inline citations, footnote-style references) is now a baseline UX expectation, not a feature.

---

## 7. Long-context patterns at 1M tokens

### 7.1 Headline vs effective context

Headline (Opus 4.7: 1M; Gemini 2.5 Pro: 2M) is what the model accepts. Effective context — the range over which performance degrades minimally — is closer to 200–400K for multi-needle tasks. Independent NIAH-style benchmarks at 1M typically report ~89% single-needle retrieval and ~56% on 8-needle variants. The NoLiMa benchmark (Modarressi et al. 2025) makes the gap explicit: when needles must match by meaning rather than literal string, scores collapse far below NIAH numbers across all current frontier models.

### 7.2 Lost in the middle

The U-shaped curve from Liu et al. (2023, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)) is still operative. Information at the **start or end** of a long context is retrieved with high fidelity; information in the **middle 30–70%** is retrieved with 5–15 point lower accuracy. Architectural fixes (position interpolation, sliding-window attention, ring attention) have shifted the curve down but not eliminated it.

**Operational implication.** When packing long contexts deliberately, put the most retrieval-critical material at the head or tail. The middle is for support that does not need to be precisely re-surfaced.

### 7.3 Hierarchical summarization for >300K corpora

When corpora exceed ~300K tokens, the dominant pattern is hierarchical summarization: chunk the corpus, summarize each chunk, summarize the summaries. The model sees the summary tree; the agent drills into raw chunks on demand via a `get_full_chunk(id)` tool. GraphRAG community summaries are a specific instance of this pattern over a graph topology.

### 7.4 "1M context does not replace RAG" — the 2026 consensus

The hopeful 2024 framing ("just put everything in context") collapsed under three forces: per-query token cost; middle-of-context degradation; the requirement for citation provenance. The mature 2026 position: long context **changes the boundary** between RAG and in-prompt, raising the corpus-size threshold above which RAG is mandatory from ~50K (2023) to ~500K (2026). It does not eliminate RAG.

---

## 8. Agent memory frameworks

### 8.1 MemGPT / Letta (Packer et al. 2023)

Virtual-memory hierarchy inspired by operating systems. **Core memory** stays in context (analogous to RAM); **archival memory** lives in a vector store (analogous to disk); **recall memory** indexes raw conversation history. The agent issues OS-style paging calls to move data between tiers. The original paper introduced two evaluation domains: document analysis beyond context limits, and multi-session chat with long-term consistency. Open-sourced as [letta-ai/letta](https://github.com/letta-ai/letta); MemGPT rebranded to Letta in Sept 2024 as the project expanded from a research prototype into a platform for stateful agents.

### 8.2 Mem0 (Chhikara et al. 2025, [arXiv:2504.19413](https://arxiv.org/abs/2504.19413))

Two-stage architecture. **Phase 1**: process each user-assistant message pair plus a summary of recent context; an LLM extracts salient facts. **Phase 2**: each candidate fact is compared against the top-10 most-similar existing memories; the LLM decides whether to add, update, delete, or ignore. A scoring layer evaluates importance via relevance + recency. Reported results: 26% improvement on LLM-as-judge over OpenAI's memory; 91% lower p95 latency; >90% token-cost savings vs full-context approaches. Graph-memory variant adds ~2% on top. ~25K GitHub stars as of mid-2026.

### 8.3 LangGraph memory primitives

Two layers:

- **Short-term:** thread-scoped `State`, persisted by checkpointers attached at compile time. After every node runs, the checkpointer writes the current state; on `invoke()` with the same thread ID, LangGraph reads the latest snapshot.
- **Long-term:** `BaseStore` — a key-value store with namespaces (tuples of strings) and arbitrary-dict values. Survives across threads. `store.put()` / `store.search()` are the read/write primitives.

The split maps cleanly onto the episodic/long-term distinction in §1. Checkpointers handle conversation continuity within a session; stores handle persistent knowledge across sessions.

### 8.4 LangChain memory classes

The original `ConversationBufferMemory`, `ConversationSummaryMemory`, and siblings are now mostly **deprecated**. The LangChain team's own guidance in 2025 was to migrate to LangGraph for any non-trivial memory needs.

### 8.5 Cline's "memory bank"

A folder of structured markdown files — `projectbrief.md`, `productContext.md`, `activeContext.md`, `progress.md`. The agent re-reads them at the start of every session. Pure file-as-memory; no embeddings, no database. Popular precisely because it composes with git and is debuggable by eyeball.

### 8.6 Write-back to project memory on insight

Claude Code's `# memorize` prefix is the canonical user-facing affordance: when the user types `# I prefer Y`, the agent routes the fact to the appropriate leaf file in project memory. The pattern generalizes: any write-back surface that converts in-session insight into durable memory raises the ceiling on long-running collaboration.

---

## 9. Anti-patterns

1. **"RAG everything."** When the corpus contains heavy boilerplate (legal disclaimers, repeated headers, license blocks), retrieval drowns in irrelevant high-similarity matches. Filter at index time or use BM25 to break ties.
2. **Re-embedding the entire corpus on every change.** Use content-addressed chunk IDs (hash of normalized chunk content); re-embed only changed hashes. Critical for any corpus where ingestion is not a one-shot batch.
3. **Storing chunks without provenance.** Without `(doc_id, chunk_id, offsets, version)` you cannot debug retrieval failures, cannot audit, and cannot delete per-user data on request. Bake provenance in at schema-design time.
4. **Memory without recency or decay.** Long-term memory that never expires drifts into lies (cf. §1.4). Build invalidation in — either explicit TTLs, contradiction-driven overwrites (Mem0's update/delete decisions), or recency-weighted retrieval scoring.
5. **Treating long context as a panacea.** Middle-of-haystack still degrades. Always benchmark on multi-needle and meaning-match (NoLiMa-style) evals, not just classical NIAH.
6. **Reading raw retrieval into the orchestrator instead of distilled summaries.** Re-anchors the orchestrator on whatever phrasing the retrieval returned. Distill before reading (the claude-critic-stack pattern with `subagent-distiller`).
7. **One memory namespace per tenant in a shared vector store.** Cross-tenant leakage via shared embeddings is a real failure mode (private substrings of one tenant nearest-neighbor to another's query). Use per-tenant indexes or hardened metadata filters.
8. **Optimizing embedding model before adding a reranker.** A reranker on a mediocre embedding model beats a SOTA embedding model with no reranker on most benchmarks. Add the reranker first; tune embeddings second.

---

## 10. Top 12 memory/RAG/long-context practices — ranked by leverage

1. **Pick the right memory layer per write.** The four-failure-mode framing (§1.7) is the single biggest lever. Most production bugs trace to a write going into the wrong substrate.
2. **Add a reranker before tuning anything else in RAG.** Highest single ROI; Voyage Rerank 2.5 or Cohere Rerank 3 are defensible defaults.
3. **Hybrid search (BM25 + dense + RRF) before any clever retrieval architecture.** Solves the literal-identifier problem cheaply. Skip at your peril if the corpus has codenames, errors, or SKUs.
4. **Contextual retrieval (LLM-prefixed chunks) for any corpus where chunks lose meaning out of context.** 49% retrieval-failure reduction is the published number; consistent with reproductions through 2026.
5. **File-as-memory over in-memory state for any agent that runs longer than one turn.** Survives crashes, compaction, sub-agent boundaries. Composes with git.
6. **Provenance tuples on every retrieved span.** `(doc_id, chunk_id, offsets, scores, version)`. Bake in at schema time, not retrofit.
7. **Content-addressed chunk IDs.** Re-embed only what changed. Required at any non-trivial corpus size with non-batch ingestion.
8. **Cache the canon-style prefix when the corpus fits.** Prompt caching at 90% discount makes corpus-in-prompt economical for read-heavy <500K-token corpora.
9. **Plan for memory invalidation from day one.** Either TTLs, contradiction-driven overwrites (Mem0 pattern), or recency-weighted scoring. Without it, long-term memory degrades silently.
10. **Use the memory tool (or equivalent file scratchpad) to survive compaction.** Critical for any session that approaches the context window's budget.
11. **Benchmark retrieval on your own corpus, not on MTEB.** MTEB is a useful prior; in-domain recall@5 with rerankers is the actual decision input. Build an internal eval set of 50–200 question/answer pairs from real queries.
12. **Distill retrieval results before passing to the orchestrator.** Prevents anchoring on retrieval phrasing; produces a written artifact for audit; replaces the brittle "model summarizes verbally" pattern.

---

## 11. References

- Anthropic. ["Introducing Contextual Retrieval"](https://www.anthropic.com/news/contextual-retrieval), Sept 2024.
- Anthropic. ["Memory tool" docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool), Sept 2025.
- Anthropic / Schluntz & Zaharia. ["Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents), Dec 2024.
- Packer et al. ["MemGPT: Towards LLMs as Operating Systems"](https://arxiv.org/abs/2310.08560), 2023.
- Chhikara et al. ["Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"](https://arxiv.org/abs/2504.19413), 2025.
- Edge et al. ["From Local to Global: A GraphRAG Approach to Query-Focused Summarization"](https://arxiv.org/abs/2404.16130), 2024.
- Asai et al. ["Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"](https://arxiv.org/abs/2310.11511), 2023.
- Yan et al. ["Corrective Retrieval Augmented Generation"](https://arxiv.org/abs/2401.15884), 2024.
- Liu et al. ["Lost in the Middle: How Language Models Use Long Contexts"](https://arxiv.org/abs/2307.03172), TACL 2023.
- Santhanam et al. ["ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction"](https://arxiv.org/abs/2112.01488), 2022.
- Voyage AI. ["voyage-3-large: state-of-the-art general-purpose embedding"](https://blog.voyageai.com/2025/01/07/voyage-3-large/), Jan 2025.
- Modarressi et al. ["NoLiMa: Long-Context Evaluation Beyond Literal Matching"](https://arxiv.org/html/2502.05167v2), ICML 2025.
- [microsoft/graphrag](https://github.com/microsoft/graphrag), [letta-ai/letta](https://github.com/letta-ai/letta), [mem0ai/mem0](https://github.com/mem0ai/mem0), [pgvector 0.8.0 release notes](https://www.postgresql.org/about/news/pgvector-080-released-2952/).
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard), continuously updated.
