# `.genesis/` — founding documents

Files that predate or shipped with the initial commit of `claude-critic-stack` and are preserved here as historical seed material. Not active workflow surface; not referenced from `CLAUDE.md` or any agent. Hidden (`.`-prefix) so it stays out of `ls` and out of the active repo surface, but tracked in git.

Inclusion criterion: file existed in or before the initial commit (`6328aaf`, 2026-04-23 *"baseline claude-critic-stack before Ultraplan refinement"*) and has since been superseded by primitives the repo grew on top of it.

## Contents

- [five-pressures.md](.genesis/five-pressures.md) — original five-failure-mode checklist (created 2026-04-22, in initial commit). Four of its five pressures are now absorbed by the 13-step workflow (reframe → step 2; outside-view → steps 3–5; name-uncertainty → step 12; consequence-imagine → step 12). The one pressure not redundantly enforced is #2 (*"Enumerate-before-select: list ≥3 candidate solutions before recommending one"*) — flagged in [item 13's synthesis](.claude/session-artifacts/2026-04-27-item-13-orphans-fate/synthesis.md) as an open question for a future workflow-design session.
- [architecture-review.md](.genesis/architecture-review.md) — original 7-step workflow doc (in initial commit, never edited since). Single-`critic` agent + three-subagent shape; superseded by the 13-step workflow in [CLAUDE.md](CLAUDE.md) and the 14 agents in [.claude/agents/](.claude/agents/). Was the only file in `workflows/`; that directory is now gone. Superseding session: see [item 4's synthesis](.claude/session-artifacts/2026-04-27-item-04-stale-workflow-docs/synthesis.md).
- [ok-cool-this-is-warm-balloon.md](.genesis/ok-cool-this-is-warm-balloon.md) — Phase-1/Phase-2 plan that drove the redesign from the day-1 baseline into the current shape. Already shipped per git log (commits `cfbba1f` Phase 1, `dbb741d` Phase 2). Preserved as the design record for *why* the stack looks the way it does.
