# Scope map — shadow comparator vs existing primitives

| Existing primitive | Disposition | Reason |
|---|---|---|
| `critic-architecture` | **extend** | Stays as Opus-authoritative lens. A new sibling `critic-architecture-shadow` (Sonnet) runs in parallel under `SHADOW_PANEL=1`. Original is unchanged. |
| `critic-operations` | **extend** | Same pattern: Opus stays, Sonnet sibling added. |
| `critic-product` | **extend** | Same pattern. |
| `frame-challenger` | **subsume (no change)** | Runs pre-generator; shadow comparator runs post-critique. No overlap, no conflict. Frame-challenger is not affected. |
| `subagent-distiller` | **subsume (no change)** | The comparator emits its own structured table; no need to re-invoke distiller on comparator output. |
| `requirement-classifier` | **subsume (no change)** | Step 1 of the workflow; not in the panel layer. Untouched. |
| `outside-view` | **subsume (no change)** | Step 3; pre-panel. Untouched. |
| `canon-librarian` | **subsume (no change)** | Step 4; pre-panel. Untouched. |
| `scope-mapper` | **subsume (no change)** | Step 7; pre-generator. Untouched. |

## New primitives introduced

| New primitive | Why new (not extension) | Conflict with existing |
|---|---|---|
| `critic-architecture-shadow` | Different `model:` pin in frontmatter; cannot be a parameter to existing agent because Claude Code's Agent tool dispatches by name. | None. |
| `critic-operations-shadow` | Same reasoning. | None. |
| `critic-product-shadow` | Same reasoning. | None. |
| `critic-comparator` | New role: cross-lens diff. No existing primitive serves this. | None. |

## Conflicts

None identified. The shadow lane is purely additive.

## Default disposition statement

The default for new entries is `subsume` or `replace`; this scope-map deviates by choosing `extend` for the three lens primitives. Stated reason: the entry's design preserves Opus authority on each existing lens by construction; replacing the existing lenses would discard that property.
