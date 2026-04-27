# Candidate recommendation — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Author.** Orchestrator (step 9 of 12-step workflow).
**Reads:** [requirement.md](requirement.md), [frame.md](frame.md), [scope-map.md](scope-map.md), [challenges.md](challenges.md), and the three distillations under [distillations/](distillations/).
**Does not read:** raw subagent returns (anti-anchoring rule).

---

## Position

Ship **option (a) plus an audience declaration** as a single PR. Concretely:

1. **Delete** [workflows/architecture-review.md](../../../workflows/architecture-review.md) and the now-empty `workflows/` directory.
2. **Rewrite** [README.md](../../../README.md):7-13 from the Phase-1 *"three subagents"* framing to a four-paragraph current-shape framing. Replace [README.md](../../../README.md):29's pointer to the deleted workflow file with pointers to [CLAUDE.md](../../../CLAUDE.md) and [.claude/session-artifacts/README.md](../../README.md). **In addition,** add a single sentence at the top of the rewritten README — before the *"What this is"* list — that **declares the primary audience** of the README and the workflow surface. (See "Audience declaration" below.)
3. **In the rewritten README**, include a one-line *gap statement* that names what the post-(a) reading order does *not* give the reader: `"There is no standalone human-readable workflow tutorial yet; the 12-step contract is in CLAUDE.md (operator-facing) and the per-session artifact layout in .claude/session-artifacts/README.md."` This is the outside-view's *"name the gap"* mitigation.
4. **Defer (b) and (c) with a trigger condition,** not a date. Encode the trigger in [upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md](../../../upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md) — the upgrade entry that originated this item: revisit the unified-doc question when (i) a contributor other than the maintainer needs to run the workflow, or (ii) [CLAUDE.md](../../../CLAUDE.md) is materially restructured, or (iii) the README's audience-declaration changes — whichever is first.
5. **Audit the three Explore gaps before commit:** singular-`critic` references in [.claude/agents/](../../../.claude/agents/) internals, [prompts/](../../../prompts/), and [upgrades/](../../../upgrades/). [scope-map.md](scope-map.md) flagged these as un-closed by [Explore](distillations/Explore.md). Either confirm they are clean (the likely outcome), or expand the PR's scope to include them.
6. **Mark item 4 done** in [plans/2026-04-27-repo-cleanup-punch-list.md](../../../plans/2026-04-27-repo-cleanup-punch-list.md):81 with `✅ done <YYYY-MM-DD>`. Update the upgrade entry's lifecycle row at [upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md](../../../upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md):17 to mark 🔨 implemented.

## How this addresses the frame-level objection

The frame-challenger's load-bearing objection (carry-forward, [challenges.md](challenges.md):39):

> *"The frame names the doc but not the reader; until the primary audience for the workflow surface is declared, every option (a/b/c, defer/bundle) is locally defensible and the next stale-doc punch-list item is already accruing."*

The candidate addresses this by **declaring the audience inline in the rewritten README** — not by writing a new doc, not by deferring the audience question, not by bundling (b)/(c). The one-sentence declaration is the cheapest possible response to the objection that still answers it.

## Audience declaration (proposed)

The maintainer should pick one of the three frames the challenger named and write it into the README. Drafted phrasing for each so the maintainer can choose:

- **Audience = maintainer + Claude (the live use case today).** *"This README is written for the maintainer of this stack and for Claude reading it as part of context. Forkers and external adopters can navigate from here, but the Heilmeier-grade 'what is this and why' is in the* Philosophy *section, not in this README's main body."*
- **Audience = forker / external adopter (the aspirational use case).** *"This README is written for someone evaluating whether to fork this stack. The 12-step workflow that defines the stack's behaviour is operator-facing and lives in `CLAUDE.md`; the README walks you to it."* This phrasing implies a longer *"What this is"* section with more onboarding work — option (b)/(c)-flavoured.
- **Audience = both, sequenced.** *"The first three paragraphs are written for a forker evaluating the stack; everything below is written for the maintainer and for Claude reading the file as context."* Most flexible; biggest editing burden.

**Recommended pick: maintainer + Claude (the first frame).** The stack is a personal R&D lab; the live audiences today are the maintainer and Claude. Pretending the README serves forkers when no forkers exist is a category-mismatch in the other direction. If forkers materialise, the trigger condition fires and option (b) or (c) gets revisited under the *new* declared audience.

