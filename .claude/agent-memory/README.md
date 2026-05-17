# .claude/agent-memory/

**Anthropic-documented slot for subagent persistent memory.** Empty by design — populate only when a subagent declares `memory: user` in its frontmatter.

From [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory):

> `.claude/agent-memory/<agent-name>/MEMORY.md` — Subagent persistent memory (when `memory: user` is set).

## What goes here

When a subagent is configured with `memory: user`, Claude Code persists its memory across invocations into `.claude/agent-memory/<agent-name>/MEMORY.md`. The file is managed by Claude Code; the curator's role is to occasionally prune it.

## Why this is empty

None of the 14 agents in [.claude/agents/](.claude/agents/) currently use `memory: user`. This repo's anti-anchoring discipline argues against per-agent persistence (each invocation should be evidentiarily fresh). If a concrete need emerges where cross-session memory genuinely outweighs the anti-anchoring cost, set `memory: user` on the relevant agent and this folder will populate automatically.

## See also

- [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
- [Anthropic — Create custom subagents](https://code.claude.com/docs/en/sub-agents)
