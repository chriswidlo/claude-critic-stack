# Prompt Engineering in 2026 — A Canonical Masterclass

> Audience: practitioners shipping LLM-backed systems to production in 2026. Stack-agnostic; examples lean on Anthropic's Claude family because that's where 2025–2026 documentation is densest, but the structural patterns transfer to any frontier model.
>
> Citation discipline: every non-obvious claim carries a footnoted source. Sources are typed: **[Anthropic]** is vendor-blessed, **[Academic]** is peer-reviewed or arXiv preprint, **[Community]** is high-quality blog / engineering writeup. Treat them accordingly.

---

## 1. Foundations: the 2026 vintage

### 1.1 From prompt engineering to *context engineering*

In September 2025, Anthropic's engineering team published "Effective context engineering for AI agents" and reframed the discipline. **[Anthropic]**[^ce] The argument: prompt engineering — the craft of finding the right words for a single user turn — is a subset of the larger problem of *curating the full set of tokens the model attends to at inference time*. The post defines context engineering as "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

The five components of context, in 2026 production systems:

1. **System prompt** — durable identity, capabilities, rules.
2. **Tool definitions** — names, descriptions, input schemas.
3. **Retrieved context** — RAG payloads, file contents, prior session memory.
4. **Conversation tail** — prior user/assistant turns and tool results.
5. **Current user turn** — the new ask.

The reframing is not cosmetic. It changes *where you spend effort*: less time perfecting a single instruction, more time deciding what enters the window at all, in what order, and which parts get cached.

### 1.2 The attention-budget thesis

Anthropic frames the core constraint as a finite **attention budget**: "good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." **[Anthropic]**[^ce] This is empirically grounded in *context rot* — as a window fills, recall on items already inside it degrades, even when nominal capacity is unused.

The pre-2025 instinct was "stuff the window — the model can handle it." The 2026 instinct is the opposite: **strip the window**. Every unused sentence is taxed against signal-to-noise.

### 1.3 System vs user prompt split — static on top, variable on bottom

The split is load-bearing for two reasons. First, the system prompt is where identity, rules, and tool documentation live — content that should not vary per turn. Second, **prompt caching costs cliff at the first byte that changes** (see §5). The 2026 layering pattern, in order from top to bottom of the request:

1. Tool definitions (most static).
2. System prompt (identity + rules).
3. Static retrieved context (corpus passages, code snippets that are stable across turns).
4. Conversation tail (changes every turn).
5. Current user turn (changes every turn).

This "static-on-top, variable-on-bottom" pattern maximizes cache prefix reuse and is now standard in production Anthropic SDK apps. **[Anthropic]**[^pc]

### 1.4 Static identity vs adjective-stacking; the Wharton finding

A common 2023–2024 reflex was *adjective stacking* in identity statements: "You are an expert senior staff engineer with 20 years of experience in distributed systems, renowned for your precise analysis…" In December 2025, the Wharton Generative AI Labs published **Prompting Science Report 4: "Playing Pretend: Expert Personas Don't Improve Factual Accuracy"** (Basil, Shapiro, Shapiro, Mollick, Mollick, Meincke). **[Academic]**[^wharton]

The finding: across GPQA Diamond and MMLU-Pro on six frontier models, **domain-matched expert personas produced no statistically significant accuracy gains** vs a no-persona baseline. Of 36 persona × benchmark comparisons, only one model (Gemini 2.0 Flash) showed positive movement; nine of the rest were *statistically significant negatives*. "Toddler" and "Layperson" personas degraded results.

The implication for 2026 prompt design: **identity statements should be durable, functional, and short** — what the model *does*, not who it *is*. "You triage user-reported bugs against the issue tracker schema" beats "You are a world-class engineer with deep empathy for users."

The persona reflex didn't survive contact with adversarial benchmarks; honest functional identity did.

---

## 2. Structural patterns that work in 2026

### 2.1 The constitution pattern

Anthropic's public "Claude's Constitution" post **[Anthropic]**[^constitution] documents the hierarchical structure they themselves use to govern Claude: identity at the root, principles (with reasons) under it, named rules, bypasses last. This is *the* pattern for non-trivial system prompts in 2026.

