# canon-librarian raw return — 2026-04-27 upgrade-folder-shape-implementation

## Corpus coverage
Partial. The corpus has strong material on **idempotency**, **release simplicity / small-batch changes**, and **simplicity as a design constraint** (Google SRE Book, fully ingested). The canonical sources for the most relevant topics — Fowler's *Refactoring* (small-step discipline, "make the change easy, then make the easy change"), Feathers' *Working Effectively with Legacy Code* (seams, characterization tests for shape changes), and Helland's *Life Beyond Distributed Transactions* (eventual-consistency framing) — are **stubs in this corpus**. Their citations are recorded; their texts are not. I will not ventriloquize them.

The corpus contains **nothing** on: git rename detection mechanics, slug/path repetition conventions across language ecosystems (Java package=path, Rust mod, Go directory=package), parallel-change / expand-and-contract migration patterns by name, or the "bundle unrelated bug fix" anti-pattern as such. These are real industry positions, but they are not in *this* corpus.

## Single-source warning
What follows leans almost entirely on the **Google SRE Book (2016)**. That is one viewpoint — large-scale operations at a hyperscaler — applied to a personal R&D lab. Read the relevance notes with that mismatch in mind.

---

## Supporting passages

### 1. Idempotent fixes — the case *for* writing the migration as a script
Google SRE Team, *Site Reliability Engineering* (2016), §7 "The Evolution of Automation at Google" — "Resolving Inconsistencies Idempotently"

> "The unit test already knew which cluster we were examining and the specific test that was failing, so we paired each test with a fix. If each fix was written to be idempotent, and could assume that all dependencies were met, resolving the problem should have been easy—and safe—to resolve. Requiring idempotent fixes meant teams could run their 'fix script' every 15 minutes without fearing damage to the cluster's configuration."

Relevance: Argues for *idempotency* as the design property a migration script must have — relevant to choice 2 (single-script-with-sed vs Python-with-AST). The script's correctness property matters more than the choice of language; whichever you pick, it must be safe to re-run.

### 2. Same passage, the cautionary half — the case *against* taping fixes onto a flaky pipeline
Google SRE Team, *Site Reliability Engineering* (2016), §7 "Resolving Inconsistencies Idempotently"

> "Looking back, this approach was deeply flawed; the latency between the test, the fix, and then a second test introduced flaky tests that sometimes worked and sometimes failed. Not all fixes were naturally idempotent, so a flaky test that was followed by a fix might render the system in an inconsistent state."

Relevance: Directly relevant to choice 5 (eventual consistency vs operator pause vs edit-the-writer-first). Google's own retrospective: pretending a fix is idempotent when it isn't is *worse* than admitting non-idempotency and adding a coordination step. Pushes against Option A.

### 3. Release simplicity — small batches over bundled changes
Google SRE Team, *Site Reliability Engineering* (2016), §8 "Release Engineering" / Ch.7 "The Evolution of Automation" — "Release Simplicity"

> "Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously. If we release 100 unrelated changes to a system at the same time and performance gets worse, understanding which changes impacted performance, and how they did so, will take considerable effort or additional instrumentation. If the release is performed in smaller batches, we can move faster with more confidence because each code change can be understood in isolation in the larger system."

Relevance: Direct hit on choice 4 (bundling unrelated bug-fix into the migration edit). The SRE position is: don't bundle. The reasoning ("understand the impact of a single change") applies to a 30-file lab as well as to production.

### 4. Modularity and "grab-bag" anti-pattern — applies to scripts, not just binaries
Google SRE Team, *Site Reliability Engineering* (2016), Simplicity chapter

> "As a system grows more complex, the separation of responsibility between APIs and between binaries becomes increasingly important. This is a direct analogy to object-oriented class design: just as it is understood that it is poor practice to write a 'grab bag' class that contains unrelated functions, it is also poor practice to create and put into production a 'util' or 'misc' binary. A well-designed distributed system consists of collaborators, each of which has a clear and well-scoped purpose."

Relevance: Soft argument against choice 2's "single-script-with-sed-on-index" if the script accumulates unrelated responsibilities. A migration script that does (a) move files, (b) rewrite an index, and (c) fix a normalize bug is a grab-bag. The anti-pattern is named here.

### 5. Simplicity as the prerequisite — argues *against* over-engineering for 30 files
Google SRE Team, *Site Reliability Engineering* (2016), Simplicity chapter — "A Simple Conclusion"

> "This chapter has repeated one theme over and over: software simplicity is a prerequisite to reliability. We are not being lazy when we consider how we might simplify each step of a given task. Instead, we are clarifying what it is we actually want to accomplish and how we might most easily do so. Every time we say 'no' to a feature, we are not restricting innovation; we are keeping the environment uncluttered of distractions so that focus remains squarely on innovation, and real engineering can proceed."

Relevance: Cuts both ways. Argues against a Python-with-AST-parser solution for ~30 files (over-tooled). Also argues against a sprawling sed pipeline that grows new responsibilities (also a complexity smell).

### 6. Composable patterns over frameworks
Anthropic, *Building Effective Agents* (2024)

> "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed... the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

Relevance: Off-domain (LLM agents, not migration scripts), but the underlying claim — simplest composable pattern over heavy framework — is a soft vote against "Python with proper AST/parser" for a 30-file move. Use only if existing material does not suffice.

---

## Contradicting or complicating passages

### A. Same SRE retrospective complicates the "just write a script" reflex
Google SRE Team, *Site Reliability Engineering* (2016), §7 — "The Inclination to Specialize"

