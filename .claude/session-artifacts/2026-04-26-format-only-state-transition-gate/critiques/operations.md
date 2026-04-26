# Operations lens — critic-operations

**Verdict:** `rework`

**One-line summary:** Phase 1's six-week "observation window" has no measurement instrument; without a hand-labeled ground-truth set produced before the first audit run, the script's output becomes its own validation.

## Most likely incident
At T+11 weeks, a tolerant-grep pattern returns "pass" for an entry that documents a sibling probe; operator notices, loses faith, stops reading the report. Cause: tolerant matcher with no measurement of false-positive *or* false-negative rate, no labeling step.

## Blast radius
- Scope: 22 entries + n new during window. Small absolute.
- Human radius: 1 (solo operator). But: the operator's trust is the only consumer, and the proposal has no way to detect when that trust expires.

## Rollout / rollback gaps
- Phase 0 rollback: trivial (delete script). Honest.
- Phase 1 has no exit criterion other than "≥3 catchable drifts." No "saw nothing — now what" branch beyond a hand-wave.
- Phase 2 rollback: dishonest. Once N entries advanced through `/advance-upgrade`, removing the command leaves operator without an undo path except manual edit, which the proposal deprecated.

## Observability gap
`AUDIT-LOG.md` is prose, manual, single-file. No structured fields → no trend over runs. No "did the operator actually run the script" signal. No false-positive rate, no false-negative rate, no audit-skip rate. The four signals outside-view's modal failure mode would announce are all invisible.

## Cost at failure
- Steady-state: ~20 minutes operator time over 6 weeks. Cheap.
- False-positive cascade: trust-debits accumulate, no measurement.
- False-negative invisibility: zero in the moment, infinite-by-erosion later.
- Phase 2 retry-storm: no "force-advance with reason" escape valve; operator → manual edit → schema in open conflict with operator.

## Frame-level objection
**Phase 1 is not an observation window — it is a measurement program with no instrument.** Without a labeled validation set produced *before* the script's first run, the script's output becomes its own validation. Self-grading the validator with the same judgment the validator was supposed to replace.

**Secondary frame objection:** for a solo operator, no surface is non-bypassable in the traditional sense. The honest reframe is: the only non-bypassable mechanism is one that runs *without operator action and produces an artifact the operator sees regardless of intent* — a scheduled job posting into a surface the operator looks at anyway. The proposal does not propose this and explicitly avoids the closest analogue (pre-commit hook).

## What would flip to approve
(a) Hand-label 22 entries before first audit run; first run produces a confusion matrix not a vibe.
(b) Replace AUDIT-LOG.md with structured append (`pass_rate`, `false_positive_count`, `runs_since_last`).
(c) Name invocation surface concretely (cron / Routine / wired into existing command), not "trivially invocable" TODO.
(d) State Phase 2 rollback path honestly.
