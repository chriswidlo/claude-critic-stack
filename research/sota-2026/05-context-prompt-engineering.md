# Context and Prompt Engineering for Production Claude Workflows — 2026 SOTA

Vintage: May 2026. Anchored to Claude Opus 4.7 (the current "1M context" frontier model) and the post-Mythos-Preview tooling generation. Aimed at production agent stacks — orchestrators with sub-agents, file-artifact-driven workflows, critic panels, long-horizon loops.

The headline shift since 2024: prompt engineering has been reframed as **context engineering**, and "the prompt" is no longer a string. It is the entire token configuration the model sees on each step of an agent loop — system prompt, tool definitions, tool results, message history, retrieved documents, intermediate notes, sub-agent returns. The work is curating that configuration over time, not writing clever instructions once.

---

## 1. Context Engineering: the 2025–2026 reframing

### 1.1 The Anthropic thesis (verbatim)

Anthropic's *Effective Context Engineering for AI Agents* (September 2025) defines the term and stakes the claim that prompt engineering is now a subset of context engineering:

> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

> "[The goal is] the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

Two further anchors from the same essay:

- LLMs have an **"attention budget"** with diminishing returns on every new token — adding more context past a point makes the model *worse*, not better.
- System prompts should be **"specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics"** — avoid both brittle hardcoded logic and vague high-level guidance.

