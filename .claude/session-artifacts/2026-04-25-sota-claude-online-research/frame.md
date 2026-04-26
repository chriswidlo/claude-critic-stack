# Frame

## Revision 1

### User's framing (verbatim)
> "Best way, SOTA, getting Claude to do online research that will result in best complete research done… solutions, that take advantage of general AI infrastructure, best practices, modern solutions, all available tools, and Claude Code… plugins, MCPs etc. just find out who and how solve research that is an online research of anything."

### What the user is implicitly optimizing for
**Completeness of the landscape survey** — a single comprehensive picture of "the SOTA stack" with everything in it (tools, MCPs, plugins, agent topologies, vendor offerings). The implicit assumption is that more comprehensive = more useful, and that there is a recognizable SOTA that one can adopt.

### Alternative optimizations the user did *not* name

1. **Trust-per-token / refusal-rate.** The hardest problem in online research is not coverage — it is: *of the claims this pipeline returned, what fraction can I cite without rechecking?* A pipeline that returns 3 well-grounded claims with sources beats one that returns 30 plausible-sounding ones. SOTA on this axis looks very different from SOTA-on-coverage.

2. **Refresh half-life.** The answer to "how should Claude do online research" decays in weeks. Anthropic shipped a Research feature in 2025; OpenAI's Deep Research, Perplexity Deep Research, GLM-4.6 research mode, and the Claude Agent SDK all moved this year. The right artifact may not be a snapshot recommendation but a *re-investigation routine* (i.e., the canon-refresher pattern, applied to research-tooling itself).

3. **Decision downstream.** Investigation-without-decision is the failure mode the classifier named. The right reframe is: *what would you do differently tomorrow morning if I told you the answer is X versus Y?* If the answer is "nothing changes," the question is decorative and I should refuse to write a long survey.

4. **Build-vs-buy.** The user listed "MCPs, plugins, Claude Code commands" — implying a build. But the SOTA *operator-grade* answer in 2026 is increasingly "use Anthropic Research / OpenAI Deep Research as the engine, and only build the orchestration layer." Building the engine is rarely the right call.

### Honest friction with the user's framing

- "Best… complete" is an over-specified objective. Complete-on-what-axis? Recall? Citation accuracy? Time-to-report? Cost? These rank candidates differently.
- "Who and how is this being solved" assumes a settled SOTA. The honest answer in 2026 is **the field is fragmented**: Anthropic's Research, OpenAI Deep Research, Perplexity, You.com, GLM, plus open-source orchestration (LangGraph, CrewAI, Claude Agent SDK, smolagents, OpenDeepResearch). Asking for "the SOTA" rather than "a defensible architecture for *my* use case" forces a false consensus.
- "Use parallel agents" is a method instruction to *me*, not a property of the answer. It does not entitle the answer to be longer.

### Working frame for downstream steps

> "Given that 'online research with Claude' is fragmented across (a) hosted research products, (b) Claude-Code-native agentic patterns, (c) MCP-mediated tool access, and (d) open-source orchestrators, what is the minimum architecture that gives a single user defensible research output, and what is the cheapest test that tells them they need more?"

This is the frame the generator (step 9) must serve. The completeness-survey framing is preserved as a fallback only if the user names a build target.

### Frame bias to police throughout
- Research theater (classifier's flag).
- Vendor-as-solution: defaulting to "use Anthropic Research" because the user is in Claude's stack is anchoring, not analysis.
- Tool-list bias: a list of tools is not an architecture.
