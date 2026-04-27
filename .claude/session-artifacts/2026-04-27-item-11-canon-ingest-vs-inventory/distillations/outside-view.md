## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on whether to write a clarifying README paragraph distinguishing two canon YAMLs (sources.ingest.yaml vs inventory) in a solo-maintained tooling repo. Subagent returned a "below base rate" verdict with the recommendation to close as overtaken-by-events.

## Direct facts
1. [outside-view] No hard numbers in canon exist for this exact reference class. (confidence: direct)
2. [outside-view] The punch-list author's confusion was about the librarian's behavior, not about the two YAMLs' relationship. (confidence: direct)
3. [outside-view] The canon directory recently underwent a folder-shape migration. (confidence: direct)
4. [outside-view] No WebSearch was performed; canon corpus (Ousterhout, Brooks neighborhood) was consulted. (confidence: direct)

## Inferred claims
1. [outside-view] Speculative clarifying docs in solo repos prevent a future misread roughly 20–35% of the time. (confidence: inferred — qualitative prior, no hard numbers)
2. [outside-view] Docs written in response to an actual attested misread succeed 50–60% of the time. (confidence: inferred — qualitative prior)
3. [outside-view] This case sits closer to the speculative end because the originating confusion was not about the YAMLs themselves. (confidence: inferred)
4. [outside-view] Typical failure mode: doc is briefly accurate, then a future refactor (rename, merge, absorb sources.ingest.yaml into a generated artifact) silently invalidates the paragraph for 6+ months. (confidence: inferred)
5. [outside-view] Second-most failure mode: paragraph is correct but ignored — readers prone to misreading the YAMLs do not read canon/README.md first. (confidence: inferred)
6. [outside-view] Pulling-up factor: the paragraph is cheap and small. (confidence: inferred)
7. [outside-view] Lift condition for revisiting: a second reader independently misreads the relationship, converting it from speculative to attested. (confidence: inferred)

## Authority-framed claims
1. "Qualitative priors from corpus neighborhood (Ousterhout on comments-as-design, Brooks on doc rot, YAGNI literature)" — underlying claim: these authors' positions support treating speculative clarifying docs as low-yield and doc-rot-prone. Quote present in output: no. Confidence: unsupported (no quotes; ventriloquized neighborhood reference).

## Contradictions surfaced
None within the subagent's return. The subagent presented one consistent forecast direction (below base rate) with both a pulling-down and a pulling-up factor named, but no contradicting passages were retrieved or surfaced.

## Subagent's own verdict (verbatim)
"Below base rate. Close as overtaken-by-events with a one-line note. Lift condition: write paragraph only if/when a *second* reader independently misreads the relationship — then it's attested, not speculative."

## Gaps the subagent missed
- No quoted canon passages — the Ousterhout/Brooks/YAGNI references are neighborhood-level rather than direct citations. Orchestrator should rely on canon-librarian distillation for actual passages.
- No estimate of the cost side of the cheap-and-small factor (e.g., maintenance cost of a stale paragraph versus zero-cost of not writing).
- No discussion of whether absorbing sources.ingest.yaml into a generated artifact is actually planned or merely hypothetical — the failure-mode scenario is presented as plausible without grounding.
- No reference class for "two-file naming-confusion docs" specifically; the chosen class is broader (speculative clarification docs generally).

## Token budget
~430 tokens.
