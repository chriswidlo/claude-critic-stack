# canon/

The curated corpus the `canon-librarian` agent retrieves from.

## Layout

```
canon/
├── README.md       (this file)
├── sources.yaml    (manifest — what should be here and why)
└── corpus/         (actual ingested material; gitignored)
    ├── kleppmann-ddia/
    ├── evans-ddd/
    ├── fowler-refactoring/
    └── ...
```

## What goes in `corpus/`

Text you are licensed to have on your machine, in a form the librarian can grep. In practice:

- **Books you own** — OCR'd from ebooks you purchased, or plain-text versions from O'Reilly / Manning / Pragmatic if your subscription permits.
- **Open-access papers** — ACM / arXiv / author websites.
- **Author-published essays** — Fowler's `martinfowler.com`, Hohpe's `enterpriseintegrationpatterns.com`, Allspaw on Adaptive Capacity Labs, etc.
- **Conference talks with published transcripts** — InfoQ, GOTO, strangeloop-transcripts repos.

One folder per work, preferably with `source.txt` (plain text), `citation.yaml` (author/title/year/chapter-offsets), and a `README.md` explaining what you ingested and where it came from.

## What does *not* go in `corpus/`

- Pirated ebooks.
- Content under active copyright that you lack the license to store.
- Blog posts from authors who didn't publish them for long-term reproduction (check their site's terms).
- Summaries or paraphrases — the librarian is meant to retrieve *actual passages*. Summaries defeat the point.

## Ingestion workflow

1. Add an entry to `sources.yaml` for what you're adding.
2. Create `corpus/<slug>/` with the source text and a `citation.yaml`.
3. Verify the librarian can find it: invoke the `canon-librarian` agent with a test query on a known topic from that source, confirm the passage is returned with correct citation.

## Keeping the corpus honest

Every ~6 months, walk the corpus and ask: *what is now wrong here?* Several entries were correct in their publication year and are now stale (e.g., mid-2010s microservices enthusiasm). Do not delete these — mark them `stale: true` in `citation.yaml`. The librarian is expected to flag stale passages in output.

The corpus is not an archive. It is a working library. It has to be curated by someone who has read the material.
