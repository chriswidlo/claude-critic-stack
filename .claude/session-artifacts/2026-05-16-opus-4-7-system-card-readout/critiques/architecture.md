# Critic — Architecture lens (v2, loop-2 re-review)

## Verification against v1 flip-conditions

**(a) Decouple R2/R3 with separate falsifiers.** Satisfied. R3 in [CLAUDE.md](CLAUDE.md) is now stated as the *invariant* with explicit asymmetric direction language: *"if `outside-view` does not flag the anchor, the orchestrator must catch it at synthesis."* R2 in [.claude/agents/outside-view.md](.claude/agents/outside-view.md) is the detection arm. Falsifiers in repo-changeset.md sections R2 and R3 are now distinct: R3 can stand without R2 (degraded but coherent); R2 cannot stand without R3. The parent-child layering is correct.

**(b) Re-layer F2 hand-off at the comparator enum.** Satisfied. The F2 interim fail-safe bullet in [CLAUDE.md](CLAUDE.md) operates on `unavailable` from any Opus lens and names its retirement condition at the comparator-schema layer: *"This rule retires when the comparator schema gains a `refused` value distinct from `unavailable`."* The companion schema split is tracked in [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/). The hand-off is correctly at the comparator-enum layer, not at the lens layer.

**(c) Per-primitive expiration / re-trigger conditions on no-change rows.** Satisfied. The no-change table in repo-changeset.md (Per-agent / per-rule decisions → "Reviewed: explicit no-change" subsection) now has a last-column re-trigger condition for each row. Two rows correctly mark `n/a — rule is invariant` (path-discipline, hard gate) — that is the correct disposition for true invariants, not a gap.

## Residual frame-level concerns (noted, not blocking)

- The R5 fail-safe is itself a vendor-anchored decision (named in "Named ways this could be wrong"), but the change-set surfaces this honestly.
- R1's placement in `upgrades/profound/` remains a direction-of-coupling concern from v1, but is now mitigated by the explicit re-entry trigger and the companion-change pairing with the comparator schema split. Not a frame-level objection at v2.

## Single most important unresolved item

The CLAUDE.md "Things you must not do" section is becoming a dumping ground for heterogeneous rules: invariants (path discipline), workflow gates (hard gate on scope-map/challenges), and session-specific fail-safes (R5). R5 is correctly placed *now* — but the section lacks a sub-structure that distinguishes "invariant" from "interim fail-safe with named retirement condition." Foreseeable refactor, not a current defect. Out of scope for this loop.

## Verdict

**approve.** All three v1 flip-conditions are satisfied at the correct architectural layers; what would change the verdict is evidence that the asymmetric R2/R3 coupling does not actually hold under operator use (e.g., a session where R3 fires without R2 ever having flagged), which is by construction a post-deployment observation.
