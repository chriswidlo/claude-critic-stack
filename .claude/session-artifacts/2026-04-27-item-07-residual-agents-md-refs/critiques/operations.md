# Operations critique — item 7 (residual AGENTS.md references)

## 1. Most likely incident

At time T (six weeks after this commit lands), a meta-reviewer auditing whether the constitutional-layer-goals-modules upgrade actually delivered its claimed benefit reads the rewritten cell *"CLAUDE.md drift against GOALS.md becomes detectable"*, ticks it off as installed, and closes the audit. Root cause: the original benefit claim was a parity claim between two documents that — together — produced a crosscheck; rewriting the cell to a single-document claim deflated the benefit but preserved the *appearance* of an installed control, so the audit had no surface that paged.

## 2. Blast radius

- **Three upgrade-entry cells** — every reader from this commit forward.
- **Two upgrade entries** whose argumentative weight depends on those cells. If either entry's value claim is load-bearing for a downstream decision (a meta-review, a "should we revert this upgrade" decision, a canon-refresher proposing similar entries), the deflation propagates.
- **Future canon entries** modeled on these as templates — if a contributor reads the rewritten cell and copies the (now weaker) benefit phrasing as house style, the failure fans out into the upgrade canon.

## 3. Rollout / rollback

- Single commit, no flag, no canary — acceptable for prose *if* mechanical reversibility holds.
- `git revert` reverses the commit byte-level, but **only until the next edit to any of the five touched cells**; after that, rollback is a forward-fix.
- No two-systems-running period: the moment the commit lands, the new cell text is the only text any reader sees. **Detection of regression has to happen in pre-commit review, not post-commit observation.** The plan's verification step (#8, grep) is a presence detector, not a regression detector.

## 4. Observability gap

This proposal makes invisible:

- **Whether a rewritten benefit cell still carries argumentative weight.** No metric, no signal. Outside-view distillation called out 60–75% silent-scope-shrink rate on pure-A passes. Plan accepts the risk by appeal to small N (three cells) and shallow cells (single sentences). That mitigation is **inverted** — short cells *hide* their argumentative structure, and small N means there is no statistical noise to flag deflation against. Small + shallow is the *worst* regime for this failure mode, not the best.
- **The original wording of rewritten cells.** Survives only in `git log -p` on three specific files. Not surfaced anywhere a future meta-reviewer would naturally look (no strikethrough, no erratum, no Superseded-by).

The plan's verification (`grep -rn "AGENTS\.md"`) is a string-presence check. It does not catch:
- references-by-paraphrase (e.g., a cell saying *"both root-level constitutional docs"*);
- the literal string broken across line wraps;
- the symmetry question itself — the grep cannot tell whether the rewrite preserved the cell's argument.

## 5. Cost at failure

- **Success:** ~30 minutes; six edits; one commit.
- **Silent failure (most likely):** a future agent invocation cites the rewritten benefit cell as evidence that drift detection is installed. The cost is paid in *the wrong downstream decision*. Invisible until a bad citation produces a visibly-wrong recommendation.
- **Loud failure:** one revert, one re-plan, one new upgrade entry. **The plan implicitly assumes this is the worst case. The assumption is wrong** — silent failure is the worst case.

## 6. Frame-level objection

The plan frames item 7 as *textual cleanup with a tasteful exception list* and verifies via grep. The operational frame is **this is a state-change to the upgrade canon's argumentative content, and the canon has no read-side observability**. There is no metric, no log, no audit hook that pages on a future reader misreading a rewritten cell. In an operational system, you would not deploy a state-change to an unmonitored data store without (a) a pre-deploy invariant check or (b) a post-deploy detector.

The plan's deferral of the symmetry question to a follow-up upgrade entry is the load-bearing weakness. **A filed follow-up is not an ops mitigation — it is a TODO.** The "we'll address this in a future ticket" pattern is exactly the anti-defense where intent gets treated as control.

## 7. Lens-specific weakest-link

Step 8 (verification by grep) is the weakest link. It confirms the *string* was scrubbed; it does not verify the *cells' arguments* survived the scrub. Given the outside-view's 60–75% silent-scope-shrink estimate and the plan's own acknowledgment that cells #4 and #6 are admitted scope-shrinks, the verification step is **inverted**: it confirms the failure-prone operation completed without checking the failure mode the operation is most likely to produce.

## 8. Verdict

`rework`.

**Smallest change to approve:** replace step 8's grep-only verification with a per-cell argumentative-load reread (one critic-lens pass on each rewritten cell with the prompt *"is this benefit claim still load-bearing or did it just lose a premise?"*), AND add a one-line erratum next to each rewritten upgrade-entry cell so the rewrite leaves a visible trail. Either change alone is insufficient.
