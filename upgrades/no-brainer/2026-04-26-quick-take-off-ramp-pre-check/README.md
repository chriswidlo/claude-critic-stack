# Quick-take off-ramp pre-check

| Field | Value |
|---|---|
| 📌 **title** | Quick-take off-ramp pre-check |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The user's question was a meta-validation: "is your prior writeup optimal?" The orchestrator went straight into the full 12-step workflow. The workflow ran, triple-vetoed a candidate, ran a rewrite, and arrived at "your prior was directionally right with one factual correction." That outcome was visible from inspection within five minutes. The CLAUDE.md off-ramps for `quick-take`, `skip the critic`, and *"factual question — answer directly from canon-librarian"* were not considered before launching. |
| 💡 **essence** | The CLAUDE.md offers explicit off-ramps for cases where the full workflow is overkill. The orchestrator does not consult them as a pre-step; it just defaults to the full workflow whenever the question is non-trivial. There is no friction asking "is this a workflow-shape question or a quick-take-shape question?" before spending 11 steps. |
| 🚀 **upgrade** | One line at the top of the orchestrator's default behavior: *before invoking step 1 (classifier), check explicitly whether the question matches one of the documented off-ramps (quick-take, skip-the-critic, factual-from-canon).* If yes, use it. If no, proceed to step 1. The off-ramps already exist; the missing piece is making the orchestrator look at them by default rather than only when the user invokes them. |
| 🏷️ **tags** | discipline, workflow-routing, off-ramps |
| 🔗 **relates_to** | 2026-04-26-meta-validation-lacks-prior-was-right-output |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The asymmetry](#the-asymmetry)
- [Why this is a no-brainer](#why-this-is-a-no-brainer)
- [What the pre-check should ask](#what-the-pre-check-should-ask)
- [Why this won't fix everything](#why-this-wont-fix-everything)

## The asymmetry

The workflow's hard gates ("don't proceed without scope-map and challenges") are well-codified — the orchestrator will refuse to skip them. The workflow's exits are not — the off-ramps live in CLAUDE.md as conditional permissions ("if the user says X, then Y is allowed") rather than as default checks the orchestrator runs every time.

This produces an asymmetric default: when in doubt, run the full workflow. The expensive choice is the unflagged choice.

The karpathy session is the cheap example: meta-validation question, prior was likely right, full workflow ran anyway, ended where the user could have ended in five minutes. The expensive examples are the ones nobody notices — every casual question that gets escalated to the workflow because no one stopped to ask whether it should be.

## Why this is a no-brainer

The off-ramps are already written. The classifier already exists. Adding one explicit pre-step — *"check the off-ramp conditions before invoking step 1"* — does not change any agent, does not change any artifact, does not change the workflow's contract. It is a one-paragraph addition to the orchestrator's default behavior.

The savings are bounded but real: every question that should have been a quick-take but wasn't, gets cheaper. The cost is one read-and-decide per invocation, which is rounding error.

## What the pre-check should ask

Before invoking the classifier, the orchestrator should answer three questions explicitly:

1. **Is this a factual question** ("what does the CAP theorem say", "how does X work")? If yes — bypass the workflow, route directly to canon-librarian.
2. **Did the user ask for a quick take?** If the prompt contains "quick", "tldr", "short answer", "off the cuff", or otherwise signals the user wants velocity over rigor — invoke the quick-take exit.
3. **Is this a meta-validation of a prior in this conversation?** If the user is asking "was that right" rather than "what should I do" — strongly consider the quick-take exit, or the (proposed) `meta-validation` mode. Do not default to full workflow.

If all three answer no, proceed to step 1.

## Why this won't fix everything

The orchestrator can still be wrong about which question shape it is looking at. A meta-validation that *should* trigger the full workflow (because the prior was actually wrong on multiple load-bearing points) could be off-ramped by mistake.

But the failure mode of "off-ramped a question that needed the workflow" is recoverable — the user can re-ask with more substance and the orchestrator can route through. The failure mode of "ran the full workflow on a quick-take question" is a session of process for an answer that was already cheap, which is exactly the karpathy session's shape.

Asymmetric error costs justify asymmetric default. Right now the default is "run the workflow." Make it "run the workflow unless one of the documented off-ramps applies."
