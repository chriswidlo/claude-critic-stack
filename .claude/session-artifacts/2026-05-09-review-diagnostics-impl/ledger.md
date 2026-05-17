# Session ledger — 2026-05-09-review-diagnostics-impl

## Counts

| Category | Count | Source of truth |
|---|---|---|
| Agent calls (subagent invocations) | 15 | classifier (1) + outside-view (1) + canon-librarian (1) + Explore (1) + distillers (3) + scope-mapper (1) + frame-challenger (1) + critic-panel × 2 loops (3 × 2 = 6) |
| Artifacts (markdown files in session dir, excluding ledger.md itself) | 23 | `find <session-id> -name '*.md' -not -name 'ledger.md' \| wc -l` |
| Critic-panel loops used | 2 / 2 | decision-log.md has `## Loop 1` and `## Loop 2` headings |
| Loop cap reached | true | loops used == 2 |
| Decisions in synthesis | 10 | 5 bullets under `## Post-critique recommendation` + 5 numbered items under `## Named uncertainties` |

## Derived ratios

- Agent-calls per decision: 15 / 10 = 1.5
- Artifacts per decision: 23 / 10 = 2.3
- Loops to convergence: 2/2

## Warnings

- ⚠️ candidate needed maximum rework; first-pass framing was off

## Notes

The session's frame-challenger surfaced a strong frame-level objection (workflow-economics, not workflow-observability) that the loop-1 candidate engaged with at the field level rather than the aggregate-boundary level. Loop-2 critics (architecture and operations) returned `rework` again at the cap; the cap-stop routes their disagreements (lock-as-presence vs. lock-as-liveness, missing identity dimension on `metrics.json`, mechanical coupling-debt detector, schema-vs-parser version-skew rule, retention rule for staging/orphan dirs, Phase A→B promotion observable) into synthesis as named uncertainties and named patches rather than another rewrite.

Product flipped from `rework` (loop 1) to `approve` (loop 2) with two named patch suggestions (stub-string threshold leak; deferred-items review cadence), both folded into the recommendation bullets.

The "loop cap reached" warning fires honestly: the v1 candidate's organizing unit (fields rather than aggregate boundaries) was wrong and forced the rewrite, then the v2 candidate's `parser.lock` specification was incomplete on the liveness dimension and produced the second rework. A first-pass frame that named "synchronization contract on metrics, not field-level pruning" would have produced a v1 candidate the panel could approve in one loop.

Ratio thresholds (agent-calls/decisions = 1.5; artifacts/decisions = 2.3) sit comfortably under the schema's 10 / 8 limits despite the doubled critic-panel run, because the synthesis carried 10 decisions (5 recommendation bullets + 5 uncertainties), keeping the ratio denominators healthy.
