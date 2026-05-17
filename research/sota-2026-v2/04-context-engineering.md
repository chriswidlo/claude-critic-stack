# Context Engineering — Canonical 2026 Reference

**Status:** Industry-standard discipline as of 2026.
**Scope:** Production AI workflows on any model family. Examples lean on the Claude stack because that is where the practice was first named in vendor documentation, but the primitives are model-agnostic.

---

## 1. The Reframing (2025–2026)

In September 2025 Anthropic published *Effective Context Engineering for AI Agents*, the post that retired "prompt engineering" as the senior term of art and replaced it with **context engineering**. The definition is worth quoting in full because every subsequent industry argument rests on it:

> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts." — Anthropic, *Effective Context Engineering for AI Agents*, Sept 2025

The post's framing of stakes is equally load-bearing:

> "LLMs, like humans, have a limited working memory capacity… they have an *attention budget* that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM."

Two consequences follow.

**Prompt engineering becomes a subset.** In the 2024 sense a prompt was a string: a system message plus a user message, human-written, static. By 2026 a prompt is an assembly: system message + tool definitions + streamed tool results + message history + mid-loop retrievals. Anthropic's post: prompt engineering is now "the *initial* effort of writing your prompts effectively," while context engineering is "the iterative, broader question of *what configuration of context is most likely to generate our model's desired behavior?*" The prompt is no longer a string. It is a runtime artifact, regenerated every turn.

**Context is a finite resource.** Per the same post: "context must be treated as a finite resource with diminishing marginal returns." The deepest break with 2024 practice, which assumed "context is free, stuff everything in." See §12 anti-patterns.

### The five components of context

Anthropic decomposes the assembled context into five independently managed surfaces:

1. **System prompt** — the role, the operating instructions, the invariants. Should use "simple, direct language." Stable across a session; cache-friendly.
2. **Tool definitions** — the JSON schemas the model sees for callable tools. Should have "minimal overlap in functionality." Each tool steals attention from real work (see §11 on the tool-description budget).
3. **Tool results** — what comes back from the environment when the agent calls a tool. Usually the single largest source of context bloat in an agent loop (see §5).
4. **Message history** — the running transcript of user and assistant turns plus prior tool calls. Grows monotonically until something is done about it.
5. **Retrieved / loaded documents** — RAG hits, file reads, pasted context, search results pulled in mid-task.

Each surface has its own caching characteristics, its own write/read cadence, its own failure mode. Treating them as a single bag is the most common mistake in 2024-era agent codebases.

---

## 2. Context Rot — The Empirical Problem

The reason context engineering became its own discipline is that *more context makes models worse, in measurable ways, well before the window fills up.*

### The benchmark evidence

The decisive empirical work landed in mid-2025 from two independent groups.

**Chroma Research, July 2025 — "Context Rot."** 18-LLM study (Anthropic, OpenAI, Google, Meta, xAI). Headline: "contrary to the assumption of uniform context processing, performance degrades significantly with longer inputs." Degradation appears on tasks trivial in isolation — semantic retrieval, repeated-word recall. A needle 100% recoverable at 1K tokens fell to chance-level at 100K on several frontier models. The frame: "Context rot is not context window overflow… A model with a 200K token window can exhibit significant degradation at 50K tokens."

**LMU Munich / Adobe Research, Feb 2025 — NoLiMa (Needles without Literal Matches).** Variant of needle-in-a-haystack where the needle is connected to the query by latent reasoning ("Kiasma is in Helsinki → which character lives in Finland?") rather than literal lexical overlap. Two-step reasoning numbers at 32K tokens:

- GPT-4o: 99% (short) → 70% (32K)
- Claude 3.5 Sonnet: 88% → 30%
- Gemini 2.5 Flash: 94% → 48%
- Llama 4 Scout: 82% → 22%

Three-step (character location + state association) collapsed further across the board.

