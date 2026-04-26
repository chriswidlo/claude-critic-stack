# Outside-View — format-only state-transition gate (raw return)

**Canon-first note.** Canon has stubs for Kahneman/Lovallo (1993), Flyvbjerg (2006), Tetlock (2015) on outside-view methodology, but corpus folder is gitignored — methodology texts not grep-able on this machine. Canon does **not** cover the specific reference class (personal-tooling validator adoption, pre-commit hook abandonment, single-operator content-convention enforcement). Web results below are flagged as gap-fills, not promoted to canon.

## 1. Reference class

Three classes in order of predictive value:

- **(Most predictive) Self-imposed personal-workflow validators on a small markdown/notes corpus, single operator, no external accountability.** Custom Zettelkasten linters, Obsidian/Logseq schema-enforcement scripts, personal git pre-commit hooks for journal/notes repos, hand-rolled state-machine checks. Population ~22 entries, 8-state lifecycle, no team to satisfy.
- **(Adjacent) Pre-commit/format hooks on small solo repos** — conventional-commits enforcers, frontmatter validators, remark-lint. Same operator-as-enforcer dynamic; bypass is one `--no-verify` away.
- **(Adjacent, weaker fit) Workflow-state validators in low-code/CMS systems (Sanity, Contentful, Notion automations).** These have multi-user pressure and platform lock-in punishing bypass; selection pressure absent here, so this class over-predicts adoption.

Team-CI reference class explicitly excluded per user constraint.

## 2. Base rate

No clean published base rate. Estimates, flagged:

- **Forte Labs PKM survey (web, not canon)**: ~68% of PKM-tool adopters abandon within six months. *Tool* adoption, not *self-imposed schema* adoption — latter is harder.
- **Pre-commit hook ecosystem (web)**: well-documented `--no-verify` escape when hooks add friction >1–2s or produce false positives; on solo repos, abandonment higher because no peer review catches bypass.
- **Custom Zettelkasten/Obsidian plugins**: large fraction built and used 2–8 weeks, then absorbed into muscle memory (validator removed) or silently bypassed.

**Estimated base rate of sustained adoption past 6 months: 15–30%.** Soft estimate. Modal outcome (~50–60%): "built, used briefly, then bypassed or removed." Meaningful minority (~15–25%): "built but never integrated into actual edit loop."

Sub-question: of those adopted, how many drift from format-only into quality judgment? High — scope creep into quality is typical drift and itself a leading abandonment indicator.

## 3. Position relative to the reference class

**Favorable (above base rate):**
- **Format-only, not quality-evaluating.** Single biggest favorable factor. Quality gates on personal R&D notes are nearly always abandoned. Format-only gates have much better track record because they answer a yes/no the operator agrees with in advance.
- **Small bounded corpus (~22 entries).** Validator's blast radius small; can be exhaustively tested against existing corpus on day one.
- **Discrete named state set (8 states).** Easier to specify than free-form linting.
- **Operator authored the lifecycle.** Self-designed schemas more likely to survive than imposed ones.

**Unfavorable (below base rate):**
- **Single operator, no external enforcement.** When validator says no and operator wants yes, operator wins.
- **8 states is on the high end for personal lifecycle.** Most surviving personal workflows collapse to 3–5 states within a year. 8-state spec is itself a candidate for the typical failure mode.
- **"Required body elements per state" is a moving spec.** Validator encodes today's idea of what a "spiked" or "prepared" entry contains. R&D notes evolve in form; validator will lag operator's actual template, producing false positives.
- **No deployment surface that forces invocation.** Unless gate runs on every save (file watcher, plugin, pre-commit), it runs only when operator remembers — i.e. when operator already knows entry is valid.

Net: **mildly favorable on design, mildly unfavorable on enforcement surface.** Roughly at base rate, perhaps slightly above if integration question is solved.

## 4. Typical failure mode (rough order of likelihood)

1. **Lifecycle spec drift.** Operator changes how a "spiked" entry is written but doesn't update validator. Validator starts producing false positives. After 2–3 false positives, operator stops trusting it. Validator becomes vestigial. **Modal outcome.**
2. **State collapse.** Within 2–3 months operator notices 3 of 8 states never used (e.g. `prepared` and `accepted` collapse; `value-proved` and `completed` collapse). Validator now enforces lifecycle operator no longer believes in.
3. **Bypass-by-default.** Validator only runs on explicit invocation. Operator drifts to editing without invoking. After a month, half the corpus inconsistent.
4. **Scope creep into quality judgment.** Operator (or LLM-agent variant) starts adding "is this idea worth promoting?" checks. Gate becomes adversarial. Abandoned within weeks.
5. **One-off "first run" success then disuse.** Built, run once, fixes applied, never run again because corpus is "clean." Technically a win — but ongoing-check value never realized.

Non-failure path: validator runs automatically on every save or commit, takes <500ms, false-positive rate <5%, and the lifecycle spec is revised in lockstep with the validator (i.e., validator *is* the lifecycle spec).

## 5. Outside-view verdict

**Within tolerance, conditional on integration surface.**

At or slightly above base rate *if and only if* the enforcement-surface problem is solved before building features. Decide **before writing the validator** how it gets invoked on every edit (file watcher, editor plugin, git pre-commit on the notes repo, or agent-mediated edits that always call it). If invocation is "I'll run it manually" or "the agent will probably remember," forecast drops to bottom of range (~15%) — modal outcome is failure mode #3.

**Lift conditions:**
- Pin validator to a specific invocation surface that does not depend on operator memory.
- Co-locate lifecycle spec and validator in one file, so spec drift forces validator update.
- Pre-commit to a state-collapse review at the 6-week mark; treat collapse as expected, not as failure.

## Sources (web gap-fill, not canon)
- Forte Labs / PKM abandonment: https://glasp.co/articles/personal-knowledge-management
- Pre-commit hooks fundamentally broken (jyn.dev): https://jyn.dev/pre-commit-hooks-are-fundamentally-broken/
- Pre-commit debate (BigGo): https://finance.biggo.com/news/202510210735_Git-Pre-Commit-Hook-Debate
- dev.to: https://dev.to/afl_ext/are-pre-commit-git-hooks-a-good-idea-i-dont-think-so-38j6
- Thoughtworks: https://www.thoughtworks.com/insights/blog/pre-commit-don-t-git-hooked

## Canon stubs consulted (methodology only)
- Kahneman & Lovallo (1993), *Timid Choices and Bold Forecasts*
- Flyvbjerg (2006), *From Nobel Prize to Project Management*
- Tetlock (2015), *Superforecasting*
