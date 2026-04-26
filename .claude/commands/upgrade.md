---
description: Capture a profound, novel, or creative idea for upgrading this AI system into the upgrades/ R&D lab — fast, formatted, filed.
argument-hint: <the thought, in any form — a sentence, a paragraph, a half-baked idea>
---

You are the operator's lab assistant. The user has invoked `/upgrade` with input. Your job is to capture that input as a properly-formatted entry in the `upgrades/` R&D lab at the root of `claude-critic-stack`.

The user's input: $ARGUMENTS

(If `$ARGUMENTS` is empty or unclear, ask one clarifying question, then proceed once you have enough.)

## Your task

1. **Read the lab spec.** Read `upgrades/README.md` for the tier definitions, required format, meta table fields, and state lifecycle. Read `upgrades/no-brainer/2026-04-26-rnd-lab.md` for the canonical example of a well-formed entry.

2. **Decide the tier.** Use the decision rule:
   - 💎 **profound** — revolutionary insight, would fundamentally change the system, novel
   - 🚀 **outlandish** — visionary, ambitious, long timeline, large planning surface
   - ✅ **no-brainer** — obvious value, low effort, would implement in 30 minutes
   - 🌿 **normal** — ordinary creative idea, modest impact, modest effort
   When in doubt, default downward.

3. **Generate the meta-table fields.** All seven required, plus optional `tags` / `relates_to` if they help:
   - `title` — what this entry is, in a phrase. Specific, not generic.
   - `tier` — the tier you decided (with emoji prefix matching the table in the README).
   - `author` — `operator`, `ai`, or `collaborative`.
   - `created` — today's date (YYYY-MM-DD).
   - `catalyst` — what triggered this thought. Cite the conversation, session id, observation, paper, anything that grounds the entry in its origin moment.
   - `essence` — the punchline. What's profound, novel, or valuable about this idea, in 1–2 sentences.
   - `upgrade` — how this elevates the AI system in this repo, in 1–2 sentences.

4. **Pick a slug.** Format: `<YYYY-MM-DD>-<short-kebab-slug>`. The slug should be 2–5 words capturing the entry's identity. Filename will be `<slug>.md`.

5. **Generate the state table.** All eight states listed; only `🌱 created` has a date (today); all others show `—`:

   ```markdown
   | State | Reached |
   |---|---|
   | 🌱 created | YYYY-MM-DD |
   | 🔬 spiked | — |
   | 📋 prepared | — |
   | ✅ accepted | — |
   | ⚙️ run-through-repo | — |
   | 🔨 implemented | — |
   | 💎 value-proved | — |
   | 🏁 completed | — |
   ```

6. **Generate a TOC.** Even short entries get one. The TOC names the sections, which forces the entry to be structured enough to be re-read.

7. **Write the entry body.** Beautifully written prose. Real sentences, not bullet outlines. Tables, mermaid diagrams, ASCII diagrams, or emoji-color when they genuinely help. Honest about confidence — hedge in words, not in structure. Length is whatever the idea earns.

8. **Write the file.** Create `upgrades/<tier>/<slug>.md`. Create the tier subfolder if it doesn't exist.

9. **Report back.** Tell the user: the path written, the tier chosen (and why if non-obvious), the title, and one-sentence essence. Keep this under 100 words.

## Required entry skeleton

Every entry must follow this exact skeleton, in this exact order:

```markdown
# <H1 title>

| Field | Value |
|---|---|
| 📌 **title** | <title> |
| 🎯 **tier** | <emoji> <tier-name> |
| 👤 **author** | <operator|ai|collaborative> |
| 📅 **created** | YYYY-MM-DD |
| ⚡ **catalyst** | <one-paragraph catalyst> |
| 💡 **essence** | <1–2 sentence essence> |
| 🚀 **upgrade** | <1–2 sentence upgrade> |

(Append optional rows 🏷️ **tags** and/or 🔗 **relates_to** below the meta table when they help.)

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | — | — | — | — | — | — | — |

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
- **Do not invent additional state values.** The eight states are fixed: `created`, `spiked`, `prepared`, `accepted`, `run-through-repo`, `implemented`, `value-proved`, `completed`. New entries always start at `created` only.
- **Do not skip the TOC** even for short entries. Three sections is fine; zero sections is not.
- **Do not file in the wrong tier just because it's the easier folder.** If the entry is genuinely profound, file it as profound.
- **Do not write the entry to anywhere other than `upgrades/<tier>/`.** Not to session-artifacts, not to memory, not to canon. The lab is the lab.

## When the input is ambiguous

If the input is too short to determine tier, essence, or upgrade — ask one question. Examples:
- "What's the upgrade — how would the system get better if this is right?" (when the input names an observation but no consequence)
- "Is this a quick fix or a months-long arc?" (when the scope is unclear between no-brainer and outlandish)
- "Are you proposing this as a change, or noticing it as a pattern?" (when shape is unclear)

One question, then proceed. Do not interrogate the operator into rewriting their thought.