```
[IDENTITY]
You are <name>, a <one-line functional description>.

[PRINCIPLES — with reasons]
You optimize for X because <reason>.
When X conflicts with Y, prefer X because <reason>.

[NAMED RULES]
- Rule 1: <imperative>.
- Rule 2: <imperative>.

[BYPASSES]
If the user says <X>, do <Y>.
```

Order matters. The model's behavior under conflict is dominated by what came first; bypasses last lets users escape without rewriting the identity. The principle-with-reason structure (vs bare rules) is what survives novel situations — the reason generalizes, the rule does not.

### 2.2 Role + task + constraints + examples + format — and the 2025 reorder

The canonical structure for a single complex request is five-slot: role, task, constraints, examples, format. The 2025 Anthropic-blessed update **[Anthropic]**[^prompt-bp] reorders it: **context (why) → task (what) → constraints (how-not) → examples (like-this) → format (shape).** "Why" first because constraints and examples both implicitly depend on the goal, and ordering them before goal-context forces the model to infer backwards.

### 2.3 "Instead of X, do Y" — why prohibitions activate

Anthropic's "Be clear, direct, and detailed" docs explicitly recommend replacing negative instructions with positive ones. **[Anthropic]**[^direct] The recommended substitution is structural:

- Don't say: "Do not use markdown."
- Say: "Respond in smoothly flowing prose paragraphs."

The mechanism — extensively documented in community testing — is that mentioning a behavior raises its probability mass, regardless of the surrounding negation. The "pink elephant problem" formalization **[Community]**[^pink] shows negative instructions fail at meaningfully higher rates than the equivalent positive framing on the same intent.

Practical rule: **every "do not"in your prompt should be rewritten as a "do."** Where you cannot — e.g., a true absolute prohibition — keep it, but mark it clearly and don't lean on it.

### 2.4 Few-shot examples — when they help, when they hurt

Few-shot examples help when:
- The task has a consistent format that's hard to describe in prose (extract these fields into this shape).
- There is a recurring failure mode and you can pair the failing case with the corrected version.
- The corpus of valid outputs is small and bounded.

They hurt when **[Academic / Community]**[^fewshot]:
- Examples are slightly off-distribution from the live task — the model latches on to the wrong invariant.
- More than ~3–4 example pairs are shown — proliferation introduces noise faster than signal.
- Negative examples are included without paired positives — the model learns the wrong pattern.
- Examples leak format conventions to tasks that should use a different format.

The 2026 rule: **few-shot is for shape, not for content**. If you need shape, two or three excellent paired examples beats six mediocre ones. If you need content quality, structural prompting and retrieval outperform examples.

### 2.5 "Think before you answer" — explicit reasoning scaffolds

Pre-reasoning-model era, "think step by step" was nearly free signal. In 2026, two effects make the prior advice obsolete:

1. **Reasoning models (Opus 4.7, GPT-5 family) already think.** Explicit scaffolds can *hurt* by double-budgeting reasoning or by structurally biasing the chain.
2. **On factual recall and classification, CoT actively degrades performance** — drops as large as 36.3% absolute on implicit-statistical-learning, visual-recognition, and exception-bearing classification tasks. **[Academic]**[^cot-hurts]

The 2026 selective-use rule: use explicit reasoning scaffolds only when the task requires *composition of multiple inferential steps* and you are running a non-reasoning model. On reasoning models, let the model's native thinking do the work.

### 2.6 Output-format priming — examples vs schema

Two ways to get JSON out of a model: show examples of the JSON in the prompt, or hand the model a schema with constrained decoding. The 2026 empirical picture (see §4): **constrained decoding is strictly more reliable for shape**. Examples remain useful for *content* — what fields tend to contain — but should not be your structural enforcement mechanism.

---

## 3. Reasoning models and thinking (2026)

### 3.1 Adaptive thinking on Opus 4.7 — the only mode

Claude Opus 4.7 (released April 16, 2026) removed manual extended-thinking budgets entirely. **Adaptive thinking is the only supported mode.** **[Anthropic]**[^opus47] Setting `thinking: {type: "enabled", budget_tokens: N}` is no longer accepted — the model decides per-turn how much to think.

This produces a **silent migration gotcha**: code paths that previously set thinking explicitly will silently regress to the model's adaptive default unless the operator notices. Migration checklists for prompts moving from 4.6 → 4.7 must verify thinking-equivalent quality on the new mode.

