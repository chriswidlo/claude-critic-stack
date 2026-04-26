# claude-critic-stack

A stack-agnostic adversarial review layer for architecture and design decisions.

## What this is

Three things:

1. **A critic subagent** with explicit authority to reject, structured to resist agreeability and local anchoring.
2. **A canon librarian subagent** that retrieves from a curated corpus of industry literature — and is required to return contradicting sources, not just supporting ones.
3. **An outside-view subagent** that forces reference-class forecasting before any decision.

These run *from this directory*, deliberately outside any specific repo. The working directory is the anchor for Claude's default framing — invoking the critic from inside `my-repo/` makes it reason about the repo's conventions. Invoking it from here makes it reason about the industry.

## What this is not

- Not a replacement for human architectural judgment. It's a structural compensator for known LLM failure modes (agreeability, pattern-overfit, recency bias, confident mediocrity on decisions requiring taste).
- Not a "persona agent." No "think like Martin Fowler" prompts. Personas steer vocabulary, not judgment.
- Not a silver bullet. Expect it to improve decision *quality* by surfacing ignored alternatives and stated assumptions, not to produce novel insight on its own.

## How to use

```bash
cd path/to/claude-critic-stack
claude
> I'm considering [design decision from my other repo]. Context: [...]. Review it.
```

The `CLAUDE.md` in this directory triggers the critic workflow. See `workflows/architecture-review.md` for the full routing.

## Populating the canon

See `canon/sources.yaml` for the manifest of expert sources and `canon/README.md` for ingestion notes. The corpus itself lives in `canon/corpus/` and is gitignored — you own the licensing for whatever you put there.

## Philosophy (two sentences)

Books teach what to do. Apprenticeship teaches when. This stack is a very good library with a mandatory dissenting reader attached — not an apprentice.
