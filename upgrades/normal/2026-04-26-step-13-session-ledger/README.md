# Step 13 — session ledger format

| Field | Value |
|---|---|
| 📌 **title** | Step 13 — session ledger format |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator: *"I don't want to include money estimates. But some kind of summary could be nice, and estimations, but ai usually estimates in human work, but building with ai require different estimation lense."* The workflow ends at Step 12 (synthesis) with no record of *what the session cost in workflow terms* — agent calls, artifacts produced, loops to convergence. Without this, the user has no signal for "is this workflow earning its calls?" |
| 💡 **essence** | A new Step 13 immediately after synthesis: write `session-artifacts/<id>/ledger.md`. Records workflow-cost in AI-native units, not human-time or money: agent calls by type, artifacts produced, loops through critic-panel, distinct decisions made, tool calls by category. From these, derive three ratios: agent-calls-per-decision (analysis density), artifacts-per-decision (paperwork density), loops-to-convergence. Above-threshold values surface as warnings. |
| 🚀 **upgrade** | The workflow gains self-diagnosis. *"Did this session produce more analysis than action?"* becomes a mechanical question with a numerical answer. Sessions where the workflow over-elaborated (the failure mode the workflow-overdesigns entry names) become detectable in the ledger before the operator notices in the synthesis. Pairs with the cross-session memory write to give cross-session continuity. |
| 🏷️ **tags** | workflow, ledger, metrics, self-diagnosis, synthesis |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-04-26 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | — | — |

accepted by operator (auto-mode authorization) on 2026-04-27.

Session id for the run-through: `2026-04-27-step13-ledger-impl`.

## Table of contents

