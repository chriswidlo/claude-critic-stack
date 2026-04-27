# Synthesis — upgrade-folder-shape implementation

The workflow ran with a disagreement at loop 2. Product critic held out at `rework` while architecture and operations approved candidate v2. Per CLAUDE.md's two-loop cap, this synthesis surfaces the disagreement and hands the headline question back to the operator.

## Classifier label and alternative
- **Primary:** `refactor`
- **Alternative:** `extend` — would become primary if the critique centered on the *new affordance* (entries-as-folders enabling stapled artifacts) rather than mechanics.

## Reframe
The orchestrator did not write a separate `frame.md` for this run (PREPARE state already framed the question; the workflow critiqued implementation choices). The operative reframe came from the loop-1 panel: *the candidate accretes structure that looks like discipline but actually defers the load-bearing decisions*. v2 was rewritten around that frame.

## Reference-class forecast (from outside-view distillation)
Class: solo-operator content-repo restructurings, N=10–100, with one index file to lockstep-rewrite + a tooling/config file determining future-entry shape. Closest adjacents: Hugo leaf-bundle migrations, Jekyll `_posts` → collections, Obsidian re-foldering.

Base rate: ~75–85% joint success (clean completion + no partial state + operator continues using new shape + link integrity holds). Above base rate primarily because of tooling-first sequencing (the slash-command edit lands first).

Modal failure: `sed` regex misses an edge-case link form. Failure mode #3 (partial migration becomes permanent) is *enabled* by the chosen "migrate at any pace" coordination strategy.

## Canon passages (supporting and contradicting)
- **Supporting (SRE 2016 simplicity):** "Simple releases are generally better than complicated releases." → Direct hit on the bundle-bug-fix-with-shape-edit decision; v2 splits them.
- **Supporting (SRE 2016 modularity):** "Just as it is poor practice to write a 'grab bag' class... it is also poor practice to create a 'util' or 'misc' binary." → Direct hit on the script doing four things; v2 dissolves the script.
- **Contradicting (SRE 2016 idempotency cautionary half):** *"Pretending a fix is idempotent when it isn't is worse than admitting non-idempotency."* → Direct hit on Option A (bare eventual consistency); v2 dodges this by removing the script entirely.
- **Contradicting (Fowler stub):** *"Refactoring is by definition behavior-preserving; if you're changing behavior, that is not a refactoring."* → Bundling a behavior change (bug fix) with a structural move means the operation is no longer a refactoring.
- **Bias flag:** every quoted passage is from Google SRE Book — single-source. Hyperscaler ops applied to a personal R&D lab. Mismatch real.
- **Gaps flagged:** slug/path-repetition conventions across language ecosystems (Java/Rust/Go), git rename mechanics, Strangler Fig by name, "don't write a script for 30 files" folk wisdom, commit-hygiene literature.

## Scope-map summary
PREPARE state served as the scope-map (9-row consumer survey). Conflicts identified there (slash-command edit out-of-scope; LEDGER link rewrite; README prose update; `relates_to` heterogeneity) were resolved into the implementation plan. No fresh primitives surfaced in the workflow.

## Frame-level challenge and how the recommendation addresses it
Challenger's load-bearing objection: *"plan optimizes for one bounded engineering session that ships a clean batch while reference class rewards no silent compounding errors and visible mixed-state accounting; script+Option-C only wins on the first."*

v1 addressed this with amendments (counter, idempotency, lift conditions). The panel showed those amendments accreted structure rather than fixed the frame. v2 addressed it by adopting strangler-style — no batch, no clean-batch failure mode, no silent compounding because the gate fires loudly per-entry at advancement.

The product critic's loop-2 frame-level objection adds a new constraint: **v2's strangler is a substantive product revision the operator did not accept**. Synthesis adopts this and hands the strangler-vs-batch question back.

## Post-critique recommendation (LABELED)

**The synthesis cannot recommend a single implementation without operator input.** The product critic's loop-2 objection is correct: choosing strangler (v2) silently revises what the operator accepted in PREPARE (batch + `bin/migrate-upgrade-shape.sh`). The headline question for the operator is:

> **Strangler (v2) or batch (PREPARE/v1)?**

The two options materially differ:

