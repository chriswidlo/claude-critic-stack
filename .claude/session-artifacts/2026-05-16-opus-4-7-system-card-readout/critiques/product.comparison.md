# Comparison — product lens (v2, loop-2)

| field | opus lane | sonnet shadow lane |
|---|---|---|
| verdict | approve | approve |
| weakest-link | Synthesis-template addition is *render-on-trigger*, not *render-always*, so quiet sessions still produce no audit trail that the new bullets fired correctly; "None flagged" empty-case is a false-negative attractor if trigger logic is buggy; fail-safe override path is undefined. | R4 (canon ingest for declined findings F6/F7) remains a human-curator discovery problem — stubs are grep-discoverable but require the curator to find them; F2 fail-safe halt requires "explicit operator override" but does not specify what constitutes valid override, what it produces in `decision-log.md`, or how long it persists. |
| frame-objection | v2 partially adopts the v1 frame ("translate findings into a disclosure surface") but stops short of producing a standalone disclosure surface (e.g., `MODEL-NOTES.md` keyed to the model version powering the stack); disperses 4.7-specific disclosure across CLAUDE.md, two agent files, an upgrades entry, and a session-artifact directory — correct for *enforcement*, wrong for *legibility*; gap belongs in R1, not v3-blocking. | F2 fail-safe is framed as a temporary bridge with retirement trigger pointing at R1's `created`-stage entry; R1 has no SLO, no spike, no prepared state, so the bridge may persist indefinitely as a "permanent tax disguised as a bridge"; change-set does not define what "stalled" looks like or what happens twelve sessions from now. |

## Agreement class

`agree`

## One-line gloss

Both lanes return `approve` and both verify the v1 flip-conditions met (R2/R3 landed in contract files with co-falsifier linkage; F2's live state visible at the orchestrator-rule layer); residual concerns differ in vocabulary but converge on the same underlying defect — the fail-safe's override path is undefined and its retirement trigger depends on R&D work with no completion target.

## Triangulation signal for synthesis

- Shadow concurs on verdict and on the load-bearing v1-to-v2 flip (invisible flavor text became operator-blocking gate); the "named but not landed / not surfaced to operators" v1 critique is now closed across both lanes.
- SHADOW_PANEL value case: both lanes independently flagged the override-ceremony underspecification — that catch is *correlated* (not shadow-only), which strengthens it as a high-confidence carry-forward to a future session.
- Non-overlapping residuals worth surfacing separately: Opus lane uniquely names "render-on-trigger vs. render-always" measurement debt (no audit trail that bullets fired correctly) and the absent standalone disclosure surface (`MODEL-NOTES.md`-style); shadow lane uniquely names the bridge-becomes-tax failure mode (F2 fail-safe could persist indefinitely if R1 stalls, with no "stalled" definition). Two distinct residual classes around the same fail-safe; both belong in carry-forward.
