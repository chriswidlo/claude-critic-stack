# Decision Log

## Loop 1 — after critic-panel on recommendation-v1

Step 10 verdicts:
- critic-architecture = **reject** (verifier is a cross-cutting concern masquerading as a module; cross-family verifier is a wager dressed as topology; stack↔pipeline cycle).
- critic-operations = **rework** (no cost-cap enforcement primitive; no rollback; no observability; framed as composition when it is a lifecycle problem under 60–90 day substrate churn).
- critic-product = **reject** (no mode-chooser UI; "refuse to ship one-command" is paternalism; per-claim bucket badges add cognitive load without an action affordance; "the question is unanswerable" is the orchestrator dodging).

Routing: **rewrite**, not replan. The lenses accept the S/D/P insight in spirit but reject the surface and the load-bearing engineering choices. Routed to step 9 with all three lenses' objections in hand. The frame remains intact; the recommendation regenerates.

Key changes for v2 forced by the panel:
1. Mode S becomes the **default**, not a co-equal option. Outside-view's base rates support this directly; the v1 fork was analyst-fiction.
2. The cross-family verifier is **dropped** as the architectural spine. Replace with on-disk-artifact verifier (producer→claims.jsonl, verifier→verification.jsonl) only when the user opts into Mode D for a specific run.
3. The stack↔pipeline cycle is **broken**: critic-panel is invoked post-result on demand, not as a pipeline consumer.
4. Mode D ships as a **one-command opt-in** with cognitive guardrails (bucket badges, latency/cost meter visible in result), not as gated interrogation.
5. Mode P is repositioned as a **result-shape** ("here are 12 ranked sources, you synthesize") accessible from the same `/research` entry, not a separate mode the user must pre-classify into.
6. Pair Mode D with a **quarterly re-validation routine** as a non-optional condition of adoption (operations critic).
7. Add **shadow-mode** for the verifier (one week log-only) before it is allowed to fail a run (operations critic).
8. Honestly name the **gaps the recommendation cannot fill** with current Claude Code primitives (cost cap enforcement, hook concurrency arbiter, run-log persistence).
