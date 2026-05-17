# Anthropic Engineering & Research on Building AI Workflows (2024–2026)

A citation-heavy survey of Anthropic posts on AI agents and workflows, with verbatim quotes, distilled patterns, caveats, and answers to seven cross-cutting questions. Dates note what's been superseded.

---

## 1. *Building Effective Agents* — Schluntz & Zhang, **Dec 19, 2024**

[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) is the canonical taxonomy. It draws a hard line:

> "Workflows: Systems where LLMs and tools are orchestrated through predefined code paths."
>
> "Agents: Systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."

Five workflow patterns and one agent pattern, verbatim:

- **Prompt chaining** — *"Decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one."* For tasks *"easily and cleanly decomposed into fixed subtasks."*
- **Routing** — *"Classifies an input and directs it to a specialized followup task."* For *"distinct categories that are better handled separately."*
- **Parallelization** — *"LLMs can sometimes work simultaneously on a task and have their outputs aggregated programmatically."* For speed or *"multiple perspectives."*
- **Orchestrator-workers** — *"A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."* For *"complex tasks where you can't predict the subtasks needed."*
- **Evaluator-optimizer** — *"One LLM call generates a response while another provides evaluation and feedback in a loop."* For *"clear evaluation criteria, and when iterative refinement provides measurable value."*
- **Agents** — *"Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement."* For *"open-ended problems where it's difficult or impossible to predict the required number of steps."*

**Tools get equal billing to prompts:** *"Tool definitions and specifications should be given just as much prompt engineering attention as your overall prompts."* Three heuristics: give the model *"enough tokens to 'think' before it writes itself into a corner"*; *"Keep the format close to what the model has seen naturally occurring in text on the internet"*; avoid formatting overhead. A good definition *"often includes example usage, edge cases, input format requirements, and clear boundaries."*

**Most actionable.** Start with the simplest composition (a single LLM call with retrieval and tool calls). The core stance: *"Don't hesitate to reduce abstraction layers and build with basic components as you move to production."*

**Most overlooked.** Frameworks *"can also make it tempting to add complexity when a simpler setup would suffice."* The five workflow patterns are a menu to pick *one* from, not a checklist to compose. All quotes from [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents).

---

## 2. *How we built our multi-agent research system* — Jun 13, 2025

[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) is the production case study for orchestrator-worker, with hard numbers.

Headline: *"multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%."* Cost: *"agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."* Quality driver: *"token usage by itself explains 80% of the variance"* in research quality. Latency: *"these changes cut research time by up to 90% for complex queries."*

**Worth it:** *"Multi-agent systems excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools."* **Not worth it:** *"Most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time."* Also: *"Some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today."*

**Subagent context strategy:**

> "Subagents facilitate compression by operating in parallel with their own context windows, exploring different aspects of the question simultaneously."

> "Rather than requiring subagents to communicate everything through the lead agent, implement artifact systems where specialized agents can create outputs that persist independently."

The second sentence is the rationale behind Claude Code's subagent transcript model and the session-artifact directories used throughout the present repository.

**Production reliability.** *"Minor changes cascade into large behavioral changes, which makes it remarkably difficult to write code for complex agents."* Remediation is checkpointing not retry: *"we built systems that can resume from where the agent was when the errors occurred."* Rollouts use *"rainbow deployments to avoid disrupting running agents."*

**Eval methodology:** *"We started with a set of about 20 queries representing real usage patterns."* *"A single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements."* But humans still catch what LLM judges miss: *"Human testers noticed that our early agents consistently chose SEO-optimized content farms over authoritative but less highly-ranked sources."*

**Most actionable.** Artifact/filesystem handoff avoids the synchronous bottleneck: *"the lead agent can't steer subagents, subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent to finish."*

**Most overlooked.** *"Agents struggle to judge appropriate effort for different tasks."*

**Anti-patterns flagged:** vague subagent prompts, *"Bad tool descriptions can send agents down completely wrong paths"*, and eval delay (*"AI developer teams delay creating evals because they believe only large evals with hundreds of test cases are useful"*).

