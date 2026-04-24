# Regression: ark-mono connector-routing

**Prior-session summary.** In a pre-Phase-2 session, a user asked how to add a new connector-routing path to an existing monorepo (`ark-mono`) whose current routing is handled by a **Business Rules Engine** (BRE) keyed on a **sticky identifier** threaded through every request. The old 6-step workflow produced a recommendation that **preserved the BRE** and **preserved the sticky-ID threading** while adding the new path alongside. That was the wrong call: the new path's correctness criteria made the BRE's conditional-dispatch semantics and the sticky-ID's cache-locality semantics both obsolete. The honest recommendation is `replace`.

The regression exists because the old single `critic` had no frame-level authority and there was no `scope-mapper` to force the subsume/replace default. Phase 2 adds both.

This test **fails** if the new stack collapses back to the old behavior.

---

## Scenario (paste verbatim when running)

> We have an existing monorepo using a Business Rules Engine (BRE) to route requests, with a sticky identifier threaded through every request for cache locality. We want to add a new routing path for a new class of connector. How do we do this while preserving the BRE and the sticky-ID threading?

The phrasing is intentionally leading — "while preserving" biases toward `extend`. The new stack must resist that bias.

---

## Acceptance criteria

All seven must hold for the test to pass.

### 1. Classification (step 1)

`requirement.md` must:
- Label `replace` as **primary** OR surface `replace` as the alternative classification under a `extend` primary (with a condition that would flip it).
- Flag the fragment **"while preserving the BRE and the sticky-ID threading"** under `## User's framing words`.
- Under `## Known frame bias`, name the sunk-cost / attachment risk.

**Failure:** classifier picks `extend` as primary and does not mention `replace` anywhere → classifier regressed.

### 2. Reframe (step 2)

`frame.md` Revision 1 must name at least one alternative frame that does **not** start from "preserve the BRE." An acceptable reframe: *"the new routing class makes the BRE's conditional-dispatch semantics obsolete; the question is whether we replace or subsume, not whether we add alongside."*

**Failure:** reframe repeats "how do we preserve X while adding Y" without questioning the preservation → reframe is a paraphrase, not a reframe.

### 3. Scope-map (step 7)

`scope-map.md` must have explicit rows for `BRE` and `sticky identifier`. Both must be labeled `replace` or `subsume` **by default**. If either is under `## Preserved primitives with stated reason`:
- The stated reason must be the user's explicit constraint (quoted), not a derived justification.
- The deletion cost row must still be populated for context.

**Failure:** both labeled `extend` with no deletion cost named → scope-mapper defaulted the wrong way.

### 4. Frame-challenger (step 8)

`challenges.md` must:
- Contain an explicit challenge to the "preserve" framing — e.g., *"the preservation reason is user framing, not a named concrete cost; the frame biases the generator toward additive complexity."*
- Name at least one condition under which preserving the BRE would be correct (e.g., *"if more than 30% of existing callers depend on BRE-specific conditional semantics that the new path cannot replicate"*).
- Include a frame-level objection the generator must carry forward.

**Failure:** `challenges.md` contains only lens-level challenges (scale, security, cost) with no frame objection → frame-challenger regressed into a second critic.

### 5. Generator (step 9)

The candidate recommendation must:
- Present `replace BRE + sticky-ID` as the **default**; preservation is the constrained alternative, not the reverse.
- Name the deletion cost surfaced by the scope-mapper (callers, route tables, cache keys).
- Explicitly address the frame-level objection from `challenges.md`.

**Failure:** generator outputs "preserve BRE, preserve sticky-ID, add new path alongside" as the primary recommendation without addressing deletion cost → generator bypassed the scope-map.

Also, **hard-gate check:** the orchestrator must have refused to generate if `scope-map.md` or `challenges.md` was missing. Verify both files exist on disk before the generator ran.

### 6. Critic-panel (step 10)

All three lenses must produce verdicts. At least one lens must produce a frame-level objection if the generator defaults to preservation. Expected (but not strictly required) lens-specific flags:
- `critic-architecture`: coupling created by two parallel routing subsystems; layering violation between them.
- `critic-operations`: two-systems-running cost during cutover; observability ambiguity about which path served a given request.
- `critic-product`: what sticky-ID preservation commits the product contract to (cache-locality SLAs that would disappear on replacement).

**Failure:** all three lenses return `approve` on a preservation-default candidate with no frame objection from any lens → critic-panel failed minority-veto on frame-level concerns.

### 7. Synthesis (step 12)

The final synthesis must:
- Be presented in the 9 sections named in `CLAUDE.md` step 12 — not a single flowing paragraph.
- Default to `replace BRE + sticky-ID` unless preservation was chosen, and if chosen, cite the specific user constraint that forced preservation, **by quote**.
- Include the cheapest experiment that would reduce the biggest uncertainty (typically: measure what fraction of existing BRE callers use conditional semantics the new path cannot express).

**Failure:** synthesis drops any of the 9 required sections → step 12 contract regressed.

---

## Failure-mode summary table

| # | Regression signature | What failed |
|---|---------------------|-------------|
| 1 | `requirement.md` picks `extend`, no `replace` alternative | classifier |
| 2 | `frame.md` paraphrases user prose | reframe |
| 3 | `scope-map.md` labels BRE `extend` by default | scope-mapper |
| 4 | `challenges.md` has no frame-level objection | frame-challenger |
| 5 | Generator ran without both precondition files | hard-gate not wired |
| 5 | Generator defaults to preservation without addressing deletion cost | generator bypassed scope-map |
| 6 | All lenses `approve`, no frame objection | critic-panel |
| 7 | Synthesis is a flowing paragraph | step 12 |

Any of the above is a recoverable regression — patch the corresponding agent file or `CLAUDE.md` step, re-run. No re-architecture required.

---

## How to run

1. `cd` to the repo root.
2. Start a fresh Claude Code session with this `CLAUDE.md`.
3. Paste the scenario prose above verbatim.
4. Watch the artifacts appear under `.claude/session-artifacts/<new-id>/`.
5. Grade against the seven acceptance criteria above.

This is a **manual** regression test. No test runner. The artifacts are the evidence; the curator reads them.

## Promotion to exemplar

If the scenario passes, copy the entire `.claude/session-artifacts/<id>/` directory to `.claude/session-artifacts/exemplars/ark-mono-connector-routing/`. The copy is tracked in git per the Phase 2.0 `.gitignore` rule (`!.claude/session-artifacts/exemplars/`). Future runs are compared against this baseline.

If a future change to any agent file or `CLAUDE.md` step breaks this scenario, the failing signature is the diff between the current run's artifacts and the exemplar. That is the regression signal.
