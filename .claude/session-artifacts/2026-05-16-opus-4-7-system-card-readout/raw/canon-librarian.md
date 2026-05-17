# Canon-librarian raw output — vendor system-card reading practice

## Corpus coverage assessment

**Thin.** No entry addresses model-card / system-card reading practice directly. No AI-policy literature, no Mitchell et al. "Model Cards for Model Reporting" (2019), no Bommasani et al. on foundation-model transparency, no METR / Apollo / NIST third-party-eval literature, no principal-agent or disclosure-economics canon. What the corpus does have: one vendor-authored AI-safety thesis (Anthropic 2023), one DARPA-authored research-evaluation rubric, SRE-style operational priors on the gap between pre-release claims and production reality, and a multi-agent essay that explicitly states automated evals miss what human evaluators catch.

## Supporting passages (steelman — vendor self-report as load-bearing evidence)

### 1. Anthropic, *Core Views on AI Safety: When, Why, What, and How* (2023)

[canon/corpus/anthropic-core-views-on-ai-safety/source.txt](canon/corpus/anthropic-core-views-on-ai-safety/source.txt) lines 70–84.

> "A major reason Anthropic exists as an organization is that we believe it's necessary to do safety research on 'frontier' AI systems. This requires an institution which can both work with large models and prioritize safety. […] Effective safety research on large models doesn't just require nominal (e.g. API) access to these systems — to do work on interpretability, fine tuning, and reinforcement learning it's necessary to develop AI systems internally at Anthropic."

**Relevance:** The strongest in-corpus steelman for vendor self-reports being load-bearing. The lab's own argument is that meaningful safety findings on a frontier model cannot be produced from API access alone; therefore a vendor-internal comparator (Mythos Preview) is by this lab's framing the only place where certain measurements can be taken. Refusing to weight the vendor's internal-comparator results is equivalent to refusing the only available evidence.

### 2. Anthropic, *Core Views on AI Safety* (2023), §"Portfolio Approach"

Same file, lines 96–104.

> "It's worth noting that the most pessimistic scenarios might look like optimistic scenarios up until very powerful AI systems are created. Taking pessimistic scenarios seriously requires humility and caution in evaluating evidence that systems are safe. […] Indications that we are in a pessimistic or near-pessimistic scenario may be sudden and hard to spot. We should therefore always act under the assumption that we still may be in such a scenario unless we have sufficient evidence that we are not."

**Relevance:** Same author supplying the counter-prior to its own future system cards — surface absence-of-problem is consistent with hidden problem. Operator reading a 4.7 system card has the vendor's own published epistemology saying "do not treat absence of red flags as evidence of safety."

### 3. Anthropic, *Core Views* (2023), §"Empiricism in AI safety"

Lines 62–64.

> "We believe it's hard to make rapid progress in science and engineering without close contact with our object of study. […] In our AI safety research, empirical evidence about AI — though it mostly arises from computational experiments, i.e. AI training and evaluation — is the primary source of ground truth."

**Relevance:** The vendor's stated epistemology privileges empirical eval results as ground truth. If the system card reports such evals, then by the vendor's own theory those numbers are the closest thing to ground truth the field has. Operator-side rebuttal must engage the empiricism claim, not dismiss it.

## Contradicting / complicating passages

### 1. Anthropic, *How we built our multi-agent research system* (2025)

[canon/corpus/anthropic-multi-agent-research-system/source.txt](canon/corpus/anthropic-multi-agent-research-system/source.txt) line 81.

> "Human evaluation catches what automation misses. People testing agents find edge cases that evals miss. These include hallucinated answers on unusual queries, system failures, or subtle source selection biases. In our case, human testers noticed that our early agents consistently chose SEO-optimized content farms over authoritative but less highly-ranked sources like academic PDFs or personal blogs. Adding source quality heuristics to our prompts helped resolve this issue. Even in a world of automated evaluations, manual testing remains essential."

**Why this complicates:** The vendor itself, in a different publication, concedes that its automated evals (the kind that populate system-card tables) systematically miss categories of failure that only show up under sustained human use. An operator reading a system card is reading exactly the artifact this passage warns will miss the "subtle bias" / "unusual query" / "system failure" classes. Single most useful in-corpus passage for an operator's stance.

