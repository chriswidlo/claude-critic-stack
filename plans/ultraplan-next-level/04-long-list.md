# 04 — Long list of upgrade vectors (part 1 of 2)

Twenty-one vectors, one paragraph each. No selection here — diversity is the goal. Numbered so §06 can refer back. Part 2 ([04a-long-list-part-2.md](04a-long-list-part-2.md)) carries vectors 12–21 and the list-shape commentary.

## 1. Decision-record-as-substrate

Reframe what the workflow produces. Today, the *output* is a synthesis written into the chat. Tomorrow, it is also a versioned *decision record* — a small structured artifact (`decision.md` + `decision.yaml`) capturing the question, the frame, the rejected alternatives, the recommended path, the named uncertainties, and a stable id. The synthesis becomes a view onto the record, not the record itself. Retrieval, calibration, and revisit primitives all need a stable substrate; this is it. (Foundational.)

## 2. Calibration revisit agent

A new agent that, on a cadence (manual, scheduled, or triggered), opens a past decision-record and asks: *what actually happened?* The operator answers. The agent scores the recommendation against the outcome on three axes — *was the framing right? was the recommended path taken? did it work?* — and writes a `revisit.md` next to the original record. Over time, these become a Tetlock-style track record. The cheapest mechanism the stack has for stopping ceremony from drifting into ritual. (Operational.)

## 3. Critic-panel collapse to one parametrised critic

The three lens files ([critic-architecture](../../.claude/agents/critic-architecture.md), [critic-operations](../../.claude/agents/critic-operations.md), [critic-product](../../.claude/agents/critic-product.md)) share ~80% of their skeleton; the differentiation is the section names and the lens-specific anti-patterns list. Replace with one `critic` agent that takes a `--lens` argument. Run it three times in parallel for the same effect, or — more interesting — let the orchestrator (or a small `lens-selector`) choose 1–3 lenses based on the question. This is the **mandatory removal** per brief §4f. (Structural; removal.)

## 4. Structured agent return contracts

Today, every agent emits markdown and the [subagent-distiller](../../.claude/agents/subagent-distiller.md) exists because the markdown contract is loose. Push the discipline upstream: each agent emits a small JSON envelope alongside its markdown (e.g. `{verdict: "rework", confidence: "direct", contradictions: [...], frame_objections: [...]}`). The distiller then becomes optional or disappears entirely; the orchestrator reads structured fields. This is the *type system* the stack has been gesturing toward. (Structural.)

## 5. Eval harness with paired scenarios

Today there is one regression scenario ([tests/regression/ark-mono-connector-routing.md](../../tests/regression/ark-mono-connector-routing.md)), manually graded. Build an `evals/` directory with N paired scenarios (each pair is the same question with one varied detail that should change the answer; the scoring asks whether the workflow noticed the variance). Auto-graded with a separate grader prompt. Every change to an agent runs the suite. This is what protects the stack from silent regressions and is the precondition for any aggressive refactoring. (Operational.)

## 6. Promote-session-to-eval primitive

A `/promote-eval <session-id>` command that captures the just-finished session as a new eval scenario, with the artifacts as the expected pattern. The eval suite grows from real use rather than from operator imagination. Coupled with #5, this turns the workflow into a *self-growing test set*. (Operational.)

## 7. Inverted librarian — contradiction-first retrieval

The current [canon-librarian](../../.claude/agents/canon-librarian.md) retrieves relevant passages and is *also* required to surface contradictions. Split the modes. Keep the relevance-first librarian for steps 3–5. Add an inverted invocation at step 9 (or 10): given the *candidate*, retrieve only what *contradicts* the candidate. The contradicting passages become an explicit input to the critic. This addresses Zheng et al.'s self-preference / agreeability bias by giving the critic external, retrieval-grounded ammunition. (Structural.)

## 8. Corpus-coverage map as a librarian precondition

Before retrieving for a question, the librarian first emits a coverage map: *for this topic, the corpus has full coverage of X, stub-only coverage of Y, and no coverage of Z*. The orchestrator sees the map before seeing passages and can decide whether to invoke `WebSearch` for declared gaps. Today the librarian flags gaps after the fact; promoting the gap-map to a precondition shifts the framing from "here is what I found" to "here is what I have, and what I don't." (Structural.)

## 9. Operator-bias profile

A per-operator `profile.md` capturing known biases the orchestrator must compensate against. *"This operator over-indexes on consistency-with-existing-systems; reframe step should default-challenge that."* Builds slowly via the calibration revisit agent (#2). The stack today treats every operator as the median operator; over time, calibrated revisits should reveal each operator's *characteristic* failure modes, and the orchestrator can pre-empt them. (Interfacial.)

## 10. Pre-mortem mode (Klein-style oral, not artifact-heavy)

Add a mode where the workflow skips most artifact production and produces only a structured pre-mortem: *imagine this recommendation has failed in 12 months. Write the post-mortem.* This is conceptually different from the [frame-challenger](../../.claude/agents/frame-challenger.md) because it operates on a *recommended path*, not a *frame*. Klein's evidence (HBR, 2007) is that pre-mortems surface more risks than equivalent prospective analyses. The stack does not currently do this. (Structural.)

## 11. Adversarial-debate variant of the critic panel

Replace minority-veto with two-critic debate plus a judge, per Khan et al. (2024 ICML; arXiv:2402.06782). Two critic instances are given the candidate from opposing positions ("argue this is wrong" / "argue this is right"); a third instance, with a *separate* prompt and ideally a different model, judges the transcript. Khan et al.'s evidence suggests this lifts judge accuracy on hard truthfulness tasks. Worth comparing — empirically — against the current minority-veto panel. (Structural; would replace #3 if shipped together.)

(Vectors 12–21 continue in [part 2](04a-long-list-part-2.md), followed by the list-shape commentary.)
