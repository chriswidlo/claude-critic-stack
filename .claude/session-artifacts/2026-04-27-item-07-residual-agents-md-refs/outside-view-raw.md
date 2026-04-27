# Outside-view raw return — item 7

## 0. Canon-first

The agent attempted to read the canon corpus directory but its tools did not allow directory listing in this thread. It proceeded with web search, naming the gap explicitly: **canon coverage of "documentation reference cleanup after deletion of a constitutional artifact" is unknown to me from this session; I could not enumerate `canon/corpus/`.** The base-rate work below leans on web sources for currency. None of the cited web results should be promoted to canon by this citation alone.

Canonical frames that *should* exist in the corpus and that the agent invoked from prior knowledge rather than retrieval:
- **Kahneman & Lovallo (1993)** on inside-vs-outside view — relevant because the inside view of "just delete the dead string" feels cheap and obvious; the outside view asks how often that leaves a silent argumentative wound.
- **Chesterton's Fence** — relevant inverted: when a referenced *partner* fence is removed, the surrounding argument's load-bearing structure may now sit on air, and a string-scrub will not detect that.
- **Naur (1985), "Programming as Theory Building"** — the theory of an artifact lives in heads and surrounding prose, not just the artifact itself; deleting the artifact does not automatically delete the theory it was holding up, which is why downstream prose now lies.

## 1. Reference class

Three plausible classes; ranked by predictiveness:

1. **Most predictive — "Reconciling downstream documentation after deletion of a co-equal/partnered artifact in a small documentation corpus."** Specifically: removing a constitutional or policy doc that was named in parity with a surviving sibling, and then deciding how to update the downstream prose that referenced the pair. The "parity" framing matters — the deleted thing was not a peripheral mention, it was a *structural counterweight* in arguments.
2. **Second — Decommissioning a component / API and pruning references.** Closer to the live-doc category (1) above; less close to the upgrade-cell and historical-narrative categories.
3. **Third — General "stale comment / reference rot."** Too broad. The unique feature here (removed item was a *premise*, not a *pointer*) is lost in this class.

The unique structural feature: the deleted file was **load-bearing in arguments**, not merely **named in lists**. That distinguishes this from generic dead-link cleanup.

## 2. Base rate

Numbers below are qualitative estimates flagged as such — no precise quantitative data was retrieved.

- **Pure string-scrub passes (option A) on argument-bearing references:** estimated **60–75%** leave at least one silent-scope-shrink (a benefit claim, an invariant, or a rationale whose premise just became 50%-true and reads as overclaiming). Anchored in: (a) comment-rot literature showing local edits to references rarely propagate to surrounding prose; (b) broken-windows finding that one un-reconciled inconsistency seeds more; (c) refactoring-tooling observation that "silent" reference removal is the dominant failure mode when no human re-reads the surrounding context.
- **Argument-level rereads (option B) on small corpora (<100 referencing sites):** estimated **20–35%** over-engineer — typically by promoting cosmetic edits to substantive rewrites that re-litigate already-settled decisions, or by introducing new claims the rereader finds "more honest" but that were not part of the original record. The over-engineering rate rises sharply with corpus size; for very small corpora (≤ ~20 referencing sites split across three categories, as here) the rate is at the low end.
- **Failure asymmetry:** (A)'s failure is **silent** (you do not notice the weakened argument; it surfaces months later as a confused reader or a contradictory upgrade). (B)'s failure is **visible** (PR diff is bigger than expected, reviewer pushes back, you cut scope). Visible failures self-correct; silent failures compound.

Flag: these percentages are *estimates*, not retrieved statistics. They are directionally defensible from the cited web literature on code rot, broken windows, and refactoring scope drift but are not themselves measurements.

## 3. Position relative to base rate

Features of this proposal vs. the reference class:

**Above base rate (favorable):**
- Corpus is small and the referencing sites are categorized into exactly three buckets with different semantics — that is unusually clean.
- The deleted artifact was a *named co-equal*, not a deeply embedded primitive; the load-bearing-ness is concentrated, not diffuse.
- The repo is an adversarial-review stack with a critic-panel discipline. The infrastructure to detect silent-scope-shrinks already exists.

