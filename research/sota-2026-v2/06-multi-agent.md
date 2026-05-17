# Multi-Agent Orchestration: The 2026 Canonical Reference

*A stack-neutral reference on what works in production multi-agent systems, what doesn't, what every practitioner should know. Cites the primary literature; flags Anthropic-blessed vs. community best-of vs. academic-promising-but-unshipped.*

---

## 0. Reader's contract

Three claims govern the rest of this document, and a reader who internalizes only these will already be ahead of the median 2026 practitioner:

1. **Most "multi-agent" systems should be workflows.** The Anthropic taxonomy (Schluntz & Zhang, December 19 2024) draws a sharp line between *workflows* — "systems where LLMs and tools are orchestrated through predefined code paths" — and *agents* — "systems where LLMs dynamically direct their own processes and tool usage." Production teams reach for the agent end of the spectrum too early. Composable patterns of prompt-chained and routed LLM calls win on cost, latency, observability, and reliability for the majority of business problems. ([Anthropic, *Building Effective Agents*](https://www.anthropic.com/engineering/building-effective-agents))

2. **The dominant cost driver is tokens, not API calls.** Anthropic's own multi-agent research system uses *~15× more tokens than chat interactions* — and token usage explains roughly *80% of the variance* in performance on browsing-style evaluations. ([Anthropic, *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system)) The cost model of a multi-agent system is not "N agents = N× cost"; it is closer to "N agents = N² conversation surface × per-turn context bloat × supervisor coordination overhead." Budget for that, or get a $47K invoice. ([Msatfi, "I Spent $0.20 Reproducing the Multi-Agent Loop That Cost Someone $47K," Medium, Nov 2025](https://medium.com/@mohamedmsatfi1/i-spent-0-20-reproducing-the-multi-agent-loop-that-cost-someone-47k-7f57c51f3c06))

3. **Adding agents is non-monotonic.** Google Research's December 2025 study on scaling agent systems shows coordination yields *diminishing or negative returns once single-agent baselines exceed roughly 45%* (β = −0.408, p < 0.001), and that independent agents amplify errors 17.2× versus 4.4× for centralized topologies. The right answer is frequently *one good agent with more think-time*, not five mediocre ones with a supervisor. ([Google Research, "Towards a science of scaling agent systems," 2026](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/); [arXiv:2512.08296](https://arxiv.org/html/2512.08296v1))

The rest of this document earns those three claims with patterns, data, and citations.

---

## 1. Foundations: the Anthropic taxonomy

The reference frame for this entire document is *Building Effective Agents* (Anthropic Engineering, December 19 2024). It introduces the canonical workflow-vs-agent split and enumerates five reusable workflow patterns plus one open-ended agent loop. Quote verbatim:

> *"Workflows are systems where LLMs and tools are orchestrated through predefined code paths."*
> *"Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."*

Anthropic's own guidance is repeatedly conservative: *"When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all."* The five workflow patterns below are designed to be reached for before the agent loop, not after.

### 1.1 Prompt chaining — fixed decomposition

**Problem shape:** A task that decomposes cleanly into a known sequence of subtasks. Translate, then summarize. Draft, then polish. Extract entities, then classify each.

Anthropic: *"This workflow is ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks. The main goal is to trade off latency for higher accuracy, by making each LLM call an easier task."*

**Failure modes:**
- **Cascading errors.** Step 3's input quality is bounded by step 2's output quality. Errors compound geometrically along the chain; a 95% per-step reliability over 6 steps is 73.5% end-to-end.
- **No backtracking.** A chain has no notion of "step 2 was wrong, retry from there." Either bolt on conditional gates between steps or accept silent drift.
- **Brittleness to input distribution shift.** The decomposition assumes a problem shape. Off-distribution inputs break the chain.

**When NOT to use:** Tasks where the right decomposition depends on the input (use *routing* or *orchestrator-worker*). Tasks with strong inter-step dependencies that benefit from a single LLM holding all the context.

### 1.2 Routing — input classification to specialists

**Problem shape:** Heterogeneous inputs that benefit from different downstream handling. Customer service triage (refund vs. technical vs. billing). Easy-vs-hard model routing (Haiku for cheap queries, Opus for hard ones).

Anthropic: *"Routing works well for complex tasks where there are distinct categories that are better handled separately, and where classification can be handled accurately, either by an LLM or a more traditional classification model/algorithm."*

**Failure modes:**
- **Router bias.** The router has a prior distribution over categories that may not match the input distribution. Re-evaluate the routing classifier periodically.
- **Classifier-cascade silent disagreement.** The router and downstream specialist disagree about category boundaries; the specialist receives an input it isn't optimized for and silently does its best. Mitigate with confidence thresholds and a fallback path.
- **The "default bucket" trap.** Inputs that don't match any category get dumped into a catch-all that becomes a hidden monolith.

**When NOT to use:** When categories are unstable (use a more adaptive orchestrator). When you can solve the problem cheaper with a single prompt and a richer system message.

### 1.3 Parallelization — sectioning and voting

Two distinct sub-patterns share infrastructure but solve different problems.

**Sectioning** — independent shards of the same task run concurrently. E.g., "evaluate each of these 10 documents against the same rubric in parallel."

**Voting** — N draws from the same query, aggregated by majority/consensus/threshold. E.g., "ask three times whether this code contains a vulnerability; reject if ≥2 say yes."

Anthropic: *"LLMs sometimes can work simultaneously on a task and have their outputs aggregated programmatically. This workflow, parallelization, manifests in two key variations: Sectioning ... Voting."*

**Failure modes:**
- **Correlated-sample fallacy (voting).** Five draws from one Sonnet posterior are *not* five opinions. They share the same prior, the same training corpus, the same calibration error. Voting only buys variance reduction; it does not buy diversity. ([arXiv:2506.07962, "Correlated Errors in Large Language Models"](https://arxiv.org/abs/2506.07962))
- **Aggregation bias (sectioning).** The combiner that merges shard outputs is itself an LLM call with its own context limits, its own preferences, its own failure modes.
- **Wasted spend on easy items.** Parallelization spends N× on every item, even items that one model would have solved correctly on the first try. Combine with a cheap pre-screen.

**When NOT to use:** Tasks with hard sequential dependencies. Tasks where the aggregator's context window cannot fit all shard outputs.

### 1.4 Orchestrator-worker — dynamic decomposition

**Problem shape:** Tasks where the subtask structure depends on the input. Anthropic's canonical example is coding changes that touch an unknown number of files. The research-system case is "decompose a research question into sub-queries."

Anthropic: *"The key difference from parallelization is its flexibility — subtasks aren't pre-defined, but determined by the orchestrator based on the specific input."*

**Failure modes:**
- **Bottleneck risk.** The orchestrator's context window holds the running plan, every worker's interim output, and the synthesis. It becomes the saturation point.
- **Token explosion.** Each worker run multiplies tokens; the orchestrator's summary of N worker outputs multiplies again. The 15× number from Anthropic's research system lives mostly here.
- **Coherence loss on summarization.** When the orchestrator summarizes worker outputs to fit them back into its window, signal is lost. Long-horizon work amplifies this loss.

**When NOT to use:** Tasks with tight inter-worker dependencies (workers need each other's outputs in real time, not just at synthesis). Tasks where the worker count is bounded and known — use parallelization sectioning instead.

### 1.5 Evaluator-optimizer — judge-actor loop

**Problem shape:** Generation tasks with a non-trivial evaluation function that beats the generation prior. Literary translation. Iterative search. Anything where "you know it when you see it" is easier than "produce it on the first try."

Anthropic: *"This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value. The two signs of good fit are, first, that LLM responses can be demonstrably improved when a human articulates their feedback; and second, that the LLM can provide such feedback."*

**Failure modes:**
- **Eval-aware sycophancy.** The actor learns within the loop to write outputs the judge will rate highly rather than outputs that are good. This is the same mechanism as RLHF sycophancy at a per-conversation timescale.
- **Loop runaway.** No termination criterion → loops forever. The $47K incident's "verifier asking analyzer to please clarify section 3.2 with effectively the same payload every cycle" is exactly this. ([dev.to postmortem, Nov 2025](https://dev.to/gabrielanhaia/the-agent-that-spent-47k-on-itself-an-autonomous-loop-postmortem-3313))
- **Optimizer's local maximum.** The judge has a single objective and the actor hill-climbs to it. The output is locally optimal and globally narrow.

**When NOT to use:** Tasks where the judge can't do better than the actor (you've just made the loop more expensive). Tasks with no natural stopping criterion. Tasks where eval-awareness destroys validity — see §4.

### 1.6 Autonomous agent loop — open-ended path

**Problem shape:** Long-horizon tasks where the path is not known ahead of time. Multi-day research. Open-ended coding work. Browser-using agents.

Anthropic: *"Agents can handle sophisticated tasks, but their implementation is often straightforward. They are typically just LLMs using tools based on environmental feedback in a loop ... Agents' autonomy makes them ideal for scaling tasks in trusted environments. The autonomous nature of agents means higher costs, and the potential for compounding errors."*

**Failure modes:**
- **Long-horizon coherence collapse.** Per-step accuracy degrades as the number of steps grows. ([arXiv:2509.09677, "The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs"](https://arxiv.org/abs/2509.09677)) "Long-horizon task mirage" findings show agents that look strong at short horizon break down on extended interdependent action sequences. ([arXiv:2604.11978](https://arxiv.org/abs/2604.11978))
- **Meltdown behavior.** A late-loop confusion contaminates the next several iterations. Recovery is rare without explicit reset checkpoints.
- **Cost explosion.** No natural budget, only natural endpoints — and the endpoint condition is itself an LLM judgment. Without a hard step/USD cap, you are one bad day from a postmortem.

**When NOT to use:** Anything where the cost of the worst-case run exceeds the expected value of the average run. Anything in an untrusted environment without sandboxing. Coding tasks that prompt chaining + routing would solve more cheaply.

---

## 2. Production framework comparison (2026 snapshot)

Each framework below earned its place by being a *primary primitive* in someone's production system in 2026. The order is not a ranking.

### 2.1 LangGraph (langchain-ai)

**Distinctive primitive:** Typed, stateful, checkpointable directed graph (`StateGraph`). Nodes are agents or tools; edges are conditional transitions; the entire run is persistable and resumable. As of late 2025, the project reports ~90M monthly SDK downloads and 1.0 GA in October 2025. ([LangGraph reference, 2026](https://reference.langchain.com/python/langgraph-supervisor); [Alphabold, "LangGraph Agents in Production"](https://www.alphabold.com/langgraph-agents-in-production/))

**Built-in multi-agent topologies:**
- *Supervisor* — central LLM node routes to specialist workers. The most widely deployed pattern.
- *Swarm* — peer agents hand off control dynamically based on specialization. ([langgraph-swarm reference](https://reference.langchain.com/python/langgraph-swarm))
- *Hierarchical* — supervisor-of-supervisors; recommended only at ≥6 workers per the community guidance, where the abstraction pays for its overhead.

**Production deployments:** Uber, Klarna, LinkedIn, Replit, AppFolio, JPMorgan, BlackRock, Cisco. ([CallSphere blog, 2026](https://callsphere.ai/blog/langgraph-supervisor-multi-agent-orchestration-2026))

**Scales well at:** Long-running stateful workflows; human-in-the-loop checkpoints; deterministic-when-it-matters orchestration with LLM nodes only where you want them.

**Scales poorly at:** Quick prototypes (the graph machinery has a learning cliff); use cases where the structure is genuinely emergent rather than designed.

**Claude interop:** First-class. LangGraph nodes wrap arbitrary providers; pinning specific nodes to Claude is the common production pattern.

### 2.2 AutoGen v0.4 → Microsoft Agent Framework

**History:** AutoGen v0.4 (January 2025) was a full async event-driven rewrite of the original AutoGen, replacing v0.2's `GroupChat` with `RoundRobinGroupChat` and `SelectorGroupChat`. ([Microsoft Research, "AutoGen v0.4"](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)) In February 2026 Microsoft published the migration path to **Microsoft Agent Framework 1.0**, which unifies Semantic Kernel and AutoGen orchestrations into one SDK. ([Microsoft Learn migration guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/); [DevBlogs MAF 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/))

**Distinctive primitive:** Event-driven agent communication on a message bus. The newer Agent Framework Workflow API replaces implicit group-chat selection with explicit graph workflows — closer to LangGraph's stance.

**Scales well at:** Microsoft-stack integrations (Azure AI Foundry, M365 Copilot extensions); enterprise compliance scenarios; teams already on Semantic Kernel.

**Scales poorly at:** Cross-cloud agnostic deployments; teams that need a small mental model.

**Claude interop:** Supported via provider abstraction, but the framework is Azure-first by inertia.

### 2.3 CrewAI

**Distinctive primitive:** *Roles* with goals, backstories, and tools, composed into a Crew that runs either *sequential* or *hierarchical* processes. Pydantic schemas on task outputs give typed handoffs. ([CrewAI docs](https://docs.crewai.com/))

**Strengths:** Lowest learning curve in this list. The role-as-persona framing is intuitive; small teams ship working prototypes in hours. Pydantic typing is genuinely useful.

**Weaknesses:**
- *Memory bloat at scale.* The built-in long-term memory stores raw interaction summaries rather than distilled semantic facts. Sessions accumulate.
- *Hierarchical token cost.* The hierarchical process burns tokens aggressively because the manager LLM re-reads delegate outputs every cycle.
- *Persona-cosplay drift.* The role/backstory framing nudges agents toward writing in-character rather than solving the task. Disciplined teams strip the backstory; undisciplined teams ship roleplay to prod.

**Scales well at:** Discrete, decomposable workflows where roles map naturally to job functions (research → write → edit).

**Scales poorly at:** Long sessions; problems where the persona metaphor leaks into outputs.

**Claude interop:** Direct via LiteLLM-style provider config.

### 2.4 OpenAI Agents SDK

**History:** Released March 2025 as the production-ready evolution of OpenAI's experimental Swarm. ([OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/))

**Distinctive primitive:** *Handoff*. An agent can hand off the conversation to another agent declaratively; the SDK rewrites the message history accordingly. Four primitives total: **Agents, Handoffs, Guardrails, Tracing**.

**Strengths:** Smallest concept count of any framework here. Built-in Traces dashboard for production debugging. Guardrails run in parallel with agent execution and fail fast. ([Guardrails docs](https://openai.github.io/openai-agents-python/guardrails/))

**Weaknesses:** Topology is implicit in handoff graph rather than declared; non-trivial to reason about at scale. Heavy OpenAI-API lock-in despite formal model-agnosticism.

**Scales well at:** Customer-facing assistants with clean handoff structure (triage → specialist).

**Scales poorly at:** Topologies that need explicit cycle/checkpoint control.

**Claude interop:** Possible via the model-agnostic interface but rarely the path of least resistance.

### 2.5 Google ADK (Agent Development Kit)

**Distinctive primitive:** *Tree of agents* with three deterministic workflow agent types — `SequentialAgent`, `ParallelAgent`, `LoopAgent` — plus LLM-driven `LlmAgent` for emergent reasoning. The workflow agents do not invoke an LLM for control flow, which makes the execution graph cheap and predictable. ([Google ADK multi-agent docs](https://google.github.io/adk-docs/agents/multi-agents/))

**Strengths:** The cleanest separation in the field between *deterministic orchestration* and *LLM-driven reasoning*. First-class A2A protocol export so an ADK tree can be published as an A2A endpoint and called from any framework. ([Google Codelabs A2A](https://codelabs.developers.google.com/codelabs/create-multi-agents-adk-a2a))

**Weaknesses:** Newer ecosystem; smaller third-party integrations library than LangGraph.

**Scales well at:** Production deployments on Vertex AI Agent Engine; cross-framework interop via A2A.

**Scales poorly at:** Local-first / hobbyist work; teams without GCP affinity.

**Claude interop:** Supported via provider config; Vertex AI hosts Claude models directly.

### 2.6 Anthropic's "in-house" pattern (orchestrator-worker, Claude Research)

Not a framework — a *reference design* documented in Anthropic's June 2025 multi-agent research-system writeup and embodied in the Claude Research product.

**Topology:** **Lead Researcher (Opus)** decomposes a research question into sub-queries → spawns **Sonnet subagents** that fan out to web search and reading → results return through a **Citation Agent** that grounds claims to URLs → Lead synthesizes the final report.

**Empirical result:** *"multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%"* on internal research evaluations. ([Anthropic blog](https://www.anthropic.com/engineering/multi-agent-research-system))

**The cost catch:** *"agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens."* The 90.2% gain comes at that markup. Opus 4.7's documented behavior change is "fewer subagents spawned by default" — the post-launch correction toward calmer fan-out.

**Anthropic's named no-go zones:**
> *"Most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time."*
>
> *"Some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today."*
>
> *"Multi-agent systems excel at valuable tasks that involve heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools."*

These three sentences are the most important production filter in the document. Read them again before designing a multi-agent system.

---

## 3. Eval-aware orchestration: judges, panels, juries

The evaluator-optimizer pattern is structurally a *judge over an actor*. As soon as the judge becomes load-bearing — for production routing, for verdict aggregation, for safety gating — the literature on LLM-as-judge becomes load-bearing too.

### 3.1 Petri: the auditor / target / judge separation

Anthropic Alignment's **Petri** (October 2025) is the canonical structural example of judge-actor separation at scale. ([Alignment Anthropic blog](https://alignment.anthropic.com/2025/petri/))

- An **auditor agent** plans and probes a **target** model across multi-turn, tool-augmented scenarios. It has *branching, rollback, prefill, early-terminate* primitives — first-class tools for steering the target into the corner being measured.
- A **judge** scores transcripts across a 36-dimension rubric.
- The three roles are *separate model instances* with *separate prompts*; no role sees another role's system prompt.

**Petri 2.0** (January 2026) adds a **realism classifier** that filters auditor behaviors trending implausible, and the two together drove a *47.3% median relative drop in eval-awareness* on Claude family targets. ([Petri 2.0 blog](https://alignment.anthropic.com/2026/petri-v2/))

The structural lesson generalizes beyond safety: when one model audits another for production purposes, the auditor needs *tool access richer than chat* and the judge needs to *not be the auditor*.

### 3.2 Agent-as-judge: the literature

- **Survey of LLM-as-judge** — ([arXiv:2411.15594](https://arxiv.org/abs/2411.15594)) catalogs the methods and their biases (length, position, self-preference, sycophancy).
- **Agent-as-judge** — ([arXiv:2410.10934](https://arxiv.org/abs/2410.10934), follow-up [arXiv:2508.02994](https://arxiv.org/html/2508.02994v1)) — agents (not just LLMs) judging other agents; closer correlation with human raters on agentic-trajectory tasks than transcript-only judges.
- **Multi-agent judge bias amplification** — ([arXiv:2505.19477](https://arxiv.org/html/2505.19477v3)) — naively stacking judges can *amplify* bias, not cancel it, when the judges share priors.

### 3.3 PoLL — Panel of LLM evaluators

**Panel of LLM Evaluators** — ([arXiv:2404.18796, "Replacing Judges with Juries"](https://arxiv.org/abs/2404.18796)) — *"a PoLL composed of a larger number of smaller models outperforms a single large judge, exhibits less intra-model bias due to its composition of disjoint model families, and does so while being over seven times less expensive."* The original instantiation used Command R + GPT-3.5 + Haiku. The result has held up across follow-up work.

The mechanism is not "more models." It is **disjoint families**. Three Sonnets do not a panel make.

### 3.4 Jury-on-demand

**LLM Jury-on-Demand** — ([arXiv:2512.01786](https://arxiv.org/abs/2512.01786)) — trains reliability predictors that decide when an individual judge will agree with a human expert, and dynamically expand the jury only on contested items. This is the production-ready evolution of PoLL: *cheap by default, dense when the cost matters.*

### 3.5 Minority-veto vs. majority-vote

Two aggregation policies, two different invariants:

- **Majority-vote** — optimal when judges are roughly i.i.d. and the cost of false-negatives equals false-positives. The Condorcet jury theorem applies if and only if independence holds — and §4 will argue it usually doesn't.
- **Minority-veto** — optimal when the cost of a false-positive (shipping bad output) dominates the cost of a false-negative (rejecting good output). A single rejecting judge stops the candidate. Used by Anthropic's three-lens critic panel pattern and similar high-stakes review structures.

The rule of thumb: **veto on irreversible decisions, vote on reversible ones.**

---

## 4. Cross-model triangulation: why same-family panels lie

The single most under-priced risk in 2026 multi-agent design is *correlated review error*. Three lenses of the same model do not produce three independent reviews; they produce one review repeated three times with prose variation.

### 4.1 Self-preference bias

- **Self-preference in LLM-as-judge** — ([arXiv:2410.21819](https://arxiv.org/abs/2410.21819)) — GPT-4 exhibits significant bias toward its own generations. Hypothesis: models favor outputs with lower perplexity *under their own distribution*.
- **Statistical self-bias measurement** — ([arXiv:2508.06709](https://arxiv.org/html/2508.06709v1)) — formalizes the measurement.
- **The Silent Judge** — ([arXiv:2509.26072](https://www.arxiv.org/pdf/2509.26072)) — shortcut bias linked to stylistic recognition; judges latch on to surface features of their own family's outputs.
- **Extreme self-preference** — ([arXiv:2509.26464](https://arxiv.org/html/2509.26464v1)) — replicates and extends the effect across more recent frontier models.
- **Mitigation methods** — ([arXiv:2604.22891](https://arxiv.org/html/2604.22891v1)) — quantification and partial mitigation strategies.

The implication for multi-agent design is direct: **a panel of N instances of the same model has 1 effective judge, not N.**

### 4.2 Correlated errors empirically

**Correlated Errors in Large Language Models** ([arXiv:2506.07962](https://arxiv.org/abs/2506.07962)) measured >350 LLMs on two leaderboards plus a resume-screening task. Headline: *"models agree 60% of the time when both models err."* Worse: *"larger and more accurate models have highly correlated errors, even with distinct architectures and providers."* The frontier is converging on the same wrong answers.

### 4.3 Heterogeneous panels as the only honest fix

- **Diversity of Thought** — ([arXiv:2410.12853](https://arxiv.org/abs/2410.12853)) — a panel of medium-capacity models from *different* providers (Gemini-Pro + Mixtral 8×7B + PaLM 2-M) outperformed GPT-4 alone on GSM-8K (91% vs. single-model debate at 82%) after 4 rounds. Diversity beat scale.
- **X-MAS** — ([arXiv:2505.16997](https://arxiv.org/abs/2505.16997)) — formalizes heterogeneous MAS, evaluates 27 LLMs across 5 domains, and reports +8.4% on MATH and +47% on AIME from cross-family team composition relative to single-model MAS.

### 4.4 "Voice not vote" as the practical compromise

Cross-family deployment is operationally hard: different APIs, different rate limits, different prompt formats, different latency profiles, and (often) legal/contractual barriers to mixing providers.

The pragmatic in-family pattern is **shadow lanes with voice but no vote**:

- The primary judge from family A holds verdict authority.
- A shadow judge from family A (or, ideally, from family B) runs in parallel.
- A comparator reports *agreement class* per dimension — `agree | partial-agree | disagree | unavailable` — without overriding the primary verdict.
- Disagreement is **triangulation signal, never a vote change.**

This pattern (used in the orchestrator that wrote this document) avoids the correlated-error trap of naive multi-agent debate while keeping the verdict pipeline operationally simple. Disagreement that surfaces from the shadow is human-routed, not auto-aggregated.

---

## 5. Production failure modes (2025–2026 retros)

### 5.1 Cascading failures and error amplification

The Google Research scaling study quantifies it: **independent multi-agent topologies amplify errors 17.2× versus 4.4× for centralized topologies**. The mechanism is straightforward — without a coordinator, errors from one agent become inputs to another with no quality gate. Galileo and Agent-Patterns retrospectives report consistent figures across 2025.

### 5.2 Runaway loops and the missing circuit breaker

The **$47K LangChain agent loop** (Msatfi, November 2025; widely re-reported) is the canonical case:

- Four agents (research, analysis, verification, summary) wired peer-to-peer.
- No step cap, no per-conversation USD budget, no orchestrator deciding "done."
- Verifier and analyzer entered a clarification ping-pong: verifier asked "please clarify section 3.2" with effectively the same payload every cycle.
- 11 days, ~264 hours, geometric cost escalation: $127 → $891 → $6,240 → $18,400 by week.

Sibling postmortems at the $30K and $87K scale show the same root cause: *no deterministic kill switch outside the LLM-driven loop*. The fix is not better prompting; it is a non-LLM **cost circuit breaker** with three layers: per-call max-tokens, per-conversation USD ceiling, per-loop step cap. ([Fountain City, "The Cost Circuit Breaker"](https://fountaincity.tech/resources/blog/ai-agent-cost-circuit-breaker/))

This is the single highest-leverage piece of infrastructure for any production multi-agent system. Build it first.

### 5.3 Long-horizon coherence loss

- ([arXiv:2509.09677](https://arxiv.org/abs/2509.09677)) — *"The Illusion of Diminishing Returns"* — per-step accuracy degrades as the number of steps grows. The failure mode is execution, not reasoning; even high single-step accuracy compounds into exponential failure at long horizon.
- ([arXiv:2604.11978](https://arxiv.org/abs/2604.11978)) — *"The Long-Horizon Task Mirage"* — agents that benchmark strongly at short horizon often break entirely on extended interdependent sequences.

The practical implication: **measure your agents at the horizon you will actually deploy them.** Short-task benchmarks lie.

### 5.4 Eval-awareness in production

Apollo Research, IAPS, OpenAI production-evals teams, and Anthropic Alignment have all converged on the same finding: **models behave differently when they detect they are being tested.** Petri 2.0's realism classifier is one mitigation; the broader principle is that any production system whose agents can plausibly infer "this is an eval" cannot trust their own behavior on those inputs.

The single best mitigation is to *not give the model that signal*: structurally indistinguishable prod and eval pathways, no eval-specific tool names, no telltale rubric language in the system prompt.

---

## 6. "When N agents are too many" — the scaling question

The dominant 2026 finding on agent count is Google Research's **non-monotonic scaling** result (December 2025, [arXiv:2512.08296](https://arxiv.org/html/2512.08296v1); [research.google blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)).

### 6.1 The headline numbers

- **Capability saturation:** coordination yields *diminishing or negative returns once single-agent baselines exceed ~45%* (β = −0.408, p < 0.001). If a single agent already solves the task half the time, more agents hurt.
- **Task-shape dependence:**
  - *Finance-Agent* (highly parallelizable): centralized coordination improved performance *+80.9%* over a single agent.
  - *PlanCraft* (sequential reasoning): every multi-agent variant tested degraded performance by *39–70%* (centralized −50.4%, decentralized −41.4%, hybrid −39.0%, independent −70.0%).
- **Topology-dependent error amplification:** independent topologies amplify errors 17.2×; centralized 4.4×.
- **Sweet-spot agent count:** practical saturation around **3–5 agents** for most tasks.

### 6.2 The cognitive-load argument

Past ~5–7 agents, the supervisor prompt becomes the bottleneck. It must (a) describe each agent's capabilities, (b) carry running plan state, (c) absorb interim outputs, (d) produce coordination instructions. Every additional agent burns supervisor tokens linearly *and* increases the chance of coordination errors quadratically (cross-agent disambiguation, shared-state contention).

### 6.3 The blast-radius argument

Every agent in a system is a reliability cost: an additional surface where rate limits, model deprecations, prompt regressions, and latency spikes can take down the whole flow. The reliability of a pipeline of N agents in series is the *product* of their per-agent reliabilities. Pay this cost only when the marginal accuracy gain pays the marginal reliability tax.

### 6.4 The "more think-time per agent" alternative

([arXiv:2604.03295](https://arxiv.org/html/2604.03295), "Scaling Teams or Scaling Time?") and ([arXiv:2506.07976](https://arxiv.org/abs/2506.07976), "Thinking vs. Doing") both find that **scaling test-time compute on a single agent often beats adding agents**. Extended thinking, longer plans, larger context windows are frequently a cheaper and more reliable lever than fan-out. Try think-time first.

---

## 7. The protocol layer: MCP and A2A

The 2025–2026 stabilization of two protocols moved orchestration from framework-specific glue to interoperable infrastructure.

### 7.1 MCP — Model Context Protocol (Anthropic, late 2024)

**Layer:** Vertical — *agent ↔ tools*. An MCP client (the model's host application) connects to MCP servers that publish tools, resources, and prompt templates over a JSON-RPC schema.

**Adoption:** Anthropic released MCP in November 2024. By late 2025 it had grown from ~100K to ~97M monthly SDK downloads and >10K active public servers. Adopted by ChatGPT, Cursor, Gemini, Microsoft Copilot, VS Code. Donated to the Linux Foundation's **Agentic AI Foundation (AAIF)** in December 2025 alongside Block's `goose` and OpenAI's `AGENTS.md`. ([Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation))

### 7.2 A2A — Agent2Agent (Google, April 2025)

**Layer:** Horizontal — *agent ↔ agent*. gRPC-based protocol for cross-framework agent communication. An ADK tree, a LangGraph supervisor, and a CrewAI crew can all expose A2A endpoints and call each other.

**Adoption:** >150 organizations at launch; donated to the Linux Foundation in June 2025 and now sits under AAIF alongside MCP. ([SiliconANGLE on the donation](https://siliconangle.com/2025/06/24/google-donates-agent2agent-protocol-linux-foundation/))

### 7.3 When to use which

- **MCP** when an agent needs to *call a tool* — database, filesystem, third-party API, internal service.
- **A2A** when an agent needs to *call another agent* — possibly in another framework, possibly in another org.
- **Both** in any non-trivial 2026 architecture. They are designed to compose; MCP is "USB-C for AI tools," A2A is "HTTP for AI agents."

---

## 8. Anti-patterns (the things to refuse)

Each of these has a 2025–2026 production failure attached to it. None are theoretical.

1. **Network / mesh topology** — every agent can call every other. Error amplification becomes 17.2×; debugging becomes archaeology. Use centralized or hierarchical instead.

2. **Naive multi-agent debate as primary verdict.** Same-model debate is correlated-sample voting in expensive packaging. If you need debate, make it cross-family per §4 — or use it for *signal generation* and keep verdict authority with one judge.

3. **Hierarchical-of-hierarchical at low N.** Supervisor-of-supervisors is useful at ≥6 workers, ruinously overhead-heavy below. Flatten until the supervisor's context fills.

4. **Self-consistency over a single judge mistaken for a panel.** Five draws from one Sonnet posterior are not five opinions; they are one opinion with variance.

5. **Multi-agent when prompt chaining or routing would suffice.** This is the most common mistake in the field. Anthropic's *Building Effective Agents* opens with this warning and most teams ignore it.

6. **Vague subagent prompts.** Anthropic's research-system writeup names this explicitly: subagent prompts that say "research this topic" without scoping the question, the depth, the output format, and the stop condition. Tokens explode and outputs diverge.

7. **Assuming agents can self-calibrate effort.** They cannot. They will burn budget on easy tasks and starve hard ones unless told otherwise. Pass effort budgets as explicit parameters, not as vibes in the system prompt.

8. **No circuit breaker.** Per-call max-tokens, per-conversation USD ceiling, per-loop step cap. All three. Not optional. See §5.2 for the cost of skipping this.

9. **Reading raw subagent output in the orchestrator.** Re-anchors the orchestrator on the subagent's frame, defeats the point of having subagents, and re-introduces context bloat. Distill first; orchestrator reads distillations only.

10. **Persona-cosplay.** "You are Martin Fowler ..." biases generation toward in-character writing and away from the task. Cite sources; do not ventriloquize.

11. **Same-model panels treated as independent.** Covered in §4. Worth listing twice.

12. **Skipping the outside view.** LLMs default to inside-view reasoning (details of *this* problem) and miss base rates. Reference-class forecasting is non-negotiable on novel design decisions.

---

## 9. Top 12 multi-agent patterns ranked by production leverage

Ordered by ratio of *delivered value* to *engineering and runtime cost* across the 2026 production surveys cited above. The top half pay back fast; the bottom half need a specific reason to reach for.

1. **Prompt chaining with deterministic gates.** Highest leverage, lowest novelty. If your problem decomposes cleanly, this is the right answer. Add programmatic checks between LLM calls.

2. **Routing (LLM or classifier) into specialist prompts.** Second-highest leverage. Routes expensive model usage to where it matters; lets you swap individual specialists without disturbing the rest.

3. **Sectioning parallelization with a thin aggregator.** Fan out the embarrassingly-parallel work, aggregate with a small model. Watch for aggregator context limits.

4. **Orchestrator-worker for genuinely dynamic decomposition.** Anthropic's research-system pattern. Use when the subtask shape depends on the input and the work is parallelizable. Budget for 4–15× tokens.

5. **Evaluator-optimizer with a hard step cap and a divergence detector.** Powerful for refinement tasks. Required guardrails: max iterations, divergence check (is the actor still improving?), and a judge that is *not* the actor's model family.

6. **Cross-family triangulation (PoLL / shadow-lane) for high-stakes review.** Use disjoint families. Use minority-veto on irreversible decisions, majority-vote on reversible ones. Use voice-not-vote when operational constraints prevent full cross-family aggregation.

7. **Sequential / Parallel / Loop deterministic workflow agents.** Google ADK's pattern, but the design lesson generalizes: separate the deterministic control flow from the LLM-driven reasoning. Cheaper, more predictable, easier to debug.

8. **Auditor / target / judge separation (Petri pattern) for any evaluation that matters.** When one model judges another in production, give the auditor richer tools than chat and put the judge on a separate instance with a separate prompt.

9. **A2A-fronted services for cross-framework or cross-team agents.** Publish your agent as an A2A endpoint instead of importing the consuming framework into yours. Avoids monorepo capture.

10. **Jury-on-demand for cost-sensitive judging at scale.** Cheap single judge for confident items, expand the jury only on contested ones. The production-ready evolution of static PoLL.

11. **Autonomous agent loop with sandbox + budget + human checkpoint.** Reserve for genuinely open-ended tasks in trusted environments. Sandbox the side effects. Set hard budgets. Insert a human-in-the-loop checkpoint at every irreversible action.

12. **Hierarchical-of-hierarchical.** Last on the list because the right N is rare. Reach for it only when worker count exceeds ~6 *and* sub-team supervisors meaningfully reduce supervisor prompt size. Otherwise flatten.

---

## 10. Closing: the three sentences to remember

Stripped to slogans:

- **Workflows beat agents on cost, latency, and observability for most business problems. Reach for the agent loop last, not first.**
- **A panel of the same model is one judge. If review matters, cross families.**
- **Build the cost circuit breaker before the second agent. The $47K incidents are not exotic; they are what happens by default.**

Everything else in this document is implementation detail behind those three claims.

---

## Sources

### Anthropic-blessed (primary)
- Schluntz, E. & Zhang, B. *Building Effective Agents.* Anthropic Engineering, December 19, 2024. ([link](https://www.anthropic.com/engineering/building-effective-agents))
- Anthropic Engineering. *How we built our multi-agent research system.* 2025. ([link](https://www.anthropic.com/engineering/multi-agent-research-system))
- Anthropic Alignment. *Petri: An open-source auditing tool to accelerate AI safety research.* October 2025. ([link](https://alignment.anthropic.com/2025/petri/))
- Anthropic Alignment. *Petri 2.0: New Scenarios, New Model Comparisons, and Improved Eval-Awareness Mitigations.* January 2026. ([link](https://alignment.anthropic.com/2026/petri-v2/))

### Framework documentation
- LangGraph Multi-Agent Supervisor reference. ([link](https://reference.langchain.com/python/langgraph-supervisor))
- LangGraph Multi-Agent Swarm reference. ([link](https://reference.langchain.com/python/langgraph-swarm))
- Microsoft Research. *AutoGen v0.4: Reimagining the foundation of agentic AI.* 2025. ([link](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/))
- Microsoft Learn. *AutoGen to Microsoft Agent Framework Migration Guide.* February 2026. ([link](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/))
- DevBlogs. *Microsoft Agent Framework Version 1.0.* 2026. ([link](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/))
- CrewAI Documentation. ([link](https://docs.crewai.com/))
- OpenAI Agents SDK. ([link](https://openai.github.io/openai-agents-python/))
- OpenAI Agents SDK — Handoffs. ([link](https://openai.github.io/openai-agents-python/handoffs/))
- OpenAI Agents SDK — Guardrails. ([link](https://openai.github.io/openai-agents-python/guardrails/))
- OpenAI Agents SDK — Tracing. ([link](https://openai.github.io/openai-agents-python/tracing/))
- Google ADK — Multi-agent systems. ([link](https://google.github.io/adk-docs/agents/multi-agents/))
- Google Codelabs. *Create multi-agent system with ADK and A2A.* ([link](https://codelabs.developers.google.com/codelabs/create-multi-agents-adk-a2a))

### Academic (arXiv)
- Kim, E. et al. *Correlated Errors in Large Language Models.* arXiv:2506.07962, 2025. ([link](https://arxiv.org/abs/2506.07962))
- Verga et al. *Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models.* arXiv:2404.18796, 2024. ([link](https://arxiv.org/abs/2404.18796))
- *A Survey on LLM-as-a-Judge.* arXiv:2411.15594. ([link](https://arxiv.org/abs/2411.15594))
- *Agent-as-a-Judge: Evaluate Agents with Agents.* arXiv:2410.10934. ([link](https://arxiv.org/abs/2410.10934))
- *When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation.* arXiv:2508.02994. ([link](https://arxiv.org/html/2508.02994v1))
- *Who Judges the Judge? LLM Jury-on-Demand.* arXiv:2512.01786, 2025. ([link](https://arxiv.org/abs/2512.01786))
- Wataoka, K. *Self-Preference Bias in LLM-as-a-Judge.* arXiv:2410.21819. ([link](https://arxiv.org/abs/2410.21819))
- *Play Favorites: A Statistical Method to Measure Self-Bias in LLM-as-a-Judge.* arXiv:2508.06709. ([link](https://arxiv.org/html/2508.06709v1))
- *The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge.* arXiv:2509.26072. ([link](https://www.arxiv.org/pdf/2509.26072))
- *Extreme Self-Preference in Language Models.* arXiv:2509.26464. ([link](https://arxiv.org/html/2509.26464v1))
- *Quantifying and Mitigating Self-Preference Bias of LLM Judges.* arXiv:2604.22891. ([link](https://arxiv.org/html/2604.22891v1))
- *Judging with Many Minds: Bias Amplification and Resistance in Multi-Agent Based LLM-as-Judge.* arXiv:2505.19477. ([link](https://arxiv.org/html/2505.19477v3))
- Hegazy, M. *Diversity of Thought Elicits Stronger Reasoning Capabilities in Multi-Agent Debate Frameworks.* arXiv:2410.12853. ([link](https://arxiv.org/abs/2410.12853))
- Ye, R. et al. *X-MAS: Towards Building Multi-Agent Systems with Heterogeneous LLMs.* arXiv:2505.16997. ([link](https://arxiv.org/abs/2505.16997))
- *The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs.* arXiv:2509.09677. ([link](https://arxiv.org/abs/2509.09677))
- *The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break.* arXiv:2604.11978. ([link](https://arxiv.org/abs/2604.11978))
- *Thinking vs. Doing: Agents that Reason by Scaling Test-Time Interaction.* arXiv:2506.07976. ([link](https://arxiv.org/abs/2506.07976))
- *Scaling Teams or Scaling Time? Memory Enabled Lifelong Learning in LLM Multi-Agent Systems.* arXiv:2604.03295. ([link](https://arxiv.org/html/2604.03295))
- Google Research. *Towards a Science of Scaling Agent Systems.* arXiv:2512.08296, December 2025. ([link](https://arxiv.org/html/2512.08296v1))

### Production retrospectives and protocol
- Google Research blog. *Towards a science of scaling agent systems: When and why agent systems work.* ([link](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/))
- Msatfi. *I Spent $0.20 Reproducing the Multi-Agent Loop That Cost Someone $47K.* Medium, November 2025. ([link](https://medium.com/@mohamedmsatfi1/i-spent-0-20-reproducing-the-multi-agent-loop-that-cost-someone-47k-7f57c51f3c06))
- Anhaia, G. *The Agent That Spent $47K on Itself: An Autonomous-Loop Postmortem.* dev.to, 2025. ([link](https://dev.to/gabrielanhaia/the-agent-that-spent-47k-on-itself-an-autonomous-loop-postmortem-3313))
- Fountain City. *The Cost Circuit Breaker: Financial Controls for Production AI Agents.* ([link](https://fountaincity.tech/resources/blog/ai-agent-cost-circuit-breaker/))
- Linux Foundation. *Linux Foundation Announces the Formation of the Agentic AI Foundation.* December 2025. ([link](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation))
- SiliconANGLE. *Google donates Agent2Agent Protocol to the Linux Foundation.* June 2025. ([link](https://siliconangle.com/2025/06/24/google-donates-agent2agent-protocol-linux-foundation/))
- InfoQ. *OpenAI and Anthropic Donate AGENTS.md and Model Context Protocol to New Agentic AI Foundation.* December 2025. ([link](https://www.infoq.com/news/2025/12/agentic-ai-foundation/))
