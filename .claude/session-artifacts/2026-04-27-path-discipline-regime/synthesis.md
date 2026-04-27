# Synthesis — path-discipline regime

The 12-step workflow consumed 2 of 2 loop budget. Loop 1 vetoed at frame; loop 2 approved with advisory notes. This is the post-critique synthesis.

## Classification

**Primary label:** `refactor`. **Alternative classification:** `replace` — would be primary if the operator picks Option B or C. The classifier flagged a frame bias to watch: refactor framing tends to smuggle behavior changes under "just cleanup."

## Reframe (current revision)

**Frame Revision 2 (active):** *"Decide the smallest concrete action on path-discipline that (a) does not trap the repo into a substrate-by-precedent it hasn't designed, (b) preserves the privacy + grep-stability properties currently working, (c) addresses the 9-vs-9 compliance gap with a mechanism that survives base-rate scrutiny, and (d) names what would have to be true for a future gate-substrate decision to overturn this one."*

This superseded Revision 1 ("which option A/B/C/D enforces clause 2 best") after loop 1's convergent veto reframed the question from *enforcement* to *substrate*.

## Reference-class forecast

Solo-maintainer style rules without automated enforcement: ~30% are still complied-with at 6 months from a 50/50 baseline. Mode is drift to lower compliance. Going *with* the natural authoring grain lifts compliance to 70-85%. **Loop-1 candidate forecast: ~35% success.** **Loop-2 candidate forecast (do-less + audit): not directly forecastable — succeeds tautologically because it commits to almost nothing; the question becomes whether the substrate decision it defers gets made later under data instead of intuition.**

## Canon — supporting and contradicting

**Supporting Option A modified (loop 1) and Option Zero modified (loop 2):**
- Anthropic *Building Effective Agents*, Appendix 2 (SWE-bench): pick the path style that's mechanically reliable for the tool, then enforce it.
- *Google SRE Book* §Consistency: 50/50 compliance is the failure mode automation exists to dissolve.

**Contradicting:**
- Anthropic *Building Effective Agents* (lines 231-237): keep format close to what the model has seen naturally; avoid formatting overhead. **Cuts toward Option B** (file-relative; go with the grain).
- Anthropic *Effective Context Engineering* (line 51): brittle hardcoded prose logic creates fragility. **Wrong-reason prose rule is the smell described.**
- *SRE Book* (line 3489): unenforced artifacts are time bombs. **Documentation-only fix is worse than no rule.**

**Canon coverage was partial.** Fowler, Beck, Feathers (refactoring discipline / convention drift) are stubs without source.txt. Hunt-Thomas (broken-windows analogy) is not in the corpus at all. **Recommendation:** ingest these for future runs; they would have sharpened the decision.

## Scope-map summary

12 primitives mapped. Key calls:
- Clause 2 of the rule: labelled `replace`, not `extend`. (Frame-challenger pushed back on this in loop 2 challenge §1.)
- The 9 file-relative violators: split-labelled (`replace` for active surfaces, `extend` for the 2 session-artifact files preserved by the longitudinal-record contract).
- Three preservations had stated reasons: privacy clause (a), consent boundary (d), longitudinal-record contract. Frame-challenger challenged all three.
- Empty-cell on pre-commit hooks: no existing primitive. Loop 1 candidate would have introduced one; loop 2 declines.

**Unresolved conflict:** the longitudinal-record contract from commit `5108ed3` had never been adjudicated against a real test case. This question was the first. Loop 2 candidate respects the contract by leaving session-artifact files untouched. The contract's *boundary* — what counts as "style" vs "privacy" — remains the operator's call, not adjudicated by a quoted rule.

## Frame-level challenges, and how the candidate addresses them

The frame-challenger raised six challenges across two loops. The post-critique recommendation addresses them as follows:

| Challenge | How v2 addresses it |
|---|---|
| Loop 1 §1 — rule is mis-located, not mis-worded | Acknowledged; named as a substrate-free follow-up (architecture lens loop-2 advisory: relocate clause 2 prose to authoring surfaces as a separate move). |
| Loop 1 §3 — preservation challenges to (a), (d), and "non-negotiable" status | Privacy clauses preserved as load-bearing; "non-negotiable" treated as evidence of attachment, not constraint; the candidate's "do less" stance neutralises the over-protection concern. |
| Loop 1 §5 — slash-command-patch is soft | Conceded. v2 ships *no* slash-command patch — the soft fix is removed. |
| Loop 1 §6 — honesty meta-challenge | Conceded explicitly in the candidate body. Operator-position statement (item 9) added to anchor against orchestrator drift. |
| Loop 2 §1 — Revision-2 frame is itself a frame error | The smallest-action test (5-min reversible, no future-contract commitment, justified on own terms) is satisfied. |
| Loop 2 §2 — steelman Option Zero | This candidate IS Option Zero, modified. |
| Loop 2 §3 — steelman Option Negative (delete clause 2) | Considered. Deferred until 30-day audit data is in. |
| Loop 2 §6 — workflow-as-wrong-tool | Captured as a separate upgrade entry naming the meta-finding. |

