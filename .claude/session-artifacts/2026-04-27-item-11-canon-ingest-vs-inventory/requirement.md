## Primary label
investigation

## Default frame (from label)
Frame downstream steps as: "what would we do differently if we knew the answer?" The original symptom in item 11 is overtaken by events — fix-(b) shipped in commit 92d9387, and the librarian greps [`canon/corpus/`](../../../canon/corpus/) directly rather than reading either YAML. The remaining live question is small and binary: close item 11 as no-op, or also document the ingest-vs-inventory lifecycle in [`canon/README.md`](../../../canon/README.md) to prevent future readers from re-raising the same false alarm.

## Known frame bias
Investigation framing tends to produce research theater — drafting README prose to "close the ticket" when the ticket's premise is already false. Watch for: writing a lifecycle section nobody is currently confused about, gold-plating documentation to justify having opened the session, or expanding scope into a general "canon docs refresh" because the README doesn't mention `sources.ingest.yaml` at all.

## Secondary label (if any)
extend — if the decision tilts toward documenting the lifecycle, the work is a monotonic addition to an existing primitive ([`canon/README.md`](../../../canon/README.md)), not a new capability.

## Alternative classification
extend — becomes primary the moment the orchestrator decides "yes, document the lifecycle in canon/README.md." The investigation collapses to a one-bit decision (close vs. document); whichever bit wins selects the label of the actual follow-on work.

## User's framing words
- "Reconcile canon ingest vs. inventory" (punch-list title) — presumes the two YAMLs are out of sync and that reconciliation is the action. Reality: they are now in sync, and neither is what the librarian reads. The framing word "reconcile" is the user's assumption, not a finding.
- "the librarian may not find them" (punch-list rationale) — presumes a retrieval mechanism (YAML lookup) the librarian does not use.
- Done-when clause "both files in sync OR canon/README.md documents the lifecycle" — the user has already enumerated the two exits. The investigation reduces to picking one.

## Gaps
- Is there a near-term reader (a new contributor, a future orchestrator run) who would actually be misled by canon/README.md's silence on `sources.ingest.yaml`? If no concrete audience is named, "close as overtaken-by-events" wins by default.
- Is `sources.ingest.yaml` itself a stable primitive, or a transient queue that may be folded into `sources.yaml` later? If transient, documenting its lifecycle now ossifies a shape meant to be temporary.
- Does any other artifact in the repo (agent prompt, upgrade entry, workflow doc) currently reference `sources.ingest.yaml` in a way that presumes a different lifecycle than what canon/README.md would say?
