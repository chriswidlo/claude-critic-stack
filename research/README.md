# research/

SOTA distillations of external research, dated and tiered. Before researching a topic, **grep this directory first** — a recent distillation likely exists.

## Read this when
- You are about to invoke `WebSearch` or `WebFetch` on a topic adjacent to AI agents, Claude Code, multi-agent design, MCP, evals, or AI-readable documentation.
- You need to cite SOTA on an architectural decision and want to know what the canon already records.
- You want to know whether a prior session has already settled a question.

## Skip if
- You need the contents of `canon/corpus/` (those are *primary* sources; this directory holds *distillations* of them plus URLs not snapshotted).
- You need workflow templates or schemas (those live in `.claude/session-artifacts/README.md` and `canon/README.md`).

## Layout

```
research/
├── README.md                  (this file — the index)
├── sota-2026/                 (SUPERSEDED 2026-05-16; kept for audit)
│   ├── 00-MASTER-SYNTHESIS.md (was over-anchored to worktree concerns)
│   └── 01-13-*.md             (~52,000 words across 13 topics)
└── sota-2026-v2/              (CURRENT)
    ├── 00-MASTER-SYNTHESIS.md (~6,500 words; 6 load-bearing primitives, 20 ranked practices, 58 anti-patterns)
    ├── 01-claude-code-platform.md
    ├── 02-anthropic-practices.md
    ├── ...
    ├── 15-headless-ci-cost.md
    └── 16-ai-readable-docs.md (folder READMEs, AI-doc SOTA; this turn)
```

## Active distillations (current)

| File | Topic | Last verified | Next review by | Volatility |
|---|---|---|---|---|
| [sota-2026-v2/00-MASTER-SYNTHESIS.md](research/sota-2026-v2/00-MASTER-SYNTHESIS.md) | Master synthesis of all 15 v2 reports | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/01-claude-code-platform.md](research/sota-2026-v2/01-claude-code-platform.md) | Claude Code features inventory | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/02-anthropic-practices.md](research/sota-2026-v2/02-anthropic-practices.md) | Anthropic engineering best practices | 2026-05-15 | 2026-11-15 | slow |
| [sota-2026-v2/03-prompt-engineering.md](research/sota-2026-v2/03-prompt-engineering.md) | Prompt engineering SOTA | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/04-context-engineering.md](research/sota-2026-v2/04-context-engineering.md) | Context engineering thesis | 2026-05-15 | 2026-11-15 | slow |
| [sota-2026-v2/05-tool-design.md](research/sota-2026-v2/05-tool-design.md) | Tool/function design | 2026-05-15 | 2026-11-15 | slow |
| [sota-2026-v2/06-multi-agent.md](research/sota-2026-v2/06-multi-agent.md) | Multi-agent orchestration | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/07-memory-rag-context.md](research/sota-2026-v2/07-memory-rag-context.md) | Memory, RAG, agent state | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/08-evals.md](research/sota-2026-v2/08-evals.md) | Evals, golden datasets, judges | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/09-critic-panels.md](research/sota-2026-v2/09-critic-panels.md) | Critic panels, multi-lens review | 2026-05-15 | 2026-11-15 | slow |
| [sota-2026-v2/10-safety-guardrails.md](research/sota-2026-v2/10-safety-guardrails.md) | Safety, guardrails, prompt injection | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/11-mcp-ecosystem.md](research/sota-2026-v2/11-mcp-ecosystem.md) | MCP protocol + ecosystem | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/12-ai-dev-ecosystem.md](research/sota-2026-v2/12-ai-dev-ecosystem.md) | Aider/Cursor/Continue/Cline survey | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/13-tdd-spec-verification.md](research/sota-2026-v2/13-tdd-spec-verification.md) | TDD, spec-driven dev, verification | 2026-05-15 | 2026-11-15 | slow |
| [sota-2026-v2/14-project-instructions.md](research/sota-2026-v2/14-project-instructions.md) | CLAUDE.md / AGENTS.md SOTA | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/15-headless-ci-cost.md](research/sota-2026-v2/15-headless-ci-cost.md) | Headless Claude, CI, cost mgmt | 2026-05-15 | 2026-08-15 | fast |
| [sota-2026-v2/16-ai-readable-docs.md](research/sota-2026-v2/16-ai-readable-docs.md) | Folder READMEs + AI-doc authoring | 2026-05-17 | 2026-08-15 | fast |

## Superseded

| File | Superseded by | Reason | Date |
|---|---|---|---|
| [sota-2026/00-MASTER-SYNTHESIS.md](research/sota-2026/00-MASTER-SYNTHESIS.md) | sota-2026-v2/00-MASTER-SYNTHESIS.md | Over-anchored to worktree concerns; v2 retargeted to general workflow | 2026-05-16 |
| [sota-2026/01-13-*.md](research/sota-2026/) | sota-2026-v2/01-15-*.md | Same — v1 had worktree framing bleed | 2026-05-16 |

Files kept on disk for audit; do not link to or cite v1 in new work.

## Volatility cadences (from canon)

| Tier | Cadence | Applies to |
|---|---|---|
| `durable` | no timer | Foundational research, established principles |
| `slow` | 365 days | Engineering essays, methodology docs |
| `fast` | 90 days | Anthropic engineering essays, AI tooling, blog posts |
| `volatile` | 30 days or live-only | Model benchmarks, current API behavior |

## Maintenance — how to add a distillation

1. Determine the topic and volatility tier.
2. If continuing the sota-2026-v2 series, use the next sequential number; otherwise create a sibling subdir with a date prefix (e.g., `2026-08-15-<topic>/`).
3. Front-load the file with frontmatter-style metadata:
   ```markdown
   **Vintage:** YYYY-MM-DD.
   **Volatility tier:** <tier>.
   **Next review by:** YYYY-MM-DD.
   **Status:** active.
   ```
4. Body: organize as Definite / Emerging / Contested / Gaps. Cite every claim.
5. Append a row to the "Active distillations" table above.

## Maintenance — how to supersede

1. Author the replacement distillation.
2. In the original file, change `**Status:** active` to a SUPERSEDED line with a real link — e.g. `**Status:** SUPERSEDED by research/sota-2026-v3/00-MASTER-SYNTHESIS.md on 2026-09-15`.
3. Move the row from "Active" to "Superseded" in this README.
4. Do **not** delete the old file — keep for audit per the canon convention (mark stale, don't delete).

## How this directory relates to `canon/`

- **`canon/`** stores **primary sources** (snapshotted books/papers/essays) + the live-fetch registry for URLs too volatile to snapshot.
- **`research/`** stores **distillations** — secondary synthesis of multiple primary sources, plus our own structured findings.

A distillation in `research/` may cite entries in `canon/`. The reverse is not true — `canon/` is for primary material only.

## Anti-patterns

- **Adding a distillation without dates.** Without `Vintage:` and `Next review by:`, future-AI can't tell if the doc is current.
- **Citing without URLs.** Every claim must be source-checkable. Unsourced prose is opinion.
- **Hiding gaps.** Honest "I searched X, found nothing" beats fabricated SOTA.
- **Deleting superseded distillations.** Audit trail matters; the failure mode of v1 (worktree-anchored) is itself signal.
