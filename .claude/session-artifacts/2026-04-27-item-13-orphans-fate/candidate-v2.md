# candidate-v2.md — item 13 (orphans fate)

## What changed from v1

Three convergent critic objections drove the rewrite:
- **Architecture:** v1's "no new primitive" was a measurement error — it was paying the full cost of a new primitive (session-artifact-as-deletion-log) without naming it. **Fix:** name the primitive explicitly. Smallest honest version: a 5-line `prompts/RETIRED.md` breadcrumb file. Path-keyed discoverability where the deleted artifacts lived.
- **Operations:** v1 atomic-PR'd a CLAUDE.md amendment, two deletes, and a rename together with no audit and no rollback criterion. **Fix:** drop the rename (replaced with header-only on the original filename); audit done (see §Inbound-link audit); CLAUDE.md amendment dropped entirely (see next bullet).
- **Product:** v1 slipped a workflow-contract change (CLAUDE.md step-9 amendment) into a janitorial sweep — bait-and-switch. **Fix:** drop the amendment. If pressure #2 is genuinely missing from the 12-step generator, that is a workflow-design decision worth its own session, not a one-liner riding on a cleanup PR.

## Position (v2)

**Five concrete actions, one commit, no CLAUDE.md amendment, one named new primitive (`prompts/RETIRED.md`).**

| orphan | disposition | concrete action |
|--------|-------------|-----------------|
| O1 — [prompts/five-pressures.md](../../../prompts/five-pressures.md) | **delete** | `git rm prompts/five-pressures.md`. No CLAUDE.md amendment. |
| O2 — [prompts/ultraplan-next-level.md](../../../prompts/ultraplan-next-level.md) | **delete** | `git rm prompts/ultraplan-next-level.md`. Coordinate with item 07 plan (see §Inbound-link audit). |
| O3 — [plans/ok-cool-this-is-warm-balloon.md](../../../plans/ok-cool-this-is-warm-balloon.md) | **header-only retention; no rename** | Prepend a one-line `> **Status:** shipped 2026-04-24, retained as design-record (alternatives-not-taken).` Filename unchanged; zero link-breakage. |
| O4 — [.claude/session-artifacts/exemplars/](../../exemplars/) | **defer to item 5, with explicit close-out clause** | Item 13 closes with footer note "O4 disposition deferred to item 5; if item 5 abandons the promotion mechanism, delete `exemplars/` then." Item 13 does not stay open indefinitely. |
| P — standing policy | **named explicitly: `prompts/RETIRED.md`** | New 5-line file in `prompts/` listing each removed prompt with one-line rationale + commit SHA. Discoverable by `ls prompts/` and `find . -name "RETIRED*"`. Lives where the deleted artifacts lived. |

## The new primitive, named

**`<dir>/RETIRED.md`** — a sentinel breadcrumb file added to any repo directory that is being emptied of all its load-bearing occupants in a sweep.

Contract:
1. **One per directory**, lifetime equal to the directory's lifetime.
2. **Format:** Markdown bullet list, one bullet per retired artifact, format `- <filename> — retired <YYYY-MM-DD>, <one-line reason>, recover via \`git show <sha>:<path>\`.`
3. **Created at deletion time**, in the same commit as the deletions.
4. **Updated, never replaced**, when subsequent deletions occur in the same dir.
5. **Removed** when the directory itself is deleted (file is its own record; nothing to migrate).

This is a new primitive. It is named explicitly. Its failure mode (the file goes stale or is removed without the dir being deleted) is observable: `ls <dir>/` shows mismatch between RETIRED.md content and actual file presence.

This satisfies architecture's "explicit > implicit primitive" objection. It is *less* of a new primitive than the implicit session-artifact-as-deletion-log v1 was paying for, because:
- It does not require any reader to know about the workflow's session-artifact convention.
- It does not couple `plans/` (work-tracking) to `.claude/session-artifacts/` (session record).
- It does not require slug-naming discipline on session ids.
- It does not impose any new contract on CLAUDE.md, agents, or the 12-step workflow.

## Inbound-link audit (operations critic's blocker)

Grep performed; results:

