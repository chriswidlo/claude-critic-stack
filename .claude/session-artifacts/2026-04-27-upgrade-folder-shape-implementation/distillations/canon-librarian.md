# canon-librarian distillation — 2026-04-27 upgrade-folder-shape-implementation

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canonical guidance on five implementation choices around a 30-file folder-shape migration (slug/path repetition, single-script-vs-AST, single-batch-vs-per-entry commits, bundling a bug fix, eventual-consistency vs operator-pause vs edit-writer-first). Librarian returned partial coverage: strong on Google SRE Book material (idempotency, release simplicity, modularity, simplicity-as-prerequisite); declared stubs for Fowler, Feathers, Beck, Helland; declared multiple corpus gaps.

## Single-source warning (verbatim, preserve)
> "What follows leans almost entirely on the **Google SRE Book (2016)**. That is one viewpoint — large-scale operations at a hyperscaler — applied to a personal R&D lab. Read the relevance notes with that mismatch in mind."

Every quoted passage below is from Google SRE Book 2016. The mismatch with personal-R&D-lab context is real and orchestrator should weight accordingly.

## Direct facts

1. **[SRE Book 2016, §7 "Resolving Inconsistencies Idempotently"]** "Requiring idempotent fixes meant teams could run their 'fix script' every 15 minutes without fearing damage to the cluster's configuration." — argues for idempotency as the design property a migration script must have. (confidence: direct)

2. **[SRE Book 2016, §7, cautionary half — preserve verbatim for Option A critique]** "Looking back, this approach was deeply flawed; the latency between the test, the fix, and then a second test introduced flaky tests that sometimes worked and sometimes failed. Not all fixes were naturally idempotent, so a flaky test that was followed by a fix might render the system in an inconsistent state." — Google's own retrospective: pretending a fix is idempotent when it isn't is *worse* than admitting non-idempotency and adding a coordination step. **Direct hit against choice 5 Option A ("eventual consistency").** (confidence: direct)

3. **[SRE Book 2016, §8 / Ch.7 "Release Simplicity" — preserve verbatim, direct hit on choice 4 bundling]** "Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously... If the release is performed in smaller batches, we can move faster with more confidence because each code change can be understood in isolation in the larger system." — **Direct hit against choice 4 (bundling unrelated bug-fix into shape migration).** (confidence: direct)

4. **[SRE Book 2016, Simplicity chapter — preserve verbatim, "grab bag" anti-pattern named for combined-script]** "As a system grows more complex, the separation of responsibility between APIs and between binaries becomes increasingly important. This is a direct analogy to object-oriented class design: just as it is understood that it is poor practice to write a 'grab bag' class that contains unrelated functions, it is also poor practice to create and put into production a 'util' or 'misc' binary. A well-designed distributed system consists of collaborators, each of which has a clear and well-scoped purpose." — A migration script that does (a) move files, (b) rewrite an index, and (c) fix a normalize bug is a grab-bag; the anti-pattern is named here. (confidence: direct)

5. **[SRE Book 2016, Simplicity chapter, "A Simple Conclusion"]** "Software simplicity is a prerequisite to reliability... Every time we say 'no' to a feature, we are not restricting innovation; we are keeping the environment uncluttered of distractions." — Cuts both ways: against AST-parser over-tooling for ~30 files, also against a sed pipeline that grows new responsibilities. (confidence: direct)

6. **[SRE Book 2016, §7 "The Inclination to Specialize"]** "Automation code, like unit test code, dies when the maintaining team isn't obsessive about keeping the code in sync with the codebase it covers... The most functional tools are usually written by those who use them." — A one-shot personal-lab migration runs once; cuts against building long-lived automation harness. (confidence: direct)

7. **[SRE Book 2016, §7, leaky-abstraction passage]** "We often assume that pushing a new binary to a cluster is atomic... However, real-world behavior is more complicated... leaving the system in an inconsistent state." — Atomicity assumptions usually leak; tension with both "single batch commit" and "per-entry commits if not independently meaningful." (confidence: direct)

8. **[SRE Book 2016, §8]** "We have embraced the philosophy that frequent releases result in fewer changes between versions." — Reframes choice 3 from style preference to "what is the smallest commit that leaves the repo in a valid state?" (confidence: direct)

9. **[Anthropic, *Building Effective Agents*, 2024]** "The most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns." — Off-domain (LLM agents); soft vote against AST-parser solution. (confidence: direct, off-domain)

## Inferred claims

