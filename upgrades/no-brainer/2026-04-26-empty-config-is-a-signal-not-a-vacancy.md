# Empty config is a signal, not a vacancy

| Field | Value |
|---|---|
| 📌 **title** | Empty config is a signal, not a vacancy |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. Explore found the global `CLAUDE.md` was 0 bytes. The orchestrator's scope-mapper labeled it "vacant slot — not a primitive, nothing to subsume / replace / extend / conflict with." That labeling treated the empty state as nothingness. The product critic later flagged this: *the empty file is a deliberate product configuration, not vacant real estate*. The labeling shaped every downstream step until the critic caught it. |
| 💡 **essence** | The scope-mapper's vocabulary (subsume, replace, extend, conflict) does not have a word for *the current state is the chosen state*. Empty files, missing configurations, absent hooks — these get labeled as gaps rather than as configurations-by-omission. The labeling is silent and load-bearing: once "vacant", the slot is treated as something to fill. |
| 🚀 **upgrade** | A fifth label for the scope-mapper: `**preserve-as-empty**` (or `preserve-as-default`). Applies when an existing primitive is in its initial / default / empty state and the user has not signaled intent to change it. Forces the candidate at step 9 to either justify the change of state or treat the slot as occupied. Mechanical, additive, cheap. |
| 🏷️ **tags** | scope-mapper, vocabulary, configuration-as-signal |
| 🔗 **relates_to** | 2026-04-26-posture-vs-content-frame-check |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The labeling failure](#the-labeling-failure)
- [Why a fifth label, not just better prose](#why-a-fifth-label-not-just-better-prose)
- [The label's contract](#the-labels-contract)
- [Adjacent applications](#adjacent-applications)

## The labeling failure

The scope-mapper's existing labels (`subsume`, `replace`, `extend`, `conflict`) all assume the existing primitive *has content* against which the new requirement can be related. When the existing primitive is empty — a 0-byte CLAUDE.md, an unset env var, a missing hook — none of the labels fit cleanly. The mapper's actual response in the karpathy session was to invent a non-label: "n/a — vacant slot — nothing to subsume / replace / extend / conflict with."

That non-label is a category error. The slot is not "nothing." It is "deliberately empty." Those are different states with different implications:
- "Nothing here, fill it" → adding content is uncontroversial; user wanted the slot used.
- "Deliberately empty, leave it" → adding content is a posture change; user did not ask.

The mapper currently cannot distinguish them, so it routes both into "vacant" and the candidate at step 9 inherits the "fill it" disposition.

## Why a fifth label, not just better prose

Better prose in the rationale column would not have caught this. The rationale column already said "empty file is a vacant slot." The label *is* the load-bearing carrier. Without a labeled state for "preserve-as-empty," the candidate gets no clean way to honor the empty-as-chosen possibility.

A label is also a flagging mechanism for downstream steps: the frame-challenger can check whether any preserved-as-empty primitives exist and apply the posture-vs-content frame check; the critics can challenge candidates that overrule a `preserve-as-empty` without explicit user permission.

## The label's contract

Append to `scope-mapper.md`:

> **`preserve-as-empty`** — applies when an existing primitive is in its initial, default, or empty state, and there is no signal that the user has asked for the state to change. The label is stronger than `extend` and weaker than `conflict`: it asserts that the primitive's current state is itself the chosen configuration, and that any candidate that changes the state must justify the change as a deliberate user-facing posture shift, not as a gap-fill.
>
> Common cases: empty CLAUDE.md files, empty `installed_plugins.json`, missing global skills directory, unset env vars whose absence has user-visible effect, hooks that are notably absent.
>
> The label is *not* applied when the primitive is empty due to a preceding step (e.g., the file was just deleted) or when the user has explicitly asked for the slot to be populated.

## Adjacent applications

The same label resolves adjacent confusions:
- A repo with no `tests/` directory: gap, or chosen testing strategy?
- A settings file with default values throughout: unconfigured, or trust-defaults posture?
- An agent set with no critic hooks: missing observability, or chosen lightness?

In each case, the label `preserve-as-empty` (or `preserve-as-default`) gives the workflow a clean way to say "noted, not changing" rather than implicitly defaulting to "fill it."