**MRCR v2 at 1M tokens.** The current frontier benchmark. Opus 4.6: 76% in early 2026, a fourfold improvement over Sonnet 4.5's 18.5% — still a one-in-four failure rate. Opus 4.7 (Q2 2026): 89% single-needle, 56% 8-needle. Even the best frontier model loses nearly half its multi-needle recall once eight independent facts must be tracked through 1M tokens.

### The "effective" window vs the nominal window

The 2026 working consensus, drawn from the Chroma study and corroborated by production reports from Inkeep, Morph, and Anthropic's own cookbook:

- **Nominal window:** what the model card says (200K, 1M).
- **Effective window for single-needle:** ~70–80% of nominal on frontier models.
- **Effective window for multi-needle production work:** 200K–400K tokens on Opus-class models, less on smaller models. Past that, accuracy on multi-fact reasoning falls below thresholds most production systems can tolerate.

Treat the 1M window as a *capacity* number, not a *quality* number.

### Lost in the middle

Liu et al. ("Lost in the Middle," 2023) established the recency/primacy effect: facts placed at the beginning or end of the context are recovered far more reliably than facts in the middle. The 2025–2026 work confirms the effect persists in frontier models despite training improvements. Operational corollary: load-bearing content goes at the top or the bottom of the context, never in the middle.

### Why per-token signal degrades — the architectural intuition

Self-attention is a softmax over *n²* pairwise scores; a fixed probability mass is distributed across all of them. Adding tokens does not buy attention, it dilutes it. FlashAttention and friends reduce *compute*, not *dilution*. Context rot is a property of attention itself, not a bug in any specific model.

---

## 3. The Three Primitives

Anthropic's Sept 2025 post names three primitives for long-horizon agents. They are not optional; an agent loop that omits all three will hit context rot before it finishes any non-trivial task.

### 3.1 Compaction

Take the running message history when it nears the window limit, summarize it, reinitialize a new context window with the summary in place of the raw transcript. Continue.

The Claude SDK exposes this as `compact_20260112`, configurable with a trigger threshold (minimum 50K input tokens), an `instructions` field that lets the application specify what the summarizer must preserve, and an output `compaction` content block that replaces prior messages.

**Preserve:** decisions made, constraints stated, names of entities and files, anomalies encountered, quantitative figures with units, unresolved questions.
**Drop:** re-fetchable file contents, search-result bodies, raw command outputs, verbose tool returns, intermediate scratch reasoning.

Cookbook example: a research agent's 1M-token run that would peak at 335K is held to 169K peak with compaction enabled. Same task, half the working set.

Claude Code adds the `PreCompact` hook (live 2026; `PostCompact` requested, not GA) for intervention before the summarizer runs — typically used to inject "preserve verbatim" markers around load-bearing fragments.

### 3.2 Structured note-taking

The agent's external memory, written to disk in artifacts the agent itself can re-read on later turns. Distinct from compaction: compaction summarizes *the conversation*; note-taking emits *findings*. One artifact per phase, named for the phase: `requirement.md`, `frame.md`, `distillations/canon-librarian.md`, `scope-map.md`, `challenges.md`, `synthesis.md`, `ledger.md`. This is the pattern this very repository uses — and it generalizes.

The discipline: distillations beat raw dumps. After a subagent returns 8K tokens of search results, write a 1K-token distillation; the orchestrator reads only the distillation thereafter. Reading raw subagent output after distillation re-anchors the orchestrator to the noise the distillation removed.

Cline's "memory bank" pattern is the same idea named differently: a structured set of project-scoped markdown files (`projectbrief.md`, `activeContext.md`, `progress.md`, `systemPatterns.md`) the agent reads on every session bootstrap.

### 3.3 Sub-agent context isolation

Each sub-agent runs in a fresh context window, inheriting nothing from the orchestrator beyond what the orchestrator hands it explicitly. The sub-agent does its verbose work — reads twelve files, runs the test suite, scrapes a log — and returns a compressed result. The orchestrator's context absorbs only the return.

