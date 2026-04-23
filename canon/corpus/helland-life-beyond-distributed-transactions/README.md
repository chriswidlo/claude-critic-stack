# helland-life-beyond-distributed-transactions

**Status:** STUB (pdf-manual) — canonical source is a PDF, not auto-ingestable.

**Author:** Pat Helland
**Title:** Life Beyond Distributed Transactions: an Apostate's Opinion
**Year:** 2007
**Primary source:** https://ics.uci.edu/~cs223/papers/cidr07p15.pdf (CIDR 2007, open-access, UCI mirror)
**Alternate source:** https://queue.acm.org/detail.cfm?id=3025012 (ACM Queue, updated 2017 version — blocks bots with HTTP 403)
**License:** author-published open access

## Why there is no `source.txt`

The paper is distributed as a PDF. `bin/ingest-canon.mjs` doesn't parse
PDFs — its `pdf-manual` fetch mode is a signal that curator action is
required. Nothing is broken; this is the intended handoff point.

## How to populate this entry

1. Download the PDF:
   ```
   curl -o /tmp/helland.pdf https://ics.uci.edu/~cs223/papers/cidr07p15.pdf
   ```
2. Convert to plaintext:
   ```
   pdftotext -layout /tmp/helland.pdf /tmp/helland.txt
   ```
   (`pdftotext` is in the `poppler` package: `brew install poppler`.)
3. Ingest:
   ```
   node ./bin/ingest-owned-book.mjs helland-life-beyond-distributed-transactions /tmp/helland.txt
   ```
   The helper writes `source.txt`, hashes it, and flips `citation.yaml`
   `body_completeness: stub` → `full`.

## What the librarian does until this is populated

Returns the citation with a note that the full text is not ingested.
Points at the PDF URL so a user can read the primary source directly.
Does not substitute a different author's treatment of entities, sagas,
or eventual consistency.
