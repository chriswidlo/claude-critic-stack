# Architecture critique — item 7 (residual AGENTS.md references)

## 1. Weakest structural link

**The plan invents a new module boundary ("live contracts" vs. "dated authorial records") that does not exist anywhere in the repo's documented architecture, and uses that invented boundary to license writes into 🔖-committed upgrade-entry bodies.**

[`.claude/session-artifacts/README.md`](../../session-artifacts/README.md) documents an explicit immutability discipline for one persistent surface (session artifacts: *"Noise-removal pruning is forbidden — it destroys the very longitudinal signal the tracking exists to capture"*). The same README enumerates the lab (`upgrades/`) as a peer persistent surface alongside `session-artifacts/`, `canon/`, and `memory/` — but the immutability discipline for the lab is undocumented. The plan reads that documentation gap as license to edit lab entries in place, on a cost-asymmetry argument. That is an aggregate-boundary decision being made inside a 🟡-minor hygiene task. The plan even admits this in its own *Open question* section (*"the answer is not principled — it's a cost-driven cut"*). The next item that touches a 🔖-committed upgrade entry body will cite item 7 as precedent, and the cost-driven cut becomes the de facto convention without ever having been ratified.

## 2. Invariants at risk

The candidate names one assumption. It does not name these:

1. **Lifecycle-marker monotonicity.** The state row at the top of each upgrade entry advertises a position in `🌱 → 🏁`. The implicit invariant is that body content under a given marker is *the body the marker was placed against*. Edit the body without advancing or annotating the marker, and the marker now advertises a state for content that did not exist when the marker was set. The plan's row 4/5/6 edits violate this without acknowledging the marker exists.
2. **LEDGER-to-entry-body coherence.** [`upgrades/LEDGER.md`](../../../../upgrades/LEDGER.md) is the sibling-of-record. The plan never reads it. If LEDGER summarizes any of the four edited cells, an in-place rewrite silently desyncs LEDGER from entry.
3. **Module-decomposition row coupling.** The cell at `constitutional-layer-goals-modules/README.md`:42 is one row of an *aggregate* — a multi-row table that is the upgrade entry's structural deliverable. The plan treats the row as cell-local. The "orchestration" module's `Owns` column reads `CLAUDE.md, AGENTS.md, the workflow, gates`; strip `AGENTS.md` and the orchestration module is `{CLAUDE.md, the workflow, gates}` — and "the workflow" and "gates" are not files but processes. The architectural claim of the row was that orchestration was the *document-anchored* module; deletion converts it into a mostly-process module — a different structural claim.
4. **Allowlist-as-policy invariant.** [`.gitignore`](../../../../.gitignore) is ignore-by-default; every `!`-rule is a deliberate admit. The line `!AGENTS.md` is therefore not an inert no-op (the plan's claim) — it is a *forward-compat hook* that documents *"if this file is ever recreated at root, admit it without a .gitignore edit."* Deleting the line removes a forward-compat affordance.

## 3. Coupling and direction

- **Wrong-direction dependency.** The plan files a follow-up upgrade ("Supersede-don't-edit convention") *as a consequence* of item 7's edits, while item 7 is itself being justified by the absence of that convention. Temporal cycle: the action that would be retroactively wrong under the convention is the action that prompted the convention.
- **Cross-module write from hygiene into lab.** The plan executes one hygiene task that writes into two distinct modules per the constitutional-layer entry's own decomposition. The plan does not justify why a single commit should cross that boundary.
- **Cycle through the catalyst footnote.** Row #7/#8's "footnote pointing forward to the punch-list item 7" introduces a dependency from a 🔖-committed profound-tier upgrade entry to a transient operator planning doc. Plans age out; entry then carries a footnote whose target is a closed punch-list line.

## 4. Ignored architectural alternatives

1. **Tombstone file.** Recreate `AGENTS.md` at root as a one-line tombstone: *"Retired YYYY-MM-DD — see [`plans/2026-04-27-repo-cleanup-punch-list.md`](../../../../plans/2026-04-27-repo-cleanup-punch-list.md) item 7."* Zero edits to upgrade-entry bodies; `.gitignore`:21 is no longer misleading; CLAUDE.md:9 enumeration is no longer broken; catalysts at `:9`/`:38` of `workflow-blind-to-the-lab` need no footnote because the file they name still exists. Cost: one new file. **Respects the lab's implicit immutability invariant; makes the deletion reversible at any time; preserves all dated authorial records verbatim.**
2. **Strikethrough-and-erratum, applied symmetrically across all five upgrade occurrences.** The frame-challenger's preferred answer. Architecturally this is the move that *does not invent a new module boundary* — it applies the documented session-artifact discipline to its peer persistent surface (the lab).

## 5. Frame-level objection

The candidate's frame is *"audit four jobs the string is doing, kill three, preserve one."* That frame is doing the work that **a missing primitive** should be doing. The repo has documented immutability for `session-artifacts/` and undocumented immutability (or mutability) for `upgrades/`. **Item 7 is not a hygiene question — it is the first instance that forces the lab's mutability discipline to be named.** Resolving item 7 by inventing a per-occurrence ad-hoc rule and filing the principled question as a follow-up gets the precedence backwards: the convention should be ratified first, and item 7's edits should be the convention's first application, not its retroactive precedent.

## 6. Verdict

`reject`.

**Smallest change to flip to `approve`:** do not edit any upgrade-entry body in item 7. Either (a) replan to file the "supersede-don't-edit" convention upgrade first, ratify it, and re-scope item 7 as its first application; or (b) adopt the **tombstone alternative** — confine item 7's writes to one new root file plus the punch-list `✅` line — zero edits to existing bodies, zero precedent set.
