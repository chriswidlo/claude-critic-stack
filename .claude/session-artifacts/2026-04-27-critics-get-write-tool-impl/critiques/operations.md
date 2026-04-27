# Operations critique — `2026-04-27-critics-get-write-tool-impl`

## 1. Most likely incident

At T+~5 sessions after rollout, an operator running Step 10 sees the panel-aggregate read complete with two files present and one silently absent or stale; minority-veto logic uses a partial vote count and the orchestrator passes a self-modifying change on a 2-of-2 read of files that should have been 3-of-3. Root cause was Assumption A2 — three critics writing in parallel under instruction-level scoping have no write-time assertion that `<session-id>` was propagated correctly, so a stale-session-id critic wrote to a prior session's `critiques/` directory and the current session's directory was missing one file the orchestrator did not notice was missing.

## 2. Blast radius

- **Per-incident scope:** one design decision per affected session. In a research/lab repo this is small in user-population terms (one operator) but high in decision-leverage terms — every veto missed is a design that ships unchallenged. Cannot estimate frequency without measurement; outside-view's "30–50% of tool-grant rollouts cause one observable incident in first 50 invocations" applies, but this stack runs ~1 session/day at most, so first incident is plausibly within 30–50 days.
- **Cross-session contamination:** a stale-session write to a *prior* session's `critiques/` directory mutates an audit artifact that has already been treated as a postmortem of record. That is not bounded to the current session — it corrupts the historical ledger. Outside-view §inferred 8 and §inferred 9 named this as the asymmetric-reversal cost.
- **Self-modifying class amplification:** the first such incident is most likely on a self-modifying change (because that is the class with the weakest review under the candidate's own Defense 2 — replan does not detect *missing* files, only *bad verdicts*). Blast radius on self-modifying changes is higher because the agent surface itself is what's being changed.
- I **cannot estimate** how often `<session-id>` mis-propagation occurs because Explore §Gap 2 explicitly named the propagation mechanism as undocumented. That is itself the blast-radius answer: unknowable from inside the candidate.

## 3. Rollout / rollback

- **Rollout strategy:** the candidate proposes a flag-day swap of CLAUDE.md Step 10 wording + simultaneous frontmatter changes to all three critics. There is **no canary** (e.g., grant Write to one critic for N sessions, observe), **no shadow traffic** (run new shape and old shape in parallel for the same session), and **no flag** (the change is in CLAUDE.md prose; either the orchestrator follows new wording or it doesn't). The "first ~5 sessions are themselves the cheapest experiment" claim in Tradeoffs §5 is **not a rollout strategy, it is hope**. A rollout strategy says *what signal you watch* and *what triggers rollback*; the candidate names neither.
- **Rollback path:** Tradeoffs §1/§5 and Assumptions A4 imply rollback is "revert CLAUDE.md and frontmatters." That is a forward-fix dressed as a rollback, because:
  - Outside-view §inferred 9 explicitly: "once distillers/synthesis read critic-emitted artifacts, rollback requires rewriting consumers." Step 12 synthesis under the new shape reads `critiques/<lens>.md` — if any session has run synthesis on critic-authored files, the synthesis prose itself is now anchored to artifacts whose authorship contract changes on rollback.
  - The candidate does not say what happens to in-flight sessions during rollback.
- **Two-systems-running cost:** **not named.** The candidate does not state whether old `critiques.md` aggregate files coexist with new per-lens files during transition, nor whether Step 11 rewrite-loops mid-transition can produce mixed-authorship artifacts (orchestrator-paraphrased v1, critic-authored v2). Scope-map row "Per-lens `critiques/<lens>.md` precedent" flags this gap; the candidate does not resolve it.

## 4. Observability gap

- **What goes invisible:** today, the orchestrator's transcript *contains* the critic's prose return inline. After the change, the prose lives in a file the orchestrator may or may not have read. If the file is missing, malformed, or written to the wrong path, the orchestrator's transcript will contain only a verdict label (the inline contract) — not the body. Diagnosing "what did this critic actually say" requires going to disk and matching against a session-id whose propagation contract is not specified.
- **Metric that would confirm "the thing went well":** count of `critiques/<lens>.md` files matching the active session-id, written within the wallclock window of Step 10. **I do not know whether this metric is collected.** The candidate's Assumption A1 names a hook that *would* collect it ("a `PostToolUse` hook on the critic agents that logs every `Read` they perform") — and explicitly states the hook is **not in the candidate but should be added if A1 ever fails.** That is observability deferred to post-incident, which is the failure mode.
- **Specifically missing:** no metric for (a) write-path matching active session, (b) all-three-files-present before Step 11/12 reads, (c) sibling-Read attempts (the A1 detection mechanism). All three are named in the candidate as future work.

## 5. Cost at failure

- **Retry storms / amplification:** parallel-write means a malformed session-id propagates to three writes simultaneously, not one. The candidate's "symmetric to other Write-holders" framing in Tradeoffs §2 ignores that other Write-holders run sequentially, so one bad session-id produces one bad artifact, not three. **Fan-out factor: 3x** at the write boundary, and 3x again if Step 11 triggers a rewrite loop (3 critics × 2 revisions = 6 potentially-misplaced files per session).
- **Human on-call load:** in this repo, the "operator" *is* the on-call. Each incident requires the operator to: (a) realize a verdict was missed/corrupted, (b) reconstruct what the critic actually said by going to disk across multiple session directories looking for orphans, (c) decide whether the synthesis that already ran on bad input needs replay. Outside-view §inferred 8 named this as "potentially invisible unbounded loss" — the cost is in *detection latency*, which the candidate does not estimate (outside-view §gap 5 also flagged this).
- **Cost of A1 failing once:** the candidate concedes "even once" makes the proposal materially worse than status quo. The detection mechanism for that failure is the un-built hook. So the cost-at-failure for A1 is **catastrophic-and-undetected** by construction.

## 6. Frame-level objection

The candidate frames this as "extend an established Write-pattern to three more agents." The operational frame is that this is **a step-change in concurrency posture**, not an extension. Every existing Write-holder (`subagent-distiller`, `scope-mapper`, `frame-challenger`) runs **once, sequentially**, with the orchestrator's full attention on the returned artifact. The critics run **three-in-parallel**. Concurrency is not a parameter you tune; it is a different operational regime with its own failure classes (TOCTOU, write-ordering, partial-fan-out completion, session-state visibility). The candidate's Assumption A2 acknowledges this exists ("most load-bearing assumption") and then proceeds without instrumenting it. The Write-holder precedent does not transfer because the precedent is sequential. **Operations rejects the precedent-by-analogy.**

A second frame-level objection: the candidate's "first ~5 sessions are the cheapest experiment" treats production as the test environment. In an ops frame, production is where you *validate* a change you've already de-risked elsewhere — not where you *discover* whether your load-bearing assumption holds. The lab repo collapses dev/staging/prod into one filesystem, but that does not entitle the design to skip the de-risk step; it intensifies the requirement to do it via shadow run, canary on a single critic, or a dry-run mode where the file is written to a `.dry/` subdirectory and compared to orchestrator-paraphrase before cutover.

## 7. Verdict

**rework**

The verdict would change to `approve` if the candidate added (a) a write-time session-id assertion in each critic's body — even instruction-level, even a single sentence asserting "abort if `<session-id>` is empty or matches a session whose directory predates this invocation by >1 hour" — and (b) a single-critic canary stage (grant Write to `critic-architecture` only, run for 5 sessions under the new contract, observe missing-file rate, then expand to all three) instead of a flag-day swap of all three at once.
