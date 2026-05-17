# Outside-View Forecast — raw return

## 1. Reference class

**Most informative class:** Enterprise vertical-domain RAG/retrieval systems built for agentic consumption in regulated, high-churn document corpora (legal, financial regulation, healthcare guidelines, tax). Pathologies shared: (a) authoritative source-of-truth requirement with citation; (b) frequent amendments / supersession (high churn); (c) heavy tabular / numeric / cross-referenced structure that defeats naive chunking.

**Adjacent classes:**
- Vertical foundation-model knowledge plays (BloombergGPT, Harvey, Casetext CoCounsel) — triangulates "build vs. retrieve." Custom-trained domain LLMs have underperformed RAG-on-frontier-models since GPT-4.
- Agentic tool/MCP retrieval surfaces (2024–2026 wave). Triangulates "is the surface RAG or a tool catalog." Tool retrieval emerged as a distinct problem in late 2025 once internal MCP servers exceeded ~hundreds of tools.
- Internal enterprise search / KM portals (pre-LLM, 2005–2020). Triangulates organizational failure: most internal KBs went stale and unused regardless of search quality.

Vertical-RAG is most predictive of *technical* outcome; KM-portal is most predictive of *organizational* outcome (will agents use it).

## 2. Base rate

No clean published rate. Indicative data:
- "Simple RAG rarely survives production" — recurring 2025 finding (Faktion, Zeta Alpha, RAGFlow YE 2025).
- Anthropic Contextual Retrieval baseline failure rate **5.7%** for top-20 with naive embedding. Regulated/tabular content typically worse.
- Internal KM portals (pre-LLM): 60–80% declined into disuse within 18 months without dedicated curation team.
- Agentic RAG: **25–40% reduction in irrelevant retrievals** vs. naive RAG, but new failure modes (loops, over-retrieval).

**Working base rate (qualitative):** of comprehensive vertical-domain knowledge silos for agent consumption, ~**20–30% become load-bearing** within 12 months; **40–50% ship but become "shelfware silos"** (agents bypass, humans fall back to source); **20–30% abandoned** within 18 months.

## 3. Position relative to base rate

**Lifts probability of success:**
- Source-of-truth mapping is *known and finite* (e.g., APRA standards, ASIC instruments, specific Acts) rather than "all banking knowledge."
- Refresh pipeline tied to upstream regulator publication feeds is part of the design from day 1, not phase 2.
- Agent-side evaluation harness (BigLaw-Bench-style) precedes the silo build.
- Tabular/numeric content has structured ingestion path, not just text chunking.

**Drops probability:**
- Goal stated as "any needed information" — *unbounded scope is the strongest predictor of shelfware* in this class.
- No named agent task / consumption pattern.
- "Comprehensive" framing — comprehensiveness historically trades off against freshness in regulated domains. AU banking corpus alone (Acts, regs, APRA prudential, ASIC RGs, AUSTRAC, industry codes, court decisions, internal policy) is ~10⁵–10⁶ pages with multiple update cadences.
- No mention of regulator-feed contract or licensing path.

**Verdict:** at or slightly below base rate until consumption pattern and refresh path are named.

## 4. Dominant failure modes (ranked)

1. **Staleness / freshness paradox.** Regulated content amends faster than re-ingestion. Healthcare-RAG (2026): 12% of agent decisions used >24h-stale guidelines before real-time refresh added. AU banking has multiple cadences (APRA quarterly, ASIC ad-hoc, legislation parliamentary cycle, industry codes annual).
2. **Tabular / cross-referenced content defeats chunking.** Banking docs ~30–60% tables, capital ratios, schedules, defined-term webs. Naive chunking strips definitions from references; RAG returns confidently wrong numbers. Unsolved at general level (BM25→Corrective RAG benchmarks 2025).
3. **Agent doesn't use it.** Tool surface mismatch. Single `search_kb()` tool → keyword collapse, missed multi-hop queries. 50 fine-grained tools → tool-retrieval problem.
4. **Citation / source-attribution failure.** Regulated domain *requires* "this came from APRA APS 112 §27 v2024-07." RAG returns passages but not version-anchored citations. Kills compliance use cases at audit, not at demo.
5. **Scope explosion / "comprehensive" trap.** KB tries to cover everything → freshness drops → trust drops → agents fall back to direct source lookup. Classic KM death spiral.
6. **Build vs. buy mis-step.** BloombergGPT lesson: training/curating custom vertical model has been beaten by frontier-model + good retrieval since 2023.

## 5. SOTA architectural choices — empirically supported vs. buzzword-heavy

**Empirically supported (2024–2026):**

