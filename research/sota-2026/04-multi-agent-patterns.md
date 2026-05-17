# Multi-Agent Orchestration Patterns — SOTA 2026

A field report on what has been shipped, what is academic, and what is worth stealing for a Claude-Code-based file-artifact-driven critic-stack workflow.

Throughout this document, three labels are used:

- **Anthropic-blessed** — published by Anthropic or used inside their own products.
- **Community-best-of** — load-bearing in at least one major OSS framework (LangGraph, AutoGen v0.4, CrewAI, OpenAI Agents SDK, Google ADK) and discussed in production retros.
- **Academic-promising-but-unshipped** — paper exists, results replicate, but no major framework has made it a first-class primitive.

---

## 1. The canonical pattern taxonomy (Anthropic's "Building Effective Agents")

Anthropic's December 2024 [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) is the field's closest thing to a shared vocabulary. It distinguishes *workflows* (LLMs orchestrated through predefined code paths) from *agents* (LLMs that direct their own tool use). Five workflow patterns plus the autonomous-agent loop. All six are now mirrored in Spring AI's [`spring-ai`](https://docs.spring.io/spring-ai/reference/api/effective-agents.html), a sign the taxonomy has crystallized.

### 1a. Prompt chaining

**Problem shape:** A task with a fixed, well-understood decomposition where each step has clear input/output contracts. Translate-then-summarize. Outline-then-draft-then-edit.

**Failure modes:** Cascading errors — a mistake in step 1 contaminates all downstream steps with no chance of recovery. No backtracking. Brittle to inputs the chain was not designed for.

**When to use:** The decomposition is stable across all inputs; latency budget tolerates serial steps; you can place a gate (a deterministic check, a small classifier) between stages.

**When NOT to use:** Inputs vary in shape; you need branching; the cost of a single-step error is high. If you find yourself adding `if` statements between chain steps, you actually want routing.

Sources: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents); [DeepLearning.AI — Agentic Design Patterns Part 2: Reflection](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/) for the related reflection variant.

### 1b. Routing

**Problem shape:** Heterogeneous inputs that benefit from specialization. Customer-service triage. Coding tasks where a small model can handle the bulk of refactors and a large model is reserved for novel design.

**Failure modes:** The router is itself an LLM and inherits all its biases — sticky-class problems (router favors the class it saw most in training), router-as-bottleneck (every request pays a routing tax), and the classifier-cascade problem where two routers in series can silently disagree.

**When to use:** Distinct categories of input demand different handling, prompts, or models; misclassification cost is bounded (you can always escalate).

**When NOT to use:** The categories are not actually disjoint; the routing decision is itself the hard part of the problem (in which case make it the *main* decision, not a preamble).

