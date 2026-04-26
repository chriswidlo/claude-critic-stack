# Build a separate research stack as sibling, communicating only via the corpus

| Field | Value |
|---|---|
| 📌 **title** | Build a separate research stack as sibling, communicating only via the corpus |
| 🎯 **tier** | 🚀 outlandish |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator asked whether building another system specifically for research would be the right move — one responsibility per system. The retrospective on the stack also flagged "I cannot run Anthropic Research itself" as a real tooling gap that no in-stack agent can fully fill. The shape of "deep research vs adversarial review" is genuinely different and forcing both into one stack would compromise both. |
| 💡 **essence** | A separate `claude-critic-stack` sibling — call it `claude-research-stack` — whose only job is corpus expansion and deep research. It runs at its own cadence (perhaps nightly), with its own settings.json, its own agents (research specialists, citation auditors), its own model preferences (perhaps Sonnet for cost at high volume). It writes to a *shared* `canon/corpus/` that this stack reads via `canon-librarian`. The two stacks talk via the filesystem, not via direct invocation. |
| 🚀 **upgrade** | Single-responsibility per system: research-stack optimizes for breadth and rigor; critic-stack optimizes for adversarial review; neither compromises for the other. The corpus becomes a real asynchronous boundary; both stacks can evolve independently. The architecture is composable instead of monolithic. The retrospective's "I cannot run Anthropic Research" gap is partially closed by building a system the operator can run. |
| 🏷️ **tags** | architecture, composability, research, multi-stack, separation-of-concerns |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The shape of the proposed sibling](#the-shape-of-the-proposed-sibling)
- [Why the corpus is the right boundary](#why-the-corpus-is-the-right-boundary)
- [What this would take](#what-this-would-take)
- [Risks and unknowns](#risks-and-unknowns)
- [Open questions](#open-questions)

## The shape of the proposed sibling

`claude-research-stack` is a separate working directory, separate `.claude/`, separate `settings.json`, separate `CLAUDE.md`. Its agents are research-specialized: deep-fetcher (open-web research), citation-auditor (verifies cited papers actually exist), corpus-curator (decides what to ingest), perhaps a survey-synthesizer (multi-source synthesis on a topic). Its workflow is not the 12-step adversarial-review workflow; it is something more like Anthropic's multi-agent research pattern — orchestrator + specialists + filesystem artifacts.

It runs at a different cadence: research is a long-running process, not a per-decision call. Could be triggered manually ("research X") or on a schedule (weekly survey of new arXiv papers in a relevant area).

## Why the corpus is the right boundary

The two stacks must share *something*. Three options were considered:

- **Direct invocation** (critic-stack `claude -p`'s into research-stack and waits) — tight coupling, complex error surface, distributed-systems problems for no benefit.
- **Shared session-artifacts** — leaks each stack's internal state into the other's context. Bad.
- **Shared corpus** — research-stack writes to `canon/corpus/`; critic-stack reads it via `canon-librarian` exactly as it already does. The integration surface is one filesystem boundary, async, no protocol other than "what counts as a corpus entry."

The corpus is the right boundary because it is the *intent* of both systems' existence: the critic-stack consumes canon to ground review; the research-stack produces canon to ground future review. Direct invocation would conflate "wanting an answer right now" (critic-stack's mode) with "exploring the literature" (research-stack's mode) — two operations with incompatible cadences.

## What this would take

- A new repo, scaffolded as a sibling of `claude-critic-stack`. Probably `~/Development/Projects/claude-research-stack`.
- Either a shared corpus directory accessed by both stacks (filesystem mount), or a synchronization mechanism (research-stack pushes corpus updates; critic-stack pulls).
- A common entry schema for corpus entries (already mostly exists in this stack's `canon/corpus/<slug>/citation.yaml`).
- Research-stack's own agent suite. Probably 5-8 agents.
- Research-stack's own workflow doc.
- A clear protocol for what counts as a "ready to merge" corpus entry — verification, citation audit, body-completeness check.

This is a months-long project. Probably 4-8 weeks of design and initial scaffolding, then ongoing improvement.

## Risks and unknowns

- **Maintenance load doubles.** Two systems, two harness-config files, two CLAUDE.md docs to keep current. If the operator's attention is finite, one stack will rot.
- **Corpus-schema drift.** Both stacks read and write the same corpus; schema changes require coordinated updates.
- **Research output quality is unmeasured.** Adversarial review has clear success criteria (panel verdicts); research has fuzzier criteria (does the corpus get richer?). Without measurement, research-stack could produce noise indistinguishable from signal.
- **The retrospective's "I cannot run Anthropic Research" gap may not actually be solved by a self-built version.** Anthropic Research has tooling we don't (a search index, a model fine-tuned for research, etc.). A self-built research-stack is a different thing.

## Open questions

- Is the right scope of the research-stack just "corpus expansion," or does it include "deep dives on operator-named topics" (more like Anthropic Research)?
- Should the research-stack's outputs be ratified by *this* stack's adversarial-review workflow before landing in the corpus? That would be elegant (each stack's strength compensates for the other's) but introduces coupling we explicitly tried to avoid.
- Is there a smaller version that captures most of the value — perhaps just `canon-refresher` extended into a more aggressive research mode within this same stack?
