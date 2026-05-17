# Anthropic engineering & research publications on AI workflow design — canonical survey, 2026

**Scope.** Every Anthropic-authored publication (engineering blog, alignment-science blog, cookbook, system-card excerpt, and platform docs) that bears on how to design AI workflows and agents, as of May 2026. Each claim is anchored to a verbatim quote and a dated URL. This document is intended to be the foundation citation set so that downstream practitioner notes do not have to re-research the canon.

**Reading conventions.** Quoted material is verbatim, italicized or block-quoted; `[...]` marks in-quote elisions. Dates are original publication when known. Behavior-change claims tied to model versions are noted as such — they expire on the next model release.

---

## 1. Engineering blog — workflow & agent canon

### 1.1 *Building Effective Agents* — Erik Schluntz & Barry Zhang, Dec 19 2024

URL: `https://www.anthropic.com/engineering/building-effective-agents`. The canonical taxonomy. Every later Anthropic post on agents refers back to this vocabulary; the cookbook `patterns/agents/` is its reference implementation.

**Workflow vs. agent distinction (load-bearing).**

> *Workflows: "Systems where LLMs and tools are orchestrated through predefined code paths."*
>
> *Agents: "Systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."*

This distinction is the single most-cited frame in the rest of the corpus. Practitioner consequence: choose workflow when steps are predictable; choose agent only when the path can't be enumerated.

**The five workflow patterns.**

1. **Prompt chaining** — *"Decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one."*
2. **Routing** — *"Classifies an input and directs it to a specialized followup task."*
3. **Parallelization** — *"LLMs can sometimes work simultaneously on a task and have their outputs aggregated programmatically,"* with two variants:
   - *Sectioning: "Breaking a task into independent subtasks run in parallel."*
   - *Voting: "Running the same task multiple times to get diverse outputs."*
4. **Orchestrator-workers** — *"A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."*
5. **Evaluator-optimizer** — *"One LLM call generates a response while another provides evaluation and feedback in a loop."*

**The autonomous agent loop.** Agents *"begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently."* They obtain *"ground truth from the environment at each step"* and may *"pause for human feedback at checkpoints."*

**When workflows vs agents.** Workflows fit *"complex tasks where there are distinct categories that are better handled separately"* with predictable steps. Agents fit *"open-ended problems where it's difficult or impossible to predict the required number of steps"* and where *"you can't hardcode a fixed path."*

**Tool design guidance (the "ACI" frame).** *Invest in agent-computer interfaces (ACI) as much as human-computer interfaces (HCI).* Specific instructions:

- *"Give the model enough tokens to 'think' before it writes itself into a corner."*
- *"Keep the format close to what the model has seen naturally occurring in text on the internet."*
- *Avoid "formatting overhead such as having to keep an accurate count."*
- *Include "example usage, edge cases, input format requirements, and clear boundaries."*

**Anti-pattern.** *"Avoid adding complexity unless it 'demonstrably improves outcomes.' Start with simple prompts, optimize them with comprehensive evaluation before implementing multi-step systems."* This is the canon's first and most important "do not" — it gates every other recommendation in the corpus.

### 1.2 *How we built our multi-agent research system* — Jun 13 2025

URL: `https://www.anthropic.com/engineering/multi-agent-research-system`. Production case for orchestrator-worker; source of the most-cited numerical claims about multi-agent systems.

**The three numbers everyone quotes:**

- *"multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%"* on their internal research eval.
- *"multi-agent systems use about 15× more tokens than chats"* — the cost ceiling.
- *"token usage by itself explains 80% of the variance"* in browsing-agent performance.

**When multi-agent vs single-agent (verbatim):** *"Multi-agent systems excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools."* Poor fits: *"domains requiring all agents to share the same context"* or *"many dependencies between agents."* Cross-reference the 15× cost — multi-agent is only justified when task value clears that bar.

**Artifact handoff.** *"Rather than requiring subagents to communicate everything through the lead agent, implement artifact systems where specialized agents can create outputs that persist independently... reduces token overhead from copying large outputs through conversation history."* Operational consequence of sub-agent context isolation: outputs land in storage, not the orchestrator's window.

