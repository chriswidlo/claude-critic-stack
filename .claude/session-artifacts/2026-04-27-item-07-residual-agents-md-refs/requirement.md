# Requirement classification — item 7 (residual AGENTS.md references)

## Primary label
**refactor**

## Default frame (from label)
Frame downstream steps as: *"what observable change would falsify 'behavior unchanged' here? — every edit must demonstrably preserve the meaning of historical/narrative prose while removing the file-name from prose that would mislead a reader acting on it today."*

## Known frame bias
The risk is calling a behavior change a refactor: edits to "prescriptive" prose may quietly drop a *requirement* (e.g., a constitutional-layer column heading promising a future benefit) rather than just rephrase it — that's a scope shrink, not a refactor.

## Secondary label (if any)
**investigation** — the load-bearing work is *judging* which sentences in three upgrade-entry READMEs are narrative vs. prescriptive; that judgment must precede any edit and is itself a small audit.

## Alternative classification
`investigation` would become primary if the user wanted a per-occurrence categorization table (live/historical, prescriptive/narrative) delivered without edits — i.e., the deliverable is the classification of the prose, not the rewritten prose.

## User's framing words
- *"refactor of language under a constraint that historical record stays immutable"* — user explicitly proposes the `refactor` label.
- *"live docs ... no longer name `AGENTS.md`"* / *"action prose ... needs to be revised"* — presumes targeted edits, consistent with refactor.
- *"Catalyst sections describing the past can stay"* / *"Session-artifact mentions are historical record — don't edit"* — explicit invariants the refactor must preserve.

What would change the classification: if any of the three upgrade-entry READMEs turns out to contain a prescriptive AGENTS.md reference whose *intent* (not just wording) no longer holds, removing it is `replace` (swapping the prescription for a different one) or even a scope shrink, not refactor.

## Gaps
- No per-line judgment yet on which of the cited lines ([`upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md`](../../../upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md):11/:42; [`upgrades/no-brainer/2026-04-26-git-strategy-documentation/README.md`](../../../upgrades/no-brainer/2026-04-26-git-strategy-documentation/README.md):11; [`upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md`](../../../upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md):9/:38) are narrative vs. prescriptive — that's the core decision and isn't pre-resolved by the punch-list.
- `.gitignore` line drift — punch-list body says line 33; current grep finds `!AGENTS.md` at line 21. Same line semantically; punch-list line numbers are stale (file evolved between audit and execution).
- For `.gitignore`'s `!AGENTS.md` allowlist line, the choice between *delete the line* (refactor: behavior unchanged because the file doesn't exist) vs *leave it* (forward-compat if AGENTS.md returns) is unstated. Default-frame answer: deleting it is observably behavior-preserving today; leaving it presumes a future that may not arrive.
- Whether [`CLAUDE.md`](../../../CLAUDE.md):9's artifact list is enumerative (drop AGENTS.md, list shrinks) or exemplary (rephrase to "and similar root-level constitutional docs") — affects whether this is a pure deletion or a rewording.
