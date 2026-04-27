# Distillation — outside-view (path-discipline regime)

## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on a path-discipline rule (Options A keep+fix, B flip to file-relative, C hybrid leading-slash) in a solo-maintainer repo with LLM agents in the authoring loop. Subagent returned reference-class identification, base rate ~30%, per-option forecasts, and a `Below base rate` verdict for A and C; `Within tolerance` for B conditional on preserving privacy + grep-stability.

## Direct facts
1. [outside-view §0] Subagent declared a canon-retrieval gap: could not access `canon/corpus/` directly and cited the *class* of canon coverage rather than specific passages. (confidence: direct)
2. [outside-view §0] WebSearch was used only to cross-check the reference class, not to set the base rate. (confidence: direct)
3. [outside-view §0] Sources cited: joseparreogarcia.substack.com, datacamp.com, builder.io, code.claude.com best practices. (confidence: direct)
4. [outside-view §5] Forecast for (A) keep+fix+patch slash command: ~35% still-in-force-and->80%-complied at 6 months. (confidence: direct)
5. [outside-view §5] Forecast for (B) flip to file-relative: ~70% complied-with, ~45% probability original purposes (privacy + grep-stability) survive; success-as-defined ~45%. (confidence: direct)
6. [outside-view §5] Forecast for (C) hybrid leading-slash: ~20%. (confidence: direct)
7. [outside-view §2] Stated base rate of success across class: ~30%, flagged as estimate, not measured. (confidence: direct)
8. [outside-view §2] Quoted anchor: solo-maintainer style rules without automated enforcement run "roughly 20–35%" still-complied at 6 months from a 50/50 baseline. (confidence: direct — but anchors themselves are subagent estimates, see Inferred)
9. [outside-view §2] Quoted anchor: rules whose stated justification contains a known-wrong reason "tends to be discarded entirely within 2–3 encounters." (confidence: direct as a subagent claim; underlying empirical basis not cited)

## Inferred claims
1. [outside-view §1] The most predictive reference class is "project-internal authoring conventions in single-maintainer repos enforced socially, with LLM agents in the loop." (confidence: inferred)
2. [outside-view §1] Adjacent classes: personal-wiki link conventions (Obsidian/Logseq), solo OSS `CONTRIBUTING.md` pre-CI, lab-notebook house style. (confidence: inferred)
3. [outside-view §3] The proposal sits *slightly below* base rate for (A), *above* for (B), *below* for (C). (confidence: inferred)
4. [outside-view §3] Naming the wrong reason explicitly is a "+ signal" because most rule-owners never audit. (confidence: inferred)
5. [outside-view §3] A rule whose own tooling (the slash command) violates it is "on borrowed time." (confidence: inferred)
6. [outside-view §3] Three options on the table is itself a signal that the operator is no longer convinced of (A). (confidence: inferred)
7. [outside-view §4] Typical (A) failure mode: rule not formally repealed; compliance bumps then drifts to 50–60% within 2–3 months; at 6 months violations are unnoticed. (confidence: inferred)
8. [outside-view §4] Typical (B) failure mode: "regret cost" — grep-stability lost on day of flip, discovered ~4 months later. (confidence: inferred)
9. [outside-view §4] Typical (C) failure mode: "confusion drift" collapsing to anything-goes within 8 weeks. (confidence: inferred)
10. [outside-view Verdict] What would lift (A) above base rate: a non-optional mechanical gate (pre-commit hook or agent-side validator), not just a slash-command patch. (confidence: inferred)
11. [outside-view Verdict] Reference-class clarification proposed: measure actual 30-day compliance by path-type (artifact vs. prose vs. agent-authored). (confidence: inferred)

## Authority-framed claims
1. "the canon is known to cover (Kahneman/Lovallo on outside view, Tetlock on calibration, and the Claude-Code best-practices ecosystem on CLAUDE.md conventions)" — underlying claim: these authors anchor the methodological reference class. Quote present in output: no. Confidence: unsupported.
2. "if canon has stubs on Fowler / Beck / Hunt-Thomas on convention drift, those are the most relevant" — underlying claim: those authors speak to convention drift. Quote present: no. Confidence: unsupported (subagent itself flags as conditional).
3. "broken windows for documentation" pattern (§1) — underlying claim: one wrong reason poisons the whole rule's legitimacy. Quote present: no (no Wilson/Kelling citation). Confidence: unsupported as authority frame; the underlying mechanism is offered as the subagent's own inference (treat as inferred).

## Contradictions surfaced
- Within (B): "~70% complied-with" vs. "~45% probability original purposes survive" — the option succeeds on compliance but can defeat its own purpose. The subagent did not collapse this; it is preserved as the central tension for (B).
- (A) is *slightly above* base rate on the "+ signals" list (§3) yet the Verdict says (A) is *below* base rate. Resolution per subagent: net slightly below because the natural authoring grain runs against (A) and the slash-command currently violates it. Carry the tension forward — the "above/below" call hinges on whether a mechanical gate is added.

## Subagent's own verdict (verbatim)
"**Below base rate** for Options (A) and (C) as currently scoped. **Within tolerance** for (B) only if the operator first verifies that the privacy and grep-stability properties can be preserved under file-relative paths."

## Gaps the subagent missed
- No specific corpus passage retrieved; canon-librarian distillation should be checked for actual Fowler/Beck/Hunt-Thomas coverage on convention drift before the orchestrator treats §0's "class citation" as canonical.
- Base rate ~30% is explicitly an estimate; no empirical study cited. Orchestrator should treat the percentages as rank-ordering, not point estimates.
- The subagent does not address whether agent-side enforcement (CLAUDE.md rule + agent-prompt validator) is meaningfully different from a pre-commit hook in this stack — relevant because the user's authoring loop is agent-heavy.
- No discussion of the cost of *measuring* current compliance (the proposed clarifying experiment) — feasibility unaddressed.
- Option (B)'s "verify privacy + grep-stability can be preserved" is a precondition but the subagent did not enumerate how to verify it.

## Token budget
~780 tokens.
