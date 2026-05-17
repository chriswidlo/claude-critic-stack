# Plan — SOTA upgrade for the canon corpus + retrieval

## Context

The repo is `claude-critic-stack`: a solo, closed-world adversarial-design-review harness. The 12-step workflow (`CLAUDE.md`) and the three-lens critic panel are mature. The **corpus and retrieval are not** — the librarian runs grep + Read over plain text, no chunking, no index, no eval. 22 corpus dirs exist; only 10 have `source.txt` (the rest are stubs); 51 of ~99 unique topics have **zero** ingested text. ~40% of ingested works are Anthropic-published. Sessions report "partial coverage" with 4–8 declared gaps every time.

`upgrades/` already files the strategic direction (`canon-coverage-audit-and-priority-additions`, `corpus-bias-compensation-step`, `closed-world-mcp-allowlist`, `citation-audit-as-canon-discipline`, `critic-panel-correlated-by-default`). This plan does the engineering and content work those entries imply, sequenced for execution.

`README.md` was stale (referenced singular "critic", pointed to `workflows/architecture-review.md` which no longer exists; the doc is now `.genesis/architecture-review.md`). Already rewritten in a separate change — short, simple, honest about current state. Layer H below is the *future* README rewrite that lands after the engineering work is done.

**Outcome:** retrieval becomes BM25-over-chunks with metadata-driven contradiction surfacing; corpus content fills the load-bearing gaps; an eval harness pins regression; `README.md` describes the system as it actually is.

---

## Hard constraints (preserved end-to-end)

1. **Closed-world.** No vendor-live retrieval. No npm install storms. Zero-dep Node 18+ for all `bin/` scripts (vendor pure-JS BM25 + Porter-2 stemmer).
2. **Contradictions are the product.** Every retrieval improvement must preserve or strengthen "≥1 contradicting passage per query."
3. **`CLAUDE.md` is frozen.** Librarian-facing changes go in `.claude/agents/canon-librarian.md`, not `CLAUDE.md`.
4. **Manual curation.** Refresher proposes; curator accepts.

---

## Layers, in execution order

### G — Reconcile sources files (foundation)

Single source of truth: `canon/sources.ingest.yaml` becomes authoritative; `canon/sources.yaml` becomes generated.

- **Modify** `canon/sources.ingest.yaml`: per-entry add `cluster:` (e.g. `distributed_systems`), `human_notes: |`, `fetchable: bool` (false for `pdf-manual`).
- **Create** `bin/sync-sources.mjs` with `--check` (diff; nonzero on drift) and `--emit` (regenerate `sources.yaml`, grouped by cluster, sorted by year, render `human_notes` as `notes:`).
- **Modify** `canon/sources.yaml`: header `# GENERATED — do not edit by hand`.
- Effort: S. Risk: one-time migration (annotate every existing ingest entry with `cluster`).

### D — Metadata schema extensions

Schema fields the librarian needs for staleness, contradiction, and source-balance:

```yaml
era: foundational | mainstream | current | frontier   # ingester defaults from year
consensus: canonical | disputed | superseded
last_validated_at: "2026-04-30"
disagrees_with: [<slug>, ...]                          # hand-curated, load-bearing
publisher_class: vendor-research | vendor-engineering | academic | independent-author | standards-body
```

- **Modify** `bin/ingest-canon.mjs` `buildCitationYaml()` — emit new fields with defaults. `era` heuristic: pre-2000 foundational; 2000–2018 mainstream; 2019–2024 current; 2025+ frontier. `publisher_class` from URL host.
- **Modify** all existing `canon/corpus/*/citation.yaml` (additive).
- **Modify** `.claude/agents/canon-librarian.md`: paragraph on how to read these fields; explicit rule that `disagrees_with` triggers a forced contradiction surface — if any chunk in top-K cites slug X and X has `disagrees_with: [Y]`, force-promote one Y chunk into the citation set.
- Effort: S. The `disagrees_with` cross-references are incremental ongoing curation work.

### A2/A3/A4 — Content fills via fetchable sources (parallel-safe, runs the existing ingester)

Extend `canon/sources.ingest.yaml` with these new entries (all open-access, all fetchable by existing modes):

