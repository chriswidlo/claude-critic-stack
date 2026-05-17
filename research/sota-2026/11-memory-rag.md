# Memory, Retrieval, RAG, and Agent State Management — 2026 Vintage

*Research report, May 2026. Scope: how production AI workflows in 2026 handle memory and retrieval; how the claude-critic-stack's `canon/corpus/` + librarian pattern fits the landscape; what to consider adopting.*

---

## 1. The 2026 taxonomy of "memory"

The word "memory" has fractured. In 2026 the working vocabulary in production systems looks roughly like the human cognitive-psychology borrow, but with each layer mapped to a different technical primitive. Conflating them is the most common source of broken agent designs.

**Context-window memory.** Ephemeral, per-turn. The model literally sees these tokens. With Opus 4.7 at 1M tokens, Gemini 2.5 Pro at 2M, and GPT-5 at ~400k effective, the context window has stopped being a binding constraint for most knowledge-work tasks and started being a *budget* constraint (prompt-caching economics, attention degradation past ~200k). Tradeoff: zero retrieval latency, full attention, but cost scales linearly per turn and recall on the "middle of the haystack" still degrades past 200k tokens despite the headline numbers (cf. NoLiMa, Hsieh et al. 2024, which showed needle-in-haystack metrics overstate practical recall).

**Working memory.** Within an agent turn. The scratchpad, intermediate tool results, the "thinking" block. Implementations: Anthropic's extended thinking blocks, OpenAI's reasoning summaries, agent scratchpads in LangGraph/CrewAI. Tradeoff: invisible to the user, but consumes context budget and can mislead subsequent steps if the model commits to a wrong intermediate.

**Episodic memory.** Per-session, persistent across turns. The current conversation's history, plus any session-scoped state. Implementations: the conversation array itself; session-scoped key-value stores; in this repo, the `.claude/session-artifacts/<id>/` directory is precisely episodic memory rendered as files. Tradeoff: dies with the session unless explicitly promoted; cheap and clean while alive.

**Long-term memory.** Across sessions, persistent for days to months. The "I talked to this user last Tuesday about their migration plan" capability. Implementations: ChatGPT's memory feature (rolled out 2024, expanded 2025), Claude's project-level memory (rolled out late 2025), the auto-memory pattern in Claude Code (`memory/MEMORY.md` + leaf files). Tradeoff: powerful when right, *actively harmful* when stale or wrong — there is no automatic invalidation primitive in any shipping product as of mid-2026.

**Procedural memory.** "I learned how to do X." Stored not as facts but as routines — code, playbooks, prompts, skill files. Implementations: Claude Code's `~/.claude/skills/`, OpenAI's GPTs/Custom Actions, LangGraph subgraphs registered as named tools. The 2026 trend: procedural memory is increasingly *written as code or markdown* rather than embedded, because the agent needs to read and reason about the procedure, not retrieve fuzzy nearest-neighbors of it.

**Semantic memory.** Factual knowledge stored as embeddings + retrieval. The traditional RAG corpus. Implementations: vector stores + chunked documents + reranker. Tradeoff: scales to arbitrary corpus sizes, but the retrieval quality is bounded by chunk boundaries and embedding model recall — both of which the agent cannot fix at query time.

The taxonomy matters because the failure modes are different. Episodic memory fails by dying. Long-term memory fails by lying. Semantic memory fails by missing. Procedural memory fails by being out of date. A single "agent memory" abstraction that blurs these (early LangChain `ConversationBufferMemory` and friends) reliably produces systems that fail in all four ways at once.

---

## 2. Anthropic's memory primitives

Anthropic shipped four distinct memory primitives between 2024 and early 2026, each addressing a different layer of the taxonomy.

**The memory tool (client-side scratchpad).** Announced as part of the Agent SDK in late 2025. The `memory` tool is a client-side filesystem-backed scratchpad — the model issues `memory.read` / `memory.write` / `memory.list` calls, the SDK persists them, and on the next turn the model can re-read what it wrote. Crucially, *the storage is opaque to Anthropic*; the SDK writes to wherever the client configures (local disk, S3, etc.). Use when: an agent needs working memory that survives compaction within a session, or coordination state between sub-agents. Don't use for: long-term user memory (no decay), or large corpora (no retrieval — it's flat read).

