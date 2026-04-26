# Constitutional layer — `GOALS.md`, `MODULES.md`, per-module READMEs

| Field | Value |
|---|---|
| 📌 **title** | Constitutional layer — `GOALS.md`, `MODULES.md`, per-module READMEs |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's instinct that the repo would become messy as more capabilities land, combined with the absence of any documented goals or module contracts. CLAUDE.md captures operational doctrine well; nothing captures *what this stack is for* or *what each module's contract is*. The seven-capability taxonomy was articulated mid-conversation but lives only in session-artifact `frame.md`, nowhere on disk. |
| 💡 **essence** | Three small documents at the constitutional layer: `GOALS.md` (what this stack is for and what it is not — the test against which every future "should we add X" question gets evaluated), `MODULES.md` (the module decomposition with each module's contract: owns, reads-from, writes-to, must-not), per-module `README.md` files mirroring the contract for that module. None of these introduce new behavior; they make existing implicit behavior auditable and constrain what comes next. |
| 🚀 **upgrade** | Future additions land cleanly because their boundary is pre-defined. The seven-capability taxonomy gains an on-disk home. CLAUDE.md/AGENTS.md drift becomes detectable (both should reference GOALS.md identically). The repo gains a foundation that everything else can be tested against. Without this, every new module bleeds into adjacent ones within ~5 commits. |
| 🏷️ **tags** | architecture, modularity, goals, contracts, foundation |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The three documents](#the-three-documents)
- [Module decomposition](#module-decomposition)
- [Why this lands first, before any other modular work](#why-this-lands-first-before-any-other-modular-work)

## The three documents

**`GOALS.md`** at root. Three or four sentences:
- *Primary goal:* produce post-critique design recommendations on questions pasted in from elsewhere.
- *Secondary goal:* surface frame-level objections the user wouldn't have caught alone.
- *Tertiary goal:* accumulate cross-session knowledge (corpus, lab, memory) that improves future runs.
- *Non-goals:* be a target codebase. Be a coding assistant. Replace human judgment.

Every future "should we add X" decision tests against this doc. If X doesn't serve a stated goal or contradicts a non-goal, the answer is no.

**`MODULES.md`** at root. Names each module, links to its README, gives a contract table. Loaded for any meta-question about the stack. The seven-capability taxonomy lives here as the disciplined version of the conversational sketch.

**Per-module `README.md`.** One per module. One-line purpose, named inputs (what it reads from), named outputs (what it writes to), named non-responsibilities, change rules.

## Module decomposition

| Module | Owns | Reads from | Writes to | Must NOT |
|---|---|---|---|---|
| **orchestration** | CLAUDE.md, AGENTS.md, the workflow, gates | every other module | session-artifacts, decision-log | reach into agent internals |
| **classification** | requirement-classifier, frame-challenger, scope-mapper | requirement, distillations | requirement.md, frame.md, scope-map.md, challenges.md | run retrieval or critique |
| **retrieval** | canon-librarian, canon-refresher, corpus, ingest scripts | canon/corpus/, web sources | canon/corpus/, librarian distillation | hold session state |
| **outside-view** | outside-view agent | canon, web | outside-view distillation | duplicate librarian |
| **distillation** | subagent-distiller | raw subagent returns | distillations/ | reason about content |
| **critique** | three lens panel + (later) comparator + (later) security/epistemic | candidate, distillations | critiques/, comparisons | rewrite candidates |
| **lab** | upgrades-curator (slash command), upgrades/ | observations, canon | upgrades/ | block live workflow |
| **session-artifacts** | per-session ephemeral output | n/a | itself | leak across sessions |
| **harness** | settings.json, hooks, env-var bypasses | nothing | enforces gates | live in agent prompts |
| **memory** | auto-memory, project memory | session ledgers, lab | ~/.claude/projects/.../memory | overwrite without dedupe |

## Why this lands first, before any other modular work

Documentation precedes code. If GOALS.md and MODULES.md don't exist, every other addition (new agent, new lens, new stack) has no constitutional layer to test against. The discipline being bought is *modularity-by-construction* — each new piece lands in a slot the documents already anticipate, rather than bleeding into an adjacent module's surface.

The cost is two short documents and a handful of READMEs (~2-3 hours of writing). The value is the ability to evaluate every future "should we add X" question against named goals and contracts. Without the constitutional layer, those evaluations happen in conversation and decay; with it, they happen against an artifact and persist.