**A2 — fill canonical gaps:**
- `fowler-strangler-fig` (`html`, martinfowler.com)
- `fowler-event-driven` (`html`, martinfowler.com)
- `allspaw-infinite-hows` (`html`)
- `conway-1968-how-do-committees-invent` (`html`, mirror)
- `parnas-modules-1972` (`pdf-manual` — stub until owned-book ingest)
- `cynefin-snowden-boone-2007` (`pdf-manual`)
- `team-topologies-skelton-pais-summary` (`html`, official site essay)
- `kahneman-lovallo-1993` (`pdf-manual`)
- `flyvbjerg-2006-reference-class` (`pdf-manual`)

**A3 — currency (2024–2026):**
- `mialon-gaia-2023` (arxiv 2311.12983)
- `jimenez-swe-bench-2024` (arxiv 2310.06770)
- `yao-tau-bench-2024` (arxiv 2406.12045)
- `lu-bm25s-2024` (arxiv 2407.03618) — directly justifies Layer C
- `khattab-colbert-2020` (arxiv 2004.12832) — sets the v2-deferred bar honestly
- `karpathy-software-3` (`html`, author-published)

**A4 — diversity (break Anthropic concentration toward ~25%):**
- `google-prompt-engineering-whitepaper-2024` (`html-multi`)
- `bubeck-sparks-of-agi-2023` (arxiv)
- `gorilla-patil-2023` (arxiv)
- `chatbot-arena-zheng-2023` (arxiv)
- `simon-willison-annual-review-2025` (`html`)
- `hamel-husain-evals` (`html`)

Effort: S per entry, M total. Risk: dead URLs — same defensive pattern as the existing arxiv-abs guard (`bin/ingest-canon.mjs:343`).

### B — Chunker

`bin/chunk-corpus.mjs` (new):

- Splits each `canon/corpus/<slug>/source.txt` at heading boundaries; emits `canon/corpus/<slug>/chunks/<NNNN>.md` + `chunks/manifest.json`.
- Chunk frontmatter: `chunk_id`, `slug`, `parent_heading: [...]` (max depth 4), `char_offset: [a, b]`, `token_estimate` (`chars/4`), `source_sha256_short`.
- Greedy-pack body lines under each heading until target tokens (default 500); split on `\n\n` boundary if a heading section exceeds; never mid-paragraph.
- AWS-SaaS-Lens / SRE-book have synthetic `=== Title ===` separators from existing `html-multi` / `aws-docs` modes — treat as H2.
- CLI: `node ./bin/chunk-corpus.mjs [--only=<slug>] [--force] [--target-tokens=500]`. Idempotent via `source_sha256_short` skip.
- Effort: M.

### C — BM25 retrieval

Two new scripts, one new index dir, one librarian-agent edit:

- **Create** `bin/build-index.mjs`: tokenize chunks (lowercase, `/[^a-z0-9]+/`, len 2–30, ~40-word stopword list, vendored Porter-2 stemmer ~150 LOC). Compute BM25 stats (k1=1.2, b=0.75). Write `canon/index/bm25.json` (~200 KB) and `canon/index/postings.json` (~600 KB) and `canon/index/manifest.json`. CLI: `[--incremental]` re-tokenizes only chunks whose sha changed.
- **Create** `bin/query-canon.mjs`: `--q "<terms>" --k 8 [--diversify-by=slug] [--json]`. Default human output: rank, score, slug, parent-heading path, chunk path, 240-char preview. `--diversify-by=slug` caps hits per slug at 2 — load-bearing for contradiction surface (without it, the longest source dominates top-K).
- **Modify** `.claude/agents/canon-librarian.md`: one paragraph — "Prefer `node ./bin/query-canon.mjs --q '<terms>' --k 8 --diversify-by=slug` for initial candidate retrieval; use Grep for exact-phrase / quoted queries." Tools list unchanged (`Bash` already granted). Add the `disagrees_with` force-promotion rule (from Layer D) here.
- **No dense embeddings in v1.** Deferred to a future v2 with local Ollama; explicitly out of scope (cited reason: closed-world rule + zero-dep posture).
- Effort: M.

### E — Retrieval eval harness

