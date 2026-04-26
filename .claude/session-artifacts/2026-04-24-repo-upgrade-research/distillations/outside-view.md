## Source agent
outside-view

## Invocation summary
The orchestrator asked for the reference-class forecast for upgrading this repo. Canon covered the baseline principles; web research was then used for currency on 2025-2026 agent architecture selection, judge reliability, and curated-domain retrieval performance.

## Direct facts
1. [Anthropic, Building Effective Agents (2024)] recommends starting with the simplest system that works and adding complexity only when it demonstrably improves outcomes. (confidence: direct)
2. [Anthropic, How we built our multi-agent research system (2025)] found that multi-agent research excelled on breadth-first queries, but also reported roughly 15x chat-level token use for multi-agent systems. (confidence: direct)
3. [Google Research blog summarizing "Towards a Science of Scaling Agent Systems" (January 28, 2026)] reports that centralized multi-agent coordination improved performance by 80.9% on parallelizable tasks, while multi-agent variants degraded performance by 39-70% on sequential planning tasks; independent multi-agent systems amplified errors by up to 17.2x. (confidence: direct)
4. [Google Research blog summarizing "Towards a Science of Scaling Agent Systems" (January 28, 2026)] says a predictive model identified the optimal architecture for 87% of unseen task configurations using measurable task properties such as decomposability and tool density. (confidence: direct)
5. [Balog, Metzler, Qin, SIGIR 2025] provide empirical evidence that LLM judges can be biased toward LLM-based rankers and can struggle to detect subtle performance differences. (confidence: direct)
6. [Guo et al., PNAS 2026 / Google Research publication page] reports that expert-curated, domain-specific retrieval outperformed closed models on complex literature questions in a specialized scientific domain. (confidence: direct)

## Inferred claims
1. The reference class is not "software repos" in general; it is small, research-oriented LLM review stacks that are deciding whether to become richer multi-agent systems or remain lean prompt systems with better evidence and evals. (confidence: inferred)
2. In this class, the common failure mode is architecture-task mismatch: adding more agents, judges, or orchestration before proving that the task is parallelizable and that the extra coordination is worth the cost. (confidence: inferred)
3. For this repo specifically, the outside view favors upgrades in evaluation, corpus quality, context management, and runtime selection heuristics ahead of async multi-agent expansion or heavyweight frameworking. (confidence: inferred)

## Authority-framed claims
none

## Contradictions surfaced
- Multi-agent coordination can massively help on decomposable research tasks vs. the same coordination materially hurting sequential tasks.
- LLM-as-judge can scale evaluation well in practice vs. recent evidence that judges can be biased and weak at detecting subtle deltas.

## Subagent's own verdict (verbatim)
Below base rate — if "upgrade" means adding more agents and orchestration by default. Within tolerance — if "upgrade" means better evals, better corpus quality, and architecture selection matched to task shape.

## Gaps the subagent missed
- No direct measurement exists yet for how parallelizable this repo's actual target tasks are.
- No current cost/latency baseline exists for the stack's workflow steps.
- No calibration dataset exists for judge drift inside this repo.

## Token budget
~700
