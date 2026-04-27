# Scope map — folder-shape depth bug fix (item 2)

## Existing primitives touched

| primitive | source (where it was named) | relationship | one-line rationale |
|-----------|-----------------------------|--------------|--------------------|
| 1. Two named broken files (`critics-get-write-tool/README.md`, `workflow-docs-scattered-and-stale/README.md`) | requirement.md, punch-list, [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md) | replace | The `../`-chain link bodies inside each file get rewritten to repo-root form (under option a); the file objects survive but the link surface is replaced wholesale. |
| 2. `living-poweruser-knowledge-module/README.md` (1 old flat-shape ref at L48) | [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md) §wider scope | extend | One-line edit; same edit class as item 3, surfaced by Explore but outside the two named-file scope. Extension is justified because exclusion would knowingly leave a Explore-confirmed broken link in active surface. |
| 3. Item 3 of punch list ("Fix pre-folder-shape `.md` references" — 3 upgrade-README occurrences) | requirement.md §gaps, [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md) §old flat-shape refs | subsume | Two of the three occurrences (L20, L158, L190) live in the *same file* as item 2's targets; the third (L48 of living-poweruser) is one-line. Same edit class, same files, same review pass. Bundling chosen — see "Bundling decision" below. |
| 4. Item 1's plan (`plans/2026-04-27-item-01-path-discipline-decision.md`, recommends Option A, uncommitted) | requirement.md §conditional shape, frame.md §reframe | conflict | Item 2's correct fix-form is determined by item 1's resolution. Cannot proceed under both options simultaneously. See "Requires decision" below. |
| 5. Path-discipline rule in `CLAUDE.md` L7-16 | CLAUDE.md, requirement.md | extend | Rule already mandates repo-root-relative; the broken files are in violation of an existing rule. Item 2 brings them into compliance — this extends the rule's *enforcement footprint* without changing its text. |
| 6. `/upgrade` slash command (`.claude/commands/upgrade.md`) | item-1 plan reference (per task brief) | extend | Item 1's plan names this as the structural cause of recurring drift but does not modify it as part of item 2. Preserved with stated reason: structural fix is item 1's plan-step territory, not item 2's. |
| 7. Session-artifact sanctity rule (commit 5108ed3, [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)) | task brief, [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md) §inferred §4 | extend | Rule explicitly forbids style-editing session-artifact files. Item 2 must respect the boundary; the 7 flat-shape occurrences in session-artifacts stay broken-by-policy. The rule's coverage extends to this work. |
| 8. Two PASS files (`canon-r-and-d-lab-management-expansion`, `decision-registry-adl`) | [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md) §wider scope | extend | No edit needed; they already comply. Reference value: they prove repo-root-relative form is achievable and currently in use. Preserved as-is by virtue of being correct. |
| 9. No link-checker in CI | requirement.md §gaps, [outside-view.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/outside-view.md) §verdict | extend | Outside-view names a mechanical verification step as a precondition for its "leaning favorable" verdict. Item 2 extends the falsifiability surface with at minimum a one-shot grep or local link-check; whether it ships a CI hook is a generator-step call. |
| 10. `bin/check-path-discipline.sh` (proposed in item 1 plan §Step 6) | task brief | conflict | Both item 1 and item 2 have a plausible claim to ship this. Cannot live in two plans. See "Requires decision" — defaulted to "out of item-2 scope" with rationale below. |
| 11. `r-and-d-lab-thesis/README.md` (mixed depth) | [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md) §wider scope | extend | Mixed file (some `../../` broken, some `../../../` correct). Same edit class. Including it under the same convention sweep is defensible; excluding it leaves a known partial-broken file in active surface. Default to extend (include in sweep). |

## Deletion cost (for subsume/replace rows)

- **Primitive 1 (two named files, replace):** 22 broken-or-wrong link occurrences rewritten (per Explore per-file tables, not the summary count of 20). Callers: zero inbound link audit was performed by Explore — flagged gap. Data migrations: none (text-only). Config surface: none. Blast radius is limited to the two file bodies; commit-bisectability stays intact if the two files are committed together. Risk: hand-edited 30-link batch typo rate is ~1-2 per outside-view §inferred §5 — verification step (grep for residual `../../`-without-third-dot, or markdown-link-check) is required, not optional.

- **Primitive 3 (item 3 bundling, subsume):** 3 link rewrites absorbed into item 2's diff. Callers: zero. Data migrations: none. Config surface: none. The deletion is of "item 3" as a separate punch-list line — punch-list is updated to mark item 3 closed-by-item-2. Blast radius: punch-list bookkeeping only.

## Bundling decision (item 3 into item 2)

