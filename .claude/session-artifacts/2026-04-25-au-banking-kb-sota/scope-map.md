# Scope Map — AU Banking Knowledge Silo

Note: there is no target codebase. Primitives below are *architectural candidates* the SOTA literature surfaces. Relationship is "what the new requirement (a SOTA AU-banking agent retrieval surface, frame-revised toward provenance + freshness + agent-shaped) does to each candidate if a future design inherits it." Default is `subsume` or `replace`.

## Existing primitives touched

| # | primitive | source | relationship | one-line rationale |
|---|-----------|--------|--------------|--------------------|
| 1 | Naive vector-DB RAG (chunk → embed → top-k) | outside-view (5.7% baseline failure); canon C1, multi-agent essay | **replace** | Anthropic + 2025 production literature converges on naive RAG as a failure mode; baseline failure rate is the floor, not a starting point. |
| 2 | Hybrid retrieval (dense + BM25 + RRF) | outside-view (5–15% precision lift; contextual+BM25 = 49% failure cut) | **extend** | Hybrid is the empirically-supported floor for regulated text; earns standalone existence because BM25 carries defined-term/section-number lookup that dense alone strips. |
| 3 | Anthropic Contextual Retrieval (LLM-prepended chunk context at index time) | outside-view (35→49→67% failure cut); canon (notably absent — staleness flag) | **extend** | Largest single retrieval-quality lever in the cited evidence; standalone because it's an index-time transform orthogonal to retrieval shape. Conflict with cost envelope flagged below. |
| 4 | Cross-encoder / ColBERT late-interaction reranking | outside-view (67% cut with rerank; ColBERTv2 memory ~90% reduction); canon (named gap) | **extend** | Reranker is the second-largest precision lever and operates on a different stage (post-retrieval). Standalone because removing it forfeits the 5.7→1.9% endpoint. |
| 5 | GraphRAG / KG-augmented retrieval | outside-view (72–83% multi-hop; arXiv 2506.05690 anti-blanket) | **conflict** — see Requires decision | Evidence splits: wins on schema-heavy multi-hop, loses on factoid; cannot be defaulted in or out without a named query mix. |
| 6 | Structured ingestion with rich metadata (jurisdiction, instrument, section, version, effective-date) | outside-view ("metadata-filtering before semantic search is the underrated lever"); frame D | **extend** | Provenance-first frame makes this load-bearing, not optional. Standalone because it's the substrate every other retrieval layer filters on. |
| 7 | Hierarchical / community indexing (regulator → instrument → clause) | outside-view (15–30% precision in financial-services) | **extend** | Mirrors the actual document tree of AU regulation (APRA prudential standards, ASIC RGs, Federal Register instruments); cheap structural prior with named precision lift. |
| 8 | Long-context-as-RAG-replacement (1M+ window, no retrieval) | outside-view (60% multi-fact recall, $15/query); canon C2 (context rot) | **replace** (with nothing — i.e., reject) | Both empirics (multi-fact recall) and canon (context rot, attention budget) reject this for a 10⁵–10⁶ page corpus. Replacement = retrieval architecture, not a bigger window. |
| 9 | Custom domain LLM (BloombergGPT-style) | outside-view (dominated by frontier+RAG since 2023); canon (named gap) | **replace** | Reference-class verdict is unambiguous; cost + staleness + frontier-model gap make this a category error for a 2026 build. |
| 10 | Agentic retrieval / agent-navigated tool surface (Anthropic just-in-time, MCP) | canon §1, §2 ("just in time", hybrid for finance/legal); outside-view (25–40% irrelevant-retrieval reduction; loop failure modes) | **extend** | Frame A elevates this to the architecture itself; standalone because it's the *control* layer that decides when each of #2/#3/#4/#6 fires. Conflict with cost flagged below. |
| 11 | Filesystem-as-store with grep/glob (Claude Code pattern) | canon §9 ("bypassing stale indexing") | **conflict** — see Requires decision | Anthropic's own production stance argues this can outperform vector indexes for high-churn corpora; for a 10⁶-page regulator corpus the generalization is unproven. Cannot be defaulted without a decision. |
| 12 | Live systems-of-record federation (call APRA/ASIC/Federal Register APIs at read time) | canon (librarian-flagged gap #4); frame B | **conflict** — see Requires decision | This is the "don't build a KB at all" position; mutually exclusive with primitives #1–#7 as the *primary* surface. Hybrid is conceivable but the user has not chosen. |
| 13 | Vendor regtech corpora (Thomson Reuters Practical Law AU, LexisNexis, CCH, RegRoom) | outside-view gap #5 (build-vs-buy not surveyed) | **conflict** — see Requires decision | Build-vs-buy is unresolved; vendor corpora subsume #1–#7 if licensable, but introduce licensing/egress constraints the user has not addressed. |
| 14 | Refresh / invalidation pipeline keyed to regulator publication cadence | frame B; outside-view ("12% stale-decision" healthcare datum; lift condition #2) | **extend** | Frame-revised optimization names freshness as a top-3 metric. Standalone because it is orthogonal to retrieval shape and is the artifact, not the snapshot. |
| 15 | Citation / version-anchoring schema (instrument + section + version + effective-date) | frame D; outside-view gap #6; canon §7 (CitationAgent pattern) | **extend** | Provenance is non-optional in regulated AU domain; standalone because it is a contract every downstream answer must satisfy regardless of retrieval choice. |
| 16 | Eval harness with gold Q/A set (BigLaw-Bench-style, version-anchored) | outside-view (lift condition #3, "evals before silo"); canon gap #1 | **extend** | Frame C makes this the first artifact, not the last; standalone because without it none of #1–#15 can be ranked. |
| 17 | Tool-retrieval layer (which-tool-to-call) | outside-view (emerged late-2025 as distinct problem) | **extend** | Once #10 is in, scaling past ~hundreds of tools requires a meta-retrieval step; standalone because it operates on tool descriptions, not documents. |
| 18 | Human-in-the-loop / approval gate for regulated answers | canon gap #3 | **extend** | Regulated-domain requirement orthogonal to retrieval; standalone because it is a control-flow primitive on the answer path, not on the retrieval path. |

## Deletion cost (for replace rows)

- **#1 Naive vector-DB RAG:** callers = none yet (greenfield); deletion cost is rhetorical — must be argued against in the design doc because it is the LLM-default mental model the user implicitly proposed. Blast radius if a team ships it anyway: 5.7% baseline top-20 failure floor, no provenance schema, staleness blind-spot.
- **#8 Long-context replacement:** deletion cost = forfeit the "no retrieval pipeline" simplicity story; must replace with retrieval architecture. Cost envelope: at $15/query × consumer-banking volume this dies on cost before it dies on recall.
- **#9 Custom domain LLM:** deletion cost = forfeit the "owned model" narrative; replace with frontier-model + RAG. Blast radius: ~7-figure training spend avoided, frontier-model dependency accepted.

## Requires decision (conflicts)

- **#5 GraphRAG vs hybrid (#2):** both can coexist technically, but defaulting GraphRAG-in adds index-build cost, schema curation, and a multi-hop query mix the user has not characterized. Decision needed: is the month-1 query mix multi-hop schema-heavy (defined-term webs, supersession chains) or factoid (rates, thresholds, RG numbers)? Without this, the relationship cannot be assigned.
- **#10 Agentic retrieval vs cost envelope:** canon C3 names the conflict directly — multi-agent ≈ 15× chat tokens; "economic viability requires high-value tasks." For consumer-facing banking Q&A at retail volume, agentic retrieval is uneconomic; for compliance-officer or banker workbench it is justified. Decision needed: which consuming agent.
- **#11 Filesystem-as-store vs vector index:** Anthropic's stance generalizes from a coding corpus (Claude Code over a repo). A 10⁶-page regulator corpus across heterogeneous publishers is not obviously the same shape. Decision needed: is the corpus filesystem-shaped (one canonical tree per regulator, stable paths) or graph-shaped (cross-references, supersessions)?
- **#12 Live federation vs built KB:** mutually exclusive as the *primary* surface. Decision needed: are APRA/ASIC/AUSTRAC/Federal Register APIs (a) available, (b) rate-limit-tolerable for read-time agent traffic, (c) versioned in a way that supports point-in-time queries? If yes to all three, #12 subsumes #1–#7.
- **#13 Vendor regtech vs build:** decision needed: is licensing a vendor corpus (and accepting their citation schema and refresh cadence) cheaper than building #6 + #14 + #15 in-house? The outside-view explicitly flagged this as un-surveyed.

## Preserved primitives with stated reason (non-default)

None. Every `extend` row above earns standalone existence by named technical reason (different stage of the pipeline, different control surface, different contract), not by ownership or continuity. There are no primitives preserved for political or backwards-compatibility reasons because there is no incumbent stack.

## Primitives the distillations did not name but the query implies

- **PII / data-residency controls (APP, CPS 234).** Canon librarian flagged the gap; not in the candidate menu but a regulated-AU build will need it.
- **Multi-jurisdiction handling (NZ/SG/HK for AU bank subsidiaries).** Outside-view named this as a gap; affects metadata schema #6.
- **Cost-per-query budget primitive.** Outside-view explicitly flagged absence; the agentic-vs-static choice (#10) cannot be made without it.
- **Latency budget (p95) for the consuming agent.** Outside-view flagged absence; reranker (#4) and agentic (#10) both consume this.
- **Defined-term / supersession-chain resolver.** Implied by "30–60% of banking documents are tables/defined-term webs" but not surfaced as a distinct primitive in either distillation.

These are candidates for a follow-up Explore or a second canon pass; the orchestrator decides whether to re-scope before generation.