**Claude Code's auto-memory pattern.** The pattern the user has on disk right now: `memory/MEMORY.md` is an index, with leaf files like `feedback_reframe_after_subagents.md`. The taxonomy is `{user, feedback, project, reference}` — `user_*` is durable facts about the user, `feedback_*` is corrections from past sessions, `project_*` is project-specific, `reference_*` is durable lookup content. This is *long-term memory* rendered as a flat-file store with a written-by-the-model index. The genius: it's grep-able, version-control-friendly, human-auditable, and uses no embeddings. The cost: the model has to re-read the index every session and decide what's relevant — there is no semantic retrieval. Anthropic's bet (correct, in 2026): with 1M context, you can just put the whole index in the prompt.

**File-as-memory patterns.** Broader than the above: any time an agent writes a file and a later turn (or session) reads it, that's memory. The claude-critic-stack uses this everywhere — `requirement.md`, `frame.md`, `distillations/`, `challenges.md`, `critiques.md`, `synthesis.md`, `ledger.md` are all *episodic memory primitives*. The orchestrator explicitly reads them between steps rather than relying on the conversation. This is the *recommended* Anthropic pattern as of the 2025 "Building Effective Agents" post by Schluntz & Zaharia — files as the memory substrate, not in-memory state.

**Conversation compaction.** Claude Code ships `PreCompact` and `PostCompact` hooks. When the context window approaches its budget, the harness summarizes older turns and replaces them with the summary. The hooks let projects (a) inject extra material to preserve across compaction (`PreCompact`) and (b) re-bootstrap session state after compaction (`PostCompact`). This is the bridge between context-window memory and episodic memory: without it, long sessions either OOM or silently lose early-turn context. The 2026 best practice: keep important decisions on disk (file-as-memory) and let compaction be lossy for the conversation transcript itself.

**Long context as an alternative to RAG.** Opus 4.7 at 1M tokens fundamentally changes what counts as "RAG." For corpora under ~500k tokens (roughly: a 300-page book, or 200 typical markdown files), it is now defensible to just *put the whole corpus in the prompt*, with prompt-caching to amortize the cost across queries. Anthropic's prompt-caching docs (updated Feb 2026) show 90% discount on cached prefix tokens, which makes corpus-in-prompt economically competitive with vector search for read-heavy, low-write corpora. The `canon-librarian` agent in this stack is effectively betting on this — it grep-loads canon entries into Claude's context rather than vector-retrieving them.

---

## 3. RAG patterns in 2026

The 2023 "naive RAG" pipeline (chunk by character count → embed with `text-embedding-ada-002` → cosine similarity → top-k → stuff into prompt) is now considered a baseline to beat, not a target architecture. Modern RAG has stratified into several patterns.

**Advanced RAG.** Chunking gets smarter (semantic chunking with sentence transformers; recursive chunking that respects markdown structure; parent-document retrieval where the chunk is the search unit but the parent doc is what's returned). Queries get rewritten (HyDE — Hypothetical Document Embeddings, Gao et al. 2022 — generates a fake answer and embeds *that*; query expansion via LLM). Search is hybrid (BM25 + dense, with Reciprocal Rank Fusion). Results get reranked (Cohere Rerank 3, Voyage Rerank 2.5, ColBERTv2 late-interaction). Most production RAG systems in 2026 do all of these.

**The "RAG is dead" debate.** Started in earnest when Gemini 1.5 shipped 1M context (Feb 2024) and Google's research team published "RAG vs Long Context" results showing long context winning on most QA benchmarks. The 2026 consensus, after another 18 months of evidence: **both, with the dividing line at corpus size and cost**. Long context wins when: corpus < ~500k tokens, queries are diverse (so per-query retrieval cost dominates), freshness matters per-turn. RAG wins when: corpus > 1M tokens (still doesn't fit), cost-per-query matters more than recall ceiling, you need citation provenance, or the corpus updates faster than you can re-prompt-cache. Anthropic's own "Contextual Retrieval" blog post (Sept 2024) split the difference: small corpora → context + caching; large corpora → contextual chunking (where each chunk is prefixed with an LLM-generated summary of its place in the doc) + hybrid retrieval. That pattern is still the strongest single recommendation in mid-2026.

**Recent evolution.** Three named patterns dominate the 2025–2026 RAG literature:

