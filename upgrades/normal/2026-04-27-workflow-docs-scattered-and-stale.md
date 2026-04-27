# Workflow docs are scattered and partly stale

| Field | Value |
|---|---|
| 📌 **title** | Workflow docs are scattered and partly stale |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-27 |
| ⚡ **catalyst** | Surfaced as an adjacent finding during session [`2026-04-27-critics-get-write-tool-impl`](../../.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/) — after the 12-step run-through-repo concluded, the operator asked whether any README in the repo describes the 12-step process: what each step produces, what it functions as, and where the boundaries between steps live. The honest answer was *no, partial docs across multiple files, no single source of truth, and one stale conflict that the top-level README still treats as authoritative*. |
| 💡 **essence** | The repo has authoritative behaviour-level documentation (`CLAUDE.md`) and authoritative artifact-layout documentation (`.claude/session-artifacts/README.md`), but no reader-facing doc that ties step-purpose, step-output, step-boundary, and agent-owner together in one read. Worse, the top-level [`README.md`](../../README.md) still points readers at [`workflows/architecture-review.md`](../../workflows/architecture-review.md) — a stale 7-step earlier version of the workflow that conflicts with the current 12-step (still references a single `critic` agent, now the three-lens panel). New readers arriving via the front door get an outdated mental model. |
| 🚀 **upgrade** | Either (a) delete the stale `workflows/architecture-review.md` and update the top-level README to point at `CLAUDE.md` + `.claude/session-artifacts/README.md`, (b) write a new `workflows/12-step-workflow.md` that supersedes the stale file and unifies what's currently scattered, or (c) expand `.claude/session-artifacts/README.md` beyond physical layout into a step-by-step what-and-why. The cheapest path (a) is genuinely XS; (b) and (c) are S–M and would deliver a single doc the operator and any future contributor can read once and have a complete mental model of the workflow. |
| 🏷️ **tags** | docs, workflow, readme, stale, repo-hygiene |
| 🔗 **relates_to** | constitutional-layer-goals-modules, rnd-lab, agent-subdirectories-by-module |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-27 | — | — | — | — | — | — | — |

## Table of contents

