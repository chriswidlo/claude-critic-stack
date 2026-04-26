# Meta-validation lacks a "prior-was-right" output mode

| Field | Value |
|---|---|
| 📌 **title** | Meta-validation lacks a "prior-was-right" output mode |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The user asked the workflow to validate a casual prior writeup about a community plugin. The workflow ran end-to-end, the panel triple-vetoed the first candidate, the rewrite converged back near the original prior with **one** factual correction. The honest answer was "your prior was directionally right; here's the one fact you got wrong." But the workflow's structure forced the synthesis to keep producing action items — an A/B to run, a posture choice to confirm, hedges to remember. The user-facing output is heavier than the actual delta warrants. |
| 💡 **essence** | When the workflow is invoked on a prior decision (meta-validation), the most honest possible output is often "the prior stands; correction is X." The workflow has no clean output mode for that — its synthesis template demands a recommendation, named uncertainties, an experiment to run. So even when the right delta is one corrected sentence, the user receives a multi-section synthesis that *looks* like new direction. |
| 🚀 **upgrade** | A `meta-validation` mode (or a synthesis variant) where the headline is "your prior holds, with corrections" rather than "here's a new recommendation." The full workflow still runs (and should run — it's what catches the corrections), but the output mode shifts: surface the corrections at the top, downgrade the action set, name when "do nothing further" is the actual deliverable. |
| 🏷️ **tags** | meta, workflow-output, synthesis, anti-patterns |
| 🔗 **relates_to** | 2026-04-26-workflow-overdesigns-when-told-to-underdesign |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What was observed](#what-was-observed)
- [Why this is structural](#why-this-is-structural)
- [What a meta-validation mode could look like](#what-a-meta-validation-mode-could-look-like)
- [Relation to the existing over-design entry](#relation-to-the-existing-over-design-entry)
- [Open questions](#open-questions)

## What was observed

The user asked: "run this through this repo to decide if your writeup and plan is optimal." The workflow ran end-to-end on a prior writeup that recommended (1) don't install the karpathy-skills plugin, (2) most of its content duplicates Claude Code defaults, (3) optionally drop a line into the user's global CLAUDE.md, (4) the plugin packaging mechanism is the more interesting lesson.

The workflow surfaced one real correction: the prior assumed the user's global `CLAUDE.md` was already populated with content; Explore showed it is empty (0 bytes). That single fact made one specific claim in the prior wrong.

The workflow then triple-vetoed a second-pass candidate that over-corrected on the new fact ("populate the empty file with 8–15 lines"), converged back near the original prior, and produced a synthesis with: a labeled post-critique recommendation, three named uncertainties, an A/B experiment, a posture-choice question handed back to the user.

Net actionable delta for the user: one fact correction, plus a one-hour optional A/B if they want certainty. The synthesis around it is ten times longer.

## Why this is structural

The synthesis template (`/CLAUDE.md` step 12) requires:
- The classifier label and the alternative.
- The reframe.
- The reference-class forecast.
- Canon passages, supporting and contradicting.
- The scope-map summary.
- The frame-level challenge and how the recommendation addresses it.
- The post-critique recommendation, explicitly labeled.
- At least three named uncertainties.
- The cheapest experiment that would reduce the biggest uncertainty.

Every one of those sections must be filled. There is no clause in the template that says: "if the post-critique recommendation is a small correction to a prior, surface that and shrink the rest." So even when the workflow's actual finding is "your prior holds, with one correction," the synthesis pads it out to look like a fresh recommendation.

This is downstream of the same structural bias the `workflow-overdesigns-when-told-to-underdesign` entry names — every workflow step is incentivized to add structure; nothing is incentivized to recognize when the right answer is small.

The meta-validation case is sharper because the bias has a specific symptom (action items manufactured to fill template slots) that the user can see: they asked "is my writeup optimal?" and got back a multi-section synthesis instead of a yes/no/with-corrections.

## What a meta-validation mode could look like

Three candidates, increasing in invasiveness:

1. **Synthesis-template variant.** When the prior workflow input *is* a prior recommendation (detected by the classifier — `investigation` label was the alternative classification in this session), the synthesis template shrinks: headline = "prior verdict + corrections"; the canon/scope-map/forecast/uncertainties become a collapsible "audit trail" rather than the body. Same workflow, different output mode.

2. **A `prior-was-right` first-class verdict at step 12.** Synthesis must answer one question before proceeding: *did the workflow change the prior's direction, or only refine it?* If the latter, surface the refinement as the headline and bury the rest. Mechanically: a header sentence that reads "Direction: confirmed / corrected / overturned."

3. **Classifier change.** Add `meta-validation` as a primary label. When chosen, the workflow runs the same steps but the synthesis is contractually different — it must produce a verdict on the prior, not a recommendation in its own right.

Each is small. The pattern being mitigated is structural: the workflow currently has no way to tell the user "we ran the full process and the conclusion is your hunch was right" without it sounding like a new conclusion.

## Relation to the existing over-design entry

The profound entry `2026-04-26-workflow-overdesigns-when-told-to-underdesign` named the general bias: every workflow step adds structure; nothing recognizes when austerity is the right answer.

This entry names a specific manifestation of that bias — meta-validation specifically. The general entry's proposed fixes (minimalist lens, smallest-possible-answer frame, pre-synthesis "could this be 10% of itself" check) would partially help here too. But meta-validation has its own honest answer ("your prior holds") that the general fixes do not directly produce — they would still generate a recommendation, just a smaller one.

So: this is a normal-tier addition that the profound entry does not subsume.

## Open questions

- Is meta-validation common enough to warrant its own mode, or rare enough that a one-off note in the synthesis template is sufficient?
- Does the bias toward "fresh recommendation in the output" come from the synthesis template specifically, or from the orchestrator's instinct to demonstrate work? The template change would not fix the latter.
- If the workflow can return "prior-was-right" as a clean verdict, does that create a new failure mode — orchestrators returning that verdict to avoid hard recommendations?
- Should the same shape apply when the workflow is run on someone *else's* prior recommendation (a PR review, a proposal from a colleague)? Probably yes, but the social dynamics are different — "your prior holds" reads differently when the prior is your own vs. a stakeholder's.