Claude Code is the canonical implementation: Task-tool spawn, fresh window per spawn, ~10 in parallel. Anthropic's recommendation: "verbose operations — test runs, log scrapes, doc fetches, big file reads — belong inside sub-agents." The point is context hygiene for accuracy, not just parallel speed. A 40K-token test run should never touch the orchestrator's window.

---

## 4. Tool-Result Handling

In any non-trivial agent loop, tool results are the largest single source of context bloat. A file read returns a file. A search returns hits. A shell command returns its stdout. Multiply that by twenty turns and the window is gone.

Four patterns, in rough order of how aggressively to apply them:

**1. Just-in-time retrieval over pre-loading.** Pass lightweight identifiers — paths, query handles, URLs, IDs — and let the model resolve on demand. The 2026 default. Pre-loading every potentially relevant document "in case the model needs it" is the pre-2024 anti-pattern. A 30-file repo dump costs ~150K tokens; the agent typically needs three of those files, costing ~15K on demand.

**2. Cap at write time.** Bound every tool return at the implementation layer. A `bash` tool piped through `head -c 50000` cannot blow the window. A search tool returning top-N snippets, not full docs, cannot blow the window. Property of the tool, not of the agent.

**3. Lift-and-summarize on read.** When a large result is genuinely needed, do not put the raw blob on the message bus. Pipe through a summarizer; put the summary on the bus; keep the raw in a side cache, reachable by ID.

**4. Clear when stale.** Claude's `clear_tool_uses_20250919` walks the message list and replaces old `tool_result` blocks with `"[cleared to save context]"` while keeping the `tool_use` record (the model still knows the call happened). Server-side, no inference cost. Configure `keep` (most-recent N preserved) and `clear_at_least` (minimum tokens cleared, so cache invalidation is worth the rewrite).

### Tool results as a safety surface

Tool results are also an attack surface. 2026 convention: **wrap every external tool result in an untrusted-content envelope** (`<tool_result_untrusted>…</tool_result_untrusted>` or equivalent) so the model treats it as data, not as user instructions. Length-bounding compounds the defense: a prompt-injection attacker controlling a fetched page needs setup tokens to build a convincing payload; a hard 4K cap denies the room. Both are context-engineering moves with safety payoffs.

---

## 5. File-as-Memory Pattern

The single most consequential pattern of 2026 production agent design: **on-disk markdown beats in-conversation state for any non-trivial workflow.**

The argument has three legs.

**Survives compaction.** A markdown file persists when the conversation summarizes. Decisions on disk are immune; the summarizer is imperfect even with good `instructions`.

**Survives the session.** Conversation is per-session; `progress.md` is per-project. Restart, fork, hand off, audit — the file is still there.

**Is grep-able.** The model reads a file in O(1) on its decision. Re-reading 200 turns of transcript is O(transcript). Files turn search into seek.

### Patterns within the pattern

**One artifact per phase.** Name the file for the phase, not for the content. `requirement.md`, `frame.md`, `scope-map.md`, `challenges.md`, `synthesis.md`. Predictable names mean the agent and the human both know where to look without index files.

**Consent-gated writes.** The agent proposes edits; the user — or an explicit workflow step — commits. The Claude Code edit-tool model generalizes. Auto-write agents drift; consent-gated agents are reviewable.

**Distillation, not dumps.** A phase artifact is the *output* of the phase, not the transcript. A 1.5K-token distillation is the context-engineering artifact; the 12K-token raw log is the audit artifact. Keep both, read different ones.

**Cross-session persistence.** Memory tools (Claude's `memory_20250818`, Cline's memory-bank, agent-SDK file-backed memory) extend the pattern across sessions. Same discipline: structured, phase-named, distilled.

Anthropic's *Building Effective Agents* (Dec 2024) and *Effective Context Engineering* (Sept 2025) both name file-backed state as the recommended pattern. By 2026 agents that omit it are visibly worse on multi-hour tasks.

---

