# Requirement classification

## Primary label
investigation

## Default frame (from label)
"What would we do differently if we knew the answer? If nothing, the question is decorative." Frame the zone-readers, canon retrieval, and outside-view as adversarial extraction against a single primary document (the Opus 4.7 System Card), with each invariant tied in advance to a downstream repo-change decision it could flip — so no zone-reader finding lands without a named change-set hook it would influence.

## Known frame bias
**Research theater.** Producing a comprehensive, well-cited readout that no downstream decision actually depends on. The mitigation is the user's own structural choice — binding the investigation to a concrete repo change-set under the hard gate — but the bias remains: zone-readers will be tempted to surface "interesting" findings that do not bear on any agent, rule, or canon entry, padding the dossier without changing the change-set.

## Secondary label
**new** — the downstream phase produces a concrete change-set against [.claude/agents/](.claude/agents/), [CLAUDE.md](CLAUDE.md), and [canon/](canon/), some of which will be net-new primitives (e.g., a system-card-derived canon entry, a new agent contract clause, a new invariant in the orchestrator rules) rather than modifications to existing ones.

## Alternative classification
**extend** — would become primary if the change-set turns out to be dominated by amendments to existing agent contracts, [CLAUDE.md](CLAUDE.md) clauses, and canon entries (preserving their current contracts while adding 4.7-derived constraints), rather than introducing net-new primitives. The Phase 4 [scope-map.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/scope-map.md) will reveal which it is; if scope-map rows are mostly `extend`, reclassify.

## User's framing words
- *"Produce the deepest possible adversarial readout … and translate the findings into a concrete change-set"* — presumes investigation-then-design, which the classifier accepts as primary=investigation, secondary=new. The user's own note ("two phases internally") confirms this is the intended reading rather than a hidden single-label decision.
- *"Treat the system card as a primary risk dossier, not a marketing document"* — adversarial framing, not a label assumption.
- *"runs through the full critic-panel under SHADOW_PANEL=1 before synthesis"* — presumes the change-set is decision-bearing enough to warrant triangulation; consistent with investigation feeding a downstream decision rather than pure inquiry.

What would change the classification: if the user dropped the change-set requirement and asked only for the readout, the secondary `new` would vanish and this would be pure `investigation`. If the user dropped the readout and asked only "what should we change in the repo given 4.7," it would flip to `new` (or `extend`) with investigation as a subordinate gather step.

## Gaps
- Whether the change-set is expected to touch canon corpus entries (a net-new entry for the system card itself is planned in Phase 9) or only agents and [CLAUDE.md](CLAUDE.md) — this affects whether secondary should be `new` or `extend`. (Resolved: yes, canon ingest is in scope as a *proposal* for [canon/sources.ingest.yaml](canon/sources.ingest.yaml), not a direct write to [canon/corpus/](canon/corpus/).)
- Whether "concrete change-set" means a written proposal artifact ([repo-changeset.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/repo-changeset.md)) or actual file edits committed in this session. The former is investigation-with-design-output; the latter would push the primary label toward `new`/`extend`. (Working assumption: written proposal only; agent/CLAUDE.md/canon edits are deferred until after critic-panel approval.)
- Whether any 4.7 finding could plausibly invalidate an existing primitive outright (would introduce `replace` as a third candidate); current framing assumes additive/amendment changes only.
