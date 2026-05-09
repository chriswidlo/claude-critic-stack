# Distillation — outside-view

## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on whether restricting critics' read access to the target repo improves panel independence. Subagent declared canon **unconsulted** in this pass (canon directory not directly readable from its shell; refused to fabricate citations) and produced a forecast based on web-sourced reference classes. Verdict: below base rate with a specific lift path.

## Direct facts

1. [No Free Labels, arXiv 2503.05061] Reference-grounded judges show higher human-agreement than ungrounded ones, with self-preference bias also reduced. (confidence: direct)
2. [FACTS Grounding (DeepMind, 2025); RAGAS] Treat grounding as the mechanism for reducing hallucinated critique — ungrounded judges are the failure mode being measured against. (confidence: direct)
3. [Tomkins et al., PNAS 2017] Single-blind reviewers favored famous authors; this is an authorship-identity effect, not a content-grounding effect. (confidence: direct)
4. [Dror et al., 2006 onward — Linear Sequential Unmasking] Forensic examiners reach different conclusions when given case context vs. when blinded, and the blinded version is closer to ground truth. (confidence: direct)
5. [Subagent self-report] Canon directory was not directly readable in this run; canon treated as unconsulted rather than fabricated. (confidence: direct)

## Inferred claims

1. [outside-view] The closest reference class for the question is LLM-as-judge / model-graded evaluation systems; the literature there is built on the assumption that grounding the judge improves discrimination. (confidence: inferred)
2. [outside-view] Across audit (SOX/ISA 200), peer review (single-/double-blind), red team, and code review, **zero of four** practices use information-blinding of the artifact as an independence mechanism — independence is operationalized relationally/structurally, not informationally. (confidence: inferred)
3. [outside-view] Base rate that "grounded reviewers produce better verdicts than ungrounded ones" is ~70–85% directionally in LLM-as-judge literature. (confidence: inferred — subagent qualifies "qualitatively")
4. [outside-view] Base rate for "information-isolation across reviewers improves panel discrimination" is low and mostly negative; produces incommensurate verdicts. (confidence: inferred)
5. [outside-view] The shadow comparator already addresses model-family correlation; adding informational isolation would target a different correlation source without evidence that source is load-bearing — Kahneman–Lovallo inside-view failure. (confidence: inferred)
6. [outside-view] Typical failure mode #1: reviewers reject feasible designs and approve elegant-but-infeasible ones (verdicts get crisper but less correct; high self-consistency, low human-agreement). (confidence: inferred)
7. [outside-view] Typical failure mode #2: isolation is leaky and untracked — "candidate" prompt leaks target-repo concepts anyway; org gains a claim of independence it cannot honor. (confidence: inferred)
8. [outside-view] Forensic-blinding becomes the right reference class only when a lens's job is a **narrow technical conformance check** with the invariant fully specified; for holistic judgment, grounding wins. (confidence: inferred)
9. [outside-view] `critic-operations` is the most plausible candidate for partial isolation (narrow on latency/cost/deploy invariants); architecture and product read as holistic. (confidence: inferred)
10. [outside-view] Lift path to within-tolerance: (a) name a threat model, (b) declare the panel's job (calibrated vs. abstract), (c) treat isolation as per-lens choice tied to narrow-vs-holistic job. (confidence: inferred)

## Authority-framed claims

1. "Kahneman & Lovallo (1993), Tetlock, and Flyvbjerg are the methodological backbone but are invoked here as method, not as base-rate sources for this specific question" — underlying claim: methodology of reference-class forecasting; not used as base-rate source. Quote present in output: no. Confidence: unsupported (as base-rate input); used only as method.
2. "Kahneman–Lovallo 'inside view' failure: solving a vivid local problem without checking whether it is the binding constraint" — underlying claim: the proposal exhibits inside-view bias. Quote present in output: no. Confidence: unsupported (authority frame; no quote from Kahneman–Lovallo provided).
3. "Dror's 'linear sequential unmasking' protocols show forensic examiners reach different conclusions…" — underlying claim: blinded forensic analysis improves ground-truth proximity. Quote present in output: no, but cited as primary literature with year. Confidence: direct (specific protocol named, claim is the protocol's documented finding).

## Contradictions surfaced

- **Primary class (LLM-as-judge, audit, peer review, red team, code review)**: grounding the reviewer in the artifact improves verdict quality; independence is relational, not informational. → argues *against* isolating critics from target repo.
- **Contradicting class (jury sequestration, forensic blinding per Dror et al.)**: context-blinding is the independence mechanism and has strong empirical support. → argues *for* isolation, but only when the task is narrow technical comparison with a fully specified invariant.
- Resolution offered by subagent: pick reference class by per-lens job type (narrow vs. holistic). Subagent did not fully resolve which lenses qualify.

## Subagent's own verdict (verbatim)

"**Below base rate, with a specific lift path.** The proposal as a panel-wide information-isolation move has no support in any comparable reference class and a strong contradicting base rate from LLM-as-judge work. It moves to **within tolerance** if the team (a) names a threat model, (b) declares the panel's job (calibrated vs. abstract), and (c) treats isolation as a per-lens choice tied to whether that lens's job is narrow-technical or holistic."

## Gaps the subagent missed

- **Canon was not consulted.** Subagent self-flagged this. Orchestrator should re-invoke `canon-librarian` (already in this session's parallel batch — confirm distillation covers the same ground) or accept that outside-view is web-only here.
- **No quantified base rate for the forensic-blinding reference class.** Subagent gave a directional 70–85% for grounding-helps but no comparable number for blinding-helps-on-narrow-tasks.
- **No threat model produced.** Subagent flags that frame.md hard-question 1 needs a documented case of correlated lens approval from shared target exposure; subagent did not attempt to construct or find one.
- **`critic-product` and `critic-architecture` not analyzed for narrow sub-tasks.** Only `critic-operations` was named as a partial-isolation candidate; the other two were dismissed as holistic without decomposition.
- **No engagement with the shadow-comparator interaction.** Claim that shadow already handles model-family correlation is asserted; the question of whether informational isolation and model-family decorrelation could be complementary (rather than redundant) is not explored.

## Token budget
~850 tokens.
