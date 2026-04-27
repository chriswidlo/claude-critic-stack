# Candidate recommendation — Step-13 session ledger

## Position

Ship a Step-13 ledger as a *paste-and-fill template* rendered by the orchestrator into `.claude/session-artifacts/<id>/ledger.md` after synthesis. The ledger format lives in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) (added section: *Ledger schema*) — one source of truth, grep-friendly markdown table, ratios shown derived (math visible), warnings include a suggested response. Synthesis (Step 12) gains a final one-line citation: *"Ledger: <counts summary>; <warnings or 'no warnings'>"*. CLAUDE.md gains a Step 13 section. No hook plumbing in this entry — explicit dependency note for entry #14.

## Concrete shape

### A. New section in CLAUDE.md after step 12

```markdown
13. **Ledger.** Write `session-artifacts/<id>/ledger.md` from the paste-and-fill template documented in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md). The ledger records counts (agent calls, artifacts, loops), shows derived ratios with the math visible, and surfaces threshold warnings with suggested responses. The final line of synthesis cites the ledger summary inline so the operator re-encounters the signal at the point of attention.
```

Plus: extend the "Things you must not do" list with: *"Do not skip the ledger. The synthesis is not complete until ledger.md exists and synthesis.md cites it."*

### B. New section in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)

A `## Ledger schema` section defining the paste-and-fill template:

```markdown
# Session ledger — <session-id>

## Counts
| Category | Count | Source |
|---|---|---|
| Agent calls (subagent invocations) | <N> | count of files in distillations/ minus -raw suffix |
| Artifacts produced (markdown files) | <N> | wc -l-style count of `.md` files in this session dir |
| Critic-panel loops | <N> | from decision-log.md |
| Loop cap reached | true \| false | from decision-log.md ("Loops used: N/2") |
| Decisions in synthesis | <N> | count of explicit recommendations in synthesis.md |

## Derived ratios
- Agent-calls per decision: <N> / <D> = <ratio>
- Artifacts per decision: <N> / <D> = <ratio>
- Loops to convergence: <N>/2 (cap=2)

## Warnings
- ⚠️ if agent-calls / decision > 10: "consider whether the workflow produced more analysis than action"
- ⚠️ if artifacts / decision > 8: "consider whether documentation is exceeding decisions"
- ⚠️ if loops cap reached: "candidate needed maximum rework; first-pass framing was off"
- (omit warnings list entirely if none triggered)

## Notes
<free-form prose. aggregators ignore this section.>
```

The `## Counts`, `## Derived ratios`, and `## Warnings` headings are load-bearing — aggregators key on them. `## Notes` is the orchestrator's free-form spillover so the table-rows stay clean.

Schema documents:
- The thresholds (10 / 8 / 2) live in this README only — change once, every future ledger picks up the new threshold.
- "Decision" is defined: *the explicit recommendation in synthesis, plus any explicitly-named alternatives the operator must choose between.*
- "Agent call" is defined: *one invocation of a subagent via the Agent/Task tool, counted at the orchestrator level. Sub-tool calls inside an agent (Read, WebFetch) do not count.*

### C. Synthesis citation pattern

The last line of every synthesis.md is the ledger summary, in this exact form:

```
Ledger: agent-calls=<N>, artifacts=<N>, loops=<N>/2; warnings: <list or "none">.
```

This makes the warnings load-bearing in the operator-facing artifact without forcing the operator to open ledger.md.

### D. Example ledger

A worked example shipped at [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md), derived from the format-only-state-transition-gate session (which has 20 artifacts, 2 loops, ~14 agent calls). Demonstrates the schema with real numbers and shows how the warnings render.

### E. Explicit non-goals (deliberately not shipped)

- No script that auto-generates the ledger. Manual paste-and-fill by the orchestrator. Hook automation belongs to #14.
- No cross-session aggregator script. The ledger format is *designed for* aggregation; the aggregator itself is a separate future entry.
- No ratio-stored-as-data. Counts only; ratios shown derived.
- No threshold tuning automation. Thresholds change by editing one README section.

## Named tradeoffs

