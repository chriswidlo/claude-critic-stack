# Candidate Recommendation — Generator (Step 9)

## Position

**The SOTA answer in 2026 is not a single knowledge silo.** It is a **five-layer retrieval-and-control surface** anchored by a provenance contract and an eval harness, with the consuming agent's identity treated as a load-bearing input — not a deferrable detail. Two of the five layers preserve the user's underlying intent (a thing the bank can point at and defend); the silo as a single store is rejected as 2023-vintage architecture that has been outperformed in regulated, high-churn domains since 2024–2025.

Concretely, the layered architecture I recommend is:

**Layer 1 — Source-of-truth catalog (not silo).**
Typed registry of authoritative sources, each with an access mode (federation API, scheduled pull, manual ingest) and a metadata contract `(jurisdiction, publisher, instrument_id, section, version, effective_date, supersedes, supersedes_at)`. Sources for AU banking specifically: APRA Connect / Prudential Standards, ASIC RGs and instruments, Federal Register of Legislation, AUSTRAC guidance, RBA decisions, ABA codes, bank's own product/policy stores. Vendor regtech corpora (Practical Law AU, LexisNexis, CCH) optionally plug in here under their own license envelope. **The catalog is the durable bank-facing artifact** — what an APRA inspector points at when they ask "what is the source of truth your AI uses."

**Layer 2 — Ingest + refresh pipeline keyed to per-source cadence.**
Each source class has a refresh SLA: APRA prudential — event-based on publish + daily fallback poll; ASIC — daily; legislation — parliamentary cycle + ad-hoc; product PDS / interest rates — hourly; RBA decisions — 6-weekly. Diff-aware (re-process only changed material) and version-preserving (every artifact retains supersession chain — point-in-time queryability is required for compliance defense). Tabular content (capital-ratio schedules, fee tables, defined-term webs) goes through a structured-extraction path, not text chunking.

**Layer 3 — Retrieval substrate (hybrid + contextual + rerank, structured-metadata-first).**
Default stack: BM25 + dense (RRF fusion) + Anthropic-style contextual retrieval at index time + cross-encoder or ColBERT-late-interaction reranker. Structured metadata pre-filter (`jurisdiction`, `instrument`, `effective_date`) is applied **before** semantic search — this is the underrated lever in regulated text. Hierarchical index (regulator → instrument → clause) over the natural document tree. Defined-term resolver and supersession-chain resolver as first-class retrieval modes, not as side-channels of generic chunk retrieval.

**Layer 4 — Agent surface (typed tool catalog, not generic search).**
Expose retrieval as specialised tools (`find_prudential_standard`, `resolve_defined_term`, `lookup_pds_for_product`, `fetch_current_rate`, `check_supersession`, `find_regulatory_guide`) rather than a single `search_kb()`. Each tool's contract is narrow, typed, and self-describing (ACI = HCI principle). MCP as the integration substrate. Agentic retrieval (multi-step, planner-driven) is enabled only for query types where the eval harness shows it wins on a quality/cost basis; for simple factoid lookup, single-shot retrieval is correct. Tool retrieval (which-tool-to-call) only becomes a problem past ~50 tools — design the catalog to stay under that ceiling unless growth justifies it.

**Layer 5 — Answer disposition + audit (this is Frame E, carried).**
Every emitted fact carries a citation `(instrument, section, version, effective_date, retrieved_at)`. Pre-emit classifier checks queries against the personal-advice threshold (Corporations Act s766B) and AFSL coverage; high-stakes / threshold-crossing → human-in-the-loop or decline-with-redirect. Append-only audit log records `(query, retrieved_set, answer, citations, model+version, timestamp, disposition)`. **This layer is the regulator-defensible artifact**; Layer 1 + Layer 5 together are what survives an audit.

**Foundation under all five: the eval harness.**
~200 gold Q/A pairs across the agent's actual query mix, version-anchored to specific source instruments and sections, built **before** the pipeline (Frame C). The eval is how you rank candidate variants of layers 3 and 4 empirically rather than by literature reflex. It is also the cheapest research artifact to produce — and is what makes "the SOTA way" a question with an answer in your context, not a generic answer.

## Named tradeoffs

- **Provenance-first vs ingest cost.** Layer 1's metadata contract requires every chunk to carry instrument/section/version/effective-date. Cost: every ingest path becomes an editorial pipeline, not a blob loader. Benefit: defensible answers; without it, Layer 5 is decorative.
- **Layered surface vs cognitive complexity.** Five layers vs one silo is harder to onboard new contributors to and harder to explain in a procurement deck. The single-silo framing wins on legibility; the five-layer surface wins on every load-bearing technical metric.
- **Refresh pipeline as artifact vs build snapshot.** The architecture has no "shipped" state — it has an operating state. Cost: ongoing ops budget. Benefit: a static snapshot of AU banking is wrong by month 6.
- **Eval-first vs time-to-first-answer.** Building the gold set takes 1–2 weeks before any answer ships. Cost: looks slow. Benefit: the alternative is choosing layer-3 variants by vibes.
- **Typed tools vs generic search.** Tool catalogs require domain modeling that a `search()` endpoint sidesteps. Cost: more design upfront. Benefit: agents bypass generic search but use typed tools (the canon C1 finding).
- **Federation vs built KB for high-churn content.** Calling APRA/ASIC APIs at read time wins on freshness, loses on latency and rate-limit risk. The architecture defers this within Layer 1: federation for high-churn (rates, live PDS), built KB for stable (legislation, RGs). The choice per source is a configuration, not a redesign.

