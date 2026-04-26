# Requirement classification

**Question:** Should the claude-critic-stack repo adopt Context7 MCP, and if so in what form?

## Primary label
`extend`

## Default frame (from label)
"Does Context7 belong as an extension to existing primitives (canon-librarian, canon-refresher, outside-view), or as a separate primitive (new subagent / Skill)? Extension must expand surface area monotonically without weakening canon-first discipline."

## Known frame bias
The `extend` framing pushes toward overloading existing primitives. Canon-librarian could fracture if it gains a second retrieval backend with different freshness, trust, and anti-confirmation semantics than the curated corpus.

## Secondary / alternative label
`new` — shapes C (dedicated `library-docs` subagent) and E (Skill outside the workflow) are net-new capabilities, not modifications of existing primitives. Becomes primary if the chosen shape is C or E.

A third reading: `investigation` — if the answer is shape A ("do nothing pending more evidence"), the question collapses into a base-rate / frequency question.

## Framing-words audit
- "adopt … and if so in what form" — neutral.
- B and D phrasings presume `extend`.
- C and E phrasings presume `new`.
- A presumes `investigation`.
The question is shape-pluralistic; no single label is smuggled in.

## Named gaps (must be answered before generation)
1. **Base rate:** how often do design questions in this stack actually hinge on library-specific API surfaces?
2. **Trust model:** does Context7 output count as canon (curated, contradiction-required) or as web (currency-only)?
3. **Failure mode:** if Context7 returns stale/wrong info, who catches it? Canon has contradicting-passage rule; Context7 does not.
4. **Premise conflict:** shape E presumes ad-hoc code work happens in this dir, but CLAUDE.md states cwd is "deliberately not a target codebase."
5. **Cost/latency budget:** per workflow run if Context7 is invoked in steps 3–5.
