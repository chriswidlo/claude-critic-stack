# Step 12 — experiment-running branch

| Field | Value |
|---|---|
| 📌 **title** | Step 12 — experiment-running branch |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective: *"I never ran the cheapest experiment despite naming it as load-bearing. My own synthesis said 'do the 30-query Haiku-verifier test before building anything.' I had Agent, WebSearch, and WebFetch. I produced more plans instead of running the experiment. The honest version of step 12 would have been: 'the experiment is the next move; want me to run it now?' — not 'here is more architecture.'"* |
| 💡 **essence** | Step 12 currently names "the cheapest experiment that would reduce the biggest uncertainty" as a synthesis deliverable. It is named, not run. Add a branching rule: classify the experiment as `runnable-here / runnable-but-needs-user / not-runnable`. If `runnable-here` and within budget (~20 agent-calls), the orchestrator offers to run it before declaring synthesis closed. The synthesis is provisional until the experiment runs or is explicitly skipped. |
| 🚀 **upgrade** | Naming the experiment becomes inseparable from running the experiment when running is possible. The "I produced more plans instead of running it" failure mode becomes structurally hard. Sessions that name a runnable cheapest-experiment cannot end without the operator either running it or explicitly opting out. |
| 🏷️ **tags** | workflow, synthesis, experiments, follow-through |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The classification](#the-classification)
- [The branching rule](#the-branching-rule)
- [Why this is normal, not no-brainer](#why-this-is-normal-not-no-brainer)

## The classification

When Step 12 names the cheapest experiment, the orchestrator classifies it:

| Classification | Meaning | Action |
|---|---|---|
| **runnable-here** | Tools available (Agent, WebSearch, WebFetch, Bash); no human-in-loop required; estimated under ~20 agent-calls. | Offer to run before closing synthesis. |
| **runnable-but-needs-user** | Requires the user to run something (paste an Anthropic Research output, run a query in their actual repo, install something). | Name what the user has to do explicitly. Synthesis remains provisional until user opts in or out. |
| **not-runnable** | Requires capabilities not present (a paywalled API, a hosted product, human judgment, a long-running experiment). | Name the blocker. Synthesis is final, but explicitly marked "experiment not run; verdict provisional on the named uncertainty." |

The classification is a one-line orchestrator judgment, not a separate agent call.

## The branching rule

Added to CLAUDE.md, in the Step 12 description:

> **12.5. Experiment-execution check.** After naming the cheapest experiment, classify it as `runnable-here / runnable-but-needs-user / not-runnable`. 
> 
> - If `runnable-here`: estimate the agent-call budget. If under ~20, offer the user: *"The experiment is the next move. I can run it now (estimated N agent-calls, ~M minutes). Run, or close synthesis?"* The synthesis is provisional until the user picks.
> - If `runnable-but-needs-user`: name what the user has to do, in one paragraph. The synthesis closes provisionally; the operator decides whether to run.
> - If `not-runnable`: name the blocker explicitly in the synthesis ("this experiment requires X which I cannot do"). Synthesis closes; the named uncertainty stays open.

## Why this is normal, not no-brainer

- The classification logic is simple but the budget estimate is non-trivial: how does the orchestrator estimate agent-call count for an experiment it has named but not run?
- The "offer to run" interaction is real workflow surface — needs an explicit user-confirmation pattern that doesn't currently exist in CLAUDE.md.
- Pairs with the workflow-overdesigns-when-told-to-underdesign entry: the experiment-running branch is partly a counter-bias against the workflow's tendency to substitute more architecture for actual runs.
- The agent-call budget threshold (20) is conjecture; the right number is empirical.

Real value, real but bounded effort. Normal tier.
