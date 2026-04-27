# 09 — Risks to the entire plan

These are the things that, if true, would invalidate not just one proposal but the whole frame of the plan. Honest about the scenarios where the right move is *less*, not more.

## R1 — The operator does not actually want measurement

The plan is built on a reframe that says: the highest-leverage move is to instrument the stack so additions and removals can be evaluated. If the operator's honest goal is *to use the stack as it is, well, on a few hard decisions per quarter* — and not *to evolve the stack as a long-term R&D project* — then the calibration substrate (S1) is overhead and the eval harness (S3) is overengineering. The shortlist becomes mostly noise. The right move is two of S6 or S4 (incremental capability that does not require measurement to justify) and a quiet retreat from the rest.

**Signal that this risk is real:** the operator looks at the calibration-revisit cadence and answers honestly that they will not fill it in.

## R2 — The model capability assumption is wrong

The plan implicitly bets that model capability over the next 6–12 months will *not* eat the stack — that the structural properties (hard gates, audit trail, contradicting retrieval, frame-level objection capture) remain useful even as model reasoning improves. If a single Claude (or any model) with extended thinking can produce well-frame-challenged, well-contradicted reasoning in a single call by mid-2026, the stack's marginal value collapses, and most of the proposed work is wasted.

**Signal that this risk is real:** Anthropic ships, or peer labs ship, an inference-time-compute mode that demonstrably produces frame-challenged, contradicting-evidence-grounded reasoning at single-prompt scale, on the question classes the stack is used for.

The mitigation is partial: even if model capability subsumes the *reasoning* work, the *audit trail* property (versioned decision records, calibration revisits, ablation scoring) does not collapse — the trail is a property of the *system*, not the model. S1 specifically retains value under R2; S2, S3, S4 substantially lose value.

## R3 — The user-base assumption is wrong

The plan assumes the operator is the primary (perhaps sole) user, working alone, with operator-time as the binding constraint. If the stack's user base over the next 12 months will include teammates, the plan is significantly under-specified. *Multi-user* concerns (per-operator profiles done right, shared eval scenarios, cross-operator calibration aggregation, ADR export to team tooling) are barely touched in the long list — only #9, #16, #18 gesture at them, and all three are cut from the shortlist.

**Signal that this risk is real:** the operator names a teammate (or two, or an entire team) as a near-term user when reading this plan.

If R3 is real, the plan should be re-shaped to put #18 (synthesis-as-ADR export) and #9 (operator-bias profile, generalised to per-team) on the shortlist, and S5 (retire requirement-classifier) probably moves down — multi-operator workflows benefit more from explicit labeling, not less.

## R4 — The corpus is the actual bottleneck and nothing else matters until it's fixed

[02-reading-landscape.md](02-reading-landscape.md) and [01-reading-repo.md](01-reading-repo.md) document that the corpus is mostly stubs and Anthropic-engineering-heavy. If the *real* highest-leverage move is to spend the next quarter populating the canon (OCR'ing owned books, ingesting open-access papers, sourcing vendor-published essays for the topics the librarian is silent on), then S4's inverted-librarian work is downstream of corpus expansion and the rest of the plan is rearranging deck chairs.

**Signal that this risk is real:** running the cheapest experiment for S4 (manual coverage-map invocation on two recent sessions) shows that the librarian's coverage on most operator-actual queries is "stub-only" or "none", and the operator's reaction is *"yeah, this is the real problem."*

The mitigation is operational: corpus expansion is a different kind of work (slow, license-bound, rights-checking) and can run *in parallel* with S1 + S3 without competing for them. But if R4 is real and severe, the plan's prioritisation is wrong; S4 jumps to the head of the queue and the corpus-expansion work it depends on becomes the actual project.

## R5 — The reframe is parochial

The reframe in [03-reframe.md](03-reframe.md) says "close the outcome loop." But the *forecasting-tradition* analogy (Tetlock, Flyvbjerg, Klein) imports a discipline that fits *prediction* well and may fit *design decisions* less well than I claimed. Many design decisions do not have crisp resolved outcomes — they have continuous, partial, noisy signals over years, mediated by many other decisions. If the *outcome loop* in design is fundamentally underspecified relative to the outcome loop in forecasting, the calibration substrate (S1) is grading on noise and the revisit data is more illusion than signal.

**Signal that this risk is real:** after S1 ships and a quarter of revisits accumulate, the inter-revisit agreement on the *outcome as predicted?* axis is no better than chance, and the *frame correct?* axis is what carries all the signal.

This is partially anticipated in S1's failure modes. The mitigation is to lean harder on the *frame correct?* axis (which is more about whether the workflow asked the right question) and treat the outcome axis as a weak signal. If R5 is real, the plan does not collapse — it just becomes *the workflow auditing its own framings over time*, which is still valuable, but is a smaller claim than "calibrated forecasting machine."

## R6 — Goodhart on the eval harness

S3 builds a harness; S2 and S5 are defended against it. But once a metric is the basis for shipping decisions, the system optimises toward the metric. After ~12 months, the agents (and the operator's prompt edits) drift toward producing the *features* the harness checks for, whether or not the underlying reasoning is sound. The harness is now confirming a behaviour the agents have learned to perform, not a property the workflow has.

**Signal that this risk is real:** ablation deltas trend toward zero over time on every removal candidate — meaning every agent has learned to produce "correct" patterns even when its actual contribution is hollow.

This is the most serious risk in the plan and the one I am least confident is fully mitigated. The proposed mitigations (adversarial scenarios where features are present but reasoning is wrong; alternate-model graders) are partial and laborious.

## What the operator should take from this section

The plan is *not* a one-way door. Each shortlist item has a cheapest experiment that is itself a falsification test for the plan's premises:

- S1's experiment falsifies R1 (will the operator do the work?).
- S3's experiment falsifies R6 partially (can the harness even grade this scenario?).
- S4's experiment falsifies R4 (is corpus the bottleneck or is librarian behaviour the bottleneck?).

If any of those experiments come back negative, the plan should be re-shaped *before* the corresponding build. The order in [08-sequencing.md](08-sequencing.md) is deliberately constructed so the cheap experiments come first and the heavy builds come after the data.

If the operator's reaction to this section is *"I am most worried about R2 / R3"*, the right next conversation is about which model-capability and user-base assumptions the operator actually holds. The plan can adapt to either; it cannot adapt to both being unstated.
