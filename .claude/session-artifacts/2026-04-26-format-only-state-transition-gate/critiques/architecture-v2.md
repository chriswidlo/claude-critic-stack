# Architecture lens — loop 2

**Verdict:** `approve` (with non-blocking improvements named below)

**One-line:** v2 successfully addresses all three loop-1 "what would flip to approve" conditions; remaining concerns are soft and improvable in implementation.

## Loop-1 conditions, addressed

(a) README named as single source of truth and dependency inverted — done.
(b) Audit collapsed entirely; conflation cannot occur — done.
(c) Rightmost-column invariant explicitly named as load-bearing and reported by the script — done.

## Remaining concerns (non-blocking)

1. **README is now machine-read; nothing in the README signals this.** Add an HTML comment marker or explicit sentence inside the new section: *"the `/upgrade advance` subcommand parses this table — preserve column shape."*
2. **Unnamed invariants the script depends on:**
   - Table-shape stability (column count/order/header text) of the README's two tables.
   - Emoji-as-stable-identifier (script keys on `🔬`, `📋`, etc.; transliteration to text breaks it).
   - Section-heading-presence ≠ section-content-meaningful (warning-only posture admits this implicitly; should be named).
   - Subcommand dispatch determinism in the slash command (first-arg = verb vs first-arg = capture content).
3. **New cross-directory coupling:** `.claude/commands/upgrade.md` now hard-depends on `upgrades/README.md`. Name this; if the lab is ever vendored or renamed, the command breaks.
4. **Schema-as-types alternative not engaged.** One sentence acknowledging it (gate at entry-creation via templating, vs. gate at advancement) would close the loop.

## Frame-level reservation (lens-adjacent, not blocking)

Subcommand-of-`/upgrade` overloads a verb. Defensible but the candidate didn't name that it picked between two contestable frames ("minimum slash-commands-to-remember" vs "each command has one job"). Reversibility is real; not load-bearing enough to block.
