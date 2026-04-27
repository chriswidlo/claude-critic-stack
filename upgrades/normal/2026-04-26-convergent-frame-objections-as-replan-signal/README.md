# Convergent frame objections as replan signal

| Field | Value |
|---|---|
| 📌 **title** | Convergent frame objections as replan signal |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The critic-panel returned three independent `rework` verdicts. Each lens produced a frame-level objection in addition to its lens-specific critique. The three frame objections — *coupling regret not edit regret* (architecture), *detection cost not rollback cost* (operations), *posture choice not content choice* (product) — converged on a single underlying insight: the candidate's frame was the wrong frame. Step 11's decision rule treats `rework` as design-fixable and `reject` as frame-broken. The decision-log noted convergence and chose rewrite anyway because individual fixes were actionable. The rewrite then converged back near the original prior — evidence the rewrite was working around the frame, not within it. |
| 💡 **essence** | Step 11's current rule looks at each verdict in isolation: rework is rewrite; reject is replan. It does not look at the *cross-lens pattern of frame objections*. When three lenses produce frame objections that converge on the same underlying insight, that is a stronger signal than three lenses each producing a different design-fixable critique — and it is currently invisible to the decision rule. |
| 🚀 **upgrade** | A small addition to step 11: before deciding rewrite vs. replan, the orchestrator must summarize the three frame objections in one sentence each and note whether they converge on a shared insight. If yes, treat as `replan` regardless of whether the lens-specific design fixes are individually actionable. The lens vetoes count, but their *collinearity* counts more. |
| 🏷️ **tags** | step-11, critic-panel, decision-rule, frame-veto |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The signal that was lost](#the-signal-that-was-lost)
- [Why convergence matters more than count](#why-convergence-matters-more-than-count)
- [The exact rule](#the-exact-rule)
- [What it would have done in this session](#what-it-would-have-done-in-this-session)

## The signal that was lost

When three independent lenses, each looking through a different frame (structure / operations / product), independently produce frame-level objections that turn out to be the same insight in different vocabulary, that is statistically improbable under the hypothesis that the candidate's frame was correct. It is the panel-equivalent of three independent reviewers all flagging the same omission — strong evidence that something structural is wrong, not that three coincidental small things are wrong.

The current step-11 rule does not see this. It sees three reworks, each with an actionable design fix attached, and routes to rewrite. The convergence is recorded in the critiques.md aggregation but does not change the routing.

## Why convergence matters more than count

Imagine two scenarios:

- **Scenario A**: three reworks, three frame objections that point at three different things ("you ignored cost", "you ignored migration", "you ignored team capacity"). Three separate weaknesses; rewrite covering all three is feasible.
- **Scenario B**: three reworks, three frame objections that point at the same thing ("the regret frame ignores X", "the rollback frame ignores X", "the content frame misses X"). One underlying weakness; rewrite is unlikely to address it because the frame *itself* generated the weakness.

Both produce the same step-11 routing under the current rule. They should not. Scenario B is replan territory — the frame needs to change before the candidate can usefully be rewritten.

The karpathy session was scenario B and was rewritten anyway. The rewrite converged back near the original prior (which was rejecting the frame's premise — adopt nothing — without being able to say "the frame was wrong"). The rewrite worked, in the end, but only by smuggling a frame change into a rewrite slot.

## The exact rule

Append to step 11 in CLAUDE.md:

> Before deciding rewrite vs. replan, write a one-sentence summary of each lens's frame-level objection. If the three summaries reduce to the same underlying insight (different vocabulary, same load-bearing claim), route to `replan` regardless of whether individual lens-specific design fixes are actionable. Convergence is the signal; lens-specific fixes are noise relative to it. Record the convergent insight in `decision-log.md` as the trigger.
>
> If the three summaries point at three distinct insights, the existing rule applies: `rework` if specific and actionable, `replan` if frame-broken.

## What it would have done in this session

Step 11 in this session would have produced:
- architecture frame objection: "regret frame counts file-state regret, not coupling/mental-model regret"
- operations frame objection: "rollback cost is not the binding constraint; detection cost is"
- product frame objection: "this is a posture choice, not a content choice"

One-sentence reduction: *the frame counts the wrong inventory; the binding axis is detection / coupling / posture, not content / rollback.* That is a single insight in three vocabularies.

Under the proposed rule, this would have routed to `replan` — back to step 7 (re-run scope-mapper under a posture-choice frame) or step 8 (re-run frame-challenger). The candidate-v2 would have been written under that frame from the start, instead of being a rewrite that smuggled the new frame in retrospectively.

The end-state would likely have been similar (the workflow converged on "do nothing" anyway), but the path would have been one loop shorter and the synthesis would have been able to label the recommendation as frame-derived rather than as rework-derived.
