# Git strategy documentation for this repo

| Field | Value |
|---|---|
| 📌 **title** | Git strategy documentation for this repo |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | operator |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator named this directly mid-conversation: *"I think we need to document git strategy for this repo, later though just adding it to the list."* No documented strategy currently exists for commit message conventions, branching, PR norms, or capability tagging in commits. As capabilities land from this lab (`implemented` state), the relationship between commits and capabilities should be auditable. |
| 💡 **essence** | A `GIT.md` (or section in `MODULES.md`) at root that documents: commit message conventions, branch naming, when to PR vs commit-to-main, how to tag commits with capability references (e.g., `feat: critics-write-tool [upgrades/no-brainer/2026-04-26-critics-get-write-tool.md]`), and how the lab's state lifecycle interacts with git history (a lab entry's transition to 🔨 `implemented` should reference the commits that did the implementing). |
| 🚀 **upgrade** | Commits become readable history. Capability-by-commit pattern becomes possible (a query like "show me commits that implemented lab entries" is mechanical). The lab's state lifecycle gains a real anchor — `implemented` is not just a date but a set of commits, traceable. CLAUDE.md and AGENTS.md drift becomes commit-traceable. |
| 🏷️ **tags** | git, documentation, capability-ledger, conventions |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What `GIT.md` should cover](#what-gitmd-should-cover)
- [The lab-to-commits link](#the-lab-to-commits-link)
- [Why no-brainer](#why-no-brainer)

## What `GIT.md` should cover

Sections, in order of importance:

1. **Commit message conventions.** Subject line shape, when to add body, how to tag with capability references. Probably Conventional Commits as a starting point, with a tag suffix for lab-entry references.
2. **Capability tagging in commits.** When a commit implements a lab entry, the commit message should reference the entry by path: `feat: shadow-comparator panel [upgrades/profound/2026-04-26-critic-panel-correlated-by-default.md]`. This makes lab-to-commits queries mechanical.
3. **Branching strategy.** When to PR, when to commit to main, what gets a PR vs a direct push. Single-operator repo can probably use direct-to-main for most changes, PR only for risky migrations.
4. **The `.claude/session-artifacts/` git policy.** Currently mostly gitignored except `exemplars/` and `README.md`. Document the rule explicitly so it doesn't drift.
5. **The `upgrades/` git policy.** Tracked. Each entry is its own commit (or batched per session). State-table updates are commits ("upgrades: 2026-04-26-critics-get-write-tool moves to implemented").

## The lab-to-commits link

The lab's state lifecycle (🌱 → 🏁) gains real meaning when each transition is anchored to commits. When an entry moves to 🔨 `implemented`, the implementing commits' SHAs (or the merge commit if a PR) are referenced in the entry — either appended to the body or added as an optional `implemented_by:` field in the meta table.

This creates the capability-ledger pattern the operator-AI conversation discussed earlier: not as a separate `CAPABILITIES.md` file, but as the natural read of the lab when filtered by `implemented` state. *"Show me capabilities landed in 2026-Q2"* becomes a directory query plus a commit-log read.

## Why no-brainer

The change is documentation. ~1 page. No code, no behavior change. The value is concrete: as the lab fills with entries and as those entries start moving through states, the ability to trace state transitions to git history is mechanical only if the conventions are documented.

Best landed after the constitutional layer (`GOALS.md` + `MODULES.md`) since `GIT.md` is part of the same constitutional set, but doesn't depend on them.
