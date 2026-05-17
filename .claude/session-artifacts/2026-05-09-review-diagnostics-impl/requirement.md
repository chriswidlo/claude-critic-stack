# Requirement classification

## Primary label

`investigation`

## Default frame (from label)

"What would we do differently if we knew the answer?" — every review finding (AI-blindness validation, regression evidence, SOTA gap) must map to a concrete downstream action (revert, patch, queue follow-up, accept-as-is) or be dropped as decorative.

## Known frame bias

**Research theater.** The workflow can produce a thorough-looking critique of the shipped diagnostics layer that surfaces no actionable change, generating artifacts that justify the review rather than altering the system under review. Watch for: critic objections that are interesting but unactionable; SOTA opportunities that are listed without prioritization; regression checks that report "no drift detected" without specifying what would have constituted drift.

## Secondary label

`extend` — the review brief explicitly enumerates SOTA opportunities (per-step duration, cost-in-$, cross-session aggregation, privacy mode, parser-accuracy fixes) that, if any are queued as follow-up work coming out of synthesis, make the operative label additive-to-the-shipped-primitive rather than purely diagnostic.

## Alternative classification

`extend` — becomes primary if the user's actual ask is "decide which SOTA upgrade ships next" rather than "validate what shipped." Signal: synthesis is expected to *name* a specific follow-up upgrade rather than merely flag candidates. Reframe under `extend` and run scope-mapper against the diagnostics surface as an existing primitive whose contract may grow.

A third candidate, `refactor`, is weaker but worth flagging: if the review concludes the shipped layer needs structural rework without behavior change (parser rewritten for nested-subagent accuracy, hook stderr-suppression hardened), the implementation-fix half of the output is `refactor`-shaped. It does not displace the primary because the review itself is investigative; refactor would describe a *follow-up* session, not this one.

## User's framing words

- "this entry is now the subject of a follow-up 12-step run-through-repo, not a forward-looking proposal" — presumes investigation
- "validate that claim, find regressions, and surface SOTA improvements" — investigation framing on the first two clauses; extend framing on the third
- "Run the 12-step adversarial review against the just-shipped diagnostics implementation" — review = investigation
- "identify SOTA upgrades worth queueing as follow-up work" — explicitly defers extend-decisions to a later session, which keeps this session in investigation territory

What would change the classification: if the user, mid-session, asks the workflow to commit to a specific SOTA upgrade rather than queue candidates, the label flips to `extend` and step 7 (scope-mapper) treats the diagnostics layer as the primitive being grown.

## Gaps

- Is the synthesis expected to *rank* the SOTA candidates or merely list them? Ranking pulls toward `extend`; listing keeps `investigation`.
- Is reverting any part of the shipped implementation in scope, or is the shipped state treated as a floor? If the floor is fixed, the investigation cannot produce a `replace` outcome even if a critic argues for one.
- Does the operator want the regression check to *block* further upgrade work until findings are addressed, or is it informational? Blocking pulls toward a decision-shaped output that strains the `investigation` frame.
- The dogfooding loop (this review produces diagnostics on itself) is unspecified as an input to the review — is self-observation evidence the workflow should weigh, or out-of-scope?