## Named assumptions that flip the recommendation if wrong

1. **The consuming agent's shape is characterizable within ~1 week.** If the user genuinely cannot name the consuming agent (retail Q&A bot vs compliance-officer workbench vs banker assist vs regulator-facing audit tool), the cost/quality tradeoff space splits and the architecture above over-commits. **Flip:** if the consumer is unnamed and stays unnamed, recommend instead an *eval-and-catalog-only* deliverable (Layers 1 + 5 + harness, defer 2–4) — that produces the durable artifact without committing the retrieval shape.

2. **APRA Connect / ASIC / Federal Register / AUSTRAC expose point-in-time queryable APIs.** The architecture's federation option in Layer 1 depends on this. **Flip:** if regulator APIs are not point-in-time queryable, Layer 2 must own the version history (heavier build, ~3× ingest complexity, and the "silo" framing the user proposed becomes more defensible because the bank's own store *is* the version-anchored source of truth in the absence of regulator-side history).

3. **The user is asking a design question, not a literature-survey question.** Frame-challenger Frame F: "what is the SOTA way" can be read as "give me the field map" rather than "commit to an architecture." **Flip:** if the user wanted a survey, the right deliverable is the scope-map + the canon contradictions + the outside-view base rate, *without* the prescription above. Step-12 synthesis must offer both shapes and let the user choose.

4. **The query mix is factoid-and-section-lookup dominated, not multi-hop.** GraphRAG is recommended **off** by default in Layer 3. **Flip:** if a representative 50-query sample shows ≥20% supersession-chain / defined-term-web / cross-instrument multi-hop queries, a graph layer becomes mandatory rather than optional, and Layer 3's complexity rises.

5. **The agent's answers are general-information, not personal advice.** Frame E (liability) is real but bounded if the agent never crosses the personal-advice threshold. **Flip:** if the agent gives anything resembling personal advice, the entire architecture is dominated by Layer 5; Layers 1–4 are subordinated to a "decline + escalate" default and the cost question collapses (the cheapest correct answer is "no, ask a human").

## Ways this could be wrong (beyond the assumptions)

- **The 5-layer architecture is over-engineered for a research/exploration KB.** If the user's actual goal is "load all AU banking content somewhere I can poke at it with Claude," a flat tagged corpus + Claude with a file-reading tool is cheaper and within 80% of the quality envelope. The architecture above is correct for production banking AI; it is overkill for a personal knowledge project.
- **The "no single silo" position is a fashion call.** The canon's voice is one-sided (Anthropic 2024–2025) and the librarian flagged this. There is a reading where the field is over-correcting against vector DBs because of a 2023 hangover, and the correct 2027 answer is hybrid-with-a-real-silo. I do not think this is the case but I cannot rule it out from the gather.
- **Frame E may not bind for the user's actual context.** If this is for a non-Australian user studying *how* you would build this for AU banking (research project), the liability layer is academic. The recommendation's emphasis on Layer 5 and AFSL is contingent on the user being a regulated AU institution; if not, downweight Layer 5.

## Frame-level objection from challenges.md, addressed

The frame-challenger's hardest point: *"the recommendation must justify why retrieval architecture is the right deliverable at all, given (a) the unnamed consuming agent, (b) the unanswered live-API question, and (c) the possibility that the user wanted a field map rather than a design."*

My answer:
- (a) is converted into Assumption #1 (and an alternative architecture if it fails).
- (b) is converted into Assumption #2 (and resolved within Layer 1's federation/build hybrid).
- (c) is converted into Assumption #3 (and the synthesis step must offer both shapes).
- The "retrieval architecture" framing is *not* substituted for "knowledge silo" — Layer 1 (catalog) and Layer 5 (audit log) are the silo-shaped artifacts, preserved deliberately. What I reject is the *single-store* form of silo, not the durable-artifact intent.

## Conflict resolutions from scope-map.md

- **#5 GraphRAG** — closed: OFF by default, ON only if eval shows ≥20% multi-hop. Reason: defaulting in adds index-build cost the corpus does not justify without query evidence; structured metadata + hierarchical index captures most multi-hop value cheaply.
- **#10 Agentic retrieval cost** — recast as a 2x2 (consumer Q&A vs workbench × static vs agentic): consumer→static, workbench→agentic. The architecture supports both; deployment chooses.
- **#11 Filesystem-as-store** — closed: rejected as primary index for a 10⁶-page heterogeneous-publisher corpus; useful as a secondary raw-artifact store for downloaded PDFs.
- **#12 Live federation vs built KB** — closed within Layer 1 as a per-source configuration: high-churn (rates, current PDS) → federate; stable (legislation, prudential standards) → build. Pre-condition is the API probe (Assumption #2).
- **#13 Vendor regtech vs build** — closed: hybrid. Vendors for editorial/secondary content under license; in-house for primary regulator material and provenance contract; treated as a procurement decision parallel to architecture.

## Cheapest experiment that reduces the biggest uncertainty

**1-week probe + gold set:** (i) Five-line API capability check on APRA Connect, ASIC, Federal Register of Legislation, AUSTRAC (resolves Assumption #2). (ii) 50-query gold set drawn from real or representative agent queries, version-anchored against instruments/sections, scored by hand (resolves Assumption #4 and gives a baseline for ranking Layer-3 variants). (iii) One sentence from the user naming the consuming agent's identity (resolves Assumption #1; if they cannot, that's also information).

This experiment costs ~1 person-week and would change the recommendation in 3 of the 5 assumption-flip cases.
