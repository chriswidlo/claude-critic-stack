# Frame challenges — upgrade-folder-shape implementation

## Frame as given

The orchestrator's frame is "shape migration as a small, scripted refactor." The implementation is treated as ~30 mechanical `git mv`s plus a `sed` over `LEDGER.md`, packaged into one `bin/migrate-upgrade-shape.sh`, sequenced behind an upstream slash-command edit (Option C). The slug-repetition convention (`<slug>/<slug>.md`) is taken as settled by the entry's body ("identity should be visible at every level"), the slash-command bug fix is folded into the same edit as the path-shape change, and "make a script" is taken as the obvious tool for N≈30. The optimization target is *uniformity of shape across the lab, achieved in one bounded engineering session*.

## Alternative frame

**Reframe: "this is a one-shot janitorial pass on a personal-lab corpus, not a refactor."** Under this frame the verb is not *migrate*, it is *tidy*. The N is small enough that each entry can be visually verified by a human in seconds; the asymmetric cost is in *mistakes that compound silently*, not in *labor*. The optimization target flips from "uniformity in one batch" to "no silent compounding errors, regardless of how long the corpus stays mixed-shape." Concretely, this frame favors **by-hand migration with a checklist** over a script — `git mv` and a manual LEDGER edit per entry, eyes on each diff, no `sed` regex to debug, no idempotency property to prove, no `bin/` directory introduced for a tool that runs once. The folk-wisdom canon-gap the librarian flagged ("don't write a script for 30 files") is the load-bearing premise of this frame. The script frame inherits a class of failures (regex misses, idempotency edge cases, partial-state semantics) that the by-hand frame does not have at all.

## Condition under which the current frame is wrong

The current frame is wrong if the actual modal failure is *operator stalls mid-migration and forgets the script's exact invariants by the time they return* — in which case the script's existence makes resumption *harder* than picking up a checklist, because the operator must re-derive what the script assumed about the repo state before re-running it.

## Challenges to scope-map preservations