**Rainbow deployments.** *"We use rainbow deployments to avoid disrupting running agents, by gradually shifting traffic from old to new versions while keeping both running simultaneously."* Agent runs are long-lived state machines; treat traffic shifting like a stateful database migration, not a stateless web rollout.

**Eval methodology.** *"Started with a set of about 20 queries representing real usage patterns"* — don't wait for a benchmark suite. *"A single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent"* — multi-call rubric grading lost.

**Sub-agent context handling.** *"Agents can spawn fresh subagents with clean contexts while maintaining continuity through careful handoffs... retrieve stored context like the research plan from their memory rather than losing previous work."* First layer of the three-layer context-hygiene stack (see §1.3).

**Prompt-engineering principles.** Orchestrators: teach delegation with clear objectives, output formats, tool guidance, boundaries; *scale effort to query complexity* (simple = 1 agent / 3–10 calls; complex = 10+ subagents); use extended thinking to plan. Subagents: *start wide, then narrow down;* use interleaved thinking to evaluate gaps; *use 3+ tools in parallel* for speed. General: *think like your agents* via Console simulations; embed *explicit heuristics* for tool selection; *let agents improve themselves* by having Claude diagnose failure traces.

**Anti-patterns flagged:** vague orchestrator instructions ("research the semiconductor shortage"); sequential subagent execution where parallel would do; overinvestment in simple queries; synchronous-only execution.

### 1.3 *Effective Context Engineering for AI Agents* — Sep 29 2025

URL: `https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents`. The post that elevated "context engineering" above prompt engineering as the dominant design concern for long-running agents.

**The attention-budget frame.**

> *"Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context."*

This is the cognitive frame that organizes the rest of the post. Practical consequence: every token in context spends budget; cheap tokens (boilerplate, stale logs) crowd out expensive ones (the actual problem statement).

**Context engineering vs. prompt engineering — the distinction.**

> *"Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."*

Prompt engineering = what you write. Context engineering = what's in the window at inference time, however it got there.

**Compaction (verbatim).**

> *"Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary... The art of compaction lies in the selection of what to keep versus what to discard, as overly aggressive compaction can result in the loss of subtle but critical context... we recommend carefully tuning your prompt on complex agent traces. Start by maximizing recall to ensure your compaction prompt captures every relevant piece of information from the trace, then iterate to improve precision by eliminating superfluous content."*

Operational order: recall first, then precision. Skipping the recall pass is how teams lose load-bearing context in compaction.

**Structured note-taking (agentic memory).**

> *"Structured note-taking, or agentic memory, is a technique where the agent regularly writes notes persisted to memory outside of the context window. These notes get pulled back into the context window at later times... This strategy provides persistent memory with minimal overhead."*

**Sub-agent context isolation.**

> *"Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)... This pattern... showed a substantial improvement over single-agent systems on complex research tasks."*

Combine 1.2 + 1.3 to get the *three layered recommendations for sub-agent context handling*: (a) spawn fresh sub-agents with clean contexts; (b) persist intermediate work in artifacts/files, not in the orchestrator's window; (c) return condensed distillations (1–2k tokens), not raw exploration traces.

**Bloated-tool-set anti-pattern (most-quoted line in the post).**

> *"One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."*

**Just-in-time vs. pre-computed context.**

> *"Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."*

This is the operational rationale for tools like Read, Grep, and Glob over front-loaded vector RAG: cheaper context, fresher data, lower risk of stale or wrong material polluting the window.

### 1.4 *Best practices for Claude Code* — `code.claude.com/docs/en/best-practices`

Originally on `anthropic.com/engineering/claude-code-best-practices`; 308-redirects to the docs home. Continuously edited; quotes here are as of May 2026.

**Core constraint underlying everything.** *"Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."*

**Explore-Plan-Code-Commit, verbatim phases.**

1. *Explore.* *"Enter plan mode. Claude reads files and answers questions without making changes."*
2. *Plan.* *"Ask Claude to create a detailed implementation plan."*
3. *Implement.* *"Switch out of plan mode and let Claude code, verifying against its plan."*
4. *Commit.* *"Ask Claude to commit with a descriptive message and create a PR."*

