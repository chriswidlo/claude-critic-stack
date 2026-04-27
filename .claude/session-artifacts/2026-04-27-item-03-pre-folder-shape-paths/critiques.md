# Critic-panel aggregate — item 3 — loop 1

## Verdicts

| lens | verdict | one-line objection |
|------|---------|--------------------|
| architecture | rework | Candidate treats commits as the unit of architectural design; should design file-graph end state and derive minimum commit sequence from it. |
| operations | rework | WIP accounting problem, not commit-structuring problem — "you cannot reduce WIP by adding WIP." Three-commit envelope adds 2 new pieces of WIP to close 1 ticket. |
| product | rework | Workflow generating its own scope. Operator asked for closure; candidate returns open threads (commit B placeholder + commit C deferred + frame revision they didn't ask for). |

## Frame-level convergence

All three lenses converged on the **same** frame-level objection: the candidate over-engineered a small, mechanical operator ask into a multi-commit choreography that bills the operator for findings the workflow surfaced.

This is the signal upgrade [#11 convergent-frame-objections-as-replan-signal](upgrades/normal/2026-04-26-convergent-frame-objections-as-replan-signal/README.md) names: when independent lenses converge on the same frame, replan, do not rewrite.

## Lens-specific surface notes (carried forward to replan)

**Architecture (rework):**
- Commit A's correctness depends on Commit B being a coherent unit, but Commit B's content branches on operator answer.
- "redirects.md" primitive (frame Reframe 1 option b) was dismissed without engaging.
- Real architectural unit is the file-graph end state, not the commit log.

**Operations (rework):**
- Commit A → C must land in order (same hunks); commit B is independent.
- "Two-systems-running" period bounded only by item 1's velocity, which is unknown — no calendar deadline.
- Most likely incident: T+8 weeks operator re-edits line 138 to "tidy" the parenthetical, undoing the only nav repair.
- Observability gap: no signal at T+3 months distinguishing "B deliberately open" from "B forgotten."

**Product (rework):**
- Operator's five-word ask vs. candidate's three-commit + open-question response.
- New affordance "deferred commit slot" (commit B) has no carrier in repo.
- Honest minimum: apply 4 edits, delete Done-when #5, note unresolved question in commit message OR as new punch-list line item.

## Routing

Step 11 routing decision: **replan**. Convergent frame-level objection means a rewrite at step 9 against the same frame would reproduce the failure. Append revision 2 to [`frame.md`](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/frame.md) and re-enter generator at step 9 with the collapsed frame. Do not re-run scope-mapper or frame-challenger — the work is intact; only the orchestrator's framing was wrong.

Logged separately in [`decision-log.md`](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/decision-log.md).
