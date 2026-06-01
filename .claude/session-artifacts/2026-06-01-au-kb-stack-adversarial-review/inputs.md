# Inputs actually reviewed

## Under-review artifacts (on disk, read in full)

| Artifact | What it is |
|---|---|
| [synthesis.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/synthesis.md) | Step-12 final synthesis; field-map-first, 5-layer prescription as appendix |
| [candidate.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/candidate.md) | Step-9 generator: the 5-layer architecture in full |
| [research-rag-patterns.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/research-rag-patterns.md) | The deep survey (pattern taxonomy, component landscape, build-vs-buy, sources) |
| [scope-map.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/scope-map.md) | 18 primitives, subsume/replace/extend/conflict |
| [challenges.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/challenges.md) | Frame-challenger: frames A–F, scope-conflict challenges |
| [critiques.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/critiques.md) | Critic panel: 3×rework, unanimous veto |
| [decision-log.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/decision-log.md) | Step-11 routing: rewrite-at-synthesis |
| [outside-view-raw.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/outside-view-raw.md) | Reference-class forecast, failure modes, empirically-supported-vs-buzzword |
| [topical-mcp-silo-slot.md](garden/specimen/2026-05-05-topical-mcp-silo-slot.md) | The generalization: kapa-shape MCP-per-silo as a repo "slot" |

Distillations ([canon-librarian](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/distillations/canon-librarian.md),
[outside-view](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/distillations/outside-view.md))
were read but are downstream of the raw returns above.

## Independent outside sources imported (NOT in the original's citation list)

These are the anti-correlation evidence — academic / third-party, not retrieval-vendor blogs:

1. **Thakur, Reimers, Rücklé, Srivastava, Gurevych — "BEIR: A Heterogeneous Benchmark for
   Zero-shot Evaluation of IR Models" (NeurIPS 2021, arXiv 2104.08663).** BM25 is a strong
   out-of-domain/zero-shot baseline, often outperforming more complex neural retrievers absent
   in-domain training; in-domain performance does not predict out-of-domain generalization.
2. **"Benchmarking LLM Faithfulness in RAG with Evolving Leaderboards" (EMNLP 2025 Industry,
   arXiv 2505.04847).** *"Weak and inconsistent relationship between retrieval quality and
   generation faithfulness"* — high-quality retrieval frequently co-occurs with unfaithful
   generation; grounding does not eliminate unfaithfulness or numeric extrapolation.
3. **Denser.ai — independent replication of Anthropic Contextual Retrieval (2024–25).**
   Reproduced the directional gain (keyword Recall@20 70.48 → 89.26) and matched it with
   open-source models. Caveat: replicated on the *same* Anthropic dataset (code/fiction/arXiv),
   **not** on regulated tabular legal text; and Denser.ai is itself a retrieval vendor.
4. **Federal Register of Legislation (legislation.gov.au) + OPC; ALRC DataHub.** Point-in-time
   *compilations* (law as in force on a date) are a core, free FRL feature. A clean official
   *machine-readable API / OData* for programmatic point-in-time retrieval is **not** clearly
   documented; third-party bulk datasets exist via webscraping (ALRC DataHub). This is the exact
   fact the original left "unverified (uncertainty #2)" — and it remains genuinely unverified.

Full URLs and dates are carried in
[convergence-audit.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/convergence-audit.md).
