# Product-lens critique (Loop 2) — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Lens.** Product / user-surface.
**Loop.** 2.
**Prior verdict on v1.** rework. Approve-condition: rewrite *Philosophy (two sentences)* (or replace with *What is this and why*) to actually answer Heilmeier (i)/(ii)/(iii) in jargon-free prose, in the same PR.

## 1. User-visible consequence

A first-time human reader opens [README.md](../../../../README.md) and now reads, in order: a categorical *What this is* paragraph (no counts), a *What this is not* paragraph, *How to use*, *Populating the canon*, and a rewritten *What is this and why* trio of paragraphs that names failure modes, who cares, and the difference. The pointer the v1 audience declaration set up (in CLAUDE.md per move #3) now lands a reader on prose that *does* try to answer Heilmeier rather than on the old *library/apprentice* metaphor.

Day-1 reader experience: more accurate **and** the Heilmeier moment is attempted in the same surface.

## 2. Heilmeier check on v2's actual draft text

- **(i) What are you trying to do, in absolutely no jargon?** Paragraph 1: LLM design assistants agree too readily, miss base rates, treat retrieval as confirmation, produce confident answers when they shouldn't; this stack makes the AI route every decision through agents whose job is to push back. **Answered.** Light jargon ("LLM," "agents," "base rates," "retrieval") — domain lingua franca, intelligible from context. Not pure-Heilmeier, materially closer than *Philosophy (two sentences)* ever was.
- **(ii) Who cares?** Paragraph 2: anyone making architectural decisions where being wrong is expensive and the failure mode is "the AI agreed with my first instinct." **Answered.** Crisp; names buyer, names pain.
- **(iii) If successful, what difference will it make?** Paragraph 3: the user gets a recommendation with a forced reframe, named tradeoffs, named assumptions, named ways the answer could be wrong, and the cheapest experiment — instead of a confident paragraph silently anchored to the codebase or the framing. **Answered.** Names deliverable; names contrast.

All three Heilmeier questions are attempted in the same artifact, in the same PR, in plain-enough prose. Loop-1 approve-condition met.

## 3. Commitments implied

- Rewritten *What is this and why* is now the load-bearing onboarding prose. Future framing edits will be edits to *the* onboarding paragraph. Stickier.
- On-record audience separation: README ↔ cold human; CLAUDE.md ↔ Claude + operator-maintainer.
- Categorical-not-enumerative README. Pre-commit hook makes this load-bearing.

## 4. Migration burden

- **Maintainer:** ~1-2h, named honestly.
- **External bookmarkers of `workflows/architecture-review.md`:** redirect stub at `workflows/README.md`. One-hop redirect, strictly better than v1's 404.
- **Future contributors editing the README:** must think categorically. Hook-enforced.
- **Forker arriving in next 90 days:** category-mismatched-onboarding burden materially reduced.

## 5. Product affordances

**Better:**
- Heilmeier-grade *what is this and why* in the README itself. Pointer-that-doesn't-resolve closed.
- Two reading depths: *What this is* (shape) and *What is this and why* (purpose). Cold reader can stop after either.
- Fast-disqualification preserved.
- Redirect stub preserves external link integrity.

**Worse:**
- Long. Three paragraphs of dense prose where v1 had two sentences. Some readers will skim.
- "LLM-driven design assistants" is light jargon. Acceptable for declared audience (cold *technical* reader); borderline against pure-Heilmeier.

## 6. Frame-level objection (residual, not veto)

**The audience declaration lives in CLAUDE.md, but the Heilmeier-grade onboarding lives in README.md.** A cold reader who lands on CLAUDE.md first reads the redirect to README.md — that works. But the reverse — a reader who reads the README's *What is this and why* and wants to know who the README is *for* — is no longer answered in the README itself. v2 made the README explicitly cold-reader-facing in move #5 but does not state that fact *in the README*.

A one-liner near the top of the README ("This README is written for any human reader coming in cold; the workflow contract for operators and Claude lives in [CLAUDE.md](CLAUDE.md).") would close it. Worth flagging, not worth blocking on.

## 7. Verdict

**approve.**

Conditional on move #4 shipping with the drafted text (or close to it). If move #4 slipped to a follow-up, the loop-1 objection re-fires unchanged.