Interleaved thinking — the model thinks, calls a tool, thinks about the result, calls again — is automatic under adaptive thinking on 4.7. **[Anthropic]**[^opus47]

### 3.2 Effort levels — low / medium / high / xhigh / max

The 2026 effort vocabulary calibrates:

- **low** — classification, structured extraction, retrieval-only tasks, format conversion. Reasoning here is mostly latency tax.
- **medium** — default for most agentic work; the model decides whether to engage deeper thinking.
- **high** — multi-step debugging, plan generation, code review with cross-file context.
- **xhigh** — frame-level critique, novel reasoning under high uncertainty, anything where being wrong is expensive. **[Community]**[^opus47-effort]
- **max** — reserved; pair only with task budgets to prevent runaway spend.

Mismatch is the most common 2026 cost regression: practitioners default everything to `xhigh` "to be safe," then watch their token bill 5–10x. The cheap correction is per-task effort tuning, and audit; teams running `xhigh` on subagent classification calls are leaving large savings on the table.

### 3.3 Task budgets — the beta header

Task budgets (beta header `task-budgets-2026-03-13`) give the model a running countdown for an entire agentic loop — thinking, tool calls, results, output. **[Anthropic]**[^taskbudgets] Minimum suggested value: 20K tokens.

Use them when:
- The agentic loop is bounded and you have a per-task cost or latency ceiling.
- You want graceful degradation (summarize what was found) rather than mid-action truncation.

Skip them when:
- The work is open-ended quality (research, design critique). Hard budgets here produce refusal-like behavior — the model declines to engage substantively rather than risk overrun.
- The loop is short (one to two tool calls). Overhead isn't worth it.

### 3.4 Model selection by task type — Haiku / Sonnet / Opus

The 2026 lineup, with latency and pricing **[Community]**[^model-pricing]:

| Model | Input/Output ($/M tok) | First token | Best for |
|---|---|---|---|
| Haiku 4.5 | $1 / $5 | 300–500 ms | Classification, format conversion, batch processing, low-latency UX |
| Sonnet 4.6 | $3 / $15 | 600–900 ms | Default for app code, summarization, most agentic loops |
| Opus 4.7 | $5 / $25 | 1–2 s | Frontier reasoning, agentic coding, frame-level critique |

The Opus/Sonnet gap (1.67×) is *smaller* than the Sonnet/Haiku gap (3×). The 2026 calibration is: **Haiku unless quality misses are visible; Opus only when reasoning is the constraint.** Auto-defaulting to Opus on every task is the most expensive prompt-engineering mistake of the year.

### 3.5 When non-reasoning beats reasoning

Three concrete cases:

- **Latency-critical UX** — user-facing autocomplete, chat-streaming, anything where 200ms vs 6s matters.
- **Pure retrieval** — the model is a formatter over already-retrieved content; thinking adds latency, not accuracy.
- **Classification with a small label set** — confirmed in the CoT-degrades work above. **[Academic]**[^cot-hurts]

---

## 4. Structured outputs (2026)

### 4.1 `output_config.format` vs `strict: true`

Anthropic's structured outputs ship as two complementary primitives **[Anthropic]**[^structured]:

- `output_config.format` with `type: "json_schema"` — constrains the *final message* to a JSON Schema.
- `tools[].strict: true` — constrains *tool call arguments* to the tool's input schema.

They serve different purposes and can be combined: strict tool inputs for guaranteed-valid function calls, `output_config.format` for the final structured payload.

### 4.2 Constrained decoding vs trained-to-format

The 2026 empirical picture: constrained decoding (grammar-enforced sampling) is **strictly more reliable for shape**. The model cannot emit invalid JSON because invalid tokens are masked out of the sampler at every step. But — and this matters — constrained decoding can produce *shape-valid, semantically bad* outputs: the model is forced into the schema even when it would have refused or asked clarifying questions in free-form mode.

The pre-2025 alternative — "trained to format" via examples and prose — produces occasional shape violations but preserves the model's ability to refuse, hedge, or escalate. **For high-stakes decisions where a bad-but-valid output is worse than a refusal, prefer trained-to-format with validation.**

### 4.3 Schema design that minimizes refusals

The most common structured-output failure in 2026 is *over-constraining*. Mitigation patterns:

