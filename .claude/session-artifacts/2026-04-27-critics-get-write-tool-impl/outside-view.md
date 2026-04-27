# Outside-view forecast — granting filesystem write to previously-prose-only agents

## 0. Canon-first note

**Declared gap.** The outside-view agent could not grep `canon/corpus/` from its invocation (no Bash/Grep tool available). Treat the base-rate numbers below as **first-principles + web-evidence estimates**, not canon-anchored. The orchestrator should reconcile against `canon.md` (which the librarian produced in parallel).

Web sources used (currency only, not promoted to canon):
- Golden Corpus, *The Four Ways AI Agents Fail* — agent failure taxonomy.
- safishamsi/graphify Issue #195 — concrete Claude Code incident: subagent silently under-counted by >50% because verb similarity routed work to a read-only Explore agent. **Directly relevant.**
- Embrace The Red — ACL race conditions and TOCTOU in concurrent permission systems.
- TrueFoundry — multi-agent production reality, default-open permissions causing catastrophic deletions.

---

## 1. Reference class

The proposal sits at the intersection of **four candidate classes**, ranked by predictive power:

**Primary: "Audit-trail systems where the recording responsibility moves from a downstream paraphraser to upstream emitters."** JUnit-XML / structured-log / dictation-software class. Each producer becomes responsible for its own structured artifact; the aggregator stops transcribing.

**Secondary: "Tool-permission expansion in agent stacks where the new tool is filesystem write."** Agents that previously had only read/search/return-prose now get Write.

