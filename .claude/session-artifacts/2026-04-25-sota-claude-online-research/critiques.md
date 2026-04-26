# Critic Panel — Aggregated Verdicts

## Loop 1 (recommendation-v1)
- **architecture: reject** — verifier is a cross-cutting concern masquerading as a module; cross-family verifier is a wager dressed as topology; stack↔pipeline cycle.
- **operations: rework** — no cost-cap enforcement primitive; no rollback; no observability; framed as composition when it is a lifecycle problem under 60–90 day substrate churn.
- **product: reject** — no mode-chooser UI; "refuse to ship one-command" is paternalism; per-claim badges add cognitive load without an action affordance; "the question is unanswerable" is the orchestrator dodging.

Routing: rewrite. Major changes recorded in `decision-log.md`.

## Loop 2 (recommendation-v2)
- **architecture: rework** — `claims.jsonl` schema has no owner and is implicit-prompt-coupled; URL stability and DAG semantics for synthesis claims undefined; verifier monotonicity not guaranteed; verification should be against frozen page snapshots, not live URLs.
- **operations: rework** — shadow-week pass criteria are vibes-based; quarterly Routine not enforceable as a control; weekly cost ceiling missing; producer's pre-run cost estimate requires N citations the producer doesn't yet know; "no mid-run abort" documented but not mitigated.
- **product: rework** — footer nag taxes every Mode S result; absent-badge ambiguous (verified-passed vs. verifier-didn't-run vs. Mode S); Mode S + ribbon may *be* the product, with Mode D as a power-user extension that should not sit on the default install path.

Routing: **two-loop cap reached; escalate to synthesis with disagreements named** per the workflow.

## Unresolved disagreements carried to synthesis
1. Schema ownership for `claims.jsonl` (architecture).
2. Live-URL vs. frozen-snapshot verification (architecture; this is the strongest single objection still open).
3. Shadow-mode pass criteria as numbers, not vibes (operations).
4. Quarterly Routine enforceability — soft policy vs. hard control (operations).
5. Weekly aggregate cost ceiling on `--audit` (operations).
6. Per-result footer nag — discoverability vs. decision tax (product).
7. Whether Mode D belongs on the default install path or in a separate extension package (product).
