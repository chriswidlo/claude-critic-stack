# Critic-panel verdicts

## Loop 1 — vetoed

| Lens | Verdict | Frame-level objection (one-line) |
|---|---|---|
| Architecture | **rework** | Candidate ships a *gate-substrate by accident*; first hook becomes the template for every future gate. |
| Operations | **rework** | Change-management problem against a self-modifying authoring loop, not a compliance problem. No canary, no telemetry, no kill-switch. |
| Product | **rework** | The hook is a *contract change*, not infrastructure. Two asymmetric users, no rejection-message UX. |

**Convergent frame objection:** the candidate solves the wrong problem at the wrong level. Substrate / change-management / contract — three lenses, same shape. **Replan triggered.**

## Loop 2 — approved (with advisory concerns)

| Lens | Verdict | Advisory frame note |
|---|---|---|
| Architecture | **approve** | The lab is becoming the *deliberation-substrate by accident*. Two profound/normal entries opened in the same loop where the conclusion is "do less." Watch for lab-as-pressure-relief-valve. |
| Operations | **approve** | The 30-day audit is a scheduled task with no scheduler. Same shape as loop 1's substrate gap, smaller scale. Decisional drift, not operational drift — outside this lens's remit. |
| Product | **approve** | Operator-position statement is partial retirement (70%) + partial externalisation (30%). "Nothing changes on ship day" is a probabilistic win contingent on the audit firing. |

## What v2 ships

- One prose edit at [`CLAUDE.md`](CLAUDE.md):16 (factual correction of reason (c)).
- T+30 audit commitment (operator action, no scheduler).
- Two new upgrade entries naming the substrate question and the workflow-overrun finding.
- Required operator-position statement.

## Residual advisory items not blocking the approve

1. Title the gate-substrate entry as a *question* (`does-this-stack-need-a-gate-substrate/`), not a *spec*.
2. Consider relocating clause 2's prose from CLAUDE.md to the four authoring surfaces as a separate substrate-free prose move (architecture lens, loop 1 + loop 2).
3. Anchor the T+30 audit by writing the date into [`decision-log.md`](decision-log.md) so the next workflow scan finds it.
4. Make the operator-position statement load-bearing: the workflow respects "ship more" or "ship less" responses, doesn't default to silence.

These are recommendations to incorporate into the synthesis, not new critiques.
