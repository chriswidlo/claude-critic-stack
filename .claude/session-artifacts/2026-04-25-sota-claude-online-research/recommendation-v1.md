# Generator — Candidate Recommendation v1

## Position

There is no single SOTA architecture for "Claude does online research." There is a **three-mode design space indexed by the consequence-tolerance of the user's downstream decision**, and the right answer for any given user is exactly one of these modes — not a blend, not the maximum:

- **Mode S — Scout (low consequence, high volume).** Use a hosted Deep Research product (Anthropic Research, OpenAI Deep Research, Perplexity Labs) directly. No local pipeline. No verifier. One-line disclaimer attached to every output: *"5–15% of citations may be fabricated; do not act on this without re-reading sources."*

- **Mode D — Defensible middle (load-bearing for the user, not yet adversarial).** Use the scope-map's composition with three corrections from the frame-challenger applied. This is the build path. Detail below.

- **Mode P — Principal (irreversible decision, adversarial readers).** Use Claude as a **literature scout that stops at "here are 12 candidate sources, ranked, with a one-paragraph faithful summary of each."** No autonomous synthesis. No verifier-blessed report. The user does the synthesis themselves with the sources in front of them, because Devil's Advocate's 23.5% WebArena ceiling and the verifier's correlated-error failure mode mean no autonomous pipeline can carry the consequence.

**The user's question — "what is the SOTA way" — is therefore unanswerable in its given form.** It must be re-asked as: *what mode am I in for this question?* That re-asking is the deliverable.

## The Mode-D composition (the only one with engineering content)

The scope-map's seven-element composition is mostly correct, with three corrections forced by the frame-challenger:

1. **Entry**: `/research <question>` slash command. Kept verbatim.
2. **Retrieval**: Auditable substrate (`WebSearch` + `WebFetch`) is primary. **A hosted engine is optional and demoted.** *Correction #1: do not run hosted-engine and local-retrieval in parallel as the scope-map implies; the verifier-fetches-the-engine's-URLs critique is sound and the redundant-retrieval cost is real. Use the hosted engine only when local retrieval misses, and label its contributions as "high-recall, unaudited."*
3. **Parallelism**: ≤3 read-only subagents, no nesting, each returns 1–2K compressed summary (canon's context-engineering pattern). Cap total fan-out budget at 15× the equivalent chat tokens (canon's own cost number) and **abort the run** if exceeded — not a soft warning.
4. **Tools**: Exactly three MCP servers wired by default — one general web (Tavily or Brave), one academic (Exa or ArXiv), one browser-render (Playwright) for paywalled/JS-heavy pages. Tool docstrings are owned by the user, not vendor defaults — canon (BEA Appendix 2) attributes 40% of completion-time wins to tool description quality.
5. **Hard gate**: Hook-driven `CitationAgent` post-tool-call. **Correction #2: the verifier must run on a different model family from the producer** (e.g., Haiku 4.5 verifies Opus 4.7, or vice versa) to break the correlated-error mode the frame-challenger identified. The verifier checks: (i) URL fetchable, (ii) URL content semantically supports the specific quoted claim — not just topic-match. **Correction #3: the verifier scores in three buckets — `verified` / `partial` / `unverifiable` — and the report must surface the buckets to the user. No green-checkmark single bit.** This kills the "false-god" failure.
6. **Decision wrapper**: This adversarial-review stack (canon-librarian, outside-view, critic-panel) consumes the verified report and emits a critic-panel pass before user delivery. Subsumes the role of a separate "research QA" layer.
7. **Refresh**: One Routine, monthly, runs `canon-refresher` against research-tooling sources only. Surfaces a diff for the user; **does not auto-apply.** Frame-challenger's "infrastructure-for-a-non-returning-user" risk is real, so the refresh is a notification, not an action.

## What gets discarded

LangGraph, CrewAI, smolagents, AutoGen, OpenDeepResearch (as runtimes; usable as pattern sources). Plugins/Skills as the entry point (defeats auditability). RAGAS/TruLens/DeepEval/FActScore (canon-uncovered, no effectiveness data). Gemini/Perplexity as the engine (no Claude-stack synergy; same reference class as the chosen hosted engine). Multi-engine cross-checking (cost doubles, no quality data).

