# Critic-panel verdicts — item 11 candidate v1

| Lens | Verdict | Frame-level objection (one-line) | Lift to approve |
|---|---|---|---|
| architecture | rework | Commit 92d9387 is the *second* drift on the two-file denormalization; in architecture, second occurrence is the signal. The candidate inscribes the split rather than reopening it. | (a) move the truth-about-retrieval to [`canon-librarian.md`](../../../.claude/agents/canon-librarian.md) (the mechanism), not the punch-list; OR (b) explicitly open a follow-on item for fold into one file with `fetchable:` field, naming 92d9387 as the second-drift trigger. |
| operations | rework | The lift condition ("a second on-disk misread elsewhere") is unobservable without a recurring audit; deferring on it is deferring forever. | (a) add a checkable detection recipe (grep recipe in canon/README.md or canon-refresher audit step); OR (b) replacement prose schema-agnostic to file count ("YAML files in canon/ are catalogs, not retrieval indexes"). |
| product | rework | Lift condition triggers only after a misread is committed (after the harm). The README is the durable surface; the punch-list is ephemeral. Fixing only the ephemeral one inverts the lifecycle. | drop the "ask one question first" experiment (it re-asks the user's own done-when), AND land the fix at a durable surface — one-line correction at [`canon/README.md`](../../../canon/README.md):3 OR a "Retrieval:" line in [`canon-librarian.md`](../../../.claude/agents/canon-librarian.md). |

## Convergent signal

All three lenses, independently, want the fix to land at a **durable surface** (the agent prompt and/or canon/README.md), not only at the punch-list. Operations adds: phrase the truth in a way that survives a future fold into one YAML. Architecture adds: name the architectural follow-on so commit 92d9387 is captured as evidence, not closed as a one-off.

## Minority-veto status (loop 1)

Three lenses, three `rework`. No `approve`. Mandatory routing to step 11.

## Loop 2 — re-review of [candidate-v2.md](candidate-v2.md)

| Lens | Verdict (v2) | One-sentence rationale |
|---|---|---|
| architecture | approve | Both lift conditions met: edit #1 moves truth to `canon-librarian.md`, edit #4 opens fold follow-on naming 92d9387 as second-drift trigger. |
| operations | approve | Schema-agnostic phrasing at edit #1; pre-commit grep recipe satisfies the detection-check requirement. |
| product | approve | Round-trip experiment dropped; fix lands at two durable surfaces before the ephemeral one. |

**Minority-veto cleared.** Three approves, no veto. Proceeding to step 12.
