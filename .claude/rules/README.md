---
paths: ["__placeholder_never_matches_anything__"]
description: HOWTO — not a rule. Documents what this folder is for. The paths glob is intentionally non-matching so this file does not auto-load.
---

# .claude/rules/

**Anthropic-documented slot for topic-scoped instructions.** Empty by design — add a rule here when you have one that genuinely applies only to a subset of paths (e.g., "when editing Python files, do X").

From [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory):

> `.claude/rules/` — Topic-scoped instructions; supports `paths:` frontmatter glob gating.

## What goes here

A `.md` file per rule, with YAML frontmatter declaring a `paths:` glob list. When Claude touches a file matching the glob, the rule is auto-loaded into context for that turn. Path-scoped rules are the documented alternative to bloating root [CLAUDE.md](CLAUDE.md) with rules that don't apply globally.

## When to add one

Concrete trigger: you find yourself writing a rule in CLAUDE.md that begins *"When editing X..."*, *"In Y files..."*, *"For Z components..."*. That's a rule that should live here with a `paths:` gate, not in the always-loaded CLAUDE.md.

## See also

- [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
- [Anthropic — How Claude remembers your project (memory)](https://code.claude.com/docs/en/memory)
