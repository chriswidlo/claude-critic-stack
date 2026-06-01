# Topical-MCP-silo as a repo capability

| Field | Value |
|---|---|
| 📌 **title** | Topical-MCP-silo as a repo capability |
| 🎯 **category** | 🌳 specimen |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-05 |
| ⚡ **catalyst** | Session `2026-04-25-au-banking-kb-sota` and the deeper survey at `.claude/session-artifacts/2026-04-25-au-banking-kb-sota/research-rag-patterns.md`. The Temporal MCP at `temporal.mcp.kapa.ai` is the worked-example anchor — adding it to Claude Code dramatically improves any Temporal-related task by exposing one typed narrow tool over the vendor's docs. |
| 💡 **essence** | The kapa.ai shape (one MCP server per topical knowledge silo, exposing a single tool that returns `{source_url, content}` chunks, backed by hybrid + contextual retrieval + rerank) is a *replicable slot*, not a one-off. The slot multiplies cleanly: each new topic is a configuration exercise, not a project. The repo's existing `canon-librarian` is the embryonic in-stack form of the same shape. |
| 🚀 **upgrade** | A standardized topical-MCP-silo capability inside this repo: a build pipeline (source registry → ingest → contextualize → embed → index → hybrid+rerank retrieval → MCP-over-HTTP surface) plus a chunk-contract every silo respects. Once the scaffold exists, any topical knowledge surface (AU banking, claude-code internals, vendor docs of any kind) is a config-and-corpus addition. The first instance built end-to-end (most likely AU banking, by stress-test logic) proves the slot. |
| 🏷️ **tags** | mcp, knowledge-tools, rag, retrieval, infrastructure, slot |
| 🔗 **relates_to** | 2026-04-26-corpus-bias-compensation-step, 2026-04-26-citation-audit-as-canon-discipline |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-05 | 2026-06-01 | 2026-06-01 | 2026-06-01 | — | — | — | — | — | — |

## Table of contents

