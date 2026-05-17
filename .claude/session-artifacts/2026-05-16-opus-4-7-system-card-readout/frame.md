# Frame

## Revision 1 — orchestrator's reframe (2026-05-16)

### The user's framing
*"Produce the deepest possible adversarial readout of the Claude Opus 4.7 System Card, then propose a concrete change-set against this repo."*

This framing implicitly optimizes for **completeness of risk-dossier coverage** — read every section, quote every number, decide every agent. It treats the system card as a load-bearing document that should reshape the repo.

### What is the user implicitly optimizing for?
- **Audit-grade traceability.** Every conclusion in `synthesis.md` should resolve to a verbatim quote with `(§X.Y, p.NN)`.
- **Decision-bearing change-set.** Phase 6 produces a concrete proposal, not a survey.
- **Independence from vendor narrative.** Adversarial reading; "do not be agreeable" applies to the system card itself.
- **Process-discipline showcase.** Running the workflow under `SHADOW_PANEL=1` exercises the triangulation primitive on a high-stakes target.

### Alternative reframe — "operator update under vendor self-report uncertainty"
A weaker but more honest framing: **the Opus 4.7 System Card is a vendor-published artifact and we cannot independently verify most of its claims.** What we can do is:

1. Inventory the vendor's claims (zone reads).
2. Identify which claims, *if true as stated*, would change how this repo's agents and orchestrator should behave.
3. Identify which claims have third-party verification (UK AISI, external red teams cited in the card) versus which rest only on Anthropic's internal evals.
4. Build a change-set that is robust to the most likely failure mode of vendor self-reports: *over-claim of safety, under-disclosure of caveats.*

Under this reframe, the readout is not "what did Anthropic say" but "**what should we change** *given that Anthropic said this and we cannot fully verify it*." The unit of progress shifts from coverage to *operator action*.

### Where the user's frame is right
- The system card is genuinely the best primary source available about model behavior under conditions a typical operator cannot reproduce (helpful-only snapshots, white-box internals, evaluation-awareness probing).
- Adversarial reading + verbatim citation discipline genuinely defends against the "marketing-summary" failure mode.

### Where the user's frame is at risk
- **Coverage bias.** Reading "every section" is expensive; if a finding does not bear on a repo decision, it is dead weight in `synthesis.md`. The classifier flagged this as `research theater` — a real risk here.
- **Vendor-anchor risk.** Even adversarial reading of a single vendor's document anchors the readout to that vendor's framing. The outside-view step is the only counterweight; it must do real work, not be a perfunctory gesture.
- **Asymmetric verifiability.** Claims about *capabilities* are partially verifiable by operators (we run benchmarks). Claims about *alignment* and *welfare* are largely not. The change-set should weight these differently — a 4.7 capability claim can hit a benchmark adapter; a 4.7 welfare-self-report claim can only update a stance.

### Operating bias for the rest of the workflow
The orchestrator commits to the user's framing **modified by** the alternative reframe in this revision: zone-readers will be told to verify *invariants tied to candidate repo changes* (per the classifier's `research-theater` mitigation), not to "find every interesting fact." The Phase 5 `four-storylines.md` will be drawn from claims that *would change operator behavior*, not from the most quotable claims in the document.

### Constraint inherited from the user's prompt
- 4.7 is treated as a **fresh baseline.** No 4.6 delta. No "what changed since" framing.
- This makes Phase 3 outside-view do extra work: it must supply the base-rate counterweight that a 4.6 delta might otherwise have provided.

### Non-goals (named to bound scope)
- Reproducing Anthropic's evaluations.
- Auditing the methodology of the cited third-party assessors.
- Speculating on Mythos Preview (referenced repeatedly in the 4.7 card but out of scope per the user's "4.7-only" constraint).
- Proposing changes to the repo for which the system card is *not* the load-bearing evidence.