## 6. The Split-and-Merge Pattern

Claude Code supports up to ~10 parallel sub-agents (practical ceiling — beyond that, coordination overhead negates the speedup). The pattern: when work decomposes into genuinely independent subtasks, dispatch them in one parallel batch and merge the returns.

**When parallelism pays:** six 30-second tasks finish in 30 seconds wall-clock, each in an isolated window, the orchestrator absorbs only the returns. Canonical cases: analyses across files that do not share state, retrievals across distinct corpora, lens-based reviews (a three-lens critic panel), independent web fetches.

**When it does not pay:** shared mutable state, sequential dependencies, tasks that need to negotiate. Fan-out costs tokens; if the merge requires more than concatenation, you have bought parallel inference and serial wall-clock.

Heuristic: parallelize when the merge is *append*; serialize when the merge is *compare* or *resolve*.

---

## 7. Compaction in Claude Code Specifically

Claude Code 2026 exposes two hook events around compaction. Their semantics are load-bearing for any production agent that runs past the conversation-window threshold.

**`PreCompact`** — fires *before* the summarizer runs. Used to:

- Inject "preserve verbatim" directives around identity / persona / governance fragments.
- Snapshot the full pre-compaction conversation to disk (recoverable audit trail).
- Re-emit load-bearing facts as a fresh user message so the summarizer treats them as recent rather than mid-transcript.

**`PostCompact`** — fires *after* compaction. Not yet GA as of mid-2026 (open feature request, multiple workarounds in the community). When available, the intended use is to:

- Re-bootstrap session-level constants (project name, conventions, current branch).
- Verify identity-structural markers survived the summarization (three signals in the community implementations: ALIVE / WEAK / SILENT).
- Re-load the agent's working `memory.md` so post-compaction reasoning has the same anchor as pre-compaction reasoning.

The 2026 best practice given the hook gap: **keep important decisions on disk; treat the transcript as a scratchpad that compaction will summarize lossily.** A decision in chat will be paraphrased away. A decision in `decisions.md` survives arbitrary compactions.

---

## 8. Prompt Caching as Context Engineering

Prompt caching is not just a cost optimization. It is a context-engineering primitive: it makes the cost of putting large stable content in context near-zero, which changes what is rational to put in context.

### The economics

Anthropic's pricing as of mid-2026:

- **Cache write:** 1.25× base input rate (5-minute TTL) or 2× base (1-hour TTL).
- **Cache read:** 0.1× base input rate — a 90% discount.
- **Break-even:** roughly two cached calls; from the third onward it is pure savings.

Worked example on Sonnet 4.6 at $3/MTok: a 100K-token cached prefix costs $0.30 per read after the first write. Without caching, every call costs $300 per million tokens of input.

### The four-breakpoint layering

The standard cache layout for an agent stack, ordered from most-stable to least-stable:

1. **Tool definitions** — change only on tool-set evolution. Cache the whole block.
2. **System prompt** — changes on agent revision. Cache after.
3. **Static context** (large pasted docs, retrieved corpora, project documentation) — changes on context refresh. Cache after.
4. **Conversation tail** — changes every turn. Do not cache.

Four `cache_control` breakpoints, in that order. The Claude API attaches each breakpoint to the last cacheable block at or before its position; misplacement means silent cache miss.

### Cache hit rate as a primary observability metric

Track cache hit rate the way you track p95 latency. The Anthropic SDK's usage object exposes `cache_creation_input_tokens` and `cache_read_input_tokens` per response; compute hit rate as `cache_read / (cache_read + cache_creation + input)` over a rolling window.

A 2026 ProjectDiscovery report: moving dynamic content out of the cacheable prefix took hit rate from 7% to 74% in a single deployment — ~10× cost compression on the cached path. **Cache hit rate is a dashboard metric, not a debugging metric.**

### Why timestamps and request IDs silently kill cache hit rate

