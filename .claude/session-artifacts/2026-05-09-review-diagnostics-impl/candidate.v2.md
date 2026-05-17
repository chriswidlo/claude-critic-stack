# Candidate recommendation v2 — review-diagnostics-impl

This is loop 2. The v1 candidate ([candidate.md](candidate.md)) was rejected by all three lenses. The rewrite addresses the binding objections in [critiques.md](critiques.md) directly, does not defend the prior posture, and ships **two load-bearing actions plus a deferred list with named re-entry conditions** — per the product lens's #10 ("seven ranked actions queued is the research-theater failure mode the frame promised to counter-pressure").

## Position (one sentence)

**Land two structural changes — an executable schema contract that gates producer/consumer drift, and a hook-exec wrapper with a synchronization-aware Stop discipline — and explicitly defer everything else with a named re-entry condition. Honor the operator's dogfooding framing; do not retire the catalyst question; tell the truth on the dashboard.**

## What changed from v1

The v1 candidate had the right *posture* (kill more than ships) but applied it to the wrong *unit of analysis* (fields rather than aggregate boundaries and synchronization), used the wrong *contract shape* (prose rather than executable schema), and produced a net-negative day-after-ship operator experience. The rewrite:

- Drops from seven actions to **two load-bearing + one deferred set with re-entry conditions**.
- Replaces "kill `verdicts` field + demote `duration_seconds`" with **"keep both collected, tell the truth on the render"** — the catalyst question stays a live product surface.
- Replaces prose conformance with **`metrics.schema.json` (JSON Schema draft-2020-12) + producer/consumer validation**.
- Adds a **synchronization contract** between Stop hook's parser and ledger-render's metrics read: `parser.lock` sigil, bounded poll, loud-skip on timeout. Eliminates the silent-skip-as-fallback class of incidents.
- Wraps `hook-exec.sh` in **additive rollout** (two-systems-running window of ≥5 sessions) with **named failure semantics** (fail-open + named fallback to convention if wrapper missing).
- Drops the Heilmeier 6-month clock; replaces with a **session-count re-entry condition** tied to action volume rather than calendar.
- Drops dogfooding-as-confounder pessimism: the operator runs review-shaped sessions on this stack and that is the use case being supported.

## Action 1 — Executable schema contract

Add `<target>/.claude/schemas/metrics.schema.json` (~30 lines, JSON Schema draft-2020-12) declaring the `metrics.json` shape:

- **Required at top level**: `tokens.total {input: int, output: int}`, `tokens.by_agent` (object, agent-type → `{input: int, output: int, calls: int}`).
- **Optional**: `duration_seconds` (int), `tool_calls.total` (int), `tool_calls.by_tool` (object), `loops` (int), `verdicts` (object).
- **Removed from required surface**: nothing. Both `verdicts` and `duration_seconds` stay collected and rendered when populated; consumers must handle the missing-field case.
- **Validated**:
  - `<target>/bin/parse-session-metrics.py` validates its output against the schema before write at line 251; on validation failure, the parser writes `metrics.json.invalid` (separate file, never read by consumers) and exits non-zero — the Stop hook surfaces this in the host hook log only, never to AI context.
  - `<target>/.claude/skills/ledger-render/SKILL.md` and `<target>/.claude/skills/explain/SKILL.md` validate input against the schema before read; on validation failure, silent-skip per the existing missing-file policy.
- **Documented**: `<target>/.claude/session-artifacts/README.md` gains a one-paragraph "Metrics conformance" section that *cites* `metrics.schema.json` as authoritative; the README does not enumerate fields (the schema is the source of truth).

Cost: ~1.5 hours. Files added: 1. Files edited: 3. Files deleted: 0.

**Why first.** The architecture lens's binding objection (prose conformance is decoration) and the product lens's "schema contract is a real commitment, treat it as one" objection both land on the same fix. The schema gates everything downstream — once the contract is executable, the field-level decisions ("kill verdicts? defer per-step timing?") become parser-author choices the schema enforces, not synthesis-level edicts.

**Tell-the-truth-on-the-dashboard rider.** As part of action 1, edit `<target>/.claude/skills/explain/SKILL.md:41` so the duration card renders, when fewer than 3 sessions have populated `duration_seconds`:

```
no diagnostics data yet — populates after 3 sessions
```

