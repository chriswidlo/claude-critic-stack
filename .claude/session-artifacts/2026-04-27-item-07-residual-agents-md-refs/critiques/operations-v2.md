# Operations critique v2 — item 7 (tombstone alternative)

## 1. Most likely incident

At time T (3-9 months out), a contributor opens `AGENTS.md` to "leave a quick note" and appends a paragraph to the tombstone. Root cause: a one-line tombstone has no machine-enforced invariant against accretion, and v2 ships no CI check, no header marker tooling could assert on, and no documented review rule for changes to this file — so the tombstone slowly drifts into a half-populated AGENTS.md that misrepresents the repo's actual agent surface.

## 2. Blast radius

- **Anyone landing on `AGENTS.md`** via the eight existing references reads whatever the file currently contains.
- **Cannot estimate** how many downstream agent-invocation paths read `AGENTS.md` *content* as input. v2's plan does not enumerate readers of the file's contents — only readers of the file's existence. **That gap is itself an observability problem.**

## 3. Rollout / rollback

- **Rollout.** Single commit, additive (one new file, one punch-list line). Appropriate.
- **Rollback.** `git rm AGENTS.md` plus revert the punch-list `✅` line. The eight pre-existing references then re-break to their pre-v2 state — i.e., rollback returns the repo to *the broken state item 7 was filed to fix*, not to a clean baseline. **The plan does not name this consequence.** Owes one sentence.

## 4. Observability gap

Loop-1's two operations objections (silent-scope-shrink, grep-only verification inverted) are **moot** under v2. v2 makes zero body edits.

But v2 introduces a different gap:

- **Tombstone-rot is invisible.** The "this is a tombstone" status is encoded only in prose inside the file body. Nothing machine-readable asserts content matches the intended shape. Drift from "tombstone" to "tombstone plus a TODO" does not page anything.
- **No marker for tooling.** A header like `<!-- TOMBSTONE: do not extend; replace wholesale or leave alone -->` would let a one-line CI grep enforce the invariant. v2's heading `# AGENTS.md (tombstone)` is human-readable but not anchored as a machine contract.
- **Verification proposal is sufficient for the precondition, insufficient as ongoing control.** The grep confirms eight references resolve at commit time. Provides no ongoing signal.

## 5. Cost at failure

- **v1 silent failure**: future agent cites a deflated benefit cell as evidence that drift detection is installed → wrong downstream decision. Hard to detect, self-concealing.
- **v2 silent failure**: contributor appends to tombstone → file misrepresents repo's agent surface. Cost is **visible the moment anyone opens the file** — heading still says `(tombstone)`, accreted content is visibly anomalous.

v2's failure is **materially less costly** than v1's. **But** v2 carries one cost v1 did not: a permanent low-grade attractor. A one-line file at repo root with a familiar name is exactly the sort of file that gets edited absentmindedly. Cumulative probability of accretion non-trivial over multi-year horizon.

## 6. Frame-level objection

v2 frames the tombstone as a *static artifact*. The operational frame is that **a tombstone is not an artifact, it is a control with an enforcement gap**. Every other immutability discipline in this repo has either a documented rule or a structural enforcement. The tombstone has neither — its "do not extend" property is encoded in a single prose sentence inside the file it is trying to protect, the weakest possible enforcement location.

The fix is small. A one-paragraph addition to CLAUDE.md (or a brief mention in the punch-list resolution) saying "files named as tombstones are not to be extended; replace wholesale or leave alone" would convert the implicit rule to explicit.

## 7. Lens-specific weakest-link

The tombstone has no enforcement against accretion: no documented rule, no header marker a CI check could assert against, no recurring sweep, no review hint beyond the prose self-description.

## 8. Verdict

`rework`.

**Smallest change to approve:** add a single sentence to the tombstone body marking it as immutable-by-convention (*"This file is a tombstone — do not extend it; replace wholesale or leave it alone"*), AND add one explicit sentence to the plan's rollback section naming the consequence (rollback returns the repo to the broken-reference state item 7 was filed to fix). Optionally a CI grep asserting the tombstone marker.
