# Operations-lens critique — path-discipline regime (loop 1)

## Verdict: rework

## Frame-level objection

The candidate frames this as a *compliance* problem. Operationally, this is a **change-management problem against a live, self-modifying authoring loop**. The repo runs the workflow on itself. Adding a `PostToolUse` hook to a system whose workflow consists of ~12 Write operations per session means the hook is in the critical path of the very tool that authored it. The candidate's own "ways this could be wrong" §2 names this and proceeds anyway. A change-management framing demands warn-only rollout, telemetry before enforcement, and a documented kill-switch — none of which the candidate provides.

The candidate also treats the 14-day audit as if it were a control. **An audit is not a control; it is a measurement.** No automated action fires if compliance degrades, and the audit itself has no mechanism. Candidate's own §3 admits "audits in solo repos are forgotten" — naming the risk does not retire it.

## Most likely incident

T = first `/upgrade` after merge. Slash-command Write of an entry README containing one inherited file-relative link triggers the `PostToolUse` hook. Root cause: `bin/check-path-discipline.sh` runs *after* the Write succeeds at the filesystem level (`PostToolUse` semantics) but the candidate treats it as a pre-commit gate. The candidate never specifies whether `PostToolUse` in this stack actually has reject-and-revert semantics or only emits non-blocking warnings. **That's the load-bearing operational unknown and it is not addressed.**

## Blast radius

If the hook misfires:
- Every Write/Edit on active surfaces is blocked. Active surfaces per the candidate = majority of the authoring surface of this repo.
- A workflow run mid-session (steps 6, 7, 8, 9, 10 all Write) hits the hook on every artifact write *if* artifacts are misclassified. The exclusion is asserted, not demonstrated.
- Solo repo, so blast unit is "sessions per day"; every session in flight when a buggy hook lands fails partially or fully.

## Rollout / rollback gaps

Candidate proposes single-step landing. Missing:
- **No canary.** Hook should ship in *warn-only* mode first.
- **No shadow.** No way to see what the hook *would* have rejected before it goes live.
- **Rollback path exists but is undocumented.** Two-line `.claude/settings.json` revert. Candidate must name it.
- **No two-systems period.** Soft and hard enforcement ship together; no fallback layer producing telemetry.

## Observability gap

Candidate names a single observable: 14-day audit re-running the Explore script.

Invisible to the proposal:
- Hook rejection rate per session.
- Agent retry behaviour on rejection (assumption 3 is unfalsifiable without it).
- Workflow stalls.
- False-positive rate / operator-override count.

The 14-day audit is collected by ad-hoc script invocation — between days 0 and 14 the regime is operationally dark.

## Cost at failure

- **Session deadlock.** Agent hits hook, retries identically, loops. Cost = stalled workflow run, partial artifacts, decision-log inconsistent.
- **Authoring abandonment.** If `/upgrade`'s instant-capture property breaks, the operator stops capturing. The R&D lab loses its inflow — worse than the rule it enforces.
- **Hook-induced corruption of the longitudinal record.** A wrong exclusion regex rejects writes mid-workflow, leaving partial files. Violates the longitudinal-record contract more thoroughly than any retroactive sweep.
- **Human on-call.** Solo maintainer; every false-positive is a context switch — exactly the load the rule was supposed to remove.

## Specific operational concerns

- **Self-recursion:** *this very session* is a counterexample to the rollout assumption. The candidate.md write contains `(\.\./)` patterns inside fenced regex; if the hook had been live during step 9, the candidate-write itself could have been affected. Minimum staging: warn-only first.
- **Audit substrate:** unspecified. Options are scheduled `Routines` agent, calendar reminder, manual memory. Candidate must pick one.
- **Hook bypass:** silent. Operator-experience model on rejection of a write the operator believes correct: edit settings → write → re-enable? Override? Suffer?
- **SLO model:** one signal, no SLO. Required additions: hook-rejection-rate, agent-retry-loop-detection, workflow-stall count, override count.

## What flips the verdict to approve

A named warn-only rollout phase before blocking; a concrete substrate for the 14-day audit (scheduled agent, Routines entry, or in-repo calendar artifact); a documented hook-bypass procedure with logged-override metric; and a kill-switch sentence in `.claude/settings.json`-revert form named in the candidate body.
