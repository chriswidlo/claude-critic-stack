# Candidate v2 — format-only state-transition gate (warning, derived schema, day-1)

## Position

**Ship a warning-only gate on day 1 as a subcommand of the existing `/upgrade` command.** The gate reads its schema from a new advisory table added to `upgrades/README.md` (not from grep patterns hidden in a script). It produces a one-screen warning when the operator (or an AI agent) asks to advance an entry whose body is missing the required sections for the new state. It does not block. It does not retire the manual-edit flow. It does not introduce a new file the operator has to remember.

The audit-first phasing of v1 is discarded. The lab's existing contract (manual advancement, descriptive-not-prescriptive lifecycle) is preserved. The new affordance is *one warning* at the moment of advancement.

## What ships on day 1

### 1. README addition — the schema table (~15 lines of markdown)

A new table inserted in `upgrades/README.md` immediately after the existing state-lifecycle table. Single source of truth for what each state requires:

```markdown
### Required body elements per state

| Required-by-state | Element the body must contain | Tolerance |
|---|---|---|
| 🔬 spiked | a heading matching `/spike|tried|probe|explored/i` | section can be empty; presence of heading is enough |
| 📋 prepared | a heading matching `/plan|next steps|implementation plan/i` | as above |
| ✅ accepted | line containing `accepted by` and a date | freeform |
| ⚙️ run-through-repo | a session-id reference (`<YYYY-MM-DD>-<slug>`) | matches the session-artifacts directory naming |
| 🔨 implemented | at least one git short-SHA (`[a-f0-9]{7,40}`) OR `implemented_by:` field in meta | either is sufficient |
| 💎 value-proved | at least one session-id reference + a heading matching `/value|evidence|outcome/i` | both required |
| 🏁 completed | a heading matching `/closure|closed|completed/i` and a date | freeform |

The gate (`/upgrade advance`) reads this table to know what to check. To change the schema, edit this table — the gate updates next run. The lifecycle is descriptive (manual edit still allowed); this table is the gate's reference, not a prescriptive contract.
```

The schema lives in the README. Architecture critic's load-bearing objection (schema-in-script duplicates README) is addressed: there is one schema, in one place.

### 2. Subcommand of `/upgrade` — `/upgrade advance <entry-path> <new-state>`

Extension to `.claude/commands/upgrade.md`. When the slash command is invoked with `advance` as first argument:

1. Reads `upgrades/README.md` and parses the *Required body elements per state* table into a tiny in-memory schema.
2. Reads the entry at `<entry-path>`.
3. Determines the entry's current state (rightmost-filled column in the state table) — and **explicitly notes if that detection is ambiguous** (multiple non-em-dash cells separated by gaps; per the architecture critic's invariant #1).
4. Looks up `<new-state>` in the schema; checks the entry body for each required element using tolerant regex from the table.
5. Produces a one-screen report (stdout) in this exact shape:

```
Entry: upgrades/normal/<file>.md
Current state (detected): 🔬 spiked
Requested advance to:    📋 prepared

Schema for 📋 prepared (from README §Required body elements per state):
  ✓ heading matching /plan|next steps|implementation plan/i  →  found at line 47 ("## Plan")

All required elements present. Suggested edit:
  Replace state-table cell:  prepared | —   →   prepared | 2026-04-26

Apply this edit yourself in the file, OR run with `--apply` to have the slash command write it.
```

Or, when something is missing:

```
Entry: upgrades/normal/<file>.md
Current state (detected): 🔬 spiked
Requested advance to:    📋 prepared

Schema for 📋 prepared (from README §Required body elements per state):
  ✗ heading matching /plan|next steps|implementation plan/i  →  not found

Missing 1 required element. Advance is allowed (manual edit always permitted), but
the lab's lifecycle contract says 📋 prepared entries should contain a Plan section.
Suggested fix:
  Add a `## Plan` section to the entry body before advancing.
