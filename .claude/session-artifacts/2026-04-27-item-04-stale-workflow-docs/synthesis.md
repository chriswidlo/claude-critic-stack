# Synthesis — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Workflow loops.** 2 (loop 1 = three rework verdicts; loop 2 = three approve verdicts).

---

## 1. Classifier label

**Primary: replace.** Default frame: stale top-level docs should be removed or rewritten. Frame bias: sunk-cost attachment to the existing primitive.

**Alternative classification: refactor** (if the claim were "behaviour unchanged, only reorganising pointers" — rejected because the candidate genuinely changes what new readers are pointed at). Frame-challenger surfaced a substantive third alternative — **new** — under the audience-reframe (build the first iteration of a workflow doc rather than the last iteration of cleaning up a stale one).

## 2. The reframe (current revision)

The user's frame was *correctness of first-read for a human reader*. The frame-challenger named the un-asked upstream question as the load-bearing one: **whom is this repo's workflow surface for?** Three candidate audiences (Claude reading CLAUDE.md auto-context, the maintainer, a forker) were silently bundled.

The candidate (v2) accepts the reframe and acts on it: **CLAUDE.md is for Claude + the operator-maintainer; README.md is for any human reader coming in cold (including forkers).** Each doc gets one declared audience, not a bundle. This unblocks the doc-shape decision: with the README's audience declared as cold-human, ship a Heilmeier-grade *What is this and why* paragraph in the same PR — not a pointer to a deferred doc.

## 3. Outside-view forecast

**Reference class:** small internal/OSS tools deleting a stale process/workflow doc and redirecting the entry-point README to one or two existing authoritative docs, with a "unify later" deferral.

**Base rates:**
- Deletion + redirect succeeds as a correctness move: ~80–90%.
- Two-doc onboarding works: ~40–60%, conditional on disjoint scope and named coverage.
- Deferred unified doc actually completed within 6 months: **~20–35%**.

**Position:** v2 sits above the base rate on the deletion leg; on the deferral leg, v2 lifts above v1's baseline by adding (a) a pre-commit hook (a structural early-warning system) and (b) a Heilmeier-grade rewrite *now* (so the deferred unification is no longer load-bearing for first-read correctness).

**Typical failure mode:** deferred unified doc never gets written; the pointer becomes the de facto workflow doc; readers form partial mental models. v2's mitigation: ship the Heilmeier-grade content now; defer only the *expanded* unified doc, which is no longer a correctness blocker.

## 4. Canon passages (supporting and contradicting)

**Supporting (favour the v2 collapse-to-canonical move):**
- *SRE Book* ch.28 — outdated docs hurt newbies most; senior staff compensate from memory. Source: Beyer, Jones, Petoff, Murphy, *Site Reliability Engineering* (Google, 2016).
- *SRE Book* ch.28 — minimal structure, prune and overhaul, don't proliferate.
- Anthropic, *Effective Context Engineering* (2025) — `CLAUDE.md` is the canonical context surface; a parallel workflow doc creates a second index to keep in sync.
- Anthropic, *Effective Context Engineering* (2025) — minimal-but-sufficient; bloated overlapping surfaces create ambiguous decision points.

**Contradicting (favour a dedicated onboarding artifact, against pure-pointer):**
- *SRE Book* ch.28 — explicitly advocates a *dedicated* structured onboarding artifact (the on-call learning checklist) as a "social contract." Direct argument for option (b).
- Heilmeier Catechism (Heilmeier, "Some reflections on management at DARPA," 1992) — the first question is jargon-free articulation for a new reader; neither CLAUDE.md (operator-dense) nor session-artifacts/README.md (layout-only) does that. v2 addresses this by rewriting the README's *What is this and why* paragraph in the same PR.
- Anthropic, *Effective Context Engineering* (2025) — pure just-in-time retrieval has a real exploration cost; small amounts of opinionated up-front context pay back.

## 5. Scope-map summary

| primitive | relationship |
|---|---|
| `workflows/architecture-review.md` | replace (delete) |
| `workflows/` directory | preserved (with redirect stub — architecture lens approved this asymmetric tradeoff in loop 2) |
| README.md `What this is` (lines 7–13) | replace (categorical, count-free) |
| README.md routing pointer (line 29) | replace (point at CLAUDE.md + session-artifacts/README.md) |
| README.md *Philosophy* (lines 35–37) | replace (rewrite as *What is this and why* — Heilmeier-grade) |
| CLAUDE.md | extend (add *Audience* section) |
| .claude/session-artifacts/README.md | extend (gains inbound link; no edit) |
| .claude/agents/ | extend (untouched) |
| Implicit "unified workflow doc" | conflict — deferred with pre-commit hook as a structural early-warning system |

**Unresolved conflict carried into synthesis:** the deferred unified doc question. v2 reframes this from "deferred-with-no-trigger" (v1) to "deferred-with-a-structural-early-warning-system" (the hook fires on count drift, which is a precondition for revisiting the doc shape). Architecture lens flagged that the hook catches count drift but not concept drift — a known, named limitation.

## 6. Frame-level challenge and how the recommendation addresses it

**Challenge:** *"The frame names the doc but not the reader; until the primary audience for the workflow surface is declared, every option is locally defensible and globally arbitrary."*

**Resolution in v2:**
- Move #3 declares Claude + operator-maintainer as CLAUDE.md's audience, in CLAUDE.md.
- Move #5 declares cold human reader (including forkers) as README.md's audience.
- Move #4 ships Heilmeier-grade prose for the README's declared audience in the same PR.
- The doc shape now follows from the audience pick, not the other way around.