- [The gap, named](#the-gap-named)
- [What exists today](#what-exists-today)
- [The wrong-and-tracked file](#the-wrong-and-tracked-file)
  - [🔴 Concrete evidence (line-level)](#-concrete-evidence-line-level)
- [Three implementation options](#three-implementation-options)
- [Why this is normal, not no-brainer](#why-this-is-normal-not-no-brainer)
- [Why this is normal, not profound](#why-this-is-normal-not-profound)

## The gap, named

A reader new to this repo who wants to understand how the 12-step workflow actually works has no single doc to read. They will piece a model together from at least three places — the prescriptive `CLAUDE.md`, the layout-only `.claude/session-artifacts/README.md`, and the individual agent contracts in `.claude/agents/*.md` — and along the way they will likely follow the top-level `README.md`'s pointer to `workflows/architecture-review.md` and absorb a *wrong* mental model of the workflow before they figure out it has been superseded. There is no map showing how the agents compose into the steps, no per-step "what failure-class does this filter for," and no single boundary diagram between adjacent steps.

The stack's value-prop is that the workflow does specific epistemic work at each step. If a reader cannot quickly see what work happens where, they cannot evaluate whether the workflow is doing what it claims, cannot extend it without breaking it, and cannot honestly compare it to alternatives. The docs gap is therefore not just a quality-of-life issue — it weakens the operator's own ability to reason about the system.

## What exists today

| Doc | Purpose | Strength | Gap |
|---|---|---|---|
| [`CLAUDE.md`](../../CLAUDE.md) | The authoritative 12-step spec — each step's action, hard gates, off-ramps, do/don't list. | Single source of truth on *what the orchestrator must do.* | Prescriptive, not descriptive. No diagrams. No per-step "what failure-class this filters for" framing. Written for the orchestrator, not for a human reader. |
| [`.claude/session-artifacts/README.md`](../../.claude/session-artifacts/README.md) | Physical artifact layout — which file each step writes, lifecycle, the hard gate on Step 9. | Single source of truth on *where outputs land.* | Doesn't explain *why* each step exists or what it filters. Tree diagram is also missing the loop-2 critique-rewrite shapes that show up in real sessions. |
| [`README.md`](../../README.md) (top-level) | High-level pitch (three subagents, philosophy, how to invoke). | Front-door readability. | Predates the 12-step expansion. Still says "a critic subagent" (singular). Points readers at the stale workflows file as authoritative. 37 lines — out of date with the system it describes. |
| [`workflows/architecture-review.md`](../../workflows/architecture-review.md) | A 7-step workflow definition that *was* authoritative when the stack first launched. | None today — superseded. | **Wrong-and-tracked.** The 7-step shape, the single `critic` agent reference, and the absence of frame-challenger/scope-mapper/distiller all conflict with the current `CLAUDE.md`. |
| `.claude/agents/*.md` | Each agent's individual contract — inputs, output shape, must/must-not. | Rigorous per-agent boundary definitions. | No map shows how the agents compose into the workflow. Read individually, the agents are fine; read collectively as "the workflow," they require the reader to assemble the picture. |
| [`upgrades/README.md`](../README.md) | The lab — entry tiers, lifecycle, format. | Excellent at what it covers. | Not about the workflow. Mentioned only to clarify it is *not* the missing doc. |

## The wrong-and-tracked file

`workflows/architecture-review.md` is the highest-priority piece of this gap because it is *actively misleading*. The top-level `README.md` line 29 reads:

> The `CLAUDE.md` in this directory triggers the critic workflow. See `workflows/architecture-review.md` for the full routing.

A reader who follows that link gets a 7-step, single-`critic`-agent workflow that has not been current for many sessions. They form a mental model that is wrong about the number of steps, wrong about the number of critic lenses, and wrong about which artifacts exist (no `scope-map.md`, no `challenges.md`, no `distillations/`, no `frame.md` revisions). When they then try to participate in the workflow or extend it, the gap between their model and the live system is *invisible until it bites*.

This single fact — wrong-and-tracked, pointed-at-from-the-front-door — is the reason this entry is being filed rather than absorbed into operator habit. The other gaps (no unified doc, no step-purpose framing) are real and worth addressing, but they are quality-of-life concerns; the stale workflows file is a correctness concern about what new readers absorb.

### 🔴 Concrete evidence (line-level)

Three citations make the contradiction undeniable rather than impressionistic:

- [`workflows/architecture-review.md:44`](../../workflows/architecture-review.md) reads *"Invoke `critic` with the full candidate recommendation…"* — instructing the reader to call a single `critic` agent.
- [`CLAUDE.md:41–46`](../../CLAUDE.md) (Step 10) says *"Invoke the three critic lenses in parallel"* and lists `critic-architecture`, `critic-operations`, `critic-product` — the three-lens panel that replaced the single critic.
- [`.claude/agents/`](../../.claude/agents/) — there is **no** `critic` agent file. The directory contains only the three lens agents (`critic-architecture.md`, `critic-operations.md`, `critic-product.md`) plus the supporting agents (`canon-librarian`, `canon-refresher`, `frame-challenger`, `outside-view`, `requirement-classifier`, `scope-mapper`, `subagent-distiller`). A reader who follows the stale workflow's instruction to "invoke `critic`" will fail at the agent-resolution step.
- [`README.md:29`](../../README.md) — the top-level README sends new readers directly to the stale file as authoritative.

The chain — front door → stale workflow → instruction to invoke a non-existent agent — is the strongest argument for option (a) (delete + re-point) shipping now, even if options (b)/(c) wait for a separate entry.

## Three implementation options

The shapes are not mutually exclusive — a small version could ship now and a larger one could spawn later — but they are listed in increasing scope so the operator can decide where to commit.

**Option (a) — Minimum: delete and re-point.** Delete `workflows/architecture-review.md`. Update the top-level `README.md` line 29 to point at `CLAUDE.md` and `.claude/session-artifacts/README.md` instead. Update the `README.md` description from "a critic subagent" (singular) to "a three-lens critic-panel." Estimated effort: 15–30 minutes. Closes the wrong-and-tracked correctness concern entirely. Leaves the unified-doc gap for later.

**Option (b) — Mid: write a unifying workflow doc.** Replace `workflows/architecture-review.md` with a new `workflows/12-step-workflow.md` that, in one read, gives `step → purpose → produces → reads → boundary with adjacent step → which agent owns it`. Roughly the shape of a sequence diagram in prose, plus a table mapping agent files to steps. Estimated effort: 2–4 hours. Closes the unified-doc gap. Lifts repo onboarding meaningfully.

**Option (c) — Mid: expand session-artifacts/README.md.** Keep the layout content; add a per-step "what failure-class this filters for" paragraph; convert the existing tree diagram into a richer one that shows loop-1 / loop-2 shapes. Same scope as (b), different home. Best if the operator wants a single doc to absorb everything; (b) is best if the operator wants a clean reading order from `README.md` → `workflows/12-step-workflow.md` for entry-level readers and `CLAUDE.md` → `.claude/session-artifacts/README.md` for orchestrator-and-implementor readers.

The ordering of options is also a working dependency — (a) is a precondition for (b) and (c) anyway, since the stale file gets in the way of either bigger version. (a) on its own is a complete win; (b) or (c) on top is a quality multiplier.

## Why this is normal, not no-brainer

There is real design uncertainty in the choice between (a), (b), and (c). The operator may legitimately prefer the minimum cleanup (a) — leaving the unified-doc gap for a future entry — or the unifying-doc version (b), or the expanded session-artifacts version (c). Each shape has different downstream consequences for where future workflow documentation accretes. A no-brainer is something I would implement in 30 minutes with no design uncertainty; this entry has more shape-decision than that.

## Why this is normal, not profound

The observation is not novel — it is the kind of gap any engineering team accumulates after iterating on a system without keeping its README in sync. Naming it does not change how the system is thought about; it just acknowledges a mundane drift between the system and its documentation. The value of acting on this entry is *real* but it is not *insight* — it is hygiene. Profound is reserved for entries whose value is the seeing; this entry's value is the doing.
