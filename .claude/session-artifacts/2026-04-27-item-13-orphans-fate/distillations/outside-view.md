## Source agent
outside-view (item 13: orphans fate)

## Invocation summary
Orchestrator asked for a reference-class forecast on whether to (a) institute a new lifecycle primitive for orphan artifacts vs. (b) handle ad-hoc, given N=4 orphans in a solo-maintainer meta-repo. Subagent returned a verdict of "below base rate for option (a); at base rate for option (b)."

## Canon-first gap (subagent-declared)
Subagent had only Read/Web tools — no Grep/Glob to enumerate `canon/corpus/`. All canonical-work citations below are **gap-declared**; orchestrator should cross-check against canon-librarian's return for this session.

## Direct facts
1. [outside-view] Subagent's chosen reference class: solo-maintainer or 1–3 person research/tooling repos, < 2 years old, performing a first or second janitorial sweep on documentation artifacts. (confidence: direct — explicit framing choice)
2. [outside-view] Subagent rejected the "enterprise documentation lifecycle" reference class on cost-structure inversion grounds (wrong-delete cost is `git revert` here vs. audit risk in enterprise). (confidence: direct)
3. [outside-view] Subagent rejected "open-source library maintainer cleanup" class because external-link-breakage does not apply to this repo. (confidence: direct)
4. [outside-view, web] Web source cited for currency: "Best Practices for Maintaining an Open Source Project Long-Term" — Outercurve Foundation. (confidence: direct — single web cite)

## Inferred claims
1. [outside-view] Base rate estimate: ~5–10% of solo repos institute a formal lifecycle primitive on first sweep; ~80–90% go ad-hoc. Numbers are explicitly flagged "qualitative" by subagent. (confidence: inferred)
2. [outside-view] Failure mode of formal-lifecycle path: policy written, used twice, then forgotten; the policy doc itself becomes an orphan. (confidence: inferred)
3. [outside-view] Failure mode of ad-hoc path: inconsistency surfacing at second sweep; maintainer cannot reconstruct rule 6–12 months later. Cost paid in re-decision, not lost data. (confidence: inferred)
4. [outside-view] At N=4 orphans + single maintainer, repo is "nowhere near" the under-designed-regret threshold (which historically involves repos that grew past solo scale). (confidence: inferred)
5. [outside-view] Net positioning: roughly at base rate for ad-hoc success, slight tilt toward "policy might stick here" due to maintainer's process-inclination — tilt insufficient to overcome Rule of Three. (confidence: inferred)
6. [outside-view] Mitigation proposed: a one-line rule in CLAUDE.md or decision log ("Default for orphans is delete; archive only for historical value to a future decision; wire-in only if load-bearing") — ~30 seconds of work, no new primitive. (confidence: inferred)
7. [outside-view] What would lift option (a) above base rate: evidence of recurring sweep cadence (third sweep, not first), or a second maintainer joining. (confidence: inferred)

## Authority-framed claims
1. "Gall's Law inverse: complex systems designed up front rarely work (John Gall, *Systemantics*, 1975)." — underlying claim: pre-designed lifecycle policy will likely fail. Quote present in output: no. Confidence: **unsupported (gap-declared)**.
2. "Rule of Three — Martin Fowler, *Refactoring*, 1999" invoked to argue N=4 is below pattern-recognition threshold. Underlying claim: do not abstract until ≥3 instances. Quote present in output: no. Confidence: **unsupported (gap-declared)**.
3. "Michael Nygard, 'Documenting Architecture Decisions,' 2011, the ADR origin essay … cost of recording a decision is small at the moment of decision and unrecoverable later." Underlying claim: even a 4-orphan sweep should produce a written record. Quote present in output: no (paraphrase only). Confidence: **unsupported (gap-declared)**.
4. "Andy Matuschak's working notes ~2020" cited for "Zettelkasten cargo-cult" tagging-and-lifecycle taxonomies the owner never used. Quote present: no. Confidence: **unsupported (gap-declared)**.
5. "Jonathan Corbet, LWN coverage of Linux kernel `Documentation/` reorganization, 2016–2018" cited as under-designed-cleanup-regretted case. Quote present: no. Confidence: **unsupported (gap-declared)**.
6. "Nick Coghlan PEP 426 retrospective, python-dev archives ~2013" cited for `distutils2` over-design failure. Quote present: no. Confidence: **unsupported (gap-declared)**.

## Contradictions surfaced
- **Ad-hoc-sufficient (subagent's main position)** vs. **Nygard write-it-down-now school**: Nygard's principle would push toward a written policy even at N=4. Subagent reconciles by saying Nygard advocates *per-artifact decision recording* (achievable via commit messages / `decision-log.md`), not a *new primitive class*. Reconciliation is itself an interpretation, not a quote from Nygard.
- **Over-designed-regret cases** (distutils2, Zettelkasten taxonomies) vs. **under-designed-regret case** (Linux kernel Documentation/). Subagent argues the under-designed cases all involve scale beyond solo maintainer; orchestrator should note this is the subagent's calibration, not an externally validated claim.

## Subagent's own verdict (verbatim)
"Below base rate for option (a) (new lifecycle primitive); at base rate for option (b) (ad-hoc)."

## Gaps the subagent missed
- No examination of the cost of the *one-line rule* itself becoming stale or contradicted by future decisions — the mitigation is treated as free.
- No discussion of whether this repo's prior sweeps (the session-artifact directories list multiple 2026-04-27 items) already constitute a *recurring* cadence that would lift option (a) — subagent assumed "first sweep" without verifying.
- No reference-class consideration of *meta-repos whose product is process* — subagent acknowledged the meta-stack tilt but did not search for analogous meta-tooling repos (e.g., dotfiles maintainers, prompt-engineering repos) that may have their own base rates.
- Canon citations all gap-declared; canon-librarian distillation must be cross-checked before any of the named principles (Gall's Law, Rule of Three, Nygard ADR) is load-bearing in the generator step.

## Token budget
~780 tokens.
