# Architecture critique v2 — review-diagnostics-impl (loop 2)

## 1. Weakest structural link

**The `parser.lock` sigil is a file-presence-as-mutex pattern with no owner-liveness check, and `metrics.json` has no atomic-write or version stamp — so the race the synchronization contract claims to close is only narrowed, not closed.**

Three boundary cases break the contract:

a. **Stale-success race.** Parser run N writes `metrics.json`, removes `parser.lock`, exits. Stop hook fires for run N+1, copies new staging into `diagnostics/`, backgrounds parser N+1. There is a window — between staging copy and parser N+1 acquiring `parser.lock` — where ledger-render sees no lock and reads `metrics.json`. The file it reads is run N's metrics. The candidate's contract has no version stamp on `metrics.json` (e.g., `session_id` or `end_ts` field) that ledger-render can match against the session it is rendering, so the consumer cannot detect the mismatch. Schema validation passes; the data is wrong.

b. **Crashed parser + future render.** Parser writes `parser.lock` at line 30, segfaults on the host-transcript walk before line 251. `parser.lock` is now permanent. Every subsequent ledger-render for the rest of the session lifetime polls 2s, loud-skips. Operator restarts; the next session's parser sees `parser.lock` already present from the crashed predecessor and either (i) overwrites it (the candidate doesn't say) or (ii) refuses (also doesn't say). The contract does not specify lock acquisition semantics — it specifies only the consumer's poll behavior. A lock without an owner-liveness mechanism (PID + `kill -0` check, or mtime-bound staleness) is half a primitive.

c. **`metrics.json.invalid` masking last-good.** The candidate says: on parser-side validation failure, write `metrics.json.invalid` (separate file, never read). It does not say what happens to a *prior* `metrics.json` from an earlier run sitting in the same `diagnostics/` directory. If `diagnostics/` is per-session (likely from the workflow-id routing), this is moot — but the candidate doesn't make that explicit, and `stop.sh:24`'s `rm -rf "$STAGING"` is moved to parser tail per action 2b, which means `diagnostics/` is *not* wiped between sessions. A failed validation on session N+1 leaves session N's `metrics.json` in place. Consumer reads it, validates clean, renders it. Wrong session.

The lock-sigil is the right *category* of primitive. Its specification in this candidate is incomplete in three places that each independently re-open the race.

## 2. Invariants at risk (not named in the candidate)

1. **Lock liveness.** No mechanism distinguishes "parser is running and holds the lock" from "parser crashed holding the lock." Trivially fixed by writing `parser.lock` content as the parser PID and having ledger-render `kill -0` it, or by mtime-bounding (lock older than 30s is presumed dead). The candidate names neither.

2. **Metrics-to-session binding.** `metrics.json` has no field that pins it to a specific session/run. A consumer cannot detect "I am rendering session X's ledger but the metrics on disk are from session Y." The schema must require `session_id` and `end_ts` as top-level fields, and ledger-render must check both before consuming. Without this, the version-stamp invariant is implicit and violations are silent.

3. **Validation-failure idempotency.** If the parser crashes mid-write of `metrics.json` (between schema-validate and `write_text` returning), the file on disk may be truncated or partial. `write_text` is not atomic. The schema-validate step happens *in memory before* `write_text`; it does not protect the file. The atomic-write discipline (temp-file + rename) is missing.

4. **Lock acquisition semantics.** The candidate says "parser writes `parser.lock` at start." It does not say: must it not exist already? If it does exist, is that a hard fail, a logged warning + overwrite, or a wait? The choice has operational consequences.

5. **Schema evolution: producer-version ↔ consumer-version skew.** The schema is stored in-tree at `<target>/.claude/schemas/metrics.schema.json`. Producer (parser) and consumers (ledger-render, explain) all read the same schema file *at runtime*. If the operator updates the schema file between sessions — adding a required field — old `metrics.json` files in `diagnostics/` from prior sessions now fail validation in consumers. The candidate's response (silent-skip on consumer-side validation failure) hides the breakage; the operator sees missing ledger sections and does not learn that schema migration is what caused them. The schema needs a `$id` + version (e.g., `2026-05-09/metrics.schema.json`) and `metrics.json` needs to embed which schema version it was written against, so consumers can detect skew and report it loudly.

## 3. Coupling and direction

- **Parser → schema file → consumers**: dependency direction now points correctly from volatile to stable, *if* the schema is treated as the stable surface. The candidate establishes this. Approved direction.
- **`parser.lock` → ledger-render polling logic**: the consumer (ledger-render skill) now has to know the parser's protocol. This is new coupling — minor, but the SKILL.md now contains polling logic that is meaningless outside the parser-context. If the parser is ever replaced (alternative #2 from loop 1, pull-architecture), the polling code in ledger-render is dead weight that someone has to know to remove. Acceptable as transitional; should be flagged.
- **Schema file as third party between parser and consumers**: the candidate doesn't say where schema validation libraries live. If `jsonschema` (Python) is used in the parser and a JS or shell implementation is used in the SKILLs, divergent validators can produce divergent verdicts on the same `metrics.json`. The candidate's assumption 2 names cost but not implementation. Specify: parser uses `jsonschema` (vendored or stdlib check); SKILLs validate via the same library invoked through a small shell wrapper, *not* via reimplementation.
- **Layering: still violated, by design.** The parser still walks host-transcript layout, host-subagent layout, *and* workflow critiques + decision-log in one process. The candidate names this as transitional with a tripwire.

## 4. Ignored architectural alternatives

1. **Per-session diagnostics directory with full lifecycle.** Instead of a shared `diagnostics/` with a `parser.lock` sigil, each session writes to `diagnostics/<session-uuid>/`, the parser writes its outputs there, and ledger-render reads only from the directory matching the session it is rendering. This collapses the race entirely (no shared mutable state across sessions; concurrent sessions don't contend) and eliminates the need for `parser.lock` and version-stamping. The candidate inherits the existing shared-directory layout without questioning whether per-session isolation is the cleaner primitive. **Race elimination through naming, not synchronization, is the architecturally cheaper pattern** when the sessions are independent (which they are here).

2. **Atomic `metrics.json` via tmp-file + rename, with sentinel removal as the publish event.** Drop `parser.lock` entirely. Parser writes `metrics.json.tmp`, validates, `os.rename(tmp, final)`. The presence of `metrics.json` *is* the lock-released signal; its absence means parser hasn't published yet. POSIX rename is atomic on the same filesystem. Consumer reads `metrics.json` or finds it missing — there is no half-written state. This eliminates the lock-staleness class of bugs (1.b above) and the lock-acquisition-semantics question (invariant 4) in one move. **Filesystem atomicity is a stronger primitive than file-presence-as-mutex and the operating system gives it for free.**

## 5. Frame-level objection

**The candidate has adopted "synchronization contract" as the design lens but stops at the consumer-side polling protocol — it does not extend the contract to cover *what the consumer is reading*, only *when it can read*.** A complete synchronization contract has four parts: (i) when may the producer write, (ii) when may the consumer read, (iii) how does the consumer know which producer-run produced what it is reading, (iv) how do producer and consumer agree on schema version. The candidate addresses (i) implicitly (parser holds the lock during write) and (ii) explicitly (poll + bounded retry + loud-skip). It does not address (iii) — there is no `session_id`/`end_ts`/`schema_version` on `metrics.json` — and barely addresses (iv) — schema is in-tree but not versioned in the data.

The frame error is treating synchronization as a *temporal* contract (lock + poll) when it is also an *identity* contract (which run, which schema). This is the same shape of mistake the loop-1 candidate made with prose conformance: stopping at the surface where the design feels complete rather than where the contract is closed.

## 6. Direct answers to stress questions

**Q1 — does the JSON Schema contract actually solve the problem.** Mostly yes, with two specific gaps. The producer-validates-before-write + consumer-validates-before-read pattern is architecturally correct and gains the property prose lacked: executable enforcement. Gaps: (a) no `metrics.json` versioning/identity field, so a schema-clean stale file from a prior run passes validation and is consumed; (b) no `$id` or schema-version field, so producer/consumer schema drift across operator updates is silent on the consumer side. Both fixable: add `session_id`, `end_ts`, and `schema_version` as required top-level fields. With those, the stale-file boundary case becomes detectable and loud.

**Q2 — does lock-sigil + bounded-poll close the race.** **No, it narrows it.** The contract closes the within-session race modulo crash-staleness. It does not close: (a) the cross-session race where ledger-render reads a `metrics.json` from a previous session because the directory is shared and no version stamp exists; (b) the crashed-parser-leaves-stale-lock case, where `parser.lock` becomes permanent without a liveness mechanism; (c) the rename-atomicity gap, where mid-write parser crash leaves a partial `metrics.json` that may pass schema validation by coincidence. The lock primitive is right in category, incomplete in specification. To close: PID-or-mtime liveness on the lock, atomic rename for `metrics.json` publish, and a `session_id` on `metrics.json`.

**Q3 — deferred-with-tripwire posture, does it preserve the architecturally-correct end-state.** **Partially. The tripwires are too subtle.** The "parser.lock loud-skip fires" tripwire is observable (the operator sees it in the ledger). The "host-layout drift demands a parser patch" tripwire is *not* — it requires the operator, while writing a parser commit, to correctly classify it as layout-driven rather than just shipping the patch. There is no mechanical detector. The rewrite addresses the loop-1 coupling-debt-exam concern by changing the trigger from a calendar exam to a tripwire, but the tripwire that detects coupling debt is a self-report tripwire and self-report tripwires under operator pressure routinely fail to fire. Make this tripwire mechanical: a CI check, pre-commit hook, or commit-message convention that flags any parser commit touching `find_transcript`, `find_subagents_dir`, or any function that walks the host-runtime layout, and counts those commits separately.

**Q4 — what did the rewrite get wrong or miss.**

- Schema does not require `session_id`, `end_ts`, or `schema_version` (§5 above; invariants 2, 5).
- `metrics.json` write is not atomic (invariant 3); `write_text` is the same non-atomic call the v1 had.
- `parser.lock` has no liveness mechanism (invariant 1) and no acquisition semantics (invariant 4).
- The "coupling-debt-paydown via host-layout-drift tripwire" requires self-report classification; needs a mechanical detector.
- Per-session `diagnostics/<session-uuid>/` isolation (alternative #1) is a structurally cheaper way to eliminate the cross-session staleness boundary case than version-stamping `metrics.json`; the candidate does not consider it.
- Validation library divergence between parser (Python `jsonschema`) and SKILLs (unspecified) could produce inconsistent verdicts on the same data; the candidate names cost but not the single-validator commitment.

## 7. Verdict

**rework**

What would change the verdict to `approve`: add `session_id`, `end_ts`, and `schema_version` as required top-level fields in `metrics.schema.json`, with consumer-side checks that the rendered session matches; switch `metrics.json` write to atomic tmp-file + rename; specify `parser.lock` content as PID with mtime-staleness fallback (lock older than 30s presumed dead); add a mechanical detector for the host-layout-drift tripwire (commit hook or CI flagging touches to host-layout walking functions). The remaining defects (validator-library convergence, per-session directory alternative) are commentary, not gates.

Per CLAUDE.md step 11 cap, this rework verdict at loop 2 of 2 routes to **escalation to synthesis with disagreements named**, not another rewrite. The named disagreements: (i) the synchronization contract is under-specified on the identity dimension, not just the temporal one; (ii) `metrics.json` lacks atomic publish; (iii) the coupling-debt tripwire is self-report and will not fire reliably under operator pressure.
