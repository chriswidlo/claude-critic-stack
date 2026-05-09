# Canon retrieval — critic independence vs. target-repo read access

## Corpus coverage
**partial.** Direct on-point material exists on multi-agent context separation (Anthropic multi-agent research system; context engineering; building effective agents) and on review processes that are deliberately *grounded* in the artifact under review (Google SRE: PRR, code review, blameless postmortem). Coverage is weaker on LLM-as-judge calibration vs. independence trade-offs, on correlated error in panels of judges, and on anchoring effects in LLM evaluation. The closest direct adversarial-review entry — `chen-devils-advocate-2024` — is ingested as **abstract only** (ACL Anthology landing page; full PDF not parsed). `march-exploration-exploitation-1991`, `nygard-release-it`, and `hohpe-eip` are stubs.

## Supporting passages — for the user's framing (independence threatened by shared input)

### 1. Anthropic, "How we built our multi-agent research system" (2025), §Why multi-agent systems work
> "The essence of search is compression: distilling insights from a vast corpus. Subagents facilitate compression by operating in parallel with their own context windows, exploring different aspects of the question simultaneously before condensing the most important tokens for the lead research agent. **Each subagent also provides separation of concerns — distinct tools, prompts, and exploration trajectories — which reduces path dependency and enables thorough, independent investigations.**"

Relevance: Anthropic's own design treats *separation of context windows* (not just role) as load-bearing. The current critic stack provides distinct prompts/roles per lens but allows shared input (target-repo content) into all three — this passage names *path dependency* as exactly the failure mode separation is meant to prevent.

### 2. Anthropic, "Effective context engineering for AI agents" (2025), §Why context engineering is important
> "Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases. … LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM."

Relevance: Routing a target repo into critic prompts is not free — it spends attention budget that would otherwise apply to the candidate, and risks context rot in lens-specific reasoning. Indirect input-minimalism argument independent of the independence question.

### 3. Anthropic, "Effective context engineering for AI agents" (2025), §Context retrieval and agentic search
> "Letting agents navigate and retrieve data autonomously also enables progressive disclosure — in other words, allows agents to incrementally discover relevant context through exploration. … This self-managed context window keeps the agent focused on relevant subsets rather than drowning in exhaustive but potentially irrelevant information."

Relevance: An architectural middle ground for the "isolate vs. ground" axis: critics receive *references* (path, query handle) rather than pre-loaded target content, and pull only what their frame demands. Each lens loads what its frame requires, decorrelating inputs while preserving optional grounding. Mirrors Claude Code's own pattern (CLAUDE.md up front; glob/grep just-in-time).

### 4. Anthropic, "Building effective agents" (2024), §Workflow: Parallelization
> "Parallelization is effective when the divided subtasks can be parallelized for speed, or when **multiple perspectives or attempts are needed for higher confidence results**. … Reviewing a piece of code for vulnerabilities, where several different prompts review and flag the code if they find a problem."

Relevance: Anthropic's canonical framing for the panel-of-critics pattern is "multiple perspectives … for higher confidence results." Note: it does *not* claim those perspectives are independent in the statistical sense. The implicit assumption is *prompt orthogonality*. This supports the alternative position from `frame.md` (re-justify the panel on role-orthogonality) more than it supports input isolation.

### 5. Wang, Li, Deng, Roth, Li, "Devil's Advocate: Anticipatory Reflection for LLM Agents," *Findings of EMNLP 2024*, §Abstract (abstract only ingested)
> "We implement a three-fold introspective intervention: 1) anticipatory reflection on potential failures and alternative remedy before action execution, 2) post-action alignment with subtask objectives and backtracking with remedy to ensure utmost effort in plan execution, and 3) comprehensive review upon plan completion for future strategy refinement."

Relevance: The mechanism is *adversarial reflection by the same agent on the same plan* — independence by role/timing, not by input isolation. The devil's-advocate role explicitly sees the artifact under review. (Caveat: only the abstract is ingested; do not draw stronger conclusions than the abstract supports.)

## Contradicting / complicating passages — grounding in the artifact *improves* judgment

### 6. Beyer, Jones, Petoff, Murphy (eds.), *Site Reliability Engineering* (Google / O'Reilly, 2016), Ch. 32 "The Evolving SRE Engagement Model"
> "Analysis is the first large segment of work. **During this phase, the SRE reviewers learn about the service and begin analyzing it for production shortcomings. They aim to gauge the maturity of the service along the various axes of concern to SRE. They also examine the service's design and implementation to check if it follows production best practices.** Usually, the SRE team establishes and maintains a PRR checklist explicitly for the Analysis phase. … SREs also look at recent incidents and postmortems for the service, as well as follow-up tasks for the incidents."

