# Frame challenges — Step-13 session ledger

> **Authoring note:** `frame-challenger` agent could not be invoked (no `Task` tool). Orchestrator-authored, deliberately written against the orchestrator's own draft.

## Challenge 1 (alternative frame): the ledger should not exist; the warnings should be inline in synthesis

**The current frame** treats "produce an audit artifact" as the answer. **Alternative frame:** the audit-warning-signal *is the only valuable thing*; the artifact is overhead. If the orchestrator computes 14 agent-calls / 1 decision and writes "ledger: ratios above threshold; consider whether this session over-elaborated" *into the synthesis itself*, the operator gets the signal at the point of attention. The ledger.md file becomes unnecessary; the warnings live in synthesis.md as a final section.

**Condition under which this frame wins:** if no automated cross-session aggregator is ever built, the ledger file is wallpaper — the warnings inline give 100% of the value at 0% of the artifact cost.

**Condition under which the current frame wins:** if cross-session aggregation is realistic (a future `bin/scan-ledgers.sh` that reads N sessions in one pass), the per-session file is the substrate that aggregation needs. Synthesis prose isn't grep-able the same way.

**My reading:** the entry's "Pairs with cross-session memory write" line commits to aggregation. The ledger file should exist *and* its summary should be cited inline in synthesis. Both, not either-or. This is a real challenge that the generator must address explicitly.

## Challenge 2 (alternative frame): the workflow doesn't need self-instrumentation; the operator does

**Current frame:** the workflow self-diagnoses. **Alternative:** the operator diagnoses; the workflow is just dumb-and-honest about what happened. In this frame, the ledger is just a *receipt* — no thresholds, no warnings. The operator decides what's "too much."

**Condition under which this frame wins:** if thresholds are guesses (and the entry concedes they are), warnings derived from those guesses are noise. Better to ship raw counts and let the operator's pattern-recognition do the diagnosis.

**Condition under which the current frame wins:** if the operator (or AI) systematically miss over-elaboration in their own work (which is the entry's premise — over-elaboration is the failure mode being targeted), guesses-as-warnings are better than nothing as a starting point.

**My reading:** the warnings ship, but explicitly labeled as "starting heuristics, calibrate from data." The ledger should make it cheap to *change* thresholds (constants in one place, not scattered across template prose).

## Challenge 3 (challenging a preserved primitive): manual orchestrator authorship is wrong

**Scope-map preserved:** orchestrator writes the ledger manually. **Challenge:** orchestrator-authored ledgers will drift in format every session because the orchestrator regenerates the markdown each time. The schema-drift failure mode named in the outside-view distillation lands on this preservation.

**Stronger version:** even with a template, the orchestrator's free-form authorship will produce slight variations (different ordering, different prose around counts) that defeat downstream `grep`/`scan` tools.

**My reading:** the template should be *paste-and-fill*, not *paste-and-rewrite*. The orchestrator copies the template verbatim and fills in numbers. Any prose flourishes go in a designated `## Notes` section that aggregators ignore. This is a real risk and the generator must address it.

## Challenge 4 (challenging a preserved primitive): synthesis as terminus

**Scope-map preserved:** synthesis is the operator-facing terminus; ledger is internal. **Challenge:** if the operator never sees the ledger, the warnings have no re-encounter surface — the outside-view's modal failure (wallpaper) lands directly on this preservation.

**Resolution path:** the synthesis must include a one-line citation of the ledger ("ledger: agent-calls=14, artifacts=22, loops=2/2; warnings: artifacts-per-decision above threshold"). This is cheap and makes the ledger's signal load-bearing without requiring the operator to open the file.

**My reading:** this is the most important challenge. The generator must commit to the synthesis-cites-ledger pattern, or the whole system is wallpaper.

## Net challenge to the generator
1. Address whether the ledger file exists at all, given inline-in-synthesis is an alternative.
2. Address how schema drift is prevented (template, not free-form generation).
3. Address how the operator re-encounters the warnings (synthesis citation).
4. Address whether thresholds are configurable from one place.

If the generator doesn't address all four, the candidate is incomplete.
