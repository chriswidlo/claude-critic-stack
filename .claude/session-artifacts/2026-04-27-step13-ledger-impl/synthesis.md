# Synthesis — Step-13 session ledger

## Classifier label and alternative
- **Primary:** `extend` (a 13th step appended to the existing 12-step workflow; existing primitives preserved).
- **Alternative:** `new` — first quantitative observability primitive in the stack. The synthesis adopts a **mixed posture**: extend in surface, new in schema-discipline.

## Reframe (Revision 1, no replan needed)
The user's framing was implementation-flavored ("write a file at step 13"). The honest reframe asked whether the right shape is a file at all, vs an inline summary in synthesis. The synthesis answer: **both** — a file (for cross-session aggregation) and a citation in synthesis (for re-encounter). The user's framing held; no revision was needed.

## Reference-class forecast (from outside-view distillation)
Class: self-imposed lightweight metrics on personal/small-team workflows. Base rate of sustained adoption past 6 months: **20–35%**, modal failure **wallpaper** (recorded but never read). The candidate sits **slightly above base rate (~30–40%)** because it satisfies two lift conditions (one source-of-truth via the schema section + re-encounter via synthesis citation). Without those it drops to ~15%.

## Canon passages (supporting and contradicting)
- **Supporting (SRE 2016, Ch. 6):** small set of well-chosen metrics > large set of poorly-chosen ones. Three ratios is the right grain.
- **Supporting (Wlaschin):** counts as data, ratios as derived; prevents inconsistency.
- **Contradicting (Anthropic 2024, "simplest solution possible"):** every artifact has maintenance cost; resist additions over time. Addressed by hard pre-merge ceiling (8 items) and "no enrichment until 5 real ledgers exist."
- **Contradicting (Goodhart's law):** measure-becomes-target risk. Addressed by warnings being *advisory* and labeled as starting heuristics.
- **Contradicting (Ashby's law of requisite variety):** three ratios may not capture all over-elaboration modes. Acknowledged as named assumption #5 (flips recommendation if disproven by real sessions).
- **Bias flags:** corpus is heavily Anthropic-authored; "AI-native workflow self-instrumentation" has near-zero direct precedent — reasoning is by analogy.

## Scope-map summary and unresolved conflicts
- **Extend (3):** 12-step workflow (gain step 13), per-session artifact tree (gain `ledger.md`), session-artifacts README (gain ledger schema section).
- **Subsume (4):** subagent-distiller, decision-log pattern, cross-session memory write entry, exemplars folder.
- **No overlap (2):** lab state-transition gate, experiment-runner.
- **Conflict, soft (1):** entry #14 (hard-gates-as-harness-hooks). If/when #14 lands, manual orchestrator authorship becomes hook-driven; schema unchanged. Documented as a future-coupling, not a blocker.
- **Resolved conflicts:** synthesis-as-terminus (resolved by required citation pattern), counting "decisions" (resolved by parser-able definition), loop-cap-reached vs converged-at-loop-2 (resolved by separate boolean), division-by-zero (resolved by bypass-case documentation).

## Frame-level challenge and how the recommendation addresses it
The frame-challenger surfaced four challenges:
1. **Inline-only (no file)?** — addressed by *both*: file for aggregation; citation for re-encounter.
2. **Workflow vs operator self-diagnosis?** — addressed by warnings being advisory + thresholds tunable from one place.
3. **Manual authorship will drift?** — addressed by HTML-comment marker on load-bearing schema headings + Notes-section quarantine for free-form prose.
4. **Synthesis-as-terminus prevents re-encounter?** — addressed by the synthesis-citation-as-required-language pattern (literal last line of synthesis.md).

## Post-critique recommendation (labeled)

**RECOMMENDATION:** Ship the Step-13 session ledger as candidate-v2 specifies. Concretely:

1. **One new section in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)** — *Ledger schema (load-bearing)* — with HTML-comment marker, paste-and-fill template, four load-bearing headings (`## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`), bypass-case documentation, count-taking-moment definition, and threshold-tuning trigger ("after 5 ledgers").

2. **One new step 13 in [CLAUDE.md](CLAUDE.md)** — names the artifact, references the schema section, defines bypass cases, requires the citation pattern as literal last line of synthesis.

3. **One new "must not do" item in CLAUDE.md** — *"Do not skip the ledger on a non-bypassed session."*

4. **One exemplar ledger** at [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md), derived from the format-only-state-transition-gate session — a real on-disk session whose counts can be verified by inspection.

5. **No script, no hook, no aggregator** — all three are deliberate non-goals. Hook automation is entry #14's territory; aggregator is a separate future entry; the manual paste-and-fill is the day-1 deliverable.

**Total committed surface for this entry:** ~50 README lines + ~20 CLAUDE.md lines + 1 exemplar file + entry-body updates. No new files for ongoing operator work; no retiring of any existing path; no new agent.

## At least three named uncertainties

1. **Orchestrator reliability at end-of-context.** Step 13 happens at the moment the orchestrator is least reliable. Modal failure: ledger.md not written. Mitigation: paste-and-fill is shorter than free-form authorship, but reliability is not eliminated. Flips recommendation if >30% of real non-bypassed sessions skip the ledger — at that point, replace manual authorship with hook automation (depend on #14 landing, or accept obsolescence).

2. **Wallpaper outcome.** Synthesis citation is required language but unchecked. If operators/AI systematically produce malformed citations or no citation at all, the re-encounter surface fails silently. Flips if real sessions show citation drift; mitigation is a tiny grep-check at session close (future entry).

3. **Threshold guesses are off.** 10 / 8 / loop-cap may all be wrong on real distributions. The schema makes thresholds editable in one place, but the *first* 5 sessions will be uncalibrated. If all sessions trigger warnings, warnings become noise; if none trigger, system is silent.

4. **"Decision" definition stability.** Counting bulleted items under Recommendation/Uncertainties depends on synthesis structure not changing. CLAUDE.md step 12 must be edited in lockstep with this definition.

5. **Three ratios may not capture the actual modal failure.** Ashby's-law concern. If the real over-elaboration pattern is "right amount of agents, wrong agents," the ratios are silent on it.

## The cheapest experiment that would reduce the biggest uncertainty

**Uncertainty being reduced:** #1 (orchestrator reliability at end-of-context) — modal failure mode per outside-view.

**Experiment:** ship the entry, then observe the next 3 non-bypassed sessions (which will run on this stack regardless). For each, verify by `find`/`grep`:
- Does `<session-id>/ledger.md` exist?
- Does the last line of `synthesis.md` start with `Ledger: agent-calls=`?
- Are the counts in ledger.md self-consistent with directory contents?

If 3/3 sessions produce conformant ledgers, uncertainty #1 retires; the schema is durable enough to survive end-of-context. If 0–1/3 succeed, the manual-authorship assumption is wrong; escalate to hook plumbing (depend on #14) or accept that this entry's value is conditional on #14 shipping.

Cost: ~zero (the sessions happen anyway; verification is one `find` and one `tail -1`).

## Symmetry worth naming
Like the format-only-state-transition-gate entry, this is **fails-to-safe**: a missing ledger doesn't break any session; the synthesis still ships. The downside is silent — the warning signal is not generated. The bypass-case + count-taking-moment documentation prevents silent-failure-mistaken-for-success.

*(Procedural note before the citation: this synthesis was produced without `Task`-tool access; the agent-calls count reflects orchestrator-authored stand-ins for the subagent returns — see authoring notes inside each distillation/critique file. A real session would show ~7–10 agent calls. The citation line below is the literal required form per [CLAUDE.md](CLAUDE.md) step 12.)*

Ledger: agent-calls=0, artifacts=17, loops=1/2; warnings: none.
