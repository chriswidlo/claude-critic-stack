# maintenance/

**The third zone of this repo.** Sibling to [garden/](garden/), equally separated from the workflow.

## The three-zone model

| Zone | Lives in | Purpose | Workflow knows about it? |
|---|---|---|---|
| **Workflow** | [CLAUDE.md](CLAUDE.md) + [.claude/](.claude/) | The running adversarial-review system | — (workflow IS this) |
| **Garden** | [garden/](garden/) | R&D backlog: profound, novel, creative ideas for elevating the system | **No** — workflow is blind to the garden |
| **Maintenance** | `maintenance/` (this folder) | Repo hygiene: rule-conformance checks, orphan detection, freshness audits, drift catches, cleanup tasks | **No** — workflow is blind to maintenance too |

The separation is deliberate. The workflow's job is to do adversarial design review. Polluting it with hygiene chores or research backlog leaks attention into the wrong tier. Maintenance is the layer that keeps the workflow's primitives correct, but it runs *on* the workflow, never *as part of* it.

## Empty by design

This folder is a placeholder. No procedures, scripts, agents, or skills live here yet. The README is the starting point: when you need to do a maintenance pass, you come here first.

The folder is not referenced from [CLAUDE.md](CLAUDE.md) or any agent. The workflow does not invoke maintenance; maintenance is operator-triggered.

## What could go here (when the need arises)

### Audit categories (what to check)

| Category | What it catches |
|---|---|
| **Path discipline** | Absolute paths, `~/`-paths, `../`-chains, broken links across all `.md` files |
| **Schema conformance** | `canon/sources.yaml` validates against schema_version 2; every entry has required fields with valid enum values |
| **Freshness** | Canon entries past `last_verified + cadence(volatility)`; research distillations past `next_review_by` |
| **Orphans** | `canon/corpus/<slug>/` dirs without `sources.yaml` entries; `sources.yaml` entries without corpus dirs (when lifecycle ≠ live-only); skill files without slash-command registration; agents not referenced by CLAUDE.md or any other agent |
| **Stale references** | Old terminology (`12-step` → `13-step`); references to retired primitives (`parse-session-metrics.py`, `sources.ingest.yaml`); broken cross-doc links |
| **Format conformance** | READMEs follow the synthesized template in [research/sota-2026-v2/16-ai-readable-docs.md](research/sota-2026-v2/16-ai-readable-docs.md); CLAUDE.md under length target; "what + when" in agent/skill descriptions |
| **Cleanup detritus** | `.bak` files anywhere; empty placeholder folders that have outlived their relevance; commented-out code blocks |
| **Settings integrity** | `.claude/settings.json` validates as JSON; deny/allow/ask tiers complete per `research/sota-2026-v2/10-safety-guardrails.md` |
| **Diagnostics drift** | `diagnostics/metrics.json` schema_version matches the parser version; hooks are wired correctly in settings.json |
| **Memory hygiene** | The user's machine-local auto-memory (described in prose per [CLAUDE.md](CLAUDE.md) §"Path discipline") isn't contradicting current repo state |

### Tooling that lands here

Maintenance work in this repo splits along the **doctor / update** boundary, mirroring the industry convention (`brew doctor` vs `brew update`; `npm outdated` vs `npm update`; `git fetch` vs `git pull`).

**Doctor** = surfaces **broken / wrong / misaligned** state (drift, dead links, orphans, schema violations, stale terminology). Diagnoses; never modifies.

**Update** = surfaces **stale** state (time-eligible for refresh — canon past cadence, dependencies, external freshness, inventory drift). Dry-run by default; per-item apply with explicit operator approval.

**The two skills, both in DRAFT:**

| Skill | Mode | Output dir | Disable-model-invocation |
|---|---|---|---|
| [`.claude/skills/repo-doctor/SKILL.md`](.claude/skills/repo-doctor/SKILL.md) — `/repo-doctor` | Read-only diagnostic. 29 checks across 5 tiers (structural / schema / xref / format / invariants). Stays out of update's lane. | `maintenance/audits/<date>-<slug>.md` | yes |
| [`.claude/skills/repo-update/SKILL.md`](.claude/skills/repo-update/SKILL.md) — `/repo-update` | Report-by-default, apply-by-flag. 25 checks across 6 industry-canonical update categories (index-refresh, outdated-report, in-range apply, constraint-bump, lockfile refresh, state-snapshot dump). Per-item `apply --only=<id>` with explicit operator approval. Stays out of doctor's lane. | `maintenance/updates/<date>-<slug>.md` | yes |