A system prompt containing `Current date: 2026-05-17 13:42:08` or `Request-ID: 8a7c…` generates a new prefix hash every request; every request misses cache; the dashboard says "caching enabled," the bill says "caching irrelevant." Fix: push all per-request content *after* the cache breakpoint, into the conversation tail.

### Adaptive thinking + caching interaction

Opus 4.6/4.7 with adaptive thinking emit thinking blocks that become part of assistant message history. Switching thinking mode mid-conversation invalidates the message-history cache. **Pin thinking mode for the life of a cacheable session.**

### Workspace isolation gotcha

As of Feb 2026, caches are isolated per organization *and* per workspace on Anthropic API and Azure. Dev and prod do not share cached prefixes. Verify which workspace your cache benchmarks run in.

---

## 9. Long Context — The 1M-Token Era

The 1M-token window (Sonnet 4/4.5/4.6, Opus 4.6/4.7 in beta) changes the RAG-vs-long-context calculation but does not retire RAG. The 2026 decision rubric:

**Long context wins when:**

- Corpus is small (≲300K tokens, comfortably ≲200K).
- Queries are diverse (no single recurring slice the agent always wants).
- Freshness matters (the corpus changes faster than an index rebuild).
- Citation provenance is optional (the model can quote, but pin-cite is not required).
- Cost-per-query is acceptable at long-context rates (input 2× standard above 200K, output 1.5×).

**RAG still wins when:**

- Corpus is large (millions of tokens, multi-doc enterprise, code-bases over their nominal cap).
- Cost-per-query matters (long-context premium pricing is real).
- Citation provenance is required (auditable retrieval surface, chunk IDs).
- Corpus updates need to be fast and incremental (re-index a doc, not re-cache the world).

**Hierarchical summarization** is the bridge: for a corpus in the 300K–1M-token range that needs frequent re-querying, summarize each document into a 1–2K-token brief, fit the briefs into context, let the agent request full documents on demand. This is the file-as-memory pattern applied to RAG.

### Contextual retrieval (Anthropic, Sept 2024)

Anthropic's Contextual Retrieval technique is the dominant 2026 RAG improvement. Mechanism: before embedding (or before BM25 indexing) each chunk, prepend a 50–100 token LLM-generated context string that situates the chunk in the source document.

Measured improvements (1 − recall@20, i.e., retrieval failure rate):

- Contextual Embeddings alone: 35% failure reduction (5.7% → 3.7%).
- Contextual Embeddings + Contextual BM25: **49% reduction** (5.7% → 2.9%).
- With reranking added on top: 67% reduction (5.7% → 1.9%).

Cost: ~$1.02 per million document tokens, using Haiku as the contextualizer with prompt caching on the source document. Effectively free at any production corpus scale.

Anthropic's stated cutover rule: **for knowledge bases under 200K tokens, skip RAG entirely.** Put the corpus in the prompt, cache it, query it. Caching reduces cost by ~90% and latency by >2×. Contextual retrieval applies above the 200K boundary.

### Document order matters

Liu et al. ("lost in the middle") still applies. Load-bearing content at the *start* or *end* of the context, never in the middle. When stuffing retrieved chunks into long context, rank by relevance and put the highest-ranked at the bottom (most-recent position) and second-highest at the top. Middle is the dead zone.

---

## 10. Agent Context Patterns

The patterns that compose into a working agent.

**Distillation discipline.** The orchestrator reads compressed summaries, never raw sub-agent output, after the distillation step. A 1K-token distillation of an 8K-token search result is not lossy; it is *signal-enriching*. Reading both re-anchors to the noise.

**Lazy context loading via identifiers.** Pass paths, URLs, query handles; resolve on demand. The pattern composes with caching: an identifier is one token; a resolved document is many. Defer until the model decides it actually needs the bytes.

