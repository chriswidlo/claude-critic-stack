---
name: explain
description: On-demand orientation for `claude-critic-stack`. Runs `bin/explain-render.sh` and emits the bordered ASCII card it prints, wrapped in a plain code fence. Use when the user types `/explain` or asks a what-is-this / what-can-I-do-here question without naming a specific design problem. SKIP when the user is mid-session, asked a specific design question (route through the 13-step workflow), or asked a factual question (route to canon-librarian). For the 24-bit ANSI terminal-art version, use `/explain-pretty`.
allowed-tools: Bash(bin/explain-render.sh:*)
---

Run `bin/explain-render.sh`. Emit its stdout verbatim inside a plain ` ``` ` fence (no language tag). Below the fence, exactly one italic line:

`*Type /explain-pretty for the 24-bit ANSI terminal-art version.*`

No prose before, no prose after. The card is the entire output. Layout, copy, and live counts all live in the renderer — to change anything, edit `bin/explain-render.sh`, not this file.
