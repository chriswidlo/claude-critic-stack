## critic-architecture

### 1. Weakest structural link
The initial candidate over-reached toward a richer runtime before establishing a machine-readable contract for the existing prompt system. That creates a split-brain architecture where markdown prompts remain the policy source but an external harness becomes the de facto control plane.

### 2. Invariants at risk
- The stack must remain auditable by reading the repo; hidden runtime logic weakens this.
- The same session should produce comparable artifacts across runs; prose-only outputs make that fragile.
- The corpus must remain the privileged evidence source for non-current questions; ad hoc web-heavy upgrades erode this invariant.

### 3. Coupling and direction
The dangerous direction is letting runtime machinery become more authoritative than the prompt contracts that supposedly govern it. That would couple the stack to implementation detail instead of keeping prompts, corpus, and eval rubrics as the stable layer.

### 4. Ignored architectural alternatives
- Add JSON sidecars and scorecards to the existing artifact flow before adding any new runtime layer.
- Generate both Claude and Codex instruction surfaces from one canonical source instead of maintaining parallel manual variants.

### 5. Frame-level objection
The frame still leaned too much toward "platform upgrade" instead of "decision-quality upgrade."

### 6. Verdict
rework — make evaluation contracts and single-source policy generation primary, and push heavier runtime changes behind proof that the current structure cannot support them.

## critic-operations

### 1. Most likely incident
At time T, the upgraded stack starts reporting cleaner-looking scores while actual recommendation quality drifts. Root cause is an uncalibrated LLM-judge layer and missing human backchecks, so operational confidence rises faster than accuracy.

### 2. Blast radius
The radius is every design recommendation the stack produces after the upgrade, because false confidence at the review layer contaminates downstream architecture choices rather than causing a single obvious runtime failure.

### 3. Rollout / rollback
- Safe rollout exists only if new scoring and routing rules can run in shadow mode against the existing artifact flow.
- Rollback must mean "ignore the new scores and fall back to prose artifacts," not "debug the judge live."
- The two-systems-running period is unavoidable while judge calibration and cost budgets are established.

### 4. Observability gap
The stack does not currently measure critic agreement, judge drift, corpus freshness debt, or per-session token/cost budgets. Without those, an "upgrade" can look better merely because it produces more structure.

### 5. Cost at failure
The failure cost is review noise, curator time, and incorrect trust allocation. This is cheaper than a production outage, but more dangerous because it can stay invisible for a long time.

### 6. Frame-level objection
The frame treats this as a capability problem; operationally it is a calibration problem.

### 7. Verdict
rework — add shadow-mode scoring, explicit human calibration checks, and per-step cost/latency telemetry before introducing more autonomous evaluation loops.

## critic-product

### 1. User-visible consequence
The user will either get a sharper, more trustworthy dissenting review system or a busier one that feels smarter without being more useful. The line between those two outcomes is whether the new structure improves clarity and trust, not whether it adds more moving parts.

### 2. Commitments implied
Once the stack emits scores, budgets, and recommendations in structured form, users will treat them as product commitments. Reversing those semantics later will be harder than changing prose prompts.

### 3. Migration burden
The curator has to maintain rubrics, fixture sets, and dual-surface instructions if the Claude/Codex split remains manual. That is real product burden even if the stack is nominally "internal."

### 4. Product affordances better / worse
- Better: faster regression detection, clearer evidence quality, and clearer upgrade decisions.
- Worse: more maintenance burden and a risk that structured scores get mistaken for objective truth.

### 5. Frame-level objection
The product is trust in the recommendation, not sophistication of the machinery.

### 6. Verdict
approve — provided the upgrade keeps outputs legible and audit-friendly, and treats scores as decision aids rather than ground truth.