**The tool-description budget.** Every tool definition in the system prompt costs tokens — typically 100–500 each, depending on schema complexity. A 30-tool agent spends 5K–15K tokens before the user types a word, and those tokens steal attention from the model's real work. The 2026 discipline: minimal viable tool set per agent. Specialized sub-agents with narrow tool sets beat one omniagent with a kitchen drawer. (Anthropic names "bloated tool sets that cover too much" as anti-pattern #1 in *Effective Context Engineering*.)

**Memory injection patterns.** `PreCompact` hooks that re-emit load-bearing facts as a recent user message preserve them across summarization because the summarizer weights recent turns more heavily than middle-of-transcript turns. The trick generalizes: when you need a fact to survive compaction, *make it recent*.

---

## 11. Common Failure Modes

The named anti-patterns of 2026, in rough order of how often they break production agents:

**Bloated tool sets.** Overlapping tools (`read_file` + `get_file_contents` + `cat_file`), tools the agent never calls, tools whose schemas are 800 tokens of nested Pydantic. Each steals attention; collectively they confuse routing. **Cut tools until removal is painful.**

**"Stuff everything in just in case."** The pre-2024 default. Past 50K on a frontier model, additional tokens *probably* make performance worse. Pre-loaded context not consulted is paid attention budget for zero return.

**Trusting LLM-self-reported context relevance.** Asking the model "is this document relevant?" is asking the fox to guard the henhouse. Measure retrieval against task success, not model self-report.

**Caching with mutable prefixes.** Timestamps, request IDs, debug toggles — anything varying per request sitting *before* the breakpoint. Cache appears enabled, silently never hits. Verify with `cache_read_input_tokens > 0` on a second identical call.

**Treating sub-agent returns as gospel.** A sub-agent in a fresh window has no context for the orchestrator's frame. Returns need a distillation pass that interprets them against that frame. Without it, the orchestrator inherits sub-agent framing errors invisibly.

**Compaction without artifact persistence.** Letting the transcript be the only state. Post-compaction, prior decisions have been paraphrased — sometimes correctly, sometimes not. Decisions on disk are immune.

**Long-context as a substitute for thinking.** Loading 800K tokens because "Opus can handle it" is not a strategy. Effective context for multi-needle reasoning is 200K–400K. Past that you pay for tokens the model is not really attending to.

---

## 12. Anti-Patterns Explicitly Named

The community-canonical short list of things not to do:

**"RAG everything."** Indexing every doc — onboarding HR pages, deprecated runbooks, README boilerplate — produces a corpus where boilerplate dominates retrieval. The top-20 hits are dominated by repeated stock phrases ("This document is intended for…"). Curate the corpus *before* embedding. Anthropic's contextual retrieval helps, but it cannot rescue a corpus that is 60% boilerplate.

**"Context is free."** Every token reads and writes against the attention budget. Every token costs (input pricing). Every token written into the prefix that changes per-request silently kills cache hit rate. The 2024 framing "tokens are cheap, just stuff it in" is the most damaging legacy assumption in the field.

**"Long context replaces all retrieval."** It does not. Middle-of-haystack still degrades. Multi-needle still degrades. Past ~300K tokens, retrieval (with provenance, with curation, with reranking) beats raw stuffing on virtually every quality metric.

**"One giant CLAUDE.md."** Past about 150 atomic instructions, frontier models follow only the first ones and pay degrading attention to the rest. Empirical reports from Inkeep, Cline, and the Claude Code community converge on this number. Sharded instructions (per-subagent prompts, per-skill loadouts) beat monolithic instructions.

**"Cache it once and forget."** Caches expire (5-min or 1-hour TTL). Caches invalidate on prefix change. Caches are workspace-scoped. A "cache hit rate" dashboard that is not measured in production is decorative.

---

## 13. Top 12 Context Engineering Practices

Ranked by leverage. Apply in order; each compounds with the prior.

