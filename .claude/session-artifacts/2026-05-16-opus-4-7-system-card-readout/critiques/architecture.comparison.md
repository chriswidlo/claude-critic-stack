# Comparison — architecture lens (v2, loop-2)

| field | opus lane | sonnet shadow lane |
|---|---|---|
| verdict | approve | approve |
| weakest-link | "Things you must not do" in CLAUDE.md is becoming a heterogeneous dumping ground (invariants + workflow gates + session-specific fail-safes like R5) with no sub-structure distinguishing invariant from interim-fail-safe-with-retirement-condition; foreseeable refactor, not a current defect. | F2 fail-safe defines "safety-flavored session" as prose applied at orchestrator judgment, not as a deterministic gate; the requirement-classifier has no "safety-flavored" label, so the fail-safe fires on unstructured discretion — same structural gap as v1's mis-layered hand-off, one level up. |
| frame-objection | R5 fail-safe is itself a vendor-anchored decision (honestly surfaced in "Named ways this could be wrong"); R1's placement in `upgrades/profound/` remains a direction-of-coupling concern carried over from v1, now mitigated by explicit re-entry trigger and companion-change pairing — not frame-level at v2. | If requirement-classifier is extended with a "safety-flavored" label and the F2 fail-safe references that classifier output rather than prose, the structural gap closes (named as improvement, not precondition). |

## Agreement class

`agree`

## One-line gloss

Both lanes verify all v1 flip-conditions landed at the correct architectural layers and approve; both also carry forward residual concerns about R5 / F2's coupling, but neither concern is frame-level or blocking.

## Triangulation signal for synthesis

- Shadow concurs across the v1 flip-condition verifications (R2/R3 asymmetric direction, F6/F7 stubs landed, F2 hand-off re-layered at comparator-enum, `subagent-distiller` "still works" gone). High-confidence approve.
- SHADOW_PANEL value case: the shadow lane caught a residual the Opus lane did not — the "safety-flavored" trigger is a prose definition resolved at orchestrator discretion, with no classifier-output backing. Opus lane named a related but distinct residual (heterogeneous "Things you must not do" section needing sub-structure). Two non-overlapping residuals, both worth carrying into a future session, neither flips the v2 verdict.
