# Draft / experimental status marker for README sections that depend on yet-to-exist tools

| Field | Value |
|---|---|
| 📌 **title** | Draft / experimental status marker for README sections that depend on yet-to-exist tools |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-format-only-state-transition-gate` added a "Required body elements per state" schema table to `upgrades/README.md`. The table is a **contract for a tool that does not yet exist** — the `/upgrade advance` subcommand is sketched in an upgrade entry but not built. A reader of the README today sees the table and may assume the contract is enforceable. The HTML comment marker added in-line is too quiet. |
| 💡 **essence** | Adopt a single visible convention for marking README sections that document a contract whose enforcement does not yet exist. A short blockquote at the top of the section: `> **Draft contract — gate not yet productionized. See [<entry>](path).**` Generalizes to any future "we're committing to this convention before the tool exists" surface. |
| 🚀 **upgrade** | Readers (operator, AI agents, future-self) see at a glance which README sections describe shipping behavior versus which describe intended-but-not-yet-enforced behavior. The lab gains a vocabulary for "this is what we want to be true" vs "this is what is true today" without requiring the tool to ship before the contract is documented. |
| 🏷️ **tags** | readme, conventions, documentation, draft-state, lab-hygiene |
| 🔗 **relates_to** | 2026-04-26-format-only-state-transition-gate |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The problem](#the-problem)
- [The convention](#the-convention)
- [Why no-brainer](#why-no-brainer)

## The problem

`upgrades/README.md` currently contains a "Required body elements per state" table whose purpose is to be machine-read by a `/upgrade advance` subcommand. That subcommand does not exist. A reader who finds the table reasonably assumes it is enforceable. It is not.

The same shape will occur every time a contract is captured in the README before its enforcement mechanism ships. Without a convention, the README accumulates aspirational tables that look like load-bearing ones.

## The convention

A short blockquote at the top of any README section that documents a not-yet-enforced contract:

```markdown
> **Draft contract — gate not yet productionized.** This section documents the
> intended discipline for X. The `/upgrade advance` subcommand that enforces it
> is sketched at [link to upgrade entry] but not yet built. The discipline is
> opt-in (and currently un-enforceable) until the tool ships.
```

One line of structure: marker + reason + link. When the tool ships, the blockquote is deleted. The presence of the blockquote is itself the signal that the section is draft.

Pair with: a `## Status` line in the upgrade entry's body, mirroring the marker so the two surfaces stay in sync.

## Why no-brainer

- One paragraph of README convention. ~5 minutes to add the blockquote to the existing schema table; ~5 minutes to add a `## Status` mirror to the format-only-state-transition-gate entry.
- Generalizes to any future case (every upgrade entry that proposes a contract before shipping the enforcement is a candidate).
- Zero behavior change. Zero cost. Pure clarity.
