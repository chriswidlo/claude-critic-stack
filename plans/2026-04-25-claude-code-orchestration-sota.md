# SOTA knowledge dump: Claude Code orchestration & extension primitives (April 2026)

> **Status (2026-04-25):** Documentation upgrade only. **No new primitives, no agent additions, no repo behavior changes.** This file captures the synthesised state-of-the-art on Claude Code orchestration as of April 2026. Final placement of this knowledge — canon entry, new `docs/sota/` folder, extended README, expanded `canon/sources.ingest.yaml`, or some combination — is intentionally **left to the upgrade process** to decide after Ultraplan refinement.

## What this is

A research artifact produced by routing the question *"are subagents still SOTA, or should I author skills, or something else?"* through this stack's own adversarial-review workflow (reframe → outside-view → canon-librarian → generator → critic → synthesis), then iterating after the user pointed out missed primitives (slash commands, output styles, Routines, Managed Agents) and an entirely missed axis (multi-model / cross-model orchestration).

Two critic rounds. The first round forced abandonment of a "skills are SOTA" framing in favour of a workload-conditional routing table. The second round forced a full rewrite that (a) dropped unverifiable arXiv-ID-with-specific-numbers citations to snippet-level claims, (b) regrouped a 19-row flat catalog into four mechanism groups, (c) separated mechanisms from usage patterns, (d) restored cross-model orchestration to its proper weight after over-correction.

## What this is NOT

- Not an implementation plan for any new primitive.
- Not a recommendation to add skills, agents, hooks, or any other authored object to this repo.
- Not vendor-canonical guidance — Anthropic's docs are the canonical source. This is a *synthesis* across vendor docs, community signal, recent literature (snippet-level), and applied judgment.
- Not stable for 12 months. Primitive consolidation in this ecosystem has accelerated (slash commands collapsed into skills; Routines and Managed Agents shipped April 8 / April 14 2026). Re-validate this document each release cycle.

## Provenance & retrieval honesty

- **Canon librarian explicitly returned `## Corpus coverage: none`** for the specific Claude-Code-Skills-vs-subagents question. Corpus contains general 2024–2025 agentic-design essays (Anthropic *Building Effective Agents*, *Effective Context Engineering for AI Agents*, *How we built our multi-agent research system*, *Agentic Problem Frames 2026*) but no ingested body text on Skills, slash commands, hooks, MCP, `CLAUDE.md`, or post-2025-Q3 Claude Code material.
- **Web fallback was authorized** under the stack's own routing rule. Anything cited from the web is not promoted to canon by being cited once.
- **Some research streams admitted snippet-only retrieval** — particularly the 2026 multi-model literature pass. Specific paper IDs and percentages from those streams are flagged as **directional, unverified at primary source** below. The upgrade process should re-verify before committing infrastructure on them.
- **Outside-view base rates** were the forecaster's estimates from adjacent reference classes (developer-tool extension primitives, LLM agent frameworks, plugin marketplaces). They are not measured field statistics.

---

## 1. Terminology

There is no universally settled umbrella term for the set {skills, subagents, hooks, MCP servers, CLAUDE.md, slash commands, output styles, plugins, Routines, Managed Agents, ...}. Three live options:

- **"Primitives"** — community/practitioner term (Daniel Miessler, alexop.dev, most blog taxonomies). Best single word: precise, vendor-neutral, treats them as composable building blocks. **Recommended for prose.**
- **"Extensions"** — Anthropic's official term. The docs page is literally titled *Extend Claude Code*. **Recommended when citing Anthropic.**
- **"Components" / "surface"** — informal ("the Claude Code surface area"). Looser; useful when discussing the whole authored layer including settings.

**Do not use as umbrella terms:**
- "Tools" — means MCP-style function calls specifically.
- "Agents" — means one specific primitive (subagents).
- "Plugins" — a *distribution wrapper*, not the unit being distributed.

---

## 2. The reframe that drove this synthesis