1. **[canon-librarian]** Whichever language/tool you pick for the migration, idempotency is the load-bearing correctness property — derived from fact 1. (confidence: inferred)
2. **[canon-librarian]** Per-entry commits are the *less* coupled choice only if each commit is independently meaningful; a half-done shape migration is not. Tension, not resolution. (confidence: inferred)
3. **[canon-librarian]** SRE material covers *adjacent* ground for git commit hygiene but the canonical commit-hygiene literature (Tim Pope, Torvalds) is absent from corpus. (confidence: inferred)

## Authority-framed claims (stubs — preserve verbatim)

1. **Fowler, *Refactoring* (2nd ed., 2018) — STUB.** Underlying claim: "Refactoring is by definition behavior-preserving; if you're changing behavior, that is not a refactoring." Quote present in output: **no**. Confidence: **unsupported (stub)**. **Direct hit on choice 4** — bundling a bug fix into a structural move means the operation is no longer a refactoring. Librarian explicitly refuses to paraphrase from memory.

2. **Fowler, *Refactoring* — STUB.** Underlying claim: "Make the change easy, then make the easy change." Quote present in output: **no**. Confidence: **unsupported (stub)**. **Direct hit on choice 5 Option C** (edit-the-writer-first). Librarian explicitly refuses to paraphrase from memory.

3. **Feathers, *Working Effectively with Legacy Code* (2004) — STUB.** Underlying claim: characterization tests before changing untested code. Quote present in output: **no**. Confidence: **unsupported (stub)**. Relevant to whether any safety net exists for the migration.

4. **Beck — STUB.** Small-step discipline (each step compiles, each step's tests pass). Quote present in output: **no**. Confidence: **unsupported (stub)**.

5. **Helland, *Life Beyond Distributed Transactions* (2007) — STUB, fetch-blocked (403 to bots on ACM Queue).** Underlying claim: eventual consistency is a coordination protocol with named guarantees, not a synonym for "we'll fix it later." Quote present in output: **no**. Confidence: **unsupported (stub)**. Would complicate choice 5 Option A if ingested. Librarian explicitly flags as known gap; do not substitute another author.

## Contradictions surfaced

- **Idempotency-supporting passage (fact 1) vs idempotency-cautionary passage (fact 2)** — same SRE retrospective: *requiring* idempotency enables safe re-runs; *assuming* idempotency where it doesn't hold causes inconsistency. Both halves apply to choice 5.
- **"Frequent small releases" (fact 8) vs "per-entry commits only meaningful if standalone" (inferred 2)** — SRE position pulls toward smaller batches but only when each unit is independently valid; tension unresolved for choice 3.
- **"Just write a script" (idempotency / release simplicity) vs "automation rots" (fact 6)** — for a one-shot personal-lab migration, the long-lived-automation lessons cut against building a maintained harness.
- **"Single clean batch commit" (atomicity preference) vs "atomicity assumptions leak" (fact 7)** — the natural preference is challenged but not replaced.

## Subagent's own verdict (verbatim)

> "Corpus coverage: **Partial.**"

> "The canonical sources for the most relevant topics — Fowler's *Refactoring*... Feathers' *Working Effectively with Legacy Code*... and Helland's *Life Beyond Distributed Transactions*... are **stubs in this corpus**. Their citations are recorded; their texts are not. I will not ventriloquize them."

## Gaps the subagent flagged (preserve all)

1. **Slug-as-folder-name + slug-as-filename (path repetition conventions).** No corpus material on Java package=path, Python `__init__.py`, Rust mod-file, Go package=directory, or "README.md inside the folder" alternative. Real industry debate, not represented.
2. **Git rename-detection mechanics.** Nothing on git's heuristic rename detection, threshold percentages, `git mv` vs `mv + git add -A` log differences.
3. **Strangler Fig / expand-and-contract / parallel-change patterns *by name*.** Fowler bliki and *Refactoring Databases* (Sadalage/Ambler) not in corpus.
4. **"Don't write a script for 30 files" folk wisdom.** No canonical source in corpus; librarian cannot return a citation.
5. **Bundling-changes-in-one-commit / commit-hygiene anti-pattern.** SRE "Release Simplicity" is adjacent; Tim Pope "A Note About Git Commit Messages," Torvalds on small commits not in corpus.

## Staleness flags
SRE Book (2016) — release simplicity / idempotency / automation-rots claims not topics where consensus has shifted; treat as current. Anthropic *Building Effective Agents* (2024) current. All stubs not ingested.

## Token budget
~1450 tokens.
