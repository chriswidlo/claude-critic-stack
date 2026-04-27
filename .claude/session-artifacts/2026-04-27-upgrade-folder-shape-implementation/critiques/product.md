# Product lens — loop 1

**Verdict:** `rework`

**One-line:** slug-vs-README.md is a naming-contract decision being deferred into "decide later" when reversal becomes 30× more expensive after migration runs; three open questions to operator is two too many; orchestrator hiding behind operator's prior accept rather than re-evaluating under implementation-critique lens.

## Day-1 visibility
**Single most operator-visible change:** LEDGER grows a header line "Flat-shape entries remaining: N" that ticks down across runs. That counter — not folder shape — is what operator sees every time they open LEDGER during the migration window.

**Second-most-visible:** slug appears twice in every path (`no-brainer/2026-04-26-foo/2026-04-26-foo.md`). Every `cd`, every fuzzy-find, every Obsidian backlink, every grep result carries the slug twice — forever, until convention is re-litigated.

## Pruned affordances (worse, not named in candidate)
- **GitHub web reading degrades.** Walking to `upgrades/no-brainer/<slug>/` shows a one-file directory listing, not the rendered doc. README.md inside the folder would have auto-rendered.
- **Path autocomplete gets worse.** `upgrades/no-brainer/2026-04-26-up<TAB>` used to complete to a `.md`; now completes to a folder, requires another `<TAB>`, completes to the same slug again.
- **`find upgrades/ -name "*.md"`** now returns LEDGER, README, and 30 entry docs. Filtering "just entry docs" used to be `-maxdepth 2`; now requires knowing the slug-rep convention to filter.

## Frame-level objection
**The candidate frames "decide later" as virtue (anti-anchoring, preserving operator agency) when it is actually the orchestrator deferring a contract decision into a state where reversal is 30× more expensive.** Slug-vs-README.md is a *naming contract* decision, not an *implementation detail*. Naming contracts are cheapest to change before migration, most expensive to change after. Putting it in "open questions handed to operator at synthesis" is structurally the wrong place; belongs as a **blocking decision before generator step**.

**Three open questions is too many of the wrong kind.**
- Q3 (script worth setup cost?) — re-litigating accept; should be off-ramp note, not co-equal third question.
- Q1 (slug-rep) — real binding decision; should not be one-of-three.
- Q2 (C vs C-prime vs D) — candidate already picked C-prime; presenting open is performative.

**One question deserves operator attention. Three signals orchestrator is uncomfortable committing.** Failure mode the lab's "honest about confidence" principle exists to prevent.

## On specific points
- **Tidy-by-hand reframe** — challenger landed real hits (script inherits failure class by-hand doesn't have at all; for N=30 a checklist takes the same wall-clock). Candidate's defense is "operator authorized" + "script gains value if any future entry needs migration." Second is *speculative future value* used to justify *concrete present complexity*. First is anchoring on prior accept rather than re-evaluating.
- **LEDGER counter** — assumption #1 ("operator will look at counter periodically") has no evidence behind it. Feature designed for a reading habit nobody confirmed exists.
- **Migration window TBD + heavyweight engineering** — modal execution is "operator runs it Sunday afternoon, takes 30 minutes, never runs it again." Most of the engineering pays premiums on risks that don't fire.

## What would flip to approve
Move slug-vs-README.md from "open question handed to operator at synthesis" to a **blocking decision before script runs**, and reduce three open questions to one.