Why this complicates: The Production Readiness Review — the closest industrial analogue to a critic-operations lens — is *defined by* its grounding in the target service. Reviewers literally study design, implementation, recent incidents, and postmortems of the artifact. Without that grounding, the operations-readiness claim is meaningless — the lens can only critique the candidate *as an abstract design*, which is a different and weaker judgment.

### 7. Beyer et al., *Site Reliability Engineering* (2016), Ch. 36 (production-readiness for SRE-built tools)
> "If your solution enjoys broad adoption, it may become critical to SREs in order to successfully perform their jobs. Therefore, reliability is of utmost importance. Do you have proper code review practices in place? Do you have end-to-end or integration testing? **Have another SRE team review the product for production readiness as they would if onboarding any other service.**"

Why this complicates: Independence is achieved by *team identity* — *another* SRE team, applying *the same grounded review*. Not by withholding artifact access. Pattern: *correlated review error is mitigated by reviewer-set diversity, not by input deprivation.* This maps onto the existing shadow-comparator (cross-model triangulation on identical inputs) more naturally than onto an input-isolation regime.

### 8. Beyer et al., *Site Reliability Engineering* (2016), Ch. 15 "Postmortem Culture: Learning from Failure"
> "A blamelessly written postmortem assumes that everyone involved in an incident had good intentions and did the right thing with the information they had. … When postmortems shift from allocating blame to investigating the systematic reasons why an individual or team had incomplete or incorrect information, effective prevention plans can be put in place."

Why this complicates: A postmortem is adversarial review of an outcome that *requires* full grounding — timeline, logs, dependencies. The discipline that makes it *fair* is framing rule (blameless, system-level), not context-withholding. By analogy: panel fairness comes from *frame discipline* (lens-specific question, role-orthogonality, upstream frame-challenger) rather than information isolation. Removing target access is not the only — and per the SRE tradition, not the primary — way to control reviewer bias.

### 9. Anthropic, "How we built our multi-agent research system" (2025), §Evaluation
> "We used an LLM judge that evaluated each output against criteria in a rubric: factual accuracy …, citation accuracy …, completeness …, source quality …, and tool efficiency …. **We experimented with multiple judges to evaluate each component, but found that a single LLM call with a single prompt outputting scores from 0.0–1.0 and a pass-fail grade was the most consistent and aligned with human judgements.**"

Why this complicates: Anthropic's production experience pushed *away* from a multi-judge panel toward a single, well-prompted judge with a clear rubric — citing consistency and human-alignment, not inter-judge independence, as the deciding metric. Direct evidence against the implicit "more lenses = better" assumption beneath the framing. (Caveat: rubric was for research-output grading, more objective than design review.) Burden on the panel: *what does each lens uniquely add that one grounded judge with a multi-criterion rubric does not?*

### 10. Anthropic, "How we built our multi-agent research system" (2025), §Lessons learned
> "Some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today. For instance, **most coding tasks involve fewer truly parallelizable tasks than research**, and LLM agents are not yet great at coordinating and delegating to other agents in real time."

Why this complicates: Critics-on-a-design-decision is closer to the "shared context, dependencies between agents" regime than to breadth-first research where parallel subagents shine. Anthropic flags this as a *bad fit* for multi-agent decomposition. If the panel cannot be cleanly decomposed because every lens needs the same target-repo content, the response per this passage is not "fix the inputs" — it is "reconsider whether parallel decomposition is the right architecture."

## Stubs / known gaps surfaced

- `chen-devils-advocate-2024` — abstract-only ingest. Mechanism details that would speak directly to "adversarial role with vs. without artifact grounding" are in the full PDF, not the corpus.
- `march-exploration-exploitation-1991` — declared stub; not directly on point.
- `nygard-release-it` and `hohpe-eip` — stubs (citation.yaml only, no source.txt). Both contain primitives (Bulkhead; channel/decoupling) practitioners cite for review-process isolation; the corpus does not let the librarian quote them.

## Gaps the corpus does not answer

1. **LLM-judge calibration vs. independence trade-off, quantified.** No corpus entry reports an experiment comparing judge accuracy with vs. without access to the artifact. WebSearch likely warranted (2024–2026 LLM-as-judge literature on grounded vs. blind judging).
2. **Correlated error rates across same-family judges on identical inputs.** Shadow-comparator targets this, but the corpus contains no measurement of how much input-sharing (vs. model-family sharing) drives the correlation. The frame's three-way distinction (inter-lens, inter-model, inter-input) is not separated empirically here.
3. **Anchoring effects in LLM evaluators specifically.** Human-judgment anchoring literature is established off-corpus; not in this corpus, and applicability to LLM critics is not given.
4. **Staleness flag.** Anthropic posts are 2024–2025; SRE book is 2016. The "more isolation = more independence" intuition for human reviewers (security red-teaming, blinded peer review) has shifted in the LLM-judge literature toward "rubric quality and reference-grounding dominate." A 2026 retrieval against current LLM-evaluation literature is recommended before locking a recommendation.
