# Requirement classification — `2026-04-27-critics-get-write-tool-impl`

## The question

Should we add the `Write` tool to the three critic agents (`critic-architecture`, `critic-operations`, `critic-product`) and have each critic persist its full verdict to `.claude/session-artifacts/<session-id>/critiques/<lens>.md`, returning only a one-line summary inline? And should we keep the existing aggregate `critiques.md` as a thin index (3-row table: lens · verdict · path-to-file) or drop it?

## Primary label
`extend`

## Default frame (from label)
Does adding `Write` to the critics belong as an extension of the existing critic-agent contract, or as a separate primitive (e.g., a post-critic persistence hook)? Extension is right when surface area grows monotonically — here, each critic gains one capability (persist own verdict) without altering its review contract. The aggregate-`critiques.md` keep/drop sub-question is a second, independent extension/replacement choice nested inside the first.

## Known frame bias
Overloading the critic primitive until it fractures. The risk is that "critic also writes" today becomes "critic also reads prior critiques, writes, updates index, signs artifact" tomorrow. Watch for the second responsibility creeping in under cover of the first. Also: extension framing tends to under-question whether the *orchestrator's* transcription job should be replaced wholesale (which is what's actually happening to the aggregate file) — that piece is closer to `replace` than `extend`.

## Secondary label
`replace` — the aggregate `critiques.md` artifact, in its current form (orchestrator-authored full transcription), is being replaced by per-lens authored files. The keep-as-thin-index option is replacement-with-residue, not preservation.

## Alternative classification
`refactor` would become primary if the claim were "no behavior change — same verdicts, same audit trail, just authored differently." It is not primary because behavior *does* change: the audit artifact's authorship shifts from orchestrator-paraphrase to reviewer-original. That is a contract change in what `critiques/<lens>.md` *means*, not a structural rearrangement. Calling this a refactor would be the exact anti-pattern named in the classifier rules ("behavior change sneaking in under refactor").

## User's framing words
- "**add** the Write tool" — presumes `extend`.
- "**keep** the existing aggregate `critiques.md` as a thin index **or drop** it" — presumes the choice is between `extend` (keep) and `replace` (drop), correctly framing the sub-question.
- The upgrade entry's wording "audit trail becomes the agent's own writing" is closer to `replace` semantics for the aggregate artifact than the surface "add Write" suggests.

What would change the classification: if the proposal also altered *what each critic reviews* (e.g., critics read each other's files before voting), the primary would shift to `new` (a new cross-critic protocol). If the proposal only restructured where the orchestrator writes the same content, primary would be `refactor`.

## Recursive-frame note
The question is the critic-panel reviewing a change to the critic-panel. The relevant frame-bias amplification: critics tend to approve self-improvements that increase their own authority/surface (here, write access). Step 10 should weight the operations-lens objection more heavily than usual, since "more tool grants to agents" is an ops-surface change the architecture and product lenses are structurally less alert to.

## Gaps
- **Scope of `Write`.** Frontmatter `tools: Write` is unscoped at the harness level; the spike notes scoping happens "in instruction." Is instruction-level scoping sufficient, or should there be a hook/permission rule? Affects whether this is `extend` (instruction-scoped) or edges toward `migrate` (moving permission enforcement from prose to harness).
- **Session-id passing.** The spike flags this as an orchestrator-side change. If session-id passing requires a new invocation-prompt protocol shared across agents, that is a second `extend` on the orchestrator, not part of this one.
- **Aggregate file's downstream consumers.** Step 12 synthesis reads the panel result. If anything else (a future agent, an export script) reads `critiques.md`, drop-vs-keep stops being XS-reversible.
- **What "one-line summary inline" must contain.** Verdict + top objection is proposed; if the orchestrator's veto logic (Step 10–11 routing) parses the inline return, the format is a contract, not a convenience.
