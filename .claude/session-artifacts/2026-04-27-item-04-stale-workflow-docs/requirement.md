# Requirement classification — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Source.** [plans/2026-04-27-item-04-stale-workflow-docs.md](../../../plans/2026-04-27-item-04-stale-workflow-docs.md)

## Primary label

**replace**

## Default frame (from label)

Subsume/replace is the default: the stale top-level docs — the Phase-1 framing in [README.md](../../../README.md) and the 7-step [workflows/architecture-review.md](../../../workflows/architecture-review.md) — should be removed or rewritten to point at the current authoritative shape ([CLAUDE.md](../../../CLAUDE.md) + [.claude/session-artifacts/README.md](../../README.md)). Preserving either of the old docs requires a stated reason.

## Known frame bias

Sunk-cost attachment to the existing primitive — the risk is rationalising *"update in place"* on `workflows/architecture-review.md`, or partially preserving the old README framing for continuity, when the cleaner move is to replace outright.

## Secondary label

**investigation** — the question is partly meta-sequencing: *"ship (a) now and defer (b)/(c), or do them together?"* That sequencing question has an investigative flavour (cost of two passes vs. one), but the underlying ask is still a replace.

## Alternative classification

**refactor** — would become primary if the claim were *"behaviour of the docs is unchanged, we are just reorganising pointers."* It is not primary because the user is explicitly removing a misrouting doc and changing what new readers are pointed at; that is a behaviour change in the documentation surface, not a structural-only edit.

## User's framing words

- *"ship option (a) … alone now, and defer … to a separate upgrade entry"* — presumes the work decomposes into a minimal delete-and-redirect now plus a unified-doc effort later. The classification would shift toward `new` (for option b: a fresh `workflows/12-step-workflow.md`) or `extend` (for option c: expanding [.claude/session-artifacts/README.md](../../README.md)) if the user reframed as *"should we build the unified doc"* rather than *"should we delete the stale one."*
- *"minimum: delete … and rewrite"* — presumes replace is the floor. That presumption matches the classification, but note it is the user's, not independently derived.

## Gaps

- Is the goal to **stop misrouting readers** (replace, ship (a) now) or to **produce a single canonical workflow doc** (which would be `new` — option b — and a different scope)?
- Does the user consider [CLAUDE.md](../../../CLAUDE.md) itself the canonical workflow doc going forward, or a stepping stone toward a dedicated `workflows/12-step-workflow.md`?
- Is there any external link or fork relying on `workflows/architecture-review.md` at its current path? If yes, deletion vs. redirect-stub is a live sub-decision inside the replace.