## Post-critique recommendation (labelled)

**Take the smallest action that fixes the factual error and buys data:**

1. **Edit [`CLAUDE.md`](CLAUDE.md):16.** Replace reason (c) with: *"keeps internal references stable across moves and grep-discoverable as a single canonical token (links of this form display as text addresses and may not click-navigate from subdir-relative renderers — navigation is via file tree or grep)."* One-line edit. Reversible in 30 seconds.

2. **Open one upgrade entry** at [`upgrades/profound/2026-04-27-does-this-stack-need-a-gate-substrate/`](upgrades/profound/2026-04-27-does-this-stack-need-a-gate-substrate/). Tier: profound. Title phrased as a question (per architecture-lens loop-2 advisory), not a spec. Body includes the loop-1 architecture critique as catalyst. State: 🌱 created.

3. **Open one upgrade entry** at [`upgrades/normal/2026-04-27-workflow-overruns-on-housekeeping/`](upgrades/normal/2026-04-27-workflow-overruns-on-housekeeping/) capturing the meta-finding from challenge §6 — running the full 12-step on a housekeeping question cost 2 critic loops + 6 subagent invocations to arrive at "do less." This entry feeds back into a future workflow-routing decision.

4. **Anchor the T+30 audit** by writing a dated line into [`.claude/session-artifacts/2026-04-27-path-discipline-regime/decision-log.md`](.claude/session-artifacts/2026-04-27-path-discipline-regime/decision-log.md): *"audit due 2026-05-27"* (per operations-lens loop-2 advisory). Next workflow scan picks it up.

5. **Operator-position statement.** The operator must write — in this synthesis or in the gate-substrate entry's body — one of:
   - *"I accept the wait. Punch-list items 2 and 3 stay blocked for 30 days while I gather data."*
   - *"I disagree, ship more."* — re-runs the workflow with the operator's chosen heavier action.
   - *"I disagree, ship less."* — drops even the prose edit; do nothing.

   Silence is not an accepted response (per product-lens loop-2 condition for approve).

6. **Do NOT** patch `/upgrade`. Do NOT patch the three Write-capable agents. Do NOT ship a hook. Do NOT sweep the 7 active-surface violator files. Do NOT edit the 2 session-artifact files. **The active inaction is the recommendation.**

7. **Punch-list correction.** Update [`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md) item 2 to exclude session-artifact files from the depth-fix scope (they are protected by the longitudinal-record contract from commit `5108ed3`).

## Three named uncertainties

1. **Does the 30-day audit actually fire?** Outside-view base rate says solo-maintainer audits forget. The dated decision-log entry is a soft mitigation; the operator-position statement is another. Neither is a real scheduler. If the audit slips to T+60 or never, the deferral collapses into permanent Option Zero.

2. **Does the lab pattern (file-an-entry-when-stuck) become substrate-by-stealth?** Architecture lens loop-2 flagged this. v2 opens *two* entries in the loop where it concludes "do less." If this becomes the orchestrator's default move on every loop, the lab is the new gate-substrate by accident.

3. **Was the operator's lean toward Option A actually right and the workflow talked them out of it?** Product lens noted 30% externalisation in the operator-position statement. The trajectory (preserve+enforce → defer-substrate → defer-everything) is a 180° flip on enforcement strength executed by the orchestrator without the operator stating they changed their mind. The operator may want Option A back after seeing this synthesis. That is a legitimate response.

## Cheapest experiment that reduces the biggest uncertainty

**Run the Explore audit script at T+30** (date 2026-05-27). Inputs: same author-class taxonomy as the loop-1 distillation. Outputs: violation rate per author class. Cost: one Explore invocation (~5 minutes of agent time).

This experiment reduces uncertainty #1 directly and #2 partially. It does not address #3, which is decided by the operator's response to this synthesis.

## Honest meta-finding

The full 12-step workflow run on a housekeeping question (one factually-wrong word in CLAUDE.md) consumed two critic loops, nine subagent invocations, ~25 KB of artifacts, and arrived at *"correct the factual error and gather data."* The intuitive call would have arrived in 5 minutes. This is captured as its own upgrade entry, not absorbed into this run's recommendation. **The workflow self-repaired** — it caught the orchestrator's three-position drift, vetoed an over-shipped first candidate, and forced the smaller correct answer. **The cost of self-repair was disproportionate to the problem.** Both findings are real.
