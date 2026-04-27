# Seed research — Claude Code power-user synthesis (2026-04-26)

This file is the verbatim research output produced during the session that catalysed the parent entry. It is preserved as a *deposit-shape illustration* — one of (so far) two concrete examples of what the proposed living module would hold. The other is the earlier session's `temporary/decision-registry.md` and `temporary/claude-code-expert-playbook.md`.

The two together show the **shape variety** the module's schema must absorb without collapsing: a long structured registry on one side, a tighter opinionated synthesis with rankings and citations on the other.

The status-bar section was de-prioritized in the conversation's final user-facing version (the operator said *"we learned everything"* about status bars). It is preserved here because the lab's discipline is over-preservation, not under-preservation. Future readers can decide which subset is still current at the moment they read it.

---

## Table of contents

- [Part 1 — Best status bar (preserved verbatim)](#part-1--best-status-bar-preserved-verbatim)
- [Part 2 — How the harness actually works](#part-2--how-the-harness-actually-works)
- [Part 3 — Shortcuts that change day-to-day](#part-3--shortcuts-that-change-day-to-day)
- [Part 4 — The three modes and when to use each](#part-4--the-three-modes-and-when-to-use-each)
- [Part 5 — Slash commands you'll actually use](#part-5--slash-commands-youll-actually-use)
- [Part 6 — `CLAUDE.md` (the highest-leverage file in any repo)](#part-6--claudemd-the-highest-leverage-file-in-any-repo)
- [Part 7 — Hooks (where the real power is)](#part-7--hooks-where-the-real-power-is)
- [Part 8 — Subagents](#part-8--subagents)
- [Part 9 — Skills](#part-9--skills)
- [Part 10 — MCP (Model Context Protocol)](#part-10--mcp-model-context-protocol)
- [Part 11 — Plugins and the marketplace](#part-11--plugins-and-the-marketplace)
- [Part 12 — Flags worth knowing](#part-12--flags-worth-knowing)
- [Part 13 — The workflows top users actually run](#part-13--the-workflows-top-users-actually-run)
- [Honest caveats](#honest-caveats)
- [Sources](#sources)

---

## Part 1 — Best status bar (preserved verbatim)

### How the statusline actually works (read this first)

Claude Code's statusline is **just a shell command**. On every tick, Claude Code pipes a JSON blob to the script's stdin, and whatever the script prints to stdout becomes the bar. Configured under the `statusLine` key in the global Claude Code settings:

```json
{
  "statusLine": {
    "type": "command",
    "command": "npx -y ccstatusline@latest",
    "padding": 0
  }
}
```

The JSON it pipes you includes the model name, working directory, transcript path, session id, cost so far, context tokens used, and more. Every "statusline" project is just a script that consumes that JSON and emits ANSI-styled text. Knowing this means you are never locked in — swap the `command` string and you have swapped the bar.

You can also run `/statusline` *inside* Claude Code and it generates a script for you in plain English ("show git branch, model, and cost").

### Ranked recommendations (live GitHub stars at the time of the session, 2026-04-26)

| Rank | Project | Stars | Lang | Best for |
|---|---|---|---|---|
| 1 | **sirmalloc/ccstatusline** | 8.3k | TypeScript | Default pick. 50+ widgets, interactive TUI config, powerline, themes, multi-line. Actively shipped (v2.2.8 the same week). |
| 2 | **Haleclipse/CCometixLine** | 2.8k | Rust | Fastest. Bundles utilities to patch out "Context low" warnings + enable verbose mode. Pick this if statusline latency annoys, or for the patcher. |
| 3 | **kamranahmedse/claude-statusline** | 1.1k | Shell | Minimal, no deps. Pick this if avoiding npm. |
| 4 | **Owloops/claude-powerline** | 1.0k | TypeScript | Vim-style powerline with rate-limit (5h block + 7d) visibility, budget thresholds, six themes. Installs as a plugin. |
| 5 | **chongdashu/cc-statusline** | 576 | TypeScript | Simpler ccstatusline alternative. |
| — | **ccusage statusline** | (companion) | — | Not a "statusline project" — a usage analytics CLI with a `statusline` subcommand. Best historical cost tracking in the ecosystem. Many users compose ccstatusline (display) + ccusage (cost engine). |

**Recommendation:** ccstatusline. De-facto standard (~5× the runner-up), updated constantly, TUI configurator means no hand-edited JSON.

```json
{ "statusLine": { "type": "command", "command": "npx -y ccstatusline@latest", "padding": 0 } }
```

Then run `npx ccstatusline` once outside Claude to open the TUI and pick widgets.

**Pick CCometixLine instead if** any of these is true: hundreds of statusline ticks a day and a compiled bar matters; want the bundled "remove Context-low warning" patcher; no Node toolchain wanted on the machine.

**Pick claude-powerline instead if** rate-limit (5h block / 7d rolling) visibility matters specifically.

**Don't bother with the long tail** (sub-500 stars, single-author shell scripts). The top three cover every real need.

### Honest caveat

A statusline is decoration. The features that actually change day-to-day are plan mode, hooks, subagents, and `CLAUDE.md` — not which Nerd Font icon shows the branch. An hour of theming powerline glyphs is not a productivity gain.

---

## Part 2 — How the harness actually works

Claude Code is a thin shell around an LLM with tool access. Most of the leverage comes from configuring **what context loads, what tools are allowed, and what runs around each tool call** — not from clever prompting. Three config surfaces do almost all the work:

- The user's **personal** Claude Code settings (hooks, permissions, env vars, status line) — held in the user's global Claude Code config.
- The repo's **shared** Claude Code settings (checked in, applies to teammates) — held under the repo's `.claude/` directory.
- The repo's **`CLAUDE.md`** at the root — instructions injected into every session in this directory tree.

Everything else (slash commands, agents, skills, plugins) is layered on top.

---

## Part 3 — Shortcuts that change day-to-day

| Key | What it does |
|---|---|
| **Shift+Tab** | Cycles permission modes: default → auto-accept → plan |
| **Esc** | Stop Claude (Ctrl+C exits the CLI — wrong key) |
| **Esc Esc** | Jump back to a previous user message; edit and resend |
| **Shift+Enter** | Newline in prompt (run `/terminal-setup` once to enable) |
| **`!<cmd>`** | Run a shell command; output drops into the conversation |
| **`#<note>`** | Quick auto-memory note ("always use MUI components") |
| **`@<path>`** | Inline a file reference into the prompt |
| **Ctrl+V** | Paste image (yes, even on macOS — not Cmd+V) |
| **Shift+drag** | Drag a file in to reference by path |

**Shift+Tab is the most important shortcut in the whole tool.** From normal mode, one press → auto-accept (Claude executes without asking), two presses → plan mode (Claude explores and proposes but writes nothing). Used every session.

---

## Part 4 — The three modes and when to use each

| Mode | Use when |
|---|---|
| **Plan** (Shift+Tab ×2) | Unfamiliar codebase, large refactor, ambiguous task, anything to review before code is written |
| **Auto-accept** (Shift+Tab ×1) | Plan agreed, task well-scoped, walk-away-okay |
| **Default** | Normal interactive work, small edits, exploration |

Canonical flow: `Shift+Tab Shift+Tab` → state task → iterate the *plan* until it's right → `Shift+Tab` → walk away while it executes one-shot. The workflow Boris Cherny (Claude Code's creator) publicly recommends. Leverage: a wrong plan fixed in 20 seconds beats a wrong implementation undone in 8 minutes.

---

## Part 5 — Slash commands you'll actually use

### Daily

| Command | What it does |
|---|---|
| `/clear` | Wipe context, start fresh. Use **between unrelated tasks**. Cheap, big effect on output quality and cost. |
| `/model` | Switch model mid-session |
| `/plan` | Toggle plan permission mode (alternative to Shift+Tab) |
| `/cost` | Show session cost |
| `/review` | Built-in PR review |
| `/security-review` | Security-focused review of pending branch changes |

### Configure once

| Command | What it does |
|---|---|
| `/init` | Scaffold a new `CLAUDE.md` for the repo |
| `/terminal-setup` | Enable Shift+Enter for newlines (one-time) |
| `/hooks` | Interactive menu to configure hooks (much easier than hand-editing JSON) |
| `/permissions` | Pre-approve safe commands (`Bash(npm test:*)`, `Bash(git status)`) so prompts stop |
| `/install-github-app` | Wires up automatic PR review by Claude on every PR. Highest-ROI background automation. |
| `/agents` | List and manage subagents |
| `/mcp` | Inspect / manage MCP servers |
| `/memory` | Manage the auto-memory file |
| `/ide` | Connect to VS Code / JetBrains |

### Automation

| Command | What it does |
|---|---|
| `/loop <interval> <cmd>` | Run a prompt or slash command repeatedly. Local, up to 3 days. (`/loop 5m /check-deploy`) |
| `/schedule` | Schedule a routine in the cloud — keeps running when laptop is off |

### Repo-local custom commands

A markdown file at `<repo>/.claude/commands/<name>.md` becomes `/<name>`. Subfolders nest (`builder/plugin.md` → `/builder/plugin`). Inside, `$ARGUMENTS` interpolates args. Two-minute investment, infinite reuse for any prompt typed more than twice.

---

## Part 6 — `CLAUDE.md` (the highest-leverage file in any repo)

`CLAUDE.md` at repo root is loaded into every session in that directory tree. Hierarchical — also valid in subdirectories for area-specific rules, and a global personal `CLAUDE.md` exists at the user's Claude Code config location for everywhere-rules.

**What to put in it:**
- Build/test/lint commands the agent should run
- Architectural rules ("DB access goes through `db/queries/*`, never raw SQL in routes")
- Stack choices ("Use TanStack Query, not SWR")
- File-layout conventions
- Mistakes Claude has made before, written as rules

**Anthropic's official advice:** every time Claude does something wrong, append the rule to `CLAUDE.md` so it doesn't repeat. Treat it as a living lessons-learned file, not a static doc.

**Counter-discipline:** keep it short. A 30-line precise `CLAUDE.md` beats a 300-line essay. Long ones get skimmed and burn the context budget on every session.

---

## Part 7 — Hooks (where the real power is)

Hooks are shell commands that run on lifecycle events. Configured via `/hooks` (menu) or directly in the repo's shared Claude Code settings. The events that matter:

| Event | Use for |
|---|---|
| `PreToolUse` | Block / modify tool calls before they run (refuse `rm -rf`, auto-approve `git status`) |
| `PostToolUse` | Run after edits — Prettier, eslint --fix, `tsc --noEmit`, the test suite |
| `SessionStart` | Load context, print reminders |
| `Stop` | Desktop notification when Claude finishes |
| `UserPromptSubmit` | Inject context per-prompt, redact secrets, validate |

Example — auto-format every edit:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "prettier --write $CLAUDE_FILE_PATH" }]
    }]
  }
}
```

The win: **the agent sees its own failures.** A `PostToolUse` hook that runs `tsc --noEmit` means Claude can't ship un-typing code without immediately seeing the error and fixing it. Every hook tightens the feedback loop by one notch.

This is also where **automated behaviors** ("from now on when X, do Y") get wired. Memory and `CLAUDE.md` cannot fulfill those — only hooks can, because the harness, not the model, executes them.

---

## Part 8 — Subagents

Markdown files at `<repo>/.claude/agents/<name>.md` with frontmatter defining a specialized agent: model, allowed tools, system prompt, optional `isolation: worktree` for parallelism.

Two reasons to use them:

1. **Context isolation** — the subagent's transcript doesn't pollute the main thread. Big research dumps stay scoped.
2. **Parallelism** — multiple subagents run concurrently when invoked in a single message.

This very repo's `.claude/agents/` directory is itself a working example: a 12-step workflow where `requirement-classifier`, `canon-librarian`, `outside-view`, three `critic-*` lenses, and others get composed.

**Practical pattern:** specialized critic / reviewer agents (architecture, ops, product, security) spawned in parallel after a generation step. Each veto on its own — minority-vetoes prevent groupthink.

---

## Part 9 — Skills

Skills (`<repo>/.claude/skills/<name>/SKILL.md`) are reusable workflows that **auto-trigger when context matches**. The distinction from agents: agents are invoked by name, skills are invoked when the situation matches.

Use for: changelog generation, dep bumps, security review templates, onboarding flows — anything done the same way every time.

**Anti-pattern:** installing 20 plugins/skills hoping one catches the conventions. Every skill sits in the context budget at session start. The most experienced users run **0–3 plugins** and write a precise `CLAUDE.md` instead. Three good skills beat twenty fighting for attention.

---

## Part 10 — MCP (Model Context Protocol)

`claude mcp add <name>` wires Claude to external systems. Highest-ROI integrations:

| MCP | Why |
|---|---|
| **Linear / Jira** | Pull tickets, update status, attach context — no manual ticket-paste-into-prompt |
| **GitHub** | PR / issue / check operations from inside the session |
| **Sentry / Grafana** | Read error rates and dashboards while debugging |
| **Postgres / BigQuery** | Query directly when investigating data bugs |
| **Playwright / Chrome** | Frontend verification — Claude loads the page and reads the console |
| **Slack** | Read threads as context (read-mostly; careful with write) |

The leverage: most "I had to manually copy 30 lines of error output into the prompt" moments disappear when the MCP gives Claude direct read access.

---

## Part 11 — Plugins and the marketplace

`/plugin marketplace add <repo>` then `/plugin install <name>`. The official Anthropic marketplace has ~100 plugins (a third Anthropic-built, the rest partner). Browse via `/plugin` or at the marketplace directory.

Notable workflow plugins:
- **Superpowers** — multi-agent dev methodology (brainstorm → spec → plan → execute → review → merge)
- **Linear plugin** — first-class issue-tracker integration
- **Recall** — full-text search across past Claude sessions

**Honest take:** the median plugin is not worth the context cost. Install precisely, audit what each one adds, remove the ones whose absence wouldn't be noticed.

---

## Part 12 — Flags worth knowing

| Flag | What it does |
|---|---|
| `--dangerously-skip-permissions` | Bypass all permission prompts. **Throwaway worktrees only.** Never the main repo. |
| `--add-dir <path>` | Give Claude access to a second directory in the same session (monorepo + sibling repo) |
| `--permission-mode plan` | Start directly in plan mode |
| `--continue` / `-c` | Resume the most recent session |
| `--resume <id>` | Resume a specific session by id |
| `--print` / `-p` | Non-interactive mode for scripts and CI |

---

## Part 13 — The workflows top users actually run

### Workflow 1 — Plan, then auto-accept, then leave
`Shift+Tab Shift+Tab` → state the task → iterate until plan is right → `Shift+Tab` → walk away. Don't iterate on code; iterate on the plan.

### Workflow 2 — Parallel sessions across worktrees
Open N terminal tabs. In each: `git worktree add <path>` and `claude` inside. Assign one independent task per tab. Zero merge conflicts because each is a separate working copy. Serious users run 5 in parallel; some compose with browser sessions for 10–15 concurrent agents.

For automated parallelism: put `isolation: worktree` in a subagent's frontmatter and the orchestrator spawns it in its own checkout.

### Workflow 3 — Verification > everything
Anthropic's stated #1 tip. Concretely:
- `PostToolUse` hook running `tsc --noEmit` + the test suite
- Playwright or Chrome MCP so frontend changes are actually loaded and the console is read
- `/security-review` and `/review` before any push

If only one thing from this guide is adopted, this one.

### Workflow 4 — Lean `CLAUDE.md`, not a plugin festival
30 lines of repo-specific rules beat 15 generic plugins fighting for context. Specificity wins.

### Workflow 5 — `/install-github-app` for automated PR review
One-time setup. After this, every PR opened in the repo gets reviewed by Claude — catches genuine logic errors and security issues. Customize the prompt in `.github/claude-code-review.yml`.

### Workflow 6 — Memory hygiene
The harness already auto-persists user preferences and feedback. Maintain it with:
- `/memory` to inspect
- `#<note>` to drop a quick preference inline
- "forget X" to remove an entry

Store non-obvious things (corrections, why-decisions, project context). Don't store anything derivable from code or `git log`.

### Workflow 7 — `/loop` and `/schedule` for ambient automation
- `/loop 10m /check-deploy` — poll a build until done; notification each tick
- `/schedule` — for "open a cleanup PR in 2 weeks" or "every Monday triage flaky tests"

These let Claude be treated as a background process, not just a foreground tool.

---

## Honest caveats

- **More tools ≠ more productive.** The leverage compounds in plan mode + hooks + a tight `CLAUDE.md`. Plugins, statuslines, and themes are decoration.
- **Context engineering > prompt engineering.** Model quality is no longer the bottleneck; what loads into the window is. `CLAUDE.md`, hooks that prune output, scoped subagents — that's where the wins are.
- **There is no secret SOTA setup.** It's the same engineering hygiene — small steps, fast feedback, written context — applied to an agent. Skepticism toward "ultimate workflow" claims is warranted.
- **Some commands seen in single sources were omitted** because verification across multiple sources or in the official docs failed. The CLI changes fast; verify with `/help` in the local installation before relying on any single tip.

## Sources

Status-bar projects (live GitHub star counts at session time, 2026-04-26):
- [sirmalloc/ccstatusline (8.3k stars)](https://github.com/sirmalloc/ccstatusline)
- [Haleclipse/CCometixLine (2.8k stars)](https://github.com/Haleclipse/CCometixLine)
- [Owloops/claude-powerline (1.0k stars)](https://github.com/Owloops/claude-powerline)
- [kamranahmedse/claude-statusline (1.1k stars)](https://github.com/kamranahmedse/claude-statusline)
- [chongdashu/cc-statusline (576 stars)](https://github.com/chongdashu/cc-statusline)
- [ccusage statusline guide](https://ccusage.com/guide/statusline)
- [Official: Customize your status line](https://code.claude.com/docs/en/statusline)

Power-user tips and workflows:
- [Claude Code power user tips — Anthropic Help Center](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips)
- [Common workflows — Claude Code Docs](https://code.claude.com/docs/en/common-workflows)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Discover and install plugins — Claude Code Docs](https://code.claude.com/docs/en/discover-plugins)
- [Boris Cherny's workflow (X)](https://x.com/aakashgupta/status/2007347705945944153)
- [Steve Sewell — How I use Claude Code (Builder.io)](https://www.builder.io/blog/claude-code)
- [hesreallyhim/awesome-claude-code (40.9k stars)](https://github.com/hesreallyhim/awesome-claude-code)
- [Parallel workflow guide](https://www.shareuhack.com/en/posts/claude-code-parallel-workflow-guide-2026)
- [Best Claude Code plugins — tested review](https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review)
- [Marco Lancini — My Claude Code Setup (2026)](https://blog.marcolancini.it/2026/blog-my-claude-code-setup/)
