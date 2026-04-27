# Frame — item 7 (residual AGENTS.md references)

## Revision 1

### How the user framed it
*"Live docs no longer name `AGENTS.md`. Catalyst sections describing the past can stay; action prose needs to be revised. Session artifacts are immutable historical record."*

The user is implicitly optimizing for **textual hygiene under an immutability constraint** — get rid of the misleading file-name in places that prescribe, leave it alone in places that narrate.

### Reframe (orchestrator's restatement)

The user's frame treats this as *string-removal with a tasteful exception list*. The more useful frame is **"what is each occurrence of `AGENTS.md` doing for the reader, and does that job still need to be done?"**

The string `AGENTS.md` is doing one of four jobs in the corpus:

1. **Naming a live convention** (CLAUDE.md path-discipline list, .gitignore allowlist) — *this job is broken*, because the convention has no referent. The string is a lie of omission.
2. **Naming a future commitment** (upgrade-entry "🚀 upgrade" columns claiming `AGENTS.md drift becomes detectable/traceable`) — *this job is broken*, because the commitment refers to a co-equal partner doc that no longer exists. The benefit is half-claimed.
3. **Naming a module composition** (`constitutional-layer-goals-modules`:42 — listing AGENTS.md as part of the "orchestration" module) — *this job is broken*, because a module composed of `{CLAUDE.md, AGENTS.md, ...}` is not the current shape. This is closer to a structural error than a textual one.
4. **Naming a past investigation finding** (`workflow-blind-to-the-lab` catalyst and body — *"CLAUDE.md and AGENTS.md contain zero references to upgrades/"*) — *this job still works*, because it describes a state of the world at the time of investigation. Past tense, immutable.

Reframed in one sentence: **this is not "scrub a deleted filename"; it is "audit four jobs the filename was doing, kill the three that have no referent, preserve the one that documents history."**

### What the user is implicitly optimizing for
**Minimum-disruption hygiene** — touch the smallest number of lines that prevent a future reader from acting on stale prescriptions; leave everything else.

### Alternative optimization (the reframe surfaces)
**Prescription integrity** — every column heading, module-composition list, and live convention list in the repo should refer only to artifacts that exist. The fact that several upgrade entries claim *"X drift becomes detectable"* about a non-existent X means the entries' value claims are partially false. Fixing the string fixes the claim.

These two optimizations agree on the live-convention edits (CLAUDE.md, .gitignore) and the catalyst preservation. They diverge on the upgrade-entry "🚀 upgrade" columns: under "minimum-disruption hygiene," you swap `AGENTS.md` for nothing or for ellipsis; under "prescription integrity," you have to ask whether the *benefit* still holds without AGENTS.md as a partner, and rewrite the cell to be honest about what's now true.

### Implicit-optimization tradeoff
- Min-disruption is faster and lower-blast-radius, but ships a half-honest cell that future readers may still trip on (the cell now reads *"CLAUDE.md drift becomes detectable"* — true, but the *original argument* was about parity between CLAUDE.md and AGENTS.md; that argument silently dies in the edit).
- Prescription-integrity is slower (requires rereading each upgrade entry's argument and judging whether it survives the deletion of one of its premises), but the result is honest.

### Frame I am NOT adopting
"Restore AGENTS.md" — out of scope. The deletion happened; this item is about reconciling the corpus with that fact, not relitigating it.

### Question the workflow is being asked to evaluate
**Should item 7's resolution operate at level (1) — string-scrub of broken references — or at level (2) — argument-level reread of the three upgrade entries to verify their claims still hold without the deleted partner doc?**

The classifier said `refactor` with a known bias toward calling a scope-shrink a refactor. The reframe sharpens that bias: if the upgrade entries' arguments rest on *parity* between two docs and one is gone, then "edit out the dead string" is precisely the kind of silent scope-shrink the classifier warned about.
