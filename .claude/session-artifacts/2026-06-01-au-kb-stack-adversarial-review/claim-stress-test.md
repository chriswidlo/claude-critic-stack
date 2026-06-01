# Question 2 — Stress-test of the five claims, ranked weakest → strongest

Ranking by *how easily I can break it*. Weakest first.

---

## (e) "The anti-hallucination stack reduces hallucination on numeric/tabular claims." — WEAKEST

**This is the claim that breaks cleanest, and it's the one that matters most for banking.**

The architecture's anti-hallucination story is: contextual retrieval + hybrid + rerank (Layer
3) + citation/version-anchoring (Layer 5). Every cited number for that stack — the 5.7% → 1.9%
chain — measures **retrieval failure rate**: *did the right chunk make it into the top-k?* None
of it measures **grounding faithfulness**: *given the right chunk, did the model emit the right
number?*

These are different variables, and independent research says they barely correlate.
"Benchmarking LLM Faithfulness in RAG" (EMNLP 2025, arXiv 2505.04847) finds a *"weak and
inconsistent relationship between retrieval quality and generation faithfulness"* — high-quality
retrieval frequently co-occurs with unfaithful generation. The architecture's **own**
outside-view already conceded this from the other direction: tabular/cross-referenced content is
failure mode #2 and *"unsolved at the general level"*
([outside-view-raw.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/outside-view-raw.md) §4).

So the stack pours its effort into the variable (retrieval recall) that the worst failure mode
(wrong capital-ratio number, wrong fee, wrong threshold) is *least* sensitive to. A model can
retrieve APS 112 §27 perfectly and still transpose a digit, misread a table cell, or apply a
superseded rate. **Verdict: the anti-hallucination claim is asserted, not evidenced, and is
aimed at the wrong metric.** What would actually move numeric faithfulness — verbatim-span
quoting, table-cell-level extraction, a numeric-faithfulness eval gate, refusal-on-ambiguity —
is exactly what the stack does *not* foreground.

---

## (b) "Build the full stack" vs "BM25 baseline, earn each component via eval." — SECOND WEAKEST

The research **states the right principle and then violates it.** It says "eval harness first…
without this, 'SOTA' is a literature reflex"
([research-rag-patterns.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/research-rag-patterns.md) §9.3)
— then immediately specifies Voyage-3-large + Qdrant + contextual retrieval + Voyage rerank-2.5
+ optional GraphRAG/RAPTOR, **before a single eval point exists.** That is the literature reflex
it warned against.

Independent evidence backs the user's instinct: BEIR (Thakur et al., NeurIPS 2021) shows **BM25
is a strong zero-shot/out-of-domain baseline**, often beating more complex neural retrievers
absent in-domain training — and in-domain wins don't predict out-of-domain generalization. For a
*novel* regulatory corpus with no labeled data, BM25 + structured metadata filter is not a
strawman floor; it is a genuinely competitive starting point that the full stack must *earn* its
way past on a real eval. The original's own contradicting source ("stop optimizing retrieval",
ragaboutit 2025) says the same.

**Verdict: (b) is weak as stated.** The eval-first principle, taken seriously, *mandates* the
BM25 baseline the user proposes and forbids speccing the full stack up front. The research
should have ended at "build BM25 + eval, then earn each layer," and instead it pre-committed.

---

## (c) "BUILD rather than FEDERATE the law." — PARTIALLY WEAK (and the user's premise is shaky too)

This one cuts both ways, and intellectual honesty requires saying so.

- **Against build:** FRL point-in-time *compilations* (the law as in force on a date) are a free,
  core feature of legislation.gov.au. For the legislation subset, building and maintaining your
  own version-history store partly **rebuilds a free public good** — and version-anchoring law
  yourself means you, not the Commonwealth, are now liable for getting "as in force on date X"
  right.
- **For build (defending the original):** the user's premise that *"the FRL API gives
  point-in-time text free"* is **not verified.** A clean official machine-readable API / OData is
  not clearly documented; programmatic access today largely means scraping or third-party bulk
  datasets (ALRC DataHub). The original explicitly left this as "unverified (uncertainty #2)" —
  and that caution was correct. Federation needs a *queryable point-in-time API*, not just a
  website with point-in-time pages.
- **Scope correction either way:** "the law" is only one source class. APRA prudential standards,
  ASIC RGs/instruments, AUSTRAC guidance, and bank-internal policy are **not** on FRL and cannot
  be federated from it. So "build vs federate" is a **per-source** decision (the synthesis
  already said this), and the headline "build the law" over-generalizes from one tractable subset.

**Verdict: moderately weak as a blanket claim.** The right answer is "federate the legislation
subset *if and only if* a point-in-time API is confirmed; the API is currently unconfirmed; build
everything else." Neither the research's "build" nor the user's "federate" survives as stated.

---

## (d) "MCP is the right interface for a single first consumer." — MODERATELY WEAK (YAGNI)

The typed-tool / ACI argument is real: a narrow `find_prudential_standard()` tool beats a generic
`search()` endpoint, and the chunk contract is a clean boundary. But **MCP-over-HTTP** for *one*
in-process consumer buys a server, auth, rate-limiting, hosting, and a refresh worker to solve a
problem one consumer doesn't have: cross-process, cross-team tool sharing.

The specimen **admits this against itself**: the slot's value "is the slot, not any single
instance," and "the second-through-Nth silo cost goes from months to configuration"
([topical-mcp-silo-slot.md](garden/specimen/2026-05-05-topical-mcp-silo-slot.md)). By its own
logic, with N=1 consumer there is no slot value yet — only slot *cost*. The repo's own
`canon-librarian` is cited as "the embryonic in-stack form": an **in-process** tool, no HTTP, no
auth. That is the right shape until a second consumer exists.

**Verdict: weak as a day-one choice — premature interface generalization.** Ship the retrieval
logic as a library / in-stack Agent tool first; wrap it in MCP-over-HTTP the day a second,
out-of-process consumer is real. MCP is the right *eventual* interface, not the right *first* one.

---

## (a) "hybrid-RAG + provenance is right for a regulated point-in-time corpus." — STRONGEST

I cannot break the direction, only the packaging.

Hybrid (BM25 + dense + RRF), a structured metadata pre-filter on
`(instrument, section, version, effective_date)`, and a non-optional citation contract are all
well-supported — BM25 carries exact-token defined-term/section lookups dense embeddings strip,
and the metadata filter (the synthesis's own "underrated lever") does most of the regulated-text
work *before* semantics. The provenance contract is simply correct for an auditable domain.

What I *can* contest: (i) the "3-layer grounding" branding (claim e) is mis-aimed; (ii) "hybrid"
should be *earned* on the eval, not pre-bundled with contextual + rerank + a managed vector DB
(claim b); (iii) for point-in-time supersession, much of this is a **structured-query** problem,
not a semantic-retrieval one (see [alternatives.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/alternatives.md)).

**Verdict: directionally sound; the failure is sequencing and labeling, not the core idea.**

---

## Ranking summary (weakest → strongest)

1. **(e)** anti-hallucination on numeric/tabular — *mis-aimed at retrieval recall; independent
   evidence says recall ≠ faithfulness.*
2. **(b)** build-it-all vs earn-it — *violates its own eval-first rule; BM25 baseline is genuinely strong.*
3. **(c)** build vs federate the law — *blanket claim over-generalizes; both premises unverified.*
4. **(d)** MCP for one consumer — *YAGNI; in-process tool until a 2nd consumer exists.*
5. **(a)** hybrid + provenance — *sound direction; only packaging/sequencing is contestable.*