|  | **Batch (what was accepted in PREPARE)** | **Strangler (what v2 proposes)** |
|---|---|---|
| Day-1 reality | Lab uniformly shaped after one ~30-min sitting | Lab mixed-shape for weeks/months (or forever for cold entries); gate refuses per-entry as touched |
| New surface | `bin/` directory + migration script | Gate gains a path-shape rule |
| Failure mode | Script bugs (regex misses, half-migrated states); operator stalls mid-migration | Cold entries never migrate (the candidate calls this "right outcome") |
| Terminal state | Yes, clear "migration done" moment | No, asymptotic; "are we done?" needs a `find` one-liner |
| Operator load | Run script once, eyeball output | Per-entry friction at advancement time, indefinitely |
| Ops critic loop-1 lift conditions | Required (verification, idempotency, pre-flight, tripwire) | Sidestepped — no batch step to fail at |
| Architecture risk | LEDGER promotion to dashboard via counter; permanent `bin/` commitment | Gate gains second concern (path-shape on top of body schema); two `README.md`-named files (lab overview + entry doc) |

**If operator chooses BATCH:** revert to v1's plan with the four lift conditions adopted (idempotency three-state, `--status` mode, pre-flight case-collision check, post-migration verification grep). LEDGER counter dropped per architecture critic; `bin/` location decided (top-level vs `upgrades/.bin/`); slug-vs-README.md decided (recommend README.md per challenger arguments, but operator can override).

**If operator chooses STRANGLER:** v2's plan stands as written, with three documentation tasks added (gate's README updated to reflect path-shape concern; flat-shape tail at 🌱 documented in `upgrades/README.md`; on-demand `find` one-liner promoted into `upgrades/README.md` for discoverability).

The slug-vs-README.md decision rides along with whichever option is chosen — the candidate recommends README.md for both options, with the same rationale (GitHub auto-render, Hugo convention, autocomplete, no slug-rep verbosity). Operator can override.

## At least three named uncertainties

1. **Will the operator choose batch or strangler?** This is the primary open question. v2's silent revision was the workflow's failure to surface this earlier; synthesis surfaces it now.
2. **Is README.md the right convention?** Recommended by both v2 and (under batch) the synthesis. Steel-manned by the challenger; one existing folder-shaped entry uses slug-rep convention. If operator disagrees, slug-rep stands.
3. **Does the gate's "format-only" identity survive adding a path-shape rule?** Architecture loop-2 critic flagged this as a real-but-acceptable trade. If a third or fourth rule lands on the gate later, the gate accretes policy-enforcement responsibility without naming it. Worth watching.
4. **For strangler: do cold flat-shape entries staying flat forever actually matter?** v2 calls this "right outcome." Product critic calls it "lab uniformity given up indefinitely." The honest answer depends on whether anyone (operator, future agent, future reader) actually cares about uniform shape across cold entries.
5. **For batch: will the four lift conditions actually be implemented or treated as aspirational?** Operations loop-1 critic flagged this. If lift conditions are implemented sloppily, the script ships with the recovery-shape failure mode it was supposed to defend against.

## Cheapest experiment that would reduce the biggest uncertainty

**Uncertainty being reduced:** #1 (batch vs strangler — the operator decision).

**Experiment:** present this synthesis to the operator and ask them to choose. No agent-call cost; no implementation cost; the experiment IS the operator's answer. The workflow's job at the cap is to surface the question cleanly, which the synthesis above does.

If operator answer is **batch**: the second-cheapest experiment is implementing v1's plan with one entry first (the dogfood — this very entry), running the script with all four lift conditions, and observing what fails. ~15 minutes. Outcome: either lift conditions are robust (proceed to batch all 30) or they leak (the recovery-shape failure mode product/ops loop-1 named is real and the candidate needs another pass).

If operator answer is **strangler**: the second-cheapest experiment is updating the gate with the path-shape rule, then attempting to advance one flat-shape entry (any entry currently at 🌱 — there are ~28). ~5 minutes. Outcome: either the gate's printed migration command is actionable (operator runs the `git mv`, advances, done) or it's vague (gate output needs work; same failure mode as the format-only gate's original spike feedback).

## What this workflow run produced

- A documented spike + prepare for the entry (already in entry body before this run).
- An accept (operator's, recorded).
- A loop-1 panel that converged on a real frame failure (accreting structure that defers decisions).
- A loop-2 candidate v2 that addressed the convergent insight but introduced a new product-frame failure (silent revision of accept).
- A synthesis that surfaces the operator-facing question with both options laid out.
- A documented disagreement (product critic v2 = rework) preserved in critiques.md and decision-log.md.

The workflow's value here was *catching* the v1 over-engineering (loop 1) and *catching* the v2 silent-revision (loop 2). The implementation is not yet ready to ship, but the operator now has a clean choice to make rather than a foregone conclusion.
