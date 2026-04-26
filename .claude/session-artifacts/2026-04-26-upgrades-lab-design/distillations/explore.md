# Distillation — Explore

## Source agent
Explore (repo-scan of `claude-critic-stack`)

## Invocation summary
Orchestrator asked Explore to map existing primitives in the stack relevant to designing an `upgrades/` R&D lab: directories, schemas, maturity primitives, naming, cross-reference patterns, failure tracking, top-level docs, precedents. Explore returned a comprehensive map of presences and (load-bearing) absences.

## Direct facts

1. [Explore] Existing top-level directories: `.claude/agents/` (10 agents), `.claude/session-artifacts/` (gitignored except `exemplars/`), `canon/corpus/`, `bin/`, `pages/`, `journals/`, `logseq/`, `tests/regression/`, `prompts/`, `plans/`. (confidence: direct)
2. [Explore] No directory named `upgrades/`, `lab/`, `research/`, `rnd/`, `ideas/`, `backlog/`, or `discoveries/` exists. (confidence: direct)
3. [Explore] Agent frontmatter fields: `name`, `description`, `tools` (comma-separated). (confidence: direct)
4. [Explore] Canon `citation.yaml` fields: `slug`, `author`, `title`, `year`, `kind`, `topics`, `source_url`, `fetched_at`, `sha256`, `license`, `body_completeness`, `chapter_offsets`, `stale`, `notes`. (confidence: direct)
5. [Explore] `body_completeness` enum values on disk: `stub | full | toc_plus_chapters | abstract_only | fetch_blocked`. (confidence: direct)
6. [Explore] `stale: true|false` exists on canon entries. (confidence: direct)
7. [Explore] Critic verdict enum: `approve | rework | reject` (three-level, minority-veto). (confidence: direct)
8. [Explore] Distillation per-claim confidence enum: `direct | inferred | unsupported`. (confidence: direct)
9. [Explore] Session directory naming: `<YYYY-MM-DD>-<slug>` (e.g., `2026-04-24-ark-mono-connector-routing`). (confidence: direct)
10. [Explore] Agent files use kebab-case role names; canon slugs use `<author>-<title-short>` kebab-case; topics are flat kebab-case tags. (confidence: direct)
11. [Explore] No version numbers, no status suffixes, no priority ranks anywhere in naming. (confidence: direct)
12. [Explore] `frame.md` uses `## Revision N` accretion pattern — revisions appended, not edited in place; revisions are siblings, not nested. (confidence: direct)
13. [Explore] Librarian citation format: `[Author, Title (Year), §Chapter]`. (confidence: direct)
14. [Explore] Session artifacts have predictable section headers per artifact type but no formal frontmatter. (confidence: direct)
15. [Explore] `tests/regression/` captures known prior mistakes as scenario-based tests (failure archival by example). (confidence: direct)
16. [Explore] `decision-log.md` per session captures replan-vs-rewrite pivot points only. (confidence: direct)
17. [Explore] `plans/ok-cool-this-is-warm-balloon.md` marks items C3, C6, C7, C12, C13 as "deferred" — a deferred-capabilities list. (confidence: direct)
18. [Explore] Top-level docs: `CLAUDE.md` (8426 bytes, master 12-step workflow), `AGENTS.md` (8429 bytes, Codex-runtime parallel with `.Codex/` paths), `README.md` (2027 bytes). (confidence: direct)
19. [Explore] The seven-capability taxonomy appears nowhere on disk except this session's `frame.md`. (confidence: direct)
20. [Explore] Canon stubs are referential placeholders for future ingestion. (confidence: direct)

## Inferred claims

1. [Explore] `body_completeness` is the closest existing analog to a "maturity level" field; no general-purpose maturity primitive exists outside canon. (confidence: inferred)
2. [Explore] No formal `supersedes / builds-on / refutes` relationship graph exists anywhere — cross-reference is informal (step-number + filename) within sessions and `[Author, Title (Year), §Chapter]` for canon. (confidence: inferred)
3. [Explore] Failure tracking is decision-bound: regression scenarios attach to specific past mistakes; decision-logs attach to specific session pivots; agent guardrail sections ("Things you must not do") attach to specific agent contracts. No standing "killed ideas / rejected designs / anti-patterns / postmortem" directory exists. (confidence: inferred)
4. [Explore] Stack philosophy as expressed in artifact layout: every discussed decision routes through the 12-step workflow and lands an artifact; the stack does not currently support a "backlog of unworked ideas." (confidence: inferred)
5. [Explore] Session completion status is not explicitly tracked as a field — workflow completion is implicit in artifact presence. (confidence: inferred)
6. [Explore] Token budgets (≤600, ≤2k) are implicit per agent in prose, not formalized as schema fields. (confidence: inferred)
7. [Explore] `CLAUDE.md` and `AGENTS.md` carry near-duplicate content (8426 vs 8429 bytes) for Claude vs Codex runtimes; this is a flagged drift risk from a prior session. (confidence: inferred)

## Authority-framed claims
None. Explore returned its own observations; no "as X argues" framing.

## Contradictions surfaced
None internally — Explore is descriptive of the repo, not synthetic. The load-bearing tension is between absences and the new requirement, which the scope-mapper must resolve, not Explore.

Notable structural tension Explore flagged for downstream:
- **Free-form lab notebook** (operator's stated "unlimitedly long doc, anyone writes anything") **vs. existing schema discipline** (every artifact has predictable headers, enums, kebab-case, citation format). The stack has no precedent for unstructured long-form prose; `pages/` and `journals/` are Logseq-adjacent but not used as workflow artifacts.

## Subagent's own verdict (verbatim)
Explore did not return a single verdict line; it returned a structural map. The orchestrator-supplied framing is: "structural absences are as load-bearing as structural presences for scope-mapping."

## Gaps the subagent missed

1. Did not characterize how `pages/`, `journals/`, `logseq/` are actually used (tracked but uncommitted in git status); their relationship to a future `upgrades/` is unresolved — could be precedent, could be unrelated.
2. Did not enumerate which of the 10 agents in `.claude/agents/` would plausibly need to *read* an upgrades artifact (integration touchpoint count is unknown).
3. Did not surface whether `exemplars/` (the one tracked subdir of session-artifacts) constitutes a precedent for "promoted" or "mature" artifacts — relevant to the maturity-ladder design.
4. Did not check whether `prompts/` has any schema or naming pattern that might be analogous to a lab-method primitive.
5. Did not return the contents of `plans/ok-cool-this-is-warm-balloon.md`'s deferred items (C3, C6, C7, C12, C13) by name — scope-mapper may need these to check overlap with the proposed lab.
6. Did not test whether the seven-capability taxonomy has any *implicit* on-disk footprint (e.g., agent descriptions clustering around the seven categories) even though it is not named on disk.

## Token budget
~880 tokens.
