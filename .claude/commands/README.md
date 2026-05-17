---
description: NOT A COMMAND — guard file. Do not invoke. .claude/commands/ is the legacy directory; create new commands as skills under .claude/skills/<name>/SKILL.md instead.
disable-model-invocation: true
---

# .claude/commands/ — DO NOT ADD FILES HERE

**This folder is the legacy form of Claude Code commands. The forward-canonical form is skills.**

Anthropic explicitly merged commands into skills ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)):

> *"Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way... Skills add optional features: a directory for supporting files, frontmatter to control whether you or Claude invokes them, and the ability for Claude to load them automatically when relevant."*

## STOP — if you came here to add a new command

**Don't.** Go to [.claude/skills/](.claude/skills/) instead. Create `.claude/skills/<name>/SKILL.md`. Same `/name` invocation, plus you get:

- A directory for supporting files (templates, scripts, reference docs)
- `disable-model-invocation` frontmatter to control whether the AI can auto-fire it
- `paths` glob gating for path-scoped activation
- `context: fork` for isolated execution
- `${CLAUDE_SKILL_DIR}` for relative file references
- Auto-discovery in Claude's `/` menu

## Why this folder is empty

Previously contained `.claude/commands/upgrade.md`. Migrated to [.claude/skills/upgrade/SKILL.md](.claude/skills/upgrade/SKILL.md) on 2026-05-17 per the [Operating principle](README.md#operating-principle--ratchet-forward-never-sideways) (ratchet forward to the documented SOTA form).

This README is kept as a guard: any future AI agent or contributor that walks here looking to "add a custom command" reads this first and learns the correct path.

## See also

- [.claude/skills/README.md](.claude/skills/README.md) — skill inventory + authoring conventions
- [Anthropic — Extend Claude with skills](https://code.claude.com/docs/en/skills) — the official deprecation notice
- [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory) — full directory inventory
