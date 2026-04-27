# Candidate v2 — path-discipline regime

## Position

**Option Zero modified.** Do less. Specifically:

1. **Reword reason (c) in [`CLAUDE.md`](CLAUDE.md):16** to describe what clause 2 actually provides (stable, grep-discoverable text address; click-navigation is via file tree, not link). One-sentence edit. Reversible.
2. **Do not patch [`.claude/commands/upgrade.md`](.claude/commands/upgrade.md).**
3. **Do not patch the three Write-capable agents.**
4. **Do not ship a `PostToolUse` hook.**
5. **Do not retroactively sweep the 7 active-surface violator files.**
6. **Do not edit session artifacts.**
7. **Re-run the Explore compliance audit at T+30 days.** Same script, same author-class breakdown.
8. **Open one new upgrade entry** at [`upgrades/profound/2026-04-27-gate-substrate-spec/`](upgrades/profound/2026-04-27-gate-substrate-spec/) named "Gate-substrate spec — what kind of policy primitive does this stack support" with the loop-1 architecture lens's frame-objection as its catalyst. Tier: profound (it's a substrate decision). State: 🌱 created.
9. **Operator-position statement (required, per loop-2 challenge §5):** the operator confirms in writing — in the upgrade entry's body or a one-line decision-log entry — *"I am choosing to wait on the substrate decision until I have 30-day data, and I accept that punch-list items 2 and 3 remain blocked during this window."* If the operator cannot or will not write that statement, the candidate is wrong and the workflow should escalate to synthesis-with-disagreements.

## Why this is what loop 1 was missing

Loop 1 shipped a hook + slash-command patch + agent-prompt patches + sweep + 14-day audit + agent contract + rejection-message UX + rollback path. Six of those are *substrate primitives* this repo has never had. Loop-1 candidate was inventing six primitives in one shot, dressed as "fix the rule." All three lenses noticed.

**Candidate v2 ships zero new primitives.** Reason (c) is a one-line prose correction that replaces a factually-wrong sentence with a factually-correct one. Reversible in 30 seconds. Commits to no contract, no surface, no precedent.

## Addressing the convergent frame-level objection

> "The candidate is solving the wrong problem at the wrong altitude. This is a substrate / change-management / contract decision."

Accepted. The substrate decision is correctly the question — and it's bigger than this run can settle. **Loop 2's response to that frame is to refuse the substrate decision now**, name it explicitly as a follow-up (item 8 above), and gate the substrate decision on data we don't yet have (the 30-day audit).

## Addressing each loop-2 challenge

**§1 — Revision-2 frame is itself a frame error.** Conceded. The Revision-2 frame said "ship something small and name the substrate as a follow-up." The challenge: "smallest action" is itself a substrate decision when the small action is a hook/script/bypass-contract. **Candidate v2's small action is a one-line prose edit, not a hook or a script or a contract.** The smallest-action test from challenge §4 — *5-minute reversible, no future-contract commitment, justified on own terms* — is satisfied: prose edit is reversible, commits to no future contract, justified by "the existing reason is factually wrong; correcting a factual error is its own justification."

