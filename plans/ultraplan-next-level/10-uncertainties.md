# 10 — Three things I am most uncertain about

Vague hedging adverbs do not count. These are named gaps. Each is paired with the evidence that would resolve it.

## U1 — Whether the operator will fill in calibration revisits

The single most load-bearing assumption in S1 (and therefore the spine of the plan) is that the operator will spend ~30 minutes per past decision answering structured questions about how it played out. Without that, the substrate is theatrical and the foundational reframe collapses to the "habit" counter-proposal in [07-deepdive-decision-record-substrate.md](07-deepdive-decision-record-substrate.md). I cannot tell from outside whether the operator has the temperament for sustained retrospective work. The signal I have — that the [upgrades/](../../upgrades/) lab exists and has been seeded with content — is consistent with an operator who *will* invest in structured reflection. The signal in the other direction — that there is no current revisit habit visible in the artifacts — is consistent with an operator who *will not*.

**Evidence that would resolve it:** running the S1 cheapest experiment for three weeks and observing whether the by-hand `decision.yaml` authoring is sustained or abandoned. ~2.5 hours of operator time. The most informative single data point in the entire plan and the cheapest to obtain.

## U2 — Whether the eval harness can produce non-noisy verdicts at the scale the operator can sustain

The S3 harness needs ~10–20 scenarios to produce signal that is not dominated by per-run variance. Authoring scenarios is real cognitive work — each is a small designed experiment with a paired variant, an artifact-feature schema, and (optionally) a grader prompt. If the operator can sustain ~1 new scenario per fortnight, the harness reaches signal-strength in ~5–10 months. If they can sustain only ~1 per quarter, the harness sits at insufficient power for ~3 years and is producing noisy verdicts the whole time. There is also a hidden axis: how *stable* per-run grading is — Zheng et al.'s grader-noise data suggests inter-run agreement on the same scenario is well below 100% even with careful prompts. The combined uncertainty (how fast scenarios accumulate × how stable the grader is) determines whether the harness is honest measurement or expensive theatre.

**Evidence that would resolve it:** convert the [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md) to one harness scenario, run it five times in a row, and measure (a) how often the same verdict is produced and (b) how long the conversion took relative to the operator's available time. ~3–4 hours of operator time. If the inter-run agreement is below ~80%, the grader half of the harness is unreliable; the artifact-feature half may still be usable on its own.

## U3 — Whether the corpus, as it actually exists, can support contradiction-first retrieval

The S4 inverted-librarian proposal assumes the corpus contains contrary voices on the topics the operator's questions actually touch. Reading [canon/sources.yaml](../../canon/sources.yaml) and walking [canon/corpus/](../../canon/corpus/), the *fully ingested* subset is heavily Anthropic-engineering literature and a few open-access papers; the books that would hold the strongest contrary voices (Vernon's *Strategic Monoliths*, Helland's *Life Beyond Distributed Transactions* in PDF, Nygard's *Release It!*) are stubs. If the operator's typical question is on a topic where the canon has only one ingested voice, contradiction-first retrieval will produce weak passages or nothing at all, and the proposal does not deliver its promised value.

**Evidence that would resolve it:** the S4 cheapest experiment — manually invoking the librarian in contradiction-first mode against two recent candidates and observing whether the corpus produces sharper refutations than the existing relevance-first librarian's "at least one contradicting passage" rule produces. ~2 hours of operator time.

## What these three uncertainties share

All three are **resolvable cheaply within the next two to three weeks** by running experiments the operator can do in operator-time, without committing to any builds. The plan is structured so that running these three experiments is the first work on the timeline ([08-sequencing.md](08-sequencing.md), Phase A weeks 0–3). If even two of the three come back ambiguous, the plan should be re-shaped before any agent files are edited.

The honest position: I built the plan by reading the repo and the literature. The plan's value is bounded by how well that reading predicts the operator's actual behaviour and the corpus's actual coverage. Until those are tested, every claim above is a hypothesis with reasoning behind it but no evidence under it.
