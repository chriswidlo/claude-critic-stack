## Source agent
canon-librarian

## Invocation summary
The orchestrator asked for canon evidence relevant to improving an adversarial-review stack for design work. The corpus had good coverage on agent simplicity, reflection, context management, multi-agent research, and operational simplicity, with meaningful contradictions rather than a single pro-complexity story.

## Direct facts
1. [Anthropic, Building Effective Agents (2024)] says the most successful implementations used "simple, composable patterns" and recommends starting simple, optimizing with evals, and adding multi-step agentic systems only when simpler solutions fall short. (confidence: direct)
2. [Anthropic, Effective Context Engineering for AI Agents (2025)] states that context is finite, that stronger long-horizon agents need compaction, structured note-taking, and sometimes sub-agent architectures, and that subagents should return condensed summaries rather than their full search traces. (confidence: direct)
3. [Anthropic, How we built our multi-agent research system (2025)] reports a 90.2% internal-eval improvement over a single-agent baseline on breadth-first research tasks, but also reports roughly 15x chat-level token use for multi-agent systems. (confidence: direct)
4. [Anthropic, How we built our multi-agent research system (2025)] recommends starting evals immediately with small samples and says a rubric-based single LLM judge worked well for scaling free-form evaluation, while human testing still caught failures automation missed. (confidence: direct)
5. [Wang et al., Devil's Advocate: Anticipatory Reflection for LLM Agents (2024)] reports improved WebArena success and a 45% reduction in trials and plan revisions from anticipatory and post-action reflection. (confidence: direct)
6. [Google SRE Book (2016), monitoring chapter] says the critical path from problem onset through paging and triage should stay simple and comprehensible. (confidence: direct)

## Inferred claims
1. This repo is directionally right to use dissent, reflection, and distillation, but it is under-instrumented relative to the evaluation discipline the canon now argues for. (confidence: inferred)
2. The canon supports stronger memory, compaction, and artifact handoff patterns more than it supports adding ever more critic personas. (confidence: inferred)
3. The repo's next leverage point is not another prompt role by default; it is making the existing roles easier to measure, compare, and prune. (confidence: inferred)

## Authority-framed claims
none

## Contradictions surfaced
- [Anthropic, Building Effective Agents (2024)] says to add complexity only when it demonstrably improves outcomes vs. [Anthropic, Multi-Agent Research System (2025)] showing large gains from multi-agent orchestration on the right class of research tasks.
- [Wang et al. (2024)] supports explicit anticipatory critique loops vs. [Google SRE Book (2016)] pushing simplicity in critical operational paths; more critique can help quality but also create harder-to-debug systems.

## Subagent's own verdict (verbatim)
Corpus coverage: good

## Gaps the subagent missed
- The corpus does not yet include strong peer-reviewed material on judge bias and agent-architecture selection from 2025-2026.
- The corpus is still heavy on architecture/books and light on recent agent-evaluation literature.
- Many foundational books remain stubs rather than full text.

## Token budget
~650