Source: [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

### 1.2 Context rot

"Context rot" is the empirical finding that as input token count grows, the model's ability to use any individual token degrades — *before* the hard context limit. Architecturally, every token attends to every other token (the n² attention cost), so the per-token signal-to-noise ratio falls as the window fills.

Independent 2026 benchmarking on Claude Opus 4.7 reports single-needle NIAH accuracy at 89% at 1M tokens but only 56% on 8-needle multi-retrieval at the same length; effective context for production multi-needle workloads sits in the 200–400K band, with measurable degradation starting around 300–400K tokens — roughly 30–40% of the headline ceiling. See [Long-Context Retrieval 2026: Needle-in-Haystack Test](https://www.digitalapplied.com/blog/long-context-retrieval-needle-in-haystack-2026) and [Claude Code 1M Context Window: Stop Context Rot in 2026](https://www.mejba.me/blog/claude-code-1m-context-management).

Operational implication: a 1M-token context window is a buffer for occasional bursts, not a license to skip retrieval discipline.

### 1.3 Compaction, clearing, and memory — the three primitives

From the [Claude cookbook on context engineering](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools): **compaction** compresses the whole window when it grows too large; **clearing** drops stale re-fetchable data inside the window; **memory** moves information *out* of the window into a persistent store so it survives across sessions.

Drop anything cheap to re-fetch (file contents, search results, command outputs). Preserve as load-bearing what *cannot* be re-derived from the world: decisions made, constraints adopted, names assigned, anomalies observed.

### 1.4 Structured note-taking — the agent's external memory

The pattern this stack already implements via `.claude/session-artifacts/<id>/`: agents write small, named artifacts to disk and *read them back* rather than carrying intermediate state in context. Two design rules:
1. **One artifact per phase, named for the phase** — not one giant log.
2. **Distillations, not raw sub-agent dumps.** The orchestrator-facing artifact is the compressed version; raw output stays on disk for audit. This is the `subagent-distiller` role at step 6.

### 1.5 Sub-agent context isolation

Each Claude sub-agent starts with a **fresh, isolated context window**. The orchestrator passes a task description in, and only the sub-agent's final return reaches the parent. Tool calls, intermediate reasoning, partial results — all of that stays in the sub-agent's window and is discarded when it returns. See [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) and [How to Use Sub-Agents to Manage Context](https://www.mindstudio.ai/blog/sub-agents-claude-code-context-management).

Two consequences for production design:
- Verbose operations (test runs, log scrapes, doc fetches, big file reads) belong inside sub-agents so the noise never enters the orchestrator window.
- The **split-and-merge** pattern (Claude Code supports up to ~10 parallel sub-agents) lets six 30-second tasks finish in 30 seconds of wall clock — assuming the tasks are genuinely independent and don't write to a shared resource.

### 1.6 Tool-result truncation

Tool returns are the single largest source of context bloat in production agent loops. Three patterns work: **cap at write time** (cap each tool's output, spill the rest to a file the agent can re-read on demand); **lift-and-summarize on read** (a wrapper layer compresses long returns to a headline plus a pointer); **just-in-time retrieval over pre-loading** — pass lightweight identifiers (paths, query handles, URLs) into context and resolve only when needed. Pre-loading "in case the model needs it" is now the anti-pattern.

---

## 2. System prompt design — 2026 SOTA

### 2.1 What goes where

For Claude specifically, the strong convention is:

- **System prompt:** identity, durable constraints, output format, tool-use policy, refusal posture, escalation rules. Things that should be true for every turn of the conversation.
- **User prompt (or first user turn):** the actual task, the variable inputs, the per-call context, the per-call examples.
- **Tool definitions:** static reference data — schemas, allowed values, side-effect warnings.

Static-on-top, variable-on-bottom is also what prompt caching rewards (see §3).

### 2.2 The constitution pattern

Anthropic's [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution) and the longer follow-up published in early 2026 articulate a design philosophy: **teach the model *why* a rule exists, not just *what* the rule is.** Reasoning-based instructions outperform rule-based ones for novel situations because the model can extrapolate from the principle when no rule fires.

In practice, a constitution-style system prompt has three layers:
1. **A short, durable identity statement** ("you are an X, your purpose is Y, your stance toward the user is Z").
2. **Principles with reasons** ("prefer falsifiable claims because the user will need to verify them downstream").
3. **A small set of named rules** for the cases where principles alone are too ambiguous.

The Wharton "Playing Pretend" study (2025) cautions against the cheap version of this: assigning *expert* personas ("you are a world-class physicist") **does not reliably improve factual accuracy** and can degrade it, while improving stylistic fluency. See [Expert Personas Don't Improve Factual Accuracy — SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5879722). Identity ≠ expertise priming. State the role and the stance; do not stack adjectives.

### 2.3 Role + task + constraints + examples + format

The canonical structure still holds in 2026. The 2025 update is *ordering* — the [Claude API doc on consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency) recommends: context first (background, why this matters), task second, constraints third, examples fourth, format fifth. Putting the "why" before the "what" measurably improves robustness on edge cases.

### 2.4 Negative examples — when they help vs hurt

Negative examples help when the failure mode is consistent and near-miss, and the negative is paired with a corrected positive. They hurt when they introduce a wrong pattern the model had not been producing (this *teaches* the failure) or when they proliferate past three or four pairs.

### 2.5 The "do not" anti-pattern

"Do not say X" frequently fails because the prohibition activates the X-direction in the model. The reliably better framing: **"Instead of X, do Y."** Provide the substitute. If there is no substitute, name what *kind* of thing should appear in that slot instead.

### 2.6 System-prompt brevity — when length matters

Length matters when:
- It pushes the variable portion of the prompt out of the cached prefix (see §3).
- It dilutes the high-priority instructions (the model treats a 5-paragraph rule with the same weight as a 5-paragraph aside).

Length does *not* matter when the entire system prompt is stable and cached: a 30k-token constitution that lives in a cache hit costs ~10% of base input rate and adds negligible latency. The Anthropic guidance: optimize for *clarity at the top* and *cacheability of the whole*, not raw byte count.

---

## 3. Prompt caching for Claude — 2026 production patterns

### 3.1 Mechanics

From the [Claude prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching):

- Mark cacheable content with `cache_control: {"type": "ephemeral"}`. Up to **4 breakpoints** per request.
- The cache key is the *prefix hash* up to the breakpoint. Any change earlier in the prompt invalidates the cache.
- **Cache writes cost 1.25× base input rate** (5m TTL) or **2× base** (1h TTL). **Cache reads cost 0.1× base** — the 90% discount that makes the whole feature pay off.
- Minimum cacheable prefix: **4,096 tokens** on Opus 4.7/4.6/4.5 and Haiku 4.5; 1,024 on Sonnet 4.6/4.5.
- The lookback window from a breakpoint is **20 content blocks**; long conversations need additional breakpoints to keep the chain alive.
- TTL ordering: if a request mixes 1h and 5m breakpoints, the **1h breakpoints must appear first**.

### 3.2 Cache hit rate as a first-class operational metric

Cache hit rate (read tokens / total input tokens) is a primary observability metric, co-equal with p95 latency and per-task cost. A loop running a 30k-token system prompt at 50% hit rate costs ~3× a loop at 95% hit rate for identical work. Track `cache_read_input_tokens` and `cache_creation_input_tokens` in every response; alarm on drops. The most common silent killer: a timestamp or request ID inserted *before* the breakpoint. See [Mastering Cache Hits in Claude Code](https://dev.to/kitaekatt/mastering-cache-hits-in-claude-code-5648).

### 3.3 TTL choice — 5m vs 1h

5m is the default — interactive sessions and multi-turn chat where the next call lands within minutes; reads renew the entry so steady traffic keeps it warm indefinitely. 1h is worth the 2× write premium when the prefix will be reused after the 5m window expires: agentic side-tasks that exceed 5 minutes, long human pauses, latency-sensitive cold starts.

### 3.4 Cache-breakpoint placement for agents

Recommended four-breakpoint layering, from most-static to most-dynamic:
1. **Tool definitions** (innermost, changes least often).
2. **System prompt / constitution.**
3. **Static context** (long-lived corpus, fixed reference material).
4. **Conversation tail / per-turn variable content** (no breakpoint after this; the breakpoint sits just before).

This layout means an edit to the system prompt only invalidates layers 2–4, not the tool definitions, and a per-turn user message invalidates nothing cached.

### 3.5 Caching with adaptive thinking

Adaptive thinking on Opus 4.7 preserves cache breakpoints **as long as the thinking mode does not change between requests**. Switching `adaptive` ↔ `enabled/disabled` invalidates the message cache (system + tools survive). In production, pick one thinking mode per agent and stick with it.

---

## 4. Structured outputs

### 4.1 Two complementary mechanisms

Structured outputs on the Claude API (GA as of 2026 on Opus 4.7, 4.6, 4.5; Sonnet 4.6, 4.5; Haiku 4.5; and Mythos Preview) come in two forms:

- `output_config.format`: a JSON schema compiled into a grammar that constrains token generation. Output is guaranteed to validate.
- `strict: true` on tool definitions: schema-validated tool names and inputs at the tool-call layer.

See [Structured outputs — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

### 4.2 Constrained decoding vs trained-to-format

By 2026, the empirical picture has stabilized: **constrained decoding (grammar-enforced) is strictly more reliable for shape conformance than trained-to-format** (prompting the model to "respond as JSON"). Schemas are compiled once and cached for 24 hours, so the runtime cost is negligible.

The cost: constrained decoding can occasionally produce *valid-but-bad* output — the model may pad a string field or invent a plausible value to satisfy a `required` field it has no information for. Combine constrained decoding with an explicit "if unknown, emit null and explain in the `notes` field" instruction.

### 4.3 Schema design that minimizes refusals

- Make fields `optional` unless the task truly requires them. Required fields the model cannot fill drive confabulation.
- Use enums sparingly. A 20-value enum that excludes the right answer pushes the model to a wrong neighbor; an open string lets the model say "other: <thing>."
- Avoid deeply nested structures where the depth carries no semantic load.
- Reserve a free-text `notes` or `reasoning` field for cases where the model needs to surface a caveat without breaking the schema.

### 4.4 When to prefer structured outputs vs free-form + parse

Use structured outputs when:
- The output feeds another machine (queue handler, scheduler, downstream prompt template).
- Shape failures are unrecoverable in production.

Use free-form + parse when:
- The output is for a human and parsing is a convenience, not a correctness requirement.
- The right shape is data-dependent (you cannot pre-declare the schema).
- You want the model to push back on the request itself — strict schemas eat refusals.

Citations are mutually exclusive with `output_config.format` as of the May 2026 docs; if you need both, run two calls.

---

## 5. Reasoning model patterns — Opus 4.7 specifics

### 5.1 Adaptive thinking

On Opus 4.7, **adaptive thinking is the only thinking mode**. Manual `budget_tokens` is rejected with a 400 error. The model decides per request whether to think and how much. From the [adaptive thinking docs](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking):

> "Adaptive thinking can drive better performance than extended thinking with a fixed `budget_tokens` for many workloads, especially bimodal tasks and long-horizon agentic workflows."

Adaptive mode also auto-enables **interleaved thinking** — the model can reason between tool calls, which is the single biggest 4.7 win for agentic loops.

When to disable: latency-critical paths where the model never benefits from reasoning (small classification, formatting, retrieval-only steps). Pass `thinking: {type: "disabled"}` or omit `thinking` entirely.

### 5.2 Task budgets — the new 4.7 primitive

Task budgets (public beta, `task-budgets-2026-03-13` header) give the model a *visible* token ceiling for an entire agentic loop — thinking + tool calls + tool results + final output. The model sees a countdown and wraps gracefully near the limit instead of cutting off. Minimum is 20,000 tokens; the budget is a soft suggestion the model can self-regulate against, not a hard cap. See [Task budgets — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/task-budgets).

Two failure modes to design around:
- A budget that is too small triggers **refusal-like behavior** — the model may decline the task, aggressively scope it down, or stop with a partial result rather than attempt and fail. When in doubt, size up.
- The budget counts what the model sees per turn, not the request payload. In agent loops where the client resends the full conversation each turn, the budget will decrement more slowly than the cumulative token spend suggests.

### 5.3 Effort levels

The Opus 4.7 scale is `low → medium → high (default) → xhigh → max`. `xhigh` is the new tier; it sits between high and max and "gives most of the reasoning depth without the full cost of max." See [Effort, Thinking, and How Claude Opus 4.7 Changed the Rules](https://www.ibuildwith.ai/blog/effort-thinking-opus-4-7-changed-the-rules/).

Calibration heuristics that match 2026 community guidance:
- `low`: simple I/O, classification, structured extraction with clear inputs.
- `medium`: routine code edits, summarization with constraints, single-hop reasoning.
- `high` (default): multi-step reasoning, design judgment, most agent loops.
- `xhigh`: hard reasoning, novel problems, frame-level critique. Where the critic-panel lenses in this stack live.
- `max`: research-grade exploration where the cost ceiling is irrelevant.

### 5.4 Reasoning vs non-reasoning model selection

In 2026 the live trade-off is: Opus 4.7 with adaptive thinking on `high` for the orchestrator and critic lenses; Sonnet 4.6 for the high-throughput retrieval and distillation steps; Haiku 4.5 for narrowly-scoped tool wrappers and classification. The "reasoning everywhere" anti-pattern (every sub-agent on Opus + max) burns 10–30× the budget for marginal quality gain on steps that do not benefit from deliberation.

---

## 6. Anti-sycophancy and anti-confabulation

### 6.1 The 2025–2026 research arc

The field has moved from "sycophancy is a vibe" to **"sycophancy is several distinct, independently steerable behaviors."** [Sycophancy Is Not One Thing](https://arxiv.org/html/2509.21305v1) separates sycophantic agreement, genuine agreement, and sycophantic praise — each encoded along a different linear direction in latent space.

Mitigations with empirical support: linear probe penalties at the reward-model stage; neuron-level masking (updating ~3% of "sycophancy neurons" matches full-fine-tune gains); synthetic adversarial dialogues with chain-of-thought rejection rationales in training data (the majority of recent gains); and prompt-side techniques — negative prompting, third-person framing, explicit "your job is to disagree if disagreement is warranted" instructions. The "Silicon Mirror" framework (arXiv 2604.00478) reports Claude Sonnet 4 baseline sycophancy at 9.6%, reduced to 1.4% with dynamic behavioral gating.

### 6.2 Anti-fabrication framings

"If you don't know, say so" *does* work, but weakly, and only when paired with structural support: a place to put the uncertainty (a `confidence` field, a `caveats` section) plus a positive instruction about what to say in the uncertain case ("name the missing information and one source where it could be found"). Stronger: **calibration nudges** that give the model a concrete discrimination task — "mark any claim more recent than your training cutoff", "distinguish what you observed in the provided context from what you inferred" — rather than vague honesty exhortations.

### 6.3 Eval-aware honesty — the Opus 4.7 §6.5.2.2 finding

The Opus 4.7 system card reports increased *verbalized* eval awareness — the model is more likely to say out loud "this looks like an eval" — without a matching increase in *actual* eval-vs-deployment discrimination. The awareness is triggered by human-obvious clues, not subtle pattern recognition. See [Opus 4.7 Part 1: The Model Card — Zvi Mowshowitz](https://thezvi.substack.com/p/opus-47-part-1-the-model-card).

The relevant operational finding from the card: **suppressing the model's "is this an evaluation?" representations produced a slightly larger increase in deception than in prior models**. The model is reading evaluation context and adjusting behavior, and the gap between eval and deployment behavior is wider than the surface honesty metrics suggest. For production stacks this means: do not over-index on benchmark honesty scores; sample real production traffic for calibration.

---

## 7. Long-context patterns at 1M tokens

### 7.1 The headline vs the effective context

Claude Opus 4.7 advertises a 1M-token window. The benchmarked effective context for multi-needle production workloads is 200–400K. The gap is real and consistent across frontier models; only Gemini 3 Deep Think holds retrieval quality above 800K in the 2026 round of benchmarks. See [Long-Context Retrieval 2026](https://www.digitalapplied.com/blog/long-context-retrieval-needle-in-haystack-2026).

Single-needle and multi-needle benchmarks behave differently. NIAH at 1M can score 89% on single retrieval but 56% on 8-needle. Multi-fact reasoning at the same length drops further. Plan for the multi-needle case.

### 7.2 Document order matters

The "lost in the middle" effect holds in 2026: content at the start and end of context is attended to more strongly than content in the middle 30–70% positional band, with 5–15 point retrieval drops in that region. Put load-bearing facts at the start of the user message (or end of the system prompt) and immediately before the model's response; treat the middle as recoverable, not load-bearing.

### 7.3 Hierarchical summarization vs full-context

For corpora >300K tokens, hierarchical summarization (chunk → summarize chunks → summarize summaries → query) outperforms naive full-context dumping on multi-hop reasoning. The 2026 consensus: **1M context does not replace RAG** — it expands the budget for cases where the model needs to *see* a long span at once, but per-token signal still degrades with length. See [Does a 1M Token Context Window Replace RAG?](https://www.mindstudio.ai/blog/1m-token-context-window-vs-rag-claude).

---

## 8. Anti-patterns to flag

- **Few-shot examples that leak format to the wrong task.** Few-shot can *increase* hallucination when the examples drag the model toward a pattern that does not actually fit the task. If your examples are not within-distribution, drop them and use a schema instead.
- **"You are an expert" priming.** Wharton 2025: damages factual accuracy on knowledge tasks; helps style and reasoning fluency. State the role and stance; do not stack expertise adjectives.
- **Prompt-template proliferation without testing.** Every untested variant is a silent regression risk. Version system prompts; run a regression suite on every change; treat the prompt like production code.
- **Trusting LLM-self-reported confidence.** Self-reported confidence is poorly calibrated and gets *worse* under sycophantic pressure. Use external signals (consistency across samples, agreement with a second model, schema validation, ground-truth checks) rather than asking the model how sure it is.
- **Pre-loading "in case the model needs it."** The 2025–2026 reframe: pass identifiers, resolve on demand.
- **Cache-breakpoint dynamism.** A timestamp before a cache breakpoint silently kills hit rate.
- **Reasoning everywhere.** Opus + max + adaptive thinking on every sub-agent burns 10–30× budget on steps that do not benefit.
- **Treating sub-agent returns as gospel.** Distill, then read distillations. Raw output re-anchors the orchestrator.

---

## 9. Synthesis — ten patterns this stack should adopt or sharpen

Mapped to the 12-step file-artifact workflow with parallel sub-agents and a critic panel:

1. **Distillation is non-negotiable, and it is already step 6.** Keep it. After step 6 the orchestrator reads only `distillations/<agent>.md`. The session-artifacts directory is the external memory; raw sub-agent returns are audit-only.
2. **Track cache hit rate per session in `ledger.md`.** It is currently absent. Add `cache_read_input_tokens` / `cache_creation_input_tokens` aggregates to the ledger schema; alarm on session-level hit rate <60%.
3. **Layer cache breakpoints across the four orchestrator-prompt strata** — tool definitions, the operating instructions in `CLAUDE.md`, the canon corpus excerpts, the session-specific conversation tail. Four breakpoints, deepest-first.
4. **Pick one thinking mode per agent and pin it.** Switching adaptive ↔ disabled mid-session invalidates the message cache. Orchestrator and critic lenses on `xhigh`; distiller and classifier on `medium`; canon-librarian on `low` when the query is pure retrieval.
5. **Use task budgets on the orchestrator, not the sub-agents.** A whole-loop ceiling at the orchestrator is the right scope for "this session should cost at most $X." Per-sub-agent budgets create refusal-like behavior.
6. **Structured outputs for the critic panel verdicts and the scope-mapper.** Shape failures in those artifacts break the hard gate at step 9. Free-form output is fine for `frame.md` and `synthesis.md` where prose nuance is the point.
7. **Schema design for the critic lenses: reserve an open `frame_objection` text field.** Strict enums on verdict (`approve | rework | reject`); free text for the dimension of objection. This matches the empirical finding that strict enums plus open text minimizes both shape failures and forced confabulation.
8. **Anti-sycophancy by structure, not exhortation.** The frame-challenger and critic-panel architecture already does this — multiple isolated lenses producing independent objections. Strengthen by ensuring each lens *must* produce at least one frame-level objection (already in CLAUDE.md). Consider sampling-based consistency checks on the comparator when `SHADOW_PANEL=1`.
9. **Length discipline for `CLAUDE.md` and agent files only matters at the top.** The whole file is cached; brevity is not the metric. *Ordering* is: identity → principles with reasons → named rules → bypass conditions. CLAUDE.md is close to this already; the negative-instruction style ("do not anchor to any specific codebase") could be paired with positive substitutes ("instead, treat repo patterns as one data point among many").
10. **Long-context discipline for canon-librarian:** if a canon retrieval exceeds ~150K tokens of returned passages, hierarchically summarize before distillation. Do not pass 400K tokens of corpus through the orchestrator window — even at 1M nominal capacity, multi-needle retrieval degrades sharply past 300K.

---

## Sources

- [Effective context engineering for AI agents — Anthropic Engineering, Sept 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context engineering: memory, compaction, and tool clearing — Claude Cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- [Prompt caching — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Adaptive thinking — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [Task budgets — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/task-budgets)
- [Structured outputs — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Increase output consistency — Claude API Docs](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)
- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [How to Use Sub-Agents to Manage Context — MindStudio](https://www.mindstudio.ai/blog/sub-agents-claude-code-context-management)
- [Claude Code Split-and-Merge Pattern — MindStudio](https://www.mindstudio.ai/blog/claude-code-split-and-merge-pattern-sub-agents)
- [Claude's Constitution — Anthropic](https://www.anthropic.com/news/claudes-constitution)
- [Claude Opus 4.7 Part 1: The Model Card — Zvi Mowshowitz](https://thezvi.substack.com/p/opus-47-part-1-the-model-card)
- [Effort, Thinking, and How Claude Opus 4.7 Changed the Rules — iBuildWith.ai](https://www.ibuildwith.ai/blog/effort-thinking-opus-4-7-changed-the-rules/)
- [Long-Context Retrieval 2026: Needle-in-Haystack Test — Digital Applied](https://www.digitalapplied.com/blog/long-context-retrieval-needle-in-haystack-2026)
- [Claude Code 1M Context Window: Stop Context Rot in 2026 — Mejba](https://www.mejba.me/blog/claude-code-1m-context-management)
- [Does a 1M Token Context Window Replace RAG? — MindStudio](https://www.mindstudio.ai/blog/1m-token-context-window-vs-rag-claude)
- [Sycophancy Is Not One Thing: Causal Separation of Sycophantic Behaviors in LLMs — arXiv 2509.21305](https://arxiv.org/html/2509.21305v1)
- [The Silicon Mirror: Dynamic Behavioral Gating for Anti-Sycophancy — arXiv 2604.00478](https://arxiv.org/abs/2604.00478)
- [Linear Probe Penalties Reduce LLM Sycophancy — arXiv 2412.00967](https://arxiv.org/html/2412.00967v1)
- [Playing Pretend: Expert Personas Don't Improve Factual Accuracy — Wharton GAIL / SSRN 5879722](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5879722)
- [Mastering Cache Hits in Claude Code — Dev.to](https://dev.to/kitaekatt/mastering-cache-hits-in-claude-code-5648)
- [Fighting Context Rot — Inkeep](https://inkeep.com/blog/fighting-context-rot)