- [The ledger format](#the-ledger-format)
- [The three derived ratios and their thresholds](#the-three-derived-ratios-and-their-thresholds)
- [Why this matters](#why-this-matters)
- [Spike](#spike)
- [Implementation plan](#implementation-plan)
- [Implementation](#implementation)
- [Verified](#verified)
- [Committed](#committed)

## The ledger format

`session-artifacts/<id>/ledger.md`. Written by the orchestrator at Step 13 (after synthesis):

```markdown
# Session ledger — <session-id>

## Counts
- Agent calls: classifier (1), parallel-gather (3), distillations (3), scope-mapper (1), frame-challenger (1), generator (orchestrator), critic-panel rounds (2 × 3 = 6), comparator (0)
- Artifacts produced: requirement.md, frame.md (2 revisions), 3 distillations, scope-map.md, challenges.md, candidate.md (2 versions), 3 critique files × 2 loops = 6, critiques.md, decision-log.md, synthesis.md, ledger.md
- Tool calls: Read (12), Write (8), Bash (2), WebFetch (1)

## Loops
- Critic-panel loops: 2 (cap reached)
- Replans: 1 (loop 1 → loop 2)
- Rewrites: 0

## Decisions made
- 1 decision (the lab design recommendation)
- 5 named uncertainties
- 1 cheapest-experiment named (run, or not)

## Derived ratios
- Agent-calls per decision: 14
- Artifacts per decision: ~22
- Loops to convergence: 2 / 2 (cap)

## Warnings
- ⚠️ Loops-to-convergence at cap. Consider whether the question's framing could have been addressed without two full loops.
- ⚠️ Artifacts-per-decision (22) above threshold (8). Consider whether the synthesis is producing more documentation than action.
```

## The three derived ratios and their thresholds

- **agent-calls-per-decision.** Threshold: ~10. Above means the workflow is producing more analysis than action. Surface as warning.
- **artifacts-per-decision.** Threshold: ~8. Above means paperwork is exceeding decisions. Same warning.
- **loops-to-convergence.** 0 is suspicious (panel always approves — possibly correlated agreement). 1 is healthy. 2+ means the candidate needed real rework.

Thresholds are starting heuristics; the day-90 review of accumulated ledgers should empirically calibrate them.

## Why this matters

This entry's catalyst is the workflow-overdesigns-when-told-to-underdesign profound entry. A ledger that surfaces "this session produced 22 artifacts for 1 decision" gives the operator-and-AI a numerical signal of the over-elaboration the profound entry describes. Without the ledger, that signal is anecdotal; with it, it is mechanical.

The cost is small (orchestrator writes one extra file at Step 13, derived from existing artifacts). The value scales with how often the workflow runs — every session adds a data point to the cross-session pattern.

Pairs with the cross-session memory write (write a one-page session-summary memory at synthesis) so the next session on a similar question has rehydration context, including last time's ledger.

## Spike

A quick probe confirmed the ledger's counts are mechanically derivable from artifacts the workflow already produces:

- The on-disk exemplar session at [.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/](.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/) has 19 markdown files, 2/2 loops (per its [decision-log.md](.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/decision-log.md)), and 1+5=6 decisions in its [synthesis.md](.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/synthesis.md). Agent calls (14) are reconstructable from the agents named in artifact filenames + the standard step sequence.
- A simple `find ... -name '*.md' \| wc -l` plus a `grep "Loops used:" decision-log.md` is enough to populate every load-bearing field. No new tooling required for the day-1 design; hook automation (entry #14) is a strict refinement.

Spike verdict: viable. The ledger format is mechanically computable from the existing artifact tree, so manual paste-and-fill is realistic and a future hook is a strict improvement, not a rescue.

## Implementation plan

Six concrete edits, all small, all reversible:

1. Add a *Ledger schema (load-bearing)* section to [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) with HTML-comment marker, paste-and-fill template, four load-bearing headings, bypass cases, count-taking moment, threshold-tuning trigger.
2. Add Step 13 to [CLAUDE.md](CLAUDE.md), with cross-link to the schema section.
3. Add the synthesis citation requirement to CLAUDE.md step 12 (final line of synthesis.md).
4. Add one new "Things you must not do" item: don't skip the ledger.
5. Update the artifact-tree diagram in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) to include `synthesis.md` and `ledger.md`.
6. Ship one worked exemplar at [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md), derived from the format-only-state-transition-gate session.

Non-goals (deliberately deferred): no script, no aggregator, no hook plumbing. Hook automation is entry #14's territory.

## Implementation

Done in this commit. Files touched:

- [CLAUDE.md](CLAUDE.md) — added Step 13, the synthesis citation requirement at end of Step 12, and the new "must not do" item.
- [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) — added the *Ledger schema (load-bearing)* section with HTML-comment marker, paste-and-fill template, bypass cases, definitions, threshold tuning, citation pattern. Updated the artifact-tree diagram to include `synthesis.md` and `ledger.md`.
- [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md) — new exemplar derived from the format-only-state-transition-gate session.
- [.claude/session-artifacts/2026-04-27-step13-ledger-impl/](.claude/session-artifacts/2026-04-27-step13-ledger-impl/) — the run-through-repo session artifacts (requirement, frame, distillations, scope-map, challenges, candidate v1+v2, critiques, decision-log, synthesis, ledger). The session itself is the first real-use test of the ledger schema (and surfaced one procedural note: write the ledger *after* all other artifacts exist, not before, so its self-reported counts are exact).

Schema choices made explicit in the entry body:

- **Table over prose** for `## Counts` — aggregators key on rows; prose would require parsing.
- **Ratios derived, not stored** — counts are data; ratios are deterministic functions. Storing both invites drift (Wlaschin / illegal-states-unrepresentable).
- **Three thresholds, one location** — 10 / 8 / loop-cap live in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) only. Edit once, every future ledger picks up the change.
- **Synthesis citation as required language** — the final line of synthesis.md must literally start with `Ledger: agent-calls=`. Without enforcement-as-language, citation drift is the modal failure (per outside-view + product critic).

Dependency on entry #14 (hard-gates-as-harness-hooks) named explicitly: if/when #14 lands, hook-emitted counts replace orchestrator-counted files. Schema unchanged; source of counts shifts. This is a strict refinement, not a contract change.

## Verified

Pre-commit coherence checks performed:

- The four load-bearing headings (`## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`) appear identically in (a) the schema template in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md), (b) the exemplar [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md), and (c) the run-through-repo session's [ledger.md](.claude/session-artifacts/2026-04-27-step13-ledger-impl/ledger.md). All three render the same shape.
- The HTML-comment marker on the schema section names the downstream readers (CLAUDE.md step 13, the exemplar) so a future renamer of headings sees the dependency.
- CLAUDE.md step 12 ends with the synthesis-citation requirement before the "Things you must not do" section, and step 13 immediately follows step 12. No section ordering anomaly.
- The cross-link from CLAUDE.md step 13 to the schema section uses a repo-root-relative markdown link ([.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)) per path discipline.
- The "must not do" item is appended to the existing list, not interpolated — keeps existing order stable.
- The artifact-tree diagram in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) now includes `synthesis.md` and `ledger.md`; previously it omitted both.
- The exemplar's counts are independently recomputable: `find .claude/session-artifacts/2026-04-26-format-only-state-transition-gate -name '*.md' -not -name 'ledger.md' \| wc -l` returns 19; `decision-log.md` records "Loops used: 2/2"; the synthesis has 1 recommendation + 5 uncertainties.
- Bypass cases are documented in both the schema section AND CLAUDE.md step 13. The two definitions agree.
- The state table on this entry has 10 columns (created, spiked, prepared, accepted, run-through-repo, implemented, verified, committed, value-proved, completed) — the new 10-state lifecycle, including 🩺 verified and 🔖 committed before the value/completion states. Matches [upgrades/README.md](upgrades/README.md)'s state-lifecycle table.

The ledger schema is unambiguous: definitions for "decision" and "agent call" are explicit, count-taking moment is named, bypass cases are exhaustive (quick-take, pure-factual, all-other-non-bypassed), thresholds live in one place. The exemplar renders correctly against the template. The CLAUDE.md additions sit cleanly between Step 12's synthesis spec and the "Things you must not do" list.

## Committed

Commit `3ecc59a` on branch `worktree-agent-a3a9d5fb`: *"Land step-13-session-ledger: workflow-cost ledger after synthesis"*. Staged via the per-session changes list at [.claude/session-artifacts/2026-04-27-step13-ledger-impl/changes.md](.claude/session-artifacts/2026-04-27-step13-ledger-impl/changes.md) — concurrent-session work on the same worktree was excluded from staging.
