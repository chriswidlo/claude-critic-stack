# Product-lens critique — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Lens.** Product / user-surface.
**Reads.** [candidate.md](../candidate.md), [frame.md](../frame.md), [challenges.md](../challenges.md), [scope-map.md](../scope-map.md), three distillations, [README.md](../../../../README.md).

## 1. User-visible consequence

A first-time human reader (forker, evaluator, or maintainer-six-months-from-now) opens [README.md](../../../../README.md), reads four paragraphs that name "12 steps / 10 agents / three-lens panel," reads a one-sentence audience declaration that says *"this README is for the maintainer and Claude,"* reads a gap statement, and is then handed off to two docs — one operator-dense ([CLAUDE.md](../../../../CLAUDE.md)) and one layout-only ([.claude/session-artifacts/README.md](../../README.md)) — neither of which answers Heilmeier's *"what are you trying to do, in absolutely no jargon, and who cares?"*

The user-visible delta vs. today: front-door correctness improves; front-door *purpose-in-plain-language* does **not** improve. The current README's *Philosophy (two sentences)* at lines 35–37 is the only Heilmeier-grade content in the artifact, and the candidate explicitly leaves it untouched while pointing the new audience declaration *at* it. Reader's experience on day 1: more accurate, equally jargon-dense at the load-bearing moment.

## 2. Commitments implied

- **An on-record audience declaration.** A README that says *"this is for the maintainer and Claude"* is a contract with future readers. Reverting it is a louder edit than adding it would have been originally.
- **CLAUDE.md as the de facto human-onboarding surface for the next 6–12 months.** The candidate's correctness argument depends on CLAUDE.md being readable by the declared audience. The day this ships, CLAUDE.md is operator-dense, and the README has just told readers it is the workflow doc.
- **A trigger condition that has no observation mechanism.** A commitment with no observer is a commitment that compounds silently.
- **The *Philosophy (two sentences)* paragraph as the load-bearing Heilmeier-answer.** Because the audience declaration points at it, it now *has* to carry that weight. It currently says *"Books teach what to do. Apprenticeship teaches when. This stack is a very good library with a mandatory dissenting reader attached — not an apprentice."* Good prose, but **not** a Heilmeier answer.

## 3. Migration burden

- **The maintainer.** Six tasks for the PR; underprices the watching-for-the-trigger commitment with no tooling.
- **Claude in future sessions.** New self-referential instruction surface; novel, unaudited.
- **Forker arriving in next 90 days.** Candidate explicitly accepts category-mismatched onboarding. *Conscious acceptance of a bad onboarding is still a bad onboarding.*
- **Anyone bookmarking [workflows/architecture-review.md](../../../../workflows/architecture-review.md) externally.** Explore §5 flagged un-audited. Adaptation: 404, no redirect stub.
- **Whoever ships option (b) or (c) later.** Has to recreate the `workflows/` directory or pick a new home.

The candidate's framing of migration burden as *"nobody downstream has to change anything"* elides the forker case the candidate itself enumerates as an accepted cost.

## 4. Product affordances

**Better:**

- Cannot misroute to a non-existent agent via a deleted file. Correctness floor rises.
- The audience declaration creates a new affordance: future doc-shape decisions have a stated criterion to test against.
- The gap statement gives a forker a fast bounce. *Fast disqualification is a feature for the disqualified reader.*

**Worse:**

- The aspirational forker audience is *explicitly pruned*. The current README's line 17 calls the stack "a structural compensator for known LLM failure modes," which is closer to a Heilmeier answer than anything in the candidate's rewrite. The candidate prunes this capability.
- The reader who wants a Heilmeier-grade *"what is this and why"* gets pointed at *Philosophy (two sentences)* — which the candidate did not rewrite. **A pointer that does not resolve is worse than no pointer.**
- "Two-doc onboarding" is sold as benign because scopes are disjoint. Disjoint scopes are a feature for the reader who already knows which doc to start with; they are a defect for the reader who does not.
- Trigger-based deferral creates a new product affordance ("we'll revisit when forkers arrive") with no observation surface.

## 5. Frame-level objection

**The candidate's frame is *"deletion + redirect + audience declaration ships correctness."* The product-lens frame is *"the README is a contract with whoever reads it, and the contract that ships is: we will not answer the why, but we will tell you we are not answering it."* Those two contracts read very differently from the reader's seat.**

The candidate claims to *address* the frame-challenger's carry-forward objection by adding a one-sentence audience declaration. That is a *minimum-effort acknowledgement*, not an *answer*. The frame-challenger's deeper move ([challenges.md](../challenges.md):29) was that the candidate's notion of "correctness" is **absence of falsehood** while Heilmeier's bar is **presence of purpose in plain language**. The candidate explicitly accepts that it does *not* meet Heilmeier's bar inside the rewritten README — and points at *Philosophy (two sentences)*, which it did *not* rewrite. Reading that paragraph against Heilmeier's questions:

- *"What are you trying to do, in absolutely no jargon?"* — does not answer this; uses "library," "apprentice," "dissenting reader" as Heilmeier-jargon for this domain.
- *"Who cares?"* — not addressed.
- *"If successful, what difference will it make?"* — not addressed.

**The candidate relocates the Heilmeier objection from the front-door framing into the *Philosophy* section and then leaves the *Philosophy* section unrewritten. That is not addressing the objection; that is moving the lump under a different part of the rug.**

A second frame-level objection: the candidate frames the audience question as *"pick one of three audiences and write a sentence."* The challenger's actual claim was that the audience *determines the doc shape*. The candidate picks an audience *and* ships option (a) — internally consistent — but treats the audience declaration as *justification* for the doc shape it had already chosen, rather than as the upstream input. The order of operations is reversed.

## 6. Verdict

**rework.**

What would change the verdict: rewrite the *Philosophy (two sentences)* paragraph (or replace it with a *What is this and why* paragraph) to actually answer Heilmeier's first two questions in jargon-free prose, **as part of the same PR** — not as a deferred follow-up — so the audience declaration's pointer resolves to a destination that delivers what the pointer promises.
