# 00 — Confirmations

## Constraint confirmation (per brief §5 item 8)

I did not read the contents of [`upgrades/no-brainer/`](../../upgrades/no-brainer/), [`upgrades/normal/`](../../upgrades/normal/), [`upgrades/outlandish/`](../../upgrades/outlandish/), [`upgrades/profound/`](../../upgrades/profound/), or [`upgrades/LEDGER.md`](../../upgrades/LEDGER.md) while preparing this plan. I read only [`upgrades/README.md`](../../upgrades/README.md) and the [`/upgrade` slash command](../../.claude/commands/upgrade.md), to understand the lab's *form*. Where this plan's proposals collide with existing lab entries, that is convergence, not cribbing.

## Reading confirmation (per brief §1)

I read, in full, before writing:

- [README.md](../../README.md), [CLAUDE.md](../../CLAUDE.md).
- All ten agents under [.claude/agents/](../../.claude/agents/): [requirement-classifier](../../.claude/agents/requirement-classifier.md), [canon-librarian](../../.claude/agents/canon-librarian.md), [canon-refresher](../../.claude/agents/canon-refresher.md), [outside-view](../../.claude/agents/outside-view.md), [subagent-distiller](../../.claude/agents/subagent-distiller.md), [scope-mapper](../../.claude/agents/scope-mapper.md), [frame-challenger](../../.claude/agents/frame-challenger.md), [critic-architecture](../../.claude/agents/critic-architecture.md), [critic-operations](../../.claude/agents/critic-operations.md), [critic-product](../../.claude/agents/critic-product.md).
- [workflows/architecture-review.md](../../workflows/architecture-review.md) (the legacy 6-step) and [prompts/five-pressures.md](../../prompts/five-pressures.md).
- [canon/README.md](../../canon/README.md), [canon/sources.yaml](../../canon/sources.yaml), [canon/sources.ingest.yaml](../../canon/sources.ingest.yaml), [canon/refresh-feeds.yaml](../../canon/refresh-feeds.yaml). Sampled corpus directories: `anthropic-multi-agent-research-system`, `chen-devils-advocate-2024`, `shinn-reflexion-2023`, `evans-ddd` (stub). No `AGENTS.md` exists in this repo (checked).
- [.claude/session-artifacts/README.md](../../.claude/session-artifacts/README.md) and one full session end-to-end: [2026-04-26-context7-adoption-in-critic-stack](../../.claude/session-artifacts/2026-04-26-context7-adoption-in-critic-stack/) — including its `requirement.md`, `frame.md`, `scope-map.md`, `challenges.md`, `critiques.md`, `decision-log.md`. Also the regression scenario [tests/regression/ark-mono-connector-routing.md](../../tests/regression/ark-mono-connector-routing.md) and the prior plan [plans/ok-cool-this-is-warm-balloon.md](../../plans/ok-cool-this-is-warm-balloon.md).
- [bin/ingest-canon.mjs](../../bin/ingest-canon.mjs) (head; the Phase-1 hygiene context).

## Path-discipline confirmation

No absolute paths or `~/`-paths appear in any file in this deliverable. Inside-repo references are repo-relative markdown links from this directory. Outside-repo references are by name + URL, never by user-machine path. (Brief §2f.)

## Anti-agreeability confirmation

Several proposals in this plan argue against the operator's apparent direction. The shortlist contains at least one **removal** (per §4f) and at least one **foundational reframe** (per §4g) that argues "the most valuable thing this stack could become is not a better adversarial reviewer." If the reviewer reads this plan and finds nothing in it uncomfortable, I have failed the brief. (Brief §2c.)

## Citation honesty

Where I cite a paper, I give author + title + year + URL. Where I am uncertain a citation exists or have not verified it, I say so explicitly. The corpus has prior fabrication history (the deleted `agentic-problem-frames-2026` slug, noted in [canon/sources.ingest.yaml](../../canon/sources.ingest.yaml)); I do not want to add to it.
