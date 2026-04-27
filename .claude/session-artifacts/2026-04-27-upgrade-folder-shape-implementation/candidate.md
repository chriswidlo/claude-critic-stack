# Candidate v2 — strangler migration, README.md inside folder, no script

## Position

The convergent loop-1 panel feedback is sharper than v1 admitted. Rewrite the candidate around the underlying insight all three lenses surfaced: **stop accreting structure that defers the load-bearing decisions.** Concretely, that means dropping things v1 added (the LEDGER counter, the elaborate lift conditions, the top-level `bin/` directory, the deferred slug-vs-README.md decision) and making smaller, more honest commitments.

**Five revisions from PREPARE / v1, each grounded in specific critic feedback:**

1. **Convention: `<slug>/README.md` inside the folder, not `<slug>/<slug>.md`.** *(Product critic: naming-contract decisions cost 30× more to reverse after migration. Architecture critic: slug-repetition lacks an enforcer; identity-at-every-level proves too much. Challenger: README.md auto-renders on GitHub, matches Hugo's leaf-bundle convention, kills the path-autocomplete-twice problem.)* This is a binding decision in this candidate, not an open question. Operator can override; the candidate recommends it.

2. **No batch migration script. Strangler-style instead.** *(Architecture critic explicitly named this alternative. Operations critic showed the script's lift-conditions are forward-path engineering for a recovery-shape problem. Product critic showed the engineering pays premiums for risks that don't fire when migration is one-sitting.)* The format-only state-transition gate gains one rule: it refuses to advance any flat-shape entry past 🌱 created. Existing flat-shape entries migrate naturally as they progress through lifecycle. No `bin/` directory needed.

3. **No LEDGER counter. No mutation of LEDGER by tooling.** *(Architecture critic's frame-level objection: LEDGER's identity is "index"; counter promotes it to "dashboard" silently. Operations critic: counter counts wrong thing anyway — un-started not in-flight.)* Backstop instead: one shell one-liner the operator can run any time, `find upgrades/ -maxdepth 2 -type f -name "20*.md" | grep -v LEDGER | grep -v README` returns the list of un-migrated entries. Derived state, not stored.

4. **Slash-command edit kept, split into two commits.** *(Operator already authorized in accept. SRE 2016 + Fowler stub on bundling = direct hit. Bug fix is its own decision unit.)* Two commits to `.claude/commands/upgrade.md`: first the bug fix (vertical → horizontal state table), second the path-shape change (write `<tier>/<slug>/README.md`).

5. **Migrate the one existing folder-shaped entry** (`upgrades/normal/2026-04-26-living-poweruser-knowledge-module/`) to the new README.md convention. *(One `git mv` of `<slug>/<slug>.md` → `<slug>/README.md`. Cost is minimal; benefit is uniform shape post-decision.)*

## What v2 ships on day 1

| Step | Action | Effort |
|---|---|---|
| 1 | `upgrades/README.md` — folder shape becomes canonical, `<slug>/README.md` is the convention. ~10 lines of prose. | XS |
| 2a | `.claude/commands/upgrade.md` — bug fix only (step 5 vertical → horizontal). Commit. | XS |
| 2b | `.claude/commands/upgrade.md` — path-shape change (write `<tier>/<slug>/README.md`). Commit. | XS |
| 3 | Update format-only state-transition gate's `🔬 spiked` rule (and successor states) to refuse advancing flat-shape entries. *(See Strangler-rule appendix below.)* | XS |
| 4 | Migrate the one existing folder-shaped entry: `git mv upgrades/normal/<slug>/<slug>.md upgrades/normal/<slug>/README.md`. | XS |
| 5 | Update LEDGER row for that entry to point at `<slug>/README.md`. | XS |
| 6 | Update this entry's state-table 🔨 implemented. | XS |

**Total: ~30 minutes of bounded edits. No `bin/` directory. No script. No counter. No idempotency property to prove.**

## What v2 does NOT do (and why)

| Removed | Why removed |
|---|---|
| `bin/migrate-upgrade-shape.sh` | Architecture critic: top-level `bin/` is a permanent architectural commitment, not a directory choice. Operations critic: the script's complexity pays premiums for compounding-error risks that don't fire in one-sitting modal execution. Product critic: speculative-future-value used to justify concrete-present-complexity. |
| Idempotency / pre-flight / verification / four-lift-conditions | Operations critic: forward-path engineering for a recovery-shape problem. Strangler-style sidesteps the entire failure class by having no batch step to fail at. |
| LEDGER "Flat-shape entries remaining: N" counter | Architecture: LEDGER is index, not dashboard. Operations: counter's predicate misses half-migrated state anyway. Product: feature designed for a reading habit nobody confirmed exists. |
| Big-bang migration of all ~30 entries | Strangler is slower (weeks/months vs one sitting) but the value of "all entries same shape" is near zero relative to "all NEW entries same shape + old entries migrate as touched." Personal R&D lab; no consumer is waiting. |
| Slug-vs-README.md as "open question handed to operator at synthesis" | Product critic: 30× more expensive to reverse after migration. Made into a binding recommendation in v2 — operator overrides if disagrees, but the default is committed. |
| Three open questions to operator | Reduced to one (the slug-vs-README.md recommendation; everything else is decided). Operator's job at accept is to confirm or override the named decision, not to adjudicate three. |

## Strangler-rule appendix

The format-only state-transition gate (`.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py` for now; will productionize as `/upgrade advance` later) currently checks body content against a schema in the README. The new rule it gains:

> Before checking the body, check the entry's path. If the entry is at `<tier>/<slug>.md` (flat shape), refuse to advance past 🌱 created. Print: *"This entry is in flat shape. Migrate to folder shape (`<tier>/<slug>/README.md`) before advancing. Migration is `git mv <tier>/<slug>.md <tier>/<slug>/README.md` followed by updating the LEDGER link."*

The rule lives in the script. It does not write anything to the entry or to LEDGER. It just refuses to advance, with an actionable message naming the exact `git mv` to run.

This converts the migration from a batch operation into a per-entry gate the operator passes through naturally. After ~6 months, every entry that has reached `🔬 spiked` or beyond is in folder shape; entries that stay at `🌱 created` indefinitely never get migrated, which is the right outcome (they aren't being touched, no work to enforce, no harm).

## Named tradeoffs

| Trade | Cost paid | Cost avoided |
|---|---|---|
| Strangler vs batch | Migration takes weeks/months instead of one sitting; lab lives in mixed shape during that window. | Every failure mode the script's four lift conditions exist to handle. The script itself. The `bin/` directory. The counter. The recovery procedure. The idempotency proof. |
| README.md vs `<slug>/<slug>.md` | One existing folder-shaped entry needs one extra `git mv` to migrate. Slug-rep convention's "identity at every level" is given up. | GitHub web auto-render. Hugo-conventional. Path autocomplete works in one TAB. `find -maxdepth 2 -name "*.md"` filtering stays sensible. The unenforced "folder-name == doc-filename" invariant the architecture critic flagged just doesn't exist as a problem. |
| One open question vs three | Operator can't easily say "all of these are wrong" without rejecting the whole candidate. | Orchestrator-uncomfortable-committing failure mode the product critic named. Decisions are made; operator confirms or overrides the recommendation. |
| Bug-fix split into separate commit | One extra commit. | Coarser revert unit if either edit is wrong. |
| Updating the gate (an existing primitive) instead of writing a new script | The gate gains a third concern (path-shape check) on top of body-content check. Some coupling. | A new, throwaway, never-runs-again script. The `bin/` directory. |

## Named assumptions (would flip the recommendation if wrong)

1. **The operator agrees that "uniform shape across all entries by date X" is not load-bearing.** If they want a clean lab in one sitting (rather than one that converges over months), strangler is wrong and the batch script is right. The candidate assumes mixed-shape during the migration is fine because no consumer is waiting.
2. **README.md auto-render is actually load-bearing for the operator.** If they primarily read the lab in `cat`, `less`, or Obsidian (not GitHub web), the README.md advantage is hypothetical. The candidate weights GitHub web as a real surface; if the operator never opens github.com on this repo, this argument loses force.
3. **The format-only gate is the right enforcement surface for the strangler rule.** If the operator advances entry states by hand-editing the date (which the README still permits — "manual act") rather than by invoking the gate, the strangler rule never fires. Mitigation is the same as the existing gate's: voluntary use; warning-only would be the natural extension if blocking proves friction.
4. **The existing folder-shaped entry's owner is OK with the `<slug>/<slug>.md` → `<slug>/README.md` rename.** That entry was authored by a parallel session. If they object to the rename, the convention decision becomes contested. Mitigation: ask before renaming, or leave that entry as the exception with a note in its body.

## Named ways this could be wrong

1. **Strangler is the candidate's central commitment, and it's the most contestable.** Strangler trades "uniform-by-date-X" for "uniform-eventually." Some operators find that intolerable; the candidate assumes this operator does not. If wrong, strangler is the wrong shape and the batch script is back on the table.
2. **The README.md decision may itself be premature.** The challenger and product critic landed real hits, but the existing folder-shaped entry's convention was set without considering README.md either. Both decisions (slug-rep AND README.md) are ad-hoc; neither was deliberately chosen against the other in a head-to-head. v2 picks README.md based on critic feedback; if that feedback is itself anchored on Hugo conventions that don't actually apply to a personal R&D lab, the recommendation is weaker than it looks.
3. **Updating the gate's rule is itself an `.claude/`-side change** the candidate didn't pre-authorize. The format-only gate's prototype lives in `.claude/session-artifacts/`; productionizing the strangler rule means editing that script (or its eventual `/upgrade advance` form). This is in scope of what the operator authorized in accept (the slash-command edit), but worth flagging.
4. **"Cost is minimal" for migrating one folder-shaped entry assumes the parallel session that authored it is reachable.** If they're not, the decision is unilateral. Acceptable for a personal repo; worth naming.

## Frame-level objection from challenges.md — addressed

Challenger's frame-level: *"plan optimizes for one bounded engineering session that ships a clean batch while reference class rewards no silent compounding errors and visible mixed-state accounting."*

v1 addressed this with amendments (LEDGER counter, idempotency, lift conditions). The panel showed those amendments accreted structure rather than fixed the frame.

**v2 addresses it by choosing strangler.** Strangler does not ship a clean batch; it ships a small set of edits that change the *contract* (slash-command writes new shape; gate refuses to advance flat-shape) and lets the corpus migrate by natural advancement. There is no "clean batch" failure mode because there is no batch. There is no "silent compounding errors" failure mode because the gate fails loudly per-entry at the moment of advancement. Mixed-state accounting becomes visible via the on-demand `find` one-liner.

The challenger's *"tidy not migrate"* alternative frame is essentially adopted, with one difference: instead of doing it by-hand at one sitting, the strangler rule does it by-hand per entry over time, with the gate as the forcing function. Same frame, distributed execution.

## Convergent insight from loop-1 panel — explicitly addressed

The panel converged on: *the candidate accretes structure that looks like discipline but actually defers the load-bearing decisions*. v2's response is to drop the structure that was deferring the decisions:

- Drop counter → no LEDGER promotion to dashboard.
- Drop script → no `bin/` permanent architectural commitment.
- Drop "decide later" on slug → make the binding decision now.
- Drop three open questions → reduce to one (the slug-vs-README.md recommendation, where operator confirms or overrides).

Each of these is a smaller-not-larger move. The total surface of v2 is meaningfully smaller than v1, which was meaningfully smaller than the PREPARE plan.

## Single open question for operator

**Is README.md inside the folder the right convention, or is `<slug>/<slug>.md` (the convention used by the one existing folder-shaped entry) right?**

If README.md: v2 stands as-is.
If `<slug>/<slug>.md`: revert the README.md sections of v2; everything else (strangler rule, no script, no counter, bug-fix split) still applies.

Recommendation: README.md, for the reasons named (GitHub auto-render, Hugo convention, no slug-rep verbosity, no naming-invariant enforcement burden, one extra `git mv` cost is bounded).
