# 05 — Shortlist

Six vectors selected from the long list of twenty-one. The selection is biased by the reframe in [03-reframe.md](03-reframe.md): close the loop first, prune the fat second, add capability third. Cuts and reasons are in [06-cuts.md](06-cuts.md).

The shortlist contains:

- **At least one removal** (S2: critic-panel collapse, fused with S5: ablation).
- **At least one foundational reframe** (S1: decision-record-as-substrate + calibration revisit).

## S1 — Decision-record-as-substrate plus calibration revisit (#1 + #2 + #15 fused)

**Position.** The most valuable change is to make the workflow produce a small, durable, machine-readable *decision record* on every run, and to add a single new agent that periodically revisits past records to score them against what actually happened. The synthesis becomes a view onto the record; calibration becomes the substrate against which every other proposal can be evaluated. Includes a hard gate so the residual-disagreement contract becomes mechanical, not prose.

**Why this beat the others.** Three reasons. First, every other proposal in the long list — additions, removals, refactors — *should* be evaluated against a calibration record, and there is currently nothing to evaluate against. Calibration is a precondition. Second, the literature the stack imports its discipline from (Tetlock, Flyvbjerg, Klein) is forecasting literature, and the entire edifice of forecasting-as-a-discipline is built on calibration; the stack is currently doing forecasting without the calibration. Third, this is the cheapest single move with the highest cascade — a small structured artifact unlocks revisit, retrieval, ablation, and outcome-aware ablation in turn.

**Tier.** Foundational.

**Costs.** New artifact format to design and version. A new agent to author and maintain. Operator-time obligation: revisits only work if the operator answers them, which is a real ongoing cost and the most likely failure mode. Some session-artifacts will need migration or grandfathering. The hard gate addition to the synthesis step is small but a behaviour change to step 12.

## S2 — Critic-panel collapse to one parametrised critic, plus ablation harness (#3 + #21)

**Position.** Replace the three lens files with one `critic` agent taking a `--lens` argument; let the orchestrator choose 1–3 lenses based on the question. Build an ablation harness coupled to the eval suite (S3 below) so this and every other future removal can be empirically defended. This is the **mandatory removal** per the brief.

**Why this beat the others.** Two reasons. First, the three lens files share an authoring voice, share ~80% of their skeleton, and produced *convergent* objections in the [Context7 session](../../.claude/session-artifacts/2026-04-26-context7-adoption-in-critic-stack/critiques.md) — three lenses naming the same shape of error from three angles. The triplication is paying for redundancy, not independence. Second, the same-model self-preference bias documented in Panickssery, Bowman, Feng (2024; arXiv:2404.13076) means three same-model lenses do not give three independent judges; they give one biased judge wearing three hats. Compressing surfaces this honestly.

**Tier.** Structural / removal.

**Costs.** Risk of losing the *prompt-level* pressure that the three files exert on each other (the critic-product file's anti-patterns differ from critic-architecture's; consolidating may lose that texture). Mitigated by the lens-as-section-template approach. Without the ablation harness in S3, this is a faith-based removal; with it, a defensible one. Modest implementation surface.

## S3 — Eval harness with paired scenarios and self-growth (#5 + #6)

**Position.** Build `evals/` containing N paired scenarios (two questions differing in one detail that should change the answer; the score asks whether the workflow noticed). Auto-graded with a separate grader prompt. Add `/promote-eval <session-id>` so real sessions can be canonicalised as evals. Run the suite on every change to an agent or to [CLAUDE.md](../../CLAUDE.md).

**Why this beat the others.** This is the *operational complement* to S1 (S1 measures real-world calibration; S3 measures workflow-internal correctness). Without S3, every refactor is a faith move; with it, the stack can shrink defensibly. The self-growth via promote-eval addresses the most likely failure mode of any test suite — that it ossifies into the operator's initial imagination of what the stack should do, not what it is actually used for.

**Tier.** Operational.

**Costs.** Auto-graders are themselves LLMs and have all the LLM-judge failure modes documented in Zheng et al. (2023; arXiv:2306.05685). Mitigation: pair each scenario with explicit *artifact-feature* checks (does `scope-map.md` contain row X with label `replace`?) that grade by pattern, not by model. The harness itself becomes maintenance surface — an additional thing to keep working — and adds wall-clock time to the change-iteration loop.

