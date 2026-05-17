---
name: upgrade
description: Capture a profound, novel, or creative idea for upgrading this AI system into the garden/ R&D lab — fast, formatted, filed. Invoke as `/upgrade <thought>`. Use when the operator wants to capture an R&D idea without leaving the current session. SKIP for routine task tracking, status updates, or ideas already fully implemented (those become commits, not entries).
argument-hint: <the thought, in any form — a sentence, a paragraph, a half-baked idea>
allowed-tools: Bash(date:*) Bash(mkdir:*) Bash(ls:*) Bash(cat:*) Read Write
---

You are the operator's lab assistant. The user has invoked `/upgrade` with input. Your job is to capture that input as a properly-formatted entry in the `garden/` R&D lab at the root of `claude-critic-stack`.

The user's input: $ARGUMENTS

(If `$ARGUMENTS` is empty or unclear, ask one clarifying question, then proceed once you have enough.)

## Your task

1. **Read the lab spec.** Read `garden/README.md` for the category definitions, the 2×2 operational test, required format, meta table fields, and state lifecycle. Read `garden/volunteer/2026-04-26-rnd-lab/README.md` for the canonical example of a well-formed entry.

2. **Decide the category.** Run the decision rule sequentially; stop at first `yes`. Cross-check against the 2×2 (insight axis × scope axis) — both must agree, and if they disagree the cascade wins.
   - 🌹 **heirloom** — reframes thinking; value is the seeing itself, regardless of action
   - 🌳 **specimen** — long-timeline ambitious bet; months of work, roadmap required to start
   - 🍀 **volunteer** — obvious, would implement in 30 minutes, uncontested value
   - 🌿 **perennial** — modest creative work, real value, bounded scope (the default)
   When in doubt between two adjacent cells, default to the **smaller scope** (volunteer over perennial, perennial over specimen).

3. **Generate the meta-table fields.** All seven required, plus optional `tags` / `relates_to` if they help:
   - `title` — what this entry is, in a phrase. Specific, not generic.
   - `category` — the category you decided (with emoji prefix matching the table in `garden/README.md`).
   - `author` — `operator`, `ai`, or `collaborative`.
   - `created` — today's date (YYYY-MM-DD).
   - `catalyst` — what triggered this thought. Cite the conversation, session id, observation, paper, anything that grounds the entry in its origin moment.
   - `essence` — the punchline. What's profound, novel, or valuable about this idea, in 1–2 sentences.
   - `upgrade` — how this elevates the AI system in this repo, in 1–2 sentences.

4. **Pick a slug.** Format: `<YYYY-MM-DD>-<short-kebab-slug>`. The slug should be 2–5 words capturing the entry's identity. The slug becomes the entry's folder name; the doc inside is named `README.md`.

5. **Generate the state table.** All ten states listed horizontally as columns, with a single date row underneath; only `🌱 created` has a date (today); all others show `—`:

   ```markdown
   | 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
   |---|---|---|---|---|---|---|---|---|---|
   | YYYY-MM-DD | — | — | — | — | — | — | — | — | — |
   ```

6. **Generate a TOC.** Even short entries get one. The TOC names the sections, which forces the entry to be structured enough to be re-read.

7. **Write the entry body.** Beautifully written prose. Real sentences, not bullet outlines. Tables, mermaid diagrams, ASCII diagrams, or emoji-color when they genuinely help. Honest about confidence — hedge in words, not in structure. Length is whatever the idea earns.

8. **Write the file.** Create `garden/<category>/<slug>/README.md`. The entry is a folder named with the slug; the canonical doc inside is `README.md`. All four category subfolders already exist; do not create new ones.

9. **Report back.** Tell the user: the path written, the category chosen (and why if non-obvious), the title, and one-sentence essence. Keep this under 100 words.

## Required entry skeleton

Every entry must follow this exact skeleton, in this exact order:

```markdown
# <H1 title>

| Field | Value |
|---|---|
| 📌 **title** | <title> |
| 🎯 **category** | <emoji> <category-name> |
| 👤 **author** | <operator|ai|collaborative> |
| 📅 **created** | YYYY-MM-DD |
| ⚡ **catalyst** | <one-paragraph catalyst> |
| 💡 **essence** | <1–2 sentence essence> |
| 🚀 **upgrade** | <1–2 sentence upgrade> |

(Append optional rows 🏷️ **tags** and/or 🔗 **relates_to** below the meta table when they help.)

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | — | — | — | — | — | — | — | — | — |

## Table of contents

- [Section A](#section-a)
- [Section B](#section-b)
...

## Section A

<body prose>

## Section B

<body prose>
```

## Constraints

- **Do not invoke other agents.** This is a one-shot capture, not a workflow. Read the spec, format, write, report.
- **Do not over-engineer the entry.** Match length to input depth. If the operator wanted a 5,000-word position paper, they would have written it themselves.
- **Do not use YAML frontmatter.** The lab uses visible markdown tables. Do not prepend a `---` block.
- **Do not invent additional state values.** The ten states are fixed: `created`, `spiked`, `prepared`, `accepted`, `run-through-repo`, `implemented`, `verified`, `committed`, `value-proved`, `completed`. New entries always start at `created` only.
- **Do not skip the TOC** even for short entries. Three sections is fine; zero sections is not.
- **Do not file in the wrong category just because it's the easier folder.** If the entry is genuinely heirloom (reframes thinking), file it as heirloom even when the implementation looks small.
- **Do not write the entry to anywhere other than `garden/<category>/<slug>/README.md`.** Not to session-artifacts, not to memory, not to canon. The garden is the garden. Folder shape is the canonical convention; do not write flat `<slug>.md` files.

## When the input is ambiguous

If the input is too short to determine category, essence, or upgrade — ask one question. Examples:
- "What's the upgrade — how would the system get better if this is right?" (when the input names an observation but no consequence)
- "Is this a quick fix or a months-long arc?" (when the scope is unclear between volunteer and specimen)
- "Are you proposing this as a change, or noticing it as a pattern?" (when shape is unclear — proposal-shape suggests volunteer/perennial; reframing-shape suggests heirloom)

One question, then proceed. Do not interrogate the operator into rewriting their thought.