**§2 — Steelman Option Zero.** This candidate IS Option Zero, modified to also fix the factual error in reason (c). The case: the rule has produced **zero measurable harm** (Explore §7: zero `/Users/` leaks, zero broken-link complaints in the operator's recorded sessions). 50/50 compliance is information, not damage. Acting on a signal that has produced no harm risks introducing harm to fix a phantom. The cheapest correct response to a 50/50 split that has produced no harm is to *measure for longer* before deciding.

**§3 — Steelman Option Negative.** Considered. Deleting clause 2 entirely is the cleanest reduction of CLAUDE.md surface; it retires the debate. The case for it: the rule's strongest defenders (privacy, grep-stability) survive in clauses 1, 3, 4, 5; clause 2 is style, and the cost of removing it is zero unless someone can name a concrete capability lost. **Candidate v2 does not delete clause 2 because a 30-day compliance audit produces the data that decides this.** If the audit shows compliance worsening AND no harm from the worsening, Option Negative becomes the correct follow-up. If the audit shows compliance recovering naturally (e.g., new authoring sessions trend repo-root because the AI saw the rule on its second read), the rule earns its keep. Both branches exist; v2 declines to choose.

**§4 — Smallest-action test.** Stated above. Reversible: yes (one-line prose revert). No future-contract commitment: yes (no hook, no patch, no sweep). Justified on own terms: yes (correcting a factual error is its own reason).

**§5 — Deepened honesty meta-challenge.** Conceded. The orchestrator (me) has executed three positions in three loops:
- Plan (pre-workflow): preserve rule, fix reason (c), patch slash command — **moderate enforcement**.
- Loop 1 candidate: preserve rule, fix reason, patch slash command + 3 agents + ship hook + sweep — **maximum enforcement**.
- Loop 2 candidate (this): preserve rule, fix reason, do nothing else, measure — **minimum enforcement**.

That's a 180° flip on enforcement strength executed without explicit operator statement. The frame-challenger called this out as defensive reframing. **The honest read:** I responded to each round of critique by choosing whichever shape avoided the prior round's veto, and the trajectory is toward less action because each veto came with a "you're shipping too much" sub-message. The workflow did its job — it talked the orchestrator out of premature commitment — but the cost is the orchestrator looks weather-vane-y. The mitigation: I am explicitly stating that v2 is *minimum enforcement on purpose*, not as drift, and I am asking the operator (item 9 above) to make their own position statement so the decision is anchored to operator intent, not orchestrator drift.

**§6 — Workflow-as-wrong-tool condition.** Conceded as meta-finding. Path-discipline is a housekeeping question. Running the full 12-step on it has cost ~2 critic rounds + ~6 subagent invocations to arrive at "do less." The intuitive call ("just fix reason (c) and move on") would have arrived in 5 minutes. **The meta-lesson is its own upgrade entry**: candidate v2 includes opening a second new entry [`upgrades/normal/2026-04-27-workflow-overruns-on-housekeeping/`](upgrades/normal/2026-04-27-workflow-overruns-on-housekeeping/) capturing this finding so the workflow-routing rule can be revisited (e.g., add a "is this a housekeeping question?" pre-check to step 1 that recommends bypassing).

## Named tradeoffs

| Tradeoff | This candidate accepts |
|---|---|
| Punch-list items 2 and 3 remain blocked for 30 days | **Yes.** They were already blocked on item 1; this preserves that. |
| 50/50 compliance may worsen | **Acknowledged.** That's exactly the signal we're measuring. |
| Operator may experience "no progress" as failure | **Acknowledged.** The progress *is* the data we're collecting + the substrate question being named. |
| The substrate decision is deferred, not answered | **Yes, on purpose.** Substrate by precedent is what the panel rejected. |
| One-line prose edit is "embarrassingly small" for a run that consumed two critic loops | **Yes.** That is the meta-finding from challenge §6. |

## Three assumptions that would flip the recommendation

1. **30-day audit shows violation rate >70%** (vs. current 50%). The "wait-and-see" premise fails: drift is accelerating, not stable. Substrate decision becomes urgent; loop-1 candidate or Option D becomes correct.
2. **A new authoring surface is added in the interim** (e.g., a new Write-capable agent for canon-ingest, a new slash command). The current author-class taxonomy expands. "Wait" no longer fits because the surface area changed; need to re-scope.
3. **The operator names a concrete capability they want now that depends on full enforcement** (e.g., "I want to write a script that does cross-artifact reference auditing and it needs canonical paths"). The "no harm yet" premise fails because a new use case demands the rule's full enforcement now.

## Ways this could be wrong

- **The 30-day audit doesn't happen.** Solo-maintainer audits are forgotten (outside-view). v2 mitigates by making the audit the *only* commitment; it is the entire ask. If even that is forgotten, the regime self-deletes back to status quo and no harm is done — but no learning either.
- **30 days is the wrong window.** Could be 7 days, could be 90. v2 picks 30 because it's longer than a single sprint and shorter than a season; arbitrary. If compliance is volatile (some weeks high, some low), 30 days may not be enough signal.
- **The "no harm" claim is wrong.** Maybe a future user (operator's future self) hits a broken link and silently routes around it. We wouldn't see that in the data we have.
- **Naming the substrate as a follow-up is itself substrate-by-precedent.** The act of opening an upgrade entry titled "gate-substrate spec" implies the substrate is needed. v2's defence: opening an entry is not committing to it; the lab explicitly admits ideas that may turn out to be wrong.

## Confidence

**Medium.** Higher than loop 1 because the candidate ships less and therefore is wrong in fewer ways. Lower than ideal because two of the three named flip-conditions (drift acceleration, new surfaces) are partially observable; the audit may not catch them in time.

The cheapest experiment that reduces the biggest uncertainty: **run the Explore audit at T+30** as specified. The script already exists (it produced the loop-1 distillation); cost is one Explore invocation.