## S4 — Inverted librarian + corpus-coverage map (#7 + #8)

**Position.** Two coupled changes to the librarian. (a) Add a contradiction-first invocation mode used at step 9 or 10, where the librarian is given the *candidate* and asked to retrieve only what would refute it. (b) Promote gap-flagging to a *precondition*: the librarian's first emission for any query is a coverage map (what canon has full / stub / no coverage of), so the orchestrator can decide what to do about gaps before reading passages.

**Why this beat the others.** The current contradicting-passage requirement is structurally good but practically brittle when the corpus has only one voice on a topic — which is *most topics*, given the corpus shape documented in [02-reading-landscape.md](02-reading-landscape.md). Both changes address this: contradiction-first retrieval forces sharper opposition; coverage-map-first surfaces the brittleness rather than papering it over with stretched relevance.

**Tier.** Structural.

**Costs.** Additional retrieval pass per session (latency, tokens). The contradiction-first mode is a *new capability* of the librarian, and its quality depends on whether the corpus actually contains contradictions of typical candidates — for many topics it will not, which is exactly the failure the coverage map will surface. Modest implementation surface, but the diagnostic honesty may be uncomfortable: it will reveal that the stack's "must contradict" rule is often mechanically satisfied with weak passages.

## S5 — Retire the requirement-classifier; fold its work into the reframe (#14)

**Position.** Delete the [requirement-classifier](../../.claude/agents/requirement-classifier.md) agent. Move the label, the secondary label, the framing-words audit, and the gaps section into the reframe step (step 2) itself, performed by the orchestrator. Reduce the workflow from 12 steps to 11.

**Why this beat the others.** The classifier is a one-pass labeler that produces ~600 tokens; the reframe step that follows it has both the input and the context to do the same job. The two-hop structure forces the orchestrator to *re-read* the classifier output before reframing, which is a cost without an obvious benefit. Removing it tightens the reframe's accountability — the orchestrator owns both the label and the frame, and cannot defer one to the other. This is the **second removal** in the shortlist; together with S2 it argues for *less* total agent surface, not more.

**Tier.** Structural / removal.

**Costs.** Loses the explicit `## User's framing words` and `## Alternative classification` sections as *separately-authored* artifacts; the regression test in [tests/regression/ark-mono-connector-routing.md](../../tests/regression/ark-mono-connector-routing.md) currently asserts on `requirement.md` content and would need to assert on `frame.md` instead. Risk that folding the work into the orchestrator dilutes it because the orchestrator is busy. Mitigation: the reframe step's contract makes the labeling sub-section *required*, not optional — discipline preserved, hop saved. If S3 is not in place, this is risky to ship; with S3, the eval suite catches dilution.

## S6 — Pre-mortem mode (#10), pruned

**Position.** Add a single new operating mode where the workflow runs the first eight steps, then skips the generator, and instead runs a structured pre-mortem on the *most likely candidate* the orchestrator would have produced. Output is a written post-mortem-from-the-future. This is conceptually distinct from the frame-challenger (which operates on the frame) and from the critic-panel (which operates on the actual candidate).

**Why this beat the others.** Klein's pre-mortem evidence (HBR, 2007) is one of the few decision-quality interventions with both rigorous backing and minimal scaffolding. The stack does not currently do this; the frame-challenger is the closest primitive but operates on framing, not on the recommended path. Pre-mortems specifically catch the failure mode where the frame is right, the candidate is reasonable, and the implementation fails for reasons that were imaginable but not imagined.

**Tier.** Structural / minor.

**Costs.** New mode adds prompt mass and a new artifact (`pre-mortem.md`). The mode's distinctness from the existing critic-panel could blur — without care, pre-mortem becomes "another critic." Mitigation: pre-mortem refuses to evaluate the candidate; it *imagines forward* from the candidate. Smallest item on the shortlist; included because evidence-strength is high relative to surface area.

## What is *not* on the shortlist, named

S1–S6 contain **two foundational moves** (S1 reframes the substrate; S4 reframes retrieval), **two removals** (S2 and S5), **one operational backbone** (S3), and **one capability addition** (S6). I deliberately did not include any item that adds a *new agent* without an evaluation hook (cuts list explains).

Sequencing across the shortlist is in [08-sequencing.md](08-sequencing.md). The deep dives are in `07-deepdive-*.md` files, covering S1, S2+S3 paired, and S4.