When to skip the plan step: *"For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly... If you could describe the diff in one sentence, skip the plan."*

**Verification is the single highest-leverage practice.**

> *"Give Claude a way to verify its work. Include tests, screenshots, or expected outputs so Claude can check itself. This is the single highest-leverage thing you can do."*

The frame: without verification, *"you become the only feedback loop, and every mistake requires your attention."*

**Visual iteration.** Use the *Claude in Chrome extension* to *"open new tabs in your browser, test the UI, and iterate until the code works."* The general principle is to give Claude a closed loop over the artifact it's modifying — tests for code, screenshots for UI, linter output for style.

**Codebase Q&A.** Treat Claude like a senior engineer for onboarding: ask *"How does logging work?"*, *"Why does this code call `foo()` instead of `bar()` on line 333?"* *No special prompting required.*

**CLAUDE.md content rules.** *"CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules."* **Include:** Bash commands Claude can't guess; code-style rules that differ from defaults; testing instructions and preferred runners; repo etiquette (branch naming, PR conventions); architectural decisions specific to your project; environment quirks; common gotchas. **Exclude:** anything Claude can infer from code; standard language conventions; detailed API docs (link to them); frequently changing info; long tutorials; file-by-file descriptions; self-evident practices like "write clean code."

Diagnostic test: *"For each line, ask: Would removing this cause Claude to make mistakes? If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"*

**The hooks-vs-MCP-vs-CLI-vs-skills-vs-subagents hierarchy.** The doc presents these as orthogonal extension points, each with a clear when-to-use:

- *CLI tools* — *"the most context-efficient way to interact with external services."* Use `gh`, `aws`, `gcloud`, `sentry-cli`.
- *MCP servers* — *"to connect external tools like Notion, Figma, or your database."* Use when CLI doesn't exist or when you need rich structured context (designs, monitoring panels).
- *Hooks* — *"for actions that must happen every time with zero exceptions. Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."*
- *Skills* — *"`SKILL.md` files in `.claude/skills/`"* for *"domain knowledge and reusable workflows... Claude loads them on demand without bloating every conversation."*
- *Subagents* — *"specialized assistants in `.claude/agents/` that Claude can delegate to for isolated tasks... run in their own context with their own set of allowed tools."*

Decision rule, distilled: deterministic = hook; rich external = MCP; CLI-shaped external = CLI tool; reusable knowledge with side effects = skill; isolated context work = subagent.

**The five common failure patterns (verbatim).**

1. *The kitchen sink session* — *"You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information. Fix: `/clear` between unrelated tasks."*
2. *Correcting over and over* — *"Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches. Fix: After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned."*
3. *The over-specified CLAUDE.md* — *"If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise. Fix: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook."*
4. *The trust-then-verify gap* — *"Claude produces a plausible-looking implementation that doesn't handle edge cases. Fix: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it."*
5. *The infinite exploration* — *"You ask Claude to 'investigate' something without scoping it. Claude reads hundreds of files, filling the context. Fix: Scope investigations narrowly or use subagents so the exploration doesn't consume your main context."*

**Subagents for investigation.** *"Since context is your fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries."*

**Parallel sessions.** Four mechanisms: worktrees, the desktop app, Claude Code on the web, and agent teams. The Writer/Reviewer pattern is explicitly endorsed: *"a fresh context improves code review since Claude won't be biased toward code it just wrote."*

**Headless / non-interactive mode.** *"With `claude -p 'your prompt'`, you can run Claude non-interactively, without a session... how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow."* For fan-out across files: loop `claude -p` with `--allowedTools` to scope permissions during unattended runs.

### 1.5 *Claude Code sandboxing* — Oct 20 2025

URL: `https://www.anthropic.com/engineering/claude-code-sandboxing`. Frames sandboxing as the solution to "approval fatigue" and prompt-injection blast radius. *"Sandboxing safely reduces permission prompts by 84%."* Both halves matter: *"effective sandboxing requires both filesystem and network isolation."* Without filesystem isolation an agent escapes; without network isolation it can exfiltrate credentials it never read. Filesystem is restricted to the working directory; network routes through a proxy that *"enforces restrictions on the domains that a process can connect to."*

