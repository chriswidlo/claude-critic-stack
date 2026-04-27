# Critic — Operations lens v2 — item 06 (loop 2)

## 1. Most likely incident

At time T (~6–18 months out), `agentic-engineering-research` is pruned or rewritten or its tip moves past `13c09b0`. An operator or `canon-librarian` consult lands on the `Status` paragraph and reads the citation. The pointer rots; the text stays grammatically true ("the source material *was* preserved on a branch named X at commit Y"); no operator action is required because no action against `main` is implied.

**Meaningfully different from loop 1.** In loop 1, pointer rot meant the row's executable plan was un-executable and the entry was lying. In v2, pointer rot means a historical note is harder to verify — does not produce a contradiction with the row's contract.

## 2. Blast radius

- Two entries' `Status` paragraphs + transitively any reader who tries to verify the historical claim. Verification cost rises; semantic correctness intact.
- `canon-librarian` ranking signal from a Group E row is "captured observation, no action," which matches reality. No bad-action risk.

## 3. Rollout / rollback

- **Rollout:** trivial content-only change.
- **Rollback path:** materially clearer than v1. Three reversible steps: `git revert` reinstates Group D rows; deleted migration sections recoverable from history; Group E rows removed by deleting inserted lines. Each independent.
- **Two-systems-running period:** **does not apply.** Loop 1's b′ had two simultaneous truths (executable migration text + meta-prose denying it); v2 deletes the executable text. One truth post-merge. Strongest operational property of v2.

## 4. Observability gap

Partially closed.

- **Better:** state-token + group-membership now agree. Loop 1's gap (state cell `🌱` live while body prose said `superseded`) is gone.
- **Still uncollected:** no metric for branch-ref reachability. v2 makes this acceptable because actionability does not depend on it.
- **Still gap:** no dated review trigger. v2 effectively argues none is needed because entries are in the "no action" partition. Lands for these two entries; does not land for recurrence.

## 5. Cost at failure

- **Pointer rot:** low cost — historical note, no action prescribed.
- **Recurrence cost:** real, partially mitigated. Group E placement is cheaper than Group D rescue but still a per-instance decision with no written rule. Outside-view's threshold (≥5 instances or 3rd occurrence) for promoting per-instance to as-rule still not adopted.
- **Group E inflation:** v2 grows Group E from 1 row to 3. If the next research session lands on a third branch and produces 2–4 more entries, Group E reaches 5–7 rows and starts to function as a parking lot rather than an observation shelf. Cost-at-failure here is convention-drift.
- **Human on-call load:** zero — solo doc repo.

## 6. Frame-level objection

Carry-forward operations frame from loop 1 — *freshness-and-reachability of cross-artifact pointer chains* — is **partially answered, partially deferred**:

- **Answered:** the LEDGER-row → entry-body chain no longer carries an executable claim that depends on branch reachability. The chain still exists but no link triggers operator action when it rots. Eviction-of-actionability achieved via relocation rather than literal eviction.
- **Deferred:** the *class* problem (every future research-branch session reproduces this) is shifted from Group D rescue to Group E placement, not eliminated. Legitimate deferral when the deferred cost is bounded; Group E inflation is the bound to watch.

Not a frame-level objection — a frame-level deferral.

## 7. Verdict

`approve`

What would change the verdict: if Group E inflation reaches a threshold the operator considers parking-lot-shaped, the next instance should force the rule-writing move rather than another Group E placement.
