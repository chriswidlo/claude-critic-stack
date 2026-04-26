# Architecture lens — critic-architecture

**Verdict:** `rework`

**One-line summary:** the audit script's grep schema *is* the per-state transition schema, smuggled in as Phase 0 with no source-of-truth coupling to the README it implicitly forks.

(Full inline review preserved in orchestrator transcript; key load-bearing critiques below.)

## Weakest structural link
Two sources of truth for the lifecycle: README prose semantics + bash grep patterns. Candidate frames "schema lives in script" as parsimony but it is the duplication the proposal claims to avoid.

## Invariants at risk (unnamed)
1. Rightmost-filled-column = current state (script depends; README invites backfill).
2. Body-section presence implies body-section truth (grep cannot tell coincidental SHA from load-bearing one).
3. Tolerant matching is monotonically tolerant (no rule prevents tightening invalidating prior passes).
4. Phase 2 "/advance-upgrade is the only write path" — false on day one, historical entries written by manual edit.
5. AUDIT-LOG.md is itself ungated content, no schema, no parser.

## Coupling and direction
- Volatile (grep patterns) → stable (README) is the wrong direction. Should be inverted: script reads README as input.
- Hidden cycle through the operator: script reports → operator updates entries to pass → script reports again. The script *does* mutate entries, through the operator.
- Phase 2's same-script-in-`--enforce` mode conflates out-of-band auditor and in-band gate (SRE 2016 ch.26 explicitly separates these).

## Ignored alternatives
1. README-as-schema parser — script reads README directly, derives rules.
2. Folder-as-state — collapse schema problem to a `mv` precondition.
3. Schema-as-types — illegal states unrepresentable via templating.

## Frame-level objection
**The audit and the gate should not share a schema.** Audit's job is to *discover* what the lifecycle looks like; gate's job is to *enforce* what it should be. Conflating them — same script in `--enforce` mode — pre-commits the gate's schema to whatever the audit happened to grep for. Measurement that becomes contract is no longer measurement.

## What would flip to approve
(a) Name README (or explicit derived schema file) as single source of truth; invert dependency.
(b) Separate the audit artifact (discovery) from any future gate (contract) — different code paths, different artifacts.
(c) Name rightmost-column-equals-current-state as a load-bearing invariant the audit cannot itself check.
