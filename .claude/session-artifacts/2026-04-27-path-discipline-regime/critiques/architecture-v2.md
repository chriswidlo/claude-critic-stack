# Architecture-lens critique — path-discipline regime (loop 2)

## Verdict: approve

## Frame-level objection (advisory; does not block approval)

**The lab itself is becoming the gate-substrate by accident.** Repo now has two substrate-shaped artifacts emerging in parallel: the *runtime* gate-substrate (correctly deferred) and the *lab* deliberation-substrate (currently being instantiated through profound/normal-tier entries). Loop 1 caught the runtime one; loop 2 ships an instance of the lab one without naming it. The architecture question loop 2 should be asking is not "what is the runtime gate-substrate" but **"what is the contract between the workflow and the lab — when does deferring to an upgrade entry constitute deciding, and when does it constitute punting?"**

## Substantive points

- **"No new substrate primitive" — runtime claim holds; deliberation-substrate claim does not.** Runtime: zero hooks, zero scripts, zero settings. Genuinely untouched. Deliberation: opening a `profound`-tier entry titled "Gate-substrate spec" claims a namespace; future gate questions will route into it by name-collision. **Mitigation:** title the entry as a question (`does-this-stack-need-a-gate-substrate/`), not a spec. The word "spec" commits to a deliverable shape.
- **30-day audit is a quiet contract.** Commits to (a) script existing, (b) author-class taxonomy stable at T+30, (c) operator calendar attention, (d) decision rule for audit output. v2 names (a) and (c), not (b) or (d). Honest framing: "smallest contract while preserving optionality" — name it as such.
- **"Do less" is architecturally sound on runtime; under-named on meta.** The asymmetry between the one prose edit v2 makes (reason c) and the four prose edits it could make (relocate clause 2 to the four authoring surfaces, per loop-1 architecture critique) is unjustified. Moving prose between files is no more contract-creating than rewording reason (c). v2 should consider this as a separate, substrate-free prose change.

## What flips approve → reject

If the upgrade entry is named with `-spec` rather than as an open question, OR if v2 fails to consider relocating clause 2's prose to the four authoring surfaces as a separate, substrate-free prose change.
