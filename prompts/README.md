# prompts/

**Working / historical folder for prompts the operator (or AI) wants to keep across sessions** — typically copy-paste briefs destined for external tools (Anthropic ultraplanning remote agent, web Claude sessions, teammate's terminal), or session-bound prompts that proved valuable enough to commit.

## Read this when

- You arrived here because a file path under `prompts/` was referenced.
- You're about to add a prompt and need to know whether this folder is the right home.

## Skip if (this is the default)

- **The AI walking the repo cold should IGNORE this folder.** It is not a Claude Code primitive. Nothing here is auto-loaded. Nothing here is `/`-invocable. No agent or skill references prompts/ as input.
- You're looking for reusable Claude Code prompts — those belong in [.claude/skills/](.claude/skills/) (where they're auto-discovered and `/`-invocable).
- You're looking for durable design rationale — that belongs in [upgrades/](upgrades/) or commit messages.

## What this folder is NOT

- **Not a Claude Code primitive.** Anthropic does not recognize `prompts/` as a documented directory. Custom convention only.
- **Not auto-discovered.** Files here are not loaded, indexed, or surfaced by any tool.
- **Not authoritative.** A file here does not imply a decision was made. It's working material.
- **Not for reusable workflows.** Those become skills.

## What this folder IS for

- **Copy-paste briefs destined for tools OUTSIDE Claude Code.** The current example: `ultraplan-next-level.md` is a paste-into-Anthropic-ultraplanning-remote-agent brief. It's stored here so the operator can find it again, share it across machines via git, and revise it across sessions.
- **Session-bound prompts worth committing.** If a particularly good prompt drafted during a session has reusable value but doesn't fit the skill-shape (because it targets an external tool, or is one-shot, or the structure doesn't pay off), it can land here.
- **Historical record of prompts that shaped the work.** Like `.genesis/` for founding docs, but for prompts specifically.

## Rules

1. **Files here must self-explain.** Each prompt file should open with a header stating: what it's for, where to paste/use it, when it was last revised. AI agents walking past `prompts/` will not read the contents unless explicitly directed.
2. **Commit if there's value.** This folder is tracked. If a prompt has reuse value (cross-machine, cross-team, cross-session), commit it. If it's pure one-shot scratch, delete after use — same as [plans/](plans/).
3. **Do not reference prompts/ from CLAUDE.md, agent files, skill files, or hooks.** Nothing in the live workflow depends on this folder. If you find yourself wanting to wire a workflow primitive to a file in `prompts/`, that file should be a skill instead.
4. **Do not store secrets, credentials, or PII.** The folder is tracked; treat it as public for repo-share purposes.

## What goes where (decision table)

| Use case | Right home |
|---|---|
| Reusable prompt I want to invoke as `/name` | [.claude/skills/<name>/SKILL.md](.claude/skills/) |
| Paste-into-external-tool brief | `prompts/` (here) |
| Per-session reasoning artifact | `.claude/session-artifacts/<session-id>/` |
| Ephemeral planning scratch for current session | [plans/](plans/) (auto-delete on completion) |
| R&D idea worth preserving | [upgrades/](upgrades/) |
| Durable design rationale | Commit message + relevant agent/skill/CLAUDE.md edit |

## Current contents

| File | Purpose | Last revised |
|---|---|---|
| `ultraplan-next-level.md` | Paste-into-Anthropic-ultraplanning-remote-agent brief for proposing next-level upgrades to this stack. | (see git log) |

## See also

- [.claude/skills/README.md](.claude/skills/README.md) — where reusable Claude Code prompts belong instead
- [plans/README.md](plans/README.md) — the ephemeral session-scratch convention
- [Anthropic — Extend Claude with skills](https://code.claude.com/docs/en/skills) — why most "prompt files" should be skills
