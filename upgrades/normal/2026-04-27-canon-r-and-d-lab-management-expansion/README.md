# Expand canon with R&D-lab-management sources — deferred batch from the thesis research

| Field | Value |
|---|---|
| 📌 **title** | Expand canon with R&D-lab-management sources — deferred batch from the thesis research |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-27 |
| ⚡ **catalyst** | Researching how real R&D labs operate (for the [thesis upgrade](../../profound/2026-04-27-r-and-d-lab-thesis/README.md)) surfaced ~45 cited sources, none of which existed in the curated corpus. Three highest-leverage sources were ingested immediately ([heilmeier-catechism](../../../canon/corpus/heilmeier-catechism/README.md), [anthropic-core-views-on-ai-safety](../../../canon/corpus/anthropic-core-views-on-ai-safety/README.md), [march-exploration-exploitation-1991](../../../canon/corpus/march-exploration-exploitation-1991/README.md)). The rest deserve consideration but not immediate ingestion — this entry is the punch-list. |
| 💡 **essence** | The corpus today is software-architecture + AI-agents. R&D-lab management is a *new category* the corpus has zero coverage of. Expanding it carries a real risk (drifting the corpus off-axis); deferring it carries a real cost (every future "should this primitive ship" question runs through `outside-view` and `frame-challenger` against a corpus that has nothing on the topic). The entry tracks what to add, in what order, and the cost of each. |
| 🚀 **upgrade** | A staged ingest plan: ~7 HTML-fetchable sources land first (each XS via the existing manifest + ingest script); ~3 PDFs/papers land second (pdf-manual stubs, then `bin/ingest-owned-book.mjs` after `pdftotext`); ~6 books land third (operator-owned, `bin/ingest-owned-book.mjs` only if the operator owns them). Each addition extends the new `research_and_innovation:` category in [`canon/sources.yaml`](../../../canon/sources.yaml). |
| 🏷️ **tags** | canon, library, ingest, r-and-d-management, curation |
| 🔗 **relates_to** | 2026-04-27-r-and-d-lab-thesis, 2026-04-26-canon-coverage-audit-and-priority-additions |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-27 | — | — | — | — | — | — | — |

## Table of contents

