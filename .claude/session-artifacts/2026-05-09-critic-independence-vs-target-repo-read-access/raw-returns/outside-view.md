# Outside-view forecast — critic independence vs. target-repo read access

## 0. Canon-first note

Canon directory was not directly readable from this agent shell (directory listing tool unavailable in this run). Treating canon as **unconsulted in this pass** rather than fabricating citations. The reference classes below draw on web search; orchestrator should treat any specific number as web-sourced, not canon-promoted. Kahneman & Lovallo (1993), Tetlock, and Flyvbjerg are the methodological backbone but are invoked here as method, not as base-rate sources for this specific question — there is no megaproject database for "AI critic panels."

## 1. Reference class chosen

**Primary class: LLM-as-judge / model-graded evaluation systems where the judge is given access to grounding context (rubric, source artifact, retrieved passages) about the artifact under review.**

This is the closest analogue: an automated reviewer passing verdict on an artifact, with a knob controlling how much of the surrounding context the reviewer sees. The current literature (FACTS Grounding, RAGAS, RetrievalGroundedness judges, Gu et al. 2025 survey, "No Free Labels" 2025) is built almost entirely around the assumption that grounding the judge in the relevant context **improves** discrimination relative to ungrounded judgment — and that the dominant failure modes are bias *types* (position, length, self-preference, sycophancy) rather than information contamination.

**Secondary classes considered:**
- **Audit / familiarity threat (SOX, ISA 200).** Independence is operationalized as *economic and relational separation*, not *informational separation*. Auditors must read the books — that's the job. Familiarity threat is about *repeated exposure to the same auditee over time* and *social entanglement*, not about reading the artifact under audit.
- **Academic peer review (single- vs. double-blind).** Blinding is of *authorship*, not of *the work*. The reviewer always reads the paper. PNAS 2017 (Tomkins et al.) found single-blind reviewers favored famous authors — but this is an authorship-identity effect, not a content-grounding effect.
- **Red team / security.** Red teams are *required* to study the system to attack it credibly; their independence is structural (separate reporting line, separate incentives), not informational. "Black-box" red team exercises exist but are recognized as a weaker form of testing precisely because the team lacks grounding.
- **Code review (human).** Reviewers always read the code. Documented bias is *social* (collegiality with author, seniority asymmetry), not informational. There is no serious tradition of "blind code review where reviewer cannot see the code."

The user's framing — that target-repo read access threatens independence — does not have a strong analogue in any of these reference classes. Across audit, peer review, red team, code review, and LLM-as-judge, the dominant pattern is: **the reviewer reads the artifact; independence is enforced by relational/structural separation, not informational starvation.**

## 2. Base rate

**For "grounded reviewers/critics produce better verdicts than ungrounded ones":** the base rate is **high — roughly 70–85% in the LLM-as-judge literature** as a directional claim, qualitatively. Specific anchors:

- FACTS Grounding (DeepMind, 2025) and RAGAS treat grounding as *the* mechanism for reducing hallucinated critique — i.e., ungrounded judges are the failure mode being measured against.
- "No Free Labels" (arXiv 2503.05061) shows reference-grounded judges have higher human-agreement than ungrounded ones, with self-preference bias also reduced.
- Across audit, code review, and peer review, **zero** of the four established practices use information-blinding of the artifact as an independence mechanism. Independence is always relational.

For "information-isolation across reviewers improves panel discrimination": **base rate is low and mostly negative**. Inter-reviewer information variance generally produces *incommensurate* verdicts (different reviewers answering different questions), not better aggregate signal. This is the academic-peer-review failure mode where reviewer 2 read the paper and reviewer 3 skimmed the abstract.

## 3. Position relative to base rate

The proposal as currently framed (consider isolating critics from the target repo to protect independence) sits **below the base rate** of comparable interventions. Specific features pushing it down:

- **Wrong axis of independence.** Every comparable practice (audit, red team, peer review, code review, LLM-judge) operationalizes independence as *role/structural*, not informational. Pulling on the informational lever to fix correlation is unprecedented in the reference class.
- **Frame ambiguity not yet resolved.** Frame.md correctly notes that grounded vs. ungrounded critics are *answering different questions*. The base-rate finding is that mixing both modes in one panel without naming the mode produces the worst of both worlds (incommensurable verdicts, minority-veto over different objects).
- **The shadow comparator already addresses model-family correlation.** Adding informational isolation would add a *second* decorrelation mechanism aimed at a *different* correlation source, without evidence the second source is actually load-bearing. This is exactly the Kahneman–Lovallo "inside view" failure: solving a vivid local problem without checking whether it is the binding constraint.

