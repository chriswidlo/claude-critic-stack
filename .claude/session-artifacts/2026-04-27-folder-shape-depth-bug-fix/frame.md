# Frame — folder-shape depth bug fix (item 2)

## Revision 1

### What the user implicitly framed
"Item 2 is a mechanical fix. Add `../` to depth-broken chains so they click. Two files. Maybe twenty link edits. Done in an afternoon."

The framing optimizes for **completing a punch-list line item**. Item 2 reads as a contained chore.

### What that framing hides
Item 2 is the *symptom* of a regime collision, not a standalone bug. The symptom appears because:

1. The folder-shape migration (`<slug>.md` → `<slug>/README.md`, commit `c2fe604`) deepened every entry's path by one level **without** rewriting the link targets it contained. That migration was a structural change with a known long tail; item 2 is the long tail.
2. The two named files happen to be authored after the migration in `../`-chain style, so the deepening broke them. Files written in repo-root style (the rule's intended form) would have been immune.
3. The "fix" depends entirely on which path-discipline regime is in force after item 1. Under option (a), the right edit is "rewrite to repo-root form" — adding more `../` is wrong. Under option (b), the right edit is "add one `../`" — rewriting to repo-root is wrong. Same broken link, opposite resolutions.

### Reframe

The honest question is not "fix the broken links" but:

> **"What's the smallest change that makes the two files consistent with the path-discipline regime that wins item 1, while also reducing the chance the same bug recurs on the next folder-shape migration?"**

That reframe forces three things the original framing did not:

- A **regime check first** — don't edit until item 1's choice is committed in CLAUDE.md.
- A **scope check** — verify only those two files have the bug; other folder-shape entries may have been authored in repo-root style and be immune.
- A **recurrence check** — the next structural migration (e.g. `<slug>/README.md` → `<slug>/index.md` or some future folder reshape) will deepen paths again. Repo-root-relative links are immune; `../`-chain links break again. The fix-direction has consequences for the next migration's blast radius.

### Alternative optimization the user is not naming

The user is optimizing for **punch-list completion**. An alternative the user is not naming: **migration durability** — every `../`-chain link in the repo is a latent bug waiting for the next folder reshape. Item 2's two files are visible because they happen to break *now*. Other entries are fragile in the same way, just not currently broken. The wider question is whether to use item 2 as the wedge for a one-pass conversion of all active-surface entries to repo-root form, eliminating the latent bug class — or to keep item 2 narrow and accept that the next migration will produce a similar punch-list line.

### What I am explicitly not deciding here
- Whether item 1 will resolve to (a) or (b). That's item 1's decision, not item 2's.
- Whether item 3 should be bundled with item 2. That is a scoping question for step 7 (scope-mapper).
- Whether to add a link-checker. That is a recurrence-prevention question for step 9 (generator).

### Friction with the user's framing
The user said "write the best plan how to approach this item." The honest answer is that the best plan is **conditional**, with a hard precondition on item 1. Treating item 2 as unconditionally actionable is the failure mode I am refusing.