- **Create** `tests/retrieval-eval/gold-queries.yaml`: 15 queries, each with `expect_slugs`, `expect_sections`, `must_contradict_pair` (e.g. `[vernon-strategic-monoliths, anthropic-multi-agent-research-system]`), `k`. Spans: stability (×2), DDD vs strategic monoliths (×2 — known contradictor pair), event-driven taxonomy, refactoring, agent orchestration, multi-agent vs single, context engineering, outside view, multitenancy, hexagonal vs DDD layering, Heuer ACH, Heilmeier critique, BM25S vs ColBERT, product discovery.
- **Create** `bin/eval-retrieval.mjs`: invoke `query-canon.mjs --json` for each gold query; score recall@K, section overlap (substring match into `parent_heading`), contradiction-surface rate (% queries where both slugs of any `must_contradict_pair` appear in top-K). Emit `tests/retrieval-eval/results-<YYYY-MM-DD>.md`. Exit nonzero if recall@K drops >10% vs prior baseline.
- **Create** `tests/retrieval-eval/README.md`: scoring rules + how to add a gold query.
- Manual/judged tier (run librarian agent, eyeball outputs) deferred to v2.
- Effort: M (gold-set authoring is the slow part — write expectations *before* tuning the index, not after).

### A1 — Owned-book ingestion (long curator-bound work; runs continuously)

Use existing `bin/ingest-owned-book.mjs` to flip the existing 12 stubs to full text. v1 priority order (highest leverage — these are gaps cited in nearly every session):

1. `evans-ddd`
2. `fowler-refactoring` (2018)
3. `nygard-release-it` (2018)
4. `feathers-legacy-code`

v2: `meszaros-xunit`, `hohpe-eip`, `beck-tdd`, `vernon-strategic-monoliths`, `vernon-iddd`, `fowler-poeaa`. Plus the cognitive-lens additions per A5 (Heuer, Klein, Kahneman *Thinking Fast and Slow*).

After each book lands: re-chunk that slug (`chunk-corpus.mjs --only=<slug>`), incremental-rebuild index (`build-index.mjs --incremental`), re-run eval (`eval-retrieval.mjs`).

Effort: L (curator-bound; not engineering).

### A5 — Lens fills (product / forecasting / cognitive)

Product critic lens has zero canonical material. Forecasting leans on March + Heilmeier alone.

- Product: `cagan-inspired` (owned-book), Christensen JTBD HBR essay (often mirrored, `html` candidate), one Marty Cagan SVPG essay (`html`).
- Forecasting: Tetlock "ten commandments" Edge.org essay (`html`); Kahneman/Lovallo (already in A2).
- Cognitive: Heuer *Psychology of Intelligence Analysis* (CIA-public, `pdf-manual` → owned ingest); Klein *Sources of Power* (owned); Kahneman *Thinking, Fast and Slow* (owned).

v1: Heuer + Tetlock essay + one Cagan piece. Rest v2.

### F — Refresher feed widening

**Modify** `canon/refresh-feeds.yaml`. Add:
- `google-research-blog` (RSS) — keywords `[agent, retrieval, eval, ranking]`
- `microsoft-research-blog`
- `arxiv-cs-ir`
- `arxiv-cs-se`
- (Optional: `usenix-login`, `mlsys-proceedings` as `manual_check` until/unless RSS surfaces)

Per-feed schema add: `publisher_class:`, `diversification_weight: 1.0` (boosts under-represented classes when refresher proposes).

Tighten existing `arxiv-cs-ai` keywords: add `eval, benchmark, bm25, colbert, rerank`; drop `prompting` (firehose).

Effort: S.

### H — README rewrite (final pass after engineering lands)

Once Layers G–F are in, do a second README pass to mention the new scripts (`bin/chunk-corpus.mjs`, `bin/build-index.mjs`, `bin/query-canon.mjs`, `bin/eval-retrieval.mjs`) and replace "currently grep + Read; chunker + BM25 planned" with the now-true description. Keep it short.

Effort: S.

---

## Execution sequence (and why)

