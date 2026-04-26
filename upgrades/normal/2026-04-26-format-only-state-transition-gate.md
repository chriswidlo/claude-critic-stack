# Format-only state-transition gate for upgrade entries

| Field | Value |
|---|---|
| 📌 **title** | Format-only state-transition gate for upgrade entries |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The lab's eight-state lifecycle (🌱 → 🏁) is currently advanced by hand-editing the state-table date. Nothing checks that the entry actually meets the conditions for the new state. As the lab fills, AI agents will handle most of these transitions, and without a structural gate the entries will drift in format and the state column will lose meaning — `🔨 implemented` could be claimed against an entry whose body has no commit reference. The operator named the gap directly: *"a gate so the AI that handles upgrades doesn't get confused and all upgrades follow the same pattern and do not drift off."* |
| 💡 **essence** | A **format-only, warning-only** validator invoked at advancement time as a subcommand of `/upgrade`. Reads its schema from a table in `upgrades/README.md` (single source of truth), checks the entry body for the required regex element of the requested new state, and prints a one-screen line-cited report. It does **not** evaluate idea quality, context, or judgment. It does **not** block the advancement — the lab's lifecycle remains descriptive, and manual editing of the state table is always allowed. The warning's only job is to name what's missing at the moment the operator (or AI) is paying attention to the entry. |
| 🚀 **upgrade** | False advancement (claiming `🔨 implemented` against an entry with no commit reference) becomes visible at the moment of advancement, not weeks later. AI agents handling upgrades get a deterministic, opt-in surface that says "this is what the lab's lifecycle expects for state X." Format consistency emerges from the warning being specific (regex + suggested heading text) rather than from enforcement. **Fails to safe:** if the gate is ignored or never invoked, the lab continues exactly as it does today. |
| 🏷️ **tags** | lab, lifecycle, gate, format-validation, drift-prevention |
| 🔗 **relates_to** | profound/2026-04-26-subagents-claim-writes-not-on-disk |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | 2026-04-26 | — | — | 2026-04-26 | — | — | — |

> **Update history (most recent first).** State table reflects sessions that touched this entry; the body has been revised since `🌱 created` to incorporate v2 design (warning-only, schema-in-README, subcommand factoring) following the workflow run. The original v1 design (separate script, blocking gate, audit-first phasing) was rejected on loop 1 of the critic-panel; v2 was approved on loop 2. See `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/synthesis.md` for the full record.

## Table of contents

