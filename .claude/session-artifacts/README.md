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
└── decision-log.md         # replan-vs-rewrite decisions (step 11)
```

The orchestrator assigns the session id on step 1 — typically
`<YYYY-MM-DD>-<first-4-to-6-words-of-question>`, e.g.
`2026-04-24-connector-routing-ark-mono`.

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
- **Promotion to `exemplars/`.** If a session produces a regression-worthy
  reference (e.g. a baseline like `tests/regression/ark-mono-connector-routing.md`),
  the curator copies the whole `<session-id>/` directory into `exemplars/`
  under a descriptive name. `exemplars/` is the *curated* shelf; the rest of
  session-artifacts is the *raw* shelf. Both are tracked.

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
when promoted, (b) a fresh clone gets the regression scenarios,
(c) `.gitignore` governs ephemera with one line.

## `.gitignore` choice (documented)

All session subdirectories are tracked. The earlier design ignored them
by default and required curator promotion to `exemplars/`; in practice the
promotion ritual was too high-friction (after 8 active sessions, `exemplars/`
remained empty) and the longitudinal-reflection use case was lost. The
current design favors completeness for the human reader at the cost of
some repo bloat (~100KB per session) and a privacy-redaction obligation.
If you reverse this, do it by reinstating the
`.claude/session-artifacts/*/` ignore line — one-line, reversible.
