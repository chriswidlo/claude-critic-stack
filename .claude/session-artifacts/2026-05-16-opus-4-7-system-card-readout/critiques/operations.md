# Critic — Operations lens (v2)

## Flip-condition verification

| v1 flip-condition | v2 status | Evidence |
|---|---|---|
| (a) Correct 87% → ~70% with observability gap named | **Met** | repo-changeset.md §"Operational arithmetic correction" corrects to 70.4%, names independence-overstates and observability gap (no inter-lens correlation metric). |
| (b) State R2/R3 rollback cost | **Met** | "Rollback = `git revert` of three small bullet additions ... No data migration. No two-systems period." |
| (c) SLO or explicit "no SLO; parking lot" for R1 | **Met** | "parking lot with a tripwire" — re-entry trigger is the next `SHADOW_PANEL=1` session on a stack-meta or alignment-flavored candidate. Event-trigger SLO rather than indefinite parking. |
| (d) Rank F2 resolutions by rollout cost | **Met** | (i) lowest / (iii) medium / (ii) highest, with reasons tied to contract-change surface area. |

Bonus check — operations-shadow's flip-condition (install interim fail-safe **before** the user resolves F2): met as R5, a new CLAUDE.md "Things you must not do" bullet that halts synthesis on safety-flavored sessions when any Opus lens returns `unavailable`. Retirement trigger named (comparator schema gains `refused` distinct from `unavailable`), so the fail-safe is bounded rather than ratcheting.

## Residual concerns (not blocking)

1. **Refusal-correlation coefficient is still unmeasured.** v2 acknowledges this honestly rather than guessing — correct posture, but the workflow still cannot tell an operator whether the F2 fail-safe is over- or under-firing in practice. Belongs in a future session's scope.
2. **R5 fail-safe's own blast radius assumed-acceptable.** Assumption D names this — if the actual fraction of safety-flavored sessions is high, the fail-safe creates a completion bottleneck. Not measured, but explicitly flagged as falsifier.
3. **R6 "named failure modes flagged" bullet may render `none flagged` 100% of the time** if operators don't actively populate it. Assumption E owns this falsifier.

These are honest carry-forwards, not v2 defects.

## Verdict

**approve.**

All four v1 flip-conditions are addressed in v2; the operations-shadow's interim-fail-safe demand is also honored at the correct (CLAUDE.md invariant) layer with a named retirement trigger.
