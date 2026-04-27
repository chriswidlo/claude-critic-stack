# 08 — Sequencing across the shortlist

If the operator decides to attempt all six shortlist items over the next 6–12 months, the order matters because three of the six **earn the right** to the others.

## The dependency shape

```
S1 (decision-record + revisit)         ─┐
                                         ├─→  unlocks #4, #9, #12, #16 from the long list
S3 (eval harness + ablation)           ─┤
                                         ├─→  empirically defends every removal, including S2 and S5
S2 (critic-panel collapse)             ←─┘    (depends on S3 for defensibility)
S5 (retire requirement-classifier)     ←─┘    (depends on S3 for safety)

S4 (inverted librarian + coverage map) — independent of the above; can ship in parallel
S6 (pre-mortem mode)                   — independent; smallest item; can ship anytime
```

Two precondition pairs. **S3 is a precondition for safe S2 and S5** because removals without an eval harness are faith moves. **S1 is a precondition for the post-shortlist backlog** (#4, #9, #12, #16, #17, #19) because every one of those is a measurement-or-substrate move that needs the substrate.

S4 and S6 are operationally independent. They can run in parallel with the main spine or be deferred entirely depending on the operator's appetite.

## Recommended order

### Phase A — substrate (weeks 0–6)

1. **S1 cheapest experiment** (≈ week 0–1). Hand-author `decision.yaml` for three real sessions; decide go/no-go. If no, the foundational reframe was wrong and the plan re-shapes.
2. **S1 build** (≈ week 1–4). Schema, agent, step-12 wiring, hard gate on residual disagreement. Migrate ~5 most-recent session-artifacts to also have a `decision.yaml` (mostly mechanical).
3. **S3 cheapest experiment** (≈ week 2–3, in parallel with S1 build). Convert [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md) to one `expected-features.yaml`; run with and without `critic-product` ablated. Decide go/no-go on harness.
4. **S3 build** (≈ week 3–6, overlap with S1 finish). Runner script, ablation wrapper, promote-eval slash command. Convert one or two more existing scenarios.

End of Phase A: substrate exists, ~3 scenarios in `evals/`, decision-record on every new session, residual-disagreement gate live.

### Phase B — defensible shrink (weeks 6–14)

5. **S2 collapse** (≈ week 6–9). With the eval harness in place, perform the critic-panel collapse. Run pre/post against the suite. Document the deltas — both the collapses that produced no measurable change (good — confirms the redundancy) and the ones that did (which becomes the lens-selection rule the orchestrator uses).
6. **S5 retire requirement-classifier** (≈ week 9–12). Same pattern. Update [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md) assertions to live in `frame.md` rather than `requirement.md`. Run pre/post against the suite. If a kill criterion fires (e.g., `frame.md` consistently misses the framing-words capture that `requirement.md` produced), revert and document why.
7. **Ablation pass on every remaining agent** (≈ week 12–14). With S2 and S5 defended, run the same ablation pattern against [scope-mapper](../../.claude/agents/scope-mapper.md), [frame-challenger](../../.claude/agents/frame-challenger.md), [subagent-distiller](../../.claude/agents/subagent-distiller.md). The likely outcome (per the long list's commentary) is one or two more removal candidates surface — **do not act on them in this phase**. Capture the deltas; bring them as new `upgrades/` entries; let the operator decide outside the workflow.

End of Phase B: agent count reduced by 2 (panel collapse → 1 critic, classifier removed). Eval harness has ~5–7 scenarios. Ablation deltas captured for the rest of the agent roster.

### Phase C — capability under measurement (weeks 14–24)

8. **S4 inverted librarian + coverage map** (≈ week 14–18). Cheapest experiment first; build only if the experiment shows a real signal. The eval harness (S3) catches regressions in librarian behaviour. Coupling: the contradiction-first invocation needs at least one eval scenario that asserts on contradicting-passage volume per session, otherwise the failure mode "net contradictions drop" is invisible.
9. **S6 pre-mortem mode** (≈ week 18–22). Smallest item. Add the mode, add one eval scenario that exercises it, ship.
10. **S1 first calibration revisit pass** (≈ week 22–24). After ~6 months of accumulated decision records, run revisits across the back catalogue. This produces the first real calibration data — the first moment in the stack's history where the operator can see *what predictions held up*. Almost certainly the most informative single hour the operator will spend on the stack in the year.

End of Phase C: substrate has data; surface area is smaller than at start; capability has been added under measurement.

### Phase D — react to data (weeks 24+)

The post-shortlist backlog (#4, #9, #12, #16, etc.) becomes prioritised by what the calibration data and ablation deltas actually show. This is the phase that the rest of the plan exists to make possible. *Do not commit to specific work in this phase now*; the data will name the work.

## What blocks what — explicit

- S2 build is blocked on S3 cheapest experiment (need at least one harness scenario to grade against).
- S5 retire-classifier is blocked on S3 build (need the [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md) running through the harness, so the test that currently asserts on `requirement.md` can be re-pointed).
- S4 contradiction-first step is *helped* by S3 (regression scenario for contradicting-passage volume) but not strictly blocked.
- The post-shortlist backlog is blocked on S1 producing data, which takes ~6 months minimum.

## What can be parallelised

- S1 build and S3 build can run in parallel; they touch different surfaces.
- S4 cheapest experiment can run anytime — it requires only the existing librarian and one or two recent sessions.
- S6 can ship before S2 if the operator wants a cheap visible win early.

## What is hard-deferred

- Most of the post-shortlist backlog. Building #4 (structured agent return contracts), #9 (operator-bias profile), #12 (cross-session retrieval) before the substrate exists is the *exact* mistake the reframe argues against.
- Anything that depends on Anthropic feature parity (Skills behaviour, Routines availability, MCP server changes). The plan as written assumes only existing primitives.

## Re-ordering allowances

If the operator's appetite is for a cheap visible win and they want to descope: **ship S6 first** (smallest), then **S3 alone** (build the harness without acting on it), then revisit. This produces an honest measurement substrate without committing to either substrate work (S1) or removals (S2, S5). Three months of the harness running unused is itself diagnostic.

If the operator's appetite is for the most provocative single move: **S2 + S3 together** (the deep-dive [07-deepdive-critic-collapse-and-ablation.md](07-deepdive-critic-collapse-and-ablation.md)) is the proposal that most actively reshapes the stack and has the strongest forcing-function on subsequent decisions.

If the operator's appetite is for the most foundational single move and they trust their prior on the reframe: **S1 alone** (the deep-dive [07-deepdive-decision-record-substrate.md](07-deepdive-decision-record-substrate.md)). It is the longest-lived change and the one whose value compounds the most over time.

The plan is robust to any of these prunings. None of them break the others.