Features that could lift it back to the base rate:
- An explicit threat model (frame.md hard-question 1) showing a documented case where shared target-repo exposure produced correlated lens approval.
- A declared *role for the panel* — "calibrated against deployable reality" vs. "judgment without priors" — so verdicts become commensurable.
- Treating informational isolation as **one lens's job**, not the panel's posture (e.g., one critic explicitly ungrounded, two grounded — diversity of inputs as a feature, not panel-wide isolation).

## 4. Typical failure mode at the base rate

Projects in the "tighten reviewer independence by restricting their inputs" reference class typically fail in one of two ways:

1. **Reviewers reject feasible designs and approve elegant-but-infeasible ones** (the calibration loss frame.md flagged). The verdict gets crisper but less correct. In LLM-judge work, this shows up as judges with high self-consistency but low human-agreement.
2. **The isolation is leaky and untracked.** Critic prompts include "the candidate," which references target-repo concepts, which leak the system into the critic's context anyway. The org now has a *claim* of independence it cannot honor — worse than admitting the dependency. This is the audit-firm failure mode (informal client influence the formal independence rules don't catch).

The signature symptom in the AI-critic context: **lens verdicts become more confident and more uniform**, while ground-truth quality of decisions does not improve. The panel feels sharper; the decisions don't get better. This is the most common LLM-eval failure.

## 5. Contradicting reference class

**Jury sequestration / blinded forensic analysis.** In US criminal trials and in some forensic disciplines (notably DNA mixture interpretation and fingerprint comparison post-Dror et al. 2006), context-blinding of the analyst/juror is *the* independence mechanism, and the empirical case for it is strong. Dror's "linear sequential unmasking" protocols show forensic examiners reach different conclusions when given case context vs. when blinded, and the blinded version is closer to ground truth.

This contradicts the primary class. The distinguishing feature: in forensic analysis, the analyst's job is **a narrow comparison task** ("does print A match print B") where context is genuinely irrelevant to the technical judgment but psychologically suggestive. If a critic-lens's job can be characterized that narrowly — e.g., "does this design satisfy invariant X" with X fully specified — then forensic-style blinding becomes the right reference class and the base rate flips.

The orchestrator should treat this as the **frame test**: if any lens's job is genuinely a narrow technical conformance check, blind it. If the lens's job is holistic judgment, ground it. The current panel (architecture / operations / product) reads as holistic, not narrow — but `critic-operations` in particular may be partially narrow (latency, cost, deploy invariants), and that lens is the most plausible candidate for partial isolation.

## 6. Outside-view verdict

**Below base rate, with a specific lift path.** The proposal as a panel-wide information-isolation move has no support in any comparable reference class and a strong contradicting base rate from LLM-as-judge work. It moves to **within tolerance** if the team (a) names a threat model, (b) declares the panel's job (calibrated vs. abstract), and (c) treats isolation as a per-lens choice tied to whether that lens's job is narrow-technical or holistic. Forensic-blinding is the only reference class where information-isolation has a strong empirical record, and it applies only to narrow tasks.

## Sources

- No Free Labels: Limitations of LLM-as-a-Judge Without Human Grounding (arXiv 2503.05061)
- Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (llm-judge-bias.github.io)
- A Survey on LLM-as-a-Judge (Gu et al., arXiv 2411.15594)
- FACTS Grounding benchmark (DeepMind, 2025)
- RetrievalGroundedness judge (Databricks docs)
- Auditor independence threats and malpractice claims (Journal of Accountancy, 2023)
- Reviewer bias in single- versus double-blind peer review (Tomkins et al., PNAS 2017)
- Code Review (Wikipedia summary, OECD reviews)
- AI Red Teaming (Mindgard, 2024)
- Reference class forecasting (Wikipedia summary)
- Timid Choices and Bold Forecasts (Kahneman & Lovallo, 1993)
- Linear Sequential Unmasking in forensic science (Dror et al., 2006 onward)
