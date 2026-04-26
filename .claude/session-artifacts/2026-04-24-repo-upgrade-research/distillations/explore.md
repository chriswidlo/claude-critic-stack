## Source agent
Explore

## Invocation summary
The orchestrator inspected the repository itself because the user explicitly asked what is in this repo. The repo is not an application codebase; it is a prompt-and-corpus scaffold for adversarial design review, with a small amount of supporting Node automation.

## Direct facts
1. The repo root contains [README.md], [CLAUDE.md], [AGENTS.md], [workflows/architecture-review.md], [prompts/five-pressures.md], [plans/ok-cool-this-is-warm-balloon.md], [tests/regression/ark-mono-connector-routing.md], [canon/] and [bin/]. (confidence: direct)
2. There are 10 agent-spec markdown files under `.claude/agents/`: `requirement-classifier`, `canon-librarian`, `outside-view`, `subagent-distiller`, `scope-mapper`, `frame-challenger`, `critic-architecture`, `critic-operations`, `critic-product`, and `canon-refresher`. (confidence: direct)
3. The canon inventory currently contains 19 corpus entries: 6 `full`, 11 `stub`, 1 `toc_plus_chapters`, and 1 `abstract_only`. (confidence: direct)
4. The executable code footprint is small: the main scripts are `bin/ingest-canon.mjs` and `bin/ingest-owned-book.mjs`. (confidence: direct)
5. Regression coverage is currently manual-first: `tests/regression/ark-mono-connector-routing.md` describes a manual grading procedure rather than an automated test runner. (confidence: direct)
6. `plans/ok-cool-this-is-warm-balloon.md` documents a completed or in-progress "Phase 2 SOTA upgrade" that added the 12-step workflow, session artifacts, the critic panel, and canon hygiene. (confidence: direct)
7. The working tree contains an untracked `AGENTS.md` that adapts the stack to Codex and points at `.Codex/...`, while the tracked repo files still use `.claude/...` and `CLAUDE.md`. (confidence: direct)

## Inferred claims
1. The repo's primary asset is its review method and evidence library, not software execution logic. (confidence: inferred)
2. The strongest current capabilities are framing discipline, corpus-backed retrieval, and audit-friendly artifact generation. (confidence: inferred)
3. The biggest current weakness is not "missing more prompts"; it is that evaluation, freshness, and operational calibration are still comparatively manual. (confidence: inferred)

## Authority-framed claims
none

## Contradictions surfaced
- The repo presents itself as intentionally outside target codebases, yet the user can still ask repo-specific questions and the workflow then needs lightweight repository exploration.
- The stack now exists in both `CLAUDE.md`/`.claude` and `AGENTS.md`/`.Codex` forms, which risks documentation drift across runtimes.

## Subagent's own verdict (verbatim)
The repo is a prompt-and-corpus adversarial review stack with light ingestion tooling, not a full runtime platform.

## Gaps the subagent missed
- No measurement exists for artifact quality over time.
- No automated scorecard exists for critic precision/recall, corpus freshness, or session cost.
- No machine-readable contract exists alongside the markdown artifacts.

## Token budget
~500
