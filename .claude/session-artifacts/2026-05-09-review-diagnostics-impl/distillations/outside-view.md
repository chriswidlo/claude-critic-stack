## Source agent
outside-view

## Invocation summary
Orchestrator asked for reference-class forecast on the proposed diagnostics layer (hook-based instrumentation parsing Claude Code's undocumented transcript layout). Subagent returned a four-class taxonomy, an unsourced base-rate estimate, a "below base rate, narrowly" verdict on the strict success definition, and a cheapest-experiment recommendation.

## Direct facts
1. [canon/sources.yaml inventory] Canon covers forecasting methodology (Kahneman/Lovallo 1993, Flyvbjerg 2006, Tetlock 2015) and ops-adjacent (Google SRE 2016, Nygard 2018) — but corpus body is gitignored, so only inventory citations are available, not passages. (confidence: direct)
2. [canon inventory gap declaration] Canon does not cover three of four candidate reference classes: AI-observability projects, hook-based instrumentation tied to undocumented internal layouts, self-measurement traps (March 1991 partial). (confidence: direct)
3. [upgrade entry, quoted by subagent] The diagnostics layer parses `<encoded-cwd>/<claude-uuid>/subagents/agent-<id>.jsonl` plus sibling `.meta.json`, layout self-described as "undocumented in current Anthropic refs." (confidence: direct)
4. [WebSearch sources cited] Public exemplar of the AI-observability class exists: disler/claude-code-hooks-multi-agent-observability on GitHub. (confidence: direct)

## Inferred claims
1. [outside-view] Class (1) — hooks against undocumented internal layouts — is the most predictive class because host-product layout changes silently zero the parser; it bounds survival even if other dimensions go well. (confidence: inferred)
2. [outside-view] Modal failure for class (1): six-to-nine months post-ship, a host-product update silently changes path or schema; parser returns "transcript-missing" or zero attribution rather than crashing; dashboard renders flat/wrong numbers; rewrite costs ~50% of original effort and is deferred. (confidence: inferred)
3. [outside-view] Secondary failure mode: dogfooding-as-validation — first sample is a review session (easy workload), forming a misleadingly low-cost prior that misleads diagnosis when real sessions run hot. (confidence: inferred)
4. [outside-view] Tertiary failure: decay — instrument works, nobody opens dashboard, alive but functionally dead at ~3 months. (confidence: inferred)
5. [outside-view] AI-blindness invariant breaking via hook stderr leak is possible but is **not** the modal failure; the review's emphasis there may be over-indexed against the actual risk distribution. (confidence: inferred)
6. [outside-view] Above-base-rate features: same author/consumer (no adoption gap), small surface (~600 lines, gitignored output), failure-mode is recoverable ("transcript-missing" vs corrupt data). (confidence: inferred)
7. [outside-view] Below-base-rate features: explicit undocumented-layout dependency, loose verdict/loop regexes, convention-based stderr suppression, dogfood-only validation, prose-enforced step-1 operator handoff. (confidence: inferred)
8. [outside-view] Net position: slightly below base rate for joint survival × use; at or slightly above base rate for the looser "ships and runs" definition. (confidence: inferred)
9. [outside-view] Lifts that would move it above base rate: canary detecting silent zero-attribution, tightened anchored regexes, structural `hook-exec.sh` wrapper enforcing redirect, non-dogfood replay sample. (confidence: inferred)
10. [outside-view] Cheapest experiment: replay three pre-2026-05-09 session-artifact directories' transcript JSONL through the parser in isolation; check (a) `metrics.json` produced, (b) by-agent token sums match transcript total within 5%, (c) verdict/loop counts match hand-count of `critiques/*.md` and `decision-log.md`. ~1 hour cost. (confidence: inferred)

## Authority-framed claims
1. "Hooks against undocumented internal layouts — 6-month survival without rewrite is, in qualitative estimate, ~40–60%." — underlying claim: ~40–60% 6-month survival rate. Quote present in output: no (subagent self-flags "Estimate, not sourced"). Confidence: **unsupported**.
2. "Internal instrumentation continued use after 6 months — well-attested class, with the typical figure being ~30–50% of internal dashboards going unconsulted within a year of ship." — underlying claim: ~30–50% decay rate. Quote present in output: no (asserted as "well-attested" but no citation given; sources list includes platformengineering.org and getdx.com but no specific passage tied to the figure). Confidence: **unsupported**.
3. "Joint survival × use — multiplying these, a defensible base rate is ~15–30% of such projects 'succeed' by the stated definition at the 6-month mark." — underlying claim: ~15–30% joint success rate. Quote present in output: no (subagent self-flags "Estimate; flag as such"). Confidence: **unsupported**.
4. "If the success definition is loosened to 'ships and is technically functional on day 1,' base rate climbs to ~80%+" — underlying claim: ~80%+ ships-and-runs base rate. Quote present in output: no. Confidence: **unsupported**.
5. "Hyrum's Law" invoked as analog for class (1). Quote present in output: no; named as "closest analog… also not in canon." Confidence: **unsupported** (named without content).

## Contradictions surfaced
- Subagent did not surface internal contradictions in the source material (canon body is gitignored; only inventory was reachable). Tension noted within the subagent's own output: review's emphasis on AI-blindness leak vs. subagent's claim that this is not the modal failure — this is a disagreement between the candidate's framing and the outside-view verdict, not a contradiction within retrieved canon.

## Subagent's own verdict (verbatim)
"**Below base rate, narrowly**, on the joint survival × use definition. Within tolerance on the looser ships-and-runs definition."

## Gaps the subagent missed
- No sourced base rate. All three quantitative anchors (~40–60%, ~30–50%, ~15–30%) are unsourced estimates; the orchestrator should not treat the joint ~15–30% figure as a calibrated probability.
- Did not enumerate cases where the layout dependency is *not* fragile (e.g., if Anthropic publishes the schema or stabilizes a public hooks-output spec). The risk model is one-sided.
- Did not cost the proposed canary or `hook-exec.sh` wrapper, so the orchestrator cannot trade off "lift to above base rate" against marginal implementation effort.
- Did not address whether the diagnostics being load-bearing for *workflow-economics* decisions (vs. decorative dashboard) would alter the decay base rate; the decay rate cited is for "internal dashboards," but the proposal couples diagnostics to ledger citations in synthesis.md, which may bind consumption.
- No discussion of whether the three-replay experiment is feasible given that pre-2026-05-09 sessions ran without the workflow-id.txt handoff — the staging directory may not exist for those sessions.

## Token budget
~830 tokens.
