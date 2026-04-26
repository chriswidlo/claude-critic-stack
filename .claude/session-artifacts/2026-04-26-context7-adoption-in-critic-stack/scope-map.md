# Scope map — Context7 adoption in claude-critic-stack

The proposed requirement is shape-pluralistic. Adoption shapes under evaluation:

- **A** — do nothing (no adoption)
- **B** — add Context7 as a raw MCP tool available to all agents
- **C** — wrap Context7 in a dedicated `library-docs` subagent
- **D** — extend `canon-refresher` to pull Context7-sourced material into the corpus
- **E** — adopt Context7 as a Claude Code Skill, out-of-workflow

Each row of the table evaluates the relationship per shape. Shape A is omitted from row labels because it changes nothing — it is the baseline against which every other shape must justify itself.

## Existing primitives touched

| primitive | source (where it was named) | shape | relationship | one-line rationale |
|-----------|-----------------------------|-------|--------------|--------------------|
| canon-librarian | CLAUDE.md, distillations/canon-librarian.md | B | conflict | Adds a second retrieval surface with different trust/freshness semantics; violates librarian-first routing unless gated. |
| canon-librarian | same | C | extend | New `library-docs` subagent sits as a second adapter behind the librarian's retrieval port (Cockburn S5/C6); librarian remains the trust-tier owner. |
| canon-librarian | same | D | extend | Librarian gains additional ingested corpus material; retrieval surface unchanged. |
| canon-librarian | same | E | extend | Skill operates outside the workflow; librarian untouched in-workflow. |
| canon-refresher | CLAUDE.md, distillations/outside-view.md §3 | B | extend | No change to refresher; B operates at query-time, not corpus-time. |
| canon-refresher | same | C | extend | No overlap; refresher continues to propose corpus entries, library-docs answers per-query. |
| canon-refresher | same | D | subsume | D is exactly canon-refresher's job extended to a new feed source; the existing refresher absorbs Context7 as one more input. The *separate* idea of "Context7 as a live primitive" is deleted under D. |
| canon-refresher | same | E | extend | Out-of-workflow Skill, no overlap. |
| canon corpus (canon/corpus/) | CLAUDE.md, distillations/canon-librarian.md | B | extend | Corpus untouched; Context7 results live alongside, not inside. |
| canon corpus | same | C | extend | Corpus untouched; library-docs serves a parallel retrieval channel. |
| canon corpus | same | D | conflict | Pre-ingesting fast-moving third-party API docs into a curated principle-level corpus stales instantly (canon-librarian S3) and dilutes the curation criterion ("principle-level"). User has not chosen between corpus-purity and corpus-freshness. |
| canon corpus | same | E | extend | Skill is out-of-band; corpus untouched. |
| outside-view agent | CLAUDE.md | B | extend | Outside-view gains an additional tool surface but its canon-first rule still binds. |
| outside-view agent | same | C | extend | No interaction; outside-view does not call library-docs. |
| outside-view agent | same | D | extend | Indirect: outside-view reads canon, which now contains more material. |
| outside-view agent | same | E | extend | No interaction. |
| subagent-distiller | CLAUDE.md | B | extend | Distiller compresses any subagent return; gains no new behavior, processes more raw material. |
| subagent-distiller | same | C | extend | Library-docs return must be distilled like any other subagent return. Adds one distillation file per run. |
| subagent-distiller | same | D | extend | No interaction. |
| subagent-distiller | same | E | extend | Skill output bypasses distiller (out-of-workflow); no in-workflow change. |
| Parallel-gather slot (steps 3–5) | CLAUDE.md "12-step workflow" | B | extend | Tool added inside existing slot; no slot change. |
| Parallel-gather slot | same | C | extend | Adds a fourth conditional sibling (library-docs) to {outside-view, canon-librarian, Explore}; gated by "question names a library + version." |
| Parallel-gather slot | same | D | extend | No workflow-shape change; refresher already runs out-of-workflow. |
| Parallel-gather slot | same | E | extend | No workflow-shape change; Skill is out-of-workflow by definition. |
| Librarian-first / canon-first routing rule | CLAUDE.md "Things you must not do" | B | conflict | An ungated MCP tool on every agent lets agents bypass librarian-first; the rule depends on canon-librarian being the *first* call for research questions. |
| Librarian-first routing rule | same | C | extend | Rule preserved if library-docs is invoked *via* librarian (or after it), not in parallel-as-peer. Requires explicit routing language: "librarian first; librarian routes to library-docs when query names library+version." |
| Librarian-first routing rule | same | D | extend | Routing unchanged; refresher operates outside the routing rule. |
| Librarian-first routing rule | same | E | extend | Out-of-workflow; rule scope is in-workflow only. |
| Claude Code Skills mechanism | CLAUDE.md, distillations/canon-librarian.md gap (13) | B | extend | Unused. |
| Claude Code Skills mechanism | same | C | extend | Unused. |
| Claude Code Skills mechanism | same | D | extend | Unused. |
| Claude Code Skills mechanism | same | E | subsume | E *is* the Skills mechanism populated with a Context7 binding; the previously-empty Skill surface is consumed by this one Skill. The "general-purpose Skill mechanism" idea is replaced by "the Context7 Skill." |
| settings.json / mcp servers config | repo settings.json | B | extend | New MCP server entry added; existing entries untouched. |
| settings.json / mcp servers config | same | C | extend | Same — Context7 MCP entry added so the library-docs subagent can call it. |
| settings.json / mcp servers config | same | D | extend | New MCP entry consumed only by the refresher. |
| settings.json / mcp servers config | same | E | extend | New MCP entry plus a Skill manifest entry. |

