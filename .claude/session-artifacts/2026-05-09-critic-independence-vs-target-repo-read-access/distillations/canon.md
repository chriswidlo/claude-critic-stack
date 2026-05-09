## Source agent
canon-librarian

## Invocation summary
Orchestrator asked the librarian to retrieve corpus material on critic independence vs. target-repo read access (whether allowing critics to read the artifact under review compromises their independence). Librarian returned 10 passages split supporting / contradicting, plus stubs and gaps. Coverage declared **partial**.

## Direct facts (with full citations)

### Supporting passages — independence threatened by shared input

1. [Anthropic, "How we built our multi-agent research system" (2025), §Why multi-agent systems work] Each subagent provides "separation of concerns — distinct tools, prompts, and exploration trajectories — which reduces path dependency and enables thorough, independent investigations." (confidence: direct)

2. [Anthropic, "Effective context engineering for AI agents" (2025), §Why context engineering is important] "Context rot": as tokens in the window increase, recall accuracy decreases; LLMs have an "attention budget" depleted by every new token. (confidence: direct)

3. [Anthropic, "Effective context engineering for AI agents" (2025), §Context retrieval and agentic search] Agentic search enables "progressive disclosure" — agents incrementally discover relevant context rather than "drowning in exhaustive but potentially irrelevant information." (confidence: direct)

4. [Anthropic, "Building effective agents" (2024), §Workflow: Parallelization] Parallelization is effective when "multiple perspectives or attempts are needed for higher confidence results"; example given is several different prompts reviewing code for vulnerabilities. (confidence: direct)

5. [Wang, Li, Deng, Roth, Li, "Devil's Advocate: Anticipatory Reflection for LLM Agents," *Findings of EMNLP 2024*, abstract only] Mechanism is a three-fold introspective intervention by the same agent: anticipatory reflection, post-action alignment with backtracking, and comprehensive review on plan completion. (confidence: direct, but **abstract-only ingest** — full PDF not parsed)

### Contradicting passages — grounding *improves* judgment

