# Question under review

Are we compromising the independence of our critic panel by introducing the option for critics (and earlier workflow steps) to read the destination/target repo? How should we approach this trade-off, and how deep does the influence of target-repo grounding already go in the current stack?

## Constraints / context

- The stack is `claude-critic-stack`; critics are the three lens agents (`critic-architecture`, `critic-operations`, `critic-product`) plus their Sonnet shadows.
- Target-repo access today shows up at least in: step 5 (`Explore`) when a target codebase is provided, the `critique-prep` / `critique-start` skills which explicitly route a target path into the session, and possibly via inputs/handoffs visible to later steps.
- Independence in the panel is currently asserted via minority-veto, parallel invocation, and lens separation — not via information isolation.
- Path discipline and the strict separation between "design question repo" and "target codebase" is load-bearing per CLAUDE.md.

## What the user is asking the workflow to do

Diagnose the current depth of target-repo influence on the critic panel, decide whether that influence threatens lens independence, and recommend an approach (preserve, restrict, isolate, or formalize) — with evidence drawn from a thorough read of the repo.
