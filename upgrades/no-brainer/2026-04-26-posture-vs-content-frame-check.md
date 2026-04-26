# Posture-vs-content frame check

| Field | Value |
|---|---|
| 📌 **title** | Posture-vs-content frame check |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. Three independent critic lenses (architecture, operations, product) returned `rework` on a candidate that proposed populating the user's empty global CLAUDE.md with 8–15 lines. All three frame objections converged: the question is not *which lines* but *whether this layer should be populated at all*. The empty file was a posture, not a vacancy. |
| 💡 **essence** | When a candidate edits a configuration layer, the frame-challenger should always check whether the layer's current state is itself a deliberate configuration before reasoning about what content should go in it. Empty files are not always empty by accident; vacant slots are not always vacant; defaults left untouched are often the chosen state. The current frame-challenger contract names alternative *frames* but does not name the alternative *that the current state is the correct state*. |
| 🚀 **upgrade** | One sentence added to the `frame-challenger` contract: when the candidate proposes adding to a layer, the challenger must produce one challenge of the form *"the current state of this layer is the correct state — populating it is the change being made, and the user has not asked for it."* Mechanical, repeatable, cheap to apply. |
| 🏷️ **tags** | frame-challenger, discipline, configuration |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The pattern](#the-pattern)
- [Why this is a no-brainer](#why-this-is-a-no-brainer)
- [The exact rule](#the-exact-rule)
- [Where it would not apply](#where-it-would-not-apply)

## The pattern

A surprisingly large class of design questions takes the form *"should we add X to layer Y?"* The default analysis ranks candidate values of X. The unasked question is whether Y's current contents are themselves the right answer.

In the karpathy session, Y was the user's global CLAUDE.md. It was empty. The candidate ranked which 8–15 lines would best fill it. Three critics independently noticed: the empty state was load-bearing. The user has Claude Code installed and has chosen, deliberately or by inertia-that-functions-as-deliberation, to leave the file empty. Populating it was the design change, regardless of which lines went in.

This pattern recurs:
- *"Should we add a hook for X?"* — but is the absence of hooks itself the chosen ergonomic?
- *"Which permission should we add to settings?"* — but is the per-prompt confirmation the chosen friction?
- *"What should the default model be in this skill?"* — but is `inherit` the chosen behavior?

In each case the configuration layer's current state is not a vacuum to be filled; it is a value, often by omission.

## Why this is a no-brainer

The rule is one sentence in one agent's contract. It costs zero per invocation that does not apply (the challenger just notes "current state is empty content, not chosen empty state — the challenge does not bind"). It costs one challenge in the cases where it does apply, which is exactly when the workflow is most likely to ship a thing the user did not ask for.

The cost of *not* having the rule is what happened in this session: one full critic-panel loop spent re-deriving the insight that the lenses had to converge on independently. With the rule, the frame-challenger surfaces it in step 8 and the candidate at step 9 either addresses it or shows why the layer's current state is not load-bearing.

## The exact rule

Append to `frame-challenger.md` instructions:

> If the candidate proposes adding content to, removing content from, or modifying an existing configuration layer (any file, any settings entry, any artifact whose current state has user-visible effect), produce one challenge of the form: *"the current state of this layer is itself a configuration the user has chosen, possibly by deliberate inaction. Populating / changing / removing it is the design change the candidate is making, and the user has not necessarily asked for that change. Confirm intent before treating the layer as a vacant slot."*
>
> The challenge can be retired in the candidate at step 9 by either (a) showing that the user explicitly asked for the layer to be modified, or (b) showing that the current state is provably accidental rather than chosen.

## Where it would not apply

This is a check on configuration layers — files and settings the user owns and has visibility into. It does not apply to internal artifacts the workflow produces (`.claude/session-artifacts/`, distillations, etc.) where the workflow has authority to populate without asking.

It also does not apply to truly fresh layers that the candidate is creating from scratch — but those should be rare; most additions are to existing layers.