## Named tradeoffs

| tradeoff | what we give up | what we get |
|---|---|---|
| Three-mode fork instead of one architecture | A clean one-line answer | A defensible answer that survives the scout/principal extremes |
| Local retrieval primary, hosted engine demoted | Hosted-engine recall and breadth | Auditable URL set; no opaque-vendor ceiling on citation correctness |
| Cross-family verifier (Haiku verifies Opus) | Single-vendor simplicity; one model is cheaper | Breaks the correlated-error failure mode the frame-challenger named |
| Three-bucket verifier output | The reassuring single green checkmark | Surfaces unverifiability rather than papering over it |
| Hard fan-out cap (3-wide, 15× chat tokens) | Some long-horizon research breadth | Prevents the "Valley of Death" cost-blowout failure mode |
| Routine as notification, not action | Hands-off freshness | User stays in the loop; system doesn't drift under the user |
| Mode-P refuses to synthesize | The "just give me a report" affordance | Doesn't license user trust the pipeline cannot earn |

## Named assumptions (≥3 that would flip the recommendation if wrong)

1. **The user can place themselves in S/D/P with reasonable accuracy.** If users systematically over-place themselves in P (false sophistication) or under-place in S (false thrift), the recommendation produces overhead-without-benefit (P-as-S) or false-confidence (S-as-D). The whole framing depends on user calibration; if calibration is bad, the recommendation is worse than "always use hosted."

2. **A cross-family LLM verifier produces uncorrelated errors with the producer.** This is the load-bearing assumption behind the verifier surviving the frame-challenger's false-god critique. It is plausible (different training data mixtures, different RLHF) but **not measured** — outside-view's gap #3 explicitly flagged verifier effectiveness as unquantified. If Haiku-verifying-Opus shares the producer's blind spots (same web data, similar refusal patterns), the gate is theatre.

3. **Citation hallucination is the dominant failure mode.** This came from outside-view; if the dominant failure is actually *omission* (the agent missed an entire relevant body of work), then a citation verifier is the wrong gate — what the user needs is a *coverage* check, which no element in the composition provides.

4. **Hosted engines remain at 40–55% joint success and don't improve.** If Anthropic Research / OpenAI DR ship a per-claim verifier next quarter that closes the 5–15% citation gap, Mode D collapses into Mode S — the local pipeline's value proposition disappears.

5. **The user has at least one weekly research need.** If research is one-shot, the Routine refresh and the slash command + hook setup are pure setup cost. The recommendation collapses to "use hosted, accept the error, move on."

## Named ways this could be wrong

- **The three-mode fork is itself the research-theater the classifier warned about.** A simpler answer — "use Anthropic Research; for the 5% of queries where you cannot accept the error, do it by hand" — may be strictly better, since most users do not have stable enough research needs to maintain the Mode-D composition.
- **The cross-family verifier may not exist as a Claude Code primitive yet.** Hooks can invoke another `claude -p` with a different model, but the latency and cost accounting around it is unproven; if it triples the cost without halving the error, it loses.
- **The canon's reliance on Anthropic-authored sources** (librarian's missed gap) means the entire mental model — orchestrator-worker, 5-axis rubric, just-in-time context — is one vendor's architectural taste presented as best practice. The recommendation inherits that bias and amplifies it.
- **Mode P may be unreachable for most users.** Telling a user "actually, do the synthesis yourself" is a valid recommendation but a poor product experience; users will route around it by collapsing to Mode D and over-trusting the green-bucket output. The honest recommendation may need to *refuse to ship Mode D as a one-command experience* to prevent that drift.

## Frame-level objection addressed

The frame-challenger's objection was: *the recommendation must name which user it is for, or it is unfalsifiable.* This recommendation forks on exactly that axis (S/D/P), and refuses to collapse to a single answer. It accepts the corollary cost — there is no one-line SOTA — because the alternative is a recommendation that is right for one user-class and malpractice for the other two.
