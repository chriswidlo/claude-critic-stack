## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on a folder-shape depth-bug fix, comparing Option A (convention migration to repo-root-relative links across ~30 edits in 2 files, bundled with punch-list item 3) vs. Option B (mechanical "add one ../" fix, ~17 edits). Subagent returned a verdict of "within tolerance, leaning favorable" for Option A, conditional on two safeguards.

## Direct facts
1. [outside-view §0] Subagent declared it could not Grep/Bash and therefore did not directly scan canon/corpus/; cites Fowler/Beck and Hunt/Thomas from memory only. (confidence: direct)
2. [outside-view §0] No WebSearch was performed. (confidence: direct)
3. [outside-view §2] Repo-root-relative markdown link conventions are well-supported by GitHub, Obsidian, and most static site generators. (confidence: direct — asserted as tooling fact)
4. [outside-view §5] Verdict: "Within tolerance, leaning favorable, for Option A" — provided (a) a mechanical verification step (link checker or grep for residual `../`) and (b) a one-line convention note committed alongside. (confidence: direct)
5. [outside-view §5] If either condition is dropped, forecast degrades to "at base rate" and Option B becomes competitive on effort-adjusted grounds. (confidence: direct)

## Inferred claims
1. [outside-view §1] The dominant reference class is "opportunistic scope expansion during a small mechanical fix in a docs/notes repo" (Boy Scout / refactor-while-you're-in-there pattern), not "markdown link maintenance." (confidence: inferred)
2. [outside-view §2] Bounded convention migrations on <5 files / <50 edits complete cleanly ~80–90% of the time when done in one sitting. (confidence: inferred — explicitly flagged as qualitative estimate, not measured)
3. [outside-view §2] Mechanical "add one ../" fixes succeed ~95% but recur ~60–70% on the next structural change. (confidence: inferred — flagged estimate)
4. [outside-view §2] Opportunistic scope expansion across a conceptual boundary completes ~70–80% vs. ~85–90% for narrow scope; bundling item 2 with item 3 is "coherent" because both are link-form issues. (confidence: inferred — flagged estimate)
5. [outside-view §2] Hand-edited 30-link batches have a typical ~1–2 broken-link typo rate. (confidence: inferred — flagged estimate)
6. [outside-view §3] Option A is "above base rate" because scope is small, bundled item is same edit kind, convention already endorsed by repo CLAUDE.md path-discipline rule, and latent-bug-class elimination is real (folder reshape recurs). (confidence: inferred)
7. [outside-view §4] Typical failure modes: Option A — partial migration leaving mixed state; Option B — silent recurrence on next reshape; bundling — boundary blur from item 3 stalling the whole bundle. (confidence: inferred)
8. [outside-view §0] The canon "almost certainly" contains Fowler/Beck on refactoring scope discipline and Hunt/Thomas on DRY and "broken windows." (confidence: inferred — speculation about corpus contents)

## Authority-framed claims
1. "Convention migrations historically trade one bug class for another (Hunt/Thomas warning)." — underlying claim: convention migrations swap one class of bug for another. Quote present in output: no. Confidence: unsupported (cited from memory, not from corpus, no quote provided).
2. Implicit framing of Fowler's *Refactoring* and Kahneman & Lovallo (1993) as supporting sources at end of return. Underlying claim: these works back the scope-discipline reasoning. Quote present in output: no. Confidence: unsupported (subagent self-flagged as "canon-adjacent, not canon-verified").

## Contradictions surfaced
None within the subagent's own output. Subagent flagged that a canon grep could surface contradicting passages and would shift the forecast — but did not retrieve any.

## Subagent's own verdict (verbatim)
"Within tolerance, leaning favorable, for Option A — provided two conditions: 1. A mechanical verification step after the edit (markdown link checker or grep for residual ../ patterns). 2. A one-line convention note committed alongside the change."

Confidence: moderate.

## Gaps the subagent missed
- No actual canon retrieval performed; the canon-librarian distillation must carry the corpus-grounded view. Orchestrator should not treat the Fowler/Hunt/Thomas/Kahneman citations here as canon evidence.
- Did not quantify or assess the actual size of punch-list item 3 (called out only as a forecast-shifting unknown).
- Did not check whether the repo has a link-checker in CI (called out as a forecast-shifting unknown but not investigated).
- Did not address whether a third folder-shape migration is anticipated (i.e., the recurrence-elimination value of Option A is asserted but not grounded).
- Did not examine whether mixing this fix with punch-list item 3 violates a commit-atomicity norm in the repo.
- Did not produce a numeric base rate for "markdown convention migrations in personal/notes repos" — only qualitative bands.

## Token budget
~750 tokens.
