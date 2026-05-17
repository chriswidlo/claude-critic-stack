# Synthesis — SOTA for an AI-consumed knowledge surface (AU banking as the test case)

This is the orchestrator-delivered final synthesis (Step 12). The candidate (`candidate.md`) was reworked under unanimous critic veto; routing decision in `decision-log.md` was *rewrite at synthesis* — restructure the output shape to honor the user's "research, not execute" mode rather than re-run upstream steps. The shape below is field-map-first, prescription-as-appendix.

## Classifier label
`investigation` (primary), `new` (alternative).
The default frame the label carries is *"terminate in a decision-relevant comparison of approaches, not a literature dump."* The alternative classification (`new`) would have biased toward over-designing before evidence. The user's "research" framing keeps this on the `investigation` side: a map with one optional shape, not a build plan.

## Reframe (Revision 1)
The user said *"knowledge silo for AI."* The orchestrator named four reframes the field would push back with:
- **Frame A — Agent's tool ecosystem, not a silo.** The 2025–2026 shift is toward an agent with multiple specialised tools (BM25, dense, structured SQL, web fetch) deciding what to call per sub-question.
- **Frame B — Live pipeline, not static artifact.** The artifact is the ingest + refresh + invalidation pipeline, because regulated content has a half-life.
- **Frame C — Query-shaped corpus.** Build the gold-question set first, ingest only what the queries prove you need.
- **Frame D — Provenance-first.** In a regulated domain, every fact carries `(instrument, section, version, effective_date)`. That biases toward structured ingestion over blob-chunk-embed.

The frame-challenger added two more:
- **Frame E — Liability-allocation architecture.** Under AU financial-services law (Corporations Act s766B, ASIC RG 36/244/271, AFSL coverage), the binding constraint is *who is on the hook when the agent is wrong.* Retrieval is downstream of liability gating.
- **Frame F — No KB at all.** Thin agent calls APRA/ASIC/Federal Register/bank APIs at read time. The only persistent artifact is the citation contract.

**Honest friction:** the phrase *"knowledge silo for AI"* is a 2023-vintage formulation. The 2026 question is closer to *"what is the agent's retrieval surface,"* and the answer is rarely a single store. *But* — the frame-challenger forced this naming — the silo framing is *more correct than the reframe* under three conditions: (a) consuming agents are heterogeneous and unknown, so a curated corpus is the durable artifact and the retrieval layer is replaceable; (b) the procurement/political reality is that *"we built the bank's authoritative AI knowledge base"* gets funded while *"we built a retrieval router"* doesn't; (c) a regulator inspector asking *"what is the source of truth your AI uses"* expects an answerable noun.

## Reference-class forecast (outside-view)

Reference class: **enterprise vertical-domain RAG/retrieval systems built for agent consumption in regulated, high-churn corpora** (legal, financial regulation, healthcare, tax). Indicative qualitative base rate (no clean published figure): **~20–30% become load-bearing within 12 months; 40–50% ship as shelfware; 20–30% abandoned within 18 months.** The strongest single predictor of shelfware in this class is **unbounded scope** ("comprehensive / any needed information" — the framing the user used).

Six dominant failure modes, ranked: (1) staleness — regulated content amends faster than re-ingestion; (2) tabular / cross-referenced content defeats naive chunking — banking documents are 30–60% tables and defined-term webs; (3) agent doesn't use it — tool surface mismatch; (4) citation/version-anchoring failure — kills compliance use cases at audit, not at demo; (5) scope explosion — the comprehensive trap; (6) build-vs-buy mis-step — custom domain LLMs (BloombergGPT-style) have been beaten by frontier-model + RAG since 2023.

## Canon — what the corpus says, including what it contradicts itself on

The corpus on this question is **thin and one-sided** (only Anthropic 2024–2025 essays were retrievable). The librarian flagged this as a finding, not a consensus.

**Supporting passages:**
- *Anthropic, Effective Context Engineering (2025)* — agents increasingly use *just-in-time* retrieval (lightweight identifiers, load at runtime via tools), and pre-indexed retrieval is named as suiting "less dynamic content, such as legal or finance work."
- *Anthropic, multi-agent research system (2025)* — static-RAG (top-k → generate) is named as a failure mode versus multi-step search; the *CitationAgent* pattern attaches source locations post-hoc; multi-agent ≈ **15× chat tokens**.
- *Anthropic, Building Effective Agents (2024)* — MCP as third-party tool integration surface; the *ACI = HCI effort* rule for tool design.

