## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon guidance on a folder-shape depth bug fix — narrow mechanical link-fix vs. wider convention migration. Librarian returned partial corpus coverage: Google SRE chapters 1, 5, 9, 15 yielded direct quotes; Fowler/Feathers/Beck/Nygard are stubs (no quotes available).

## Direct facts

1. [Beyer et al., SRE (2017), Ch. 5 "Eliminating Toil"] Toil is defined as work that is "manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows"; if the system is in the same state after the task, the task was probably toil. (confidence: direct)

2. [SRE (2017), Ch. 5, footnote 21] "The system needs to be simplified and rebuilt to either eliminate the underlying failure conditions or deal with these conditions automatically"; until that redesign ships, applying human judgment per incident "is definitely toil." (confidence: direct)

3. [SRE (2017), Ch. 9 "Simplicity" — Negative Lines of Code] "Every line of code changed or added to a project creates the potential for introducing new defects and bugs"; deletion of unneeded code is praised. (confidence: direct)

4. [SRE (2017), Ch. 9 — Release Simplicity] "Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously." (confidence: direct)

5. [SRE (2017), Ch. 9, citing Brooks "No Silver Bullet" 1986] Essential complexity is inherent to the problem; accidental complexity "can be resolved with engineering effort." (confidence: direct)

6. [SRE (2017), Ch. 9 — "I Won't Give Up My Code!"] "Code that is never executed, gated by a flag that is always disabled, is a metaphorical time bomb"; source control already enables reversal, so commented/dead code is distraction. (confidence: direct)

7. [SRE (2017), Ch. 1 — risk continuum] "We strive to make a service reliable enough, but no more reliable than it needs to be" — over-investment wastes opportunities including tech-debt cleanup. (confidence: direct)

8. [SRE (2017), Ch. 15 "Postmortem Culture"] Postmortems "should establish what happened in detail, find all root causes of the event, and assign actions to correct the problem or improve how it is addressed next time." (confidence: direct)

## Inferred claims

1. [canon-librarian] A purely mechanical link-fix-by-count is a textbook toil case; convention migration is the engineering substitute that makes recurrence impossible. (confidence: inferred — librarian's mapping of SRE Ch. 5 toil definition onto the link-fix scenario)

2. [canon-librarian] The Negative-Lines-of-Code argument supports a wider cleanup only if the migration shrinks the rule-set; a migration that adds tooling does not qualify. (confidence: inferred)

3. [canon-librarian] Bundling the link fix with a convention migration mixes a symptom fix with a speculative class change, defeating bisectability per Release Simplicity. (confidence: inferred)

4. [canon-librarian] The essential-vs-accidental distinction forces the question whether depth-fragile linking is essential (markdown) or accidental (chose absolute over relative); only accidental justifies wider migration. (confidence: inferred)

5. [canon-librarian] Postmortem framing suggests a third path: narrow fix now + separately-tracked structural action item (CI link check, path-discipline rule), not bundled into the symptom commit. (confidence: inferred)

6. [canon-librarian] The "I Won't Give Up My Code!" passage cuts against half-migration: if you migrate the convention, finish it; otherwise don't start. (confidence: inferred)

7. [canon-librarian] The risk-continuum passage warns the boy-scout impulse can itself be over-engineering if the failure class rarely fires. (confidence: inferred)

## Authority-framed claims

None. Librarian cited only Beyer et al. (SRE) and Brooks (via SRE's own citation). No "as X would say" framings; all author attributions are accompanied by direct quotes from the corpus passages or SRE's own ventriloquism of Brooks.

## Contradictions surfaced

- **Fix the class vs. keep the diff narrow.** Facts 1-3 (toil definition, redesign-vs-judgment, Negative LOC) push toward wider convention migration. Fact 4 (Release Simplicity) pushes toward narrow bisectable diff. Librarian preserved both poles rather than collapsing.
- **Boy-scout cleanup vs. opportunity cost.** Fact 3 (Negative LOC praises cleanup) vs. Fact 7 (risk continuum: even cleanup has cost; over-reliability/over-cleanup wastes opportunities).
- **Half-migration is forbidden vs. narrow-diff-now.** Fact 6 ("don't keep dead code, finish migrations") tension with Fact 4 (one change at a time) — together they imply: either commit fully to migration in its own change, or don't start; never half-do it inside a symptom fix.
- **Symptom fix vs. root cause.** Fact 8 (postmortem: assign actions to correct root cause) tension with Fact 4 (single change per release) — librarian resolves with the "third path" inference (track structural work separately).

## Subagent's own verdict (verbatim)

"**Partial.**" (corpus coverage)

## Gaps the subagent missed

The librarian itself flagged these gaps; passing through:
- Boy-scout rule explicit framing (Fowler/Beck/Martin) — stubs only.
- Broken-windows-in-code (Wilson/Kelling contagion analogue) — no corpus entry.
- Refactoring durability under future structural change — Feathers/Fowler stubs.
- Convention-migration recurrence prevention via tooling — no entry.
- Staleness: SRE 2016/2017; doc-tooling and link-checking practice has evolved.

Additional gap the orchestrator should note: librarian did not address the markdown-link-specific question (relative vs. absolute path conventions in docs repos) — entire retrieval is from a production-services SRE corpus mapped analogically onto a documentation-repo problem. The analogical mapping is the librarian's, not the corpus's.

## Token budget
~820 tokens.