- **GraphRAG** (Microsoft Research, Edge et al. 2024, open-sourced as `microsoft/graphrag`). Builds a knowledge graph from the corpus at index time using an LLM, then retrieves *subgraphs* rather than chunks. Strong on "global" questions ("what are the main themes of this corpus") that defeat similarity search. Expensive to build (LLM calls per entity), and the graph staleness problem is unsolved.
- **Self-RAG** (Asai et al. 2023, refined through 2025). The model emits special tokens (`[Retrieve]`, `[No Retrieve]`, `[Relevant]`, `[Irrelevant]`) that gate retrieval and self-critique. Effectively turns retrieval from a pre-pass into an agent decision.
- **Corrective RAG / CRAG** (Yan et al. 2024). After retrieval, a lightweight classifier evaluates whether the retrieved docs are sufficient; if not, falls back to web search or query rewriting. The pattern is now baked into LangGraph templates and LlamaIndex's `CorrectiveRAGPack`.

**Agent-native RAG.** The most important architectural shift of 2025–2026: retrieval is no longer a pre-pass that runs before the LLM sees the question. It is a *tool the agent calls*, often multiple times, with refined queries. Cursor's codebase search, Claude Code's `Grep` + `Read` combo, Devin's repo navigation, and the `canon-librarian` agent in this stack all share this shape. The agent reasons about what to retrieve, retrieves, reads, and decides whether to retrieve again. The pre-pass RAG architecture is now considered a special case (single-shot retrieval at turn 0). See Anthropic's "Building Effective Agents" (Dec 2024) and the agentic-search literature (Search-o1, Li et al. 2025) for the canonical framing.

---

## 4. Vector store landscape (2026)

The vector-store wars settled into three tiers.

**Managed/hosted.** Pinecone (still the default for greenfield production; serverless tier dropped per-query costs ~10x in 2024), Weaviate (strong hybrid search, GraphQL API, BYO embeddings), Qdrant (Rust core, strong on filtering/payload queries, increasingly popular for on-prem), Milvus (Zilliz Cloud; the scale leader, 10B+ vector deployments). Selection: Pinecone if you want zero-ops; Weaviate if hybrid search is core; Qdrant if you need rich metadata filtering; Milvus if you're past 100M vectors.

**Embedded.** Chroma (the dev-experience leader, Python-first; production story improved in 2025 with Chroma Cloud), LanceDB (columnar, multimodal-friendly, increasingly the choice for ML pipelines), FAISS (still the in-process benchmark; no persistence layer of its own). Selection: Chroma for prototypes and small production; LanceDB if you have multimodal needs or arrow/parquet pipelines.

**Co-located (vector lives in your existing DB).** `pgvector` is now the *default recommendation* for any team that already runs Postgres — the 0.7 release (2024) added HNSW, the 0.8 release (2025) added iterative scans, and at corpus sizes under ~10M vectors it is competitive with dedicated stores on latency while saving an entire piece of infrastructure. `sqlite-vec` (Asg017, released 2024) provides the same story for SQLite. DuckDB's `vss` extension (2024) added HNSW to the OLAP database, making "vector search joined to your analytics tables" a one-query operation.

**Selection criteria, ranked by what actually matters in 2026:**
1. **Where does your data already live?** If Postgres, use `pgvector`. The operational cost of a second database almost never pays back.
2. **Do you need hybrid (lexical + dense)?** If yes, Weaviate, Qdrant, or Postgres (`pgvector` + `pg_trgm`/`tsvector`).
3. **Scale.** Past ~100M vectors, dedicated systems (Milvus, Pinecone) win on tail latency.
4. **Filtering complexity.** Qdrant's payload filters are the strongest in the field.
5. **Deployment surface.** Embedded (Chroma, LanceDB, sqlite-vec) if you're shipping a desktop/CLI tool.

---

## 5. Embedding models 2026

The embedding-model field reorganized around three vendors and a strong open-source tier.

**Voyage AI.** Anthropic-recommended for Claude integrations (the Anthropic docs explicitly call out Voyage). `voyage-3` (general purpose, 1024 dims, strong cross-domain), `voyage-3-large` (the current top-of-MTEB-leaderboard model as of early 2026), `voyage-code-3` (code-specialized, dominant on CodeSearchNet benchmarks), `voyage-finance-2`, `voyage-law-2` (domain-tuned). Voyage's Rerank 2.5 is also state-of-the-art on reranking benchmarks. Anthropic acquired Voyage AI in early 2025, which sharpened the recommendation.

