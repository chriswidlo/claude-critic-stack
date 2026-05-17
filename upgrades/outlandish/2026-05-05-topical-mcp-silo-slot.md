# Topical-MCP-silo as a repo capability

| Field | Value |
|---|---|
| 📌 **title** | Topical-MCP-silo as a repo capability |
| 🎯 **tier** | 🚀 outlandish |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-05 |
| ⚡ **catalyst** | Session `2026-04-25-au-banking-kb-sota` and the deeper survey at `.claude/session-artifacts/2026-04-25-au-banking-kb-sota/research-rag-patterns.md`. The Temporal MCP at `temporal.mcp.kapa.ai` is the worked-example anchor — adding it to Claude Code dramatically improves any Temporal-related task by exposing one typed narrow tool over the vendor's docs. |
| 💡 **essence** | The kapa.ai shape (one MCP server per topical knowledge silo, exposing a single tool that returns `{source_url, content}` chunks, backed by hybrid + contextual retrieval + rerank) is a *replicable slot*, not a one-off. The slot multiplies cleanly: each new topic is a configuration exercise, not a project. The repo's existing `canon-librarian` is the embryonic in-stack form of the same shape. |
| 🚀 **upgrade** | A standardized topical-MCP-silo capability inside this repo: a build pipeline (source registry → ingest → contextualize → embed → index → hybrid+rerank retrieval → MCP-over-HTTP surface) plus a chunk-contract every silo respects. Once the scaffold exists, any topical knowledge surface (AU banking, claude-code internals, vendor docs of any kind) is a config-and-corpus addition. The first instance built end-to-end (most likely AU banking, by stress-test logic) proves the slot. |
| 🏷️ **tags** | mcp, knowledge-tools, rag, retrieval, infrastructure, slot |
| 🔗 **relates_to** | 2026-04-26-corpus-bias-compensation-step, 2026-04-26-citation-audit-as-canon-discipline |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-05-05 | — | — | — | — | — | — | — |

## Table of contents

- [The seeing — what kapa.ai actually is](#the-seeing--what-kapaai-actually-is)
- [Why this is a slot, not an instance](#why-this-is-a-slot-not-an-instance)
- [The chunk contract — the only thing that must be invariant](#the-chunk-contract--the-only-thing-that-must-be-invariant)
- [Backend is a per-corpus choice, not a slot decision](#backend-is-a-per-corpus-choice-not-a-slot-decision)
- [Why this is outlandish — honest scoping](#why-this-is-outlandish--honest-scoping)
- [Open questions](#open-questions)

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