**Below base rate (unfavorable):**
- Category 2 ("forward-looking benefit columns claiming parity between two docs") is *exactly* the silent-scope-shrink trap. The benefit was framed as parity. With one side gone, the parity claim is now either trivially true (only one doc to track) or false (the comparison no longer exists). A scrub that replaces `CLAUDE.md and AGENTS.md` with `CLAUDE.md` quietly changes the argument from "drift between two artifacts becomes detectable" to "drift in one artifact becomes detectable" — a *much weaker* claim, possibly tautological.
- Category 3 (historical narrative / catalysts) is the opposite trap: a reread risks rewriting history. Catalysts should *not* be edited; they record what was true at the time.
- The three categories require **three different cleanup policies**, not one. A single-mode pass (either pure A or pure B uniformly applied) will be wrong in at least one category.

## 4. Typical failure mode

For (A) — pure string-scrub:
- Dominant failure: **silent benefit-deflation** in upgrade-entry cells. The cell still claims a benefit, but the benefit's argument now rests on a single doc where it previously rested on two. No reader notices because the prose still parses; the claim is just weaker than it reads. Six months later, a future agent cites the upgrade entry as evidence of a discipline that was never quite installed.
- Secondary failure: live constitutional docs (category 1) get scrubbed correctly because the change is mechanical, but the tone of the surrounding rule drifts — "apply to CLAUDE.md and AGENTS.md alike" becomes "apply to CLAUDE.md," and the *generality* of the rule (it was meant to apply to *any* root-level constitutional doc) is silently lost.

For (B) — full argument-level reread:
- Dominant failure: **catalyst contamination**. Rereading historical narrative under current knowledge produces "honest" rewrites that retcon what was actually known at the time. This is worse than a silent-scope-shrink because it destroys audit trail.
- Secondary failure: the rereader finds the upgrade-entry argument *did* depend on the deleted partner, and rather than honestly marking the upgrade as "premise weakened, benefit revised down," they rewrite the cell to claim a different benefit that was never the original justification. **Post-hoc rationalization disguised as cleanup.**

## 5. Outside-view verdict

**Reference class unclear at the level of a single A-vs-B choice; the proposal is below base rate if a single mode is applied uniformly, within tolerance if the three categories are split.**

The framing of the question (A vs. B) is itself the largest risk. The three referencing categories have different correct treatments:

- **Category 1 (live constitutional docs):** option A is correct *if* the rule's generality is preserved. Concretely: do not just delete `AGENTS.md` from the path-discipline rule; rewrite the rule to name the *class* (root-level constitutional artifacts) it was meant to govern, so the rule survives the next such artifact. **A-with-a-generality-check, not pure A.**
- **Category 2 (forward-looking benefit cells in upgrade entries):** option B is correct. The benefit claim was *load-bearing* on the partner doc. A scrub here is the silent-scope-shrink trap. The honest move is to mark the cell as "premise revised: AGENTS.md removed; benefit now reads as <X> rather than <Y>" or to retire the cell. Highest-risk category.
- **Category 3 (historical catalysts):** option A is correct, with a stronger constraint: **do not edit catalysts at all**. Catalysts are dated records of what was found at the time. If `AGENTS.md` was grepped and found empty in March, that finding stands as historical fact even though the file no longer exists. Add a forward-pointer footnote ("AGENTS.md was subsequently deleted on <date>; see <link>") rather than editing the narrative.

**What would lift this above base rate:** explicitly decide per-category, not globally. Name each category's policy in a one-paragraph decision record before touching any file. The cheapest mechanism that prevents silent-scope-shrink in category 2 is to run each touched upgrade-entry cell past one critic lens (operations or product) with the prompt "is this benefit claim still load-bearing or did it just lose a premise?" — that single check, applied to ~5–10 cells, costs less than the rework cost of a silent scope shrink discovered six months later.

**What would clarify the reference class further:** a count of how many referencing sites fall in each of the three categories. If category 2 is one cell, this is trivial; if it is fifteen cells with interlocking arguments, the cost calculus shifts toward (B) for that category and the over-engineering risk recedes.

---

Sources (web, post-canon-gap):
- Reference class forecasting — Wikipedia
- The broken windows theory applies to technical debt — Empirical Software Engineering
- Code rot and productivity — DX
- Chesterton's Fence — thoughtbot
- Misusing Chesterton's Fence — Econlib
- Safe Delete refactoring — JetBrains ReSharper
- Refactoring made right — Kiro
- Catalog cleanup job (orphaned entities) — Backstage