**OpenAI.** `text-embedding-3-small` and `text-embedding-3-large` (Jan 2024, still current — OpenAI has not shipped a v4). Strong general-purpose, Matryoshka-truncatable to lower dimensions for storage savings. The default for OpenAI-stack teams.

**Cohere.** `embed-v3` (English, multilingual, and a `light` variant). Strong on enterprise search, paired with Cohere Rerank 3. Particularly good multilingual coverage.

**Open-source.** BGE (BAAI General Embedding, M3 release adds multi-vector + sparse), E5 (Microsoft, mistral-7b-instruct backbone for the large variants — surprisingly strong), `nomic-embed-text-v1.5` (open weights *and* open training data, Matryoshka). For teams that need on-prem or want to avoid per-query embedding costs, the open tier closed most of the quality gap with closed models in 2024–2025.

**Specialized.** Code: `voyage-code-3`, `jina-embeddings-v2-code`, `nomic-embed-code`. Multimodal: `voyage-multimodal-3`, `jina-clip-v2`. Long-context: `jina-embeddings-v3` (8192 tokens).

The 2026 rule of thumb: start with `voyage-3` if you're on Anthropic, `text-embedding-3-large` if you're on OpenAI, `BGE-M3` if you're on-prem. Re-evaluate only if you measure retrieval failures.

---

## 6. Chunking and retrieval patterns

**Chunking.** The 2023 default (500-token chunks with 50-token overlap) is now considered an anti-pattern for anything non-trivial. Current practice:

- **Semantic chunking** (Greg Kamradt's notebook popularized it; LlamaIndex and LangChain both ship it) splits at semantic boundaries detected by sentence-embedding distance. Better recall, more variable chunk sizes.
- **Recursive chunking** (markdown-aware, code-aware) respects document structure. The default in most 2026 toolkits.
- **Parent-document retrieval** indexes small chunks for precision but returns the parent doc (or a wider window) for context. The most widely-deployed pattern in production.
- **Contextual retrieval** (Anthropic, Sept 2024): each chunk is prefixed with a 50–100 token LLM-generated summary of its place in the document. Anthropic reported a 49% reduction in retrieval failures when combined with rerank. Now the highest-leverage chunking intervention.

**Hybrid search.** BM25 (lexical) + dense (semantic) combined via Reciprocal Rank Fusion. Catches exact-term matches that embeddings miss (codenames, error strings, function names). Cheap to add, almost always improves recall.

**Re-ranking.** Run a slower, more accurate model on the top-50 retrieved chunks to pick the top-5. Cohere Rerank 3, Voyage Rerank 2.5, and ColBERTv2 (late-interaction, open) are the standard choices. Reranking is the single highest-ROI addition to a naive RAG pipeline.

**Query rewriting.** HyDE (hypothetical document embeddings), multi-query (generate N rewrites, search all, fuse), step-back prompting (generate a more general version of the question, search both). Cheap LLM calls that buy meaningful recall.

**Citation tracking.** Provenance is no longer optional. Production RAG pipelines in 2026 track `(doc_id, chunk_id, char_offset_start, char_offset_end, retrieval_score, rerank_score)` for every retrieved span, and surface them in the model's response as inline citations. Anthropic's Citations API (2024) and OpenAI's `file_search` annotations bake this in at the model level.

---

## 7. Agent memory patterns from production

**MemGPT / Letta** (Packer et al. 2023, now `letta-ai/letta`). Virtual-memory hierarchy: a small "core memory" always in context, a larger "archival memory" in a vector store, and OS-style paging between them. The model issues function calls (`memory_insert`, `memory_search`) that the runtime services. The most influential design of the 2023–2025 era; Letta (the company) productized it in 2024.

**Mem0** (`mem0ai/mem0`, ~25k stars by 2026). Open-source agent memory layer. Extracts facts from conversations, stores them with metadata (user, session, timestamp), retrieves on relevance + recency. Now ships first-class integrations with most agent frameworks.

**LangGraph memory primitives.** Three layers shipped through 2025: short-term (thread-scoped state, the graph's `State`), long-term (a `BaseStore` interface with implementations for in-memory, Postgres, Redis), and persistent checkpoints (resumable graph runs). This is the cleanest framework-level taxonomy in 2026.

**LangChain memory classes.** `ConversationBufferMemory`, `ConversationSummaryMemory`, `VectorStoreRetrieverMemory`, etc. — largely deprecated in favor of LangGraph's primitives. Historical interest only; if a 2026 design references these, it's outdated.

**Cline's "memory bank" pattern.** Cline (the VSCode coding agent) ships a `memory-bank/` convention: a folder of markdown files (`projectbrief.md`, `productContext.md`, `activeContext.md`, `progress.md`, etc.) that the agent reads at session start and writes to as the project evolves. Mirrors the Claude Code auto-memory pattern but project-local rather than user-global. Influential because it demonstrates that *the user maintaining the memory by hand* is a viable design — the model proposes edits, the user accepts.

**Write-back to project `CLAUDE.md` on insight.** Increasingly common pattern: at the end of a session, the agent proposes additions to `CLAUDE.md` capturing what it learned. Claude Code shipped this as the `# memorize` prefix in 2025 (`# this project uses ESM` adds a line to `CLAUDE.md`). The interaction model is *consent-gated edits to a human-maintained file*, not silent writes to an opaque store.

---

## 8. For this stack specifically

**`canon/corpus/` + `canon-librarian` as RAG.** The `canon/corpus/` directory is a curated knowledge corpus; `canon-librarian` retrieves from it via grep + read, with an explicit "must return at least one contradicting passage" rule that operationalizes the anti-confirmation discipline most RAG pipelines lack. Compared to industry best practice:

- *What you have that industry doesn't:* an anti-confirmation discipline baked into the retriever, not bolted on at synthesis time. This is genuinely novel — most production RAG systems will happily return five passages that all agree with the query because cosine similarity selects for that. Forcing one contradiction is structural friction against the same bias that the 12-step workflow's frame-challenger addresses.
- *What you lack:* semantic retrieval. Grep-based retrieval misses paraphrases — if the corpus says "eventual consistency" and the query asks about "BASE semantics", grep won't bridge that. For a corpus of the current size (small enough to fit in Opus 4.7's 1M context), this is fine: the librarian agent has the entire corpus index in its prompt and can reason about paraphrases. Past ~500 entries this breaks down.

**Should you add embeddings + vector search?** Not yet. The break-even point for adding a vector store to a grep-based corpus is roughly when the corpus index no longer fits in the librarian's prompt budget *or* when the contradiction-finding requirement starts failing because grep can't find paraphrased contradictions. Until then, embeddings add infrastructure and re-indexing cost without solving a real problem. When you cross the threshold, the right move is `sqlite-vec` co-located with the existing markdown files, BM25 + dense hybrid, and contextual retrieval (LLM-generated prefixes per entry).

**The auto-memory at the user's global Claude location.** The `{user, feedback, project, reference}` taxonomy + `MEMORY.md` index + leaf files is best-of-breed for long-term memory in 2026. It is grep-able, version-controllable, human-auditable, and decay-free *because the user can read and delete entries*. The only missing primitive is *recency/decay signaling* — there is no per-entry "last useful" timestamp, so stale memories aren't surfaced for review. Adding `last_referenced_at` to leaf-file frontmatter and an occasional review pass would close this.

**What memory primitive is missing that would help the 12-step workflow?** The strongest candidate: **cross-session episodic memory** — a way for session N to know what session N-1 decided without re-loading every artifact. Today, each session re-reads `canon/corpus/` from scratch and has no awareness of recent sessions' synthesis outputs. A `sessions-index.md` (auto-generated from `ledger.md` files) that summarizes the last 20 sessions' classifications, frames, and recommendations would let the orchestrator detect "this looks like the question we answered three weeks ago" and either reuse or deliberately diverge. This is the gap between *episodic* (per-session) and *long-term* (across-session) memory in the current design.

---

## 9. Anti-patterns

**RAG everything.** Indexing every document a team has ever written produces a corpus where the most-similar match to almost any query is some boilerplate template. Retrieval quality degrades sub-linearly with corpus size if you don't curate. The rule: *every doc in your RAG corpus should pay rent in retrievals*. If a doc has never been retrieved in a quarter of usage, evict it.

**Re-embedding the entire corpus on every change.** Common in early pipelines. The fix is *content-addressed chunk IDs* (hash of chunk text) so only changed chunks re-embed. Most modern frameworks support this; many homegrown pipelines don't.

**Storing chunks without provenance.** Chunks without `(source_doc, char_offset, retrieval_path)` cannot be cited, cannot be evicted when the source is updated, and cannot be audited when the model says something wrong. Provenance is not optional. The claude-critic-stack's habit of writing artifacts as markdown files with explicit cross-references (and the path-discipline rule that enforces repo-relative links) is the right model — every retrieved fact traces to a file.

**Memory without recency/decay.** Long-term memory that only grows poisons new sessions with stale facts. The fix is some combination of: TTL on memory entries, last-used-at timestamps with periodic review, explicit user-facing memory management ("review and delete stale memories"), and *generation-aware* memory (memory written by Claude 3.5 is flagged as such when retrieved into a Claude 4.7 session, because the older model's biases are baked in).

**Treating long context as a panacea.** Even at 1M tokens, attention degrades. The middle-of-haystack problem (Liu et al. 2023, "Lost in the Middle"; NoLiMa, Hsieh et al. 2024) is reduced but not eliminated. Putting a 900k-token corpus in context and expecting the model to find a fact buried at token 450k is unreliable. Long context is a *budget*, not a *solution*.

---

## 10. Synthesis: top 10 memory/RAG patterns to consider

1. **Contextual retrieval** (Anthropic, Sept 2024): LLM-generated chunk prefixes summarizing the chunk's place in its document. Highest single ROI on retrieval quality. *For this stack: applies if/when canon corpus grows past ~500 entries.*
2. **Hybrid BM25 + dense + rerank.** The 2026 production default. Reranking alone often doubles useful-precision-at-5.
3. **Agent-native retrieval as a tool, not a pre-pass.** Already the design in this stack via `canon-librarian`. Generalize: any future retrieval (web, code, prior sessions) should be a tool call by the orchestrator, not a pre-pass.
4. **Parent-document retrieval.** Index small, return large. Mitigates chunk-boundary failures.
5. **File-as-memory with consent-gated writes.** Every meaningful piece of state is a file. The model proposes edits; the user (or a verified workflow step) commits. This stack already does this; it is the right answer.
6. **Cross-session episodic index.** *New for this stack:* auto-generate a `sessions-index.md` from `ledger.md` files, so the orchestrator can detect repeat questions and consult prior syntheses.
7. **Anti-confirmation discipline in the retriever, not just the synthesizer.** The `canon-librarian`'s "must return one contradicting passage" rule is industry-leading; document it as a transferable pattern.
8. **Provenance for everything retrieved.** `(doc, char_range, retrieval_score)` on every span. The Citations API formalizes this; for file-as-memory systems, repo-relative markdown links serve the same purpose.
9. **Recency/decay metadata on long-term memory.** `last_referenced_at` + periodic review. Closes the staleness gap in the current auto-memory design.
10. **Prompt-cached corpus-in-context for small corpora.** With Opus 4.7 at 1M tokens and 90% cache discounts, corpora under ~500k tokens are economically competitive with vector search and qualitatively better (no chunking artifacts). The right baseline to beat before adding vector infrastructure.

---

## References

- Anthropic, "Building Effective Agents" (Schluntz & Zaharia, Dec 2024).
- Anthropic, "Introducing Contextual Retrieval" (Sept 2024). The 49% retrieval-failure-reduction result.
- Anthropic Prompt Caching docs (updated Feb 2026).
- Anthropic Citations API documentation.
- Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization," Microsoft Research, 2024. `microsoft/graphrag`.
- Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," 2023.
- Yan et al., "Corrective Retrieval Augmented Generation" (CRAG), 2024.
- Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE), 2022.
- Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," 2023.
- Hsieh et al., "NoLiMa: Long-Context Evaluation Beyond Literal Matching," 2024.
- Packer et al., "MemGPT: Towards LLMs as Operating Systems," 2023. `letta-ai/letta`.
- `mem0ai/mem0` (open-source agent memory).
- LangGraph documentation, memory primitives section (2025).
- Cline `memory-bank/` pattern documentation.
- Voyage AI model cards: `voyage-3`, `voyage-3-large`, `voyage-code-3`, Voyage Rerank 2.5.
- `pgvector` 0.8 release notes (2025); `asg017/sqlite-vec` (2024); DuckDB `vss` extension docs.
- MTEB leaderboard (HuggingFace), state as of early 2026.
- Li et al., "Search-o1: Agentic Search-Enhanced Large Reasoning Models," 2025.
