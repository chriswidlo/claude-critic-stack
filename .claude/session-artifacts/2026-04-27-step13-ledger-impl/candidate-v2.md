# Candidate v2 — Step-13 session ledger

## What changed from v1
v2 absorbs the panel's pre-merge requirements (architecture #1+#2, operations #1+#2+#3, product #3). Architecture #3 (cross-link CLAUDE.md → schema) is folded in (cheap). Operations' optional fallback script is deferred. The frame, scope-map, and overall shape are unchanged.

## Position
Same as v1, with six tightenings.

## The schema in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)

Insert under the "Lifecycle" section, marked as load-bearing:

```markdown
## Ledger schema (load-bearing)

<!-- machine-read source for ledger.md schema. CLAUDE.md step 13 and any
     example ledgers refer to this section. do not change heading text
     ('## Counts', '## Derived ratios', '## Warnings', '## Notes') without
     also updating CLAUDE.md step 13 and the exemplar ledger. -->

Every non-bypassed session writes `<session-id>/ledger.md` from this template.
Counts are taken just before ledger.md is written; ledger.md does not count
itself. Aggregators key on the four headings below.

# Session ledger — <session-id>

## Counts
| Category | Count | Source of truth |
|---|---|---|
| Agent calls (subagent invocations) | <N> | one count per Agent-tool invocation in this session |
| Artifacts (markdown files in session dir, excluding ledger.md itself) | <N> | `find <session-id> -name '*.md' -not -name 'ledger.md' | wc -l` |
| Critic-panel loops used | <N> / 2 | from `decision-log.md`, lines matching "Loops used: N/2" |
| Loop cap reached | true \| false | true iff loops used == 2 |
| Decisions in synthesis | <N> | bulleted items under synthesis.md's `Recommendation` and `Uncertainties` headings |

## Derived ratios
- Agent-calls per decision: <agent-calls> / <decisions> = <ratio>
- Artifacts per decision: <artifacts> / <decisions> = <ratio>
- Loops to convergence: <loops>/2

## Warnings
- if `agent-calls / decisions > 10`: ⚠️ "consider whether the workflow produced more analysis than action"
- if `artifacts / decisions > 8`: ⚠️ "consider whether documentation is exceeding decisions"
- if loop cap reached: ⚠️ "candidate needed maximum rework; first-pass framing was off"
- if zero warnings: render the line "warnings: none"

## Notes
<orchestrator's free-form prose; aggregators ignore this section.>
```

**Bypass cases (no ledger written):**
- `quick take` invocations (steps 3–11 bypassed): no ledger.
- Pure factual questions answered by canon-librarian without classification or workflow: no ledger.
- All other sessions (including veto-stopped sessions): ledger required. Veto-stopped sessions render `decisions=0` and `ratios=N/A` for division-bound ratios.

**Threshold tuning instructions:** thresholds (10 / 8 / loop cap) live in this section only. Edit them here once 5 real ledgers reveal whether they are tight or loose; future ledgers pick up the change at next render.

**Decision definition (sharper than v1):** a "decision" is one bulleted item under either the `Recommendation` heading or the `Uncertainties` heading in synthesis.md. This is mechanically countable. If synthesis structure changes (CLAUDE.md step 12 spec edited), update this definition in the same commit.

## CLAUDE.md additions

### New step 13

```markdown
13. **Ledger.** Write `session-artifacts/<id>/ledger.md` by paste-and-filling the schema in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) (Ledger schema section). Counts come from session-dir contents and decision-log.md; ratios are shown derived (math visible); warnings render only when thresholds are crossed.

   **Bypass:** no ledger for `quick take` or pure-factual sessions. All other sessions, including veto-stopped, require the ledger.

   **Synthesis citation (required):** the final line of synthesis.md must be exactly: `Ledger: agent-calls=<N>, artifacts=<N>, loops=<N>/2; warnings: <list or "none">.` This makes the warnings visible at the operator-facing terminus. A session without this line is incomplete.
```

### New "Things you must not do" item
*"Do not skip the ledger on a non-bypassed session. The synthesis is incomplete until ledger.md exists and synthesis.md cites it."*

## Exemplar ledger
Ship one worked example at [.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md), derived from the format-only-state-transition-gate session — a real, on-disk session whose counts can be verified by inspection. The exemplar lives under exemplars/ rather than alongside the original session because exemplars/ is the documented "curated shelf" for reference artifacts.

## Pre-merge checklist (every item must hold)
1. HTML-comment marker on the schema section in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md). ✓
2. Tightened "decision" definition (parser-able). ✓
3. Bypass cases documented in schema section. ✓
4. Count-taking moment defined ("just before ledger.md is written"). ✓
5. CLAUDE.md instruction on ledger-required-or-bypassed. ✓
6. Citation-pattern-as-required-language in CLAUDE.md. ✓
7. Cross-link from CLAUDE.md step 13 to the schema section. ✓ (the markdown link in step 13 above)
8. Exemplar ledger shipped. ✓ (next file)

All eight pre-merge items are now in the candidate.

## Frame-level objection coverage
1. *Inline-only?* — addressed: file + citation, both. Aggregation needs the file.
2. *Operator diagnoses, not workflow?* — addressed: thresholds advisory; operator tunes from one place.
3. *Manual authorship drifts?* — addressed: HTML-comment marker locks load-bearing headings; Notes section quarantines free-form drift.
4. *Synthesis-as-terminus?* — addressed: synthesis citation is required language.

## Named assumptions (unchanged from v1, still load-bearing)
1. Orchestrator reliably writes ledger.md (post-context-exhaustion concern; mitigated partly by paste-and-fill, but not eliminated).
2. Citation pattern is followed literally (mitigated by required-language framing).
3. "Decision" definition holds across session shapes.
4. Cross-session aggregation eventually happens.
5. Three ratios capture modal failure.

## Where v2 could still be wrong
- The schema section is now ~50 lines of [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md). That's not small. If the README itself is rewritten (someone reorganizes it), the load-bearing headings could move silently. Mitigation: HTML-comment marker. Residual risk: real.
- The synthesis citation pattern requires exact-string compliance. Without an automated check, drift is the modal failure. The product critic flagged this; the rewrite added "required language" but no checker. A future entry could add a tiny line-grep at session close.
- Counts come from heterogeneous sources (file count, decision-log grep, synthesis-section count). Each source is fragile to format change. The schema names the source-of-truth for each, but this is documentation, not enforcement.
