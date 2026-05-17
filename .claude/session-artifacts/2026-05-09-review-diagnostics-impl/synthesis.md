# Synthesis — review-diagnostics-impl

## Classification

- **Primary label**: `investigation`
- **Alternative classification**: `extend` — frame-challenger argued this label flip would be more honest given that scope-map produced a ranked three-action list (an `extend`-shaped output, not investigation-shaped). Synthesis carries this slip explicitly: the session ran under the `investigation` frame but produced extend-shaped recommendations.
- **Frame bias the label carries**: research theater — findings that look thorough but map to no concrete action.

## Reframe (current)

The orchestrator's reframe replaced the user's *did-we-build-it-right* framing with **instrument-fit + dogfooding-as-confounder**: optimize the review for whether the shipped layer actually answers the operator's four catalyst questions, and treat this session's metrics as a sample-of-one drawn from the easiest possible workload.

Loop 1's product critique flagged the dogfooding-as-confounder half as a frame *choice*, not a discovery, and the loop-2 candidate dropped that pessimism. Final operative reframe: **instrument-fit, with the operator's review-shaped use case treated as the dominant load.**

## Reference-class forecast (outside-view distillation)

- **Class**: hooks against undocumented internal layouts (most-predictive); per-session AI-agent observability layers (active class); internal dev-tooling instrumentation decay; self-measurement traps.
- **Base rate**: ~15–30% joint survival × use at 6 months (definition: still producing usable data, consulted ≥monthly). All four numerical anchors (~40–60%, ~30–50%, ~15–30%, ~80%+) are subagent-flagged as **unsourced estimates**, not calibrated probabilities.
- **Position**: slightly **below base rate** on the strict definition, **at or slightly above** on the looser "ships and runs" definition.
- **Modal failure**: 6–9 months post-ship, host layout changes silently; parser returns `transcript-missing` or zero attribution; dashboard renders flat/wrong numbers; rewrite costs ~50% of original effort; deferred because diagnostics aren't load-bearing for any decision.
- **AI-blindness leak is *not* the modal failure** for the class. The review's load-bearing emphasis on it may be over-indexed against the actual risk distribution.

## Canon (supporting and contradicting)

**Supporting**

- **Anthropic, "How we built our multi-agent research system" (2025)**: precedent for AI-blind structural observability — *"we monitor agent decision patterns and interaction structures—all without monitoring the contents of individual conversations."*
- **Google SRE Book, Ch.6 §Four Golden Signals (2016)**: shipped layer covers all four (duration≈latency, agent-calls≈traffic, verdicts≈errors, tokens≈saturation) → minimally canonical.
- **Anthropic, "Effective evaluation of agents" (2025)**: ship small samples and iterate (≥20 queries) — partial cover for v1's deferred SOTA.

**Contradicting (load-bearing)**

- **Google SRE Ch.6 §As Simple as Possible**: *"Data collection… that is rarely exercised should be up for removal. Signals that are collected, but not exposed in any prebaked dashboard nor used by any alert, are candidates for removal."* → cuts directly against the upgrade entry's SOTA wishlist.
- **Google SRE Ch.6 §loose-coupling**: *"using web APIs for pulling summary data in a format that can remain constant over an extended period of time."* → cuts directly against the parser walking the undocumented Claude Code internal subagent JSONL layout.
- **Heilmeier Catechism (1975)**: *"What are the mid-term and final 'exams' to check for success?"* → upgrade entry's lifecycle row shows `value-proved: —`. No exam was named at ship time.

**Stub flags**: Nygard *Release It!*, Feathers *Working Effectively*, March 1991 — relevant authors named in canon inventory but not ingested. Reasoning that depends on them is authority-citation, not passage-citation.

## Scope-map summary

12 primitives mapped:

