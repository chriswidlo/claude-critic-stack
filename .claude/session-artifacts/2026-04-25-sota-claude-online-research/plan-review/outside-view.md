# Outside-view review — plan v3 (frequency-conditional triage for solo developer)

## Reference class

**Frequency-conditional self-triage protocols administered to a single user with no external accountability.** Adjacent classes (descending predictiveness): GTD adoption, solo-dev internal-tooling projects (N=1 audience), build-vs-buy heuristics for indie hackers, microservices-vs-monolith heuristics for small teams.

The plan is half productivity protocol (regime 1, regime 2 checklist) and half tooling project (regime 3 verifier). Base rates differ across the halves; the plan does not separate them.

## Base rates (estimates from web; canon gap declared)

- **Honest self-classification of activity volume:** Self-report studies on physical activity (closest hard-data analogue) show 30–60% overestimation of high-status activities (Schaller 2016; Matt et al. 1999). "Load-bearing research with an LLM" carries a moderately high-status flavor. Expect 1.3–2× overestimation on first count.
- **Personal productivity systems retained at 12 months:** ~20–30% of GTD-style adopters still running the full protocol after a year (community/practitioner sources).
- **Quarterly cadence performed by solo users with no external accountability:** ~15–25% do the second quarterly review on time; <10% do the fourth.
- **Solo-developer 1–2-hour internal tools actually in use at 90 days:** ~30–45%.

## Position

**Above class:** triage question is operationalized; default is "no change" (rare and good); transitions explicitly bounded; author had three loops of critic feedback.

**Below class:** threshold (8 / 9–40 / 41+ in 8 weeks) is unmeasurable from self-report; quarterly re-evaluation has low enforcement base rate; "1–2 hours" is canonical underestimate; no instrumentation to detect protocol decay.

Net: **slightly below base rate.** Regime 1 default rescues much of the downside (success-by-vacuity for ~60% of users); regimes 2 and 3 face the full headwind.

## Typical failure modes

1. **Regime 1 path (~60%):** Plan "succeeds" trivially — user picks regime 1, never re-evaluates, would have done that anyway. Value-add near zero.
2. **Regime 2 path (~25%):** User writes the checklist file, follows it for 2–3 queries, silently stops. Failure invisible until a fabricated citation drives a bad decision.
3. **Regime 3 path (~15%):** Self-classifies inaccurately; builds verifier in 6–12h (not 1–2h); runs it 5–20× in month 1, 0–2×/month thereafter; hosted engine's Markdown changes; abandoned tool.

**Deepest failure:** plan has no detector for regime mismatch. Re-evaluation uses the same biased self-report as the original.

## Verdict: below base rate.

Lifters above base rate (descending cheapness):
1. Replace self-reported count with a 2-week observation period.
2. Generate the quarterly re-evaluation as a calendar entry on regime-pick.
3. Add an abandonment signal (script that records last-run-date of `verify-research.md`; warns if regime-3 selected but verifier unused 30 days).
4. Cap regime 3 entry behind a 4-week regime-2 sunk-cost gate.

Without at least #1 and #2, plan is a well-written instance of a category that does not work for solo users at the rates the plan implicitly assumes.

Sources: Schaller 2016 (PMC4889825); Matt et al. 1999; NN/G diary studies; practitioner posts on solo-dev tooling and quarterly reviews.
