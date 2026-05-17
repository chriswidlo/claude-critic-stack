# `garden/` — R&D lab for `claude-critic-stack`

This folder is the garden. It is the place where profound, novel, and creative ideas about how to elevate the functionality, effectiveness, and accuracy of this repo's AI system are written down — independently of the workflow, independently of any session, with no ceremony beyond what each entry decides for itself.

It is not a backlog. It is not a planning system. It is not a project tracker. It is a **lab notebook tradition**: the place where thinking lives before it knows what it is, and where it can stay long enough to mature, mutate, or be quietly killed.

## What an entry is — and what it is not

An entry is a **seed of thought** — a proposal that someone (operator, AI, or both) thought worth writing down. Filing an entry is a low-ceremony act: any category, any length, any shape, half-baked welcome, wrong-on-arrival welcome. Authoring is the easy part, and *that is by design* (see [Principles](#principles--encourage-freedom-mind-only-security)).

What an entry is **not**:

- **Not a task.** Filed ≠ to-be-implemented. Most entries should never become commits; the garden's job is to catch the ones that should.
- **Not a decision.** "Someone wrote it down" is not "this is happening." The operator has not agreed by virtue of an entry's existence.
- **Not pre-reviewed.** The author of an entry is the only person who has looked at it at filing time. That view is *one perspective*, not the verdict.
- **Not a backlog item ranked for execution.** No priority field, no scheduling, no due dates. Entries are not work — they are *candidates for work*.

### What turns a seed into a real upgrade

An entry may graduate into a real change to this repo *if and only if* it earns the graduation through the [state lifecycle](#the-state-lifecycle). Each of the ten states is an **epistemic checkpoint** that filters a class of failure the prior state cannot see:

- 🌱 **created** marks the entry's existence — captured before it can be lost.
- 🔬 **spiked** filters infeasible ideas — does the basic mechanism even work?
- 📋 **prepared** filters misfit, duplication, and wrong-shape implementations — does this entry survive contact with the rest of this repo's primitives, principles, and existing capability?
- ✅ **accepted** filters *"operator does not actually want this as designed"* — an explicit operator decision on the entry as it stands, not on the original idea.
- ⚙️ **run-through-repo** filters design-level critique on the *implementation choices* — the original 13-step (if any) judged the adoption decision; this state judges the implementation.
- 🔨 **implemented** filters bugs and broken builds via real code plus a smoke test.
- 🩺 **verified** filters local-OK-but-globally-broken — no broken refs, no stale paths, no doc-implementation drift, no contradictions with sibling artifacts.
- 🔖 **committed** filters work-on-disk-but-not-in-git — commit SHA recorded; the implementation is reproducible.
- 💎 **value-proved** filters *"looked good in design, did not survive contact with use"* — evidence from real workflow runs.
- 🏁 **completed** filters tech-debt-by-omission — residual disagreements either resolved or explicitly closed.

A graduating entry, surfaced through these states, must satisfy in aggregate:

- **Tangible value** — a specific class of failure prevented, work made cheaper, or epistemic gap closed. Not "would be nice."
- **Demonstrably better than the alternatives this repo could choose** — including doing nothing, doing a smaller version, or absorbing this work into an existing entry. The comparator is local to this stack, not the global state of the art.
- **Belongingness in this repo specifically.** The right idea for *this* stack's primitives (canon, outside-view, the critic-panel, the garden itself) and principles (closed-world trust, librarian-first, anti-anchoring). Generic-good-idea is not the same as right-for-here.
- **No better-existing solution.** No subsumption by an existing primitive, no duplication of capability already shipped, no fragmentation of a bigger entry that already contains this proposal as a sub-piece.

### The asymmetry the garden depends on

**Permissive on authoring; disciplined on implementation.** Anyone — operator, AI, future agent — is welcome to file anything. Nobody is welcome to ship without the lifecycle.

Skipping states is not "fast." Each state exists because it filters a failure the prior state cannot see; skipping a state means shipping with that failure class undetected. The garden has documented this anti-pattern in its own entries (`format-only-state-transition-gate`, `casual-output-is-workflow-unprotected`, `subagents-claim-writes-not-on-disk`) — the failures keep recurring because the structural enforcement is still wishful, not real.

## Table of contents

- [What an entry is — and what it is not](#what-an-entry-is--and-what-it-is-not)
- [What goes here](#what-goes-here)
- [Principles — encourage freedom, mind only security](#principles--encourage-freedom-mind-only-security)
- [How entries are organized — the four categories](#how-entries-are-organized--the-four-categories)
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

The garden is **deliberately permissive** about *how* an idea is captured. Discipline lives in the filing (the four categories, the meta + state tables, the slug-naming convention). Authoring is yours. There is no editorial gate on creativity, length, shape, or content. Short ideas don't need padding; long ideas don't need compression. The garden exists to catch things that wouldn't survive a backlog — that means the format must not impose backlog-like constraints.

### Encouraged

- **Any length.** A paragraph is fine. Thirty pages is fine. The idea decides.
- **Any body shape.** Prose, tables, mermaid diagrams, ASCII art, lists, fenced code-for-illustration, embedded images, transcripts, multi-perspective debates, raw thinking. Mix and match. Use what serves the idea.
- **Any content type.** Observations, manifestos, half-baked sketches, fully-formed designs, speculative fiction about the system's future, retrospective notes about why something failed, questions answered by future entries, contradictions left unresolved.
- **Folder-shaped entries (the canonical shape).** Every entry is a folder named with its slug; the canonical doc inside is `README.md`. Supporting artifacts (transcripts, prototypes, sample outputs, draft notes, working files, sub-folders) live alongside — the entry's `README.md` documents what's there. The folder is yours to organize.
- **Wrong, half-baked, speculative, theoretical, embarrassing.** All welcome. Mark wrongness in prose at the top when it surfaces; the entry stays as historical record.
- **Creativity, vision, exploration, novelty.** The garden's purpose. If an idea would feel awkward in a Jira ticket but you'd defend it over a beer, it belongs here.

### The only limits — minimal security boundaries

These exist to protect the repo and its operator. They are not editorial restrictions; they are the lines that exist for everything in this codebase, surfaced here because the garden is permissive on everything else.

- **No malicious-intent information.** No instructions for harming people, exploiting systems for unauthorized access, building weapons, or other clearly harmful content.
- **No executable scripts inside entries.** Code shown for illustration (fenced markdown, clearly non-executable, kept short) is welcome and encouraged. Anything meant to *run* belongs outside the entry — a `bin/` directory, `.claude/session-artifacts/<id>/`, or wherever the repo's existing conventions place it. The entry can link to or describe the script.
- **No dangerous downloads or embedded payloads.** Don't include binaries. If web content is load-bearing for an idea, **prefer linking to it** over copying its content into the entry. Links are auditable; embedded copies aren't.
- **No secrets.** No API keys, tokens, passwords, private credentials, or other anything-confidential. Use `<placeholder>` syntax in examples that need them.
- **No law-breaking content.** Standard disclaimer.

That is the entire restriction list. Everything not on it is allowed and encouraged.

## How entries are organized — the four categories

By the **value-and-scope character of the entry**, with explicit operational tests so categorization is fast, unambiguous, and deterministic across sessions. The point of these categories is not just to sort entries — it is to **encourage thinking across the full spectrum**. Every category deserves entries; an empty category is a signal that thinking has gotten too narrow.

### The hard rule — categorize by idea-character, never by technology

An idea is a **creative thought about functionality — a logical or behavioral novelty**. Whatever primitives, technologies, or files are needed to realize it are downstream of the idea, not what the idea *is*. Categorizing by primitive (a `hooks/` folder, an `agents/` folder, a `frontmatter-edits/` folder) collapses the space of ideas onto the space of mechanisms and kills creativity at the filing step.

The four categories below are defined by **the character of the idea**: how revolutionary, how ambitious, how obvious, how ordinary. Two entries that touch the same primitive (e.g., both edit a frontmatter) can land in different categories; two entries in the same category can use entirely different primitives. That is the point.

### The four categories

| Category | What it is | Lives in |
|---|---|---|
| 🌹 **heirloom** | A reframing whose value is *the seeing itself*. An entry that shifts how we'd evaluate the next idea, regardless of whether anyone acts on it. The kind of entry you'd want to tell another engineer about, regardless of whether anything ships from it. | `garden/heirloom/` |
| 🌳 **specimen** | A long-timeline ambitious bet — months of work, multiple unknowns, a roadmap to start. Value is in the *scope of what successful realization would unlock*. The demanding featured plant: talk of the season if it survives. | `garden/specimen/` |
| 🍀 **volunteer** | Obvious, low-effort, uncontroversial. Would be implemented immediately given 30 minutes of focused attention. Hesitation is the only thing keeping it from being done — like a tomato that volunteers in last year's bed: you'd be silly not to keep it. | `garden/volunteer/` |
| 🌿 **perennial** | Modest creative work with real value and real bounded scope. Neither revolutionary nor obvious — the reliable backbone that runs the garden. Returns every year. The bread-and-butter. | `garden/perennial/` |

### Operational test — the 2×2

Every entry sits in exactly one cell. **Two axes**:

- **Insight axis** — does the entry reframe how we think, or work within the current frame?
- **Scope axis** — is the realization small/quick, or large/long-timeline?

|  | **Small scope / quick** | **Large scope / long-timeline** |
|---|---|---|
| **Reframes how we think** | 🌹 **heirloom** | 🌳 **specimen** |
| **Incremental — within current frame** | 🍀 **volunteer** | 🌿 **perennial** |

### Decision rule — apply in this order

Run sequentially. Stop at the first `yes`. The cascade and the 2×2 must agree; if they disagree the entry is borderline and the **cascade wins** (it tests the load-bearing question first).

```
1. Is the value of this entry primarily a REFRAMING — does it
   change how I'd think about the next idea, regardless of whether
   anyone acts on it?                                          → heirloom

2. Is the scope a BET larger than I can plan in one sitting —
   months of work, multiple unknowns, or a roadmap to start?   → specimen

3. Would I IMPLEMENT it right now if I had 30 minutes —
   no design uncertainty, value uncontroversial?               → volunteer

4. Else — modest creative idea, real value, real bounded work  → perennial
```

When in doubt between two adjacent cells, default to the **smaller scope** category (volunteer over perennial, perennial over specimen). Promotion later is cheap; demotion implicitly happens by the entry just sitting at `🌱 created` for a long time.

### Per-category operational tests

Each category names a 1-sentence definition, a "fits" example, a "doesn't fit" example, and the disambiguation rule against its nearest neighbor. These are the **deterministic criteria** — an AI sorting an entry must apply them, not guess.

#### 🌹 heirloom

- **Definition:** A reframing whose value is in the seeing itself. The entry shifts how we'd evaluate the next idea, regardless of whether we act on it.
- **Fits:** [`r-and-d-lab-thesis`](garden/heirloom/2026-04-27-r-and-d-lab-thesis/README.md) — names that the garden's graduation gates silently appeal to an unwritten thesis. The seeing IS the contribution; whether the `THESIS.md` ever lands is downstream.
- **Doesn't fit:** A reframe that comes packaged with a 30-minute fix — if the fix is the load-bearing part, file as `volunteer` and note the reframe in the body.
- **Disambiguation vs. specimen:** Heirloom value lives in the *seeing*. Specimen value lives in the *building that follows from the seeing*. Test: *would you write this entry even knowing nobody will ever act on it?* Yes → heirloom. Only-as-a-roadmap → specimen.

#### 🌳 specimen

- **Definition:** A long-timeline ambitious bet. Months of work, multiple unknowns, a roadmap required before work can start. Value is in the scope of what successful realization unlocks.
- **Fits:** [`scope-projector-capability`](garden/specimen/2026-04-26-scope-projector-capability/README.md) — a future-projection agent that extrapolates any proposal to its mature form. Long horizon, real unknowns, would unlock a new step in the workflow.
- **Doesn't fit:** Something whose implementation plan you can write today and start tomorrow. That's a `perennial`.
- **Disambiguation vs. perennial:** Specimen requires a roadmap before work can start. Perennial can be planned in one sitting. Crisp test: *could you write the implementation plan today and start building tomorrow?* No → specimen. Yes → perennial (regardless of total duration).

#### 🍀 volunteer

- **Definition:** Obvious, low-effort, uncontroversial. Would be implemented immediately given 30 minutes of focused attention. Hesitation is the only thing keeping it from being done.
- **Fits:** [`tighten-run-through-repo-regex`](garden/volunteer/2026-04-26-tighten-run-through-repo-regex/README.md) — a single regex tightening on the state-transition gate. Clear, bounded, uncontested.
- **Doesn't fit:** Anything where the value is contested or the design is uncertain. If you find yourself writing arguments in the entry body, it's not a volunteer.
- **Disambiguation vs. perennial:** Volunteer is *uncontested*. Perennial is *contested-but-bounded* — real design choices, real tradeoffs, but bounded work. Test: *would two reasonable people disagree on whether this should be done?* No → volunteer. Yes → perennial.

#### 🌿 perennial

- **Definition:** Modest creative work with real value and real bounded scope. Neither revolutionary nor obvious — the workhorse category that holds the garden together.
- **Fits:** [`three-layer-security-module`](garden/perennial/2026-04-26-three-layer-security-module/README.md) — three-layer security design. Real design tradeoffs, real value, bounded work; not revolutionary insight, not a multi-month moonshot.
- **Doesn't fit:** Anything trivial enough to ship in 30 minutes (file as `volunteer`) or anything requiring months and a roadmap (file as `specimen`).
- **Disambiguation:** Perennial is the *default*. If you've ruled out heirloom (no reframing), specimen (no roadmap needed), and volunteer (not 30-min trivial), it's perennial.

### What is NOT a valid grouping

Anti-patterns to refuse if the garden grows and someone proposes a re-organization:

- ❌ **Grouping by primitive** — `hooks/`, `slash-commands/`, `agents/`, `bash-scripts/`. Same primitive can serve wildly different ideas.
- ❌ **Grouping by file touched** — `claude-md-edits/`, `settings-json-edits/`. The file is implementation; the idea is what changes.
- ❌ **Grouping by workflow step** — `step-1/`, `step-13/`. The workflow is one application surface; ideas live above it.
- ❌ **Grouping by status** — `done/`, `in-progress/`. The state table already carries this; folder-by-status causes entries to move physically when nothing about the idea changed.

The only valid axis is **idea-character** (the four categories). Cross-cutting concerns (security, observability, audit) belong in the body or in `tags`, not in folder names.

## Required format for every entry

Every entry has the same structural skeleton:

1. **H1 title.**
2. **Meta table** (vertical: field column | value column).
3. **State table** (horizontal: ten states as columns, single row of dates underneath).
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
| 🎯 **category** | 🌹 heirloom \| 🌳 specimen \| 🍀 volunteer \| 🌿 perennial |
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

**State table** — ten states, all listed, horizontal (states as columns, single date row underneath):

```markdown
| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | — | — | — | — | — | — | — | — | — |
```

The current state is the **rightmost filled-in column**. Un-reached states show em-dash (`—`). The visual progression reads left-to-right: filled cells are reached states, em-dashes are not yet. You can see from across the room how far along an entry is.

## The state lifecycle

Ten states, each with a color that resembles the state. Most entries never reach `completed`; that's fine. Some entries stop at `created` and stay there; that's also fine. The lifecycle is a *spine* the entry can climb, not a *requirement* it must fulfill.

| Color | State | Meaning |
|---|---|---|
| 🌱 | **created** | The entry exists. Just written down. |
| 🔬 | **spiked** | Someone did exploratory or prototype work — quick probe to see if the idea is viable. |
| 📋 | **prepared** | Detailed enough that next steps are clear. Ready to be acted on or formally proposed. |
| ✅ | **accepted** | Operator has agreed: this is worth pursuing. |
| ⚙️ | **run-through-repo** | The idea was put through the 13-step adversarial-review workflow as a design question. |
| 🔨 | **implemented** | The work is done — code edits, agent updates, schema changes complete in the working tree. Not yet verified globally, not yet in git. |
| 🩺 | **verified** | The implementation has been globally checked: no broken refs, no stale paths, no doc-implementation drift, no contradictions with sibling artifacts. Coherence verified before commit. |
| 🔖 | **committed** | The implementation is in git: commit SHA(s) recorded in entry body or `committed_in:` meta field; commit message references the entry's slug; the agent's per-session change list (see [Per-session change tracking](#per-session-change-tracking) below) was scoped to own-session work only. |
| 💎 | **value-proved** | The implementation has demonstrated value in real sessions. Not just shipped — *worked*. |
| 🏁 | **completed** | Closed. No more action expected. The entry stays as historical record. |

### Per-session change tracking

Before advancing to 🔖 committed, the session that performed the implementation maintains an explicit running list at `.claude/session-artifacts/<id>/changes.md`. One line per file touched: `<verb> <path>` where verb is `created` / `modified` / `renamed` / `deleted`. Updated by the agent as it works — not at the end. Reasons:

- **File-based, not memory-based** — context can be cleared, compacted, or rerouted; a list that lives only in conversation context vanishes mid-work.
- **Auditable** — the list can be diffed against `git status` to verify "I claim I touched these paths; let's see if reality agrees."
- **Hookable** — a `PreToolUse` or `PostToolUse` hook can append to it automatically when files are written.
- **Scopes `git add`** — the discipline at 🔖 committed is `git add` only paths from this list. Never `git add -A` or `git add .`. This prevents accidentally committing concurrent-session work.

The convention is named here as part of the garden's lifecycle. It naturally extends to any session that commits, not just garden-modifying sessions; promotion to a workflow-wide CLAUDE.md instruction is a separate future entry.

A state is reached by editing the table to fill in the date. There is no automation; it's a manual act of "yes, this happened." If a state is reached out of order (e.g., `implemented` before `accepted` because the operator just did it), fill in both dates honestly — the lifecycle is descriptive, not prescriptive.

If an idea turns out to be wrong or no longer worth pursuing, mark this in prose at the top of the body — the garden is free-form enough to absorb honest negation without needing a `killed` state.

### Required body elements per state

The (forthcoming) `/upgrade advance` subcommand reads this table to know what to check before suggesting advancement to a new state. Each row names one state; the regex is a tolerant pattern matched (case-insensitive, multiline) against the entry body. The check is **advisory, not blocking** — the lifecycle remains descriptive (manual edit always allowed). False positives are friction; false negatives are corruption — patterns intentionally lean tolerant.

<!-- machine-read by the upgrade-transition gate (see garden/perennial/2026-04-26-format-only-state-transition-gate/README.md). do not change column count or order. -->

| State | Required body element | Regex |
|---|---|---|
| 🔬 spiked | A heading naming the spike work (e.g. `## Spike`, `## What I tried`, `## Probe`). | `^#+\s+.*(spike\|tried\|probe\|explored)` |
| 📋 prepared | A heading naming the plan (e.g. `## Plan`, `## Next steps`, `## Implementation plan`). | `^#+\s+.*(plan\|next steps\|implementation)` |
| ✅ accepted | A line stating "accepted by" with a date. | `accepted by.*\d{4}-\d{2}-\d{2}` |
| ⚙️ run-through-repo | A session-id reference (matching `YYYY-MM-DD-slug`). | `\d{4}-\d{2}-\d{2}-[a-z0-9-]+` |
| 🔨 implemented | A heading naming the implementation work (e.g. `## Implementation`, `## Implemented`, `## What was done`). | `^#+\s+.*(implementation\|implemented\|what was done\|what changed)` |
| 🩺 verified | A heading naming the verification (e.g. `## Verified`, `## Pre-commit review`, `## Coherence check`, `## Global review`). | `^#+\s+.*(verified\|verification\|pre-commit review\|coherence check\|global review)` |
| 🔖 committed | A git short-SHA in the body OR a `committed_in:` row in the meta table. | `\b[a-f0-9]{7,40}\b\|committed_in:` |
| 💎 value-proved | A heading naming the evidence (e.g. `## Value evidence`, `## Outcome`, `## Demonstrated`). | `^#+\s+.*(value (proved\|evidence)\|outcome\|demonstrated)` |
| 🏁 completed | A heading naming closure (e.g. `## Closure`, `## Closed`, `## Completed`). | `^#+\s+.*(closure\|closed\|completed)` |

This table is the single source of truth for the gate's checks. To change what a state requires, edit this table — the gate updates next run. If the lifecycle is collapsed (states removed) or extended (states added), update the state-lifecycle table above and this table together.

## How to add an entry

1. Pick the category using the [decision rule](#decision-rule--apply-in-this-order) — cross-check against the [2×2](#operational-test--the-2x2).
2. Create `garden/<category>/<YYYY-MM-DD>-<short-kebab-slug>/README.md`. The entry is a folder named with the slug; the canonical doc inside is `README.md`. All four category subfolders exist; pick the one your decision-rule answer landed in.
3. Add H1 title, meta table, state table (with `created` filled in), TOC, body to that `README.md`.
4. Commit.

That's it. No INDEX to update, no lint to run, no schema to ratify, no review to schedule.

**Why folder + README.md.** Every entry is a folder so it has room to grow supporting artifacts (transcripts, prototypes, sample outputs, draft notes — see [Principles](#principles--encourage-freedom-mind-only-security)). The doc inside is named `README.md` so GitHub auto-renders it when the folder is opened on the web, and so `find` / autocomplete behave predictably. Other files in the entry's folder are supporting material, organized however the entry decides — the entry's `README.md` documents what's there.

## The `/upgrade` slash command

For one-shot capture without ceremony, use `/upgrade <thought>`. The slash command instructs the AI to:

1. Read the input.
2. Decide the category using the decision rule and the 2×2 cross-check.
3. Generate the meta-table fields (`catalyst`, `essence`, `upgrade`) from the input + current conversation context.
4. Pick a slug.
5. Generate the state table with `created` filled in.
6. Generate a TOC.
7. Write a beautifully-formatted entry to the right category folder.
8. Report back what was created.

The operator just dumps the thought; the AI does the formatting and filing. Use this when capture should not have to compete with thinking. Defined at [.claude/skills/upgrade/SKILL.md](.claude/skills/upgrade/SKILL.md).

The verb `/upgrade` is kept (rather than renamed to `/garden` or `/plant`) because the underlying act is *upgrading the AI system* — the folder is `garden/` because that names the holding-place; the verb describes the aspiration. The two carry different work.

Direct file authoring (without the slash command) is also fine — sometimes the operator wants full control, especially for `heirloom/` and `specimen/` entries where the prose itself is part of the idea.

## Optional writing prompts — shape of thought

When you're starting a new entry and don't know what *kind* of thought you're capturing, picking a shape often unlocks the writing. This is an **optional writing aid** — not a filing axis (that's the category folder), not a maturity tracker (that's the state lifecycle). Most entries can be written without ever consulting this list; the list exists for the moment you're stuck.

R&D entries take recurring shapes that draw from three rigorous traditions — **Bruner's epistemic stance** (paradigmatic vs. narrative), **Peirce's inferential moves** (abduction / induction / deduction), and **Searle's speech-act theory** (assertive / directive / commissive / expressive / declarative). The eight shapes below are a practitioner amalgam, not a formal taxonomy. Use them as **generative prompts** when staring at a blank file, not as classification rules to apply after the fact.

Engineering doc traditions (PEP, RFC, ADR) classify by *intent / stage / subsystem* because they coordinate action across teams. The garden classifies by *shape of thought* because it is **upstream of commitment** — most entries here will never ship, and the writing-aid value is in the moment of capture.

- 🔍 **observation** — "I noticed X." A pattern, anomaly, signal, or gap.
- 🔄 **reframing** — "We've been seeing this as X; it's actually Y."
- ⚡ **provocation** — "What we're doing is wrong because Y."
- 🌌 **speculation** — "What if X?" An imaginative thought experiment.
- 🧩 **synthesis** — "X and Y are actually the same thing."
- 🛠️ **proposal** — "We should do X." (The garden's modal shape — ~69% of entries.)
- 🪞 **reflection** — "Looking back, X happened because Y." Includes retrospectives — the entry IS the historical record of work already shipped.
- 📊 **audit** — "I systematically surveyed X; here's what the survey shows." Distinct from observation: audits enumerate ≥N items, often spawning sub-entries.

If using a shape helps you write, mention it in the body. The shapes are **invitations** — the rare ones (provocation, speculation, synthesis) are kept here even when uncommonly used, so the garden's voice doesn't self-censor those modes. The shape is a writing tool, never a filing rule.

## What this folder is not

- **Not a backlog.** Entries don't have priority fields. The state lifecycle tracks progress, not urgency.
- **Not a roadmap.** No ordering by sequence. The state of one entry has no relationship to the state of another.
- **Not the workflow's institutional memory.** Cross-session memory lives in the user's machine-local Claude Code auto-memory store (described in prose, not as a path, per the path-discipline rule in [CLAUDE.md](CLAUDE.md) §"Path discipline").
- **Not a place for routine notes.** The garden is for thoughts profound enough to deserve a TOC, the seven meta fields, and the state spine.
