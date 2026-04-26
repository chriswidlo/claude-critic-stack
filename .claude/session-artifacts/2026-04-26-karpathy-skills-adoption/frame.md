# Frame

## Revision 1

### User's implicit frame
"Is the prior writeup optimal?" — a binary validation request against an unstated criterion of "optimality," anchored on the prior recommendation as the unit of analysis. Implicitly optimizing for: **confidence that the recommendation is the right one**, with the workflow used as a confirmation/rejection signal.

This frame is weak because:
1. "Optimal" has no operationalization. Optimal *for what*? Setup time? Long-term harness coherence? Recovery cost from a wrong choice?
2. It anchors on the candidate. The workflow is structurally biased toward producing critique on the artifact in front of it, which means a "yes it's optimal" outcome is unlikely-by-construction even if the prior recommendation is fine. Validation-of-self via adversarial review tends to produce changes for change's sake.
3. It treats the karpathy repo as a one-shot decision (install / don't install) rather than as a signal about the ambient ecosystem.

### Alternative frame A — Regret-minimization, not optimality
Reframe the question as: **"Across the small set of plausible actions (do nothing / drop a line into global CLAUDE.md / install plugin globally / install plugin into this repo / fork-and-adapt the packaging pattern), which action has the worst recovery cost if it turns out to be wrong, and which has the best?"**

This shifts from "is the recommendation optimal" (point estimate) to "which action's failure mode is cheapest to undo" (option value). The prior recommendation roughly maps to "do nothing or drop a line" — both have near-zero recovery cost. So under this frame, the prior recommendation is dominated only if a more expensive action carries a large enough upside to justify the recovery risk.

Under this frame, the question to the workflow becomes: **does any of the more-expensive actions (install globally; adopt the packaging pattern for the user's own conventions) carry enough upside to justify its recovery cost?** That is a more honest decision question than "is the writeup optimal."

### Alternative frame B — Ecosystem-signal, not artifact
Reframe as: **"The karpathy repo is one of many community-published Claude Code plugins that have started appearing on marketplaces. The right question is not what to do with this one — it is what policy the user wants for evaluating *future* such plugins, of which this is the first concrete instance."**

Under this frame, the prior recommendation is incidentally fine but addresses the wrong scope. The durable artifact would be a 5-line decision rule the user applies to the next ten such plugins, not a one-line edit to global CLAUDE.md.

### Where the user's framing is honest, where it is weak
- **Honest**: explicitly invoking the workflow on the prior recommendation, accepting that the workflow may produce a verdict of `rework` or `replan` against the orchestrator's own output. That is the correct hygiene.
- **Weak**: "optimal" smuggles in a single-criterion frame; the candidate has at least three plausible criteria (setup cost, harness coherence, regret cost) that point in different directions.

### Frame chosen for this run
**Alternative frame A (regret-minimization)** as primary, with frame B (ecosystem-signal) as a check that the chosen action is not pessimal across the *next* ten such repos. The classifier's "extend" label still applies — the unit of action is still a tweak to existing primitives — but the decision criterion is now option-value, not optimality.

### What this frame demands of the generator (step 9)
The candidate must:
1. Enumerate the action set (at least 4 actions) and rank them by recovery cost, not by perceived correctness.
2. Name the upside that would have to be true for each more-expensive action to be worth its recovery cost.
3. State whether the prior recommendation survives this reframe unchanged, with one tweak, or rewritten.
