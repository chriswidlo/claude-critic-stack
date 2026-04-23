# cockburn-hexagonal-architecture

**Status:** FETCH_BLOCKED — canonical source temporarily unreachable.

**Author:** Alistair Cockburn
**Title:** Hexagonal Architecture
**Year:** 2005
**Source:** https://alistair.cockburn.us/hexagonal-architecture/
**License:** author-published-essay

## Why there is no `source.txt`

The automated ingest run on 2026-04-23 failed because the origin server's
HTTPS certificate has expired. Both `curl` and Node's `fetch` refuse to
establish a connection. The essay itself is freely published by the author;
the issue is purely a transport-layer block on the origin.

## How to populate this entry

**Option A — wait for the cert to renew**, then:

```
node ./bin/ingest-canon.mjs --only=cockburn-hexagonal-architecture --force
```

**Option B — manual ingest** from a local plaintext copy (e.g., if you
saved the page earlier or have an offline archive):

```
node ./bin/ingest-owned-book.mjs cockburn-hexagonal-architecture path/to/hexagonal.txt
```

## What the librarian does with this stub

Returns the citation with a note that the full text is not ingested. Does
not substitute a different source's treatment of hexagonal architecture.
Does not fabricate quotes.
