# Synthesis — format-only state-transition gate

## Classifier label and alternative
- **Primary:** `new` (a capability the lab does not yet have).
- **Alternative:** `extend` — would become primary if the gate is treated as mechanical enforcement of the README's already-defined lifecycle, not as a new artifact with its own per-transition schema. The synthesis below adopts the **extend posture**: schema lives in the README; gate is a thin reader.

## Reframe (Revision 2 — restored after loop 1 replan)
Design a gate the operator can use **on day 1**, format-only, that does not require flipping any existing contract in the lab. The gate is a non-blocking warning surface on the existing manual-edit flow, not a replacement for it. (Revision 1 had drifted to "audit first, defer the gate" — the panel rejected this as non-responsive to the user's framing.)

## Reference-class forecast (from outside-view distillation)
Class: self-imposed personal-workflow validators on a small markdown corpus, single operator, no external accountability. Estimated base rate of sustained adoption past 6 months: **15–30%**. Modal failure mode: **lifecycle spec drift** (validator lags operator's actual entry template; false positives erode trust until validator is bypassed or removed). Lift conditions: pin invocation surface that doesn't depend on memory, co-locate spec and validator (one source of truth), accept lifecycle collapse as an expected revision rather than a failure.

The synthesized recommendation is at or slightly above the base rate because it satisfies one lift condition (schema and validator share one source — the README) and partially satisfies the second (invocation is at the moment of advancement, when operator/AI attention is on the entry).

## Canon passages (supporting and contradicting)
- **Supporting (SRE 2016, Ch. 26):** "validators that catch nothing get abandoned" — favors a gate that fires at advancement (where it has work to do), not a periodic audit (where it may sit idle).
- **Supporting (Cockburn, ports-and-adapters):** the slash command is a port for the lab's lifecycle — adapter (markdown table parsing) is replaceable behind the port.
- **Contradicting (Anthropic 2024, "simplest solution possible"):** an 8-state lifecycle validator may be over-engineering for a 22-entry corpus. Addressed by warning-only posture (no enforcement cost) and schema-in-README (zero new files).
- **Contradicting (SRE 2016 internal tension):** "When too strict, even simple, appropriate changes cause validation to fail. As a result, engineers abandon data validation altogether." Addressed by tolerant regex and warning-only posture (false positives become friction, not corruption).
- **Contradicting (Anthropic 2025, folder-as-state):** the state could be encoded by file location instead of a state-table column. Acknowledged but not adopted — preserved as a future-entry candidate if the table-based approach proves load-bearingly wrong.
- **Bias flags carried forward:** canon over-represents Anthropic-authored sources (treat their convergence as one voice). Several relevant traditions (Postel/IETF, Wlaschin/illegal-states-unrepresentable, BPMN/statecharts, personal-tool adoption literature) have no canon entry.

## Scope-map summary
- **Conflict (3 live, all decided in v2):** README's "no automation" sentence vs gate existence — *resolved by warning-only posture; the sentence stays exactly as written.* `/upgrade` vs `/advance-upgrade` vs `/upgrade advance` — *resolved as subcommand of `/upgrade`.* Lifecycle as descriptive vs prescriptive — *resolved as descriptive (gate is advisory).*
- **Replace (1):** none. v2 deliberately replaces nothing.
- **Extend (3):** the 8-state lifecycle (preserved with reason: it's the contract being enforced); per-tier folders (orthogonal axis); `/upgrade` slash command (gains an `advance` subcommand).
- **No existing agent does any part of this job.** The gate is a script (or shell-style logic inside the slash command), not an LLM agent.

## Frame-level challenge and how the recommendation addresses it
The frame-challenger surfaced four challenges. The synthesis position on each:

1. **Audit-first reframe (build the audit, defer the gate):** **rejected** by the panel as non-responsive. Loop 1 adopted it; loop 2 backed out. The synthesized gate is the audit (run at advancement time), not separate from it.
2. **Falsifier (zero entries past `created` → modal failure is disuse):** **honestly named.** v2 assumption #1 commits the gate to dying of disuse if no entries advance. That is the correct fate. Cost is zero; learning value is real.
3. **Lifecycle collapse to 3-5 states:** **deferred but not dismissed.** Schema lives in the README; if the operator decides to collapse, the table is updated and the gate follows. No lifecycle change is precondition for shipping.
4. **Folder-as-state alternative:** **acknowledged, not adopted.** Documented for a future entry.

## Post-critique recommendation (labeled)

**RECOMMENDATION:** Ship a warning-only state-transition gate as a subcommand of `/upgrade`, with the schema living in a new advisory table in `upgrades/README.md`. Day-1 deliverable; no phased rollout; no replacement of the existing manual-edit advancement path.

Concrete shape:

1. **One new advisory table in `upgrades/README.md`** (~15 lines), inserted after the existing state-lifecycle table. The table names, for each state past `🌱 created`, the required body element and the regex tolerance. This table is the single source of truth.

2. **Subcommand `/upgrade advance <entry-path> <new-state>`** in `.claude/commands/upgrade.md`. When invoked: parses the README's required-elements table, reads the entry, detects the entry's current state from the rightmost-filled column (and explicitly reports its detection so mis-detections are visible), checks the entry body for each required element using the table's regex, and prints a one-screen line-cited report. The command is non-blocking — it warns and suggests; the operator decides whether to proceed.

3. **Optional `--apply` flag** that writes the date to the state table on the operator's behalf only if the check passes. **Pre-merge requirement (operations critic):** `--apply` must either refuse on a dirty working tree, or print `git diff --stat` before writing. Manual editing remains the documented default; `--apply` is a convenience.

4. **One CLAUDE.md sentence:** *"When advancing a lab entry's state, prefer `/upgrade advance <path> <state>` over direct table editing — it surfaces missing required sections."*

5. **Improvements before merge (architecture critic, non-blocking):**
   - HTML-comment marker in the README's new schema section noting the table is machine-read.
   - One sentence acknowledging the schema-as-types alternative (gate at entry-creation via templating) as a deliberately not-adopted path.
   - One sentence naming the new cross-directory coupling (`.claude/commands/upgrade.md` → `upgrades/README.md`).

6. **Cheap operations enhancement (non-blocking, recommended):** when `/upgrade advance` runs, append one line to a single log file. Lets the operator detect silent disuse via `wc -l` vs `git log` count of state-table changes. Adds one file but bounded value, no new contract.

**Total committed surface:** ~15 lines of README, ~80–120 lines of slash-command logic, one CLAUDE.md sentence, three pre-merge improvements above. No new files for the operator. No retiring of any existing path. No new agent.

## At least three named uncertainties

1. **Whether the operator (and AI) will invoke `/upgrade advance` rather than edit the table directly.** Modal failure mode per outside-view. v2 commits to "dies of disuse" as honest fate, but no liveness signal exists without the optional invocation log.
2. **Whether the required-elements schema in the README is roughly right.** First few real advancements will reveal regex tolerance gaps. The README-as-source-of-truth design makes revision cheap, but the *first* schema is a guess — there's no labeled validation set.
3. **Whether warning-only carries enough signal to be acted on.** Could become theatre if AI sessions systematically advance past warnings. v2 acknowledges this; escalation path stays open (CLAUDE.md instruction "if `/upgrade advance` reports missing elements, do not advance" can be added later without contract change).
4. **Whether subcommand-of-`/upgrade` is the right factoring.** Verb-overload concern from architecture critic. Reversible — splitting back to `/upgrade-advance` later is mechanically easy.
5. **Whether the schema-in-README pattern survives the first README rewrite.** Loud failure (script errors) over silent drift, but if a future README revision changes table shape without the operator noticing, the gate breaks.

## The cheapest experiment that would reduce the biggest uncertainty

**Uncertainty being reduced:** #1 (operator/AI invocation rate) — modal failure mode per outside-view.

**Experiment:** Implement the gate end-to-end in one session (estimated 2–3 hours: ~15 lines README, ~100 lines slash command, ~1 line CLAUDE.md). Then, **deliberately advance one of the existing 22 entries** (the `rnd-lab` entry — it's already implemented in the sense that the lab exists). Run `/upgrade advance upgrades/no-brainer/2026-04-26-rnd-lab.md "💎 value-proved"`. Observe:
   - Does the schema's required regex for `💎 value-proved` (a session-id reference + a "value/evidence/outcome" heading) actually fire correctly?
   - Does the warning name what's missing in a way that suggests a concrete next edit, or is it vague?
   - How long does the entire flow take from the operator's seat?

If the experiment takes <30 seconds and the warning is actionable, uncertainty #2 (schema correctness) is partly retired and uncertainty #3 (signal carries) gets first data. If the warning is vague or the flow is annoying, the gate is killed before it ships to a second entry.

**Classification per the experiment-running-branch entry:** `runnable-here` and within budget. The script can be written and tested in a single session; the experiment costs <20 agent-calls.

## Symmetry worth naming (operations critic)

The blast radius of this gate failing equals the blast radius of not having built the gate at all. This is a **fails-to-safe** change: at worst it dies of disuse and the lab continues exactly as it does today. Worth saying out loud — most upgrade entries do not have this property.