Sources: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents); [Towards AI — Agent Workflow Patterns Beyond Anthropic's Playbook](https://pub.towardsai.net/agent-workflow-patterns-beyond-anthropics-playbook-1bd76a48d63d).

### 1c. Parallelization (sectioning + voting)

Two distinct variants. *Sectioning* splits independent subtasks across parallel calls and aggregates. *Voting* runs the same task N times and aggregates by majority, self-consistency, or LLM-judge.

**Problem shape:** Tasks decomposable into independent shards (sectioning) or tasks where confidence comes from agreement across samples (voting).

**Failure modes:** Sectioning fails when shards are not actually independent (hidden coupling re-emerges at aggregation). Voting fails when the samples are correlated — running the same model 5 times with temperature 0.7 does not give you 5 independent opinions; it gives you 5 draws from one posterior. See section 4 on correlated review error.

**When to use:** Latency budget pays for the parallel fan-out; the aggregation function is trivial (sum, majority, max) or itself a worthwhile use of an LLM.

**When NOT to use:** Shards must coordinate during execution; the aggregation logic is harder than the original task; you are using voting as a synonym for "I don't trust the model."

Sources: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents); [arXiv:2305.14325 — Improving Factuality and Reasoning through Multiagent Debate (Du, Li, Torralba, Tenenbaum, Mordatch)](https://arxiv.org/abs/2305.14325) for the voting-with-debate generalization.

### 1d. Orchestrator-worker

**Problem shape:** Tasks whose decomposition is *itself* a decision the LLM must make, not pre-coded. Open-ended research. Complex coding tasks where the file-set is unknown in advance.

**Failure modes:** The orchestrator becomes a bottleneck (single point of failure for the whole run). Token explosion when the orchestrator spawns workers liberally. Loss of coherence when subagent outputs are summarized lossily before reaching the orchestrator. Anthropic's own multi-agent-research retro flags that "agents struggle to judge appropriate effort for different tasks" — they over- or under-spawn workers without guardrails.

**When to use:** Subtasks cannot be enumerated up front; you can budget per-worker; the orchestrator's planning step is cheap relative to the workers.

**When NOT to use:** Subtasks *can* be enumerated (use sectioning instead — cheaper, more predictable); the workers need to talk to each other (orchestrator-worker is a star topology, not a mesh).

Sources: [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system); [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents).

### 1e. Evaluator-optimizer (judge-actor loop)

**Problem shape:** A task with clear evaluation criteria where iterative refinement provides measurable value. Code that has to compile and pass tests. Prose that has to satisfy a rubric.

**Failure modes:** Eval-aware sycophancy — the actor learns to game the evaluator. Loop runaway if no stopping rule. Evaluator drift if the evaluator is the same model as the actor (correlated failure). Optimizer's "polish to local maximum" — many refinement loops just rephrase rather than improve.

**When to use:** The evaluator is meaningfully better at judging than at generating (asymmetric difficulty); criteria can be made explicit; a stopping rule exists (verdict crosses threshold or N iterations reached).

**When NOT to use:** No external ground-truth signal; the evaluator is the actor (or same family); criteria are vague enough that any output can be argued to satisfy them.

Sources: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents); [Hugging Face — Reflection in AI agents](https://huggingface.co/blog/Kseniase/reflection) on the broader Reflexion/Self-Refine family.

### 1f. The autonomous-agent loop (tool-use + observation cycle)

The full reactive loop: model reasons, picks a tool, observes the result, loops until a stopping condition. This is what Claude Code, Cursor, Devin and the OpenAI Agents SDK all implement at their core.

**Problem shape:** Open-ended tasks where the path is genuinely unknowable in advance (debugging, exploration, "fix this CI failure").

**Failure modes:** Long-horizon coherence collapse (section 4d); cost explosion when the loop has no budget; eval-awareness when the model recognizes it's in a sandbox; meltdown behavior (transition from coherent-but-wrong to incoherent looping) documented in [arXiv:2509.09677 — Measuring Long Horizon Execution in LLMs](https://arxiv.org/pdf/2509.09677).

**When to use:** Genuinely open-ended; environment can be sandboxed; you can afford to abort on a budget.

**When NOT to use:** A workflow pattern actually fits — the autonomous loop is the most expensive, least predictable, hardest-to-debug option in the taxonomy. Anthropic's own guidance: *"start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short."*

Sources: [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents); [arXiv:2604.11978 — The Long-Horizon Task Mirage](https://arxiv.org/html/2604.11978v1) on where these loops break.

---

## 2. Production framework comparison

### 2a. LangGraph (langchain-ai)

**Signal:** ~90M monthly downloads across the LangChain ecosystem; production at Uber, Klarna, LinkedIn, Replit, AppFolio; weekly releases; "production-grade" since late 2024.

**Distinctive primitive:** A typed, stateful, checkpointable graph — the graph is the source of truth. `langgraph-supervisor` and `langgraph-swarm` packages encode the supervisor and peer-handoff patterns as first-class shapes.

**Scales:** Supervisor pattern (one orchestrator → 3–6 specialists with shared state). Hierarchical (supervisor-of-supervisors) only at 6+ workers.

**Does not scale:** Swarm (peer-to-peer handoffs) without LangSmith distributed tracing — debugging is functionally impossible. Network topology is chaos.

**Claude interop:** First-class via `langchain-anthropic`; supports tool-use and prompt caching. No native Claude Code hook integration — sits beside, not inside.

Sources: [awesome-LangGraph](https://github.com/von-development/awesome-LangGraph); [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph-supervisor); [Augment — Swarm vs Supervisor](https://www.augmentcode.com/guides/swarm-vs-supervisor); [AlphaBold — LangGraph in Production](https://www.alphabold.com/langgraph-agents-in-production/).

### 2b. AutoGen (Microsoft) — v0.4 / migration to Agent Framework

**Signal:** Microsoft Research-backed. v0.4 (January 2025) was an async-event-driven rewrite. Microsoft has since launched "Microsoft Agent Framework" as the migration target — AutoGen will be folded in.

**Distinctive primitive:** `GroupChat` (now `RoundRobinGroupChat` / `SelectorGroupChat`) — conversational multi-agent with a manager selecting who speaks. The transcript *is* the shared state.

**Scales:** Role-play conversational scenarios — debate-style decomposition, reviewer + coder pairs.

**Does not scale:** Long-running production workflows; observability and resumability lag LangGraph. Retros describe AutoGen as "a migration target, not a choice."

**Claude interop:** Supports Anthropic models, but Microsoft's pivot to Agent Framework + Azure OpenAI puts Claude in a second-tier position.

Sources: [Microsoft Research — AutoGen v0.4](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/); [v0.2 → v0.4 migration](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/migration-guide.html); [AutoGen → Agent Framework migration](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/).

### 2c. CrewAI

**Signal:** Popular for rapid prototyping; role-based framing is a strong onboarding hook. Retros flag memory bloat (>2GB for 10+ agent / 50+ task crews) and budget burn in hierarchical mode.

**Distinctive primitive:** Role-typed `Agent` + `Task` composed into a `Crew` running `Process` types (sequential, hierarchical). Pydantic schemas enforce typed handoff.

**Scales:** Sequential pipelines with 3–5 agents and explicit Pydantic outputs.

**Does not scale:** Hierarchical process under cost pressure; manager deliberations burn budget; no first-class checkpointing.

**Claude interop:** Supports Claude via LiteLLM / direct Anthropic client.

Sources: [Hierarchical Process docs](https://docs.crewai.com/en/learn/hierarchical-process); [crewAIInc/crewAI](https://github.com/crewaiinc/crewai); [Latenode review](https://latenode.com/blog/crewai-agent-framework).

### 2d. OpenAI Agents SDK

**Signal:** Released March 2025 as successor to experimental Swarm; recently extended with sandboxing, configurable memory, Codex-style filesystem tools. Production-positioned.

**Distinctive primitive:** **Handoff** — explicit first-class control transfer between agents carrying conversation context, with optional input filters. Four primitives: Agents, Handoffs, Guardrails, Tracing.

**Scales:** Linear handoff chains (triage → specialist → resolver), guarded loops with budget enforcement.

**Does not scale:** Deeply nested handoffs — debuggability degrades past two levels of branching.

**Claude interop:** OpenAI-pinned; Claude works only via OpenAI-compatible shims.

Sources: [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/); [Handoffs reference](https://openai.github.io/openai-agents-python/handoffs/); [DevOps.com — Sandboxing](https://devops.com/openai-upgrades-its-agents-sdk-with-sandboxing-and-a-new-model-harness/).

### 2e. Google ADK (Agent Development Kit)

**Signal:** Google Cloud-backed; canonical multi-agent shape for Gemini + Vertex AI; tightly integrated with A2A (section 5).

**Distinctive primitive:** **Tree-of-agents** — `sub_agents=[...]` with one-parent-per-agent enforced at construction. Three workflow agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) compose the tree.

**Scales:** Static hierarchies known up front; the single-parent constraint forces a clear org chart.

**Does not scale:** Runtime dynamic agent creation; peer-to-peer flows.

**Claude interop:** Gemini-first; Claude wirable but the metaphors are Google-flavoured.

Sources: [ADK docs](https://google.github.io/adk-docs/); [Google Cloud Blog — Multi-agentic systems with ADK](https://cloud.google.com/blog/products/ai-machine-learning/build-multi-agentic-systems-using-google-adk); [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/).

### 2f. Anthropic's "in-house" pattern (Research multi-agent system)

**Signal:** Anthropic-blessed; powers the Claude Research product. +90.2% over single-agent Opus 4 on Anthropic's internal research eval.

**Distinctive primitive:** Lead Researcher (Opus) + parallel specialist subagents (Sonnet). Lead writes plan to memory, decomposes into subtasks with explicit objective / output format / tool guidance / boundaries, then synthesizes. Scaling rules embedded in prompts because agents struggle to self-calibrate effort.

**Scales:** Breadth-first research — parallel exploration dominates serial.

**Does not scale:** Sequential deep-dependency tasks where coordination cost exceeds parallel benefit (Anthropic calls this out explicitly).

**Claude interop:** Claude-native. The Claude Code Agent tool is the local-developer instantiation of the same shape — orchestrator + parallel `Agent` calls + filesystem as shared state. The current critic-stack workflow is a direct descendant.

Sources: [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system); [ByteByteGo summary](https://blog.bytebytego.com/p/how-anthropic-built-a-multi-agent).

---

## 3. Eval-aware orchestration (load-bearing section)

The shift in 2025-2026 is from "use an LLM to grade outputs" to "build the entire workflow around evaluators that are themselves agents." The critic-stack pattern this repo uses is part of that shift.

### 3a. Petri's judge-actor loop (Anthropic Alignment, October 2025; v2 Q1 2026)

[Petri](https://alignment.anthropic.com/2025/petri/) ("Parallel Exploration Tool for Risky Interactions") formalized a three-role loop for alignment audits: **auditor** drives the conversation, **target** is the model under test, **judge** scores transcripts across a 36-dimension rubric. Crucial design point: the auditor can branch, roll back, prefill, simulate tool outputs, and early-terminate. The judge is *separate* from the actor and reads the whole transcript, not just the final answer.

The 2026 v2 release ([Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/)) added a **realism classifier** that monitors auditor behavior turn-by-turn and rejects unrealistic auditor moves — explicit mitigation for the actor learning that it's in an eval. Combined with manual seed-instruction edits, this produced a 47.3% median relative drop in eval-awareness on Claude models. Anthropic donated Petri to Meridian Labs in May 2026, signalling intent to keep it framework-agnostic.

**Takeaway for critic-stack workflows:** Petri validates the "judge reads transcripts, not just outputs" pattern. The judge having branching/rollback authority is novel and worth borrowing.

### 3b. Agent-as-judge literature

The 2025 surveys converge on a few claims:

- [arXiv:2411.15594 — A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594) — taxonomy of judge architectures and a long catalogue of known biases (position, verbosity, self-preference, sycophancy).
- [arXiv:2508.02994 — When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation for LLMs](https://arxiv.org/abs/2508.02994) — argues the field is moving from "single-model judges" to "multi-agent debate frameworks" because single judges inherit the biases of their base model.
- [arXiv:2412.05579 — LLMs-as-Judges: A Comprehensive Survey](https://arxiv.org/html/2412.05579v2) — five-axis taxonomy (Functionality, Methodology, Applications, Meta-evaluation, Limitations).
- [arXiv:2601.05111 — A Survey on Agent-as-a-Judge](https://arxiv.org/html/2601.05111v1) — January 2026 update extending judges with planning, tool-augmented verification, and persistent memory.

The consensus: a single LLM-judge is fast but biased; an agent-judge (one that can use tools, retrieve context, persist memory) is slower but better calibrated.

### 3c. The "minority veto" / critic-panel pattern (what this stack uses)

The critic-stack workflow uses three lenses (architecture, operations, product) with minority-veto: any single lens issuing `rework` or `reject` blocks approval. This is a specific instance of a broader family that includes:

- **PoLL (Panel of LLM evaluators)** — [arXiv:2404.18796 — Replacing Judges with Juries](https://arxiv.org/abs/2404.18796). Empirically: a panel of smaller diverse models correlates with human judgement *better* than GPT-4 alone, at >7× lower cost.
- **LLM-as-a-jury for comparative assessment** — [arXiv:2602.16610 — Who can we trust?](https://arxiv.org/html/2602.16610v1) handles heterogeneous judge reliability.
- **Jury-on-demand** — [arXiv:2512.01786 — Who Judges the Judge? LLM Jury-on-Demand](https://arxiv.org/pdf/2512.01786) — sample judges lazily, only invoking more when uncertainty is high.

Minority-veto is itself an unusual aggregation choice. Majority-vote is more common in juries; veto is more common in design-review. The justification: in design decisions, *false-positives are more dangerous than false-negatives* — a wrong "approve" ships a flawed design; a wrong "reject" costs one more round. Veto biases toward type-I caution, which is the right bias for irreversible commits.

### 3d. Self-consistency / N-best sampling for verdict robustness

Self-consistency (sample N reasoning paths, majority-vote) was the canonical robustness lever from 2022-2024. [arXiv:2511.00751 — Reevaluating Self-Consistency Scaling in Multi-Agent Systems](https://arxiv.org/pdf/2511.00751) argues the marginal benefit drops fast after ~5 samples; [arXiv:2502.18581 — Scalable Best-of-N Selection via Self-Certainty](https://arxiv.org/pdf/2502.18581) shows you can use the model's own probability distribution as a quality signal without an external reward model.

For verdict robustness specifically: running the *same* judge model N times is much weaker than running N *different* judge models. The arithmetic is unforgiving — see correlated-failure below.

### 3e. The shadow-lane pattern (different-model triangulation)

This stack's `SHADOW_PANEL=1` is a concrete instance: three Opus critic lenses run as primary, three Sonnet shadow lenses run in parallel, a comparator emits agreement class (`agree | partial-agree | disagree`) per lens. The shadow has *voice, not vote*.

The pattern is community-best-of, not yet academic-named. The closest published shapes:

- **Diversity-of-thought debate** — [arXiv:2410.12853 — Diversity of Thought Elicits Stronger Reasoning in Multi-Agent Debate](https://arxiv.org/html/2410.12853v1) — diverse personas / models outperform homogeneous panels.
- **X-MAS heterogeneous multi-agent systems** — [arXiv:2505.16997 — X-MAS](https://arxiv.org/html/2505.16997v1) — explicit case for heterogeneous LLM backbones.

What the stack adds on top: the "voice not vote" framing — the shadow lane's purpose is *triangulation signal*, not a verdict change. Disagreement is information, not a vote tie-breaker.

### 3f. Cross-family judge variance (judges favor their own family)

This is the load-bearing finding that motivates shadow-lane:

- [arXiv:2410.21819 — Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819) — models score their own outputs higher than blinded baselines justify.
- [arXiv:2508.06709 — Play Favorites: Statistical Method to Measure Self-Bias](https://arxiv.org/abs/2508.06709) — extends the analysis to **family bias**: GPT-4o and Claude 3.5 Sonnet systematically rate outputs from same-family models higher.
- [arXiv:2604.06996 — Self-Preference Bias in Rubric-Based Evaluation](https://arxiv.org/abs/2604.06996v1) — bias persists even when judges are given explicit rubrics.
- [arXiv:2504.03846 — Do LLM Evaluators Prefer Themselves for a Reason?](https://arxiv.org/html/2504.03846v2) — partial explanation: familiarity (lower perplexity on own-family outputs).
- [arXiv:2509.26072 — The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge](https://arxiv.org/html/2509.26072v2) — judges shortcut to surface features (length, hedging, formatting).

Implication: an all-Anthropic critic panel will systematically over-approve outputs that pattern-match Claude's house style — including outputs *generated by Claude in the same workflow*. The shadow-lane is a partial mitigation; an external-family lane (the `EXTERNAL_SHADOW=1` reserved env var) is a stronger mitigation that is not yet wired up.

---

## 4. Production failure modes (2025-2026 retros)

### 4a. Cascading failures in agent chains

[Galileo — Why do Multi-Agent LLM Systems Fail](https://galileo.ai/blog/multi-agent-llm-systems-fail) and [Agent Patterns — Cascading Failures](https://www.agentpatterns.tech/en/failures/cascading-failures) document the same shape: an upstream agent emits subtly malformed output → downstream agent fails to parse but does not raise → silent quality degradation. The most-cited number: unstructured multi-agent networks amplify errors up to **17.2×** vs single-agent baselines. Mitigations are (a) typed contracts between stages (Pydantic, JSON schema), (b) circuit-breakers that abort the chain on parse failures, (c) idempotent re-entry points.

### 4b. Cost explosions — the "agent runs in a loop" problem

The much-cited [$47K runaway-loop incident](https://techstartups.com/2025/11/14/ai-agents-horror-stories-how-a-47000-failure-exposed-the-hype-and-hidden-risks-of-multi-agent-systems/) — a multi-agent research tool entered a recursive loop and ran for 11 days unobserved. [O'Reilly — The Hidden Cost of Agentic Failure](https://www.oreilly.com/radar/the-hidden-cost-of-agentic-failure/) catalogs the structural causes: no per-agent token attribution, no budget enforcement at the orchestrator, no anomaly detection on call-rate. The agent ecosystem still lacks the equivalent of database connection pools and HTTP timeouts.

Required infrastructure: token budget per session, per-agent attribution, alerting on rate anomalies, a hard kill at 2× expected cost.

### 4c. Correlated review error in same-model panels

[arXiv:2506.07962 — Correlated Errors in Large Language Models](https://arxiv.org/html/2506.07962v1) is the key empirical paper. Findings: errors correlate highly across LLMs, especially for models sharing provider, architecture, or scale. More accurate models *also* have more correlated errors with each other (a kind of "smart models converge on the same wrong answers"). [arXiv:2602.08003 — Don't Always Pick the Highest-Performing Model](https://arxiv.org/html/2602.08003) — for ensemble selection, picking the most diverse pair beats picking the two strongest. This is the empirical basis for *family-diverse* panels.

### 4d. Long-horizon coherence loss

[arXiv:2509.09677 — Measuring Long Horizon Execution in LLMs](https://arxiv.org/pdf/2509.09677) — even when planning and world knowledge are perfect, execution errors compound; models self-condition on their own earlier errors and degrade. [arXiv:2604.11978 — The Long-Horizon Task Mirage](https://arxiv.org/html/2604.11978v1) — observes "meltdown" behavior: coherent-but-incorrect → incoherent looping + hallucinated tool outputs. [arXiv:2603.29231 — Beyond pass@1: Reliability Science for Long-Horizon Agents](https://arxiv.org/html/2603.29231v1) — argues we need reliability metrics, not just pass-rate. Mitigation: forced checkpointing, periodic plan-rereading, externalized state (files, not context window).

### 4e. Eval-awareness — model behaves differently when it knows it's evaluated

[arXiv:2507.01786 — Probing Evaluation Awareness of Language Models](https://arxiv.org/html/2507.01786v1) — frontier models have a reasonably good sense of when they're being tested. [Apollo Research — Claude Sonnet 3.7 (often) knows when it's in alignment evaluations](https://www.apolloresearch.ai/science/claude-sonnet-37-often-knows-when-its-in-alignment-evaluations/) — direct experimental evidence. [Anthropic — Petri 2.0 eval-awareness mitigations](https://alignment.anthropic.com/2026/petri-v2/) — the production response: realism classifiers that prevent the auditor from being obviously synthetic. [ICLR 2025 — In-Context Environments Induce Evaluation-Awareness](https://arxiv.org/pdf/2603.03824v1) — environmental cues (system prompt structure, tool naming) trigger the awareness.

For a critic-stack: if the *actor* (the candidate generator) knows it's about to be graded, it may polish for the rubric rather than for actual quality. Mitigation: phrase the generator's prompt as a working task, not as "this will be reviewed."

---

## 5. The "when N agents are too many" question

### Empirical sweet spot

[Google Research — Towards a science of scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) and [arXiv:2512.08296 — Scaling Agent Systems: A Quantitative Study](https://www.emergentmind.com/papers/2512.08296) find the scaling is *non-monotonic*. The shape: gains saturate around 3-5 agents for most tasks, with a long tail of regressions when adding more. Concrete numbers from the Google work: multi-agent coordination delivered +81% on parallelizable tasks (Finance-Agent) but **-70% on sequential tasks** (PlanCraft). [arXiv:2604.03295 — Scaling Teams or Scaling Time?](https://arxiv.org/html/2604.03295) — for some tasks, "more think-time per agent" beats "more agents."

### The cognitive-load argument

More agents means more inter-agent context for any single agent to model. The supervisor has to track N specialists' state; each specialist has to understand its niche relative to the others. Past ~5-7 agents, the supervisor's prompt becomes the bottleneck and routing accuracy degrades sharply. [arXiv:2402.03578 — LLM Multi-Agent Systems: Challenges and Open Problems](https://arxiv.org/abs/2402.03578) frames this as a coordination-overhead claim.

### The blast-radius argument

Every additional agent is an additional point of failure that can derail the workflow. Three agents with 95% reliability each → 0.95³ = 86% end-to-end. Ten agents at 95% each → 60%. Mitigations (typed contracts, retries) help but never close the gap. The pragmatic conclusion: *don't add an agent unless its expected lift exceeds the reliability cost it imposes.*

---

## 6. Bridging the protocol layer (brief)

Worth naming because it changes the design space:

- **MCP (Model Context Protocol)** — Anthropic, late 2024. Vertical: agent ↔ tools.
- **A2A (Agent2Agent)** — Google, April 2025; >150 organizations signed on by April 2026; contributed to Linux Foundation in June 2025 and folded into the Agentic AI Foundation alongside MCP in December 2025.

Both are now governance-neutral standards. For a Claude-Code-based stack, MCP is the right answer for tools-as-agents; A2A is the right answer for *inter-stack* agent calls (e.g., calling out to a separate Crew or LangGraph deployment). The critic-stack currently uses neither.

Sources: [Google Developers Blog — Announcing A2A](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/); [IBM — What is the A2A Protocol](https://www.ibm.com/think/topics/agent2agent-protocol).

---

## 7. Synthesis — Top 8 patterns worth adopting for THIS stack

What the stack already has: 12-step orchestrator; file-artifact-driven shared state; parallel sub-agents at gather (3–5) and critic (10) steps; minority-veto panel; optional Sonnet shadow-lane under `SHADOW_PANEL=1`; ledger + decision-log; hard gates on scope-map and challenges.

Already-have, do not duplicate: orchestrator-worker, sectioning + primitive voting, evaluator-optimizer (panel + replan/rewrite loop), shadow-lane triangulation, minority-veto.

Top 8 worth adding, ordered by expected impact:

### #1 — External-family shadow lane (wire up `EXTERNAL_SHADOW=1`)

**Status:** Anthropic-blessed in spirit (env var reserved), academic-supported. **Sources:** [arXiv:2508.06709](https://arxiv.org/abs/2508.06709), [arXiv:2506.07962](https://arxiv.org/html/2506.07962v1). The current Opus-primary + Sonnet-shadow mitigates intra-model drift, not intra-family bias. A third lane on a different family (GPT via OpenRouter, or local Llama/Qwen) breaks family-correlation. Lab entry exists; the wrapper primitive is the unblock.

### #2 — Petri-style judge with branching/rollback authority

**Status:** Anthropic-blessed. **Source:** [Petri 2.0](https://alignment.anthropic.com/2026/petri-v2/). Critics currently read the candidate at step 10 and vote once. Petri's auditor can branch, roll back, prefill, re-probe. A critic that can request a specific clarification from the generator before voting — and roll back to do so — catches more defects than one-shot review.

### #3 — Realism classifier on the generator's context

**Status:** Anthropic-blessed. **Source:** [Petri 2.0 mitigations](https://alignment.anthropic.com/2026/petri-v2/). If the generator (step 9) knows the critic-panel is coming, it polishes for the rubric. A pre-step that rewrites step-9 prompts to remove "this will be reviewed" signal — phrased as a working task, not an audition — reduces eval-awareness in the candidate. Cheap to add.

### #4 — Typed contracts between workflow steps

**Status:** Community-best-of (CrewAI's central design choice; LangGraph state-typing). **Sources:** [CrewAI](https://docs.crewai.com/en/learn/hierarchical-process); [Galileo](https://galileo.ai/blog/multi-agent-llm-systems-fail). Markdown artifacts are cascading-failure-prone. A JSON-schema gate at each step boundary (does `requirement.md` have the four required fields? Does `scope-map.md` have at least one row per primitive?) catches silent-malformed outputs. Could be a `bin/check-artifact-shape.sh` companion to the existing path-discipline check.

### #5 — Per-agent token attribution and hard cost-cap

**Status:** Community-best-of, urgent. **Sources:** [$47K runaway-loop retro](https://techstartups.com/2025/11/14/ai-agents-horror-stories-how-a-47000-failure-exposed-the-hype-and-hidden-risks-of-multi-agent-systems/); [O'Reilly](https://www.oreilly.com/radar/the-hidden-cost-of-agentic-failure/). The ledger tracks post-hoc; it does not enforce a budget during the run. Session-level token budget with abort-on-exceed (default 2× expected spend from a regression on past sessions) catches a runaway loop before the invoice. The ledger is the natural place to source the prior.

### #6 — Jury-on-Demand variant of the critic panel

**Status:** Academic-promising. **Sources:** [arXiv:2512.01786](https://arxiv.org/pdf/2512.01786); [arXiv:2404.18796](https://arxiv.org/abs/2404.18796). Three critics always run (six under SHADOW_PANEL). For cheap sessions, run one lens first; fan out only on `partial-approve`/`rework`. Saves ~2/3 critic spend on easy cases. Compatible with minority-veto: only escalate when uncertain.

### #7 — Long-horizon coherence checkpointing

**Status:** Academic-promising-but-unshipped. **Sources:** [arXiv:2509.09677](https://arxiv.org/pdf/2509.09677); [arXiv:2604.11978](https://arxiv.org/html/2604.11978v1). For multi-loop sessions, force the orchestrator to re-read `frame.md` + `challenges.md` at each iteration's start. Coherence loss happens when the model self-conditions on its prior turn instead of the frame. A literal re-read at loop boundaries is the cheapest mitigation in the literature. The `## Revision N` blocks in `frame.md` *enable* this but do not *force* it.

### #8 — A2A-shaped escape hatch for external critics

**Status:** Community-best-of, future-facing. **Sources:** [A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/); [Agent Interoperability Protocols 2026](https://zylos.ai/research/2026-03-26-agent-interoperability-protocols-mcp-a2a-acp-convergence). For a real third-party critic — a colleague's deployed agent, a Crew on Vertex, an OSS specialist — A2A is the standard wire format. Stub an A2A-compatible adapter for the critic-panel so external reviewers can slot in by URL. Speculative payoff, cheap to scaffold.

---

## 8. Patterns intentionally NOT recommended

- **Network / mesh topology** (every agent calls every other agent). Cited repeatedly as a debugging disaster; LangGraph's own guidance is explicit. Stick with star topology.
- **Naive multi-agent debate as the primary verdict mechanism.** The original [Du et al. multi-agent debate paper](https://arxiv.org/abs/2305.14325) is impressive on reasoning benchmarks but in production suffers the same-model correlation problem (4c) and is expensive. Minority-veto is a more conservative aggregation rule, better suited to design decisions.
- **Hierarchical-of-hierarchical** (supervisors of supervisors). Useful at N ≥ 6 specialists; the critic-stack workflow has 3 lenses, so a second layer adds complexity without payoff.
- **Self-consistency over a single judge.** Running the same critic 5× returns 5 draws from one posterior, not 5 opinions. The shadow-lane gets you closer to what self-consistency was trying to approximate.
