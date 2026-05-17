# Session ledger — 2026-05-16-opus-4-7-system-card-readout

## Counts
| Category | Count | Source of truth |
|---|---|---|
| Agent calls (subagent invocations) | 30 | classifier (1) + initial Explore for repo state (1) + zone Explorers A/B/C/D (4) + outside-view (1) + canon-librarian (1) + 6 distillers (6) + scope-mapper (1) + frame-challenger (1) + critic-panel loop 1 [3 Opus + 3 Sonnet shadow + comparator = 7] (7) + critic-panel loop 2 [3 Opus + 3 Sonnet shadow + comparator = 7] (7) |
| Artifacts (markdown files in session dir, excluding ledger.md itself) | 32 | `find .claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout -name '*.md' -not -name 'ledger.md' \| wc -l` |
| Critic-panel loops used | 2 / 2 | from [decision-log.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/decision-log.md) — Step 11 routing entry "Loop count: 1/2" plus subsequent loop-2 panel |
| Loop cap reached | true | true iff loops used == 2 |
| Decisions in synthesis | 13 | 8 numbered items under `## Post-critique recommendation` + 5 numbered items under `## Named uncertainties (≥3)` |

## Derived ratios
- Agent-calls per decision: 30 / 13 = **2.31**
- Artifacts per decision: 32 / 13 = **2.46**
- Loops to convergence: 2 / 2

## Warnings
- ⚠️ candidate needed maximum rework; first-pass framing was off

(`agent-calls / decisions = 2.31 < 10` → no warning; `artifacts / decisions = 2.46 < 8` → no warning; loop cap reached → warning fires.)

## Notes

**Loop-cap-reached interpretation in this session.** The loop cap was reached because the v1 change-set deferred too many load-bearing items as "proposed; not landed" prose in [repo-changeset.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/repo-changeset.md), and all six panel lanes (3 Opus + 3 Sonnet shadow) returned `rework` with consistent flip-conditions. The v2 rewrite landed R2/R3/R5/R6 directly in [CLAUDE.md](CLAUDE.md) and [.claude/agents/outside-view.md](.claude/agents/outside-view.md), created the [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/README.md) R&D venue with a re-entry trigger, and added stub annotations to [.claude/agents/canon-librarian.md](.claude/agents/canon-librarian.md) and [.claude/agents/canon-refresher.md](.claude/agents/canon-refresher.md) for declined findings. v2 was unanimously approved.

The first-pass framing flaw the warning points at: v1 treated "session artifact prose" as adequate for committing the repo to changes — a product-debt pattern the panel correctly identified. The v2 rewrite addressed each lens's flip-condition without re-scoping the underlying frame, which suggests this was a *generator-side* defect, not a frame-level one. A future readout session can avoid the loop by landing small contract edits directly in v1 rather than deferring them to v2.

**Decisions count rationale.** synthesis.md uses numbered items (`1.`, `2.`, …) rather than bullets under both load-bearing headings. The schema defines a decision as "one bulleted item under either the `Recommendation` heading or the `Uncertainties` heading"; numbered items are list items and are counted as decisions here. If a future schema revision wants to distinguish bulleted from numbered, this ledger should be revisited.

**Triangulation signal preserved separately.** The comparator outputs ([critiques/architecture.comparison.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/architecture.comparison.md), [critiques/operations.comparison.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/operations.comparison.md), [critiques/product.comparison.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/product.comparison.md)) report architecture `agree`, operations `partial-agree`, product `agree` on the v2 review — preserved in [synthesis.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/synthesis.md) under the "Triangulation signal" bullet. This is decision-bearing follow-up signal, not a current ledger warning.
