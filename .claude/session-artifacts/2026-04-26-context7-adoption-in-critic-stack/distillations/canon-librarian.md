## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage on adopting Context7 (live third-party doc retrieval) into the critic-stack. Librarian returned `partial` coverage with 5 supporting + 6 contradicting passages, plus 6 declared gaps.

## Direct facts
1. [Anthropic, "Building effective agents", Dec 2024] MCP is named as an integration mechanism: "...allows developers to integrate with a growing ecosystem of third-party tools..." (confidence: direct)
2. [Anthropic, "Building effective agents", Dec 2024] "...we recommend finding the simplest solution possible, and only increasing complexity when needed." (confidence: direct)
3. [Anthropic, "Building effective agents", Dec 2024] Frameworks "create extra layers of abstraction that can obscure the underlying prompts and responses ... a common source of customer error." (confidence: direct)
4. [Anthropic, "Multi-agent research system", Jun 2025] "...an agent searching the web for context that only exists in Slack is doomed from the start." (confidence: direct)
5. [Anthropic, "Multi-agent research system", Jun 2025] "...agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats." (confidence: direct)
6. [Anthropic, "Multi-agent research system", Jun 2025] "...minor changes cascade into large behavioral changes ... Agents are stateful and errors compound." (confidence: direct)
7. [Anthropic, "Effective context engineering", Sep 2025] Just-in-time retrieval pattern: "...agents ... maintain lightweight identifiers ... and use these references to dynamically load data into context at runtime using tools." (confidence: direct)
8. [Anthropic, "Effective context engineering", Sep 2025] On bloated tool sets: "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better." (confidence: direct)
9. [Anthropic, "Effective context engineering", Sep 2025] Sub-agent architectures: each "...might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary..." (confidence: direct)
10. [Cockburn, "Hexagonal Architecture", Jan 2005] "A port identifies a purposeful conversation. There will typically be multiple adapters for any one port..." (confidence: direct)
11. [Cockburn, Jan 2005] "My selection tends to favor a small number, two, three or four ports..." (confidence: direct)
12. [librarian gap declarations] evans-ddd, hohpe-eip, nygard-release-it, vernon-strategic-monoliths are `body_completeness:stub` — no ingested body text. (confidence: direct)
13. [librarian gap declarations] No corpus material on Claude Code "Skills" as integration primitive, version-pinned doc registries, or empirical studies on "tool addition increases hallucination." (confidence: direct)

## Inferred claims
1. [canon-librarian] S2 implies an agent restricted to curated canon is structurally unable to answer "what does library X v4.2.1 export"; supports adding *some* live-docs surface. (confidence: inferred)
2. [canon-librarian] S3 argues *against* option D (corpus-refresher trigger) because pre-ingesting fast-moving third-party docs stales instantly. (confidence: inferred)
3. [canon-librarian] S4 favors option C (dedicated subagent) over option B (raw tool on every existing agent) by separation-of-concerns analogy to canon-librarian. (confidence: inferred)
4. [canon-librarian] C2 directly strikes option B: two retrieval tools with overlapping-but-distinct trust models create the ambiguous-tool-choice failure mode. (confidence: inferred)
5. [canon-librarian] C3 weighs against option E (Skills) because Skills tend to be the most opaque integration shape. (confidence: inferred)
6. [canon-librarian] C4 implies any chosen option needs a *gating predicate* (fire only when question names specific library + version), not unconditional invocation. (confidence: inferred)
7. [canon-librarian] C5 supports option C over B on blast-radius grounds, and supports staged rollout regardless. (confidence: inferred)
8. [canon-librarian] C6 + S5 together suggest Context7 should sit *behind* canon-librarian as a second adapter on the same retrieval port, with librarian responsible for trust-tier labeling. (confidence: inferred)
9. [canon-librarian] Synthesis on hallucination: tools *decrease* hallucination when answers replace guessing; *increase* anchoring when tool output is privileged over conflicting curated material. (confidence: inferred; no direct passage)

## Authority-framed claims
None. The librarian consistently quoted source text rather than ventriloquizing. All "Anthropic recommends..." / "Cockburn argues..." framings in the report are backed by an inline quote from the cited document.

## Contradictions surfaced
- **Add a live-docs surface (S2) vs. don't add complexity by default (C1).** S2: missing right tool guarantees failure; C1: default is don't add, must clear "what currently fails" bar.
- **Just-in-time retrieval via tools (S3) vs. tool-set bloat / ambiguous tool choice (C2).** S3 endorses runtime tool loading; C2 warns the runtime decision among overlapping tools is itself the failure mode.
- **MCP as canonical integration (S1) vs. framework opacity (C3).** S1 endorses MCP-style integration; C3 cautions third-party retrieval frameworks obscure what's under the hood.
- **Sub-agent architectures provide isolation (S4) vs. multi-agent token cost ~15× (C4).** S4 favors a new subagent for clean context; C4 says new subagent only viable on high-value tasks with gating.
- **Multiple adapters per port are normal (S5) vs. keep ports few, 2–4 (C6).** S5 permits a Context7 adapter alongside canon; C6 cautions against proliferation — Context7 should be a second adapter on the existing retrieval port, not a new port.
- **Implied: tool addition decreases vs. increases hallucination.** No direct passage either way; librarian flagged this as gap (6).

## Subagent's own verdict (verbatim)
"Partial. Strong on agent design (Anthropic's three engineering essays) and architectural boundaries (Cockburn). Weak/empty on trust-tier separation between retrieval sources and coupling between agents and external retrieval backends..."

## Gaps the subagent missed
- No retrieval against any non-Anthropic, non-Cockburn source on *retrieval-augmented generation evaluation* (e.g. RAG benchmarks, citation-faithfulness studies) — would directly bear on whether Context7 reduces or amplifies hallucination.
- No passage retrieved on *cache invalidation / staleness semantics* of third-party doc registries, even though that is the core risk of option D and a secondary risk of B/C.
- No retrieval on *cost of capability not used* — i.e., the carrying cost of an installed-but-rarely-fired backend, separate from per-invocation token cost (C4 covers only the latter).
- The 6 declared gaps are corpus-shape gaps (stubs), not query-shape gaps — librarian did not attempt to bound *what* would have been retrieved had the stubs been filled.

## Token budget
~860 tokens.
