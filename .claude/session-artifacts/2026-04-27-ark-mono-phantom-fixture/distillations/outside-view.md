## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on the phantom-fixture decision (options a/b/c) for session `2026-04-27-ark-mono-phantom-fixture`. Subagent returned three reference classes, three estimated base rates, a position-relative-to-base-rate analysis, a dominant failure mode, and three verdicts.

## Confidence-affecting meta-fact
- **Canon-first failure self-reported.** The subagent stated it "could not enumerate `canon/corpus/` directly in this run" and that testing-discipline / golden-master canon entries were not retrievable by it. It noted the parallel canon-librarian did surface them (see [canon.md](.claude/session-artifacts/2026-04-27-ark-mono-phantom-fixture/canon.md)). The forecast leans on standard reference-class forecasting plus public literature instead. Orchestrator should treat the forecast's canon-grounding as **partial / by-proxy**, not direct.

## Direct facts
1. [outside-view] Subagent self-reported canon enumeration failure; relied on Kahneman/Lovallo 1993, Flyvbjerg, and public snapshot/golden-master literature instead. (confidence: direct)
2. [outside-view] Sources cited at end include: Characterization test (Wikipedia); Understand Legacy Code; DEV.to Jest snapshot post; Rust golden-master snapshots post; ACM TOSEM "Survey of Flaky Tests"; Slack Engineering "Handling Flaky Tests at Scale"; Atlassian "Taming Test Flakiness"; Shaped "Golden Tests in AI". (confidence: direct)
3. [outside-view] Subagent labeled all numeric base rates as "estimates, not measured." (confidence: direct — explicit label preserved)
4. [outside-view] Cited industry-reported flaky-test rate of "13–21% of passing-history test failures are flaky in mature CI" attributed to Microsoft Research / Atlassian Jira figures. (confidence: direct — quote present, but no inline citation linking the specific number to a specific paper)

## Estimated base rates (preserve "estimate" label)
1. [outside-view] Q1 — first-run pass rate of a never-executed test against drifted infrastructure: **estimated 15–30%**. Probability option (a) yields clean exemplar without revision: **~20% (estimate)**. Probability of a useful run after one minor fix: **~50–60% (estimate)**. Multi-step degradation math given: 12 steps × 95%/step ≈ 54%; 12 × 90% ≈ 28%. (confidence: inferred — estimates, explicitly labeled)
2. [outside-view] Q2 — load-bearing vs illustrative doc slugs in <6mo repos with mismatched word-order: **estimated 20–35% load-bearing**. Option (b) immediate regression risk: **~25% (estimate)**. (confidence: inferred — estimate)
3. [outside-view] Q3 — "ceremony without baseline" infra meaningfully exercised within 6 months: **estimated <30%**. (confidence: inferred — estimate)

## Inferred claims
1. [outside-view] Three reference classes apply, ranked by predictiveness: RC-A (declared-but-never-executed regression tests / golden fixtures in young repos, first run after structural rebuild) most predictive; RC-B (aspirational doc example identifiers); RC-C (empty/placeholder fixture infrastructure — "ceremony without baseline"). (confidence: inferred)
2. [outside-view] Features moving proposal **above** RC-A base rate: markdown spec not executable code (narrower failure modes); same agent stack authored and will execute (small intent gap); repo purpose is review discipline (higher prior for careful authorship). (confidence: inferred)
3. [outside-view] Features moving proposal **below** RC-A base rate: stack rebuild between authorship and run is the literature's drift event; doc-slug word-order mismatch is a canary that the spec was not proofread; 12-step orchestrated workflow has high spec/behavior drift surface; empty `exemplars/` dir is literal RC-C signature. (confidence: inferred)
4. [outside-view] Net position: "at or slightly below the RC-A base rate." Option (a) succeeding in one shot is a minority outcome. (confidence: inferred)
5. [outside-view] Dominant failure mode is NOT "test fails and reveals real defect." It is: first run fails on spec/agent mismatch that is neither defect nor test signal but authoring drift; without a prior green anchor, the fix-the-test vs fix-the-agents decision is unprincipled; exemplar slot stays empty another cycle. (confidence: inferred)
6. [outside-view] Secondary failure modes: snapshot tyranny (incidental output locked as canonical, future legitimate improvements reverted); doc-slug normalization premature (third rename round if run produces different output, e.g. different date prefix); ceremony-without-baseline persists if option (b) chosen. (confidence: inferred)
7. [outside-view] What would lift option (a) above base rate: pre-committing in writing before the run to (i) expected agent outputs per step, (ii) rule distinguishing wrong-spec from wrong-agent, (iii) max post-hoc spec edits before the attempt is declared a failed exemplar. (confidence: inferred)

## Authority-framed claims
1. "Snapshot/golden-master practitioners universally report that the first capture is the easy step but matching a prior spec on first run is rare when the system underneath has shifted." — underlying claim: first-run match against prior spec is rare after system drift. Quote present in output: no (no specific practitioner quoted). Confidence: **unsupported** (asserts consensus without quoting any source).
2. "Snapshot-testing literature treats this as a recognizable anti-pattern: golden-master discipline collapses if no golden is ever written." — underlying claim: empty-fixture infrastructure is a named anti-pattern. Quote present in output: no (literature gestured at, no passage quoted). Confidence: **unsupported**.
3. Implicit Kahneman/Lovallo 1993 + Flyvbjerg framing of reference-class forecasting — underlying claim: this method is the appropriate forecasting method here. Quote present in output: no. Confidence: **unsupported as cited** (methodologically standard, but no direct quote).
4. Microsoft Research / Atlassian Jira "13–21% flaky" number — underlying claim: mature-CI flaky rates are 13–21%. Quote present in output: no specific citation tying number to source. Confidence: **inferred → treat as unsupported pending verification**.

## Contradictions surfaced
- **Within Q2:** subagent says the slug mismatch itself is "strong evidence the slug is currently illustrative" (lowers regression risk) AND that in a discipline-focused repo "future readers may treat the slug as load-bearing even if no current reader has" (raises norm-setting risk). Carried through, not collapsed.
- **Above-vs-below base rate features:** the proposal has explicit features pulling both directions (markdown-not-code, same-stack authoring vs. rebuild drift, canary mismatch, 12-step surface, empty exemplars). Subagent resolved net to "at or slightly below" but the underlying tension is real.

## Subagent's own verdict (verbatim)
- Option (a) executed naively: **"Below base rate"**.
- Option (c) — split the work (fix slug to consistent placeholder now; file regression run as dated item with pre-committed acceptance criteria): **"Within tolerance"**.
- Option (b) as a permanent move: **"Below base rate"** (removes visible bug at cost of teaching that example slugs are illustrative; compounds RC-C entrenchment).

## Gaps the subagent missed
- No direct canon retrieval; orchestrator should cross-check against the canon-librarian distillation, not treat this forecast as canon-grounded.
- No quantification of cost-of-dirty-run vs. cost-of-deferral — verdicts are framed as base-rate position, not expected-value.
- No discussion of option (a)+(c) hybrid: run now AND pre-commit acceptance criteria. Subagent treats (c) as splitting work, not as a precondition for (a).
- "Stack rebuild" is asserted as a drift event but the magnitude / surface of the actual rebuild is not characterized — base rate may apply more or less depending.
- Specific Microsoft / Atlassian flaky-rate citation not pinned to a paper; orchestrator may want to verify before quoting downstream.

## Token budget
~950 tokens.