6. [Beyer, Jones, Petoff, Murphy (eds.), *Site Reliability Engineering* (Google/O'Reilly, 2016), Ch. 32 "The Evolving SRE Engagement Model"] In the PRR Analysis phase, "SRE reviewers learn about the service and begin analyzing it for production shortcomings … examine the service's design and implementation" and review recent incidents/postmortems. (confidence: direct)

7. [Beyer et al., *SRE* (2016), Ch. 36] For SRE-built tools with broad adoption: "Have another SRE team review the product for production readiness as they would if onboarding any other service." (confidence: direct)

8. [Beyer et al., *SRE* (2016), Ch. 15 "Postmortem Culture"] A blameless postmortem "assumes that everyone involved in an incident had good intentions"; effectiveness comes from investigating systematic reasons for incomplete information, not from allocating blame. (confidence: direct)

9. [Anthropic, "How we built our multi-agent research system" (2025), §Evaluation] "We experimented with multiple judges to evaluate each component, but found that a single LLM call with a single prompt outputting scores from 0.0–1.0 and a pass-fail grade was the most consistent and aligned with human judgements." (confidence: direct)

10. [Anthropic, "How we built our multi-agent research system" (2025), §Lessons learned] "Some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today … most coding tasks involve fewer truly parallelizable tasks than research." (confidence: direct)

## Inferred claims (librarian's relevance commentary)

1. [canon-librarian] Anthropic's multi-agent design treats *separation of context windows* (not just role) as load-bearing; current critic stack provides distinct prompts but allows shared target-repo input across all three lenses, exposing the "path dependency" failure mode. (confidence: inferred)

2. [canon-librarian] Routing target repo into critic prompts spends attention budget that would otherwise apply to the candidate — input-minimalism argument independent of the independence question. (confidence: inferred)

3. [canon-librarian] Architectural middle ground: critics receive *references* (path/query handle) rather than pre-loaded content, pulling only what their frame demands. Decorrelates inputs while preserving optional grounding. (confidence: inferred)

4. [canon-librarian] Anthropic's parallelization framing does *not* claim independence in the statistical sense; the implicit assumption is *prompt orthogonality*, which supports re-justifying the panel on role-orthogonality more than on input isolation. (confidence: inferred)

5. [canon-librarian] PRR is the closest industrial analogue to a critic-operations lens and is *defined by* grounding in the target service; without it, operations-readiness critique reduces to abstract design critique — a weaker judgment. (confidence: inferred)

6. [canon-librarian] In SRE practice, independence is achieved by *team identity* (another SRE team), not by input deprivation: "correlated review error is mitigated by reviewer-set diversity, not by input deprivation." This maps onto shadow-comparator (cross-model triangulation on identical inputs) more naturally than onto an input-isolation regime. (confidence: inferred)

7. [canon-librarian] By analogy from blameless postmortems: panel fairness comes from *frame discipline* (lens-specific question, role-orthogonality, upstream frame-challenger), not information isolation. (confidence: inferred)

8. [canon-librarian] Anthropic's production experience pushed *away* from a multi-judge panel toward a single well-prompted judge with a clear rubric — direct evidence against the implicit "more lenses = better" assumption. Caveat: rubric was for research-output grading, more objective than design review. (confidence: inferred)

9. [canon-librarian] Critics-on-a-design-decision is closer to the "shared context, dependencies" regime Anthropic flags as a bad fit for multi-agent decomposition; the response is not "fix the inputs" but "reconsider whether parallel decomposition is the right architecture." (confidence: inferred)

## Authority-framed claims
None detected. Librarian quoted sources directly; no "as X argues" ventriloquy.

## Contradictions surfaced

- **Separation vs. grounding (load-bearing tension):**
  - Passage 1 (Anthropic multi-agent, 2025): separation of context windows reduces path dependency.
  - Passage 6 (SRE Ch. 32): PRR reviewers must study design, implementation, incidents, postmortems of the artifact.

- **Reviewer diversity mechanism — input isolation vs. team/identity diversity:**
  - Passage 1 implies path-dependency fix is separation of input/context.
  - Passage 7 (SRE Ch. 36): independence comes from *another team* applying the *same grounded review*.

- **Panel-of-judges vs. single rubric judge:**
  - Passage 4 (Anthropic 2024): multiple perspectives → higher confidence.
  - Passage 9 (Anthropic 2025): production experience preferred a single well-prompted judge over multiple judges.

- **Multi-agent decomposition fit:**
  - Passages 1 & 4 endorse parallel subagents/critics.
  - Passage 10 warns coding/shared-context tasks are a poor fit for multi-agent decomposition today.

## Subagent's own verdict (verbatim)
"**partial.**" (corpus coverage)

## Gaps the subagent missed / declared unanswered
1. LLM-judge calibration vs. independence trade-off, quantified — no corpus entry compares judge accuracy with vs. without artifact access. WebSearch likely warranted (2024–2026 LLM-as-judge literature on grounded vs. blind judging).
2. Correlated error rates across same-family judges on identical inputs — corpus does not separate inter-lens / inter-model / inter-input correlation empirically.
3. Anchoring effects in LLM evaluators specifically — established for humans, not given for LLM critics.
4. Staleness flag — Anthropic posts 2024–2025; SRE book 2016. Field has shifted toward "rubric quality and reference-grounding dominate"; 2026 retrieval against current LLM-evaluation literature recommended before locking a recommendation.

Stubs limiting retrieval:
- `chen-devils-advocate-2024` — abstract-only; mechanism details on adversarial role with vs. without grounding are in the unparsed full PDF.
- `march-exploration-exploitation-1991` — declared stub.
- `nygard-release-it`, `hohpe-eip` — stubs (citation.yaml only); contain Bulkhead and channel/decoupling primitives relevant to review-process isolation but not quotable.

## Token budget
~1,150 tokens.