1. **Schema rigidity vs aggregation value.** The paste-and-fill template constrains the orchestrator's authorship, which feels mechanical for a workflow that prides itself on judgment. The trade is that aggregation-readiness compounds with every session; the per-session friction is small.

2. **Inline citation in synthesis vs synthesis purity.** Adding a "Ledger:" line at the end of synthesis dilutes synthesis as "the considered recommendation" and makes it part-receipt. The trade is that without inline citation the warnings are wallpaper.

3. **Three ratios vs N ratios.** Three may not capture all over-elaboration modes (Ashby's law concern from canon). Adding ratios over time is cheap *if* the schema is in one place; resisting addition keeps signal-to-noise high.

4. **Manual authorship vs hook automation now.** Hooking PostToolUse to count agent calls automatically would eliminate authorship drift and would be more reliable. The cost is plumbing complexity that belongs to #14. Doing it now would conflate two entries.

## Named assumptions (any of these wrong → recommendation flips)

1. **The orchestrator will reliably write ledger.md every session.** If the orchestrator skips it under deadline pressure or context exhaustion, the ledger is dead. *Flip:* if real sessions show >30% skip rate, replace manual authorship with a hook (sooner) or remove the step entirely.
2. **The synthesis citation pattern will not be hand-waved.** If orchestrators write "Ledger: see ledger.md" instead of inlining the counts and warnings, the re-encounter surface fails. *Flip:* tighten the CLAUDE.md spec to require literal counts in the citation, or pre-render via hook.
3. **The "decision" definition holds across session shapes.** Some sessions will have 0 explicit recommendations (a `quick take` bypass) and produce division-by-zero. *Flip:* either skip the ledger for bypassed sessions (most likely), or define a degenerate-case format ("decisions=0; ratios=N/A").
4. **Cross-session aggregation will eventually happen.** If no aggregator ever ships, the per-session schema rigidity is pure cost. *Flip:* relax the template to free-form prose; warnings inline only.
5. **Three ratios capture the modal failure.** If the real over-elaboration patterns are not captured by these three (e.g., the bug is "right amount of agents, wrong agents"), the signal is silent on the actual problem. *Flip:* add a fourth ratio (e.g., agent-diversity-index) once a real session reveals the gap.

## Named ways this could be wrong

- **Goodhart drift:** orchestrators game the ratios by skipping agents to keep the count low. The instructions explicitly forbid this, but instructions don't prevent it.
- **Schema bit-rot:** future CLAUDE.md edits change what step 12 outputs without updating step 13's "decision count" derivation. The two docs drift; the ratios become wrong silently.
- **Wallpaper outcome:** even with synthesis citation, the operator/AI ignore warnings because the threshold guesses are bad. The whole system becomes ceremonial after 5 sessions.
- **Conflation with entry #14:** if #14 ships hook-based ledger writes shortly after this entry, the manual authorship described here is immediately obsolete and the docs must be edited again. Worth saying out loud: this entry's design is *expected* to be partially superseded.

## Frame-level objection from challenges.md and how this addresses each

1. *"Inline-in-synthesis is enough; the file is overhead."* Addressed by **doing both**: file exists for aggregation; inline citation exists for re-encounter. Aggregation is the load-bearing reason for the file.
2. *"Workflow doesn't need self-instrumentation; operator does."* Addressed by labeling thresholds as starting heuristics, keeping warnings advisory, and putting threshold values in one place so the operator can tune them.
3. *"Manual orchestrator authorship will drift."* Addressed by paste-and-fill template (load-bearing headings, free-form Notes section quarantines drift).
4. *"Synthesis-as-terminus preservation prevents re-encounter."* Addressed by the synthesis citation pattern — ledger summary is the literal last line of synthesis.

## Dependency on entry #14

Entry #14 (hard-gates-as-harness-hooks) is in flight on a parallel worktree. If/when #14 ships hook-based per-step counters, this entry's "manual orchestrator authorship" becomes "orchestrator paste-and-fills from hook-emitted counts." That is a strict refinement, not a contract change — the schema remains the same; the *source* of the counts shifts from "orchestrator counts files in session dir" to "hooks emitted these counts during the session." Document the dependency in the entry body; do not block on it.