---

## 3. *Effective Context Engineering for AI Agents* — Sep 29, 2025

[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) retired "prompt engineering" for agent work:

> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."

Three primitives anchor the discipline:

- **Compaction** — *"taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary."*
- **Structured note-taking** — *"the agent regularly writes notes persisted to memory outside of the context window."*
- **Sub-agent context isolation** — *"Rather than one agent attempting to maintain state across an entire project, specialized sub-agents can handle focused tasks with clean context windows."*

Tool design tightens: *"Tools should be self-contained, robust to error, and extremely clear with respect to their intended use."*

**Most actionable.** Treat the context window as a budget, not a scratchpad — compaction + note-taking + sub-agent isolation keep it below the degradation threshold.

**Most overlooked anti-pattern:** *"One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use."* The temptation to wire up every available MCP server fights this directly. All quotes from [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

---

## 4. *Best practices for Claude Code* — surveyed **May 2026**

[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) is the most prescriptive Anthropic document on agentic workflows and the authoritative source for the `CLAUDE.md` question (Q6).

### 4a-c. Explore-Plan-Code, Verification, Visual Iteration, Codebase Q&A

> "Letting Claude jump straight to coding can produce code that solves the wrong problem. Use plan mode to separate exploration from execution."

Four phases: Explore (plan mode) → Plan → Implement → Commit. Caveat: *"If you could describe the diff in one sentence, skip the plan."*

Verification is the single highest-leverage instruction: *"Include tests, screenshots, or expected outputs so Claude can check itself. This is the single highest-leverage thing you can do."* *"Claude performs dramatically better when it can verify its own work."*

Visual iteration via the Claude in Chrome extension which *"opens new tabs in your browser, tests the UI, and iterates until the code works."* Template: *"[paste screenshot] implement this design. take a screenshot of the result and compare it to the original."*

Codebase Q&A: *"You can ask Claude the same sorts of questions you would ask another engineer."* No special prompting required.

### 4e. CLAUDE.md (Q6)

> "CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can't infer from code alone."

> "Keep it concise. For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

Locations: home (`~/.claude/CLAUDE.md`, all sessions), project root (`./CLAUDE.md`, git-tracked), project root (`./CLAUDE.local.md`, gitignored), parent dirs (monorepo cascade), child dirs (on-demand). Imports via `@path/to/file`.

Diagnostic: *"If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."* Include: bash commands, non-default style rules, testing instructions, repo etiquette, gotchas. Exclude: anything inferrable from code, standard conventions, detailed API docs. Emphasis works: *"You can tune instructions by adding emphasis (e.g., 'IMPORTANT' or 'YOU MUST') to improve adherence."*

### 4f. Hooks vs MCP vs CLI (Q3)

CLI first (*"the most context-efficient way to interact with external services"*); MCP for stateful integrations (issue trackers, DBs, monitoring); hooks for invariants — *"Use hooks for actions that must happen every time with zero exceptions. … Hooks are deterministic and guarantee the action happens."*

### 4g. Sub-agents and parallel sessions (Q7)

> "Since context is your fundamental constraint, subagents are one of the most powerful tools available. … Subagents run in separate context windows and report back summaries."

Parallel sessions are recommended for *quality* too: *"a fresh context improves code review since Claude won't be biased toward code it just wrote."* For fan-out: `claude -p` in a shell loop with `--allowedTools` scoping.

### 4h. Anti-patterns ("Common failure patterns")

Kitchen-sink session (fix: `/clear` between tasks); correcting over and over (fix: after two failed corrections, `/clear` and write a better prompt); over-specified CLAUDE.md (fix: ruthlessly prune); trust-then-verify gap (fix: always provide verification); infinite exploration (fix: scope narrowly or use subagents). All from [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices).

**Most actionable.** Provide verification on every non-trivial task — *"the single highest-leverage thing you can do."*

**Most overlooked.** Bloated CLAUDE.md causes the model to ignore instructions; teams add but never prune.

---

## 5. The Anthropic Cookbook — agent patterns directory

[anthropic-cookbook / patterns / agents](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents/) holds reference implementations for *Building Effective Agents*: `basic_workflows.ipynb` (prompt chaining, routing, multi-LLM parallelization), `evaluator_optimizer.ipynb`, `orchestrator_workers.ipynb`. *"Example minimal implementations of common agent workflows discussed in the blog."* No framework dependencies.

**Most actionable:** read `orchestrator_workers.ipynb` *before* adopting any framework — the pattern is roughly 60 lines of Python. **Most overlooked:** no reference "agent" pattern beyond orchestrator-workers — intentional, since the agent pattern is the *last* option in the taxonomy.

---

## 6. Alignment Science: Petri & Bloom — eval-driven development

### 6a. Petri — **Oct 6, 2025**

[Petri](https://alignment.anthropic.com/2025/petri/) operationalizes "use AI agents to evaluate AI agents":

> "An open-source framework for automated auditing that uses AI agents to test the behaviors of target models across diverse scenarios."

> "The auditor agent forms the core of Petri's probing capabilities. It consists of two main components: a detailed system prompt and a set of tools."

> "The judge component scores generated transcripts across multiple dimensions."

The auditor/judge split — separate prompt for probing, separate prompt for scoring — is the pattern this repo's critic-panel lenses adopt.

### 6b. Petri 2.0 — **Jan 22, 2026**

[Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/) adds *"improvements to transcript realism to help counter eval-awareness"* and 70 new seed instructions. Load-bearing concern: *"A model may act more cautious or aligned during a test than it would under real deployment."* Fix: *"a realism classifier that helps keep auditor behavior within realistic bounds."* Remove environment-driven giveaways like *"implausible user behavior, inconsistent tool responses, or obviously planted honeypots"*; task-driven cues stay.

### 6c. Bloom — **Dec 19, 2025**

[Bloom](https://alignment.anthropic.com/2025/bloom-auto-evals/) complements Petri:

> "Bloom is an agentic framework for generating targeted evaluations for researcher-specified behavioral traits."

> "Bloom serves a complementary but separate purpose: generating in-depth evaluation suites for specific behaviors and quantifying their severity and frequency across automatically generated scenarios."

Four launch behaviors: *"delusional sycophancy, instructed long-horizon sabotage, self-preservation and self-preferential bias—across 16 frontier models."* Validation: *"Bloom's evaluations correlate strongly with our hand-labelled judgments and reliably separate baseline models from intentionally misaligned ones."*

**Most actionable.** Adopt the split: Petri-style open-ended audits to discover failure modes; Bloom-style targeted suites to quantify. Most teams skip step one — which is why evals stay green while users complain.

**Most overlooked.** Eval-awareness is real: *"Evaluation realism remains an open challenge"* ([Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/)).

---

## 7. *Claude Opus 4.7* — Release notes, **Apr 16, 2026**

[What's new in Claude Opus 4.7](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7) — several changes directly affect agent prompt design.

**Adaptive thinking replaces extended-thinking budgets:** *"Extended thinking budgets are removed in Claude Opus 4.7. … Adaptive thinking is the only thinking-on mode, and in our internal evaluations it reliably outperforms extended thinking."* It is *"off by default. Requests with no `thinking` field run without thinking."*

**Task budgets (beta):** *"A task budget gives Claude a rough estimate of how many tokens to target for a full agentic loop, including thinking, tool calls, tool results, and final output. The model sees a running countdown and uses it to prioritize work and finish the task gracefully as the budget is consumed."* Reserve for bounded workloads; *"for open-ended agentic tasks where quality matters more than speed, do not set a task budget."* This is the explicit fix for *"Agents struggle to judge appropriate effort for different tasks."*

**Behavior changes that invalidate older prompt scaffolding (verbatim):**

> "More literal instruction following, particularly at lower effort levels. The model will not silently generalize an instruction from one item to another, and will not infer requests you didn't make."
>
> "Response length calibrates to perceived task complexity rather than defaulting to a fixed verbosity."
>
> "Fewer tool calls by default, using reasoning more. Raising effort increases tool usage."
>
> "More regular progress updates to the user throughout long agentic traces. If you've added scaffolding to force interim status messages, try removing it."
>
> "Fewer subagents spawned by default. Steerable through prompting."

**Tokenizer change** — *"This new tokenizer may use roughly 1x to 1.35x as many tokens when processing text compared to previous models."* Update `max_tokens` headroom; recompute per-token costs.

**Most actionable.** Re-baseline existing prompts on 4.7 with defensive scaffolding *removed* — *"try removing that scaffolding and re-baselining."*

**Most overlooked.** Adaptive thinking is **off by default**. A prompt migrated as-is from 4.6 with no `thinking` field runs thinking-off on 4.7 — silently changes behavior across an entire agent fleet.

---

## 8. *Claude Code quality postmortem* — Apr 23, 2026

[An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) is the only Anthropic post that reads like a SEV postmortem — required reading for anyone shipping agent software.

Three overlapping changes degraded Claude Code: *"On March 4, we changed Claude Code's default reasoning effort from `high` to `medium`"* (reverted Apr 7); *"On March 26, we shipped a change to clear Claude's older thinking from sessions that had been idle for over an hour"* — a bug made this happen *every turn*, leaving Claude *"forgetful and repetitive"*; *"On April 16, we added a system prompt instruction to reduce verbosity… it hurt coding quality and was reverted on April 20."*

The deep observation: *"Neither our internal usage nor evals initially reproduced the issues."* *"These bugs passed multiple human and automated code reviews, as well as unit tests, end-to-end tests, automated verification, and dogfooding."* Remediation: *"a larger share of internal staff use the exact public build"*, *"tighter controls on system prompt changes"*, *"soak periods, a broader eval suite, and gradual rollouts."*

**Most actionable.** Treat every system-prompt change and every model-default change as a release with its own eval gate. The worst bug was a cache bug that progressively erased thinking — exactly the kind of failure integration tests miss because turn one looks fine.

**Most overlooked.** Per-change evals don't catch the *interaction* of three independent changes shipped six weeks apart. You need soak time on the integrated build.

---

## Cross-cutting questions — direct answers with citations

### Q1. When multi-agent vs single-agent?

[Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system): *"Multi-agent systems excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools."* Negative case: *"most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time."* Confirmed by Opus 4.7's *"Fewer subagents spawned by default"* ([Opus 4.7 release notes](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)).

### Q2. Sub-agent context handling?

Three layered recommendations: (1) Run them in their own context windows — *"Subagents facilitate compression by operating in parallel with their own context windows"* ([Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)); (2) Pass artifacts, not chat — *"implement artifact systems where specialized agents can create outputs that persist independently"* (same); (3) Use sub-agents as a context-isolation primitive — *"specialized sub-agents can handle focused tasks with clean context windows"* ([Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

### Q3. Tools vs MCP vs hooks?

From [Claude Code best practices](https://code.claude.com/docs/en/best-practices): CLI tools first (*"the most context-efficient way to interact with external services"*); MCP for stateful integrations (issue trackers, DBs, monitoring); hooks for invariants (*"Use hooks for actions that must happen every time with zero exceptions. … Hooks are deterministic and guarantee the action happens"*). [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) warns: *"One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use."*

### Q4. Evals?

Start small now: *"We started with a set of about 20 queries representing real usage patterns. … AI developer teams delay creating evals because they believe only large evals with hundreds of test cases are useful"* ([Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). LLM-as-judge works if kept simple: *"a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent."* Pair open-ended auditing ([Petri](https://alignment.anthropic.com/2025/petri/)) with targeted suites ([Bloom](https://alignment.anthropic.com/2025/bloom-auto-evals/)). Watch for eval-awareness ([Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/)).

### Q5. Prompt caching?

See [Prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). Agentic tool use is one of the highest-leverage caching cases — each turn re-sends the prefix. Cache reads are 0.1× input price; 5-min writes 1.25×; 1-hr writes 2×. Tool surface and model identity are cache boundaries. The 15× multi-agent multiplier makes caching mandatory in production.

### Q6. CLAUDE.md?

Covered in §4e. Keep short; pin to bash commands, non-default style, workflow rules, gotchas, env quirks; exclude anything inferrable; `@path/to/file` imports; place at home / project root / parent / child; *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"* ([Claude Code](https://code.claude.com/docs/en/best-practices)).

### Q7. Parallel sub-agents?

Research breadth: parallel subagents, accept 15× cost — *"token usage by itself explains 80% of the variance"* ([Multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system)). Coding: prefer parallel *sessions* (Writer/Reviewer) — *"a fresh context improves code review since Claude won't be biased toward code it just wrote"* ([Claude Code](https://code.claude.com/docs/en/best-practices)). Scale: shell-loop `claude -p` with `--allowedTools`. Bottleneck to design around: *"the lead agent can't steer subagents, subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent to finish."*

---

## Anti-patterns Anthropic explicitly flags (consolidated)

- Premature framework abstraction: *"Don't hesitate to reduce abstraction layers and build with basic components as you move to production."* [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- Vague subagent prompts, bad tool descriptions, assuming agents know how much effort to spend, delaying evals. [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- *"Bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use."* [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Bloated CLAUDE.md, kitchen-sink sessions, correction loops past two, trust-then-verify gap, infinite exploration. [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Migrating prompts to Opus 4.7 without removing scaffolding. [Opus 4.7 release notes](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7)
- Shipping system-prompt changes without per-model evals and soak periods. [April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem)
- Running evals that look like evals: *"A model may act more cautious or aligned during a test than it would under real deployment."* [Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/)

## Top 12 actionable patterns — ranked

1. **Give Claude a way to verify its work** (tests, screenshots, expected outputs) — *"the single highest-leverage thing you can do"* ([Claude Code](https://code.claude.com/docs/en/best-practices)).
2. **Start with the simplest workflow that works** — *"Don't hesitate to reduce abstraction layers"* ([Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)).
3. **Manage context as a budget** — compaction + note-taking + sub-agent isolation ([Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
4. **Use Explore-Plan-Code** for non-trivial coding ([Claude Code](https://code.claude.com/docs/en/best-practices)).
5. **Keep CLAUDE.md short and pruned** — bloat causes ignored instructions ([Claude Code](https://code.claude.com/docs/en/best-practices)).
6. **Run subagents in their own context with artifact-based handoff** ([Multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system)).
7. **Build evals on day one with ~20 real queries** ([Multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system)).
8. **Use a single LLM call with 0.0–1.0 score + pass/fail as judge** ([Multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system)).
9. **Pair Petri-style open-ended audits with Bloom-style targeted suites** ([Petri](https://alignment.anthropic.com/2025/petri/) + [Bloom](https://alignment.anthropic.com/2025/bloom-auto-evals/)).
10. **Hooks for invariants, CLI tools first, MCP for stateful integrations** ([Claude Code](https://code.claude.com/docs/en/best-practices)).
11. **Treat each tool description as load-bearing prompt engineering** ([Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)).
12. **For long-running agents, design for resumability and rainbow deployments** ([Multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system)).

---

## Reading order for a new builder

[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) → [cookbook patterns/agents](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents/) → [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) → [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) → [Claude Code best practices](https://code.claude.com/docs/en/best-practices) → [Petri](https://alignment.anthropic.com/2025/petri/) + [Bloom](https://alignment.anthropic.com/2025/bloom-auto-evals/) + [Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/) → [Opus 4.7 release notes](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7) → [April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem).

The Dec 2024 taxonomy is stable. Model defaults and tool surfaces are not — re-check release notes and Claude Code best practices quarterly.
