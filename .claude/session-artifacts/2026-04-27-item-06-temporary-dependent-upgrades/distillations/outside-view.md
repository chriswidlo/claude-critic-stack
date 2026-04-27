## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on four options for handling two upgrade entries that depend on a directory preserved on a sibling branch (not on `main`). Subagent returned a primary reference class (deferred personal-KB notes / ADR dropped-entries), qualitative base-rate estimates per option, position-relative analysis, failure modes, and a verdict.

## Direct facts
1. [Corry et al. 2021, arXiv, "Zombie Datasets" paper] "the persistence of references after the underlying artifact has moved is the source of harm, not the move itself." (confidence: direct)
2. [Corry et al. 2021] Their prescription is "active communication of deprecation, not passive parking." (confidence: direct)
3. [arXiv 2022, "Detecting Outdated Code Element References in Software Repository Documentation"] Empirical finding: outdated references are the modal state, not the exception. (confidence: direct)
4. [Subagent self-report] Canon corpus directory read failed this run; canon stubs (Hickey, Heuer, Heilmeier) were invoked from memory, not Grep-verified. (confidence: direct)
5. [Subagent self-report] No published rates exist for this micro-class; per-option percentages are qualitative estimates. (confidence: direct)

## Inferred claims
1. [outside-view] Option (b) supersede-with-honest-negation has the best estimated resolution rate (~70–80%) and lowest zombie risk because `superseded` is terminal in ADR practice. (confidence: inferred)
2. [outside-view] Option (c) ⏸️-park has the highest zombie risk (~70% stay dormant); resume conditions are rarely tripped or noticed. (confidence: inferred)
3. [outside-view] Option (d) write-a-new-rule has ~80% zombie rate; canonical failure mode is "rule inflation" / "process for a population of one." (confidence: inferred)
4. [outside-view] Option (a) restore risks the asset diverging between `main` and the worktree branch within ~6 months, recurring the original cross-branch reference problem in inverted form. (confidence: inferred)
5. [outside-view] Option (d) is itself an instance of the class it tries to govern (meta-risk). (confidence: inferred)
6. [outside-view] Two entries already in this state suggests a pattern, not a one-off — but not yet enough recurrence to justify (d). Threshold proposed: ≥5 more cross-branch references in 6 months, or a third instance. (confidence: inferred)
7. [outside-view] Lifecycle "superseded" is native to the stack already; (b) is not a new convention. (confidence: inferred)
8. [outside-view] If (c) is chosen, it should carry a date-bound (not event-bound) resume trigger plus a default-to-supersede if date passes untouched. (confidence: inferred)
9. [outside-view] If only reason to restore is to fix references, (a) "solves a documentation problem with a structural change — wrong tool." (confidence: inferred)

## Authority-framed claims
1. "The Heuer / Tetlock observation applies: explicit deferral mechanisms ('park', 'watch list') are *underused as terminal states*." — underlying claim: people add to deferral lists but rarely remove items; ADR's "Superseded" works because it is terminal. Quote present in output: no. Confidence: unsupported.
2. "Hickey's 'Hammock' works only when the hammock is actively revisited; in practice, items put down stay down." — underlying claim: deferral mechanisms require active revisit to function. Quote present in output: no. Confidence: unsupported.
3. "The Heilmeier catechism (in your ingest queue) bites option (d) directly: 'What are the midterm and final exams?' — a one-shot rule has no exam." — underlying claim: a rule applied once with no recurring evaluation criterion fails Heilmeier's test. Quote present in output: yes (the "midterm and final exams" phrase, partial). Confidence: direct on the phrase, inferred on the application to (d). Heilmeier flagged as ingest-queue, not yet canon.
4. "In ADR practice this is called 'process for a population of one.'" — underlying claim: ADR community has a named anti-pattern for governance written for non-recurring situations. Quote present in output: no. Confidence: unsupported.

## Contradictions surfaced
- None internally. The subagent's four options are scored against each other but the analysis is internally consistent. No contradicting passage was carried through (the subagent flagged that canon read failed, so contradicting-passage retrieval did not run).

## Subagent's own verdict (verbatim)
"Below base rate for options (c) and (d). Within tolerance for (b). Mixed for (a)."

## Gaps the subagent missed
- **Canon read failed** — Mandatory #0 (canon-first) was not actually executed this run. Orchestrator should weigh this: the outside-view verdict rests on web sources + memory of canon stubs, not verified canon retrieval. Re-invoke canon-librarian explicitly for Hickey, Heuer, Heilmeier, and any ADR-status-handling entries.
- **No quantification of "how often does this kind of cross-branch reference recur in this repo"** — the (d)-threshold ("≥5 more in 6 months" or "third instance") is asserted, not derived from repo history. A grep over prior session artifacts could ground this.
- **Option (b)'s "honest-negation pointer" content is not specified** — what minimum information makes the negation note load-bearing vs. terse? Subagent gestured at "one sentence of context" but did not specify fields.
- **No analysis of hybrid options** (e.g., supersede now + restore later if independent need arises). Subagent treated the four options as mutually exclusive.
- **No reference-class check on the cost of the (d) rule itself** — even if rule-inflation risk is ~80%, the cost of an unused rule may be near-zero in a solo repo. Subagent assumed nonzero ongoing cost without sizing it.

## Token budget
~780 tokens.
