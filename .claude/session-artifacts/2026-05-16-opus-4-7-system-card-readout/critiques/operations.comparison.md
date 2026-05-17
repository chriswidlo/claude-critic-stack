# Comparison — operations lens (v2, loop-2)

| field | opus lane | sonnet shadow lane |
|---|---|---|
| verdict | approve | approve |
| weakest-link | Refusal-correlation coefficient remains unmeasured (v2 acknowledges honestly rather than guessing); workflow still cannot tell an operator whether the F2 fail-safe is over- or under-firing in practice; R5 blast-radius assumed-acceptable (Assumption D); R6 "named failure modes flagged" may render "none flagged" 100% of the time if operators don't populate it (Assumption E). | F2 override ceremony is undefined: rule says "requires explicit operator override" but does not specify what constitutes valid override or where it must be recorded; operator either proceeds silently (defeating audit trail) or stalls session unnecessarily. |
| frame-objection | Not raised as frame-level at v2 — operations-shadow's v1 demand (interim fail-safe before user resolves F2) is honored as R5 at the correct CLAUDE.md invariant layer with named retirement trigger. | Override mechanism is specified at the rule layer but not at the workflow layer; "explicit operator override" is mechanically unenforceable in the way the step-9 HARD GATE is — asymmetry is load-bearing for safety-flavored sessions; fix is one line specifying override must appear as a named `decision-log.md` entry, no v3 required. |

## Agreement class

`partial-agree`

## One-line gloss

Both lanes return `approve` and agree all v1 flip-conditions landed (arithmetic correction, R2/R3 rollback cost, R1 tripwire, F2 ranked resolutions, R5 interim fail-safe), but the shadow lane raises a frame-level residual — the override ceremony is mechanically undefined — that the Opus lane does not name; Opus lane instead emphasizes unmeasured refusal-correlation as the carry-forward.

## Triangulation signal for synthesis

- Partial-agree on operations lens: shadow concurs on the verdict and on the landing of all v1 flip-conditions, but identifies a *new* residual the Opus lane missed — the F2 override mechanism is unenforceable in the way the HARD GATE is enforceable, because "explicit operator override" has no specified artifact form. Shadow proposes a one-line fix (override must appear as named `decision-log.md` entry).
- SHADOW_PANEL value case: this is exactly the asymmetric-catch pattern the shadow lane exists to surface. Opus lane carries forward measurement debt (correlation coefficient, R5 blast-radius, R6 false-empty); shadow lane carries forward enforcement debt (override ceremony). Two non-overlapping residual classes; both should be named in synthesis carry-forward.
- Neither lane flips to `rework` on its own residual; the shadow's override-ceremony fix is small and surfaceable as a follow-up rather than a v3 trigger.
