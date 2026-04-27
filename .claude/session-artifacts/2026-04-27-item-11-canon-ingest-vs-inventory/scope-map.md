# Scope map — item 11: reconcile canon ingest vs. inventory

## Existing primitives touched

| primitive | source (where it was named) | relationship | one-line rationale |
|-----------|-----------------------------|--------------|--------------------|
| [`canon/sources.yaml`](../../../canon/sources.yaml) | requirement prose; frame.md | extend | Already correct post-92d9387; role (human-curated inventory, includes owned books) is the permanent design — touch only if README needs to reference it. |
| [`canon/sources.ingest.yaml`](../../../canon/sources.ingest.yaml) | requirement prose; frame.md | extend | Already correct as a strict subset fetch queue; role is permanent and lifecycle-driven — no change to the file itself. |
| [`canon/README.md`](../../../canon/README.md) | requirement prose | extend | Currently omits `sources.ingest.yaml` entirely; adding a lifecycle paragraph extends the doc's coverage without replacing what is there. |
| [`canon/corpus/`](../../../canon/corpus/) | requirement prose; frame.md | extend | The actual retrieval surface; untouched by this item. Listed because the punch-list's wrong rationale implicates it. |
| [`.claude/agents/canon-librarian.md`](../../../.claude/agents/canon-librarian.md) | requirement prose | extend | Behavior is already correct (greps `corpus/`). No change required; listed because the punch-list mis-describes its query target. |
| [`.claude/agents/canon-refresher.md`](../../../.claude/agents/canon-refresher.md) | requirement prose | extend | Already references both YAMLs correctly; no change required. |
| [punch-list item 11 in `plans/2026-04-27-repo-cleanup-punch-list.md`](../../../plans/2026-04-27-repo-cleanup-punch-list.md) | requirement prose | replace | The item's stated rationale is factually wrong (librarian does not query either YAML; the "drift" is a category error). The closing edit must replace the wrong rationale, not just stamp `done`. |

## Deletion cost (for subsume/replace rows)

- **punch-list item 11 wrong rationale**: callers = future readers of the punch-list (including the user and any agent that ingests `plans/`); data migrations = none (markdown text only); config surface = none. Blast radius is documentation-local. Cost of *not* deleting: the false claim "the librarian queries sources.yaml" stays on disk and will re-trigger the same false alarm on the next sweep. Replacement text must (a) state the librarian reads `corpus/` directly, (b) state that `sources.ingest.yaml` is a strict subset of `sources.yaml`, not a parallel list, and (c) mark the item `✅ done <date>` per the punch-list's own item-handling protocol.

## Requires decision (conflicts)

- **`canon/README.md` currently describes only `sources.yaml` + `corpus/`; it does not mention `sources.ingest.yaml`.** This is a latent conflict with candidate action 2 (add a lifecycle paragraph). It is not a hard conflict — extending the README is additive — but the user has not chosen between:
  1. Minimum-touch close: only fix the punch-list, leave README silent on the ingest queue.
  2. Belt-and-braces close: also extend README so the inventory/queue split is documented at the source of truth, not only in a closed punch-list item.
  Generator must pick one and name the tradeoff (legibility-now vs. scope-creep-on-a-cleanup-item).

## Preserved primitives with stated reason (non-default)

- **`canon/sources.yaml` and `canon/sources.ingest.yaml` (both files unchanged)**: preserved because the investigation established that the asymmetry between them is permanent and correct (10 owned-books have no fetch URL and belong in inventory only). The user's explicit constraint, surfaced in the requirement prose, is that the split is "permanent and lifecycle-driven." Removing or merging them would destroy a working two-tier index for a non-defect.
- **`canon-librarian.md` and `canon-refresher.md`**: preserved because their current behavior is what the investigation validated as correct. The punch-list's claim that the librarian queries a YAML is the artifact that is wrong, not the agent.

## Primitives the distillations did not name but the query implies

- **The punch-list's own item-handling protocol** (the convention that closed items get `✅ done <date>` appended to their heading). Named in the requirement prose but not in any distillation; the generator should follow it verbatim rather than invent a new closure format.
- **commit `92d9387`** — referenced as the fix that already landed the three missing entries. Worth citing in the close-out note so the audit trail is one click away, but it is a git object, not a repo primitive to map.
- **`bin/ingest-canon.mjs`** — the consumer of `sources.ingest.yaml`. Not named in the candidate actions; relevant only if the README paragraph (action 2) describes the ingest pipeline. Flag if generator chooses action 2.
