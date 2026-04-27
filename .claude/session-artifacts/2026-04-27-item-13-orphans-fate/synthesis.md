# Synthesis — item 13 (orphans fate)

Session: `2026-04-27-item-13-orphans-fate`. Routed through the full 12-step workflow with one critic-rewrite loop. Final critic verdict: 3-of-3 approve.

---

## 1. Classifier label

**Primary:** `new` — because the user's two-layer ask explicitly invited a *standing policy* (a new lifecycle primitive for "expired-utility documents"), and that policy layer was a candidate new primitive.

**Alternative classification:** `refactor` — would have been primary if the user conceded no new primitive was needed and the task reduced to "move/delete four files without changing what the repo can do." The pipeline's outcome ended up closer to refactor (one tiny named primitive + four file-system actions; no policy promoted to CLAUDE.md), confirming the alternative classification carried real weight.

The classifier's flagged frame bias — "over-designing the policy before evidence" — was the load-bearing risk and proved real: v1 of the candidate did over-design (CLAUDE.md amendment + implicit primitive); the critic-panel caught it; v2 corrected.

## 2. Reframe (final revision)

**User's framing:** "Wire-in, archive, or delete each of these four orphans."

**Reframe:** "Are these four orphans the same kind of thing? If yes, what minimum primitive lets the repo distinguish 'live reference' from 'frozen evidence' without inventing a new lifecycle? If no, on what axis do they differ — and does that axis already have a venue?"

The reframe surfaced that the four orphans are *not* the same kind of thing — three different shapes (failed-to-bootstrap primitive, frozen evidence, shipped-design-record) plus one entangled-with-another-item case. That non-uniformity is the key fact the per-orphan dispositions track.

Implicit user optimization: tidy repo + low future maintenance.
Alternative optimization considered: cheap reversibility of past judgment (orphans as frozen evidence, not cruft). The final recommendation lands closer to *both* — tidy by deleting truly-expired artifacts (O1, O2), reversible-by-evidence by retaining O3 in place with a header.

## 3. Reference-class forecast (from outside-view distillation)