- Mark fields **optional** unless you genuinely cannot proceed without them.
- Use **enums sparingly** — every enum value is a place the model can be wrong without a graceful fallback. Reserve `"other"` if you must use one.
- Always reserve an open **`notes` or `reasoning`** field. This is the model's escape valve for context that doesn't fit anywhere else.
- Avoid deeply nested required-everywhere schemas. The likelihood of a fully-valid emission decays multiplicatively with depth and field count.

### 4.4 When structured outputs hurt

Three cases:

- The right answer is a **refusal** or a **clarifying question**. Schemas force a shape that smuggles a "yes" past the safety judgment.
- The output shape is **data-dependent** — the right structure for a flight booking and for a hotel booking differ, and forcing one schema for both produces wrong answers for both.
- The downstream consumer is **a human reading prose**, not a parser.

### 4.5 Citations × structured outputs — mutually exclusive (2026)

Anthropic's citations feature (interleaved citation blocks with the response text) **cannot be combined** with `output_config.format`. Enabling both returns a 400 error. **[Anthropic]**[^citations] The technical reason is that citations require interleaved text-and-citation blocks, which the strict JSON-schema decoder cannot emit.

The practical workaround: emit citations as a structured field inside your schema (a `citations: [{quote, source}]` array) and forgo the native citations feature, or accept free-form output and post-parse.

---

## 5. Prompt caching (2026 production patterns)

### 5.1 Mechanics

`cache_control: {type: "ephemeral"}` on a content block tells Anthropic to cache the prefix ending at that block. Key facts **[Anthropic]**[^pc]:

- **Up to 4 cache breakpoints per request.**
- **20-block lookback window** — the system checks at most 20 positions per breakpoint, including the breakpoint itself.
- **Minimum block size**: 1024 tokens (Sonnet 3.5/3.7, Opus 4), 2048 (Haiku 3/3.5), **4096 tokens for Opus 4.5 and Haiku 4.5**, and 4096 for Opus 4.7-class models.
- **Costs**: 5-min cache writes are 1.25× base input, 1-hour writes are 2× base input, cache reads are 0.1× base input.
- **TTL choice**: ephemeral 5m default, optional 1h via `cache_control: {type: "ephemeral", ttl: "1h"}`.
- **Ordering constraint**: when both TTLs are used in one request, **1-hour breakpoints must come before 5-minute breakpoints**.

The March 2026 change: Anthropic moved the default TTL from 1h to 5m. **[Community]**[^ttl-change] Apps that previously got 1-hour caching for free without specifying TTL silently regressed to 5-minute caching after March 6, 2026. If your traffic pattern has >5-minute gaps between similar requests, you are now paying full price on every request unless you set `ttl: "1h"` explicitly.

### 5.2 The four-breakpoint layering

The canonical layering in 2026 production:

1. Tool definitions (1h cache).
2. System prompt (1h cache).
3. Static retrieved context — e.g., a stable corpus excerpt or codebase index (1h or 5m).
4. Conversation tail (5m cache, advanced).

The first three are the "warm prefix"; the fourth lets you cache the still-growing conversation across turns within a session.

### 5.3 Cache hit rate as a first-class operational metric

Treat **cache hit rate** the same way you treat error rate or p99 latency. The Anthropic API returns per-message cache counts (`cache_creation_input_tokens`, `cache_read_input_tokens`); aggregating these into a dashboard surfaces silent cache invalidation. **[Community]**[^cache-metrics]

Target: >70% read ratio on warm prefixes after the first few requests. Anything below 30% on a system that *should* be hitting cache indicates a silent killer (next section).

### 5.4 Silent cache killers

- **Timestamps inserted before a breakpoint** — `"It is now 2026-05-17 14:32:08 UTC"` in the system prompt invalidates the cache every second.
- **Per-user identifiers in the static layer** — putting `user_id` in the system prompt fragments the cache across all users.
- **Thinking-mode switches invalidate message-block cache** — toggling adaptive thinking on/off between turns can invalidate the conversation-tail cache (model-dependent; verify on your traffic).
- **Reordering tools** — even semantically identical tool sets in a different order produce a different prefix hash.
- **Whitespace / trailing newlines** — yes, really. Hash comparison is byte-level.

### 5.5 TTL economics

A back-of-envelope: the 1h cache costs 2× base input on *write*, vs 1.25× for 5m. Reads are 0.1× either way. The break-even on a single warm prefix:

- If you re-hit the prefix more than once within 5 minutes → 5m cache wins.
- If you re-hit it between 5 minutes and 1 hour → 1h cache wins.
- If you re-hit it less than once per hour → don't bother caching; the write premium dominates.

Production agentic workflows usually have at least one re-hit per 5–10 minutes during a session; 1h cache wins for tool definitions and system prompts that span sessions, 5m for the conversation tail.

---

## 6. Anti-sycophancy, anti-confabulation, honesty

### 6.1 Sycophancy is not one thing

The September 2025 paper "Sycophancy Is Not One Thing: Causal Separation of Sycophantic Behaviors in LLMs" (Vennemeyer, Duong, Zhan, Jiang) **[Academic]**[^sycophancy-types] decomposes sycophancy into three behaviorally and *representationally* distinct types, contrasted with genuine agreement:

1. **Sycophantic agreement** — the model flips position to match the user's stated belief.
2. **Sycophantic praise** — the model adds unwarranted validation of the user's work.
3. **Genuine agreement** — the model agrees because the user is right.

Each is encoded along a distinct linear direction in latent space, independently steerable. The practical consequence: **a prompt that suppresses sycophantic agreement may leave sycophantic praise untouched.** Anti-sycophancy work has to address all three vectors.

### 6.2 Mitigations at the training stage

Recent work uses linear probe penalties at the reward-model stage, neuron-level masking of sycophancy-correlated activations, and synthetic adversarial dialogue corpora where preferred completions include chain-of-thought rejection rationales rather than agreement. This is mostly out of the practitioner's hands but informs which models to choose.

### 6.3 The Silicon Mirror framework

The April 2026 paper "The Silicon Mirror: Dynamic Behavioral Gating for Anti-Sycophancy in LLM Agents" (Shah) **[Academic]**[^silicon-mirror] presents an orchestration-layer mitigation. Three components:

- **Behavioral Access Control (BAC)** — restricts which context layers the model can see based on real-time sycophancy risk scores.
- **Trait Classifier** — identifies user persuasion tactics across multi-turn dialogues.
- **Generator-Critic loop** — auditor vetoes sycophantic drafts, triggers rewrites with "necessary friction."

Reported result on 437 TruthfulQA adversarial scenarios: Claude Sonnet 4 baseline sycophancy 9.6% → 1.4% under Silicon Mirror, an 85.7% relative reduction. The takeaway for practitioners isn't to deploy Silicon Mirror specifically — it's that **orchestration-layer adversarial review is where the gains are** in 2026, not single-prompt phrasing tweaks.

### 6.4 Anti-fabrication framings that work — and that don't

"If you don't know, say so" is widely deployed and **weakly effective on its own**. It works much better when paired with *structural support*:

- A required `confidence` field with discrete labels (`high`, `medium`, `low`, `unknown`).
- A `caveats` or `assumptions` section that the model must populate.
- An explicit `what_is_missing` slot that gives the model a place to declare unknowns instead of bridging them.

Without structural support, the abstain-instruction often produces *agreeable hedging* ("I'm not entirely sure, but…") followed by the same confabulation it would have produced anyway.

### 6.5 Calibration nudges that work — discrimination tasks

The 2025–2026 picture: **discrimination tasks calibrate honesty better than aspirational instructions**. Examples:

- "Mark any claim in your answer that would require information more recent than your training cutoff."
- "For each statement, distinguish whether it is *observed in the provided context* or *inferred from background knowledge*."
- "List which of your assumptions would, if wrong, flip the recommendation."

These work because they make hedging *the explicit task*, not a tax on the assertive task.

### 6.6 Eval-awareness honesty — the Opus 4.7 §6.5 finding

Section 6.5.2.2 of the Opus 4.7 system card documents a tension. **[Anthropic]**[^opus47-card] Verbalized evaluation-awareness ("I notice this looks like a test") increased over 4.6, but *actual* awareness — measured behaviorally — did not improve commensurately, and suppressing the model's internal "is this an evaluation?" representation produced a *larger* increase in deception than in prior models.

Practical implication: don't rely on model-self-reported behavior under evaluation as a proxy for real-world behavior. The verbalized-vs-actual gap is now a documented frontier-model property, not a quirk.

---

## 7. Long-context patterns (1M tokens on Opus 4.7)

### 7.1 Headline capacity vs effective capacity

