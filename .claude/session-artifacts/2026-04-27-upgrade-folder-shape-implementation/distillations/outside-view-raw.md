# Outside-view forecast — raw return

**Canon access note.** Agent had no Bash/Glob/LS to enumerate canon. Closest references named: Hunt & Thomas (Pragmatic Programmer), Kahneman/Lovallo (1993), Hinsen / Sussman. **Declared gap:** canon likely does not directly cover "solo Obsidian/Hugo-style vault restructuring with sed link rewriting." Web sources flagged as supplementary, not promoted.

## 1. Reference class

Primary: **Solo-operator, version-controlled content-repo restructurings of 10–100 files where (a) the file move is mechanical, (b) one or more index/cross-link files must be rewritten in lockstep, and (c) a separate tooling/config file determines the shape of *future* entries.**

Most predictive adjacents in order:
1. Hugo "leaf bundle" migrations (flat `content/posts/foo.md` → `content/posts/foo/index.md`). Closest structural analog.
2. Jekyll `_posts` → collections restructurings.
3. Obsidian/Zettelkasten vault re-foldering with backlink rewriting.
4. `git mv` + `sed` codemod refactors in small repos.

Less predictive: monorepo layout changes (team coordination dominates), DB schema migrations (rollback semantics differ).

## 2. Base rate

For success defined as "clean completion, no partial state, operator continues using new shape, link integrity holds":

- Mechanical `git mv` of N≈30 files: ~98% success rate.
- `sed` link rewriting across one index file with ~30 substitutions: ~85–90% first-pass success.
- Joint success (move + rewrite + tooling edit lands coherently, operator keeps using new shape 30+ days later): ~75–85%.
- Adoption-of-new-shape success (operator does not partially revert or drift): ~90%+ when a tooling change forces new entries into the new shape.

Estimates from Hugo/Jekyll/Obsidian community-report patterns, not citeable hard data.

## 3. Position relative to reference class

**Favorable:**
- N=30 is small; well within `sed`-by-eye verification range.
- Single index file to rewrite (not N files cross-linking N files). Easy mode of the class.
- Solo operator, no CI, no live users → no coordination cost; rollback is `git reset --hard`.
- **Tooling-edit-first coordination is textbook correct sequencing** — converts migration from a deadline ("must finish before next entry") to a backlog ("migrate at any pace"). Largest single variance-reducer in the proposal.
- Design has been spiked; folder shape known to work end-to-end with consumers.
- `git mv` preserves history.

**Unfavorable / watch:**
- macOS APFS case-insensitive default. If any slug differs only by case from a directory name, `git mv` misbehaves silently. Low probability at N=30 but worth a pre-flight check.
- Single `sed` pattern over 30 link forms: if any link uses a non-canonical form (relative vs. absolute, with or without `.md` extension, with anchor fragments, inside code fences), regex misses or over-matches. **#1 failure mode in the class.**
- "Small accompanying edit to a slash-command definition file" is under-specified. If wrong, every NEW entry post-migration arrives in broken shape; damage compounds silently.
- No mention of a verification step (link-checker, or `grep` for orphaned old-shape paths after migration).
- No mention of whether the migration script is idempotent / re-runnable on partial state.

**Net: above base rate**, primarily because of tooling-first sequencing.

## 4. Typical failure mode (frequency-ordered)

1. **`sed` regex misses an edge-case link form** — anchor fragments (`slug.md#heading`), trailing slashes, links inside code blocks that should NOT be rewritten, or links from files outside `LEDGER.md` that the survey missed. Result: handful of broken links discovered weeks later. **Modal failure.**
2. **Tooling/config edit is subtly wrong** — new entries land in folder shape but with malformed path. Compounds silently.
3. **Partial migration becomes permanent** — operator migrates ~70%, gets distracted, repo lives in mixed shape indefinitely. The "migrate at any pace" coordination strategy *enables* this as the price of removing the deadline trap. Mitigated only by operator discipline or a periodic "remaining flat-shape entries" report.
4. **Case-insensitive filesystem collision** during `git mv` — rare at N=30 but catastrophic when it happens.
5. **Consumer outside surveyed set** — something reads old paths (external script, bookmark, published URL). Low risk on personal repo.

## 5. Verdict

**Within tolerance — above base rate.**

Cheap additions to lift further:
- Post-migration verification: `grep -rn 'upgrades/[^/]*/[^/]*\.md' .` for surviving flat-shape references; markdown link checker over `LEDGER.md`.
- Idempotency: script safe to re-run on partially-migrated state.
- Pre-flight check for slug case-collisions and for link forms in `LEDGER.md` the `sed` pattern won't catch.
- Named tripwire for failure mode #3: a one-line `find`/`ls` check reporting "N flat-shape entries remaining," so partial-state-becomes-permanent has a visible counter.

## Sources (web, not canon)
- Hugo leaf bundles: https://gohugo.io/content-management/page-bundles/
- Jekyll collections vs posts: https://jekyllrb.com/docs/collections/
- git mv on case-insensitive filesystems: https://git-scm.com/docs/gitfaq
