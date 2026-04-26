# Requirement — format-only state-transition gate

## Primary label
new

## Default frame (from label)
What shape should this gate take, and what's the cheapest experiment that distinguishes shapes (script-only vs script+assist agent, hook vs slash command) before committing to one?

## Known frame bias
`new` tends to over-design before evidence — the gate may grow a schema, a config file, a downgrade path, and a limitations.md emitter before a single real transition has been gated against the existing 21 entries.

## Secondary label
extend — the gate is being added to an existing primitive (the lab's lifecycle state-table convention), not built standalone; it expands the surface area of the lab format monotonically by making one column load-bearing.

## Alternative classification
extend would become primary if the operator decides the gate is just an enforcement layer on the already-defined lifecycle (no new schema, just "the README's stated requirements, mechanically checked") rather than a new artifact with its own per-transition schema and interaction model.

## User's framing words
- "Design a ... gate" — presumes `new`.
- "format-only ... Refuse any scope expansion into idea evaluation" — pre-commits the scope boundary; strongly disfavors `investigation` and `refactor`.
- "choice between bash script vs LLM agent" and "choice of integration point (pre-commit hook vs slash command)" — frames the design space as a 2×2 of pre-decided axes; classifier flags this because the real shape-question may not be either axis (e.g., the gate could be a step inside the existing `/upgrade` command rather than a new hook or new slash command).
- "this workflow run will refine" the existing draft — signals a sketch already exists, which is why `new` is correct (capability does not yet run) but with a strong pull toward `extend` (the sketch exists in prose).

## Gaps
- Is there an existing `/upgrade` slash command that the gate should live inside, or is `/advance-upgrade` genuinely a new command? If the former, this is `extend`, not `new`. **(Answer: yes, `/upgrade` exists at `.claude/commands/upgrade.md`.)**
- Will the gate be invoked by humans, by AI agents acting on the operator's behalf, or both? The interaction-model choice hinges on this.
- Are the seven transitions equally likely to need gating, or is the real failure mode concentrated on `🔨 implemented`? A single-transition gate is a different shape from a seven-transition gate.
- Does "the prior state correctly reached" mean "the prior state's required elements are present in the body now" or "there exists historical evidence the prior state was legitimately reached at the time it was claimed"?
- Is the schema authoritative (gate is the source of truth) or descriptive (README is source of truth, gate mechanically enforces it)?

## Meta — write gap
`requirement-classifier` agent currently has only `Read` in its tool list; the orchestrator persisted this artifact. CLAUDE.md says the agent writes `requirement.md` — discrepancy worth a `limitations.md` entry once that pattern lands.
