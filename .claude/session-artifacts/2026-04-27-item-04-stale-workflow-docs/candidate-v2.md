# Candidate recommendation — v2 (post-critique rewrite) — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Loop.** 2.
**Reads.** [critiques.md](critiques.md), [critiques/architecture.md](critiques/architecture.md), [critiques/operations.md](critiques/operations.md), [critiques/product.md](critiques/product.md), [candidate.md](candidate.md) (v1, for delta comparison).

---

## Position

Ship a single PR that does **all** of the following — the candidate is now substantively wider than v1, because the critic panel established that the v1 mechanisations were performative and three lenses each demanded a structural change.

### Concrete moves

1. **Delete** [workflows/architecture-review.md](../../../workflows/architecture-review.md). **Keep `workflows/` as a directory with a single redirect file** (`workflows/README.md`, ~5 lines: *"Workflow contract is in [CLAUDE.md](../CLAUDE.md). This directory exists to redirect any external link from the previous `architecture-review.md` location."*). This addresses architecture's "ignored alternative #4" — the asymmetric cost of an external-link 404 is unrecoverable; cost of a stub is one file.

2. **Rewrite the `What this is` section of [README.md](../../../README.md) (lines 7-13) to be categorical, not enumerative.** Replace *"Three things: 1. A critic subagent… 2. A canon librarian subagent… 3. An outside-view subagent…"* with prose that names *categories* of agents and a *workflow shape* without ever naming specific counts. Example phrasing:

   > *"A multi-step workflow that puts a candidate decision through four kinds of pressure before producing a recommendation: classification of what the question actually is; retrieval from a curated industry corpus that is required to surface contradictions; reference-class forecasting against the outside view; and a critic panel of independent lenses with veto authority. The workflow's contract — every step, every artifact, every gate — lives in [CLAUDE.md](CLAUDE.md), which is the only doc that has to stay in lockstep with the agents under [.claude/agents/](.claude/agents/)."*

   This addresses the architecture lens's invariant #1 (one-source-of-truth for shape) by making it structurally impossible to violate: the README does not name counts, so counts cannot drift.

3. **Move the audience declaration into [CLAUDE.md](../../../CLAUDE.md), not the README.** Add a short *Audience* section at the top of CLAUDE.md (just under the existing introduction):

   > *"This file is read by Claude as part of automatic context loading and by the maintainer when modifying agent contracts. It is the workflow's contract — operator-facing, dense, and assumes the 12-step shape. If you are a forker or external evaluator, this is not the doc that explains what the stack is for; that is in [README.md](README.md). If you are extending the stack, this is the doc to keep in lockstep with [.claude/agents/](.claude/agents/)."*

   This addresses the architecture lens's frame-level objection: the audience declaration now lives in the same artifact as the workflow contract, so the contract author cannot edit the workflow without seeing the audience claim. Eliminates the third-surface drift risk.