**Contradicting passages — the canon contradicts itself:**
- **C1 (frame-level):** Anthropic's own production stance argues for filesystem + grep + agent navigation **bypassing pre-built embedding indexes** for high-churn corpora. The same essays that endorse hybrid retrieval also undercut vector-DB-as-default.
- **C2:** Long-context windows do *not* substitute for retrieval — "context rot" and finite attention budget hold "for the foreseeable future" even at million-token windows.
- **C3:** Agentic retrieval is endorsed *and* costed at ~15× chat tokens — a real economic objection internal to the same essay.
- **C4 (silence-as-finding):** the corpus is silent on GraphRAG, ColBERT/late-interaction, structured-stores-beat-RAG, BloombergGPT-style stacks, and even Anthropic's own *Contextual Retrieval* (Sep 2024). Treat the canon's voice as one input, not the field's consensus.

**WebSearch (currency, not promoted canon)** filled the gaps: *Anthropic Contextual Retrieval* (Sep 2024) — naive embedding baseline failure rate **5.7%** for top-20; contextual embeddings cut failure 35%, contextual + BM25 49%, with reranking **67%** (5.7% → 1.9%). Hybrid (dense + BM25 + RRF) reliably yields 5–15% precision lift. ColBERTv2 / Jina-ColBERT-v2 production-feasible (~90% RAM reduction). Hierarchical/community indexing reports 15–30% precision improvement in financial-services. GraphRAG 72–83% on multi-hop and 90%+ on schema-heavy queries — *but* the June-2025 paper "When to use Graphs in RAG" (arXiv 2506.05690) argues against blanket adoption (factoid queries underperform hybrid). Long-context-as-replacement: ~60% multi-fact recall at $15/query; largely debunked for production at this corpus scale by mid-2026. A live counter-position to all of the above: *"the secret to scaling enterprise RAG is to stop optimizing retrieval"* (ragaboutit, 2025) — beyond a baseline, returns shift to consumption patterns and freshness.

## Scope-map — the tradeoff space, distilled

Eighteen architectural primitives evaluated. The relevant rows:

| Primitive | Verdict | One-line reason |
|-----------|---------|-----------------|
| Naive vector-DB RAG | **replace** | 5.7% top-20 failure floor; dominated by every alternative below. |
| Hybrid (dense + BM25 + RRF) | **floor** | Cheap, mandatory baseline for regulated text. |
| Anthropic Contextual Retrieval | **largest single lever** | 67% failure-rate reduction with rerank; cost is one Claude call per chunk at index time. |
| Cross-encoder / ColBERT rerank | **second lever** | Precision lift on top-k; ColBERTv2 memory-mapped is production-feasible. |
| Structured ingestion with metadata | **load-bearing** | Most accuracy gains in regulated text come from filtering before semantic search, not better embeddings. |
| Hierarchical index (regulator → instrument → clause) | **cheap structural prior** | Mirrors the actual document tree; 15–30% precision lift. |
| GraphRAG | **conditional** | Default OFF; ON only if a real query sample shows ≥20% multi-hop / supersession. Defaulting it in adds index-build cost the corpus may not justify. |
| Long-context-as-replacement | **reject** | Multi-fact recall and cost both kill it at corpus scale. |
| Custom domain LLM (BloombergGPT-style) | **reject** | Dominated by frontier + RAG since 2023. |
| Agentic retrieval / MCP tool surface | **conditional** | ~15× tokens; consumer-Q&A → static, workbench → agentic. |
| Filesystem-as-store | **secondary at most** | Anthropic's stance generalises from a coding repo (one tree, stable paths); a 10⁶-page heterogeneous-publisher regulator corpus is graph-shaped. |
| Live federation (APRA/ASIC/FRL APIs at read time) | **per-source decision** | Federate high-churn (rates, current PDS); build for stable (legislation, RGs). Pre-condition: the regulators must expose point-in-time queryable APIs — *unverified*. |
| Vendor regtech (Practical Law AU, LexisNexis, CCH) | **procurement-parallel hybrid** | Vendor for editorial/secondary; in-house for primary regulator material. Build-vs-buy is rarely all-or-nothing in regtech. |
| Refresh / invalidation pipeline | **the artifact** | The deliverable is the operating pipeline, not the snapshot. Per-source SLA: APRA event-based + daily fallback; ASIC daily; legislation parliamentary cycle; product PDS hourly; RBA 6-weekly. |
| Citation / version-anchoring schema | **non-optional** | Every emitted fact needs `(instrument, section, version, effective_date, retrieved_at)`. |
| Eval harness, gold Q/A | **first artifact** | Build before the silo. The eval is what makes "SOTA" answerable in your context. |
| Tool-retrieval layer | **only past ~50 tools** | Don't pre-build it; design the catalog to stay under the threshold. |
| Human-in-the-loop / approval gate | **bounded by Frame E** | If the agent crosses the personal-advice threshold, this becomes the dominant primitive. |

## Frame-level challenge and how this synthesis addresses it

