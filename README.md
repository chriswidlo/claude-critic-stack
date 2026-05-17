# claude-critic-stack

*Rigorous second opinions for important decisions.*

> **Rename shortlist** — `claude-critic-stack` is a placeholder. Candidates under consideration (pick one when ready):
>
> Purvapaksha | Sugya | Machloket | Resection | Trutina | Stretto | Mondo | Mu-mon | Rashnu
> Crux | Foil | Hossen | Kintsugi | Witan | Elenchus | Krisis | Aporia

A solo, closed-world adversarial-design-review harness. You bring a design question; the stack runs a 13-step workflow with a three-lens critic panel, a canon librarian over a curated corpus, and an outside-view forecaster. Runs from this directory — never inside the target repo, deliberately, so Claude's default frame is "the industry" rather than "your codebase."

## Quickstart

**What it does** — You bring a hard design question. The stack stress-tests it before answering.

**What you get back** — A recommendation, named tradeoffs, dissenting evidence, three uncertainties.

**How long** — Minutes. You don't drive — read the synthesis at the end.

**How to start** — Type your question. Prefix `quick take:` for a one-paragraph version instead of the full review.

*Already running `claude` in this repo? Type `/explain` for the live tour — current canon, session history, an interactive picker.*

## What it is

- **Three-lens critic panel** — `critic-architecture`, `critic-operations`, `critic-product`. Each lens has authority to reject; minority-veto. Optional shadow lenses on a second model triangulate by model diversity (`SHADOW_PANEL=1`).
- **Canon librarian** over [`canon/corpus/`](canon/corpus/). Required to surface at least one contradicting passage per query. Routes `lifecycle: live-only` entries to WebFetch and flags stale `snapshot+refresh` entries (see [canon/README.md](canon/README.md) for the schema). Currently grep + Read over plain text; a chunker + BM25 index is a deferred R&D candidate.
- **Outside-view forecaster** that consults canon first; WebSearch only for currency or declared gaps.
- **Frame discipline** — `requirement-classifier`, `frame-challenger`, `scope-mapper`, and `subagent-distiller` run before the generator, with a hard gate on `scope-map.md` + `challenges.md`.
- **Per-session artifacts** under `.claude/session-artifacts/<id>/`. Curator-promoted runs land in `exemplars/`.

The corpus is presently Anthropic-heavy and operations-forward, with canonical works on DDD, refactoring, stability patterns, and forecasting still as stubs awaiting owned-book ingestion. Honest about its gaps.

## What it isn't

- Not a replacement for human architectural judgment. It's a structural compensator for known LLM failure modes — agreeability, pattern-overfit, recency bias, confident mediocrity on decisions requiring taste.
- Not a persona agent. No "think like Martin Fowler" prompts. Personas steer vocabulary, not judgment.
- Not a silver bullet. Expect it to improve decision *quality* by surfacing ignored alternatives and stated assumptions, not to produce novel insight on its own.

## How to use

```bash
cd path/to/claude-critic-stack
claude
> I'm considering [design decision from my other repo]. Context: [...]. Review it.
```

What you can type once you're in. Two of these are **explicit trigger phrases** you type literally; the rest is **auto-routed** by the orchestrator based on the shape of your question.

Auto-routed (just ask in prose; the orchestrator picks the path):

- **Decision-shaped question** ("should I X?", "design Y", "is Z a good idea?") → full 13-step workflow.
- **Knowledge-shaped question** ("what does the CAP theorem say?", "explain X") → answered directly from canon, no workflow.

Explicit trigger phrases (type them literally to force a path):

- **`quick take: <question>`** — bypass the workflow for a single-paragraph answer. Use sparingly; the structure exists for a reason.
- **`skip the critic-panel`** (or `skip the critic`) — runs the full workflow but skips steps 10–11.

Slash commands (zero-friction utilities):

- **`/explain`** — this menu, on demand, without leaving chat.
- **`/upgrade`** — capture a creative R&D idea into [`upgrades/`](upgrades/).
- **`/critique <doc-path>`** — one-shot adversarial review. Mints a session, freezes the doc as `question.md` + `inputs.md`, then runs the full 13-step workflow against it in the same chat. Synthesis is presented at the end (~5–15 min). Slug auto-derived from the doc's H1; target defaults to current repo; grounding defaults to follow-AI-docs. No questionnaire.
- **`/session-bootstrap`** — mint an empty session-dir skeleton by hand (rare; use `/critique` when you have a doc).

[`CLAUDE.md`](CLAUDE.md) is the operating manual — the 13-step workflow, the hard gates, the must-nots, and the agent inventory all live there. Read it.

## Populating the canon

