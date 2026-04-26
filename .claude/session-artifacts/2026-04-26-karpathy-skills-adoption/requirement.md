## Primary label
extend

## Default frame (from label)
Frame the decision as: does adopting karpathy-skills (or fragments of it) expand the surface area of the user's existing global `CLAUDE.md` monotonically, or does it duplicate/conflict with primitives already in the default system prompt and the global `CLAUDE.md`? Treat the prior recommendation as the candidate extension and ask which of its five clauses survive a subsume/replace test against existing primitives.

## Known frame bias
Extend-framing tends to overload the existing primitive (global CLAUDE.md) by accreting "harmless" additions until it fractures into incoherent or contradictory guidance — exactly the failure mode that motivated the prior recommendation to drop "1–2 lines" rather than the whole file.

## Secondary label
investigation — the user is asking the workflow to validate a prior recommendation, which is partly a "did we get this right?" retrospective on an already-formed decision.

## Alternative classification
investigation becomes primary if the user's actual ask is "audit my reasoning trace" rather than "tell me what to install." Signal: if no setup change is on the table regardless of outcome, it is decorative and the label flips.

## User's framing words
- "validate its own prior writeup and recommendation" — presumes the prior recommendation is the unit of analysis (anchors to extend/refactor of an existing decision, not a fresh `new` decision).
- "should the prior recommendation stand, get rewritten, or get replanned?" — explicitly frames as a meta-validation, biasing toward extend/refactor of the prior artifact rather than re-deciding from scratch.
- Clause 4 "Optionally drop 1–2 lines…" — presumes extension of the global `CLAUDE.md` is the live option.

What would change the classification: if validation surfaces that the karpathy plugin's *packaging pattern* (not its content) is the real artifact under consideration, the label flips to `new` (build/adopt a plugin-distribution capability the user does not currently have). If validation concludes "do nothing," it collapses to `investigation`.

## Gaps
- Is the user evaluating the *content* (four principles) or the *packaging mechanism* (marketplace plugin as a conventions-distribution channel)? The prior recommendation hints the latter is the novel value but does not commit.
- What is the user's current global `CLAUDE.md` actually saying? Without its contents, the subsume/replace test in step 7 cannot be run rigorously.
- Is there a population of repos where the user wants conventions applied uniformly (which would make the plugin-packaging angle load-bearing), or is this a single-machine setup (which makes packaging irrelevant)?
- Does "validate" mean "confirm" or "stress-test"? The workflow assumes the latter; if the user wants the former, the critic-panel will feel adversarial-by-design.
