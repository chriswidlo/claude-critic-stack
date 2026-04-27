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

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The ledger format](#the-ledger-format)
- [The three derived ratios and their thresholds](#the-three-derived-ratios-and-their-thresholds)
- [Why this matters](#why-this-matters)

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