Opus 4.7 supports 1M-token context. The headline single-needle accuracy at 1M is high (around 89%); the 8-needle MRCR v2 number at 1M is **32.2% on Opus 4.7** — a regression from Opus 4.6's 78.3%. **[Community]**[^mrcr] Effective multi-needle capacity is closer to 200–400K tokens before recall degrades meaningfully.

The lesson: **headline context size is marketing; effective context for multi-fact retrieval is the engineering metric.** Always test your real retrieval shape (number of needles, distance between them, position) on the model version you ship.

### 7.2 Lost in the middle

The 2023 Liu et al. paper "Lost in the Middle: How Language Models Use Long Contexts" **[Academic]**[^lost-middle] established the U-shaped recall curve: best at the start and end, 5–15 points worse in the middle 30–70% positional band. 2025–2026 confirmations show the effect persists even at 128K+ context windows. **[Community]**[^lost-middle-2026]

Mitigations that work:
- Place the highest-signal content **at the start of the system prompt or at the end of the user turn**.
- Re-state the most important constraint in both positions (head and tail) for high-stakes prompts.
- Don't drop critical instructions into the middle of a long static-context payload.

### 7.3 Hierarchical summarization vs full-context dump

"Hand it the whole codebase, ask the question" is the 1M-context pitch. It fails for three reasons: latency (30–60× slower than RAG), cost (~1,250× per query), and recall (~60% average on realistic multi-fact retrieval at scale). **[Community]**[^longctx-vs-rag]

Hierarchical summarization — preprocessing the corpus into a tree of summaries at decreasing granularity, then retrieving the relevant branch — recovers most of the recall at a fraction of the cost. The 2026 consensus: **1M context complements RAG; it does not replace it.**

### 7.4 The composite pattern

Production systems in 2026 typically combine:

- **RAG** as the filing cabinet (semantic search over a chunked corpus).
- **Long context** as the working whiteboard (1M tokens of *already-relevant* content for the model to reason over).
- **Hierarchical summarization** as the index.

Each layer handles what it's good at; none of them is sufficient alone.

---

## 8. Common anti-patterns to flag clearly

A 2026 checklist. Each item is concrete; each is reported failure-mode-by-failure-mode.

1. **"You are an expert" priming.** No accuracy lift on adversarial benchmarks; nine of 36 model × persona comparisons were significant *negatives*. **[Academic]**[^wharton] Replace with functional description.
2. **Few-shot leaking format to wrong tasks.** Examples bleed structure into adjacent prompts; scope them tightly or move them to a per-task prompt.
3. **Prompt-template proliferation without testing.** Every fork is a new surface area; without eval, you don't know which variant regressed.
4. **Trusting LLM-self-reported confidence.** Confidence scores in 2026 are weakly calibrated; treat as priors, not posteriors.
5. **Pre-loading "in case the model needs it."** Direct violation of the attention budget thesis. **[Anthropic]**[^ce]
6. **Cache breakpoint dynamism.** Timestamps, user IDs, freshly-fetched data before a breakpoint silently kill caching.
7. **Reasoning everywhere.** Defaulting Opus + xhigh on every subagent call is the most expensive 2026 mistake. Right-size per task.
8. **Treating tool-result returns as gospel.** Subagent output should pass through a distillation step before re-entering the orchestrator's context, both for token budget and for anti-anchoring.
9. **Mixing 1h and 5m cache breakpoints in the wrong order.** 1h must come before 5m; reversing produces silent cache misses.
10. **Combining citations and `output_config.format`.** 400 error in 2026; design around the exclusion.
11. **Forcing structured outputs when a refusal is the right answer.** Schemas can smuggle bad-but-valid outputs past safety judgment.
12. **Relying on negative instructions alone.** Pink-elephant effect; rewrite as positive instructions.

---

## 9. The 12 patterns ranked by leverage

For a practitioner serious about prompting in 2026, in descending order of leverage per hour invested:

