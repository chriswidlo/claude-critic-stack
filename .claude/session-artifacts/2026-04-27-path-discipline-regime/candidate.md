# Candidate recommendation — path-discipline regime

## Position

**Option A modified — keep the rule, fix reason (c), and make the mechanical gate mandatory rather than optional.** Specifically:

1. Reword reason (c) in [`CLAUDE.md`](CLAUDE.md):16 to describe what clause 2 actually provides (stable, grep-discoverable text address; click-navigation is via file tree, not link).
2. **Add a `PostToolUse` Write/Edit hook** that rejects file-relative `(\.\./)` markdown link targets in active surfaces (`upgrades/<tier>/<slug>/`, `plans/`, top-level docs, `.claude/agents/`, `.claude/commands/`). Hook lives at [`bin/check-path-discipline.sh`](bin/check-path-discipline.sh) (new) and is wired in [`.claude/settings.json`](.claude/settings.json). Session artifacts are explicitly excluded.
3. Patch [`.claude/commands/upgrade.md`](.claude/commands/upgrade.md) with one paragraph instructing repo-root link form. (Soft enforcement — paired with hook, not standalone.)
4. Patch the three Write-capable agent prompts (`frame-challenger`, `scope-mapper`, `subagent-distiller`) with the same one-paragraph reminder.
5. Sweep 7 active-surface violator files (6 entry READMEs + [`upgrades/LEDGER.md`](upgrades/LEDGER.md):1-line) into compliance. Defer the punch-list at [`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md) to the same sweep.
6. Leave the 2 file-relative session-artifact files unchanged per the longitudinal-record contract from commit `5108ed3`.
7. Schedule a **14-day post-implementation audit** using the same Explore script as a regression check. If new agent-authored files show <80% compliance, escalate to step 11 (replan to Option B).

## Addressing the frame-level objection

The frame-challenger's primary objection: *"without a mandatory mechanical gate, Option A is documentation-only, and the corpus says documentation-only is worse than no rule."*

**Accepted.** The original plan placed the gate as step 6, marked "optional, defer if scope creeps." That was the soft fix dressed up as structural that the challenger named. The candidate above promotes the gate to load-bearing — without it, the recommendation is Option B (or no rule). The slash-command and agent-prompt patches stay, but as **belt-and-suspenders** — failing them is annoying, failing the gate blocks the write.

The challenger also named an alternative frame: *"the rule is mis-located, not mis-worded — CLAUDE.md is for decision-process behaviour, path-style is an authoring convention; distribute clause 2 to the four authoring surfaces and remove it from CLAUDE.md."*

**Considered, rejected.** Two reasons:
- The rule applies to operator-authored top-level docs ([`README.md`](README.md), [`upgrades/LEDGER.md`](upgrades/LEDGER.md), [`upgrades/README.md`](upgrades/README.md), [`tests/regression/`](tests/regression/), [`plans/`](plans/)). The operator is not invoking a slash command or an agent when writing those — distributing to authoring surfaces leaves operator authoring uninstructed.
- Distribution multiplies the places the rule must stay in sync with itself. Centralised in CLAUDE.md + a single hook is one source of truth.

The alternative frame is not unreasonable; it's just costlier in this repo's shape. Recording it as a *deferred option* in step 11 / synthesis if the operator prefers it.

## Named tradeoffs

| Tradeoff | This candidate accepts |
|---|---|
| Editor click-navigation from subdirs | **Lost** — but mitigated by file-tree + grep. |
| Authoring friction (gate may reject AI output) | **Increased** — agent must self-correct on hook fail. The friction is the point. |
| Maintenance surface (new hook script, new agent-prompt clauses) | **Added** — ~50 lines of bash + ~3 paragraphs in agent prompts. |
| Grep-stability across longitudinal record | **Preserved.** This is the main thing the rule was added to protect. |
| Privacy property (no `/Users/` or `~/`) | **Preserved.** Reasons (a) and (d) untouched. |
| Speed of the 14-day verification | **Slow** — the recommendation is conditional and we won't know if it worked for two weeks. Operator must accept the wait. |

## Named assumptions (any one wrong → recommendation flips)

1. **The dominant artifact consumer is `grep` (operator + agents), not click-navigation in a markdown viewer.** If the operator actually clicks entry links in VS Code or Obsidian as a primary navigation mode, the loss of clickability matters and the right answer is Option B.

2. **A `PostToolUse` Write/Edit hook is operationally compatible with the `/upgrade` flow.** Hooks fire on every Write — a hook that rejects writes will interrupt the slash command's "instant capture" property. If the hook makes capture feel broken to the operator, the soft-enforcement-only fallback is correct (and accepts ~35% compliance per outside-view base rate).

3. **Agents can self-correct on hook failure.** When the hook rejects a Write, the agent must (a) read the rejection message, (b) understand it as a path-style violation, (c) regenerate the artifact in the right style. If agents cannot do this reliably (e.g., they retry the same write or give up), the gate produces session deadlocks rather than compliance. The 14-day audit is partly there to catch this.

4. **The longitudinal-record contract from commit `5108ed3` should bind this question.** The frame-challenger pushed back on this preservation. If the operator concludes the contract was scoped too narrowly (privacy-only sweeps were a 2026-04-26 decision; this is a 2026-04-27 question), then the 2 file-relative session-artifact files should be in scope and the preservation logic in step 6 above is wrong.

5. **The 100%-of-violations-are-post-rule pattern from the Explore distillation is causal, not coincidental.** If the actual cause is something else (e.g., the folder-shape migration changed how authors think about paths), the slash-command + agent-prompt patches treat the wrong root cause and compliance won't improve.

## Ways this could be wrong (named, not exhaustive)

- **The base rate is wrong.** Outside-view's ~30% number is a qualitative anchor, not measured. If solo-maintainer style rules with mechanical gates *actually* sustain 60-80% compliance, then the gate is over-engineered for this scale.

- **The mechanical gate breaks the "decision-stack" property of the repo.** This repo is meta — its job is to review *other* design decisions. Adding a runtime hook to its own authoring loop introduces a feedback path that may interact with the workflow in unexpected ways (e.g., a critic-panel agent calls Write to record a critique, hits the hook, fails, the workflow stalls). Need to test the hook against a real session before declaring it safe.

- **The 14-day audit is itself a fragile commitment.** Audits in solo repos are forgotten. The audit needs an explicit calendar reminder or a scheduled background agent; otherwise it's a documentation-only commitment exactly like the rule it's auditing.

- **The honesty meta-challenge from the frame-challenger lands.** The orchestrator (me) authored the punch-list in violation of the rule. Recommending the rule be preserved with mandatory enforcement *might* be post-hoc rationalisation — the violation came first, the case for preservation came after. The signal that it isn't post-hoc: I downgraded "fix and patch" to "fix and patch and gate," which is *less* convenient for me than the original plan. If I were rationalising, I'd have kept the gate optional.

- **Option D (move clause 2 out of CLAUDE.md, distribute to four authoring surfaces) is not given a fair hearing.** I considered and rejected it in 2 sentences. The critic-architecture lens may want to push on that.

## What this candidate does NOT decide

- Whether the LEDGER row's single file-relative violation should be fixed in this sweep or in punch-list item 10.
- Whether the punch-list itself (item 2 specifically) should be edited to reflect the session-artifact restraint, or whether it stays as authored and the new candidate document supersedes it via the decision-log.
- The exact bash pattern for the hook (regex on `\]\(\.\./` is the obvious starting point but doesn't catch every form — `[../foo](../foo.md)` style links from a subdir, etc.). Implementation detail; not a frame issue.
- Whether to update [`.claude/agents/`](.claude/agents/) read-only agents that don't have Write access (they can't write paths, but they cite them in prose). Answer: not in this candidate's scope.

## Confidence

**Medium-low**, downgraded from the plan's "medium." Three things I'm uncertain about:

1. The hook-vs-flow interaction (assumption 2).
2. Agent self-correction on hook failure (assumption 3).
3. Whether the operator agrees that the longitudinal-record contract should bind here (assumption 4).

The 14-day audit is the cheapest experiment that reduces the biggest uncertainty (1 + 3 together).
