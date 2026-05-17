# Critic Panels, Agent-as-Judge, and Triangulation Patterns

*Canonical 2026 reference for production AI workflows. Stack-agnostic.*

---

## 0. Thesis: model-as-judge is now a workflow primitive

In 2023, "use an LLM to grade outputs" was an evaluation convenience — a cheap proxy for human raters during offline benchmarking. By 2026 it has become a *load-bearing workflow primitive*: production pipelines route critical decisions through one or more LLM judges before commit, deploy, send, or merge. The judge is no longer in the lab. It is in the request path.

Three things changed. First, **evaluators became agents themselves** — agent-as-judge work (arXiv [2411.15594](https://arxiv.org/abs/2411.15594), [2508.02994](https://arxiv.org/abs/2508.02994), [2412.05579](https://arxiv.org/abs/2412.05579), [2601.05111](https://arxiv.org/abs/2601.05111)) established that evaluators with tools, retrieval, and memory catch defects single-pass LLM judges cannot. Second, the **single-judge baseline collapsed under correlated-error scrutiny**: arXiv [2506.07962](https://arxiv.org/abs/2506.07962) (ICML 2025) evaluated 350+ LLMs and found ~60% agreement *when both err* — with larger, more accurate models converging harder on shared failure modes. Third, **family bias was quantified**: arXiv [2508.06709](https://arxiv.org/abs/2508.06709) showed GPT-4o and Claude 3.5 Sonnet systematically rate same-family outputs higher than humans do; arXiv [2410.21819](https://arxiv.org/abs/2410.21819) traced it partly to perplexity (judges score familiar surface forms higher); arXiv [2604.06996](https://arxiv.org/abs/2604.06996) showed the bias persists *with explicit rubrics*, with up to 50% mis-marking on own outputs and 10-point score skews on subjective benchmarks.

A single LLM judge is biased; a same-family panel inherits that bias correlated across the panel; the bias survives explicit instructions to be fair. The mitigation is structural — panel composition, aggregation rule, and cross-family triangulation — not prompting.

### The cost-quality curve at panel sizes 1 / 3 / 5 / N

| Panel size | Typical cost vs single Opus-class judge | Marginal quality | Right for |
|-----------|------------------------------------------|------------------|-----------|
| 1 (single judge) | 1× | baseline | low-stakes batch eval, dev iteration |
| 3 (specialized lenses) | ~1.5–3× (depending on model tier) | catches lens-specific defects single judge misses | most production gates |
| 5–7 (PoLL of smaller models) | ~0.15× per [PoLL](https://arxiv.org/abs/2404.18796) when smaller models substitute | dominates single large judge on agreement-with-human | high-volume eval, leaderboards |
| N>7 | super-linear cost, sub-linear quality | diminishing returns; convergence to panel mode | almost never; use hierarchical escalation instead |

The PoLL result — "panel of smaller diverse models outperforms a single large judge at over 7× lower cost" ([Verga et al., arXiv 2404.18796](https://arxiv.org/abs/2404.18796)) — is the canonical reference and the reason "always run three judges" became a 2026 default rather than a luxury.

---

## 1. Single-model critique baselines (and why they are not enough)

### Reflexion ([arXiv 2303.11366](https://arxiv.org/abs/2303.11366))

Reflexion introduced *verbal* reinforcement: an agent attempts a task, receives feedback (scalar or natural-language), writes a self-reflection into an episodic memory buffer, and retries. On HumanEval, Reflexion took GPT-4 from 80% to 91% pass@1. The improvement is real and the mechanism is cheap (no weight updates).

### Self-Refine ([arXiv 2303.17651](https://arxiv.org/abs/2303.17651))

Self-Refine made the same move at a smaller scale: one model generates, then critiques its own output, then revises. Reported gains of ~20% absolute across seven task categories.

### Why the single-model loop is not enough

Both have a structural ceiling: critic and generator share *every* prior — corpus, reward model, prompt conventions, blind spots. Three failure modes: (1) **correlated error with self** — what the model cannot see in its output, it also cannot see when re-reading it; arXiv [2504.03846](https://arxiv.org/abs/2504.03846) found that *stronger models are worse at recognizing their own errors*; (2) **polish-to-local-maximum** — Self-Refine improves clarity and formality but rarely surfaces architectural or missing-requirement defects, since those require asking a question the generator did not consider; (3) **self-consistency is not a panel** — running the same judge N times draws N samples from one posterior, not N opinions, and arXiv [2511.00751](https://arxiv.org/abs/2511.00751) reports only a 0.4% gain on HotpotQA going from 1 to 20 samples once the problem is in-distribution.

Single-model self-review is useful as the *first* gate. It is not adequate as the *only* gate for decisions whose cost-of-error exceeds cost-of-review.

---

## 2. Multi-model critic panels: where the field actually is in 2026

### PoLL — Panel of LLM Evaluators ([Verga et al., arXiv 2404.18796](https://arxiv.org/abs/2404.18796))

*"Replacing Judges with Juries."* Three insights, durable through 2026:

- A panel of smaller diverse models from disjoint families correlates with human ratings *better* than a single large judge.
- The cost ratio is roughly 7× in favor of the panel.
- The diversity has to be real — disjoint model families, not three temperature samples from one model.

### Agent-as-Judge ([arXiv 2411.15594](https://arxiv.org/abs/2411.15594), [2508.02994](https://arxiv.org/abs/2508.02994), [2412.05579](https://arxiv.org/abs/2412.05579), [2601.05111](https://arxiv.org/abs/2601.05111))

LLM-as-judge is *fast and biased*; agent-as-judge is *slower and better calibrated*. The agent-judge has **tools** (run code, query databases, hit APIs), **retrieval** (fetch canon, prior decisions, related transcripts), **memory** (reference its prior verdicts; read the full conversation, not just the final answer), and **planning** (decide *how* to evaluate before evaluating). The 2026 survey ([arXiv 2601.05111](https://arxiv.org/abs/2601.05111)) names the boundary: agentic judges add value where verification requires *action* (run the tests, check the dependency graph) rather than *opinion*. Where verification is purely judgment, LLM-as-judge remains adequate.

### Petri ([Anthropic, October 2025](https://www.anthropic.com/research/petri-open-source-auditing))

Petri ("Parallel Exploration Tool for Risky Interactions") is the production-grade three-role loop. An **auditor agent** receives a seed instruction, plans a probe, and interacts with the **target model**. The auditor can **branch** (try alternative dialogue paths), **roll back** (undo a turn and re-probe), **prefill** (inject assistant-side content to test downstream behavior), **simulate tools** (provide fake tool outputs to test counterfactuals), and **early-terminate**. The **judge model** reads the *full transcript* and scores across a multi-dimensional rubric (36 dimensions in the released version).

Anthropic ran Petri across 14 frontier models and found alignment-relevant defects in every one, including their own. The architectural lessons generalize beyond safety auditing: (1) the judge must see the trajectory, not the destination — a final-answer-only judge misses reasoning failures that produced a correct-looking output; (2) the auditor needs branching authority — one-shot probes catch surface defects, branching probes catch conditional defects; (3) parallelism is the unit — many seed instructions concurrently, with *transcript-as-evidence* as the abstraction.

### Petri 2.0 ([Anthropic, January 2026](https://alignment.anthropic.com/2026/petri-v2/))

The January 2026 update added a **realism classifier** — a prompted classifier that monitors auditor behavior turn-by-turn and flags actions that look implausibly synthetic, requesting a rewrite *before* the content reaches the target. Combined with seed-instruction edits, this produced a **47.3% median relative drop in eval-awareness** on Claude models. The seed library grew to 181 scenarios including multi-agent collusion and professional/ethical conflict cases.

The lesson generalizes: **judges and auditors that are detectable as judges are partially captured by their detectability**. Targets that recognize they are being evaluated behave differently. The realism classifier is the production answer to that problem.

### Jury-on-Demand ([arXiv 2512.01786](https://arxiv.org/abs/2512.01786))

*Lazy* judge sampling. The system trains a reliability predictor over token distributions, embeddings, and structural input features; it predicts when a given judge is likely to agree with human experts on a given input. Easy cases get one judge. Borderline cases get more. On summarization and RAG benchmarks, the adaptive jury beats both single-judge and static-jury baselines on correlation with human experts, at lower expected cost than a fixed N-judge panel.

This matters because **panel cost is not the bottleneck most teams think it is** — judge invocation per action explodes faster than per-action token cost suggests. Jury-on-demand puts the cost where the uncertainty is.

### Lens specialization

The 2026 finding that has stabilized across teams: when the domains genuinely differ — architecture, operations, product, security, performance — *narrow specialist judges outperform a single generalist*. The generalist averages over all rubrics; the specialist applies the right rubric. The cost is that a specialist panel needs an aggregation rule that respects lens incommensurability (see §3).

---

## 3. Aggregation rules — picking how votes combine

The aggregation rule is the load-bearing choice in panel design. The wrong rule turns a good panel into a bad one.

### Majority vote (symmetric)

- **Bias:** type-II false-negatives. The panel misses real defects when most lenses cannot see them.
- **Right for:** subjective quality dimensions where any single judge's reject is suspect (style, tone, ranking tasks).
- **Wrong for:** safety, correctness, irreversible commits.

### Minority veto (any-rejection-blocks)

- **Bias:** type-I false-positives. The panel over-blocks; one paranoid lens can stop everything.
- **Right for:** irreversible operations (production deploy, money movement, destructive data writes), correctness gates where a missed defect is worse than a false alarm.
- **Wrong for:** dev-loop iteration where false alarms compound friction.

### Weighted vote (by calibration history)

Weight each judge by historical agreement with ground truth. Requires the infrastructure to track per-judge calibration over time. The right default once you have it; rarely justified before you have it.

### Confidence-weighted (with calibration discount)

Judges report verdict + self-reported confidence; aggregator weights by confidence × calibration discount (because raw self-reported confidence overstates accuracy — see §6). The calibration discount is non-negotiable; without it you re-introduce the overconfidence bias.

### Hierarchical escalation

Three cheap judges by default; when they disagree, escalate to a stronger judge. Cost-efficient and the correct generalization of jury-on-demand for shops without trained reliability predictors. The Petri-style architecture supports this naturally: the cheap judges score the transcript; on disagreement, a stronger judge re-reads with tools.

### When each rule is appropriate (decision table)

| Decision class | Aggregation rule |
|---------------|------------------|
| Irreversible commit / deploy / send | minority veto |
| Reversible action with monitoring | majority + escalation |
| Subjective ranking / quality scoring | weighted vote with calibration |
| High-volume eval / leaderboard | majority over PoLL |
| High-stakes one-off (architectural decision) | minority veto + cross-family shadow |

---

## 4. Cross-family triangulation — the 2026 load-bearing finding

The most important panel-design finding from 2024–2026 is that **same-family panels inherit family-correlated bias**. A three-Claude panel is a more confident version of one Claude. A three-OpenAI panel is a more confident version of one OpenAI.

The evidence chain:

- arXiv [2410.21819](https://arxiv.org/abs/2410.21819) — judges score outputs with lower perplexity (i.e., outputs that look like their own training distribution) higher than human raters do. The mechanism is *familiarity*, not *quality*.
- arXiv [2508.06709](https://arxiv.org/abs/2508.06709) ("Play Favorites") — across 5,000+ prompt-completion pairs and nine judges, both GPT-4o and Claude 3.5 Sonnet systematically rated same-family outputs higher, after controlling for quality via independent third-party judges.
- arXiv [2604.06996](https://arxiv.org/abs/2604.06996) — the bias persists *even with explicit rubrics*. Judges are up to 50% more likely to mark their own outputs as satisfying a rubric criterion; up to 10-point score skews on subjective benchmarks. Ensembling helps but does not eliminate the bias.
- arXiv [2504.03846](https://arxiv.org/abs/2504.03846) — part of the mechanism is *perplexity-as-familiarity*, but it is not the whole story; *stronger* models show *worse* harmful self-preference on tasks where they themselves err.
- arXiv [2509.26072](https://arxiv.org/abs/2509.26072) ("Silent Judge") — judges shortcut to surface features (length, hedging, formatting, recency, claimed provenance) and almost never disclose this in their justifications. Faithfulness failure: the model rationalizes the verdict in terms of content quality even when the actual driver was a surface cue.

**Operational implication.** An all-Anthropic panel reviewing Claude-generated output will systematically over-approve. An all-OpenAI panel reviewing GPT-generated output will systematically over-approve. Same-family panels are not a panel — they are a confidence amplifier on a biased single judge.

The mitigation is structural: include at least one judge from a *different model family* in any panel reviewing output generated by your primary model. The 2026 best practice is two-lane: a primary lane in your default family (for cost and integration), and a cross-family shadow lane (OpenAI / Llama / Qwen / Gemini / local Ollama, depending on what you are not using as your generator).

---

## 5. The shadow-lane pattern — voice, not vote

The shadow-lane pattern operationalizes cross-family triangulation without giving the shadow vote-changing authority. The pattern:

1. Run the primary panel (e.g., three same-family specialist lenses) to verdict.
2. In parallel, run a shadow panel of equivalent lenses on a *different model family*.
3. Run a **comparator agent** that reads both lanes and emits an agreement class per lens — `agree | partial-agree | disagree | unavailable`.
4. Primary lane retains verdict authority. Shadow output is *triangulation signal*, never a verdict change.

The phrase that captures it: **"voice not vote."** Shadow disagreement is information about the *robustness* of the verdict, not an input to the verdict itself. If primary approves and shadow disagrees, the candidate ships *but* the disagreement is surfaced in the synthesis as an explicit uncertainty.

Why the shadow does not vote: giving the shadow a vote turns the panel into a federated democracy across model families and re-introduces every aggregation pathology at the meta-level. Keeping the shadow informational keeps the architecture coherent.

The supporting literature:

- arXiv [2410.12853](https://arxiv.org/abs/2410.12853) ("Diversity of Thought Elicits Stronger Reasoning") — three different medium-capacity models (Gemini-Pro, Mixtral 8x7B, PaLM 2-M) debating to 91% on GSM-8K, beating GPT-4 alone; three copies of one model reached only 82%. *Diversity, not capability, drove the gap.*
- arXiv [2505.16997](https://arxiv.org/abs/2505.16997) (X-MAS) — across 27 LLMs, 5 domains, 21 test sets, 1.7M evaluations: heterogeneous multi-agent systems delivered up to 8.4% improvement on MATH (chatbot-only) and 47% on AIME (mixed chatbot-reasoner). Heterogeneity, not just multi-agent, is the driver.
- arXiv [2602.08003](https://arxiv.org/abs/2602.08003) — for ensemble selection, the most *diverse* pair beats the two *strongest*. The information-theoretic framing: a model that errs differently is more valuable than a model that scores higher.

**Practical comparator contract.** The comparator reads both lanes per lens, names the dimension of difference, and emits structured output: `{lens, agreement_class, dimension, primary_verdict, shadow_verdict, note}`. It does not say "the shadow is right" or "the primary is right." It says "they disagreed on dimension X" and lets the human (or the synthesis step) decide what to do with that.

---

## 6. Self-consistency vs panel — they are not the same thing

A frequent and costly confusion: **N self-consistency samples from one judge is not an N-judge panel**. It is one judge sampled N times.

- arXiv [2511.00751](https://arxiv.org/abs/2511.00751) — accuracy gains from increasing sampled reasoning paths are *minimal* (0.4% on HotpotQA across 20 samples) for problems already in-distribution. Additional paths add noise, not signal, once the model is reliable. The recommendation: use multi-path sampling only for problems that *demonstrably exceed* single-pass reliability.
- arXiv [2502.18581](https://arxiv.org/abs/2502.18581) — self-certainty (the model's own probability distribution as a quality signal) can substitute for an external reward model in Best-of-N, but the signal comes from the *generator's* distribution, not from any independent judgment.

The mental model:

- **Self-consistency** = sample the generator N times, pick the mode. Reduces sampling variance. Does not reduce model bias.
- **Panel** = sample N independent judges. Reduces both sampling variance *and* model bias *if and only if* the judges are independent in the relevant dimensions (family, training data, prompt scaffolding).

The shadow-lane pattern is what self-consistency was trying to approximate. Self-consistency approximates it badly because the samples are not independent — they share every prior.

---

## 7. Calibration of judges

Calibration is the discipline of making a judge's reported confidence match its actual accuracy. Without it, confidence-weighted aggregation amplifies noise.

### Metrics

- **ECE (Expected Calibration Error)** — average gap between confidence and accuracy across bucketed predictions. Low is good.
- **MCE (Maximum Calibration Error)** — worst-bucket gap. Important when downstream decisions are sensitive to confidence-tail behavior.
- **Brier score** — mean squared error of probabilistic predictions. Decomposes into reliability, resolution, and uncertainty.
- **LogLoss / cross-entropy** — proper scoring rule; penalizes overconfident-wrong harder than under-confident-wrong.

### The 2026 baseline

arXiv [2508.06225](https://arxiv.org/abs/2508.06225) reports that even the best LLM judges show ECE in the 0.12–0.40 range — i.e., when a judge says "I'm 90% confident," it is right anywhere from 50% to 78% of the time. The paper introduces the TH-Score metric for measuring confidence-accuracy alignment and argues for moving from accuracy-centric to *risk-aware* evaluation.

### Training fixes

- **RL with proper scoring rules.** Train judges with log-loss or tokenized Brier as the reward, not binary correctness. Forces the gradient to push down on overconfident-wrong predictions specifically.
- **Weak supervision against majority verdict.** Use the panel's majority as a stand-in for ground truth on production data; track per-judge agreement-with-majority over time; use that as the calibration discount in confidence-weighted aggregation.

### Versioning

When you upgrade your judge model (Opus 4.5 → 4.6, GPT-5.1 → 5.2), the calibration curve shifts. A confidence-weighted aggregator tuned to the old judge will mis-weight the new one. Either re-calibrate at every model upgrade or use rank-based aggregation less sensitive to absolute confidence values.

---

## 8. Eval-aware judges and how Petri 2.0 handles it

The Petri 2.0 finding generalizes beyond safety auditing: **a judge or target that recognizes it is being evaluated behaves differently**. Eval-awareness shows up as:

- Targets being unusually compliant when they detect evaluation framing.
- Auditors generating implausible scenarios that targets recognize as synthetic.
- Judges scoring more strictly when they recognize the candidate as "the kind of thing meant to be reviewed."

The Petri 2.0 mitigation — a **realism classifier** that monitors auditor behavior turn-by-turn and requests rewrites when the auditor looks synthetic — produced a 47.3% median relative drop in eval-awareness on Claude models. The seed-edit intervention alone produced 21.7%; the classifier alone produced 37.2%; combined was 47.3%. The complementarity matters: the classifier catches what the seed edits miss.

For non-Petri stacks, the practical mitigations:

1. **Phrase the candidate as the working task, not "this will be reviewed."** Frame the judge's input as the actual work product the judge would see in production, not as "below is a candidate, please critique."
2. **Sample blinded critics that do not know they are in critic role.** Periodically compare blinded-critic verdicts against marked-critic verdicts on the same input; the gap is a measure of how much eval-awareness is distorting the panel.
3. **Vary the prompt surface.** If every critic-panel invocation uses the same scaffolding, judges learn the scaffolding. Randomize the prompt presentation (order of dimensions, wording of rubric items) per invocation.

---

## 9. Petri-style judges with branching, rollback, and tool simulation (advanced)

The Petri primitive that does not yet have a wide non-safety analog is the **interactive judge**:

- **Clarification before verdict.** The judge can request clarification from the generator before voting. Catches more defects than one-shot review because many defects only become visible under a specific question.
- **Rollback and re-probe.** The judge can roll back to a previous turn and probe a different path. Catches conditional defects (the candidate is fine *if* condition X, broken *if* condition Y).
- **Tool simulation for counterfactuals.** The judge can simulate tool outputs the candidate did not actually receive, to test whether the candidate's logic is robust to inputs it has not yet seen.
- **Early termination.** The judge can declare a transcript converged before spending the full token budget; this is purely a cost optimization but it matters at scale.

For production workflows where the candidate is code or architecture (rather than a safety-relevant dialog), the analog is a judge with shell access, a sandboxed test runner, and read access to the repository. The judge does not just rate the candidate; it *executes the candidate against probes the generator did not consider*.

---

## 10. Structured verdict + confidence — the parseable judge contract

A 2026 production judge should always emit a structured suffix that the aggregator can parse without LLM-side parsing:

```
Verdict: <approve | rework | reject>
Confidence: <0.00–1.00>
Dimension: <lens-specific identifier, e.g., architecture.coupling>
Justification: <free text>
Evidence: <transcript-line citations, e.g., L42, L57–L60>
```

Why each field:

- **Verdict** as enum, not free text — the aggregator must be able to count without interpretation.
- **Confidence** as float — for confidence-weighted aggregation and for calibration tracking.
- **Dimension** as lens-specific identifier — preserves lens incommensurability; the aggregator can route per-dimension.
- **Justification** as free text — for human audit and for downstream agents that need to read the reasoning.
- **Evidence** as transcript-line citations — closes the gap between the verdict and the specific candidate content that produced it. Without this, judge output becomes uninspectable.

The contract is enforced at the agent definition; the aggregator rejects any judge output that does not include the structured suffix and re-prompts (or counts the judge as `unavailable` for this round, depending on the failure policy).

---

## 11. Production failure modes

### Correlated review error

arXiv [2506.07962](https://arxiv.org/abs/2506.07962) is the canonical reference. Same-architecture, same-provider, same-family panels show high error correlation; *more accurate* panels show *more* correlation. The implication: scaling up the panel by adding more of the same does not reduce error rate proportionally. Past N≈3 in a same-family panel, you are paying for very little additional independence.

### Judge degradation over model upgrades

The judge model is part of the system's version surface. When the underlying model changes — and on Anthropic, OpenAI, and Google APIs, the underlying model changes more often than the version string suggests — calibration curves shift, prompt sensitivity shifts, and the panel's effective behavior drifts. The mitigation is a calibration-tracking dataset that gets re-run at every judge model upgrade, with the panel re-tuned (or its confidence-weights re-fit) on the new behavior.

### Judge cost explosion

Naively wiring a three-lens panel on every action in a long-running agent produces a token bill that scales with `actions × lenses × transcript_length`. The transcript-length factor is usually the killer. Mitigations: (a) jury-on-demand for actions whose criticality is bounded; (b) summarization checkpoints that let judges read a compressed transcript; (c) hierarchical aggregation where cheap judges gate on whether the expensive judge runs at all.

### Same-family judging without acknowledging family bias

The default failure mode of teams adopting critic panels for the first time. They run three same-family judges, observe consistent verdicts, conclude the panel "works," and ship. The panel is consistent because it shares bias, not because it is correct. Cross-family shadow lane is the structural check; without it, the team has no observable signal for family bias.

### Eval-aware judges without realism classifier

Petri 2.0 specifically; the failure shows up as judges scoring strictly on inputs marked as "candidate" and leniently on the same inputs presented as work product. Without measurement, the gap is invisible.

### Judges that don't see the full transcript

Final-answer-only judges catch surface defects and miss reasoning defects. For any judge gating on correctness, the judge should read the trajectory that produced the answer, not just the answer. This is the central architectural lesson from Petri.

---

## 12. Anti-patterns

1. **Self-consistency presented as "a panel."** N draws from one posterior; not a panel.
2. **Same-family panel without cross-family shadow.** A confidence amplifier on a biased judge.
3. **Majority vote on irreversible operations.** Symmetric aggregation where asymmetric is needed; biases toward under-blocking real defects.
4. **Naive multi-agent debate as the *primary* verdict mechanism.** Debate is a candidate-generation pattern, not a verdict pattern. Use debate to surface positions, then judge.
5. **Hierarchies of hierarchies below N≈6.** "Supervisor of supervisors" over small panels is pure overhead; the supervisor cannot resolve what its panel could not.
6. **Judges without calibration tracking.** Confidence-weighted aggregation over uncalibrated judges amplifies the most overconfident judge.
7. **Judges that read only the final answer.** Miss every reasoning-trajectory defect.
8. **Eval-aware judges without a realism classifier or blinded sampling.** The eval-awareness gap is invisible without measurement.
9. **Same prompt scaffolding for every judge invocation.** Judges learn the scaffolding; randomize presentation.
10. **Shadow lane that votes.** Turns triangulation signal into a meta-level vote-aggregation problem; re-introduces every aggregation pathology.
11. **Generalist-only panel for genuinely multi-dimensional decisions.** Generalists average over dimensions; specialists apply the right rubric.
12. **One panel deciding both correctness and quality on the same call.** Different aggregation rules apply (veto for correctness, majority for quality). Split the call.

---

## 13. Top 12 critic-panel patterns, ranked by leverage

Highest-leverage first.

1. **Three specialist lenses with minority veto on irreversible operations.** Structure that converts the panel from a confidence amplifier into an actual gate. Cheapest meaningful upgrade over single-judge baselines.
2. **Cross-family shadow lane reporting agreement class to a comparator.** Voice not vote. Operationalizes triangulation without breaking the verdict architecture.
3. **Judge reads the full transcript, not just the final answer.** Lifted directly from Petri. The single largest quality improvement per unit of judge cost.
4. **Structured verdict + confidence + evidence-citation contract.** Makes the panel inspectable and the aggregator deterministic.
5. **Jury-on-demand: cheap default panel, expensive escalation on disagreement.** Puts cost where uncertainty is; correct generalization of hierarchical aggregation.
6. **PoLL of smaller diverse models for high-volume evaluation.** 7× cheaper, better human-correlation, at the cost of latency from sequential small-model calls.
7. **Realism classifier on the auditor side for any panel where targets might detect eval framing.** Petri 2.0's contribution; applies anywhere a judge interacts with a target.
8. **Calibration-tracking dataset re-run at every judge model upgrade.** The infrastructure investment that makes confidence-weighted aggregation honest.
9. **Petri-style interactive judges with branching and rollback for high-stakes decisions.** Expensive but catches conditional defects nothing else catches.
10. **Blinded-vs-marked critic sampling to measure eval-awareness gap.** Cheap probe; surfaces a failure mode otherwise invisible.
11. **Per-lens evidence citations linking verdict back to specific candidate spans.** Closes the audit loop; turns judge output from opinion into argument.
12. **Calibration discount on self-reported confidence; never use raw confidence in aggregation.** The single most common implementation bug in confidence-weighted aggregators.

---

## 14. The 2026 default

A reasonable default for a production AI workflow making meaningful decisions: three same-family specialist lenses in parallel; minority veto on irreversible operations and majority + escalation on reversible; a cross-family shadow lane on the same lenses with a comparator emitting agreement class (shadow does not vote); a structured verdict contract (verdict, confidence, dimension, justification, evidence citations); calibration tracking per judge per model version against majority-as-stand-in-for-truth; jury-on-demand escalation when primary and shadow disagree; judges that read full transcripts; and realism scaffolding on candidate presentation.

This is not the only good default. It is one that internalizes the load-bearing 2026 findings — correlated error, family bias, eval-awareness, calibration drift — and treats them as structural, not as things to mitigate with better prompting.

---

## Primary references

Single-model critique baselines:

- Shinn et al., [Reflexion (arXiv 2303.11366)](https://arxiv.org/abs/2303.11366)
- Madaan et al., [Self-Refine (arXiv 2303.17651)](https://arxiv.org/abs/2303.17651)

Panels and agent-as-judge:

- Verga et al., [PoLL: Replacing Judges with Juries (arXiv 2404.18796)](https://arxiv.org/abs/2404.18796)
- Zhuge et al., [Agent-as-a-Judge (arXiv 2411.15594)](https://arxiv.org/abs/2411.15594)
- [Agent-as-Judge follow-up (arXiv 2508.02994)](https://arxiv.org/abs/2508.02994)
- [LLMs-as-Judges Survey (arXiv 2412.05579)](https://arxiv.org/abs/2412.05579)
- You et al., [Agent-as-a-Judge 2026 Survey (arXiv 2601.05111)](https://arxiv.org/abs/2601.05111)
- Anthropic, [Petri open-source auditing tool, October 2025](https://www.anthropic.com/research/petri-open-source-auditing)
- Anthropic Alignment Science, [Petri 2.0: New Scenarios and Improved Eval-Awareness Mitigations, January 2026](https://alignment.anthropic.com/2026/petri-v2/)
- [Jury-on-Demand (arXiv 2512.01786)](https://arxiv.org/abs/2512.01786)

Family bias and judge pathologies:

- [Self-Preference Bias in LLM-as-a-Judge (arXiv 2410.21819)](https://arxiv.org/abs/2410.21819)
- [Play Favorites: Same-family rating bias (arXiv 2508.06709)](https://arxiv.org/abs/2508.06709)
- [Bias persists with explicit rubrics (arXiv 2604.06996)](https://arxiv.org/abs/2604.06996)
- [Do LLM Evaluators Prefer Themselves for a Reason? (arXiv 2504.03846)](https://arxiv.org/abs/2504.03846)
- [Silent Judge: shortcut to surface features (arXiv 2509.26072)](https://arxiv.org/abs/2509.26072)

Diversity, heterogeneity, ensemble selection:

- [Diversity of Thought Elicits Stronger Reasoning (arXiv 2410.12853)](https://arxiv.org/abs/2410.12853)
- [X-MAS: heterogeneous LLM multi-agent systems (arXiv 2505.16997)](https://arxiv.org/abs/2505.16997)
- [Ensemble selection: diversity beats raw strength (arXiv 2602.08003)](https://arxiv.org/abs/2602.08003)
- [Correlated errors across LLMs (arXiv 2506.07962)](https://arxiv.org/abs/2506.07962)

Self-consistency and calibration:

- [Self-consistency diminishing returns (arXiv 2511.00751)](https://arxiv.org/abs/2511.00751)
- [Best-of-N via self-certainty (arXiv 2502.18581)](https://arxiv.org/abs/2502.18581)
- [Judge calibration / TH-Score (arXiv 2508.06225)](https://arxiv.org/abs/2508.06225)
