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
├── critiques.md            # critic-panel aggregate (step 10) — see Critiques layout below
├── critiques/              # ONLY under SHADOW_PANEL=1 — per-lens files
│   ├── architecture.md          # critic-architecture (Opus)
│   ├── operations.md            # critic-operations (Opus)
│   ├── product.md               # critic-product (Opus)
│   ├── architecture.shadow.md   # critic-architecture-shadow (Sonnet)
│   ├── operations.shadow.md     # critic-operations-shadow (Sonnet)
│   ├── product.shadow.md        # critic-product-shadow (Sonnet)
│   ├── architecture.comparison.md   # critic-comparator: per-lens agreement class
│   ├── operations.comparison.md
│   └── product.comparison.md
├── decision-log.md         # replan-vs-rewrite decisions (step 11)
├── synthesis.md            # operator-facing synthesis (step 12) — see Synthesis schema below
├── ledger.md               # workflow-cost ledger (step 13) — see Ledger schema below
└── diagnostics/            # OPTIONAL — per-session metrics, see Diagnostics schema below
    ├── start.ts            # SessionStart hook: unix epoch
    ├── end.ts              # SessionEnd hook: unix epoch
    ├── events.jsonl        # PreToolUse/PostToolUse/SubagentStop hooks: events per tool call
    ├── workflow-id.txt     # binding sigil written by session-bootstrap at step 4b
    └── metrics.json        # post-session parser output: tokens by agent, etc.
```

### Critiques layout — default mode vs SHADOW_PANEL mode

| Mode | What gets written |
|---|---|
| **Default** (3 lenses) | Single aggregate file `critiques.md` containing each lens's verdict. No `critiques/` subdir. |
| **`SHADOW_PANEL=1`** (6 lenses + comparator) | Aggregate `critiques.md` PLUS the `critiques/` subdir holding the 9 per-lens files (3 Opus + 3 Sonnet shadow + 3 comparison). Comparator does not modify `critiques.md` — it only emits the `.comparison.md` files. |

The aggregate `critiques.md` is the load-bearing artifact (consumed at step 11 routing). The `critiques/` subdir is the audit trail under shadow mode.

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

## Synthesis schema (load-bearing — referenced from CLAUDE.md step 12)

<!-- machine-read source for synthesis.md structure. CLAUDE.md step 12 points
     here. The ordered bullet list below is the canonical template — adding,
     removing, or reordering bullets requires updating CLAUDE.md in the same
     commit. The literal `Ledger:` citation line at the end is enforced. -->

Every non-bypassed session writes `synthesis.md` per the structure below. The orchestrator (not an agent) authors this file at step 12, AFTER critic-panel verdicts in step 10 and any replan/rewrite loops in step 11 have concluded.

### Required structure (in order)

`synthesis.md` MUST present these elements in this order. Do not collapse into a single flowing paragraph; the operator skims by section.

1. **Classifier label and the alternative classification.** From `requirement.md`. Surfaces the framing bias the classifier carried in.
2. **The reframe (current revision).** From `frame.md`'s latest `## Revision N` block. If multiple revisions exist (loops happened), cite the current one and note the revision count.
3. **Reference-class forecast.** From `distillations/outside-view.md`. The base rate, the position relative to it, and the typical failure mode.
4. **Canon passages — supporting AND contradicting.** From `distillations/canon-librarian.md`. Both kinds. Contradicting passages are non-optional per the librarian's mandatory contract.
5. **Scope-map summary and any unresolved conflicts.** From `scope-map.md`. Name preserved primitives and the reason for preservation.
6. **Frame-level challenge and how the recommendation addresses it.** From `challenges.md` cross-referenced with the candidate. The candidate that ignores the challenge is a defect.
7. **Post-critique recommendation, explicitly labeled.** The orchestrator's final candidate after step 10/11 loops. Label as "Post-critique recommendation:" — operator must be able to find it by grep.
8. **Named failure modes flagged.** Separate bullet enumerating any anchor risks that `outside-view`, `canon-librarian`, or any critic lens flagged (e.g., "inaccessible-comparator anchoring"). Empty bullet ("none flagged") is acceptable but the bullet itself is required.
9. **Triangulation signal** *(only when `SHADOW_PANEL=1` ran)*. Per-lens agreement class from `critiques/<lens>.comparison.md`. If `agree` on all three lenses: "shadow concurs across all lenses." Otherwise name the lens and the dimension of difference. **If any Opus lens returned no verdict file (refused / unavailable) and the session is safety-flavored, add a sub-bullet "refusal as triangulation signal"** — a missing verdict on safety-flavored work is itself signal.
10. **At least three named uncertainties.** Each uncertainty stated with what would make it more or less concerning.
11. **The cheapest experiment that would reduce the biggest uncertainty.** One concrete action with a stated success criterion.

### Final line (literal, required)