4. **Rewrite the *Philosophy (two sentences)* section of [README.md](../../../README.md) (lines 35-37) into a *What is this and why* paragraph that answers Heilmeier in plain language.** Replace the existing paragraph with three short paragraphs that answer *(i) what are you trying to do, in absolutely no jargon, (ii) who cares, (iii) if successful, what difference will it make.* Drafted phrasing:

   > **What is this and why.** *LLM-driven design assistants tend to agree with whoever is asking. They pattern-match to the local codebase, miss base rates, treat every retrieval as confirmation, and produce confident answers on questions where the right answer is "I don't know yet." This stack is a structural fix for those known failure modes — not a clever-prompt trick, not a persona. It works by making the AI route every decision through a sequence of agents whose job is to push back: classify the question against frame bias, retrieve from a curated corpus that is required to surface contradictions, forecast against the outside view, and pass the result through three critic lenses any of which can veto. None of these steps are clever; together they make it harder for the AI to produce a confidently-mediocre answer.*
   >
   > *Who cares: anyone making architectural decisions where being wrong is expensive and the wrong-answer mode is "the AI agreed with my first instinct."*
   >
   > *Difference: the user gets a recommendation accompanied by a forced reframe, named tradeoffs, named assumptions, named ways the answer could be wrong, and the experiment that would resolve the biggest uncertainty — instead of a confident paragraph that is silently anchored to the codebase or to the question's framing.*

   This addresses the product lens's veto: the audience declaration's pointer (in CLAUDE.md, per move #3) now resolves to a destination that delivers Heilmeier-grade content. The pointer is no longer broken-on-day-one.

5. **Pick which of "maintainer" and "Claude" the README rewrite is for, and state it.** They have orthogonal doc requirements. Decision: **the README is for any human reader (maintainer-six-months-from-now, forker, evaluator) coming in cold; CLAUDE.md is for Claude and for the maintainer when modifying contracts.** The README's *What this is* + *What is this and why* sections (moves #2 and #4 above) are written for cold human readers; CLAUDE.md's contract + Audience section (move #3) are written for the operator-facing audience. Each doc has *one* declared audience, not a bundle. This addresses the architecture lens's second frame objection.

6. **Add one concrete control.** Add a `pre-commit` git hook (committed at [.githooks/check-readme-shape.sh](../../../.githooks/check-readme-shape.sh) with `core.hooksPath = .githooks` registered in repo config) that fails the commit if [README.md](../../../README.md) names any specific count of steps, agents, or critic lenses. The hook is ~10 lines of `grep -E '\b(12|10|three|3)[- ](step|agent|lens|lenses)\b' README.md` returning non-zero. **And** add a calendar reminder for **2026-07-27** (three months out) to re-read the audience declaration in CLAUDE.md against the current state of the stack. The first control is mechanical and shipped; the second is a maintainer commitment with a concrete date. Both addressed by operations's approve-condition (a). The pre-commit hook is the falsifiable observation mechanism the v1 candidate lacked.

7. **Re-price Assumption 1 honestly.** The candidate cannot reliably measure forker traffic on this repo with the maintainer's current tooling. Mark Assumption 1 as **untestable in practice** and absorb the cost: if forkers materialise as a non-trivial population, the maintainer notices via incoming GitHub issues / PRs / referrals, not via a metric. This is a downgrade from v1's claim that the assumption *could* be tested with a 30-day traffic check. Operations's approve-condition (b).

8. **Audit the three Explore gaps before commit:** singular-`critic` references in [.claude/agents/](../../../.claude/agents/) internals, [prompts/](../../../prompts/), and [upgrades/](../../../upgrades/). Same as v1.

9. **Mark item 4 done** in [plans/2026-04-27-repo-cleanup-punch-list.md](../../../plans/2026-04-27-repo-cleanup-punch-list.md):81 with `✅ done <YYYY-MM-DD>`. Update [upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md](../../../upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md):17 lifecycle row to mark 🔨 implemented.

10. **Defer (b) and (c)** with the same trigger condition as v1, but the trigger is now meaningful because move #6 introduces the pre-commit hook (a structural early-warning system that is *not* a deferred-doc trigger but does fire on shape drift, the precondition for revisiting the unified-doc question).

## Delta vs. v1

| Aspect | v1 | v2 |
|---|---|---|
| Audience declaration location | Inside README.md | Inside CLAUDE.md |
| README's `What this is` section | Enumerative ("12 steps, 10 agents, three lenses") | Categorical (no counts) |
| Heilmeier-grade content | Pointer to unrewritten *Philosophy* | Rewritten *What is this and why* paragraph |
| Audience picked | "Maintainer + Claude" (bundle) | README ↔ cold-human-reader; CLAUDE.md ↔ Claude + operator-maintainer |
| Triggers | Three written triggers, no fire mechanism | Pre-commit hook (mechanical) + dated calendar reminder (committed) |
| `workflows/` directory | Deleted entirely | Kept with redirect stub |
| Assumption 1 testability | Claimed testable via traffic check | Marked untestable; cost absorbed honestly |

Six structural changes, all answering specific lens objections.

## Tradeoffs accepted

- **PR scope is meaningfully wider than v1.** v2 ships a pre-commit hook, an audience declaration in a different file, a rewritten *Philosophy* section, and a redirect stub. Effort is now ~1-2h (vs. v1's 30 min). This is the cost of taking the panel's vetoes seriously.
- **The pre-commit hook is a maintenance burden** — if the README ever legitimately needs to name a count, the hook fails. Mitigation: the hook can be bypassed with `git commit --no-verify` and the maintainer can decide; the hook is a *prompt to think*, not a hard constraint.
- **The rewritten *What is this and why* paragraph commits to a particular voice and framing.** Future framing changes will read as "rewriting the load-bearing paragraph" rather than "tweaking the philosophy section." Stickier than v1's voice-preserving rewrite.
- **The redirect stub at `workflows/README.md`** adds one line of permanent maintenance burden in exchange for protecting external-link integrity. Architecture lens approved this asymmetry; product/operations did not weigh in.

## Assumptions (any of which would flip the recommendation)

1. **The pre-commit hook is enforced.** If the maintainer routinely uses `--no-verify`, the structural protection collapses to a discipline question, the same shape v1 was vetoed for. **Test:** at the 2026-07-27 calendar checkpoint, `git log --grep="--no-verify"` and inspect; if more than two bypasses, the hook is decorative.
2. **CLAUDE.md is the right home for the audience declaration.** This assumes Claude reads CLAUDE.md often enough that the audience claim is "seen" by the right reader. If Claude rarely reads CLAUDE.md fully (e.g. context truncation, large workflows where CLAUDE.md is the first thing dropped), the declaration's effect diminishes. **Test:** the maintainer can sample by asking Claude in a fresh session "what is the declared audience of CLAUDE.md?" — if Claude can answer, it has been read.
3. **The rewritten *What is this and why* paragraph is actually Heilmeier-grade.** I drafted it; it has not been tested against a cold reader. **Test:** ask one external reader (a peer, not the maintainer) to read only that paragraph and report what they think the stack does. If the report matches the intent, the paragraph works. If not, iterate.

## Ways this could still be wrong

- **The audience declaration in CLAUDE.md is read by Claude but not by the maintainer.** CLAUDE.md is auto-loaded for Claude; the maintainer doesn't routinely re-read it. Maintainer-side staleness is plausible. Mitigation: the calendar reminder is partly *for* the maintainer.
- **The pre-commit hook is too narrow.** It catches *count drift* but not *concept drift* — if the workflow grows a new agent category that should appear in the README's categorical description, the hook is silent. The hook is a smoke alarm for one specific class of drift, not all drift.
- **The PR is now wide enough that it could be split.** Some panel members (the operations lens in particular) might prefer the deletion + redirect to ship first, with the hook + rewritten Philosophy in a follow-up. Counter-argument: splitting reintroduces the v1 problem of "ship a partial response to the frame challenge and trust the follow-up to land," which the panel already vetoed.

## What the v2 candidate hands the synthesis step

The post-critique recommendation has six structural changes from v1, each pinned to a specific lens objection. The frame survives unchanged. The decision the synthesis step asks the user to make is:

> *Approve v2 as-is, or reduce scope back toward v1 and accept the panel's vetoes as ungranted?*

If the user approves v2, the implementation is the ten moves above, in roughly that order, in a single PR.
