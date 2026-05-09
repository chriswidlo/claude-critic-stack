# What is this stack actually for, and is it already solved? — SOTA survey + mission anchor

| Field | Value |
|---|---|
| 📌 **title** | What is this stack actually for, and is it already solved? — SOTA survey + mission anchor |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-09 |
| ⚡ **catalyst** | Operator pushed back on a verbose synthesis from session [`2026-05-09-critic-independence-vs-target-repo-read-access`](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/) with: *"is it regressing? we should always re-align if we are diverging from our mission and vision. actually i think we need to define it first."* The pushback exposed that this repo has never written down — in non-compromising prose — what it is for, and never compared itself honestly against the SOTA. The catalyst is the gap between an unwritten mission and a stack that keeps growing. |
| 💡 **essence** | A web-wide survey of LLM-as-judge, multi-agent debate, AI code/design review, and adversarial-review methodologies (2024–2026, mostly 2025–2026) confirms that **most slices the user might confuse this stack with are crowded** — output evaluation (Prometheus, G-Eval, RAGAS, FACTS Grounding), code review (CodeRabbit, Greptile, Qodo, Sourcery, Korbit), multi-agent debate for factuality (Du et al., CourtEval), reliability via veto authority on outputs (Vijayaraghavan et al.'s "Team of Rivals", arXiv 2601.14351, Jan 2026). On those slices the stack would be redundant. **The slice that remains genuinely open is narrower than "AI design review"**: it is the *combination* of pre-decision design-question review + three-lens minority-veto + frame-challenger as a separate gated agent + reference-class forecasting as a mandatory step + anti-anchoring via on-disk subagent-distiller artifacts + canon-first contradicting-source retrieval + hard gates between steps, all as one fixed prescriptive workflow. No surveyed system combines all seven. The stack's claim is real — but it must be stated narrowly, or it dissolves into already-solved territory. |
| 🚀 **upgrade** | (a) Write a non-compromising mission section to [README.md](../../../README.md) anchored on the founding [`.genesis/five-pressures.md`](../../../.genesis/five-pressures.md) failure modes, naming what the stack is *not* (not a code reviewer, not an output grader, not RFP review). (b) Identify the Phase 2 drift surface in `.genesis/` — the Explore + critique-prep + critique-start additions never re-anchored success criteria — and document it as an addendum, not as an edit to founding docs. (c) Use this entry as input to ultraplan, not as a directly-actionable plan; it is too broad to action without a slicing decision. |
| 🏷️ **tags** | meta, mission, sota-comparison, ecosystem-survey, drift-detection, ultraplan-input |
| 🔗 **relates_to** | 2026-05-08-plugin-ecosystem-shows-enforcement-gap (parallel SOTA survey on Claude-Code-plugins axis); 2026-04-26-critic-panel-correlated-by-default (the comparator that already lands one piece); 2026-04-27-r-and-d-lab-thesis (lab as memory); .genesis/five-pressures.md (founding intent) |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-09 | — | — | — | — | — | — | — | — | — |

## Table of contents

- [Why this entry exists](#why-this-entry-exists)
- [The question, restated honestly](#the-question-restated-honestly)
- [Founding intent — what `.genesis/` says](#founding-intent--what-genesis-says)
- [What the SOTA dive surveyed](#what-the-sota-dive-surveyed)
- [Slice-by-slice: who covers what](#slice-by-slice-who-covers-what)
  - [LLM-as-judge for outputs (closed)](#llm-as-judge-for-outputs-closed)
  - [Multi-agent debate for factuality (closed)](#multi-agent-debate-for-factuality-closed)
  - [AI code review (closed)](#ai-code-review-closed)
  - [Adversarial code review patterns (closed)](#adversarial-code-review-patterns-closed)
  - [Multi-lens veto panels for outputs (closest match — Team of Rivals)](#multi-lens-veto-panels-for-outputs-closest-match--team-of-rivals)
  - [Devil's Advocate as introspection (closed)](#devils-advocate-as-introspection-closed)
  - [Premortem via AI (closed as technique)](#premortem-via-ai-closed-as-technique)
  - [Reference-class forecasting + LLMs (research, not primitive)](#reference-class-forecasting--llms-research-not-primitive)
- [What is genuinely open — the actual claim](#what-is-genuinely-open--the-actual-claim)
- [Counter-evidence — humility about multi-agent](#counter-evidence--humility-about-multi-agent)
- [Drift surface — where Phase 2 weakened the founding contract](#drift-surface--where-phase-2-weakened-the-founding-contract)
- [Proposed mission text for README.md](#proposed-mission-text-for-readmemd)
- [Open questions — for ultraplan](#open-questions--for-ultraplan)
- [What ships from this entry](#what-ships-from-this-entry)
- [Why this is profound, not normal](#why-this-is-profound-not-normal)
- [Sources](#sources)

## Why this entry exists

The operator's pushback ("define mission first; then say whether we're regressing; verify against SOTA so we don't waste effort on something already solved") landed because no document in the repo answers the meta-question *"what is this stack actually for, and what is it not?"*. [`.genesis/five-pressures.md`](../../../.genesis/five-pressures.md) names the *failure modes* the stack defends against, but does not name (a) the artifact under review (design questions vs. outputs vs. code), (b) the timing (pre-decision vs. post-hoc), (c) the comparison class. Without that, every claim of value is unfalsifiable, and every additive feature (Explore, critique-prep, critique-start, shadow comparator) compounds the ambiguity.

This entry resolves the meta-question by doing the SOTA homework the repo had not done, then proposing the mission text that survives contact with that survey. The output is **input to ultraplan** — broad enough to span README, CLAUDE.md, and `.genesis/` decisions, narrow enough that each decision is locatable.

## The question, restated honestly

*"There is no solution to what is our statement here?"* — operator's framing, paraphrased.

This is two questions stacked:

1. **Is the gap we believe we are filling actually empty?** If the AI ecosystem in 2025–2026 already ships a system that does what we do, building this is busywork.
2. **What is our statement?** A statement we cannot write in two sentences is not a statement; it is an aspiration.

The catalyst was a wall-of-text synthesis from the prior session that *talked around* both questions. The honest answer is below.

## Founding intent — what `.genesis/` says

[`.genesis/five-pressures.md`](../../../.genesis/five-pressures.md) lines 1–3, 5–31, 37 establish the founding success criterion: *"A checklist to run against any non-trivial design recommendation before shipping it to a user. Each pressure compensates for a known LLM failure mode."* The five named failure modes are:

1. **Reframe-before-answer** — accepting the user's framing uncritically.
2. **Enumerate-before-select** — confident recommendation of the first option without comparison.
3. **Outside-view-first** — inside-view detail-reasoning that misses base rates.
4. **Name-your-uncertainty** — equally-confident prose regardless of actual confidence.
5. **Consequence-imagine** — recommending patterns without modelling failure modes.

[`.genesis/architecture-review.md`](../../../.genesis/architecture-review.md) lines 22–23 establish the Phase 1 baseline: a 6-step workflow with a **single critic**, not a panel.

[`.genesis/ok-cool-this-is-warm-balloon.md`](../../../.genesis/ok-cool-this-is-warm-balloon.md) lines 24–34 introduce the Phase 2 changes: decompose the single critic into a three-lens panel; add an `Explore` step at position 5 *for repository context*. **This Phase 2 doc does not re-state success criteria.** The critic-panel decomposition and the target-repo introduction land without a written reaffirmation of what the stack is for under the new shape. That is the drift surface.

The founding intent was **role/aspect orthogonality on shared input**, never information independence. The phrase "three independent critics" — to the extent it has been repeated colloquially — is bigger than the property the stack ever claimed in writing.

## What the SOTA dive surveyed

Eleven WebSearch queries plus targeted WebFetch on the closest match (arXiv 2601.14351). Queries covered:

- LLM-as-judge frameworks (G-Eval, Prometheus, JudgeLM, MT-Bench, RAGAS, FACTS Grounding, AlpacaEval, Arena-Hard, Auto-J, Multi-Agent-as-Judge).
- Multi-agent debate / critique systems (Du et al. multi-agent debate, CourtEval, Heterogeneous Debate Engine, Adversarial Multi-Agent Evaluation, Society of Mind).
- AI code review tools (CodeRabbit, Greptile, Qodo, Sourcery, Korbit, Codacy, Cursor review, Aider review, Devin review).
- Adversarial code review patterns (MCP servers, Anthropic three-agent planner/generator/evaluator, ASDLC.io patterns, SCOUT/GUARD).
- AI design / RFC review tooling (Spec Kit, Notion AI, Amazon Q, document-review accelerators).
- Multi-lens veto panels (AI Office / Team of Rivals — Vijayaraghavan et al. arXiv 2601.14351).
- Devil's Advocate (Wang et al. EMNLP 2024 Findings, arXiv 2405.16334).
- Reference-class forecasting + LLMs (AI-Augmented Predictions, ForecastBench, superforecasting LLM benchmarks).
- Premortem via AI (Klein/Kahneman techniques as Claude skills, alfred_, Stripe-style decision frameworks).
- Anthropic adversarial review patterns and subagent architecture.
- Counter-evidence: "Single-Agent LLMs Outperform Multi-Agent" (arXiv 2604.02460), "Multi-Agent Teams Hold Experts Back" (arXiv 2602.01011), "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657), "When collaboration fails: persuasion driven adversarial influence" (Nature Sci Reports 2026).

Results below. Real URLs only; nothing fabricated; if a link goes stale, the URL was live as of 2026-05-09.

## Slice-by-slice: who covers what

### LLM-as-judge for outputs (closed)

Status: **already solved, with active 2025–2026 research filling remaining holes.**

Representative systems:
- **G-Eval** — output-grading framework using GPT-4 / Claude. Post-hoc.
- **Prometheus** / **Prometheus-2** — open-source LLM judges with rubric prompts. Post-hoc.
- **RAGAS** — RAG output evaluation; faithfulness + context-relevance. Post-hoc.
- **FACTS Grounding** (DeepMind, 2025) — factuality benchmark for grounded responses. Post-hoc.
- **JudgeLM**, **Auto-J**, **MT-Bench**, **AlpacaEval 2 (length-controlled)**, **Arena-Hard** — pairwise / pointwise output graders.
- **Multi-Agent-as-Judge** (arXiv 2507.21028, 2025) — multi-dimensional human-evaluation alignment.
- **Multi-Agent Debate for LLM Judges with Adaptive Stability Detection** (OpenReview Vusd1Hw2D9, 2025) — debate-based output judges.

Why it doesn't cover us: **all post-hoc**. Inputs are generated outputs, not pre-decision design questions. Coverage of output-grading is functionally complete; building another would be redundant.

Notable risk surfaced: *"Jury-of-LLMs evaluation is at risk of being initial-vote-dependent, where panel members anchor on first impressions and rarely revise them"* — validates the anti-anchoring concern as real, even though the research is for output panels.

### Multi-agent debate for factuality (closed)

Status: **active research area; converging on court-style frameworks.**

- **Du et al., "Improving Factuality and Reasoning in Language Models with Multiagent Debate"** ([composable-models.github.io/llm_debate](https://composable-models.github.io/llm_debate/)) — agents critique each other's reasoning; majority on math / factuality.
- **CourtEval** — three roles: Grader (Judge), Critic (Prosecutor), Defender (Defense). Used for safety + factuality evaluation.
- **Heterogeneous Debate Engine** (arXiv 2603.27404, 2026) — identity-grounded cognitive architecture for ethical tutoring.
- **Adversarial Multi-Agent Evaluation through Iterative Debates** (OpenReview 06ZvHHBR0i / arXiv 2410.04663) — iterative debate for evaluation.
- **AgentCourt**, **AgenticSimLaw** — courtroom simulation for high-stakes decisions.

Why it doesn't cover us: targets *output factuality* and *claim verification*. None target a design question authored by the user *before* generation. Court-style is closer in shape but presumes a verdict on a fact, not a recommendation on a design.

### AI code review (closed)

Status: **commercially saturated, 2024–2026.**

- **CodeRabbit** — PR review SaaS.
- **Greptile** — repo-aware AI code review.
- **Qodo** (formerly Codium AI) — test-and-review coverage.
- **Sourcery** — AI refactoring suggestions.
- **Korbit** — engineering-team-focused PR review.
- **Codacy** + AI extensions.
- **Cursor review** mode.
- **Aider review** modes.
- **Devin review** (Cognition Labs).
- **GitHub Copilot Workspace** review affordances.
- **Sweep AI** auto-PR-fix.

Why it doesn't cover us: targets *PR diffs* or *whole-repo code*. Not design questions. Commercial saturation means a stack that drifted toward "design review for code" would be solving a solved problem.

### Adversarial code review patterns (closed)

Status: **patterns documented; multiple implementations.**

- [Adversarial Code Review pattern (ASDLC.io)](https://asdlc.io/patterns/adversarial-code-review/) — distinct critic agent reviews builder-agent code against spec.
- [Open-source 4-agent adversarial code review team](https://dev.to/frank_brsrk/i-open-sourced-a-4-agent-adversarial-code-review-team-any-coding-agent-can-call-it-as-an-mcp-36oe) — MCP server callable by any coding agent.
- **Anthropic three-agent (planner / generator / evaluator)** — GAN-inspired separation of generation from evaluation.
- **SCOUT / GUARD** pattern — adversarial stress-test (2 agents, not panel).

Why it doesn't cover us: code-level targets, two-agent or single-orchestrator-evaluator pairs. None implement minority-veto across three lens roles, none have a frame-challenger before generation.

### Multi-lens veto panels for outputs (closest match — Team of Rivals)

Status: **directly addressed by Vijayaraghavan et al. (Jan 2026), but for post-hoc output review.**

- **"If You Want Coherence, Orchestrate a Team of Rivals: Multi-Agent Models of Organizational Intelligence"** — [arXiv 2601.14351](https://arxiv.org/abs/2601.14351), Vijayaraghavan et al., Isotopes AI, January 2026.
- Implements: AI office of specialists; veto authority per critic; unanimous-approval gate; CodeCritique / ChartCritique / OutputCritique / PlanCritique as named lenses; Swiss-cheese model + stage-gated oversight.

What it shares with claude-critic-stack: multi-lens veto, role-orthogonal critics, structural separation between perception (planning/reasoning) and execution.

What it does *not* share (verified via WebFetch on the abstract):

| Feature | claude-critic-stack | Team of Rivals |
|---|---|---|
| Pre-decision review of design questions | ✓ | ✗ (post-hoc on generated artifacts) |
| Frame-challenger as separate gated agent before generation | ✓ | ✗ |
| Reference-class forecasting / outside-view as mandatory step | ✓ | ✗ |
| Anti-anchoring via subagent-distiller artifact (raw stays on disk) | ✓ | ✗ (architectural separation, not artifact-discipline) |
| Canon-first retrieval with mandatory contradicting passage | ✓ | ✗ |
| Hard gates on `scope-map.md` + `challenges.md` before generation | ✓ | ✗ |
| Workflow as a fixed 12-step recipe with named artifacts | ✓ | implements role-based architecture, not a step-locked recipe |

This is the closest *system-level* match. It validates many of the same intuitions (rivals, veto, role-orthogonal critics) and proves the value-proposition is at least defensible. It also bounds the claim of novelty: anyone who hears "multi-lens veto for AI" should be told about Team of Rivals.

### Devil's Advocate as introspection (closed)

- **Wang et al., "Devil's Advocate: Anticipatory Reflection for LLM Agents"** — [arXiv 2405.16334](https://arxiv.org/abs/2405.16334), EMNLP 2024 Findings.
- Three-fold introspective intervention by **the same agent**: anticipatory reflection, post-action alignment, comprehensive review on plan completion.
- Open-source: [Wingtail/devils-advocate](https://github.com/Wingtail/devils-advocate).

Why it doesn't cover us: same-agent introspection, not a separate frame-challenger gate. Our `frame-challenger.md` agent runs *before* generation and is invoked by the orchestrator as a hard precondition; Wang et al.'s pattern lives inside one agent's reasoning trace.

### Premortem via AI (closed as technique)

- [Premortem skill on explainx.ai](https://explainx.ai/skills/parcadei/continuous-claude-v3/premortem)
- [Civil Learning, "Ask Claude to Predict Your Failure: The Premortem Method"](https://civillearning.medium.com/ask-claude-to-predict-your-failure-the-premortem-method-d1c0ce8d914d) (May 2026)
- [alfred_, "The Pre-Mortem"](https://get-alfred.ai/blog/pre-mortem-technique)
- [Adaptive Planning: Comparing Human and AI Responses in Premortem Planning](https://link.springer.com/content/pdf/10.1007/978-3-031-76827-9_15)

Status: **technique is widely known**; multiple implementations exist as skills, prompts, blog posts. None implement it as a *workflow primitive* with a hard gate. Closest in shape is the `frame-challenger` step but the connection is not stated in our docs and may be worth naming.

### Reference-class forecasting + LLMs (research, not primitive)

- [AI-Augmented Predictions: LLM Assistants Improve Human Forecasting Accuracy](https://arxiv.org/abs/2402.07862) — assistant designed for "superforecasting advice" raised prediction accuracy 24–28%.
- [ForecastBench](https://forum.effectivealtruism.org/posts/zwzgR8iuFEcJms3Hu/announcing-forecastbench-a-new-benchmark-for-ai-and-human-forecasting) — AI-vs-human forecasting benchmark.
- [Reference Class Forecasting (Wikipedia / Flyvbjerg)](https://en.wikipedia.org/wiki/Reference_class_forecasting).
- [Reference class forecasting: promises, problems, and a research agenda moving forward (Tandfonline 2025)](https://www.tandfonline.com/doi/full/10.1080/09537287.2025.2578708).

Status: **research artifacts and benchmarks exist; no integrated workflow primitive**. Our `outside-view` agent operationalizes this as a mandatory step with canon-first ordering. That is rare in the surveyed literature.

## What is genuinely open — the actual claim

The slice that remains genuinely open is **the combination of all of the following, executed as one prescriptive workflow**:

1. **Pre-decision** review of a *design question* (not outputs, not code, not contracts, not academic papers).
2. **Three-lens minority-veto panel** with role-orthogonal critics (architecture / operations / product).
3. **Frame-challenger as a separate, gated agent** before generation.
4. **Reference-class forecasting** (outside-view) as a mandatory workflow step.
5. **Anti-anchoring via on-disk subagent-distiller artifacts** — raw subagent output stays on disk; only distillations reach the orchestrator.
6. **Canon-first retrieval** with anti-confirmation-bias rules (must return contradicting passages).
7. **Hard gates** between steps (refuse to proceed without `scope-map.md` + `challenges.md`).

No surveyed system combines all seven. The closest is Team of Rivals, which has (2) but for post-hoc output review and lacks (1), (3), (4), (5), (6), (7). Anthropic's planner/generator/evaluator has parts of (2) but as a 2-3 agent pattern, not as a 12-step workflow with named artifacts and hard gates.

**Honest framing for the mission section:** *"This stack exists to apply structured adversarial review to pre-decision design questions, against a named set of LLM failure modes."* Stronger claims (e.g., "first system to do X") would not survive contact with Team of Rivals or the multi-agent-debate literature. Weaker claims (e.g., "another LLM judge") would be wrong.

## Counter-evidence — humility about multi-agent

These results argue we should be careful about *universalizing* the stack's value:

- [**"Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets"**](https://arxiv.org/abs/2604.02460) — under fixed compute, a single agent often wins. Implication: the stack's multi-agent decomposition pays for itself only when *frame error* is the binding constraint, not when raw reasoning depth is.
- [**"Multi-Agent Teams Hold Experts Back"**](https://arxiv.org/abs/2602.01011) — multi-agent panels can suppress strong individual reasoning.
- [**"Why Do Multi-Agent LLM Systems Fail?"** (Cemri et al., arXiv 2503.13657)](https://arxiv.org/pdf/2503.13657) — failure-mode taxonomy for multi-agent systems.
- [**"When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate"** (Nature Scientific Reports 2026)](https://www.nature.com/articles/s41598-026-42705-7) — a single persuasive adversary can disrupt panel verdicts. Implication: the panel's robustness against a confident-but-wrong lens is unmeasured.
- **Anthropic's own multi-agent research** preferred a single well-prompted judge with a rubric over multi-judge for output evaluation. Implication: for graded evaluation, the panel may be overkill; this stack's value depends on the design-question target where holistic judgment matters.

The mission text must not over-claim. The stack is well-suited to questions where the dominant failure mode is *the frame*, not the reasoning depth.

## Drift surface — where Phase 2 weakened the founding contract

Verified by reading `.genesis/`:

- **Phase 1** ([`.genesis/architecture-review.md`](../../../.genesis/architecture-review.md)): single-critic 6-step workflow on shared input. Five-pressures intact. No target-repo concept.
- **Phase 2** ([`.genesis/ok-cool-this-is-warm-balloon.md`](../../../.genesis/ok-cool-this-is-warm-balloon.md)): decomposes critic into three lenses (architecture / operations / product); adds `Explore` step at position 5; introduces `subagent-distiller`, `scope-mapper`, `frame-challenger`. **Does not re-state success criteria under the new shape.**

The drift surface is at the seam: Phase 2 silently widened the stack's surface (target-repo grounding, three lenses, more agents) without naming what success now looks like. Three concrete consequences:

- The "three independent critics" colloquialism became plausible because no doc said "they are role-orthogonal on shared input."
- The Explore + critique-prep + critique-start additions never had to justify themselves against the five pressures.
- The shadow-comparator entry (`upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md`) had to recover the missing decorrelation reasoning *after the fact*.

**Resolution:** add an addendum to `.genesis/` (do not edit the founding docs) marking the Phase 2 widening and noting the absence of re-stated success criteria. This becomes the locator for any future "is the stack drifting?" check.

## Proposed mission text for README.md

Final, non-compromising. To be added as a top-level `## Mission` section in [README.md](../../../README.md), positioned at the bottom (after existing content) so it serves as the audit anchor:

```markdown
## Mission

**This stack exists to apply structured adversarial review to pre-decision
design questions** — the kind of questions a senior engineer asks before
writing any code, where the dominant failure mode is *frame error* (solving
the wrong problem confidently) rather than *implementation error* (solving
the right problem incorrectly).

It is built against five named LLM failure modes (see [.genesis/five-pressures.md](.genesis/five-pressures.md)):

1. **Reframe-before-answer** — accepting the user's framing uncritically.
2. **Enumerate-before-select** — recommending the first option without comparison.
3. **Outside-view-first** — inside-view detail-reasoning that misses base rates.
4. **Name-your-uncertainty** — equally-confident prose regardless of actual confidence.
5. **Consequence-imagine** — recommending patterns without modelling failure modes.

It is **not** a code reviewer, **not** a post-hoc output grader, **not** an
RFP/contract/document review tool. Those slices are well-served elsewhere
(CodeRabbit, Greptile, Qodo, Prometheus, G-Eval, FACTS Grounding,
Vijayaraghavan et al.'s "Team of Rivals" — arXiv 2601.14351).

**What it claims to be:**
- A fixed adversarial-review workflow (12 steps), not a soft pattern.
- Multi-lens (architecture / operations / product), with minority-veto.
- Anti-anchoring by artifact discipline — raw subagent output stays on disk;
  only distillations reach the orchestrator.
- Canon-first and outside-view-first by *mandatory step ordering*, not by prompt.

**What it does not claim:**
- *Information independence* between lenses. Lenses share a common
  candidate; decorrelation is by **role/aspect** (different prompts ask
  different questions) and optionally by **model family**
  (`SHADOW_PANEL=1`). Inter-input independence is not enforced.
- *Universal superiority* of multi-agent decomposition. Recent results
  ([arXiv 2604.02460](https://arxiv.org/abs/2604.02460),
  [2602.01011](https://arxiv.org/abs/2602.01011),
  [2503.13657](https://arxiv.org/pdf/2503.13657)) show multi-agent often
  loses to a single well-prompted judge on simpler tasks. Use this stack
  when frame error is plausibly the binding constraint; otherwise, don't.

**Drift detection.** A claim that this stack is "three independent critics"
is wrong as written. The stated property is the one above. If a future
edit silently re-introduces a stronger claim, that is regression. The
ledger schema and this Mission section are the audit anchors.
```

## Open questions — for ultraplan

Ordered roughly by decision-blocking weight:

1. **Is the mission section the right placement, or should it be a separate `MISSION.md`?** A separate file is more discoverable from a fresh clone (less scrolling) but less cohesive with the existing README. Trade-off: discoverability vs. cohesion.

2. **Should CLAUDE.md cross-reference the Mission?** Current operator preference: cautious ("don't pollute"). One option: a single line in CLAUDE.md §"Default behavior" pointing to README §Mission, no rewrite. Another option: leave CLAUDE.md untouched; Mission lives in README only, drift detection is a manual exercise. Strongest option (rejected pre-emptively for CLAUDE.md hygiene): rewrite CLAUDE.md preamble around the Mission. Decision deferred to ultraplan.

3. **Should the `.genesis/` addendum be a new file or an edit to an existing one?** Founding-docs hygiene says *new file* (preserve original intent as written). Practical readability says *edit the index* if there is one. Verify whether `.genesis/` has an index file before deciding.

4. **Does the mission text foreclose future expansion?** The phrase "It is **not** a code reviewer" makes a hard exclusion. If the stack later genuinely *does* code review (e.g., via a new lens), the text needs revision. Trade-off: clarity now vs. flexibility later. Default: clarity now; revisions are a feature, not a defect.

5. **Should the comparison to Team of Rivals be more prominent or less?** It is the closest published match. Naming it directly is honest and keeps drift-detection sharp. But it also frames the stack as "Team of Rivals + 6 things," which understates the original framing-failure-mode angle.

6. **Is the "five named LLM failure modes" the right anchor, or should the Mission anchor on something else?** The five pressures are founding intent but they are *failure modes*, not *positive outcomes*. A Mission that names only what the stack avoids may be incomplete. Counter: the stack's value *is* avoidance of those failure modes. Verdict probably "yes, anchor on five pressures" but worth challenging.

7. **What is the cheapest forward-test of "the gap is real"?** Possibilities: (a) feed an existing design question to ChatGPT-with-search and to claude-critic-stack and compare verdicts — but this is a slow N=1; (b) survey users (you have an N of one — yourself — and you cannot survey yourself unbiased); (c) wait for the Team of Rivals paper to be cited by something that *does* attempt design-question pre-review and treat that as the actual ground truth.

8. **Has anyone built a `claude-critic-stack` shaped thing privately at a company?** Anthropic, OpenAI, DeepMind, Microsoft, Google all have internal review processes. Any of them could be running an adversarial-review workflow on design questions internally. Public evidence is silent. Implication: even if the gap looks open externally, it may be filled internally.

9. **What is the right cadence to re-run this SOTA survey?** The field moves fast. A six-month re-survey discipline would catch new entrants. Possible cadence: every 6 months, or on any major Claude/GPT release. Currently nothing in the repo schedules this.

10. **Should the existing "three independent critics" colloquialism be hunted down everywhere it appears?** Grep across all repo files would surface every occurrence. Some may be in upgrade entries, which `feedback_lab_is_creative_hub` says are not edited by cleanup. Path-discipline-style discipline says: name the rule once in Mission, leave existing usages, but never write it again.

11. **Is there a benchmark we should produce?** A "design-question review" benchmark — a set of design questions with expert-judged verdicts — would let any tool (claude-critic-stack, Team of Rivals, ChatGPT) be measured. None exists publicly. Building one is a significant project but might be the highest-leverage move for proving the gap is real.

12. **What is the relationship between the Mission and the existing five-pressures?** The five-pressures are the *defense*. The Mission is the *positioning*. They serve different audiences. Should they live in the same place or be cross-referenced from different homes?

13. **Is "frame error vs. implementation error" the right axis?** The Mission text uses this binary. Real failure modes are mixed. A more honest text might say "the stack defends against frame error specifically among the five named modes; implementation error is out of scope." Worth ultraplan attention.

14. **Should a Sources / SOTA-comparison file live in the repo, or only in this upgrade entry?** This entry has the full survey. A condensed comparison-matrix file (perhaps `docs/sota-comparison.md`) would be more discoverable but creates a maintenance burden. Trade-off: discoverability vs. hygiene.

## What ships from this entry

This upgrade entry does not itself ship code or doc edits. It is **input to ultraplan**. Two adjacent decisions are loosely coupled to it:

- **Mission section in [README.md](../../../README.md).** Operator may take the proposed text directly (low-risk, additive) or run it through ultraplan first (higher-quality, slower).
- **CLAUDE.md cross-reference.** Operator was cautious about polluting CLAUDE.md. Default: skip. Open question 2 holds the decision.

The SOTA survey itself is the deliverable and lives here. If ultraplan produces a different mission text, this entry remains the SOTA evidence base regardless.

## Why this is profound, not normal

A normal upgrade is a defined change with a measurable acceptance test. This entry is **a recalibration of the stack's stated purpose**, grounded in evidence that wasn't previously gathered. The downstream changes it implies — Mission section, drift addendum, possible CLAUDE.md cross-reference, possible benchmark project — are individually small but their *coherence* depends on this evidence base. Profound entries are the ones that change what subsequent normals are *for*; this one does that.

It also belongs in `profound` because it is the kind of work that, if the stack drifts again in 6 months, this entry is what a future operator (or model) would re-read to figure out what we thought we were doing. That is the lab's role per [`upgrades/profound/2026-04-27-r-and-d-lab-thesis/README.md`](../../profound/2026-04-27-r-and-d-lab-thesis/README.md).

## Sources

### LLM-as-judge & multi-agent debate

- [When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation for LLMs](https://arxiv.org/html/2508.02994v1)
- [Multi-Agent Debate for LLM Judges with Adaptive Stability Detection (OpenReview)](https://openreview.net/forum?id=Vusd1Hw2D9)
- [Multi-Agent-as-Judge: Aligning LLM-Agent-Based Automated Evaluation with Multi-Dimensional Human Evaluation](https://arxiv.org/html/2507.21028v1)
- [Efficient LLM Safety Evaluation through Multi-Agent Debate](https://arxiv.org/html/2511.06396)
- [LLM-As-Judge: 7 Best Practices & Evaluation Templates (Monte Carlo Data)](https://www.montecarlodata.com/blog-llm-as-judge/)
- [LLM-as-a-judge: a complete guide (Evidently AI)](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [LLM as a Judge — Primer and Pre-Built Evaluators (Arize)](https://arize.com/llm-as-a-judge/)
- [Improving Factuality and Reasoning in Language Models with Multiagent Debate (Du et al.)](https://composable-models.github.io/llm_debate/)
- [Adversarial Multi-Agent Evaluation of Large Language Models through Iterative Debates (arXiv 2410.04663)](https://arxiv.org/html/2410.04663v1)
- [Heterogeneous Debate Engine: Identity-Grounded Cognitive Architecture for Resilient LLM-Based Ethical Tutoring](https://arxiv.org/html/2603.27404v1)
- [Courtroom-Style Multi-Agent Debate with Progressive RAG and Role-Switching for Controversial Claim Verification](https://arxiv.org/html/2603.28488v1)
- [Adaptive heterogeneous multi-agent debate for enhanced educational and factual reasoning](https://link.springer.com/article/10.1007/s44443-025-00353-3)

### Multi-lens veto panels (closest match)

- [If You Want Coherence, Orchestrate a Team of Rivals: Multi-Agent Models of Organizational Intelligence (arXiv 2601.14351)](https://arxiv.org/abs/2601.14351)
- [alphaXiv mirror](https://www.alphaxiv.org/abs/2601.14351)
- [Team of Rivals: Isotopes AI's Multi-Agent Architecture for Reliability (YouTube)](https://www.youtube.com/watch?v=z5sV4n8Pjs4)

### Devil's Advocate / introspection

- [Devil's Advocate: Anticipatory Reflection for LLM Agents (arXiv 2405.16334)](https://arxiv.org/abs/2405.16334)
- [Devil's Advocate (ACL Anthology PDF)](https://aclanthology.org/2024.findings-emnlp.53.pdf)
- [Wingtail/devils-advocate (GitHub)](https://github.com/Wingtail/devils-advocate)
- [Don't Just Translate, Agitate: Using Large Language Models as Devil's Advocates for AI Explanations](https://arxiv.org/html/2504.12424v1)
- [Modern Impact, "Is Your LLM Creating an Echo Chamber?"](https://www.modernimpact.com/is-your-llm-creating-an-echo-chamber/)

### Adversarial code review

- [Adversarial Code Review pattern (ASDLC.io)](https://asdlc.io/patterns/adversarial-code-review/)
- [I open-sourced a 4-agent adversarial code review team (DEV Community)](https://dev.to/frank_brsrk/i-open-sourced-a-4-agent-adversarial-code-review-team-any-coding-agent-can-call-it-as-an-mcp-36oe)
- [Orchestrating AI Agents: A Subagent Architecture (Clouatre)](https://clouatre.ca/posts/orchestrating-ai-agents-subagent-architecture/)
- [Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Anthropic — Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Claude Agent SDK & Managed Agents (Zylos Research)](https://zylos.ai/research/2026-04-20-claude-agent-sdk-managed-agents-architecture)
- [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems (arXiv 2604.14228)](https://arxiv.org/html/2604.14228v1)
- [AddyOsmani — Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/)

### Reference-class forecasting / superforecasting + LLMs

- [AI-Augmented Predictions: LLM Assistants Improve Human Forecasting Accuracy (arXiv 2402.07862)](https://arxiv.org/abs/2402.07862)
- [Reference class forecasting (Wikipedia)](https://en.wikipedia.org/wiki/Reference_class_forecasting)
- [Superforecasting LLM (Emergent Mind)](https://www.emergentmind.com/topics/superforecasting-llm)
- [ForecastBench (EA Forum)](https://forum.effectivealtruism.org/posts/zwzgR8iuFEcJms3Hu/announcing-forecastbench-a-new-benchmark-for-ai-and-human-forecasting)
- [Reference class forecasting: promises, problems, and a research agenda (Tandfonline 2025)](https://www.tandfonline.com/doi/full/10.1080/09537287.2025.2578708)
- [Bayes and Base Rates (Morgan Stanley / Counterpoint Global)](https://www.morganstanley.com/im/publication/insights/articles/article_bayesandbaserates_ltr.pdf)
- [Bent Flyvbjerg — reference class forecasting paper (arXiv 1710.09419)](https://arxiv.org/pdf/1710.09419)

### Premortem via AI

- [Premortem skill (explainx.ai)](https://explainx.ai/skills/parcadei/continuous-claude-v3/premortem)
- [Civil Learning, "Ask Claude to Predict Your Failure" (Medium)](https://civillearning.medium.com/ask-claude-to-predict-your-failure-the-premortem-method-d1c0ce8d914d)
- [Adaptive Planning: Comparing Human and AI Responses in Premortem Planning (Springer)](https://link.springer.com/content/pdf/10.1007/978-3-031-76827-9_15)
- [The Pre-Mortem: Gary Klein's Technique (alfred_)](https://get-alfred.ai/blog/pre-mortem-technique)
- [Kepner-Tregoe — The "Premortem" technique to de-bias decisions](https://kepner-tregoe.com/blogs/the-premortem-technique-to-de-bias-decisions/)
- [The Premortem (Edge.org)](https://www.edge.org/response-detail/27174)

### Multi-agent counter-evidence

- [Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning (arXiv 2604.02460)](https://arxiv.org/abs/2604.02460)
- [Multi-Agent Teams Hold Experts Back (arXiv 2602.01011)](https://arxiv.org/abs/2602.01011)
- [Why Do Multi-Agent LLM Systems Fail? (Cemri et al., arXiv 2503.13657)](https://arxiv.org/pdf/2503.13657)
- [When collaboration fails: persuasion driven adversarial influence in multi agent LLM debate (Nature Sci Reports 2026)](https://www.nature.com/articles/s41598-026-42705-7)
- [LLM Multi-Agent Systems: Challenges and Open Problems (arXiv 2402.03578)](https://arxiv.org/html/2402.03578v2)
- [Rethinking the Bounds of LLM Reasoning: Are Multi-Agent Discussions the Key? (ACL 2024 / arXiv 2402.18272)](https://aclanthology.org/2024.acl-long.331.pdf)
- [Can LLM Agents Really Debate? A Controlled Study (arXiv 2511.07784)](https://arxiv.org/pdf/2511.07784)

### AI design / document review tooling (broader landscape)

- [Best AI for Document Review in 2026 (Leah AI)](https://leahai.com/blog/best-ai-document-review)
- [AI Tools for Academic Peer Review: What They Actually Check in 2026 (Thesify)](https://www.thesify.ai/blog/ai-tools-academic-peer-review)
- [AI Design Reviews: Ultimate 2026 Guide (Klay Studio)](https://www.theklaystudio.com/ai-design-reviews-ultimate-2026-guide/)
- [Top 7 AI Design Review Tools for Mid-to-Large Creative Teams in 2026](https://www.theklaystudio.com/top-7-ai-design-review-tools-for-mid-to-large-creative-teams-in-2026/)
- [Document AI Reviews & Ratings 2026 (Gartner Peer Insights)](https://www.gartner.com/reviews/product/document-ai)
- [GitHub — akashtalole/ai-document-review (Azure-based agentic document review accelerator)](https://github.com/akashtalole/ai-document-review)
- [PaperReview.ai Review 2026: Free AI, Clear Limits (Manusights)](https://manusights.com/blog/paperreview-ai-review-2026)

### Workflow / orchestration framing

- [LangGraph Multi-Agent Architecture: Building a Self-Critiquing AI Debate System (Towards AI)](https://towardsai.net/p/machine-learning/langgraph-multi-agent-architecture-building-a-self-critiquing-ai-debate-system)
- [The 2026 Guide to Agentic Workflow Architectures (Stack AI)](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures)
- [Best AI Models for Agentic Workflows in 2026 (MindStudio)](https://www.mindstudio.ai/blog/best-ai-models-agentic-workflows-2026)
- [Andrej Karpathy: The AI Workflow Shift Explained 2026](https://www.the-ai-corner.com/p/andrej-karpathy-ai-workflow-shift-agentic-era-2026)
- [LLM Council: A New Era of Multi-Model Intelligence (Medium / Manish Kumar)](https://medium.com/@manishmandal9734/llm-council-a-new-era-of-multi-model-intelligence-c59726b3d9c2)
- [GitHub All-Stars #10: llm-council — AI Consensus mechanism (VirtusLab)](https://virtuslab.com/blog/ai/llm-council)
- [Stop Letting LLMs Orchestrate Your AI Agents (Abdelaziz Notes)](https://www.abdelaziznotes.com/posts/stop-letting-llms-orchestrate-your-ai-agents)
- [What Is Claude Code Ultra Plan's Multi-Agent Architecture? Three Explorers Plus One Critic (MindStudio)](https://www.mindstudio.ai/blog/claude-code-ultra-plan-multi-agent-architecture)
- [Karpathy shares 'LLM Knowledge Base' architecture (VentureBeat)](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
- [LLMs Judging Architecture: Generative AI Mirrors Public Polls (Preprints.org 202508.0418)](https://www.preprints.org/manuscript/202508.0418)
- [GitHub — VoltAgent/awesome-ai-agent-papers (curated 2026 papers)](https://github.com/VoltAgent/awesome-ai-agent-papers)
- [A Graph-based Framework for Multi-Agent LLM Collaboration (arXiv 2604.17148)](https://arxiv.org/pdf/2604.17148)
- [Multi-Agent Collaboration Mechanisms: A Survey of LLMs (arXiv 2501.06322)](https://arxiv.org/html/2501.06322v1)
- [Practices for Governing Agentic AI Systems (Shavit, Agarwal et al., OpenAI)](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf)

### Method classics (cited as method, not as base rate)

- [Reference class forecasting — Wikipedia](https://en.wikipedia.org/wiki/Reference_class_forecasting)
- [Timid Choices and Bold Forecasts (Kahneman & Lovallo, 1993)](https://bear.warrington.ufl.edu/brenner/mar7588/Papers/kahneman-lovallo-mansci1993.pdf)
- [Site Reliability Engineering (Beyer, Jones, Petoff, Murphy eds.) — Ch. 32, Ch. 36, Ch. 15](https://sre.google/sre-book/table-of-contents/)