…instead of `~10 min`. The string is forecast-shaped, not apologetic. Address the product lens's "what stub string does the operator read every session" question directly. `duration_seconds` is **not** demoted; it remains a populated field rendered the moment data exists. This bundles into the schema-validation edit because it touches the same file region.

## Action 2 — Synchronization-aware hook-exec wrapper

Two coupled sub-actions on the host-runtime side, both addressing operations objections #5 and #7.

### 2a — `hook-exec.sh` wrapper, additive rollout

Add `<target>/.claude/hooks/hook-exec.sh` (~25 lines): takes a command, runs it under `set +e` with stdout and stderr both redirected to a staging log (never AI context); exits 0 on any inner failure.

Rollout:

1. **Phase A (≥5 sessions): two systems running.** All three hook scripts gain *new* commands routed through `hook-exec.sh`, but existing inline `2>/dev/null` redirects stay. The wrapper is exercised but not load-bearing; if it has a bug, the convention catches the leak.
2. **Phase B (cutover): convention removed, wrapper load-bearing.** After ≥5 sessions confirm Phase A works, edit the three hook scripts to remove inline redirects. The phase-A snapshot is preserved as a tagged commit (`pre-wrapper-cutover-2026-05-XX`) for rollback.
3. **Failure semantics:** if `hook-exec.sh` is missing or non-executable at session start, hooks **fail-open** with one-line stderr to host hook log (never AI context); a `session-start.sh` guard checks for the wrapper's presence and falls back to the inline-redirect convention if the wrapper is absent. The wrapper bug never blocks a Claude Code session.

### 2b — Stop-hook synchronization: lock sigil + bounded poll + loud-skip

Adopt operations option (c) + (d): the parser writes a `parser.lock` sigil at start (line 30 of parser, after argv parse) and removes it at successful end (after `metrics.json.write_text`). The Stop hook's order changes:

```
1. write end.ts
2. cp staged events/timestamps to diagnostics/
3. nohup parser ... &      ← parser writes parser.lock then runs
4. record parser pid in diagnostics/parser.pid
5. exit 0
```

Crucially: `rm -rf "$STAGING"` is **moved to the parser tail** (after successful `metrics.json` write), not the Stop hook (current line 24). If the parser crashes, the staging dir survives for forensic inspection. Operations objection #8 second half resolved.

Ledger-render gains a bounded poll (in the SKILL):

```
when about to read metrics.json:
  if diagnostics/parser.lock exists and < 2 seconds old:
    sleep 0.5; retry up to 4 times
  if parser.lock still exists after 2 seconds:
    write "## Metrics\n\n_parser-still-running at ledger-render time_\n" — loud-skip
  if metrics.json missing AND no parser.lock:
    silent-skip (the existing fallback — parser never ran, e.g., bypass session)
```

This collapses the operations lens's four options into one chosen path: lock-sigil with bounded poll, loud-skip on timeout, silent-skip on no-parser-was-expected. The class of "silent-skip masked a real failure" incidents (operations §1) is closed.

Cost: ~3 hours total for action 2 (wrapper + rollout + Stop-hook reorder + parser lock + ledger-render poll). Files added: 1. Files edited: 4 (three hooks, ledger-render skill, parser).

**Why second.** Operations identified the Stop-hook ↔ ledger-render race as the binding frame-level objection ("two-process synchronization problem with no synchronization primitive"). Architecture identified the wrapper failure-semantics gap. Both land in this single coupled action.

## Deferred — with named re-entry conditions

These are explicitly deferred. Each has a re-entry condition that, if met, re-opens the question. This is the product lens's "deferred-with-named-re-entry-condition" requirement.

