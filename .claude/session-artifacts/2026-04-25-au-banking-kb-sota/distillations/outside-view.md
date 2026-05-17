# Distillation — outside-view

## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on building a SOTA AU-banking knowledge silo for agent consumption. Subagent returned a vertical-RAG reference class, a qualitative base rate, six ranked failure modes, an empirically-vs-buzzword breakdown of SOTA architectural choices, and a "below base rate" verdict.

## Direct facts (numerical / empirical, with cited source)
1. [Anthropic Contextual Retrieval, 2024] Naive embedding baseline failure rate top-20 = **5.7%**. (direct)
2. [Anthropic Contextual Retrieval, 2024] Contextual embeddings cut failure 35%; contextual + BM25 cuts 49%; with reranking 67% (5.7% → 1.9%). (direct)
3. [Faktion / Zeta Alpha / RAGFlow YE 2025] "Simple RAG rarely survives production" — recurring 2025 finding. (direct)
4. [unspecified, "Healthcare-RAG 2026"] 12% of agent decisions used >24h-stale guidelines before real-time refresh added. (direct)
5. [unspecified] Hybrid retrieval (dense + BM25 + RRF) yields 5–15% precision lift across domains. (direct)
6. [Sease / Weaviate, 2025] ColBERTv2 / Jina-ColBERT-v2 memory-mapped reduces RAM ~90%. (direct)
7. [unspecified financial-services deployments] Hierarchical/community indexing reports 15–30% precision improvement. (direct)
8. [FalkorDB; arXiv 2506.05690 "When to use Graphs in RAG", June 2025] GraphRAG hits 72–83% on multi-hop; FalkorDB 90%+ on schema-heavy; paper argues against blanket adoption; factoid queries underperform hybrid. (direct)
9. [unspecified] Agentic RAG: 25–40% reduction in irrelevant retrievals vs. naive RAG, with new failure modes (loops, over-retrieval). (direct)
10. [tianpan.co 2026-04; tokenmix.ai] Gemini 1.5 Pro 99.7% single-needle, ~60% multi-fact recall; Claude Opus 4.6 MRCR v2 78.3% at 1M; ~$15/query, 20–30s TTFT. (direct)
11. [ragaboutit, 2025] Position quoted: "The secret to scaling enterprise RAG is to stop optimizing retrieval." (direct)
12. [subagent] AU banking corpus scope estimated at ~10⁵–10⁶ pages across Acts, regs, APRA prudential, ASIC RGs, AUSTRAC, codes, court decisions, internal policy. (direct as subagent's estimate; underlying sources not cited)

## Inferred claims
1. [outside-view] Working qualitative base rate for "comprehensive vertical-domain knowledge silos for agent consumption": ~20–30% become load-bearing within 12 months; 40–50% ship as shelfware; 20–30% abandoned within 18 months. (confidence: inferred; no cited study)
2. [outside-view] Vertical-RAG reference class predicts technical outcome; KM-portal class (pre-LLM, 2005–2020, "60–80% declined into disuse within 18 months without dedicated curation") predicts organizational outcome. (inferred)
3. [outside-view] Banking documents are "~30–60% tables, capital ratios, schedules, defined-term webs"; naive chunking strips definitions from references. (inferred — percentage not sourced)
4. [outside-view] Custom-trained domain LLMs (BloombergGPT-style) have underperformed RAG-on-frontier-models since GPT-4 / 2023. (inferred — directional claim, no benchmark cited)
5. [outside-view] Tool retrieval emerged as a distinct problem in late 2025 once internal MCP servers exceeded "hundreds of tools." (inferred)
6. [outside-view] In regulated domains, most accuracy gains come from metadata-filtering before semantic search, not from better embeddings. (inferred — asserted as "underrated")
7. [outside-view] Long-context-as-RAG-replacement is "largely debunked for production by mid-2026" for banking-scale silos. (inferred from the recall/cost numbers above)
8. [outside-view] MCP is action layer, not retrieval layer; hybrid (RAG-for-grounding + MCP-for-action) is "converging 2026 practice." (inferred)
9. [outside-view] Strongest single predictor of shelfware in this class is unbounded scope ("comprehensive / any needed information"). (inferred)

## Authority-framed claims
1. "Anthropic Contextual Retrieval" numbers (5.7% → 1.9%, 35/49/67%) — underlying claim: contextual retrieval + rerank cuts failure ~67%. Quote present in output: no (numbers cited, no quote). Confidence: direct (Anthropic published these).
2. "ragaboutit (2025): The secret to scaling enterprise RAG is to stop optimizing retrieval" — underlying claim: post-baseline retrieval-quality returns diminish vs. consumption/freshness/eval work. Quote present: yes (one sentence). Confidence: direct.
3. "Harvey's BigLaw-Bench" cited as exemplar of evals-before-silo — underlying claim: teams that built domain evals first outperformed silo-first teams. Quote present: no. Confidence: unsupported (no comparative study cited).
4. "Faktion / Zeta Alpha / RAGFlow" — underlying claim: simple RAG rarely survives production. Quote present: no. Confidence: inferred (multi-source attribution, no quote).
5. "BloombergGPT lesson" — underlying claim: training custom vertical model is dominated by frontier+RAG. Quote present: no. Confidence: unsupported as causal claim; widely-held industry view but not benchmarked here.
6. "arXiv 2506.05690 'When to use Graphs in RAG'" — underlying claim: paper argues against blanket GraphRAG adoption. Quote present: no. Confidence: inferred.

## Contradictions surfaced
- **Pro-GraphRAG vs anti-GraphRAG.** FalkorDB/community-indexing benchmarks (72–83%, 90%+ on schema-heavy, 3.4× accuracy in some multi-hop cases) vs. arXiv 2506.05690 arguing against blanket adoption and factoid queries underperforming hybrid.
- **Optimize retrieval vs stop optimizing retrieval.** Anthropic Contextual Retrieval claims ~67% failure-rate reduction from retrieval-side work; ragaboutit (2025) argues post-baseline retrieval-quality work has diminishing returns vs. consumption/freshness/eval work.
- **Comprehensiveness vs freshness.** Subagent asserts these trade off in regulated domains; not directly contradicted in the return but flagged as the central scope tension.
- **Long-context as RAG replacement.** Strong single-needle recall (99.7%) vs. weak multi-fact recall (~60%) and prohibitive cost ($15/query, 20–30s TTFT) — same technology, opposing implications.

## Subagent's own verdict (verbatim)
"**Below base rate** as currently scoped — primarily because of (a) 'comprehensive / any needed information' framing — strongest single predictor of shelfware — and (b) absence of named refresh pipeline tied to regulator feeds and named consuming agent task."

Lift conditions named: (1) replace "comprehensive" with ranked month-1 agent tasks; (2) name refresh SLA per source class before architecture; (3) build eval harness with version-anchored citations before the silo; (4) default architecture = hybrid retrieval + Anthropic contextual + cross-encoder rerank + structured metadata filtering, GraphRAG only on proven multi-hop patterns, MCP as action surface.

## Gaps the subagent missed
- No AU-specific base rate; reference class is global vertical-RAG. AU regulator licensing/feed contracts (APRA, ASIC, AUSTRAC, Federal Register of Legislation) are not enumerated — material because failure mode #1 (staleness) and the "no regulator-feed contract" risk both depend on which feeds are actually obtainable.
- No cost envelope. Anthropic contextual retrieval requires "one Claude call per chunk at index time" on a 10⁵–10⁶ page corpus; absolute $ figure never computed.
- No latency budget for the consuming agent — agentic RAG and reranking both add latency; subagent does not say what tolerable p95 looks like.
- "Comprehensive trap" is named as the dominant risk but no concrete shortlist of which agent tasks would constitute a defensible month-1 scope.
- Build-vs-buy alternative (existing AU regtech vendors — e.g., Thomson Reuters Practical Law AU, LexisNexis, CCH, RegRoom) not surveyed; subagent only addresses build-vs-frontier-model, not build-vs-vendor.
- Citation/version-anchoring failure (#4) is named but no concrete schema (instrument + section + version + effective-date) requirement is given for the eval harness.
- Multi-jurisdiction edge (AU banks operating in NZ/Singapore/HK) not addressed.

## Token budget
~950 tokens.