- **6 extend**: ledger schema (additive `## Metrics` block), 3 hook scripts, ledger-render skill, explain skill, settings.json hooks block, the 12-step workflow itself (gains a Heilmeier obligation under the candidate's original posture; dropped under the v2 candidate).
- **3 replace**: parser (eventually, conditioned on a stable host surface), `workflow-id.txt` prose handoff, regex pair (verdict + loop).
- **1 subsume**: schema doc — preserved because the same change-set updated it. **Frame-challenger objected** that "no drift surfaced" is unsupportable when zero completed sessions have populated `diagnostics/`. Honest call is `extend`, not `subsume`. v2 candidate accepts this.
- **1 conflict**: undocumented Claude Code transcript layout. Not owned by this repo; canon §loose-coupling says the parser "should not exist in its current form." v2 candidate accepts as transitional with a tripwire.

## Frame-level challenge and how the recommendation addresses it

The frame-challenger surfaced **workflow economics, not workflow observability**: for each metric the layer emits, name the workflow decision it changes; metrics with no named decision are removal candidates per canon §As Simple as Possible.

The v1 candidate took this seriously and produced a kill-or-defer table for `verdicts`, `duration_seconds`, `tool_calls`, `loops`. The panel rejected v1 not because the table was wrong but because the *organizing unit* was wrong (fields, not aggregate boundaries) and the *day-after-ship product surface* was net-negative.

The **v2 candidate** answers the frame-level objection differently: instead of pruning fields, **install a schema contract that forces every future field-decision to be explicit, and a synchronization contract that ensures the metrics actually reach a consumer**. The "workflow decision changed by metric" question moves from a one-shot synthesis judgment to a continuous discipline enforced by JSON Schema validation and `parser.lock` semantics. Fields stay collected; consumers gain or lose visibility based on the contract, not on a panel verdict.

## Post-critique recommendation

**Recommendation**: Land the v2 candidate ([candidate.v2.md](candidate.v2.md)) — schema contract (action 1) + synchronization-aware hook-exec wrapper (action 2) — **with three named patches that the loop-2 critics required and the cap-stop prevented from being absorbed into a loop-3 rewrite.**

Recommendation bullets:

- **Land action 1 (schema contract).** Add `<target>/.claude/schemas/metrics.schema.json` (JSON Schema draft-2020-12) with `tokens.total` and `tokens.by_agent` required, all other fields optional. Producer validates before write; consumers validate before read; consumer-side validation failure → silent-skip per existing missing-file policy. Update the explain skill's stub string to threshold-agnostic wording (`no diagnostics data yet — populates as data accumulates`) per product.v2 patch suggestion 10.
- **Land action 2 (wrapper + synchronization), patched.** `<target>/.claude/hooks/hook-exec.sh` with additive Phase A → Phase B rollout; Stop hook reorder so `rm -rf "$STAGING"` runs at parser tail. **Patch from architecture.v2 / operations.v2**: `parser.lock` is a *liveness* primitive, not presence-only — content is `{pid, start_ts}`; ledger-render's poll, on timeout, checks PID-alive and lock-age and emits distinguishable strings (`_parser-running-slow_` vs `_parser-crashed-stale-lock_`). **Patch from architecture.v2**: `metrics.json` write uses tmp-file + `os.rename` (POSIX atomic); schema requires `session_id`, `end_ts`, and `schema_version` as top-level fields; ledger-render checks that `session_id` matches the rendered session before consuming.
- **Specify the Phase A → Phase B promotion gate as an observable** per operations.v2: `git diff` shows no inline-redirect change between Phase A entry and cutover; staging hook log shows wrapper invocations at the expected count across ≥5 sessions. "≥5 sessions" without an observed property is a vibes check.
- **Add a deferred-items review cadence** per product.v2: ledger-render checks the deferred table on every invocation; if any tripwire condition has fired since last session, surface a one-line `_deferred-item-N tripped: <condition>_` in the ledger. The deferred table is reviewed mechanically, not by operator memory.
- **Resolve the schema-vs-parser version-skew rule** per operations.v2: parser writes per its native shape; consumers decide whether to silent-skip. A producer-side schema check that rejects the parser's own output is a bootstrap failure — the parser-side validation is for *catching its own bugs*, not for enforcing schema versioning. Schema versioning is a consumer-side responsibility (consumer reads `schema_version` field and compares to its own expected version; on mismatch, loud-skip with `_schema-skew-detected: parser=X, consumer=Y_`).

**Decisions in this synthesis** (countable per the README schema): 5 recommendation bullets + the uncertainties below.

## Named uncertainties

1. **Whether the parser's typical runtime exceeds the 2-second poll budget on real (non-dogfood) workloads.** If yes, loud-skip fires routinely; the synchronization contract pollutes ledgers; synchronous-parser-in-Stop becomes the cheaper choice. We have no evidence either way — the parser has never run on a real workflow. *Confidence: low.*
2. **Whether the host-layout drift tripwire fires reliably under operator pressure.** Architecture.v2 named the self-report classification problem ("operator ships a parser patch and forgets to classify it as layout-driven"). Without a mechanical detector — a CI check or pre-commit hook flagging touches to `find_transcript`/`find_subagents_dir` — the deferred-with-tripwire posture has a known leak path. *Confidence: medium-low.*
3. **Whether the `metrics.json` cross-session staleness boundary case (architecture.v2 §1a) is real or theoretical.** With per-session `diagnostics/<id>/` directories and atomic writes plus `session_id` field added per the recommendation, the named race is closed. But the architecture lens preferred the per-session-uuid isolation as the architecturally cheaper pattern; if the existing per-session routing has any leak path, the staleness window re-opens. *Confidence: medium.*
4. **Whether 6–8 hours is the realistic implementation budget.** Product.v2 estimated 6–8h vs. the candidate's 4.5h, factoring first-time JSON Schema discipline. The patches added in this synthesis (PID + start_ts in lock, tmp-file rename, deferred-items review cadence in ledger-render, schema versioning) push the budget further. The realistic figure is closer to **8–10 hours, likely two sittings**. *Confidence: medium.*
5. **Whether the operator runs ≥20 review-shaped sessions in the next 6 months.** Below this volume, averages and per-step timing are pre-empirical, and several deferred-table tripwires never fire because their re-entry conditions are session-count-driven. The deferral becomes a forever-deferral. *Confidence: medium-low — depends on operator usage patterns the panel has no evidence base on.*

## Cheapest experiment that would reduce the biggest uncertainty

The largest-leverage uncertainty is **#1 (parser runtime vs. 2-second poll budget)** because every other uncertainty is conditional on the synchronization contract working. Outside-view's cheapest-experiment recommendation is the right shape: **replay three pre-2026-05-09 session-artifact directories' transcript JSONL through the parser in isolation**.

Concrete:
- Sessions: `2026-04-27-critics-get-write-tool-impl` (complete workflow), `2026-04-25-sota-claude-online-research`, and one more named in [distillations/explore.md](distillations/explore.md).
- Measurements per replay: (a) does parser produce `metrics.json`? (b) what is parser wall-clock runtime? (c) does `tokens.total` equal `sum(tokens.by_agent)` within 5%? (d) do parsed verdict/loop counts match a hand-count?
- Cost: ~1 hour.
- Output: a single observation each on uncertainties #1, #3, and a partial signal on #2. If parser runtime is reliably <2s on the three replays, uncertainty #1 collapses; if any replay produces zero attribution silently, uncertainty #2 (modal failure) is empirically validated.

This experiment was named in the v1 candidate as action 3 and deferred in the v2 candidate as a tripwire. **The synthesis recommends running it** as part of the implementation pass, before the action-2 Phase A starts. Phase A's "≥5 sessions" gate becomes meaningful only against a parser that has been validated on non-dogfood data; the replay experiment is the cheapest way to do that.

---

## Triangulation note

`SHADOW_PANEL` was not set; no shadow lanes ran. Disagreement signal in this synthesis comes from the regular three-lens panel, with architecture and operations dissenting at loop-2 cap and product approving with patch suggestions. The disagreements are surfaced individually under "Named uncertainties" rather than collapsed.

---

Ledger: agent-calls=15, artifacts=23, loops=2/2; warnings: loop cap reached.
