# Research — SOTA architecture for the topical knowledge-retrieval tool

_Phase research folder. Created 2026-06-01. This is the go-to folder for the architecture-decision phase of the [topical-MCP-silo specimen](garden/specimen/2026-05-05-topical-mcp-silo-slot/README.md)._

The question: **what is the proven, expert-recommended SOTA way to build a topical knowledge-retrieval tool (quick, accurate, relevant retrieval over local docs + websites + databases, consumed by an AI agent) — MCP or otherwise?** Six independent research axes were run in parallel; this folder holds their cited findings and the converged recommendation.

## The answer (executive)

> **An owned, thin, eval-driven hybrid-retrieval core — dense embeddings + BM25 fused with RRF, Anthropic-style contextual chunk augmentation at index time, and a cross-encoder reranker — exposed to agents as an MCP server with a single provenance-returning search tool, with graph and agentic layers gated OFF by default.**

It does **not** have to be MCP at the core — the load-bearing artifact is the owned `retrieve(query)` core and the `{source_url, content}` chunk contract; MCP is the recommended-but-swappable delivery surface (now a Linux Foundation standard). The accuracy is won in the **hybrid + rerank + eval** layer, not in tool/vendor choice. Six axes and the prior 2026-04-25 session converged on this — the convergence is the signal. Full decision, stage-by-stage table, and rejected alternatives: **[07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md)**.

## Files

| # | File | What it covers | Verdict in one line |
|---|---|---|---|
| 00 | [00-source-map-au-banking.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/00-source-map-au-banking.md) | First-instance source strategy (S2a regulator probe) | Federate the law (FRL API, point-in-time free); build-and-version the guidance |
| 01 | [01-interface-surface.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/01-interface-surface.md) | How the tool is exposed to an agent | MCP single-tool over an owned HTTP core; plain REST until a 2nd consumer |
| 02 | [02-core-retrieval.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/02-core-retrieval.md) | Chunking, embeddings, hybrid | Contextual chunks → voyage-3.5/Qwen3 → dense+BM25+RRF; BM25 is mandatory |
| 03 | [03-reranking-advanced.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/03-reranking-advanced.md) | Rerank, late-interaction, query transforms | Broad retrieve → RRF → cross-encoder rerank; HyDE harmful for precise lookup |
| 04 | [04-graph-agentic-rag.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/04-graph-agentic-rag.md) | GraphRAG, agentic RAG | Both OFF by default; graph ON only if entity-dense + ≥15–20% multi-hop (lazy variant); agentic stays in the caller |
| 05 | [05-infrastructure-buildvsbuy.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/05-infrastructure-buildvsbuy.md) | Vector stores, frameworks, build-vs-buy | pgvector/Qdrant + BM25, no heavy framework, build thin in-house |
| 06 | [06-proven-deployments-experts.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/06-proven-deployments-experts.md) | What leaders actually run/recommend | Hybrid+rerank+eval is shipped as the default by every major cloud; convergent |
| 07 | [07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md) | **The converged single recommendation** | The decisive document — read this one |

## Sub-axis: anti-hallucination

A dedicated five-axis sub-study on how the tool resists hallucination — built into the tool *and* as a harness around the consuming agent. Converged answer: three-layer defense-in-depth (structural citation + abstention in the tool; claim-level verification in a harness; calibrated abstention + measurement as a policy wrapper). See **[anti-hallucination/README.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/README.md)** and its [recommendation](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/06-recommendation.md).

## How this was produced

Six parallel research agents (general-purpose, web-enabled), one per axis, each required to: prioritise authoritative 2025–2026 sources, cite every non-obvious claim with URL + date, name proven adopters, surface ≥1 contrarian view, and obey repo path discipline. Outputs verified on disk (1,300+ lines, path-clean) and cross-checked for convergence before synthesis. Vendor-reported magnitudes are flagged as directional, not portable — see the anchor-risk section of [07](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md).

## Where this sits in the roadmap

This folder completes the **architecture decision** that precedes the build. Remaining Phase-1 work: the **gold Q/A eval set (S2b)** — the real SOTA lever, and what the architecture is then tuned against. No retrieval code is written until the eval harness can grade it.
