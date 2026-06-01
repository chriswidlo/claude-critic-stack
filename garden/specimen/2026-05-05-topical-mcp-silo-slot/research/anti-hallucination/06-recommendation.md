# Recommendation — the anti-hallucination architecture

_Synthesised 2026-06-01 from the five axes in this folder (01–05). Integrates with the retrieval architecture in [07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md)._

This answers the question directly: **anti-hallucination is not one mechanism in one place — it is defense-in-depth across three layers, half built *into the tool* and half built as a *harness around the agent's tool use*.** Each layer catches a failure class the layer before it structurally cannot see. The governing principle, repeated independently by every axis: **the system must abstain rather than guess, and it must publish a measured, bounded, audited hallucination rate — never a "hallucination-free" claim.**

## Table of contents

- [The one-paragraph answer](#the-one-paragraph-answer)
- [The three layers — and what each catches](#the-three-layers--and-what-each-catches)
- [Layer 1 — in the tool (structural grounding)](#layer-1--in-the-tool-structural-grounding)
- [Layer 2 — the harness around tool use (verification)](#layer-2--the-harness-around-tool-use-verification)
- [Layer 3 — policy and measurement (the regulated-domain wrapper)](#layer-3--policy-and-measurement-the-regulated-domain-wrapper)
- [Built-in-tool vs harness — the explicit split](#built-in-tool-vs-harness--the-explicit-split)
- [How it extends the chunk contract](#how-it-extends-the-chunk-contract)
- [The honest ceiling](#the-honest-ceiling)
- [Rejected / deferred and flip conditions](#rejected--deferred-and-flip-conditions)

## The one-paragraph answer

Build anti-hallucination as **three layers**: (1) **in the tool**, return chunks as Anthropic-style `search_result` content blocks with verbatim `cited_text` plus per-chunk provenance, and have the *tool itself* own a calibrated abstention signal (`match_quality: high|low|none`) so it returns a structurally distinct "no confident match" state instead of a weak chunk; (2) **as a harness around the agent's tool use**, run a fast claim-level faithfulness verifier — decompose the answer into atomic claims, bind each to a cited chunk, and check each with a small specialized detector inline (block-and-fallback), escalating only borderline cases to an LLM judge; (3) **as a policy + measurement wrapper**, gate on calibrated abstention (refuse/escalate when grounding is absent), route regulated triggers to a human, and continuously measure claim-level faithfulness + citation coverage + abstention rate against an in-domain gold set. The non-negotiable invariant across all of it: **every correction or verification step consumes new external evidence, never the model's own prior text.** This is the convergent practice of Anthropic (Citations), Harvey, kapa.ai, Perplexity, and Glean, and it is risk reduction — not a guarantee.

## The three layers — and what each catches

| Layer | Where it lives | Failure class it catches | Why the prior layer can't |
|---|---|---|---|
| **1. Structural grounding** | In the tool | *Reference* hallucination (fabricated/miscited sources) | n/a — first line |
| **2. Faithfulness verification** | Harness around tool use | *Unfaithful synthesis* (cited source exists but doesn't support the claim) | citations guarantee the quote is real, not that the answer follows from it — 50–90% of cited responses are not fully supported (axis 01) |
| **3. Abstention + measurement** | Policy wrapper | *Answering the unanswerable* (confident answer when evidence is absent) | a verifier scores what was said, not whether anything should have been said; abstention must be a first-class action (axis 03, 05) |

## Layer 1 — in the tool (structural grounding)

The strongest cheap win, because it makes a whole failure class *structurally* impossible rather than statistically rarer.

- **Verbatim citations.** Return retrieved chunks as Anthropic `search_result` content blocks with `citations.enabled: true`. The model's answer then carries `cited_text` that is guaranteed-verbatim from the source — reference hallucination becomes structurally impossible. Proven: Endex cut source hallucinations ~10% → 0% via the Citations API; Thomson Reuters CoCounsel uses it for legal/tax. (axis 01)
- **Provenance per chunk.** Every chunk carries `instrument_id, section, version, effective_date, source_url, retrieved_at, superseded?`. For AU banking this is load-bearing and the [federated FRL source](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/00-source-map-au-banking.md) supplies most of it directly.
- **The tool owns abstention.** A calibrated threshold on the rerank score maps to a `match_quality` enum (`high|low|none`); below threshold the tool returns a structurally distinct `no_confident_match` state, not a weak chunk. This must live in the tool because abstention *cannot* be left to the consumer — AbstentionBench (NeurIPS 2025) found reasoning fine-tuning *degrades* a model's abstention by ~24%. (axis 01)
- **One bounded corrective re-retrieval.** A CRAG-style lightweight retrieval evaluator may trigger exactly one bounded re-retrieval **against the curated corpus only — never the open web**. CRAG posts the largest measured single-technique wins (+19% PopQA; +36.6% PubHealth on a 7B base). (axis 03)

## Layer 2 — the harness around tool use (verification)

This is the "AI harness around the AI when it uses the tool" the requirement asked for. It is a **generator + separate-verifier (two-model) pattern**, with the verifier keyed on the retrieval context captured at the MCP boundary.

- **Claim-level, not response-level.** Decompose the answer into atomic claims; bind each to the chunk it cites; verify each claim against that evidence. Claim-level is what Harvey runs (measured ~0.2% claim-level hallucination). (axis 02, 05)
- **Tiered verifier cascade.** A fast encoder/NLI detector on *every* response (Galileo Luna-2 or Vectara HHEM, ~150–200ms; or Bespoke-MiniCheck-7B, ~GPT-4 grounding accuracy at 1/100–1/400 the cost), escalating only borderline scores to an explainable LLM judge (Patronus Lynx, or a managed grounding check). Inline, **block-and-fallback**. (axis 02, 04)
- **Placement.** Run the verifier as an output rail keyed on the context returned by the MCP `search` call (an `mcp_post_tool`-style hook). Sharp caveat from axis 04: NeMo Guardrails' standard input/output rails *cannot see MCP tool-call arguments* — argument-level checks must wrap the tool directly.
- **Numeric/tabular claims get a deterministic check.** General entailment detectors degrade on finance/regulation; a figure cited from a table needs an exact check, not an NLI score. (axis 02)
- **The invariant.** Every verification/correction step consumes *new external evidence*. Intrinsic self-correction (model re-reading its own output with no new evidence) leaves accuracy flat or *degrades* it (Huang et al., ICLR 2024) — the bottleneck is error *localization*, not fixing. (axis 03)

## Layer 3 — policy and measurement (the regulated-domain wrapper)

- **Calibrated abstention policy.** Use conformal abstention to put a distribution-free statistical ceiling on the hallucination rate while minimising needless refusals (DeepMind, arXiv 2405.01563). The tool emits the below-threshold signal (Layer 1); the *caller* owns the abstain / ask-for-clarification / escalate policy. (axis 03)
- **Human-in-the-loop on regulated triggers.** If the answer crosses a personal-advice / liability threshold, route to human review — this is the Frame E concern from the prior session, carried structurally.
- **Continuous measurement on an in-domain gold set.** Track claim-level faithfulness, citation coverage, and calibrated abstention rate. Offline gold-set gate + a cheap distilled online detector. Build target: ~1k in-domain labelled examples → ROC-AUC ~0.85 (Eugene Yan). **The gold set must deliberately include unanswerable questions whose correct answer is "abstain"** — otherwise you train confident guessing (OpenAI/Kalai, 2025). This reuses and extends the **S2b gold Q/A set**. (axis 05)

## Built-in-tool vs harness — the explicit split

The requirement asked whether this is built into the tool *or* a harness. The answer is **both**, by design:

| Mechanism | Tool | Harness (caller-side) | Rule |
|---|---|---|---|
| Verbatim `cited_text` + provenance | ✅ | | cheap, evidence-local, deterministic → tool |
| `match_quality` / `no_confident_match` signal | ✅ | | abstention signal must be tool-owned (AbstentionBench) |
| CRAG retrieval evaluator + 1 bounded re-retrieval | ✅ | | evidence-local → tool |
| Claim-level faithfulness verifier (two-model) | | ✅ | spans the whole answer → caller/harness |
| Abstain / clarify / escalate **policy** | | ✅ | goal-level decision → caller |
| CoVe / RARR deep claim re-verification | | ✅ (opt-in via `verification_level`) | generator-token-heavy → caller, opt-in |
| Measurement + gold-set gate | | ✅ | system-level → harness |

Split rule (from axis 03): **cheap + evidence-local + deterministic → the tool; goal-level + answer-spanning + generator-token-heavy → the caller.** "Smart about retrieval, dumb about goals."

## How it extends the chunk contract

The prior architecture's chunk contract was `{source_url, content}`. Anti-hallucination extends it to:

```json
{
  "source_url": "<authoritative URL w/ version anchor>",
  "content": "<chunk markdown>",
  "cited_text": "<guaranteed-verbatim span>",
  "match_quality": "high | low | none",
  "provenance": {"instrument_id": "...", "section": "...",
                 "version": "...", "effective_date": "...", "superseded": false}
}
```

…and adds, at the response level (not per-chunk), a `no_confident_match` state the tool can return instead of chunks. The harness layer wraps the consuming agent and is corpus-agnostic — so, like the retrieval core, it is part of the reusable slot, not the AU-banking instance.

## The honest ceiling

Per repo anti-anchoring discipline, stated plainly:

1. **Hallucination is not eliminable.** OpenAI/Kalai et al. (Sept 2025) show statistical pressure + eval incentives reward guessing; Vectara's leaderboard shows a ~2–3% floor even on the easiest grounded task. This architecture *reduces and bounds* the rate and *fails safe* (abstains) — it does not promise zero.
2. **Production regulated RAG still hallucinates.** Stanford RegLab found commercial legal RAG tools (Lexis+, Westlaw) hallucinate **17–33%** despite "hallucination-free" marketing (arXiv 2405.20362). Do not repeat that marketing claim.
3. **The verifier is a correlated second model that can itself hallucinate.** On the hard human-curated FaithBench, *all* methods — including LLM judges — sit near 50% accuracy (axis 02). The load-bearing investment is therefore the **in-domain gold set + abstention**, not the choice of verifier model.
4. **Vendor numbers are inaccessible-comparator anchors.** Endex 10%→0%, Harvey 0.2%, AWS "99%", HHEM leaderboard positions — all vendor-reported on vendor data. Re-validate every figure on the AU-regulation eval set before trusting it.

The deliverable of this layer is therefore **a published, measured, audited hallucination rate with a fail-safe abstention path — not a guarantee.**

## Rejected / deferred and flip conditions

| Option | Status | Flip condition |
|---|---|---|
| In-tool citation *alone* as "the" solution | Rejected | never — solves reference hallucination only, not unfaithful synthesis |
| LLM-as-judge on every response (no small detector) | Rejected for inline | acceptable async/offline; inline only if latency budget is generous |
| RAGAS / TruLens scores as a runtime gate | Rejected | keep them on the *offline* dashboard; they don't correlate well enough to gate on (RAGAS zero-scored 83.5% of FinanceBench, axis 02) |
| Intrinsic self-correction (no new evidence) | Rejected | never — degrades correct answers (Huang et al.) |
| Full agentic verification loop in the tool | Deferred to caller, opt-in | when the caller is *not* itself an agent |
| GraphRAG / heavy structure for grounding | Deferred | inherits the [axis-04 graph condition](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/04-graph-agentic-rag.md): entity-dense + ≥15–20% multi-hop |
| "Just use a bigger model" | Rejected as sufficient | base rate drops but plateaus at a few percent; never zero |

---

**Bottom line:** anti-hallucination is a three-layer, defense-in-depth design — structural citation + abstention *in the tool*, claim-level verification *in a harness around tool use*, and calibrated abstention + measurement *as a policy wrapper* — all gated on the in-domain gold set (S2b) and reported as a bounded, audited rate. It composes cleanly onto the hybrid-RAG + MCP architecture and is itself part of the reusable slot.
