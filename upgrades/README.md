# `upgrades/` — R&D lab for `claude-critic-stack`

This folder is the lab. It is the place where profound, novel, and creative ideas about how to elevate the functionality, effectiveness, and accuracy of this repo's AI system are written down — independently of the workflow, independently of any session, with no ceremony beyond what each entry decides for itself.

It is not a backlog. It is not a planning system. It is not a project tracker. It is a **lab notebook tradition**: the place where thinking lives before it knows what it is, and where it can stay long enough to mature, mutate, or be quietly killed.

## What an entry is — and what it is not

An entry is a **seed of thought** — a proposal that someone (operator, AI, or both) thought worth writing down. Filing an entry is a low-ceremony act: any tier, any length, any shape, half-baked welcome, wrong-on-arrival welcome. Authoring is the easy part, and *that is by design* (see [Principles](#principles--encourage-freedom-mind-only-security)).

What an entry is **not**:

- **Not a task.** Filed ≠ to-be-implemented. Most entries should never become commits; the lab's job is to catch the ones that should.
- **Not a decision.** "Someone wrote it down" is not "this is happening." The operator has not agreed by virtue of an entry's existence.
- **Not pre-reviewed.** The author of an entry is the only person who has looked at it at filing time. That view is *one perspective*, not the verdict.
- **Not a backlog item ranked for execution.** No priority field, no scheduling, no due dates. Entries are not work — they are *candidates for work*.

### What turns a seed into a real upgrade

An entry may graduate into a real change to this repo *if and only if* it earns the graduation through the [state lifecycle](#the-state-lifecycle). Each state is an **epistemic checkpoint** that filters a class of failure the prior state cannot see:

- 🔬 **spiked** filters infeasible ideas — does the basic mechanism even work?
- 📋 **prepared** filters misfit, duplication, and wrong-shape implementations — does this entry survive contact with the rest of this repo's primitives, principles, and existing capability?
- ✅ **accepted** filters *"operator does not actually want this as designed"* — an explicit operator decision on the entry as it stands, not on the original idea.
- ⚙️ **run-through-repo** filters design-level critique on the *implementation choices* — the original 12-step (if any) judged the adoption decision; this state judges the implementation.
- 🔨 **implemented** filters bugs and broken builds via real code plus a smoke test.
- 💎 **value-proved** filters *"looked good in design, did not survive contact with use"* — evidence from real workflow runs.
- 🏁 **completed** filters tech-debt-by-omission — residual disagreements either resolved or explicitly closed.

A graduating entry, surfaced through these states, must satisfy in aggregate:

- **Tangible value** — a specific class of failure prevented, work made cheaper, or epistemic gap closed. Not "would be nice."
- **Demonstrably better than the alternatives this repo could choose** — including doing nothing, doing a smaller version, or absorbing this work into an existing entry. The comparator is local to this stack, not the global state of the art.
- **Belongingness in this repo specifically.** The right idea for *this* stack's primitives (canon, outside-view, the critic-panel, the lab itself) and principles (closed-world trust, librarian-first, anti-anchoring). Generic-good-idea is not the same as right-for-here.
- **No better-existing solution.** No subsumption by an existing primitive, no duplication of capability already shipped, no fragmentation of a bigger entry that already contains this proposal as a sub-piece.

### The asymmetry the lab depends on

**Permissive on authoring; disciplined on implementation.** Anyone — operator, AI, future agent — is welcome to file anything. Nobody is welcome to ship without the lifecycle.

Skipping states is not "fast." Each state exists because it filters a failure the prior state cannot see; skipping a state means shipping with that failure class undetected. The lab has documented this anti-pattern in its own entries (`format-only-state-transition-gate`, `casual-output-is-workflow-unprotected`, `subagents-claim-writes-not-on-disk`) — the failures keep recurring because the structural enforcement is still wishful, not real.

## Table of contents

- [What an entry is — and what it is not](#what-an-entry-is--and-what-it-is-not)
- [What goes here](#what-goes-here)
- [Principles — encourage freedom, mind only security](#principles--encourage-freedom-mind-only-security)
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

## Principles — encourage freedom, mind only security

The lab is **deliberately permissive** about *how* an idea is captured. Discipline lives in the filing (the four tiers, the meta + state tables, the slug-naming convention). Authoring is yours. There is no editorial gate on creativity, length, shape, or content. Short ideas don't need padding; long ideas don't need compression. The lab exists to catch things that wouldn't survive a backlog — that means the format must not impose backlog-like constraints.

### Encouraged

- **Any length.** A paragraph is fine. Thirty pages is fine. The idea decides.
- **Any body shape.** Prose, tables, mermaid diagrams, ASCII art, lists, fenced code-for-illustration, embedded images, transcripts, multi-perspective debates, raw thinking. Mix and match. Use what serves the idea.
- **Any content type.** Observations, manifestos, half-baked sketches, fully-formed designs, speculative fiction about the system's future, retrospective notes about why something failed, questions answered by future entries, contradictions left unresolved.
- **Folder-shaped entries.** When a single `.md` isn't enough — when an idea wants supporting data, draft notes, example outputs, screenshots, transcripts, working files — promote the entry to a folder named with the entry's slug. The canonical entry doc lives inside as `<slug>.md`. (Mechanics still being settled — see open lab entries on folder migration.)
- **Wrong, half-baked, speculative, theoretical, embarrassing.** All welcome. Mark wrongness in prose at the top when it surfaces; the entry stays as historical record.
- **Creativity, vision, exploration, novelty.** The lab's purpose. If an idea would feel awkward in a Jira ticket but you'd defend it over a beer, it belongs here.

### The only limits — minimal security boundaries

These exist to protect the repo and its operator. They are not editorial restrictions; they are the lines that exist for everything in this codebase, surfaced here because the lab is permissive on everything else.

- **No malicious-intent information.** No instructions for harming people, exploiting systems for unauthorized access, building weapons, or other clearly harmful content.
- **No executable scripts inside entries.** Code shown for illustration (fenced markdown, clearly non-executable, kept short) is welcome and encouraged. Anything meant to *run* belongs outside the entry — a `bin/` directory, `.claude/session-artifacts/<id>/`, or wherever the repo's existing conventions place it. The entry can link to or describe the script.
- **No dangerous downloads or embedded payloads.** Don't include binaries. If web content is load-bearing for an idea, **prefer linking to it** over copying its content into the entry. Links are auditable; embedded copies aren't.
- **No secrets.** No API keys, tokens, passwords, private credentials, or other anything-confidential. Use `<placeholder>` syntax in examples that need them.
- **No law-breaking content.** Standard disclaimer.

That is the entire restriction list. Everything not on it is allowed and encouraged.

## How entries are organized — the four tiers

By the **value-and-scope tier of the upgrade idea**, with explicit boundaries so classification is fast and unambiguous. The point of these tiers is not just to sort entries — it is to **encourage thinking across the full spectrum**. Every tier deserves entries; an empty tier is a signal that thinking has gotten too narrow.

### The hard rule — categorize by idea-character, never by technology

An idea is a **creative thought about functionality — a logical or behavioral novelty**. Whatever primitives, technologies, or files are needed to realize it are downstream of the idea, not what the idea *is*. Categorizing by primitive (a `hooks/` folder, an `agents/` folder, a `frontmatter-edits/` folder) collapses the space of ideas onto the space of mechanisms and kills creativity at the filing step.

The four tiers below are defined by **the character of the idea**: how revolutionary, how ambitious, how obvious, how ordinary. Two entries that touch the same primitive (e.g., both edit a frontmatter) can land in different tiers; two entries in the same tier can use entirely different primitives. That is the point.

### The four tiers

| Tier | What it is | Test | Lives in |
|---|---|---|---|
| 💎 **profound** | A revolutionary *insight* that would fundamentally change how the system works or how we think about it. Novel — something we genuinely had not considered. The kind of entry whose value is *the seeing*, regardless of effort to act on it. | Would I be excited to tell another engineer about this? Does it shift how I'd evaluate future ideas? | `upgrades/profound/` |
| 🚀 **outlandish** | A visionary, ambitious, long-timeline *bet*. May require significant planning, may be unproven, may be impractical — but exciting. The kind of entry whose value is in the scope of what it would unlock. | Is this a months-long project, or an unproven moonshot? Would I need a roadmap to start? | `upgrades/outlandish/` |
| ✅ **no-brainer** | An obvious *win*. Low effort, uncontroversial value, can be implemented quickly. The kind of entry where hesitation is the only thing keeping it from being done. | Would I implement this immediately if I had 30 minutes and full attention? | `upgrades/no-brainer/` |
| 🌿 **normal** | An ordinary creative *idea*. Modest impact, modest effort, real value. Neither revolutionary nor obvious nor moonshot. The bread and butter. | None of the above more strongly fits, but the idea is worth writing down. | `upgrades/normal/` |

### Decision rule — apply in this order

Run the questions sequentially. Stop at the first `yes`.

```
1. Is the value of this entry primarily an INSIGHT — does it
   change how I'd think about the next idea, regardless of whether
   anyone acts on it?                                          → profound

2. Is the scope a BET larger than I can plan in one sitting —
   months of work, multiple unknowns, or a roadmap to start?   → outlandish

3. Would I IMPLEMENT it right now if I had 30 minutes —
   no design uncertainty, value uncontroversial?               → no-brainer

4. Else — modest creative idea, real value, real bounded work  → normal
```

When in doubt between two tiers, default to the **lower** one (no-brainer over normal, normal over outlandish). Promotion later is cheap; demotion implicitly happens by the entry just sitting at `🌱 created` for a long time.

### What is NOT a valid grouping

Anti-patterns to refuse if the lab grows and someone proposes a re-organization:

- ❌ **Grouping by primitive** — `hooks/`, `slash-commands/`, `agents/`, `bash-scripts/`. Same primitive can serve wildly different ideas.
- ❌ **Grouping by file touched** — `claude-md-edits/`, `settings-json-edits/`. The file is implementation; the idea is what changes.
- ❌ **Grouping by workflow step** — `step-1/`, `step-12/`. The workflow is one application surface; ideas live above it.
- ❌ **Grouping by status** — `done/`, `in-progress/`. The state table already carries this; folder-by-status causes entries to move physically when nothing about the idea changed.

The only valid axis is **idea-character** (the four tiers). Cross-cutting concerns (security, observability, audit) belong in the body or in `tags`, not in folder names.

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

### Required body elements per state

The (forthcoming) `/upgrade advance` subcommand reads this table to know what to check before suggesting advancement to a new state. Each row names one state; the regex is a tolerant pattern matched (case-insensitive, multiline) against the entry body. The check is **advisory, not blocking** — the lifecycle remains descriptive (manual edit always allowed). False positives are friction; false negatives are corruption — patterns intentionally lean tolerant.

<!-- machine-read by the upgrade-transition gate (see upgrades/normal/2026-04-26-format-only-state-transition-gate.md). do not change column count or order. -->

| State | Required body element | Regex |
|---|---|---|
| 🔬 spiked | A heading naming the spike work (e.g. `## Spike`, `## What I tried`, `## Probe`). | `^#+\s+.*(spike\|tried\|probe\|explored)` |
| 📋 prepared | A heading naming the plan (e.g. `## Plan`, `## Next steps`, `## Implementation plan`). | `^#+\s+.*(plan\|next steps\|implementation)` |
| ✅ accepted | A line stating "accepted by" with a date. | `accepted by.*\d{4}-\d{2}-\d{2}` |
| ⚙️ run-through-repo | A session-id reference (matching `YYYY-MM-DD-slug`). | `\d{4}-\d{2}-\d{2}-[a-z0-9-]+` |
| 🔨 implemented | A git short-SHA in the body OR an `implemented_by:` row in the meta table. | `\b[a-f0-9]{7,40}\b\|implemented_by:` |
| 💎 value-proved | A heading naming the evidence (e.g. `## Value evidence`, `## Outcome`, `## Demonstrated`). | `^#+\s+.*(value (proved\|evidence)\|outcome\|demonstrated)` |
| 🏁 completed | A heading naming closure (e.g. `## Closure`, `## Closed`, `## Completed`). | `^#+\s+.*(closure\|closed\|completed)` |

This table is the single source of truth for the gate's checks. To change what a state requires, edit this table — the gate updates next run. If the lifecycle is collapsed (states removed) or extended (states added), update the state-lifecycle table above and this table together.

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
