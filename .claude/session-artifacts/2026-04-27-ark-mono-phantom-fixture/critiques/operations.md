# Critique — Operations lens

Session: `2026-04-27-ark-mono-phantom-fixture`
Lens: operations (translated: blast radius of decisions, cost over time, observability of whether the recommendation is working, rollback shape)

## 1. Most likely incident

At T+90 days from this session, a future operator opens [`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md), sees item 5b sitting unstarted next to items 6–13 also sitting unstarted, and silently retires the whole punch list as "old planning debris" during a janitorial pass. Root cause: this proposal closed the *visible* defect (doc-divergence) and shifted the *invisible* one (an unrun regression test in a repo that claims regression discipline) into a row whose only forcing function is operator memory — the proposal added no due-date, no reminder, no observability hook, and no link from any active surface back to 5b.

## 2. Blast radius

If 5b rots:
- Affected artifacts: [`tests/regression/ark-mono-connector-routing.md`](tests/regression/ark-mono-connector-routing.md) (continues to claim acceptance criteria nobody has verified), [`.claude/session-artifacts/exemplars/.keep`](.claude/session-artifacts/exemplars/.keep) (stays empty), the regression-discipline claim in [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md) (becomes load-bearing rhetoric).
- Affected workflows: every future invocation of the 12-step workflow runs without a green anchor.
- Affected operators: the next person to ask "is this stack actually validated?" gets a No, dressed as a Yes by the presence of [`tests/regression/`](tests/regression/).

## 3. Rollout / rollback

**Rollout shape:** step 1 atomic; step 2 atomic. Commit rollout clean.

**Rollback of step 1 (placeholder slug):** cheap. Reverting restores the prior phantom slug. Cost: one revert. **Rollback signal not specified** — there is no review gate beyond the committing operator's preview.

**Rollback of step 2 (file 5b):** cheaper still — delete the row. But this rollback *causes* the most-likely-incident in §1: silently deleting 5b is indistinguishable from silently letting it rot.

**Two-systems-running period:** the period where the punch-list contains both the closed item-5 row and the open 5b row. Outside-view base rate from the distillation: <30% of "ceremony without baseline" infra exercised within 6 months. The proposal accepts this base rate without a forcing function to beat it.

## 4. Observability gap

- **Whether 5b is rotting.** No metric, no scheduled check, no link from any "live" surface back to item 5b.
- **Whether the placeholder is being copied as a real slug.** Mitigation proposed is documentation, not a control. There is no grep-based or lint-based check named.
- **Whether the distiller-step gap is the only spec-currency drift.** Assumption #2 defers verification to 5b's contract step. If 5b rots, the deferred verification rots with it.

## 5. Cost at failure

Failure mode = 5b rots.

- **Operator attention cost when failure is finally noticed:** higher than running it now. The candidate accepts this trade ("attention later, with a written contract that bounds it"). The bound is the contract, but the contract has not been written and will be written later by the same operator under the same attention pressure that justified deferring it. This is a structural reason to expect the deferral to fail.
- **Sunk-cost compounding:** every future session's synthesis carries the implicit warranty of an existence-proven exemplar. If the exemplar never exists, every interim synthesis was authored against a hypothetical anchor.
- **Erosion of the "regression discipline" claim:** F2 in challenges.md named this. The candidate addresses F2 by saying 5b will eventually fix it; if 5b rots, F2 is unaddressed *and* the proposal claimed it was being addressed. That is worse than (a)'s honest dirty run.

## 6. Frame-level objection

The candidate's frame is "spread the work across two sessions, with a contract bounding the second session." The operations frame is: **a contract that is authored *by the same operator* who deferred the work, *at the same attention budget* that caused the deferral, *with no forcing function between deferral and authoring*, is not a control — it is a wish.** The proposal has correctly identified that a pre-committed exemplar contract would lift option (a) above its base rate, and has correctly identified that authoring such a contract on this session would consume attention. It has *not* explained why the contract will get authored on a *future* session when it is being deferred from this one.

The reframe: *this is not a "split the work" problem; this is a "what creates the forcing function for the contract to be written" problem.* The candidate provides no forcing function. The proposal should either (i) author the exemplar contract *this session* (collapsing (c') into a heavier (a)), or (ii) attach 5b to a forcing surface that will reliably page the operator. Without one of those, (c') is (a)-deferred-indefinitely with extra paperwork.

## 7. Verdict

`rework` — would change to `approve` if the proposal added a named forcing function for item 5b (a dated trigger, a CI check on the empty exemplars directory, or a hard rule that 5b must be authored before the next session of any kind opens) such that 5b's status becomes observable from outside the punch-list file itself.
