# evans-ddd

**Status:** STUB — owned-text not yet ingested.

**Author:** Eric Evans
**Title:** Domain-Driven Design: Tackling Complexity in the Heart of Software
**Year:** 2003
**ISBN:** 978-0321125217
**License:** paywalled, no open edition

This work is referenced in `canon/sources.yaml` but its full text is not in
the corpus because it is under active copyright with no open-access edition.
Do not ingest pirated copies.

## How to populate this entry

If you own the book and have an OCR'd or publisher-provided plaintext of it:

```
node ./bin/ingest-owned-book.mjs evans-ddd path/to/owned-text.txt
```

The helper copies the text to `source.txt`, hashes it, and flips
`citation.yaml` `body_completeness: stub` → `full`.

## What the librarian does with this stub

When this slug is the best match for a query, the librarian returns:

> Corpus stub: Eric Evans, *Domain-Driven Design* (2003) is in the manifest
> but the full text is not ingested. The librarian cannot quote from it.

Preferable to silently returning a weaker passage from a different work or
fabricating a quote.
