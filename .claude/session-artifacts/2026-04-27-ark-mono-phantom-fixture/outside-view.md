# Outside-View Forecast — phantom-fixture decision

**Canon-first note:** outside-view agent reported it could not enumerate `canon/corpus/` directly in this run. Declared gap: testing-discipline / golden-master entries were not retrievable by this agent (the canon-librarian, run in parallel, did surface them — see [canon.md](.claude/session-artifacts/2026-04-27-ark-mono-phantom-fixture/canon.md)). The forecast leans on standard reference-class forecasting (Kahneman/Lovallo 1993; Flyvbjerg) plus public literature on snapshot/golden-master testing and flaky-test rates.

---

## 1. Reference class

This decision sits at the intersection of three reference classes. Most predictive listed first.

- **RC-A (most predictive): "Declared but never-executed regression tests / golden fixtures in young repos, first run after a structural rebuild."** Specifically: a test artifact authored against an *evolving* agent set, where the agents have changed since authorship, with zero baseline ever captured. Closest published analogues: Feathers-style characterization tests authored against legacy code on day one; snapshot suites established immediately after a framework swap; CI smoke tests added during onboarding but never executed against the production graph.
- **RC-B: "Documentation example identifiers (slugs, IDs, sample names) in early-stage repos."** Sub-class: identifiers that were authored aspirationally rather than as transcripts of real runs.
- **RC-C: "Empty-fixture / placeholder-fixture infrastructure"** — repos that ship the *shape* of a regression suite (directories, runners, README) without a single concrete recorded artifact. Snapshot-testing literature treats this as a recognizable anti-pattern: golden-master discipline collapses if no golden is ever written.

The proposal is most usefully forecast against RC-A. RC-B and RC-C frame the (b) and (c) options.

## 2. Base rates

Numbers below are estimates, not measured. Flagged as such.

- **Q1 — first-run pass rate of a never-executed test against drifted infrastructure.** Estimated **15–30%**. Sources of the pessimism: (i) industry-reported flaky-test rates of 13–21% of *passing-history* test failures are flaky in mature CI (Microsoft Research, Atlassian Jira numbers); a never-run test has *no* passing history and accumulates every drift since authorship. (ii) Snapshot/golden-master practitioners universally report that the *first* capture is the easy step but matching a *prior* spec on first run is rare when the system underneath has shifted. (iii) Multi-step agent workflows (12 steps here) have a per-step degradation; if each step has 95% fidelity to the spec, end-to-end is ~54%; at 90%, ~28%. Estimate: probability that option (a) yields a clean exemplar without at least one revision is **~20%**. Probability it yields a *useful* run (passes after one minor fix) is **~50–60%**.
- **Q2 — load-bearing vs. illustrative doc slugs.** Estimated **20–35% load-bearing** in repos under ~6 months old where the slug is *cited in two places with mismatched word order*. The mismatch itself is strong evidence the slug has not been clicked by a human reader since authorship — load-bearing references get corrected fast because they break for the reader. So the evidence is mostly that the slug is currently illustrative. Counter-pressure: in a repo whose entire purpose is process discipline, *future* readers may treat the slug as load-bearing even if no current reader has. Net: substituting a real slug (option b) carries **low immediate regression risk (~25%)** but moderate **norm-setting risk** — it teaches the repo that example slugs can be fabricated.
- **Q3 — failure mode for "regression infra without a single populated fixture."** This is a named pattern in the snapshot-testing literature: **"ceremony without baseline."** Base rate of such infrastructure being meaningfully exercised within 6 months of authorship: estimated **<30%**. The dominant outcome: the runner bit-rots faster than it accumulates fixtures, and the first real run (when finally attempted) finds the runner itself broken before any test logic executes. Secondary outcome: a fixture is captured under duress, never reviewed, and becomes the de-facto spec — locking in whatever state the system happened to be in that day, including bugs ("snapshot tyranny").

## 3. Position relative to base rate

Features that move this proposal **above** the RC-A base rate:
- The test is a markdown spec, not executable code — failure modes are narrower (no runner to bit-rot, only agent-output drift).
- The author is the same agent stack that will execute it; semantic gap between authoring intent and execution intent is small.
- The repo's stated purpose is review discipline, raising the prior that the test was authored carefully.

Features that move it **below** the RC-A base rate:
- Stack rebuild between authorship and first run is exactly the drift event the literature warns about.
- The doc-slug word-order bug is a *canary*: if two top-level docs disagree on the slug, the test spec is unlikely to have been proofread against the current agent set either.
- Twelve-step orchestrated workflow with multiple subagent boundaries — high surface area for spec/behavior drift.
- "Exemplars/ is empty" is the literal RC-C signature.

Net: this proposal sits **at or slightly below** the RC-A base rate. Option (a) succeeding in one shot is a minority outcome.

## 4. Typical failure mode

The dominant failure mode for this reference class is **not** "the test fails and reveals a real defect." It is:

> **The first run fails on a spec/agent mismatch (a step name, an artifact filename, an assertion phrasing) that is neither a real defect nor a real test signal — it's an authoring drift. The team then has to decide whether to "fix the test" or "fix the agents." Without a prior green run as anchor, this decision is unprincipled. The test becomes a punch-list item that absorbs hours, and the exemplar slot stays empty for another cycle.**

Secondary failure modes:
- **Snapshot tyranny** (if the run is forced green): the first capture locks in incidental output as canonical. Future legitimate agent improvements break the snapshot and get reverted because "the regression test caught it."
- **Doc-slug normalization premature**: harmonizing docs to a slug whose run has not yet succeeded means a *third* renaming round when the run produces something different (e.g., a different date prefix because it runs tomorrow, not today).
- **Ceremony without baseline persists**: option (b) — substituting an existing real session — neutralizes the visible bug but cements the pattern that the regression infra is decorative.

## 5. Outside-view verdict

**Below base rate** for option (a) executed naively (run now, harmonize docs to whatever the run produces, expect a clean exemplar). The base rate says first-run-clean is a minority outcome and the cost of a dirty run is doc-churn plus a snapshot-tyranny risk.

**Within tolerance** for option (c) — split the work. Fix the doc word-order bug to *any* consistent placeholder slug now (cheap, reversible, removes the canary), and file the regression run as its own dated item with explicit acceptance criteria *before* it runs (what counts as pass; what counts as authoring-drift-not-defect; whether the first capture is treated as canonical or as a draft). This matches the snapshot-testing literature's discipline requirement: decide *what a passing run means* before you run it.

**Below base rate** for option (b) as a permanent move — it removes the visible bug at the cost of teaching the repo that example slugs are illustrative, which compounds with the empty `exemplars/` dir to entrench RC-C.

What would lift option (a) above the base rate: pre-committing, *in writing, before the run*, to (i) a list of expected agent outputs at each of the 12 steps, (ii) a rule for distinguishing "test spec is wrong" from "agent behavior is wrong," and (iii) a maximum number of post-hoc spec edits permitted before the run is declared a failed exemplar attempt rather than a successful one.

---

Sources cited by agent:
- Characterization test — Wikipedia
- Regression vs. Characterization vs. Approval Tests — Understand Legacy Code
- Don't Break UI with Jest Snapshot Testing — DEV
- Snapshots: Automating Golden Master Regression Tests in Rust
- A Survey of Flaky Tests — ACM TOSEM
- Handling Flaky Tests at Scale — Slack Engineering
- Taming Test Flakiness — Atlassian Engineering
- Golden Tests in AI — Shaped
