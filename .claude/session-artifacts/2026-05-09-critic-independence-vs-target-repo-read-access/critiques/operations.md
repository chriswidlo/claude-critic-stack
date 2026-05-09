# Critic — Operations lens

## 1. Most likely incident

At session-time T, a routine architecture review under the new "default-no-target" contract approved a candidate whose recommendation contradicted a load-bearing target-repo invariant; symptom was a clean three-lens approve followed by the human merging the change and discovering on first run that the target's existing constraint made the recommendation a no-op (or worse, a regression). Root cause was the candidate-composition discipline note (move 3) being silently violated under length pressure — the orchestrator paraphrased the target-repo invariant into the candidate body rather than quoting it as `<target>/...`, the lens read paraphrase as ungrounded reasoning, and the per-lens opt-in to `$CRITIC_TARGET` (move 2) was never logged because the orchestrator believed the candidate already carried the constraint.

## 2. Blast radius

Cannot estimate in users/regions — this stack does not run production traffic. The relevant blast radius is **session-shaped**:

- **Per-incident:** one bad recommendation lands in the user's target repo. If the user is the sole operator (the case in this stack today, per Explore §10 — "no session in this repo has yet exercised critique-prep + critique-start end-to-end"), blast radius = one merge, one revert, one rebuild of trust in the panel.
- **Cross-session amplification:** the new contract is global — every future session inherits it. A silent default-allow drift in the decision-log opt-in (see §4) means the failure mode is not one bad session, it is a *class* of sessions where the panel produces ungrounded approvals while claiming grounded calibration. I cannot estimate the rate; no metric in the repo currently measures it.
- **Trust radius:** if the user discovers post-hoc that critic verdicts have been rendered against paraphrased target content rather than quoted, the credibility of every prior approve in the ledger is retroactively in question. That is a wider blast than any single session.

## 3. Rollout / rollback

- **Rollout strategy:** none named. The candidate proposes editing CLAUDE.md, `critique-start/SKILL.md`, and adding a discipline note in step 9. These are atomic edits to load-bearing prose; there is no flag, no canary, no shadow-mode-for-the-rule-itself. The "cheap experiment" (move 4) is gated *before* the structural changes (1–3), but moves 1–3 are still proposed as a single CLAUDE.md commit. Missing: a staged rollout where the discipline note ships first as advisory, the contract change ships second after N sessions have been audited under the new note.
- **Rollback path:** git revert on the CLAUDE.md / SKILL.md edits. This is mechanically a forward-fix in disguise — once N sessions have run under the new contract and produced artifacts that assume default-no-target, reverting the prose does not undo their decision-log entries or their candidate-composition shape. The artifacts persist; the contract they were built against does not. There is no rollback to the *artifact state*, only to the *rule text*.
- **Two-systems-running period:** unbounded. The candidate does not name a deprecation window for the old "if they verify facts" wording. Existing in-flight sessions (none today, per Explore §10, but the *next* session could start before the edit lands) would run under whichever wording was current at step 10 invocation. The candidate is silent on this.
- **Cost during the dual period:** not named. At minimum: orchestrator must remember which contract a given session was started under, and the ledger schema does not currently capture this.

## 4. Observability gap

This is the load-bearing operations critique. The candidate makes the following invisible:

- **Contract violation by a critic.** If `critic-architecture` decides to `WebFetch` a public GitHub URL named in the candidate (Explore §inferred 8 — "WebFetch is a loophole rather than a backdoor"), the new "default-no-target" rule has been violated. **There is no detector.** No hook (Explore §26 — "no `hooks` section present"), no agent-file-level prohibition, no post-run audit. The operator finds out only by reading the critic's output and noticing it cites target content the critic was not supposed to have. I do not know whether any session-artifact tooling currently greps critic outputs for `<target>/...` dereferences; the candidate does not propose adding one.
- **Decision-log opt-in becoming silent default-allow.** The candidate's move 2 says: "to pass `$CRITIC_TARGET` to a specific lens, the orchestrator must record the decision in `decision-log.md`." This is an unenforced human discipline. Failure mode: orchestrator passes `$CRITIC_TARGET` and forgets to log; or logs once at session start with vague language and then re-uses the grant across multiple step-10 invocations without re-logging. **There is no detector for "the orchestrator passed `$CRITIC_TARGET` to a lens but did not log it."** A linter that diffed the critic invocation arguments against `decision-log.md` entries would close this — the candidate does not propose one. Without it, this is a control on paper, not in practice.
- **Candidate-composition discipline drift.** Move 3 forbids paraphrasing target content into the candidate body. There is no metric for "candidate.md contains target-repo narrative not behind a `<target>/...` reference." A simple grep heuristic ("does candidate.md mention strings that appear in target-repo content but not behind a quote-marker") is not proposed. I do not know whether such a check is feasible without target-repo read access from the linter — possibly not, which is itself an observability problem the candidate inherits.
- **The metric that would confirm "the thing went well."** The intended outcome of the discipline note is "shadow lanes agree on lenses where target framing was disciplined out." That is the experiment in move 4. After move 4 runs once, **there is no proposed ongoing metric** — no per-session shadow-comparator agreement-class trend, no "sessions where comparator returned `disagree` on candidate-shaping" counter. The discipline becomes invisible after the one-shot probe. I cannot confirm whether the comparator's `agree | partial-agree | disagree | unavailable` outputs are aggregated anywhere across sessions; my read of `.claude/agents/critic-comparator.md` and the LEDGER references is that they are not.

