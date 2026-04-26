# Scope Map

## Existing primitives touched

| primitive | source (where it was named) | relationship | one-line rationale |
|-----------|-----------------------------|--------------|--------------------|
| **A1. Anthropic Research (Claude.ai)** | user prose; outside-view | extend | Hosted engine sits at base rate (40–55% joint success) for in-distribution queries; the new requirement adds an audit/citation-verification layer on top rather than reimplementing retrieval. |
| **A2. OpenAI Deep Research** | user prose; outside-view | conflict | Cannot coexist as the engine alongside A1 in a "minimum architecture for a single user" — picking both doubles cost and reconciliation burden with no quality gain reported. User has not chosen. |
| **A3. Perplexity Deep Research / Labs** | user prose; outside-view | replace | Same reference class as A1; replaced by A1 because the user's stack is Claude-native and source transparency is comparable. Deletion cost: nil (no integration exists). |
| **A4. Gemini Deep Research** | user prose; outside-view | replace | Same reference class as A1; no Claude-stack synergy. Replaced by A1 by default. |
| **B1. WebSearch tool (Claude Code)** | user prose; canon (BEA "start simple") | extend | Primitive retrieval that the orchestration layer wraps; cannot be subsumed because hosted engines are opaque and WebSearch is the auditable fallback per outside-view. |
| **B2. WebFetch tool** | user prose | extend | Required for per-claim citation verification (deterministic re-fetch of cited URLs); the verifier *is* a WebFetch loop. |
| **B3. Subagents (Agent tool, parallel fan-out)** | canon (multi-agent essay); user prose | extend | Canon supports parallel fan-out for token-budget reasons (80% of variance); kept but constrained to read-only research subagents with compressed returns per context-engineering essay. |
| **B4. Plugins / Skills** | user prose | replace | The "research skill" pattern is replaced by an explicit orchestrator command + verifier; skills hide the pipeline and defeat auditability, which is the working frame's core requirement. |
| **B5. MCP servers (Brave, Tavily, Exa, Firecrawl, Playwright, Reddit, ArXiv, GitHub)** | user prose; canon gap | extend (selective) | Tool design is a larger lever than prompt tweaks (canon: 40% time decrease). Keep 2–3 (one general web, one academic, one browser-render); the rest are extension points, not defaults. |
| **B6. Hooks (pre/post-tool-call)** | user prose | extend | Required to enforce the citation-verifier as a hard gate post-research-call; this is the deterministic gate the outside-view named as the lifter above base rate. |
| **B7. Slash commands** | user prose | extend | Entry point for the research routine; trivially preserved. |
| **B8. Background agents / Routines** | user prose; frame revision 1 (refresh half-life) | extend | Preserved specifically to host the canon-refresher applied to research-tooling itself, addressing the frame's "answer decays in weeks" concern. |
| **B9. This adversarial-review stack (canon-librarian, outside-view, critic-panel, scope-mapper)** | CLAUDE.md; user prose | subsume | The new requirement is *itself* an instance of this stack's output; the stack subsumes the "decision-quality wrapper" role any research pipeline would otherwise need to grow. |
| **C1. LangGraph** | user prose; outside-view | replace | Open-source orchestrator class sits at 10–20% joint success (outside-view); replaced by Claude Code's own subagents + hooks because BEA explicitly argues against framework-first orchestration ("start with LLM APIs directly"). |
| **C2. CrewAI** | user prose; outside-view | replace | Outside-view names CrewAI as a prototyping tool unfit for production survival. Replaced by C3 if any SDK is needed at all. |
| **C3. Claude Agent SDK** | user prose | extend | The thin substrate under Claude Code subagents; preserved because B3 implicitly depends on it, but not invoked directly. |
| **C4. smolagents (HuggingFace)** | user prose | replace | Same class as C1/C2; no Claude-stack affinity, no canon coverage, no named reason to preserve. |
| **C5. OpenDeepResearch** | user prose | replace | Open-source reference implementation; useful as a *pattern source*, not as a runtime. Replaced by the in-stack composition. |
| **C6. AutoGen** | user prose | replace | Same as C1/C2/C4. |
| **D1. LLM-as-judge 5-axis rubric** | canon (multi-agent essay) | extend | Canon-direct primitive; the eval harness for the verifier. Preserved verbatim from the Anthropic essay (factual / citation / completeness / source quality / tool efficiency). |
| **D2. Separate CitationAgent post-pass** | canon (multi-agent essay) | extend | Named in canon as the most reliable citation check; preserved as the hard gate the outside-view called the dominant lifter above base rate. |
| **D3. RAGAS / TruLens / DeepEval / FActScore** | user prose; canon-declared gap | replace | Canon declares zero coverage; outside-view does not name an effectiveness number. Replaced by D1+D2 because adding an unevaluated eval framework violates the working frame's "minimum architecture" constraint. |

## Deletion cost (for subsume/replace rows)

