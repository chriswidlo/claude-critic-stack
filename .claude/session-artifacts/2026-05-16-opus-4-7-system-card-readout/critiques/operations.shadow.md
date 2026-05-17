# Operations shadow critique — Opus 4.7 system-card readout change-set (v2)

Lane: Sonnet shadow (`critic-operations-shadow`). Voice, not vote. Loop 2 of 2.

## Verification of flip-conditions before re-verdict

**Flip-condition (a) — F2 interim fail-safe.** Verified landed. [CLAUDE.md](CLAUDE.md) "Things you must not do" terminal bullet: halts synthesis when any Opus lens returns `unavailable` on a safety-flavored session, requires explicit operator override, names the retirement trigger (comparator schema gains `refused` value distinct from `unavailable`).

**Flip-condition (b) — concrete adoption gate for R2/R3.** Verified landed. R2 in [.claude/agents/outside-view.md](.claude/agents/outside-view.md) "Recognized anchor risks" with co-falsifier; R3 in [CLAUDE.md](CLAUDE.md) MUSTNOT with explicit pass-through ("if `outside-view` does not flag the anchor, the orchestrator must catch it at synthesis"). R1 routes to [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/README.md) with a named trigger condition, not open-ended deferral.

## 1. Most likely incident

Safety-flavored session runs; Opus lens returns `unavailable`; F2 fail-safe fires and halts synthesis correctly. Operator, facing explicit override prompt, is uncertain how to proceed: rule says "requires explicit operator override" but does not specify what constitutes valid override or where it must be recorded. Operator either proceeds silently (defeating audit trail) or stalls session unnecessarily. Root cause: the halt is enforced; the override ceremony is undefined.

## 2. Blast radius

Narrow and contained relative to v1. Primary v1 risk — silent synthesis proceeding on two approves plus one `unavailable` — is closed. Residual: any safety-flavored session with `unavailable` Opus lens hits undefined recovery. Failure mode is operator friction and audit gap, not undetected synthesis bypass. Fully recoverable retroactively if override-ceremony gap is later specified.

## 3. Rollout / rollback

R2 + R3 + F2 fail-safe rollback: single `git revert` of three small additions across two files. No data migration. R1 at `created` stage — nothing to rollback. Trigger condition is the stack's documented cadence model, not indefinite deferral. Materially improved over v1.

## 4. Observability gap

Primary gap from v1 addressed: `unavailable` is now actionable (halt) rather than silently consumed. Two residual gaps:

1. **Override is unobserved.** When an operator overrides the fail-safe, no artifact records the decision. `decision-log.md` schema does not include an override field.
2. **Inter-lens refusal correlation unmeasured.** Acknowledged explicitly. Session-level refusal probability band remains estimated (40–60%) rather than measured.

## 5. Cost at failure

- True `unavailable` (timeout/error): fail-safe fires, halts synthesis. Cost = stalled session + operator time. Recoverable.
- Refused verdict: indistinguishable from `unavailable`; fail-safe fires. Same cost. Recoverable.
- Override without ceremony: no session cost, but unrecoverable audit gap.

v1 primary cost driver — "two approves plus one `unavailable` parsed as no-veto, synthesis proceeds" — is closed.

## 6. Frame-level objection

The override mechanism is specified at the rule layer but not at the workflow layer. CLAUDE.md names "explicit operator override" as the gate-pass but does not define what *explicit* means: a session comment, a `decision-log.md` field, a re-invocation flag. The step-9 HARD GATE is enforceable mechanically; the F2 override gate is not — it depends on operator interpretation, softer than the hard-gate pattern. For safety-flavored sessions, this asymmetry is load-bearing.

The fix is small (one line specifying that override must appear as a named entry in `decision-log.md`) and does not require a v3.

## 7. Verdict

`approve`. Both flip-conditions verified landed and operational. Residual concerns (override-ceremony ambiguity, unmeasured inter-lens correlation) are named, bounded, and do not reopen the v1 primary failure mode. Flip to `rework` if a future session shows a `decision-log.md` where an operator override is not recorded but synthesis proceeded on a safety-flavored candidate with `unavailable` Opus lens.
