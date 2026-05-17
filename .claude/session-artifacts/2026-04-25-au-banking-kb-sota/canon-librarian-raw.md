# Canon retrieval — KB/retrieval surface for an AI agent (AU banking)

## Corpus coverage
**Thin to partial.** The corpus has strong coverage of *agent design and context management* (three Anthropic essays, 2024–2025) and adjacent material on integration, DDD, and distributed-state hygiene (Hohpe, Evans, Helland — all stubs, citations only). The corpus has **no entries** on: RAG architectures, vector databases, hybrid retrieval (BM25+dense), reranking, contextual retrieval (Anthropic 2024), GraphRAG (Microsoft 2024), ColBERT / late-interaction, BloombergGPT or domain-specific LLM stacks, regulatory-document ingestion pipelines, or KB freshness/invalidation as a research topic. These are explicit gaps; flag as WebSearch targets downstream.

The most relevant retrievable material is the Anthropic context-engineering and multi-agent essays, which take a position on retrieval architecture that *is itself contrarian* relative to the standard "vector DB + RAG" mental model. That contrarian position is the strongest contradicting passage the corpus offers, and it is on-corpus.

---

## Supporting passages

### 1. Anthropic, "Effective Context Engineering for AI Agents" (2025), §"Context retrieval and agentic search"
> "Today, many AI-native applications employ some form of embedding-based pre-inference time retrieval to surface important context for the agent to reason over. As the field transitions to more agentic approaches, we increasingly see teams augmenting these retrieval systems with 'just in time' context strategies. Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."

**Relevance:** Directly addresses the architectural choice between pre-indexed embedding retrieval and agent-tool-driven retrieval. For a regulated, high-churn domain like AU banking, the "lightweight identifiers + load on demand" framing maps onto querying authoritative systems-of-record (APRA prudential standards register, ASIC instruments, RG/INFO numbering) at read time rather than re-embedding on every change.

### 2. Anthropic, "Effective Context Engineering for AI Agents" (2025), §"Context retrieval and agentic search" (hybrid recommendation)
> "In certain settings, the most effective agents might employ a hybrid strategy, retrieving some data up front for speed, and pursuing further autonomous exploration at its discretion. … The hybrid strategy might be better suited for contexts with less dynamic content, such as legal or finance work."

**Relevance:** Anthropic explicitly names *finance and legal* as the domain where pre-indexed retrieval still earns its keep relative to pure agentic exploration. This is the closest the corpus comes to a recommendation for the AU banking case. Note the framing: "less dynamic content" — a claim that may not hold for fast-moving regulatory guidance and product-disclosure regimes; surface this for challenge.

### 3. Anthropic, "Effective Context Engineering for AI Agents" (2025), §"Why context engineering is important"
> "Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases. … LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount."

**Relevance:** Direct argument against the "just dump it all in the long context window" position. Even if a 1M-token window covers the regulatory corpus, recall degrades. Implies retrieval architecture matters even as windows grow — pertinent to the long-context-vs-RAG debate.

### 4. Anthropic, "How we built our multi-agent research system" (2025), §"Architecture overview"
> "Traditional approaches using Retrieval Augmented Generation (RAG) use static retrieval. That is, they fetch some set of chunks that are most similar to an input query and use these chunks to generate a response. In contrast, our architecture uses a multi-step search that dynamically finds relevant information, adapts to new findings, and analyzes results to formulate high-quality answers."

**Relevance:** Names static-RAG as a failure mode for open-ended, multi-faceted queries — exactly the shape of "what are the obligations under CPS 230 for a payments provider relying on a third-party cloud" type questions that span multiple instruments.

### 5. Anthropic, "How we built our multi-agent research system" (2025), §"Production reliability" + Appendix "Subagent output to filesystem"
> "Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator. This prevents information loss during multi-stage processing and reduces token overhead from copying large outputs through conversation history."

**Relevance:** The artifact-and-reference pattern is directly applicable to a regulatory KB: subagents retrieve, structure, and persist with citation; the lead agent operates on references not raw content. Also: the **CitationAgent** described in this essay (lead agent emits report → CitationAgent attaches source locations) is the canon's only direct treatment of provenance/citation as a first-class architectural concern.

### 6. Anthropic, "Building Effective Agents" (2024), §"Building blocks: The augmented LLM" and Appendix 2
> "The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. … one approach is through our recently released Model Context Protocol, which allows developers to integrate with a growing ecosystem of third-party tools."
> "One rule of thumb is to think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI)."

**Relevance:** Establishes the MCP-as-tool-surface frame and the ACI principle. For a banking KB designed for AI consumers, the implication is that the surface should be tool-shaped (typed, narrow, well-documented) rather than a generic "search this index" endpoint.

---

## Contradicting / complicating passages

### C1. Anthropic, "Effective Context Engineering for AI Agents" (2025), §"Context retrieval and agentic search" — directly contradicts the default "vector DB + RAG" mental model
> "This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand. … Claude Code is an agent that employs this hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees."

