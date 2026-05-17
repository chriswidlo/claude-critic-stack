# Critic — Product lens (shadow)

Lane: Sonnet shadow (`critic-product-shadow`). Voice, not vote. v2 — loop-2 re-review.

## Loop-2 re-review context

v1 verdict was `rework`. Two flip-conditions stated:
- (a) R2 and R3 must land in contract files or be routed to `upgrades/profound/` with tracking parity to R1.
- (b) F2's live refusal risk must be visible at the repo surface, not buried in a session artifact.

Both addressed.

## 1. User-visible consequence

Most user-visible consequence is genuine improvement in operator experience for safety-flavored sessions: the F2 interim fail-safe in [CLAUDE.md](CLAUDE.md) now halts synthesis before a misleading comparator result can propagate. In v1, an operator running `SHADOW_PANEL=1` on a safety-adjacent candidate would receive a triangulation-signal bullet that said "shadow disagrees with Opus lane" with no indication that the disagreement was measurement artifact (Opus refused) rather than substantive disagreement. Now blocked.

Secondary consequence: operators encounter a hard halt requiring explicit override on safety-flavored sessions where an Opus lens is `unavailable`. Cost disclosed (retirement condition names the trigger), but operators who hit it before the R&D entry lands experience refusal-as-interruption with no automated path forward.

## 2. Commitments implied

R2 is now a contract clause in [outside-view.md](.claude/agents/outside-view.md) with co-falsifier linking to corresponding [CLAUDE.md](CLAUDE.md) MUSTNOT. Coupling explicit. Stronger than v1's prose-in-session-artifact state.

R3 includes self-retiring condition. Bounded commitment with expiry trigger, not open-ended debt.

R1 in [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/README.md) at `created` stage with open questions and concrete next-session trigger. No SLO, but acceptable for `created` stage.

R4 (canon ingest path for declined findings F6, F7) remains a human-curator discovery problem. The stubs are grep-discoverable but require the curator to find them. Residual gap, not blocker.

## 3. Migration burden

Operators of existing sessions do not inherit F2 fail-safe retroactively. Sessions mid-flight on safety-adjacent candidates have no automatic protection. Acceptable because the fail-safe is an orchestrator rule at session-start.

Future operators re-entering R1 entry at `spiked` stage have clear guidance.

The added "Named failure modes flagged" + "refusal as triangulation signal" sub-bullet are additive.

## 4. Affordances better / worse

**Better:**
- F2 halt at orchestrator-rule layer, visible on every session start.
- R2 inaccessible-comparator recognition in the agent contract operators actually invoke.
- Synthesis step 12 surfaces refusal as triangulation signal — the "Opus refused vs. Opus disagreed" conflation is named and handled.
- Stubs in `canon-librarian.md` and `canon-refresher.md` make declined-finding decisions grep-discoverable.

**Worse (residual):**
- R4 (benchmark contamination screen, self-report noise floor) remains proposed-not-tracked.
- F2 fail-safe halt requires "explicit operator override" but does not specify what constitutes valid override, what override produces in `decision-log.md`, or how long override persists.

## 5. Frame-level objection

v2 makes a bounded bet that the F2 interim fail-safe will not outlive its welcome. Fail-safe retires when comparator schema splits `unavailable` from `refused`. That split is tracked in R1 entry — at `created` stage with no SLO, no spike, no prepared state. Retirement condition references future artifact with no completion target. Fail-safe could persist indefinitely if R&D entry stalls.

A halt-requiring-override that persists past the point where it is still the cheapest intervention becomes a friction tax. Change-set does not define what "stalled" looks like or what happens if fail-safe is still in place twelve sessions from now. Frame-level concern: temporary bridge (as framed) vs. permanent tax disguised as a bridge (failure mode).

Does not flip verdict — `created`-stage R&D entry is the right landing zone, retirement condition is stated. Operator should note: bridge has no completion SLO.

## 6. Verdict

**approve**.

Both v1 flip-conditions met: R2 and R3 landed in contract files with co-falsifier linkage; F2's unresolved state visible at the orchestrator-rule layer (CLAUDE.md MUSTNOT, readable on every session start). Residual gaps (R4 discovery mechanism, override-procedure underspecification, R1 SLO absence) are below the rework threshold.

Verdict would revert to `rework` if (a) F2 fail-safe halt produces no operator-guidance on what constitutes valid override; or (b) R1 entry is not advanced to `spiked` within two sessions invoking `SHADOW_PANEL=1` on safety-adjacent candidates.
