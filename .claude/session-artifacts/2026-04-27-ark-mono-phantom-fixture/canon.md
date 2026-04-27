## Corpus coverage

Partial. The most directly on-point works in the corpus — Beck (TDD), Feathers (Working Effectively with Legacy Code), and Meszaros (xUnit Test Patterns) — are all **stub entries** (paywalled, owned-text not yet ingested). I cannot quote them. The single corpus work with executable text on this topic is the Google SRE book (2016), which carries useful material on the *purpose* of regression tests and on cleanup-work prioritization. Net: the corpus can speak to the framing, but the canonical test-discipline references that would most cleanly resolve the question are unavailable.

## Supporting passages

1. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 17 "Testing for Reliability" — System tests > Regression tests.**
   > "Regression tests can be analogized to a gallery of rogue bugs that historically caused the system to fail or produce incorrect results. By documenting these bugs as tests at the system or integration level, engineers refactoring the codebase can be sure that they don't accidentally introduce bugs that they've already invested time and effort to eliminate."
   Relevance: A regression test that has *never executed* cannot serve this function — it neither documents a real prior failure nor protects against re-introduction. This is the strongest in-corpus argument for option (a): run it now, because until it runs the artifact does not actually do the job a regression test exists to do.

2. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 17 — Creating a Test and Build Environment.**
   > "Once source control is in place, you can add a continuous build system that builds the software and runs tests every time code is submitted. ... It's essential that the latest version of a software project in source control is working completely. When the build system notifies engineers about broken code, they should drop all of their other tasks and prioritize fixing the problem."
   Relevance: Tests on disk that are not wired into CI and have never run sit outside this loop entirely — they are Schrödinger tests. The SRE prescription is to bring them into the build, not to document around them.

3. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 17 — testing culture.**
   > "If every bug is converted into a test, each test is supposed to initially fail because the bug hasn't yet been fixed. As engineers fix the bugs, the software passes testing and you're on the road to developing a comprehensive regression test suite."
   Relevance: The expected first state of a fresh regression test is **fail**, not pass. This complicates the user's implicit assumption that running an unrun test is a quick formality — historically a meaningful fraction of newly authored regression tests are aspirational and red on first execution. Plan for that, not against it.

## Contradicting or complicating passages

1. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 17 — cost of testing.**
   > "It's important to note that tests have a cost, both in terms of time and computational resources. At one extreme, unit tests are very cheap ... At the other end of the spectrum, bringing up a complete server with required dependencies (or mock equivalents) to run related tests can take significantly more time—from several minutes to multiple hours—and possibly require dedicated computing resources. Mindfulness of these costs is essential to developer productivity, and also encourages more efficient use of testing resources."
   Why this complicates the framing: The "just run it" instinct assumes negligible activation cost. Golden-master/fixture generation often needs a representative environment, real I/O, or production-like data; if the test is a heavyweight system or end-to-end fixture, "run it now" can quietly turn into a multi-hour environment-bootstrap project. That is when option (b) — defer-and-patch-docs — stops being lazy and starts being correct triage.

2. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 11 "Being On-Call" — aside on cleanup work.**
   > "You never run out of cleanup work. Your ticket count might be at zero, but there is always documentation that needs updating, configs that need cleanup, etc. Your future on-call engineers will thank you, and it means they're less likely to interrupt you during your precious make time."
   Why this complicates the framing: Frames the choice in the opposite direction from passage #2 above. Doc-rot and config-rot are first-class debt; patching docs that point at non-existent state is *not* a cop-out, it is the kind of grungy hygiene work the SRE book elsewhere praises. Used carefully this supports option (b) when the doc-fix is the actual user-visible harm and the fixture's absence is not currently blocking anyone.

## Stub entries that would likely be decisive if ingested

- **Kent Beck, *Test-Driven Development: By Example* (2002).** ISBN 978-0321146533. *Stub; full text not ingested.* Almost certainly contains the canonical "if it didn't run, it doesn't exist" formulation, but I will not invent a quote.
- **Michael Feathers, *Working Effectively with Legacy Code* (2004).** ISBN 978-0131177055. *Stub; full text not ingested.* The canonical reference for *characterization tests* — tests that pin down current behavior before you trust them. Directly relevant to "should an unrun golden-master be trusted as a fixture or treated as a hypothesis?" but unavailable to quote.
- **Gerard Meszaros, *xUnit Test Patterns* (2007).** ISBN 978-0131495050. *Stub; full text not ingested.* Catalogs test smells including "Test Code Duplication," "Obscure Test," and notably the family around fixtures that have drifted from the system under test. Would likely be decisive on golden-master hygiene; unavailable to quote.
- **Martin Fowler, *Refactoring* (2nd ed., 2018).** ISBN 978-0134757599. *Stub; full text not ingested.* General "tests must be runnable and run" discipline; unavailable to quote.

## Gaps the corpus does not answer

- **Base rate that a long-undeclared-but-unrun regression test passes on first execution.** No in-corpus passage gives a number; the SRE bug-to-test passage hints "expect fail," but that is a prescription, not a measured base rate.
- **Broken-window theory applied to documentation pointing at non-existent fixtures.** Not directly addressed in the readable corpus. (Kerievsky / Hunt-Thomas territory; not currently ingested.)
- **Triage rubric for "defer-vs-run-now" specifically for test artifacts** as opposed to feature work or incidents. The SRE book treats tests as production code worthy of CI, but does not offer a defer-with-known-debt protocol for the specific case of an unrun fixture.
- **Snapshot/golden-master testing as a discipline** (Emily Bache, approval testing, etc.) is not represented in the corpus at all. This is the topic-shaped hole most worth flagging.

## Staleness note

The Google SRE book is from 2016. Its core claims about regression tests as a "gallery of rogue bugs" and about CI being non-negotiable have, if anything, hardened since then; these are not stale. The *absence* of modern snapshot/approval-testing references (Bache 2022, etc.) is a corpus gap, not a staleness issue with what is present.
