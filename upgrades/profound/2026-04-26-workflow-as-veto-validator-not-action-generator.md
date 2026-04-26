# Workflow as veto-validator, not action-generator

| Field | Value |
|---|---|
| 📌 **title** | Workflow as veto-validator, not action-generator |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. Three lenses returned `rework` on the first candidate. The rewrite produced a candidate that explicitly recommended *do nothing* (with a small correction). The workflow's strongest, most decisive output was a refusal — a rejection of two consecutive candidates' drift toward action. The workflow's weakest output was the synthesis, which had to manufacture an action item ("optionally run an A/B") to fill the template. The shape of value was: rejection-strong, generation-weak. |
| 💡 **essence** | The 12-step workflow is currently shaped as an action-generator: classifier → reframe → gather → scope-map → challenge → generate → critique → synthesize-recommendation. The shape implies the deliverable is a recommendation. But the workflow's actual high-value output across many sessions is *veto* — the panel kills bad candidates, the frame-challenger kills bad frames, the scope-mapper kills false greenfield. Shaping the workflow as an action-generator wastes the rejection-strength: every veto is followed by a forced generation that may have nothing useful to add. |
| 🚀 **upgrade** | A second workflow shape: `validate-mode`. Same agents, different output contract. The deliverable is a verdict on a presented candidate (or a presented prior, or a presented decision-in-flight) — not a fresh recommendation. The synthesis becomes "your candidate stands / your candidate is wrong on these axes / your frame is wrong, here is the better frame." Action items are optional and absent by default. The workflow stops manufacturing value where it has none and lets the rejection be the value. |
| 🏷️ **tags** | workflow-shape, modes, value-attribution, meta |
| 🔗 **relates_to** | 2026-04-26-meta-validation-lacks-prior-was-right-output, 2026-04-26-workflow-overdesigns-when-told-to-underdesign |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [Where the workflow's value actually comes from](#where-the-workflows-value-actually-comes-from)
- [The shape mismatch](#the-shape-mismatch)
- [Two modes, same agents](#two-modes-same-agents)
- [The validate-mode contract](#the-validate-mode-contract)
- [What this changes about how the user invokes the workflow](#what-this-changes-about-how-the-user-invokes-the-workflow)
- [Risks and resistance](#risks-and-resistance)

## Where the workflow's value actually comes from

Look at what the workflow does well across sessions:
- The classifier surfaces an alternative label — usually a better one — and the orchestrator notices the user's framing was too narrow. **Value: a frame veto.**
- Outside-view kills inside-view enthusiasm with a base rate. **Value: a confidence veto.**
- Canon-librarian returns contradicting passages, forcing the candidate to address counter-evidence. **Value: a one-sided-evidence veto.**
- Scope-mapper finds existing primitives the candidate ignored. **Value: a false-greenfield veto.**
- Frame-challenger names alternative frames. **Value: a frame-lock veto.**
- The critic panel returns rework / reject. **Value: a candidate veto.**

The pattern is consistent. The workflow's high-value outputs are vetos. Generations — the post-critique candidate, the synthesis recommendation — are downstream artifacts that may or may not have content beyond "what survived the vetos."

## The shape mismatch

The workflow's documented contract (CLAUDE.md step 12 synthesis) requires:
- a labeled post-critique recommendation
- at least three named uncertainties
- the cheapest experiment to reduce the biggest uncertainty

Each of these is a *generation* artifact. None of them allow "your candidate was right; nothing to add" or "your candidate was wrong; here is what was wrong; no replacement offered" to be the headline. The shape forces the workflow to produce action even when its actual finding is "no action."

This is the shape mismatch. The workflow's strength is veto. The workflow's required output is generation. So every workflow run that produced a strong veto then has to invent a generation to fit the template. Sometimes the invented generation is fine (small correction, useful suggestion). Sometimes it is structural padding around a verdict the synthesis cannot say plainly.

The karpathy session is one example. Two candidates, both effectively vetoed back to the original prior. The synthesis manufactured "optionally run an A/B" as the action item because the template demanded one. The actual value of the session was the veto; the action item was decoration.

## Two modes, same agents

The proposal is not to replace the workflow. It is to add a second mode that uses the same agents under a different output contract:

| | **generate-mode (current)** | **validate-mode (proposed)** |
|---|---|---|
| Input | a design question, no candidate | a candidate (or prior, or in-flight decision) |
| Steps 1–8 | as documented | as documented |
| Step 9 | orchestrator generates candidate | orchestrator restates the user's candidate without modification |
| Step 10 | panel critiques the orchestrator's candidate | panel critiques the user's candidate |
| Step 11 | rewrite-vs-replan as documented | rewrite-vs-replan rerouted to the user, not to the orchestrator |
| Step 12 | recommendation + uncertainties + experiment | verdict + corrections + frame challenge if any. No required experiment, no manufactured action. |

The agents do not change. The artifacts on disk do not change. Only the synthesis contract changes — and the orchestrator's role at step 9 (passive restatement instead of active generation).

## The validate-mode contract

The synthesis under validate-mode reads like a verdict, not a recommendation:

```
## Verdict on the candidate

Direction: confirmed | corrected | overturned

If confirmed: the candidate stands. The workflow caught no load-bearing errors. <list any minor refinements>.
If corrected: the candidate stands with the following corrections: <list>. The corrections are not new direction; they are repairs to the candidate's premises.
If overturned: the candidate's frame or central claim is wrong. <state the better frame or claim>. The user must decide whether to revise the candidate or abandon it.

## Frame challenge (if any)
## Named uncertainties (if any)
## Suggested experiment (optional, only if the user explicitly asks)
```

Three sections marked optional. Three sections marked "if any." The synthesis can be five lines. The synthesis is allowed to be five lines.

## What this changes about how the user invokes the workflow

Currently the user opens the workflow by asking a design question. The orchestrator generates everything from scratch.

Under validate-mode, the user opens the workflow by presenting a candidate: *"I'm thinking about doing X. Here's my reasoning. Validate."* Or: *"Here's a writeup I produced. Tell me if it's right."* Or: *"I'm about to commit to Y. Catch problems."*

This is a different shape of invocation. It maps cleanly onto:
- PR review (the candidate is the PR)
- Design-doc review (the candidate is the doc)
- Meta-validation of a prior (the candidate is the prior reply)
- Pre-commit gut-check on a decision-in-flight

All of these are real use cases the workflow currently handles awkwardly because they have to be coerced into "design question shape" to fit the generate-mode contract.

## Risks and resistance

- **Risk**: validate-mode lets the orchestrator off the hook for hard recommendations. The orchestrator can always say "your candidate is fine" when generating one would be the more honest output.
  - *Mitigation*: validate-mode requires the panel to actively critique. The orchestrator does not generate the candidate, so it cannot bias toward approval. If the candidate is bad, the panel says so.
- **Risk**: the line between generate-mode and validate-mode is fuzzy. Many user inputs have a partial candidate inside a partial design question.
  - *Mitigation*: the classifier already does this disambiguation. Add a mode-detection step: did the user present a candidate, or did they ask the orchestrator to produce one?
- **Risk**: validate-mode encourages the user to anchor on their own candidates rather than ask open questions.
  - *Mitigation*: this is real, but the user already does this; validate-mode just admits it openly. Better to validate honestly than to coerce candidate-presentations into open-question shape.

The deeper resistance is that validate-mode admits the workflow's value is rejection. Calling it that out loud feels like a downgrade — the workflow stops being a Rolls-Royce design-generation pipeline and becomes a heavyweight critic. But that may be what it actually is, and admitting it lets the workflow stop pretending otherwise.
