# Decision log

## 2026-05-16 — Phase 6 generator decision (loop 0)

The frame-challenger ([challenges.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/challenges.md)) issued a frame-level objection: *the generator must demonstrate that the change-set it proposes would not have been produced by reading the executive summary alone.* The generator addressed this by:

1. Producing a small change-set (3 contract edits + 1 canon proposal + 1 hand-off) and explicitly declining 4 findings that would have produced surface-area increases in an exec-summary-only readout.
2. Tying every proposed change to a body passage with section + page + line citation, and naming the falsifier per change.
3. Recording the F2 conflict as a user-decision hand-off.

## 2026-05-16 — Step 11 routing (loop 1)

Step 10 critic-panel verdict on `repo-changeset.md` v1: **all three Opus lenses returned `rework`**. Comparator agreement classes: architecture `agree`, operations `partial-agree`, product `agree`. Routing decision per CLAUDE.md step 11:

- **Design-level rework, not frame-level.** All six lenses produced specific, actionable objections (decouple R2/R3, name asymmetric dependency direction, install interim fail-safe halt rule, correct 87% → ~70% arithmetic, attach SLO or parking-lot status to R1, surface declined findings in target files via stubs, amend synthesis template). No lens objected to the underlying frame (the small evidence-tied change-set is correctly small per the lenses); the objection is to *how* the change-set is shipped — too many "proposed; not landed" rows that won't be discoverable next session.
- **Routing: rewrite (return to step 9, not step 7/8 replan).** Frame stays. Generator rewrites repo-changeset.md v2 with:
  - Land R2 (outside-view contract clause) and R3 (CLAUDE.md MUSTNOT) directly, with R3 named as invariant and R2 as detection (asymmetric dependency).
  - Install interim F2 fail-safe halt rule in CLAUDE.md (operations-shadow's specific ask).
  - Add stub annotations to target files for the four declined findings (product Opus + product shadow ask).
  - Create [upgrades/profound/2026-05-16-eval-context-disclosure/README.md](upgrades/profound/2026-05-16-eval-context-disclosure/) so R1 has a real venue with a tracked slug, not "deferred to non-existent."
  - Amend the synthesis template (CLAUDE.md step 12) to enumerate "named failure modes flagged" and "refusal as triangulation signal" as required bullets.
  - Correct the arithmetic (87% → ~70% under independence, with correlation/loop caveats and observability-gap call-out).
  - Rank F2 resolutions by rollout cost; ship default = (i) accept-with-fail-safe.
- **Loop count: 1/2.** One more loop available before escalation-to-synthesis.

The comparator triangulation note is preserved: shadow concurs on architecture and product; operations is partial-agree with uncorrelated catches (Opus arithmetic; shadow fail-safe absence) — both treated as additive in the rewrite.

## 2026-05-16 — Phase 1 partition departure

The Opus 4.7 System Card TOC structurally differs from the plan-time expected layout. Per the user's "make the reasonable call and continue" directive, the four-zone partition was rebalanced rather than escalated. Documented in [toc-map.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/toc-map.md). No replan required.

## 2026-05-16 — F2 conflict (held; resolution defaulted in v2)

F2 (12% → 33% AI-safety R&D refusal regression × Opus-pinned critic lenses) was originally handed to the user. After Step 11, the rewrite ships **default = (i) accept refusal as workflow cost**, gated by an interim fail-safe halt rule in CLAUDE.md that requires explicit operator override for safety-flavored sessions where any Opus lens returns `unavailable`. The user can change the default later by selecting (ii) or (iii); the fail-safe runs in all three cases.
