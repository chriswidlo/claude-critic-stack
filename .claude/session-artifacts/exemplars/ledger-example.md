# Session ledger — 2026-04-26-format-only-state-transition-gate

> **Exemplar.** This is a worked example of the ledger schema documented in
> [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)
> (*Ledger schema (load-bearing)*). It is derived from the on-disk session
> at
> [.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/](.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/),
> which converged at the loop cap. Counts can be verified by inspection.

## Counts
| Category | Count | Source of truth |
|---|---|---|
| Agent calls (subagent invocations) | 14 | classifier (1) + outside-view (1) + canon-librarian (1) + distillers (3) + scope-mapper (1) + frame-challenger (1) + critic-panel × 2 loops (6) = 14 |
| Artifacts (markdown files in session dir, excluding ledger.md itself) | 19 | `find 2026-04-26-format-only-state-transition-gate -name '*.md' -not -name 'ledger.md' \| wc -l` |
| Critic-panel loops used | 2 / 2 | from `decision-log.md` ("Loops used: 2/2") |
| Loop cap reached | true | loops used (2) == cap (2) |
| Decisions in synthesis | 6 | 1 explicit recommendation + 5 named uncertainties under `synthesis.md`'s `Recommendation` and `Uncertainties` headings |

## Derived ratios
- Agent-calls per decision: 14 / 6 = 2.33
- Artifacts per decision: 19 / 6 = 3.17
- Loops to convergence: 2/2

## Warnings
- ⚠️ candidate needed maximum rework; first-pass framing was off (loop cap reached)

## Notes

This session is a **worked example of a healthy-but-loopy** workflow run.
Both denominator-driven ratios (agent-calls/decision = 2.33; artifacts/decision = 3.17)
are well below their thresholds (10 and 8 respectively) — the workflow was
not over-elaborated relative to its decision output. The single warning
fires on loop cap reached, which is the correct signal: loop 1 produced a
candidate the panel rejected as non-responsive (see `decision-log.md`,
loop 1 entry); loop 2 corrected and converged. Two loops to convergence
means real rework happened, not gaming.

The exemplar demonstrates that "loop cap reached" is a *neutral* signal,
not a damning one — sometimes the framing is off and rework is the right
response. The warning's suggested action ("first-pass framing was off")
matches what the decision-log actually records: loop 1 adopted the
challenger's audit-first reframe; loop 2 backed out and rewrote against
the user's literal framing. The warning surfaced what happened.

The 1 explicit recommendation under `synthesis.md`'s `## Post-critique
recommendation (labeled)` heading plus the 5 bulleted uncertainties under
`## At least three named uncertainties` together count as 6 decisions per
the schema definition. Aggregators that grep for these two heading texts
will produce the same count.

This exemplar was produced retroactively (the session pre-dates the
ledger schema). Future ledgers will be written at the moment the session
ends, not after-the-fact, so the synthesis-citation line will match the
counts exactly.
