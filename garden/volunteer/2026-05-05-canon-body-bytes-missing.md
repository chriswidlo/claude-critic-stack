# Canon body bytes missing for three Anthropic entries

| Field | Value |
|---|---|
| 📌 **title** | Canon body bytes missing for three Anthropic entries |
| 🎯 **category** | 🍀 volunteer |
| 👤 **author** | ai |
| 📅 **created** | 2026-05-05 |
| ⚡ **catalyst** | While running the canon-librarian during session `2026-04-25-au-banking-kb-sota` (RAG patterns research), the librarian discovered it could not quote any Anthropic essay despite three of them being marked as fully ingested. `citation.yaml` for each declares `body_completeness: full`, but the corpus directory contains only `citation.yaml` + provenance `README.md` — no `body.md` or `source.txt` is on disk. |
| 💡 **essence** | The canon has a silent integrity gap: metadata claims completeness the filesystem does not back up. The librarian honored its no-paraphrase-from-memory rule and surfaced the gap, which means any prior session that quoted these essays was either reconstructing from training data or quoting the empty file (silently failing). |
| 🚀 **upgrade** | Re-ingest the three entries so a body file lands on disk, OR fix the ingester (`bin/ingest-canon.mjs`) to refuse to mark `body_completeness: full` without writing a body, OR add a verifier that flags drift between `citation.yaml` and on-disk artifacts. The first restores the immediate value; the second prevents recurrence. |
| 🏷️ **tags** | canon, integrity-bug, librarian, ingestion |
| 🔖 **committed_in** | 19e73f9 (curative re-ingest), b36e40e (preventive gate + verifier) |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-05 | — | — | — | — | 2026-05-17 | 2026-05-17 | 2026-05-17 | — | — |

## Table of contents

- [What the librarian saw](#what-the-librarian-saw)
- [Why this matters more than it looks](#why-this-matters-more-than-it-looks)
- [The three affected entries](#the-three-affected-entries)
- [Two fixes — one curative, one preventive](#two-fixes--one-curative-one-preventive)

## What the librarian saw

When asked to surface RAG/retrieval material, the canon-librarian inspected each potentially-relevant entry directory. For three Anthropic entries, the structure was:

```
canon/corpus/anthropic-effective-context-engineering/
├── citation.yaml            # body_completeness: full, sha256 recorded
└── README.md                # provenance only
```

No `body.md`, no `source.txt`, no HTML — only the metadata claiming completeness. The librarian followed its no-paraphrase rule and reported the gap rather than hallucinating quotes.

## Why this matters more than it looks

This is a **silent failure mode**. There is no error at retrieval time, no alarm in CI, no broken link. The librarian just returns less than it should — and unless someone notices, the silence reads as "canon has nothing to say on this topic."

Worse: any previous session that *did* receive useful quotes from these entries was either getting them from the model's training data leaking through (anti-canon), or operating in a state where these files existed and were later removed (history would show this), or running with some now-absent retrieval path. None of those failure modes are visible at the call site.

## The three affected entries

- `canon/corpus/anthropic-effective-context-engineering/` (Anthropic, 2025) — *Effective Context Engineering*
- `canon/corpus/anthropic-multi-agent-research-system/` (Anthropic, 2025) — *Multi-agent research system*
- `canon/corpus/anthropic-building-effective-agents/` (Anthropic, 2024) — *Building Effective Agents*

All three are publicly fetchable; re-ingestion is mechanical.

## Two fixes — one curative, one preventive

**Curative (~30 minutes):** re-run the ingester against the three URLs so a body lands on disk. Verify `sha256(body)` matches the recorded `citation.yaml` value; if it doesn't, the recorded sha is from a different snapshot and should be updated.

**Preventive (~1 hour):** modify `bin/ingest-canon.mjs` to refuse to write `body_completeness: full` unless a body file is present and its sha256 verifies against the metadata. Alternatively, add a `bin/verify-canon.mjs` that walks the corpus and exits non-zero on drift; wire it into a pre-commit or CI hook.

The curative fix is independent of the preventive one. Both are single-sitting tasks. Either one alone improves the situation; both together close the loop.
