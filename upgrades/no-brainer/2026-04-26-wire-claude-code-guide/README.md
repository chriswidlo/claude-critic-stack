# Wire `claude-code-guide` into the workflow's parallel-gather step

| Field | Value |
|---|---|
| 📌 **title** | Wire `claude-code-guide` into the workflow's parallel-gather step |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | ai |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective on the stack noted that operations-lens critiques repeatedly caught the orchestrator on Claude Code primitives the orchestrator did not actually understand ("Claude Code does not expose a mid-run abort," "hooks cannot terminate an in-flight turn"). The agent that knows what Claude Code actually supports — `claude-code-guide` — was sitting unused. It is built into the harness, not a file in `.claude/agents/`, but it is invokable via the Agent tool from any session. |
| 💡 **essence** | When a design question's surface area touches Claude Code primitives (hooks, MCP servers, slash commands, settings.json, plugins, harness mechanics), the workflow currently has no routing rule that consults the agent that actually knows. It treats Claude Code as background knowledge the orchestrator already has — but the orchestrator does not have it accurately. |
| 🚀 **upgrade** | One paragraph added to CLAUDE.md, in the Steps 3–5 parallel-gather section: *"If the question's surface area touches Claude Code primitives, `claude-code-guide` joins the parallel-gather set. `Explore` stays skipped unless a target codebase is also named."* That single routing change makes Claude-Code-shaped design questions ground their candidates in what the harness actually does, not in what the orchestrator believes it does. |
| 🏷️ **tags** | workflow, routing, agents, claude-code, claude-code-guide |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What gets added](#what-gets-added)
- [Why this is high-leverage](#why-this-is-high-leverage)
- [Trigger heuristic](#trigger-heuristic)

## What gets added

A paragraph in CLAUDE.md, in the Steps 3–5 section, after the existing list of parallel-gather agents:

> **If the question's surface area touches Claude Code primitives** — hooks, MCP servers, slash commands, settings.json, plugin/skill mechanics, subagent semantics, agent file format, the Agent SDK, or Claude API integration — **`claude-code-guide` joins the parallel-gather set**. It is the harness-internal agent that knows what Claude Code actually supports vs. what the orchestrator may believe it supports. `Explore` stays skipped unless a target codebase is also named.

That is the entire change. No new agent file (claude-code-guide is already available globally), no settings update, no workflow restructure.

## Why this is high-leverage

The retrospective's specific complaint was: the operations critic kept catching candidates that proposed mid-run aborts, hook-driven turn termination, and other Claude Code mechanics that don't exist. Each catch was a panel-veto that triggered a replan loop. Each loop cost an Opus pass on three lenses. The cumulative cost of *not* asking claude-code-guide upfront was multiple replan loops per Claude-Code-touching session.

The fix costs one paragraph in a markdown file. The value is closing a class of replan loop that doesn't need to happen.

## Trigger heuristic

When does a question "touch Claude Code primitives"? A loose heuristic for the orchestrator (which can be encoded in the CLAUDE.md paragraph): the question mentions any of the following terms — hook, MCP, slash command, settings.json, agent (in the harness sense, not the architecture sense), subagent, plugin, skill, harness, runtime, Agent SDK, Claude API, or describes a behavior that the orchestrator would need to verify is supported by Claude Code before designing against it.

When in doubt, invoke claude-code-guide. The cost of a single extra subagent call is trivial; the cost of designing against an idealized Claude Code is real.
