# Agentic-engineering reference library from session research

| Field | Value |
|---|---|
| 📌 **title** | Agentic-engineering reference library from session research |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session 2026-04-26 — extensive research on Claude Code expert practitioners (Boris Cherny, IndyDevDan, Cole Medin, Anthropic engineering, Sankalp). Output assembled in `temporary/`: a 409-entry decision registry, a 327-line narrative playbook, four full video/podcast transcripts, and a README. The session ended with the operator asking how to extract durable value from this material rather than letting it die in `temporary/`. |
| 💡 **essence** | A large body of cited, structured material on agentic engineering and Claude Code practice was produced as a side effect of a research session. The material is not canon-shaped (heavily four-voice), but it is operator-grade reference: a registry of definitive rules, a narrative companion, and the primary-source transcripts behind both. Letting it sit in `temporary/` wastes it; lifting it whole into `canon/` violates the anti-confirmation rule. The right move is a third home — an operator-facing reference library — plus selective canon promotion of the transcripts as primary sources. |
| 🚀 **upgrade** | Promote the `temporary/` artifacts to a permanent `references/agentic-engineering/` library that the operator (and future agents that read it, e.g. `claude-code-guide`) can rely on, while routing the transcripts through canon-refresher as individual primary-source entries. This gives the repo a durable knowledge base for the domain it most closely operates in (agentic systems) without polluting canon with viewpoint-monoculture. |
| 🔗 **relates_to** | wire-claude-code-guide, citation-audit-as-canon-discipline, corpus-bias-compensation-step |
| 🏷️ **tags** | reference, canon, claude-code-guide, agentic-engineering, viewpoint-diversity, operator-tooling |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What's in `temporary/` right now](#whats-in-temporary-right-now)
- [The asymmetry of value](#the-asymmetry-of-value)
- [Why "lift the whole folder into canon" is wrong](#why-lift-the-whole-folder-into-canon-is-wrong)
- [Why "delete it" is also wrong](#why-delete-it-is-also-wrong)
- [The proposed third path](#the-proposed-third-path)
- [Concrete migration plan](#concrete-migration-plan)
- [Open questions deliberately left for the workflow](#open-questions-deliberately-left-for-the-workflow)
- [What success looks like](#what-success-looks-like)

## What's in `temporary/` right now

A research session that started as *"what are the best Claude Code YouTube channels?"* expanded — through the operator's *"learn everything from them"* prompt — into ~14 hours of mixed-source synthesis. The output, on disk:

```
temporary/
├── README.md                              (index)
├── decision-registry.md                   ★ 409 sourced entries, 26 sections (A–Z)
├── claude-code-expert-playbook.md         narrative version, 327 lines
└── transcripts/
    ├── 01-indydevdan-the-claude-code-feature-senior-engineers-keep-missing.md
    ├── 02-indydevdan-one-agent-is-not-enough.md
    ├── 03-cole-medin-gitnation-talk-PLACEHOLDER.md  (transcript not provided)
    ├── 04-anthropic-even-engineers-use-this-workflow.md
    └── 05-boris-cherny-lennys-podcast.md
```

Sources weighted by entry count: Anthropic engineering blog (already partly in canon), Boris Cherny (Lenny's podcast + 87-tip compilation + Pragmatic Engineer interview), IndyDevDan (two transcripts + course curriculum), Anthropic engineers / Mejba video on interactive artifacts, Cole Medin (PIV/PRP framework), Sankalp's production-user blog, disler's open-source hooks repos.

The registry is **definitive-only**: every entry has a rule, a *why*, and a citation. Speculation was dropped. Where two sources disagreed, the more specific or more recent was kept.

The transcripts are **verbatim primary sources** with one prompt-injection audit note (a fake user/assistant exchange embedded in the Anthropic engineers transcript was preserved at the bottom of that file, marked).

## The asymmetry of value

This material is asymmetric in two important ways and the upgrade has to respect both.

**First asymmetry — quality vs. diversity.** The material is high-quality (sourced, terse, definitive) but low-diversity (≈5 voices, all bullish on agentic coding). For canon retrieval, diversity matters more than quality past a threshold — the librarian's job is to surface dissent, not to reinforce consensus. For operator reference, the opposite is true: quality and recall matter more than diversity, because the operator is using it to *act*, not to *audit a recommendation*.

**Second asymmetry — synthesis vs. source.** The registry and playbook are remixes; the transcripts are primary sources. A canon entry needs an atomic citable source — *"per Boris Cherny on Lenny's Newsletter, 2026-04-25, [exact claim]"*. The transcripts have that property; the registry does not.

These two asymmetries point at two different homes inside the repo, not one.

## Why "lift the whole folder into canon" is wrong

The repo's `CLAUDE.md` is explicit:

> *"Do not treat canon retrieval as confirmation. If every passage agrees with you, you didn't search hard enough."*

The 409 registry entries mostly agree with each other. There is no skeptic position represented — no "agentic coding is overhyped," no documented multi-agent production failure case study, no piece arguing CLAUDE.md is the wrong abstraction. Adding the registry as canon entries would weaken the librarian-first rule rather than strengthen it.

It would also overlap directly with three canon entries that already exist: `anthropic-building-effective-agents`, `anthropic-effective-context-engineering`, `anthropic-multi-agent-research-system`. The registry is partly downstream of those.

## Why "delete it" is also wrong

This repo is itself an agentic system — multi-agent workflow, hooks, subagents, skills, the same primitives the registry is about. When the critic stack reviews a design question about agentic patterns (and increasingly it will), the operator and the agents both need accessible domain reference. The transcripts in particular contain claims and patterns that aren't in canon yet (specialized self-validation hooks inside skills, three-tier orchestrator/leads/workers with persistent expertise files, the three-layer interactive-artifact pattern). Throwing them away because they aren't canon-shaped is wasteful.

Also: this work pairs with two existing upgrades.

- **#9 wire-claude-code-guide** — that subagent's job is to answer "how does Claude Code do X?" questions during parallel-gather. It currently has WebFetch/WebSearch. A local reference library is a faster, cited, offline-capable answer source.
- **#7 corpus-bias-compensation-step** and **#8 citation-audit-as-canon-discipline** — both treat viewpoint-balance and citation provenance as first-class concerns. This upgrade is in the same family.

## The proposed third path

Three moves, each independently reversible:

1. **Promote `temporary/decision-registry.md` and `temporary/claude-code-expert-playbook.md` to a new `references/agentic-engineering/` directory.** Operator reference, not canon. Read by the operator and — if upgrade #9 lands — by `claude-code-guide` as a local-first answer source before WebFetch.

2. **Route the four transcripts through `canon-refresher`** as proposed primary-source entries. Each gets the standard review block; the operator accepts or discards. If accepted, they live in `canon/corpus/<source-slug>/` with proper attribution and date. The librarian retrieves them like any other source, with the citation marker `verified` per upgrade #8.

3. **Open a separate, smaller follow-up: source dissent.** Find 2–3 *contradicting* sources on agentic engineering — production failures, skeptic posts, "vibe coding considered harmful" critiques — and propose those for canon too. This is the move that makes the librarian's anti-confirmation rule actually bite when a Claude-Code-design question comes in. This is its own future upgrade entry, not part of this one.

## Concrete migration plan

If this upgrade is accepted, the implementation is bounded:

| Step | Action | Effort |
|---|---|---|
| 1 | `git mv temporary/decision-registry.md references/agentic-engineering/decision-registry.md` | XS |
| 2 | `git mv temporary/claude-code-expert-playbook.md references/agentic-engineering/playbook.md` | XS |
| 3 | Move `temporary/README.md` content into `references/agentic-engineering/README.md`, drop the "temporary" framing, update internal links | XS |
| 4 | Add a top-level `references/README.md` explaining what this directory is and how it differs from `canon/corpus/` | XS |
| 5 | For each transcript in `temporary/transcripts/`, run canon-refresher with the transcript as input. Curator accepts/discards each independently | S |
| 6 | If upgrade #9 (`wire-claude-code-guide`) is also being implemented, update its agent definition to read from `references/agentic-engineering/` first, WebFetch second | XS — only if #9 is in flight |
| 7 | Delete `temporary/` once steps 1–3 are merged | XS |
| 8 | Add an entry to `CLAUDE.md` describing what `references/` is and when to consult it (kept short — one paragraph) | XS |

Total: S effort. No design uncertainty in steps 1–4 and 7–8. Steps 5–6 depend on other workflows already being defined.

## Open questions deliberately left for the workflow

These are the points where I'm not confident and want the 12-step adversarial workflow to bite if this entry advances to `⚙️ run-through-repo`:

1. **Should `references/` exist as a sibling to `canon/`, or should it be `canon/operator-reference/` to keep all curated knowledge under one root?** Argument for sibling: different retrieval semantics (operator-read vs. librarian-read). Argument for sub-folder: fewer top-level directories, all knowledge co-located. Lean toward sibling, weakly.

2. **Does `claude-code-guide` actually want a local reference, or does its value proposition depend on freshness?** Claude Code itself is moving fast — Boris's tip #46 (`/effort max`) didn't exist a quarter ago. A local reference can date. WebFetch always reflects current docs. The right answer might be "local for canon-stable patterns, web for product-surface specifics" — but that's a design decision, not an obvious win.

3. **Are the transcripts canon-quality, or are they the wrong shape — long-form video transcripts vs. the curated essays the librarian currently retrieves?** The corpus has Anthropic engineering posts (essay-shape) and book chapters (essay-shape). A 100KB podcast transcript may need different chunking or summary metadata to retrieve usefully. Defer to canon-refresher's review block.

4. **Maintenance cadence.** When a new high-signal transcript drops (sankalp posts, Boris drops a 100-tip update), who updates the registry? Manually? Via canon-refresher routine? This is a *normal* problem, not a *normal*-tier problem — surface it but don't solve it here.

## What success looks like

If this upgrade reaches `💎 value-proved`, the signal is:

- The operator references `references/agentic-engineering/decision-registry.md` directly during a Claude Code design discussion at least twice without re-explaining its existence.
- A canon-librarian retrieval for a Claude-Code-related design question cites at least one of the migrated transcripts with a verified marker.
- A new transcript is added (post-migration) by appending to the registry rather than starting a new `temporary/` folder.

If, six months later, no one has cited it and the registry has gone stale, the entry should be honestly demoted in the body and probably the directory archived. The lab tradition is *honest negation* — if this turned out to be wrong, this entry should say so when that's clear.
