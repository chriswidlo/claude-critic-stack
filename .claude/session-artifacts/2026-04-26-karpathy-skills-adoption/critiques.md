# Critic-panel verdicts

| Lens | Verdict | Frame-level objection |
|------|---------|----------------------|
| architecture | **rework** | Regret-minimization counts file-state regret, not coupling/mental-model regret; "minimize coupling regret, not edit regret." Reads volatile content (a tweet) into a stable layer (global standing instructions) — wrong dependency direction. |
| operations | **rework** | Detection cost is the binding constraint, not rollback cost. The frame elides detection. No attribution mechanism makes "rollback when wrong" structurally infeasible even if file-deletion is one keystroke. |
| product | **rework** | This is a posture choice (trust-defaults vs explicit-hygiene-layer), not a content-selection question. The empty file is a deliberate product configuration; populating it is itself the change, not the lines added. |

## Lens-specific design-level objections (the actionable rework items)

- **architecture:** read `quality-assurance-validator.md` to resolve A1 before shipping; add explicit precedence rule between standing instructions and agents (header sentence); justify global vs. project on coupling-direction grounds, not user-machine-topology grounds.
- **operations:** demote from "Recommended global add" to "project-scoped canary in one repo first"; add concrete attribution mechanism (sentinel phrase echoed by Claude when the instruction fires, OR run the canon-endorsed A/B over ~10 tasks per canon #4) before promoting; bound the two-systems-running period with an explicit review date.
- **product:** name the posture choice (trust-defaults vs explicit-hygiene); confirm user intent on the empty file before populating; drop the "provisional" hedge (it is shipping by another name) or genuinely run the A/B first.

## Convergence

All three frame-level objections converge on one insight: the candidate framed this as **which 8–15 lines to add**, but the actual decision is **whether to populate the empty global CLAUDE.md at all** — a posture/detectability/coupling question that requires either user input or measurement, neither of which the workflow performed.
