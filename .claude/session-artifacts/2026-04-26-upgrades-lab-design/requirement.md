## Primary label
new

## Default frame (from label)
What shape should `upgrades/` take, and what's the cheapest experiment that distinguishes shapes — i.e., which prior-art lab structures (industrial R&D, academic lab notebooks, ML research repos, design-system pattern libraries) does this resemble closely enough to borrow form, and which dimensions force a novel structure?

## Known frame bias
Over-designing before evidence: the operator has explicitly demanded a mature future-state design with no phase-one compromise, which doubles the bias — the classifier flags that the *constraint itself* amplifies the default failure mode of `new`. Downstream steps should treat "mature from day one" as a stated preference to be honored, while still naming which structural commitments are reversible vs. which lock in.

## Secondary label (if any)
extend — the lab is also an institutional-memory layer over the existing stack (CLAUDE.md workflow, `.claude/agents/`, `.claude/session-artifacts/`); the `upgrades/` directory must compose with those, not replace them.

## Alternative classification
extend would become primary if the question were "how does `upgrades/` integrate with the existing 12-step workflow and agent layer" rather than "what is the internal structure of a mature R&D lab." The current question foregrounds internal structure (document types, disciplines, maturity ladder, failure archive, naming) — that's `new`. If a later turn pivots to integration semantics, reclassify.

## User's framing words
- "mature R&D lab ... in its full future form"
- "Not a starter scaffold to be evolved later"
- "Design for the mature future state, not phase-one-evolves-later"
- "Global view first, trickle down"
- "No 'start flat, subdivide later' compromises"
- "Group by value/capability, never by mechanical edit type"
- "the working name `upgrades` over `discoveries` ... recommend whether `upgrades` is the right semantic"
- "grounded in prior art on R&D structure, NOT ad-hoc"

These presume: (a) the artifact must be designed top-down at full maturity (forecloses incremental discovery of structure); (b) prior art exists and should ground the design (forecloses pure invention); (c) the name is provisional (opens semantic re-labeling). The classification stays `new` regardless — these are constraints on the new thing, not signals of a different label. What would change the classification: if the operator revealed an existing `upgrades/`-shaped directory in another repo to be ported, this becomes `migrate`; if there's already a partial `upgrades/` to be reorganized, `refactor`.

## Gaps
- Is there a precedent lab structure in the operator's prior repos or reading (e.g., a specific industrial R&D taxonomy, lab-notebook convention, ADR-variant) that should anchor the prior-art search, or is the librarian to surface candidates cold?
- What's the read/write cadence — is `upgrades/` written by the orchestrator mid-session, by a curator agent post-session, by the operator manually, or all three? This shapes whether the structure optimizes for machine-write or human-read.
- Does "mature future state" imply a target scale (number of artifacts, contributors, sessions/week)? The right structure for 50 artifacts differs from 5,000.
- Is the failure archive for failed *upgrades* (rejected experiments) or failed *stack runs* (workflow breakdowns)? These are different disciplines.
