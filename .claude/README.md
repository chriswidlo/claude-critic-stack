# .claude/

Project-scoped Claude Code configuration. Eight subdirectories + two settings files. Each subdirectory has its own README; this file is the navigation index.

**Read this when:** you're walking `.claude/` cold and want to know what each subdirectory is for, or which slots are Anthropic-documented vs. custom convention. **Skip if:** you already know which subdirectory you need.

## Inventory

| Path | Anthropic-documented? | Status | Doc |
|---|---|---|---|
| [.claude/CLAUDE.md](CLAUDE.md) *(repo-root variant)* | yes | We use repo-root `CLAUDE.md` instead | [CLAUDE.md](CLAUDE.md) |
| [.claude/settings.json](.claude/settings.json) | yes, committed | Permissions, hooks, env. **In use.** | inline comments |
| [.claude/settings.local.json](.claude/settings.local.json) | yes, gitignored | Personal overrides | inline |
| [.claude/agents/](.claude/agents/) | yes | 14 agents driving the 13-step workflow | [agents/README.md](.claude/agents/README.md) |
| [.claude/skills/](.claude/skills/) | yes | 7 skills (slash-command-triggered behaviors) | [skills/README.md](.claude/skills/README.md) |
| [.claude/hooks/](.claude/hooks/) | convention, not a reserved slot | 7 AI-blind hook scripts for diagnostics | [hooks/README.md](.claude/hooks/README.md) |
| [.claude/commands/](.claude/commands/) | yes, **legacy** | Guard-only — `/name` invocations are skills now | [commands/README.md](.claude/commands/README.md) |
| [.claude/session-artifacts/](.claude/session-artifacts/) | custom convention | Per-session reasoning artifacts; schema + ledger live here | [session-artifacts/README.md](.claude/session-artifacts/README.md) |
| [.claude/rules/](.claude/rules/) | yes | **Empty by design** — for path-scoped rules when need emerges | [rules/README.md](.claude/rules/README.md) |
| [.claude/agent-memory/](.claude/agent-memory/) | yes | **Empty by design** — for subagent persistent memory when `memory: user` is set | [agent-memory/README.md](.claude/agent-memory/README.md) |
| [.claude/output-styles/](.claude/output-styles/) | yes | **Empty by design** — for project-scoped system-prompt styles | [output-styles/README.md](.claude/output-styles/README.md) |
| [.claude/plugins/](.claude/plugins/) | yes | **Empty by design** — for project-shippable plugins (this stack as plugin, or consumed plugins) | [plugins/README.md](.claude/plugins/README.md) |

## Auto-loaded vs lazy-loaded (the load-bearing distinction)

| Surface | Loaded when |
|---|---|
| Root [CLAUDE.md](CLAUDE.md) | Every session, every turn (auto) |
| `.claude/settings.json` | Every session start (auto) |
| `.claude/rules/*.md` with matching `paths:` glob | When Claude touches a matching file (lazy) |
| `.claude/skills/<name>/SKILL.md` | When skill is invoked (lazy) |
| `.claude/agents/<name>.md` | When agent is invoked (lazy) |
| `.claude/hooks/*.sh` | On the bound Claude Code event (automatic, AI-blind) |
| Any folder README (this file, subfolders) | When AI/human reads files in that folder (lazy) |

Per the [Anthropic memory docs](https://code.claude.com/docs/en/memory): everything in root CLAUDE.md is paid for on every turn; everything elsewhere is free until consulted. This is why the folder READMEs in this directory are thorough — they cost nothing until needed.

## See also

- [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory) — authoritative slot inventory
- [Anthropic — How Claude remembers your project](https://code.claude.com/docs/en/memory) — auto-load vs lazy-load semantics
- [Root CLAUDE.md](CLAUDE.md) — the always-loaded operating manual
- [Root README.md](README.md) — repo-level orientation