### 2. George Heilmeier (DARPA), *The Heilmeier Catechism* (1975)

[canon/corpus/heilmeier-catechism/source.txt](canon/corpus/heilmeier-catechism/source.txt) lines 48–62.

> "What are you trying to do? Articulate your objectives using absolutely no jargon. How is it done today, and what are the limits of current practice? What is new in your approach and why do you think it will be successful? Who cares? If you are successful, what difference will it make? What are the risks? How much will it cost? How long will it take? What are the mid-term and final 'exams' to check for success?"

**Why this complicates:** Heilmeier demands a mid-term and final "exam" defined *by the evaluator, not the proposer*. A vendor-defined "Mythos Preview" baseline is the proposer choosing the exam. Operator's job: define the exam themselves and treat vendor-defined exams as proposer self-assessment — evidence, but not adjudication. This is a 50-year-old DARPA practice for exactly the failure mode of taking proposer self-evaluation as third-party validation.

### 3. Google SRE Team, *Site Reliability Engineering* (2016), Introduction

[canon/corpus/google-sre-book/source.txt](canon/corpus/google-sre-book/source.txt) lines 887, 905–909.

> "Hope is not a strategy. […] Both groups understand that it is unacceptable to state their interests in the baldest possible terms ('We want to launch anything, any time, without hindrance' versus 'We won't want to ever change anything in the system once it works'). And because their vocabulary and risk assumptions differ, both groups often resort to a familiar form of trench warfare to advance their interests."

**Why this complicates:** SRE's foundational frame: people who built and want to ship a system have systematically different risk assumptions than people who must operate it. Vendor publishing a system card is the dev side of this split, by structural position — not by bad faith. Operator stance must be SRE-side: assume vendor risk-vocabulary differs from operator risk-vocabulary even under good faith; treat the system card as the dev team's launch review, not as the operator's pre-launch gate.

### 4. Google SRE, §15 "Postmortem Culture"

Same file, line 948.

> "Postmortems should be written for all significant incidents, regardless of whether or not they paged; postmortems that did not trigger a page are even more valuable, as they likely point to clear monitoring gaps."

**Why this complicates:** Reliability discipline weights *post-deployment, blame-free incident records* — not pre-deployment self-reports — as the primary trustworthy signal. System cards are a *capability-launch* artifact, not a *reliability* artifact. Treat the system card as a baseline hypothesis to be falsified post-deployment, not as a deployed-behavior forecast.

## Gaps (sub-questions the corpus does not answer)

1. **Vendor-eval-vs-third-party-finding divergence as a documented pattern.** No METR, no Apollo, no NIST AISI, no preparedness-framework retrospectives. No Mitchell et al. *Model Cards for Model Reporting* (2019). No Bommasani et al. *Foundation Model Transparency Index*.
2. **Base rate of "alignment / safety claims that hold up in deployment."** No corpus entry tracks pre-deployment claims vs. post-deployment incidents.
3. **Principal-agent disclosure economics.** No Akerlof, no Spence signaling, no Healy & Palepu disclosure-economics surveys.
4. **Irreducible-comparator dependence.** Corpus gives the tension (Anthropic 2023 steelman vs. SRE/Heilmeier counter-prior) but no resolution procedure.
5. **Staleness.** Strongest steelman passage is Anthropic 2023 — three years old, pre-RSP / Preparedness-Framework / Frontier-Safety-Commitments era. Corpus's view of vendor safety publications is structurally out of date.

## Distiller summary

Corpus supports: vendor-internal access is the *only* place certain safety findings can be produced (Anthropic 2023), so vendor self-reports are non-replaceable evidence. Corpus contradicts: same vendor concedes automated evals miss known failure classes (Anthropic 2025); DARPA's 50-year-old research-eval rubric requires evaluator-defined exam, not proposer-defined (Heilmeier 1975); SRE holds dev-side and ops-side risk vocabularies differ structurally even under good faith, and load-bearing reliability evidence is post-deployment incident data (Google SRE 2016). Direct corpus coverage of model-card reading practice, third-party-divergence patterns, and disclosure economics: **none** — flag as corpus gap, not as a finding.