### 1.6 *Claude Code auto mode* — Mar 25 2026

URL: `https://www.anthropic.com/engineering/claude-code-auto-mode`. Auto mode is *"a new mode for Claude Code that delegates approvals to model-based classifiers — a middle ground between manual review and no guardrails."* Three-tier filtering: built-in allowlist, in-project file ops (reviewable via VCS), transcript classifier for shell/web/external/out-of-project ops. Classifier accuracy: *0.4% false-positive, 17% false-negative on real overeager actions* — positioned as replacement for `--dangerously-skip-permissions`, not for deliberate approval on *"high-stakes infrastructure."*

### 1.7 *Enabling Claude Code to work more autonomously* — Sep 29 2025

URL: `https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously`. Announcement bundling checkpoints, subagents, hooks, background tasks. Key recommendation: *"use them in combination with version control."* Checkpoints are explicitly not a git replacement: *"Checkpoints apply to Claude's edits and not user edits or bash commands."*

### 1.8 *An update on recent Claude Code quality reports* — Apr 23 2026

URL: `https://www.anthropic.com/engineering/april-23-postmortem`. The only SEV-style public postmortem from Anthropic on agent quality. Three independent changes interacted to produce six weeks of degradation:

1. *"On March 4, we changed Claude Code's default reasoning effort from `high` to `medium`"* — reverted April 7.
2. *"On March 26, we shipped a change to clear Claude's older thinking from sessions that had been idle for over an hour"* — a bug caused this to repeat every turn. Fixed April 10.
3. *"On April 16, we added a system prompt instruction to reduce verbosity"* — degraded coding quality. Reverted April 20.

Why detection was slow: *"Because each change affected a different slice of traffic on a different schedule, the aggregate effect looked like broad, inconsistent degradation,"* and *"neither our internal usage nor evals initially reproduced the issues."* Load-bearing lesson — internal eval coverage didn't catch a regression production users felt within days.

Remediation: usage-limit reset, cache-bug fix (v2.1.101), reasoning-effort revert, verbosity-prompt revert, Code Review using Opus 4.7. Stated future changes: *ensure a larger share of internal staff use the exact public build;* tighter system-prompt controls including per-model evals, ablation testing, gradual rollouts for intelligence-affecting modifications. **Practitioner read:** if Anthropic struggles to ship safe prompt changes against a stable model, treat your own system-prompt edits with the gravity of code deploys.

---

## 2. Alignment Science blog — eval & honesty canon

### 2.1 *Petri* — Oct 6 2025

URL: `https://alignment.anthropic.com/2025/petri/`. Open-source auditing framework — **auditor agent** + **judge agent** + transcript viewer. The auditor *"forms the core of Petri's probing capabilities"* (sends user messages, sets system prompts, creates synthetic tools, simulates tool results, rolls back conversations, prefills responses). The judge *"first extracts key highlights and citations from the transcript — creating a structured outline"* before synthesis.

The **36 scoring dimensions** include `misaligned_behavior`, `cooperation_with_human_misuse`, `unprompted_deception_toward_user`, `unprompted_sycophancy`, `unprompted_encouragement_of_user_delusion`, `unprompted_leaking`, `unprompted_whistleblowing`, `unprompted_blackmail`, `unprompted_self_preservation`, `audit_situational_awareness`, `overrefusal`, plus emotional manipulation, broken tool use, and self-serving bias.

Workflow: hypothesis → seed instructions → automated assessment → iteration. Best practices: be specific; start simply and iterate; explicitly indicate which tools to use; *"encourage agency when testing autonomous behaviors;"* name target behaviors.

Caveat: *"Petri is not primarily built to be a benchmark and is not a substitute for careful human review."* And: *"Many Petri transcripts contain clues that a model could use to discern that the generated scenario isn't a real deployment"* — the eval-awareness problem that Petri 2.0 (§2.3) addresses.

### 2.2 *Bloom: an open-source tool for automated behavioral evaluations* — Dec 19 2025

URL: `https://alignment.anthropic.com/2025/bloom-auto-evals/`. Bloom is the four-stage automated pipeline that generates behavioral evaluations from a researcher-provided seed.

**The four stages.**

