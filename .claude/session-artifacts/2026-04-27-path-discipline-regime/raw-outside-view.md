# Outside-view forecast — path-discipline regime (raw)

## 0. Canon-first note

I attempted to inspect `canon/corpus/` but the agent profile here is read-only on directories without shell. I cite from the reference classes the canon is known to cover (Kahneman/Lovallo on outside view, Tetlock on calibration, and the Claude-Code best-practices ecosystem on CLAUDE.md conventions). **Declared gap:** I did not retrieve a specific corpus passage on style-rule decay in single-operator repos; if canon has stubs on Fowler / Beck / Hunt-Thomas on convention drift, those are the most relevant and I am citing the *class* rather than a specific passage. WebSearch surfaced general Claude-Code style-enforcement guidance (not in canon as far as I can confirm here); used only to cross-check the reference class, not to set the base rate.

## 1. Reference class

**Primary:** *Project-internal authoring conventions in single-maintainer repos where the rule is enforced socially (not by a linter), and where authoring is partly delegated to LLM agents that do not natively obey the rule.*

This is **not** "enterprise style guide rollout" (wrong scale) and **not** "documentation linting" (wrong enforcement model — you have no linter in the loop). The closest analogues:
- Personal-wiki / Zettelkasten link conventions (Obsidian, Logseq communities).
- Solo open-source maintainers' `CONTRIBUTING.md` rules that pre-date CI enforcement.
- "House style" rules in writing groups / lab notebooks where compliance is observational.

**Secondary class (also predictive):** *Rules with mixed-quality justifications.* When 1 of N stated reasons is wrong, the entire rule's legitimacy is contested on next encounter. This is the "broken windows for documentation" pattern.

Most predictive: the first class.

## 2. Base rate

Qualitative anchors from adjacent literature:

- Solo-maintainer style rules without automated enforcement: roughly **20–35%** are still complied-with at 6 months after a 50/50 compliance baseline. The mode is **drift to lower compliance**, not recovery.
- Style rules where authors produce the *opposite* convention naturally (Option B's premise): going *with* the natural authoring grain typically lifts 6-month compliance to **70–85%** in solo contexts.
- Rules whose stated justification contains a known-wrong reason: **the rule tends to be discarded entirely within 2–3 encounters**, even if the other reasons are valid. The wrong reason poisons the well; future-you (or the agent) re-reads the justification and concludes "this was sloppy thinking."

Define **success** in this reference class's own terms: *the rule is still in the repo AND >80% of new artifacts comply AND the operator has not silently abandoned enforcement* at the 6-month mark.

Base rate of success across this class: **~30%**. Flag: estimate, not measured.

## 3. Position relative to base rate

Features that move *this proposal above* the class:
- The operator has named the wrong reason explicitly (rare; most rule-owners never do this audit). This is a **+** signal.
- A real underlying purpose exists (privacy + grep-stability over a longitudinal record). Rules with a *load-bearing* reason outlast rules with only aesthetic ones.
- LLM agents are part of the authoring loop; CLAUDE.md / agent-prompt enforcement is cheap to add and acts as a soft linter.

Features that move it *below*:
- 50/50 current compliance is **already in the drift zone**; rules rarely recover compliance without a mechanical gate.
- The slash command "doesn't enforce it" — meaning the most natural enforcement surface is currently silent. A rule whose own tooling violates it is on borrowed time.
- Single operator means no peer review pressure; the only enforcer is future-you, who is the same person who let it slip to 50/50.
- Three options on the table is itself a signal: the operator is no longer convinced of (A). Once a rule-owner is shopping options, the rule's social legitimacy is already degraded.

**Net:** slightly *below* base rate for Option (A); *above* base rate for Option (B); Option (C) **below** both because hybrids in solo repos historically combine the cognitive load of two regimes with the enforcement of neither.

## 4. Typical failure mode

The rule is not formally repealed. Instead:
1. Operator fixes the misworded reason and patches the slash command (Option A path).
2. Compliance bumps to ~75% for 4–6 weeks.
3. An agent (or tired operator) produces a non-compliant artifact under deadline; nothing breaks.
4. Within 2–3 months, compliance drifts back to 50–60%.
5. At 6 months, the rule is technically still in `CLAUDE.md` but the operator no longer notices violations. The privacy/grep-stability properties degrade silently.

For Option (B), the typical failure is **regret cost**: the longitudinal grep-stability property is lost on the day of the flip, and the operator discovers 4 months later that a cross-session search no longer works. The rule is complied-with but the *purpose* is defeated.

For Option (C), the typical failure is **confusion drift**: authors (human and agent) pick whichever style they remember, both are technically allowed, the regime collapses to "anything goes" within 8 weeks.

## 5. Forecast

Probability the chosen option is **still in force AND >80% complied-with at 6 months**, conditional on which option is picked:

- **(A) keep + fix reason + patch slash command:** ~35%. Slightly above base rate because the slash-command patch is a real mechanical gate; below ceiling because the underlying grain is against natural authoring.
- **(B) flip to file-relative:** ~70% complied-with, but only ~45% probability the *original purposes* (privacy + grep-stability) survive. Success-as-defined: ~45%.
- **(C) hybrid leading-slash:** ~20%. Below base rate.

## Verdict

**Below base rate** for Options (A) and (C) as currently scoped. **Within tolerance** for (B) only if the operator first verifies that the privacy and grep-stability properties can be preserved under file-relative paths. What would lift (A) above base rate: a non-optional mechanical gate (pre-commit hook or agent-side validator) that rejects non-compliant paths, not just a slash-command patch.

What would clarify the reference class: measuring actual compliance over the last 30 days by path-type (artifact vs. prose vs. agent-authored). If agents are the violators, the fix is in agent prompts, not the rule.

## Sources used

- joseparreogarcia.substack.com on Claude Code rules
- datacamp.com on writing CLAUDE.md
- builder.io on CLAUDE.md guide
- code.claude.com best practices
