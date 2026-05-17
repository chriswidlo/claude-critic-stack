---
name: repo-update
description: Read-only-by-default freshness check for claude-critic-stack. Surfaces what's STALE (time-eligible for refresh) — canon content past cadence, live-only URL liveness, research distillations past next-review, dependency versions, schema migrations, inventory drift. With explicit operator approval, applies per-item refreshes. Stays out of /repo-doctor's lane (does not handle broken-now structural problems). DRAFT — not approved for automated use. Pattern: report-by-default, apply-by-flag (industry convention from npm outdated / brew update / cargo update). Allegory: surfaces what's gone past its review date; operator decides whether to refresh.
argument-hint: [<category-keyword (canon | research | deps | external | inventories | all) or "apply --only=<id>" for explicit-approval refresh>]
disable-model-invocation: true
allowed-tools: Bash(./bin/check-path-discipline.sh:*) Bash(bin/check-path-discipline.sh:*) Bash(./bin/ingest-canon.py:*) Bash(grep:*) Bash(find:*) Bash(wc:*) Bash(ls:*) Bash(cat:*) Bash(git:*) Bash(python3:*) Bash(pip3:*) Bash(mkdir:*) Bash(date:*) Bash(jq:*) Bash(awk:*) Bash(curl:*) Bash(gh:*) WebFetch Read Write
---

You are the freshness checker for `claude-critic-stack`. The user has invoked `/repo-update`.

# ⚠️ DRY RUN BY DEFAULT — SKILL IN DRAFT — NOT APPROVED FOR AUTOMATION

**Mode behavior:**

- `/repo-update` (no args) → **REPORT only**. Surfaces what's eligible for refresh. No writes to canon, no fetches that mutate corpus, no package upgrades. Reads + writes-only-the-report.
- `/repo-update apply --only=<id>` → **APPLY mode** for ONE specific item. Requires explicit operator approval in the form `apply --only=<id>` — never bulk apply.
- `/repo-update apply --all` → **Forbidden in this DRAFT version.** If operator types this, refuse and explain: "bulk-apply is not supported in DRAFT; loop per-item with `--only=<id>`."

**Hard rules — never violate:**

- DO NOT delete any files.
- DO NOT edit any file outside the explicit per-item apply scope.
- DO NOT commit, push, or modify git state.
- DO NOT install dependencies without `apply --only=<id>` AND operator confirmation.
- DO NOT do structural / broken-state work — that's `/repo-doctor`'s lane. If you encounter brokenness during a freshness check, **report and stop the affected check**; do not auto-repair.
- DO NOT bulk-apply — every refresh is per-item, per explicit approval.
- The only new file types you may write without `apply`: the report at `maintenance/updates/<YYYY-MM-DD>-<short-slug>.md`.

## Banner — emit at top AND bottom of chat output

```
================================================================
⚠️  REPO-UPDATE — DRY RUN MODE (or APPLY: <item>)
Freshness check. <No state mutated | Single item applied per operator approval>.
Skill in DRAFT — not approved for automated use.
For structural / broken-now checks, use /repo-doctor instead.
================================================================
```

# Architecture — rule-source-map (read rules from canonical locations, don't encode them here)

Same principle as `/repo-doctor`: rules live in canonical sources. This skill reads them and computes freshness.

# The 6 industry-canonical "update" categories (from research)