1. **Understand** — an agent reads the behavior description and any few-shot example transcripts, then generates a detailed understanding of what you're trying to measure (mechanisms, why-it-matters, summaries of examples).
2. **Ideate** — the agent generates evaluation scenarios designed to elicit the behavior of interest.
3. **Rollout** — an agent runs the scenarios in parallel, writing the system prompt and the initial user message, and simulating both the user and any tool responses so the environment develops dynamically.
4. **Judge** — the judge model scores each transcript for the target behavior plus secondary qualities; scores go to a meta-judge that produces an overall suite summary.

**What it surfaced first.** Four alignment-relevant suites: *delusional sycophancy*, *instructed long-horizon sabotage*, *self-preservation*, and *self-preferential bias.* The headline practitioner claim: *"These only took a few days to conceptualize, refine and generate with Bloom."* The competitive frame against static benchmarks: *"Unlike open-ended auditing, Bloom takes a researcher-specified behavior and quantifies its frequency and severity across automatically generated scenarios."*

### 2.3 *Petri 2.0* — Jan 22 2026

URL: `https://alignment.anthropic.com/2026/petri-v2/`. The headline improvement is realism mitigations against eval-awareness, plus 70 new seed scenarios.

**Eval-awareness drop on Claude.** *"On Claude models, the interventions together lead to a 47.3% median relative drop in eval-awareness compared to a 21.7% drop with just the new seeds."* The 25.6-point gap is the contribution of the realism classifier on top of the seed-quality work.

**The realism classifier.** *"A prompted realism classifier that monitors auditor behavior at each turn"* — it flags implausible actions and requests rewrites before content reaches the tested model. It distinguishes task-driven eval-awareness cues (inherent to the scenario) from environment-driven cues (implausible user behavior, inconsistent tool responses) and targets only the latter.

**New seed categories.** Collusion in multi-agent settings; conflicts between professional obligations and ethical considerations; scenarios where the target receives sensitive information that could exonerate another party; situations where the target can call a helpful-only model that lacks safety constraints.

### 2.4 *Modifying LLM Beliefs with Synthetic Document Finetuning* — Apr 24 2025

URL: `https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/`. SDF is *"(1) using an LLM to generate synthetic documents that reference a proposition, and then (2) doing supervised finetuning (SFT) on these documents as if they were additional pre-training data."* Three practitioner-relevant applications: **honeypotting** (*"SDF-inserted beliefs can influence the behavior of models pursuing malign objectives, making it easier to catch their malicious actions"*); **unlearning** (overwriting hazardous-topic knowledge that persists through jailbreaks); and **detecting misalignment** through model-organism research.

### 2.5 *Steering Evaluation-Aware Language Models to Act Like They Are Deployed* — Oct 2025 (arXiv 2510.20487)

The empirical motivation: *Anthropic found that Claude Sonnet 4.5 gave zero misaligned responses on a set of safety evaluations during pre-deployment testing, however Claude also mentioned that it is being evaluated over 80% of the time.* The technique adds a steering vector to activations to suppress evaluation-awareness during evaluation. The practitioner relevance is indirect but important: any safety eval that doesn't account for eval-awareness is over-reporting safety on frontier models. For agent builders, this is the formal justification for Petri 2.0's realism work and a warning that your own internal evals may be overestimating production behavior if they look obviously like tests.

---

## 3. Cookbook — `github.com/anthropics/anthropic-cookbook`

### 3.1 `patterns/agents/`

Reference implementation of *Building Effective Agents.* Three notebooks: `basic_workflows.ipynb` (chaining, routing, multi-LLM parallelization), `evaluator_optimizer.ipynb`, `orchestrator_workers.ipynb`. README: *"example minimal implementations of common agent workflows discussed in the blog."* Read with §1.1, not as production templates. Copy the control flow, not the prompts.

### 3.2 `misc/building_evals.ipynb`

Companion to §1.2's *"start with 20 queries"* claim. Demonstrates LLM-as-judge and code-based graders and judge-prompt iteration. (Cell content not reliably extractable from GitHub HTML; read the notebook directly.)

### 3.3 *Contextual retrieval* — Sep 19 2024

