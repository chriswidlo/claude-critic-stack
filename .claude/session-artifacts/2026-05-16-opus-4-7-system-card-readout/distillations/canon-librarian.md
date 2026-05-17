## Source agent
canon-librarian

## Invocation summary
Orchestrator asked the librarian for corpus retrieval on vendor system-card / model-card reading practice (in service of an Opus 4.7 system-card readout). Librarian returned three supporting passages (steelman: vendor self-report as load-bearing) and four contradicting passages (vendor self-report as structurally suspect), plus an explicit "corpus is thin" coverage flag and a staleness flag on the strongest steelman.

## Direct facts (verbatim canon quotes — citable without raw)

1. **Anthropic 2023, *Core Views on AI Safety*, [source.txt](canon/corpus/anthropic-core-views-on-ai-safety/source.txt) L70–84.** "Effective safety research on large models doesn't just require nominal (e.g. API) access to these systems — to do work on interpretability, fine tuning, and reinforcement learning it's necessary to develop AI systems internally at Anthropic." (confidence: direct)

2. **Anthropic 2023, *Core Views*, "Portfolio Approach," same file L96–104.** "Indications that we are in a pessimistic or near-pessimistic scenario may be sudden and hard to spot. We should therefore always act under the assumption that we still may be in such a scenario unless we have sufficient evidence that we are not." (confidence: direct)

3. **Anthropic 2023, *Core Views*, "Empiricism in AI safety," same file L62–64.** "In our AI safety research, empirical evidence about AI — though it mostly arises from computational experiments, i.e. AI training and evaluation — is the primary source of ground truth." (confidence: direct)

4. **Anthropic 2025, *How we built our multi-agent research system*, [source.txt](canon/corpus/anthropic-multi-agent-research-system/source.txt) L81.** "Human evaluation catches what automation misses. People testing agents find edge cases that evals miss. These include hallucinated answers on unusual queries, system failures, or subtle source selection biases. […] Even in a world of automated evaluations, manual testing remains essential." (confidence: direct)

5. **Heilmeier 1975, *DARPA Catechism*, [source.txt](canon/corpus/heilmeier-catechism/source.txt) L48–62.** "How is it done today, and what are the limits of current practice? […] What are the mid-term and final 'exams' to check for success?" (confidence: direct)

6. **Google SRE 2016, Introduction, [source.txt](canon/corpus/google-sre-book/source.txt) L887, L905–909.** "Hope is not a strategy. […] because their vocabulary and risk assumptions differ, both groups often resort to a familiar form of trench warfare to advance their interests." (confidence: direct)

7. **Google SRE 2016, §15 Postmortem Culture, same file L948.** "Postmortems should be written for all significant incidents, regardless of whether or not they paged; postmortems that did not trigger a page are even more valuable, as they likely point to clear monitoring gaps." (confidence: direct)

## Inferred claims (librarian's framing of which way each passage cuts)

1. [canon-librarian] Anthropic 2023 L70–84 cuts FOR vendor self-reports being load-bearing: only internal access produces certain safety measurements, so vendor-internal comparators (e.g., a "Mythos Preview" baseline) are non-replaceable evidence. (confidence: inferred)
2. [canon-librarian] Anthropic 2023 L96–104 cuts AGAINST naive vendor-self-report trust: the same vendor's published epistemology says absence of red flags is not evidence of safety. (confidence: inferred)
3. [canon-librarian] Anthropic 2023 L62–64 cuts FOR weighting vendor empirical evals as ground truth; operator rebuttal must engage the empiricism claim, not dismiss it. (confidence: inferred)
4. [canon-librarian] Anthropic 2025 L81 is the "single most useful in-corpus passage for an operator's stance" — vendor concedes automated evals (the kind populating system-card tables) systematically miss failure classes. (confidence: inferred)
5. [canon-librarian] Heilmeier 1975 cuts AGAINST: vendor-defined baselines = proposer choosing the exam; operator must define their own. (confidence: inferred)
6. [canon-librarian] Google SRE Introduction cuts AGAINST: dev-side and ops-side risk vocabularies differ by structural position, even under good faith — vendor-as-dev publishing a launch artifact ≠ operator-side gate. (confidence: inferred)
7. [canon-librarian] Google SRE §15 cuts AGAINST: reliability discipline privileges post-deployment incident data over pre-deployment self-reports; treat the system card as a hypothesis to be falsified post-deployment, not a behavior forecast. (confidence: inferred)

## Authority-framed claims

1. "Corpus coverage: **Thin**. No entry addresses model-card / system-card reading practice directly." — underlying claim: corpus has no direct coverage of the topic (no Mitchell et al. 2019 Model Cards, no Bommasani Transparency Index, no METR / Apollo / NIST AISI literature, no principal-agent / disclosure-economics canon). Quote present in output: no (librarian's own assertion, no quoted absence-evidence — but verifiable against corpus inventory). Confidence: inferred (librarian is authoritative for its own corpus).
2. "Strongest steelman passage is Anthropic 2023 — three years old, pre-RSP / Preparedness-Framework / Frontier-Safety-Commitments era. Corpus's view of vendor safety publications is structurally out of date." — underlying claim: the load-bearing pro-vendor-self-report passage is stale relative to current 2026 vendor-safety practice. Quote present in output: no (no post-2023 vendor-safety-framework canon entry shown to contrast). Confidence: inferred.

## Contradictions surfaced

- **Anthropic-vs-Anthropic (the load-bearing tension).** Anthropic 2023 (fact #1): meaningful frontier safety work *requires* vendor-internal access — so vendor-internal comparator results are the only available evidence. VS. Anthropic 2025 (fact #4): the vendor's *own* automated evals miss hallucinations, system failures, and subtle biases; "human evaluation catches what automation misses." Same author, opposite cut on whether a system card's eval tables can stand alone.
- **Vendor empiricism vs. proposer-defined exam.** Anthropic 2023 L62–64 (fact #3): empirical eval results are "primary source of ground truth." VS. Heilmeier 1975 (fact #5): the exam must be defined by the evaluator, not the proposer — vendor-chosen evals are proposer self-assessment.
- **Pre-deployment claim vs. post-deployment evidence.** Anthropic 2023 frames pre-release internal research as load-bearing. VS. Google SRE §15 (fact #7): only post-deployment incident records (especially the non-paging ones) are trustworthy reliability signal.

## Subagent's own verdict (verbatim)

"Corpus coverage assessment: **Thin.**"
"Direct corpus coverage of model-card reading practice, third-party-divergence patterns, and disclosure economics: **none** — flag as corpus gap, not as a finding."

## Gaps the subagent missed

The librarian named its own gaps thoroughly (vendor-vs-third-party divergence patterns, base rate of safety-claims-holding-in-deployment, principal-agent disclosure economics, irreducible-comparator-dependence resolution procedure, staleness of Anthropic 2023). Additional gaps the orchestrator should note:

1. No passage on **how operators should weight a vendor's own contradiction of itself** (Anthropic 2023 vs. 2025) — the corpus surfaces the tension but offers no decision rule.
2. No passage on **adversarial / red-team eval methodology** specifically (the librarian flagged no Apollo / METR; also no in-corpus red-team primer to substitute).
3. No passage on **system-card-as-marketing-document** critique — the librarian frames vendor-as-dev-side (SRE), not vendor-as-commercial-actor.
4. The librarian flagged staleness on Anthropic 2023 but did not flag whether Anthropic 2025 (the contradicting passage) is *itself* about a different artifact class (multi-agent research system writeup, not a system card) — the orchestrator should note the cross-domain transfer is itself an inference.

## Token budget
~1,050 tokens.