- [Spike](#spike)
- [What ships — the warning gate](#what-ships--the-warning-gate)
- [The schema — single source of truth in the README](#the-schema--single-source-of-truth-in-the-readme)
- [What was deliberately NOT built (and why)](#what-was-deliberately-not-built-and-why)
- [What is deferred until git strategy lands](#what-is-deferred-until-git-strategy-lands)
- [Open questions](#open-questions)

## Spike

A working prototype was built and run against three real entries in session `2026-04-26-format-only-state-transition-gate` (~25 minutes end-to-end). Artifacts:

- Schema table added to `upgrades/README.md` §"Required body elements per state".
- Prototype script at `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py` (~110 lines Python, read-only).
- Experiment report at `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/experiment-report.md`.

**Findings (summary):** the schema-in-README pattern works — a regex tuning was made in the README *before* the first run, and the script picked it up next invocation. Warning messages are specific and actionable (~2ms per check). Two real flaws surfaced in the spike: (a) markdown-table parser dropped rows whose regex contained `\|` — caught and fixed in 5 minutes; (b) the `⚙️ run-through-repo` regex matches any session-id-shaped string in the body, including `relates_to:` cross-references, producing a false positive on the rnd-lab entry. The first is fixed; the second is documented and pending tightening when productionized.

The spike validated v2 design without falsifying any of its assumptions. Productionization (slash-command integration, `--apply` flag, invocation log) is deferred until git strategy lands and CLAUDE.md/`.claude/commands/` changes are in scope.

## What ships — the warning gate

A subcommand of the existing `/upgrade` slash command:

```
/upgrade advance <entry-path> <new-state>
```

When invoked it (1) parses the schema table from `upgrades/README.md`, (2) reads the entry file, (3) detects the entry's current state from the rightmost-filled cell in the state table — and explicitly reports that detection, so mis-detections (e.g., backfilled middle cells) are visible, (4) looks up the requested new state in the schema, and (5) checks the entry body for the required regex element.

Output is a one-screen report naming what was looked for, what was matched (or missed), and a suggested next edit. Sample (passing case, from the spike run):

```
Schema for 🔬 spiked (from upgrades/README.md):
  element: A heading naming the spike work (e.g. ## Spike, ## What I tried, ## Probe).
  regex:   ^#+\s+.*(spike|tried|probe|explored)

  ✓ matched at line 31: '## Spike'

All required elements present.
Suggested edit: in the state table, replace '—' under '🔬 spiked'
with today's date (2026-04-26).
```

**Warns; does not block.** The lab's lifecycle remains descriptive — manual edit of the state table is always allowed. The warning is the value: it names the missing element with the regex that looked for it and the heading text that would satisfy it.

The state-table edit happens by hand (preserves the README's "manual act" contract). A future `--apply` flag is sketched but deliberately not built yet (see *What is deferred*).

## The schema — single source of truth in the README

The required-elements schema lives in `upgrades/README.md` under §"Required body elements per state." One row per state past `🌱 created`; the regex is visible in the markdown. To change what a state requires, edit the README — the gate updates next run.

This pattern (markdown-table-as-config) avoids the dominant failure mode the architecture critic flagged on loop 1: two sources of truth (README prose + script grep patterns) drifting apart. With schema-in-README, the gate cannot be wrong without the README also being wrong. They are the same statement.

Tunability was demonstrated in the spike: the `💎 value-proved` regex was tightened in the README (from `value|evidence|outcome` to `value (proved|evidence)|outcome|demonstrated`) before the first run, to avoid matching an unrelated heading "Why organize by **value**-tier" in the rnd-lab entry. The script picked up the tightening on next invocation. No script edit; no second source of truth to keep in sync.

## What was deliberately NOT built (and why)

| Omitted | Reason |
|---|---|
| Pre-commit git hook | Outside-view distillation: pre-commit hooks on solo repos are a high-bypass surface. Operators learn to `--no-verify` within weeks. |
| Standalone audit script (separate from gate) | Folded into the gate. One code path. The audit is the gate, run at advancement time — not periodically. |
| `AUDIT-LOG.md` periodic file | Operations critic loop 1: any tool whose invocation depends on operator memory becomes the modal failure mode (bypass-by-default). The warning IS the instrument; it fires *at the moment of advancement* when the operator is already paying attention. |
| `/advance-upgrade` as a sibling command | Product critic loop 1: splits operator mental model. Subcommand of `/upgrade` keeps "the lab has one command for one set of operations." |
| Hand-labeled validation set across 22 entries | Warning-only makes no accuracy claim. False positives are friction, not corruption. The labeling cost was demanded by the operations critic in loop 1 *as a precondition for an audit-mode tool that claimed measurement* — v2 doesn't claim measurement, so the labeling isn't required. |
| Phased rollout / "Phase 2" of the gate | Product critic loop 1: deferred contract decisions get more expensive. Day-1 ships the contract. The schema can be tuned in the README as evidence accumulates; the slash command can iterate; no phasing required. |
| Seven separate per-transition schemas with compound conditions | One regex per state for v1 simplicity. If a state genuinely needs an AND across two requirements (the spike's `💎 value-proved` originally proposed both a session-id AND a heading), the schema-in-README pattern can express it via two rows; parser extension is small. Deferred until first real need. |

## What is deferred until git strategy lands

These are real, named, and explicitly future-state — not lost:

- **`--apply` flag.** Writes the state-table date on the operator's behalf if the gate passes. Pre-merge condition from the operations critic: must either refuse on a dirty working tree OR show `git diff --stat` before writing. Both depend on git conventions that don't yet exist in this repo (see LEDGER #16).
- **Slash-command integration.** The spike is a standalone Python script under `.claude/session-artifacts/`. Productionizing it as `/upgrade advance` requires editing `.claude/commands/upgrade.md` — out of scope for the spike per session constraints.
- **CLAUDE.md sentence.** *"When advancing a lab entry's state, prefer `/upgrade advance <path> <state>` over direct table editing — it surfaces missing required sections."* Deferred with the slash-command edit.
- **Invocation log.** Operations critic loop 2's optional improvement: append one line per invocation to a tracked log file so the operator can detect silent disuse via `wc -l` vs git history. Cheap; useful; deferred until the gate is productionized.
- **Loud failure on schema-row dropout.** The spike silently drops schema rows whose markdown is malformed. Architecture critic loop 2's "loud failure over silent drift." Productionization should error if any row fails to parse.

## Open questions

- **Should the rightmost-filled-column heuristic be replaced by a transition log?** Backfilling a middle cell (which the README explicitly invites) confuses current-state detection. The script reports its detection so mis-detections are visible, but the heuristic is fragile.
- **Should the gate emit a `limitations.md` entry when it warns?** Would create a cross-system audit trail of attempted-but-flagged transitions. Pairs with the limitations.md upgrade entry (LEDGER #2).
- **Does the schema need compound conditions (AND across multiple regexes per state)?** v1 schema uses one regex per state. The spike worked. If real entries surface cases where a state genuinely requires two things in the body, the parser can be extended to handle multi-regex rows.
- **How does the gate interact with the workflow-overdesigns counter-bias entry (LEDGER #6)?** If "could this be 10% of itself" becomes a pre-synthesis check, the gate's existence is itself testable against that check (10% of the gate is the warning script — already what we have).
- **Is `⚙️ run-through-repo` the right state to gate at all?** The spike surfaced that the regex matches any session-id-shaped string in `relates_to:` references, false-passing rnd-lab. Tightening the regex to verify the session-id directory exists is the cheap fix; rethinking the state is the deeper one. Captured as a separate upgrade entry.