- **A2 (OpenAI DR), A3 (Perplexity), A4 (Gemini DR):** callers = none in the user's stack; data migrations = none; config surface = API keys not provisioned. Deletion is free; the cost is *opportunity* (cross-engine triangulation) and is named in the conflict row for A2.
- **B4 (Plugins/Skills):** callers = none yet; data migration = none; config surface = `.claude/skills/` would have housed a research skill — deleted in favor of an explicit slash command + hook composition. Cost: loses the "one-word invocation" affordance.
- **B9 (adversarial-review stack) subsume:** no deletion — subsume here means the stack *absorbs the role* a separate research-quality wrapper would otherwise play. Blast radius = zero new code; the stack already runs.
- **C1 (LangGraph), C2 (CrewAI), C4 (smolagents), C5 (OpenDeepResearch), C6 (AutoGen):** callers = none; migrations = none; config surface = no Python deps added. Deletion cost is the loss of stateful checkpointing (LangGraph's named strength per outside-view) — flagged as a residual the generator must address (likely via Routines + structured note-taking from canon's context-engineering essay).
- **D3 (RAGAS et al.):** callers = none; migrations = none; config surface = no eval pipeline configured. Cost: foregoes published groundedness metrics, replaced by D1's 5-axis rubric which canon endorses but is Anthropic-authored (source-diversity risk per librarian's missed gap).

## Requires decision (conflicts)

- **A1 (Anthropic Research) vs A2 (OpenAI Deep Research) as the hosted engine.** Both cannot be the default engine in a minimum architecture because (a) cost doubles, (b) reconciling divergent citation sets requires a meta-verifier that does not exist, (c) outside-view treats them as the same reference class with the same opaque-retrieval failure mode. User has not chosen. Default in absence of decision: A1, on grounds of stack-locality only — this is a weak reason and the frame-challenger should challenge it.

## Preserved primitives with stated reason (non-default)

- **B1 (WebSearch) and B2 (WebFetch):** preserved because they are the only auditable retrieval path. Hosted engines (A1/A2) are opaque per outside-view; without B1/B2 the verifier (D2) has nothing to re-fetch against.
- **B3 (Subagents):** preserved because canon (multi-agent essay) anchors the 80%-of-variance-from-token-budget claim to parallel fan-out. Removing them collapses to single-agent, which canon shows underperforms by 90.2% on Anthropic's eval — even discounted heavily for self-promotion bias, the gap is large.
- **B8 (Routines):** preserved because frame.md Revision 1 names refresh half-life as an unstated user optimization; Routines are the only primitive in the set that addresses it.
- **D1 + D2 (5-axis rubric + CitationAgent):** preserved because outside-view names the citation verifier as the single dominant lifter above base rate across all three classes.

## Primitives the distillations did not name but the query implies

- **Prompt-injection defense for web-fetched content** (canon-declared gap #3). The verifier reads attacker-controlled HTML; no primitive in the set handles this.
- **Cost guardrails / token budget caps** (outside-view "Valley of Death" failure mode). No named primitive; Claude Code has no built-in spend cap.
- **Human-in-the-loop checkpoint primitive** (canon-librarian missed gap). Long-horizon research runs need a review gate; no Claude Code primitive maps cleanly — slash command + Routine pause is the closest improvisation.
- **Frozen model + harness version pinning** (outside-view lifter). Claude Code does not expose a stable pinning primitive; outside-view itself flagged this as unverified-feasible.
- **Reproducibility / run-log primitive.** Implicit in "defensible output" but unnamed; would require hook-driven persistence beyond `.claude/session-artifacts/`.

These are candidates for a follow-up Explore or canon-refresher pass; they are *not* added to the primitive table because the scope-mapper does not introduce primitives.

## Minimum viable composition

The smallest combination of preserved primitives that defensibly meets the working frame ("minimum architecture that gives a single user defensible research output"):

1. **Entry point:** B7 (slash command), e.g. `/research <question>`.
2. **Retrieval substrate:** B1 (WebSearch) + B2 (WebFetch) as the auditable path; A1 (Anthropic Research) as an *optional* high-recall first pass whose output is then re-grounded by 3–4. Hosted engine is never the final authority.
3. **Parallel exploration:** B3 (subagents) fanned out at most 3-wide, each returning compressed 1–2K-token summaries per canon's context-engineering pattern. No nested fan-out (canon: coordination is weak).
4. **Tool surface:** B5 restricted to exactly three MCPs — one general web (Tavily or Brave), one academic (ArXiv or Exa), one browser-render (Playwright) for paywall/JS-heavy pages. Everything else is opt-in per query.
5. **Hard gate (the lifter):** B6 (post-tool-call hook) invokes D2 (CitationAgent) which re-fetches every cited URL via B2, scores groundedness on D1's 5-axis rubric, and *fails the run* if citation accuracy < threshold. This is the single non-negotiable element; everything else is replaceable.
6. **Decision-quality wrapper:** B9 (this stack) consumes the verified output and routes through critic-panel before the user sees it. Subsumes any need for a separate "research QA" layer.
7. **Refresh routine:** B8 (Routine) re-runs the canon-refresher pattern monthly against research-tooling sources, addressing the frame's refresh-half-life concern.

Not in the composition: every C-class orchestrator, every hosted engine besides A1, plugins/skills, and D3. They are available as extension points if a named failure mode in the minimum composition forces them in — but the burden is on the failure, not on the user.

Residual the generator must address: the LangGraph deletion cost (stateful checkpointing) is replaced here by Routine + session-artifacts persistence, which is weaker. If long-horizon (>1 hour) runs become routine, this composition is undersized.
