# canon/

The curated corpus the `canon-librarian` agent retrieves from, plus the manifest that drives ingestion and refresh.

## Layout

```
canon/
├── README.md            (this file — schema reference)
├── sources.yaml         (SINGLE SOURCE OF TRUTH, schema_version 2)
├── refresh-feeds.yaml   (RSS/Atom feeds for canon-refresher agent)
└── corpus/              (ingested material; source.txt files are gitignored)
    ├── <slug>/
    │   ├── source.txt   (plain text; gitignored)
    │   ├── citation.yaml (generated lockfile, per-entry post-fetch record)
    │   └── README.md    (generated; human-readable provenance)
    └── ...
```

## The two-file design (manifest + lockfile)

Per the package-manifest convention (`package.json` + `package-lock.json`, `Cargo.toml` + `Cargo.lock`):

| File | Role | Edited by | Read by |
|---|---|---|---|
| `canon/sources.yaml` | **Manifest** — declares what should exist | Human curator | `bin/ingest-canon.py`, `canon-librarian` agent |
| `canon/corpus/<slug>/citation.yaml` | **Lockfile** — records what was actually fetched | `bin/ingest-canon.py` (machine) | `canon-librarian` agent for provenance |

**There is no separate fetch-queue file.** The ingester reads `sources.yaml` directly and filters by `lifecycle` and `fetch_mode`. Adding a second manifest is the canonical split-registry failure mode (Kafka/Confluent schema-registry literature).

---

## `canon/sources.yaml` — manifest schema (schema_version 2)

Top-level structure:

```yaml
schema_version: 2

entries:
  - slug: <kebab-case>
    author: <string>
    title: <string>
    year: <YYYY>
    category: <kebab-case>
    kind: <enum>
    topics: [<kebab-case>, ...]
    source_url: <https URL>
    license: <enum>
    lifecycle: <enum>
    volatility: <enum>
    last_verified: <YYYY-MM-DD>
    fetch_mode: <enum>
    notes: |
      <optional free-form prose>
```

### Required fields (every entry MUST have)

| Field | Type | Validation | Purpose |
|---|---|---|---|
| `slug` | string | kebab-case; unique across all entries; matches `corpus/<slug>/` if any | Stable identifier; never changes once entry exists |
| `author` | string | non-empty | Primary author or organisation |
| `title` | string | non-empty | Work title (exact, not paraphrased) |
| `year` | integer | 4 digits | Publication year (most recent edition if multiple) |
| `category` | string | kebab-case | Grouping tag; for display only; does NOT affect `canon-librarian` retrieval |
| `kind` | enum | see below | Type of work |
| `topics` | list of strings | kebab-case; min 1 | Tags `canon-librarian` greps on for retrieval |
| `source_url` | string | https URL | Canonical location of the work |
| `license` | enum | see below | Provenance/compliance signal |
| `lifecycle` | enum | see below | How the entry relates to the corpus |
| `volatility` | enum | see below | Implied review cadence |
| `last_verified` | date | `YYYY-MM-DD` | When the curator last checked this entry |
| `fetch_mode` | enum | see below | How the ingester retrieves (or `none` for live-only) |

### Optional fields

| Field | Type | Purpose |
|---|---|---|
| `notes` | multi-line string | The ONLY free-form field. Provenance, caveats, edition notes. Do not encode structured data here — add a typed field instead. |

### Strict enums

#### `kind` — what type of work

| Value | Use for |
|---|---|
| `book` | Long-form publication / monograph |
| `paper` | Academic / conference / research paper |
| `essay` | Author-published long-form blog post or article |
| `talk` | Conference talk with published transcript |
| `standard` | Spec or RFC (HTTP, MCP, AGENTS.md, etc.) |
| `docs` | Vendor product documentation |

#### `lifecycle` — how the entry relates to the corpus

| Value | Has `corpus/<slug>/` dir? | Refresh policy | When to use |
|---|---|---|---|
| `snapshot-only` | yes | Never re-fetched | Durable content; URL may die but the snapshot suffices |
| `snapshot+refresh` | yes | Re-fetch per `volatility` cadence | Content evolves; both snapshot AND live URL valuable |
| `live-only` | **no** | Always live-fetched at query time | Snapshotting is wrong (too volatile, too large, too noisy) |