(No `scope-map.md` was read in this invocation; the orchestrator's handoff did not enumerate preserved primitives. If the scope-map preserved the `bin/` directory introduction, the bash-tooling choice, or the LEDGER-as-single-source-of-truth assumption, those preservations should be challenged in their own pass. Flagging this as a gap rather than fabricating preservations.)

## Challenge to the slug-repetition convention `<slug>/<slug>.md`

The entry's body defends repetition with "identity should be visible at every level." That is one ergonomic claim; the canon-librarian's gap report flagged that **real industry debate exists across language ecosystems** (Java package=path, Python `__init__.py`, Rust `mod.rs` historically and `mod_name.rs` post-2018, Go package=directory, Node `index.js`, Hugo `index.md` leaf bundles) and the corpus does not adjudicate it. The librarian's note that "README.md inside the folder" is a real alternative is not a stylistic quibble — it is the dominant convention in the closest reference class the outside-view named (Hugo leaf bundles use `index.md`, not `<slug>/<slug>.md`).

**Steel-man for `README.md` inside the folder:**

1. **GitHub and most filesystem browsers auto-render `README.md` when the folder is visited.** Walking `upgrades/no-brainer/2026-04-26-upgrade-entries-as-folders/` on github.com would render the doc inline; walking the same folder under the slug-repetition convention shows a directory listing with one file, and the reader has to click through. The convention loses the most common reader path.
2. **Renaming a folder costs one `git mv`; renaming a folder *and* its identically-named child costs two coordinated `git mv`s.** Slug churn (which the lab has tolerated before — see the date prefix on every slug, evidence that identity is already not stable) becomes more expensive under repetition.
3. **The "identity at every level" argument proves too much.** By that logic the meta table inside the doc should also repeat the slug as an explicit field; the H1 already does, and that is sufficient. The path is a locator, not a place to re-state identity.
4. **The entry's own justification for rejecting `README.md` ("collision with sub-folders that want their own README") is weak at N=0** — no entry today has a sub-folder, let alone one wanting a README, and the failure mode is recoverable (rename the inner README) if it ever appears.

The slug-repetition convention biases the downstream answer toward *"every reader is a CLI user with `ls`"* and against *"some readers are GitHub web users, some are Obsidian users, some are future-LLM-readers expecting Hugo conventions."* The convention may still be right; it has not been challenged on its merits in the entry's body.

## Challenge to bundling the slash-command bug fix into the migration edit

The plan folds the step-5 vertical-state-table bug fix into the same edit as the step-4/step-8 path-shape change to `.claude/commands/upgrade.md`, justified as "bonus, in the same file." The canon-librarian returned a **direct hit** from the SRE Book 2016 against this: *"Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously."* The Fowler stub adds: by definition, a refactoring is behavior-preserving; bundling a behavior change makes the operation no longer a refactoring. The requirement-classifier's frame-bias note named this same risk: *"items 4 and 6 are behavior changes hiding inside a 'shape migration'; the refactor frame will tend to wave them through as incidental cleanup."*

**Steel-man for "fix the bug separately":**

1. **The bug has independent existence and independent falsifiability.** It either currently produces wrong output for new entries or it does not. Whichever answer, that determination has nothing to do with folder shape. Bundling forces the migration's verification report to include "did the state-table-format fix work" — which the migration script cannot verify because state-table format is rendered downstream.
2. **If the path-shape edit is wrong and gets reverted, the bug fix reverts with it** — even though the bug fix was not the cause. `git revert` becomes coarser than the actual decision unit.
3. **If the bug fix is wrong and gets reverted, the path-shape edit reverts with it** — and now new entries land in flat shape again, breaking Option C's premise that all new entries arrive in folder shape.
4. **The bug pre-existed the migration discussion.** That it was noticed during the survey is a discovery, not a coupling; the right response to "I found another bug while I was here" is to record it and ship it separately, not to pile it onto the change in flight.
5. **N=2 file edits costs nothing in commits.** The cost of separation is one extra commit. The cost of bundling, if either edit is wrong, is a tangled revert.

The bundling biases the downstream answer toward *"this single file's edits are atomic"* and against *"each edit has its own success criterion and its own revert path."*

## Challenge to Option C as the right coordination strategy

Outside-view's distillation made the trade explicit: Option C is *"the largest single variance-reducer in the proposal"* AND it *"enables failure mode #3 (partial migration becomes permanent)."* The orchestrator's plan accepts this trade and offers no fourth option. The trade is real but not forced.

**A fourth option — "Option D, deadline-with-tooling":** land the slash-command edit (so new entries arrive correctly) AND set a **dated commitment in the entry's state table** for completing the existing-entry migration (e.g., "migration of pre-2026-04-27 entries committed by 2026-05-04; if not done, the entry's state regresses from ✅ accepted to 📋 prepared and the slash-command edit is reverted"). This re-introduces the deadline that Option C removed, but binds it to a *visible counter* (the lab's own state-table discipline) rather than to operator memory. Failure mode #3 ("partial migration becomes permanent") is mitigated by the same mechanism the lab already uses for every other commitment: state-table dates that the operator has to look at.

A weaker fourth option — **"Option C-prime"**: Option C plus the lift condition the outside-view subagent named verbatim — *"a one-line `find`/`ls` check reporting 'N flat-shape entries remaining,' so partial-state-becomes-permanent has a visible counter."* Add this to `LEDGER.md` as a header line that updates on each migration. The mixed-state becomes self-reporting rather than invisible.

The choice between C, D, and C-prime is not litigated in the entry. Option C is presented as **preferred** without comparison to a deadlined variant, and the "migrate at any pace" framing actively obscures the partial-permanence risk that the outside-view distillation named as failure mode #3.

The Option C bias is *"removing the deadline trap is unambiguously good"* — it is not, when the deadline trap is the only thing forcing closure on a job the operator has explicitly de-prioritized ("migration window TBD by operator").

## Frame-level objection the orchestrator should carry forward

The plan optimizes for "one bounded engineering session that ships a clean batch" while the actual reference class (solo lab, ~30 files, no consumers, no deadline) rewards "no silent compounding errors and visible mixed-state accounting" — those are different optimizations and the script-plus-Option-C combination only wins on the first one.
