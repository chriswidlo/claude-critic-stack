## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage on KB/retrieval surface design for an AI agent in AU banking. Librarian returned partial-coverage retrieval: six supporting passages (all Anthropic 2024–2025), four contradicting/complicating signals (C1–C4, including a corpus-silence finding), three on-topic stubs, and eight explicit WebSearch gaps. Self-rated coverage: **thin to partial**.

## Direct facts

1. [Anthropic, "Effective Context Engineering for AI Agents" (2025), §"Context retrieval and agentic search"] Agents are increasingly augmenting embedding-based pre-inference retrieval with "just in time" strategies that maintain lightweight identifiers and load data at runtime via tools. (confidence: direct)
2. [Anthropic, same essay, same section] Hybrid strategy (some pre-indexed, some autonomous exploration) is named as "better suited for contexts with less dynamic content, such as legal or finance work." (confidence: direct)
3. [Anthropic, same essay, §"Why context engineering is important"] "Context rot" is asserted: recall degrades as context length grows; LLMs have a finite "attention budget." (confidence: direct)
4. [Anthropic, same essay, §"Context engineering for long-horizon tasks"] Larger context windows do not eliminate context-pollution and relevance concerns "for the foreseeable future." (confidence: direct)
5. [Anthropic, "How we built our multi-agent research system" (2025), §"Architecture overview"] Static-RAG (top-k similar chunks → generate) is named as a failure mode versus multi-step search that adapts to findings. (confidence: direct)
6. [Same essay, §"Benefits of a multi-agent system"] Quoted token-economics: agents ≈ 4× chat tokens; multi-agent systems ≈ 15× chat tokens. (confidence: direct)
7. [Same essay, §"Production reliability" + appendix] Subagents persist work to external systems and pass lightweight references back; the CitationAgent pattern attaches source locations post-hoc. (confidence: direct)
8. [Anthropic, "Building Effective Agents" (2024), §"Building blocks" + Appendix 2] MCP is named as the third-party tool integration surface; the "ACI = HCI effort" rule of thumb is stated. (confidence: direct)
9. [Anthropic, "Effective Context Engineering" (2025)] Claude Code is cited as an example: CLAUDE.md dropped in up front; glob/grep used for just-in-time navigation, "effectively bypassing the issues of stale indexing." (confidence: direct)
10. [Corpus state] Helland 2007, Hohpe & Woolf 2003, Evans 2003 are present as **stubs (citation-only, body not ingested).** (confidence: direct)

## Inferred claims

1. [canon-librarian] The corpus's voice on retrieval architecture is "one-sided toward the Anthropic agentic-retrieval position." (confidence: inferred)
2. [canon-librarian] The "less dynamic content" framing applied to finance/legal "may not hold for fast-moving regulatory guidance and product-disclosure regimes" — surfaced for challenge. (confidence: inferred)
3. [canon-librarian] The artifact-and-reference pattern from the multi-agent essay is "directly applicable to a regulatory KB." (confidence: inferred)
4. [canon-librarian] For high-volume low-margin banking interactions, 15× token economics may make static retrieval correct on cost grounds even if it loses on quality. (confidence: inferred)
5. [canon-librarian] For AU banking, the "lightweight identifiers + load on demand" framing maps onto querying authoritative systems-of-record (APRA, ASIC, RG/INFO) at read time rather than re-embedding on every change. (confidence: inferred)
6. [canon-librarian] The implication of the ACI principle for a banking KB is that the surface should be tool-shaped (typed, narrow, well-documented) rather than a generic search endpoint. (confidence: inferred)

## Authority-framed claims

1. "Anthropic's stated position, working from production agents, is that filesystem + grep + agent navigation can outperform pre-built embedding indexes." — underlying claim: filesystem-based navigation can beat vector indexes for high-churn corpora. Quote present in output: yes (the Claude Code / CLAUDE.md passage in C1). Confidence: direct (quoted) but the generalization beyond Claude Code's coding context to AU banking is **inferred** by the librarian, not stated by Anthropic.
2. "Anthropic explicitly names finance and legal as the domain where pre-indexed retrieval still earns its keep." — underlying claim: hybrid retrieval is the recommended architecture for finance. Quote present in output: yes (passage 2). Confidence: direct. Note: Anthropic's framing assumes finance is "less dynamic content"; that premise is contestable for AU regulatory work.
3. References to GraphRAG (Microsoft 2024), ColBERT (Khattab & Zaharia), BloombergGPT (2023), and "structured-data-beats-RAG arguments from Snowflake/Databricks blogs." — underlying claim: contradicting literature exists. Quote present in output: **no** — the librarian names these works to flag their absence, not to summarize them. Confidence: **unsupported within this corpus retrieval**; treat as WebSearch targets, not as evidence yet.