**Hard invariant**: `lifecycle: live-only` REQUIRES `fetch_mode: none`. `fetch_mode: none` REQUIRES `lifecycle: live-only`. The ingester rejects any other combination.

#### `volatility` — implied review cadence

| Value | Cadence | Examples |
|---|---|---|
| `durable` | no timer (review only on doubt) | Fowler refactoring, Evans DDD, Kleppmann DDIA, Lamport |
| `slow` | 365 days | SRE book, Anthropic Core Views, established research papers |
| `fast` | 90 days | Anthropic engineering essays, AGENTS.md spec, AI-tooling blog posts |
| `volatile` | 30 days (or use `lifecycle: live-only`) | Model benchmarks, current API behavior, weekly changelogs |

**Derived (computed at read time, not stored)**: `next_review_by = last_verified + cadence(volatility)`. The `canon-librarian` agent flags entries past `next_review_by` when retrieving.

#### `license` — provenance / compliance signal

| Value | Use for |
|---|---|
| `publisher-published-essay` | Publisher's own engineering blog (Anthropic, Stripe, etc.) |
| `publisher-open-access` | Publisher releases content openly (Google SRE book, AWS docs) |
| `author-published-essay` | Author's personal site (Fowler on martinfowler.com) |
| `author-published-open-access` | Author hosts open PDF (Helland CIDR PDF, March on NTNU mirror) |
| `arxiv-open-access` | arXiv preprint |
| `acl-open-access` | ACL Anthology paper |
| `paywalled-no-open-edition` | Curator owns the book; no open edition exists |
| `unclear` | License needs review before ingest (do not auto-fetch) |

#### `fetch_mode` — how the ingester retrieves

