# `upgrades/` — R&D lab for `claude-critic-stack`

This folder is the lab. It is the place where profound, novel, and creative ideas about how to elevate the functionality, effectiveness, and accuracy of this repo's AI system are written down — independently of the workflow, independently of any session, with no ceremony beyond what each entry decides for itself.

It is not a backlog. It is not a planning system. It is not a project tracker. It is a **lab notebook tradition**: the place where thinking lives before it knows what it is, and where it can stay long enough to mature, mutate, or be quietly killed.

## Table of contents

- [What goes here](#what-goes-here)
- [How entries are organized — the four tiers](#how-entries-are-organized--the-four-tiers)
- [Required format for every entry](#required-format-for-every-entry)
- [The two prepended tables — meta and state](#the-two-prepended-tables--meta-and-state)
- [The state lifecycle](#the-state-lifecycle)
- [How to add an entry](#how-to-add-an-entry)
- [The `/upgrade` slash command](#the-upgrade-slash-command)
- [Optional writing prompts — shape of thought](#optional-writing-prompts--shape-of-thought)
- [What this folder is not](#what-this-folder-is-not)

---

## What goes here

Anything profound, novel, or creative about how to elevate this AI system. Half-baked is welcome. Wrong is welcome (write the entry, mark the wrongness in the body when it surfaces). Theoretical with no practical follow-through is welcome. Entries by the operator, by the AI, or co-written are all welcome.

What is *not* welcome: routine task tracking, status updates, ephemeral session notes (those go in `.claude/session-artifacts/<id>/`), and ideas that have been fully implemented (those become commits and `CLAUDE.md` updates, not entries here). When in doubt: if it would be interesting to re-read in a year, it belongs here.

## How entries are organized — the four tiers

By the **value-and-scope tier of the upgrade idea**, with explicit boundaries so classification is fast and unambiguous. The point of these tiers is not just to sort entries — it is to **encourage thinking across the full spectrum**. Every tier deserves entries; an empty tier is a signal that thinking has gotten too narrow.

| Tier | What it is | Test | Lives in |
|---|---|---|---|
| 💎 **profound** | A revolutionary insight that would fundamentally change how the system works. Novel — something we genuinely had not considered. | Would I be excited to tell another engineer about this? | `upgrades/profound/` |
| 🚀 **outlandish** | A visionary, ambitious, long-timeline idea. May require significant planning, may be unproven, may be impractical — but exciting. | Is this a months-long project, or an unproven moonshot? | `upgrades/outlandish/` |
| ✅ **no-brainer** | An obvious win. Low effort, uncontroversial value, can be implemented quickly. | Would I implement this immediately if I had 30 minutes? | `upgrades/no-brainer/` |
| 🌿 **normal** | An ordinary creative idea. Modest impact, modest effort. The bread and butter. | None of the above more strongly fits. | `upgrades/normal/` |

**Decision rule for ambiguous cases:**

```
1. Is this revolutionary in its insight or impact?           → profound
2. Else, is the scope/effort large or visionary?             → outlandish
3. Else, is the value obvious and the effort small?          → no-brainer
4. Else                                                       → normal
```

When in doubt between two tiers, default to the lower one. Entries can be promoted via re-tagging if they turn out bigger than expected.

Subfolders are created lazily — `no-brainer/` exists today because the first entry lives there. The other three appear when their first entry lands.

## Required format for every entry

Every entry has the same structural skeleton:

1. **H1 title.**
2. **Meta table** (vertical: field column | value column).
3. **State table** (horizontal: eight states as columns, single row of dates underneath).
4. **Table of contents** (always required, regardless of length).
5. **Body** (free-form prose, beautifully written, with tables / mermaid diagrams / ASCII / emoji-color when they help).

Free-form length. No minimum, no maximum. Real prose, not bullet outlines. Honest about confidence — hedge in words, not in structure.

## The two prepended tables — meta and state

Both tables go immediately after the H1 title, before the TOC. Both are markdown tables (rendered visibly in any renderer, no YAML frontmatter required).

**Meta table** — required fields, vertical (label column | value column):

```markdown
| Field | Value |
|---|---|
| 📌 **title** | <one-phrase title; same as H1> |
| 🎯 **tier** | 💎 profound \| 🚀 outlandish \| ✅ no-brainer \| 🌿 normal |
| 👤 **author** | operator \| ai \| collaborative |
| 📅 **created** | YYYY-MM-DD |
| ⚡ **catalyst** | What triggered this thought — session id, conversation, paper, observation |
| 💡 **essence** | What's profound / novel / valuable about this, in 1–2 sentences |
| 🚀 **upgrade** | How this elevates the AI system in this repo, in 1–2 sentences |
```

Optional rows (append when they help):

```markdown
| 🏷️ **tags** | tag1, tag2 |
| 🔗 **relates_to** | <slug>, <slug> |
```

**State table** — eight states, all listed, horizontal (states as columns, single date row underneath):

```markdown
| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | — | — | — | — | — | — | — |
```

The current state is the **rightmost filled-in column**. Un-reached states show em-dash (`—`). The visual progression reads left-to-right: filled cells are reached states, em-dashes are not yet. You can see from across the room how far along an entry is.

## The state lifecycle

Eight states, each with a color that resembles the state. Most entries never reach `completed`; that's fine. Some entries stop at `created` and stay there; that's also fine. The lifecycle is a *spine* the entry can climb, not a *requirement* it must fulfill.

| Color | State | Meaning |
|---|---|---|
| 🌱 | **created** | The entry exists. Just written down. |
| 🔬 | **spiked** | Someone did exploratory or prototype work — quick probe to see if the idea is viable. |
| 📋 | **prepared** | Detailed enough that next steps are clear. Ready to be acted on or formally proposed. |
| ✅ | **accepted** | Operator has agreed: this is worth pursuing. |
| ⚙️ | **run-through-repo** | The idea was put through the 12-step adversarial-review workflow as a design question. |
| 🔨 | **implemented** | The change is live in the repo (commits, agent updates, schema changes — whatever it took). |
| 💎 | **value-proved** | The implementation has demonstrated value in real sessions. Not just shipped — *worked*. |
| 🏁 | **completed** | Closed. No more action expected. The entry stays as historical record. |

A state is reached by editing the table to fill in the date. There is no automation; it's a manual act of "yes, this happened." If a state is reached out of order (e.g., `implemented` before `accepted` because the operator just did it), fill in both dates honestly — the lifecycle is descriptive, not prescriptive.

If an idea turns out to be wrong or no longer worth pursuing, mark this in prose at the top of the body — the lab is free-form enough to absorb honest negation without needing a `killed` state.

## How to add an entry

1. Pick the tier using the decision rule.
2. Create `upgrades/<tier>/<YYYY-MM-DD>-<short-kebab-slug>.md`. Create the subfolder if it doesn't exist.
3. Add H1 title, meta table, state table (with `created` filled in), TOC, body.
4. Commit.

That's it. No INDEX to update, no lint to run, no schema to ratify, no review to schedule.

## The `/upgrade` slash command

For one-shot capture without ceremony, use `/upgrade <thought>`. The slash command instructs the AI to:

1. Read the input.
2. Decide the tier using the decision rule.
3. Generate the meta-table fields (`catalyst`, `essence`, `upgrade`) from the input + current conversation context.
4. Pick a slug.
5. Generate the state table with `created` filled in.
6. Generate a TOC.
7. Write a beautifully-formatted entry to the right tier folder.
8. Report back what was created.

The operator just dumps the thought; the AI does the formatting and filing. Use this when capture should not have to compete with thinking. Defined at `.claude/commands/upgrade.md`.

Direct file authoring (without the slash command) is also fine — sometimes the operator wants full control, especially for `profound/` and `outlandish/` entries where the prose itself is part of the idea.

## Optional writing prompts — shape of thought

Not required, not classification, but useful when staring at a blank entry and unsure what kind of thing this is. Profound thoughts tend to come in seven shapes. Naming the shape often unlocks the entry:

- 🔍 **observation** — "I noticed X." A pattern, anomaly, signal, or gap.
- 🔄 **reframing** — "We've been seeing this as X; it's actually Y."
- ⚡ **provocation** — "What we're doing is wrong because Y."
- 🌌 **speculation** — "What if X?" An imaginative thought experiment.
- 🧩 **synthesis** — "X and Y are actually the same thing."
- 🛠️ **proposal** — "We should do X."
- 🪞 **reflection** — "Looking back, X happened because Y."

If using a shape helps you write, mention it in the body or as a tag. The shape is a writing tool, not a filing rule.

## What this folder is not

- **Not a backlog.** Entries don't have priority fields. The state lifecycle tracks progress, not urgency.
- **Not a roadmap.** No ordering by sequence. The state of one entry has no relationship to the state of another.
- **Not the workflow's institutional memory.** Memory has a separate home (`memory/`).
- **Not a place for routine notes.** A passing thought from a phone call goes in `pages/`. The lab is for thoughts profound enough to deserve a TOC, the seven meta fields, and the state spine.
