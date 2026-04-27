## Primary label
investigation

## Default frame (from label)
"What would we do differently if we knew the answer?" — the orchestrator must
treat this as a decision between two pre-named options whose tradeoff is
test-discipline integrity vs. doc-correctness cost; downstream steps should
surface which frame the repo is actually optimizing for, not pick a tactic.

## Known frame bias
Research theater — the workflow can spin on "which option" while the real
question (does the repo's regression discipline mean anything if no scenario
has ever been executed?) goes un-named. Ritualizing the choice without
forcing the frame question wastes the pipeline.

## Secondary label (if any)
new — option (a) is functionally the creation of the first real exemplar
fixture; option (b) is a doc patch. If the orchestrator collapses to (a),
the work is `new` (build the missing capability the test was designed to
produce). The user is asking which kind of work this is, which is itself
the investigation.

## Alternative classification
new — would become primary if the user had already decided to run the
scenario and was asking how to structure the exemplar. They have not;
they are asking which option to take. Hence investigation, not new.

## User's framing words
- "Should we pick (a) or (b)?" — binary framing presumes the resolution
  space is exhausted by the two options. A third option (harmonize doc
  word-order now, defer the exemplar/substitute choice as a separate item)
  is not on the table but is structurally available; the punch-list plan
  itself notes the word-order divergence is a separate bug.
- "the regression scenario ... was supposed to produce an exemplar" —
  presumes the scenario is runnable and would in fact produce a passing
  exemplar today. Unverified.
- The parent plan's "soft preference for (a)" — must not anchor the
  classifier or the orchestrator. Treat as one data point.

## Gaps
- Has the regression scenario at tests/regression/ark-mono-connector-routing.md
  ever been executed end-to-end against the current agent set? If no, (a)
  carries unbounded scope risk (a failing run becomes a new punch-list item,
  per the plan's own caveat).
- Are the example slugs in CLAUDE.md and the session-artifacts README load-
  bearing (readers actually click them) or illustrative (readers parse the
  shape only)? Determines whether substituting any real session in (b) is
  acceptable or whether the example must be the canonical exemplar.
- Is operator attention the binding constraint? If the remaining punch-list
  items 6–13 are higher-leverage, (b) is the correct triage move regardless
  of test-discipline arguments. Not stated.
- Third option not enumerated: split the work — fix the word-order
  divergence and substitute an existing session now (cheap), and file a
  separate item to run the regression and promote a real exemplar later.
  This is the plan's step 4 ("either way") elevated to a primary option.