- **Class:** solo-maintainer R&D repos < 2 years old, performing a first or second janitorial sweep on documentation. N=4 orphans.
- **Base rates (qualitative):** ~5–10% of such repos institute a formal lifecycle primitive on first sweep; ~80–90% go ad-hoc.
- **Failure mode of formal-lifecycle path:** policy doc itself becomes an orphan (Gall's Law inverse). **Failure mode of ad-hoc path:** inconsistency surfacing at second sweep, ~bounded re-decision cost.
- **Position relative to base rate:** at base rate for ad-hoc success, slight tilt toward "policy might stick here" due to maintainer's process-inclination — tilt insufficient to overcome Rule of Three.
- **Verdict from outside-view (verbatim):** *"Below base rate for option (a) (new lifecycle primitive); at base rate for option (b) (ad-hoc)."*

The final v2 candidate honors this by introducing one tiny named primitive (`<dir>/RETIRED.md`) rather than a full lifecycle policy — splits the difference between the two extremes the outside-view scored.

## 4. Canon passages (supporting and contradicting)

**Supporting "no new primitive / minimal-primitive" position (Position A):**
- Anthropic, *Building Effective Agents*, 2024: *"we recommend finding the simplest solution possible, and only increasing complexity when needed … [Frameworks] often create extra layers of abstraction … make it tempting to add complexity when a simpler setup would suffice."*
- Anthropic, *Effective Context Engineering*, 2025: Claude Code uses CLAUDE.md up front plus glob/grep just-in-time, *"effectively bypassing the issues of stale indexing … 'do the simplest thing that works' will likely remain our best advice."*
- Anthropic, *Building a Multi-Agent Research System*, 2025: scaling rules embedded to prevent *"overinvestment in simple queries, which was a common failure mode in our early versions."*

**Contradicting (Position B — write the policy down now, ADR-style):**
- Google SRE book, 2016, Ch.5: systems engineering is *"configuring production systems, modifying configurations, or documenting systems in a way that produces lasting improvements from a one-time effort."* — read against Position A: a small policy is worth writing if there is any chance it recurs.
- Anthropic *Effective Context Engineering* (2025) **read against itself**: praises glob/grep precisely because they are *named, stable primitives* that avoid stale indexes — so the same passage that argues against new maintained abstractions also argues *in favor* of having stable named primitives at all.

**Critical corpus gap acknowledged:** the four highest-value sources for this question (Fowler refactoring, Nygard *Release It* / 2011 ADR essay, Beck TDD, Feathers legacy code) are all stubs. Position B has no ingested primary-source quote — only the SRE proxy. The librarian flagged this as asymmetric support; the recommendation does not over-weight Position A on that ratio.

## 5. Scope-map summary and unresolved conflicts

| primitive | relationship | notes |
|-----------|--------------|-------|
| O1 — five-pressures.md | replace | 12-step partly absorbs; one pressure (#2) genuinely uncovered (frame-challenger correctly flagged as un-defended in v1). |
| O2 — ultraplan-next-level.md | replace | Frozen evidence; its outputs already in-tree as the punch-list and per-item plans. |
| O3 — ok-cool-this-is-warm-balloon.md | replace (v1) → preserved-with-header (v2) | Frame-challenger's "alternatives-not-taken" preservation argument carried; v2 keeps the file in place. |
| O4 — exemplars/ | conflict | Entangled with item 5; deferred with self-acting fallback. |
| P — standing policy | subsume | No CLAUDE.md amendment; one tiny named primitive (`prompts/RETIRED.md`) instead. |

**Unresolved conflicts:**
- **O4 ↔ item 5** dependency. Bounded by v2's footer fallback ("if item 5 abandons the promotion mechanism, delete `exemplars/` then"), but item 13 cannot fully close until item 5 lands.

## 6. Frame-level challenge and how the recommendation addresses it

**Frame-challenger's load-bearing objection:** *"Git history is a venue for recovery, not discoverability; deletion silently degrades the ability to answer 'why' six months later."*

**v1's response (rejected by all three critics):** substitute session-artifact directory for git as the discoverability venue. The architecture critic correctly named this as a **nameless primitive** — paying the full cost of a new convention while denying it was one. Product critic called it a **circular discoverability claim**. Operations critic called it a **structurally impossible rollback** ("you cannot revert what you do not remember to revert").

**v2's response (approved by all three critics):** name the primitive explicitly as `<dir>/RETIRED.md` — a 5-line breadcrumb file co-located with the deleted artifacts. Path-keyed discoverability where readers naturally look. The frame-challenger's premise is accepted; the consequence is paid honestly with one named convention rather than smuggled in implicitly.

**Loop-2 architecture critic's residual frame flag (carried, not blocking):** *primitive vs precedent.* `RETIRED.md` is shipped as a one-shot precedent but written up as a primitive with a 5-rule contract. Pick one. The recommendation below leans precedent — see uncertainty #1.

## 7. Post-critique recommendation

**Five concrete actions, one commit, no CLAUDE.md amendment, one named new primitive (`prompts/RETIRED.md`).**

| # | action |
|---|--------|
| 1 | `git rm prompts/five-pressures.md` (O1) |
| 2 | `git rm prompts/ultraplan-next-level.md` (O2) |
| 3 | Prepend a one-line `> **Status:** shipped 2026-04-24, retained as design-record (alternatives-not-taken).` to [plans/ok-cool-this-is-warm-balloon.md](../../../plans/ok-cool-this-is-warm-balloon.md). **No rename.** (O3) |
| 4 | Create [prompts/RETIRED.md](../../../prompts/RETIRED.md) — 5-line breadcrumb listing the two deletions with rationale + commit SHA placeholder. (P) |
| 5 | Update [plans/2026-04-27-item-07-residual-agents-md-refs.md](../../../plans/2026-04-27-item-07-residual-agents-md-refs.md) with a one-line note that `prompts/ultraplan-next-level.md` is gone (the AGENTS.md `(if present)` guard scenario evaporates). *Operations critic asked this be a row in the action table — promoted from narrative.* |
| 6 | Append `✅ done 2026-04-27` to punch-list item 13 with footer: *"O1, O2 deleted in commit `<sha>`; O3 retained-with-Status-header; O4 deferred to item 5 with self-acting fallback (if item 5 abandons the promotion mechanism, delete `exemplars/` then)."* |

**Pre-merge falsifier (commit-time, memory-independent):** open a fresh Claude Code session in this repo post-commit and ask: *"Did this repo ever have a checklist called 'five-pressures'? If so, why was it removed?"* Pass = answered in <2 minutes via `ls prompts/` → `cat prompts/RETIRED.md`. Fail = retroactively add a one-line CLAUDE.md note pointing future sessions at `RETIRED.md`.

**Out of scope explicitly:** no CLAUDE.md amendment; no `archive/`/`attic/`/`plans/shipped/` directory; no pre-emption of item 5; no `prompts/RETIRED.md` enforcement venue (agent, lint, test).

**This recommendation is labeled post-critique** — it is the v2 candidate, approved 3-of-3 by the critic-panel after one rewrite loop driven by 3-of-3 rework verdicts on v1.

## 8. Named uncertainties (≥3)

1. **Primitive vs precedent.** `prompts/RETIRED.md` is shipped as a one-shot precedent but documented as a primitive with a 5-rule contract. If the repo never has another sweep that empties a directory, the contract is over-engineering for N=1. If sweeps recur, the contract needs an enforcement venue (CLAUDE.md note, agent, or lint) — which v2 explicitly refuses to add. The honest read is that we are *betting on precedent* (one-shot use is sufficient), and naming it as a primitive is generous to the convention. Open question to the maintainer: is this a primitive or a precedent? Pick deliberately.

2. **Pressure-#2 gap in 12-step.** Confirmed by grep: CLAUDE.md step 9 + CLAUDE.md:62/74 require ≥3 *uncertainties* and ≥3 *flippable assumptions*, but do not require ≥3 *candidate solutions*. Five-pressures pressure #2 ("Enumerate-before-select: list ≥3 candidate solutions before recommending one") is the one item not redundantly covered. v2 dropped the CLAUDE.md amendment to avoid the bait-and-switch — this leaves the gap unaddressed. If a future critic-architecture review flags a candidate for under-enumerating alternatives, this decision was wrong (recoverable: re-open as its own session; `git show <sha>:prompts/five-pressures.md` recovers source).

3. **Sibling-session falsifier requires the maintainer to actually run it.** The test is concrete and runnable, but if it is skipped at commit time, v2 ships untested. This is itself a contract (the maintainer commits to running the test before merge). Mitigation: cheap (one extra prompt). But not free.

4. **O4's deferral may stall.** Item 13 closes with a self-acting fallback ("if item 5 abandons the mechanism, delete `exemplars/` then"), but if item 5 *also* defers (or stalls), `exemplars/` becomes the smallest possible orphan-of-orphans. Item 5's session is already in flight ([2026-04-27-ark-mono-phantom-fixture](../2026-04-27-ark-mono-phantom-fixture/)); risk is bounded but not zero.

5. **Sweep cadence assumption.** Outside-view's base-rate calculus (option a below threshold) assumed first sweep. Multiple 2026-04-27 session-artifact directories exist — that is one *sweep day*, not necessarily one *sweep cadence*. If a sweep happens within 6 months, option (a) (formal policy) moves toward base rate and "no rule" loses its strongest argument. The recommendation tolerates one more sweep without policy; if sweep #3 happens within a year, re-open the policy question.

## 9. Cheapest experiment (reduces the biggest uncertainty)

**The sibling-session test, run at commit time.** Open a fresh Claude Code session post-commit and pose the question above. Cost: one prompt, ~2 minutes. Reduces uncertainty #1 (primitive vs precedent — if the breadcrumb is discoverable in <30s, the precedent is sufficient and no enforcement venue is needed) and uncertainty #3 (the test itself; running it discharges the contract).

This is the cheapest experiment because (a) it requires no calendar mechanism, (b) it produces a binary observable signal, (c) the failure-mode remediation (one CLAUDE.md note) is cheap and additive, and (d) it discharges the falsifier contract immediately — there is no 6-month lag where the recommendation ships untested.

---

## What this synthesis does not do

- Does not execute the recommendation (per the approach plan, this session's job ends at recommendation; acting is a separate step requiring the maintainer's explicit go-ahead, especially since two `git rm`s are involved).
- Does not pre-empt item 5's session.
- Does not promote `<dir>/RETIRED.md` to a load-bearing CLAUDE.md convention; it ships as a precedent with the maintainer's option to formalize later.
