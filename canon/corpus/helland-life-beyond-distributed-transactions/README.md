# helland-life-beyond-distributed-transactions

**Status:** FETCH_BLOCKED — canonical source refuses automated access.

**Author:** Pat Helland
**Title:** Life Beyond Distributed Transactions
**Year:** 2007
**Source:** https://queue.acm.org/detail.cfm?id=3025012
**Alternate source:** https://www.ics.uci.edu/~cs223/papers/cidr07p15.pdf (CIDR 2007, PDF)
**License:** publisher-open-access

## Why there is no `source.txt`

The automated ingest run on 2026-04-23 failed with HTTP 403 Forbidden.
ACM Queue serves the paper to browsers but blocks programmatic user
agents. The paper is open-access; this is a scraping policy issue.

## How to populate this entry

Manual ingest from a plaintext extraction of the PDF or HTML:

```
# After converting the CIDR PDF to text (pdftotext, Preview, etc.):
node ./bin/ingest-owned-book.mjs helland-life-beyond-distributed-transactions path/to/helland.txt
```

## What the librarian does with this stub

Returns the citation with a note that the full text is not ingested. Does
not substitute a different source's treatment of entities, sagas, or
eventual consistency. Does not fabricate quotes.