- [Progress — 2026-06-01 (architecture decided, build accepted)](#progress--2026-06-01-architecture-decided-build-accepted)
- [The seeing — what kapa.ai actually is](#the-seeing--what-kapaai-actually-is)
- [Why this is a slot, not an instance](#why-this-is-a-slot-not-an-instance)
- [The chunk contract — the only thing that must be invariant](#the-chunk-contract--the-only-thing-that-must-be-invariant)
- [Backend is a per-corpus choice, not a slot decision](#backend-is-a-per-corpus-choice-not-a-slot-decision)
- [Why this is outlandish — honest scoping](#why-this-is-outlandish--honest-scoping)
- [Open questions](#open-questions)

## Progress — 2026-06-01 (architecture decided, build accepted)

> **Status: ✅ accepted.** Operator directed the full build, AU banking as the first instance. This block records progress since the seed below; the original body is kept as historical record, and where the two conflict, this block is current.
>
> Accepted by operator 2026-06-01.

### Probe & research (spiked)

Two deep research passes (parallel sub-agents; all findings on disk, path-clean) — see the phase folder [research/README.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/README.md):

- **SOTA tool architecture** — converged on an owned, thin, eval-driven hybrid-retrieval core (contextual chunks → dense + BM25 + RRF → cross-encoder rerank) exposed via MCP. The kapa shape is the proven default; *build thin, own the core* beats managed RaaS for citation-exact regulated content. Decision: [research/07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md).
- **Anti-hallucination** — three-layer defense-in-depth: in-tool citation + abstention; a claim-level verifier harness around tool use; abstention + measurement as a policy wrapper. Decision: [research/anti-hallucination/06-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/06-recommendation.md).
- **Regulator-API probe (AU banking)** — federate the law (Federal Register of Legislation API, point-in-time free), build-and-version the guidance (APRA / ASIC / AUSTRAC). Source map: [research/00-source-map-au-banking.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/00-source-map-au-banking.md).

### Open questions from the seed — now resolved

- *AU banking vs claude-code first* → **AU banking** (operator choice; hardest stress test).
- *Is the minimal chunk contract enough?* → **No — enrich it.** The contract grows from `{source_url, content}` to add `cited_text`, `match_quality`, and provenance (`instrument_id, section, version, effective_date, superseded`). Load-bearing for a regulated domain and for anti-hallucination.
- *In-repo vs sibling repo* → **staged**: the vertical slice (S1) builds in this repo; production (S3) is a sibling repo.
- *Backend tier for the AU instance* → self-host thin (pgvector/Qdrant + `bm25s` + `sentence-transformers` + FastMCP), not managed.

### Plan — three-stage roadmap (next steps)

Each stage is a hard gate on the next: complete and fact-based before the next begins.

| Stage | Name | Done-gate |
|---|---|---|
| **S2** (now) | Probe + eval harness | regulator probe ✅ · architecture decided ✅ · **remaining: ~50-pair version-anchored gold Q/A set, including deliberate "abstain" cases** |
| **S1** | Slot scaffold + AU vertical slice | thin owned core over a bounded free source subset (APRA standards built + Banking Act federated), graded against the S2 gold set, exposed via MCP with the enriched chunk contract |
| **S3** | Production scale-up | full corpus, refresh SLAs, audit, liability gating; sibling repo |

**Immediate next step: S2b — the gold eval set.** No retrieval code is written before it exists: the eval set is the SOTA lever (every expert says so) and the decider for whether GraphRAG is switched on (≥15–20% multi-hop).

## The seeing — what kapa.ai actually is

Kapa.ai runs the full RAG stack as a managed service. A vendor (Temporal, Redpanda, dozens of others) connects their docs, GitHub, Slack, forums; kapa runs ingest, chunking, embedding, hybrid retrieval, rerank, refresh. They expose the result through several surfaces — chat widget, API, Slack bot, and the relevant one here, a hosted MCP server at `<subdomain>.mcp.kapa.ai`. The MCP exposes **one tool** — `search_<PRODUCT>_knowledge_sources` — returning a list of `{source_url, content}` chunks. That is the entire surface.

The reason `claude mcp add --transport http temporal-docs https://temporal.mcp.kapa.ai` dramatically improves Claude's work on any Temporal-related task is four mechanisms compounding:

1. The tool's *name* tells the agent when to use it (ACI principle).
2. Returned chunks are evidence the agent reasons over, not generated answers.
3. The corpus is curated and bounded — it *is* the trust boundary.
4. The vendor handles freshness; the consumer carries no refresh burden.

Hidden behind that one obvious tool: four hard layers (source catalog, ingest pipeline, retrieval substrate, citation/audit) productized invisibly. That's why it feels like magic — the four hard layers are eaten and only the obvious one is consumer-visible.

## Why this is a slot, not an instance

If you build it once for one topic, you have a knowledge tool. If you build it as a *slot* — a standardized scaffold any new topical corpus can drop into — you have a repo capability. The second-through-Nth silo cost goes from "months" to "configuration."

The shape of the slot:

```
ONE MCP SERVER PER TOPICAL KNOWLEDGE SILO
  - exposes ONE tool: search_<TOPIC>_knowledge(query)
  - returns: list of {source_url, content} chunks (kapa contract)
  - backed by: source registry → ingest pipeline → INDEX → retrieval pipeline
  - refreshed on a topic-appropriate cadence
  - audited via source URLs (provenance is structural, not optional)
```

A new topic = a new source registry + a new index + an MCP route. The pipeline code, the chunk contract, the auth, the rate limiting — all reused.

## The chunk contract — the only thing that must be invariant

Every silo, regardless of backend, returns the same shape:

```json
[
  {"source_url": "<authoritative URL with version anchor if available>",
   "content":    "<chunk text in markdown>"},
  ...
]
```

Ranked descending by relevance. No generated answer. No model-side reasoning baked in. The agent reasons over the chunks. This contract is what makes silos interchangeable from the agent's perspective and what makes the slot composable.

## Backend is a per-corpus choice, not a slot decision

The backend behind the chunk contract is *not* part of the slot's invariants. Different corpora deserve different backends:

- **Tiny / curated** (canon-scale, dozens of files) → grep over markdown. The current `canon-librarian` shape. Don't add complexity.
- **Medium / vendor-shaped** → managed kapa.ai if budget allows; self-hosted Qdrant/Chroma MCP server otherwise.
- **Huge / multi-source / pipeline-control needed** → self-host the full stack: hybrid (BM25 + dense via Qdrant or Turbopuffer) + Anthropic Contextual Retrieval at index time + Voyage rerank-2.5. Wrap in MCP-over-HTTP.

The slot's contribution is making this a per-corpus *choice* rather than a per-corpus *project*.

## Why this is outlandish — honest scoping

Three reasons this is filed as outlandish, not normal:

1. **Effort.** A first-instance end-to-end build (eval harness → source registry → ingest → contextualize → embed → index → hybrid+rerank → MCP server → refresh worker) is months of work even with managed components.
2. **Unproven for our use case.** The kapa pattern is proven for vendor-controlled docs. Government-published, version-anchored content (the AU-banking stress test) is *plausibly* the same shape but hasn't been demonstrated end-to-end in this repo.
3. **Reversibility.** Once silos exist and consumers depend on them, changing the chunk contract or the slot's invariants is expensive. The design choices in v1 will live for years.

Mitigations: build the eval harness *first*, build one instance end-to-end before generalizing, keep the chunk contract narrow, and treat the slot as v0 — invariants can be revised before the second silo lands.

## Open questions

- Should the first instance be AU banking (high-stress, validates the pattern hardest) or claude-code internals (low-stakes, fastest feedback loop)? The stress-test logic favors AU banking; the iteration-speed logic favors claude-code.
- Does the slot belong inside this repo, or as a sibling repo? `2026-04-26-research-stack-as-sibling` raises a structurally similar question for the workflow stack.
- How does the slot relate to Anthropic's Skills / Tool-Search direction (where *tools themselves* become indexed knowledge)? If Tool-Search becomes the dominant 2026 pattern, MCP-per-silo may need to compose with it rather than stand alone.
- What is the right authentication model? Public OAuth (kapa-style) makes silos cross-team usable but adds operational surface; API key is simpler but locks consumption to known parties.
- Is the chunk-contract enough, or do we need a richer return shape (e.g., `effective_date`, `version`, `confidence`) for regulated-domain silos? The kapa contract is deliberately minimal; the previous session's synthesis argued some consumers need more.