`synthesis.md` MUST end with the ledger citation line — verbatim format:

```
Ledger: agent-calls=<N>, artifacts=<N>, loops=<N>/2; warnings: <list or "none">.
```

A session whose `synthesis.md` does not end with this exact line is incomplete. The `/ledger-render` skill at step 13 enforces this (Edit-in-place if missing).

### Bypass cases (no synthesis written)

- `quick take` invocations: synthesis bypassed (single paragraph reply with a one-line bypass flag).
- Pure factual questions answered by `canon-librarian`: no synthesis.

### Why the structure is rigid

Step 12 is the **only operator-facing surface**. The 11 elements are calibrated against named LLM failure modes (see [.genesis/five-pressures.md](.genesis/five-pressures.md)):
- Element 1 (classifier + alternative) defends against single-frame anchoring.
- Element 2 (reframe revision) defends against accepting the user's framing uncritically.
- Element 3 (reference-class) defends against inside-view detail-reasoning.
- Element 4 (supporting + contradicting) defends against confirmation bias.
- Element 8 (named failure modes flagged) defends against silent anchor adoption.
- Element 9 (triangulation signal) defends against correlated review error.
- Element 10 (three uncertainties) defends against equally-confident prose.
- Element 11 (cheapest experiment) defends against recommendations-without-falsifiability.

Collapsing the structure is not a stylistic choice; it dismantles the failure-mode defenses.

---

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
  countable. If [CLAUDE.md](CLAUDE.md) step 12's synthesis structure
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

## Diagnostics schema (additive, optional)

<!-- additive layer over the load-bearing ledger schema. Existing ledgers
     without the `## Metrics` block remain valid. The `diagnostics/` subdir
     is captured by the hook chain in `.claude/hooks/` and the parser at
     `bin/diagnostics/aggregate-session.py`. AI-blind: hooks suppress output. -->

Per-session diagnostics live in a dedicated `diagnostics/` subfolder, separated
from business artifacts. Capture is **AI-blind**: bash hooks under
[.claude/hooks/](.claude/hooks/) write silently; the orchestrator never sees
their output, and critics at step 10 are not affected.

### Files in `diagnostics/`

| File | Producer | Purpose |
|---|---|---|
| `start.ts` | `SessionStart` hook | unix epoch when Claude session began |
| `end.ts` | `Stop` hook | unix epoch when Claude session ended |
| `events.jsonl` | `PostToolUse` hook | `{ts, tool}` per tool call (audit trail) |
| `metrics.json` | [bin/diagnostics/aggregate-session.py](bin/diagnostics/aggregate-session.py) | derived: tokens by agent, tool counts, verdicts, loops |

### `metrics.json` schema

```json
{
  "duration_seconds": 562,
  "tokens": {
    "total": { "input": 124530, "output": 18920 },
    "by_agent": {
      "main":                { "input": 1344,  "output": 1243758, "calls": 0 },
      "canon-librarian":     { "input": 22000, "output": 3200,    "calls": 1 },
      "critic-architecture": { "input": 15000, "output": 4500,    "calls": 1 }
    },
    "source": "transcript-parsed"
  },
  "tool_calls": { "total": 23, "by_type": { "Read": 8, "Bash": 7, "Agent": 5 } },
  "verdicts":   { "architecture": "approve", "operations": "approve", "product": "rework" },
  "loops": 1
}
```

### `## Metrics` block in `ledger.md`

When `diagnostics/metrics.json` exists, the [ledger-render skill](.claude/skills/ledger-render/SKILL.md)
appends a `## Metrics` block to `ledger.md` after `## Notes`. The block
heading is **additive, not load-bearing** — older ledgers without the block
remain valid. The block content is the YAML rendering of `metrics.json`,
preserving the same keys.

### Bridge between Claude session UUID → workflow id

Hooks fire on `SessionStart` (Claude UUID is known) but the workflow id isn't
assigned until step 1 of [CLAUDE.md](CLAUDE.md). The bridge is a small handoff:

1. Hooks initially stage to `.claude/.metrics/staging/<claude-uuid>/`.
2. Step 1 of the workflow writes the workflow id to
   `.claude/.metrics/staging/<claude-uuid>/workflow-id.txt`.
3. The `Stop` hook reads that file, moves staged data into
   `<workflow-id>/diagnostics/`, removes staging, and triggers the parser.
4. If `workflow-id.txt` is missing (session aborted before step 1, quick-take
   bypass, etc.), the Stop hook archives staged data to
   `.claude/.metrics/orphan/<claude-uuid>/` so nothing is lost and nothing
   pollutes session-artifacts.

## `.gitignore` choice (documented)

All session subdirectories are tracked. The current design favors
completeness for the human reader at the cost of some repo bloat
(~100KB per session) and a privacy-redaction obligation. If you reverse
this, do it by reinstating the `.claude/session-artifacts/*/` ignore
line — one-line, reversible.
