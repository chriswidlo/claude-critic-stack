# Outside-view distillation — Context7 adoption

## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on adopting Context7 (MCP server for code-currency retrieval) into claude-critic-stack across shapes A-E. Subagent returned a verdict differentiated by shape, anchored to workflow-mismatch and capability-accretion reference classes.

## Direct facts
1. [outside-view §0] Canon directory listing failed via Read; subagent worked from named entries (anthropic-building-effective-agents, anthropic-effective-context-engineering, anthropic-multi-agent-research-system, fowler-refactoring, evans-ddd) plus WebSearch confirming Context7 behavior. (confidence: direct)
2. [outside-view §0] No Flyvbjerg/Kahneman/Tetlock loaded directly; base rates self-flagged as estimates. (confidence: direct)
3. [outside-view §1] Context7 was built for codegen freshness; critic-stack consumes design questions. (confidence: direct — observable product positioning)
4. [outside-view §3] canon-refresher already exists in the stack as a slot for "watching external sources" without writing to canon. (confidence: direct — verifiable in repo)
5. [outside-view §3] Stack already has canon-first discipline and librarian-first routing. (confidence: direct — encoded in CLAUDE.md)

## Inferred claims
1. [outside-view] Primary reference class is "adding a retrieval source designed for workflow type A into an agent stack built for workflow type B"; category mismatch is the dominant feature. (confidence: inferred)
2. [outside-view] Secondary class "capability-accretion in opinionated review systems" (Code Climate, SonarQube, ESLint, Danger.js) shows pattern of opinion erosion as third-party rule packs accrete. (confidence: inferred — pattern claim, examples named but not quoted)
3. [outside-view §2] Workflow-mismatch tool installs split roughly: ~20-30% used as designed, ~40-50% installed-but-unused/misused, ~20-30% removed within a year. (confidence: inferred — explicitly flagged as qualitative estimate)
4. [outside-view §2] Curated + third-party retrieval in parallel produces contradictory retrievals in ~1/3 of non-trivial queries. (confidence: inferred — qualitative estimate)
5. [outside-view §4] Modal failure mode is not "tool breaks/unused" but "tool fires on questions it wasn't built for; vendor docs treated as authoritative; adversarial-review character degrades silently." (confidence: inferred)
6. [outside-view §4] Secondary failure: canon-first honored in letter not spirit — corpus thins on library-level questions because "Context7 has it." (confidence: inferred)
7. [outside-view §3] Vendor docs are persuasive artifacts; the critic stack is built to resist persuasive artifacts, so injecting them is in tension with central discipline. (confidence: inferred)
8. [outside-view §5] Lift threshold for shapes C/E above base rate: measured demo that >=15-20% of question log bottlenecks on current library-API facts canon cannot serve. (confidence: inferred — proposes a numeric threshold)

## Authority-framed claims
1. "Anthropic's own guidance (Effective context engineering, Writing tools for agents) favors on-demand, narrow, token-efficient retrieval over preloading — consistent with shape B, against shape C." — underlying claim: Anthropic guidance prefers on-demand narrow retrieval. Quote present in output: no. Confidence: unsupported (named documents but no quoted passage).
2. "Shape D consistent with `extend over new` scope-mapper default and Fowler preference." — underlying claim: Fowler prefers extending existing primitives over adding new ones. Quote present in output: no. Confidence: unsupported (Fowler invoked without quote).

## Contradictions surfaced
- Shape-level split inside the verdict itself: shapes B and D are "within tolerance"; shapes C and E are "below base rate"; shape A is the base rate. Not a contradiction in the source, but a non-collapsible differentiation the orchestrator must preserve — there is no single verdict.
- Tension between "extend canon-refresher (shape D) is scope-map-aligned" and "but it solves a different problem (corpus freshness) than Context7 was built for (per-query injection)" — i.e., the most discipline-aligned shape may not be a real fit for the tool.
- No retrieved passage directly contradicting the caution stance was surfaced; subagent notes "no class points to 'adopt freely'." Possible under-search.

## Subagent's own verdict (verbatim)
"Below base rate for shapes C and E. Within tolerance for B and D. Shape A is the base rate."

## Gaps the subagent missed
- No actual quoted passage from Anthropic's "Effective context engineering" or "Writing tools for agents" — both are named-entry citations only. Orchestrator may want canon-librarian to surface the verbatim guidance.
- No direct base-rate citation (Flyvbjerg/Kahneman/Tetlock not loaded); all percentages are self-flagged estimates, not retrieved figures.
- No reference class for "MCP servers in non-codebase agent systems" — explicitly declared too new to base-rate; orchestrator should not expect this gap to close from canon.
- No counter-class searched (e.g., "tools that looked workflow-mismatched but turned out useful"); the subagent admits all classes pull in the same direction, which is a confirmation-bias risk on its own forecast.
- Cost/effort of each shape not estimated — verdict is on value/risk only.
- No engagement with whether design questions in this stack actually do or do not name libraries at meaningful frequency — the failure-mode example ("should we adopt Temporal") is hypothetical.

## Token budget
~720 tokens.
