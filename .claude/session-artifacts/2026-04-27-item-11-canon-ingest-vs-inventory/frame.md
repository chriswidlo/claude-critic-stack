# Frame

## Revision 1

### User's implicit frame
The punch-list frames item 11 as **data-drift between two YAMLs** with a remedy of "reconcile" (sync the files) or "document the split." Both options assume the files are the load-bearing surface.

### Reframe
The actual load-bearing surface for retrieval is the **directory tree** at [`canon/corpus/`](../../../canon/corpus/). Both YAMLs are *secondary index files* with different roles:
- [`sources.yaml`](../../../canon/sources.yaml) = **human-curated inventory** (what *should* be there, with topics/notes/rationale). Includes 10 owned-books that have no ingestable URL.
- [`sources.ingest.yaml`](../../../canon/sources.ingest.yaml) = **machine-readable fetch queue** for `bin/ingest-canon.mjs`. Subset of `sources.yaml`: only entries whose corpus body can be auto-fetched from a URL.

So the right framing is not "reconcile two parallel lists" but **"a single inventory with a fetchable subset."** The question is whether that asymmetry — which is permanent and correct — is *legible* to a future reader.

### What the user is implicitly optimizing for
**Hygiene of catalog files.** Treating any divergence as a defect to be reconciled.

### One alternative optimization
**Cost of misdiagnosis.** Item 11 was opened on a wrong reading of how retrieval works (the punch-list claims "the librarian queries `sources.yaml`" — it doesn't; it greps the corpus tree). Optimizing for this means the cheapest fix is *not* documentation prose — it is removing the false rationale from the punch-list itself, so the next reader doesn't re-raise the same false alarm.

### Honest friction
The user's punch-list line "If the librarian queries `sources.yaml` (the inventory) rather than `sources.ingest.yaml` (the queue), it can't find the source" is wrong on both halves: the librarian queries neither, and `sources.ingest.yaml` is a strict subset of `sources.yaml`, not a separate "queue" with different membership. The item is a category error, not a data drift. That should be named, not papered over.
