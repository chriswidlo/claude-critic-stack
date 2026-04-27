# Critiques aggregate — `2026-04-27-critics-get-write-tool-impl`

## Loop 1 (original candidate: add Write to critics + Defense 1 + Defense 2 + thin-index aggregate)

| Lens | Verdict | Top objection (one line) | Full critique |
|---|---|---|---|
| Architecture | **reject** | Role-fusion: collapsing reviewer + author-of-record dissolves the orchestrator chokepoint. | [critiques/architecture.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/critiques/architecture.md) |
| Operations | **rework** | Concurrency-posture step-change treated as extension; no write-time session-id assertion, no canary. | [critiques/operations.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/critiques/operations.md) |
| Product | **rework** | Operator surface regresses; thin-index is unnamed schema; Defense 2 is unconditional tax for unmeasured bias. | [critiques/product.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/critiques/product.md) |

**Routing:** replan to Step 8 under new frame (parliament-with-clerk separation).

## Loop 2 (candidate v2-C: orchestrator-as-sole-writer + byte-fidelity prose contract; drop aggregate; escalate recursion)

| Lens | Verdict | Top objection (one line) | Full critique |
|---|---|---|---|
| Architecture | **rework** | v2-C picks the weaker enforcement mechanism (prose contract vs. structured return); byte-fidelity is undefined across encoding/escaping/normalization. | [critiques/architecture-v2.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/critiques/architecture-v2.md) |
| Operations | **rework** | Prose contract is not a control (no forcing function, no detection primitive, no recovery); orchestrator-paraphrase relocated, not eliminated. | [critiques/operations-v2.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/critiques/operations-v2.md) |
| Product | **rework** | Drop-the-aggregate overshoots; verdict-at-a-glance affordance removed; operator-escalation is workflow-evasion not affordance. | [critiques/product-v2.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/critiques/product-v2.md) |

**Routing:** loop cap reached. Synthesize with disagreements named.

## Convergent loop-2 fixes the panel named (additive)

The three loop-2 reworks point at small, concrete additions. They are non-conflicting and combine into a "v2-C+" the panel did not get to see:

1. **Index file** (product) — `critiques/INDEX.md` listing `lens · verdict-label · filename`, with verdict vocabulary pinned to `approve | rework | reject`. Restores at-a-glance affordance.
2. **Delimiter-escaping rule + encoding spec** (architecture) — define what "verbatim between `<critique>` and `</critique>`" means under whitespace, unicode, line-ending normalization. Place the closing delimiter on its own line; body must not contain that line.
3. **Content-addressed envelope** (architecture) — orchestrator computes sha256 of the bytes it persists; writes `# sha256: <digest>` as a header. Detection becomes mechanical.
4. **Step 12 partial-read policy** (operations) — if any per-lens file is missing or empty, halt synthesis and re-invoke; do not proceed on N-of-3.
5. **Concrete operator action on self-modifying changes** (product) — replace synthesis-time escalation disclaimer with either (a) a one-line operator checklist or (b) a warn-but-not-block routing rule.

Together, items 1–5 are roughly the same scope as v2-C itself (each is one CLAUDE.md sentence or one short artifact). They constitute the "what would change my verdict to approve" actionable list across all three lenses for the loop-2 candidate.

## Note on incentive surface (loop 2)

Architecture explicitly noted in loop 2 that its status-quo-on-self-modification bias from loop 1 is *lower* on v2-C, because v2-C does not modify the architecture lens's surface (no Write grant). If anything, the bias may now run the other way (toward approving a change that leaves the agent file alone). The orchestrator should weight this as: *all three loop-2 reworks have measurable structural objections (specific invariants, missing primitives, named affordance losses) rather than vocabulary objections; each is actionable*.

## Decision

Per CLAUDE.md Step 11: cap at two full loops; past that, escalate to synthesis with the disagreements named. **Synthesis runs.**