URL: `https://www.anthropic.com/news/contextual-retrieval`. Headline: *"Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49%."* With reranking: *67%.* The technique: *"Contextual Retrieval solves this problem by prepending chunk-specific explanatory context to each chunk before embedding."* Economically viable only with prompt caching (~$1.02 per million document tokens). When: *"For knowledge bases exceeding 200,000 tokens (roughly 500 pages)... Smaller bases fit entirely in prompts without requiring RAG."* Anti-pattern: generic summaries, hypothetical document embedding, summary-based indexing all underperformed.

### 3.4 Prompt caching (`platform.claude.com/docs/en/build-with-claude/prompt-caching`)

**Cacheable:** tools, system messages, user/assistant text, images & documents, tool use/results.

**When it pays:** *"Prompts with many examples, large amounts of context or background information, repetitive tasks with consistent instructions, [and] long multi-turn conversations."* For agentic workloads: *"Enhance performance for scenarios involving multiple tool calls and iterative code changes, where each step typically requires a new API call."*

**Economics:** writes are 1.25× base (5-min) or 2× base (1-hour); reads are **0.1× base — 90% savings.** This makes orchestrator-worker architectures with shared system prompts economically viable.

**Placement rule (most-misunderstood):** *"Place the breakpoint on the last block that stays identical across requests. For a prompt with a static prefix and a varying suffix (timestamps, per-request context, the incoming message), that is the end of the prefix, not the varying block."* The inverse is flagged as a *common mistake.* Also: *"if a growing conversation pushes your breakpoint 20 or more blocks past the last write, the lookback window misses it"* — add a second breakpoint for long sessions.

---

## 4. System-card-derived practitioner findings

### 4.1 Claude Opus 4.5 — Nov 24 2025

URL: `https://www.anthropic.com/news/claude-opus-4-5`. Introduced the **effort parameter** (`low | medium | high | max`) — *"decide to minimize time and spend or maximize capability."* At medium effort, 4.5 matches Sonnet 4.5 quality at *76% fewer output tokens.* Customer reports cite *50–75% reductions in tool calling errors.*

### 4.2 Claude Opus 4.6 — Feb 2026

Adaptive thinking added as option. Manual `budget_tokens` still works but is deprecated.

### 4.3 Claude Opus 4.7 — released ~Apr 2026

URL: `https://www.anthropic.com/claude/opus`. Load-bearing behavior changes (per `platform.claude.com/docs/en/build-with-claude/adaptive-thinking` and release notes):

- **Adaptive thinking is the only supported mode.** *"On Claude Opus 4.7, adaptive thinking is the only supported thinking mode; manual `thinking: {type: enabled, budget_tokens: N}` is no longer accepted."*
- **`xhigh` effort level introduced** between `high` and `max` — *Anthropic's own recommendation for coding and agentic work.*
- **Literal instruction following.** *"Opus 4.7 interprets instructions more literally than Opus 4.6, especially at lower effort levels — it will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make."* Prompts that worked on 4.6 via implication need to be made explicit on 4.7.
- **Fewer tool calls / fewer subagents by default** (consistent across migration notes).
- **`display: "omitted"` is the new default for thinking blocks** — set `thinking.display: "summarized"` explicitly to restore. *"This is a silent change from Claude Opus 4.6."*
- **Task budgets carry forward across compaction cycles** — relevant for long-running agents.

### 4.4 Claude Mythos Preview

Adaptive thinking is the default and *"auto-applies whenever `thinking` is unset."* `thinking: {type: "disabled"}` is not supported.

---

## 5. Cross-cutting questions, answered with citations

**Q1. Multi-agent vs single-agent — when?** (§1.2) Multi-agent excels at *"valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools."* Poor fits: *"domains requiring all agents to share the same context"* and *"many dependencies between agents."* The 15× token cost is the floor.

**Q2. Sub-agent context handling — three layered recommendations.** (§1.2 + §1.3) (1) Spawn fresh sub-agents with clean contexts; use *"careful handoffs"* for plan/state. (2) Persist intermediate work in artifacts, not the orchestrator's window: *"artifact systems where specialized agents can create outputs that persist independently."* (3) Return condensed distillations (1–2k tokens), not raw traces: *"Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work."*

