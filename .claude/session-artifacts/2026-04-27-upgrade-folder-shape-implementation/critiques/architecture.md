# Architecture lens — loop 1

**Verdict:** `rework`

**One-line:** the "self-reporting counter" silently promotes `LEDGER.md` from index to runtime status surface; `bin/` is a permanent architectural commitment treated as a directory choice; load-bearing question "what is LEDGER.md" is unasked.

## Weakest structural link
LEDGER.md is being made a write-target of `bin/migrate-upgrade-shape.sh`. Before: human-curated index. After: runtime status surface written by a one-shot tool. Two consumers (LEDGER readers + script writer) now have to agree on counter format, location, lifecycle. Contract undocumented in candidate.

## Invariants at risk (unnamed)
1. Folder-name == doc-filename (`<slug>/<slug>.md`) — nothing enforces it. The gate doesn't verify parent-dir matches file basename.
2. One `.md` per entry folder, and that one is the entry doc — no enforcement; sibling `.md` files would be structurally indistinguishable.
3. LEDGER counter at N=0 — does the line stay, get deleted, signal "done" or "never started"?

## Coupling and direction (wrong)
Volatile (script, one-shot, will rot) writes to stable (LEDGER, lab's most-referenced index). Arrow points from throwaway tool *into* durable index. SRE "grab bag" passage applies almost verbatim — script does (a) move files, (b) rewrite LEDGER links, (c) write status counter, (d) verification grep. Four responsibilities, one binary, all touching the same file.

## Ignored alternatives
1. Counter in `bin/migration-state.txt` — same visibility; preserves LEDGER as index-only.
2. **No counter at all** — `make` target or shell alias computes count on demand. Derived state vs stored state.
3. Script at `upgrades/.bin/` — co-located with data; avoids declaring repo-global "bin/".
4. **Strangler-style** — write new shape's invariants into `check-transition.py` (gate refuses to advance flat-shape entries); entries migrate naturally as they advance; no batch script needed.

## Frame-level objection
**The actually-load-bearing question is "what is `LEDGER.md`?"** — index, queue, dashboard, log, or contract. Today: index. Counter amendment promotes it to dashboard. Script's link rewrites treat it as contract. Until the lab decides what LEDGER *is*, every tool that touches it negotiates its meaning ad-hoc. Each negotiation accretes one more responsibility.

**Second:** introducing top-level `bin/` is not a directory choice; it's a declaration that the repo now has "executable tooling, repo-global." First inhabitant sets the convention. That's a bigger decision than the migration it serves.

## What would flip to approve
(a) Move counter out of LEDGER OR justify in writing what LEDGER.md *is* and why a counter belongs there.
(b) Justify top-level `bin/` against the alternative of `upgrades/.bin/` or co-locating with the data.
