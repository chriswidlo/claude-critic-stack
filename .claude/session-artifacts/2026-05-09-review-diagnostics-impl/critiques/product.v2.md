# Product-lens critique v2 — review-diagnostics-impl (loop 2 of 2)

## Opening dissent

The rewrite earns its rework verdict on every loop-1 objection that bound. The catalyst question stays a live surface; the dashboard tells the truth instead of lying with a synthetic average; seven actions collapsed to two; Heilmeier's industrial clock is gone; dogfooding-as-confounder is dropped. What remains to push on is narrower: the stub-string wording leaks an internal threshold ("3 sessions") to the operator surface, and the deferred-with-tripwire posture quietly recreates the seven-action backlog under a different name unless someone *reads* the deferred table. Both are correctable in-place; neither is unshippable.

## 1. User-visible consequence

Day-after-ship, the operator opens `/explain` and the duration card reads `no diagnostics data yet — populates after 3 sessions` instead of `~10 min`. That is the smallest, most-visible product surface in the rewrite, and it is now honest. The `## Metrics` block in `ledger.md` keeps `verdicts` and `duration_seconds`. After ≥3 review-shaped sessions, the card flips to a real number; the catalyst question begins answering itself in trajectory.

A second visible consequence: the ledger may, on rare sessions where the parser exceeds the 2s bound, render `_parser-still-running at ledger-render time_`. That is a new operator-visible string. It is loud-skip by design, and the operator should *want* to see it the first time it appears. It does become noise if it fires often.

## 2. Commitments implied

The schema contract is the load-bearing commitment. Once `metrics.schema.json` exists and consumers validate against it, the schema is the authoritative shape; future fields require schema edits before producer or consumer can use them. The rewrite correctly flags this as a commitment rather than a doc note. Reversing it later means breaking consumers — that is the right amount of weight for a contract.

The `parser.lock` sigil is a second contract: it is now a documented synchronization primitive between two processes. Removing it later is a behavior change, not a refactor.

The deferred-table re-entry conditions are *softer* commitments — they are tripwires the operator is committing to honor *if seen*. Their force depends on the operator actually noticing them.

## 3. Migration burden

The rewrite estimates ~4.5 hours. Realistic figure for a solo operator unfamiliar with JSON Schema discipline, including context-switching: **6–8 hours, likely spread across two sittings**.

- Schema authoring + validating against an existing `metrics.json` sample: 1.5h is plausible *if* JSON Schema is already familiar; add 1–2h for first-time learning curve and `jsonschema` library install/vendor decision.
- Phase A logging: ≥5 sessions of operator dogfooding before Phase B. Wall-clock cost is ~zero per session but calendar drag is real — Phase B may sit waiting for a week if the operator runs sparsely.
- Stop-hook reorder + `rm -rf "$STAGING"` move to parser tail + ledger-render bounded poll: nontrivial because three files must change in coordination, and a misordered edit silently leaves the race in place.

## 4. Product affordances — better and worse

**Better:**

- The dashboard becomes honest. `~10 min` (false confidence) → `populates after 3 sessions` (forecast).
- Catalyst question stays answerable in trajectory.
- Schema-conformant `metrics.json` affords future skills without re-discovery.
- Loud-skip is a *new affordance for the operator*: synchronization failures become visible rather than silent.

**Worse / pruned:**

- The operator must now read a deferred-items table and remember tripwires. If they don't, the deferred items become a hidden backlog.
- First-time JSON Schema overhead is real.
- The "3 sessions" number is now load-bearing on an operator-facing string.

## 5. Frame-level objection

**The deferred-with-tripwire posture is honest only if the tripwires are *reviewed*, not merely *armed*.** The rewrite frames deferral as "if a tripwire fires, the item re-enters; if no tripwire fires for six months, the item was correctly deferred." That is a clean accountability story *if* there is a moment at which the operator looks at the table. The rewrite does not specify that moment. Nothing in the proposal forces the operator to ever re-read the deferred table after this synthesis ships.

This is the seven-action backlog re-emerging in a different shape: ten deferred items with named conditions, no scheduled review, and reliance on the operator's memory to notice when a condition fires. The product-shaped fix is to specify a *deferred-items review cadence* — either tied to a real event (every Nth session, or on the next workflow change), or built into the upgrade-entry lifecycle (the entry is not "closed" until the deferred table is walked). Without that, the rewrite has half-traded a backlog for a hidden backlog.

A secondary frame-level note: **the stub string leaks an internal threshold to the operator surface.** "3 sessions" matches the explain skill's existing `≥3 sessions` threshold. The operator does not need to know that number; it is internal mechanism. Threshold-agnostic wording — `populates as data accumulates` or `populates after a few sessions` — would not commit the dashboard to a specific count and would not need to change if the threshold is later tuned.

## Direct answers to the stress questions

1. **Stub wording.** "3 sessions" leaks an internal threshold. Prefer `no diagnostics data yet — populates as data accumulates` or `no diagnostics data yet — needs a few more sessions`. If the operator runs sparsely, they will read this string for *weeks*, not days. Threshold-agnostic wording reads as forecast-shaped at any cadence.
2. **Two actions vs. one.** Two is the load-bearing minimum. Action 1 without action 2 leaves the AI-blindness invariant unstressed and the silent-skip-as-fallback failure mode in place. Action 2 without action 1 leaves drift between producer and consumer ungated. They are coupled; cutting either drops a binding loop-1 objection.
3. **Deferred-with-tripwire posture.** Honest deferral only if reviewed. Currently it's a hidden backlog with armed tripwires and no review cadence. Recommend the rewrite specify either (a) a per-session check ("when ledger-render runs, if any deferred-table condition has fired since last session, surface it"), or (b) a cadence tied to upgrade-entry lifecycle ("the entry is not closed until the deferred table is walked once").
4. **Migration burden.** ~4.5h optimistic. 6–8h realistic, likely split.
5. **Catalyst question's current-state answer.** Stays partial. The rewrite preserves `duration_seconds` collection and rendering; per-step breakdown waits for ≥20 sessions. From a product lens, **acceptable** — because the *trajectory* now points at the catalyst question being more answerable over time, not retired.
6. **Day-after-ship operator experience.** Net-neutral to slightly net-positive. The dashboard tells the truth (+). The catalyst question is preserved (+ vs. v1 minus). The operator must edit five files and sequence Phase A→B (cost). The deferred table sits unread unless the rewrite specifies otherwise (cost, latent).
7. **What did the rewrite miss?** The stub-string threshold leak and the absent deferred-items review cadence. Both correctable in-place, neither structural.

## 6. Verdict

**approve**

Leading indicator to watch: **the loud-skip rate in `## Metrics`**. If `_parser-still-running at ledger-render time_` fires more than once in the first 10 post-ship sessions, the synchronous-parser-in-Stop alternative (assumption #3 flip condition) is the cheaper choice and the rewrite's lock-sigil pick was wrong. If it fires zero or once, the synchronization contract is sound.

Second leading indicator: **whether the operator references the deferred table unprompted within the first 5 post-ship sessions**. If they do, the table is doing its job; if they don't, the deferred-items review cadence gap is real and should be patched before another deferred-heavy proposal lands in this stack.

What would have flipped this to rework: any one of (a) the stub string still reading as apology rather than forecast, (b) the deferred posture replacing seven ranked actions with ten armed tripwires *and no review cadence whatsoever*, or (c) the catalyst question being retired rather than preserved. None tripped; the rewrite is shippable.

Synthesis should carry forward the two patch suggestions (stub-string threshold leak; deferred-items review cadence) as named uncertainties rather than re-opening loop 3.