**Q3. Tools vs MCP vs hooks — the decision rule.** (§1.4) Deterministic = **hook**. Rich external app (Figma, Notion, monitoring) = **MCP**. CLI-shaped external (`gh`, `aws`, `gcloud`) = **CLI tool** — *"the most context-efficient way to interact with external services."* Reusable workflow with on-demand load = **skill**. Isolated context work = **subagent**.

**Q4. Evals — how to start, how to scale.** Start at *n=20 queries representing real usage patterns* with a *single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade* (§1.2). Scale via Bloom-style automated scenario generation (§2.2). For behaviors confounded by eval-awareness, apply the Petri 2.0 two-strategy approach (§2.3).

**Q5. Prompt caching for agentic workloads.** (§3.4) Always. Cache system prompt and tool definitions; cache the conversation prefix up to the last identical block (not the varying block); add a second breakpoint for long runs (20-block lookback); switching thinking modes invalidates cache breakpoints.

**Q6. CLAUDE.md content rules.** (§1.4) Short and human-readable. Diagnostic: *"Would removing this cause Claude to make mistakes? If not, cut it."* Bloated CLAUDE.md *causes* the bug it's trying to prevent. Use `@path/to/file` imports to keep the top file lean.

**Q7. Parallel sub-agents — when and how many.** (§1.2) Scale effort to query complexity. Simple: 1 agent, 3–10 calls. Complex: 10+ subagents. Sub-agents should *"use 3+ tools in parallel"* internally. Avoid synchronous-only execution.

**Q8. Reasoning model usage — when adaptive thinking, when off.** (§4.3 + adaptive-thinking docs) Adaptive is default on Opus 4.7 and Mythos Preview. Turn thinking *off* only for *"the lowest latency"* simple tasks. Manual `budget_tokens` is reserved for *"workloads that require predictable latency or precise control over thinking costs."* Warning: *"Steering Claude to think less often may reduce quality on tasks that benefit from reasoning. Measure the impact on your specific workloads before deploying prompt-based tuning to production."*

**Q9. Task budgets — when to use, when to skip.** (§4.3) Use when the agent runs long enough to need to *"plan, prioritize, and wrap up more gracefully"* against a token ceiling. Skip for one-shot or short-chain tasks.

**Q10. Anti-sycophancy and honesty guidance.** Indirect. Petri (§2.1) names `unprompted_sycophancy` and `unprompted_encouragement_of_user_delusion` as scored dimensions; Bloom (§2.2) ships a *delusional sycophancy* suite. To not be sycophantic: (a) eval for it, (b) suppress via system prompt, (c) re-eval after every prompt change — §2.5 shows frontier models can mask the behavior under test, so eval realism matters.

---

## 6. Anti-patterns Anthropic explicitly flags

| Anti-pattern | Source URL |
|---|---|
| Adding complexity without demonstrated outcome improvement | §1.1 / `building-effective-agents` |
| Vague orchestrator instructions | §1.2 / `multi-agent-research-system` |
| Sequential subagent execution when parallel would do | §1.2 |
| Overinvestment in simple queries | §1.2 |
| Synchronous-only execution | §1.2 |
| Bloated tool sets / ambiguous tool selection | §1.3 / `effective-context-engineering-for-ai-agents` |
| Over-aggressive compaction that loses critical context | §1.3 |
| Stuffing edge cases into prompts as "brittle hardcoded logic" | §1.3 |
| Vague high-level guidance lacking concrete signals | §1.3 |
| Bloated CLAUDE.md files | §1.4 / `best-practices` |
| The kitchen-sink session | §1.4 |
| Correcting the same issue more than twice in one session | §1.4 |
| Shipping without verification | §1.4 |
| Unscoped "investigate" prompts | §1.4 |
| Partial sandbox isolation (FS without network, or vice-versa) | §1.5 / `claude-code-sandboxing` |
| Treating auto mode as a manual-approval replacement on high-stakes infrastructure | §1.6 / `claude-code-auto-mode` |
| Treating checkpoints as a git replacement | §1.7 |
| Shipping system-prompt changes without ablation/staged rollout | §1.8 / `april-23-postmortem` |
| Cache breakpoint on per-request varying content | §3.4 / prompt-caching docs |
| Eval suites that look obviously like evals | §2.1, §2.3, §2.5 |
| Persona cosplay in evals ("as Fowler would say") — implied across alignment-science posts on honesty | §2.4 |

