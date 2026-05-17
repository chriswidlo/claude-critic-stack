# plans/

**Ephemeral scratchpad.** Files here are temporary planning notes for the current session — NOT durable design content, NOT roadmap items, NOT an institutional record.

## Read this when

- You found a `plans/*.md` file and want to know whether to treat it as authoritative.
- You're about to add a plan file and want to know the convention.

## The rule

Per the operator's working convention:

> `plans/` files are temporary scratchpads for the current session. **Delete them when the work lands.** Do not archive. Do not git-add to preserve history. Git already preserves the past — keeping stale plan files around just confuses future readers (human and AI) about what's current.

## What this means in practice

- **A plan file in `plans/` does NOT represent committed direction.** It's a working document the operator (or AI) used to organize one session's thinking. If the work landed, the plan should be deleted; the implementation IS the record. If the work didn't land, the plan is stale.
- **Treat any plan file present here as suspect** — check git log for when it was last touched relative to the work it describes. Stale plans are common; that's the cost of an ephemeral folder being committed.
- **Do NOT cite `plans/` as a primary source.** Durable design rationale lives in [upgrades/](upgrades/) (R&D lab) or in commit messages. `plans/` is operational scratch, not knowledge.

## What goes elsewhere

| If the content is... | It belongs in... |
|---|---|
| A creative R&D idea worth keeping | [upgrades/](upgrades/) (per the upgrade tier system) |
| A durable design decision | A commit message + relevant agent/skill/CLAUDE.md edit |
| Cross-session institutional memory | The user's machine-local Claude Code auto-memory (described in prose per [CLAUDE.md](CLAUDE.md) §"Path discipline") |
| A research distillation | [research/](research/) (dated, tiered) |
| Per-session reasoning artifacts | `.claude/session-artifacts/<session-id>/` |

## Why this folder exists at all (vs being gitignored)

History: `plans/` was originally intended as a durable planning surface; it has since been demoted to ephemeral. Rather than gitignore the folder (which would prevent operator from sharing a plan with reviewers across machines), the convention is "tracked-but-cleaned" — plans CAN be committed temporarily for sharing, but MUST be deleted when the work lands.

This README exists to make the "ephemeral" rule discoverable to AI agents and human readers. Without it, an agent walking the repo cold would treat `plans/<file>` as authoritative and propagate stale assumptions.

## Anti-patterns

- **Citing `plans/<file>` as authoritative.** Treat as suspect; check git log.
- **Leaving plans behind after work lands.** Delete via [bin/safe-rm.sh](bin/safe-rm.sh).
- **Adding a plan and never deleting it.** If you wouldn't put it in `upgrades/` or a commit message, it probably doesn't need to be in the repo at all.