```

The warning names the missing element with the exact regex it looked for and the exact section heading it suggests. Vague warnings get ignored; specific warnings get acted on.

### 3. Optional `--apply` flag

If the check passes, `/upgrade advance ... --apply` writes the date to the state table on the operator's behalf. If the check fails, `--apply` refuses with the warning above. The flag is a convenience, not a requirement; manual editing remains the default path documented in the README. The README's "manual act" sentence stays exactly as written.

## What does NOT ship

| Deliberately omitted | Why |
|---|---|
| `bin/audit-upgrades.sh` standalone script | Folded into the slash command. One code path, not two. (Addresses architecture critic's audit-vs-gate-shouldn't-share-schema by having only the gate.) |
| `AUDIT-LOG.md` periodic file | Operations critic: invocation-surface that depends on memory is the modal failure mode. The warning IS the instrument, and it fires *at the moment of advancement* — exactly when the operator's attention is on the entry. |
| Pre-commit hook | Outside-view: high-bypass surface for solo repos. |
| `/advance-upgrade` as new sibling command | Product critic: splits operator mental model. Subcommand of `/upgrade` keeps "the lab has one command" invariant. |
| Required hand-labeling of 22 entries | A warning-only gate makes no claim of accuracy — false positives are friction, not corruption. Labeling is required only if we claim a measurement; we don't. |
| Phased rollout | Product critic: deferred contract decisions get more expensive. Ship the contract on day 1; iterate on the schema (in the README table) as needed. |
| Read-the-README-as-prose parser | The README's state-lifecycle and the new required-elements table are already markdown tables; the script parses tables, not prose. |

## Named tradeoffs

| Trade | Cost paid | Cost avoided |
|---|---|---|
| Warning-only, not blocking | A determined operator (or AI) can ignore the warning and advance anyway. The gate is theatre if ignored. | Conflict with README's "descriptive-not-prescriptive" stance. Conflict with operator's stated value of zero-ceremony advancement. Conflict with the bypass-by-default failure mode (no bypass needed if it doesn't block). |
| Schema lives in the README | Editing the schema requires editing the README — a slightly heavier touch than editing a config file. | Two-source-of-truth duplication (the architecture critic's load-bearing objection). |
| Subcommand of `/upgrade`, not a new command | `/upgrade` now does two things (capture, advance). Cognitive coupling. | Splitting the operator's mental model across two slash commands. The lab has one command for one set of operations. |
| Run on demand at advancement, not on schedule | Advances that happen by direct file edit (no slash-command call) are not gated at all. | A scheduled/cron audit that produces an artifact the operator may or may not read — the modal failure mode operations critic identified. The gate fires *at the moment the operator is already paying attention*. |
| Depends on the rightmost-filled-column current-state heuristic | Per architecture critic invariant #1: backfilled middle cells confuse it. | Re-modeling state advancement as a transaction log rather than a date row — much larger change. We accept the heuristic and have the script *report* its detection so the operator catches mis-detections. |

## Named assumptions (would flip the recommendation if wrong)

1. **The operator (and AI) will invoke `/upgrade advance` rather than edit the table directly.** If muscle memory is "open file, type date," the gate never fires. Mitigation: when an AI is implementing a state advancement, instruct it (via CLAUDE.md update — small) to use `/upgrade advance`. The operator can still edit by hand. If neither happens after 4 weeks of advancements, the assumption is wrong and the gate dies of disuse, which is the correct fate.
2. **The required-elements schema in the README is roughly right.** If, after a few real advancements, the operator finds themselves disagreeing with the schema's regex matches, the schema needs revision *in the README*, not the script. The single source of truth is load-bearing exactly here: "the gate is wrong" and "the README is wrong" become the same statement.
3. **A warning-only gate carries enough signal to be acted on.** If operators systematically ignore warnings ("yes I see it's missing the section, advancing anyway"), the gate is theatre. Mitigation: if the warning is ignored ≥ 3 times across a month, that's data — the schema is too strict, or the section is genuinely optional, or the lifecycle state is muddled. Each ignore informs the next schema revision.
4. **Tolerant regex is more useful than strict regex for this corpus.** Same as v1's assumption #4. If the regex is too tolerant (passes everything) the warnings have no information; too strict (rejects normal prose) and warnings are noise. The regex lives in the README so the operator can tune it directly when they encounter a false fire.

## Named ways this could be wrong

1. **The architecture critic's "audit-and-gate-conflated" objection may still apply, in a softer form.** The candidate has only a gate now (no separate audit), but the gate doubles as a discovery surface (running it across many entries reveals corpus state). The conflation is not eliminated, just reduced from two artifacts to one. If this matters in practice, a future entry can split them.
2. **The schema-in-README solves duplication but introduces a new dependency: the README must remain a parseable table.** If a future README revision shapes the table differently, the script breaks. We accept loud failure (script errors) over silent drift, but the operator must know "the README's state table is now machine-read."
3. **The product critic's "responsive on day 1" objection is satisfied by the warning, but only weakly.** A warning that is ignored as easily as a manual edit might not feel like a gate to the operator who asked for "AI doesn't drift." If the operator wanted a hard block, this candidate is still under-responsive — and the operator should say so. The candidate explicitly cannot promise "AI doesn't drift" because no surface in a solo repo can guarantee that without becoming a high-bypass surface (operations critic's secondary frame objection).
4. **Subcommand-of-`/upgrade` may be the wrong factoring.** `/upgrade` was designed for capture; folding `advance` into it may overload the verb. A small `/upgrade help` listing all subcommands becomes necessary. If it gets messy, splitting back into `/upgrade-advance` is a reversible decision.

## How the loop-1 lens objections were addressed in v2

| Critic | Loop-1 objection | v2 response |
|---|---|---|
| architecture | Two sources of truth (README prose + script grep). | Schema lives in a README table; script parses the table. One source. |
| architecture | Audit and gate share schema dishonestly. | No separate audit. Only the gate. |
| architecture | Rightmost-filled-column invariant is unstated and load-bearing. | The script reports its detected current-state explicitly so mis-detection is visible. Named as an explicit limitation in tradeoffs. |
| operations | Phase 1 has no measurement instrument. | No Phase 1. The gate runs at advancement time; the warning IS the measurement, fired when the operator's attention is on the entry. |
| operations | AUDIT-LOG.md is unstructured prose. | No AUDIT-LOG.md. |
| operations | Phase 2 rollback is dishonest. | No Phase 2. Rollback = remove the subcommand. Manual edit still works. |
| operations | No non-bypassable surface for solo operator. | Acknowledged in "ways this could be wrong" #3. Warning-only is the honest shape; pretending otherwise lies to the operator. |
| product | Day-1 ships zero gate-shaped affordance. | Day-1 ships the gate. It warns, it doesn't block, it works the moment it's installed. |
| product | Deferred contract decision. | No deferral. Contract change is one new advisory README table — additive, doesn't flip any existing sentence. |
| product | Operator asked for a gate, candidate replied "audit first." | Candidate replies with a gate. |

## Frame-level objection from challenges.md — partially addressed

The challenger's audit-first reframe was the load-bearing objection in challenges.md. v2 explicitly does NOT adopt it. The reasoning: the panel collectively identified that the audit-first reframe is non-responsive to the user's framing, and that the falsifier the challenger named (0 entries past `created`) is itself addressable by the gate (when an entry advances, the gate fires; if no entry ever advances, the gate has zero cost).

The challenger's secondary points are absorbed:
- **Folder-as-state alternative:** still not adopted; documented as a future-entry candidate if the state-table approach proves load-bearingly wrong.
- **Targeted gating (only 🔨 and 💎):** v2 gates all 7 transitions but with cheap regexes; cost is the schema table, which is small. If false-positive rate is high on early states (🔬, 📋), the regex can be loosened to "any section heading at all" — effectively making those transitions ungated in practice.
- **Lifecycle collapse to 3-5 states:** orthogonal to the gate. If the operator decides to collapse, the README table is updated and the gate follows.

## Minimum committed surface

- ~15 lines added to `upgrades/README.md` (one new advisory table).
- ~80–120 lines added to `.claude/commands/upgrade.md` (the `advance` subcommand handler — bash or Python, parses one markdown table, runs regexes, prints a report).
- One CLAUDE.md sentence: "*When advancing a lab entry's state, prefer `/upgrade advance <path> <state>` over direct table editing — it surfaces missing required sections.*"

That's it. No new files. No new artifacts. No phased rollout. The lab's contract is preserved; the gate is additive and advisory.
