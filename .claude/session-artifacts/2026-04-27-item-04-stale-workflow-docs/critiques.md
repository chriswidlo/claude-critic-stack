# Critic-panel aggregate — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`

## Loop 1 verdicts

| Lens | Verdict | Frame-level objection (one-line) |
|---|---|---|
| Architecture | rework | Audience declaration is a third doc surface; declaration belongs in CLAUDE.md; ships zero controls. |
| Operations | rework | Control-design problem with zero controls — both audience declaration and trigger-based deferral are claims about the future with no observation mechanism. |
| Product | rework | Candidate relocates the Heilmeier objection into a *Philosophy* paragraph it did not rewrite; pointer-that-does-not-resolve is worse than no pointer. |

**Loop 1 aggregate: rework. Routed to step 9 for rewrite.** See [decision-log.md](decision-log.md).

## Loop 2 verdicts (post-rewrite, on [candidate-v2.md](candidate-v2.md))

| Lens | Verdict | Residual concern (one-line) |
|---|---|---|
| Architecture | **approve** | Pre-commit hook is bypassable per-commit; in a single-maintainer no-CI repo, "structural" effectively collapses to "habitual." Bounded, not frame-breaking. |
| Operations | **approve** | Pre-commit hook is opt-in per-clone via `core.hooksPath`; recommend a one-line installer note. |
| Product | **approve** | Audience declaration is in CLAUDE.md but README does not state who *it* is for; one-liner at top of README would close. Worth flagging, not blocking. |

**Loop 2 aggregate: approve.** All three lenses approved v2; each named one residual concern not severe enough to veto.

## Carry-forward residuals to fold into the synthesis

1. **CI vs. pre-commit hook tradeoff** — architecture noted that GitHub Actions would survive `--no-verify` and be repo-enforced; v2 chose the lighter mechanism. Worth naming in the synthesis as a known limitation in this repo's no-CI posture.
2. **Recurring vs. single-shot calendar reminder** — operations noted the 2026-07-27 reminder fires once. Easy follow-up: add a recurring quarterly check after the first one fires.
3. **README self-description for cold reader** — product noted the README does not state who it is written for. A one-line addition at the top closes this; cheap.
4. **Concept drift vs. count drift** — both architecture and operations noted that the hook catches count drift but not concept drift. Acknowledged in v2's own *Ways this could still be wrong*; the synthesis should preserve this as a named uncertainty.

These are folded into synthesis (step 12) as named uncertainties and follow-up actions, not as new vetoes.