1. **G** sources reconciliation
2. **D** metadata schema (every later ingest depends on it)
3. **A2 / A3 / A4** open-access content fills (purely additive, runs in parallel with B)
4. **B** chunker
5. **C** BM25 indexer + query CLI
6. **E** eval harness — pin baseline before any tuning
7. **A1** owned-book ingestion (long curator-bound; chunk + index + eval incrementally as books land)
8. **F** refresh-feed widening (independent; do anytime)
9. **A5** lens fills (mix of fetchable now + owned later)
10. **H** README final pass (last — describes the system as it now is)

Foundations (G, D) come before everything because every subsequent artifact reads those schemas. Content (A2–A4) lands before structure (B) lands before retrieval (C) lands before eval (E) — strict dependency chain. Eval pins a baseline before the long-tail A1/A5 work, so books landing produce a measurable retrieval signal rather than vibes. The final README pass goes last because it must describe what exists, not what is aspired to.

---

## Critical files

### Create
- `bin/sync-sources.mjs`
- `bin/chunk-corpus.mjs`
- `bin/build-index.mjs`
- `bin/query-canon.mjs`
- `bin/eval-retrieval.mjs`
- `tests/retrieval-eval/gold-queries.yaml`
- `tests/retrieval-eval/README.md`
- `canon/index/{bm25,postings,manifest}.json` (built artifacts; gitignored)
- `canon/corpus/<slug>/chunks/{<NNNN>.md, manifest.json}` (built artifacts; gitignored)

### Modify
- `bin/ingest-canon.mjs` — extend `buildCitationYaml()` with Layer D fields
- `canon/sources.ingest.yaml` — add `cluster`, `human_notes`, `fetchable`; add A2/A3/A4/F entries
- `canon/sources.yaml` — header reset to `# GENERATED — do not edit by hand`
- `canon/refresh-feeds.yaml` — add diversity feeds; tighten keywords
- `canon/corpus/*/citation.yaml` — additive Layer D fields
- `.claude/agents/canon-librarian.md` — query-CLI convention + `disagrees_with` force-promotion rule
- `.gitignore` — add `canon/index/` and `canon/corpus/*/chunks/`
- `README.md` — final pass per H (initial honest-current-state rewrite already shipped)

### Do NOT touch
- `CLAUDE.md` (frozen by user)
- Anything under `.claude/agents/` other than `canon-librarian.md`
- The 12-step workflow
- `upgrades/` entries (per memory: lab entries are allowed to be wrong; cleanup must not edit bodies)

---

## Verification

End-to-end check after each layer lands:

- **G:** `node ./bin/sync-sources.mjs --check` exits 0; spot-check that `sources.yaml` is byte-identical to `--emit` output.
- **D:** every `citation.yaml` has the five new fields; ingester emits them on a fresh fetch.
- **A2/A3/A4:** `node ./bin/ingest-canon.mjs` exits 0; new slug dirs exist with `source.txt`, `citation.yaml`, `README.md`; provenance frontmatter present; sha256 stable.
- **B:** `node ./bin/chunk-corpus.mjs --only=<slug>` exits 0; chunks/manifest.json round-trips offsets back to source.txt; rerun is idempotent.
- **C:** `node ./bin/build-index.mjs` exits 0; `node ./bin/query-canon.mjs --q "circuit breaker" --k 8` returns hits with `nygard-release-it` (post-A1) or `google-sre-book` (already ingested) in top-3; `--diversify-by=slug` reduces same-slug repeats.
- **E:** `node ./bin/eval-retrieval.mjs` writes `tests/retrieval-eval/results-<date>.md`; recall@8 ≥ baseline; contradiction-surface rate ≥ 60% on the 15 gold queries.
- **A1 (per book):** stub flipped, chunked, indexed, eval re-run, recall@8 on the relevant gold query goes up.
- **F:** `canon-refresher` produces non-empty review blocks from at least 3 new feeds.
- **A5:** product-lens gold queries (e.g. "what does the product contract commit to when we ship X") return non-empty top-K with non-Anthropic primary slugs.
- **H:** `README.md` renders cleanly on GitHub; no dead links; new reader can run the system from README + `CLAUDE.md` alone.

Final: re-run the existing `tests/regression/ark-mono-connector-routing.md` scenario end-to-end; the librarian's distillation should now cite Evans + Vernon (post-A1) on bounded-context vs strategic-monolith, surface the contradiction explicitly, and the eval baseline should not regress.
