## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on the proposed folder-shape migration (flat → leaf-bundle, ~30 files, solo operator, `git mv` + `sed` link rewrite + tooling-config edit). Subagent returned a "within tolerance — above base rate" verdict with four named lift conditions and five frequency-ordered failure modes.

## Direct facts
1. [outside-view] Canon access was degraded: agent had no Bash/Glob/LS to enumerate canon; nearest references named are Hunt & Thomas (Pragmatic Programmer), Kahneman/Lovallo (1993), Hinsen, Sussman. (confidence: direct)
2. [outside-view] Declared canon gap: "canon likely does not directly cover 'solo Obsidian/Hugo-style vault restructuring with sed link rewriting.'" (confidence: direct)
3. [outside-view] Web sources cited (supplementary): Hugo leaf bundles docs, Jekyll collections docs, git-scm gitfaq on case-insensitive filesystems. (confidence: direct)
4. [outside-view] Reference class is "solo-operator, version-controlled content-repo restructurings of 10–100 files" with mechanical move + lockstep index/cross-link rewrite + a tooling/config file shaping future entries. (confidence: direct)
5. [outside-view] Most predictive adjacent: Hugo leaf bundle migrations (flat `content/posts/foo.md` → `content/posts/foo/index.md`). (confidence: direct)
6. [outside-view] `git mv` preserves history; rollback is `git reset --hard` (no CI, no live users). (confidence: direct)

## Inferred claims (base rates — explicitly flagged by subagent as "not citeable hard data")
1. [outside-view] Mechanical `git mv` of N≈30 files: ~98% success. (confidence: inferred)
2. [outside-view] `sed` link rewriting across one index file with ~30 substitutions: ~85–90% first-pass success. (confidence: inferred)
3. [outside-view] Joint success (move + rewrite + tooling lands coherently, operator still using new shape 30+ days later): ~75–85%. (confidence: inferred)
4. [outside-view] Adoption-of-new-shape success: ~90%+ when a tooling change forces new entries into the new shape. (confidence: inferred)
5. [outside-view] N=30 is within "sed-by-eye verification range." (confidence: inferred)
6. [outside-view] Tooling-edit-first sequencing converts the migration "from a deadline ('must finish before next entry') to a backlog ('migrate at any pace')" and is "the largest single variance-reducer in the proposal." (confidence: inferred)
7. [outside-view] macOS APFS case-insensitive default: low probability of slug/dir case collision at N=30 but worth a pre-flight check. (confidence: inferred)
8. [outside-view] The under-specified "small accompanying edit to a slash-command definition file" is a silent-compounding risk: if wrong, every NEW post-migration entry arrives in broken shape. (confidence: inferred)
9. [outside-view] No verification step and no idempotency claim are observed in the proposal. (confidence: inferred)

## Authority-framed claims
None. Subagent named Hunt & Thomas, Kahneman/Lovallo, Hinsen, Sussman only as canon-presence references; no claim is attributed to them. No ventriloquism.

## Contradictions surfaced
None internal. Subagent did surface a tension it did not call a contradiction: the tooling-first sequencing that earns the "above base rate" lift is the *same* mechanism that enables failure mode #3 (partial migration becomes permanent). Orchestrator should treat this as a structural tradeoff, not a flaw.

## Subagent's own verdict (verbatim)
"Net: above base rate, primarily because of tooling-first sequencing."

Also verbatim from §5: "Within tolerance — above base rate."

### Lift conditions (verbatim, all four)
- "Post-migration verification: `grep -rn 'upgrades/[^/]*/[^/]*\.md' .` for surviving flat-shape references; markdown link checker over `LEDGER.md`."
- "Idempotency: script safe to re-run on partially-migrated state."
- "Pre-flight check for slug case-collisions and for link forms in `LEDGER.md` the `sed` pattern won't catch."
- "Named tripwire for failure mode #3: a one-line `find`/`ls` check reporting 'N flat-shape entries remaining,' so partial-state-becomes-permanent has a visible counter."

### Modal failure mode (verbatim, #1)
"`sed` regex misses an edge-case link form — anchor fragments (`slug.md#heading`), trailing slashes, links inside code blocks that should NOT be rewritten, or links from files outside `LEDGER.md` that the survey missed. Result: handful of broken links discovered weeks later. Modal failure."

### Failure mode #3 (verbatim, with the coordination-strategy flag)
"Partial migration becomes permanent — operator migrates ~70%, gets distracted, repo lives in mixed shape indefinitely. The 'migrate at any pace' coordination strategy *enables* this as the price of removing the deadline trap. Mitigated only by operator discipline or a periodic 'remaining flat-shape entries' report."

### Other failure modes (frequency-ordered, condensed)
2. Tooling/config edit subtly wrong → new entries land with malformed path; compounds silently.
4. Case-insensitive filesystem collision during `git mv` — rare at N=30 but catastrophic when it occurs.
5. Consumer outside surveyed set (external script, bookmark, published URL) — low risk on a personal repo.

## Gaps the subagent missed
- No quantification of the failure-mode-#3 mitigation: subagent names "operator discipline" and a "remaining flat-shape entries report" but does not estimate how much either lifts the joint-success rate.
- No reference-class data on what fraction of mixed-shape "permanent" repos are actually harmful vs. tolerable. Implicit assumption that mixed-shape is bad; never tested.
- Canon-degraded run: subagent could not enumerate the corpus, so the "canon likely does not cover this" claim is itself unverified. Orchestrator may want a canon-librarian pass to confirm or contradict.
- No discussion of whether the spike already validated the `sed` pattern against the actual `LEDGER.md` link forms, or whether the pattern is still hypothetical.
- Failure mode #2 (tooling/config edit subtly wrong) is named as silently compounding but no lift condition addresses it directly — only the post-migration `grep` partially catches it, and only for shapes that have already been written.

## Token budget
~830 tokens.