- [The three already-ingested sources (for context)](#the-three-already-ingested-sources-for-context)
- [Stage 1 — HTML-fetchable, ingest-on-decision](#stage-1--html-fetchable-ingest-on-decision)
- [Stage 2 — PDFs / papers (pdf-manual stubs)](#stage-2--pdfs--papers-pdf-manual-stubs)
- [Stage 3 — Books (operator-owned, OCR path)](#stage-3--books-operator-owned-ocr-path)
- [Why staged, not all-at-once](#why-staged-not-all-at-once)
- [The corpus-axis-drift risk](#the-corpus-axis-drift-risk)
- [How to ingest each stage](#how-to-ingest-each-stage)
- [Open questions](#open-questions)

## The three already-ingested sources (for context)

These landed on 2026-04-27 alongside the [thesis upgrade entry](../../profound/2026-04-27-r-and-d-lab-thesis/README.md). They are the floor of useful R&D-lab-management coverage:

| Slug | Author / title | Why this one first |
|---|---|---|
| [heilmeier-catechism](../../../canon/corpus/heilmeier-catechism/README.md) | DARPA — The Heilmeier Catechism (1975) | Eight scale-invariant questions every R&D proposal must answer. Useful to `frame-challenger`, `critic-product`, and the upgrades-lab gates. Highest immediate leverage. |
| [anthropic-core-views-on-ai-safety](../../../canon/corpus/anthropic-core-views-on-ai-safety/README.md) | Anthropic — Core Views on AI Safety (2023) | Cleanest contemporary example of a published research thesis. Canonical reference for THESIS.md drafting. |
| [march-exploration-exploitation-1991](../../../canon/corpus/march-exploration-exploitation-1991/README.md) | James G. March — *Exploration and Exploitation in Organizational Learning* (1991) | Foundational paper for *why* lab structures exist at all. Stub (PDF) until `pdftotext` ingest. |

## Stage 1 — HTML-fetchable, ingest-on-decision

These can each be ingested with one manifest entry + `node ./bin/ingest-canon.mjs --only=<slug>`. Effort per: XS (~5 min including manifest edit). All confirmed present and reachable as of 2026-04-27.

| Proposed slug | Author / title (year) | URL | Why it would help |
|---|---|---|---|
| `reinhardt-why-darpa-works` | Benjamin Reinhardt — Why does DARPA work? (2020) | https://blog.benjaminreinhardt.com/wddw | Most-cited operating analysis of DARPA's program-manager model. Specifies the non-renewable-term + zero-in-house-research + risk-at-program-level structure load-bearing for understanding DARPA. Pairs with the Heilmeier Catechism (already in corpus). |
| `x-monkey-first-language-of-innovation` | Astro Teller / X — The Monkey, the Tiger Beetle and the Language of Innovation | https://x.company/blog/posts/the-monkey-the-tiger-beetle-and-the-language-of-innovation/ | The "monkey first" rule + pre-committed kill metrics. Useful as a verbatim alternative to the lab's lifecycle gate language. |
| `openai-charter` | OpenAI — Charter (2018) | https://openai.com/charter/ | Four-principle commitment with an explicit falsifier (the "if a value-aligned project gets there first, stop competing and assist" clause). Useful as a reference example of *commitment-vs-aspiration* in a research-lab document. |
| `deepmind-about` | DeepMind — About / Mission | https://deepmind.google/about/ | Mission as forever-true statement: "solve intelligence, and then use that to solve everything else." Reference for how a lab states a multi-decade mission. |
| `usv-investment-thesis` | Union Square Ventures — USV Thesis (1.0/2.0/3.0) | https://www.usv.com/idea/usv-investment-thesis/ | Three published, dated thesis revisions over six years. Reference example of thesis-as-revisable-commitment vs thesis-as-vague-aspiration. May need `html-multi` to capture all three. |
| `critchlow-independent-research-lab` | Tom Critchlow — Reimagining the Independent Research Lab (2021) | https://tomcritchlow.com/2021/02/24/research-studios/ | The closest existing model for a *micro-team* R&D effort. Three-phase model (audience-research fit → small artifacts → team assemblage). Specifically relevant to the upgrades/ lab's scale. |
| `mckinsey-three-horizons` | McKinsey — Enduring Ideas: The three horizons of growth | https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/enduring-ideas-the-three-horizons-of-growth | Canonical short-form treatment of the Three Horizons framework. Useful for `outside-view` when forecasting whether a primitive should ship now (H1) or wait (H2/H3). |

**Total stage-1 effort:** ~35 minutes for all seven, including manifest edits, ingest runs, and verification queries to the librarian. Each is a clean win.

**Defer-decision per source:** add only when an upgrade entry's research would have benefited from it. Don't bulk-add; the corpus stays honest if every ingestion has a named caller.

## Stage 2 — PDFs / papers (`pdf-manual` stubs)

Each needs a stub folder + `pdftotext` conversion + `bin/ingest-owned-book.mjs`. Effort per: S (~30 min including download, conversion, ingest, verification).

| Proposed slug | Author / title (year) | Source | Why it would help |
|---|---|---|---|
| `yaqub-serendipity-taxonomy` | Yaqub — *Serendipity: Towards a taxonomy and a theory* (2018) | *Research Policy* (paywalled at ScienceDirect; check for author preprint) | Strongest empirical contrarian case against R&D-portfolio formalization. Useful when frame-challenger needs to argue *against* a thesis-tightening proposal. License risk: paywalled. Confirm preprint availability before ingesting. |
| `watzinger-schnitzer-bell-breakup` | Watzinger & Schnitzer — The Breakup of the Bell System and its Impact on US Innovation | https://www.monika-schnitzer.com/uploads/4/9/4/1/49415675/watzinger_schnitzer_breakup_of_bell.pdf | Empirical natural-experiment evidence on how funding-shape change broke the most productive R&D lab in history. Author-published PDF. |
| `bush-endless-frontier-1945` | Vannevar Bush — *Science: The Endless Frontier* (1945) | https://www.nsf.gov/about/history/EndlessFrontier_w.pdf (NSF mirror, public domain — government work) | The founding document of the post-WWII US research-funding paradigm. Canonical reference for the "directed basic research" tradition Bell Labs descended from. |

**Total stage-2 effort:** ~90 minutes for all three, mostly waiting on `pdftotext` and verifying.

## Stage 3 — Books (operator-owned, OCR path)

These require operator action: own the book, OCR it (or use a publisher's plain-text version if licensed), then `bin/ingest-owned-book.mjs`. Effort per: M (~3h including acquisition, OCR, cleanup). **Add only if the operator already owns or chooses to acquire.**

| Proposed slug | Author / title (year) | Why it would help | Acquisition path |
|---|---|---|---|
| `gertner-idea-factory` | Jon Gertner — *The Idea Factory: Bell Labs and the Great Age of American Innovation* (2012) | The most-cited contemporary history of Bell Labs. Source for Mervin Kelly's four operating pillars. Heavy load-bearing across the thesis upgrade entry. | Trade book; ebook from any major retailer. |
| `cooper-stage-gate` | Robert G. Cooper — *Winning at New Products: Creating Value Through Innovation* (5th ed., 2017) | Canonical Stage-Gate reference. The "kill-is-default, continue-requires-justification" framing the upgrades-lab lifecycle gates implicitly use. | Trade book. |
| `baghai-coley-white-alchemy-of-growth` | Baghai/Coley/White — *The Alchemy of Growth* (1999) | Original Three Horizons framework. McKinsey article (stage 1) is a précis; the book has the full structure. | Out of print; Internet Archive controlled-digital-lending may apply if the operator's lending account permits. |
| `stokes-pasteurs-quadrant` | Donald Stokes — *Pasteur's Quadrant: Basic Science and Technological Innovation* (1997) | The two-axis model (use-inspired vs curiosity-driven; pure vs applied) that taxonomizes what *kind* of research a lab is doing. Useful for classifying upgrade entries beyond the four tiers. | Trade book; widely available. |
| `christensen-innovators-dilemma` | Clayton Christensen — *The Innovator's Dilemma* (1997) | The disruption framework — relevant to the question of whether the upgrades lab should be willing to ship things that look worse-on-current-axes than the existing stack. | Trade book. |
| `hiltzik-dealers-of-lightning` | Michael A. Hiltzik — *Dealers of Lightning: Xerox PARC and the Dawn of the Computer Age* (1999) | The most-cited contemporary history of PARC. Source for the Taylor "fund people, not projects" structural choice. | Trade book. |

**Total stage-3 effort:** highly variable (~half a day per book once acquired). Don't ingest speculatively — only when an upgrade entry has been waiting on the citation.

## Why staged, not all-at-once

Three reasons:

1. **Cost of ingestion is real.** Each entry adds bytes the librarian greps over, and the librarian's retrieval quality degrades when the corpus contains many topically-irrelevant entries for a given query. Ingest-on-demand keeps signal-to-noise high.

2. **The corpus is curator-territory, not auto-fill.** Per [`canon/README.md`](../../../canon/README.md): "The corpus is not an archive. It is a working library. It has to be curated by someone who has read the material." Bulk-adding sources nobody has read is a rule the corpus actively forbids.

3. **Caller-named ingestion is the discipline.** Each ingest should have a named upgrade-entry or workflow-step it serves. "Just in case" ingestion is how libraries become unreadable.

The right mental model: this entry is a *waiting list*. When a future upgrade-entry's research would have benefited from one of these sources, that's the signal to promote it from this list to a real `sources.ingest.yaml` entry. The list is reviewed when this entry is reviewed, not on a schedule.

## The corpus-axis-drift risk

The canon today is software-architecture + AI-agents. The thesis upgrade entry on 2026-04-27 introduced a *new category* (`research_and_innovation:`) with three entries. If that category grows to ~15 entries, two things happen:

1. **The corpus axis broadens.** It is no longer "software-architecture + AI-agents" — it is "software-architecture + AI-agents + R&D-lab-management." This is a real shift in what the librarian retrieves.
2. **Cross-category retrieval gets noisier.** A `canon-librarian` query on "exploration vs exploitation" now legitimately returns both March 1991 (R&D management) and any DDD passages on bounded-context exploration (different "exploration"). The librarian's prose-retrieval doesn't disambiguate by category by default.

**The hedge:** every R&D-lab-management entry should carry a `r-and-d-management` tag in its `topics:` list. The librarian uses topic tags as a filter; entries that name the tag are discoverable, entries that don't are not.

If the category exceeds ~10 entries without ever having been retrieved meaningfully, that's the early warning signal — the corpus is drifting off-axis and stage-3 ingests should pause.

## How to ingest each stage

### Stage 1 (HTML-fetchable)

For each source:

1. Add a row to the `research_and_innovation:` block in [`canon/sources.yaml`](../../../canon/sources.yaml) with author, title, year, kind, topics (incl. `r-and-d-management`), notes.
2. Add a corresponding entry to [`canon/sources.ingest.yaml`](../../../canon/sources.ingest.yaml) with slug, manifest_ref, url, fetch (`html` or `html-multi`), license, topics.
3. Run: `node ./bin/ingest-canon.mjs --only=<slug>`
4. Verify: spot-check the first 30 lines of `canon/corpus/<slug>/source.txt`; sanity-grep for a key phrase.
5. Optionally: run a `canon-librarian` test query to confirm retrieval works.

### Stage 2 (PDFs)

1. Add manifest entries as above, but with `fetch: pdf-manual`.
2. Run `node ./bin/ingest-canon.mjs --only=<slug>` — it will fail gracefully and leave a stub-shaped citation.yaml + README.md (or create those manually following the [helland pattern](../../../canon/corpus/helland-life-beyond-distributed-transactions/README.md)).
3. Download the PDF, run `pdftotext -layout`, then `node ./bin/ingest-owned-book.mjs <slug> /tmp/<slug>.txt`.

### Stage 3 (operator-owned books)

Same as stage 2 but the source is the operator's purchased ebook. Use the publisher's plain-text export when available; OCR otherwise. Same `ingest-owned-book.mjs` step.

## Open questions

1. **Cap on the new category.** Should `research_and_innovation:` be soft-capped at ~10 entries to enforce the corpus-axis-drift hedge? Default proposal: yes, with a one-line note in [`canon/sources.yaml`](../../../canon/sources.yaml).

2. **`canon-refresher` involvement.** The `canon-refresher` agent is RSS-based and won't pull these. Should the refresher gain a "manual-add suggestions" output mode where the operator drops URLs into a watch-list and the refresher proposes ingest-manifest rows? Out of scope for this entry; flag for a future entry.

3. **Tagging rigor.** Is `r-and-d-management` the right cross-cutting tag? Alternatives: `lab-management`, `innovation-portfolio`, `research-strategy`. Pick one at acceptance and apply consistently.

4. **Stage-1 batch order.** The seven stage-1 sources are listed in *load-bearing* order (Reinhardt, X-monkey-first, OpenAI Charter, DeepMind About, USV thesis, Critchlow, McKinsey). The ingest order doesn't have to match. If only three slots are available in a future session, the top three are the right call.

5. **Whether stage-3 books should be tracked here at all.** They depend on operator-owned licenses and can't be acquired by an agent. Tracking them in this entry is a *reading list*, which is a different artifact-type than a *manifest*. May want to split: a `canon-reading-list.md` separate from `sources.yaml`. Defer.
