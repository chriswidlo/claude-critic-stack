# Distillation — outside-view

## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on deleting a stale workflow doc and redirecting the README to two existing authoritative docs ([CLAUDE.md](../../../../CLAUDE.md) and [.claude/session-artifacts/README.md](../../../README.md)) with a "unify later" deferral. Subagent declared a canon-first gap, fell back to WebSearch, returned a split verdict: within tolerance on deletion, below base rate on deferral.

## Direct facts
1. [outside-view §0] Subagent could not enumerate `canon/corpus/` with its tool surface and explicitly declared the canon gap before using WebSearch. (confidence: direct)
2. [Docsie 2025, quoted §4] "When official docs fall behind, teams build their own stopgaps; these fragment knowledge and reintroduce drift." (confidence: direct)
3. [outside-view §3] The stale doc references a non-existent agent (`critic`), making it actively misleading rather than merely incomplete. (confidence: direct — fact about the artifact under review)
4. [outside-view §3] The two redirect targets have disjoint scope: [CLAUDE.md](../../../../CLAUDE.md) is behavioural/authoritative; [.claude/session-artifacts/README.md](../../../README.md) is layout-only. (confidence: direct)

## Inferred claims
1. [outside-view] Deletion of a stale doc + redirect to authoritative source succeeds as a correctness move ~80–90% of the time in the reference class. (confidence: inferred — subagent calls these "order-of-magnitude" estimates calibrated from practitioner sources, not published statistics)
2. [outside-view] "Point readers at two docs instead of writing a unified one" works as onboarding ~40–60% of the time in small projects; tolerable when scopes are disjoint and the README names what each covers; silently fails when readers must mentally join them to act. (confidence: inferred)
3. [outside-view] "Defer the unified doc" is actually completed within 6 months ~20–35% of the time in small/solo projects; modal outcome is 1–3 years of known-stale-but-not-wrong backlog state. (confidence: inferred)
4. [outside-view] The current deferral has no trigger condition, no owner-different-from-author, and no expiry — textbook shape of a deferral that doesn't get done. (confidence: inferred)
5. [outside-view] [CLAUDE.md](../../../../CLAUDE.md) is agent operating instructions, not a human workflow tutorial; pointing humans at it as the authoritative workflow doc is a category mismatch. (confidence: inferred — this is the subagent's framing critique)
6. [outside-view] Dominant failure mode is silent: deferred doc never written, the pointer becomes the de facto workflow doc, new readers form partial mental models, surfaces as confused contributions or repeated chat-explanations. (confidence: inferred)
7. [outside-view] Secondary failure mode: a third stale derivative (comment, gist, pinned chat) gets written to fill the gap, recreating the drift the cleanup was meant to remove. (confidence: inferred — supported by Docsie quote)
8. [outside-view] Trigger-based deferrals complete materially more often than time-based ones in small-project settings. (confidence: inferred — asserted, no source cited inline for the rate differential)
9. [outside-view] Naming the gap explicitly in the README ("there is no standalone human-readable workflow tutorial yet; …") is "the single most reliable mitigation in the doc-drift literature." (confidence: inferred — claim about the literature without a specific citation)

## Authority-framed claims
1. "Parnas & Clements ('A Rational Design Process: How and Why to Fake It,' 1986); Knuth on literate programming; Cunningham's original technical-debt metaphor (1992)" — underlying claim: these are canonical references that *should* be in scope for documentation drift / deferral. Quote present in output: no. Confidence: unsupported (named as canon-coverage gap, not used to derive any claim).
2. "Docsie 2025, 'Documentation Drift'" — underlying claim: stopgaps fragment knowledge and reintroduce drift. Quote present in output: yes (one sentence). Confidence: direct.

## Contradictions surfaced
- **Within the verdict itself:** deletion leg is "above base rate" / "within tolerance"; deferral leg is "at or below base rate" / "below base rate." The subagent does not collapse these — they are split on purpose and should remain split downstream.
- No contradicting passages between sources were surfaced (single source-class — practitioner blog posts on doc drift, all directionally aligned).

## Subagent's own verdict (verbatim)
"Within tolerance on the deletion. Below base rate on the deferral."

## Gaps the subagent missed
- Canon coverage was declared a gap and not closed — no canon entries verified for documentation drift, README hygiene, or technical-debt deferral. Orchestrator may want to invoke canon-librarian explicitly if any was skipped, or accept the WebSearch fallback.
- No quantified comparison between trigger-based vs time-based deferral completion rates — the recommendation rests on an asserted differential.
- No analysis of the *cost of writing the unified doc now* vs deferring — the forecast critiques the deferral but does not price the alternative.
- No consideration of whether a third option (write a minimal human-facing workflow stub now, even 1 page) outperforms both the full-write-now and defer-indefinitely poles.
- The "category mismatch" framing ([CLAUDE.md](../../../../CLAUDE.md) is agent-facing, not human-facing) is asserted but not tested against the possibility that a sufficiently literate human reader can extract the 12-step workflow from agent-facing prose.

## Token budget
~720 tokens.
