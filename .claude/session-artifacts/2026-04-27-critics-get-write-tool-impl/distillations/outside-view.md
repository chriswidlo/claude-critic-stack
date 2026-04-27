# Distillation — outside-view

## Source agent
outside-view

## Invocation summary
Orchestrator asked outside-view for a reference-class forecast on granting filesystem-write to previously-prose-only critic agents. Subagent returned a four-class forecast with a "below base rate" verdict for clean transition, declaring an upfront canon-access gap (no Bash/Grep available at invocation).

## Direct facts
1. [graphify Issue #195, web] A Claude Code subagent silently under-counted by >50% because verb similarity routed work to a read-only Explore agent. (confidence: direct)
2. [outside-view §0] The agent declared it could not grep `canon/corpus/` from its invocation; base-rate numbers are first-principles + web-evidence, not canon-anchored. (confidence: direct)
3. [outside-view §2] CI test reporting paraphraser-to-emitter migrations are estimated ~85–90% successful, with schema drift between emitters as the dominant failure. (confidence: direct, but estimate is subagent-supplied)
4. [outside-view §2] Dictation software replacing transcription is estimated ~70–80% successful when the schema is constrained. (confidence: direct, subagent estimate)
5. [outside-view §2] Structured logging migrations are estimated ~80% successful with long-tail "every service logs slightly differently" pain. (confidence: direct, subagent estimate)
6. [Embrace The Red, SEI CERT — web] ACL race conditions and TOCTOU exist as documented failure classes in concurrent permission systems. (confidence: direct)
7. [TrueFoundry — web] Default-open permissions in multi-agent production have caused catastrophic deletions. (confidence: direct, source-attributed)

## Inferred claims
1. [outside-view §1] Primary reference class is "audit-trail systems where recording responsibility moves from a downstream paraphraser to upstream emitters" (JUnit-XML / structured-log / dictation class). (confidence: inferred)
2. [outside-view §2] Composite primary-class estimate: ~75–85% achieve audit-trail-faithfulness, but ~40–60% incur a *new* failure class (schema drift, write collisions, stale artifacts). (confidence: inferred)
3. [outside-view §2] ~30–50% of "give the agent the obvious next tool" rollouts cause at least one observable incident in first 50 invocations; ~10–15% cause silent corruption detected later. (confidence: inferred — subagent admits "rough estimate")
4. [outside-view §3] Proposal sits *at* base rate (~80%) for goal-achievement but *below* base rate (~40–50%) for clean transition. (confidence: inferred)
5. [outside-view §5] Modal failure mode for this proposal is stale-session cross-contamination / wrong-path writes; session-id propagation becomes a new load-bearing invariant. (confidence: inferred)
6. [outside-view §5] Schema drift between the three critic lenses is the second-priority failure: without shared schema, the aggregator relocates rather than eliminates the paraphrase-loss problem. (confidence: inferred)
7. [outside-view §5] Self-review blind spot: the critic-panel may lack a lens named "audit-integrity" or "tool-permission-blast-radius" that would catch this category of change. (confidence: inferred)
8. [outside-view §5] Proposal trades a *visible bounded* loss (orchestrator paraphrase) for a *potentially invisible unbounded* loss (wrong-path writes). (confidence: inferred)
9. [outside-view §5] Reversal cost is asymmetric — once distillers/synthesis read critic-emitted artifacts, rollback requires rewriting consumers. (confidence: inferred)
10. [outside-view §3] Repo's existing path-discipline rules and per-step path naming move proposal *above* the base rate; self-modification + parallel-invocation concurrency move it *below*. (confidence: inferred)

## Authority-framed claims
None. The subagent cited sources by name and link rather than ventriloquizing authors.

## Contradictions surfaced
- **Goal-achievement vs. clean-transition rates.** Subagent estimates the goal (audit faithfulness) at ~80% achievable but the transition (without new failure class) at only ~50–60%. These pull in opposite directions on whether to ship.
- **Stated motivator vs. dominant risk.** Paraphrase-loss is the *stated* motivator but the subagent claims wrong-path writes are the larger (silent, unbounded) risk — i.e., the proposal may be optimizing the smaller problem.
- **Existing repo strengths vs. new failure surface.** Path-discipline + per-step naming are cited as base-rate-lifting features, while parallel critic invocation in step 10 is cited as introducing a TOCTOU/collision surface that prose-return did not have.

## Subagent's own verdict (verbatim)
"**Below base rate** for clean transition. The goal is achievable, but the proposal as stated is missing three load-bearing artifacts that the reference class says you need:
- A **session-id propagation contract** with explicit assertion at write-time (reject writes whose path doesn't match the active session).
- A **shared output schema** across the three lenses, declared once, validated at write-time.
- A **reversibility plan** — explicit answer to 'if this introduces silent corruption in the first 20 sessions, how do we roll back without rewriting consumers?'"

Lift-to-tolerance condition (verbatim): "add the three above, plus add (or name) a critic-panel lens responsible for tool-permission-blast-radius, so the self-modification blind spot is closed before the change ships."

## Gaps the subagent missed
1. **No canon reconciliation.** Subagent declared the canon-access gap upfront; orchestrator must cross-check the librarian's `canon.md` for any corpus passages on tool-permission expansion or self-modifying review systems before treating these base rates as final.
2. **No quantified incident rate for self-modifying review systems.** Tertiary class is qualitative-only ("no clean base-rate data"). Decision under uncertainty here is not bounded by the subagent's analysis.
3. **No examination of the alternative design.** Subagent did not consider intermediate options (e.g., critics return structured prose that orchestrator writes, or critics write to a single shared append-only log instead of per-lens artifacts). The framing is binary (Write-grant vs. status quo).
4. **No cost estimate for the three "load-bearing artifacts."** The verdict prescribes three additions but does not estimate their implementation cost vs. the cost of the paraphrase-loss the proposal addresses.
5. **No discussion of detection latency.** Claim that wrong-path writes are "silent and unbounded" is not paired with an estimate of how long until a consumer-failure surfaces them.

## Token budget
~880 tokens.
