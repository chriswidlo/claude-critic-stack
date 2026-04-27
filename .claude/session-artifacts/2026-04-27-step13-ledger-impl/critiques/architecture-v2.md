# Critic — architecture lens, loop 2 on candidate-v2

## What changed
HTML-comment marker added (✓). Decision definition tightened to "bulleted items under Recommendation/Uncertainties" (✓). Cross-link from CLAUDE.md step 13 to the schema section (✓).

## Frame-level posture
The coupling concern is now mitigated by the HTML-comment marker (the same convention the format-only-state-transition-gate entry uses). One source-of-truth is named; downstream sites are tagged as readers. This is the right architectural shape.

## Residual concerns (non-blocking)
- The schema section is large (~50 lines). If it grows further (a fourth ratio, a fifth count), it will dominate [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md). Worth a future-edit watch: if the schema doubles, consider moving it to its own file with a stable include-style reference.
- The decision count depends on synthesis structure not changing. CLAUDE.md step 12's bulleted list is now load-bearing in two senses (operator-facing structure + ledger-counting source). A change to step 12 must update step 13 in the same commit. Worth a CLAUDE.md sentence; not a blocker.

## Verdict
**approve.**