## 5. Cost at failure

- **Steady-state cost when the contract holds:** every session pays a small orchestrator-discipline tax (compose candidate without paraphrasing target; check whether to log opt-in). Tractable.
- **Failure-mode cost #1 — silent default-allow drift on the opt-in.** The panel produces verdicts that *claim* default-no-target calibration but were rendered against `$CRITIC_TARGET`-grounded inputs. Cost: every approve in the ledger after drift began is now of unknown type. Recovery requires re-reading every session's step-10 invocation prompt, which is not currently archived in the session artifact (Explore gap §1 — "Exact step-10 prompt structure" not retrievable from session history). The retro-audit is *not possible from on-disk evidence*.
- **Failure-mode cost #2 — discipline-drift retry storm.** If a future cleanup session tries to enforce the discipline note retroactively (re-run sessions under the new rule to validate prior verdicts), each re-run costs `agent-calls × 6` if `SHADOW_PANEL=1` (per CLAUDE.md step 10). The candidate's "cheap experiment" is one session under shadow; a retroactive validation pass is N sessions under shadow. The candidate does not name N or budget it.
- **Failure-mode cost #3 — frame-level trust failure.** If the panel's revised independence claim ("decorrelated by role/aspect on a shared input, not information-independent") is later found to be itself untrue (i.e., the role-orthogonality assumption A3 in the candidate flips — three Opus lenses on the same candidate produce one voice in three accents), the entire rebuilt claim collapses. The cost here is not an incident, it is a credibility wipe of the panel mechanism. The candidate names this risk in W2 but does not propose a measurement that would catch it before public commitment.
- **On-call load:** there is no on-call, but there is an operator. Operator load increases by: (a) per-session decision about whether to log opt-in, (b) per-session discipline check on candidate composition, (c) ongoing watch for contract violations that nothing detects automatically. This is unbudgeted.

## 6. Frame-level objection

**The candidate frames this as a contract-design problem; the operational view is that it is an enforcement problem with no enforcement primitive proposed.**

Every move in the candidate (re-stated claim, explicit table, discipline note, one-shot experiment) operates at the level of *prose in CLAUDE.md and SKILL.md*. None of them is enforced by:
- a hook (none exist in `.claude/settings.json`, per Explore §26),
- a linter on session artifacts,
- a pre-merge check on candidate.md,
- a runtime guard on the Agent invocation (impossible from inside the stack today),
- a post-hoc audit script.

The only existing enforcement primitive in the stack is the **hard gate at step 9** (refuse to proceed without `scope-map.md` and `challenges.md`) — and that gate is itself prose-enforced by the orchestrator agreeing to refuse. The candidate proposes adding more prose-enforced contracts to a stack whose existing prose-enforced contracts are already operating on the honor system. Operationally, this multiplies the surface area of "rules a busy orchestrator can quietly skip" without adding any detector.

The reframe an operations lens demands: **before adding move 2 (the per-lens table) or move 3 (the discipline note), name the detector that would reveal a violation post-hoc.** If no detector exists or can be built, the move is a wish, not a control. The candidate's move 4 (the cheap experiment) is the one move that has a built-in detector — the comparator's agreement class — but it is one-shot and produces no continuous signal.

A second frame-level objection: **the candidate treats "log it in `decision-log.md`" as if logging were the control. Logging is observation, not control.** A control would be "the orchestrator cannot pass `$CRITIC_TARGET` to a lens without first writing a decision-log entry that the Agent invocation reads." That is not what move 2 specifies; move 2 specifies a manual two-step where the orchestrator both passes the variable and (separately, by discipline) writes the log. The two are not coupled. Coupling them — even via a tiny script that refuses to invoke a lens unless a matching decision-log entry exists for this session — would be a real control. The candidate does not propose this.

## 7. Verdict

**rework**

What would change the verdict: name an enforcement primitive (a linter, a pre-invocation script, or a post-session audit grep) for at least one of moves 2 and 3, and bound the rollout (advisory note ships first; contract change ships only after the one-shot probe in move 4 returns a measurable signal and at least one subsequent session has been audited under the advisory note without violation).
