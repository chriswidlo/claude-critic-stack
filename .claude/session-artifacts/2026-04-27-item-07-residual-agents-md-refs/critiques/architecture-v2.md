# Architecture critique v2 — item 7 (tombstone alternative)

## 1. Weakest structural link

**The tombstone consumes a forward-compat hook in `.gitignore` that loop-1 (Section 2, invariant #4) explicitly named as load-bearing.**

Loop-1 named [`.gitignore`](../../../../.gitignore):21's `!AGENTS.md` line as a forward-compat affordance. v2 claims that line is "now doing real work — the tombstone needs to be tracked." But the line cannot serve both roles. Either it admits the tombstone (hook *consumed* — a future author who wants to land an actual `AGENTS.md` per upstream convention finds the slot occupied), or it remains a hook for future content (tombstone is squatting on the slot). The plan picks the first horn without acknowledging the second.

## 2. Invariants at risk

1. **Constitutional doc-set cardinality.** The repo's root-level constitutional doc set is an aggregate with documented cardinality. AGENTS.md as a tombstone makes the cardinality 3, advertising sibling-status to a file whose body declares it has no contract. The path-discipline rule's enumeration becomes *technically correct and semantically misleading* — the worst of both worlds.
2. **Tombstone-as-permanent vs. tombstone-as-transitional.** The plan's body installs an *implicit lifecycle state* (`tombstoned → replaced` or `tombstoned → permanent`) on a file with no lifecycle row, no state marker. Every other persistent surface in this repo with a state-machine has *explicit* state markers. The tombstone is the first state-bearing artifact at the constitutional layer with no state marker.
3. **Reversibility-of-deletion symmetry.** Recreating as a tombstone makes the *deletion* reversible (file exists again) but makes the *original-content recovery* asymmetric — a future author has to know to look at git history pre-tombstone.

## 3. Coupling and direction

- **Volatile-pointing-at-stable inversion.** The tombstone body links *out* to `plans/2026-04-27-repo-cleanup-punch-list.md` item 7 — a transient operator planning doc — from a root-level file whose whole purpose is to be a stable referent. Loop-1 flagged this anti-pattern; v2 *moves* the cycle, it does not eliminate it.
- **Soft-contract installation across layers.** *"If a future iteration ... replace the tombstone with the new content"* is a directive issued by a constitutional-layer file to an unspecified future authoring step. That is a coupling from the architecture layer to a not-yet-existing process, written in prose with no enforcement surface.

## 4. Ignored architectural alternatives

1. **Tombstone with explicit lifecycle row + creation date.** Adopt a `🪦 retired YYYY-MM-DD` marker at the top of the tombstone, so the file's state-bearing nature is legible as state.
2. **Symbolic absence via `.gitignore`-only fix.** Drop the `!AGENTS.md` allowlist line; let the file's non-existence be the canonical state. Refactor *only* `CLAUDE.md`:9 (one enumeration edit). The *(if present)* guard already handles `prompts/ultraplan-next-level.md`:39. Upgrade-entry references to a non-existent file remain a documentation problem — but they were always a documentation problem. Cost: one CLAUDE.md edit, one .gitignore edit. Benefit: no namespace squatting, no implicit soft contract, no invented sibling at the constitutional layer.
3. **Codify the upstream `AGENTS.md` convention now.** The convention is real and growing (Linux-Foundation-stewarded; significant adoption). The smallest principled move is to *adopt* it — author a one-paragraph `AGENTS.md` that delegates to CLAUDE.md (e.g., *"This stack's agent contract is in CLAUDE.md; AGENTS.md exists per the upstream convention as a discovery surface."*). That is not a tombstone — it is content. It resolves the same eight references, occupies the namespace *with a stated purpose*, and removes the soft-contract problem because the file's contract is its own body.

## 5. Frame-level objection

Loop-1's frame objection: item 7 was forcing the lab's mutability discipline to be named. v2 sidesteps that frame entirely — and the sidestep is itself a new frame-level problem.

**v2's frame is *"prefer additive moves; the cheapest fix that breaks no existing rule wins."*** That frame treats namespace occupation as free. **Creating a sibling at the constitutional layer is a more invasive aggregate change than rewriting three sentences inside the lab.** The plan has the asymmetry inverted.

Second frame objection: the upstream AGENTS.md convention's existence (real, adopted) means this stack's `AGENTS.md` is no longer a free-naming choice — it is a name that *carries upstream semantics*. A tombstone at this name is not a neutral marker; it is a statement that this repo *had* an AGENTS.md and *retired* it. A reader who knows the upstream convention reads that as *"this repo evaluated and rejected the agents.md convention,"* which is not what the plan means.

## 6. Verdict

`rework`.

**Smallest change to flip to `approve`:** adopt **Alternative 3** above (codify the upstream convention with a real one-paragraph `AGENTS.md` that delegates to CLAUDE.md), OR adopt **Alternative 2** (drop the `!AGENTS.md` line, edit CLAUDE.md:9's enumeration, accept the upgrade-entry references as a separate "supersede-don't-edit" question).