## 7. Post-critique recommendation (LABELLED)

**Ship a single PR containing the following ten moves, in roughly this order.** Architecture, operations, and product lenses all approved this in loop 2. Effort: ~1–2h.

1. **Delete** [workflows/architecture-review.md](../../../workflows/architecture-review.md).
2. **Add a redirect stub** at `workflows/README.md` (~5 lines): *"Workflow contract is in [CLAUDE.md](../CLAUDE.md). This directory exists to redirect any external link from the previous `architecture-review.md` location."*
3. **Rewrite [README.md](../../../README.md):7–13** (`What this is` section) to a categorical, count-free paragraph naming workflow shape and pointing at CLAUDE.md as the contract. Drafted text in [candidate-v2.md](candidate-v2.md) move #2.
4. **Rewrite [README.md](../../../README.md):29** (routing pointer) to point at [CLAUDE.md](../../../CLAUDE.md) and [.claude/session-artifacts/README.md](../../README.md).
5. **Rewrite [README.md](../../../README.md):35–37** (*Philosophy*) into a *What is this and why* trio of paragraphs answering Heilmeier (i)/(ii)/(iii). Drafted text in [candidate-v2.md](candidate-v2.md) move #4.
6. **Add an *Audience* section to [CLAUDE.md](../../../CLAUDE.md)** near the top, declaring Claude + operator-maintainer as the audience and pointing forkers at README.md. Drafted text in [candidate-v2.md](candidate-v2.md) move #3.
7. **Add a pre-commit hook** at `.githooks/check-readme-shape.sh` that fails if README.md names a count of steps/agents/lenses. Register `core.hooksPath = .githooks`. *Operations lens flag:* per-clone setting; ship a one-line installer note in the PR description (`git config core.hooksPath .githooks`) so the maintainer's clone has it.
8. **Add a calendar reminder for 2026-07-27** to re-read the audience declaration in CLAUDE.md against the current state.
9. **Audit the three Explore gaps before commit:** `grep -rn "\bcritic\b" .claude/agents/ prompts/ upgrades/`. If non-zero, expand the PR or pause.
10. **Mark item 4 done** in [plans/2026-04-27-repo-cleanup-punch-list.md](../../../plans/2026-04-27-repo-cleanup-punch-list.md):81 with `✅ done <YYYY-MM-DD>`. Update [upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md](../../../upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/README.md):17 lifecycle row to mark 🔨 implemented (option a + b's Heilmeier pillar).

**Optional one-line addition in the README** (product lens residual): a sentence near the top stating *"This README is for any human reader coming in cold; the workflow contract for operators and Claude lives in CLAUDE.md."* Closes the loop-2 product-lens residual concern. Recommend including.

## 8. Named uncertainties (≥ 3)

1. **The pre-commit hook may be uninstalled on the maintainer's actual clone.** `core.hooksPath` is per-clone, not committed. If the hook is uninstalled, the structural protection collapses. *(Operations residual.)*
2. **The hook catches count drift but not concept drift.** If the workflow grows a new agent category that should appear in the README's categorical description, the hook is silent. *(Architecture and operations residual.)*
3. **The audience pick for CLAUDE.md may not match Claude's actual reading pattern.** If Claude's context is truncated and CLAUDE.md is the first thing dropped, the *Audience* section's effect diminishes. *(Candidate's own assumption #2.)*
4. **The Heilmeier paragraph has not been tested against a cold reader.** The maintainer drafted it; the prose is plausible but unverified. *(Candidate's own assumption #3.)*
5. **The CI tradeoff was accepted without ceremony.** A GitHub Actions check would survive `--no-verify`; the candidate chose pre-commit hook for cost. If the repo's no-CI posture changes, revisit. *(Architecture residual.)*

## 9. Cheapest experiment to reduce the biggest uncertainty

**Biggest uncertainty: #4 (Heilmeier paragraph quality).** It is load-bearing for the product-lens approve-condition; if the prose does not actually meet the bar, the post-(a) reading order silently fails for the cold-human audience.

**Cheapest experiment:** ask one external reader (a peer, not the maintainer) to read only the *What is this and why* paragraph and report what they think the stack does, who they think it is for, and whether they would consider using it. **Cost:** one DM, one reply. **Information gained:** whether the prose actually lands at the Heilmeier bar, or whether the maintainer's draft is satisfying-to-the-author but opaque-to-the-reader. **Failure mode of the experiment:** the peer's domain knowledge contaminates the test (they over-fill from context). *Mitigation:* pick a peer who is not in the LLM-tooling domain.

If the peer's report matches the intended frame, the prose ships as drafted. If it doesn't, iterate before merging.

---

## 10. What this synthesis recommends to the user

**Approve [candidate-v2.md](candidate-v2.md) and ship the ten-move PR.** The two-loop critic-panel converged on approve after the v1 rewrite addressed all three lenses' specific objections. The residuals named in loop 2 are minor and addressable by the optional README one-liner (closing the product residual) and the installer note in the PR description (closing the operations residual).

The deferred (b)/(c) unified-doc work is now genuinely a follow-up rather than a known-stale tail: the README's first-read correctness is closed by move #5's Heilmeier rewrite, the audience question is closed by moves #3 and #6, and the hook provides a structural early-warning system for shape drift. Whatever (b)/(c) ends up looking like, it is now a *quality multiplier*, not a *correctness gap*.
