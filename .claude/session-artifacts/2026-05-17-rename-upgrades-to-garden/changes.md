# changes.md — session 2026-05-17-rename-upgrades-to-garden

Running list of files touched in this session. One line per file: `<verb> <path>` where verb ∈ {created, modified, renamed, deleted}.

Used to scope `git add` at commit time — only paths listed below.

## Pre-flight decisions

- **Folder rename:** `upgrades/` → `garden/`
- **Category names:** `profound → heirloom`, `outlandish → specimen`, `no-brainer → volunteer`, `normal → perennial`
- **Word swap:** `tier` → `category`
- **Slash command:** keep `/upgrade` (verb still works for "upgrade the AI system"); skill folder stays at `.claude/skills/upgrade/`
- **Category emoji set:** 🌹 heirloom · 🌳 specimen · 🍀 volunteer · 🌿 perennial
  - All four chosen so each emoji is a *recognizable canonical example* of its category, with an established phrasing backing it:
    - 🌹 heirloom rose (THE heritage flower, named cultivars going back centuries)
    - 🌳 specimen tree (actual horticulture term-of-art)
    - 🍀 lucky clover (clovers ARE the unbidden surprise plant; matches "you'd be silly not to keep it")
    - 🌿 perennial herb garden (common phrase; herbs are mostly perennials)
  - Earlier iteration used 🍅/🌳/🌾/🌿 but each was a *specific instance* (tomato, wheat) rather than a *category representative*. Revised after operator review.
  - All four avoid collision with the 10-state lifecycle emojis (🌱🔬📋✅⚙️🔨🩺🔖💎🏁).
- **Meta-row rename:** `🎯 tier` → `🎯 category`. Keep `🚀 upgrade` row as-is (describes aspiration, separate from category)
- **Skipped per feedback memory:**
  - Entry bodies (only meta-table category-row updated programmatically)
  - `research/sota-2026*/` (historical research outputs — prose mentions left alone)
  - `canon/corpus/march-exploration-exploitation-1991/` (frozen canon entry)
  - `plans/` (ephemeral per memory)

## Files touched

| Verb | Path |
|---|---|
| created | .claude/session-artifacts/2026-05-17-rename-upgrades-to-garden/changes.md |
| renamed | upgrades/ → garden/ |
| renamed | garden/profound/ → garden/heirloom/ |
| renamed | garden/outlandish/ → garden/specimen/ |
| renamed | garden/no-brainer/ → garden/volunteer/ |
| renamed | garden/normal/ → garden/perennial/ |
| modified | garden/README.md |
| modified | garden/LEDGER.md |
| modified | CLAUDE.md |
| modified | README.md |
| modified | maintenance/README.md |
| modified | .claude/agents/README.md |
| modified | .claude/agents/canon-refresher.md |
| modified | .claude/hooks/README.md |
| modified | .claude/plugins/README.md |
| modified | .claude/skills/README.md |
| modified | .claude/skills/upgrade/SKILL.md |
| modified | .claude/skills/path-check/SKILL.md |
| modified | .claude/skills/critique/SKILL.md |
| modified | .claude/skills/repo-update/SKILL.md |
| modified | .claude/skills/repo-doctor/SKILL.md |
| modified | bin/explain-state.sh |
| modified | bin/explain-card.sh |
| modified | bin/explain-render.sh |
| modified | bin/diagnostics/README.md |
| modified | 60 entry meta-tables (garden/*/*/README.md — programmatic 🎯 tier → 🎯 category sweep) |
| modified | garden/README.md — Shape-of-thought section rewrite (7→8 shapes; added audit; broadened reflection; new framing citing Bruner/Peirce/Searle traditions and contrasting with engineering doc-types) |