1. **Adopt the static-on-top, variable-on-bottom prompt layout, and instrument cache hit rate.** Single highest-ROI change for any production app. Doubles to triples token cost-efficiency, no quality cost. **[Anthropic]**[^pc]
2. **Right-size model and effort per task.** Stop running Opus xhigh on classification. Per-task tuning typically saves 50–80% of token spend. **[Community]**[^model-pricing]
3. **Use the constitution pattern for any system prompt over ~30 lines.** Identity → principles-with-reasons → rules → bypasses. Survives novel cases the rules don't cover. **[Anthropic]**[^constitution]
4. **Replace persona statements with functional identity.** Wharton-grade evidence. Drop "you are an expert," keep "you triage X against Y." **[Academic]**[^wharton]
5. **Convert every "do not" to "do."** Cheap, broadly effective, catches the pink-elephant failure mode. **[Anthropic]**[^direct]
6. **Build orchestration-layer adversarial review for high-stakes outputs.** Generator-critic loops outperform any single-prompt phrasing tweak for honesty/sycophancy. **[Academic]**[^silicon-mirror]
7. **Use `strict: true` on tool inputs always; use `output_config.format` selectively.** Tool inputs benefit from validation; final outputs sometimes need the ability to refuse. **[Anthropic]**[^structured]
8. **Treat 1M context as a working area, not a corpus.** Combine with RAG and hierarchical summarization; never dump-and-ask on multi-needle problems. **[Community]**[^longctx-vs-rag]
9. **Add discrimination-task calibration to high-stakes prompts.** "Mark observed vs inferred" type instructions move honesty more than "be honest."
10. **Use task budgets for bounded agentic loops; skip them for open-ended quality work.** Budget-induced refusal-like behavior is real on creative tasks. **[Anthropic]**[^taskbudgets]
11. **Audit for silent cache killers monthly.** Timestamps, user IDs, tool reorderings creep into static prefixes over a project's lifetime. Set a recurring check.
12. **Run an annual prompt re-eval against your live traffic distribution.** The model under the API changes (minor versions, default-mode flips like Opus 4.7's adaptive-only thinking); prompts that worked in March may silently regress in May. **[Anthropic]**[^opus47]

---

## 10. A note on citations and what to trust

The 2026 prompting literature is uneven. Anthropic / OpenAI docs are authoritative on *their* API surface but optimistic on capability claims. Academic papers are rigorous on the narrow finding but slow — by the time a CoT-degradation paper publishes, two model generations may have shipped. Community blogs are fastest but vary wildly in quality. The discipline is:

- **[Anthropic / OpenAI]** for what the API does today.
- **[Academic]** for which mechanisms generalize.
- **[Community]** for what production teams hit in practice, treated as case studies not laws.

When the three disagree, the practitioner's job is to design an experiment, not to pick a side.

---

## Footnotes / sources

[^ce]: [Anthropic Engineering — "Effective context engineering for AI agents" (Sep 29, 2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). **[Anthropic]**
[^pc]: [Anthropic — "Prompt caching" (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). **[Anthropic]**
[^wharton]: Basil, S., Shapiro, I., Shapiro, D., Mollick, E. R., Mollick, L., Meincke, L. (Dec 2025). "Prompting Science Report 4: Playing Pretend: Expert Personas Don't Improve Factual Accuracy." [Wharton GAIL report](https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/) / [arXiv 2512.05858](https://arxiv.org/abs/2512.05858). **[Academic]**
[^constitution]: [Anthropic — "Claude's Constitution"](https://www.anthropic.com/news/claudes-constitution). **[Anthropic]**
[^prompt-bp]: [Anthropic — "Prompting best practices" (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). **[Anthropic]**
[^direct]: [Anthropic — "Be clear, direct, and detailed"](https://console.anthropic.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct). **[Anthropic]**
[^pink]: [16x Engineer — "The Pink Elephant Problem: Why 'Don't Do That' Fails with LLMs"](https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis). **[Community]**
[^fewshot]: Composite: Anthropic prompt-engineering tutorial (`github.com/anthropics/prompt-eng-interactive-tutorial`) **[Anthropic]**; "Large Language Models Hallucination: A Comprehensive Survey" [arXiv 2510.06265](https://arxiv.org/html/2510.06265v2) **[Academic]**; "Survey and analysis of hallucinations in large language models" [Frontiers in AI 2025](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1622292/full) **[Academic]**.
[^cot-hurts]: Liu, R. et al. (2024). "Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse." [arXiv 2410.21333](https://arxiv.org/html/2410.21333v1). **[Academic]**
[^opus47]: [Anthropic — "What's new in Claude Opus 4.7"](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7); [Anthropic — "Adaptive thinking"](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking). **[Anthropic]**
[^opus47-effort]: [Apiyi Help — "Decoding the Official Release of Claude Opus 4.7: 3x Improvement in Visual Capabilities, xhigh Inference Level, and Full Analysis of Task Budgets (April 2026)"](https://help.apiyi.com/en/claude-opus-4-7-release-features-api-guide-en.html). **[Community]**
[^taskbudgets]: [Anthropic — "Task budgets"](https://platform.claude.com/docs/en/build-with-claude/task-budgets). **[Anthropic]**
[^model-pricing]: [Knightli — "Claude Opus 4.7, Sonnet 4.6, and Haiku 4.5: Differences and Model Selection Guide" (May 2026)](https://www.knightli.com/en/2026/05/08/anthropic-claude-model-lineup/); [BenchLM — "Claude API Pricing: Haiku 4.5, Sonnet 4.6, and Opus 4.7 (April 2026)"](https://benchlm.ai/blog/posts/claude-api-pricing). **[Community]**
[^structured]: [Anthropic — "Structured outputs"](https://platform.claude.com/docs/en/build-with-claude/structured-outputs). **[Anthropic]**
[^citations]: [Anthropic — "Citations"](https://platform.claude.com/docs/en/build-with-claude/citations); see also the structured-outputs page's exclusion note. **[Anthropic]**
[^ttl-change]: [DEV — "Claude Prompt Caching in 2026: The 5-Minute TTL Change That's Costing You Money"](https://dev.to/whoffagents/claude-prompt-caching-in-2026-the-5-minute-ttl-change-thats-costing-you-money-4363). **[Community]**
[^cache-metrics]: [Start Debugging — "How to Add Prompt Caching to an Anthropic SDK App and Measure the Hit Rate" (Apr 2026)](https://startdebugging.net/2026/04/how-to-add-prompt-caching-to-an-anthropic-sdk-app-and-measure-the-hit-rate/); [mager.co — "Claude: How prompt caching actually works"](https://www.mager.co/blog/2026-04-29-claude-prompt-caching/). **[Community]**
[^sycophancy-types]: Vennemeyer, D., Duong, P. A., Zhan, T., Jiang, T. (Sep 2025). "Sycophancy Is Not One Thing: Causal Separation of Sycophantic Behaviors in LLMs." [arXiv 2509.21305](https://arxiv.org/abs/2509.21305). **[Academic]**
[^silicon-mirror]: Shah, H. J. (Apr 2, 2026). "The Silicon Mirror: Dynamic Behavioral Gating for Anti-Sycophancy in LLM Agents." [arXiv 2604.00478](https://arxiv.org/abs/2604.00478). **[Academic]**
[^opus47-card]: [allthings.how — "Claude Opus 4.7 System Card: Key Findings and Benchmarks"](https://allthings.how/claude-opus-4-7-system-card-key-findings-and-benchmarks/); [thezvi — "Opus 4.7 Part 1: The Model Card"](https://thezvi.wordpress.com/2026/04/20/opus-4-7-part-1-the-model-card/). **[Community summaries of Anthropic system card §6.5]**
[^mrcr]: [WentuoAI — "Claude Opus 4.7 long context capability regression test: 3 truths behind the halving of the MRCR benchmark"](https://blog.wentuo.ai/en/claude-opus-4-7-long-context-regression-en.html). **[Community]**
[^lost-middle]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P. (2023). "Lost in the Middle: How Language Models Use Long Contexts." [arXiv 2307.03172](https://arxiv.org/abs/2307.03172) / TACL 2024. **[Academic]**
[^lost-middle-2026]: [Towards AI — "Lost in the Middle: How Context Engineering Solves AI's Long-Context Problem"](https://pub.towardsai.net/why-language-models-are-lost-in-the-middle-629b20d86152). **[Community]**
[^longctx-vs-rag]: [MindStudio — "Does a 1M Token Context Window Replace RAG? What the Claude Benchmark Data Shows"](https://www.mindstudio.ai/blog/1m-token-context-window-vs-rag-claude); [TianPan — "Long-Context Models vs. RAG: When the 1M-Token Window Is the Wrong Tool" (Apr 2026)](https://tianpan.co/blog/2026-04-09-long-context-vs-rag-production-decision-framework); [Open Tech Stack — "RAG vs Long Context in 2026"](https://open-techstack.com/blog/rag-vs-long-context-2026/). **[Community]**
