# Claude Code Platform — Canonical Reference (2026)

A working reference to every primitive, surface, and configuration knob in Claude Code as of May 2026 that an advanced practitioner should know. Worktree-specific material is covered in a separate document.

Citations point at the live docs on `code.claude.com`, `docs.claude.com`, and `platform.claude.com`; all behavioral claims are sourced there. The current `code.claude.com` host is the canonical doc home — `docs.claude.com/en/docs/claude-code/*` URLs 301 to `code.claude.com/docs/en/*`.

---

## 1. The bundle: Plugins

A *plugin* is the unit of shareable Claude Code configuration. Anything you can drop into `.claude/` standalone — skills, agents, hooks, commands, MCP servers, LSP servers, monitors, settings, executables — can be packaged into a plugin and distributed through a marketplace.

### 1.1 Manifest

A plugin is any directory containing `.claude-plugin/plugin.json`. The manifest's required field is `name`; everything else is optional. `name` becomes the plugin's skill-namespace prefix (`/<plugin-name>:<skill>`), so plugin-shipped skills never collide ([plugins doc](https://code.claude.com/docs/en/plugins)).

```json
{
  "name": "my-plugin",
  "description": "Shown in the plugin manager",
  "version": "1.0.0",
  "author": {"name": "..."}
}
```

If `version` is omitted and the plugin is distributed via git, the commit SHA is treated as the version — every commit counts as a new release ([plugin manifest schema](https://code.claude.com/docs/en/plugins-reference#version-management)).

### 1.2 Directory layout

Only `plugin.json` belongs inside `.claude-plugin/`. Everything else lives at the plugin root ([plugins doc](https://code.claude.com/docs/en/plugins)):

| Directory       | Purpose                                                                       |
| --------------- | ----------------------------------------------------------------------------- |
| `skills/`       | Skills as `<name>/SKILL.md` directories                                       |
| `commands/`     | Legacy flat-file slash commands (use `skills/` for new work)                  |
| `agents/`       | Subagent markdown files                                                       |
| `hooks/`        | Event handlers in `hooks.json`                                                |
| `.mcp.json`     | MCP server configurations                                                     |
| `.lsp.json`     | LSP server configurations for code intelligence                               |
| `monitors/`     | Background monitor configurations in `monitors.json`                          |
| `bin/`          | Executables added to Bash `PATH` while the plugin is enabled                  |
| `settings.json` | Default settings applied when the plugin is enabled (only `agent` and `subagentStatusLine` keys are recognized) |
| `output-styles/`| Output styles shipped with the plugin                                         |

A plugin `settings.json` setting `agent: <name>` activates one of the plugin's custom agents as the *main thread*, overriding the system prompt, tool restrictions, and model for the session ([plugins doc](https://code.claude.com/docs/en/plugins#ship-default-settings-with-your-plugin)).

### 1.3 Install and load flow

Three install routes:

- `/plugin install <name>@<marketplace>` — pulls from a known marketplace (Anthropic's `claude-plugins-official`, or any git/URL/local marketplace you've added with `/plugin marketplace add <source>`).
- `claude --plugin-dir <path>` — loads a local directory directly; accepts a `.zip` since v2.1.128. Local plugins shadow installed plugins of the same name for that session.
- `claude --plugin-url <url>` — fetches a `.zip` archive (e.g., a CI build artifact) at startup; session-scoped only ([plugins doc](https://code.claude.com/docs/en/plugins#test-your-plugins-locally)).

`--plugin-dir`, `--plugin-url`, and `--mcp-config` can be repeated, or passed as a space-separated quoted argument. After editing a loaded plugin, `/reload-plugins` reapplies skills, agents, hooks, plugin MCP, and plugin LSP without restarting Claude Code.

`--plugin-dir` cannot override a plugin that managed settings force-enable or force-disable.

### 1.4 Marketplaces and trust

Marketplaces are git repos, URLs, or local directories that publish a catalog of plugins. Administrators can constrain what users may install via four managed-only keys ([permissions doc](https://code.claude.com/docs/en/permissions#managed-only-settings)):

- `strictKnownMarketplaces` — allowlist of marketplace sources the user can install from.
- `blockedMarketplaces` — checked before download, so blocked sources never touch the filesystem.
- `allowedChannelPlugins` — restricts which plugins can register as channel sources.
- `pluginTrustMessage` — custom message appended to the trust warning shown before installation.

---

## 2. Skills

Skills are markdown files Claude can use as procedural knowledge. They replaced custom slash commands in the 2025-2026 cycle: a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy`, but skills add a directory for supporting files, richer frontmatter, and auto-load semantics ([skills doc](https://code.claude.com/docs/en/skills)).

### 2.1 Where they live and live-reload

Resolution order, highest precedence first: enterprise (managed) → personal (`~/.claude/skills/`) → project (`.claude/skills/`). Plugin skills live under `<plugin>/skills/` and use a `plugin-name:skill-name` namespace, so they cannot conflict with non-plugin skills. When a skill and a legacy command share a name, the skill wins.

Claude Code watches `~/.claude/skills/`, `.claude/skills/`, and `--add-dir` directories' `.claude/skills/`; adding, editing, or removing a skill takes effect within the current session. Creating a *top-level* skills directory that didn't exist at session start requires a restart. Project skills also load from `.claude/skills/` in every parent directory up to repo root, and Claude discovers nested skills on demand (e.g., `packages/frontend/.claude/skills/` when editing a file in that subtree) ([skills doc, live change detection](https://code.claude.com/docs/en/skills#live-change-detection)).

### 2.2 Frontmatter (full)

```yaml
---
name: my-skill                # default: directory name
description: ...              # what + when. Combined with when_to_use, capped at 1,536 chars
when_to_use: ...              # trigger phrases / example requests
argument-hint: "[issue] [fmt]"
arguments: [issue, branch]    # named positional args; map to $issue, $branch
disable-model-invocation: true   # hide from auto-load; only the user can invoke
user-invocable: false            # hide from the / menu; only Claude can invoke
allowed-tools: Read Grep         # pre-approved tools while skill is active
model: opus                      # override session model for the rest of the turn
effort: xhigh                    # low | medium | high | xhigh | max
context: fork                    # run in a forked subagent context
agent: Explore                   # subagent type when context: fork
hooks: ...                       # skill-scoped hook block
paths:                           # glob-scoped auto-load
  - "src/api/**/*.ts"
shell: bash                      # bash (default) or powershell
---
```

All fields are optional; only `description` is recommended ([skills frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)).

### 2.3 Substitutions

| Token                  | Meaning                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | Full arg string. If absent in the body, args are appended as `ARGUMENTS: <value>`.          |
| `$ARGUMENTS[N]` / `$N` | 0-based positional access. Shell-style quoting: `/skill "hello world" two` → `$0`=`hello world`. |
| `$<name>`              | Named positional from the `arguments:` frontmatter list.                                    |
| `${CLAUDE_SESSION_ID}` | Current session ID.                                                                         |
| `${CLAUDE_EFFORT}`     | Current effort level (`low`..`max`).                                                        |
| `${CLAUDE_SKILL_DIR}`  | Skill's own directory — use to reference bundled scripts regardless of CWD.                 |

### 2.4 Dynamic context injection

`` !`<command>` `` (inline) and a fenced block opened with ` ```! ` (multi-line) run shell commands *before* the skill body reaches Claude. Output replaces the placeholder; Claude sees the rendered prompt only. Set `disableSkillShellExecution: true` to neutralize this for user/project/plugin/add-dir skills (bundled and managed skills are unaffected) — most useful as a managed-settings policy ([skills, dynamic context](https://code.claude.com/docs/en/skills#inject-dynamic-context)).

### 2.5 Skill content lifecycle

When invoked, the rendered `SKILL.md` enters the conversation as one message and stays for the rest of the session — Claude Code does not re-read the file on later turns, so write standing instructions, not one-time steps. Auto-compaction re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each, with a 25,000-token combined budget across all re-attached skills, filled most-recent-first ([skill content lifecycle](https://code.claude.com/docs/en/skills#skill-content-lifecycle)).

### 2.6 Listing budget

Skill *descriptions* (not bodies) load at session start so Claude knows what's available. The budget is 1% of the model's context window by default; raise via `skillListingBudgetFraction` (e.g., `0.02`) or `SLASH_COMMAND_TOOL_CHAR_BUDGET` (fixed char count). Per-entry cap is 1,536 chars (`maxSkillDescriptionChars`). When the budget overflows, descriptions for least-invoked skills are dropped first. Run `/doctor` to see whether the budget is overflowing ([skill descriptions cut short](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short)).

### 2.7 Decision rule: skill vs slash command vs subagent

- **Skill** when the work is procedural, fits in one context, and is invoked by the model based on description matching.
- **Subagent** when the work would flood context with search results, logs, or file contents you won't reference again — the subagent does that work in its own context window and returns only the summary.
- **Custom slash command** — deprecated as a separate primitive; use a skill with `disable-model-invocation: true` for user-only manual triggers ([skills note on commands](https://code.claude.com/docs/en/skills)).

### 2.8 `skillOverrides` from settings

Control visibility per-skill from settings without editing `SKILL.md` (useful for shared-repo skills you don't own):

```json
{"skillOverrides": {"legacy-context": "name-only", "deploy": "off"}}
```

Values: `on | name-only | user-invocable-only | off`. The `/skills` menu writes this for you (`Space` cycles, `Enter` saves to `.claude/settings.local.json`). Plugin skills are not affected — manage those through `/plugin` ([skill overrides](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings)).

---

## 3. Subagents

Subagents are markdown files at `.claude/agents/<name>.md` (project), `~/.claude/agents/` (user), or `<plugin>/agents/` (plugin). They run in their own context window with their own system prompt, tools, model, permissions, and (optionally) worktree isolation ([subagents doc](https://code.claude.com/docs/en/sub-agents)).

### 3.1 Frontmatter

```yaml
---
description: ...        # what + when; Claude uses this to decide when to delegate
tools: Read, Grep, Bash # comma- or space-separated allowlist
model: haiku            # routes to cheaper model for grunt work
permissionMode: plan    # default | acceptEdits | plan | auto | dontAsk | bypassPermissions
effort: high
skills: [path-check, ledger-render]   # preloaded into subagent's context at startup
color: green            # row color in agent view
isolation: worktree     # always run in its own .claude/worktrees/ checkout
---
```

`skills` here is the inverse of a skill with `context: fork`: with `skills`, the subagent's markdown body is the system prompt and Claude's delegation message is the task; preloaded skill bodies + CLAUDE.md ride along. With `context: fork` on a skill, the agent type's system prompt drives, and the skill body is the task ([skills, run in subagent](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent)).

### 3.2 When subagent beats skill (and vice versa)

Subagent when:
- The task generates throwaway intermediate output (file lists, grep results, fetched pages) you don't want in your main context.
- You want a *different* model or permission mode for one phase (e.g., Haiku for a search pass).
- You want isolation in a worktree.

Skill when:
- The procedural knowledge is short, you want the result in your main thread, and you'd lose value by summarizing.
- The instructions need to remain "standing" across multiple turns of the same conversation.

---

## 4. Hooks

Hooks are shell commands (or HTTP endpoints) registered in `settings.json` or a plugin's `hooks/hooks.json`. They fire on lifecycle events and can read a JSON payload on stdin, write JSON or text on stdout, and signal control via exit codes ([hooks doc](https://code.claude.com/docs/en/hooks)).

### 4.1 The 2026 event roster

| # | Event                  | Lifecycle                                          | Blocking? | Matcher                                                                                       |
| - | ---------------------- | -------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------- |
| 1 | `SessionStart`         | Session begins or resumes                          | No        | `startup` / `resume` / `clear` / `compact`                                                    |
| 2 | `Setup`                | `--init-only` or `-p --init/--maintenance`         | No        | `init` / `maintenance`                                                                        |
| 3 | `UserPromptSubmit`     | User submits prompt                                | Yes       | none                                                                                          |
| 4 | `UserPromptExpansion`  | Slash command expands                              | Yes       | command name                                                                                  |
| 5 | `PreToolUse`           | Before a tool executes                             | Yes       | tool name                                                                                     |
| 6 | `PermissionRequest`    | Permission dialog appears                          | Yes       | tool name                                                                                     |
| 7 | `PermissionDenied`     | Tool auto-denied by the classifier                 | No        | tool name                                                                                     |
| 8 | `PostToolUse`          | After a tool succeeds                              | No        | tool name                                                                                     |
| 9 | `PostToolUseFailure`   | After a tool fails                                 | No        | tool name                                                                                     |
| 10| `PostToolBatch`        | Parallel batch resolves                            | Yes       | none                                                                                          |
| 11| `Notification`         | Notification emitted                               | No        | notification type                                                                             |
| 12| `SubagentStart`        | Subagent spawned                                   | No        | agent type                                                                                    |
| 13| `SubagentStop`         | Subagent finishes                                  | Yes       | agent type                                                                                    |
| 14| `TaskCreated`          | Task created via TaskCreate                        | Yes       | none                                                                                          |
| 15| `TaskCompleted`        | Task marked complete                               | Yes       | none                                                                                          |
| 16| `Stop`                 | Claude finishes responding                         | Yes       | none                                                                                          |
| 17| `StopFailure`          | Turn ends due to API error                         | No        | `rate_limit` / `authentication_failed` / `oauth_org_not_allowed` / `billing_error` / `invalid_request` / `server_error` / `max_output_tokens` / `unknown` |
| 18| `TeammateIdle`         | Agent-teams teammate about to idle                 | Yes       | none                                                                                          |
| 19| `InstructionsLoaded`   | CLAUDE.md or `.claude/rules/*.md` loaded           | No        | `session_start` / `nested_traversal` / `path_glob_match` / `include` / `compact`              |
| 20| `ConfigChange`         | Settings file changes                              | Yes (except `policy_settings`) | `user_settings` / `project_settings` / `local_settings` / `policy_settings` / `skills` |
| 21| `CwdChanged`           | Working directory changes                          | No        | none                                                                                          |
| 22| `FileChanged`          | Watched file changes                               | No        | literal filenames                                                                             |
| 23| `WorktreeCreate`       | Worktree created via `--worktree`                  | Yes       | none                                                                                          |
| 24| `WorktreeRemove`       | Worktree removed                                   | No        | none                                                                                          |
| 25| `PreCompact`           | Before context compaction                          | Yes       | `manual` / `auto`                                                                             |
| 26| `PostCompact`          | After compaction completes                         | No        | `manual` / `auto`                                                                             |
| 27| `Elicitation`          | MCP server requests user input                     | Yes       | MCP server name                                                                               |
| 28| `ElicitationResult`    | User responds to MCP elicitation                   | Yes       | MCP server name                                                                               |
| 29| `SessionEnd`           | Session terminates                                 | No        | `clear` / `resume` / `logout` / `prompt_input_exit` / `bypass_permissions_disabled` / `other` |

### 4.2 Stdin payload shape (common fields)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "...",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "hook_event_name": "EventName",
  "effort": {"level": "low|medium|high|xhigh|max"},
  "agent_id": "...",        // subagents only
  "agent_type": "Explore"   // subagents or --agent
}
```

For tool events, `tool_name`, `tool_input` (Bash: `command`, `description`, `timeout`, `run_in_background`; Write: `file_path`, `content`; Edit: `file_path`, `old_string`, `new_string`, `replace_all`; Read: `file_path`, `offset`, `limit`; etc.), and `tool_use_id` are appended.

### 4.3 Exit-code semantics

| Exit | Meaning                                                                                                  |
| ---- | -------------------------------------------------------------------------------------------------------- |
| `0`  | JSON on stdout is parsed; for `SessionStart`/`UserPromptSubmit`/`UserPromptExpansion`, stdout becomes context; for others, stdout goes to the debug log. |
| `2`  | Blocking error. Stderr is fed back to Claude as an error message. JSON ignored. Behavior per event (see below). |
| other| Non-blocking error. Transcript shows `<hook> hook error` plus the first stderr line; full stderr in debug log. |

Exit-2 *blocks* on: `PreToolUse` (block tool call), `PermissionRequest` (deny), `UserPromptSubmit` (erase prompt), `UserPromptExpansion`, `Stop`/`SubagentStop` (prevent stop), `TeammateIdle`, `TaskCreated` (roll back), `TaskCompleted`, `ConfigChange` (except `policy_settings`), `PostToolBatch` (stop agentic loop), `PreCompact`, `Elicitation`, `ElicitationResult`, `WorktreeCreate`. Exit-2 is *not* blocking on `PostToolUse`/`PostToolUseFailure` (stderr shown to Claude only), `PermissionDenied`, `StopFailure`, or any of the pure-observability events.

### 4.4 JSON control protocol

Universal fields on stdout:

```json
{
  "continue": true,
  "stopReason": "...",
  "suppressOutput": false,
  "systemMessage": "...",
  "terminalSequence": "]777;notify;Title;Body",
  "hookSpecificOutput": {
    "hookEventName": "...",
    "additionalContext": "..."
  }
}
```

Per-event extensions:

- **`PreToolUse`** — `hookSpecificOutput.permissionDecision: allow|deny|ask|defer`, `permissionDecisionReason`, `modifiedInput` (rewrite tool input before execution), `additionalContext`.
- **`PermissionRequest`** — `hookSpecificOutput.decision: {behavior: allow|deny, updatedInput, rules}` to auto-allow/deny and optionally persist a rule.
- **`PermissionDenied`** — `hookSpecificOutput.retry: true` is the only meaningful field.
- **`PostToolUse`/`PostToolUseFailure`** — `decision: "block"` prevents Claude from continuing.
- **`UserPromptSubmit`** — `decision: "block"` plus `hookSpecificOutput.sessionTitle` (auto-set session name) and `additionalContext`.
- **`Elicitation`/`ElicitationResult`** — `hookSpecificOutput.action: accept|decline|cancel`, `content: {...}` form values.
- **`WorktreeCreate`** — print path on stdout, or return `hookSpecificOutput.worktreePath`. Any non-zero exit fails creation.

Allowlisted terminal escape sequences: OSC 0, 1, 2, 9, 99, 777; BEL.

### 4.5 AI-blind hooks

Set `suppressOutput: true` to omit stdout from the debug log and never surface to Claude. Use for telemetry, lint-and-fix loops, or anything the model doesn't need to see. Pair with `decision: "block"` to deterministically force a behavior without telling Claude why.

### 4.6 Special env vars in hooks

`CLAUDE_ENV_FILE` is available in `SessionStart`, `Setup`, `CwdChanged`, and `FileChanged`. Writing `export KEY=val` lines to it persists env vars into the session.

---

## 5. MCP

Claude Code is a first-class MCP client. Servers are configured at three scopes: user (`~/.claude.json`), project (`.mcp.json`, committed), and local (`~/.claude.json`, per-machine). Transports: **stdio**, **Streamable HTTP** (the current recommended remote transport), and **SSE** (deprecated; servers should migrate to Streamable HTTP) ([MCP doc](https://code.claude.com/docs/en/mcp)).

Add servers with `claude mcp add` (stdio) or `claude mcp add --transport http <name> <url>` plus `--header` for auth. Manage at runtime with `/mcp`.

Permission syntax — `mcp__<server>` matches any tool from a server, `mcp__<server>__<tool>` matches one tool, `mcp__<server>__*` is wildcard. MCP tools follow the same `allow`/`ask`/`deny` rule precedence as built-in tools ([permissions, MCP](https://code.claude.com/docs/en/permissions#mcp)).

Managed-only keys: `allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`.

### 5.1 The bundled `ide` MCP server

The VS Code extension runs a local MCP server bound to `127.0.0.1` on a random high port, with a fresh per-activation auth token written to `~/.claude/ide/` with `0600` perms in a `0700` directory. It's hidden from `/mcp` because there's nothing to configure. Only two tools reach the model — the rest are internal RPC for diff/selection/save UI ([VS Code, the built-in IDE MCP server](https://code.claude.com/docs/en/vs-code#the-built-in-ide-mcp-server)):

| Tool                       | Behavior                                                                                  |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| `mcp__ide__getDiagnostics` | Returns language-server errors/warnings from the Problems panel; optionally scoped to one file. Read-only. |
| `mcp__ide__executeCode`    | Inserts code as a new cell at the end of the active Jupyter notebook, scrolls into view, and shows a native Quick Pick **Execute / Cancel**. Cancelling returns an error. Refuses when no notebook is active, when the Jupyter extension isn't installed, or when the kernel isn't Python. |

The Quick Pick is independent of `PreToolUse` hooks: an allowlist lets Claude *propose* execution; the Quick Pick is what lets it *actually* run.

### 5.2 Channels — MCP that pushes to you

Channels are MCP servers that push events into a running session, rather than waiting to be polled. Built-in plugin examples: Telegram, Discord, iMessage, and the localhost `fakechat` demo. Required: Anthropic auth (claude.ai or Console API key), not available on Bedrock/Vertex/Foundry; v2.1.80+. Enable with `claude --channels plugin:<name>@<marketplace>` ([channels doc](https://code.claude.com/docs/en/channels)).

Org controls (managed-only): `channelsEnabled` (master switch — default off for Team/Enterprise, default on for Console with API auth), `allowedChannelPlugins` (allowlist that replaces Anthropic's default list when set). Each channel maintains a sender allowlist established by pairing.

A channel can also *relay permission prompts* (capability declared by the server), so an allowlist sender can approve or deny tool use remotely. Treat allowlist membership as authorization-to-approve.

---

## 6. Settings + permissions

### 6.1 Precedence

Highest-to-lowest ([settings doc](https://code.claude.com/docs/en/settings)):

1. **Managed** — server-managed, MDM/OS-level (macOS plist, Windows registry HKLM/HKCU), or file-based (`managed-settings.json` plus drop-in `managed-settings.d/`).
2. **Command-line flags** — session-only.
3. **Local** — `.claude/settings.local.json` (gitignored).
4. **Project** — `.claude/settings.json` (committed).
5. **User** — `~/.claude/settings.json`.
6. **Defaults**.

Drop-in `managed-settings.d/` files sort alphabetically; scalars override later, arrays concatenate and dedupe, objects deep-merge. Use numeric prefixes (`10-`, `20-`) to control order.

A managed `policyHelper.path` (v2.1.136+) lets an admin-deployed executable compute managed settings dynamically at startup. `parentSettingsBehavior` (v2.1.133+) controls how SDK/IDE-supplied settings interact with managed: `first-wins` (default) or `merge` (parent can tighten but not loosen).

### 6.2 Permission rule merge

Permission rules **merge across scopes**; they don't override. Evaluation order is always **deny → ask → allow**, first match wins. Managed-only keys: `allowManagedPermissionRulesOnly` (when `true`, user/project settings cannot define `allow`/`ask`/`deny`).

### 6.3 Notable 2026 keys

- `effortLevel` — `low | medium | high | xhigh` (`max` doesn't persist via settings; use the env var to persist).
- `alwaysThinkingEnabled` — extended thinking on by default.
- `autoMemoryEnabled` (default `true`) and `autoMemoryDirectory` (absolute or `~/`; accepted only from managed/user, never project/local, because project files in a clone could redirect writes to sensitive locations).
- `skillListingBudgetFraction` (default `0.01`), `maxSkillDescriptionChars` (default `1536`), `skillOverrides`, `disableSkillShellExecution`.
- `claudeMd` (managed-only: organization-managed memory text injected as an instruction).
- `claudeMdExcludes` — glob patterns to skip ancestor CLAUDE.md files (most useful in monorepos).
- `sandbox.{filesystem, network, enabled, failIfUnavailable, autoAllowBashIfSandboxed, excludedCommands, enableWeakerNestedSandbox, enableWeakerNetworkIsolation}` — see §10.
- `disableAgentView`, `disableAutoMode`, `disableBypassPermissionsMode` — kill switches; effective at any scope but typically deployed via managed.

### 6.4 Path anchors (Read/Edit/Write)

Read/Edit rules use gitignore semantics with four anchor types ([permissions, read/edit](https://code.claude.com/docs/en/permissions#read-and-edit)):

| Pattern         | Anchor                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| `//path`        | Absolute, from filesystem root                                                                          |
| `~/path`        | Home directory                                                                                          |
| `/path`         | **Project root** — *not* an absolute path. The single-slash form is the most common foot-gun.           |
| `path`, `./path`| Current working directory                                                                               |

On Windows, paths normalize to POSIX (`C:\Users\alice` → `/c/Users/alice`), so `//c/**/.env` reaches a `.env` anywhere on the C drive. `//**/.env` reaches all drives.

A bare filename matches at any depth (gitignore behavior): `Read(.env)` and `Read(**/.env)` are equivalent. Symlinks check both the link path and the resolved target — allow rules require both to match, deny rules block when *either* matches.

**Sandbox path anchors differ**: in `sandbox.*`, `/path` *is* absolute. The older `//path` still works there for backward compatibility, but new sandbox configs should use `/` for absolute, `./` or bare for project-relative (or `~/.claude` if the setting lives in user settings).

### 6.5 Bash specifier matching — the gotchas

`*` matches at any position, including spans across arguments. The **space before `*` is load-bearing**: `Bash(ls *)` enforces a word boundary (`ls -la` matches, `lsof` doesn't); `Bash(ls*)` doesn't (both match). `:*` at end is equivalent to ` *`.

**Process wrappers** Claude strips before matching: `timeout`, `time`, `nice`, `nohup`, `stdbuf`. Bare `xargs` (no flags) is also stripped. **Not stripped**: `direnv exec`, `devbox run`, `mise exec`, `npx`, `docker exec` — a rule like `Bash(devbox run *)` matches *anything* after `run`, including `devbox run rm -rf .`. Always pair the runner with the inner command: `Bash(devbox run npm test)`.

**Always prompt regardless of prefix rules**: `watch`, `setsid`, `ionice`, `flock`, `find -exec`, `find -delete`. Write exact-match rules to approve specific invocations.

**Compound commands** split on `&&`, `||`, `;`, `|`, `|&`, `&`, newlines. Each subcommand is matched independently against rules; when you accept "Yes, don't ask again" for a compound, Claude saves up to 5 rules — one per subcommand — rather than one rule for the full string.

**Read-only allowlist (not configurable)**: `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd`, plus read-only `git` forms. These run without prompting in every mode. Add `ask` or `deny` rules to require prompts.

PowerShell rules use the same shape; aliases are canonicalized (`gci`/`ls`/`dir` all match `PowerShell(Get-ChildItem *)`), matching is case-insensitive, and PowerShell 7+ chain operators `&&`/`||` split compounds.

### 6.6 Permission modes

| Mode                | Behavior                                                                                                                |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `default`           | Prompt on first use of each tool.                                                                                       |
| `acceptEdits`       | Auto-accept file edits and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`) inside cwd or `additionalDirectories`. |
| `plan`              | Read-only exploration; no source edits.                                                                                 |
| `auto`              | Auto-approve with background classifier safety checks (research preview).                                               |
| `dontAsk`           | Auto-deny unless pre-approved.                                                                                          |
| `bypassPermissions` | Skip prompts. **Circuit breaker**: `rm -rf /` and `rm -rf ~` still prompt. Writes to `.git`, `.claude`, `.vscode`, `.idea`, `.husky` are *not* blocked. Lock down with `permissions.disableBypassPermissionsMode: "disable"`. |

`auto` and `bypassPermissions` are refused when dispatching a background session until you've accepted that mode interactively once.

---

## 7. Memory

### 7.1 CLAUDE.md hierarchy

Loaded broadest → most specific ([memory doc](https://code.claude.com/docs/en/memory)):

1. Managed: `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux/WSL), `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows). Cannot be excluded.
2. User: `~/.claude/CLAUDE.md`.
3. Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`.
4. Local: `./CLAUDE.local.md` (gitignore this).

All discovered files are concatenated, ordered filesystem-root-down; within a directory, `CLAUDE.local.md` is appended after `CLAUDE.md`. Files in *subdirectories* below cwd load lazily — only when Claude reads files in that subtree. After `/compact`, project-root CLAUDE.md is re-injected from disk; nested CLAUDE.md reloads next time Claude touches that subdirectory.

`@path/to/file` imports expand at launch; max 5 hops; first-time external imports show an approval dialog that, if declined, disables future external imports silently.

Block-level HTML comments (`<!-- ... -->`) are stripped before injection — use for human-only notes. Comments inside code blocks are preserved. When the file is read with the Read tool, comments stay visible.

### 7.2 `.claude/rules/`

Modular alternative for large projects. `.md` files in `.claude/rules/` (recursively, including subdirectories) load alongside CLAUDE.md. Symlinks are supported and circular symlinks are detected. The killer feature is `paths:` frontmatter for glob-scoped activation:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
```

Rules with no `paths:` load unconditionally. Path-scoped rules trigger when Claude *reads files matching the pattern*, not on every tool use ([memory, organize rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)).

### 7.3 Auto-memory

Per-project memory directory at `~/.claude/projects/<project>/memory/` (derived from the git repo root; all worktrees share one directory). The first 200 lines or 25KB (whichever comes first) of `MEMORY.md` load at session start. Topic files (`debugging.md`, `patterns.md`, etc.) are not loaded at startup — Claude reads them on demand. Override location via `autoMemoryDirectory` (managed/user only) ([memory, auto-memory](https://code.claude.com/docs/en/memory#auto-memory)).

Toggle via `/memory`, `autoMemoryEnabled: false`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Requires v2.1.59+.

Subagents can maintain their own auto-memory (see [`sub-agents#enable-persistent-memory`](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory)).

### 7.4 `claudeMdExcludes`

Glob exclusions against absolute paths; arrays merge across scopes; cannot exclude managed-policy CLAUDE.md. Most useful in `.claude/settings.local.json` for "skip the other team's CLAUDE.md" in a monorepo.

---

## 8. Operating surfaces

### 8.1 Plan mode

Cycle permission mode with `Shift+Tab`. `/plan <prompt>` (alias for plan-mode entry) and `--permission-mode plan` start in plan. The plan-acceptance dialog offers Accept (execute), Reject, or Edit the plan. `Ctrl+G` opens the prompt buffer in `$EDITOR`. Accepting a plan auto-names the resulting session.

The `opusplan` model alias runs Opus during plan mode and switches to Sonnet at execution. The Opus phase uses the **standard 200K context** — the 1M auto-upgrade does *not* extend to `opusplan` ([model-config, opusplan](https://code.claude.com/docs/en/model-config#opusplan-model-setting)).

### 8.2 Background sessions and agent view

`claude agents` opens the TUI. New sessions: `claude --bg "..."`, `/bg` inside a running session, or `←` on an empty prompt to background-and-open agent-view in one step. State icons: animated (working), yellow (needs input), dim (idle), green (completed), red (failed), grey (stopped). Process shape: `✻`/`✽` (alive), `∙` (process exited but state preserved), `✢` (`/loop` sleeping) ([agent view doc](https://code.claude.com/docs/en/agent-view)).

A per-user **supervisor process** hosts background sessions, separate from your terminal and from agent view itself. Sessions survive supervisor auto-update restarts (file watch on the binary). They do *not* survive sleep/shutdown — `claude respawn --all` after waking. Once a session finishes and sits unattached for ~1 hour, the supervisor stops its process to free resources; attaching restarts it from saved state.

Storage:
- `~/.claude/daemon.log` — supervisor log.
- `~/.claude/daemon/roster.json` — running session list.
- `~/.claude/jobs/<id>/state.json` — per-session state.

If `CLAUDE_CONFIG_DIR` is set, the supervisor runs a separate instance with its own sessions.

Every background session, by default, edits files inside a `.claude/worktrees/<id>/` git worktree (so parallel sessions don't clobber each other). Outside a git repo, sessions share the cwd. The worktree is removed when the session is deleted — push or commit first.

CLI: `claude attach <id>`, `claude logs <id>`, `claude stop <id>` (alias `kill`), `claude respawn <id>` / `--all`, `claude rm <id>`. Filter the view with `a:<agent>`, `s:<state>`/`s:blocked`, `#<pr>`, or a PR URL.

Long runs benefit from `caffeinate -d -i claude --bg "..."` on macOS — keeps the display *and* idle sleep suppressed while the background session works.

This is distinct from `run_in_background: true` on a single Bash call (which streams output asynchronously inside the same conversation) and from subagents (which run a single tool-call's worth of work in their own context window inside the same conversation).

Kill switches: `disableAgentView: true` setting or `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` env var. Pass `--permission-mode`, `--model`, `--effort` to `claude agents` (v2.1.142+) to set defaults for everything dispatched from that view.

### 8.3 Headless mode

`claude -p "<prompt>"` runs non-interactively. `--bare` (future default; flags TBD on full release) shorthand strips ceremony. `--output-format`: `text` (default), `json`, `stream-json`. `--json-schema` constrains structured output.

Stream-JSON event types:
- `system/init` — session id, model, working dir, available tools.
- `system/api_retry` — retry attempt with backoff info.
- `stream_event` — Anthropic SDK message stream events (`message_start`, `content_block_*`, `message_delta`, `message_stop`).
- `system/plugin_install` — plugin activation messages.

Stdin payload cap is 10 MB. `--allowedTools` scopes which tools the headless run may invoke.

**Agent SDK credit pool split**: per Anthropic's developer announcement, starting **June 15, 2026**, Agent SDK consumption is metered against a separate pool from interactive Claude Code consumption, so headless automation no longer competes with developer-seat quota. Plan rollouts accordingly.

### 8.4 OpenTelemetry

`CLAUDE_CODE_ENABLE_TELEMETRY=1` enables export. Exporters: `OTEL_METRICS_EXPORTER` (`otlp | prometheus | console | none`), `OTEL_LOGS_EXPORTER` (`otlp | console | none`). Standard OTLP env vars apply: `OTEL_EXPORTER_OTLP_PROTOCOL` (`grpc` or `http/protobuf`), `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_HEADERS`. Defaults: 60s metric export interval, 5s log export interval — lower (`OTEL_METRIC_EXPORT_INTERVAL=10000`) for debugging. GenAI semantic-conventions attributes (`gen_ai.*`) are emitted ([monitoring doc](https://code.claude.com/docs/en/monitoring-usage)).

### 8.5 Scheduled tasks

Three tiers ([scheduled-tasks doc](https://code.claude.com/docs/en/scheduled-tasks)):

|                            | Cloud (Routines)             | Desktop scheduled tasks                | `/loop`                              |
| -------------------------- | ---------------------------- | -------------------------------------- | ------------------------------------ |
| Runs on                    | Anthropic cloud              | Your machine                           | Your machine                         |
| Requires machine on        | No                           | Yes                                    | Yes                                  |
| Requires open session      | No                           | No                                     | Yes                                  |
| Persistent across restarts | Yes                          | Yes                                    | Restored via `--resume` if unexpired |
| Access to local files      | No (fresh clone)             | Yes                                    | Yes                                  |
| MCP servers                | Connectors per task          | Config files / connectors              | Inherits from session                |
| Permission prompts         | None (autonomous)            | Configurable per task                  | Inherits from session                |
| Min interval               | 1 hour                       | 1 minute                               | 1 minute                             |

`/loop` patterns:
- `/loop 5m <prompt>` — fixed cron interval (seconds round up to nearest minute; non-clean intervals round to nearest cron step).
- `/loop <prompt>` — **self-paced**: Claude picks 1m–1h delay each iteration based on observations, printing the chosen delay and its reason. May also drop into the **Monitor tool** to stream lines from a background script instead of polling.
- `/loop` — runs `.claude/loop.md` (project) or `~/.claude/loop.md` (user), or a built-in maintenance prompt if neither exists. The maintenance prompt continues unfinished work, tends the current branch's PR, then runs cleanup passes.

Tools: `CronCreate`, `CronList`, `CronDelete`. Cap: **50 tasks per session**. **7-day expiry** on recurring tasks (one final fire, then self-delete). One-shots delete themselves after firing.

Jitter: recurring tasks fire up to 30 minutes after the scheduled time (or half-interval for sub-hourly); one-shots scheduled for `:00`/`:30` fire up to 90 seconds early. Pick `:03` etc. if exact timing matters.

Kill switch: `CLAUDE_CODE_DISABLE_CRON=1`.

### 8.6 Statusline

A shell script you configure that receives session JSON on stdin and writes to stdout. Multi-line supported (use `\n` in output). Useful for context usage, cost, git branch, session id. See [statusline doc](https://code.claude.com/docs/en/statusline) for the JSON shape and example scripts.

### 8.7 Keybindings

`~/.claude/keybindings.json`, edited via `/keybindings`. Live-reloaded on file change. Per-context maps: `Global`, `Chat`, `Autocomplete`, `Settings`, `Confirmation`, `Tabs`, `Help`, `Transcript`, `HistorySearch`, `Task`, `ThemePicker`, `Attachments`, `Footer`, `MessageSelector`, `DiffDialog`, `ModelPicker`, `Select`, `Plugin`, `Scroll`, `Doctor` ([keybindings doc](https://code.claude.com/docs/en/keybindings)).

Modifiers: `ctrl`, `shift`, `alt`/`opt`/`option`/`meta`, `cmd`/`command`/`super`/`win` (the `cmd` group only resolves in terminals reporting Super — Kitty keyboard protocol or xterm `modifyOtherKeys`; most don't). Chords are space-separated: `ctrl+k ctrl+s`. Unbind with `null`. Uppercase letters imply Shift (`K` ≡ `shift+k`) *only* when bare — `ctrl+K` does *not* imply Shift.

Reserved (cannot rebind): `Ctrl+C`, `Ctrl+D`, `Ctrl+M` (terminals send CR for both Enter and `Ctrl+M`), Caps Lock. Terminal-multiplexer conflicts: `Ctrl+B` (tmux), `Ctrl+A` (screen), `Ctrl+Z` (SIGTSTP).

Requires v2.1.18+. Run `/doctor` to see binding validation warnings.

### 8.8 IDE integrations

**VS Code** ([vs-code doc](https://code.claude.com/docs/en/vs-code)):
- Native diff viewer for proposed edits (you can edit in the diff before accepting; Claude is told you modified it).
- Checkpoints — hover any message → rewind options: fork conversation, rewind code, or both.
- `@file:line` ranges via `Option+K`/`Alt+K`; `@terminal:<name>` to feed a terminal's output back into a prompt; `@browser` to drive a connected Chrome (requires the Claude in Chrome extension v1.0.36+).
- Resume remote sessions from claude.ai (Subscription auth only; only GitHub-repo-backed remote sessions appear in the Remote tab).
- `/plugins` UI for browsing, installing, scoping (user/project/local), and managing marketplaces — shares state with the CLI.
- `vscode://anthropic.claude-code/open?prompt=...&session=...` URI handler — `prompt` pre-fills (not auto-submitted); `session` must belong to the open workspace.

**JetBrains** integration is also available; similar diff and `@`-mention behavior.

### 8.9 Output styles

Modify Claude's system prompt directly. Built-ins ([output-styles doc](https://code.claude.com/docs/en/output-styles)):

- **Default** — standard software-engineering instructions.
- **Proactive** — make reasonable assumptions, prefer action over planning (same guidance as auto mode, without changing your permission mode).
- **Explanatory** — interleave "Insights" while coding.
- **Learning** — collaborative; inserts `TODO(human)` markers for you to implement.

Custom styles at `~/.claude/output-styles/`, `.claude/output-styles/`, or managed. Frontmatter: `name`, `description`, `keep-coding-instructions` (default `false` — set `true` if you're changing communication style but still coding), `force-for-plugin` (plugin styles only; applies automatically when the plugin is enabled, overriding the user's `outputStyle` — first loaded plugin wins on collision).

Output style is set in the system prompt at session start, so changes take effect on the next session (keeps prompt caching intact within a session).

### 8.10 Custom slash commands (legacy)

Deprecated as a distinct primitive in favor of skills. `.claude/commands/foo.md` still works and supports the same frontmatter as skills; a same-named skill wins. No new development should target this layer.

---

## 9. Models and thinking

### 9.1 Opus 4.7 (April 16, 2026)

Capabilities ([model-config doc](https://code.claude.com/docs/en/model-config)):
- **Adaptive thinking** is the only mode. 4.7 rejects manual `MAX_THINKING_TOKENS` budgets and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`.
- New effort level `xhigh` (only on 4.7); ladder is `low | medium | high | xhigh | max`.
- 1M context window (auto-upgraded on Max/Team/Enterprise plans, no extra config).
- 128K output tokens.
- High-resolution image input.
- Default model **flipped to Opus 4.7 on April 23, 2026** for Enterprise pay-as-you-go and Anthropic API users.
- Requires Claude Code **v2.1.111 or later** (`claude update`).

### 9.2 Alias resolution

| Alias    | Anthropic API / Claude Platform on AWS | Bedrock / Vertex / Foundry |
| -------- | -------------------------------------- | -------------------------- |
| `opus`   | Opus 4.7                               | Opus 4.6                   |
| `sonnet` | Sonnet 4.6                             | Sonnet 4.5                 |
| `haiku`  | latest Haiku                           | latest Haiku               |
| `best`   | equivalent to `opus`                   | equivalent to `opus`       |

Pin in third-party deployments via `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Append `[1m]` to enable 1M context (`claude-opus-4-7[1m]`). Use `modelOverrides: {}` settings for per-version routing to specific Bedrock ARNs / Vertex versions / Foundry deployments.

### 9.3 Task budgets (beta)

Header `task-budgets-2026-03-13`. Minimum 20K tokens. Soft cap (not enforced silently — model warned and may degrade). Refusal-like behavior at very low budgets is a feature, not a bug — small budgets are signaled to the model.

### 9.4 Effort ladder

`low | medium | high | xhigh | max`. `low`–`xhigh` persist (settings, env, `/effort`); `max` is session-scoped *except* when set via `CLAUDE_CODE_EFFORT_LEVEL`. Frontmatter `effort:` on a skill or subagent overrides the session level while that artifact is active, but not the env var.

Effort precedence: env var > frontmatter (when active) > `effortLevel` setting > model default. As of v2.1.117, defaults: `xhigh` on Opus 4.7, `high` on Opus 4.6 and Sonnet 4.6.

`ultrathink` anywhere in a prompt requests deeper reasoning on that turn without changing the session level (in-context instruction; effort sent to API is unchanged). "Think", "think hard", "think more" are *not* recognized keywords — passed through as ordinary prompt text.

---

## 10. Sandboxing

OS-level filesystem and network isolation for the Bash tool and its child processes ([sandboxing doc](https://code.claude.com/docs/en/sandboxing)). Built on Seatbelt (macOS), bubblewrap (Linux/WSL2; WSL1 unsupported). Native Windows support is planned.

Configuration goes under `sandbox.*` in settings:

```json
{"sandbox": {
  "enabled": true,
  "failIfUnavailable": true,
  "autoAllowBashIfSandboxed": true,
  "excludedCommands": ["docker *"],
  "filesystem": {
    "allowWrite": ["~/.kube", "/tmp/build"],
    "denyWrite": ["/etc"],
    "denyRead": ["~/.aws/credentials"],
    "allowRead": ["."],
    "allowManagedReadPathsOnly": false
  },
  "network": {
    "allowedDomains": ["github.com", "*.npmjs.org"],
    "deniedDomains": ["uploads.github.com"],
    "allowUnixSockets": ["~/.ssh/agent-socket"],
    "allowLocalBinding": true,
    "allowMachLookup": ["com.apple.coresimulator.*"],
    "allowManagedDomainsOnly": false
  },
  "enableWeakerNestedSandbox": false,
  "enableWeakerNetworkIsolation": false
}}
```

Arrays merge across scopes; `deniedDomains` takes precedence over `allowedDomains`. `failIfUnavailable: true` makes a missing sandbox a hard failure (intended for managed deployments that require sandboxing as a security gate). `autoAllowBashIfSandboxed: true` (default) — sandboxed Bash commands run without prompting, even if `ask: Bash(*)` is set. The sandbox boundary substitutes for the per-command prompt; explicit deny rules still apply; `rm`/`rmdir` targeting `/`, home, or critical paths still prompts.

Linux extra steps on Ubuntu 24.04+: an AppArmor profile granting `bwrap` userns is required; install `bubblewrap` and `socat`. On WSL2, sandboxed commands cannot launch Windows binaries (`cmd.exe`, anything under `/mnt/c/`) — add to `excludedCommands`.

Escape hatch: when a sandboxed command fails for sandbox reasons, Claude may retry with `dangerouslyDisableSandbox: true`, which routes through the normal permission prompt flow. Disable entirely with `allowUnsandboxedCommands: false`.

Security limitations: the built-in proxy enforces allowlist by client-supplied hostname *without* TLS termination, so domain-fronting attacks against broad allowlists like `github.com` are possible. For stronger guarantees, point at a custom proxy that terminates TLS and inspects traffic (`network.httpProxyPort`/`socksProxyPort`). `allowUnixSockets` to `/var/run/docker.sock` is effectively root-on-host.

The sandbox runtime is open source: `npx @anthropic-ai/sandbox-runtime <command>`.

---

## 11. What's new in 2025–2026 (consolidated)

- **Tokenizer change** — model tokenization updated across the 4.x family; cached prefixes from pre-update sessions are invalidated.
- **Adaptive thinking** — default mode on 4.6/4.7; Opus 4.7 rejects fixed budgets.
- **Task budgets** (beta, `task-budgets-2026-03-13` header) — 20K min, soft cap.
- **`xhigh` effort tier** — 4.7 only.
- **Auto-memory** — `~/.claude/projects/<repo>/memory/` since v2.1.59.
- **Hook lifecycle expansion** — ~29 events including `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `PreCompact`/`PostCompact`, `Elicitation`/`ElicitationResult`, `Setup`, `WorktreeCreate`/`WorktreeRemove`.
- **Agent view** (`claude agents` TUI, supervisor process) — research preview, v2.1.139+.
- **Channels** — MCP push to running session; Telegram/Discord/iMessage; v2.1.80+.
- **Auto permission mode** — research preview; auto-approve with background classifier.
- **Background monitors in plugins** (`monitors/monitors.json`).
- **LSP in plugins** (`.lsp.json`).
- **Sandbox** (Seatbelt/bubblewrap) — first-class with `sandbox.*` settings, `--sandbox`, `/sandbox`.
- **Agent SDK credit pool split** — June 15, 2026.
- **Keybindings file** — `~/.claude/keybindings.json` with live reload, v2.1.18+.
- **Sub-agent isolation** — `isolation: worktree` in subagent frontmatter.
- **`opusplan`** alias — Opus plans, Sonnet executes; 200K cap (not 1M).
- **Live-reload of plugins** — `/reload-plugins` covers skills, agents, hooks, plugin MCP, plugin LSP.
- **`policyHelper`** (v2.1.136+) — admin-deployed executable computes managed settings at startup.
- **`parentSettingsBehavior`** (v2.1.133+) — SDK/IDE-supplied settings can `merge` under managed.
- **Project-level model pin auto-writes to `.claude/settings.local.json`** (v2.1.117+) when `/model` differs from project pin.
- **`--plugin-dir <zip>`** (v2.1.128+) — zip archives accepted.
- **`claude agents --permission-mode/--model/--effort`** (v2.1.142+).

---

## 12. Stability map

| Stable                                                                                    | Research preview                                          | Deprecated / legacy                                              |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------- |
| Skills, subagents, hooks (full 2026 roster), MCP stdio + Streamable HTTP, plugins, plan mode, output styles, OTel, sandbox (macOS/Linux/WSL2), keybindings, scheduled tasks (`/loop`, Routines, desktop), `opusplan`, 1M context, auto-memory, Opus 4.7 | Channels, agent view, auto permission mode, voice dictation, task budgets (beta header), `EXTERNAL_SHADOW` cross-family hook primitive (announced, not yet shipped) | MCP SSE transport, custom slash commands (`.claude/commands/*.md`), fixed-thinking-budget mode on 4.6/4.5, native Windows sandbox (planned, not yet shipped) |

---

## 13. Anti-patterns

- **Bloating CLAUDE.md.** Files over 200 lines reduce adherence and burn context every session. Move multi-step procedures to skills; move file-type-specific guidance to path-scoped `.claude/rules/`.
- **MCP-for-everything.** Each connected server costs context for tool listings. Prefer Bash with `WebFetch(domain:)` allowlists for one-off integrations; reserve MCP for systems Claude needs deep access to.
- **`bypassPermissions` outside containers.** The circuit-breakers (`rm -rf /`, `rm -rf ~`) are the only protections. Writes to `.git`, `.claude`, `.vscode`, `.idea`, `.husky` are *allowed*. Run only in disposable containers/VMs.
- **Slow `PreToolUse` hooks.** Every Bash call pays the latency; a 1s hook turns a 10-tool turn into +10s wall-clock. Defer non-blocking work to `PostToolUse`/`Notification`.
- **Bash permissions that constrain arguments.** `Bash(curl https://github.com *)` is bypassed by case, redirects, env vars, and protocol switches. Use `WebFetch(domain:)` plus a Bash *deny* on `curl`/`wget`.
- **Treating environment runners as wrappers.** `Bash(devbox run *)` does *not* match the inner command — it matches anything after `run`, including destructive commands. Always pair: `Bash(devbox run npm test)`.
- **Setting `autoMemoryDirectory` from project settings.** Refused by design — a cloned repo could redirect writes to sensitive locations. Managed/user only.
- **Skill bodies as one-time steps.** Skill content stays in context for the rest of the session; write standing instructions, not "do X then stop."
- **Reading raw subagent output.** Defeats the context-savings rationale of subagents — summarize via a distillation pass and read the distillation.
- **Anchoring on outdated dynamic-skill costs.** `` !`...` `` runs *before* the skill body reaches the model; expensive shell blocks fire every invocation. Cache or use static body sections where possible.
- **Confusing 1M `opus` with `opusplan`.** The 1M auto-upgrade applies to `opus`; `opusplan` keeps the 200K cap in its plan phase.

---

## 14. Top 15 features every advanced user should know

Ranked by leverage for an experienced practitioner; one line each on what it solves.

1. **Subagents (`.claude/agents/`)** — keep search/exploration/log-spelunking out of your main context window.
2. **Skills (`.claude/skills/`)** — make repeatable procedures cheap; bodies load only when invoked, descriptions cost <1% of context.
3. **Hooks (29 events)** — deterministic enforcement around every lifecycle moment; `PreToolUse` modifies tool input, `PostToolBatch` gates the agentic loop.
4. **Plan mode + `opusplan`** — Opus designs, Sonnet executes, you review the plan before code moves.
5. **Auto-memory (`MEMORY.md`)** — Claude takes notes from your corrections automatically; first 200 lines load every session.
6. **`.claude/rules/` with `paths:` frontmatter** — modular instructions that only enter context when matching files are touched.
7. **Agent view (`claude agents`)** — one screen across all background sessions; supervisor process survives terminal closure and binary updates.
8. **Sandboxing (`sandbox.*`)** — OS-level filesystem/network isolation for Bash and *all* its children, including `terraform`, `kubectl`, `npm` scripts.
9. **Plugins + marketplaces** — version, share, and update the whole `.claude/` bundle as one unit; namespaced skills prevent conflict.
10. **MCP `ide` server (built-in)** — `mcp__ide__getDiagnostics` and `mcp__ide__executeCode`; the diff viewer and `@`-mentions go through here.
11. **Channels** — make MCP push *to* you; Telegram/Discord/iMessage your running session, including permission relay.
12. **OpenTelemetry export** — GenAI-conventions metrics and logs for cost, latency, and behavior across the org.
13. **`/loop` self-paced + Monitor tool** — poll a deploy or PR with model-chosen intervals; can switch to streamed line-by-line monitoring instead of polling.
14. **Keybindings (`~/.claude/keybindings.json`)** — every chat-input and dispatch action rebindable per-context, chord support, live reload.
15. **Headless `claude -p` + `--output-format stream-json`** — script Claude into CI, pre-commit hooks, and existing tooling; June 15, 2026 credit pool split makes this safe for production volumes.

---

## Sources

Per-section citations are inline. Primary doc roots:

- Code surfaces: [code.claude.com/docs/en/](https://code.claude.com/docs/en/) — `plugins`, `plugins-reference`, `skills`, `sub-agents`, `hooks`, `hooks-guide`, `mcp`, `channels`, `channels-reference`, `settings`, `permissions`, `permission-modes`, `memory`, `agent-view`, `scheduled-tasks`, `routines`, `model-config`, `sandboxing`, `vs-code`, `keybindings`, `output-styles`, `statusline`, `monitoring-usage`, `server-managed-settings`.
- Headless / Agent SDK: [docs.claude.com/en/docs/agent-sdk/](https://docs.claude.com/en/docs/agent-sdk/) — `headless`.
- Models, context, effort: [platform.claude.com/docs/en/](https://platform.claude.com/docs/en/) — `about-claude/models/overview`, `build-with-claude/context-windows`, `build-with-claude/effort`.