> "Automation code, like unit test code, dies when the maintaining team isn't obsessive about keeping the code in sync with the codebase it covers. The world changes around the code... By relieving teams who ran services of the responsibility to maintain and run their automation code, we created ugly organizational incentives... The most functional tools are usually written by those who use them."

Why this complicates the framing: A one-shot migration script in a personal lab will run *once*. The SRE retrospective is about *long-lived* automation. The lesson cuts in both directions: (1) don't build a long-lived automation harness for a one-shot move (complicates choice 2 toward "just do it by hand or with a small script"); but also (2) the script you write *will* rot if you keep it around — argues against script-per-step / Makefile if those files will linger unmaintained.

### B. Atomicity assumptions are usually wrong
Google SRE Team, *Site Reliability Engineering* (2016), §7

> "The trade-off here is classic: higher-level abstractions are easier to manage and reason about, but when you encounter a 'leaky abstraction,' you fail systemically, repeatedly, and potentially inconsistently. For example, we often assume that pushing a new binary to a cluster is atomic; the cluster will either end up with the old version, or the new version. However, real-world behavior is more complicated: that cluster's network can fail halfway through; machines can fail; communication to the cluster management layer can fail, leaving the system in an inconsistent state."

Why this complicates the framing: The implicit thesis behind "single-batch commit" or "Option A: eventual consistency" is that *some step* will be atomic enough. SRE's position: atomicity assumptions almost always leak. A per-entry git commit at least gives you a per-entry rollback boundary; a single batch commit gives you one rollback for everything. Counter to the natural preference for "one clean commit," the per-entry commits are arguably the *less* coupled choice — but only if each commit is independently meaningful, which a half-done shape migration is not. Tension, not resolution.

### C. Frequent small changes over big batches
Google SRE Team, *Site Reliability Engineering* (2016), §8 Release Engineering

> "We have embraced the philosophy that frequent releases result in fewer changes between versions. This approach makes testing and troubleshooting easier."

Why this complicates the framing: Slight tension with the "single-batch commit" instinct in choice 3. But also tension with "per-entry commits" if each entry-commit isn't independently sensible. The SRE frame asks: can each commit *stand alone* as a valid state? If yes, per-entry. If no (i.e., between commits the index points at moved files), then the unit-of-change is the whole migration and a single batch is more honest. This reframes choice 3 from "style preference" to "what is the smallest commit that leaves the repo in a valid state?"

### D. (Stub — counter-position not retrievable from corpus) Helland on eventual consistency
Pat Helland, *Life Beyond Distributed Transactions: an Apostate's Opinion* (2007), CIDR

> [stub entry; full text not ingested — PDF at https://ics.uci.edu/~cs223/papers/cidr07p15.pdf, ACM Queue updated version at https://queue.acm.org/detail.cfm?id=3025012 returns 403 to bots]

Why this would complicate the framing if ingested: Helland's paper is the canonical statement that eventual consistency is a *coordination protocol with named guarantees*, not a synonym for "we'll fix it later." Choice 5 Option A as described ("eventual consistency") is the kind of casual usage Helland's title ("an Apostate's Opinion") was explicitly pushing back against. The librarian flags this as a known gap; do not substitute another author's treatment.

### E. (Stub — counter-position not retrievable from corpus) Fowler / Feathers on shape-vs-behavior changes
Martin Fowler, *Refactoring* (2nd ed., 2018) — stub
Michael Feathers, *Working Effectively with Legacy Code* (2004) — stub

Both books contain the canonical positions on:
- "Refactoring is by definition behavior-preserving; if you're changing behavior, that is not a refactoring" (Fowler) — directly relevant to choice 4 (bundling a bug fix into a structural move).
- Small-step discipline: each step compiles, each step's tests pass (Fowler, Beck).
- "Make the change easy, then make the easy change" (Fowler) — relevant to choice 5 Option C (edit-the-writer-first).
- Characterization tests before changing untested code (Feathers) — relevant to whether you have any safety net at all for the migration.

These are stub entries. I will not paraphrase from memory. The corpus gap is real and worth flagging to the user as a place where the strongest counter-arguments to several of their design choices live.

---

## Gaps the corpus does not cover

1. **Slug-as-folder-name + slug-as-filename (path repetition).** No corpus material on naming-convention ecosystems (Java package=path, Python `__init__.py`, Rust mod-file, Go package=directory) or the "README.md inside the folder" alternative. This is a real debate in industry but is not represented here.
2. **Git rename-detection mechanics.** Nothing in the corpus on git's heuristic rename detection, threshold percentages, or how `git mv` vs `mv + git add -A` differ in the log.
3. **Strangler Fig / expand-and-contract / parallel-change patterns *by name*.** Fowler has named these elsewhere (bliki posts, *Refactoring Databases* with Sadalage, Pramod). None of those entries exist in this corpus.
4. **"Don't write a script for 30 files" as a stated position.** The "do it by hand" counter-argument has no canonical source in this corpus. It is folk wisdom; the librarian cannot return a citation.
5. **Bundling-changes-in-one-commit anti-pattern.** Adjacent material exists in SRE "Release Simplicity" but the git-commit-hygiene literature (e.g. Tim Pope's "A Note About Git Commit Messages," Linus Torvalds on small commits) is not in the corpus.

---

## Staleness flags

- Google SRE Book is 2016. The "release simplicity," "idempotency," and "automation rots" claims are not topics where consensus has shifted; treat as current.
- Anthropic *Building Effective Agents* (2024) is current.
- All stub entries (Fowler 2018, Feathers 2004, Beck 2002, Helland 2007) are not ingested — citations only.