The question *"is X still SOTA?"* is itself a weak frame for this domain. It collapses a multi-axis design space onto a one-dimensional timeline and treats orthogonal primitives as if they were generations of the same thing. Two specific failure modes:

1. **Motte-and-bailey risk.** "Skills and subagents are orthogonal" cannot coexist with "if forced, pick skills" — those statements compete. The first round of synthesis fell into this trap; the critic forced the rewrite.
2. **Premature consolidation risk** (outside-view forecaster's modal failure mode for "new primitive replaces old"): a user rewrites their working subagent-based stack into Skills, then 6 months later discovers Skills doesn't handle a use case subagents did, and rebuilds the subagent layer *inside* Skills, badly.

The honest reframe: there is **no single SOTA orchestration**. There is a constraint-matching procedure across mechanism groups, plus a separate cross-model axis, plus workload archetypes. Pick the smallest set that covers your bottleneck.

---

## 3. The mental model: four mechanism groups

Each row is a *mechanism* — the user-authored, repo-resident object. Usage patterns (self-critique loops, debate, architect-coder splits) are compositions on top of these and live in §4.

### Group A — Context-shaping (what the model sees)

| Mechanism | Where it lives | When to author it |
|---|---|---|
| `CLAUDE.md` / `AGENTS.md` (≤200 lines) | Repo root, user-level, or org-level | Project rules every session needs |
| `.claude/rules/` (path-scoped fragments) | Markdown files with `paths:` frontmatter | Rules tied to file patterns; load conditionally |
| Auto `MEMORY.md` | Written by Claude across sessions | Cross-session learnings; first ~200 lines load every session |
| `@`-mentions / file references | Inline in prompts | Per-message context injection distinct from CLAUDE.md |
| Output styles | `.claude/output-styles/` (markdown + YAML) | Repeated tone / role / format change |

**Bottleneck this group trades against:** model attention and context budget. Vercel's January 2026 evals (directional, unverified at primary source in this pass) reportedly showed an 8KB `AGENTS.md` outperforming a roughly equivalent skill, with skills failing to trigger in a meaningful fraction of cases. Honest implication: for plain rule injection, fatten top-level instructions before authoring skills.

### Group B — Execution-shaping (when and where work runs)

| Mechanism | Where it lives | When to author it |
|---|---|---|
| Hooks (5 flavors: command, HTTP, MCP-tool, prompt, agent) | `settings.json` or `plugin/hooks/hooks.json` | Events that must always fire (lint, format, gates) |
| Subagents | `.claude/agents/<name>.md` | Parallel work, large reads, role separation, adversarial review |
| Background tasks (`run_in_background`) | Bash and Agent SDK parameter | Long-running side work in the same session |
| Plan mode / permission modes | `settings.json`; `ExitPlanMode` tool | Read-only or restricted execution shaping |
| Sandboxed execution | Bounded process environment | Constrained tool surface for risky operations |
| Routines (cloud, scheduled — research preview, shipped April 14, 2026) | `claude.ai/code/routines` UI; `/schedule` | Cron / webhook / API-triggered runs |
| Managed Agents (public beta, shipped April 8, 2026) | `platform.claude.com` hosted service | Hosted long-running production deployment |

**Bottleneck this group trades against:** determinism (hooks), context isolation (subagents), wall-clock concurrency (background), unattended trigger surface (Routines), and infrastructure ownership (Managed Agents). Each row is a *different* execution-shape, even though the casual reader sometimes treats them as alternatives.

### Group C — Tools & boundaries

| Mechanism | Where it lives | When to author it |
|---|---|---|
| MCP servers | `.mcp.json`, managed settings, or remote | Anything crossing a process boundary (DB, API, browser, SaaS, Linear, Slack) |
| Skills, model-invocable | `.claude/skills/<name>/SKILL.md` (+ optional supporting files) | Workflow Claude should auto-load when relevant |
| Skills, user-invocable as `/cmd` | Same files, frontmatter triggers `/cmd` exposure | You want to *type the trigger* explicitly |
| **Eval harnesses** (first-class part of the orchestration stack) | Promptfoo configs, custom eval scripts, judge ensembles | The thing that tells you whether the rest works |

**On "slash commands":** legacy `.claude/commands/*.md` still resolves, but the documented path is *Skills with user-invocable frontmatter*. Skills and slash commands are the **same primitive with two invocation contracts** (model-triggered vs user-triggered). Treat them as one mechanism, two modes.

**On eval harnesses as a primitive:** this was the most important addition the second critic round forced. A stack with Skills + Subagents + Hooks + MCP and no eval harness is a stack with no fitness signal. Eval harnesses (Panel-of-LLMs / SE-Jury / Promptfoo / judge ensembles) belong in the mental model as a first-class mechanism, not as an afterthought "and you should test it."

### Group D — Distribution & authorization

| Mechanism | Where it lives | When to author it |
|---|---|---|
| Plugins | `.claude-plugin/plugin.json` manifest + bundled skills/agents/hooks/MCP/LSP/monitors | Cross-repo, cross-team sharing |
| `settings.json` / `settings.local.json` (hierarchy: managed > local > project > user) | Repo and user levels | Permissions (`allow`/`deny`), env vars, hook registration, MCP enablement |
| Agent SDK (`@anthropic-ai/claude-agent-sdk`) | npm/pip package | Authoring against the runtime *outside* Claude Code itself |

**Plugins are not an extension primitive.** They are a *distribution wrapper*. They have no runtime effect of their own — they bundle, namespace, and version other mechanisms. Conflating "use plugins" with "use skills/hooks/agents" is a category error common in early-2026 community taxonomies.

**The Agent SDK is a meta-primitive.** Claude Code is itself built on it. If your authoring target is "an application that contains agents" rather than "Claude Code as a developer tool," the SDK is the foundation, and Claude Code-specific mechanisms are not the right frame at all.

---

## 4. Usage patterns (compositions, not primitives)

These are *patterns* that compose mechanisms from §3. Treating them as primitives was a category error in the first synthesis. Each pattern can be implemented with several different mechanism choices.

| Pattern | Composition (typical) | When the pattern earns its complexity |
|---|---|---|
| **Self-critique / Constitutional-AI loop** | Subagent (implementer) + subagent (critic) in fresh contexts; orchestrator routes between them | Decisions where a wrong answer is expensive (this is what `claude-critic-stack` itself is) |
| **Plan-execute split (same model)** | Subagent (planner) → subagent (executor) | Tasks where the cost of a wrong path is much greater than the cost of planning |
| **Architect-coder split (cross-model)** | Frontier model plans, cheaper model executes | Cost arbitrage when token cost dominates (Aider, Roo Code's Architect/Code/Debug/Ask modes) |
| **Self-consistency / multi-sample** | Same model, N samples, vote or aggregate | Sampling variance is the bottleneck; high-stakes single-shot tasks |
| **Same-model aggregation (Self-MoA pattern)** | One strong model, multiple samples, aggregator | Directional 2026 finding: often beats cross-vendor mixes on at least some benchmarks (unverified at primary source) |
| **Cross-model parallel-and-judge** | N vendor models, judge synthesizes | High-stakes verification, eval credibility, vendor hedging |
| **Cross-model debate** | N models argue, judge decides | Research-active, production-rare; documented adversarial-debater failure modes |
| **Eval-driven router** | Pre-measured per-task fitness; route per request | Production routing where workload is heterogeneous |
| **High-stakes pre-commit verification with diverse checkers** | Parallel reviewers on different angles (logic / edges / security / perf), each finding independently reproduced | Cost of a wrong answer dominates cost of verification (`/ultrareview` is one productized instance) |

**Important:** the patterns are *not* mutually exclusive. A real stack can run a self-critique loop *inside* a high-stakes verification archetype, or a plan-execute split *inside* a self-consistency loop. The mistake is naming them as if they were rivalrous.

---

(continued — chunk 2 of 5)
