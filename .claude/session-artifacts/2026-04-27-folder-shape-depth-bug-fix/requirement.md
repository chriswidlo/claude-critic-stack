# Requirement classification — folder-shape depth bug fix (item 2)

## Primary label
refactor

## Default frame (from label)
"What observable change would falsify 'behavior unchanged'? The behavior to preserve is 'every link in these two README.md files resolves to the intended target'; the test is a link-checker pass (or manual click-through), not just 'the diff looks right'."

## Known frame bias
Calling a behavior change a refactor. Specifically: under option (a) of item 1, the rewrite from `../`-chains to repo-root style is a *convention change* affecting how readers (humans and tooling) parse links — that is arguably an `extend` to the path-discipline rule's surface area, not a pure refactor. Watch for scope creep into "while we're here, fix other files too."

## Secondary label (if any)
migrate — if option (a) of item 1 wins, the work is migrating these two files from one link-style regime (`../`-chains) to another (repo-root). Two-systems-running concern is trivial (a single commit flips them) but the rollback path matters if other readers/tools depend on click-resolution.

## Alternative classification
migrate — becomes primary if item 1 resolves to option (a) AND the operator chooses to bundle item 3's pre-folder-shape `.md` references into the same sweep. At that point this is a convention migration across ~30 links in two files, not a depth-arithmetic fix.

## User's framing words
"Fix the folder-shape depth bug", "broken `../` chains", "should be `../../../`", "Done when: every link in those two files clicks". The phrase "should be `../../../`" presumes option (b) of item 1 (file-relative links with `../` chains). The phrase "every link clicks" also presumes (b) — under (a), the done-condition is "every link is repo-root-relative and grep-stable", not "clicks". The classification is therefore conditional on item 1's resolution; the operator's wording leans toward (b) but item 1's plan recommends (a).

## Conditional shape (item 1 dependency)
This requirement is **blocked on item 1**. Two distinct shapes:

- **If item 1 → option (a) (repo-root rule kept):** Work expands. Rewrite every `../`-chain link in the two files to repo-root form. Likely bundles with item 3 (pre-folder-shape `.md` references). ~30 link rewrites. Frame stays `refactor` but secondary `migrate` strengthens.
- **If item 1 → option (b) (file-relative rule adopted):** Work is the literal mechanical fix as written — add one `../` to each chain in the two files. Pure `refactor`, ~15 link edits, no convention question.

Do not begin item 2 work until item 1's plan is committed and CLAUDE.md is updated. Starting earlier risks doing the wrong fix and re-doing it.

## Gaps
- Item 1's resolution is not committed; the plan recommends (a) but CLAUDE.md is unchanged.
- Whether item 3 (pre-folder-shape `.md` references) should be bundled into the same sweep under option (a) is unspecified.
- No link-checker is named; "done when every link clicks" is currently a manual definition-of-done. A mechanical check (markdown-link-check or equivalent) would make the refactor falsifiable.
- Whether other folder-shape entries beyond the two named files have the same bug is unverified — a grep for `../../` under `upgrades/*/*/README.md` would confirm scope.
