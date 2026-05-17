# .claude/plugins/

**Anthropic-documented slot for project-shippable plugins.** Empty by design — populate only when this repo is published as a plugin OR when consuming third-party plugins.

From the [Claude Code plugins documentation](https://github.com/anthropics/claude-code/blob/main/plugins/README.md):

> Plugins can live in `.claude/plugins/` and be shared via version control. A plugin is a manifest at `.claude-plugin/plugin.json` plus bundled `skills/`, `agents/`, `hooks/`, `.mcp.json`.

## What goes here

A `.claude/plugins/<plugin-name>/` directory per installed or bundled plugin, each with its own `.claude-plugin/plugin.json` manifest plus its bundled primitives.

## Why this is on the radar for this repo

Two upgrades-lab entries already consider plugin packaging:
- [upgrades/normal/2026-04-26-author-attribution-for-community-plugins/](upgrades/normal/2026-04-26-author-attribution-for-community-plugins/)
- [upgrades/outlandish/2026-04-26-critic-stack-as-installable-marketplace-plugin/](upgrades/outlandish/2026-04-26-critic-stack-as-installable-marketplace-plugin/)

If either lands — packaging this stack as a community plugin, or consuming external plugins for ancillary capabilities — populate this folder. The placeholder ensures the slot is discoverable to anyone (AI or human) thinking about plugin packaging without forcing the question now.

## See also

- [Claude Code plugins README (anthropics/claude-code)](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
- [Anthropic — Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
