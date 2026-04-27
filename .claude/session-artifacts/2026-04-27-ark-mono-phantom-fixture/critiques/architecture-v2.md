# Architecture-lens critique v2 — ark-mono phantom fixture (loop 2)

## 1. Weakest structural link

**The mtime-gated review is a forcing function only if something *reads* mtime.** v2 promotes "if `CLAUDE.md` mtime is newer than `EXEMPLAR-CONTRACT.md` mtime, a review is owed" to load-bearing status. But no module in this repo reads file mtime. There is no pre-commit hook, no CI grep, no agent rule, no `bin/` script. The mechanism is an instruction to the operator's future self, encoded in metadata that nothing inspects. Architecturally this is the same shape as the original phantom fixture: a claim of discipline whose backing module does not exist.

A second worry: the "owner module" answer is `tests/regression/EXEMPLAR-CONTRACT.md`. That places the contract for `.claude/session-artifacts/exemplars/` *outside* the directory it governs. The exemplars directory's `.keep` still has no link to its own contract. The "home module" exists but is not co-located with the artifact whose lifecycle it defines.

## 2. Invariants at risk (not those v2 already names)

1. **A forcing function is a mechanism, not a documented intention.** v2 rests on mtime comparison performed by the operator's eye.
2. **Contracts live with the directory they govern.** v2's contract lives at `tests/regression/EXEMPLAR-CONTRACT.md` but governs promotion semantics into `.claude/session-artifacts/exemplars/`. Two directories remain split (loop 1 alternative 3 was rejected without engagement).
3. **The "real slugs only" rule is enforced by reading.** No grep, no linter, no agent-side check.

## 3. Coupling and direction

- **Loop-1 cycle: cut, partially.** v2 does the spec-currency audit *in this session*. Good.
- **New cycle introduced via mtime.** Each amendment of `CLAUDE.md` re-triggers the mtime gate; discipline becomes proportional to doc churn, not actual regression risk.
- **Volatile→stable direction: still violated, more honestly.** Recorded in the contract; that is accounting, not architectural correction.
- **Layering between docs and tests: cut cleanly.** Step 2's substitution + step 3's rule resolve loop 1's layering complaint. Strongest part of v2.

## 4. Ignored architectural alternatives

1. **Single `.claude/exemplars/` directory** (loop 1 alternative 3) — not engaged.
2. **The contract as agent prompt, not document.** Embed promotion-semantics into a `regression-promoter` agent prompt; closes §1 weakest-link concern about mechanism vs. intention.
3. **Bind the mtime gate to git, not the filesystem.** Add a `CLAUDE.md`-changed-since-last-review check to the `requirement-classifier` prompt; one rule in one prompt.

## 5. Frame-level objection

The loop-1 frame-level objection still stands, narrowed: **the regression-discipline subsystem still does not cohere as an architectural unit; v2 has authored a contract document for a subsystem that has no execution surface.** The contract names promotion semantics, wrong-spec-vs-wrong-agent rules, max-edits, and a maintenance schedule — but no module performs promotion, no module evaluates wrong-spec-vs-wrong-agent, no module counts edits, no module checks the maintenance schedule. The contract is a specification of how a subsystem *would* operate if a subsystem existed. v1's phantom was an empty exemplars directory and a fabricated slug. v2's phantom is a contract document describing operations that nothing performs. The phantom has moved up one level of abstraction — from data to protocol — but its structural status is preserved.

## 6. Verdict

**rework**

What would change the verdict: replace the mtime convention with a mechanism that some module actually reads (the `requirement-classifier` checks `CLAUDE.md` git-history against a recorded last-review marker; or a `bin/` script invoked from the workflow; or an agent that owns regression-discipline review), AND co-locate the contract with the directory it governs.
