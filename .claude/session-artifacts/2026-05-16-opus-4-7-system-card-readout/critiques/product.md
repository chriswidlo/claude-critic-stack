# Critic — Product lens (v2, loop-2 re-review)

## Opening dissent

The v2 change-set closes the gap I named in v1. The operator running the next 12-step session on a safety-flavored candidate now hits a *visible* surface: the synthesis template's "Named failure modes flagged" bullet renders R2's detection, the "refusal as triangulation signal" sub-bullet renders F2's blast radius, and the F2 interim fail-safe in [CLAUDE.md](CLAUDE.md) halts synthesis rather than silently producing a degraded artifact. That is the load-bearing flip from v1: invisible-flavor-text became operator-blocking-gate.

The remaining product friction is real but lens-non-fatal: the synthesis template addition is *render-on-trigger*, not *render-always*, so quiet sessions still produce no audit trail that the new bullets fired correctly. That is a measurement debt, not a contract defect, and it is fairly named in Assumption E.

## 1. User-visible consequence

Three new surfaces the day this lands:
- Synthesis output gains a "Named failure modes flagged" bullet ([CLAUDE.md](CLAUDE.md) step 12) enumerating outside-view / canon / critic anchor flags.
- A "refusal as triangulation signal" sub-bullet appears under Triangulation when any Opus lens returns no verdict.
- Synthesis halts with explicit operator-override requirement when the safety-flavored + `unavailable` combination triggers the R5 fail-safe.

Discoverability: future operators grepping `canon-librarian.md` for "F6" / "F7" / the session-id now hit the HTML-comment stubs. Functionally a tiny `CHANGELOG` entry per agent.

## 2. Commitments implied

- Synthesis template now commits to a *required* bullet that says "none flagged" in the empty case. If the trigger logic is buggy, "none flagged" lies confidently. Durable risk.
- F2 fail-safe commits to halting safety-flavored sessions on `unavailable`. Operators will route around the halt under deadline pressure unless the override workflow is cheap; that override design is implicit, not specified.
- Declined-finding stubs commit to HTML-comment-as-changelog as a stack convention.

## 3. Migration burden

- **Next safety-flavored session operator.** Burden reduced from "invent surfacing under pressure" to "decide whether to override the halt." Correct burden to impose.
- **Future authors of `upgrades/profound/` entries.** R1's entry has an explicit re-entry trigger — a tripwire, not a date.
- **Operator looking for "what did we do for 4.7?"** No central `CHANGELOG`-equivalent, but grep on the session id hits five surfaces. Acceptable density.

## 4. Affordances better / worse

**Better:**
- Synthesis output now teaches the operator that "anchor risks" and "refusal as signal" are first-class concerns.
- F2 default + fail-safe is coherent: "we accept the cost, and refuse to silently absorb it on safety work."
- Declined findings grep-discoverable.

**Worse:**
- "None flagged" empty-case is a false-negative attractor.
- Fail-safe's override path is undefined.

## 5. Frame-level objection

v2 partially adopts the v1 frame ("translate findings into a disclosure surface"), but stops short of producing a *standalone* disclosure surface (a `MODEL-NOTES.md` keyed to the model version powering the stack). Disperses 4.7-specific disclosure across CLAUDE.md, two agent files, an upgrades entry, and a session-artifact directory. Correct for *enforcement*, wrong for *legibility*. R1's R&D entry is the natural home; the gap should be added there rather than blocking v2.

## 6. Verdict

**approve.**

Verdict would change to `rework` if the synthesis-template amendment's trigger logic has no implementation path the orchestrator can actually evaluate at step 12 — making the bullet render-as-flavor regardless. Trigger is implementable given artifacts on disk; verdict stands.