## Tradeoffs accepted

- **Forkers / external adopters get a category-mismatched onboarding** (CLAUDE.md is operator-dense). This is consciously accepted because they are not the live audience. Cost: any forker who arrives in the next 6–12 months bounces off CLAUDE.md and either reads it operator-style or leaves. Mitigation: the gap statement (point 3 above) tells them *what they are not getting,* which is the doc-drift literature's most-reliable mitigation per [outside-view distillation](distillations/outside-view.md).
- **Two-doc onboarding** (CLAUDE.md + session-artifacts/README.md) for the post-(a) reader. Accepted because the two docs have clearly disjoint scope (behavioural vs. layout), and the [outside-view distillation](distillations/outside-view.md) judged this above the reference-class base rate when scopes are disjoint and named.
- **Heilmeier's *"presence of purpose in plain language"* bar is not met inside the rewritten README itself,** only in the existing *Philosophy (two sentences)* section ([README.md](../../../README.md):35-37). Accepted because rewriting the *Philosophy* paragraph is out of scope for item 4, but the audience declaration explicitly points at it as the Heilmeier-answer location.
- **Deferral becomes trigger-based, not time-based.** Accepted because the [outside-view distillation](distillations/outside-view.md) priced time-based deferrals at 20–35% completion in the small-project class and named trigger-based as materially higher. Cost: triggers can be ignored too; this is a known weakness, not a solved problem.

## Assumptions (any of which would flip the recommendation if wrong)

1. **The live audience for the README in the next 6–12 months is the maintainer + Claude, not forkers.** If forkers are in fact the live audience, the candidate is wrong: it ships a category-mismatched onboarding. **Test:** check repo traffic / star history / any external link citations after 30 days. If forkers dominate, fire the trigger and revisit (b)/(c).
2. **`CLAUDE.md` will stay in lockstep with the workflow it describes.** The candidate relies on CLAUDE.md as the post-(a) authoritative workflow doc. If CLAUDE.md drifts from the running stack, the candidate's *"point at the doc that orchestrators have to keep correct anyway"* argument collapses. **Test:** before each `git commit` that touches `.claude/agents/` or any agent's contract, the maintainer re-reads CLAUDE.md and patches it. If this discipline lapses, the candidate's central claim is undermined.
3. **The three Explore gaps (singular-`critic` references in agents, prompts, upgrades) are in fact clean.** The candidate scopes its delete-and-rewrite to the README and the stale workflow file; if any other live doc still names a singular `critic` agent, the deletion ships an inconsistency rather than fixing one. **Test:** `grep -rn "\\bcritic\\b" .claude/agents/ prompts/ upgrades/` before commit; if non-zero, expand the PR or pause.

## Ways this could still be wrong

- **The audience declaration might be performative, not load-bearing.** A single sentence in a README can be ignored by every subsequent reader and writer. If the declaration does not actually shape downstream doc decisions (e.g. someone writes a Heilmeier-grade onboarding paragraph that contradicts the declared audience), the frame-challenger's carry-forward objection re-fires unanswered.
- **Trigger-based deferral can become indistinguishable from never-done** if no one watches for the triggers. The outside-view distillation flagged this. The candidate has no mechanism to *check* the triggers.
- **The `workflows/` directory deletion is a small irreversible move.** If option (b) ships in 6 months, the directory has to be recreated. Trivially reversible, but worth naming.
- **The candidate accepts an unaddressed Heilmeier objection** (the rewritten README does not in itself satisfy *"presence of purpose in plain language"* — it points elsewhere). The product critic may flag this as a weakest-link.

## What the critic-panel should test

- **Architecture lens:** does the candidate keep the doc-surface invariant clean (one canonical workflow doc — CLAUDE.md — with one inbound link from README), or does the audience declaration covertly create a third surface to maintain? Does the trigger-based deferral satisfy *"frame-level objection addressed"* or only *"frame-level objection acknowledged"*?
- **Operations lens:** does the trigger-based deferral have an actual observation mechanism, or is it a wish? Does the 30-day audience-traffic test in Assumption 1 have a real measurement plan? What is the rollback if the audience declaration is wrong?
- **Product lens:** does a forker arriving in the next 90 days experience the post-(a) reading order as coherent or as a category mismatch? Is the Heilmeier objection from [challenges.md](challenges.md):29 actually addressed or only relocated to the *Philosophy* section that wasn't rewritten?
