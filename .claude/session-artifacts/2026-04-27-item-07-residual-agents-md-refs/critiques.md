# Critic-panel verdicts — item 7 (residual AGENTS.md references)

## Aggregate

| Lens | Verdict | Frame-level objection |
|---|---|---|
| **Architecture** | `reject` | Item 7 is the first instance forcing the lab's mutability discipline to be named. Resolving it via per-occurrence ad-hoc rules sets retroactive precedent. |
| **Operations** | `rework` | Plan deploys a state-change to an unmonitored data store (the upgrade canon) without pre-deploy invariant check or post-deploy detector. The grep verification is a presence detector, not a regression detector. |
| **Product** | `rework` | Upgrade-entry contract with future readers is being violated: in-place rewrites of body cells don't advance lifecycle markers, leaving entries visibly silent about post-creation edits. |

**Minority-veto invoked.** Architecture's reject is frame-level; operations and product reworks converge on the same objection from different angles.

## Convergence on alternative move

All three lenses point — explicitly (architecture, product) or implicitly (operations) — at the **tombstone alternative**:
- **Architecture §4 option (a):** *"Recreate AGENTS.md at root as a one-line tombstone … zero edits to upgrade-entry bodies."*
- **Operations §8:** add a visible trail next to each rewrite. The tombstone subsumes the trail-need by eliminating the rewrites.
- **Product §6 step 2:** *"Defer the three benefit-cell rewrites until the follow-up convention exists."* Tombstone defers them indefinitely (they are no longer needed — the partner doc exists).

The architecture critic also surfaces a useful observation: `.gitignore`'s `!AGENTS.md` line is a forward-compat hook (allowlist-as-policy), not a no-op. Under tombstone, the line stops being misleading — and stays useful.

## Files
- [architecture.md](critiques/architecture.md)
- [operations.md](critiques/operations.md)
- [product.md](critiques/product.md)