1. **Adopt the file-as-memory pattern.** One artifact per phase, named for the phase, written by the agent under consent gates. Decisions live on disk, not in chat. Single biggest lever for any agent that runs more than a handful of turns.
2. **Bound every tool result at the tool layer.** Hard caps on read sizes, hard caps on stdout, top-N on search. The tool — not the agent — is responsible for not blowing the window.
3. **Use sub-agents for verbose work.** Test runs, log scrapes, large file reads, doc fetches go in fresh-window sub-agents. The orchestrator absorbs only the return.
4. **Layer prompt caching with four breakpoints.** Tools → system → static context → tail. Track `cache_read / (cache_read + cache_creation + input)` as a primary metric. Get to >70%.
5. **Cut the tool set.** Remove tools until removal is painful. Specialize sub-agents with narrow tool sets rather than building omniagents.
6. **Distill, then read only the distillation.** Subagent returns get a distillation pass; the orchestrator never re-reads the raw return. Same for compaction — the post-compaction summary is the new ground truth.
7. **Pass identifiers, resolve on demand.** Paths, URLs, query handles in the conversation; bytes only when the model decides it needs them. Defer cost.
8. **Use contextual retrieval for any RAG over 200K tokens.** Contextual Embeddings + Contextual BM25 + reranking. 67% reduction in retrieval failures, ~$1/MTok preprocessing.
9. **Wrap tool results in untrusted-content envelopes.** Safety + attention surface. Length-bound them to deny attackers room for elaborate setups.
10. **Configure compaction explicitly.** Set the trigger token threshold (typically 100K–200K). Set `instructions` that name what must survive ("preserve decisions, file names, quantitative figures with units"). Run `clear_tool_uses` first; let `compact` handle dialogue.
11. **Place load-bearing content at start or end of context, never middle.** Especially in long-context queries over retrieved chunks. Order matters.
12. **Pin a baseline context budget per agent role.** A debugger agent might get 50K of working budget; a research agent might get 300K. Treat the budget as a *design constraint*, the way memory is a design constraint in embedded systems. When the agent runs over, the answer is not "give it more budget" — the answer is to shed context.

---

## Sources

**Anthropic (industry-standard):**
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Sept 2025. The defining post.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Dec 2024. File-as-memory pattern origin.
- [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — Sept 2024. 49% / 67% retrieval-failure reductions.
- [Context Engineering: Memory, Compaction, and Tool Clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) — Claude cookbook, 2026. `compact_20260112`, `clear_tool_uses_20250919`, `memory_20250818` reference.
- [Hooks reference (Claude Code)](https://code.claude.com/docs/en/hooks) — `PreCompact` hook semantics.
- [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents) — sub-agent isolation model.

**Empirical / academic:**
- [Chroma Research — Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot) — July 2025. 18-model study; "rot before overflow" framing.
- LMU Munich / Adobe Research — [NoLiMa benchmark](https://arxiv.org/abs/2502.05167) — Feb 2025. Multi-step reasoning degradation numbers.
- Liu et al. — [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) — 2023. Recency/primacy effect.

**Production reports (industry-standard, not academic):**
- [Fighting Context Rot — Inkeep](https://inkeep.com/blog/fighting-context-rot) — practitioner synthesis.
- [Claude Code Subagents: How They Work — Morph](https://www.morphllm.com/claude-subagents) — sub-agent practice 2026.
- [How We Cut LLM Costs by 59% with Prompt Caching — ProjectDiscovery](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching) — 7% → 74% cache-hit-rate case study.
- [Claude Context Window 2026 — Morph](https://www.morphllm.com/claude-context-window) — current pricing, 1M beta details.
- [Claude Opus 4.6 Introduces Adaptive Reasoning and Context Compaction — InfoQ](https://www.infoq.com/news/2026/03/opus-4-6-context-compaction/) — MRCR v2 76% number.

**Academic-but-promising (not yet industry-standard):**
- Activation steering / context-conditioning research from Anthropic Interp team — promising work on directing attention without prompt-level changes, still pre-production as of mid-2026.
- "Context Compression via Learned Tokens" — emerging line of work on differentiable compaction. Not yet shipped in any production stack.
