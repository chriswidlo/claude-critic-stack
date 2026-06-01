# Research — anti-hallucination architecture

_Created 2026-06-01. Sub-axis of the [phase research folder](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/README.md). Five parallel research agents + one converged recommendation._

The question: **how should anti-hallucination be built — into the retrieval tool, or as a harness around the agent when it uses the tool?** The answer is **both**: defense-in-depth across three layers, each catching a failure class the prior layer structurally cannot.

## The answer (executive)

> **Three layers.** (1) *In the tool:* verbatim `cited_text` + per-chunk provenance + a tool-owned calibrated abstention signal (`match_quality` / `no_confident_match`). (2) *Harness around tool use:* a generator + separate-verifier two-model pattern running fast **claim-level** faithfulness checks inline (block-and-fallback), escalating borderline cases to an LLM judge. (3) *Policy wrapper:* calibrated abstention, human-in-the-loop on regulated triggers, and continuous measurement against an in-domain gold set. **Invariant:** every check consumes new external evidence, never the model's own text. **Honest ceiling:** this reduces and bounds hallucination and fails safe — it is not a guarantee, and you publish a measured rate, never a "hallucination-free" claim.

Full decision, the tool-vs-harness split table, and the extended chunk contract: **[06-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/06-recommendation.md)**.

## Files

| # | File | Layer | Verdict in one line |
|---|---|---|---|
| 01 | [01-in-tool-grounding-citation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/01-in-tool-grounding-citation.md) | Tool | Anthropic `search_result` blocks → verbatim `cited_text` kills *reference* hallucination; tool owns the abstention signal |
| 02 | [02-faithfulness-verification.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/02-faithfulness-verification.md) | Harness | Claim-level two-tier verifier (small detector inline + LLM-judge async); the lever is the in-domain gold set, not the model |
| 03 | [03-agentic-self-correction.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/03-agentic-self-correction.md) | Tool + caller | CRAG evaluator + bounded re-retrieval in tool; conformal abstention; deep verification opt-in to caller; never self-correct without new evidence |
| 04 | [04-guardrail-frameworks-architecture.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/04-guardrail-frameworks-architecture.md) | Harness | Generator+verifier two-model; tiered cascade keyed at the MCP boundary; harness = risk reduction + logging + HITL, not a guarantee |
| 05 | [05-proven-deployments-measurement.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/05-proven-deployments-measurement.md) | All | Anthropic/Harvey/kapa.ai/Perplexity converge on claim-level grounding + mandatory abstention + measured rate; hallucination is inherent |
| 06 | [06-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/anti-hallucination/06-recommendation.md) | — | **The converged three-layer recommendation — read this one** |

## How this was produced

Five parallel web-enabled research agents, one per axis, each required to prioritise authoritative 2025–2026 sources, cite every non-obvious claim with URL + date, name proven adopters, surface ≥1 contrarian view, and use external-URL links only. Outputs verified on disk (1,213 lines, path-clean) and cross-checked for convergence before synthesis. Vendor-reported magnitudes (Endex 10%→0%, Harvey 0.2%, AWS "99%", HHEM positions) are flagged as inaccessible-comparator anchors to re-validate on the AU eval set.

## How it connects to the rest of the phase

- **Extends the chunk contract** from the retrieval architecture in [07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md) with `cited_text`, `match_quality`, and provenance.
- **Reuses the gold eval set (S2b)** as the measurement gate — and adds the requirement that the gold set include deliberately-unanswerable "abstain" questions.
- The harness layer is **corpus-agnostic**, so like the retrieval core it is part of the reusable slot, not the AU-banking instance.