## Contradictions surfaced

- **C1 (frame-level): vector-DB-RAG default vs. agent-navigation-over-structured-surface.** The default architectural reflex (embed → vector store → similarity search) is contradicted by Anthropic's own production stance that filesystem + grep + just-in-time loading sidesteps staleness. Tension is internal to the corpus's own voice — the same essays that endorse hybrid retrieval also argue against pre-indexed embeddings as the default.
- **C2: long-context-window-as-substitute-for-retrieval is rejected.** "Context windows of all sizes will be subject to context pollution and information relevance concerns." Cuts against both RAG-maximalism and long-context-maximalism simultaneously.
- **C3: agentic retrieval is endorsed AND named as expensive.** Same essay: multi-agent ≈ 15× chat tokens; "economic viability" requires high-value tasks. For consumer-facing banking Q&A this is a real cost objection to the architecture the corpus otherwise endorses.
- **C4: corpus silence as a contradicting finding.** No passage on GraphRAG, ColBERT/late-interaction, structured-store-beats-RAG, BloombergGPT-style domain stacks, contextual retrieval (Anthropic Sep 2024 — notably absent despite being on-publisher), or KB freshness/invalidation as a research topic. **Silence is a finding, not consensus.**

Do not collapse C1 and C3: the corpus simultaneously endorses agentic retrieval (C1's resolution) and warns about its cost (C3). Both edges must reach the orchestrator.

## Subagent's own verdict (verbatim)

> "Thin to partial."
> "The canon speaks with one voice (Anthropic, 2024–2025) and that voice argues against static embedding-RAG as the default and for agent-navigated, tool-shaped retrieval with hybrid pre-indexed bootstrap — explicitly naming finance/legal as a hybrid-fit domain. The canon is silent on the contradicting literature (GraphRAG, ColBERT, structured-store arguments, BloombergGPT-style domain stacks); treat the canon view as one input, not as the field's consensus."

## Confidence / corpus-state notes

- **Corpus is single-voiced (Anthropic 2024–2025) on retrieval architecture.** Treat as one input, not field consensus.
- **Stubs flagged (citation-only, no body):** Helland 2007 (most relevant — freshness/invalidation), Hohpe & Woolf 2003 (Scatter-Gather, Aggregator, Correlation Identifier), Evans 2003 (Bounded Context, Anti-Corruption Layer). Do not synthesize quotes from these; orchestrator must not let downstream agents ventriloquize them.
- **Staleness flag:** corpus does not include Anthropic's own Sep 2024 contextual-retrieval publication — itself a freshness gap in the canon refresher's coverage.
- **WebSearch targets named explicitly by librarian:** contextual retrieval (Anthropic 2024), GraphRAG (Microsoft 2024), hybrid retrieval/reranking (BM25+dense, RRF, Cohere/Voyage rerankers), ColBERT/late-interaction, BloombergGPT and domain-specific stacks, regulatory-document ingestion (XBRL, Akoma Ntoso, AU Federal Register of Legislation/APRA/ASIC APIs), KB freshness/invalidation as research topic, AI-consumer information architecture counter-positions.

## Gaps the subagent missed

1. No retrieval on **evaluation methodology** for retrieval quality (e.g., RAGAS, BEIR, MTEB) — relevant for "how would we know the chosen architecture is working in production."
2. No retrieval on **PII / data-residency** constraints which materially shape AU banking KB design (APP, CPS 234) — though this may be out-of-scope for retrieval-architecture per se, the librarian did not flag it as a gap.
3. No retrieval on **human-in-the-loop / approval workflows** for high-stakes regulated answers — the corpus's agentic-retrieval voice is silent on when an agent must defer to a human, and the librarian did not surface this silence.
4. No engagement with the **"don't build a KB at all — call the systems-of-record live"** position; the librarian gestures at this via C1 but does not isolate it as a distinct architectural option for the scope-mapper.

## Token budget
~1,150 tokens.
