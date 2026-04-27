## Source agent
canon-librarian

## Invocation summary
Orchestrator queried canon for guidance on whether to document a structural split (e.g., README/manifest/index) before confusion has materialized, vs. letting structure self-document. Librarian returned thin coverage: only SRE 2016 is ingested; Fowler, Feathers, Beck are stubs.

## Direct facts
1. [SRE 2016, Being On-Call / Playbooks] "When humans are necessary, we have found that thinking through and recording the best practices ahead of time in a 'playbook' produces roughly a 3x improvement in MTTR as compared to the strategy of 'winging it.'" (confidence: direct)
2. [SRE 2016, Software Engineering in SRE — Negative Lines of Code] "hundreds of lines of commented code create distractions and confusion (especially as the source files continue to evolve) ... every line of code changed or added to a project creates the potential for introducing new defects." (confidence: direct)
3. [SRE 2016, Postmortem Culture] "There is no better way to learn than to document what has broken in the past." (confidence: direct)
4. [SRE 2016, Foreword (Burgess)] "Implementations are ephemeral, but the documented reasoning is priceless. Rarely do we have access to this kind of insight." (confidence: direct)
5. [canon-librarian] Fowler Refactoring (Comments smell), Feathers Working Effectively with Legacy Code, and Beck TDD are all body_completeness: stub — no ingested body text. (confidence: direct)

## Inferred claims
1. [canon-librarian] Playbook passage argues for documenting procedural intent *before* asymmetry/confusion has bitten, when cost of confusion is high. (confidence: inferred)
2. [canon-librarian] Negative-Lines-of-Code passage implies every artifact — prose explainers included — is a liability that can drift; bias toward non-creation when structure carries the meaning. (confidence: inferred)
3. [canon-librarian] Postmortem-Culture passage implies documentation-of-divergence is cheap insurance once divergence has caused real confusion; trigger is "this broke something," not "this could conceivably confuse." (confidence: inferred)
4. [canon-librarian] Burgess Foreword cuts against "let structure self-document": structure shows what, prose captures why; if split encodes a non-obvious decision, reasoning is not recoverable from file contents. (confidence: inferred)
5. [canon-librarian] README-as-load-bearing-artifact (monorepos, AI-assisted codebases) is a post-2020 phenomenon not covered by the ingested corpus. (confidence: inferred)

## Authority-framed claims
None. Librarian named authors only as citation handles for verbatim quotes; no "as X argues" ventriloquism.

## Contradictions surfaced
- **Document procedurally ahead of time** (SRE Playbooks, 3x MTTR improvement) and **document the why because reasoning is otherwise lost** (Burgess Foreword) — push toward writing the explainer before confusion arrives.
  vs.
- **Every added artifact is a liability that drifts** (SRE Negative Lines of Code) and **trigger for divergence-docs is real breakage, not hypothetical confusion** (Postmortem Culture, librarian's inference) — push toward not writing until something has actually broken.

## Subagent's own verdict (verbatim)
"## Corpus coverage
Thin."

## Gaps the subagent missed
- No coverage of README/manifest/index file genre as a distinct artifact class.
- No entry names "premature documentation" as an antipattern.
- Documentation rot/drift only touched at edges.
- Fowler Comments smell, Feathers legacy-seam documentation, Beck TDD all stubbed — top three to close.
- Did not address whether AI-assisted-codebase context changes the calculus (flagged as out-of-corpus but not analyzed).
- Suggested single WebSearch provided but not executed: "premature documentation" OR "documentation rot" OR "comments as deodorant" Fowler Feathers code smell intent README drift.

## Token budget
~520 tokens.
