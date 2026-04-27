# Candidate recommendation — item 11

## Position

**Close item 11 as overtaken-by-events.** Make exactly two edits, both in [`plans/2026-04-27-repo-cleanup-punch-list.md`](../../../plans/2026-04-27-repo-cleanup-punch-list.md):

1. Append `✅ done 2026-04-27` to the heading "## 11. Reconcile canon ingest vs. inventory" (per the punch-list's own protocol on L262).
2. **Replace** (not just annotate) the "Why it matters" paragraph (L222–223) so it no longer asserts the librarian queries either YAML. Replacement text must (a) name the false claim explicitly so future readers do not re-derive it from the surrounding prose, and (b) record the actual mechanism in one sentence: *the librarian greps `canon/corpus/`; both YAMLs are catalog-and-fetch-queue, not retrieval indexes.*

**Do not** add a lifecycle paragraph to [`canon/README.md`](../../../canon/README.md) in this session. Defer to a `lift condition`: a *second* on-disk misread of canon's data flow appears elsewhere in the repo.

## Frame-level objection addressed

The frame-challenger's principal objection was: *if a second on-disk misread of canon's data flow already exists in the repo, "close as overtaken-by-events" is wrong because the speculative→attested threshold has been crossed.* I checked: I grepped for `sources.yaml`, `sources.ingest.yaml`, and "librarian queries/reads/retrieves" across all `*.md` outside `.claude/session-artifacts/`. The only false claim about how the librarian retrieves is the one inside the punch-list at L223. The two YAMLs are referenced elsewhere only correctly (e.g., `canon-refresher.md:23` describes `sources.ingest.yaml` as a queue it proposes additions to — accurate). Lift condition is **not** met. Frame survives.

The challenger's secondary objection — *the placement question (README vs. sources.yaml header vs. ingest-canon.mjs docstring vs. librarian prompt) was pre-decided as README without examining where misreaders actually arrive* — is acknowledged: the only attested misreader arrived via the punch-list, not the README. The fix therefore goes where the misread is, not where its absence is most visible.

## Named tradeoffs

1. **Minimum-touch closeout vs. lifecycle legibility at source.** Choosing minimum-touch means [`canon/README.md`](../../../canon/README.md) continues to omit `sources.ingest.yaml` entirely. Cost: a future contributor who lands on the README first has to derive the queue/inventory split from the file headers themselves. Benefit: no doc gets written against a phantom audience and no shape gets ossified that may be refactored.
2. **Replace-the-rationale vs. preserve-as-historical.** The punch-list elsewhere treats prose as immutable historical record (see item 3, L75: *"don't rewrite history"*). I am treating the *plans/* punch-list as live working document, not historical artifact, because the protocol on L262 prescribes *editing the heading* to mark done — i.e., the document was designed to be edited in place. Risk: this distinction is mine, not the user's; the user may want even live planning docs preserved as posted.
3. **Closing without folding the YAMLs vs. fold into one file with `fetchable: true`.** The frame-challenger raised the latter. I am not taking it because: (a) the ingest script's idempotency relies on a structurally minimal queue file; (b) the human inventory has prose `notes:` fields the script doesn't need; (c) a fold is a refactor of the canon module, not a closeout of item 11. Right move, wrong session.

## Named assumptions (any one wrong → recommendation flips)

1. **The punch-list is editable in place** (not historical). If the user instead wants `plans/*.md` treated as session-artifact-grade history, the right move is *append* a correction note rather than replace L222–223 — and item 11's protocol-mandated heading edit becomes problematic too.
2. **The YAML split is permanent.** If `sources.ingest.yaml` is in fact slated for absorption into `sources.yaml` + `fetchable: true` (or for replacement by a generated artifact), then any near-term documentation of "the lifecycle" would lie within months. This assumption is *strengthened* by the absence of any in-flight refactor in the repo, but I have not confirmed with the user.
3. **No second misreader is latent.** I grepped the live tree (excluding session-artifacts). If a misread lives only in human memory ("I keep forgetting which YAML the librarian uses") and the user already has it, the lift condition is met by attestation I cannot see.
4. **The librarian agent prompt itself does not need a one-line clarification.** The frame-challenger argued correct ≠ legible; I am betting the agent prompt's existing language (`canon/corpus/` named twice on lines 9 and 32) is adequate. If the user reads it and disagrees, the cheapest follow-on is a single sentence in [`.claude/agents/canon-librarian.md`](../../../.claude/agents/canon-librarian.md) saying "the YAMLs are catalogs, not retrieval indexes" — not the README change.

## Named ways this could be wrong

- **Wrong scope of closure.** The user may have meant "look at item 11 *and* the canon-docs hygiene around it" — not just "execute the done-when clause." If so, the right move includes the README paragraph after all, and outside-view's "below base rate" verdict is overruled by the user's intent (which is not visible to outside-view).
- **Wrong locus of fix.** The misread is a category error about how retrieval works. The right fix may belong in [`canon/README.md`](../../../canon/README.md) line 3 ("the curated corpus the canon-librarian agent retrieves from") — clarifying *retrieves from corpus/, not from sources.yaml* — rather than in the punch-list. That single-line edit at the top of canon/README.md is cheaper and more discoverable than the punch-list edit.
- **Underweighting the cost of the false claim.** The punch-list line is dated 2026-04-27 (yesterday) and may be re-read this week by the same author who wrote it, with no second-misreader needed. The "speculative" framing from outside-view may be wrong on timing.

## Cheapest experiment to reduce the biggest uncertainty

Ask the user one question before committing edits: *"Do you want item 11 closed as overtaken-by-events with a punch-list rationale fix, or do you want me to also clarify retrieval mechanics in canon/README.md?"* Cost: one round-trip. Resolves assumption #1 and the first "could be wrong" simultaneously. If the user says "just close it," ship the two-line edit. If the user says "clarify the README too," the work is monotonic — the punch-list edit is unchanged, and a single sentence is added to canon/README.md.
