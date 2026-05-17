# Add ten RAG/retrieval canon entries

| Field | Value |
|---|---|
| 📌 **title** | Add ten RAG/retrieval canon entries |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | ai |
| 📅 **created** | 2026-05-05 |
| ⚡ **catalyst** | The canon-librarian, asked during session `2026-04-25-au-banking-kb-sota` for material on RAG, hybrid retrieval, reranking, GraphRAG, ColBERT, contextual retrieval, agentic retrieval, vector DBs, embeddings, and MCP-as-knowledge-surface, returned a structural empty hand: zero of 19 corpus entries cover any of those topics. The full survey it triggered — `.claude/session-artifacts/2026-04-25-au-banking-kb-sota/research-rag-patterns.md` — had to be sourced almost entirely from WebSearch. |
| 💡 **essence** | A workflow that produces canon-grounded design recommendations cannot do its job on a topic the canon is silent about. Retrieval architectures are exactly the kind of topic the workflow will be asked about repeatedly (every "knowledge silo" question routes through them). The gap is foundational, not incidental. |
| 🚀 **upgrade** | A focused curator session (or `canon-refresher` invocation followed by acceptance) that adds ten foundational RAG/retrieval entries. All ten URLs are open-access and listed below. Once in canon, future sessions on knowledge-tool design can lean on the librarian instead of falling back to WebSearch with no anti-confirmation rule. |
| 🏷️ **tags** | canon, retrieval, rag, mcp, gap-filling |
| 🔗 **relates_to** | 2026-04-26-corpus-bias-compensation-step, 2026-05-05-canon-body-bytes-missing |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-05-05 | — | — | — | — | — | — | — |

## Table of contents

- [The gap, stated](#the-gap-stated)
- [The ten proposed entries](#the-ten-proposed-entries)
- [Why these ten and not others](#why-these-ten-and-not-others)
- [How to add them — two paths](#how-to-add-them--two-paths)

## The gap, stated

The librarian's report is in the session-artifacts; the headline is that the corpus has **no entry** on any of: RAG as a pattern (no Lewis 2020), hybrid search / BM25+dense fusion, reranking (cross-encoder, ColBERT/late interaction), GraphRAG, contextual retrieval (notable miss — three other Anthropic essays are in-corpus), agentic retrieval, vector databases, embedding models, MCP-as-knowledge-surface (the MCP spec itself is absent from `sources.yaml`), or retrieval evaluation harnesses (Ragas, BEIR, TREC-RAG).

The `refresh-feeds.yaml` keyword filter (line 25) already includes `retrieval` and `tool-use` — so the refresher is *configured* to surface these. Nothing has been accepted into the corpus yet.

## The ten proposed entries

In rough order of foundationality:

1. **Lewis et al. 2020** — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — the original RAG paper.
2. **Karpukhin et al. 2020** — *Dense Passage Retrieval for Open-Domain Question Answering* (DPR) — dense-retrieval foundation.
3. **Khattab & Zaharia 2020** — *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT* — late-interaction foundation.
4. **Robertson & Zaragoza** — *The Probabilistic Relevance Framework: BM25 and Beyond* — sparse-retrieval reference.
5. **Edge et al. 2024** (Microsoft Research) — *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — GraphRAG canonical reference.
6. **Anthropic, Sep 2024** — *Contextual Retrieval* — the 5.7% → 1.9% benchmark and method. Notable miss given three other Anthropic essays are already in-corpus.
7. **Han et al. 2025 (arXiv 2506.05690 → ICLR'26)** — *When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation* — the GraphRAG corrective. Critical for not defaulting to GraphRAG.
8. **Sarthi et al. 2024** — *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*.
9. **Anthropic 2024** — *Model Context Protocol* specification — currently absent from `sources.yaml`, `sources.ingest.yaml`, and `refresh-feeds.yaml` entirely. The protocol the workflow's knowledge tools will speak.
10. **Ragas** (Es et al. 2023) **or BEIR** (Thakur et al. 2021) — a retrieval evaluation harness reference. Ragas is closer to LLM-eval; BEIR is closer to IR-eval. Pick by which the curator wants — both are open-access.

All ten are open-access. The MCP spec, the Anthropic essays, and the arXiv papers are direct fetches; ColBERT and DPR are arXiv; Lewis is on arXiv and OpenReview; RAPTOR is arXiv; Ragas and BEIR have papers + GitHub.

## Why these ten and not others

The criterion was *foundationality and contradiction coverage*, not popularity. Specifically:

- Each of items 1–4 is a *foundation* — it defines a primitive that everything downstream cites. Skipping them weakens the canon's ability to ground later sessions.
- Items 5 and 7 are deliberately a **claim/counter-claim pair** on GraphRAG. The librarian should be able to surface both when asked.
- Item 6 fixes a specific detected miss (other Anthropic essays in, this one out).
- Item 9 is mechanical canon hygiene — the protocol exists, the workflow uses it, the canon should reference it.
- Item 10 is a deliberate choice to add an *evaluation* reference — the workflow keeps recommending eval harnesses without canon support for what an eval harness *is*.

This is **not** an exhaustive list. Other strong candidates exist (Self-RAG, CRAG, HyDE, SPLADE, monoT5, the MTEB paper, Anthropic's Skills essays, vector-DB technical docs). They can land in a second batch; the ten above are the foundation.

## How to add them — two paths

**Path A — refresher-then-accept (canonical):** invoke `canon-refresher` with these ten URLs as targets. It proposes entries; the curator accepts by pasting into `canon/sources.ingest.yaml`. The ingester (`bin/ingest-canon.mjs`) does the rest. Slowest but follows the existing acceptance discipline.

**Path B — direct curator session:** the curator manually adds entries to `canon/sources.ingest.yaml` and runs the ingester. Faster; bypasses the refresher's stub-vs-fetch logic. Appropriate for a one-time foundational batch.

Either way, before adding: run the canon body-bytes fix (related entry `2026-05-05-canon-body-bytes-missing`) to ensure the ingester actually writes body files. Adding ten more entries while the integrity bug is unfixed would multiply the silent-failure surface tenfold.
