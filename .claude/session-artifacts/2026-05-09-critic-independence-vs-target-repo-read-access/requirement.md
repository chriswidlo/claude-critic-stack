# Requirement classification

## Primary label
investigation

## Default frame (from label)
Frame downstream steps around: "what would we do differently if we knew how deep target-repo grounding already runs, and at what depth does it stop being independence-safe?" — the diagnosis must point to a decision, or the question is decorative.

## Known frame bias
Investigation framing tends toward research theater — producing a thorough map of current target-repo touchpoints without committing to a preserve/restrict/isolate/formalize choice. Guard against a deliverable that is all diagnosis and no decision rule.

## Secondary label
refactor — the user is also implicitly asking whether the current independence model (minority-veto + parallel + lens separation, *not* information isolation) should be restructured without changing observable critic behavior.

## Alternative classification
extend — would become primary if the user commits to "add an information-isolation primitive to the panel" rather than "diagnose first." The current wording ("how should we approach this trade-off") keeps it diagnostic; a decision to add isolation flips it to extend (or replace, if isolation supplants minority-veto as the independence mechanism).

## User's framing words — flags
- "Are we compromising the independence" — presumes a defect exists; diagnosis-shaped, not decision-shaped.
- "introducing the option for critics ... to read the destination/target repo" — presumes the option is new/optional, when prior context (`Explore`, `critique-prep`, `critique-start`) suggests it may already be load-bearing. If grounding is already pervasive, the real label may be `replace` (swap the current implicit-grounding model for an explicit one), not `investigation`.
- "recommend an approach (preserve, restrict, isolate, or formalize)" — pre-enumerates the solution space; the workflow should not accept this menu uncritically. A fifth option ("accept correlated grounding as a feature, drop the independence claim") belongs on the table.

## Gaps to resolve in reframe (step 2)
- What threat model is "independence" defending against? (Correlated lens error from shared priors? Target-repo author influence? Sycophancy to existing code?) The recommendation depends on this.
- Is the panel's job to critique *the design question* or *the target repo's fit for the design*? These have different independence requirements.
- What's the failure mode that triggered this question — an observed correlated-approve event, or a theoretical concern?
- Does "independence" here mean inter-lens independence, or independence-from-target-repo-narrative? The current stack addresses the first; the question seems to be about the second.
