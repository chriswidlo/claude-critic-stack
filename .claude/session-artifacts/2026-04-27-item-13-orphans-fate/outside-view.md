# outside-view.md — item 13 (orphans fate)

## Canon-first declaration

Outside-view subagent attempted Mandatory #0 but had only Read/Web tools (no Grep/Glob to enumerate `canon/corpus/`). Cited canonical works are flagged **gap-declared**; orchestrator should cross-check against the canon-librarian's return.

## 1. Reference class

**Chosen class:** *Solo-maintainer or 1–3 person research/tooling repositories, < 2 years old, performing a first or second janitorial sweep on documentation artifacts.* Specifically: maintainer is also primary reader, artifacts are prose (not code), orphans number in single digits.

**Alternative considered and rejected:** *Enterprise documentation lifecycle management* (ISO 9001 records retention, large-org Confluence cleanup, ADR archival in 50+ engineer orgs). Rejected because the cost structures invert: in enterprise, cost of a wrong delete is high (someone else needed it; audit risk) and cost of a policy is amortized across many cleanups. In a solo R&D repo, cost of a wrong delete is `git revert`, and cost of a policy is paid every time the maintainer touches the repo.

A weaker alternative — *open-source library maintainer cleanup* — also rejected; those repos have external users whose links break, which this repo does not.

## 2. Base rates (qualitative, flagged)

- **Formal lifecycle primitive instituted on first sweep:** ~5–10% of solo repos. Typically maintainers with prior enterprise records-management experience.
- **Ad-hoc per-artifact decision (delete / archive-folder / wire-in):** ~80–90%. Dominant pattern.
- **Do nothing:** the *prior* state most repos are in at the moment a sweep is being considered; ruled out by the act of sweeping.

**Failure mode of formal-lifecycle path:** policy is written, used twice, then forgotten; the policy doc itself becomes an orphan; future sweep has to clean up the cleanup primitive. Gall's Law inverse: complex systems designed up front rarely work (John Gall, *Systemantics*, 1975).

**Failure mode of ad-hoc path:** inconsistency. Six months later the maintainer cannot remember why one artifact was deleted and another moved to `archive/`; the next sweep re-litigates each decision. Cost paid in re-decision, not lost data.

## 3. Position relative to base rate

**Pushing toward "ad-hoc is sufficient" (above the base rate for ad-hoc success):**
- Single maintainer — no coordination cost from inconsistency.
- N=4 orphans — well below the threshold where pattern-recognition pays off (Rule of Three — Martin Fowler, *Refactoring*, 1999).
- Repo already has session-artifact convention with date-slug IDs; archived items can be tagged in commit messages without new infrastructure.
- `git log` and `git mv` already provide a lifecycle audit trail for free.

**Pushing toward "policy may pay off" (below the base rate):**
- Repo is itself an *adversarial-review meta-stack*; meta-consistency may matter more here than typical because the repo's own behavior is its product.
- Maintainer is process-inclined (12-step workflow, hard gates, distillation artifacts) — the policy will likely actually be followed.

**Net:** roughly at the base rate for the ad-hoc path's success, with slight tilt toward "policy might stick here when it wouldn't elsewhere." Tilt not enough to overcome Rule of Three.

## 4. Typical failure mode of the more common path (ad-hoc)

**Inconsistency surfacing at the second sweep.** Maintainer deletes A, moves B to vague `archive/`, wires C, forgets D entirely. 6–12 months later cannot reconstruct the rule and either (i) wastes an hour re-deciding what their past self meant, or (ii) institutes the policy then — which is exactly what they would have done now, but with one more datapoint.

Mitigation is not a policy *primitive*; it is a **one-line rule recorded in CLAUDE.md or a decision log**: "Default for orphans is delete; archive only for historical value to a *future* decision; wire-in only if load-bearing." ~30 seconds of work, pre-empts the failure mode without a new primitive.

## 5. Historical cases

**Over-designed cleanup tooling, regretted:**
- Python `distutils` → `setuptools` → `distutils2` (PEP 382, abandoned ~2012). Successor packaging primitive designed before predecessor failure modes were characterized; `distutils2` eventually withdrawn. (Nick Coghlan PEP 426 retrospective, python-dev archives ~2013.)
- Personal-wiki tagging-and-lifecycle taxonomies the owner never used ("Zettelkasten cargo-cult", discussed in Andy Matuschak's working notes ~2020).

**Under-designed cleanup, regretted:**
- Linux kernel `Documentation/` pre-2016 accumulated stale docs without policy/owner; Jonathan Corbet's reorganization effort (LWN coverage, 2016–2018) was eventually required when ad-hoc path scaled past breaking point. Note: thousands of docs, not four.

**Calibration:** under-designed-regret cases overwhelmingly involve repos that grew past the solo-maintainer threshold without re-evaluating. At N=4 orphans and one maintainer, this repo is nowhere near that threshold.

## 6. Contradicting view

Strongest contradicting position: the *write-it-down-now* school (Michael Nygard, "Documenting Architecture Decisions," 2011, the ADR origin essay): the cost of recording a decision is small at the moment of decision and unrecoverable later. By that logic, even a 4-orphan sweep should produce a written policy, because the policy is the record of *why* you deleted vs. archived, not the rule itself.

Reconciliation: Nygard advocates recording the *decision per artifact* (which an ad-hoc commit message or short log entry achieves), not necessarily inventing a *new primitive class* for the lifecycle. The ad-hoc path with per-artifact reasoning recorded in commits or `decision-log.md` satisfies Nygard's principle without satisfying the policy-primitive proposal.

## Outside-view verdict

**Below base rate for option (a) (new lifecycle primitive); at base rate for option (b) (ad-hoc).**

Inventing a new primitive on the basis of four orphans violates the Rule of Three and risks the Gall's Law failure mode (the policy itself becomes an orphan). What would lift option (a) above the base rate: evidence of a *recurring* sweep cadence (third sweep, not first), or a second maintainer joining whose decisions need to be aligned with the first.

The ad-hoc path needs one cheap addition to hit the upper end of its base rate: a single sentence in a decision log per orphan recording *why* it was deleted/archived/wired. Not a new primitive — using primitives the repo already has.

---

## Sources

Web (currency check):
- "Best Practices for Maintaining an Open Source Project Long-Term" — Outercurve Foundation.

Canonical works cited from general knowledge (gap-declared; verify against [canon.md](canon.md)):
- John Gall, *Systemantics: How Systems Really Work and How They Fail*, 1975 — Gall's Law.
- Martin Fowler, *Refactoring*, 1999 — Rule of Three.
- Michael Nygard, "Documenting Architecture Decisions," 2011 — ADR origin essay.
- Andy Matuschak, working notes on evergreen notes and over-tagging, ~2020.
- Jonathan Corbet, LWN coverage of Linux kernel `Documentation/` reorganization, 2016–2018.