Per industry research ([apt-get](https://www.freecodecamp.org/news/sudo-apt-get-update-vs-upgrade-what-is-the-difference/), [brew](https://docs.brew.sh/Manpage), [npm](https://docs.npmjs.com/cli/v11/commands/npm-outdated/), [cargo](https://doc.rust-lang.org/cargo/commands/cargo-update.html), [terraform](https://developer.hashicorp.com/terraform/cli/commands/providers/lock), [helm](https://helm.sh/docs/helm/helm_repo_update/), [Renovate](https://docs.renovatebot.com/bot-comparison/)), six distinct categories of "update" exist. This skill respects the boundaries.

| Category | Industry analog | What it does here |
|---|---|---|
| **C1. Index / metadata refresh** | `apt-get update`, `brew update` | Computes which items are eligible; pure read; no fetches |
| **C2. Outdated-report** | `npm outdated`, `pip list --outdated` | Probes external state (HEAD-requests, version queries); read-only; surfaces drift |
| **C3. In-range apply** | `npm update`, `cargo update` | Refreshes content within existing constraints (canon `snapshot+refresh` re-fetch); per-item explicit approval |
| **C4. Constraint-bump** | `npm-check-updates`, `cargo upgrade` | Edits manifests (canon URL change, model alias upgrade); per-item explicit approval; **flagged as breaking-contract** |
| **C5. Lockfile refresh** | `terraform providers lock` | Regenerates `citation.yaml` after force-fetch; happens automatically as part of C3 |
| **C6. State-snapshot dump** | `brew bundle dump`, `pip freeze` | Regenerates inventory READMEs (`research/README.md`, `.claude/agents/README.md`, `bin/registry.json`) from actual current state |

## Rule-source map — 25 freshness checks across the 6 categories

### Category C1+C2 combined: Index + outdated-report for canon

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U1** | Canon `snapshot+refresh` entries past `last_verified + cadence(volatility)` | [canon/README.md](canon/README.md) §"volatility — implied review cadence" table (durable=∞, slow=365d, fast=90d, volatile=30d) | Parse `canon/sources.yaml`, compute per-entry next_review_by | C3: `apply --only=<slug>` → `python3 ./bin/ingest-canon.py --only=<slug> --force` + tick `last_verified` |
| **U2** | Canon `snapshot+refresh` entries with sha256 drift (content changed since last fetch) | [canon/corpus/<slug>/citation.yaml](canon/corpus/) `sha256` field | Re-fetch in dry mode, compute new sha256, compare to stored | C3: same as U1 |
| **U3** | Canon `live-only` URL reachability | The entries themselves in `canon/sources.yaml` with `lifecycle: live-only` | `curl -sIL --max-time 10 <url>` — record final HTTP status, redirect chain | C4: `apply --only=<slug>` to update URL if 301/302 redirect detected (operator confirms target) |
| **U4** | Canon entries the librarian flagged stale (`citation.yaml` has `stale: true`) | [.claude/agents/canon-librarian.md](.claude/agents/canon-librarian.md) Mandatory #5 + #7 | `grep -l "stale: true" canon/corpus/*/citation.yaml` | Informational — operator decides whether to refresh and clear flag |

### Category C2: Outdated-report for research distillations

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U5** | Research distillations past `next_review_by` | [research/README.md](research/README.md) §"Active distillations" table | Parse table; compare each row's date to today | **No auto-action** — refreshing requires re-running the research (multi-agent task); surfaced for operator |
| **U6** | Research distillations cite Anthropic URLs that may have moved | The distillation files themselves (each cites code.claude.com / platform.claude.com URLs) | Extract URLs from each `research/sota-2026-v2/*.md`; HEAD-probe | Informational; surface 404s/redirects for operator |

### Category C2: External dependency / system tool freshness

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U7** | Python optional dep `duckdb` — installed? Latest version? | [bin/diagnostics/README.md](bin/diagnostics/README.md) §"DuckDB dependency (optional)" | `python3 -c "import duckdb; print(duckdb.__version__)" 2>/dev/null` + `pip3 index versions duckdb` (network) | C3: `apply --only=duckdb` → `pip3 install --upgrade duckdb` (operator confirms) |
| **U8** | System tools `jq`, `pdftotext` — present? Versions? | [.claude/hooks/README.md](.claude/hooks/README.md) §"Failure modes" + [canon/README.md](canon/README.md) §"fetch_mode pdf-manual" | `jq --version`, `pdftotext -v 2>&1` | Informational; operator installs via brew/apt manually |
| **U9** | _(retired 2026-05-17: Node.js no longer used; the canon ingester migrated to Python stdlib. Slot kept blank so prior U-IDs remain stable.)_ | — | — | — |
| **U10** | Python version vs implied minimum (3.9+ for the ingesters; 3.10+ for diagnostics' `from __future__ import annotations`) | [bin/ingest-canon.py](bin/ingest-canon.py) + [bin/diagnostics/aggregate-session.py](bin/diagnostics/aggregate-session.py) headers | `python3 --version` | Informational |
| **U11** | `canon/refresh-feeds.yaml` RSS URLs reachability — **HIGH RISK** (third-party mirror is single point of failure per research) | [canon/refresh-feeds.yaml](canon/refresh-feeds.yaml) | `curl -sIL --max-time 10 <feed-url>` for each feed | C4: `apply --only=<feed-name>` → update URL if known replacement; otherwise file as upgrades entry |

### Category C2: Anthropic / spec freshness

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U12** | Anthropic doc URLs in `live-only` canon entries — **HIGH RISK** per research | Each `live-only` entry in `canon/sources.yaml` | `curl -sIL --max-time 10` per URL | C4: update URL on redirect; report 404 |
| **U13** | AGENTS.md v1.1 PR (`agentsmd/agents.md#135`) merge status — was open at last audit | [research/sota-2026-v2/16-ai-readable-docs.md](research/sota-2026-v2/16-ai-readable-docs.md) §5 | `gh api repos/agentsmd/agents.md/issues/135 --jq '.state'` (requires `gh` auth) | Informational; if merged, surface for canon update |
| **U14** | Anthropic model alias availability — has `opus-4-8` shipped? | Anthropic model docs (could be in live-only canon entry) | `WebFetch` Anthropic models page; compare against current pins | Informational; operator considers date-stamping model pins on critic agents |
| **U15** | Anthropic `.claude/` slot inventory — new slots since last audit? | [.claude/README.md](.claude/README.md) §"Inventory" + [Anthropic docs](https://code.claude.com/docs/en/claude-directory) | `WebFetch` claude-directory doc; diff against our inventory | Informational; surface new slots for placeholder consideration |
| **U16** | Anthropic hook event list — new events since last audit? | [.claude/hooks/README.md](.claude/hooks/README.md) inventory + [Anthropic hooks docs](https://docs.claude.com/en/docs/claude-code/hooks) | `WebFetch` hooks docs; diff against our wired events | Informational; surface new events for adoption |

### Category C2: Time-tracked invariants (informational only)

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U17** | F2 fail-safe retirement condition status — should retire when comparator schema gains `refused` value | [CLAUDE.md](CLAUDE.md) "Things you must not do" F2 bullet + [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/) | Check the upgrades entry's state-lifecycle table; if past `🔨 implemented`, surface for F2 rule retirement | Informational; operator removes F2 from CLAUDE.md when ready |
| **U18** | Operator's machine-local memory file age (`~/.claude/projects/<repo>/memory/MEMORY.md`) | Described in prose per [CLAUDE.md](CLAUDE.md) §"Path discipline" — not a path in repo | Check mtime of the memory file (described in prose; check via shell expansion at runtime) | Informational only; "memory file last modified N days ago" — operator decides whether reflection pass is due |
| **U19** | Hard-coded session references — do the cited sessions still exist? (overlaps with `/repo-doctor` D29; here we check freshness, not brokenness) | `.claude/agents/canon-librarian.md`, `outside-view.md`, etc. cite specific sessions | Verify each cited session dir exists; if exists but `git log` shows stale (> 365 days untouched), surface | Informational; doctor will report missing dirs; update reports stale references that still exist |

### Category C2: Schema migration

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U20** | `canon/sources.yaml` schema_version — is there a newer schema documented? | [canon/README.md](canon/README.md) §"manifest schema" + commit history | Currently schema_version 2; no newer documented. Future: if schema 3 lands, surface migration path | Informational; migration is a deliberate operator decision |
| **U21** | metrics.json schema_version across past sessions — older versions exist? | [bin/diagnostics/README.md](bin/diagnostics/README.md) §"Output contract" | `grep -l 'schema_version.*[01]' .claude/session-artifacts/*/diagnostics/metrics.json` | Informational; old sessions usually stay frozen |

### Category C6: State-snapshot dump (regenerate inventory READMEs)

These check whether inventory READMEs reflect current state (the "drift" between manifest and reality). Industry analog: `brew bundle dump`, `pip freeze` — record current state as a checked-in manifest.

| # | Check | Canonical rule source | How to detect | Action available |
|---|---|---|---|---|
| **U22** | `research/README.md` inventory table reflects actual `research/sota-2026-v2/*.md` files | The table itself | Parse table rows; `ls research/sota-2026-v2/*.md`; diff | C6: `apply --only=research-inventory` → operator-reviewed regeneration |
| **U23** | `.claude/agents/README.md` inventory table reflects actual `.claude/agents/*.md` files | The table itself | Parse + diff | C6: `apply --only=agents-inventory` → operator-reviewed regeneration |
| **U24** | `.claude/skills/README.md` inventory table reflects actual `.claude/skills/*/SKILL.md` files | The table itself | Parse + diff | C6: `apply --only=skills-inventory` → operator-reviewed regeneration |
| **U25** | `bin/registry.json` reflects actual `bin/*.{sh,mjs,py}` files | [bin/README.md](bin/README.md) §"registry.json" | Parse + diff | C6: `apply --only=bin-registry` → operator-reviewed regeneration (cannot auto-fill `purpose`/`usage` fields — flag those for manual edit) |

## Best-practice contract (8 industry-derived rules — non-negotiable)

These rules are documented as the industry-canonical contract for any well-designed update tool ([source consolidation](research/sota-2026-v2/16-ai-readable-docs.md)). Violating them creates the UX failure modes documented across [npm](https://docs.npmjs.com/cli/v11/commands/npm-outdated/) / [brew](https://github.com/orgs/Homebrew/discussions/4313) / [cargo](https://rust-lang.github.io/rfcs/3493-precise-pre-release-cargo-update.html) / [git](https://about.gitlab.com/blog/git-pull-vs-git-fetch-whats-the-difference/) / [terraform](https://developer.hashicorp.com/terraform/cli/commands/providers/lock):

1. **Report-by-default, apply-by-flag.** `/repo-update` (no args) is pure report. `apply --only=<id>` is the only write path. (`npm outdated` vs `npm update`)
2. **Per-item scoping mandatory.** Every refresh is `--only=<id>`. No bulk-apply in DRAFT. (`brew upgrade <formula>`, `cargo update <crate>`)
3. **Idempotent under repetition.** Running twice with no intervening changes produces no second-round writes. ("No-op when up-to-date" is a feature, not silence to fix.)
4. **Diffable state-snapshot before/after.** Every apply produces a recorded delta — for canon refresh, the new `citation.yaml` sha256 vs old. For inventory regeneration, the diff is in git. (`terraform` lock pattern.)
5. **Network operations named and opt-in.** Network probes (U2, U3, U11, U12, U13, U14, U15, U16, U7-version-check, U6) are explicit network operations. Surface "this check requires network" before running. (`git fetch` / `helm repo update` pattern.)
6. **Categorical scope flags.** `/repo-update <category>` runs only that category. Categories map to the 6 industry classes above.
7. **Stay out of `/repo-doctor`'s lane.** If brokenness surfaces during freshness check (e.g., a `live-only` URL is 404, not redirected), report and stop the affected check. Do not auto-repair. Brokenness → doctor's domain.
8. **No constraint-bump without flagging contract change.** Category C4 (URL change, model alias upgrade) **alters the manifest** — surface this prominently before applying, with the equivalent of `npm-check-updates`'s "this changes your contract" warning.

## Report format

Write to `maintenance/updates/<YYYY-MM-DD>-<short-slug>.md`. Echo the **Summary** + the **Findings** sections to chat.

```markdown
# Repo-update freshness report — <YYYY-MM-DD>-<short-slug>

⚠️ **DRY RUN MODE** (or **APPLY**: <item>).
**Skill in DRAFT** — not approved for automated use.
For structural / broken-now checks, use `/repo-doctor`.

Scope: <full | category-keyword>
Generated: <YYYY-MM-DD HH:MM:SS local>
Network operations performed: <list, or "none — offline checks only">

## Summary

| Category | Status | Stale items |
|---|---|---|
| C1+C2. Canon freshness + outdated | ✓ \| ⚠ \| ✗ | <count> |
| C2. Research distillations | ✓ \| ⚠ \| ✗ | <count> |
| C2. External deps + system tools | ✓ \| ⚠ \| ✗ | <count> |
| C2. Anthropic / spec freshness | ✓ \| ⚠ \| ✗ | <count> |
| C2. Time-tracked invariants | ✓ \| ⚠ \| ✗ | <count> |
| C2. Schema migration | ✓ \| ⚠ \| ✗ | <count> |
| C6. Inventory drift | ✓ \| ⚠ \| ✗ | <count> |

**Totals:** N checks run, M stale items, K eligible for apply.

## Findings by check

### U1. Canon snapshot+refresh past cadence
**Rule source:** [canon/README.md](canon/README.md) §"volatility" table
**Detection:** parsed `canon/sources.yaml`, computed next_review_by per entry
**Findings:**
- `<slug>`: last_verified 2026-XX-XX, volatility fast (90d), past review by N days
  → Refresh with: `/repo-update apply --only=<slug>`

[... continue for each check that found anything ...]

## Recommended apply commands (operator-decided)

For each finding, choose to:
- **Refresh** — `/repo-update apply --only=<id>` (per-item, idempotent)
- **Defer** — note the finding, plan to address later
- **Accept** — false positive or intentional (e.g., `live-only` entry that's intentionally near review-by)

**This report does NOT execute refreshes.** Run `apply --only=<id>` explicitly per item.
```

## Constraints

- **Dry-run by default.** No writes outside `maintenance/updates/<report>.md` unless `apply --only=<id>` mode.
- **Network operations are explicit.** Surface "this check requires network" before any HEAD-probe / WebFetch / gh-api call. If operator hasn't opted in, skip network checks and note in report.
- **Bulk-apply forbidden in DRAFT.** Refuse `apply --all`.
- **No cross-zone work.** Do not invoke `/repo-doctor` checks here. If brokenness surfaces, report it and recommend operator run `/repo-doctor`.
- **No model self-upgrade.** Do not change agent `model:` pinning even on operator command — that's a deliberate architectural decision that belongs in a session, not an update.
- **Banner at top and bottom of chat output.** Non-negotiable.

## When the input is ambiguous

- `/repo-update` (no args) → run full report (all categories, dry-run).
- `/repo-update <category-keyword>` → match against `canon`, `research`, `deps`, `external`, `inventories`; run only matching category.
- `/repo-update apply --only=<id>` → APPLY mode for ONE item. Confirm with operator before any write.
- `/repo-update apply --all` → REFUSE in DRAFT.
- `/repo-update help` → list category keywords + apply syntax without running.

## How this skill evolves

When the repo gains a new updateable primitive:
- Categorize it (C1-C6 per industry taxonomy).
- Add a row to the appropriate check table above, citing the **canonical rule source** (where the rule lives — never encode the rule here).
- Decide the action available: informational / C3-apply / C4-apply (with contract warning) / C6-regenerate.

When a check becomes obsolete:
- Mark the row "RETIRED" with date and reason.
- Move terminology-retirement context to `/repo-doctor`'s audit-history table (broken-state lookup), not here.

## After running

1. The report is written to `maintenance/updates/<YYYY-MM-DD>-<short-slug>.md`.
2. The chat output ends with the DRY RUN / APPLY banner.
3. The operator decides per-item: refresh / defer / accept.
4. **You do not bulk-apply.** Every refresh is per-item, per explicit operator approval.