**O1 (five-pressures.md) live inbound:**
- `plans/2026-04-27-item-13-orphans-fate.md:11` — this plan; *describes* the orphan; survives deletion.
- `plans/2026-04-27-repo-cleanup-punch-list.md:240` — punch-list; *describes* the orphan; survives deletion.
- `prompts/ultraplan-next-level.md:33,41,183` — also being deleted as O2.
- 1 immutable session-artifact ([2026-04-24-repo-upgrade-research](../../2026-04-24-repo-upgrade-research/distillations/explore.md):8) — link-rot accepted per session-artifact README.

**Live break-risk: zero.** The two "live" references are descriptive prose, not load-bearing path resolutions.

**O2 (ultraplan-next-level.md) live inbound:**
- `plans/2026-04-27-item-07-residual-agents-md-refs.md:26,57` — references the file's line 39 as a path-discipline data point ("(if present)" guard for AGENTS.md). **Coordination required:** if O2 is deleted, item 07's plan needs a one-line note that the file no longer exists and the AGENTS.md guard scenario evaporates. The action is in-scope for this commit.
- `plans/2026-04-27-item-01-path-discipline-decision.md:56` — references O2 as a path-discipline-violating file; if O2 is deleted, the violation is also gone (good — closes another path-discipline data point).
- `plans/2026-04-27-item-13-orphans-fate.md:12` and `plans/2026-04-27-repo-cleanup-punch-list.md:22,155,229,241` — descriptive; survive deletion.
- Multiple immutable session-artifacts — link-rot accepted.

**Live break-risk: 1 plan needs a one-line update** (item 07). In-scope.

**O3 (warm-balloon) live inbound (would-be rename-breakers — moot since rename dropped):**
- `plans/2026-04-27-item-13-orphans-fate.md:13` and `plans/2026-04-27-repo-cleanup-punch-list.md:242` — both reference filename. With **no rename**, both survive unchanged.
- 5 immutable session-artifacts — would have link-rotted; with no rename, they don't.

**Live break-risk: zero (rename dropped).**

## Sequencing decision (operations critic's other ask)

Operations critic wanted rename → observe → delete sequencing. With the rename dropped (O3 keeps its filename), the reversibility-asymmetry that motivated sequencing is gone:
- Deletes are reversible via `git revert` (and discoverable via the named `prompts/RETIRED.md`).
- O3 header addition is reversible via `git revert`.
- No rename means no link-breakage to observe.

**One commit is correct.** The sequencing requirement was contingent on the rename being present; once removed, atomicity is fine. Rollback criterion: if `prompts/RETIRED.md` proves insufficient as a discoverability venue (see §Falsifier), revert the deletion commit and the file is back in <30 seconds.

## Falsifier (operations + product critics' ask)

**Memory-independent trigger replaces v1's 6-month maintainer-memory test.**

The trigger is **`prompts/RETIRED.md` itself**:
- Any future session looking for `five-pressures` or `ultraplan-next-level` runs `find . -name "*pressures*"` → finds nothing in the live tree.
- Same session runs `ls prompts/` → finds `RETIRED.md`.
- Reads it → answer in <30 seconds.

If the future session does *not* run `ls prompts/` (instead going straight to git log or giving up), the discoverability mechanism has failed and the failure is observable in the session's transcript. The trigger does not require the maintainer to remember anything.

A second falsifier, weaker but cheaper: at the next sweep (whenever it happens — observable from `git log -- plans/*-cleanup*.md`), check whether the orphans were re-discovered or stayed lost. If the next sweep starts with "wait, what was five-pressures?", `RETIRED.md` failed discoverability.

## Named tradeoffs (v2)

- **One named primitive (`RETIRED.md`) vs. zero primitives.** v1 tried for zero and was caught smuggling one in implicitly; v2 explicitly takes the cost of one named primitive. Trade: one new file, one new convention to maintain, vs. honest contract surface. Architecture critic's win.
- **No CLAUDE.md amendment vs. v1's amendment.** Trade: leaves pressure #2 ("≥3 candidate solutions") unaddressed in the workflow, vs. avoids slipping a workflow contract into a cleanup PR. If the pressure is real, it gets its own session. Product critic's win.
- **Header-only on O3 vs. rename.** Trade: less visual signal in `ls plans/` (the in-flight/shipped distinction relies on the Status header line), vs. zero link-breakage and no `plans/` heterogeneity issue. Operations critic's win.
- **Coordination with item 07 vs. independent.** Trade: this commit touches one foreign plan (item 07), expanding scope slightly, vs. leaving a stale data-point reference. Single-line edit; in-scope.

