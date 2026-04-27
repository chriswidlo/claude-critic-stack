## Source agent
canon-librarian

## Invocation summary
Orchestrator asked canon for guidance on what to do with a regression/golden-master test artifact that exists on disk, is referenced in docs, but has never executed (option (a) run-it-now vs option (b) defer-and-patch-docs). Librarian returned `Partial` corpus coverage: one in-corpus source with quotable text (Google SRE 2016) and four stub entries (Beck, Feathers, Meszaros, Fowler) that are likely decisive but not ingested.

## Direct facts (from in-corpus material the agent could actually read)

1. [Google SRE 2016, Ch. 17, Regression tests] Regression tests function as "a gallery of rogue bugs that historically caused the system to fail or produce incorrect results," documented at system/integration level so refactoring engineers don't reintroduce them. (confidence: direct)
2. [Google SRE 2016, Ch. 17, Build/Test env] CI prescription: "the latest version of a software project in source control is working completely"; broken builds should cause engineers to "drop all of their other tasks." (confidence: direct)
3. [Google SRE 2016, Ch. 17, testing culture] "If every bug is converted into a test, each test is supposed to initially fail because the bug hasn't yet been fixed." Expected first state of a fresh regression test is fail, not pass. (confidence: direct)
4. [Google SRE 2016, Ch. 17, cost of testing] Tests have non-trivial cost; system/E2E tests with full dependency bring-up "can take significantly more time — from several minutes to multiple hours — and possibly require dedicated computing resources." (confidence: direct)
5. [Google SRE 2016, Ch. 11, On-Call] "You never run out of cleanup work" — documentation/config cleanup is framed as legitimate first-class work, not cop-out. (confidence: direct)

## Inferred claims (librarian's synthesis on top of the quotes)

1. [canon-librarian] A regression test that has never executed cannot perform the SRE-defined function of a regression test, since it neither documents a real prior failure nor protects against re-introduction. Inferred from fact 1. (confidence: inferred)
2. [canon-librarian] On-disk-but-uncIed tests are "Schrödinger tests" outside the SRE CI loop. Inferred from fact 2. (confidence: inferred)
3. [canon-librarian] If the unrun fixture is a heavyweight system/E2E artifact, "run it now" can balloon into a multi-hour environment bootstrap, which is when option (b) becomes correct triage rather than laziness. Inferred from fact 4. (confidence: inferred)
4. [canon-librarian] Patching docs that point at non-existent state can be the actual user-visible harm; option (b) is supportable when the fixture's absence is not currently blocking anyone. Inferred from fact 5. (confidence: inferred)
5. [canon-librarian] A non-trivial fraction of newly-authored regression tests are aspirational (red on first execution); plan for that. Inferred from fact 3. (confidence: inferred)

## Authority-framed claims

1. "Kent Beck ... almost certainly contains the canonical 'if it didn't run, it doesn't exist' formulation" — underlying claim: TDD discipline says an unrun test does not exist as a test. Quote present in output: no (stub). Confidence: unsupported.
2. "Michael Feathers ... canonical reference for *characterization tests* — tests that pin down current behavior before you trust them" — underlying claim: an unrun golden-master should be treated as a hypothesis, not a fixture, until characterized. Quote present in output: no (stub). Confidence: unsupported.
3. "Gerard Meszaros ... catalogs test smells ... fixtures that have drifted from the system under test" — underlying claim: golden-master hygiene literature would likely deem this a known smell. Quote present in output: no (stub). Confidence: unsupported.
4. "Martin Fowler, *Refactoring* (2nd ed., 2018) ... general 'tests must be runnable and run' discipline" — underlying claim: refactoring discipline requires runnable, run tests. Quote present in output: no (stub). Confidence: unsupported.

Librarian was disciplined: explicitly refused to invent quotes for stubs ("I will not invent a quote").

## Contradictions surfaced

The librarian's *supporting* passages (SRE Ch. 17 regression tests + CI: bring it into the loop, run it, expect it to fail) push toward option (a) **run-it-now**.

The librarian's *contradicting/complicating* passages push toward option (b) **defer-and-patch-docs**:
- SRE Ch. 17 cost-of-testing: heavyweight fixtures have real activation cost; "just run it" assumes negligible cost.
- SRE Ch. 11 cleanup-work aside: doc/config rot is first-class debt; patching docs that point at non-existent state is legitimate hygiene work, not avoidance.

Both poles cite the same book (Google SRE 2016). The contradiction is internal to one source, not cross-source — the librarian framed it as the SRE book's CI-rigor norm vs. the SRE book's cost-awareness/cleanup norm. Mandatory contradicting-passage requirement was met.

## Subagent's own verdict (verbatim)

"Corpus coverage: Partial."

## Gaps the subagent missed (and explicitly declared)

- **Snapshot / golden-master / approval testing as a discipline is not represented in the corpus at all** (Bache, approval-tests, etc.). Librarian flagged this as "the topic-shaped hole most worth flagging." **Orchestrator should weight: the canon may not be the right authority for this specific question.** The single readable in-corpus source (SRE 2016) speaks to regression tests in general, not to golden-master/approval-test hygiene specifically.
- No measured base rate for "unrun-but-long-declared regression test passes on first execution." (Hand-off to outside-view.)
- No broken-window-theory treatment of docs pointing at non-existent fixtures.
- No triage rubric specific to "defer-vs-run-now for test artifacts" (as distinct from features/incidents).
- The four most directly on-point references (Beck, Feathers, Meszaros, Fowler) are all stubs. The corpus's strongest authority on this question is structurally absent; downstream synthesis should treat canon weight as **partial**, not decisive.

## Token budget
~720 tokens.
