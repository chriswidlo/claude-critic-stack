# Outside-View Report: Context7 adoption in claude-critic-stack

## 0. Canon-first note

Canon directory listing failed via Read (directory). Worked from named entries (anthropic-building-effective-agents, anthropic-effective-context-engineering, anthropic-multi-agent-research-system, fowler-refactoring, evans-ddd) at level of established arguments + WebSearch confirming Context7 behavior and Anthropic's published position. No Flyvbjerg/Kahneman/Tetlock loaded directly; base rates flagged as estimates.

## 1. Reference class

Primary (most predictive): "Adding a retrieval source designed for workflow type A into an agent stack built for workflow type B." Context7 built for codegen freshness; critic-stack consumes design questions where binding constraint is judgment quality under adversarial review, not API correctness. Category mismatch is dominant feature.

Secondary: "Capability-accretion in opinionated review systems." Code Climate, SonarQube, ESLint, Danger.js — all started opinionated, gained third-party rule packs. Pattern: opinion erodes, signal-to-noise degrades, review thesis becomes harder to defend.

Tertiary: "Adding third-party retrieval source alongside curated retrieval lane." RAG with curated KB + web/freshness lane; trust/freshness conflicts recurring failure.

Weakly predictive: "MCP servers in non-codebase agent systems 6-12 months out." Too new to base-rate.

Primary and secondary pull same direction (caution); tertiary same with milder slope. No class points to "adopt freely."

## 2. Base rate (qualitative estimates, flagged)

- Workflow-mismatch tool installs: ~20-30% used as designed; ~40-50% installed-but-unused or misused; ~20-30% removed within a year.
- Opinion erosion in plugin-accreted review systems: well-attested anecdotally (Airbnb ESLint history, SonarQube rule debates), no measured success rate.
- Curated + third-party retrieval coexistence: trust conflicts rare when subordinated, contradictory retrievals in ~1/3 non-trivial queries when parallel.

Anthropic's own guidance (Effective context engineering, Writing tools for agents) favors on-demand, narrow, token-efficient retrieval over preloading — consistent with shape B (subordinate tool), against shape C (always-on subagent).

## 3. Position relative to base rate

Above-average features:
- Stack already has canon-first discipline and librarian-first routing.
- canon-refresher already exists as slot for "watching external sources" without writing to canon — shape D extends a primitive.
- Question distribution is mostly design/decision, not codegen — orchestrator already has reason to suppress tool on most questions.

Below-average features:
- Context7's value-prop is currency of code-level facts. Design questions almost never bottleneck on API specifics.
- Shape C and E both create parallel retrieval lane — config most associated with trust-conflict failure.
- Stack's central discipline is anti-anchoring. Vendor docs are persuasive artifacts; critic stack built to resist persuasive artifacts.
- "Sometimes API depends on current details" is small slice of design questions. Building structural lane for small slice usually overshoots — capability-accretion failure mode in miniature.

Net: above workflow-mismatch base rate only if shape B or D chosen. At-or-below for shapes C and E. Shape A is the base rate.

## 4. Typical failure mode

Modal failure is NOT "tool breaks" or "tool unused." It is:

**Tool fires on questions it wasn't built for; injected docs treated as authoritative by downstream agents; stack's adversarial-review character degrades silently.** Specifically:
- Design question mentions library by name (e.g., "should we adopt Temporal"). Context7 fires on Temporal. Injected docs are vendor-authored and uniformly positive. Frame-challenger and critics now must argue against fresh, confident, well-formatted vendor documentation. Adversarial review weakens.
- Six months later: stack is "more agreeable about libraries with good docs." Bias invisible per-query, visible only in aggregate.
- Capability-accretion variant: once Context7 in, next MCP server easier to justify. Two years later, anti-anchoring opinion is one voice among many tools.

Secondary failure: canon-first honored in letter not spirit. Librarian declares gap, Context7 fires; canon stops being curated to cover library-level questions because "Context7 has it." Corpus thins where it should thicken.

## 5. Verdict

**Below base rate for shapes C and E. Within tolerance for B and D. Shape A is the base rate.**

Lift for C/E above base: measured demo that ≥15-20% of question log bottlenecks on current library-API facts canon cannot serve. Without that, structural cost (parallel lane, anchoring surface, capability-accretion precedent) exceeds marginal value.

Shape B (subordinate tool, callable only when canon-librarian declares library-currency gap) = minimum-discipline-cost integration. Only shape consistent with both Anthropic's on-demand-retrieval guidance and stack's existing librarian-first rule.

Shape D (extend canon-refresher to watch library releases) consistent with `extend over new` scope-mapper default and Fowler preference, but solves different problem (corpus freshness) than Context7 was built for (per-query injection).