| Item | Re-entry condition |
|---|---|
| Tighten verdict regex (`r"\bverdict\s*[:=]\s*(\w+)"`) | First time a `metrics.json` `verdicts` field shows a known-wrong value in a real session |
| Replace loop-count grep with `## Loop N` header counting | First time `loops` value disagrees with hand-count by more than 1 |
| Per-step duration breakdown | After 20 completed workflow sessions have populated `metrics.json` (matches Anthropic's ≥20-queries evaluation guidance from canon) |
| Replay parser against pre-2026-05-09 sessions | Optional, before action 2 cutover (Phase B) — provides additional confidence but not a gate |
| Canary on transcript-found / total-tokens | Replaced by action 2's `parser.lock` + loud-skip discipline; if loud-skip fires twice, the canary becomes obligatory |
| Cost-in-$ field | After session-count re-entry above |
| Cross-session aggregation skill | After session-count re-entry above |
| Privacy-mode toggle | First time the operator runs a session against a private repo with `--privacy-mode` ask |
| Split parser into host-adapter + workflow-summarizer | If `parser.lock` loud-skip fires, OR if a host-layout drift requires more than one parser commit in a 30-day window |
| Parser canary (transcript-found, subagent-count, total-tokens) | If host-layout drift is detected once (any parser-side patch needed for layout reasons) — this is the architecture lens's coupling-debt-paydown signal in its operationally cheapest form |

## Frame-level objections, addressed directly

- **Architecture's "module-level reframe":** acknowledged. The parser is a single module spanning three aggregates. This rewrite **declares the monolith transitional** rather than fixing it. Re-entry condition for the split: parser.lock loud-skip fires once, OR a host-layout drift demands a parser patch. Both are loud failures; both unambiguously trigger the redesign.
- **Operations's "synchronization is the missing primitive":** addressed in action 2b. The lock-sigil + bounded poll + loud-skip is a named contract between two processes, replacing silent-skip-as-fallback.
- **Product's "the catalyst question is retired without replacement":** explicitly rejected as a recommendation. `duration_seconds` stays collected and rendered. The dashboard's stub string changes from `~10 min` (false confidence) to `no diagnostics data yet — populates after 3 sessions` (forecast-shaped). The operator's literal question stays answerable; the answer's *quality* improves over time as data accumulates.
- **Product's "honor operator's dogfooding":** dogfooding-as-confounder is dropped from the final posture. The operator runs review-shaped sessions on this stack and that is the use case the layer supports. The pessimism in v1's "sample-of-one validation" goes.
- **Product's "Heilmeier imports an industrial frame":** dropped. No 6-month clock. The session-count re-entry conditions in the deferred table are tied to the layer's *use*, not to a calendar.

## Named tradeoffs

- **Vs. doing nothing.** The two actions cost ~4.5 hours and add three commitments (a schema contract, an additive rollout, a synchronization contract). All three are reversible. Doing nothing keeps the layer at "shipped + un-stressed"; doing this puts the layer at "shipped + structurally enforced + synchronization-explicit."
- **Vs. the v1 seven-action posture.** This rewrite trades breadth for ownership. Two actions can be enacted by one operator in one afternoon; seven cannot. The deferred items are not promises to ship — they are tripwires. If a tripwire fires, the item re-enters consideration; if no tripwire fires for six months, the item was correctly deferred.
- **Vs. splitting the parser now.** Architecture's preferred end-state (host-adapter + workflow-summarizer) costs ~6 hours additional and ships unstressed. Deferring it to a tripwire keeps the rewrite small and lets reality decide.
- **Vs. tightening regexes now.** v1 had this in its first two actions. The rewrite defers them to known-wrong tripwires. The cost is one false-positive verdict in some future session before the tripwire fires; the gain is no premature parser edits.
- **Vs. retaining the canary.** v1 action 6 is replaced by `parser.lock` + loud-skip. The canary's job (detect silent attribution drift) is preserved; the implementation is simpler. The architecture lens noted canary-with-acceptance was postponing coupling debt; the lock-sigil approach pays the synchronization debt without taking on the coupling debt.

## Named assumptions (≥ 3 that would flip the recommendation if wrong)

1. **The operator runs review-shaped sessions on this stack as the dominant use case.** If this is true, dogfooding samples *are* representative (per product lens) and the canon ≥20-baseline gates are sensible. *Flip condition*: if the operator routinely uses the stack for non-review tasks (e.g., spot facts, ad-hoc research), the v1's dogfooding-as-confounder concern returns, and per-step timing should land sooner because the workload distribution is broader.
2. **JSON Schema validation in the parser tail and consumer prologue costs <50ms per session.** The `jsonschema` Python library or a vendored equivalent must be available. *Flip condition*: if validation cost is non-trivial (e.g., Python startup pulls in 500ms of imports the host hook didn't already pay), action 1's parser-side validation must move to a smaller mechanism (a hand-written assertion list); ledger-render and explain validation can stay because they run lazily.
3. **The lock-sigil approach is correct over choosing synchronous parser in Stop hook.** This rewrite picks the lock because it preserves <100ms Stop hook cost. *Flip condition*: if parser runtime is in fact >2 seconds in real (non-dogfood) workloads, the bounded-poll timeout fires routinely, the ledger fills with loud-skip notices, and synchronous-parser-in-Stop becomes the cheaper choice (paying 2s of Stop hook latency once instead of cluttering ledgers).
4. **Phase A two-systems-running for the wrapper is safe.** The assumption is that running both inline `2>/dev/null` and `hook-exec.sh` for the same command is harmless (the wrapper redirects what the inline redirect would have redirected). *Flip condition*: if `hook-exec.sh` materially changes the command's exit semantics, environment, or stdin handling (it should not, but assume worst case), Phase A produces inconsistent behavior across hooks. Mitigation: the wrapper is unit-tested against a representative command (e.g., `date`) before Phase A starts.

## Named ways this could be wrong

- **The schema contract could over-constrain a future producer.** If a future parser version wants to emit a new field (e.g., `cache_hit_ratio`), it must update the schema first. This is the *intended* property; the failure mode is that the operator forgets to update the schema and the new field gets silent-stripped by the parser-side validation. Mitigation: the parser's schema-validation failure path writes `metrics.json.invalid` next to a successful `metrics.json` only if old schema still passes — otherwise the parser writes `metrics.json` per the new shape and validation flags the schema as out of date.
- **Loud-skip in the ledger could be operator noise.** If the parser routinely takes >2 seconds, the ledger fills with `_parser-still-running_` notices. Mitigation: the assumption-3 flip condition above; reconsider synchronous parser if the loud-skip rate exceeds 1 in 10 sessions.
- **Phase A might be skipped under operator pressure.** "It's just a wrapper, why not cutover today?" is a tempting shortcut. Mitigation: name Phase A in the upgrade entry as load-bearing for rollback; Phase B refuses to land without ≥5 Phase-A sessions logged.
- **The deferred-with-tripwire posture could turn into "deferred forever."** If no tripwire fires, the deferred items sit. The product lens's concern about backlogs disguised as verdicts could re-emerge. Mitigation: the *absence* of tripwires firing is itself useful information — at six months, count the deferred items that have not re-entered. If most are still deferred, the operator's instinct to ship them in v1 was wrong; if many have re-entered, v1's deferral was wrong. Either way, the data is honest.
- **Killing the dogfooding-as-confounder framing might be over-correction.** If the operator does run non-review sessions and those produce wildly different metrics, the layer's averages will mislead. Mitigation: the explain card's stub string ("populates after 3 sessions") and the schema's `tool_calls.by_tool` (optional) field together let the operator notice if a session looks atypical without re-imposing pessimism.

## What success looks like (for synthesis)

A panel-approved version of this rewrite produces, in roughly the next afternoon of operator work:

- **One file added**: `<target>/.claude/schemas/metrics.schema.json`.
- **One file added**: `<target>/.claude/hooks/hook-exec.sh`.
- **Five files edited**: parser (validate output, write `parser.lock`), ledger-render skill (validate input, bounded poll), explain skill (validate input, "no data yet" stub string), README schema doc (cite the schema file), three hook scripts (Phase A: route new commands through wrapper).
- **Zero files deleted in the load-bearing pass.** No `verdicts` parser deleted; no `duration_seconds` demoted; no actions queued for the operator to remember.
- **One tagged commit** preserving the pre-wrapper hook state for Phase B rollback.

Six months from now the diagnostics layer is either (a) stable + structurally enforced + synchronization-explicit, with the deferred items either still deferred (validating v1's deferral) or re-entered through a named tripwire (validating the tripwire mechanism); or (b) one of the tripwires fired loudly and triggered a redesign, which is also a successful outcome of the design — failure modes are detected, not silent.

The catalyst question is preserved as a live product surface. The dashboard tells the truth. The day after this rewrite ships, the operator opens `/explain` and sees a stub that promises a real answer when data accumulates, instead of a stub that lies about a synthetic average. That is the smallest, most-visible product surface in the rewrite — and per the product lens, the only one that mattered.