| Value | How | Used with |
|---|---|---|
| `html` | Fetch URL, strip HTML, write `source.txt` | Single-page essays |
| `html-multi` | URL is TOC; ingester follows linked chapters (cap 100) | Multi-chapter web books (e.g., SRE book) |
| `arxiv-abs` | arXiv `/abs/` endpoint; metadata + abstract only | arXiv papers (`abstract_only` completeness) |
| `aws-docs` | AWS `toc-contents.json` walker | AWS Well-Architected lenses |
| `pdf-manual` | Curator runs `pdftotext` + `bin/ingest-owned-book.py` | PDFs hosted on author/institutional sites |
| `owned-book` | Curator runs `bin/ingest-owned-book.py <slug> <text-path>` | Books the curator owns (OCR'd or subscription plaintext) |
| `none` | Ingester does not touch | REQUIRED for `lifecycle: live-only` |

---

## `canon/corpus/<slug>/citation.yaml` — lockfile schema

Machine-generated by `bin/ingest-canon.py` on every fetch. **Do not hand-edit** — re-run the ingester instead. The lockfile carries ONLY post-fetch fields. Curator-declared fields (author, title, year, license, etc.) live in `sources.yaml` and are NOT duplicated here.

```yaml
# Generated by bin/ingest-canon.py. Do not hand-edit — run the ingester.
slug: <copied from sources.yaml>
fetched_at: <ISO 8601 datetime, set by ingester | null for stubs>
sha256: <hex string of source.txt body | null for stubs>
body_completeness: <enum>
chapter_offsets: <list of integer pairs; optional, for book chapter navigation>
stale: <boolean; manually set to true when content known to be outdated>
fetch_notes: |
  <free-form; set by ingester to record the fetch context>
```

### `body_completeness` enum

| Value | Meaning |
|---|---|
| `full` | Entire work ingested into `source.txt` |
| `toc_plus_chapters` | TOC page + linked chapters (`html-multi`, `aws-docs` modes) |
| `abstract_only` | Only abstract + metadata (`arxiv-abs` mode) |
| `stub` | Curator-declared entry; body not ingested yet |
| `fetch_blocked` | Canonical URL temporarily unreachable (cert expired, 403, etc.); see `fetch_notes` |

---

## What goes in `corpus/`

Text you are licensed to have on your machine, in a form the librarian can grep:

- **Books you own** — OCR'd from ebooks you purchased, or plain-text versions from O'Reilly / Manning / Pragmatic if your subscription permits.
- **Open-access papers** — ACM / arXiv / author websites.
- **Author-published essays** — Fowler's `martinfowler.com`, Hohpe's `enterpriseintegrationpatterns.com`, Allspaw on Adaptive Capacity Labs, etc.
- **Conference talks with published transcripts** — InfoQ, GOTO, strangeloop-transcripts repos.

## What does NOT go in `corpus/`

- Pirated ebooks.
- Content under active copyright you lack the license to store.
- Blog posts from authors who didn't publish them for long-term reproduction.
- Summaries or paraphrases — the librarian retrieves *actual passages*. Summaries defeat the point.
- **Anything where `lifecycle: live-only`** — these have no corpus dir by design.

---

## Maintenance — how to add, update, retire an entry

### Add a new entry

1. Determine the values: slug, author, title, year, category, kind, topics, source_url, license, lifecycle, volatility, last_verified (= today), fetch_mode.
2. Append a new entry block to `canon/sources.yaml` under `entries:` — follow the order: required fields in the table order, then `notes:` last.
3. Run `python3 ./bin/ingest-canon.py --only=<slug>` to fetch (skipped automatically for `owned-book` / `pdf-manual` / `live-only`).
4. For `owned-book` or `pdf-manual`, run `python3 ./bin/ingest-owned-book.py <slug> <path-to-text>`.
5. For `live-only`, no further action — the `canon-librarian` will WebFetch at query time.

### Update an existing entry

1. Change the fields in `canon/sources.yaml`.
2. If the URL or content changed: run `python3 ./bin/ingest-canon.py --only=<slug> --force` to refresh the corpus body and regenerate the lockfile.
3. Update `last_verified` to today's date.

### Retire an entry

1. Decide whether to delete it or mark it stale:
   - **Stale** (keep the historical record): set `stale: true` in `citation.yaml` AND add `notes:` to `sources.yaml` explaining why.
   - **Delete** (genuinely wrong / never-existed): remove from `sources.yaml`; delete `corpus/<slug>/` via `bin/safe-rm.sh canon/corpus/<slug>`.

### Refresh cadence checks

The `canon-librarian` agent flags entries past `last_verified + cadence(volatility)` when retrieving. A future `bin/check-canon-staleness.sh` script will list all past-cadence entries (deferred).

---

## Adding fields to the schema (the bloat-prevention rule)

The named failure mode of unified registries is enum/field bloat. To add a field or enum value:

1. Write a brief rationale in `upgrades/` explaining what the new field captures that an existing field cannot.
2. Update `canon/sources.yaml` schema header AND this README in the same commit.
3. Update `bin/ingest-canon.py` validation (`ALLOWED_*` sets + `validateSources()`).
4. Backfill the field on every existing entry — no half-measures (per [README.md](README.md) §"Operating principle — ratchet forward").

**Do not add a field "just in case"**. Every additional field is auto-loaded surface for `canon-librarian` and a maintenance burden on every entry.

---

## How the `canon-librarian` agent uses this schema

At retrieval time:

1. **For `lifecycle: snapshot-only` and `snapshot+refresh`** — grep `corpus/<slug>/source.txt`, return passages with citation from `sources.yaml` + `citation.yaml`.
2. **For `lifecycle: snapshot+refresh` past `last_verified + cadence`** — return passages BUT flag staleness AND surface the live `source_url` with "consider WebFetch to verify."
3. **For `lifecycle: live-only`** — return URL + topic match + recommend WebFetch. The librarian is a router, not a content provider, for these entries.
4. **For `body_completeness: stub`** — return citation + "stub entry; body not ingested." Do not invent quotes.
5. **For `body_completeness: fetch_blocked`** — return citation + "canonical source temporarily unreachable; see citation.yaml fetch_notes."

The librarian's full Mandatory behavior lives in [.claude/agents/canon-librarian.md](.claude/agents/canon-librarian.md).
