# Outside-view distillation — shadow comparator

## Reference class

Ensemble methods that combine learners with shared training distribution. Specifically: bagging, boosting, and same-family model ensembles in ML systems.

## Base rate

- Ensemble error reduction over single-model baseline is typically **10–30%** when learners are sufficiently independent (different architectures, different data subsets).
- Ensemble error reduction is **near-zero** when learners are highly correlated (same architecture, same training data, same fine-tuning).
- Opus + Sonnet share: the same provider, similar training corpora, the same RLHF lineage, and overlap in the constitutional AI pipeline. Correlation between their judgments on the same prompt is plausibly 0.7–0.9 on bounded reasoning tasks.

## Forecast for this proposal

If shipped as designed, Opus + Sonnet shadow at the same prompt will surface **~20–40% of the variance** that a genuinely independent model (different family, different RLHF) would surface.

That is non-zero — useful — but it is also the upper end of "performative diversity" territory. The operations cost (doubling per-lens spend) is real; the marginal triangulation signal at same-family correlation is bounded.

## What would change the forecast

- Cross-family shadow (Llama, Mistral, Gemini): would lift expected variance capture toward 60–80%, near the bagging-ensemble base rate.
- Smaller within-family shadow (Haiku rather than Sonnet): possibly higher variance per-comparison but lower-quality lens overall, so disagreement-as-signal may degrade into disagreement-as-noise.

## What the outside view does not say

The outside view cannot say whether *this specific repo's review tasks* will exhibit the same correlation as the ML benchmark literature. The operator should treat the 20–40% number as a Fermi estimate, not a measurement.
