# Question under review

Produce the deepest possible adversarial readout of the **Claude Opus 4.7 System Card** (Anthropic, 232 pp., dated 2026-04-16) and translate the findings into a concrete change-set against this repo (the agents under [.claude/agents/](.claude/agents/), the rules in [CLAUDE.md](CLAUDE.md), and the canon at [canon/](canon/)). Treat the system card as a primary risk dossier, not a marketing document: every numerical claim is verbatim-quoted with page citation, every conclusion cites a section, and the change-set runs through the full critic-panel under `SHADOW_PANEL=1` before synthesis.

## Constraints / context

- **Scope locked to 4.7 only.** Per user clarification: drop the 4.6 delta framing entirely; do not acquire the 4.6 system card, the 4.6 Sabotage Risk Report, the RSP, or any adjacent 4.6/Sonnet/Haiku/Petri publications. 4.7 is treated as a fresh baseline.
- **Path discipline.** No absolute paths or `~/`-paths in any artifact written into this repo. Repo-internal references are repo-relative markdown links; outside-repo files are described in prose. The path-check skill runs against all artifacts before completion.
- **Verbatim numbers.** Every percentage, threshold, and benchmark score is quoted with `(§X.Y, p.NN)` citation or it does not appear.
- **Distillation-only orchestrator after Phase 2.** Raw zone-reader output stays on disk; the orchestrator reads only `distillations/<agent>.md`.
- **Hard gate before generator.** [scope-map.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/scope-map.md) and [challenges.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/challenges.md) must exist before [repo-changeset.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/repo-changeset.md) is written.
- **Multi-agent narrow-objective warning** (carried forward from prior 4.6 finding): each parallel zone reader is framed as "verify the named invariants in your zone," not "find every problem."
- **SHADOW_PANEL=1.** The critic-panel runs as six lens invocations (3 Opus + 3 Sonnet shadow) plus the comparator. Opus retains verdict authority; shadows are voice, not vote.
- **No agreeableness.** If the system card's framing is weak, say so. If its evals do not support its conclusions, say so.

## What the user is asking the workflow to do

Produce a risk-dossier readout of a single primary document (Opus 4.7 System Card) and then **design** a concrete repo change-set against the readout — i.e., this is both an *investigation* (zones A–D + canon + outside-view) and a downstream *design* task (the change-set), not a single-shot decision.