## Named assumptions (v2; ≥3 that would flip)

1. **`prompts/RETIRED.md` is discoverable by `ls prompts/`.** Assumes future sessions browse directories before concluding files don't exist. If they don't (and only `find` or `git log`), the breadcrumb is invisible. Verifiable in any future session within months. (Verified-by-design: the convention says "look in the directory the file used to live in"; this is a stronger affordance than v1's "look in the session-artifact dir".)
2. **The pressure-#2 gap, if real, is worth its own session.** Assumes the maintainer is OK leaving a known small gap unaddressed for now. If they want it addressed in this PR, drop v2 and re-open with v1's amendment but as a separate commit.
3. **Item 5 will resolve O4 in finite time.** Assumes item 5 is on the punch-list and will be picked up. If it stalls indefinitely, O4 becomes the smallest-possible orphan-of-orphans. v2's footer ("if item 5 abandons the mechanism, delete `exemplars/` then") gives a self-acting fallback.
4. **The `RETIRED.md` convention will be remembered at the next sweep.** Assumes the convention is self-evident enough to be re-applied without needing a top-level rule. The file *is* the documentation of the convention; a future maintainer reading it for the first time can follow the format. If they don't, the convention dies after one use — but v2 doesn't depend on the convention propagating; one-shot use is sufficient for this sweep.

## Named ways this could be wrong (v2)

- **`RETIRED.md` may itself become an orphan.** If `prompts/` ever loses all live occupants and the maintainer doesn't delete the dir, `RETIRED.md` lives as a tombstone with no current relevance. Mitigation built into the contract (rule 5: "removed when the directory itself is deleted").
- **The pressure-#2 gap may be real and material.** If a future critic-architecture review (in another session) flags a candidate for under-enumerating alternatives, v2's choice to drop the amendment was wrong. The fix is cheap (re-open the question; `git show <sha>:prompts/five-pressures.md` recovers the source).
- **Item 07 coordination may be missed.** If the one-line update to item 07's plan is forgotten in this commit, item 07 has a stale data-point reference. Low blast radius; surface area = one plan file.
- **The "explicit primitive is better than implicit" frame may itself be wrong.** Architecture critic argued explicit wins on every axis except rhetorical. But there is a credible counter-position (the maintainer's frame in v1) that *fewer named conventions is better than more*, even if the unnamed one is doing real work. v2 takes the architecture critic's side; if the maintainer's taste actually leans the other way, v2 is wrong on its frame.

## Cheapest experiment (v2)

**At commit time, run the `RETIRED.md` test in a sibling Claude Code session.**

Open a fresh Claude Code session in this repo, post-commit, and ask: *"Did this repo ever have a checklist called 'five-pressures'? If so, why was it removed?"* Score:
- **Pass:** session reaches the answer in <2 minutes via `ls prompts/` → `cat prompts/RETIRED.md` → done.
- **Fail:** session searches git log, asks the user, or gives up. In that case, add a one-line note to CLAUDE.md path-discipline section ("when removing the last occupant of a load-bearing directory, leave a `RETIRED.md` per [convention](`<plan link>`)") so future sessions know to look.

This is **memory-independent** and **runnable immediately at commit-time** — not in 6 months. Cost: one extra prompt to a fresh session before merging.

## Verdict response to each critic

- **Architecture:** new primitive named explicitly (`prompts/RETIRED.md`); rename dropped, so link-graph audit on rename is moot; CLAUDE.md amendment dropped, so volatile→stable inversion is moot. Layering violation between `plans/` and session-artifacts is moot (no footer-link added; `RETIRED.md` lives where the deleted files lived).
- **Operations:** one commit is correct now (sequencing was contingent on the rename); CLAUDE.md amendment dropped, so no separate-commit need; falsifier replaced with a memory-independent commit-time test. Inbound-link audit done; one item-07 update in scope.
- **Product:** workflow-contract change (CLAUDE.md amendment) dropped — no bait-and-switch. Empty `prompts/` problem dissolved (RETIRED.md keeps the dir non-empty and self-explanatory). Falsifier mechanism is concrete (commit-time test in a sibling session).
