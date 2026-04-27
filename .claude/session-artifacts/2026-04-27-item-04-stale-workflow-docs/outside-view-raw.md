# Outside-View Forecast — `2026-04-27-item-04-stale-workflow-docs`

(Persisted by orchestrator from outside-view agent's read-only return.)

## 0. Canon-first

Attempted to enumerate `canon/corpus/` — directory listing not available with this agent's tool surface. **Declared gap:** could not verify whether the corpus has entries on documentation drift, README hygiene, or technical-debt deferral. Canonical names that *should* be in scope for this class — Parnas & Clements ("A Rational Design Process: How and Why to Fake It," 1986); Knuth on literate programming; Cunningham's original technical-debt metaphor (1992) — none verified ingested. WebSearch used to fill the declared gap; results below are not promoted to canon.

## 1. Reference class

Most predictive class: **Small internal/OSS tools (single maintainer or 2–4 contributors) deleting a stale process/workflow doc and redirecting the entry-point README to one or two existing authoritative docs, with a "unify later" deferral.**

Adjacent classes considered:
- *General doc-drift cleanup* (too broad — different failure profile when there's a docs team)
- *"Pointer-only" READMEs in monorepos* (closer; useful for the "two-doc landing" sub-question)
- *Deferred refactors with a written follow-up ticket* (useful for the deferral sub-question)

## 2. Base rate

No hard published statistic exists for this exact micro-decision. Qualitative base rates from the literature and practitioner reports:

- **Deletion of a stale doc + redirect to authoritative source: succeeds as a *correctness* move ~80–90% of the time.** Removing wrong information is almost always better than leaving it; the well-known failure case (broken inbound links) is local and cheap to fix.
- **"Point readers at two docs instead of writing a unified one": works as onboarding ~40–60% of the time** in small projects. The split is tolerable when (a) the two docs have clearly disjoint scope and (b) the README explicitly names what each covers. It silently fails when readers must mentally join them to act.
- **"Defer the unified doc to a future task": actually completed within 6 months ~20–35% of the time** in small/solo projects. The modal outcome is that the deferred doc lives in the backlog as a known-stale-but-not-wrong state for 1–3 years until either a contributor onboarding incident forces it or the project itself is retired.

These are estimates calibrated from cited practitioner sources; treat as order-of-magnitude.

## 3. Position relative to base rate

**Above base rate on the deletion-and-redirect leg; at or slightly below base rate on the deferral leg.**

Features lifting it above the class average:
- The two redirect targets ([CLAUDE.md](../../../CLAUDE.md) and [.claude/session-artifacts/README.md](../../README.md)) have **clearly disjoint scope** — one is behavioural/authoritative, the other is layout-only. The split is principled, not accidental.
- The stale doc references a non-existent agent (`critic`); leaving it is *actively misleading*, not merely incomplete. Deletion strictly dominates.
- Project is small and the maintainer holds the model in their head — the cost of the gap during the deferral window is bounded.

Features placing it at or below the class average:
- "Defer the unified doc" has no trigger condition, no owner-different-from-author, and no expiry. This is the textbook shape of a deferral that doesn't get done.
- Two-doc onboarding requires the reader to compose `CLAUDE.md` (12-step prose) with `session-artifacts/README.md` (layout) themselves. New readers (including future-you, including future Claude sessions) will not reliably do this composition.
- `CLAUDE.md` is *operating instructions for an agent*, not *a workflow tutorial for a human*. Pointing humans at it as the authoritative workflow doc is a category mismatch — an agent-instructions file optimizes for behaviour-shaping, not for explanation.

## 4. Typical failure mode

The dominant failure for this reference class is **not** that the deletion goes wrong. It is:

> **The deferred unified doc never gets written, and the README's "see CLAUDE.md and session-artifacts/README.md" pointer becomes the de facto workflow doc — but it is a *pointer*, not a *workflow doc*. New readers (or the maintainer six months later) bounce off `CLAUDE.md`'s agent-instruction register, miss the 12-step shape on first read, and form a partial mental model. The gap is silent because nothing breaks; it surfaces as confused contributions, mis-routed sessions, or the maintainer rewriting the explanation from scratch in chat each time someone asks.**

Secondary failure: a *third* stale derivative gets written (a comment, a gist, a chat message pinned somewhere) to fill the explanation gap, recreating the drift the cleanup was meant to remove. (Docsie 2025, "Documentation Drift": "When official docs fall behind, teams build their own stopgaps; these fragment knowledge and reintroduce drift.")

## 5. Outside-view verdict

**Within tolerance on the deletion. Below base rate on the deferral.**

The delete-and-redirect move is correct and should ship. The "defer the unified doc" leg is where the reference class predicts failure. To lift it back to within tolerance, the cheapest interventions are:

- Give the deferred doc a **trigger** rather than a date: e.g., "write the unified workflow doc the next time someone other than the maintainer needs to run the workflow, OR the next time `CLAUDE.md` is materially restructured, whichever is first." Trigger-based deferrals complete materially more often than time-based ones in small-project settings.
- In the rewritten README, **explicitly name the gap**: a single sentence saying "there is no standalone human-readable workflow tutorial yet; the 12-step shape is defined in `CLAUDE.md` (agent-facing) and the artifact layout in `session-artifacts/README.md`." Naming the gap is what keeps the two-doc redirect from silently failing — it tells the reader *what they are not getting*, which is the single most reliable mitigation in the doc-drift literature.

Without those two changes, the proposal sits at roughly the class base rate: the deletion is a clear win, the deferral is a coin-flip at best, and the modal one-year outcome is a known-stale gap nobody fixes.

## Sources

- Documentation Drift: Definition, Examples & Best Practices — Docsie, 2025.
- Documentation Rots. Here's How to Stop It. — DocsAlot, 2024.
- Documentation Debt: Inefficient docs and how we fix them — DTALES Tech, undated.
- I Document Like a Professional at Work. My Side Projects Are a Disaster. — Lausier, DEV, 2023.
- Why CI/CD Still Doesn't Include Continuous Documentation? — DeepDocs, undated.
