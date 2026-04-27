# Per-session reasoning artifacts

The 12-step workflow defined in `CLAUDE.md` produces a small set of named
artifacts per design-question session. They land here, one subdirectory per
session:

```
.claude/session-artifacts/<YYYY-MM-DD>-<short-slug>/
├── requirement.md          # requirement-classifier output (step 1)
├── frame.md                # reframe (step 2) + frame-challenger revisions (step 8)
├── distillations/          # one file per subagent return (step 6)
│   ├── outside-view.md
│   ├── canon-librarian.md
│   └── explore.md          # only if Explore ran
├── scope-map.md            # scope-mapper output (step 7)
├── challenges.md           # frame-challenger output (step 8)
├── critiques.md            # critic-panel aggregate (step 10)
├── decision-log.md         # replan-vs-rewrite decisions (step 11)
├── synthesis.md            # operator-facing synthesis (step 12)
└── ledger.md               # workflow-cost ledger (step 13) — see Ledger schema below
```

The orchestrator assigns the session id on step 1 — typically
`<YYYY-MM-DD>-<first-4-to-6-words-of-question>`, e.g.
`2026-04-26-format-only-state-transition-gate`.

## Lifecycle

Two audiences, two postures:

- **AI within-session: ephemeral scratchpad.** The orchestrator and subagents
  write freely into the current `<session-id>/` directory. No agent is
  instructed to read prior sessions, so the scratchpad voice is preserved —
  the AI does not write for posterity.
- **Human across-sessions: longitudinal record.** All session subdirectories
  ARE tracked in git. The point is drift detection — being able to look back
  and see where the workflow strengthened or weakened over time, which
  agents started producing thinner output, which frames the system kept
  picking up vs missing. Low-value sessions are themselves diagnostic data;
  do **not** prune them for noise.
- **Promotion to `exemplars/`.** If the curator judges a session to be a
  high-quality reference for future sessions, copy the whole `<session-id>/`
  directory into `exemplars/` under a descriptive name. `exemplars/` is the
  *curated* shelf; the rest of session-artifacts is the *raw* shelf. Both
  are tracked. Promotion is manual — no automated mechanism.

### Periodic hygiene — privacy only

The only sweep that should ever happen on the raw shelf is **privacy
redaction**: scrubbing pasted-in proprietary names, client identifiers,
or internal paths from other repos that ended up in `requirement.md` or
`frame.md`. Noise-removal pruning is forbidden — it destroys the very
longitudinal signal the tracking exists to capture.

## Hard gate on step 9

`CLAUDE.md` step 9 (generator) **must refuse** to proceed until
`<session-id>/scope-map.md` and `<session-id>/challenges.md` both exist.
If either is missing, the orchestrator re-runs step 7 or step 8. This is
the single most important correctness rule added in the Phase-2 upgrade;
it prevents the orchestrator from generating a candidate against an
un-challenged frame.

## Why in-repo and not in the user's global Claude Code memory dir

The Claude Code user-level memory directory is machine-local. Putting
artifacts there would scatter them across machines and make `exemplars/`
promotion awkward. Keeping them in the repo means (a) they are versioned
when promoted, (b) `.gitignore` governs ephemera with one line.

## Ledger schema (load-bearing)

<!-- machine-read source for ledger.md schema. CLAUDE.md step 13 and any
     example ledgers refer to this section. do not change the heading text
     of '## Counts', '## Derived ratios', '## Warnings', '## Notes' below
     without also updating CLAUDE.md step 13 and the exemplar ledger at
     .claude/session-artifacts/exemplars/ledger-example.md. -->

Every non-bypassed session writes `<session-id>/ledger.md` from the template
below. Counts are taken **just before `ledger.md` is written**; `ledger.md`
does not count itself. The four headings (`## Counts`, `## Derived ratios`,
`## Warnings`, `## Notes`) are the load-bearing keys aggregators rely on —
do not rename them inside individual ledgers.

### Bypass cases (no ledger written)

- `quick take` invocations (steps 3–11 bypassed): no ledger.
- Pure factual questions answered directly by `canon-librarian` without
  classification or workflow: no ledger.
- All other sessions, **including veto-stopped sessions** that never reached
  full convergence, require the ledger. Veto-stopped sessions render
  `decisions = 0` and `ratios = N/A` for division-bound ratios.

Absence of `ledger.md` from a non-bypassed session is a workflow defect.

### Template (paste-and-fill)

```markdown
# Session ledger — <session-id>

## Counts
| Category | Count | Source of truth |
|---|---|---|
| Agent calls (subagent invocations) | <N> | one count per Agent/Task-tool invocation in this session |
| Artifacts (markdown files in session dir, excluding ledger.md itself) | <N> | `find <session-id> -name '*.md' -not -name 'ledger.md' \| wc -l` |
| Critic-panel loops used | <N> / 2 | from decision-log.md, lines matching "Loops used: N/2" |
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
- if zero warnings: render the literal line "warnings: none"

## Notes
<orchestrator's free-form prose; aggregators ignore this section.>
```

### Definitions

- **"Decision"** — one bulleted item under either the `Recommendation`
  heading or the `Uncertainties` heading in `synthesis.md`. Mechanically
  countable. If [CLAUDE.md](../../CLAUDE.md) step 12's synthesis structure
  is edited, update this definition in the same commit.
- **"Agent call"** — one invocation of a subagent via the `Agent`/`Task`
  tool, counted at the orchestrator level. Sub-tool calls inside an agent
  (`Read`, `WebFetch`, etc.) do **not** count.

### Threshold tuning

Thresholds (10 / 8 / loop-cap) live in this section only — change once,
every future ledger picks up the new value. **After 5 real ledgers exist,
review the distribution:** if all sessions trigger warnings, raise
thresholds; if no sessions trigger, lower. Document the calibration in a
follow-up commit that updates this section.

### Synthesis citation

The final line of every `synthesis.md` cites the ledger summary inline so
the operator re-encounters the warnings at the operator-facing terminus:

```
Ledger: agent-calls=<N>, artifacts=<N>, loops=<N>/2; warnings: <list or "none">.
```

A non-bypassed session whose `synthesis.md` does not end with this line is
incomplete.

A worked example lives at
[.claude/session-artifacts/exemplars/ledger-example.md](.claude/session-artifacts/exemplars/ledger-example.md).

## `.gitignore` choice (documented)

All session subdirectories are tracked. The current design favors
completeness for the human reader at the cost of some repo bloat
(~100KB per session) and a privacy-redaction obligation. If you reverse
this, do it by reinstating the `.claude/session-artifacts/*/` ignore
line — one-line, reversible.
