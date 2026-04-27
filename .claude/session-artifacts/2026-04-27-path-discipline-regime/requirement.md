# Requirement classification — path-discipline regime

## The question (orchestrator-condensed)

The `claude-critic-stack` repo has a "non-negotiable" path-discipline rule in [`CLAUDE.md`](CLAUDE.md):7-16 with four stated reasons. Reason (c) — "keeps internal references clickable from any clone" — is factually wrong: markdown link resolution is file-relative, so the prescribed repo-root style does not click-navigate from subdir files. Reasons (a), (b), (d) (privacy, portability, consent boundary), plus the unstated grep-stability benefit, are sound.

A repo audit shows a 9-vs-9 split between rule-compliant repo-root-style links and file-relative `../` chains. Recent authoring drifts toward file-relative because authoring from a deep subdir naturally produces it. [`.claude/commands/upgrade.md`](.claude/commands/upgrade.md) does not instruct on path style — the structural cause of the drift.

Three options on the table:
- **A.** Keep clauses 1-5; correct reason (c); patch the slash command; rewrite 6 file-relative READMEs + punch-list.
- **B.** Flip clause 2 to file-relative; rewrite 7 repo-root-style files; lose grep-stability.
- **C.** Hybrid leading-slash (`/path/from/root.md`); GitHub-clickable + grep-stable; doesn't click in VS Code.

Operator constraint: session-artifact files must NOT be retroactively edited for style (per commit `5108ed3`, sweeps must be privacy-only).

Detailed plan: [`plans/2026-04-27-item-01-path-discipline-decision.md`](plans/2026-04-27-item-01-path-discipline-decision.md).

## Primary label

**refactor**

## Default frame (from label)

Frame downstream steps around: *"what observable change would falsify 'behavior unchanged'? The rule's stated justifications are being corrected and its enforcement surface tightened, but the prescribed path style itself must remain functionally equivalent — verify with a behavioral check (do links resolve? does grep still pin?), not just a vibe check."*

## Known frame bias

Refactor framing tends to smuggle in behavior changes under the banner of "just cleanup." Here the risk is that "fixing reason (c)" quietly becomes "weakening the rule" (Option B) or "introducing a third style" (Option C), both of which are behavior changes (link resolution semantics, grep pinning) dressed as housekeeping.

## Secondary label

**replace** — becomes primary the moment the operator picks B or C (the primitive — the path-style convention — is swapped, not preserved). Also primary if Option A is reframed as replacing the *enforcement mechanism* (prose rule) with a *structural mechanism* (slash-command instruction + lint).

## Alternative classification

`replace`. The whole question can be read as "should we replace the current path-style convention" — and the orchestrator should not inherit the operator's framing-of-A-as-the-conservative-option uncritically.

## User's framing words (and what they presume)

- *"Keep clauses 1-5, replace reason (c)"* — presumes refactor (preserve rule, fix justification).
- *"Flip clause 2" / "Hybrid"* — framed as alternatives to a refactor; but the operator's labeling of A as the "keep" option reveals an attachment to the existing rule that the classifier should not inherit.
- *"non-negotiable"* (quoted from CLAUDE.md) — operator signaling the rule's *status*, not asserting it as classifier input. Noted but not load-bearing.
- *"structural cause of the drift"* — presumes the fix is structural (slash command), which biases toward A. B and C would treat the drift as evidence the rule is wrong, not under-enforced.

## Gaps for downstream steps to address

- Is the goal to **preserve repo-root style** as the canonical primitive, or to **pick whichever style minimizes future drift**? A vs. B/C hinges on this; the operator has not stated it explicitly.
- What is the actual cost of losing grep-stability under B? Named but not quantified.
- Is the slash-command patch in-scope, or a separate follow-up? If separate, A collapses to "just fix the prose" — a much smaller refactor.
- Is there a **fourth option** the operator has implicitly excluded — drop the rule entirely and let style float? Worth surfacing in step 8.
- The privacy-only sweep constraint (commit `5108ed3`) bounds *which files* can be touched, not *which option* is chosen. Confirm the 6 drifted entry READMEs and the punch-list are NOT session artifacts before A is costed (they aren't — they're in `upgrades/` and `plans/`, not `.claude/session-artifacts/`).
