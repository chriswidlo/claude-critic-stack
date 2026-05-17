# Requirement classification

## Primary label
investigation

## Default frame (from label)
Frame downstream steps as: *"what would we do differently if we knew the SOTA answer?"* — the user wants a recommendation on storage+retrieval architecture, so the investigation must terminate in a decision-relevant comparison of approaches (e.g., vector RAG vs. graph RAG vs. hybrid vs. agentic retrieval vs. long-context cache), not a literature dump.

## Known frame bias
**Research theater** — producing a survey of retrieval techniques without committing to which one fits "AI-agent-consumed silo for a broad domain corpus," and without naming the conditions under which each approach wins.

## Secondary label
`new` — the user's terminal intent is to build a knowledge silo; the SOTA question is instrumental to that build.

## Alternative classification
`new` — would become primary if the user had already chosen an architectural approach and were asking how to implement it. The frame would then shift to "what shape should this take, and what's the cheapest experiment that distinguishes shapes?" with bias toward over-designing before evidence (e.g., committing to GraphRAG before testing whether plain vector + reranker suffices for the agent's actual queries).

## User's framing words
- *"current SOTA way to construct a knowledge silo"*
- *"such that an AI agent can go to that silo and retrieve any information it needs"*
- *"knowledge silo"* — presumes a single-store architecture; SOTA may actually favor federated or tool-routed retrieval over a monolithic silo.
- *"everything there is to know"* — presumes exhaustive ingestion is desirable; SOTA often favors curated + on-demand fetch.

The label is partly the user's framing — they explicitly ask "what is SOTA" (investigation phrasing) but want an actionable recommendation (decision phrasing). Classification would shift to `new` if the user said "we've decided on approach X, help us build it."

## Gaps
- **Who is the AI consumer?** Single agent, multi-agent, or end-user-facing chatbot? Retrieval shape differs sharply.
- **What query distribution?** Broad lookup, multi-hop reasoning, numerical/regulatory precision, or freshness-sensitive? SOTA is query-shape-dependent.
- **Update cadence:** one-shot snapshot vs. continuously refreshed? Determines whether the silo is a build artifact or a live pipeline.
- **Latency / cost budget** per agent query.
- **Provenance / citation requirements** — banking domain implies regulatory traceability, which could force structured-store + citation-preserving retrieval over pure embeddings.
- **Scale:** GB or TB of source material? Determines whether long-context-cache approaches are even on the table.
- **Is "silo" a hard constraint** (single store, single API) or shorthand for "the agent's knowledge surface" (which could be a router over multiple stores)?

---

> **Reconstruction note.** This artifact was reconstructed from the classifier's verbatim chat return after it was discovered missing during the worktree-branch preservation step (post-synthesis). The agent reported writing this file at step 1 but the harness blocked the write — the same failure mode that hit `outside-view-raw.md` mid-session, except that one was caught in flight and rewritten before the workflow continued. This file was rewritten *after* the workflow completed, transcribed faithfully from the classifier's original output preserved in conversation context. No re-classification was run; doing so post-hoc would have anchored to everything the orchestrator learned downstream and produced a non-faithful reconstruction.
>
> *Reconstructed: 2026-04-26 (one day after session). Original classifier invocation: 2026-04-25.*
