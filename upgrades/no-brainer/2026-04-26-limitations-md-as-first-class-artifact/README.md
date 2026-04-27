# `limitations.md` as a first-class per-session artifact

| Field | Value |
|---|---|
| 📌 **title** | `limitations.md` as a first-class per-session artifact |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective was itself an extraordinary instance of metacognitive self-reporting — the AI naming, in detail, what it skipped, where it lost the plot, what it claimed without evidence. The operator's question: *"is system self-reporting this kind of things while it runs? could it be writing down to some docs, comments, or self-reporting whenever it encounters something it notices about itself?"* The honest answer was no — there is no such artifact, and there is no established AI-community pattern for one. |
| 💡 **essence** | Per-session, in-flight, append-only artifact under `.claude/session-artifacts/<id>/limitations.md`. Format: `[step-N] [severity: low|med|high] [category: skipped-tool|harness-limit|context-bloat|drift|low-confidence|over-claimed|model-self-doubt] observation. affected-output: yes|no|unknown. suggested-fix: <one line>.` Written by any agent or the orchestrator whenever a meta-issue surfaces — *as it happens*, not at the end. |
| 🚀 **upgrade** | The class of failure currently invisible until manually surfaced (subagent claimed-but-didn't, orchestrator drift, low-confidence dressed as confident, harness limit hit) becomes visible in real-time. Cross-session aggregation surfaces patterns: which limitation categories recur, which sessions hit harness limits, which agents over-claim. Pairs with the proposed `subagent-claimed-writes-not-on-disk` verification hook to make the audit chain self-reporting rather than reconstruction-after-the-fact. |
| 🏷️ **tags** | metacognition, self-reporting, audit, in-flight, session-artifacts |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The artifact's shape](#the-artifacts-shape)
- [Why no-brainer](#why-no-brainer)
- [Adjacent prior art (and why it doesn't quite fit)](#adjacent-prior-art-and-why-it-doesnt-quite-fit)

## The artifact's shape

`session-artifacts/<id>/limitations.md`. Append-only, structured-but-light. Exists from session start, may have zero entries. Each entry one line:

```
[step-N] [severity: low|med|high] [category: skipped-tool|harness-limit|context-bloat|drift|low-confidence|over-claimed|model-self-doubt|other] observation. affected-output: yes|no|unknown. suggested-fix: <one line or "n/a">.
```

CLAUDE.md addition (in "Things you must do, in flight" — a new mirror section to the existing "Things you must not do"):

> Whenever you notice a meta-issue that affected the work — skipped a tool you should have used, hit a harness limit, felt context bloat, drifted from the user's question, dressed low-confidence in confident architecture, surfaced an unverified citation, conflated two questions, or were stopped by a hook — append a one-line entry to `limitations.md`. Do this *as it happens*, not at the end. The retrospective is not a summary written at synthesis; it is an audit trail accreting in flight.

A `Stop` hook (optional) reads `limitations.md` at session end and surfaces high-severity entries in the final user-facing message before synthesis.

## Why no-brainer

The implementation is text — a CLAUDE.md instruction and an artifact path convention. No new agents, no schemas to design, no tooling. The pattern works the day it lands.

The value is real and known: the operator's manual retrospective was high-quality; the structural version makes it routine instead of bespoke. The category enum forces specificity (you can't write "I went off track" in three paragraphs of hedging — you write `[step-7] [med] [drift] orchestrator started designing the workflow itself instead of the user's question`).

The cost surface is small. Every session writes a few entries to a file. If a session writes none, that is also signal.

## Adjacent prior art (and why it doesn't quite fit)

There is no canonical pattern for runtime metacognitive logging in AI agent systems. Pieces exist:

- **Reflexion** (Shinn et al., 2023) — agents reflect on outputs and update episodic memory before retrying. Closest academic analog. Limitations.md is simpler — append-only, no retry loop, no learning-from-it baked in.
- **Self-Refine** (Madaan et al., 2023) — generate, critique, refine. Different intent (output quality, not failure-mode logging).
- **Operational tracing** (LangSmith, Langfuse, Arize Phoenix) — captures tool calls and latencies, not self-reported failure modes.
- **Postmortem culture** (Google SRE) — well-established for human teams; no codified version for in-flight agents.

The closest published Anthropic discussion is in the multi-agent paper, where filesystem artifacts are recommended over inline conversation passing. limitations.md is in that spirit — a filesystem artifact for the agent's *own meta-observations*, sibling to the session-artifacts that already exist for substantive work.

This pattern, if it works, is generalizable beyond this stack and worth writing up for the community. That is downstream of value-proving it here first.
