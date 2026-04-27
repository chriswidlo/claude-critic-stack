# Operations-lens critique — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Lens.** Operations.
**Reads.** [candidate.md](../candidate.md), [frame.md](../frame.md), [challenges.md](../challenges.md), [scope-map.md](../scope-map.md), three distillations.

## 1. Most likely incident

At time T (≈ 4–8 months after this PR lands), a maintainer materially restructures [CLAUDE.md](../../../../CLAUDE.md) (changes the 12-step contract, adds/removes an agent, reshapes the panel rules) without revisiting the README's audience declaration or the deferred upgrade entry; the trigger fires silently, no observation mechanism alerts, and the README's gap statement now points at a contract that has shifted under it. Root cause: the candidate encodes the deferral trigger as a sentence inside an upgrade-entry README that nobody has a routine for re-reading on CLAUDE.md edits.

## 2. Blast radius

- **Affected reader populations:** every Claude session that auto-loads CLAUDE.md is fine. The radius is the human-reader population — and per the candidate's audience pick (maintainer + Claude), that population is approximately *one*: the maintainer.
- **Downstream artifacts that drift if the trigger never fires:** the upgrade entry stays at 🔨 implemented forever; the punch list shows ✅ done; the next stale-doc punch-list item six months out is the *next* incident, not this one.
- **Forker traffic:** the candidate's Assumption 1 names a 30-day repo-traffic test but does not name a metric source (GitHub Insights? star history? referrer logs?). Until that's named, the blast-radius-on-forkers number is "unknown, possibly zero, possibly the entire external-adopter population."

The radius is small in absolute terms because the audience is small. That is not the same as saying the radius is acceptable; if the audience pick is wrong, the radius is *the entire actual audience*.

## 3. Rollout / rollback

- **Rollout strategy.** None named. Single PR shipping six moves. For a docs-only change in a personal-lab repo this is *defensible* — but the candidate does not say so explicitly.
- **Rollback path.**
  - File deletion + `rmdir`: trivially reversible via `git revert`.
  - README rewrite: reversible.
  - Audience declaration sentence: reversible by editing the line out — but the *consequences* of the declaration shaping six months of subsequent doc decisions are *not* reversible by reverting the sentence. Same cost pattern as a wrong DB schema migration that ran for a quarter.
  - Lifecycle-row edits: reversible.

  **The non-reversible move the candidate undersells:** if the audience declaration is wrong and downstream doc work happens *under* it for 3–6 months, the rollback is "re-do whatever doc work was committed assuming the wrong audience."

## 4. Observability gap (largest operational hole)

- **Doc/code drift detection.** Nothing in the candidate fires when CLAUDE.md and the README's framing of CLAUDE.md diverge. No pre-commit hook, no CI grep, no scheduled audit. The candidate's Assumption 2 is a *discipline*, not a *control*.
- **Trigger observation mechanism.** The candidate names three triggers:
  1. *"a contributor other than the maintainer needs to run the workflow"* — observable by what? Nothing wired.
  2. *"CLAUDE.md is materially restructured"* — `git log CLAUDE.md` does not distinguish material from cosmetic. No threshold defined.
  3. *"the README's audience-declaration changes"* — circular; this is a trigger on the *maintainer's own action*, not on the *world*.

  **None have a fire mechanism.** The candidate admits this in §"Ways this could still be wrong." A trigger without an observer is a wish.
- **Audience-test metric.** Assumption 1 names *kinds* of metric without committing to any. Should either commit to a one-line scheduled-check (calendar reminder on a fixed date) or mark Assumption 1 as untestable.
- **What the candidate makes invisible.** Pre-candidate, the README-vs-CLAUDE.md drift was visible because the README's "three subagents" claim was demonstrably falsifiable. Post-candidate, the audience declaration is a maintainer-internal claim about their own intent, with no external referent — *not falsifiable* by reading any other artifact.

## 5. Cost at failure

- **Human on-call load.** Cost-at-failure mode is *re-explanation*. Each time a Claude session or future contributor reads the README and forms a wrong mental model, the maintainer pays a re-explanation cost.
- **Compounding cost.** The modal failure is a 1–3-year *known-stale-but-not-wrong* backlog state.
- **Secondary failure (from outside-view):** *"a third stale derivative gets written to fill the gap"* — operationally, the cost of the gap statement succeeding too well; readers who hit the gap may write their own stopgap.

## 6. Frame-level objection

**The candidate frames this as a doc-correctness problem with a deferred-doc-design tail. The operations frame is that this is a control-design problem, and the candidate ships zero controls.** Both the audience declaration and the trigger-based deferral are claims about the *future*, and neither is paired with an observation mechanism that fires when the claim becomes false. Same shape as deploying a circuit breaker without metrics on the trip count.

The outside-view distillation's claim that *"trigger-based deferrals complete materially more often than time-based"* is asserted without quantification. Even granting the relationship, *both* are below 50% completion in the cited reference class, and the candidate's triggers as written have no fire mechanism, so the candidate's actual completion rate is bounded above by the time-based rate (20–35%), not the trigger-based rate. The frame *"defer with a trigger"* is performing the work of feeling different from time-based, when in operational reality it is not.

## 7. Verdict

**rework.**

Verdict would change to `approve` if the candidate adds:
- (a) one concrete control that fires when at least one trigger is met — minimum acceptable: a calendar reminder on a fixed date (e.g., 2026-07-27, three months out) to re-read the audience declaration against CLAUDE.md and the upgrade entry; better: a pre-commit hook or CI grep that fails when CLAUDE.md's agent list diverges from the README's framing.
- (b) names the specific traffic metric and check cadence for Assumption 1 (or marks Assumption 1 as untestable and re-prices the recommendation accordingly).