## Deletion cost (for subsume/replace rows)

- **canon-refresher under shape D (subsume):** if D is chosen, the *standalone* "Context7 as a live primitive" framing is deleted. Blast radius: D forecloses shapes B/C/E without further deliberation. Concretely: any per-query freshness need (the actual Context7 use case per outside-view §1) is unmet — the refresher operates corpus-time, not query-time. Callers: none yet (greenfield decision); data migrations: none; config surface: one MCP server entry plus refresher prompt amendment. Cost is conceptual, not code: D answers a different question than Context7 was built for.
- **Skills mechanism under shape E (subsume):** the empty general-purpose Skills surface in this repo is consumed by one Context7-shaped Skill. Blast radius: future Skill additions must coexist with a Context7 precedent that establishes "Skills are out-of-workflow ad-hoc capabilities." Callers: zero today. Data migrations: none. Config surface: Skill manifest plus MCP entry. The deletion is of the *option* to set Skills' precedent with a different first inhabitant.

## Requires decision (conflicts)

- **canon-librarian vs shape B:** both cannot coexist because B grants every agent direct Context7 access, which collapses librarian-first routing into librarian-optional routing. User has not chosen between (a) keep librarian-first as a hard rule and route Context7 through it (which is shape C, not B) or (b) demote librarian-first to a soft default. If (b), much of the stack's discipline thesis weakens; the user should be asked to confirm before B is adopted.
- **canon-first routing rule vs shape B:** same conflict, different surface. The rule reads "do not WebSearch a research question without invoking the librarian first." A raw Context7 tool on every agent is morally equivalent to WebSearch — it is third-party live retrieval. B requires either rewriting the rule or accepting it will be honored in letter, broken in spirit (outside-view §4 secondary failure).
- **canon corpus vs shape D:** corpus curation criterion is "principle-level books and papers." Context7-sourced library API docs are not principle-level; they are reference-level and version-volatile. D requires the user to either (a) split the corpus into principle/reference tiers (a structural change to canon-librarian's trust model) or (b) accept corpus dilution. User has not chosen.

## Preserved primitives with stated reason (non-default)

- **canon-librarian under shapes C, D, E:** preserved because the librarian is the load-bearing primitive of the stack's anti-anchoring discipline (CLAUDE.md "Do not treat canon retrieval as confirmation," "librarian-first rule"). Removing or weakening it removes the stack's reason to exist. This is a stated user constraint embedded in CLAUDE.md, not a default-extend posture.
- **canon corpus under shapes B, C, E:** preserved because the curation criterion (principle-level, contradiction-required) is what distinguishes canon from web. Mixing live API docs into canon under B/C/E is not proposed; only D proposes it, and D conflicts on this preservation.
- **outside-view agent across all shapes:** preserved because none of the shapes touch reference-class forecasting; preservation is by non-overlap, not by exception.

## Shapes dominated by other shapes (orchestrator-facing observation)

- **Shape B is dominated by Shape C** on every relationship that differs: B introduces two conflicts (librarian-first, canon-librarian trust model) that C resolves by routing Context7 *through* the librarian as a second adapter. The only thing B offers that C does not is lower latency (no extra subagent hop). If latency matters more than discipline, B; otherwise C dominates.
- **Shape D answers a different question than Context7 solves.** Outside-view §3 names canon-refresher as a slot for "watching external sources" but flags it as corpus-time, not query-time. Context7's value (per its product positioning, outside-view §1) is per-query freshness. D is the most scope-map-aligned shape (`extend over new`, the classifier's default frame) but the canon-librarian distillation S3 directly opposes pre-ingesting fast-moving docs. D is the shape that *looks* disciplined but mismatches the tool.
- **Shape E is orthogonal, not competing.** E lives outside the workflow entirely; it could coexist with A, B, C, or D. The honest framing is "E or not-E" as a separate axis from "in-workflow shape A/B/C/D." Treating E as one of five mutually exclusive options is a category error baked into the question.

## Primitives the distillations did not name but the query implies

- **Trust-tier labeling on retrieval results.** Canon-librarian distillation C6+S5 implies Context7 should sit behind librarian "with librarian responsible for trust-tier labeling" — but no such labeling primitive exists today. Adoption of C requires inventing it. Worth surfacing to Explore (if the user provides repo context) or to the generator step.
- **Gating predicate** ("question names library + version"). Canon-librarian C4 names this as required for any chosen option. No such gate exists in the stack today. Any non-A shape implicitly proposes adding it.
- **Cost of installed-but-unfired backends.** Canon-librarian gap explicitly flags this as un-retrieved. Outside-view §2 estimates 40–50% of workflow-mismatched tools end up installed-but-unused. The carrying cost (config surface, mental load on future contributors, "why is this here") is a primitive the distillations gesture at but do not name. Relevant to all of B/C/D/E.
- **Question-log / telemetry primitive.** Outside-view §5 proposes a 15–20% lift threshold for shapes C/E. The stack has no question log to measure against. Either invent one (new primitive the user did not name) or accept the threshold cannot be evaluated empirically.
