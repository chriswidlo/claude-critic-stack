# Frame

## Revision 1

### What the user said
> "Find out what is the current SOTA way to create a knowledge silo for AI, in a way that AI just goes there and finds all info it needs that is available."
> Domain: Australian banking. Source corpus: "all available on the internet." Don't do the banking research; design the storage + retrieval architecture.

### The user's implicit frame
1. **Single-store frame.** "Silo" = one place, one API, one ingest pipeline. The agent has one door to knock on.
2. **Exhaustive-ingestion frame.** "Everything there is to know" = coverage is the metric; the goal is to mirror the public internet's banking content into the silo.
3. **Passive-retrieval frame.** "AI just goes there and finds info" = the agent issues a query, the silo returns chunks; classical RAG mental model.
4. **Static-artifact frame.** Build the silo once, then it's a thing the AI queries.

### What the user is implicitly optimizing for
- **Coverage** (no information missing)
- **Self-sufficiency** (the agent does not need to roam the public web)
- **Build determinism** (a silo you can point at)

### What that frame *probably misses*
- Banking content is high-churn (interest rates, RBA cash-rate decisions, APRA prudential updates, product disclosure statements, comparison-rate disclosures). A static dump is stale within a quarter.
- Banking is regulated. **Provenance** (which APRA standard, which ASIC RG, which version of which PDS) is not optional; an agent that returns "the rate is 5.85%" with no citation is unusable for a serious consumer.
- The cost of "ingest everything" scales with the public internet; the cost of "ingest the queries the agent actually loses on" scales with the agent.
- "AI just goes there" elides the question of *which AI*. A coding assistant, a customer-service bot, and a regulatory-compliance assistant want different retrieval shapes off the *same* corpus.

### Alternative frames (at least one — I'll name four)

**Frame A — Agent's tool ecosystem, not a silo.** The 2025–2026 shift in retrieval is *agentic*: the LLM has multiple specialised tools (BM25, dense vector, structured SQL, web fetch, document parser, calculator) and decides which to invoke per sub-question. The "silo" is not a store, it's a router with capabilities. This is closer to MCP-server / Anthropic-skills / agentic-RAG architecture than to "vector DB + LangChain."

**Frame B — Live pipeline, not static artifact.** The artifact is the *ingest + refresh + invalidation* pipeline, not the snapshot. Half-life-aware refresh (RBA decisions: 6-weekly; PDSs: monthly; APRA standards: yearly; bank product pages: daily) drives architecture more than raw retrieval choice does.

**Frame C — Query-shaped corpus.** Build the gold-question set first (50–500 representative agent queries). Measure what retrieval shape + corpus subset wins on those queries. Ingest only what the gold set proves you need. Coverage is the *consequence* of solving queries, not the goal.

**Frame D — Provenance-first.** Every fact the agent emits must cite a primary source identifiable by document + version + section. That biases the architecture toward structured ingestion with rich metadata (jurisdiction, document type, publisher, effective date, supersession chain) — not blob-chunk-embed. In a regulated domain this is the load-bearing constraint, not retrieval recall.

### Alternative optimization the user is *not* naming
**Retrieval precision on the queries that matter, with auditable provenance, at acceptable freshness — bounded by run-time cost.** Not coverage. Not self-sufficiency.

### What I am *not* doing in this step
- Recommending an architecture. (Step 9.)
- Asserting which frame wins. (Step 8 challenges them; step 10 critiques.)
- Pretending the user's frame is wrong. It is *one* valid frame; it is not the only one and probably not the SOTA one.

### Honest friction
The phrase "knowledge silo for AI" is a 2023-vintage formulation. The 2026 question is closer to "what is the agent's retrieval surface" — and the answer is rarely a single store. If we hold the user's silo framing rigidly, we will recommend something that the field already knows is suboptimal for high-churn regulated domains.
