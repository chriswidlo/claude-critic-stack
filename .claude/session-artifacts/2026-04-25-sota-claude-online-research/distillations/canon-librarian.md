## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for corpus retrieval on SOTA Claude-based online research agents. Librarian returned PARTIAL coverage: strong on Anthropic's own engineering essays (multi-agent system, BEA, context engineering, tool design, eval rubrics); empty on hosted competitors, open-source orchestrators, MCP server design, and independent benchmarks. Single explicitly contradicting passage came from Anthropic itself.

## Direct facts
1. [Anthropic, "How we built our multi-agent research system", 2025-06-13] Multi-agent (Opus 4 lead + Sonnet 4 subagents) outperformed single-agent Opus 4 by 90.2% on internal research eval. (confidence: direct)
2. [Same essay] Three factors explain 95% of variance on BrowseComp; token usage alone explains 80%; tool calls and model choice are the other two. (confidence: direct)
3. [Same essay, cost paragraph] "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats." (confidence: direct)
4. [Same essay] "some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today." (confidence: direct)
5. [Same essay] "LLM agents are not yet great at coordinating and delegating to other agents in real time." (confidence: direct)
6. [Same essay, Production reliability] "minor changes cascade into large behavioral changes … One step failing can cause agents to explore entirely different trajectories." (confidence: direct)
7. [Same essay] LLM-as-judge eval rubric uses 5 axes (factual accuracy, citation accuracy, completeness, source quality, tool efficiency) plus a separate CitationAgent post-pass; single LLM call returning 0.0–1.0 + pass-fail was most consistent; start with ~20 queries, not 1000. (confidence: direct)
8. [Anthropic, "Building Effective Agents", 2024-12-19] "Most successful implementations weren't using complex frameworks … Build with simple, composable patterns. Start by using LLM APIs directly." (confidence: direct)
9. [BEA, "When (and when not) to use agents"] "Find the simplest solution possible … This might mean not building agentic systems at all. For many applications, optimizing single LLM calls with retrieval and in-context examples is usually enough." (confidence: direct)
10. [Anthropic, "Effective Context Engineering for AI Agents", 2025-09-29] Just-in-time context retrieval — agents maintain lightweight identifiers (file paths, queries, links) and load dynamically; subagents use 10K+ tokens but return 1K–2K compressed summaries; lead agent only sees summaries. Three live techniques for long-horizon: compaction, structured note-taking, sub-agent architectures. (confidence: direct)
11. [BEA Appendix 2 + multi-agent post Tool design] "Spent more time optimizing tools than the prompt … bad tool descriptions can send agents down completely wrong paths"; reports a 40% decrease in task completion time from improved tool descriptions. (confidence: direct)
12. [Wang et al., "Devil's Advocate: Anticipatory Reflection for LLM Agents", EMNLP 2024] 3-fold introspective intervention (anticipatory reflection / post-action alignment with backtracking / post-completion review); 23.5% absolute success on WebArena, +3.5% over zero-shot, 45% fewer trials/revisions. (confidence: direct)
13. [Shinn et al., Reflexion, arXiv:2303.11366] Abstract-only stub entry in corpus; reflect-and-retry foundation. (confidence: direct, but limited to abstract)

## Inferred claims
1. [canon-librarian] Multi-agent benefit on BrowseComp is "mostly parallel-token-budget, not magic coordination," derived from the 80%-of-variance token figure. (confidence: inferred)
2. [canon-librarian] Tool/MCP design is a larger lever than prompt tweaks for research agents (derived from the 40% time-decrease and tool-optimization-time claims). (confidence: inferred)
3. [canon-librarian] BEA passage is a "direct argument against framework-first orchestrator selection." (confidence: inferred)
4. [canon-librarian] The Anthropic production-reliability passage is "an argument against DIY orchestration" given Anthropic itself needed rainbow deployments, full tracing, checkpoint/resume. (confidence: inferred)
5. [canon-librarian] Devil's Advocate's 23.5% absolute ceiling is "low" — author's editorial framing of the number. (confidence: inferred)

## Authority-framed claims
None of the surfaced claims are author-ventriloquized; every cited claim is anchored to a quoted or paraphrased passage from the named essay/paper. No "as X would say" framing detected.

## Contradictions surfaced
- A vs B (both inside the same Anthropic essay): the multi-agent system "outperformed single-agent Opus 4 by 90.2%" (passage 1) vs. "multi-agent systems use about 15× more tokens" and "are not a good fit" for high-coordination/shared-context tasks (passages 3–5). The most credible multi-agent critique lives inside the multi-agent promotion essay.
- Anthropic multi-agent essay vs. BEA: "build a multi-agent research system that wins on internal eval" vs. BEA's "find the simplest solution possible … This might mean not building agentic systems at all." Same publisher, ~6 months apart.
- Multi-agent essay's Production reliability passage ("minor changes cascade … gap between prototype and production is often wider than anticipated") undermines the ease-of-adoption framing implied elsewhere in the same essay.

## Subagent's own verdict (verbatim)
"Corpus coverage: PARTIAL. Strong on multi-agent orchestration, tool design, context engineering, evaluation rubrics — all from Anthropic's own engineering essays. NO entries on hosted competitors (OpenAI DR, Perplexity), open-source orchestrators (LangGraph, CrewAI, smolagents, OpenDeepResearch), MCP server design beyond passing mention, or independent benchmarks. Single explicitly contradicting passage is from Anthropic itself."

## Declared corpus gaps (carry forward verbatim)
1. No competitor product entries (OpenAI DR, Perplexity, Gemini DR; BrowseComp/GAIA/SimpleQA/FRAMES benchmarks).
2. Zero in-depth coverage of LangGraph, CrewAI, smolagents, AutoGen, OpenDeepResearch, Claude Agent SDK (BEA mentions in single bullet).
3. No MCP server design entry; no prompt-injection-via-web-content; no rate-limit/paywall handling.
4. No independent skeptic of multi-agent research (e.g., Cognition "Don't build multi-agents," LangChain critique posts); closest is Anthropic self-criticism in contradiction A.
5. No groundedness evaluation methodology beyond the 5-axis rubric (RAGAS, TruLens, DeepEval, FActScore, AIS).
6. Currency gap: most recent entry June 2025; product space has shifted since.

## Gaps the subagent missed
- Did not surface any non-Anthropic primary source on agentic web-research design (every supporting passage except Devil's Advocate and Reflexion is Anthropic-authored). Source-diversity is itself a contradiction the librarian did not flag as such.
- No retrieval on cost/latency tradeoff numbers from competitor systems to triangulate the 15×-tokens figure.
- No retrieval on failure-mode taxonomies for web-research agents (hallucinated citations, source-quality drift, prompt injection); these are likely partial-canon, not zero-canon, and were not probed.
- No coverage of human-in-the-loop checkpoints for long-running research runs, despite "long-horizon" being explicitly named in the context-engineering essay.
- Outside-view consideration: librarian did not flag that the corpus's Anthropic-heavy composition will systematically bias downstream synthesis toward Anthropic's preferred architecture.

## Token budget
~950 tokens.
