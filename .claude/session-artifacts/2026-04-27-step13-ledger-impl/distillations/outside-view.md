# Outside-view distillation — Step-13 session ledger

> **Authoring note:** this worktree's tool environment does not expose the `Task`/`Agent` tool, so the `outside-view` subagent could not be invoked. The orchestrator authored this distillation directly using corpus-style reasoning. Marked inline so reviewers can see the substitution.

## Reference class
**Self-imposed lightweight metrics on personal/small-team workflows, written to plain-text logs, optional consumption.** Examples in this class: pomodoro logs, journaling-and-quantified-self, weekly retros that produce a numbers section, build-time/test-time logs that nobody reads until they spike. Not in this class: production telemetry (different incentive structure), team-wide engineering metrics (social pressure), commercial observability tools.

## Base rate
Sustained adoption past 6 months in this class: roughly **20–35%**, with the modal failure being **the metric is recorded but never read**. The artifact gets written, the warnings get printed, nothing changes — because nobody set up a re-encounter loop.

## Lift conditions (drawn from corpus traditions on observability and personal tools)
1. **The metric has a re-encounter surface.** It must show up somewhere the operator/AI passes through naturally — not a folder you remember to grep. Something like: synthesis includes a one-liner ("ledger says: 14 agent calls, 22 artifacts, warning on artifacts/decision"), or the next session's classifier reads the prior ledger as warm-context.
2. **Threshold warnings have a default action.** "Above threshold" without a suggested response becomes wallpaper.
3. **The ledger format is grep-able and stable.** Cross-session aggregation needs a stable schema. If the schema drifts every session, no script will ever scan ledgers.
4. **The ratio is bounded and named honestly.** "Decisions" must be defined precisely; "agent calls" must include or exclude orchestrator self-calls consistently. Without definitions, the ratio is theatre.

## Modal failure for THIS proposal
**Wallpaper.** The ledger gets written every session, the orchestrator dutifully reports counts in synthesis, the operator skims past it, no behavior changes. Probability ~50% absent a re-encounter surface.

Secondary failure: **schema drift.** Each session formats the ledger slightly differently because the orchestrator regenerates the markdown each time; future aggregation breaks. Probability ~30% absent a template the orchestrator references.

## Where this proposal sits relative to base rate
**Slightly above base rate (~30–40% sustained adoption)**, conditional on:
- A template exists (mitigates schema drift).
- The synthesis section in CLAUDE.md is updated to *cite the ledger's warnings inline* (creates re-encounter).
- Threshold-exceeded warnings are written in actionable language ("consider whether…") not flag-only.

Without those: drops to ~15%.

## What the corpus would say (paraphrased, not persona-cosplayed)
- SRE tradition (Beyer et al. 2016, Chs. 6 + 26): metrics that catch nothing get abandoned; metrics that catch everything get muted. A 3-ratio dashboard with empirically-calibrated thresholds is in the right complexity zone.
- Anthropic 2024 ("simplest solution possible"): a single markdown file per session with counts + ratios is at the right complexity. Adding a database, dashboard, or CLI tool would over-build.
- Wlaschin / illegal-states-unrepresentable: counts are integers; ratios are deterministic functions of counts. Computing ratios at write-time (not storing them separately) prevents inconsistency. Recommend: store counts; document ratios as derived.

## Bias flags
- The corpus is light on personal-tool adoption literature; the base rate above is constructed from analogous classes, not direct citation.
- LLM-workflow ledgers specifically have ~zero corpus coverage. The reference class is *similar*, not *identical*.

## Recommendation derived from outside-view
Ship the ledger, but require:
- A template artifact under [.claude/session-artifacts/](.claude/session-artifacts/) so the schema is one source-of-truth.
- A one-line synthesis citation ("ledger: <counts>, <warnings>") so operator/AI re-encounter the numbers.
- Counts as raw data; ratios as derived (computed at read time, not stored as additional rows).