- **Hybrid retrieval (dense + BM25 with RRF).** 5–15% precision lift across domains. Cheap, near-mandatory baseline.
- **Anthropic-style Contextual Retrieval.** 35% failure-rate reduction from contextual embeddings; 49% with contextual BM25; **67% with reranking added** (5.7% → 1.9%). Strongest single intervention with public numbers. Cost: one Claude call per chunk at index time, mitigated by prompt caching.
- **Cross-encoder or ColBERT/late-interaction reranking.** Reliable lift on top-k. ColBERTv2/Jina-ColBERT-v2 production-feasible (memory-mapped, ~90% RAM reduction). Late interaction notably helps on technical/legal vocabulary (exact-term matching matters).
- **Structured ingestion with explicit metadata** (jurisdiction, instrument, section, version, effective-date). Underrated. Most accuracy gains in regulated domains come from being able to *filter* before semantic search, not from better embeddings.
- **Hierarchical / community indexing for regulated corpora.** Top-level (regulator) → mid-level (instrument) → leaf (clause) routing. 15–30% precision improvement reported in financial-services deployments.
- **Evaluation harness first.** Harvey's BigLaw-Bench, healthcare freshness monitoring — teams that built domain evals before the silo outperformed those that built the silo first.

**Buzzword-heavy / mixed evidence:**

- **GraphRAG.** Strong on multi-hop / "comprehensiveness" benchmarks (72–83%, 3.4× accuracy in some cases, FalkorDB 90%+ on schema-heavy queries). *But*: graph construction cost is high, schemas drift, factoid queries underperform hybrid. June 2025 paper "When to use Graphs in RAG" argues against blanket adoption. Useful for *known* multi-hop patterns (regulator → instrument → clause → defined term), not as default.
- **Agentic RAG.** Real gains (25–40% irrelevant-retrieval reduction) but introduces loops, latency, cost. Net positive *only with* confidence calibration and budget caps.
- **Long-context-as-RAG-replacement (1M tokens).** Largely debunked for production by mid-2026. Gemini 1.5 Pro: 99.7% single-needle, ~60% on multi-fact recall. Claude Opus 4.6 MRCR v2: 78.3% at 1M. ~$15/query, 20–30s TTFT. Good for whole-document reasoning over small set; *not* a substitute for banking-scale silo.
- **Custom domain LLM (BloombergGPT-style).** Underperforms frontier-model + RAG. Avoid.
- **MCP as retrieval primary.** MCP is the protocol layer; doesn't solve "which tool to call" (tool-retrieval problem). Useful for *action* surfaces, not retrieval architecture itself. Hybrid (RAG for grounding, MCP for action) is converging 2026 practice.

**Contradicting position:** *"The secret to scaling enterprise RAG is to stop optimizing retrieval"* (ragaboutit, 2025) — beyond a baseline, returns on retrieval-quality work diminish vs. work on consumption patterns, freshness, and evaluation.

## Outside-view verdict

**Below base rate** as currently scoped — primarily because of (a) "comprehensive / any needed information" framing — strongest single predictor of shelfware — and (b) absence of named refresh pipeline tied to regulator feeds and named consuming agent task.

**What would lift it to within tolerance:**
1. Replace "comprehensive" with a ranked list of agent tasks the silo must serve in month 1; cut everything else to phase 2.
2. Name refresh SLA per source class (APRA, ASIC, legislation, codes) before architecture.
3. Build the eval harness (gold Q/A with version-anchored citations) *before* the silo.
4. Default architecture: hybrid retrieval + Anthropic contextual retrieval + cross-encoder rerank + structured metadata filtering. Add GraphRAG only for specific multi-hop patterns proven in eval. MCP as action surface, not retrieval surface.

## Sources (currency, not promoted canon)

- Anthropic — Contextual Retrieval (2024)
- RAGFlow — From RAG to Context (2025 review)
- Zeta Alpha — Why GenAI Pilots Fail
- ragaboutit — RAG Freshness Paradox; Stop Optimizing Retrieval (2025)
- FalkorDB — GraphRAG vs Vector RAG benchmarks
- arXiv 2506.05690 — When to use Graphs in RAG (June 2025)
- arXiv 2507.03226 — Towards Practical GraphRAG
- tianpan.co — Long Context vs RAG (2026-04)
- tokenmix.ai — 1M Token Context Reality Check 2026
- Chroma — Context Rot
- Merge.dev — MCP vs RAG; testRigor — RAG vs Agentic RAG vs MCP
- Harvey — Enterprise-Grade RAG / BigLaw-Bench
- Sease — ColBERT in Practice 2025; Weaviate — Late Interaction overview
- Faktion — Common Failure Modes of RAG
- arXiv 2604.01733 — BM25 to Corrective RAG benchmark
