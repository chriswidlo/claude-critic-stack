# SOTA orchestration knowledge — Part 3 (sources & verifiability)

> Continuation of `plans/2026-04-25-claude-code-orchestration-sota.md` and `...-part2.md`. This file holds section 11 alone — the source list. It is the section the upgrade process most needs to verify and re-fetch at primary source.

---

## 11. Sources & verifiability

### Anthropic-official (canonical for primitive surface)

- `https://code.claude.com/docs/en/features-overview` — *Extend Claude Code* (decision table; Skill-vs-Subagent comparison)
- `https://code.claude.com/docs/en/skills` — Skills guide
- `https://code.claude.com/docs/en/sub-agents` — Subagents guide
- `https://code.claude.com/docs/en/hooks-guide` and `/hooks` — Hooks guide and reference (5 implementation flavors)
- `https://code.claude.com/docs/en/mcp` — MCP integration
- `https://code.claude.com/docs/en/memory` — Memory / `CLAUDE.md` guide
- `https://code.claude.com/docs/en/output-styles` — Output styles
- `https://code.claude.com/docs/en/plugins` — Plugins (distribution wrapper)
- `https://code.claude.com/docs/en/routines` — Routines (research preview, April 14, 2026)
- `https://code.claude.com/docs/en/ultrareview` — `/ultrareview` (one productized instance of high-stakes-verification archetype)
- `https://platform.claude.com/docs/en/managed-agents/overview` — Managed Agents (public beta, April 8, 2026)
- `https://platform.claude.com/docs/en/agent-sdk/overview` — Agent SDK (meta-primitive)
- `https://agentskills.io` — Open `SKILL.md` standard (cross-tool)

### Anthropic engineering posts (in canon manifest, body text not yet ingested in this repo as of April 2026)

- *Building Effective Agents* (2024) — `anthropic-building-effective-agents`
- *Effective Context Engineering for AI Agents* (2025) — `anthropic-effective-context-engineering`
- *How we built our multi-agent research system* (2025) — `anthropic-multi-agent-research-system`
- *Equipping agents for the real world with Agent Skills* (2025; direct fetch returned 403 in this pass)

### Community signal (lagging indicators; cited as snippets, verify before acting)

- `obra/superpowers` — top-starred plugin/marketplace bundle; skills-first composition; accepted into Anthropic plugin marketplace January 15, 2026
- `VoltAgent/awesome-agent-skills` — skills-only collection, cross-tool (Claude / Codex / Cursor / Gemini CLI)
- `hesreallyhim/awesome-claude-code` — curated list, no opinionated guidance
- `alirezarezvani/claude-skills` — mixed 235 skills + 28 agents + 27 commands; *"Skills = how, Agents = what, Personas = who"* taxonomy
- `rohitg00/awesome-claude-code-toolkit` — kitchen-sink (135 agents + 35 skills + 42 commands + 20 hooks + plugins); illustrative of the over-authoring failure mode

### Practitioner blogs / posts

- Simon Willison, *Claude Skills are awesome…* (2025-10-16, simonwillison.net) — pro-skills
- Hamel Husain, *evals-skills* (hamel.dev) — shipped evals as a skills plugin
- Daniel Miessler, *When to Use Skills vs Workflows vs Agents* (danielmiessler.com)
- alexop.dev, *Understanding Claude Code's Full Stack* — most cited mental model
- Colin McNamara, *Understanding Skills, Agents, Subagents, and MCP*
- Vercel, *AGENTS.md outperforms skills in our agent evals* (Jan 2026, vercel.com/blog) — empirical contrarian; **8KB AGENTS.md reportedly 100% pass vs 79% skill, skill not invoked 56% of cases.** Directional. Verify before citing externally.
- Boris Cherny, `howborisusesclaudecode.com` — "both subagents and skills"
- *Towards Data Science*, *Claude Skills and Subagents: Escaping the Prompt Engineering Hamster Wheel*
- Dean Blank, *A Mental Model for Claude Code* (March 2026, levelup.gitconnected.com)

### Multi-model literature (2026; **directional, retrieved at snippet level, unverified at primary source in this pass**)

- *Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets* — single-agent ties or beats multi-agent under matched compute
- *Rethinking the Value of Multi-Agent Workflow: A Strong Single Agent Baseline* — same finding in different setup
- *Self-MoA* — same-model aggregation reportedly beats cross-vendor mixes on at least one benchmark
- *DeepConf* / *ReASC* / *CISC* — efficiency-focused descendants of self-consistency; confidence-gated early stopping
- *Debating Truth* — cross-model debate, mixed results
- *AgentCourt* / *AgenticSimLaw* — courtroom-style frameworks; gains on claim verification
- *When collaboration fails* (Nature Sci Reports 2026) — adversarial debater drops group accuracy 10–40%, raises consensus-on-wrong-answers >30%
- *SE-Jury* — software-engineering-specific judge ensemble
- *LLM Jury-on-Demand* — reliability predictor that picks per-instance jury composition
- *Verdict* whitepaper (Haize Labs) — judge-time compute library
- *Mixture-of-Agents* (original) and *Self-MoA* (rethinking)

**The arXiv IDs and specific percentages from this stream were dropped from the prose synthesis** because they were retrieved at snippet level and the critic flagged citing them with precision as a credibility risk. Upgrade-process action: re-verify against primary sources before promoting any of these to canon.

### Tools / products that ship multi-model orchestration

- **Anthropic `/ultrareview`** — cloud sandbox, parallel reviewer agents on different angles, independent reproduction of findings, $5–20/run after 3 free runs (free tier reportedly expires May 5, 2026)
- **OpenRouter** — provider routing + model fallbacks; cheap-first escalation chain
- **Promptfoo** — eval-driven model-vs-model comparison
- **LangGraph** — orchestration substrate (not turnkey ensemble)
- **Aider** — `/editor-model` and `/weak-model` architect-coder split (>18 months in production)
- **Roo Code** — Architect / Code / Debug / Ask modes with restricted tool access; per-mode model selection
- **Cline**, **Continue.dev** — multi-model exposed as user config

### Reference-class adjacent (cited as base-rate evidence in outside-view step)

- VS Code extension model evolution — extensions / settings / tasks / dev containers / profiles all coexist
- Emacs `defadvice` → `nadvice` migration — coexisted for years
- npm peerDependencies / optionalDependencies / workspaces — additive, never substitutive
- GitHub Actions composite / reusable / custom — coexist with persistent user confusion
- LLM agent framework half-life 2022–2025 — LangChain agents, AutoGPT, BabyAGI, CrewAI, MetaGPT, OpenAI Assistants API, OpenAI Swarm. Most peaked-and-declined within 12 months of "SOTA" status

---

> Continued in `plans/2026-04-25-claude-code-orchestration-sota-part4.md` (sections 12–13: destinations + open questions for the upgrade process).
