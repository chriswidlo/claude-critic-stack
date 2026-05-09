# claude-critic-stack

*Rigorous second opinions for important decisions.*

A solo, closed-world adversarial-design-review harness. You bring a design question; the stack runs a 12-step workflow with a three-lens critic panel, a canon librarian over a curated corpus, and an outside-view forecaster. Runs from this directory — never inside the target repo, deliberately, so Claude's default frame is "the industry" rather than "your codebase."

## Quickstart

**What it does** — You bring a hard design question. The stack stress-tests it before answering.

**What you get back** — A recommendation, named tradeoffs, dissenting evidence, three uncertainties.

**How long** — Minutes. You don't drive — read the synthesis at the end.

**How to start** — Type your question. Prefix `quick take:` for a one-paragraph version instead of the full review.

*Already running `claude` in this repo? Type `/explain` for the live tour — current canon, session history, an interactive picker.*

## What it is

- **Three-lens critic panel** — `critic-architecture`, `critic-operations`, `critic-product`. Each lens has authority to reject; minority-veto. Optional shadow lenses on a second model triangulate by model diversity (`SHADOW_PANEL=1`).
- **Canon librarian** over [`canon/corpus/`](canon/corpus/). Required to surface at least one contradicting passage per query. Currently grep + Read over plain text; a chunker + BM25 index is planned (see [`plans/`](plans/)).
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

- **Decision-shaped question** ("should I X?", "design Y", "is Z a good idea?") → full 12-step workflow.
- **Knowledge-shaped question** ("what does the CAP theorem say?", "explain X") → answered directly from canon, no workflow.

Explicit trigger phrases (type them literally to force a path):

- **`quick take: <question>`** — bypass the workflow for a single-paragraph answer. Use sparingly; the structure exists for a reason.
- **`skip the critic-panel`** (or `skip the critic`) — runs the full workflow but skips steps 10–11.

Slash commands (zero-friction utilities):

- **`/explain`** — this menu, on demand, without leaving chat.
- **`/upgrade`** — capture a creative R&D idea into [`upgrades/`](upgrades/).
- **`/session-bootstrap`** or **`/critique-prep`** — mint a session manually for staged inputs.
- **`/critique-start`** — in a fresh session, runs the 12-step workflow against an input prepared by `/critique-prep`. The two skills are a pair: `prep` collects the design doc + target repo + grounding strategy, `start` runs the workflow against frozen inputs in a clean context window.

[`CLAUDE.md`](CLAUDE.md) is the operating manual — the 12-step workflow, the hard gates, the must-nots, and the agent inventory all live there. Read it.

## Populating the canon

- [`canon/sources.ingest.yaml`](canon/sources.ingest.yaml) — machine-readable manifest of fetchable open-access sources.
- [`canon/sources.yaml`](canon/sources.yaml) — human-readable manifest grouped by topic.
- `node ./bin/ingest-canon.mjs` — fetch open-access entries (HTML, arXiv abstracts, AWS docs, multi-page TOCs). Idempotent; `--force` re-fetches; `--only=<slug>` restricts.
- `node ./bin/ingest-owned-book.mjs <slug> <path-to-text>` — for books you own, populate a stub from local plaintext.
- `canon/corpus/*/source.txt` is gitignored. Stubs and `citation.yaml` files are tracked so the inventory stays visible in git.

You own the licensing for whatever you put in `canon/corpus/`. See [`canon/README.md`](canon/README.md) for the policy.

## Philosophy

Books teach what to do. Apprenticeship teaches when. This stack is a very good library with a mandatory dissenting reader attached — not an apprentice.

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
- A fixed adversarial-review workflow (12 steps), not a soft pattern.
- Multi-lens (architecture / operations / product), with minority-veto.
- Anti-anchoring by artifact discipline — raw subagent output stays on disk; only distillations reach the orchestrator.
- Canon-first and outside-view-first by *mandatory step ordering*, not by prompt.

**What it does not claim:**
- *Information independence* between lenses. Lenses share a common candidate; decorrelation is by **role/aspect** (different prompts ask different questions) and optionally by **model family** (`SHADOW_PANEL=1`). Inter-input independence is not enforced.
- *Universal superiority* of multi-agent decomposition. Recent results ([arXiv 2604.02460](https://arxiv.org/abs/2604.02460), [2602.01011](https://arxiv.org/abs/2602.01011), [2503.13657](https://arxiv.org/pdf/2503.13657)) show multi-agent often loses to a single well-prompted judge on simpler tasks. Use this stack when frame error is plausibly the binding constraint; otherwise, don't.

**Drift detection.** A claim that this stack is "three independent critics" is wrong as written. The stated property is the one above. If a future edit silently re-introduces a stronger claim, that is regression. The ledger schema and this Mission section are the audit anchors.
