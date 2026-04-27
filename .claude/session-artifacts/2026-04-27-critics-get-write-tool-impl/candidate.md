# Candidate recommendation — `2026-04-27-critics-get-write-tool-impl`

## Position

**Ship the proposal with two additions and one explicit non-addition.**

The implementation grants `Write` to the three critic agents and replaces the orchestrator's paraphrase work with critic-authored per-lens files plus an orchestrator-authored thin index. Two structural defenses address the frame-level objection from `challenges.md`. One thing is explicitly *not* added, with reasons.

### What ships (additions to the original entry plan)

1. **All three Plan items from the original entry**, unchanged:
   - Add `Write` to the three critic frontmatters: `tools: Read, Write, WebFetch, WebSearch`.
   - Add an output-persistence instruction to each critic body naming the path `.claude/session-artifacts/<session-id>/critiques/<lens>.md` and the inline-return contract (verdict + single most important objection).
   - Update CLAUDE.md Step 10: each critic writes its own file; orchestrator reads the files; orchestrator builds a thin index `critiques.md` (3-row table: lens · verdict · path).

2. **(NEW — Defense 1, ballot-independence) "Do not Read sibling critique files" instruction added to each critic's body.** A single sentence in the same Mandatory-stance block: *"You must not Read other critics' verdict files (`critiques/<other-lens>.md`) before completing your own write. The panel's value depends on lens independence; reading siblings collapses three votes into one."* This is instruction-level enforcement of vote independence, mirroring the instruction-level write-path scoping pattern established by `subagent-distiller`, `scope-mapper`, `frame-challenger`. It is not a hook; it is a clear contract the agent can adhere to. Symmetric to how write-path scoping is enforced today.

3. **(NEW — Defense 2, anti-rubber-stamping) "Replan-on-self-modification" rule added to CLAUDE.md Step 11.** A single bullet: *"If the candidate's scope-map includes any primitive under `.claude/agents/critic-*.md`, the orchestrator must route to **replan** regardless of panel verdict — even if all three lenses approve. Self-modifying changes pass through frame re-challenge, not panel approval alone, because the lens reviewing the change is the lens being modified."* This forces self-modifying changes (including this one, going forward) through frame-level re-challenge rather than letting a unanimous-approve close the loop. Cheap. No new agent. No new artifact.

### What is explicitly *not* added (and why)

- **No co-ship with upgrade #3 (PostToolUse verification hook).** The frame-challenger argued #3 should be a co-shipping prerequisite for the parallel-write case specifically. The candidate rejects that on the basis that (a) #3 is a `profound`-tier un-specified entry whose scope is materially larger than this entry, (b) the modal failure mode #3 guards against (wrong-path writes / stale-session contamination) is **detectable post-hoc** by reading session directories — i.e., the failure is not silent enough to require pre-deployment poka-yoke, and (c) the operator can re-rank #3 to the next session if the first ~5 sessions under the new shape surface that risk in practice. **This rejection is a load-bearing assumption** (see Assumptions §A2 below) and is the most likely place the candidate is wrong.

- **No co-ship with upgrade #14 (hard gates as harness hooks).** Same logic: orthogonal in scope, and the load-bearing prose rule "critic writes only to `<id>/critiques/<lens>.md`" is enforceable via instruction in the same way the existing Write-holders' rules are.

- **No shared output schema across the three lenses.** Each critic's existing output structure is preserved (architecture: 6 sections, operations: 7 sections, product: 6 sections — they diverge in a deliberate way that maps to lens-specific concerns). A schema would compress that divergence into uniformity that costs more than it saves; the thin index gives the orchestrator + Step 12 a uniform aggregate without forcing uniformity on the lens content.

