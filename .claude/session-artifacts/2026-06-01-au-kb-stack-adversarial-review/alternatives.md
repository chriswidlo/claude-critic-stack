# Question 3 — Alternative architectures the research did not seriously consider

The survey covered the *retrieval* design space exhaustively (naive RAG, hybrid, contextual,
rerank, ColBERT, GraphRAG, RAPTOR, agentic, long-context). It treated the problem as
**"which retrieval technique?"** throughout. The alternatives below reject that framing.

## Alternative A (primary) — Structured / relational-first, retrieval as a column

**The corpus's defining pain is not fuzzy semantic recall. It is versioned, numeric, tabular
facts with supersession.** That is a *database* problem before it is a retrieval problem.

Model the law as a normalized store keyed by `(instrument, section, version, effective_date,
supersedes)`:
- **Point-in-time** becomes a `WHERE effective_date <= :asof AND (superseded_at IS NULL OR
  superseded_at > :asof)` clause — exact, auditable, not probabilistic top-k.
- **"What changed between date X and Y"** becomes a diff/`EXCEPT` query — impossible to express
  cleanly in a vector index, trivial here.
- **Tables** (capital ratios, fee schedules) are stored *as rows/cells*, queried structurally,
  and quoted verbatim — never chunked into prose and re-summarized.
- **Full-text / BM25** lives as an index *column* (Postgres FTS, SQLite FTS5) for the genuinely
  fuzzy "find the clause about X" queries — a feature, not the architecture.
- The agent emits **typed queries against a known schema** (`get_section(instrument, section,
  asof)`, `diff_instrument(instrument, from, to)`), so the hard regulatory work is deterministic
  SQL, and the LLM is used only where language understanding is actually required.

The research considered and *rejected* filesystem-grep ("the corpus is graph-shaped"
— [challenges.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/challenges.md)) but
**never considered relational-first at all.** Yet "graph-shaped" (cross-references,
supersession chains, jurisdictional overlays) is exactly what relational schemas and recursive
CTEs were built for. Vector search is the right tool for *semantic* recall over unstructured
prose; it is the wrong default for *structured point-in-time legal lookup*.

This also reframes claim (e): with a structured store, the numeric/tabular answer is a **cell
fetched by key and quoted verbatim**, so there is no chunk-to-prose-to-number hallucination
surface for the high-value queries. Faithfulness is achieved by *construction*, not by ranking.

## Alternative B — Citation-by-construction (verbatim spans, never paraphrase)

Orthogonal to the retrieval choice. Store the **actual source bytes + character offsets**; the
tool returns a verbatim span with `(instrument, section, version, effective_date, byte_range)`
and the agent is constrained to **quote, not paraphrase, regulatory numbers and definitions.**
The original's Layer 5 binds citations to *content-hashed bytes* (an architecture-critic
fold-in) — good — but still serves *chunks the model summarizes.* Citation-by-construction
closes the gap that arXiv 2505.04847 exposes: it removes the model's opportunity to extrapolate
on the facts that carry legal/numeric risk.

## Alternative C — Costed Frame F (thin agent over sources + a cache), actually priced

The synthesis *named* Frame F ("no KB; thin agent over canonical sources + a citation contract")
but **never costed it against the full build.** For a single first consumer with a bounded
source list, "fetch-on-read from FRL/APRA/ASIC + cache + citation contract" may dominate the
five-layer build on time-to-value and on staleness (nothing is staler than your own snapshot of
a corpus the publisher already version-controls). Frame F deserved a real cost line, not a
footnote — its omission biases the decision toward "build."

## Alternative D — BM25/FTS-only + LLM rerank, *no embeddings, no vector DB*

The literal baseline claim (b) asks for, and the research never benchmarked. Given BEIR's
out-of-domain BM25 result, this may sit within a few points of the full stack on a real
regulatory eval — at a fraction of the cost and operational surface (no embedding model, no
vector DB opex, no contextualization re-runs). It is the honest control arm the eval-first
principle demands.

## Why these were missed

All four fall *outside* the "which retrieval technique" frame that the vendor-blog corpus is
written in. Vendor surveys don't propose "use Postgres and mostly don't retrieve" because that
isn't a product. This is the correlated-evidence problem
([convergence-audit.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/convergence-audit.md))
showing up as a *blind spot in the option set*, not just in the rankings.
