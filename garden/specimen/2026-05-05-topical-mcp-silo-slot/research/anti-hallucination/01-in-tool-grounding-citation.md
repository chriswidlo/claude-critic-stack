# In-Tool Grounding, Citation & Provenance Enforcement

_Researched 2026-06-01 - axis: in-tool grounding & citation_

This document covers anti-hallucination mechanisms that live **inside the retrieval tool / its response contract**, before the consuming model generates. The frame is a hybrid-RAG (dense + BM25 + rerank, contextual chunks) MCP server returning `{source_url, content}` chunks to a consuming AI agent. First instance: AU banking regulation, where citation accuracy is compliance-critical.

The central question for this axis: **what can the tool itself do — in its response shape and the platform features it rides on — to force the consumer to ground, cite, and abstain, rather than relying on a downstream prompt to ask nicely?**

---

## Table of Contents

1. [The core distinction: reference hallucination vs. unfaithful synthesis](#1-the-core-distinction)
2. [Vendor citation primitives: what each one actually guarantees](#2-vendor-citation-primitives)
   - 2.1 [Anthropic Citations API + search_result blocks](#21-anthropic)
   - 2.2 [Cohere grounded generation](#22-cohere)
   - 2.3 [OpenAI annotations](#23-openai)
   - 2.4 [Google Vertex AI grounding metadata](#24-vertex)
3. [Quote-then-answer / forced span attribution: does it reduce hallucination?](#3-quote-then-answer)
4. [Grounding & confidence metadata the tool should return](#4-grounding-metadata)
5. [Structured output / constrained generation tying claims to chunks](#5-structured-output)
6. [The "no answer found" contract](#6-no-answer-contract)
7. [Contrarian synthesis: where in-tool citation fails](#7-contrarian-synthesis)
8. [Verdict](#verdict)
9. [Sources](#sources)

---

## 1. The core distinction: reference hallucination vs. unfaithful synthesis <a name="1-the-core-distinction"></a>

Before any mechanism, fix the threat model. There are **two distinct failure modes** that get conflated, and most "citation" features only address the first:

1. **Reference hallucination** — the model invents a source, a URL, a section number, or a quote that does not exist in the corpus. This is the "ghost reference" / fabricated-citation problem.
2. **Unfaithful synthesis (citation unfaithfulness)** — the model cites a *real* span, but the claim it attaches to that span misrepresents, overgeneralizes, or even contradicts what the span says.

This distinction is the spine of the whole axis. The strongest 2025–2026 evidence shows that in-tool citation primitives largely **solve #1 and barely touch #2**:

- A 2025 study evaluating seven major LLMs across medical queries found that **between 50% and 90% of LLM responses are not fully supported by the sources they cite**, and in a substantial fraction of cases **the cited sources actively contradict the claims** they are referenced for ([arXiv 2605.06635, "Cited but Not Verified", 2026](https://arxiv.org/html/2605.06635v1)).
- "Citation architectures that prevent hallucinated references cannot prevent unfaithful statements — claims that misrepresent what the cited work actually says" (same source).
- The ICTIR 2025 paper "Correctness is not Faithfulness in RAG Attributions" formalizes this: **correctness** (does the cited doc support the statement, per an NLI model) is *necessary but insufficient* for **faithfulness** (did the model causally rely on the cited doc, rather than post-rationalizing a citation onto pre-existing parametric knowledge) ([Wallat et al., ICTIR 2025](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/wallat-2025-correctness.pdf); [arXiv 2412.18004](https://arxiv.org/pdf/2412.18004)).

**Implication for an in-tool design:** the tool can make reference hallucination *structurally impossible* (you cannot cite a span the tool did not return). It cannot, by itself, make synthesis faithful. Faithfulness requires either (a) span-locked deterministic quoting, or (b) a post-hoc verification stage — which is a separate axis but bounds what this axis can claim. Any verdict that says "citations solve hallucination" is wrong on the 2026 evidence.

---

## 2. Vendor citation primitives: what each one actually guarantees <a name="2-vendor-citation-primitives"></a>

### 2.1 Anthropic Citations API + `search_result` content blocks <a name="21-anthropic"></a>

This is the most directly relevant primitive for an MCP-server design, because Anthropic ships a content-block type **purpose-built for tool returns**.

**Mechanism.** The Citations feature chunks user-provided documents into sentences, passes them alongside the query, and Claude generates responses with citations pointing to the exact sentences/passages used ([Anthropic, "Introducing Citations", 2025-01-23](https://claude.com/blog/introducing-citations-api)). The pattern Simon Willison named **"Deterministic Quoting"**: the quoted `cited_text` is *guaranteed to be copied verbatim* from the supplied source and not lossily transformed by the model ([Simon Willison, 2025-01-24](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/)).

**The `search_result` block — the load-bearing primitive for RAG/MCP.** Anthropic later shipped `search_result` content blocks specifically so custom tools (i.e., an MCP server) can return source-attributed content and get "web-search-quality citations" ([Anthropic docs, "Search results"](https://platform.claude.com/docs/en/build-with-claude/search-results)). The response contract is exactly the `{source_url, content}` shape this project already targets:

```json
{
  "type": "search_result",
  "source": "https://example.com/article",   // Required: source URL or identifier
  "title": "Article Title",                    // Required
  "content": [                                 // Required: array of text blocks
    { "type": "text", "text": "..." }
  ],
  "citations": { "enabled": true }             // Opt-in; default OFF
}
```

When the consumer answers, each text block in its output carries a `citations` array of `search_result_location` objects:

| Field | Guarantee |
|-------|-----------|
| `cited_text` | Full verbatim text of the cited block(s); **equals `content[start_block_index:end_block_index]` joined**. Not counted toward output tokens. |
| `source` / `title` | Echoed from the original `search_result` — cannot be invented. |
| `search_result_index` | 0-based index into the `search_result` blocks the *tool returned*. |
| `start_block_index` / `end_block_index` | Slice of the `content` array. |

Three properties matter for compliance:

1. **The text block is the minimal citable unit.** Claude "cites whole blocks, not substrings within a block." To get sentence/clause-precision citations (essential for regulation, where a citation must point to the operative sub-clause), **you split chunks into smaller text blocks inside `content`** — the tool controls citation granularity by how it shapes the array.
2. **Citations are all-or-nothing per request** — mixing enabled/disabled `search_result` blocks is an error.
3. **Citations default OFF** — the tool must explicitly set `citations.enabled: true`.

**Measured impact (named adopters):**
- Anthropic internal evals: citation capability **increased recall accuracy by up to 15%** vs. custom prompt-based implementations.
- **Endex** (financial research agents): reduced source hallucinations and formatting errors **from ~10% to 0%**, with a **20% increase in references per response** ([Anthropic, 2025-01-23](https://claude.com/blog/introducing-citations-api)).
- **Thomson Reuters (CoCounsel)** — legal/tax synthesis citing primary sources; reported easier maintenance vs. their custom implementation (same source).

**Contrarian on Anthropic's primitive.** The "0% hallucination" figure is *reference* hallucination (Endex's own framing: "source hallucinations and formatting errors"). It says nothing about unfaithful synthesis. The deterministic-quoting guarantee is verbatim *copying* of the quote, not verbatim *fidelity of the claim* attached to it. A model can copy a real sentence and still write a surrounding claim that the sentence does not support — exactly the 50–90% failure mode from §1. Also note the recall figure is from a vendor's internal eval (an inaccessible-comparator anchor risk): the operator cannot independently reproduce "15% better than most custom implementations."

### 2.2 Cohere grounded generation <a name="22-cohere"></a>

Cohere's Chat endpoint (`command-a-03-2025`) is **trained to emit fine-grained citations out of the box** in RAG settings — "one citation for each specific span in the response." The `response.message.citations` object returns both the `sources` (which documents) and `start`/`end` spans (location of the supported claim *inside the reply*) ([Cohere docs, "Documents and Citations"](https://github.com/cohere-ai/cohere-developer-experience/blob/main/fern/pages/v2/text-generation/documents-and-citations.mdx); [Cohere RAG docs](https://docs.cohere.com/docs/retrieval-augmented-generation-rag)). Document-grounded chat mode "generates answers based only on provided documents, automatically filtering for relevance."

This is the closest competitor to Anthropic's primitive and arguably more granular (spans into the *reply*, not just whole source blocks). Contrarian: it is Cohere-model-locked; an MCP server that must serve any consuming agent cannot assume the consumer is a Cohere model.

### 2.3 OpenAI annotations <a name="23-openai"></a>

OpenAI's Responses API surfaces citations as **annotation objects** on output text:
- `url_citation` — URL, title, and **start/end character indices into the response** where the source was used.
- `file_citation` — references to uploaded files in file-search; note **file_search does not return the search-result content by default**, only the annotation ([OpenAI, "File search"](https://platform.openai.com/docs/guides/tools-file-search); [OpenAI Responses API reference](https://developers.openai.com/api/reference/resources/responses/methods/create)).

OpenAI's grounding story is strongest for its *own* web-search/file-search tools; there is no clean public equivalent of Anthropic's `search_result` "bring-your-own-RAG-chunk-and-get-verbatim-citations" block with a *guaranteed-verbatim* `cited_text`. Annotations give you offsets into the *answer*, which is weaker provenance than offsets into the *source*.

### 2.4 Google Vertex AI grounding metadata <a name="24-vertex"></a>

Vertex returns `GroundingMetadata` with `groundingChunks`, `groundingSupports`, and historically per-support **confidence scores in [0.0, 1.0]** ([Vertex AI `GroundingMetadata` reference](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1beta1/GroundingMetadata)).

**Critical 2025 regression — a cautionary tale for this axis.** For **Gemini 2.5 Pro / Flash and later, the confidence-score list is empty and should be ignored**; Google explicitly dropped per-support confidence scores ([Vertex docs](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1beta1/GroundingMetadata); [Google Developer Forums, 2025](https://discuss.google.dev/t/gemini-2-0-suddenly-drops-confidencescore-when-grounding-with-a-data-store/188575)). A frontier vendor shipped a model-level confidence signal, then **removed it** — strong evidence that *model-emitted* grounding-confidence is not stable enough to build a compliance gate on. This directly informs §4: prefer **retrieval-stage** confidence the tool owns over **generation-stage** confidence the consumer emits.

---

## 3. Quote-then-answer / forced span attribution: does it reduce hallucination? <a name="3-quote-then-answer"></a>

**The technique.** Require the model to *extract verbatim supporting quotes from the source first*, then condition its answer on those quotes — rather than answering and back-filling citations.

**Evidence it helps:**
- **"According-to" prompting** (directing the model to ground against observed text, à la "according to sources") improved grounding (QUIP score) across Wikipedia, PubMed, and the **U.S. legal tax code** — and often improved end-task accuracy too ([Weller et al., arXiv 2305.13252](https://arxiv.org/pdf/2305.13252)). Tax code is a near-neighbor to AU banking regulation.
- Anthropic's own guidance: for long documents, "asking Claude to extract word-for-word quotes first before performing its task grounds its responses... reducing hallucinations," and a verification pattern where the model "verifies each claim by finding a supporting quote after generating — if it can't find a quote, it must retract the claim" ([Anthropic, "Reduce hallucinations"](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)).
- **Fine-grained grounded citations** (FRONT) selects supporting quotes from retrieved sources *first*, then conditions generation on them, improving citation quality on the **ALCE benchmark** ([Huang et al., arXiv 2408.04568](https://arxiv.org/pdf/2408.04568)).
- The **ALCE** benchmark (Automatic LLMs' Citation Evaluation) is the standard harness here, scoring citation **precision/recall** via NLI entailment between the statement and the cited passage; attributed-QA systems with inline citations improve factuality *and* simplify human verification ([ACL 2025 attribution survey](https://aclanthology.org/2025.acl-long.837.pdf)).
- A 2026 medical-RAG study on **"citation-enforced prompting"** reports hallucination reduction ([MDPI Appl. Sci. 2026](https://www.mdpi.com/2076-3417/16/6/3013)).

**Contrarian — the failure mode this technique introduces:**
- Forcing quotes does not guarantee *causal* reliance. The "Correctness is not Faithfulness" line of work found that optimized models "often generate answers from internal knowledge and then perform **post-hoc citation** based on token-level similarities rather than genuine document reliance" ([arXiv 2412.18004](https://arxiv.org/pdf/2412.18004)). Quote-then-answer can degrade into *answer-then-find-a-plausible-quote* unless the quoting is structurally enforced (constrained decoding, §5) rather than prompted.
- **More citations ≠ better.** "Models generating more citations must aggregate information from a larger number of retrieved passages, increasing the likelihood of misattribution or conflation of facts" ([arXiv 2605.06635](https://arxiv.org/html/2605.06635v1)). Endex's "+20% references per response" cuts both ways.

**Net:** quote-first is a genuine, evidence-backed reducer of *reference* hallucination and a modest help on grounding, with the strongest results when the quote is *locked* (the model literally cannot emit a quote that isn't in the source). That locking is precisely what Anthropic's `cited_text` verbatim guarantee provides — the API-level version of quote-then-answer.

---

## 4. Grounding & confidence metadata the tool should return <a name="4-grounding-metadata"></a>

This is the heart of the in-tool axis: **what does the tool put alongside each chunk so the consumer can refuse or hedge?**

Design principle, derived from the Vertex regression (§2.4): **own the confidence at the retrieval stage; do not depend on the consumer's generation-stage confidence.** The tool is the only component that knows the retrieval scores; the consuming model's self-reported confidence is unreliable (AbstentionBench, §6).

Recommended per-chunk and per-response metadata:

**Per chunk:**
- `source_url` / `source_id` — stable, permanent identifier (Anthropic best practice: "clear, permanent source URLs").
- `title` — descriptive, accurate.
- `content` — split into **fine-grained text blocks** (sentence/sub-clause) so downstream `cited_text` boundaries are tight. This is the single most actionable lever for citation precision.
- `dense_score`, `bm25_score`, `rerank_score` — the three stages of the hybrid pipeline, surfaced separately.
- `provenance` — document version, effective date, jurisdiction, regulator, last-updated, supersession status. For AU banking reg, **version/effective-date is itself a correctness axis**: citing a superseded standard is a compliance defect even if the quote is verbatim.

**Per response (the abstention-enabling signals):**
- A **calibrated** top relevance signal. Cross-encoder rerankers produce scores "far more calibrated" than bi-encoder similarity, but **calibration is not free** — "some models require tuning thresholds" and you "should choose score thresholds using offline evaluation and monitor production" ([Ailog, "Reranking for RAG", 2025](https://app.ailog.fr/en/blog/guides/reranking)). Newer rerankers (e.g., zerank-2, ELO-trained) advertise out-of-the-box calibrated scores ([ZeroEntropy, 2025](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/)).
- A **`no_confident_match` boolean / `match_quality` enum** — computed by the tool from the top rerank score against an offline-tuned threshold. This is the signal the consumer keys its abstention on. **Do not return a bare float and hope the consumer interprets it** — return an explicit enum (`high` / `low` / `none`) plus the raw score.

**Contrarian on confidence metadata:** raw retrieval/rerank scores are **not probabilities** and not comparable across queries unless explicitly calibrated; a `rerank_score=0.6` means different things for different queries. Surfacing uncalibrated scores invites the consumer to invent its own (wrong) threshold. And Google's removal of confidence scores in Gemini 2.5+ is a standing warning that even vendors find generation-side confidence too unreliable to support. The mitigation: the tool computes the abstention decision itself (offline-calibrated threshold → enum), and treats the float as advisory.

---

## 5. Structured output / constrained generation tying claims to chunks <a name="5-structured-output"></a>

**State of the primitive.** Constrained decoding restricts allowable next tokens so output conforms to a JSON Schema / grammar. Industry timeline: OpenAI Structured Outputs (Aug 2024, `response_format: json_schema`), Gemini `response_schema` (May 2024), **Anthropic constrained decoding for Claude (Nov 2025)** ([G360 Technologies, 2025](https://g360technologies.com/structured-outputs-are-becoming-the-default-contract-for-llm-integrations/)). On **JSONSchemaBench** (10K real-world schemas), constrained decoding reaches empirical coverage up to **0.96** with robust compliance ([Geng et al., arXiv 2501.10868](https://arxiv.org/html/2501.10868v3)).

**How it helps grounding.** A schema can *require* every claim object to carry a `supporting_chunk_id` and `cited_span`, refusing to emit a claim with no attachment — "response formats that create checkpoints (each claim followed by evidence) force the model to map each assertion to a specific support span" ([Anthropic, "Reduce hallucinations"](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)). This is the structural enforcement that prevents quote-then-answer from degrading into post-hoc citation.

**Hard contrarian — the load-bearing limitation.** Constrained decoding can **guarantee the *shape* (every claim has a `chunk_id` field) but NOT the *truth* of the binding.** A schema can force the model to *write a chunk_id*; it cannot force that chunk to actually support the claim. The model can emit a syntactically perfect, schema-valid `{claim, chunk_id, span}` where the span does not entail the claim. Worse, some research shows over-constraining can *reduce* reasoning quality. So constrained output is necessary for machine-checkability but is **not** a faithfulness guarantee — it produces a verifiable artifact, and you still need a verifier (NLI/entailment, a separate axis) to check that `span ⊨ claim`. The one thing the tool *can* enforce structurally is **referential integrity**: reject any answer whose `chunk_id` is not in the set of returned chunks. That kills reference hallucination deterministically; it does nothing for unfaithful synthesis.

The cleanest combination, then, is: **Anthropic `search_result` blocks (verbatim `cited_text`, real source guaranteed) + constrained output requiring a returned-chunk id per claim (referential integrity) + downstream NLI verification (faithfulness).** The first two are in-tool/in-contract; the third is the next axis.

---

## 6. The "no answer found" contract <a name="6-no-answer-contract"></a>

The tool must give the consumer a **first-class way to learn there is no good evidence**, because the consumer will *not* reliably figure this out itself.

**Evidence the consumer can't be trusted to abstain unaided:**
- **AbstentionBench** (Meta, NeurIPS 2025): across 20 frontier LLMs and 20 datasets, "abstention is an unsolved problem, and scaling models is of little use." Most damning: **reasoning fine-tuning *degrades* abstention by 24% on average** — the more capable, "smarter" reasoning models are *worse* at knowing when to refuse ([Kirichenko et al., arXiv 2506.09038](https://arxiv.org/abs/2506.09038)). "A carefully crafted system prompt can boost abstention... but does not resolve models' fundamental inability to reason about uncertainty."
- Retrieval alone does not fix this: "models may still fill gaps with fabrications unless trained to prefer abstention over invention."

**Implication:** abstention must be **driven by a tool-emitted signal**, not left to the consumer's judgment. Concretely the tool should:

1. When the top calibrated rerank score is below the offline-tuned threshold, **return an explicit `no_confident_match` response** (status enum = `none`), not a low-scoring chunk dressed up as an answer. Returning weak chunks silently invites confabulation.
2. Make the empty/insufficient state **structurally distinct** from the answer state (a different response variant, not just an empty `content` array), so the consuming agent's contract can branch on it. Anthropic's own best-practice example returns an explicit `{"type":"text","text":"No results found."}` rather than an empty list ([Anthropic, "Search results"](https://platform.claude.com/docs/en/build-with-claude/search-results)).
3. Optionally degrade gracefully: return the best chunks *with* `match_quality: low` so the consumer can **hedge** ("I found related but not directly on-point material...") rather than binary refuse — Self-Aware RAG / R-Tuning teach exactly this "answer vs. abstain vs. hedge" trichotomy ([Trust or Abstain, arXiv 2605.18792](https://arxiv.org/html/2605.18792)).

**Contrarian:** abstention is a precision/recall tradeoff and over-abstention is a real cost — "rejecting too aggressively will tank recall" ([Ailog, 2025](https://app.ailog.fr/en/blog/guides/reranking)). In a compliance domain a missed-but-existing answer ("the rule does exist, you just didn't surface it") can be as harmful as a confabulation. The threshold is a tunable business decision, not a constant, and must be set by offline eval on a labeled AU-banking query set and monitored in production.

---

## 7. Contrarian synthesis: where in-tool citation fails <a name="7-contrarian-synthesis"></a>

Pulling the contrarian threads together, so the verdict is honest about its ceiling:

1. **Verbatim citation ≠ faithful claim.** The strongest single finding in the corpus: 50–90% of cited responses are not fully supported by their citations, and citations sometimes *contradict* the claim ([arXiv 2605.06635](https://arxiv.org/html/2605.06635v1)). In-tool primitives prevent fabricated references; they do not prevent unfaithful synthesis.
2. **Post-hoc citation masquerades as grounding.** Models answer from parametric memory then attach a plausible-looking quote; correctness metrics pass while faithfulness fails ([arXiv 2412.18004](https://arxiv.org/pdf/2412.18004)).
3. **Generation-side confidence is unstable** — Google removed it in Gemini 2.5+ ([Vertex docs](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1beta1/GroundingMetadata)). Don't anchor a compliance gate on the consumer's self-reported confidence.
4. **Structured output guarantees shape, not truth** ([arXiv 2501.10868](https://arxiv.org/html/2501.10868v3)). Schema validity is not entailment.
5. **Smarter consumers abstain *worse*** ([arXiv 2506.09038](https://arxiv.org/abs/2506.09038)). You cannot wait for a better model to fix this; the tool must own the abstain signal.
6. **Vendor numbers are inaccessible-comparator anchors.** The "+15% recall", "10%→0%", "+20% references" figures are vendor-internal and customer-self-reported; treat as directional, not as a reproducible benchmark.

The honest scope of this axis: **in-tool mechanisms make reference hallucination structurally impossible and make every claim machine-checkable. They do not, alone, guarantee faithfulness.** Faithfulness needs a verification axis on top.

---

## Verdict <a name="verdict"></a>

**The single SOTA set of in-tool grounding mechanisms for an MCP RAG server, mid-2026:**

1. **Return chunks as Anthropic `search_result` content blocks with `citations.enabled: true`.** This is the SOTA in-tool primitive for a `{source_url, content}` MCP server: it gives **guaranteed-verbatim `cited_text`** (deterministic quoting — reference hallucination becomes structurally impossible), source/title that cannot be invented, and source-relative block offsets. Proven adopters: Thomson Reuters CoCounsel (legal/tax), Endex (financial), with up to 15% recall improvement in vendor evals. It is also available on Bedrock and Vertex, so it is not single-cloud-locked. For provider-neutral consumers, mirror the same contract; for Cohere consumers, `command-a` grounded generation is the equivalent with finer reply-side spans.

2. **Control citation granularity by splitting `content` into sentence/sub-clause text blocks.** The text block is the minimal citable unit; for AU banking reg, citations must resolve to the operative sub-clause, so chunk fine. This is the in-tool implementation of quote-then-answer/span attribution, which the evidence (according-to prompting on tax code; FRONT on ALCE) supports as a real grounding reducer.

3. **Compute and return an explicit abstention signal, owned by the tool.** A calibrated cross-encoder rerank score → an offline-tuned threshold → a `match_quality` enum (`high` / `low` / `none`). When `none`, return a **structurally distinct `no_confident_match` response**, never a weak chunk silently. This is non-negotiable because frontier models — *especially* reasoning models — abstain unreliably on their own (AbstentionBench: −24%).

4. **Wrap the answer in a constrained-output schema that enforces referential integrity** — every claim object must carry a `chunk_id` drawn from the set of returned chunks; reject any answer citing a chunk the tool didn't return. This guarantees machine-checkability and kills the last residual reference-hallucination path.

**What to put in the tool's response contract:**

```jsonc
{
  "status": "answer | no_confident_match",      // structurally distinct states
  "match_quality": "high | low | none",         // tool-owned, offline-calibrated
  "results": [
    {
      "type": "search_result",
      "source": "<stable permanent URL/id>",
      "title": "<descriptive>",
      "content": [ { "type": "text", "text": "<sub-clause-sized block>" } ],
      "citations": { "enabled": true },
      "scores": { "dense": 0.0, "bm25": 0.0, "rerank": 0.0 },   // advisory
      "provenance": {
        "version": "...", "effective_date": "...",
        "jurisdiction": "AU", "regulator": "APRA|ASIC|...",
        "superseded": false
      }
    }
  ]
}
```

**The explicit ceiling (must be surfaced as an unresolved uncertainty):** these in-tool mechanisms eliminate fabricated references and make claims auditable, but they **do not guarantee faithful synthesis** — 50–90% of cited LLM responses are not fully supported by their citations, and citations can contradict claims. For a compliance-critical domain, the in-tool contract above is **necessary but not sufficient**; it must be paired with a downstream **NLI/entailment faithfulness verifier** (a separate axis) that checks `cited_span ⊨ claim` before the answer reaches a user. Any claim that "the Citations API solves hallucination" is false on the 2026 evidence; it solves *reference* hallucination only. Vendor improvement numbers are inaccessible-comparator anchors and should be validated on a labeled AU-banking query set, not trusted as-is.

---

## Sources <a name="sources"></a>

- [Introducing Citations on the Anthropic API](https://claude.com/blog/introducing-citations-api) — Anthropic, 2025-01-23. Citations API, deterministic quoting, Thomson Reuters / Endex adopter numbers, +15% recall.
- [Anthropic's new Citations API](https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/) — Simon Willison, 2025-01-24. "Deterministic Quoting" framing.
- [Search results (search_result content blocks)](https://platform.claude.com/docs/en/build-with-claude/search-results) — Anthropic Claude docs, 2025/2026. Full response contract, cited_text guarantee, block-as-minimal-citable-unit, all-or-nothing rule, error-handling/"No results found" pattern.
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) — Anthropic Claude docs. Quote-first, verify-or-retract, claim-then-evidence checkpoints.
- [Cohere — Documents and Citations](https://github.com/cohere-ai/cohere-developer-experience/blob/main/fern/pages/v2/text-generation/documents-and-citations.mdx) and [Cohere RAG docs](https://docs.cohere.com/docs/retrieval-augmented-generation-rag) — fine-grained out-of-the-box span citations, `command-a-03-2025`.
- [OpenAI — File search](https://platform.openai.com/docs/guides/tools-file-search) and [Responses API reference](https://developers.openai.com/api/reference/resources/responses/methods/create) — `file_citation` / `url_citation` annotations, character-offset citations into the answer.
- [Vertex AI GroundingMetadata reference](https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1beta1/GroundingMetadata) — Google Cloud. Grounding chunks/supports, confidence scores, the Gemini 2.5+ removal of confidence scores.
- [Gemini 2.0 drops confidenceScore when grounding](https://discuss.google.dev/t/gemini-2-0-suddenly-drops-confidencescore-when-grounding-with-a-data-store/188575) — Google Developer Forums, 2025. Confirms the confidence-score regression.
- [Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents](https://arxiv.org/html/2605.06635v1) — arXiv 2605.06635, 2026. 50–90% of cited responses not fully supported; citations contradict claims; more citations → more misattribution.
- [Correctness is not Faithfulness in RAG Attributions](https://arxiv.org/pdf/2412.18004) — Wallat et al., ICTIR 2025 (also [UvA PDF](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/wallat-2025-correctness.pdf)). Correctness vs. faithfulness; post-hoc citation.
- [AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions](https://arxiv.org/abs/2506.09038) — Kirichenko et al., NeurIPS 2025. Abstention unsolved; reasoning fine-tuning degrades abstention by 24%.
- [Trust or Abstain? A Self-Aware RAG Approach](https://arxiv.org/html/2605.18792) — arXiv 2605.18792, 2026. Answer/abstain/hedge trichotomy, R-Tuning "I don't know".
- ["According to ...": Prompting Language Models Improves Quoting from Pre-Training Data](https://arxiv.org/pdf/2305.13252) — Weller et al. According-to prompting improves grounding on Wikipedia/PubMed/US tax code.
- [Learning Fine-Grained Grounded Citations for Attributed LLMs (FRONT)](https://arxiv.org/pdf/2408.04568) — quote-first conditioning improves citation quality on ALCE.
- [Can LLMs Evaluate Complex Attribution in QA?](https://aclanthology.org/2025.acl-long.837.pdf) — ACL 2025. Attributed-QA / ALCE context, NLI-based citation precision/recall.
- [JSONSchemaBench: A Rigorous Benchmark of Structured Outputs](https://arxiv.org/html/2501.10868v3) — Geng et al., arXiv 2501.10868, 2025. Constrained decoding coverage up to 0.96.
- [Structured Outputs Are Becoming the Default Contract for LLM Integrations](https://g360technologies.com/structured-outputs-are-becoming-the-default-contract-for-llm-integrations/) — G360, 2025. Vendor timeline incl. Anthropic constrained decoding Nov 2025.
- [Reranking for RAG (2025 Guide)](https://app.ailog.fr/en/blog/guides/reranking) — Ailog, 2025. Cross-encoder calibration, threshold tuning, over-rejection cost.
- [Ultimate Guide to Choosing the Best Reranking Model](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/) — ZeroEntropy, 2025. Out-of-the-box calibrated rerankers (zerank-2, ELO-trained).
- [Reducing Hallucinations in Medical AI Through Citation-Enforced Prompting in RAG](https://www.mdpi.com/2076-3417/16/6/3013) — MDPI Appl. Sci., 2026. Citation-enforced prompting reduces hallucination.
