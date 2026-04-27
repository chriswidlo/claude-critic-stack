# Critic — operations lens, loop 2 on candidate-v2

## What changed
Bypass cases documented inline (✓). Count-taking moment defined (✓). CLAUDE.md "ledger-required-or-bypassed" instruction in place (✓). Optional fallback script deferred — that's fine.

## Frame-level posture
End-of-context exhaustion remains a real risk; v2 doesn't eliminate it (paste-and-fill is shorter than free-form authorship, but still requires orchestrator focus at the moment of weakest reliability). This is acceptable given the mitigation: when ledger is missing, the absence itself is a defect-marker that any later inspection (a `find` for sessions without ledger.md) will surface.

## Residual concerns (non-blocking)
- Synthesis citation is "required language" but uncheckable mechanically until #14 lands. Acceptable: silent failure → visible (missing/wrong line), not corrupting.
- "Veto-stopped sessions render decisions=0; ratios=N/A" is documented but not yet exemplified. The exemplar ledger should explicitly show the converged-loop-2 case so the format is concrete; a degenerate-case (decisions=0) example can come later from a real veto-stopped session.

## Verdict
**approve.**
