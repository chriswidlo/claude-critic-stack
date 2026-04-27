# Critic — Operations lens — item 06 temporary-dependent upgrades

## 1. Most likely incident

At time T (~2026-Q3, 60–120 days after merge), an operator or agent reading [`upgrades/LEDGER.md`](../../../../upgrades/LEDGER.md) row #18b clicks through to the entry's `Update history` block and follows the pointer to `agentic-engineering-research`@13c09b0; the ref does not resolve. Root cause: (b′)'s correctness depends on a git ref hosted on a branch the candidate explicitly excluded from this session's scope, with no enforcement that the ref remain reachable and no monitor that fires when it doesn't.

## 2. Blast radius

- Two entry bodies + one LEDGER row + transitively every reader (human or agent) that ranks/consults the LEDGER. `canon-librarian` is named in the scope-map as a LEDGER reader.
- Doc artifact only. Downstream cross-references (sister entry, plan docs) need their own back-references audited if `Update history` is the canonical version-of-truth.

## 3. Rollout / rollback

- **Safe rollout:** trivial — content-only change.
- **Rollback path:** mechanically possible via `git revert`, semantically wrong because the original phantom migration plan text is now known-false. Honest rollback would be a forward-fix to a different shape (e.g., graduation-eviction).
- **Two-systems-running period:** doc-sense, "as long as both `main` and `agentic-engineering-research` coexist." Assumption #3 names this without bounding it or naming a review cadence.

## 4. Observability gap (lens's strongest objection)

- **Discoverability of the `Update history` block.** No index, no LEDGER-level marker beyond the rewritten cell, and no convention since item 18f is itself at `🌱`.
- **Branch-reachability monitoring.** No CI or pre-commit check verifies refs cited in entry bodies remain reachable. The pointer is invisible-when-broken.
- **`superseded`-section-in-otherwise-live-entry detection.** State-table cell still reads `🌱`; tooling that reads structured state sees a live entry. Demotion is invisible to anything that reads structured state — only to a human reading prose.
- No metric the operator can check at 90 days to confirm "(b′) is working as intended."

## 5. Cost at failure

- **Pointer rot:** `Update history` blocks become footnotes pointing at nothing. Operator load: re-audit, decide what the pointer should now say (likely full supersede or eviction), edit again. **Same workflow re-run.**
- **Recurrence:** if a future research session produces another out-of-`main`-dependency entry, the operator runs the full 12-step workflow again per entry. Outside-view's threshold (≥5 in 6 months, or a third instance) is not adopted. No written trigger that promotes (b′)-per-instance to (d)-as-rule.
- **Convention drift:** if 18f is abandoned, (b′)'s discoverability mechanism is a one-off pattern.
- **Maintenance coupling:** small in solo repo, but scales with every future `Update history` retro-application.

## 6. Frame-level objection

The candidate frames this as a *content-fidelity* problem. The operations frame is that this is a **freshness-and-reachability problem**: cross-artifact pointer chain (LEDGER row → entry body `Update history` → branch ref → directory) where every link can rot independently with no monitor on any of them. Half-life of the truth is unbounded.

**Eviction is the only option that has zero ongoing reachability dependency.** (a) creates two-copies-running, (b′)/(c) create branch-pointer dependencies, (d) creates a rule-maintenance dependency. Eviction is the only post-state invariant under future branch operations. The candidate's reflective-narrative argument is fine for the architecture lens but does not engage the operational property that eviction uniquely has.

## 7. Verdict

`rework`

Path to approve: add (i) a named, dated review trigger for the `agentic-engineering-research`@13c09b0 pointer (calendar item, routine, or "if branch deleted, do X"), and (ii) one observable signal that lets a future reader/agent detect a `superseded`-section inside a `🌱` entry without reading prose.