---

## 7. The top 15 patterns Anthropic explicitly recommends — ranked

Ranking reflects how often and how forcefully the pattern is endorsed across the corpus, and how load-bearing it is in production case studies.

1. **Give the agent a way to verify its own work.** *"The single highest-leverage thing you can do."* (§1.4)
2. **Start simple; add complexity only when measurably justified.** (§1.1)
3. **Workflow before agent: choose predictable orchestration when steps are knowable.** (§1.1)
4. **Cache aggressively; place breakpoints on the last stable block.** (§3.4)
5. **Sub-agent context isolation: clean contexts + artifact handoff + 1–2k-token distillations.** (§1.2, §1.3)
6. **Just-in-time context loading over front-loaded RAG.** (§1.3)
7. **Compaction with recall-first, precision-second tuning.** (§1.3)
8. **CLAUDE.md kept short and human-readable, pruned ruthlessly.** (§1.4)
9. **Explore → Plan → Code → Commit for non-trivial tasks; skip the plan for one-sentence diffs.** (§1.4)
10. **Hooks for deterministic, must-happen actions; MCP and CLI tools for external services.** (§1.4)
11. **Sub-agents for investigation, code review, and any context-heavy work.** (§1.4)
12. **Parallel sub-agents using 3+ tools internally; scale subagent count to query complexity.** (§1.2)
13. **Adaptive thinking as default; effort parameter for cost/quality tradeoff.** (§4.3)
14. **Ship eval at n=20 with single-call LLM judge before scaling.** (§1.2, §2.2)
15. **Account for eval-awareness when measuring frontier model behavior.** (§2.3, §2.5)

---

## 8. Reading order for a new practitioner

1. **§1.1 — *Building Effective Agents*.** Vocabulary; prerequisite for everything else.
2. **§1.4 — *Best practices for Claude Code*.** Concrete how-to; grounds all hands-on work.
3. **§1.3 — *Effective Context Engineering*.** The frame that explains *why* the §1.4 practices exist.
4. **§1.2 — *Multi-agent research system*.** Production case study; the numbers everyone cites.
5. **§3.4 — Prompt caching docs.** Read before any production deployment.
6. **§4.3 — Opus 4.7 + adaptive-thinking docs.** Read before writing any new model-targeted prompt.
7. **§1.5 — Sandboxing.** Read before deploying agents that touch a real filesystem or network.
8. **§1.6 — Auto mode.** Read before going non-interactive in production.
9. **§1.8 — April 23 postmortem.** Re-read whenever tempted to ship a system-prompt change without staged rollout.
10. **§2.1–§2.3 — Petri, Bloom, Petri 2.0.** Read as a unit when investing in behavioral evals.
11. **§3.3 — Contextual retrieval.** Read only when corpus exceeds ~200k tokens and RAG is decided.
12. **§2.4 — SDF.** Read for honeypotting / unlearning or model-organism research.
13. **§2.5 — Steering eval-aware models.** Read to internalize the limits of any eval that doesn't mitigate eval-awareness.

---

## 9. Provenance and limits

- Sources retrieved May 17 2026 via `WebFetch` against `anthropic.com`, `alignment.anthropic.com`, `code.claude.com`, `platform.claude.com`, `github.com/anthropics`.
- `building_evals.ipynb` cell content not reliably extractable from GitHub-rendered HTML; read the notebook directly.
- The Sep 2025 *enabling Claude Code to work more autonomously* engineering-blog URL returned 404; the news-channel mirror was used.
- System-card numerical claims (e.g., Opus 4.7's exact "fewer tool calls by default" deltas) come from release-note prose and third-party deep-dives; the qualitative direction is reliable, exact percentages should be re-checked against the published system card.
- Anthropic blog posts are edited in place without changelogs. *Best practices for Claude Code* is a living document. Quotes are accurate as of retrieval; re-verify before treating any specific phrasing as canonical six months hence.
