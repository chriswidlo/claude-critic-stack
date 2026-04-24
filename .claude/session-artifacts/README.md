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

- **Ephemeral by default.** Per-session subdirectories are **gitignored**.
  Each session is a scratchpad; the history lives in the repo's real commits
  and in memory/, not here.
- **Promotion to `exemplars/`.** If a session produces a useful reference —
  most often because it hit a regression scenario like
  `tests/regression/ark-mono-connector-routing.md` — the curator copies the
  whole `<session-id>/` directory into `exemplars/` under a descriptive name.
  `exemplars/` IS tracked. Future runs are compared against these baselines.

## Hard gate on step 9

`CLAUDE.md` step 9 (generator) **must refuse** to proceed until
`<session-id>/scope-map.md` and `<session-id>/challenges.md` both exist.
If either is missing, the orchestrator re-runs step 7 or step 8. This is
the single most important correctness rule added in the Phase-2 upgrade;
it prevents the orchestrator from generating a candidate against an
un-challenged frame.

## Why in-repo and not `~/.claude/projects/`

The Claude-Code user-level memory directory (`~/.claude/projects/...`) is
machine-local. Putting artifacts there would scatter them across machines
and make `exemplars/` promotion awkward. Keeping them in the repo means
(a) they are versioned when promoted, (b) a fresh clone gets the
regression scenarios, (c) `.gitignore` governs ephemera with one line.

## `.gitignore` choice (documented)

Per-session subdirectories are ignored by default. `README.md` (this file)
and `exemplars/` are tracked. If you want full audit history instead,
replace the `.claude/session-artifacts/*/` line in `.gitignore` with an
allowlist approach — one line change, reversible.
