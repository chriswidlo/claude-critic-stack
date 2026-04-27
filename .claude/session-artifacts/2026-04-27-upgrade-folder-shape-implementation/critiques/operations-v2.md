# Operations lens — loop 2

**Verdict:** `approve`

**One-line:** v2 dissolved the recovery-shape failure class by removing the batch step; remaining risks lower-severity than the script's; strangler's per-entry friction is the right shape for solo-operator no-CI lab.

## Loop-1 flip-conditions
- (a) Three-state predicate: moot (no script). Strangler's "is this entry flat-shape?" is two-state and checked at advancement-time only — no half-state to silently persist.
- (b) `--status` mode: replaced by `find` one-liner. Narrower coverage (only enumerates flat-shape) but the failure modes `--status` would catch are smaller in v2 because no batch step creates them.
- (c) Per-entry commit granularity + recovery: moot (no batch).

## Operational signal of strangler
The gate's printed migration command is loud, actionable, arrives at the moment the operator has context for the entry. Right shape.

## Mixed-shape window cost
**LOWER than I credited in loop 1.** LEDGER rows already point at canonical paths per row, so subagents follow the link without caring about shape. GitHub web rendering works for both. Only `find`/`grep` corpus-wide queries pay a small cost (one extra `-o` clause).

## On-demand `find` one-liner
- Correctness: works for entries dated 2020+.
- **Discoverability concern:** lives in candidate.md (a session artifact). Operator won't remember in 4 months. Right operational home is `upgrades/README.md` under "How to find un-migrated entries." v2 doesn't say this explicitly; would strengthen but not blocking.

## Residual frame note
The gate is not a control, it is a convention with a printed message. Voluntariness is the failure mode the moment any downstream tool starts assuming "advanced entry = folder shape." Not the case today.

## What would flip to reject
A second operator joining the lab; any downstream tool starting to assume folder-shape for entries past 🌱 created without checking the path itself.
