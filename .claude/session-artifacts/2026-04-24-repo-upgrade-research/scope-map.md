## Existing primitives touched
| primitive | source (where it was named) | relationship | one-line rationale |
|-----------|-----------------------------|--------------|--------------------|
| `CLAUDE.md` / `AGENTS.md` workflow contract | explore distillation | extend | Keep the prompt-level policy layer, but add machine-readable contracts and runtime-selection rules so behavior is testable rather than purely textual. |
| `.claude/agents/*.md` prompt agents | explore distillation | extend | The agent roles are the stack's core product; they should gain clearer budgets, schemas, and eval hooks rather than be replaced by a framework. |
| `.claude/session-artifacts/*` markdown artifact trail | explore + canon distillations | extend | Keep the audit trail, but add structured sidecars so sessions can be diffed, scored, and regressed automatically. |
| `tests/regression/*.md` manual-only regression workflow | explore distillation | replace | Manual exemplars are too slow and too soft as the only quality loop; preserve exemplar cases but replace manual-only grading with a hybrid eval harness. |
| `canon/corpus/` + `sources.yaml` + `sources.ingest.yaml` | explore + outside-view distillations | extend | Curated evidence is a differentiator; the missing piece is coverage/freshness/contradiction measurement, not a different knowledge substrate by default. |
| `bin/ingest-canon.mjs` + `bin/ingest-owned-book.mjs` + `canon-refresher` | explore distillation | extend | Low-dependency ingestion is a strength; add provenance, gap reporting, and quality checks rather than replacing with a heavier retrieval stack immediately. |
| "manual markdown-only portability between Claude and Codex variants" | explore distillation | conflict | The current dual surface (`.claude` vs `.Codex`) can coexist for now, but drift between them directly undermines trust in the workflow contract. |

## Deletion cost (for subsume/replace rows)
- `tests/regression/*.md` manual-only regression workflow: callers = curator and future contributors; data migrations = convert exemplar scenarios into scored fixtures/rubrics; config surface = add eval configuration, threshold files, and a small harness.

## Requires decision (conflicts)
- Claude-native layout vs Codex-native layout: both can coexist temporarily, but without a generator or single source of truth they will drift and tell different stories about the same stack.

## Preserved primitives with stated reason (non-default)
- `.claude/agents/*.md`: preserved because the repo's core value is explicit, auditable behavioral contracts; replacing them with opaque framework wiring would erase the main differentiator.
- `canon/corpus/` and ingestion scripts: preserved because recent research strengthens, rather than weakens, the case for curated domain evidence and provenance-aware retrieval.
- `.claude/session-artifacts/*`: preserved because the artifact trail is the stack's audit surface; it should become more structured, not disappear.

## Primitives the distillations did not name but the query implies
- A cost/latency budget for each workflow step
- A machine-readable rubric format for critics and synthesis
- A source-freshness / coverage scorecard
- A runtime policy for when to stay single-agent vs parallelize vs invoke the critic panel