- [`canon/sources.yaml`](canon/sources.yaml) — single source of truth (schema_version 2). Every entry carries `lifecycle`, `volatility`, `last_verified`, `fetch_mode`. See [`canon/README.md`](canon/README.md) for the full schema reference.
- `python3 ./bin/ingest-canon.py` — fetch auto-fetchable entries (filtered by `lifecycle` and `fetch_mode`). Idempotent; `--force` re-fetches; `--only=<slug>` restricts.
- `python3 ./bin/ingest-owned-book.py <slug> <path-to-text>` — for books you own, populate a stub from local plaintext.
- `canon/corpus/*/source.txt` is gitignored. Stubs and `citation.yaml` files are tracked so the inventory stays visible in git.

You own the licensing for whatever you put in `canon/corpus/`. See [`canon/README.md`](canon/README.md) for the policy.

## Philosophy

Books teach what to do. Apprenticeship teaches when. This stack is a very good library with a mandatory dissenting reader attached — not an apprentice.

## Operating principle — ratchet forward, never sideways

When an existing primitive (schema, agent, workflow, doc structure) is identified through research as inferior to a SOTA alternative — and the alternative carries no functional drawback or material tradeoff — the response is **complete lossless rewrite to the better practice**, not migration-aware compromise.

The rule binds AI orchestrators and human contributors equally:

- **Never** propose a "half-measure to satisfy existing structure" when a clean rewrite is possible without information loss.
- **Never** defer the rewrite to "later" when the evidence is in hand.
- **Always** surface the finding immediately with: (a) SOTA evidence cited, (b) proposed rewrite scoped, (c) explicit user acceptance request.
- **User acceptance is the only gate.** Once granted, execute the rewrite completely — no partial transitions, no "keep both for now."

The principle exists because compromise-for-fit accumulates as architectural debt. A schema that is "mostly SOTA except for three legacy fields we kept" is not SOTA — it is a different schema that carries the maintenance cost of both worlds. The repo trades short-term migration discomfort for long-term clarity.

**The trigger is *evidence of better practice without material tradeoff*, not novelty for its own sake.** When research returns ambiguous findings, the trigger is not fired. The principle is not a license for churn; it is a license against compromise.

## Mission

**This stack exists to apply structured adversarial review to pre-decision design questions** — the kind of questions a senior engineer asks before writing any code, where the dominant failure mode is *frame error* (solving the wrong problem confidently) rather than *implementation error* (solving the right problem incorrectly).

It is built against five named LLM failure modes (see [`.genesis/five-pressures.md`](.genesis/five-pressures.md)):

1. **Reframe-before-answer** — accepting the user's framing uncritically.
2. **Enumerate-before-select** — recommending the first option without comparison.
3. **Outside-view-first** — inside-view detail-reasoning that misses base rates.
4. **Name-your-uncertainty** — equally-confident prose regardless of actual confidence.
5. **Consequence-imagine** — recommending patterns without modelling failure modes.

It is **not** a code reviewer, **not** a post-hoc output grader, **not** an RFP/contract/document review tool. Those slices are well-served elsewhere (CodeRabbit, Greptile, Qodo, Prometheus, G-Eval, FACTS Grounding, Vijayaraghavan et al.'s "Team of Rivals" — [arXiv 2601.14351](https://arxiv.org/abs/2601.14351)). See [`upgrades/profound/2026-05-09-sota-survey-the-actual-gap/`](upgrades/profound/2026-05-09-sota-survey-the-actual-gap/) for the full SOTA comparison.

**What it claims to be:**
- A fixed adversarial-review workflow (13 steps), not a soft pattern.
- Multi-lens (architecture / operations / product), with minority-veto.
- Anti-anchoring by artifact discipline — raw subagent output stays on disk; only distillations reach the orchestrator.
- Canon-first and outside-view-first by *mandatory step ordering*, not by prompt.

**What it does not claim:**
- *Information independence* between lenses. Lenses share a common candidate; decorrelation is by **role/aspect** (different prompts ask different questions) and optionally by **model family** (`SHADOW_PANEL=1`). Inter-input independence is not enforced.
- *Universal superiority* of multi-agent decomposition. Recent results ([arXiv 2604.02460](https://arxiv.org/abs/2604.02460), [2602.01011](https://arxiv.org/abs/2602.01011), [2503.13657](https://arxiv.org/pdf/2503.13657)) show multi-agent often loses to a single well-prompted judge on simpler tasks. Use this stack when frame error is plausibly the binding constraint; otherwise, don't.

**Drift detection.** A claim that this stack is "three independent critics" is wrong as written. The stated property is the one above. If a future edit silently re-introduces a stronger claim, that is regression. The ledger schema and this Mission section are the audit anchors.
