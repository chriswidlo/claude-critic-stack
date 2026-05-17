---
name: explain
description: On-demand orientation for `claude-critic-stack`. Emits a bordered ASCII card (Calvin S figlet title centered in a rounded box, four divider-separated sections — HOW IT WORKS, WAYS TO ASK, WHAT'S LOADED, RENAME SHORTLIST — with live disk-state counts) as the assistant's message text. No color tricks, no language-fence hacks; clean monospace layout with `╭─╮ │ ├─┤ ╰─╯` box-drawing. Always visible inline in Claude Code chat, no fold, no verbose flag. Use when the user types `/explain` or asks a what-is-this / what-can-I-do-here / how-do-I-use-this question without naming a specific design problem. SKIP when the user is already mid-session, asked a specific design question (route through the 13-step workflow instead), or asked a factual question (route to canon-librarian). For the 24-bit ANSI terminal-art version, use `/explain-pretty`.
allowed-tools: Bash(bin/explain-render.sh:*)
---

You are the orientation skill for `claude-critic-stack`. The user typed `/explain`. Your job: run the card renderer once, then emit its stdout verbatim wrapped in a plain code fence as your assistant message. No prose before, no prose after — the card is the entire output.

## Step 1 — Render the card

Run this single Bash call. The script reads live disk state and prints a single bordered ASCII card to stdout.

```bash
bin/explain-render.sh
```

## Step 2 — Emit the output wrapped in a plain code fence

Take the stdout from Step 1 verbatim (preserving every space) and emit it inside a plain ` ``` ` code fence (no language tag — we deliberately want NO syntax highlighting since the layout is the design). Below the fence, exactly one italic CTA line:

````
```
{verbatim stdout from Step 1}
```

*Type `/explain-pretty` for the 24-bit ANSI terminal-art version.*
````

## Why this approach

**Layout, not color.** After 13 iterations chasing color via fence-language hacks (yaml/python/bash/toml), every approach traded coherence for color or vice versa. v14 surrenders color entirely and commits to clean monospace layout with box-drawing borders. The card reads like a card because it IS one — bordered, sectioned, breathing.

**The renderer owns alignment.** Hand-counted box borders never align in practice. `bin/explain-render.sh` uses Python with Unicode-width awareness (`unicodedata.east_asian_width`) to pad every line to a precise 66-char inner width. Borders align by construction.

**Single source of truth.** Live counts come from `bin/explain-render.sh` (which also embeds them). Numbers are real-time; layout is hardcoded in the renderer. To change copy or layout, edit the renderer — not this skill body.

## Constraints

- **No prose before the card.** The card introduces itself.
- **No prose after the card** beyond the single italic CTA.
- **No persona, no agreeability tax.** No "great question", no "happy to help".
- **One-shot.** Do not chain into `session-bootstrap` or any other skill.
- **No path discipline violations.** The skill writes no markdown links and no paths in its output, so the rule is automatically satisfied.

## When `/explain` is the wrong call

Skip the card entirely if:

- The user is mid-session — a [.claude/session-artifacts/](.claude/session-artifacts/)`<id>/` directory is being actively populated. Ask whether they meant to continue.
- The user asked a specific design question. Route through the 13-step workflow per [CLAUDE.md](CLAUDE.md), not orientation.
- The user asked a pure factual question. Route through `canon-librarian`, not orientation.