**Shared design (both skills):**
- Rule-source-map architecture: rules live in their canonical locations (CLAUDE.md, the various READMEs, `research/sota-2026-v2/16-ai-readable-docs.md`); the skill body maps "where to find each rule + how to check against it." Skill stays correct when rules evolve in their canonical source.
- DRY RUN banner at top AND bottom of chat output.
- `disable-model-invocation: true` — operator-invoke only; no auto-fire.
- DRAFT status — surfaces findings, does not validate fixes for automation yet.

**Deferred (would land here when first needed):**

- `maintenance/bin/check-canon-schema.sh` — wraps the ingester's validation pass for use outside the skill chain.
- A scheduled `claude.ai/code` Routine that runs `/repo-doctor` + `/repo-update` weekly and posts the summaries.
- Promotion-out-of-DRAFT criteria document (after N validation runs, what raises the gate?).

None of the deferred items exist yet. They land when the need pushes them, not pre-emptively.

## Discipline (when this folder becomes active)

1. **Maintenance is operator-triggered, never workflow-triggered.** The workflow must not invoke maintenance. The point of the three-zone separation is that hygiene chores don't compete with adversarial review for attention.
2. **Maintenance scripts are read-mostly.** They *detect* drift; they *propose* cleanup. They don't auto-delete, auto-rename, or auto-edit without explicit operator approval. The exception is `safe-rm.sh` invocations for clearly-stale items (e.g., `.bak` files).
3. **Findings go into a maintenance report**, not into the workflow surface. A maintenance pass writes a single timestamped report (e.g., `maintenance/audits/2026-08-15-audit.md`) — the workflow does not consume it.
4. **Per the [Operating principle](README.md#operating-principle--ratchet-forward-never-sideways):** when maintenance surfaces a clean rewrite opportunity (legacy file, deprecated pattern), the rewrite is proposed in the next operator-facing interaction with cited evidence — not deferred indefinitely.

## How to use this folder

The recommended cadence mirrors `brew doctor` → `brew update` → `brew outdated` → `brew doctor` again (industry-canonical sandwich):

1. **`/repo-doctor`** — surface structural problems. Writes report to `maintenance/audits/<YYYY-MM-DD>-<scope>.md`. Read the report.
2. **Fix structural findings manually.** Per the [Operating principle](README.md#operating-principle--ratchet-forward-never-sideways), the human gates every change.
3. **`/repo-update`** — once structural is clean, check what's stale. Writes report to `maintenance/updates/<YYYY-MM-DD>-<scope>.md`.
4. **Apply refreshes per-item:** `/repo-update apply --only=<id>` for each item you want to refresh. Idempotent; per-item; explicit approval per refresh.
5. **`/repo-doctor` again** — after refreshes, re-verify structural integrity (some refreshes may have introduced drift in inventory READMEs, etc.).
6. **Commit the cleaned + refreshed state.**

**If the pass justifies building a new check-script,** land it under `maintenance/bin/` and reference it from the appropriate skill's check catalog so future runs invoke it.

**Both skills are currently in DRAFT.** Treat their output as informational; do not wire into automated CI yet. Promote out of DRAFT only after enough manual runs have validated the findings catalogs match operator expectations and false-positive rate is acceptable.

## What does NOT go here

- **R&D ideas** — those go to [garden/](garden/).
- **Workflow primitives** (agents, skills, hooks) — those go under [.claude/](.claude/).
- **Per-session reasoning** — that goes under `.claude/session-artifacts/<session-id>/`.
- **Ephemeral planning notes** — those go to [plans/](plans/).
- **Maintenance for the *target* repo being reviewed** — out of scope; this stack reviews other repos' designs, it doesn't audit them.

## See also

- [garden/README.md](garden/README.md) — the R&D garden (sibling zone)
- [README.md](README.md) §"Operating principle — ratchet forward" — the discipline that maintenance enforces
- [research/sota-2026-v2/16-ai-readable-docs.md](research/sota-2026-v2/16-ai-readable-docs.md) — the README authoring standard maintenance audits against