- **No rejection of the change in favor of "structured-return + orchestrator-authored verbatim writes" (option E from generator notes).** That alternative was considered and rejected: it preserves ballot independence (good) but does not give the audit artifact a single author (the orchestrator is still the writer, which the original entry's *essence* objects to). Audit faithfulness via "trust the orchestrator to copy-paste verbatim" is structurally weaker than audit faithfulness via "the agent itself wrote the file."

## Tradeoffs (named)

| Tradeoff | Direction | Rationale |
|---|---|---|
| **Audit faithfulness ↑ vs. write-surface attack/error surface ↑** | Accept the trade. | The audit artifact is the central output of the panel; making it author-original is a category improvement. The new error surface (wrong-path writes) is bounded and detectable. |
| **Ballot independence ↓ (instruction-level only) vs. recursion / sibling-read prevention ↑** | Accept instruction-level. | Hook-level enforcement requires upgrade #14 + a path-validation primitive that does not exist. Instruction-level is the convention used by every other Write-holder in the stack. The risk of a critic violating the instruction is symmetric to the risk of any Write-holder violating its scoping instruction — non-zero, but uniform across the stack rather than concentrated here. |
| **Step 11 strictness ↑ (auto-replan on self-modification) vs. session length ↑** | Accept the cost. | Self-modifying changes are rare (the lab fires one or two per quarter, judging by the upgrade ledger). Auto-replan on those specifically does not bloat the average session. The benefit is a structural defense against rubber-stamping that is independent of any individual critic's behavior. |
| **Aggregate `critiques.md` replaced (not preserved-as-empty) vs. legacy reader compatibility** | Accept the replacement. | The aggregate's full-transcription form is the primitive being replaced. Keeping an empty file would carry no signal; keeping it as a thin verdict-index does carry signal (a single read for Step 12). The thin-index variant is `replace`-with-residue, not preservation. |
| **No hard dependency on un-built upgrades vs. outside-view's "below base rate" forecast** | Accept the forecast risk; mitigate via instruction-level defenses. | Coupling to un-built upgrades is a worse failure mode (indefinite delay) than shipping under a known base-rate handicap. The first ~5 sessions under the new shape are themselves the cheapest experiment that would demote #3/#14 from "should co-ship" to "actually was needed." |

## Assumptions (the recommendation flips if any are wrong)

**A1. Instruction-level "do not Read sibling critique files" is sufficient to maintain ballot independence in practice.**
*Flips if wrong:* If any critic, in any session, Reads a sibling critique file before completing its own write — even once — the proposal is materially worse than the status quo (today's prose-return architecture cannot leak sibling content because the orchestrator does not re-prompt critics with each other's output). Detection: a `PostToolUse` hook on the critic agents that logs every `Read` they perform and flags any path matching `critiques/*.md` from the same session-id. This hook is cheap (one regex) and is not in the candidate but should be added if A1 ever fails.

**A2. Stale-session / wrong-path writes are bounded by instruction-level scoping in the same way they are for `subagent-distiller`, `scope-mapper`, and `frame-challenger`.**
*Flips if wrong:* If the parallel invocation in Step 10 introduces a class of failure (TOCTOU, session-id mis-propagation under concurrency, cross-contamination) that does not exist for the sequential Write-holders, then the proposal needs upgrade #3's verification hook as a hard prerequisite, not a "natural complement." The frame-challenger explicitly named this as the strongest argument against the candidate's no-co-ship rejection. **This is the most load-bearing assumption.**

**A3. The "replan-on-self-modification" rule effectively closes the recursion blind spot.**
*Flips if wrong:* If the rule changes only the orchestrator's routing (always-replan on critic-* changes) without changing the critic's incentive to approve self-modifying expansions, then the defense is decorative — the next iteration of replan still goes back through the same biased panel. The strongest version of this defense is the external second-opinion (shadow-comparator from upgrade #5), which is un-built. If A3 is wrong, the candidate ships under known panel-approval-discount on self-modifying changes, with no concrete discount factor named.

**A4. Audit-faithfulness is a category improvement (not a marginal one) over orchestrator-paraphrase.**
*Flips if wrong:* If the orchestrator-paraphrase failure mode that motivated the entry is *bounded and visible* (orchestrator transcript shows the paraphrase) and the new failure modes (wrong-path writes, schema drift, ballot-leak) are *unbounded and invisible*, then the proposal trades a known small loss for a potentially large hidden one — exactly the outside-view's claim #5. The candidate disagrees with this read, but the disagreement is not airtight: paraphrase loss is bounded only if someone re-reads the transcript, which under operator load is exactly the work the entry was trying to remove.

## Frame-level objection from `challenges.md` — addressed

The frame-challenger's carry-forward objection: *"the audit-faithfulness gain is small and bounded; the ballot-independence and self-modification-rubber-stamping risks are each potentially larger and unbounded — and the current frame names neither as a load-bearing constraint."*

How the candidate addresses it:

- **Ballot independence** is named as Defense 1 (instruction-level no-sibling-read) and surfaced as Assumption A1 with a concrete detection mechanism for when the assumption fails. The frame is no longer silent on the constraint; it is named, instrumented (hypothetically — A1's hook is named, not built), and falsifiable.
- **Self-modification rubber-stamping** is named as Defense 2 (replan-on-self-modification rule) and surfaced as Assumption A3 with a named stronger version (shadow-comparator) and a known discount factor that ships if A3 holds.
- **The "smaller-and-bounded vs. larger-and-unbounded" framing** is addressed by Assumption A4, which the candidate explicitly disagrees with but flags as the assumption most likely to flip the recommendation. The disagreement is honest, not defensive.

The candidate does *not* fully neutralize the frame-objection — it accepts that the proposal carries a known recursion-bias discount and a known parallel-write risk. It argues those costs are bounded by instruction-level defenses + post-hoc detection, not by harness enforcement. That argument is itself an assumption, and one of the three lenses (operations, most likely) will probably push back on it.

## Ways this could be wrong (named)

1. **Sequential-vs-parallel concurrency assumption.** The "Write-holder precedent" leans on three agents that run sequentially. The critics run three-in-parallel. If TOCTOU or invocation-order effects produce a class of failure the precedent does not see, A2 fails and the candidate needs co-ship with #3.

2. **Self-modification cadence assumption.** "Self-modifying changes are rare" is asserted without measurement. If the lab's actual rate is materially higher (e.g., once per session in the next quarter), the auto-replan rule materially extends average session length, and the trade in Tradeoffs §3 fails.

3. **No-shared-schema assumption.** The candidate keeps lens-specific output structure. If schema drift across the three lenses surfaces in Step 12 synthesis (e.g., the verdict label vocabulary diverges, or the frame-objection block format diverges enough that the orchestrator must normalize), the orchestrator's paraphrase work returns under a new name.

4. **No-co-ship-with-#3 rejection assumption.** Outside-view rated the proposal "below base rate" specifically because the missing artifact is a session-id propagation contract with write-time assertion — exactly what #3 builds. The candidate is gambling that post-hoc detection (read the directory, see if files landed) is sufficient. If that gamble fails in the first 5 sessions, the candidate must replan to a co-ship.

5. **The classifier label `extend` vs. `new`.** The frame-challenger argued the candidate is structurally `new` (two responsibilities) and the `extend` framing licenses unwarranted precedent-by-analogy. The candidate proceeds under `extend` framing while accepting the secondary `replace` label on the aggregate. If the panel finds the change introduces emergent role-conflict (reviewer ≠ author-of-record at the same agent), the classification was wrong and the candidate ships under a frame the classifier did not authorize.
