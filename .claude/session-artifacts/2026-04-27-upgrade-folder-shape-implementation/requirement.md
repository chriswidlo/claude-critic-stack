# Requirement — upgrade-entries-as-folders implementation

## Primary label
refactor

## Default frame (from label)
What observable change would falsify "behavior unchanged"? The migration must ship with a behavioral test (e.g., the format-only state-transition gate, LEDGER link resolution, slash-command output) proving entries pre- and post-migration produce identical downstream signals — a passing `git mv` is not evidence of preserved behavior.

## Known frame bias
Calling a behavior change a refactor — specifically, items 4 (relates_to normalization) and 6 (slash-command bug fix bundled into the migration edit) are behavior changes hiding inside a "shape migration"; the refactor frame will tend to wave them through as incidental cleanup when each deserves its own falsification test.

## Secondary label
extend — the folder shape monotonically expands what an entry can carry (artifacts, sub-folders) while preserving the single-`.md` contract; the file move is mechanical, the surface-area expansion is the real change.

## Alternative classification
extend would become primary if the critique centers on the *new affordance* (entries-as-folders enabling stapled artifacts) rather than the *mechanics of moving existing files*. Given the question explicitly asks about migration script design, coordination strategy, and rollback — all preservation-of-behavior concerns — refactor wins.

## Gaps surfaced by the classifier
- No behavioral test suite is named — refactor claim is unfalsifiable without one.
- Entry count & state distribution unspecified (rollback cost scales with N).
- `bin/migrate-upgrade-shape.sh` idempotency claim has no named oracle.
- `relates_to` heterogeneity may already be failing some consumer; if so, deferral is a known-bug-extension.
- `sed` LEDGER edit straddles entries — script commit-granularity (per-entry vs. one big commit) unspecified.
- Slash-command bug bundling — does the bug have current downstream effect?

## Meta — write gap
`requirement-classifier` agent has only `Read`; orchestrator persisted this artifact. Reproduces the failure mode named in `upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk.md`.
