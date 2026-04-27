# Operations critique — item 13 (orphans fate)

Target: [candidate.md](../candidate.md)

## 1. Most likely incident

At T+~90 days, a future session running step 9 (generator) produces a candidate with two named alternatives instead of three; maintainer notices, re-reads CLAUDE.md, finds the new "≥3 candidate solutions" rule, and either (a) silently ignores it (rule decays into noise) or (b) re-runs the step at one extra generation cycle. Root cause: candidate amended CLAUDE.md with a rule that lacks an enforcement mechanism in any agent prompt, so compliance is on the maintainer's eyes and the generator's voluntary attention — exactly the unmaintained-policy failure mode the frame-challenger flagged against the standing-policy P, smuggled back in through the O1 extraction.

## 2. Blast radius

- **Every future generator step** pays the rule's reading cost (negligible per session, but multiplied by N sessions per year — the 2026-04-27 day alone shows ≥7 sessions, so the multiplier is non-trivial).
- **One file rename (O3)** has unaudited inbound link radius. Candidate concedes the work was not done. Inbound references plausibly include: punch-list, item-01 plan, any session-artifact that quoted the filename, the LEDGER.
- **Two file deletions (O1, O2)** have radius bounded to historical session-artifacts (link-rot accepted) and the maintainer's muscle memory.

## 3. Rollout / rollback

- **Rollout:** none staged. Single PR-shaped change containing CLAUDE.md amendment, two deletes, and a rename. No flag, no canary, no shadow.
- **Rollback for CLAUDE.md amendment:** `git revert`. Cheap mechanically, but the rollback *trigger* is unspecified — the cheapest experiment tests discoverability, not rule cost-effectiveness. The amendment has no rollback criterion at all.
- **Rollback for O3 rename:** `git mv` back. If downstream links to the new name accumulate during the period before rollback, you get a forward-fix problem.
- **Rollback for deletions:** `git show <sha>:path` recovers content; the act of un-deleting requires the maintainer to remember the file existed. The candidate's session-artifact-as-discoverability claim *is* the un-delete trigger mechanism. If that mechanism fails, rollback is structurally impossible.

## 4. Observability gap

- The CLAUDE.md amendment has **no compliance signal**. No agent audits "did step 9 enumerate ≥3 candidates."
- The 6-month experiment **has no trigger mechanism**. Depends on the maintainer remembering, in 6 months, to ask a fresh session a specific question. No calendar entry, no test, no scheduled job. Practically, this experiment will not run.
- The rename's link-breakage would be detected by: nothing currently. No link-checker in the stack.

## 5. Cost at failure

- **CLAUDE.md amendment failure (it's ceremony):** every future generator step pays a small attention cost, plus cumulative confusion of a stale rule. Bounded, but unbounded in time — perpetual tax with no scheduled re-evaluation.
- **Discoverability failure (assumption 4 wrong):** future maintainer / session wastes time looking for context that doesn't exist. Candidate frames this as "<2 minutes vs. >2 minutes." That bound is optimistic. The actual failure is *not knowing the file ever existed*, which is unbounded — you don't search for what you don't know to look for. Cost: "phantom decisions get re-litigated from scratch with worse context" — Nygard's exact warning.
- **Rename failure (broken inbound links):** each broken link costs one human investigation (~5 min). Bounded by inbound link count, which the candidate did not count.
- **Compounding failure across all three:** the most expensive failure is the *combination* — future session asks "why was X done this way," follows a broken link from a session-artifact (rename failure) to a deleted file (deletion failure), and finds no rule about how to handle this in CLAUDE.md (we added candidate-enumeration, not discoverability rules). Exactly the scenario the frame-challenger predicted and the candidate dismissed.

## 6. Frame-level objection

The candidate frames this as a **disposal decision** with a small embedded policy nudge. The operations frame is that this is a **change-management operation on a corpus of cross-referenced artifacts**, and the unit of work is not "per-orphan disposition" but "atomic tree-delta with link-graph audit and rollback criteria." Under operations frame:
- The rename and the deletions should be sequenced separately, with the rename done *first* (only reversible-with-cost change; deletions are reversible-with-loss-of-discoverability) and observed for one full sweep cycle before deletions are committed.
- The CLAUDE.md amendment is a *separate* change that should not ride alongside file-disposal — different rollback criteria, different blast radius, different observability needs.
- Per-orphan asymmetry is a feature for analysis and a bug for execution: four heterogeneous actions in one PR have four independent failure modes that cannot be rolled back independently.

The candidate's "named tradeoffs" trades off design considerations; not operational ones. No row for "atomicity vs. sequencing" or "amendment cadence vs. disposal cadence."

## 7. Verdict

**`rework`.**

What would change the verdict: split the change into two sequenced commits — (a) rename O3 *after* a `grep -r "ok-cool-this-is-warm-balloon"` confirms the inbound-link count, with each found link rewritten in the same commit; (b) extract pressure #2 into CLAUDE.md *as a separate commit* with a stated 90-day re-evaluation criterion (e.g., "if no generator step in the next 10 sessions produces fewer than 3 candidates and no critic-architecture review flags ceremony, the rule is load-bearing; else revert") — and replace the 6-month maintainer-memory experiment with a trigger that does not depend on memory (e.g., a one-line note appended to the punch-list footer that is read by every future cleanup-sweep session by convention).
