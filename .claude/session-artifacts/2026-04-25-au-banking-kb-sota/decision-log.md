# Decision Log

## Step 10 verdict

Architecture = rework, Operations = rework, Product = rework. Unanimous, including frame-level objections from each lens.

## Routing decision: rewrite-at-synthesis (not replan)

Rationale:
- The **product** critic's frame objection ("user is in research mode, deliver a field map with the prescription as optional appendix") does not require re-running scope-mapper or frame-challenger. The frame-challenger already named this (Frame F: literature-survey reading); the candidate failed to honor it. Fix is at the synthesis output shape, not the frame.
- The **architecture** critic's fixes (Instrument as aggregate root, ACL between Layer 1 and Layer 4, content-hashed citations, event-sourced supersession) are concrete and can be folded into a *demoted* prescription appendix without dominating the deliverable.
- The **operations** critic's fixes (quarantine state machine, rollback primitive, per-query cost cap, absolute cost figures) likewise compress into the appendix.

## Action

Step 11 = rewrite, routed to step 12 (synthesis) with restructured output shape:
1. Field map first (what 2026 SOTA looks like for an AU-banking AI knowledge surface — landscape, not prescription).
2. Canon contradictions and outside-view base rate, presented as the user can read them.
3. The 18-primitive scope-map distilled to a tradeoff matrix.
4. The frame-challenger's six frames (A/B/C/D/E/F) as the user's choice space.
5. The 5-layer prescription demoted to an explicit *"if you want a concrete shape"* appendix, with arch + ops critic fixes folded in.
6. Three named uncertainties and the cheapest experiment.

This respects the user's "research, do not execute" instruction without dropping the work the critics improved.

## Loop budget

One full loop used (step 10 → step 11 → restructured step 12). Cap is two; remaining budget = one. Not used.
