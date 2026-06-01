# Agentic Self-Correction & Abstention — Detecting Weak Grounding Before You Answer

_Researched 2026-06-01 - axis: agentic self-correction & abstention_

This axis covers the **control flow** that sits between "retrieval finished" and "answer returned": the patterns that let a system *notice* its grounding is weak and *do something about it* — re-retrieve, re-query, verify individual claims, or refuse to answer — instead of confidently emitting whatever the retriever happened to surface. The deployment context is a hybrid-RAG knowledge-retrieval **tool** exposed over MCP and consumed by an **AI agent**. That last fact is load-bearing: the consumer is already an agent with its own reasoning loop, so a real architectural question is *how much of this correction logic belongs inside the tool versus in the calling agent*. First domain is Australian banking regulation — a regulated, high-stakes setting where a confident wrong answer about an obligation is worse than "I couldn't verify this."

The headline tension for 2026: the academic self-correction literature splits cleanly into **grounded** correction (re-check against retrieval / execution — works) and **intrinsic** correction (model critiques its own reasoning with no new evidence — fragile, sometimes harmful). The patterns that survived to production are the grounded ones, and the single most under-used lever in regulated domains turns out to be the cheapest: **calibrated abstention**.

---

## Table of Contents

1. [The four families and what separates them](#1-the-four-families)
2. [Self-RAG — reflection tokens, mechanism and measured gains](#2-self-rag)
3. [Corrective RAG (CRAG) — the retrieval evaluator + fallback](#3-corrective-rag-crag)
4. [Claim-level verification — CoVe, RARR, Reflexion, FLARE](#4-claim-level-verification)
5. [Abstention — the cheapest, most under-used lever](#5-abstention)
6. [The intrinsic-self-correction problem (the big contrarian)](#6-the-intrinsic-self-correction-problem)
7. [Architecture — what lives in the tool vs the calling agent](#7-architecture-tool-vs-caller)
8. [Proven adopters](#8-proven-adopters)
9. [Contrarian views, collected](#9-contrarian-views)
10. [Verdict](#verdict)
11. [Sources](#sources)

---

## 1. The four families

Four distinct things get filed under "self-correction," and conflating them is the most common design error. They differ on *what evidence the correction step gets to use*.

| Family | Trigger | What it does | Uses NEW evidence? |
|---|---|---|---|
| **Adaptive retrieval** (Self-RAG, FLARE, CRAG) | Model/evaluator judges grounding weak | Decide *whether/what* to retrieve; re-retrieve; fall back to web | Yes — re-retrieves |
| **Claim verification** (CoVe, RARR) | After a draft exists | Decompose into atomic claims, check each against evidence, edit unsupported spans | Yes (RARR re-searches; CoVe re-asks) |
| **Trajectory reflection** (Reflexion) | Task fails / external signal | Verbalize what went wrong, retry with that memory | Yes — external feedback signal |
| **Intrinsic self-correction** | Prompt: "review and fix your answer" | Model re-reads own output, no new evidence | **No** |

The 2025–2026 consensus, stated bluntly by one survey of the area, is that "intrinsic self-correction is fragile while grounded self-correction anchored in execution results is where real gains live" ([Zylos Research, 2026-05-12](https://zylos.ai/research/2026-05-12-agent-self-correction-reflexion-to-prm)). Everything in families 1–3 is grounded. Family 4 is the one to avoid as a default — see [§6](#6-the-intrinsic-self-correction-problem). For a retrieval tool, this is good news: retrieval *is* the external evidence source, so the productive forms of correction are exactly the ones a retrieval tool can do natively.

---

## 2. Self-RAG

**Mechanism.** Self-RAG (Asai et al., 2023, ICLR 2024 oral) trains a single LM to emit special **reflection tokens** inline with generation, so the model both decides when to retrieve and grades what it retrieved ([selfrag.github.io](https://selfrag.github.io/)). Four token types:

1. **`Retrieve`** — should I fetch external docs right now? (on-demand, not always).
2. **`ISREL`** (relevance) — is this retrieved passage relevant to the query?
3. **`ISSUP`** (support) — does this passage actually *support* the statement I just generated? (fully / partially / no support).
4. **`ISUSE`** (utility) — is the overall response useful (1–5)?

The model generates several candidate continuations, each annotated, then picks the best by a weighted score over the critique tokens — so relevance/support thresholds are tunable at *inference* time without retraining ([selfrag.github.io](https://selfrag.github.io/)).

**Measured gains.** Self-RAG (7B and 13B) "significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks," beating ChatGPT and retrieval-augmented Llama2-chat on open-domain QA, reasoning, and fact verification, with notably higher **citation accuracy** for long-form generation ([Asai et al., arXiv:2310.11511](https://arxiv.org/abs/2310.11511); [selfrag.github.io](https://selfrag.github.io/)). The two results that matter for a regulated tool: the support token directly targets *citation faithfulness* (does the source back the claim), and retrieval becomes on-demand rather than always-on, which cuts unnecessary retrieval.

**Cost / objection.** Self-RAG's clean form requires **fine-tuning a model to emit the tokens** — you do not get it for free on top of an off-the-shelf model. That is a poor fit for a domain-agnostic tool that must work with whatever model the calling agent uses. The widely-deployed workaround (LangGraph's "self-reflective RAG") reimplements the *grade-relevance / grade-support / decide-to-retry* logic as **separate LLM grader calls in a graph**, no fine-tuning, model-agnostic — at the cost of extra round-trips ([LangChain, "Self-Reflective RAG with LangGraph"](https://blog.langchain.com/agentic-rag-with-langgraph/)). For a tool, the *pattern* (grade relevance, grade support, gate the answer) is what transfers; the trained-token implementation does not.

---

## 3. Corrective RAG (CRAG)

**Mechanism.** CRAG (Yan et al., 2024) is the most directly applicable pattern for a retrieval tool because it is **plug-and-play and model-agnostic** — it bolts onto any RAG pipeline ([Yan et al., arXiv:2401.15884](https://arxiv.org/abs/2401.15884)). A **lightweight retrieval evaluator** (a fine-tuned **T5-large**, ~0.77B params — far smaller than the generator) scores each retrieved doc and produces a confidence degree that triggers one of three actions ([Meilisearch, "Corrective RAG"](https://www.meilisearch.com/blog/corrective-rag); [arXiv:2401.15884v3](https://arxiv.org/html/2401.15884v3)):

- **CORRECT** (confidence above upper threshold): run **knowledge refinement** — a *decompose-then-recompose* step that splits docs into "knowledge strips," drops noisy strips, and recomposes only the key ones.
- **INCORRECT** (all docs below lower threshold): **discard** internal docs entirely and fall back to **large-scale web search**.
- **AMBIGUOUS** (in between): **merge** refined internal docs with web-search results.

**Measured gains.** On top of a SelfRAG-LLaMA2-7B base, CRAG beat standard RAG by **+19.0% accuracy on PopQA, +14.9 FactScore on Biography, +36.6% on PubHealth, +8.1% on Arc-Challenge** ([arXiv:2401.15884v3](https://arxiv.org/html/2401.15884v3)). Stacked as **Self-CRAG** on top of Self-RAG, it added **+20.0% PopQA, +36.9 FactScore Biography, +4.0% Arc** (LLaMA2-7B base) ([arXiv:2401.15884v3](https://arxiv.org/html/2401.15884v3)). The big PubHealth/Biography jumps are exactly the long-form-factuality and fact-verification shapes a regulation tool cares about.

**When it helps / when it doesn't.** CRAG's premise is "not all retrieved documents are reliable" — so its value is proportional to how often your retriever returns junk. With a strong hybrid retriever + reranker (the upstream axes), the *INCORRECT* (full discard) branch fires rarely, and the value collapses to the refinement step. Two cautions: (a) the original numbers used now-deprecated `text-davinci-003` as the generator, so absolute figures will differ on a 2026 model ([arXiv:2401.15884v3](https://arxiv.org/html/2401.15884v3)); (b) the **web-fallback branch is wrong for AU banking regulation** — you do not want a regulatory-obligation answer silently sourced from an open web search. For this domain the fallback target must be a *curated authority set* (APRA / ASIC / Federal Register of Legislation), not the open web, or the answer must abstain. The evaluator + three-way routing is the keeper; the literal web-search action is not.

---

## 4. Claim-level verification

These operate *after* a draft answer exists, checking individual claims rather than gating retrieval.

**Chain-of-Verification (CoVe)** (Dhuliawala et al., Meta AI, 2023; ACL Findings 2024). Four steps: draft a baseline answer → plan verification questions about it → answer each question **independently** (the model is blocked from attending to the original draft) → synthesize a corrected answer ([arXiv:2309.11495](https://arxiv.org/abs/2309.11495)). The crucial design point — and the reason CoVe works where naive "re-read and fix" doesn't — is **factored verification**: "controlling the attention of the model so that it cannot attend to its previous answers… helps alleviate copying the same hallucinations" ([arXiv:2309.11495](https://arxiv.org/abs/2309.11495)). CoVe measurably reduces hallucination on list questions (Wikidata), closed-book MultiSpanQA, and long-form generation — but the authors are explicit it **cannot eliminate** hallucination ([arXiv:2309.11495](https://arxiv.org/abs/2309.11495)). Cost: 1 draft + N verification questions + 1 synthesis = several extra LLM calls per answer.

**RARR** (Gao et al., Google, ACL 2023) — "Retrofit Attribution using Research and Revision." Post-hoc: for any model output, it auto-**researches** attribution via standard web search, then **post-edits** unsupported spans to agree with evidence "while preserving the original output as much as possible," and attaches citations ([arXiv:2210.08726](https://arxiv.org/abs/2210.08726); [ACL Anthology 2023.acl-long.910](https://aclanthology.org/2023.acl-long.910/)). It needs "only a handful of training examples, an LLM, and standard web search." RARR is attractive because it is **model-agnostic and post-hoc** — it wraps any generator — and its output is exactly what a regulated domain wants: claims tied to sources, unsupported claims edited or flagged. Same web-source caveat as CRAG applies: point the "research" step at the curated authority corpus, not the open web.

**Reflexion** (Shinn et al., NeurIPS 2023) — verbal reinforcement. The agent reflects in natural language on a *task-feedback signal*, stores the reflection in episodic memory, and retries; it reached **91% pass@1 on HumanEval vs GPT-4's 80%** ([arXiv:2303.11366](https://arxiv.org/abs/2303.11366); [GitHub noahshinn/reflexion](https://github.com/noahshinn/reflexion)). The catch that defines its applicability: Reflexion's gains depend on a **reliable external feedback signal** (unit tests passing/failing, an environment reward). Code has that; "is this regulatory answer correct?" generally does not have a cheap ground-truth oracle. Reflexion is a *caller-loop* pattern, not a retrieval-tool pattern, and only pays off where the loop has a real grader.

**FLARE** (Jiang et al., EMNLP 2023) — Forward-Looking Active REtrieval. Iteratively predicts the *upcoming sentence*; if it contains low-confidence tokens, it uses that draft sentence as a query, re-retrieves, and regenerates ([arXiv:2305.06983](https://arxiv.org/abs/2305.06983)). Strong on long-form multi-hop (e.g. 51.0 vs 42.4 EM on 2WikiMultihopQA in one variant), but two problems make it a weak default: (1) it depends entirely on **token-confidence calibration**, and "instruction-tuned or RLHF chat models are often overconfident — they emit high-probability tokens even when hallucinating" ([Unified Active Retrieval, arXiv:2406.12534](https://arxiv.org/html/2406.12534v1)); (2) a 2024 follow-up found FLARE's retrieval-decision accuracy was only **56.50% vs 85.32%** for a trained classifier (UAR) ([arXiv:2406.12534](https://arxiv.org/html/2406.12534v1)). FLARE is interesting research, not a 2026 default.

---

## 5. Abstention

This is the lever most teams skip and the one that matters most in regulated domains. Abstention = the system returns a calibrated "I don't know / I can't verify this from the available sources" instead of a confident answer when grounding is weak.

**Why it is structurally under-supplied.** OpenAI's "Why Language Models Hallucinate" (Kalai, Nachum, Vempala, Zhang; 2025-09-06) gives the mechanism: post-training benchmarks use binary grading (1 for correct, 0 for anything else *including* IDK), so "under binary graders… the expected score-maximizing strategy is **never to abstain**" — models are trained to guess ([Kalai et al., 2025; summary](https://kingy.ai/blog/why-language-models-hallucinate-openai-paper-summary/)). Their proposed fix is to give the model an explicit **confidence target**: "answer only if confident above threshold *t*, since errors cost *t/(1−t)* points, correct answers earn 1, and IDK earns 0." This makes abstention rational when uncertainty is high. The same idea appears as a training objective in **behaviorally calibrated RL**, which rewards models for "stochastically admit[ting] uncertainty by abstaining when not confident," and finds the resulting calibration is a *transferable meta-skill* — smaller models can beat frontier models at uncertainty quantification ([arXiv:2512.19920](https://arxiv.org/abs/2512.19920)).

**The rigorous version: conformal abstention.** DeepMind's conformal-abstention method (Yadkori et al., 2024) uses the LLM to self-evaluate response self-consistency, then applies **conformal prediction** to calibrate an abstention threshold with a **distribution-free statistical guarantee** that the hallucination rate stays under a target, *while minimizing* the abstention rate. On Temporal Sequences and TriviaQA (Gemini Pro) it bounded hallucination at a far less conservative abstention rate than log-probability baselines ([arXiv:2405.01563](https://arxiv.org/abs/2405.01563); [TechXplore, 2024-05](https://techxplore.com/news/2024-05-method-mitigate-hallucinations-large-language.html)). This is the single most defensible abstention design for a high-stakes tool: you get a *tunable, provable* hallucination-rate ceiling, and the operator picks where on the precision/coverage curve to sit.

**Evidence abstention beats confident-wrong in regulated domains.** Uncertainty-based abstention "improves safety and reduces hallucinations" and the survey literature flags that "reliance on fabricated content in high-stakes domains such as medicine or law can have severe consequences" — i.e. the cost asymmetry is real and recognized ([arXiv:2404.10960](https://arxiv.org/pdf/2404.10960); [Wen et al., "Know Your Limits," TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00754/131566/Know-Your-Limits-A-Survey-of-Abstention-in-Large)). For AU banking regulation the decision-theoretic case is overwhelming: a confidently wrong statement about a CPS 230 obligation can drive a compliance error; "I can only find partial support — here are the sources I did find" cannot. **Abstention is the cheapest correction primitive** (no extra retrieval round-trip; just a threshold on a support/grounding score you already computed) and the highest-leverage in this domain.

**Contrarian on abstention.** Over-abstention destroys utility — a tool that answers 40% of questions with "I don't know" is a tool nobody calls. The conformal framing answers this directly: it *minimizes* abstention subject to the risk bound rather than abstaining freely, and "Know Your Limits" warns that abstention skills often fail to *generalize across domains* — a threshold calibrated on AU banking won't transport unchanged to a new corpus ([Wen et al., TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00754/131566/Know-Your-Limits-A-Survey-of-Abstention-in-Large)). So abstention must be **calibrated per-corpus**, not a global constant.

---

## 6. The intrinsic-self-correction problem

The strongest contrarian against this entire axis, and it must be confronted head-on.

Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024) showed that when an LLM is asked to review and fix its own reasoning **with no external feedback**, performance *does not improve and often degrades* — correct answers get flipped to wrong ([arXiv:2310.01798](https://arxiv.org/abs/2310.01798)). The diagnosed cause: the failure is in *finding* the error, not fixing it — "LLMs cannot find reasoning errors, but can correct them given the error location" ([Tyen et al., ACL Findings 2024, arXiv:2311.08516](https://aclanthology.org/2024.findings-acl.826/)). The critical survey "When Can LLMs Actually Correct Their Own Mistakes?" (TACL 2024) generalizes it: self-correction helps only when the critique step has access to **reliable external feedback** (retrieval, tools, execution, ground-truth labels); pure intrinsic re-reading is unreliable ([arXiv:2406.01297](https://arxiv.org/html/2406.01297v1)).

**Design consequence.** This is *not* an argument against self-correction in a retrieval tool — it is an argument for which kind. Self-RAG's support token, CRAG's evaluator, RARR's research step, and abstention thresholds are all grounded in **external evidence** (the retrieved documents). They are exactly the corrections Huang's result says *do* work. The forbidden pattern is the cheap one teams reach for first: "ask the model to double-check its answer" with nothing new in context. Do not build that. Every correction step in this design must consume new evidence (a re-retrieval, a support score against documents, a calibration statistic) — never just the model's own prior output.

---

## 7. Architecture — tool vs caller

The defining constraint: the consumer is **already an agent** with its own loop. So which correction belongs in the MCP tool, and which in the caller? Two postures:

- **"Smart about retrieval, dumb about goals"** — the tool owns everything it can do with the documents in hand (relevance grading, support scoring, refinement, abstention/confidence reporting) and returns a *grounded, self-assessed* result. It does **not** run a multi-turn task loop.
- **"Full agentic loop in caller"** — the tool is a thin retrieval pipe; all decide-to-retry / verify-claims / decide-to-abstain logic lives in the calling agent.

**The evidence favors the first posture, with a clean split.** Anthropic's own tool-design guidance argues tools should "return only high-signal information" and "consolidate multi-step operations within tools rather than pushing reasoning into agents" — and that any deterministic computation (a comparison, a threshold) should be done *server-side* in the tool, "rather than asking the LLM to compare them, which risks getting it wrong" ([Anthropic, "Writing Tools for Agents"](https://www.anthropic.com/engineering/writing-tools-for-agents)). The agent-aware-MCP community reaches the same conclusion: "a spec-compliant MCP server that only returns raw data is an architectural bottleneck"; responses must "help agents decide, not just contain data" ([Medium, "Agent-Aware MCP," 2025](https://medium.com/@kumaran.isk/agent-aware-mcp-10-patterns-for-actionable-tool-responses-54029e337941)).

Mapping the four families onto this split:

| Correction step | Lives in | Why |
|---|---|---|
| Relevance grading (Self-RAG `ISREL`) | **Tool** | Deterministic-ish, evidence-local, cheap. Tool sees the docs. |
| Support/grounding score (Self-RAG `ISSUP`) | **Tool** | Faithfulness is a property of (claim, retrieved doc) — both in the tool. |
| Retrieval evaluator + refinement (CRAG) | **Tool** | Operates on retrieved set; T5-scale, no big model needed. |
| **Re-retrieve / re-query** | **Tool** (bounded, 1 retry) | Tool owns the index; one corrective re-query is cheap and local. |
| Confidence / abstention signal | **Tool emits, caller decides** | Tool reports calibrated support score + "below threshold" flag; caller owns the *policy* (abstain vs ask user vs proceed) because that's goal-level. |
| Claim verification across an answer (CoVe/RARR) | **Caller** (or optional tool mode) | Spans a full generated answer the tool didn't write; needs the answer. |
| Multi-step task loop / Reflexion retry | **Caller** | Goal-level; needs task feedback the tool can't see. |

**The objection: token cost & latency.** Every correction step is extra LLM calls. Iterative-refinement loops "cost 2–3x more tokens versus single-pass," and naive multi-agent chains "triple both cost and delay" ([HockeyStack, "Optimizing Latency and Cost in Multi-Agent Systems"](https://www.hockeystack.com/applied-ai/optimizing-latency-and-cost-in-multi-agent-systems); [langcopilot, 2025-10](https://langcopilot.com/posts/2025-10-17-why-ai-agents-fail-latency-planning)). The architecture answers this two ways: (1) put the cheap, deterministic, evidence-local checks (grading, support scoring, refinement, abstention threshold) **in the tool** using a *small* evaluator (T5-scale per CRAG) — not the generator — so they cost milliseconds, not generator tokens; (2) make the expensive, generator-token-heavy verification (CoVe-style claim checking, retry loops) **opt-in by the caller** via a `verification_level` parameter, so the agent pays for it only when the stakes justify it. This mirrors Anthropic's recommended `response_format: concise | detailed` pattern ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)).

**Why not push everything to the caller** (since it's already an agent)? Because (a) the tool has information the caller doesn't — the raw retrieved docs and their scores — so support/relevance grading is *cheaper and more accurate* in the tool; (b) duplicated, uncoordinated correction in every caller is the multi-agent anti-pattern that "makes things worse" ([ImagineX, "Why Your Multi-Agent AI System Is Probably Making Things Worse"](https://www.imaginexdigital.com/insights/why-your-multi-agent-ai-system-is-probably-making-things-worse)); (c) a tool that abstains/flags low-support *uniformly* gives every consumer the same safety floor, which is what a regulated domain needs.

---

## 8. Proven adopters

- **CRAG / Self-RAG / Adaptive RAG in production form: LangGraph (LangChain).** All three are shipped as reference production tutorials, reimplemented *without fine-tuning* as grader-node graphs — the most widely-copied real-world instantiation of these patterns ([LangChain, "Self-Reflective RAG with LangGraph"](https://blog.langchain.com/agentic-rag-with-langgraph/); [LangGraph Adaptive RAG tutorial](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)).
- **Conformal abstention: Google DeepMind**, evaluated on Gemini Pro ([arXiv:2405.01563](https://arxiv.org/abs/2405.01563)).
- **CoVe: Meta AI** (original authors) ([arXiv:2309.11495](https://arxiv.org/abs/2309.11495)).
- **RARR: Google** ([ACL 2023](https://aclanthology.org/2023.acl-long.910/)).
- **Behavioral-calibration abstention: OpenAI** researchers (Kalai/Nachum/Vempala) frame it as the institutional fix for hallucination benchmarks ([Kalai et al., 2025](https://kingy.ai/blog/why-language-models-hallucinate-openai-paper-summary/)).
- **Tool-vs-caller split: Anthropic** (official tool-writing guidance) and **Datadog** (lessons from a production MCP server) both argue for high-signal, decision-supporting tool responses over raw-data pipes ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents); [Datadog, "Designing MCP tools for agents"](https://www.datadoghq.com/blog/engineering/mcp-server-agent-tools/)).

---

## 9. Contrarian views, collected

- **"Self-correction degrades correct answers."** True for *intrinsic* correction with no new evidence — Huang et al. show performance flat or worse ([arXiv:2310.01798](https://arxiv.org/abs/2310.01798)). Mitigation: only ever correct against external evidence (retrieval/support scores), never the model's own prior text.
- **"LLMs can't even find their errors."** Tyen et al.: the bottleneck is error *localization*, not correction ([arXiv:2311.08516](https://aclanthology.org/2024.findings-acl.826/)). Implication: a separate, evidence-grounded evaluator (CRAG's T5, a support scorer) beats asking the generator to self-critique.
- **"Agents don't iterate productively."** Multi-agent / iterative-refinement systems often perform *worse* and leave 85% of budget unused, while tripling cost and latency ([ImagineX](https://www.imaginexdigital.com/insights/why-your-multi-agent-ai-system-is-probably-making-things-worse); [HockeyStack](https://www.hockeystack.com/applied-ai/optimizing-latency-and-cost-in-multi-agent-systems)). Implication: bound the loop (≤1 corrective re-retrieval in-tool; verification opt-in), don't build an open-ended agentic loop in the tool.
- **"Active retrieval (FLARE) is brittle."** Relies on token-confidence calibration that chat models lack; 56.5% vs 85.3% retrieval-decision accuracy vs a trained classifier ([arXiv:2406.12534](https://arxiv.org/html/2406.12534v1)). Implication: prefer an explicit evaluator over confidence-token triggers.
- **"Abstention kills utility."** Over-abstention makes the tool useless and doesn't generalize across domains ([Wen et al., TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00754/131566/Know-Your-Limits-A-Survey-of-Abstention-in-Large)). Mitigation: conformal calibration minimizes abstention subject to a risk bound; calibrate per-corpus.
- **"Web fallback (CRAG) is dangerous in regulated domains."** A regulatory answer must not be silently sourced from the open web. Mitigation: replace the open-web fallback with a curated authority set (APRA/ASIC/legislation) or abstain.

---

## Verdict

**The single SOTA self-correction/abstention design for mid-2026 is: a grounded, evaluator-driven correction stack inside the tool, capped by calibrated abstention, with expensive claim-verification left opt-in to the caller.** Concretely, in the order an answer flows:

1. **Retrieval evaluator (CRAG-style, small T5-scale model) — in the TOOL.** Score the retrieved set; route CORRECT → refine, AMBIGUOUS → re-query + merge, INCORRECT → re-retrieve against a *curated authority corpus* (never open web), capped at **one** corrective re-retrieval. This is the most directly applicable, model-agnostic, plug-and-play pattern and carries the largest measured gains (+15–37 points on long-form factuality / fact-verification benchmarks).
2. **Relevance + support grading (Self-RAG `ISREL`/`ISSUP` pattern, reimplemented as grader calls, not fine-tuned tokens) — in the TOOL.** Produce a per-claim *support score* against the retrieved docs. This is the citation-faithfulness signal a regulated domain needs, and the tool is the only component that holds both the claim and its source.
3. **Calibrated abstention (conformal abstention, DeepMind-style) — TOOL emits the signal, CALLER owns the policy.** The tool returns a support score plus a "below-threshold / cannot verify" flag, calibrated *per-corpus* to a target hallucination-rate ceiling. The caller decides whether to abstain, ask the user, or proceed. This is the cheapest and highest-leverage primitive for AU banking regulation, where confident-wrong is strictly worse than "I can't verify this."
4. **Claim verification (CoVe-/RARR-style) — in the CALLER, opt-in.** Exposed via a `verification_level` tool parameter so generator-token-heavy verification is paid for only when stakes justify it.

The non-negotiable invariant across all four: **every correction step consumes new external evidence** (re-retrieval, support score against documents, a calibration statistic) — never the model re-reading its own output. That is the one design rule the 2024–2026 literature is unanimous on (Huang et al.; "When Can LLMs Correct Their Own Mistakes").

**Where each piece lives:** cheap + evidence-local + deterministic → **tool** (grading, support scoring, refinement, one bounded re-retrieval, abstention *signal*); goal-level + answer-spanning + generator-token-heavy → **caller** (abstention *policy*, claim verification, any multi-step retry). The tool is "smart about retrieval, dumb about goals."

**Alternatives, ranked:**
- *If fine-tuning a model for the domain is on the table:* native Self-RAG reflection tokens are tighter (one model, inference-time tunable thresholds) than reimplemented grader calls — but lose model-agnosticism, so only if the tool ships its own model.
- *If the calling agent is trusted and sophisticated:* push more (claim verification, retry policy) to the caller and keep the tool thinner — accept the risk that uncoordinated per-caller correction is inconsistent and that the safety floor is no longer uniform.
- *If latency budget is extremely tight:* drop CRAG refinement and CoVe entirely; keep **only** support scoring + abstention. Abstention alone is the minimal viable anti-hallucination control and the one you should never cut.
- *Reject as defaults:* FLARE (calibration-brittle), intrinsic self-correction (degrades answers), open-web fallback (wrong sourcing for regulation), and any unbounded agentic retry loop in the tool (cost/latency blowup with no productivity gain).

---

## Sources

- [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection — Asai et al., arXiv:2310.11511, Oct 2023 (ICLR 2024)](https://arxiv.org/abs/2310.11511)
- [Self-RAG project page — selfrag.github.io, 2024](https://selfrag.github.io/)
- [Corrective Retrieval Augmented Generation (CRAG) — Yan et al., arXiv:2401.15884, Jan 2024](https://arxiv.org/abs/2401.15884)
- [CRAG full text with results tables — arXiv:2401.15884v3](https://arxiv.org/html/2401.15884v3)
- [Corrective RAG: workflow & implementation — Meilisearch blog, 2025](https://www.meilisearch.com/blog/corrective-rag)
- [Chain-of-Verification Reduces Hallucination in LLMs — Dhuliawala et al. (Meta AI), arXiv:2309.11495, Sep 2023 (ACL Findings 2024)](https://arxiv.org/abs/2309.11495)
- [RARR: Researching and Revising What Language Models Say — Gao et al. (Google), arXiv:2210.08726 / ACL 2023](https://arxiv.org/abs/2210.08726)
- [RARR — ACL Anthology 2023.acl-long.910](https://aclanthology.org/2023.acl-long.910/)
- [Reflexion: Language Agents with Verbal Reinforcement Learning — Shinn et al., arXiv:2303.11366, NeurIPS 2023](https://arxiv.org/abs/2303.11366)
- [Reflexion reference implementation — GitHub noahshinn/reflexion](https://github.com/noahshinn/reflexion)
- [Active Retrieval Augmented Generation (FLARE) — Jiang et al., arXiv:2305.06983, EMNLP 2023](https://arxiv.org/abs/2305.06983)
- [Unified Active Retrieval for RAG (FLARE critique, retrieval-decision accuracy) — arXiv:2406.12534, EMNLP Findings 2024](https://arxiv.org/html/2406.12534v1)
- [Large Language Models Cannot Self-Correct Reasoning Yet — Huang et al., arXiv:2310.01798, ICLR 2024](https://arxiv.org/abs/2310.01798)
- [LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location — Tyen et al., arXiv:2311.08516, ACL Findings 2024](https://aclanthology.org/2024.findings-acl.826/)
- [When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey — arXiv:2406.01297, TACL 2024](https://arxiv.org/html/2406.01297v1)
- [Mitigating LLM Hallucinations via Conformal Abstention — Yadkori et al. (Google DeepMind), arXiv:2405.01563, Apr 2024](https://arxiv.org/abs/2405.01563)
- [A method to mitigate hallucinations in large language models (conformal abstention coverage) — TechXplore, May 2024](https://techxplore.com/news/2024-05-method-mitigate-hallucinations-large-language.html)
- [Uncertainty-Based Abstention in LLMs Improves Safety and Reduces Hallucinations — arXiv:2404.10960, 2024](https://arxiv.org/pdf/2404.10960)
- [Know Your Limits: A Survey of Abstention in LLMs — Wen et al., TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00754/131566/Know-Your-Limits-A-Survey-of-Abstention-in-Large)
- [Why Language Models Hallucinate — Kalai, Nachum, Vempala, Zhang (OpenAI), Sep 2025 (paper summary)](https://kingy.ai/blog/why-language-models-hallucinate-openai-paper-summary/)
- [Mitigating LLM Hallucination via Behaviorally Calibrated Reinforcement Learning — arXiv:2512.19920, Dec 2025](https://arxiv.org/abs/2512.19920)
- [Agent Self-Correction: From Reflexion to Process Reward Models — Zylos Research, May 2026](https://zylos.ai/research/2026-05-12-agent-self-correction-reflexion-to-prm)
- [Self-Reflective RAG with LangGraph (CRAG + Self-RAG production reimplementation) — LangChain blog](https://blog.langchain.com/agentic-rag-with-langgraph/)
- [Adaptive RAG tutorial — LangGraph docs (LangChain)](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)
- [Writing Tools for Agents (tool-vs-agent logic split, high-signal responses) — Anthropic Engineering](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Designing MCP tools for agents: lessons from Datadog's MCP server — Datadog Engineering](https://www.datadoghq.com/blog/engineering/mcp-server-agent-tools/)
- [Agent-Aware MCP: 10 Patterns for Actionable Tool Responses — Medium, 2025](https://medium.com/@kumaran.isk/agent-aware-mcp-10-patterns-for-actionable-tool-responses-54029e337941)
- [Why Your Multi-Agent AI System Is Probably Making Things Worse — ImagineX](https://www.imaginexdigital.com/insights/why-your-multi-agent-ai-system-is-probably-making-things-worse)
- [Optimizing Latency and Cost in Multi-Agent Systems — HockeyStack](https://www.hockeystack.com/applied-ai/optimizing-latency-and-cost-in-multi-agent-systems)
- [Why AI Agents Fail: Latency, Planning & Reflection (2025 Guide) — langcopilot](https://langcopilot.com/posts/2025-10-17-why-ai-agents-fail-latency-planning)
