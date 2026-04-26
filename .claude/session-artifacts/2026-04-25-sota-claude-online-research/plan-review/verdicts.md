# Plan v3 — Panel Verdicts

| Lens | Verdict | Strongest single objection |
|---|---|---|
| outside-view | **below base rate** | Frequency-conditional self-administered protocols with no calibration mechanism, no instrumentation, and no enforced cadence are unreliable in solo use, regardless of how well the regimes are designed. ~60% of users land in regime 1 and the plan delivers value indistinguishable from "do nothing." |
| architecture | **rework** | Regime 3's verifier is a screen-scraper of vendor Markdown masquerading as a module. The v2 critique was "claims.jsonl has no owner"; v3's response transferred ownership to a vendor with no contract and no notification channel — strictly worse. Use the hosted engine's structured API, not its Markdown. |
| operations | **rework** | Regime selection is treated as user-introspection when it is a measurement problem. Self-report over 8 weeks for "load-bearing" research is unreliable and the plan ships zero telemetry to detect misclassification. The dropped quarterly Routine must be reinstated — not as a policy, as the only remaining drift-detection mechanism. |
| product | **rework** | Regime 1 = "use Anthropic Research, attach a mental disclaimer" delivers product-shape delta of zero from "do nothing." A mental disclaimer is not a product surface; it is offloading the trust contract onto the user's working memory. |

## Convergent objections (raised by ≥2 lenses)

1. **Volume-as-axis is a category error.** Architecture: volume conflates consequence × domain-volatility × error-correlation. Operations: volume is a measurement problem the user cannot self-report. Product: the survey-once approach has no in-product chooser.
2. **No measurement loop.** Operations: regime drift is undetectable. Outside-view: solo users do not actually re-evaluate quarterly. Product: nothing reminds the user to re-run the survey.
3. **Checklist-as-file is aspirational.** Product: the user will not open it at query 50. Outside-view: ~25% follow the protocol past the first few queries; rest silently lapse.
4. **Build estimate understated.** Operations: 4–8 hours, not 1–2. Outside-view: planning fallacy on solo dev tooling, 3–10× overruns are typical.
5. **The regime-1 path = "do nothing"** problem. Outside-view: success-by-vacuity. Product: zero affordance delta.

## Concrete fixes the panel converged on

- **Use the hosted engine's structured API**, not its Markdown (architecture).
- **Ship at least one in-product affordance for regime 1** — a `/research` slash command that wraps the hosted call and appends the disclaimer to the output, so the contract is in the artifact, not in the user's head (product).
- **Make the regime-2 checklist a slash command that prints at query time**, not a file the user must remember to open (product).
- **Reinstate a minimal quarterly Routine as a measurement control** (not a policy): count actual `/verify-research` invocations and surface the implied regime alongside the user's stated regime; flag divergence (operations).
- **Replace the self-report count with a 2-week observation period** before answering the triage question. Log every load-bearing query, then count (outside-view).
- **Cap regime 3 entry behind a sunk-cost gate**: must run regime 2 for 4 weeks at the regime-3 threshold before building the verifier (outside-view).
- **Make snapshots write-once, content-addressed by (URL, fetch-time)**, with location semantics named (local-only, not iCloud-synced) (architecture, operations).
- **Add fail-closed parse semantics**: extracted-claim-count must be sanity-checked against a footnote-marker heuristic; abort on mismatch rather than silently report "0/0 verified" (architecture).
- **Name the 3am runbook**: what does the regime-3 user do when the verifier reports `fetch-failed` on 80% of a load-bearing report mid-decision? (operations).
- **Define synthesis-claim disposition**: what does the verifier do with "X and Y therefore Z" claims that have no atomic citation? (architecture).

## Net assessment

Three rework verdicts plus a below-base-rate outside-view forecast. **The plan I vouched for did not survive the panel.** The objections are specific and actionable, not frame-level — meaning a v4 *could* address them — but the convergent message is that the failure is not in the regime definitions; it is in the **assumption that a self-administered protocol with no measurement primitive can guide solo-user behavior**. Fixing v3 by piling on more affordances (slash command for the checklist, structured API parser, measurement Routine) re-introduces the engineering bloat I was trying to escape.
