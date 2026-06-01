# Structured & Agentic Retrieval — Knowledge Graphs and Multi-Step Retrieval

_Researched 2026-06-01 - axis: graph & agentic RAG_

This axis examines whether a topical knowledge-retrieval tool — accurate retrieval over local docs, websites, and databases, consumed by an AI agent — should ship with **graph-structured retrieval** (GraphRAG family) and/or **agentic/multi-step retrieval** (Self-RAG, CRAG, ReAct-style query planning) as part of its SOTA default. The first deployment target is Australian banking regulation, but the architecture is meant to be domain-agnostic.

The headline tension: both graphs and agentic loops are real capabilities that win on a specific, identifiable class of query — and both are routinely deployed where they lose money, latency, and sometimes accuracy versus a well-tuned hybrid baseline. The 2025–2026 literature is unusually clear about *when* each helps, which makes a conditional ("switch ON when…") verdict defensible rather than a blanket yes/no.

---

## Table of Contents

1. [The GraphRAG family — what each member is and costs](#1-the-graphrag-family)
2. [What problems graphs actually solve](#2-what-problems-graphs-actually-solve)
3. [When graphs HELP vs HURT — the conditions](#3-when-graphs-help-vs-hurt)
4. [Index-build cost — the cliff and how it fell](#4-index-build-cost)
5. [Agentic RAG — the patterns](#5-agentic-rag-patterns)
6. [Is agentic worth it? The 2026 cost/latency reckoning](#6-is-agentic-worth-it)
7. [Intelligence placement — tool vs calling agent](#7-intelligence-placement)
8. [Proven adopters per approach](#8-proven-adopters)
9. [Contrarian views, collected](#9-contrarian-views)
10. [Verdict](#verdict)
11. [Sources](#sources)

---

## 1. The GraphRAG family

"GraphRAG" is not one system; it is a family with very different cost profiles. All of them sit on the same premise: index a corpus as entities + relationships (a knowledge graph) instead of, or alongside, flat vector chunks, so that retrieval can *traverse* relationships rather than only match similarity.

| System | Origin | Index cost | What it's for |
|---|---|---|---|
| **Microsoft GraphRAG** | Microsoft Research, 2024 | Highest — LLM-driven entity extraction + community summarization | Global/"sense-making" queries over a whole corpus |
| **LazyGraphRAG** | Microsoft Research, Nov 2024 | ~Vector-RAG cost (0.1% of full GraphRAG) | Defers LLM use to query time; both local + global |
| **LightRAG** | HKU (HKUDS), EMNLP 2025 | ~2 orders of magnitude below GraphRAG | Domain-specific Q&A where cost matters; incremental updates |
| **nano-graphrag** | community | Minimal | Stripped-down readable GraphRAG reimplementation |
| **HybridRAG** | BlackRock + NVIDIA, ACM ICAIF 2024 | Graph + vector both built | Vector and graph retrieval merged before generation |
| **Neo4j GraphRAG / Graphiti** | Neo4j | Ontology-design-heavy up front | Enterprise graphs with native vector index + Cypher traversal |

Two design axes distinguish them:

- **When is the LLM invoked?** Microsoft's full GraphRAG spends LLM tokens at *index* time to extract entities and pre-summarize communities. LazyGraphRAG defers nearly all LLM use to *query* time, "blending vector RAG's best-first search with GraphRAG's breadth-first search through iterative deepening" ([Microsoft Research, 2024-11-25](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)).
- **Graph only, or graph + vector?** HybridRAG and Neo4j's pattern retrieve from *both* a vector store and a graph and merge; pure GraphRAG retrieves from the graph alone.

The most important 2025–2026 development is that the cost gap between "full GraphRAG" and "vector RAG" has largely collapsed for the *local-query* case (LazyGraphRAG, LightRAG), which removes the strongest historical argument against graphs — but **not** the argument that graphs don't help most query types.

---

## 2. What problems graphs actually solve

The defensible, repeatedly-measured wins for graph structure are three:

1. **Multi-hop reasoning** — questions whose answer requires chaining facts across documents ("Which subsidiary of the entity that acquired X is regulated under Y?"). Following relationship chains is the native operation of a graph. In a systematic Michigan State / Meta / IBM evaluation, Community-GraphRAG (Local) was the best performer on the HotPotQA and MultiHop-RAG multi-hop datasets; on MultiHop-RAG with Llama-3.1-70B it scored **71.17% overall vs vanilla RAG's 65.77%**, and notably **13.6% of MultiHop-RAG queries were answered correctly *only* by GraphRAG** ([Han et al., arXiv:2502.11371, Feb 2025](https://arxiv.org/html/2502.11371v2)).

2. **Global / corpus-summarization queries** — "What are the main themes across this entire body of regulation?" Vector RAG retrieves *k* nearest chunks and cannot see the whole corpus; GraphRAG's pre-computed community summaries can. The same evaluation found GraphRAG dominates on *diversity* and "broad, globally inclusive" perspectives in query-based summarization, even though vanilla RAG won on detail-faithful summarization (ROUGE-2/BERTScore against ground truth) ([Han et al., 2025](https://arxiv.org/html/2502.11371v2)).

3. **Entity-web / schema-bound aggregation** — queries that require structured joins ("count, by regulator, the obligations introduced after date D"). Practitioner reports claim vector RAG accuracy can fall to ~0% on schema-bound aggregations where graph retrieval reaches ~90% ([buildmvpfast, 2026](https://www.buildmvpfast.com/blog/graphrag-vs-vector-rag-knowledge-graph-ai-2026)) — treat the exact figures as vendor-flavored, but the *direction* is corroborated by the peer-reviewed multi-hop results above.

HybridRAG (BlackRock + NVIDIA) quantifies the merge case on financial earnings-call transcripts: HybridRAG matched or beat both pure approaches on faithfulness (0.96) and answer relevance (0.96), and recovered the **context recall (1.0)** that pure GraphRAG lost (GraphRAG fell to 0.85). Crucially, the paper names GraphRAG's failure mode directly: "GraphRAG sometimes fails to answer questions correctly whenever there is no entity explicitly mentioned in the question" ([Sarmah et al., arXiv:2408.04948, Aug 2024](https://arxiv.org/html/2408.04948v1)). Note the tradeoff inside that same table: HybridRAG's context *precision* (0.79) was the worst of the three — merging graph context pulls in tangential material.

---

## 3. When graphs HELP vs HURT

The single most directly-on-point source for this axis is the requested paper: **"When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation"** (Xiang, Wu, Zhang, Chen, Hong, Huang, Su; [arXiv:2506.05690](https://arxiv.org/abs/2506.05690), submitted 6 Jun 2025, last revised Feb 2026). Its abstract opens with the contrarian finding baked in: *"GraphRAG frequently underperforms vanilla RAG on many real-world tasks."* The paper introduces **GraphRAG-Bench** ([benchmark site](https://graphrag-bench.github.io/)), which evaluates across fact retrieval, complex reasoning, contextual summarization, and creative generation, and across the full pipeline (graph construction → retrieval → generation). Its conclusion: graph structure delivers measurable benefit specifically for **hierarchical knowledge retrieval and deep contextual reasoning** — not for the average query.

Synthesizing 2506.05690 with the systematic evaluation (2502.11371) and HybridRAG (2408.04948), the conditions are:

**Graphs HELP when:**
- The query is genuinely **multi-hop** (≥2 relationship traversals to reach the answer).
- The query is **global/thematic** over the whole corpus ("summarize all", "what are the trends").
- The corpus is **entity-dense and relationship-rich** (regulation cross-references, org structures, citation webs) — AU banking regulation plausibly qualifies.
- The answer requires **structured aggregation** a join can express but similarity cannot.

**Graphs HURT (or are wasted) when:**
- The query is a **factoid / single-hop lookup** ("What is the capital adequacy ratio threshold?"). On Natural Questions (single-hop), vanilla RAG beat GraphRAG **74.55% vs 71.27% F1** ([Han et al., 2025](https://arxiv.org/html/2502.11371v2)).
- The query needs **fine-grained detail** that graph abstraction discards.
- The query **names no entity** — graph retrieval has no anchor and can hallucinate ([Sarmah et al., 2024](https://arxiv.org/html/2408.04948v1)).
- The corpus is **small, flat, or fast-changing** — index-build cost and community-recompute cost (re-clustering on update is *not* O(1)) don't amortize ([buildmvpfast, 2026](https://www.buildmvpfast.com/blog/graphrag-vs-vector-rag-knowledge-graph-ai-2026)).
- The **knowledge graph is incomplete**: only ~65.8% of answer entities even existed in the auto-built HotPotQA KGs; triplet-only KG-GraphRAG retrieved accurately in just **39.2%** of Hotpot cases vs vanilla RAG's **88.6%** ([Han et al., 2025](https://arxiv.org/html/2502.11371v2)). A bad auto-extracted graph is worse than no graph.

**The 2026 practitioner consensus** is therefore *hybrid, not pure graph*: combine vector retrieval with a lightweight relational/graph layer and route per query. "Hybrid RAG reduces hallucination risk without full graph overhead… in 2026, this is the most pragmatic enterprise approach" ([Ninth Post / TianPan, 2026](https://tianpan.co/blog/2026-04-19-graphrag-vs-vector-rag-architecture-decision)).

---

## 4. Index-build cost

Graphs' historical killer objection was index cost, and it was real. Microsoft's own pipeline: graph extraction is ~75% of indexing cost; a ~100k-chunk corpus could consume **millions of LLM tokens** with build times of hours to days. The widely-cited anecdote is a single dataset costing **~$33,000 to index in early 2024** ([Shereshevsky, "GraphRAG Cost Cliff", Mar 2026](https://medium.com/graph-praxis/the-graphrag-cost-cliff-how-33-000-became-33-in-eighteen-months-be1b0fbe37e4)).

That cliff has fallen ~1000x in 18 months via two routes:
- **LazyGraphRAG** (Microsoft Research): index cost "identical to vector RAG and 0.1% of the costs of full GraphRAG", and on *global* queries it delivers "comparable answer quality to GraphRAG Global Search" at **>700x lower query cost** ([Microsoft Research, 2024-11-25](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)).
- **LightRAG** (EMNLP 2025): retrieval quality close to GraphRAG at roughly two orders of magnitude lower cost — ~$0.15 to process documents that cost $4–7 under traditional GraphRAG — plus *incremental* graph updates ([HKUDS/LightRAG](https://github.com/hkuds/lightrag); [learnopencv](https://learnopencv.com/lightrag/)).

Implication for this tool: **the cost objection to graphs is now largely answerable by choosing the lazy/light variant.** The remaining objection — that graphs don't help most query types — is the binding one.

---

## 5. Agentic RAG patterns

Agentic RAG replaces single-shot "retrieve k chunks → generate" with a controlled loop that can decide whether to retrieve, rewrite the query, evaluate what came back, and re-retrieve. The named patterns of the 2025–2026 canon:

- **Self-RAG** (Asai, Wu, Wang, Sil, Hajishirzi; [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)): a single model trained to emit *reflection tokens* — it decides on-demand whether to retrieve at all, then critiques its own retrieved passages and generations.
- **Corrective RAG / CRAG** (Yan et al., [arXiv:2401.15884](https://ar5iv.labs.arxiv.org/html/2401.15884), 2024): a lightweight *retrieval evaluator* scores retrieved docs and triggers one of three corrective actions, including falling back to **web search** when local retrieval is judged insufficient.
- **Adaptive RAG**: a cheap router classifies query difficulty and sends easy queries down a fast single-shot path, escalating only hard ones to the loop.
- **ReAct-style / query-planning agents**: an LLM decomposes a compound question into focused subqueries, runs them (often in parallel), reranks, and merges. This is exactly the pattern Azure AI Search productized as **agentic retrieval**: "a reasoning step in query planning… breaks down compound questions into focused subqueries… parallel retrieval… semantic reranking, and results merging" ([Microsoft Learn, agentic retrieval overview](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)).

The mechanism common to all: trade **more tokens and more latency** for **higher faithfulness on hard questions**. Vanilla RAG answers in 1–2s; an agentic loop of 3–4 iterations takes 8–12s, and loops are capped at 5–6 to prevent runaway ([MarsDevs, 2026](https://www.marsdevs.com/guides/agentic-rag-2026-guide)).

---

## 6. Is agentic worth it?

The most rigorous 2026 answer is sobering. **"Is Agentic RAG worth it? An experimental comparison of RAG approaches"** (Ferrazzi, Cvjeticanin, Piraccini, Giannuzzi; [arXiv:2601.07711v2](https://arxiv.org/html/2601.07711v2), 20 Apr 2026) compares agentic vs a well-built "Enhanced" (non-agentic) RAG across intent handling, query rewriting, document refinement, and underlying LLM. Findings:

- Agentic cost **3.3x more input tokens and 1.9x more output tokens**, took **1.5x longer**, and ran up to **3.6x higher cost** in some scenarios.
- The headline conclusion: *"a well-optimized Enhanced RAG can match or exceed Agentic performance while remaining more efficient."*
- Agentic's wins were narrow: query rewriting (+2.8 NDCG@10) and well-defined-domain intent handling (FIQA finance: 98.8 vs 95.7 F1). It **lost** on document reranking (Enhanced +5.6 NDCG@10) and **collapsed** in broad/noisy domains (FEVER fact-checking: 64.6 vs 87.9 F1).
- A damning efficiency finding: even when agents retrieved multiple times, **53% of retrieved documents were identical across iterations** — agents often don't actually iterate productively once an initial decision is made.

The token-multiplier objection compounds when agentic becomes **multi-agent**. Anthropic's production Research system "use[s] about 15x more tokens than chats" and beat single-agent Opus 4 by 90.2% on internal eval — but Anthropic is explicit that "for economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance," and that domains "that require all agents to share the same context or involve many dependencies between agents are not a good fit" ([Anthropic Engineering, 2025](https://www.anthropic.com/engineering/multi-agent-research-system)).

And the strongest academic contrarian: **"Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets"** (Tran & Kiela, [arXiv:2604.02460](https://arxiv.org/pdf/2604.02460), Apr 2026) — when token budget is held *constant*, concentrating it in one model's extended reasoning beats distributing it across agents; coordination/communication overhead offsets the collaborative gain. Douwe Kiela being a co-author (a RAG originator) gives this weight.

**The 2026 consensus is "adaptive, not always-agentic":** use a cheap router to decide *whether* agentic behavior is warranted; reserve the loop for hard queries; cap iterations; add timeouts ([MarsDevs, 2026](https://www.marsdevs.com/guides/agentic-rag-2026-guide); [Ferrazzi et al., 2026](https://arxiv.org/html/2601.07711v2)).

---

## 7. Intelligence placement

This is the axis-specific question that matters most for *this* tool: **the consumer IS already an agent.** How much retrieval intelligence belongs inside the tool vs the calling agent?

There is no peer-reviewed paper that settles "thin vs thick retrieval tool", so this section is reasoned from architecture principles plus the agentic-cost evidence above, and flagged as such.

**The case for a "thick" tool (intelligence inside):**
- The tool owns the corpus, the index, and the graph; it knows the data distribution and can route query→strategy (vector / graph / hybrid) far more cheaply than the calling agent reasoning blind.
- Putting query planning *inside* the tool avoids the **multi-agent token multiplier**: the calling agent issues one tool call, the tool runs its own (cheap, possibly non-LLM) router and parallel subqueries, and returns merged + reranked results. This is precisely Azure's productized model — agentic retrieval lives *behind the knowledge-base object*, not in the caller ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)).
- Reranking is unambiguously a tool-side win: the Enhanced-RAG reranking advantage (+5.6 NDCG@10 over agentic) ([Ferrazzi et al., 2026](https://arxiv.org/html/2601.07711v2)) is cheapest done once, server-side, with a dedicated reranker.

**The case for a "thin" tool (intelligence in the caller):**
- If the calling agent is *already* doing multi-step reasoning, a tool that *also* loops can produce **double iteration** — the caller re-retrieves because it's unsatisfied, the tool internally re-retrieved too — multiplying cost with the "53% identical docs" waste ([Ferrazzi et al., 2026](https://arxiv.org/html/2601.07711v2)).
- The caller has conversation context the tool lacks; query planning that needs chat history arguably belongs caller-side (though Azure pushes even this into the tool via the chat-thread parameter).
- A thin, predictable tool is easier to compose, cache, and reason about — the MCP-era guidance is that tools should expose "explicit, machine-readable" contracts, not unpredictable internal autonomy ([codeongrass, 2026](https://codeongrass.com/blog/mcp-server-ecosystem-integration-layer-ai-agents-2026/)).

**Synthesis position for this tool:** Put **deterministic-to-cheap retrieval intelligence inside the tool** (hybrid vector+keyword+graph routing, server-side reranking, query decomposition for compound questions), but **keep open-ended agentic looping out of the tool** and let the calling agent own that — because the caller already has a loop, and two loops is the worst of both worlds. The tool should be "smart about retrieval, dumb about goals." This matches the emerging pattern of retrieval tools "optimized for the retrieval patterns agents use" rather than re-implementing the agent ([codeongrass, 2026](https://codeongrass.com/blog/mcp-server-ecosystem-integration-layer-ai-agents-2026/)).

---

## 8. Proven adopters

| Approach | Proven adopters | Source |
|---|---|---|
| **Microsoft GraphRAG / LazyGraphRAG** | Microsoft Research (origin + production tooling) | [Microsoft Research, 2024](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) |
| **HybridRAG (vector + graph merge)** | BlackRock + NVIDIA (financial earnings analysis, ACM ICAIF 2024) | [Sarmah et al., 2408.04948](https://arxiv.org/html/2408.04948v1) |
| **Neo4j GraphRAG patterns** | Goldman Sachs, Deloitte (reported; weeks of ontology design pre-retrieval) | [sider.ai, 2025](https://sider.ai/blog/ai-tools/best-graphrag-alternatives-to-try-in-2025) |
| **LightRAG** | HKU research + open-source community (EMNLP 2025) | [HKUDS/LightRAG](https://github.com/hkuds/lightrag) |
| **Agentic / query-planning retrieval** | Microsoft Azure AI Search (productized); GlassDollar (Siemens/Mahle startup eval, ~10M docs, parallel fan-out) | [Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview); [VentureBeat, 2026](https://venturebeat.com/data/the-retrieval-rebuild-why-hybrid-retrieval-intent-tripled-as-enterprise-rag-programs-hit-the-scale-wall) |
| **Multi-agent research** | Anthropic (Claude Research, orchestrator-worker) | [Anthropic Engineering, 2025](https://www.anthropic.com/engineering/multi-agent-research-system) |
| **Self-RAG / CRAG** | Research-origin; widely re-implemented in LangGraph production stacks | [Asai et al.](https://arxiv.org/abs/2310.11511); [Yan et al.](https://ar5iv.labs.arxiv.org/html/2401.15884) |

Note on the BlackRock/Goldman/Deloitte adopters: the Goldman Sachs / Deloitte claim comes from a secondary practitioner blog, not a primary case study — treat it as suggestive, not confirmed. BlackRock+NVIDIA's HybridRAG is a primary, peer-reviewed authorship attribution.

---

## 9. Contrarian views, collected

Per the requirement, at least one contrarian per major claim:

- **"GraphRAG is overhyped / underperforms."** Direct from the requested paper's own abstract: *"GraphRAG frequently underperforms vanilla RAG on many real-world tasks"* ([Xiang et al., 2506.05690](https://arxiv.org/abs/2506.05690)). Reinforced by the single-hop loss (74.55% vs 71.27% F1) and the 39.2%-vs-88.6% triplet-retrieval collapse ([Han et al., 2502.11371](https://arxiv.org/html/2502.11371v2)).

- **"You don't even need a pre-built graph."** LogicRAG ([Chen et al., arXiv:2508.06105](https://arxiv.org/html/2508.06105v1), Aug 2025) argues pre-built graphs impose "overwhelming token cost and update latency," can encode "irrelevant or redundant information," and are "inflexible" to query variety — and instead extracts reasoning structure *at inference time* as a DAG, beating HippoRAG2 by +14.7% on 2WikiMQA while using *fewer* query-time tokens (1,777.9 vs 2,809.2). This is a direct shot at the entire pre-built-graph premise.

- **"Agentic retrieval isn't worth the cost."** Ferrazzi et al.'s core conclusion that Enhanced RAG "can match or exceed Agentic performance while remaining more efficient," plus the 53%-identical-docs waste ([arXiv:2601.07711](https://arxiv.org/html/2601.07711v2)).

- **"Multi-agent is worse than one good agent at equal budget."** Tran & Kiela, [arXiv:2604.02460](https://arxiv.org/pdf/2604.02460) (Apr 2026).

- **"Multi-agent only pays off above a value threshold."** Anthropic's own 15x-token caveat ([Anthropic Engineering, 2025](https://www.anthropic.com/engineering/multi-agent-research-system)).

- **Contrarian-to-the-contrarians ("RAG/structured retrieval is *more* foundational than ever").** RAGFlow's 2025 year-end review argues RAG didn't lose to agents — it became the "Context Engine" substrate *underneath* agents ([RAGFlow, 2025](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)). This supports investing in a strong retrieval tool, while staying neutral on graph-vs-vector.

---

## Verdict

**Graph and full-agentic capability do NOT belong in the SOTA *default* for this tool. A strong hybrid (dense + sparse + reranking) retrieval core is the default; graph and agentic are conditional, opt-in layers.**

This follows directly from the strongest evidence: the requested paper's own finding that GraphRAG *underperforms vanilla RAG on many real-world tasks* and helps only on hierarchical/deep-reasoning queries ([2506.05690](https://arxiv.org/abs/2506.05690)); the systematic single-hop loss for graphs ([2502.11371](https://arxiv.org/html/2502.11371v2)); and the rigorous finding that well-built non-agentic RAG matches or beats agentic at a fraction of the cost ([2601.07711](https://arxiv.org/html/2601.07711v2)).

**The default (always ON):**
- Hybrid retrieval: dense vector + sparse/keyword (BM25-class) + **server-side reranking**. Reranking is the highest-ROI intelligence and is unambiguously tool-side.
- Light query decomposition for compound questions (deterministic/cheap-router, not an LLM agent loop).

**Switch graph layer ON when ALL of:**
- Corpus is entity-dense and relationship-rich (AU banking regulation cross-references plausibly qualify — validate per-domain, do not assume).
- Workload contains a material share of **multi-hop** or **global/thematic** queries (measure on a held-out query set; if <~15–20% multi-hop, skip).
- You use a **lazy/light** variant (LazyGraphRAG or LightRAG), so index cost ≈ vector RAG and the cost objection disappears. Never default to full Microsoft GraphRAG's index pipeline.
- The auto-extracted graph passes a completeness check (answer-entity coverage); a bad graph is worse than none.

**Switch agentic looping ON when:**
- A measured slice of queries fails single-shot retrieval AND the per-query *value* justifies 1.5–3.6x cost and ~5–10s latency.
- Prefer **Adaptive RAG**: a cheap router escalates only hard queries; cap iterations at 5–6; add timeouts.
- Keep CRAG-style corrective fallback (e.g., to web search) as a targeted feature, not a blanket loop.
- **Crucially for this tool:** since the consumer is *already* an agent, keep open-ended looping in the *caller*, not the tool, to avoid double-iteration and the multi-agent token multiplier. The tool should be smart about retrieval, dumb about goals.

**Alternatives if the conditions don't hold:**
- **No multi-hop need →** hybrid + reranking only. This is the most defensible SOTA baseline and the 2026 enterprise consensus.
- **Multi-hop need but cost/latency-sensitive →** LogicRAG-style *inference-time* reasoning structure instead of a pre-built graph ([2508.06105](https://arxiv.org/html/2508.06105v1)).
- **Need both detail and structure →** HybridRAG merge ([2408.04948](https://arxiv.org/html/2408.04948v1)), accepting its context-precision penalty.

**Unresolved uncertainties (anchor-risk flag):** The "graphs hit 90% where vector hits 0%" and "Goldman/Deloitte adopter" claims come from practitioner blogs, not primary studies — directionally consistent with peer-reviewed work but not independently verified here. And the AU-banking-regulation entity-density assumption is *asserted*, not measured; the graph switch condition must be validated against a real query sample before committing index spend.

---

## Sources

- [When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation](https://arxiv.org/abs/2506.05690) — Xiang, Wu, Zhang, Chen, Hong, Huang, Su (arXiv:2506.05690), submitted 6 Jun 2025, revised Feb 2026. The requested paper; GraphRAG-Bench.
- [GraphRAG-Bench benchmark site](https://graphrag-bench.github.io/) — companion benchmark to 2506.05690.
- [RAG vs. GraphRAG: A Systematic Evaluation and Key Insights](https://arxiv.org/html/2502.11371v2) — Han, Ma, Wang, Shomer et al. (Michigan State / U. Oregon / Meta / IBM), arXiv:2502.11371, Feb 2025. Single-hop vs multi-hop numbers; KG-incompleteness data.
- [HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction](https://arxiv.org/html/2408.04948v1) — Sarmah, Hall, Rao, Patel, Pasquali, Mehta (BlackRock + NVIDIA), arXiv:2408.04948, ACM ICAIF 2024. Faithfulness/relevance/precision/recall table.
- [You Don't Need Pre-built Graphs for RAG (LogicRAG)](https://arxiv.org/html/2508.06105v1) — Chen et al., arXiv:2508.06105, Aug 2025. Inference-time reasoning-structure alternative.
- [Is Agentic RAG worth it? An experimental comparison of RAG approaches](https://arxiv.org/html/2601.07711v2) — Ferrazzi, Cvjeticanin, Piraccini, Giannuzzi, arXiv:2601.07711v2, 20 Apr 2026. Agentic cost/latency vs Enhanced RAG.
- [Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets](https://arxiv.org/pdf/2604.02460) — Tran & Kiela, arXiv:2604.02460, Apr 2026. Multi-agent contrarian.
- [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511) — Asai, Wu, Wang, Sil, Hajishirzi, arXiv:2310.11511, 2023.
- [Corrective Retrieval Augmented Generation (CRAG)](https://ar5iv.labs.arxiv.org/html/2401.15884) — Yan et al., arXiv:2401.15884, 2024.
- [LazyGraphRAG sets a new standard for quality and cost](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) — Edge, Trinh, Larson, Microsoft Research, 25 Nov 2024. 0.1% index cost, >700x query-cost reduction.
- [LightRAG (HKUDS)](https://github.com/hkuds/lightrag) — EMNLP 2025; ~2-orders-of-magnitude cheaper than GraphRAG, incremental updates.
- [LightRAG explainer](https://learnopencv.com/lightrag/) — LearnOpenCV; ~$0.15 vs $4–7 per-doc cost figure.
- [Agentic Retrieval Overview — Azure AI Search](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview) — Microsoft Learn, 2026 API. Tool-side query planning, subqueries, reranking, merge.
- [How Anthropic built its multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic Engineering, 2025. 15x tokens, 90.2%, value-threshold caveat.
- [The GraphRAG Cost Cliff: How $33,000 Became $33 in Eighteen Months](https://medium.com/graph-praxis/the-graphrag-cost-cliff-how-33-000-became-33-in-eighteen-months-be1b0fbe37e4) — Shereshevsky, Mar 2026. Index-cost history (practitioner).
- [Agentic RAG: The 2026 Production Guide](https://www.marsdevs.com/guides/agentic-rag-2026-guide) — MarsDevs, 2026. Adaptive routing, iteration caps, latency figures (practitioner).
- [RAG vs Graph-RAG: Which Knowledge Retrieval Strategy Actually Wins in 2026?](https://tianpan.co/blog/2026-04-19-graphrag-vs-vector-rag-architecture-decision) — TianPan / Ninth Post, Apr 2026. Hybrid consensus (practitioner).
- [GraphRAG vs Vector RAG: Knowledge Graph AI Guide 2026](https://www.buildmvpfast.com/blog/graphrag-vs-vector-rag-knowledge-graph-ai-2026) — buildmvpfast, 2026. Schema-bound aggregation figures (practitioner; treat as directional).
- [12 Best GraphRAG Alternatives to Try in 2025](https://sider.ai/blog/ai-tools/best-graphrag-alternatives-to-try-in-2025) — sider.ai, 2025. Adopter claims (practitioner).
- [The retrieval rebuild: hybrid retrieval intent tripled in Q1 2026](https://venturebeat.com/data/the-retrieval-rebuild-why-hybrid-retrieval-intent-tripled-as-enterprise-rag-programs-hit-the-scale-wall) — VentureBeat, 2026. Hybrid adoption 10.3%→33.3%; GlassDollar fan-out.
- [The MCP Server Ecosystem in 2026](https://codeongrass.com/blog/mcp-server-ecosystem-integration-layer-ai-agents-2026/) — codeongrass, 2026. Tool-contract design guidance (practitioner).
- [From RAG to Context — A 2025 year-end review of RAG](https://ragflow.io/blog/rag-review-2025-from-rag-to-context) — RAGFlow/InfiniFlow, 2025. RAG-as-Context-Engine contrarian-to-contrarians.
