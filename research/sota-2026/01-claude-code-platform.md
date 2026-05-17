# Claude Code Platform Audit — 2026-vintage

> Snapshot date: 2026-05-17. Coverage tuned for an advanced user running a 12-step adversarial-review stack about to scale to ~10 parallel worktrees. Stability labels reflect what the docs say today; research-preview surfaces can change.

## 0. Top-line context

Two structural shifts shape every decision below.

1. **Docs moved.** `docs.claude.com/en/docs/claude-code/*` 301-redirects to `code.claude.com/docs/en/*`. Anthropic API and model pages stay at `platform.claude.com/docs/en/*`. Cite the new URLs in every artifact.
2. **Five user-extensible primitives recentered the harness.** Plugins, Skills, Subagents, Hooks, MCP. Everything else — output styles, statuslines, monitors, keybindings, LSP, channels — is composition on top. Custom slash commands collapsed into Skills.

The 2026 model story is **Opus 4.7 (April 16, 2026)** with adaptive thinking. Fixed thinking budgets are gone on 4.7; effort levels (`low | medium | high | xhigh | max`) are the primary lever ([Model configuration](https://code.claude.com/docs/en/model-config), [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

---

## 1. Surfaces and primitives

### 1.1 Plugins (`.claude-plugin/plugin.json`)

**Stable.** A plugin is a directory with a manifest at `.claude-plugin/plugin.json` plus any of `skills/`, `agents/`, `hooks/hooks.json`, `commands/`, `.mcp.json`, `.lsp.json`, `monitors/monitors.json`, `bin/`, `settings.json`. It bundles every other primitive into one installable, versioned unit ([Plugins](https://code.claude.com/docs/en/plugins), [Plugins reference](https://code.claude.com/docs/en/plugins-reference)).

Three distinguishing features:
- **Namespacing.** A `acme` plugin registers its `hello` skill as `/acme:hello`. No collisions.
- **Versioning.** If `plugin.json` omits `version`, the git SHA is used — every commit is a new "version." Set `version` explicitly.
- **Marketplaces.** Distribute via Anthropic's official one or any git repo / URL / local path ([Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)).

**Common authoring mistake** (called out in docs): putting `commands/`, `agents/`, `skills/`, `hooks/` *inside* `.claude-plugin/`. Only `plugin.json` lives there.

Authoring loop: `claude --plugin-dir ./my-plugin`, then `/reload-plugins`. Also accepts `.zip` (v2.1.128+) and `--plugin-url`.

**What it solves no other primitive does:** atomic, versioned distribution of a coordinated bundle of skills+agents+hooks+MCP.

**Adoption rec for the critic stack:** Convert `.claude/agents/` + critic lenses into a private plugin once the lens roster stabilizes (probably a month out). Keep `version` explicit so worktrees don't pull partial mid-session changes.

**Anti-patterns.** Shipping without `version` while mutating `main`. Plugins that force-enable a main-thread agent via `settings.json.agent` without flagging it.

### 1.2 Skills (`.claude/skills/<name>/SKILL.md`)

**Stable.** Replaces `.claude/commands/<name>.md` (legacy commands still work; skills win on collision) ([Skills](https://code.claude.com/docs/en/skills)).

YAML frontmatter fields you'll actually use:

| Field | Purpose |
| --- | --- |
| `description` | Auto-invocation hook. First sentence load-bearing — combined description+when_to_use capped at 1,536 chars. |
| `when_to_use` | Trigger-phrase hints; appended to description. |
| `disable-model-invocation` | `true` = only user invokes via `/name`. For `commit`, `deploy`, side-effect skills. |
| `user-invocable` | `false` = only Claude invokes; hidden from `/` menu. For background-knowledge skills. |
| `allowed-tools` | Pre-approves listed tools without changing what's *available*. |
| `model`, `effort` | Per-skill override; reverts next turn. |
| `context: fork` + `agent: Explore` | Runs skill in isolated subagent. |
| `paths` | Glob list gating auto-invocation by file context. |
| `arguments`, `argument-hint` | Named positional args (`$name` expansion). |

Substitutions: `$ARGUMENTS`, `$0..$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`. Use `${CLAUDE_SKILL_DIR}` for bundled scripts — it's the only form that survives personal/project/plugin installs.

**Dynamic context injection.** ` ``!`<cmd>` `` and ` ```! ` fenced blocks execute *before* Claude sees the skill body; output inlines. Disable globally with `disableSkillShellExecution: true`; bundled and managed skills bypass that setting.

**Lifecycle gotcha.** Once invoked, rendered SKILL.md enters context as one message and stays the rest of the session. Auto-compaction reattaches most recent invocation (5K tokens each, 25K combined budget across reattached skills). After many invocations + compaction, older skills can be dropped.

**Skill > slash command > agent.**
- **Skill:** packaged, dynamic, reusable instructions dormant until needed. Default choice.
- **Slash command:** legacy; kept for backward compat.
- **Subagent:** separate context window, different model, independent permissions. Skills can fork into a subagent via `context: fork` — usually a better lever than defining a new subagent.

**Adoption rec for the critic stack:** Every orchestrator-performed step (2, 9, 11, 12, 13) is a skill candidate. You already have `session-bootstrap` and `ledger-render`; consider promoting step 2 (reframe) and step 11 (replan-vs-rewrite routing) with `disable-model-invocation: true`. Use `paths` on rule-style skills so they don't eat description budget.

**Anti-patterns.** Skill bodies >500 lines (move detail to siblings). Using skills where hooks would be deterministic ("always lint before commit" = hook, not skill).

### 1.3 Hooks

**Stable surface, expanding event roster.** 2026 lifecycle is ~30 events ([Hooks](https://code.claude.com/docs/en/hooks)):

| Category | Events |
| --- | --- |
| Session | `SessionStart`, `SessionEnd`, `Setup` |
| Prompt | `UserPromptSubmit`, `UserPromptExpansion` |
| Tool | `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch` |
| Notification | `Notification` |
| Subagent | `SubagentStart`, `SubagentStop` |
| Task | `TaskCreated`, `TaskCompleted` |
| Turn end | `Stop`, `StopFailure`, `TeammateIdle` |
| Context | `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged` |
| Worktree | `WorktreeCreate`, `WorktreeRemove` |
| Compaction | `PreCompact`, `PostCompact` |
| MCP elicitation | `Elicitation`, `ElicitationResult` |

**Stdin payload (common):** `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`. Event-specific fields layered on: `PreToolUse` adds `tool_name`, `tool_input`, `tool_use_id`; `PostToolUse` adds `tool_result`; `Stop` adds `response`; `FileChanged` adds `file_path`; `SessionStart` adds `source` (`startup | resume | clear | compact`) and `model`.

**Exit codes.**
- `0` — stdout parsed as control JSON. For `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, stdout appends to Claude's context.
- `2` — blocking error; stderr shown to Claude; JSON ignored. Blocks where the event supports blocking (PreToolUse, PermissionRequest, UserPromptSubmit/Expansion, Stop, SubagentStop, TeammateIdle, TaskCreated/Completed, ConfigChange, PreCompact, PostToolBatch, Elicitation/Result, WorktreeCreate). Non-blockable events still surface stderr but execution continues.
- Other — non-blocking; transcript shows `<hook> hook error`.

**JSON control protocol (exit 0):**

```json
{
  "continue": true,
  "stopReason": "...",
  "suppressOutput": false,
  "systemMessage": "shown to user",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask | defer",
    "permissionDecisionReason": "..."
  }
}
```

**AI-blind patterns.** Hooks run regardless of what Claude decides. Use when an instruction is "must happen at point X" rather than "should happen when Claude judges it appropriate." Examples: format-only state gates, protected-path enforcement, path-discipline checks, synthesis-citation gates.

**Adoption rec for the critic stack:** Promote path-discipline from "CLAUDE.md says no absolute paths" to a PreToolUse hook hard-blocking Edit/Write with absolute-path strings. The `path-check` skill is the human-invokable counterpart; the hook is the AI-blind enforcement. Also wire `WorktreeCreate` to seed each worktree with `.claude/worktrees/` gitignore + `.worktreeinclude` env files — once you go to 10 worktrees, manual copy-paste is friction.

**Anti-patterns.** Slow hooks on PreToolUse (every tool call pays latency — keep <100ms or move to PostToolUse). Using `continue: false` to "scold" Claude (it ends the session — prefer `permissionDecision: "deny"`). Forgetting hook decisions don't bypass permission rules — `deny` rules still deny even if a PreToolUse hook returns `allow`.

### 1.4 MCP servers

**Stable, first-class.** ([MCP](https://code.claude.com/docs/en/mcp))

Add via `claude mcp add` or `.mcp.json`. Three transports (stdio, streamable HTTP/SSE, websocket), three scopes (`local` per-user-per-dir, `project` committed, `user` global). Permission syntax: `mcp__<server>`, `mcp__<server>__*`, `mcp__<server>__<tool>`.

The VS Code extension ships its own MCP server (`ide`) exposing `mcp__ide__getDiagnostics` and `mcp__ide__executeCode` (Jupyter). Binds 127.0.0.1 with a per-activation random token.

**Channels.** MCP servers can push notifications into the session (Slack, Telegram, webhook, CI). See [Channels](https://code.claude.com/docs/en/channels).

**Adoption rec for the critic stack:** You don't currently need MCP — the stack is closed-world. One future angle: a custom MCP server exposing `canon-search` as a tool, so frame-challenger and critic-architecture could hit the corpus without full subagent invocation. Defer until canon stabilizes.

**Anti-patterns.** Adding GitHub MCP to a stack that doesn't touch GitHub (steals description budget). Committing credentials in `.mcp.json`.

### 1.5 Subagents (`.claude/agents/<name>.md`)

**Stable.** ([Subagents](https://code.claude.com/docs/en/sub-agents))

Frontmatter: `description`, `tools` (whitelist; omitted = inherit parent), `model` (`opus | sonnet | haiku | inherit`), `permissionMode` (overrides session, ignored under `auto`), `effort`, `skills` (preload list), `isolation: worktree`, `color`. Body is the system prompt.

**Subagent beats skill when:** different model, isolated context window, different tool restrictions, or persistent per-subagent memory needed. **Skill beats subagent when:** work runs inline against current context, output is short/structured, you want it visible in the main transcript.

**Adoption rec for the critic stack:** Already well-used. Next move: pin `model: haiku` on `subagent-distiller` (short-in, short-out — Opus is wasted). Set `isolation: worktree` on any agent that touches the filesystem.

**Anti-patterns.** Subagent body identical to a skill (two sources of truth). Subagent `permissionMode: bypassPermissions` (auto-mode ignores it; non-auto = enormous attack surface).

### 1.6 Custom slash commands

**Folded into Skills.** Existing `.claude/commands/<name>.md` files still work; new entries go in `.claude/skills/<name>/SKILL.md`. Migration is additive — skills add supporting files, `disable-model-invocation`, auto-load semantics.

### 1.7 Output styles

**Stable.** ([Output styles](https://code.claude.com/docs/en/output-styles))

Modifies system prompt at session start. Built-ins: Default, **Proactive** (act first, ask less — same guidance as auto mode without changing permission mode), **Explanatory**, **Learning**. Custom styles in `~/.claude/output-styles/`, `.claude/output-styles/`, or managed. Frontmatter: `name`, `description`, `keep-coding-instructions`, `force-for-plugin`. Changes take effect next session — deliberate, to preserve prompt caching.

**Adoption rec for the critic stack:** Build one "Adversarial reviewer" style. Keep coding instructions off; set tone to honest friction, no agreeableness, no persona-cosplay. Mirrors the CLAUDE.md rules at system-prompt level.

**Anti-patterns.** Custom output styles + skills that contradict them. Long custom styles (>2K tokens) — paid every session.

### 1.8 Settings hierarchy

**Stable.** ([Settings](https://code.claude.com/docs/en/settings), [Permissions](https://code.claude.com/docs/en/permissions))

Precedence, high to low:
1. Managed (platform-specific dirs)
2. Command-line flags
3. `.claude/settings.local.json` (gitignored)
4. `.claude/settings.json` (committed)
5. `~/.claude/settings.json`
6. Defaults

Permission rules **merge** across scopes, evaluated `deny → ask → allow`, first match wins. A deny anywhere in the chain wins.

Notable 2026 keys: `effortLevel`, `alwaysThinkingEnabled`, `autoMemoryEnabled`, `autoMemoryDirectory`, `skillListingBudgetFraction`, `skillOverrides`, `sandbox.{filesystem,network}`, `claudeMd` (managed-only — embed CLAUDE.md content in settings), `claudeMdExcludes`, `worktree.baseRef` (`"fresh"` or `"head"`), `disableAgentView`, `disableSkillShellExecution`, `modelOverrides` (for Bedrock/Vertex/Foundry).

**Permission specifiers — path anchor types** (gitignore semantics):
- `//path` = filesystem absolute
- `~/path` = home-relative
- `/path` = **project-root relative** (the gotcha — `/Users/alice/file` is NOT absolute)
- `path` or `./path` = cwd-relative

Bash specifiers support wildcards anywhere. `Bash(npm test *)` matches `npm test`, `npm test --watch`. Space matters: `Bash(ls *)` matches `ls -la` but not `lsof`. Process wrappers (`timeout`, `time`, `nice`, `nohup`, `stdbuf`, bare `xargs`) stripped before matching. Compound commands split on `&& || ; | |& &` — each part checked independently. Read-only commands (`ls`, `cat`, `grep`, `find`, read-only `git`) run without prompt in every mode.

**Adoption rec for the critic stack:** Project `.claude/settings.json` with deny rules on `.env`, `.git/**`, `rm -rf *`, plus allow rules for `bin/check-path-discipline.sh *` and read-only git commands. Keep `claudeMdExcludes` ready if you ever work from a monorepo subdir.

**Anti-patterns.** `bypassPermissions` outside a sandboxed container. Constraining `Bash(curl *)` with URL specifiers (fragile — use sandbox or `WebFetch(domain:...)`). Committing `settings.local.json`.

### 1.9 Memory: CLAUDE.md + auto-memory

**Stable.** Auto-memory needs v2.1.59+. ([Memory](https://code.claude.com/docs/en/memory))

CLAUDE.md hierarchy, load order (broadest first): managed → user (`~/.claude/CLAUDE.md`) → project (`./CLAUDE.md` or `./.claude/CLAUDE.md`) → local (`./CLAUDE.local.md`, gitignored). Files **concatenate**, don't override. Ancestor files load at start; descendant files lazy-load when Claude reads inside that subtree.

Imports: `@path/to/file` (relative paths resolve to the importing file). Five-hop max. External imports prompt for approval first time.

`.claude/rules/*.md` = modular alternative. Rules without `paths:` load like CLAUDE.md; rules with `paths:` load only when Claude touches matching files.

**Block-level HTML comments are stripped** from CLAUDE.md — use them for human-only notes without spending tokens.

**Auto-memory** lives at `~/.claude/projects/<repo>/memory/MEMORY.md` plus topic files. First 200 lines or 25KB of `MEMORY.md` loads each session; topic files load on demand. `autoMemoryDirectory` setting overrides location (managed/user only — not project, to prevent malicious project settings from redirecting writes).

The "auto-memory index" pattern: `MEMORY.md` indexes `feedback_*.md`, `pattern_*.md` topic files. (Your own MEMORY.md is a worked example.)

**Adoption rec for the critic stack:** Keep CLAUDE.md under 200 lines (currently fine). Migrate long prose blocks ("Things you must not do") into `.claude/rules/orchestrator-discipline.md` once you cross. Use HTML comments for maintainer-only notes.

**Anti-patterns.** Mixing personal preferences into project CLAUDE.md. Expecting auto-memory to remember what Claude didn't save (it's opportunistic). Assuming auto-memory syncs across machines — it doesn't.

### 1.10 Plan mode

**Stable.** ([Permission modes](https://code.claude.com/docs/en/permission-modes))

`Shift+Tab` cycles `default → acceptEdits → plan`. Or `claude --permission-mode plan`. Or `/plan` prefix on one prompt. In plan mode Claude reads and runs read-only commands but cannot edit. Approval offers: approve+auto, approve+acceptEdits, approve+default, keep planning, refine with [Ultraplan](https://code.claude.com/docs/en/ultraplan) (browser-based review).

`Ctrl+G` opens the plan in `$EDITOR`. Accepting auto-names the session from plan content.

`opusplan` alias uses Opus for plan, Sonnet for execution. Plan phase runs at 200K context — automatic 1M upgrade does NOT apply to opusplan.

**Adoption rec for the critic stack:** Use plan mode at step 9 (Generator) for multi-file changes. `opusplan` is right for that step.

**Anti-patterns.** Plan mode for read-only research (wastes a round — use default). Approving a plan into auto mode in an unsanitized directory.

### 1.11 Background tasks and agent view

**Research preview** for `claude agents` (v2.1.139+); underlying background-session machinery stable. ([Agent view](https://code.claude.com/docs/en/agent-view))

`claude agents` opens a TUI listing every background session you've started, grouped Needs input / Working / Completed. Each session is a full Claude Code conversation hosted by a per-user supervisor process that survives terminal close. Worktree isolation automatic inside a git repo.

Commands: `claude --bg "task"`, `claude --agent <name> --bg "task"`, `/bg` or `←` on empty prompt to background, `claude attach <id>` / `logs` / `stop` / `respawn`. Supervisor logs to `~/.claude/daemon.log`; state at `~/.claude/jobs/<id>/state.json`.

Distinct from `run_in_background: true` on a single Bash call, which is a background shell process monitored via the `Monitor` tool (stays inside one session).

**Adoption rec for the critic stack — the lever for "10 parallel worktrees."** Replace "spawn 10 terminals" with: dispatch all 10 via `claude agents` or `claude --bg`. Each gets an auto-worktree. Use `.worktreeinclude` for env copying. Use agent view's PR-status dot as scoreboard.

Two scaling concerns:
1. **Rate limits stack** — 10 background sessions burn quota ~10x. Lower-effort defaults via `claude agents --effort medium --model sonnet` for worktrees that don't need Opus.
2. **Sessions die on sleep.** `caffeinate -d` before long runs, or accept `claude respawn --all` on return.

**Anti-patterns.** Dispatching 10 sessions on Opus + `xhigh` and walking away (quota gone). Forgetting worktrees delete with sessions — commit/push before `Ctrl+X Ctrl+X`.

### 1.12 Headless mode

**Stable. `--bare` is the future default.** ([Headless](https://code.claude.com/docs/en/headless))

`claude -p "prompt"` runs non-interactively. With `--bare`, Claude skips auto-discovery of hooks, skills, plugins, MCP, auto-memory, CLAUDE.md — only flags you pass take effect.

Output: `--output-format text|json|stream-json`. `--json-schema <schema>` enforces structured output in `structured_output`. Stream JSON yields `system/init`, `system/api_retry`, `stream_event`, and (with `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1`) `system/plugin_install`. Stdin capped at 10MB (v2.1.128+).

**Note:** Starting **June 15, 2026**, Agent SDK and `claude -p` usage on subscription plans draws from a separate monthly Agent SDK credit pool. Plan budgeting accordingly.

**Adoption rec for the critic stack:** Use `claude -p --bare --append-system-prompt-file <prompt>` for CI-side critic-panel runs. Bare mode is the only way to guarantee reproducibility across contributor `~/.claude/` configs.

**Anti-patterns.** `-p` without `--bare` in CI (silently inherits local config). Building rich tooling in `-p` mode when the Python/TypeScript SDK is cleaner.

### 1.13 OpenTelemetry

**Stable.** ([Monitoring usage](https://code.claude.com/docs/en/monitoring-usage))

Enable: `CLAUDE_CODE_ENABLE_TELEMETRY=1`. Set `OTEL_METRICS_EXPORTER` (`otlp | prometheus | console | none`) and `OTEL_LOGS_EXPORTER`. Standard OTLP env vars (`OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_HEADERS`). Defaults: metrics 60s, logs 5s.

Emits metrics (token counts, costs, tool latency, session duration), events via logs/events protocol, traces (beta). Follows OTel GenAI semantic conventions.

**Adoption rec for the critic stack:** Once you cross from one user to any team, wire OTel into local Prometheus + Grafana. Reconcile workflow-ledger cost ratios against actual API spend per session_id. Only way to validate the structure-tax is paying off.

**Anti-patterns.** No `OTEL_RESOURCE_ATTRIBUTES` distinguishing dev/prod/CI (one undifferentiated stream). 5s log interval in production without checking backend ingestion limits.

### 1.14 Worktree support

**Stable.** ([Worktrees](https://code.claude.com/docs/en/worktrees))

`claude --worktree <name>` creates `.claude/worktrees/<name>/` on branch `worktree-<name>`. Default base `origin/HEAD`; set `worktree.baseRef: "head"` to branch from local HEAD. PR-based: `claude --worktree "#1234"` checks out `pull/1234/head`.

`.worktreeinclude` (gitignore syntax) copies gitignored files (`.env`, `.env.local`) into each new worktree.

In-conversation: ask Claude to "work in a worktree" — invokes the `EnterWorktree` tool. Subagent isolation: `isolation: worktree` in frontmatter — every invocation gets a throwaway worktree, removed if no changes.

Non-git VCS: register `WorktreeCreate` and `WorktreeRemove` hooks (docs show an SVN example).

**Adoption rec for the critic stack:** Add `.claude/worktrees/` to `.gitignore`. Create `.worktreeinclude` for local-only files. Decide consciously on `worktree.baseRef`: `"fresh"` for orthogonal-to-repo work (the default and right for the critic stack); `"head"` if your worktree work needs in-progress code. Dispatch via `claude agents`, not per-terminal `claude --worktree`.

**Anti-patterns.** Named worktrees in `-p` mode walked away from (not auto-cleaned). Sharing one worktree across multiple sessions.

### 1.15 Scheduled tasks: `/loop` and Routines

**`/loop` stable (v2.1.72+). Cloud Routines stable, separately.** ([Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks))

`/loop 5m check the deploy` — session-scoped cron, 7-day max. `/loop check the deploy` (no interval) — Claude self-paces, 1m–1h per iteration. `/loop` alone — built-in maintenance prompt; replaceable by `.claude/loop.md` or `~/.claude/loop.md`.

Under the hood: `CronCreate`, `CronList`, `CronDelete` tools. 5-field cron, local timezone, deterministic jitter, 50 tasks/session cap.

**Tiers:**

| | Cloud Routines | Desktop scheduled tasks | `/loop` |
| --- | --- | --- | --- |
| Where | Anthropic cloud | Your machine | Your machine, session-scoped |
| Machine on? | No | Yes | Yes |
| Open session? | No | No | Yes |
| Local files? | No | Yes | Yes |

**Adoption rec for the critic stack:** Schedule `canon-refresher` as a cloud Routine (no repo-state dependency). Use `/loop` for babysit-PR patterns if/when you adopt the upgrades-flow PR loop.

**Anti-patterns.** `/loop` for anything that must outlive the session. Forgetting `/loop` consumes quota per iteration.

### 1.16 Permission modes

**Stable. Auto mode is research preview.** ([Permission modes](https://code.claude.com/docs/en/permission-modes))

| Mode | What runs without asking |
| --- | --- |
| `default` | Reads only |
| `acceptEdits` | Reads + edits + common fs cmds (`mkdir`, `touch`, `mv`, `cp`, `rm`, `rmdir`, `sed`) within cwd/`additionalDirectories` |
| `plan` | Reads only; no edits |
| `auto` | Everything, with classifier safety (research preview; Max/Team/Enterprise/API, Opus 4.7 on Max) |
| `dontAsk` | Only pre-approved tools |
| `bypassPermissions` | Everything except `rm -rf /` and `rm -rf ~` |

**Protected paths** never auto-approve except in bypass: `.git`, `.vscode`, `.idea`, `.husky`, most of `.claude` (except `commands`, `agents`, `skills`, `worktrees`), `.gitconfig`, `.bashrc`, `.zshrc`, `.mcp.json`, `.claude.json`, etc.

**Auto mode classifier.** Separate model reviews every action. On entry, drops blanket `Bash(*)`, `Bash(python*)`, package-manager run rules, and `Agent` allow rules; restores on exit. Boundaries stated in conversation ("don't push") are honored until lifted, but lost on compaction — use deny rules for hard guarantees. Fallback: 3 consecutive blocks or 20 total → pause.

**Adoption rec for the critic stack:** Use `acceptEdits` as default for synthesis writing (steps 9, 12, 13). Use `dontAsk` for CI-side critic-panel runs. Don't enable `auto` for the orchestrator — too many workflow actions need explicit artifact confirmation.

**Anti-patterns.** Defaulting the *project* to `acceptEdits` (set in `settings.local.json`). Treating auto-mode classifier as sufficient safety.

### 1.17 Statusline

**Stable.** ([Statusline](https://code.claude.com/docs/en/statusline)) A shell script you configure receives session JSON on stdin and prints output. Multi-line supported.

**Adoption rec:** Two-line statusline — (1) model + effort + cwd-tail + git-branch, (2) context % + session-cost + current 12-step phase (read from session dir's most recently modified artifact). The phase indicator is the meaningful add when juggling 10 worktrees.

**Anti-patterns.** Slow scripts (run on every render). Unmemoized shell-out to git in a large repo.

### 1.18 Keybindings (`~/.claude/keybindings.json`)

**Stable (v2.1.18+).** ([Keybindings](https://code.claude.com/docs/en/keybindings)) Per-context map (`Global`, `Chat`, `Confirmation`, `Plugin`, `Scroll`, etc.), live reload, chord support. Reserved: Ctrl+C, Ctrl+D, Ctrl+M, Caps Lock.

Worth knowing: `chat:externalEditor` (Ctrl+G), `chat:stash` (Ctrl+S), `chat:killAgents` (Ctrl+X Ctrl+K), `app:toggleTodos` (Ctrl+T), `app:toggleTranscript` (Ctrl+O).

### 1.19 IDE integrations

**VS Code is the flagship, stable. JetBrains plugin runs the CLI in the IDE terminal.** ([VS Code](https://code.claude.com/docs/en/vs-code))

VS Code unlocks: checkpoints (rewind file edits / fork conversation), native diff viewer for proposed edits with inline editing, `@file:line` mentions (Option/Alt+K), `@terminal:<name>` to include terminal output, `@browser` (with Chrome extension) for browser automation, remote-session resume from claude.ai, plugin manager UI (`/plugins`), `vscode://anthropic.claude-code/open?prompt=...&session=...` URI handler.

CLI-only: `!` bash shortcut, tab completion, full skill/command roster.

**Adoption rec:** VS Code for orchestrator runs (diff viewer for `synthesis.md`). CLI for headless and the parallel-worktree fleet. They share transcripts — `claude --resume` picks up where extension left off.

**Anti-patterns.** Running both on the same session ID (interleaved writes). Confusing extension settings (`claudeCode.*`) with Claude Code settings (`~/.claude/settings.json`).

### 1.20 Multi-instance considerations

Two Claude Code processes in the same repo are fine if in different worktrees. They share: auto-memory directory, skill definitions, settings hierarchy, the supervisor process. They don't share: conversation context, in-session scheduled tasks, permission-mode state. For 10 parallel worktrees the constraint is rate limits and your machine's CPU/RAM, not Claude Code's design.

---

## 2. What's new in 2026 specifically

### 2.1 Opus 4.7 (April 16, 2026)

([What's new](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7), [Best practices with Claude Code](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code))

- **Adaptive thinking.** Model decides when to think and how much, per step, within session effort level. No fixed thinking budget on 4.7; `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` is ignored.
- **New effort level `xhigh`.** Default on Opus 4.7. Ladder: `low | medium | high | xhigh | max`. `max` is session-scoped, doesn't persist.
- **1M context** included with Max/Team/Enterprise; pay-as-you-go on API. Standard pricing past 200K.
- **128K max output tokens.**
- **High-res image input.**
- **Default model flip.** April 23, 2026: Enterprise pay-as-you-go and Anthropic API default flipped to Opus 4.7. Pin via `ANTHROPIC_MODEL` or `model` in server-managed settings.
- **Alias resolution.** On Anthropic API and Claude Platform on AWS, `opus` resolves to 4.7. On Bedrock/Vertex/Foundry, `opus` resolves to 4.6 unless pinned.
- **Requires Claude Code v2.1.111+.**

### 2.2 Other notable 2025–2026 changes

- **Plugins + marketplaces** as the standardized distribution unit.
- **Skills replaced custom slash commands** (legacy still works).
- **`.claude/rules/`** with path-scoped frontmatter — modular alternative to a single CLAUDE.md.
- **Auto-memory** — Claude writes its own notes (`MEMORY.md` + topic files); v2.1.59+.
- **Hooks lifecycle expansion** — PostToolBatch, TeammateIdle, Elicitation/Result, ConfigChange, CwdChanged, FileChanged, WorktreeCreate/Remove.
- **Agent view + supervisor process** — replaces tmux'ing multiple `claude` instances.
- **Channels** — MCP servers as push channels.
- **Auto permission mode** — classifier-gated autonomy (research preview).
- **Background monitors** in plugins — tail-style watchers that notify Claude.
- **LSP integration** in plugins for non-bundled languages.
- **Sandbox** for OS-level Bash isolation (separate from permissions).
- **Agent SDK CLI credit pool** (June 15, 2026) — `-p` and SDK split from interactive quota on subscriptions.
- **Keybindings file** (v2.1.18+) — per-context chord-capable rebinding.

---

## 3. Stability summary

| Surface | Status |
| --- | --- |
| Plugins, marketplaces, Skills, Hooks, MCP, Channels, Subagents | Stable |
| Custom slash commands | Deprecated for skills (still work) |
| Output styles, Settings, Memory, Plan mode | Stable |
| `run_in_background` + Monitor tool | Stable |
| Agent view + background sessions | Research preview |
| Headless `-p` / `--bare` | Stable (`--bare` future default) |
| OpenTelemetry | Stable (traces beta) |
| Worktrees + EnterWorktree/ExitWorktree | Stable |
| `/loop` + CronCreate/List/Delete, Routines | Stable |
| Permission modes (default/acceptEdits/plan/dontAsk/bypass) | Stable |
| Auto mode | Research preview |
| Statusline, Keybindings, VS Code, JetBrains | Stable |
| Adaptive thinking (Opus 4.7), Sandbox | Stable |

---

## 4. Top 10 adoption recommendations, ranked by leverage

For a 12-step adversarial-review stack about to scale to ~10 parallel worktrees:

1. **Dispatch worktrees through agent view, not terminals.** `claude agents` becomes the control plane. Add `.claude/worktrees/` to `.gitignore`; create `.worktreeinclude`. Single biggest enabler for the parallel target. ([Agent view](https://code.claude.com/docs/en/agent-view), [Worktrees](https://code.claude.com/docs/en/worktrees))
2. **Promote path-discipline from CLAUDE.md prose to a PreToolUse hook.** Hard-block Edit/Write when new content contains absolute path strings in markdown. The `path-check` skill is the human-invokable counterpart; the hook is AI-blind enforcement. ([Hooks](https://code.claude.com/docs/en/hooks))
3. **Pin `model: haiku` on `subagent-distiller`.** Distillation is short-in/short-out; Opus is wasted spend. ([Subagents](https://code.claude.com/docs/en/sub-agents))
4. **Build a custom "Adversarial reviewer" output style.** Match the don't-be-agreeable rules at system-prompt level. Run the critic stack with it; default for other work. ([Output styles](https://code.claude.com/docs/en/output-styles))
5. **Match effort to lens cost on Opus 4.7.** `xhigh` on critic lenses, `high` on librarian, `medium` on distiller. ([Model configuration](https://code.claude.com/docs/en/model-config))
6. **Wire OpenTelemetry to local Prometheus + Grafana.** Reconcile workflow-ledger cost ratios against actual API spend per session_id. Only way to validate the structure-tax. ([Monitoring](https://code.claude.com/docs/en/monitoring-usage))
7. **Use `--bare` for any CI-side critic-panel run.** Without it the run inherits whichever contributor's `~/.claude/` ran it. ([Headless](https://code.claude.com/docs/en/headless))
8. **Schedule `canon-refresher` as a cloud Routine.** Off-machine, off-session corpus candidate generation. ([Routines](https://code.claude.com/docs/en/routines))
9. **Convert the critic lenses + workflow agents to a private plugin once stable.** Versioned, namespaced, atomic updates across worktrees. Today is too early; in a month, after the lens roster settles. ([Plugins](https://code.claude.com/docs/en/plugins))
10. **Add `worktree.baseRef` to settings and a `WorktreeCreate` hook seeding env files.** Decide consciously between `"fresh"` (correct for a critic stack mostly orthogonal to repo state) and `"head"`. ([Worktrees](https://code.claude.com/docs/en/worktrees))

The non-recommendations matter too. The critic stack does not need: MCP (corpus is internal), Auto mode (workflow's structure depends on explicit gates), Bypass permissions (no containerized work), or the Chrome extension (no browser work). Resisting the temptation to adopt every shiny surface is itself a leverage move.

---

## Sources

Retrieved 2026-05-17:

- [Create plugins](https://code.claude.com/docs/en/plugins) · [Plugins reference](https://code.claude.com/docs/en/plugins-reference) · [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Hooks](https://code.claude.com/docs/en/hooks) · [Hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) · [Channels](https://code.claude.com/docs/en/channels)
- [Configure permissions](https://code.claude.com/docs/en/permissions) · [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) · [Sandboxing](https://code.claude.com/docs/en/sandboxing)
- [Settings](https://code.claude.com/docs/en/settings) · [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Output styles](https://code.claude.com/docs/en/output-styles)
- [Run Claude Code programmatically (Headless)](https://code.claude.com/docs/en/headless)
- [Monitoring (OpenTelemetry)](https://code.claude.com/docs/en/monitoring-usage)
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
- [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view)
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)
- [Customize your status line](https://code.claude.com/docs/en/statusline) · [Customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings)
- [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- [Model configuration](https://code.claude.com/docs/en/model-config) · [What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7) · [Best practices for Opus 4.7 with Claude Code](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code)
