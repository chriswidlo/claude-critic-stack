# Frame — format-only state-transition gate

## Revision 1

### The user's implicit framing
"Design a gate that prevents drift in lab entries as the AI handles state transitions." The user has already pre-decided two design axes (script vs agent; hook vs slash command) and given a hard scope constraint (format-only, no idea evaluation). The frame the user is operating in is **enforcement-mechanism design**: pick the right enforcement primitive.

### What the user is implicitly optimizing for
- **Format consistency across entries** as the lab grows from 22 to 100+ entries.
- **Mechanical detectability of false advancement** (e.g., `🔨 implemented` claimed without a commit reference).
- **Stability of the lab's lifecycle convention** under heterogeneous AI authorship — multiple sessions, multiple agents, all advancing entries against the same schema.

### Alternative framing — the orchestrator's restatement
The user named this as "build a gate." A different shape of the same problem is: **define the schema, and the gate is whatever cheaply enforces it**. Under this framing, the load-bearing artifact is the per-transition required-element schema (a single source of truth — probably a markdown table in the README or a small YAML file). The gate is a thin script that reads the schema and the entry and says yes/no. The slash-command/hook choice becomes a deployment detail, not a design decision.

A second alternative: **the failure mode is concentrated, not uniform**. The classifier asked whether all seven transitions need gating equally. The honest answer is probably no — the high-risk transitions are `🔨 implemented` (claim of work done) and `💎 value-proved` (claim of demonstrated value). The other five are either trivial (`🌱 → 🔬` is just a date+note) or operator-gated by their nature (`📋 → ✅` is the operator saying yes). Under this framing, a *targeted* gate on two transitions is the right shape; gating all seven is over-engineering.

### What this alternative optimizes for
- **Schema-first** is optimizing for a single source of truth and minimal coupling between gate and lifecycle. The gate becomes replaceable; the schema doesn't.
- **Targeted gating** is optimizing against the workflow-overdesigns failure mode the operator already flagged. Two transitions × required elements is much smaller surface than seven transitions × required elements, and the smaller surface lands faster and gets validated against real entries faster.

### Hard constraint inherited from the user
**Format-only.** If the candidate generated at Step 9 includes anything that evaluates idea quality, context, or judgment, the candidate fails its own scope check. The critic-panel must be told this explicitly so the panel doesn't rebuild the gate as a quality reviewer.

### Frame bias to watch for
- The classifier's `new` label biases toward designing a full novel system when the right answer might be "extend the existing `/upgrade` slash command with an `/upgrade advance` subcommand."
- The lab's own existence biases toward "make the lab more rigorous." But the lab is currently 22 entries old. Validating the gate against real drift requires actual drift to exist — and there is none yet.

## Revision history
- Revision 1 (2026-04-26): initial frame, written before parallel-gather. Two alternatives surfaced: schema-first (vs gate-first) and targeted gating (vs uniform gating).
- Revision 2 (2026-04-26, post loop 1 replan): restore user's frame. Discard challenger-derived audit-first reframe.

## Revision 2

### What loop 1 revealed
The candidate adopted the challenger's audit-first reframe wholesale. Product critic rejected: the operator asked for a gate, not for a measurement of whether a gate is needed. Architecture and operations critics added supporting frame-level objections (audit and gate should not share a schema; observation window without instrument is not measurement). The loop-1 candidate was internally coherent and externally non-responsive.

### Restored frame
**Design a gate the operator can use on day 1**, format-only, that does not require flipping any existing contract in the lab. The gate is a *non-blocking warning surface* on the existing manual-edit flow, not a replacement for it. The audit-first phasing is collapsed: the gate IS the audit, run once per advancement, by the operator or the AI agent advancing the entry.

### Concrete reframed shape (for the generator)
- Single command: an extension to `/upgrade` (sub-command, not new sibling). When invoked with an existing entry path and a new state, runs the format check.
- **Warns, does not block.** The check produces a one-screen report: *"this entry is missing the following sections required for state X: ..."*. The operator (or AI) reads it and decides whether to proceed. The state-table edit happens by hand (preserves the README's "manual act" contract) or is offered as a single follow-up after the warning is acknowledged.
- **Schema lives where the lifecycle lives.** Per the architecture critic's "invert dependency" objection: the schema is derived from `upgrades/README.md`'s lifecycle-table by the script, not duplicated in grep patterns. If the README is updated, the script's checks update next run.
- **No new artifact (no AUDIT-LOG.md).** Per the operations critic's "no measurement instrument" objection: the warning report at the moment of advancement IS the instrument. The operator sees it in flight, not as a separate periodic ritual that requires invocation memory.
- **Hand-labeled ground truth deferred until evidence.** The operations critic's "label 22 entries first" requirement applies if and only if we are claiming a false-positive rate. A warning-only gate makes no claim of accuracy — the operator reads the warning and judges. False positives become friction, not corruption.

### What this frame deliberately keeps small
- One command, one path through the code (existing `/upgrade`).
- Zero new files for the operator to remember (no `AUDIT-LOG.md`, no `bin/check-upgrade-transition.sh` separate from the slash command's implementation).
- Zero changes to README contract (manual edit still allowed; warning is advisory).
- Zero changes to existing 22 entries.
- Zero hypothesis about whether the gate is "needed" — the operator asked for it; we ship it; if it earns its keep, it stays; if it gets ignored, it dies the way audited-out tools die.

### What this frame is NOT
- Not the audit-first phasing of Revision 1's loop-1 candidate.
- Not a pre-commit hook (outside-view: high-bypass surface for solo repos).
- Not a slash-command-only-write-path (product critic: removes lab's smallest-ceremony advancement; conflicts with README's "manual act" sentence).
- Not a "later we will build a real gate" Phase 2 deferral. The day-1 thing IS the gate.

### Frame bias to watch in v2
- Risk that "warning-only" softens the gate to the point of being theatre. Mitigation: the warning must name *exactly* which sections are missing, with line-suggestions; vague warnings get ignored.
- Risk that derived-from-README schema doesn't actually work because the README is prose, not a parseable table. Mitigation: the README's state-lifecycle section is already a markdown table; the script reads its rows. If the table changes shape, the script breaks loudly (good) rather than silently (bad).
