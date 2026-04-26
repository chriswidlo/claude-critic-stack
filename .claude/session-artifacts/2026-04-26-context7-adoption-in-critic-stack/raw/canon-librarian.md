# Canon Librarian Report — Adding Context7 to claude-critic-stack

## Coverage

Partial. Strong on agent design (Anthropic's three engineering essays) and architectural boundaries (Cockburn). Weak/empty on trust-tier separation between retrieval sources and coupling between agents and external retrieval backends: evans-ddd (bounded contexts/ACL), hohpe-eip, nygard-release-it, vernon-strategic-monoliths are all stub entries with body_completeness:stub. Surfaced as gap markers; no fabricated quotes.

Nothing post-2025 on MCP server proliferation, "Skills" as Claude Code primitive, or version-pinned doc registries.

## Supporting passages

**S1. Anthropic, "Building effective agents" (Dec 2024), §Augmented LLM:**
> "The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. ... one approach is through our recently released Model Context Protocol, which allows developers to integrate with a growing ecosystem of third-party tools..."

Direct endorsement of MCP as canonical integration surface — supports B (tool on existing agents) or C (new subagent) over E (out-of-band Skill).

**S2. Anthropic, "Multi-agent research system" (Jun 2025), §Tool design:**
> "Using the right tool is efficient — often, it's strictly necessary. ... an agent searching the web for context that only exists in Slack is doomed from the start."

When canonical answer to "what does library X v4.2.1 export" lives outside corpus, agent that can only consult curated canon is structurally unable to answer; supports adding *some* live-docs surface.

**S3. Anthropic, "Effective context engineering" (Sep 2025), §Just-in-time retrieval:**
> "...agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."

Don't pre-ingest third-party docs (bloats canon, stales instantly); expose tool agent calls only when needed. Supports B/C; explicitly *against* D (corpus-refresher trigger), which flips back to pre-inference ingestion of fast-moving content.

**S4. Anthropic, "Effective context engineering" (Sep 2025), §Sub-agent architectures:**
> "Sub-agent architectures provide another way around context limitations. ... specialized sub-agents can handle focused tasks with clean context windows. ... Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary..."

If Context7 returns large doc chunks, separation-of-concerns favors C (dedicated subagent that consults Context7 and distills) over B (raw tool on every existing agent). Same architectural reason canon-librarian exists rather than canon access scattered.

**S5. Cockburn, "Hexagonal Architecture" (Jan 2005), §Nature of Solution:**
> "...A port identifies a purposeful conversation. There will typically be multiple adapters for any one port..."

Orchestrator's "purposeful conversation" with knowledge sources is one port (retrieval-of-claims-with-citations); canon-librarian is one adapter. Context7-backed adapter could plug same port — provided port contract (citations, distillation, anti-anchoring) honored. Supports adoption only under strict adapter contract; argues against bolting on with different return shape than canon retrieval.

## Contradicting passages

**C1. Anthropic, "Building effective agents" (Dec 2024), §When (and when not):**
> "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. ... It's about building the right system for your needs."

Default move when offered new retrieval source should be *don't add it*. Proposal must clear "what currently fails without Context7" bar, not "what becomes possible with Context7" bar. Capability-expansion alone fails this test.

**C2. Anthropic, "Effective context engineering" (Sep 2025), §Tool surface area:**
> "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

Direct strike at B — adding Context7 to existing agents creates two retrieval tools with overlapping-but-distinct trust models. Decision point "which one for question X" is exactly the ambiguity Anthropic warns against. Pushes toward C (subagent that internally knows when to consult) or E (Skill out-of-band, removes runtime decision from agent loop).

**C3. Anthropic, "Building effective agents" (Dec 2024), §Frameworks:**
> "These frameworks make it easy to get started ... However, they often create extra layers of abstraction that can obscure the underlying prompts and responses ... Incorrect assumptions about what's under the hood are a common source of customer error."

Context7 is itself framework-shaped third party — decides which docs you get, at what version, with what filtering. Canon corpus is auditable on disk; Context7's retrieval is not. If adopted, integration must preserve "what's under the hood" visibility (raw passages, source URLs, version pins). Weighs against E (Skills tend to be most opaque integration shape).

**C4. Anthropic, "Multi-agent research system" (Jun 2025), §Token cost:**
> "...agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats. For economic viability, multi-agent systems require tasks where the value of the task is high enough..."

New subagent (C) not free. If consulted on every design question (most not about library version), cost/value collapses. Whichever option chosen must include *gating predicate* (only fire when question names specific library and version), not unconditional invocation.

**C5. Anthropic, "Multi-agent research system" (Jun 2025), §Production reliability:**
> "...minor changes cascade into large behavioral changes ... Agents are stateful and errors compound."

New retrieval source changes behavior of every agent that can see it, non-locally. Frame-challenger and critic-panel tuned against current retrieval surface. B = highest-blast-radius option; C localizes change. Operations-lens argument for C over B, and for staged rollout regardless.

**C6. Cockburn (Jan 2005), §How Many Ports?:**
> "...My selection tends to favor a small number, two, three or four ports..."

Counterweight to "every new capability gets its own port/agent." If canon-librarian *is* the retrieval port, Context7 is arguably second adapter on same port — not new port. Maps to: Context7 sits *behind* librarian as second backend, librarian responsible for trust-tier labeling in returned passages.

## Cross-cutting

(a) Trust-model separation: Cockburn (S5/C6) port contract should label every passage with source/trust tier. Stub evans-ddd (ACL) and hohpe-eip would be canonical — not ingested.
(b) Coupling agents↔backends: S4 + S5 push toward *one agent owns backend, others see only distilled output*. C5 reinforces.
(c) Tool addition increasing vs. decreasing hallucination: no direct passage. C2 strongest indirect (ambiguous tool choice degrades reliability); S2 counter (missing right tool guarantees failure). Implied synthesis: tool *decreases* hallucination when answers question agent would otherwise guess at; *increases* anchoring when its output is privileged over conflicting curated material.
(d) Bounded contexts for agent capabilities: stub evans-ddd unavailable. Cockburn proxy: bound by purpose of conversation, not technology.
(e) Fewer vs. richer toolbelt: C1, C2, C6 all lean *fewer*. Richer-toolbelt argument implicit in S2 only, framed as necessity not enrichment.

## Gaps (declared per librarian rule)

1. No ingested text on bounded contexts/ACL (evans-ddd stub).
2. No ingested text on integration-pattern trust boundaries (hohpe-eip stub).
3. No ingested text on stability patterns for new third-party deps (nygard-release-it stub).
4. No corpus material on Claude Code "Skills" as integration primitive — option E cannot be evaluated against canonical guidance.
5. No corpus material specifically on version-pinned third-party doc registries.
6. No empirical study in corpus on "tool addition increases hallucination."