The distillations split:
- **Outside-view §verdict, §inferred §4:** "leaning favorable" for bundling; same edit class, coherent boundary, ~30 edits in <5 files is in the bounded-migration sweet spot (~80-90% clean completion).
- **Canon §contradictions:** Beyer "Release Simplicity" (one change at a time, bisectable) vs. Beyer "Eliminating Toil" + Negative LOC (fix the class, don't keep doing the work). Half-migration is forbidden ("I Won't Give Up My Code!").

**Position: bundle item 3 into item 2.** Stated reason: the canonical contradiction resolves in favor of bundling because two of the three item-3 occurrences are in the same file as item-2 targets, and the third is one line. "Release Simplicity" warns against bundling *unrelated* changes; here the changes are co-located in two of three files and identical in form. Splitting them produces two near-identical commits with the same review burden and the same blast radius — that is the toil pattern, not the simplicity pattern. The "half-migration is forbidden" rule (canon §inferred §6) cuts harder against splitting than the "one change at a time" rule cuts against bundling, given the colocation.

## Item 1 dependency

Item 2 is **conditional on item 1's commit** per requirement.md §conditional shape. The dependency is real: the correct fix-form differs between options.

**Stated assumption to allow item 2 to proceed without waiting:** treat item 1's plan recommendation (Option A — repo-root discipline kept) as the working assumption, because (a) Option A is already the rule in CLAUDE.md L7-16 (primitive 5), (b) the broken files are in violation regardless of which option wins (a non-broken `../`-chain link is still a path-discipline violation under the current text of the rule), (c) the two PASS files (primitive 8) already use repo-root form and have not been challenged. If item 1 resolves to Option B before item 2 ships, the work re-does in the opposite direction — flagged as an assumption-that-flips-the-recommendation for the generator step.

The honest answer remains "wait for item 1's commit." The assumption above is offered so the generator can produce a candidate; it is not an endorsement of proceeding without item 1.

## Requires decision (conflicts)

- **Primitive 4: Item 1 vs. item 2 sequencing.** Both cannot proceed independently because item 2's fix-direction is determined by item 1. User has not yet committed item 1. Recommended posture: block item 2 commit on item 1 commit; allow item 2 *planning* under stated Option-A assumption.

- **Primitive 10: `bin/check-path-discipline.sh` ownership.** Item 1's plan §Step 6 proposes it as an optional regression check; item 2's outside-view distillation requires *some* mechanical verification step. Both have a claim. **Default position:** the script ships with item 1 (structural change) and item 2 uses a one-shot inline grep (`grep -rn '\.\./\.\./[^.]' upgrades/*/*/README.md` or equivalent) as its falsifiability check. Reason: bundling a permanent CI artifact into a content-fix commit violates Release Simplicity more sharply than bundling co-located link edits does. User has not chosen; surfacing for the generator.

## Preserved primitives with stated reason (non-default)

- **Primitive 6 (`/upgrade` slash command):** preserved because item 1's plan owns the structural fix to recurrence (template/command guidance), not item 2. Editing the command inside item 2 would mix a content fix with a tooling change across an ownership boundary.
- **Primitive 7 (session-artifact sanctity rule):** preserved because the rule is explicit (commit 5108ed3) and the user has not asked to change it. The 7 flat-shape occurrences in session-artifacts stay as-is.
- **Primitive 8 (two PASS files):** preserved because they already comply — no edit is the correct edit.
- **Primitive 5 (path-discipline rule in CLAUDE.md):** preserved as text; its enforcement footprint extends. Editing the rule's text is item 1's territory.

## Cross-primitive conflicts

- **Primitive 7 (session-artifact sanctity) vs. Primitive 9 (link-checker):** any link-checker that runs across the whole repo will flag the 7 flat-shape occurrences in session-artifacts that the sanctity rule forbids editing. The check must scope-exclude `.claude/session-artifacts/` or accept persistent failures. Surfaced for the generator and frame-challenger.
- **Primitive 4 (item 1 dependency) vs. Primitive 3 (item 3 bundling):** if item 1 resolves to Option B (file-relative), item 3's flat-shape `.md` references still need fixing (they are folder-shape bugs, not path-style bugs), but item 2's link rewrites take the opposite form. The bundling decision is robust to item 1's outcome only for item 3's flat-shape fixes; for item 2's depth fixes, the bundling holds either way but the edit content flips.

## Primitives the distillations did not name but the query implies

- **Inbound links to the two named files** from elsewhere in the repo. Explore explicitly flagged this gap. If any agent/workflow/canon-entry links *into* these README files using a stale path, that link is broken in the inverse direction and item 2 will not catch it. A one-pass `grep -rn 'critics-get-write-tool\|workflow-docs-scattered-and-stale' --include='*.md'` would scope it. Prompts for a follow-up Explore.
- **Outbound links from `.claude/agents/`, `workflows/`, top-level README** to upgrade entries — also Explore-flagged. Same scoping question.
- **A canonical "what is the link convention" note** somewhere a future author will find before writing a new entry. Currently the rule lives in CLAUDE.md L7-16; whether that is sufficient is item 1's question, but item 2 may want a CHANGELOG-style note in the commit message at minimum.
- **Pre-commit hook or template guidance in `/upgrade`** — named by item 1's plan as the recurrence-prevention surface; item 2 does not touch it but assumes it exists or will exist.
