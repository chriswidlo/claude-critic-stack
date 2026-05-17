# Critic-panel aggregate verdict

## Loop 1

| Lens | Verdict | Critique |
|---|---|---|
| Architecture | **rework** | [critiques/architecture.md](critiques/architecture.md) |
| Operations | **rework** | [critiques/operations.md](critiques/operations.md) |
| Product | **rework** | [critiques/product.md](critiques/product.md) |

3-rework, 0-approve, 0-reject. Routed to step 9 rewrite. Loop 1 closed.

## Loop 2

| Lens | Verdict | Critique |
|---|---|---|
| Architecture | **rework** | [critiques/architecture.v2.md](critiques/architecture.v2.md) |
| Operations | **rework** | [critiques/operations.v2.md](critiques/operations.v2.md) |
| Product | **approve** | [critiques/product.v2.md](critiques/product.v2.md) |

2-rework, 1-approve, 0-reject. Cap of two loops reached per CLAUDE.md step 11; routed to step 12 (synthesis) with disagreements named.

## Disagreements named (carried into synthesis)

### From architecture.v2 (rework)

1. **The synchronization contract is under-specified on the identity dimension, not just the temporal one.** `metrics.json` lacks `session_id`, `end_ts`, and `schema_version` fields — a stale file from a prior run can pass schema validation and be consumed against the wrong session.
2. **`metrics.json` write is not atomic.** `write_text` can produce a partial file on parser crash mid-write; tmp-file + `os.rename` discipline is missing. Per-session `diagnostics/<session-uuid>/` isolation is a structurally cheaper alternative the rewrite did not consider.
3. **The coupling-debt-paydown tripwire is self-report.** "Host-layout drift demands a parser patch" requires the operator to correctly classify a parser commit as layout-driven; under operator pressure, self-report tripwires routinely fail to fire. A mechanical detector (CI check, pre-commit hook flagging touches to `find_transcript`/`find_subagents_dir`) would convert this to a structural signal.
4. **`parser.lock` is presence-only without liveness.** No PID, no timestamp, no `kill -0` check. A crashed parser leaves a stale lock that the consumer cannot age-out.

### From operations.v2 (rework)

5. **Lock-as-presence vs. lock-as-liveness.** Same gap as architecture #4, with operational framing: the operator has no in-band signal that distinguishes "parser running slowly" from "parser crashed." Recovery procedure is undocumented. Fix: `parser.lock` contains `{pid, start_ts}`; ledger-render checks PID-alive and lock-age; emits distinguishable strings (`_parser-running-slow_` vs `_parser-crashed-stale-lock_`).
6. **Phase A → Phase B promotion gate is a vibes check.** "≥5 sessions confirm" without an observable property is not a gate. Observable: `git diff` shows no inline-redirect change between Phase A entry and cutover; staging hook log shows wrapper invocations at the expected count.
7. **Loud-skip is permanent for the session.** No re-render path is named. A crashed parser leaves the ledger artifact lying with `_parser-still-running_` even after a manual fix.
8. **No retention rule for staging/orphan dirs.** Parser-tail cleanup solves forensic-evidence preservation but not steady-state accumulation; orphan dirs from sessions without workflow-id handoff persist indefinitely.
9. **Schema-vs-parser version-skew muddle.** The candidate's named-ways-this-could-be-wrong bullet 1 is logically self-contradictory. Synthesis must name which side wins (operations recommends: parser writes per its native shape; consumers decide whether to silent-skip — producer-side schema check that rejects the parser's own output is a bootstrap failure).

### From product.v2 (approve, with two patch suggestions)

10. **Stub-string threshold leak.** "populates after 3 sessions" exposes an internal mechanism to operator surface. Threshold-agnostic wording (`populates as data accumulates`) is preferred.
11. **Deferred-items review cadence is unspecified.** Ten armed tripwires with no scheduled review is a hidden backlog. Specify either a per-session check or a cadence tied to upgrade-entry lifecycle ("entry is not closed until deferred table is walked once").

## Net read

The rewrite materially improved on v1 — three frame-level objections from loop 1 are addressed, the candidate is shorter and more decisive, and product flipped from rework to approve. Two structural lenses still dissent. The architecture and operations objections converge on a single under-specified primitive: `parser.lock` is sequencing without liveness, and `metrics.json` is published without identity (session-id, schema-version, atomic publish). Both lenses propose the same fix shape — a richer lock and a stamped, atomically-published metrics file — at ~10 lines of code total.

This is a *cap-stop synthesis*, not an approval. The candidate cannot ship in its current form without the architecture-and-operations gaps named above being either patched or explicitly accepted-with-named-risk. The product approval is conditional on the synthesis carrying its two patch suggestions forward as named uncertainties.

Routing: **step 12 (synthesis)** with the eleven numbered disagreements above as the named-uncertainty section.
