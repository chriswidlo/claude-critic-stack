# Frame — ark-mono phantom fixture

## Revision 1

### How the user posed it

> Item 5 of the cleanup punch list needs resolution: regression scenario was supposed to produce an exemplar; exemplar dir is empty; two top-level docs cite different example slugs, neither real. Pick (a) run-and-promote, or (b) doc-substitute.

### What this question is implicitly optimizing for

**Closure of a punch-list row.** The frame inherited from the parent plan
is "make item 5 go green." Both options on the table are scoped to that
goal. (a) closes the row by producing the missing artifact; (b) closes
the row by editing the docs that cite it.

This optimization is shallow. It treats the punch-list as the unit of
work and item 5 as a discrete bug to retire. Under that frame, (b) is
strictly cheaper and (a) is over-investment.

### One alternative optimization the user did not name

**Test-discipline credibility of the stack.** The repo claims, in
`tests/regression/ark-mono-connector-routing.md`:113-117 and in
`.claude/session-artifacts/exemplars/.keep`'s implied promotion contract,
to have a regression discipline. That claim is currently unbacked: zero
exemplars exist, the one written scenario has never been executed against
the current agent set. Every additional day the empty `exemplars/` dir
sits in git is a quiet erosion of that claim.

Under this frame, the unit of work is not "punch-list row 5" but
"first execution of the declared regression discipline." (a) is the only
option that addresses it; (b) is a paper-over.

### A third optimization, between the two

**Triage of operator attention.** Items 6–13 of the punch list are
unstarted. If operator attention is the binding constraint and item-5's
documentation symptom (two docs disagree on an example slug) is the
*observable* harm to readers, then closing the doc-correctness bug fast
and deferring the regression-discipline question to its own session is
the correct sequencing — not because (b) is the "right" choice but
because conflating two questions in one session is the wrong unit of
work.

This is the third option the classifier flagged (its "split the work"
gap): harmonize word-order now, file the exemplar question separately.

### Frame the orchestrator will carry forward

**The decision is not (a) vs (b). The decision is which frame the
operator wants this session to be in:**

- **Frame F1 — punch-list closure.** The session is about retiring a
  row. Optimize for cost-to-close. Recommends (b) or the third option
  (split-and-defer). Test-discipline questions are out of scope.
- **Frame F2 — regression-discipline credibility.** The session is
  about whether the repo's claim to have regression infrastructure
  is real. Optimize for "exemplar exists by end of session."
  Recommends (a). Doc-substitution is a downgrade.
- **Frame F3 — triage.** The session is about correctly sequencing
  this item against items 6–13. Optimize for operator-attention
  preservation. Recommends the split-and-defer option. Both (a) and
  (b) as posed are wrong unit of work.

**Bias from the classifier:** investigation; surface the frame question
itself rather than pick a tactic.

**The orchestrator's stance going into steps 3–8:** treat all three
frames as live. Do not collapse to F1 because the punch-list is the
visible artifact. Do not collapse to F2 because the parent plan
softly leans (a). The reference-class search and the canon search
should produce data on which frame the operator's repo culture
actually prefers — not data confirming any single one.

### Naming the implicit assumption

The parent plan assumes the regression scenario is runnable and
would produce a passing exemplar today. If it would *fail* — i.e.,
the current agent stack regresses on one of the seven acceptance
criteria — then (a) does not produce an exemplar; it produces a
new punch-list item. F2's argument depends on that assumption
holding. Steps 3–5 should surface base rates on this kind of
"first execution of a declared but unrun test."
