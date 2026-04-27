# Operations critic — loop 1

**Verdict: rework.**

## Most likely incident

At T+8 weeks, an operator opens [`upgrades/no-brainer/2026-04-26-upgrade-entries-as-folders/README.md`](upgrades/no-brainer/2026-04-26-upgrade-entries-as-folders/README.md) to add a new entry, sees the line-138 parenthetical pointing one way and the surrounding migration-table prose pointing another, and re-edits line 138 to "tidy" it — silently undoing the forwarding pointer that was the only nav repair commit A shipped. Root cause: commit A landed an additive parenthetical in a sentence whose grammatical subject *is* the old path, with no in-file comment explaining why both strings coexist; the artifact is self-defeating without a marker.

## Blast radius

If commit A's edits are wrong: 5 string substitutions across 2 active-surface README files plus the line-138 parenthetical in 1 dogfood entry. Worst case is 5 dead links in 2 upgrade READMEs and 1 confused historical paragraph — single-digit reader-clicks per week (cannot estimate actual nav traffic; this stack has no telemetry on README reads). Reversibility: full, by `git revert` of commit A; no data plane, no consumers, no downstream services.

**The blast radius of commit A is small. The blast radius of commit B *not* landing is larger** — it leaves the policy question open across every future cleanup ticket (items 7, 12, plus item 2 which already shares files), and that's the radius the candidate is undercosting.

## Rollout / rollback

- **Rollout:** no flag, no canary — git commit on main, solo operator. Acceptable for this scale.
- **Rollback:** commit A is independently revertible. Commit C **must land after** commit A or it conflicts in the same hunks; commit B is **independent of A and C** in file scope. So sequencing constraint is A → C, with B free-floating.
- **Two-systems-running period:** the candidate names "if item 1 takes a month, edits stay in the old style until then" — i.e., **bounded only by item 1's velocity, which is unknown.** Recommend: name a calendar deadline ("if commit C has not landed by 4 weeks post-A, re-open item 3 to re-evaluate restyle in isolation").

## Observability gap

The proposal makes invisible: **the distinction between "commit B was deliberately left open pending operator decision" and "commit B was forgotten."** Three months from now, the only artifact that will exist is the plan with a footnote about commit B, and the punch list with item 3 marked done. Operator-facing signal: nothing.

Concrete fix at zero cost the candidate could adopt: append commit B as an explicit row to [`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md) with status `pending operator decision`, so the punch list itself carries the "deliberately open" signal. The candidate does not propose this.

## Cost at failure

When this fails (B and C never land):
- The 7 broken session-artifact links remain broken indefinitely. Operator-attention cost per click: small but nonzero, compounding over reads.
- The 4 active-surface lines stay in the pre-item-1 path style until item 1 chooses a style and someone remembers to come back. Risk: when item 1 lands, the operator forgets to re-touch these 4 lines, so the *new* style propagates to everything *except* the 4 lines item 3 just touched — **silent style drift at exactly the spots the cleanup pass visited.** This is the expensive failure mode; the candidate does not name it.

## Frame-level objection

The candidate frames this as a **commit-structuring problem**. The operations frame is that this is a **work-in-progress accounting problem**: the system already has ten-plus open cleanup tickets, item 1 is in flight, and the candidate's three-commit structure adds *two* new pieces of WIP (the open commit B and the deferred commit C) to close *one* ticket. **You cannot reduce WIP by adding WIP.**

The honest operational move is either (a) collapse to one commit and own the policy declaration explicitly, or (b) close item 3 as `won't fix until item 1 lands` and stop pretending the 4 active edits are independent of the style they will be restyled into within weeks.

## What would change the verdict

Name a calendar bound on commit C, add commit B as an explicit `pending` row to the punch list, and reframe the no-tooling decision as a deliberate accepted-risk item with a check-in date — not as a dispute with the outside-view's forecast.