The frame-challenger's hardest objection: **the orchestrator quietly substituted *"retrieval architecture"* for the user's *"knowledge silo,"* and the substitution is load-bearing and under-argued.** The product critic then echoed it: the workflow had stopped giving the user research and started giving them a build plan.

Addressed by: making this synthesis a *field map first*. The user can read the map and stop. The recommendation below is a single optional shape, not the answer. Frame E (liability) and Frame F (no KB) are first-class options in the map, not footnotes.

## Recommendation (post-critique) — one shape, optional

**If the user wants a single concrete shape to anchor the research against**, the SOTA-as-of-2026 shape for an AI-consumed regulated knowledge surface is *not* a single silo. It is roughly five separable concerns, of which only **two** are silo-shaped:

1. **A source-of-truth catalog** (silo-shaped) — typed registry of authoritative sources with rich metadata (`jurisdiction, publisher, instrument_id, section, version, effective_date, supersedes`). This is the noun an APRA inspector would point at.
2. **A refresh pipeline** keyed to per-source publication cadence; diff-aware; version-preserving.
3. **A retrieval substrate**: hybrid (BM25 + dense) + Anthropic Contextual Retrieval at index time + cross-encoder rerank, with structured-metadata pre-filter applied **before** semantic search. GraphRAG only on demonstrated multi-hop demand.
4. **An agent surface** of typed tools (`find_prudential_standard`, `resolve_defined_term`, `lookup_pds`, etc.) — narrow, ACI-shaped, MCP-integrated. Not a generic `search()` endpoint.
5. **An answer-disposition + audit context** (silo-shaped, separate bounded context) — citation contract, personal-advice classifier, append-only audit log. This is Frame E carried structurally, not as a verb.

Underneath all five: **a 200-pair gold Q/A eval harness, version-anchored, built first.**

**Critic-fold-ins** (the panel did not approve the candidate as written; the demoted shape inherits these corrections):
- **Architecture:** `Instrument` is an aggregate root with a dereferencing service; concept #1's metadata is dereferenced through it, not embedded as value types in #3 and #5. An anti-corruption layer separates regulator taxonomy (#1) from agent tool names (#4) so APRA reorganisations don't break the agent surface. Citations bind content-hashed bytes, not mutable chunk pointers.
- **Operations:** ingest (#2) carries an explicit state machine — `quarantined`, `partially-ingested`, `superseded`, `retracted-by-publisher` — not just "diff-aware." Per-query cost cap with a circuit breaker on agentic mode. Absolute cost envelope must be filled in (a 10⁶-page corpus full re-index is a five-to-six-figure-USD event with one Claude call per chunk; the architecture needs incremental-recovery, not just full rebuild). No rollout without an eval-harness gate and a canary fraction.
- **Product:** the prescription is offered, not pushed. If the user reads the field map and stops, that is also a complete answer.

## Three named uncertainties

1. **Who is the consuming agent?** Retail Q&A bot, compliance-officer workbench, banker assist, regulator-facing audit tool — each rotates the cost/quality space. The architecture's 2x2 (consumer→static, workbench→agentic) is a deferral until this is named. If the consuming "agent" is a heterogeneous fleet of unknown future agents, the recommendation collapses to *catalog + audit + eval harness only*; the retrieval surface is replaceable.
2. **Are APRA Connect / ASIC / Federal Register of Legislation / AUSTRAC point-in-time queryable?** Currently unverified. If yes, federation thins #2 to a federation client. If no, the user's store *is* the version-history of record, and their "silo" framing becomes more defensible — the silo is what makes the bank's answers reproducible.
3. **Is the question a literature-survey question or a design question?** This synthesis answers it as a survey-with-an-optional-shape. If the user actually wanted a commit to one shape, re-run step 9 in that mode.

## Cheapest experiment that reduces the biggest uncertainty

**~1 person-week probe** (no AU banking research required — four small mechanical things):

- A 5-line capability check on APRA Connect, ASIC, Federal Register of Legislation, AUSTRAC: *"do these expose machine-readable feeds with point-in-time querying?"* Resolves uncertainty #2.
- A 50-query gold set: representative AU-banking agent queries, hand-scored against specific instrument/section/version answers. Resolves the GraphRAG default (≥20% multi-hop → ON) and gives a baseline for ranking Layer 3 variants. Removes the need to choose architecture by literature reflex.
- One sentence naming the consuming agent. If the user cannot write that sentence, that is itself the resolution of uncertainty #1.
- (Optional) a build-vs-buy probe of vendor regtech corpora — Practical Law AU, LexisNexis, CCH, RegRoom — to know whether their license footprint covers the user's sources. Resolves the procurement-parallel question.

This experiment changes the recommendation in 3 of 5 assumption-flip cases. It is the highest-leverage, lowest-cost piece of work in this synthesis.
