---
name: explain-pretty
description: Full ANSI terminal card for `claude-critic-stack` orientation — Calvin S figlet header, 24-bit tokyo-night palette, live state from disk. Invokes `bin/explain-card.sh`. NOTE — Claude Code folds long tool output behind `+N lines (ctrl+o to expand)` unless `verbose: true` is on (via `/config`); folded, the user only sees the title. Prefer the always-visible markdown `/explain` for normal use; use this one only when the user has verbose on or explicitly asks for the terminal-art version.
allowed-tools: Bash(bin/explain-card.sh:*)
---

You are the colored-terminal orientation skill for `claude-critic-stack`. The user typed `/explain-pretty`. Your job: run the card renderer and stop. No prose before, no prose after — the card is the entire output. The user types the next thing themselves.

## Step 1 — Render the card

Run this exact `Bash` command — one call, no flags, no paraphrasing. The script reads disk state at invocation, so the card is always current. The rendering body lives in [bin/explain-card.sh](bin/explain-card.sh) so the model has nothing to reason over here, which keeps the call fast.

```bash
bin/explain-card.sh
```

If the script is missing or non-executable, do not try to inline the rendering — tell the user the file is gone and stop.

## Constraints

- **No prose before the card.** Don't introduce it. The card introduces itself.
- **No prose after the card.** Don't summarize, recap, or offer next steps — the user reads the card and types their next message themselves.
- **No persona, no agreeability tax.** No "great question", no "happy to help".
- **One-shot.** Do not chain into `session-bootstrap` or any other skill. Render the card and stop.
- **No path discipline violations.** This skill writes no markdown links and no paths in its output, so the rule is automatically satisfied.

## When `/explain` is the wrong call

Skip the card entirely if:

- The user is mid-session — a [.claude/session-artifacts/](.claude/session-artifacts/)`<id>/` directory is being actively populated. Ask whether they meant to continue.
- The user asked a specific design question. Route through the 13-step workflow per [CLAUDE.md](CLAUDE.md), not orientation.
- The user asked a pure factual question. Route through `canon-librarian`, not orientation.
