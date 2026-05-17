# Frame

## Revision 1

### The user's framing (verbatim, as captured in question.md)

> "Run the 12-step adversarial review against the just-shipped diagnostics implementation in this repo: validate the AI-blindness claim, surface regressions or quality risks in what shipped, and identify SOTA upgrades worth queueing as follow-up work."

The review brief in the upgrade entry decomposes this into four headings:

1. Workflow pollution audit (AI-blindness)
2. Regression check (did instrumentation change observable behavior of the 12-step workflow)
3. Degradation check (perceived speed, clutter)
4. SOTA opportunities (dataset richness, speed, accuracy)

### What the user is implicitly optimizing for

**Validation of a shipped artifact, plus a productive backlog.** The implementation has already landed; the operator wants the workflow to (a) confirm the AI-blindness safety property holds, (b) catch any latent regressions before the next session relies on the diagnostics, (c) hand back a list of next-tier upgrades so the work feels generative rather than terminal. Implicit reward: "we shipped something rigorous, here's a queue of next steps."

This is a *did-we-build-it-right* objective. It assumes the right thing was built and asks whether the build is sound.

### Alternative optimization (not what the user named)

**Instrument-fit.** Optimize for "is the layer measuring what the operator's diagnostic questions actually need" — the *did-we-build-the-right-thing* objective. The catalyst section of the upgrade entry names four operator questions:

- "Where did the 10 minutes go?"
- "What cost the most tokens?"
- "Are critics balanced?"
- "Did one agent dominate?"

The shipped instrumentation captures: duration_seconds (one number), tokens_by_agent, tool_calls, verdicts, loops. Map the questions to the instrument:

| Operator question | Shipped instrument answers it? |
|---|---|
| Where did the 10 min go? | Partial — total only, no per-step or per-phase breakdown |
| What cost the most tokens? | Yes — by_agent map answers this directly |
| Are critics balanced? | Yes — tokens by `critic-architecture` / `-operations` / `-product` |
| Did one agent dominate? | Yes — same source as above |

Three of four operator questions are answered. The fourth — "where did the time go" — is the one the catalyst opened *with*, and the instrument answers it least well. That is a frame-level signal: the layer was designed against the easy three-quarters of the question set, and the hardest quarter (per-step or per-phase duration) is named as a *future SOTA* rather than a *v1 requirement*.

Re-framing the review under instrument-fit forces the panel to ask: "is shipping with the load-bearing question half-answered acceptable, or did we ship a v1 that retires the catalyst question prematurely?"

### A second reframe worth surfacing

**Dogfooding-as-confounder.** The review session is itself an instance of the workflow being measured. That is novel, but it is not necessarily a clean signal. A review-session has no real critic-veto loop (the loop count is bounded by what *this* design needs, not by what a representative session needs), shorter agent prompts (the design doc is small), and no production-style time pressure. Its diagnostics will *look* like data but will not be representative of the workflow's steady-state cost. A reviewer who quotes this session's metrics as evidence that "the diagnostics layer measures workflow cost reliably" is overfitting to a sample of one, where the sample was drawn from the easiest possible workflow run.

This re-frame is narrower than instrument-fit but matters because the upgrade entry positions the dogfooding as a feature ("the implementation will measure its own first review"). The panel should treat that positioning skeptically.

### What this frame holds open

- The shipped state is treated as a floor only if the panel agrees it should be. The frame does not pre-commit to a no-revert policy. If a critic argues for partial revert (e.g., remove the verdict-regex from `metrics.json` until tightened), the synthesis must address it on its merits, not dismiss it because "shipped is shipped."
- "AI-blindness" is a load-bearing property in the upgrade entry. The frame keeps it load-bearing for the panel — a critic that finds *any* leak path (hook stderr, parse error in synthesis, env-var contamination) is producing a frame-level objection, not a lens-specific one.
- The SOTA list in the upgrade entry is *not* the panel's agenda. The panel may surface upgrades the operator did not name; it may also reject upgrades the operator did name as not-yet-justified.

### Frame bias acknowledgment

The classifier flagged "research theater" as the bias the `investigation` label carries. The reframe inherits that risk. Counter-pressure: synthesis must produce at least one finding that maps to a *concrete* downstream action — patch, revert, queue with priority, or accept-with-named-risk. A synthesis that lists findings without mapping them to actions has fallen into the research-theater trap and should be rejected by the panel.
