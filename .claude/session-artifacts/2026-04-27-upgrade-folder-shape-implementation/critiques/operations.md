# Operations lens — loop 1

**Verdict:** `rework`

**One-line:** four lift conditions are forward-path engineering; the actual failure mode is recovery-shape (operator stalls mid-migration, forgets script invariants); idempotency predicate is single-bit and misses half-migrated state.

## Most likely incident
At T+3 days, operator re-runs script after aborted first run. "Is entry already in folder shape?" returns true for entries where the file moved but LEDGER link didn't get rewritten. Script skips them. Half-migrated state becomes permanent. Operationally invisible until someone clicks a broken LEDGER link.

## Blast radius
~30 entries, one operator, no CI, no live URL. Bounded in artifacts. Larger in agent behavior — every subagent that reads LEDGER (canon-librarian, canon-refresher, classifier on cross-refs) gets stale paths and silently fails to retrieve.

## Rollback honesty
- "Run script against ONE entry first" is a canary in name only — needs a signal that fails loudly; only signal is operator eyeballing the diff.
- Crash mid-batch with dirty tree: candidate has `git status --porcelain` as pre-flight, not post-crash recovery. If script crashes after `git mv` but before `git commit`, working tree is dirty with renames; next invocation aborts on porcelain check; operator told nothing about what to do.
- Commit granularity inside step 5 unspecified.
- Two-systems-running window has no upper bound.

## Observability gap
LEDGER counter is the *only* signal. It can only be wrong "script ran successfully" or "script didn't run." It cannot detect *half-migrated entries* (folder exists, file moved, LEDGER link not rewritten) — those are neither flat nor folder, and the counter's predicate has to pick one.

No metric for: broken intra-LEDGER links, entries with folder but no `<slug>.md`, LEDGER rows pointing at unresolved paths. Each is a one-line `grep` or `find`; none in the candidate.

## Frame-level objection
**Migration-script reliability problem ≠ recovery-procedure problem.** Migrations of N=30 by solo operator on no-CI repo do not fail by being subtly buggy at scale — they fail by crashing once, operator coming back two weeks later, not remembering state, either re-running into wedged half-state OR doing rest by hand and leaving inconsistent corpus. **Four lift conditions are all forward-path properties; none is a recovery property.**

The operationally-correct addition: a `--status` mode that, with no side effects, prints how many entries are in flat / folder / half shape. The recovery primitive the four lift conditions don't provide.

## What would flip to approve
(a) Three-state idempotency predicate (flat / half / folder) with documented "complete half-migration" path.
(b) `--status` dry-run mode reporting all three states without side effects.
(c) Explicit per-entry commit granularity decision + printed-on-abort recovery procedure for dirty-tree-mid-crash case.
