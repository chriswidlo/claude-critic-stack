# Agent subdirectories by module

| Field | Value |
|---|---|
| 📌 **title** | Agent subdirectories by module |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | ai |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | `.claude/agents/` currently holds 10 flat files. The capability roadmap from this session adds at least 4 more (upgrades-curator if it exists, comparator, security lens, epistemic lens). At 14+ agents the flat layout starts to obscure the module boundaries the constitutional-layer entry proposes — agents from "classification," "retrieval," "critique," and "distillation" all sit in the same directory. |
| 💡 **essence** | Move agent files into subdirectories that mirror the module decomposition: `agents/classification/`, `agents/retrieval/`, `agents/critique/`, `agents/distillation/`, `agents/lab/`, `agents/outside-view/`. Claude Code agent loading is already recursive, so this works without runtime changes. The directory structure becomes a visible reflection of the architecture. |
| 🚀 **upgrade** | Navigability scales as agent count grows. New agents land in the right module without bleed (you don't accidentally create a critic in the classification module). The architecture becomes self-documenting from the file tree. CLAUDE.md's "Agents available in this stack" section becomes a directory listing rather than a flat enumeration. |
| 🏷️ **tags** | architecture, organization, agents, modularity |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The proposed layout](#the-proposed-layout)
- [Verification before move](#verification-before-move)
- [Why no-brainer](#why-no-brainer)

## The proposed layout

```
.claude/agents/
  classification/
    requirement-classifier.md
    frame-challenger.md
    scope-mapper.md
  retrieval/
    canon-librarian.md
    canon-refresher.md
  outside-view/
    outside-view.md
  distillation/
    subagent-distiller.md
  critique/
    critic-architecture.md
    critic-operations.md
    critic-product.md
    (later: critic-security.md, critic-epistemic.md, critic-comparator.md)
  lab/
    (eventual upgrades-curator, if it ever exists as agent rather than slash command)
```

Six subdirectories for ten agents. Some directories start with one agent; that's fine — they have growth room.

## Verification before move

Claude Code agent loading is recursive: subagents are discovered anywhere under `.claude/agents/`, regardless of nesting depth. This should be true; verify with a one-shot test before moving all files: create `agents/test/test-agent.md` and confirm it appears in available agents. If yes, proceed; if no, this entry becomes a research item instead of a no-brainer.

## Why no-brainer

The move is mechanical (`mv`), the value is uncontroversial (navigability scales), and the cost is contained (one verification + the moves). The change has no behavioral impact — agents do exactly what they did before, just from different paths.

CLAUDE.md may need a small update: the "Agents available in this stack" section can either remain a flat enumeration or migrate to a directory-grouped enumeration. Either works; the latter is slightly more honest about the architecture.
