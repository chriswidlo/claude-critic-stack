# .claude/output-styles/

**Anthropic-documented slot for project-scoped system-prompt styles.** Empty by design — add a style here only when the default Claude Code output isn't suitable for this project's purpose.

From [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory):

> `.claude/output-styles/` — Project-scoped system-prompt styles.

## What goes here

A `.md` file per output style, each describing a system-prompt customization. Users (or settings.json) explicitly select an output style; styles are not auto-loaded based on context. Useful when a project needs a consistent tone or output shape across all sessions.

## Why this is empty

The default Claude Code system prompt suits this repo's adversarial-review workflow. Custom output styles would risk overriding the discipline encoded in [CLAUDE.md](CLAUDE.md) and the per-agent prompts under [.claude/agents/](.claude/agents/). Add a style here only if a concrete need surfaces — e.g., a slimmer output for a CI-headless variant of the workflow.

## See also

- [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
- [Anthropic — Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