**Tertiary: "Self-modifying review systems"** — the critic stack approving a change to itself. Small reference class, distinctive failure mode (the reviewer's blind spot is the change being reviewed).

**De-prioritized: "Multi-agent systems migrating from prose to structured artifacts"** — too broad; collapses to the primary class once the artifact contract is specified.

The primary class is most predictive because the **technical change is small (add a Write tool) but the contract change is large (each agent now owns a path, a schema, and a write-time guarantee).**

---

## 2. Base rate

**Primary class — paraphraser-to-emitter migrations:**
- CI test reporting (humans pasting console output → JUnit XML emitted by test runners): **~85–90% successful**, dominant pattern. Failure mode is rarely the migration itself; it's *schema drift between emitters*.
- Dictation-software replacing transcribed-dictation in medical/legal: **~70–80% successful** when the schema is constrained; lower when free-form.
- Structured logging (JSON logs from each service vs. centralized log-parsing): **~80% successful**, with a long tail of "every service logs slightly differently" pain.

**Composite estimate for primary class: ~75–85% achieve the audit-trail-faithfulness goal**, but **~40–60% incur a *new* class of failure** (schema drift, write collisions, stale artifacts) that didn't exist before.

**Secondary class — tool-permission expansion to filesystem write:**
- The dominant failure when agents gain Write is **wrong-path writes, stale-session cross-contamination, and silent under-counting** (the agent thinks it wrote; it wrote to the wrong place or wrote a stub).
- Rough estimate: **~30–50% of "give the agent the obvious next tool" rollouts cause at least one observable incident in the first 50 invocations.** Most are recoverable; ~10–15% cause silent corruption only detected later.

**Tertiary class — self-modifying review systems:** No clean base-rate data. Qualitative pattern: review systems are systematically blind to changes that match their own affordances. If the critic-panel doesn't have a lens that asks "does this change introduce a path-discipline regression?", it won't catch one.

**Net base rate: the *goal* (audit faithfulness) is achievable at ~80%. The *transition* (without introducing a new failure class) is achievable at ~50–60%.**

---

## 3. Position relative to base rate

**Features that move this proposal *above* the base rate:**
- Session-id pathing convention exists and is enforced in CLAUDE.md — strong **schema discipline up front**, the #1 predictor in the JUnit-XML reference class.
- Repo has explicit **path-discipline rules** (no absolute paths, repo-relative Markdown links). Guards against the most common write-class failure.
- Orchestrator workflow names artifact paths *per step* — agents don't pick paths, they receive them. Avoids the verb-similarity-routing class of failure that bit graphify.
- Adversarial-review culture: a critic-panel exists that *can* be pointed at the change.

**Features that move this proposal *below* the base rate:**
- **Self-modification.** The critics being granted Write are the same critics whose verdicts gate the change. The lens that should catch "critics writing artifacts is a category change" may not exist.
- **Stale-session cross-contamination risk.** If a critic from session A ever runs in session B's context (orchestrator passes wrong session-id, or a critic caches), it writes to the wrong artifact. Prose-return has no such failure mode.
- **No write-time concurrency contract stated.** Three critics in step 10 run in parallel. If they share any path or compute paths via similar logic, TOCTOU/collision is now possible. Prose-return serializes naturally through the orchestrator.
- **Paraphrase-loss is the *stated* motivator, but it's the smaller risk.** Paraphrase loss is bounded and visible. Wrong-path writes are silent and unbounded.
- **Reversal cost is asymmetric.** Once critics write, downstream tooling (distillers, future agents) will start reading those artifacts. Rolling back means rewriting consumers too.

**Net position: roughly *at* the base rate for goal-achievement (~80%), but *below* the base rate for clean transition (~40–50%).**

---

## 4. Typical failure mode for the reference class

For the **primary class** (paraphraser → emitter): **"schema drift across emitters, detected months later when a consumer breaks."** Each emitter does its own thing; the aggregator stops normalizing; consumers silently get inconsistent inputs. JUnit XML's history is exactly this.

For the **secondary class** (Write-tool grant): **silent wrong-place writes** — the agent reports success, the file is created somewhere, but it's not where the orchestrator looks next, or it's in a stale session directory, or it overwrites a prior artifact. The graphify incident is the canonical instance.

For the **tertiary class** (self-modifying review): **the change passes review because the review framework lacks a lens for the category of change being made.** You don't catch what you can't see.

---

## 5. The failure mode this proposal is most exposed to

In priority order:

1. **Stale-session cross-contamination / wrong-path writes.** A critic computes its own path from session-id. Orchestrator's session-id propagation becomes a new load-bearing invariant. Under parallel invocation in step 10, a bug here writes critic-architecture's verdict into yesterday's session, and step 10's aggregator reads the wrong file. **Silent. High-impact. Hard to detect without explicit assertions.** Modal failure given the proposal's design.

2. **Schema drift between the three critic lenses.** Each lens writes its own artifact. Without a shared schema (header fields, verdict vocabulary, frame-objection block), the aggregator at step 10 starts doing schema-normalization work — the paraphrase-loss problem the change was meant to eliminate, just relocated.

3. **Self-review blind spot.** The critic-panel approves this change. None of the three lenses (architecture / operations / product) is named "audit-integrity" or "tool-permission-blast-radius." The lens that should catch *"this expansion changes the failure surface from bounded-paraphrase to unbounded-wrong-write"* may not exist in the panel.

4. **Reversal cost lock-in.** Once critics emit artifacts, distillers and the synthesis step (12) will read them directly. Rolling back to prose-return means rewriting consumers. The proposal does not name a reversibility plan.

5. **Audit-faithfulness-as-stated may not actually improve.** Paraphrase loss in the orchestrator is *visible* (transcript shows what the orchestrator wrote). Wrong-path or partial writes are *invisible* until a consumer fails. The proposal trades a visible bounded loss for an invisible unbounded one.

---

## Verdict

**Below base rate** for clean transition. The goal is achievable, but the proposal as stated is missing three load-bearing artifacts that the reference class says you need:

- A **session-id propagation contract** with explicit assertion at write-time (reject writes whose path doesn't match the active session).
- A **shared output schema** across the three lenses, declared once, validated at write-time.
- A **reversibility plan** — explicit answer to "if this introduces silent corruption in the first 20 sessions, how do we roll back without rewriting consumers?"

What would lift it to "within tolerance": add the three above, plus add (or name) a critic-panel lens responsible for tool-permission-blast-radius, so the self-modification blind spot is closed before the change ships.

---

## Sources

- [Claude Code subagent silently under-counted (graphify Issue #195)](https://github.com/safishamsi/graphify/issues/195)
- [The Four Ways AI Agents Fail — Golden Corpus](https://goldencorpus.com/building/when-agents-fail)
- [Why AI Agents Fail: 3 Failure Modes (DEV)](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb)
- [Common Agent Failure Modes — agentwiki](https://agentwiki.org/common_agent_failure_modes)
- [Multi Agent Architecture: Production Reality — TrueFoundry](https://www.truefoundry.com/blog/multi-agent-architecture)
- [Race conditions when applying ACLs — Embrace The Red](https://embracethered.com/blog/posts/2020/applying-acls-and-race-conditions/)
- [TOCTOU race conditions — SEI CERT](https://wiki.sei.cmu.edu/confluence/x/RdUxBQ)
- [JUnit XML Format Guide — Gaffer](https://gaffer.sh/blog/junit-xml-format-guide/)
- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
