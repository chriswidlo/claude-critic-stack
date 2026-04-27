# Critique — product lens — ark-mono phantom fixture

## 1. User-visible consequence

The day this ships, the operator-as-user opens [CLAUDE.md](CLAUDE.md) and sees an example session id rendered as `<YYYY-MM-DD>-<slug>` accompanied by an explanatory parenthetical. The most likely first reaction is not "ah, this is honest documentation" — it is **"this section is unfinished"**, because angle-bracket placeholders in canonical config files are a strong learned signal of stub content elsewhere in the same repo. The candidate's assumption #1 acknowledges this risk but ships anyway with "preview the rewrite before committing" as the verification step. That is not a verification — it is a one-person taste check.

The punch-list itself goes from 13 rows with item 5 open to **14 rows with item 5 partially closed and item 5b open and dependent**. A reader scanning for repo health sees one more row of debt, not one fewer.

## 2. Commitments implied

Adding item 5b is a **public, dated promise** that the operator (or some future agent) will:

- Author an exemplar contract with five named subcomponents.
- Run the regression against that contract.
- Produce the first exemplar.

Once committed to git with a date prefix, this row is load-bearing: every future reader of the punch-list treats it as live work. Untreated, it accrues the same "phantom" status that item 5 currently has — a documented commitment with no backing artifact. **The candidate is proposing to fix a phantom by writing a second, more elaborate phantom.**

The exemplar contract content also commits the repo to a specific construction-standards shape for *all* future exemplars, not just this one. This is a quietly bigger commitment than a single punch-list row — it is a de facto template. The candidate doesn't name this.

## 3. Migration burden

- **Future agents reading [CLAUDE.md](CLAUDE.md)** must now parse a placeholder shape rather than a concrete example. Pattern-completion behavior on placeholders is worse than on concrete examples.
- **The operator** inherits item 5b's contract-authoring work; bounds are aspirational.
- **The author of items 6–13** now has a precedent: when a punch-list item is half-closeable and half-deeper, split it and write a contract. The candidate calls this a "tradeoff" but does not check whether items 6–13 are bimodal.

## 4. Product affordances

**Better:**

- The doc-correctness bug is closed today.
- Future readers will not chase a dead slug.
- The distiller-step gap is named and routed to a fix.

**Worse:**

- The repo's docs now contain a self-described placeholder, which makes them read as in-progress.
- The mental model "the regression suite has no exemplar but does have a written contract for what would become one" requires the contract to exist. After step 1 ships and before 5b is picked up, the actual mental model is **"the regression suite has no exemplar, has no contract, but has a punch-list row promising both."** Strictly worse than the pre-ship "no exemplar, period" because it adds meta-debt.

## 5. Frame-level objection

The candidate frames its product surface as **the punch-list**. From a product lens, **the punch-list is not the primary surface — [CLAUDE.md](CLAUDE.md) is.** CLAUDE.md is loaded at every session start; it is the contract between the repo and every future invocation. Optimizing the artifact most users actually read for honesty by *introducing a placeholder there* and pushing the resolution into a less-read artifact (the punch-list) inverts the surface hierarchy.

The candidate treats this as a *documentation correctness* problem with a *workflow execution* shadow. The product-lens reading is the opposite: it is a *workflow execution* problem (the test was supposed to run; it didn't) with a *documentation correctness* shadow (two docs disagree). Step 1 fixes the shadow and commits-via-row-5b to fix the substance later. That is a UX of "we cleaned up the visible mess and wrote ourselves a note about the real problem" — exactly the F2 paper-over failure mode.

A second frame-level objection: the candidate's audit found the distiller-step gap and concluded "additive, not invalidating." From a product lens, **what counts as invalidating is decided by the user of the test, not by the auditor.** If a future agent runs the regression and the distiller silently misbehaves while the test passes, the test has lied about its coverage. A test that lies about coverage is a worse product than no test at all.

## 6. Verdict

**rework.**

What would change the verdict: drop the placeholder-in-CLAUDE.md move (or relocate the example into a dedicated `examples/` block where stub-shape is normal), and either (i) commit to authoring item 5b's exemplar contract in this same session before shipping step 1, or (ii) acknowledge that the precedent set by 5b for items 6–13 is bespoke rather than pattern, with a one-sentence rule for when split-then-defer-with-contract applies.