**Why this complicates the framing:** The default architectural reflex for "AI knowledge base" is *embed everything → vector store → similarity search*. Anthropic's stated position, working from production agents, is that **filesystem + grep + agent navigation** can outperform pre-built embedding indexes, particularly because it sidesteps the staleness/invalidation problem that haunts high-churn regulated domains. If true, the question for AU banking is not "what's the best vector store" but "what's the right structured surface (typed tools over canonical instruments) for the agent to navigate." This is a frame-level challenge to the question as posed.

### C2. Anthropic, "Effective Context Engineering for AI Agents" (2025), §"Context engineering for long-horizon tasks"
> "Waiting for larger context windows might seem like an obvious tactic. But it's likely that for the foreseeable future, context windows of all sizes will be subject to context pollution and information relevance concerns—at least for situations where the strongest agent performance is desired."

**Why this complicates:** Cuts against the "just use 1M-token Gemini / long-context Claude and skip retrieval" position. Even with abundant context, curation beats dumping. This complicates *both* the RAG-maximalist and long-context-maximalist positions.

### C3. Anthropic, "How we built our multi-agent research system" (2025), §"Benefits of a multi-agent system" (cost contradiction)
> "In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats. For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance."

**Why this complicates:** The multi-agent / agentic-retrieval architecture the same essay advocates is *expensive*. For high-volume, low-margin banking interactions (e.g., consumer chatbot answering a product-disclosure question), the economics may not support agentic search and a cheaper static-retrieval architecture might be correct on cost grounds even if it loses on quality. Surface this in the cost lane.

### C4. **Corpus silence as a contradicting finding**
The corpus contains **no passage** arguing that structured stores (relational, knowledge-graph, document DB with explicit schema) outperform embeddings on numerical or highly-structured content; **no passage** on GraphRAG; **no passage** on late-interaction retrievers like ColBERT. This is a real silence, not laziness — these positions exist in the broader literature (Microsoft Research GraphRAG 2024; Khattab & Zaharia ColBERT 2020/2022; numerous "structured-data-beats-RAG" arguments from Snowflake/Databricks blogs and from the Bloomberg GPT 2023 paper). Their absence means the orchestrator must treat the canon's voice on this question as *one-sided toward the Anthropic agentic-retrieval position*, and route to WebSearch for the contradicting literature.

---

## Stub / fetch-blocked entries that would be on-topic if ingested

- **Helland, "Life Beyond Distributed Transactions" (2007)** — `body_completeness: stub`. Directly relevant to the freshness/invalidation problem (entities, eventual consistency across systems of record) but body not ingested; canon contains only the citation. Do not invent quotes. Populate via `bin/ingest-owned-book.mjs` against the UCI PDF mirror to make this retrievable.
- **Hohpe & Woolf, "Enterprise Integration Patterns" (2003)** — `body_completeness: stub`. Correlation Identifier, Aggregator, Scatter-Gather patterns underlie any "agent fans out to N regulatory sources and reassembles" architecture, but body not ingested.
- **Evans, "Domain-Driven Design" (2003)** — `body_completeness: stub`. Bounded Context and Anti-Corruption Layer are highly relevant to "wrap each banking system-of-record in a typed surface for the agent" but body not ingested.

---

## Gaps the canon does not answer (route to WebSearch downstream)

1. **Contextual retrieval (Anthropic, Sep 2024).** Not in corpus despite being an Anthropic publication. Likely relevant; ingest candidate.
2. **GraphRAG (Microsoft Research, 2024).** Knowledge-graph-augmented retrieval; absent.
3. **Hybrid retrieval / reranking** (BM25+dense, Cohere/Voyage rerankers, Reciprocal Rank Fusion). Absent.
4. **ColBERT / late-interaction retrievers** (Khattab & Zaharia). Absent.
5. **BloombergGPT (2023) and domain-specific stacks.** Absent. Relevant for the "should we fine-tune / continue-pretrain on AU banking corpus vs. retrieve" decision.
6. **Regulatory-document ingestion at scale** (XBRL, Akoma Ntoso, structured legislation feeds). The corpus is silent; AU-specific (Federal Register of Legislation API, APRA register, ASIC) entirely outside canon.
7. **KB freshness / invalidation as a research topic.** Helland is the closest framework but is a stub. No on-topic passage on cache invalidation for RAG indexes, drift detection, or change-data-capture into vector stores.
8. **Information architecture for AI consumers vs. humans.** Anthropic's ACI principle is the only on-corpus voice; no counter-position (e.g., "build for humans, agents will adapt").

---

## One-line summary for the orchestrator
The canon speaks with one voice (Anthropic, 2024–2025) and that voice argues *against* static embedding-RAG as the default and *for* agent-navigated, tool-shaped retrieval with hybrid pre-indexed bootstrap — explicitly naming finance/legal as a hybrid-fit domain. The canon is silent on the contradicting literature (GraphRAG, ColBERT, structured-store arguments, BloombergGPT-style domain stacks); treat the canon view as one input, not as the field's consensus.
