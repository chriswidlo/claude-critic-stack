# Product critique v2 — verdict: rework

Persisted from inline return.

## Verdict
rework

## Were the v1 deltas addressed?

1. **Express-capture path:** Yes. `upgrades/inbox/<slug>.md` is real. 10-second `echo > inbox/x.md` works as claimed.
2. **Locking dimensions reduced 4 → 2:** Yes. Slug + promote. Three worked examples test additivity claim and pass.
3. **Day-60 ratio as a surface:** Partial. Script exists and is mechanical, but operator must initiate (pre-commit hook default-OFF). v1 critique asked for "one-line in INDEX" — that variant dropped without naming. Better than v1; not most ambient form possible.
4. **Honor `upgrades/` name:** Yes, honestly. Step-12 uncertainty for rename. Cleanest of four deltas.

## New concerns introduced by v2

1. **Day-1 ~3-hour bash-scripting marathon is itself a friction surface that contradicts the capture-first frame.** Operator's first lab interaction is yak-shaving, not R&D. v2 solves "metadata cost per entry" by pushing complexity into "build-the-tooling-first." Day-1 deliverable is four bash scripts before any R&D content lands. Capture-first promise is contingent on scripts existing — until day 1 hour 3, inbox path has no INDEX-derivation, no lint, no promote. **Different mode of same v1 failure**: v1 made operator pay metadata-tax per write; v2 makes operator pay infrastructure-tax once, upfront. Day-1 is "build the lab," not "write your first observation."

2. **Ratio-script's classification baseline ambiguity.** Day-1 meta-commits load the metric before any content lands. Day-1 ratio after script work: infinite meta:content (4 meta, 0 content). Candidate doesn't say if 3:1 trigger is from day-1 first commit, day-7 freeze, or first content commit.

3. **`SCHEMA.md`, `PROMOTION.md`, `TIMEBOX.md` are referenced but not in deliverables.** Either operator authors them too (v1 problem partially returns), or references break.

4. **Lint optionality is product risk.** Without lint enabled, INDEX could silently miss entries. Pre-commit hook default-off. Chain: `echo` → file exists → INDEX regenerates only if frontmatter well-formed → well-formedness checked only if lint runs → lint runs only if operator opts in. **Four conditional steps between `echo > inbox/x.md` and entry being indexed.** 10-second capture is true at keystroke level, false at durability level.

5. **Self-application has self-supersedes frontmatter contradiction.** Entry's `relates_to` references its own slug. Lint allows; semantically incoherent. The first entry the operator sees, modeling the format, demonstrates a confused self-relation. **Bad teaching example.**

## What the operator experiences day 1 (revised)

1. Reads design entry. Notices self-supersedes frontmatter; pauses on whether to mimic.
2. Spends ~3 hours writing four bash scripts. Not R&D content.
3. Each script-commit is meta. 4 meta : 0 content. Wonders about day-60 baseline.
4. Decides on pre-commit hook on/off (one more decision).
5. Captures first inbox entry. Works in 10 seconds. (Genuinely good.)
6. Tries to retrofit hooks. Wants to reference an existing session-artifact — but session-artifacts don't have slugs. Either promotes session-artifact first (more work) or omits reference.
7. Net: ~3.5 hours infrastructure + 1 trivial inbox capture + 1 partial retrofit. **Lab exists but day-1 labor was not R&D.**

Compared to v1's ~2 hours of meta-file authoring: v2 is *not faster* on day 1. Friction moved from "metadata tax per entry" to "tooling tax once." Better long-run shape; comparable day-1 cost.

## Friction surface (revised)

1. Day-1 ~3-hour bash build-out (NEW).
2. Pre-commit hook on/off decision (NEW).
3. Ratio baseline ambiguity (NEW).
4. Implicit meta-files referenced but not in deliverables (NEW).
5. Self-supersedes frontmatter on model entry (NEW).
6. Capture-first surface durability contingent on lint (NEW, conditional).
7. Slug-references-only-resolve-within-`upgrades/` (NEW).
8. Type-picking (4 starter types) — reduced from v1, still present.
9. INDEX.md regeneration timing unspecified (drifts if not re-run).

## Frame-level objection

**The candidate replaced "metadata tax at every write" with "tooling tax up front" and called the trade pure win.** From product, the trade is more honest (one-time cost, durable surface afterwards) but not free, and v2 over-claims. Real frame question: **does the operator want to spend day 1 writing bash, or does the operator want to spend day 1 retrofitting backlog items?** v2 has chosen "bash first" without naming it as a choice. A capture-first frame, taken seriously, would say: ship *minimum* tooling (just `promote.sh` + manual INDEX) and let the rest accrete as the lab does. Lint and ratio scripts are *operational controls* — defenses against future failure modes, not enablers of present capture. They belong on day 7 or 14, not day 1.

Restated: **v2 is structurally sound but it has imported the operations lens's required-controls into the day-1 critical path, where the product lens would say capture-affordance comes first and instrumentation comes after the first ten entries.** The four-script day-1 list is a multi-lens compromise that no single lens would have asked for in that exact shape.

## What would make this approve

1. **Split the four scripts by day.** `upgrades-promote.sh` (~30 lines) lands day 1. `upgrades-index.sh` lands when >3 entries. `upgrades-lint.sh` lands when >5 entries or before day-7 ratification. `upgrades-ratio.sh` lands by day 30. **Day-1 deliverable: one script + capture surface + first retrofit.**
2. **Fix or remove self-supersedes frontmatter.** Reference v1 in prose without slug, or omit `relates_to` entirely.
3. **Resolve implicit-meta-files question.** Either name `SCHEMA.md`, `PROMOTION.md`, `TIMEBOX.md` as explicit deliverables (accepting meta growth), or inline content into the candidate-as-first-entry.
4. **Specify the ratio baseline.** From day-1 first commit, day-7 freeze, or first content commit? Pick one in script docstring.
5. **Default lint pre-commit hook ON, with explicit opt-out.** Capture-first durability requires lint; opt-in defeats it.

Verdict moves to approve when day-1 is "write promote script, capture in inbox, retrofit one item" — not "build four scripts before doing R&D." Capture-first frame requires lab capturable on day-1 hour 1, not day-1 hour 4.
