## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage on the diagnostics-implementation review (instrument-fit, dogfooding-as-confounder, coupling to host-runtime internals, ship-then-iterate). Librarian returned **partial coverage**: Anthropic engineering essays + Google SRE Ch.6 + Heilmeier full-body; Nygard, Feathers, March 1991 are inventory-stubs (not ingested, cannot be quoted).

## Direct facts

1. [SRE Book, Ch.6 §Four Golden Signals] "The four golden signals of monitoring are latency, traffic, errors, and saturation." (confidence: direct)
2. [SRE Book, Ch.6 §Worrying About Your Tail] Single-mean aggregates obscure tail behavior; canon recommends "request counts bucketed by latencies (suitable for rendering a histogram), rather than actual latencies." (confidence: direct)
3. [SRE Book, Ch.6 §As Simple as Possible, No Simpler] "Data collection, aggregation, and alerting configuration that is rarely exercised … should be up for removal. Signals that are collected, but not exposed in any prebaked dashboard nor used by any alert, are candidates for removal." (confidence: direct) — **load-bearing contradiction to SOTA wishlist.**
4. [SRE Book, Ch.6 §As Simple as Possible] Canon recommends "maintaining distinct systems with clear, simple, loosely coupled points of integration … using web APIs for pulling summary data in a format that can remain constant over an extended period of time." (confidence: direct) — **load-bearing contradiction to the JSONL-layout parser.**
5. [Anthropic, multi-agent research system 2025, §Production reliability] "Agents make dynamic decisions and are non-deterministic between runs … we monitor agent decision patterns and interaction structures—all without monitoring the contents of individual conversations." (confidence: direct) — published precedent for AI-blind structural observability.
6. [Anthropic, multi-agent research system 2025, §Conclusion] "The compound nature of errors in agentic systems means that minor issues for traditional software can derail agents entirely." (confidence: direct)
7. [Anthropic, multi-agent research system 2025, §Effective evaluation] "Start evaluating immediately with small samples … about 20 queries representing real usage patterns." (confidence: direct) — v1 dogfooding sample is one, gap to canon-recommended ≥20.
8. [Anthropic, Building Effective Agents 2024, §Summary] "find the simplest solution possible, and only increasing complexity when needed." (confidence: direct)
9. [Anthropic, Effective context engineering 2025, §Sub-agent architectures] "Each subagent might explore extensively … but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)." (confidence: direct)
10. [Heilmeier Catechism 1975] "What are the mid-term and final 'exams' to check for success?" (confidence: direct)

## Inferred claims

1. [canon-librarian] The shipped layer covers all four golden signals (duration≈latency, agent-calls≈traffic, verdicts≈errors, tokens≈saturation), so v1 instrument-fit is "minimally canonical." (confidence: inferred)
2. [canon-librarian] `duration_seconds` as a single mean-like number cannot answer "where did the 10 minutes go" by design; per SRE tail-section this is a known failure mode of single-number aggregates. (confidence: inferred)
3. [canon-librarian] The parser walking an undocumented internal subagent JSONL layout **directly violates** the SRE loose-coupling principle; canon position is the parser "should not exist in its current form; it should call a stable API." (confidence: inferred) — open question 5 in the upgrade entry is load-bearing per canon, not a footnote.
4. [canon-librarian] Under "Building Effective Agents" minimalism, the v1 gap on per-step duration may be *correct minimalism, not a defect*; panel should require evidence of operator pain before queuing per-phase timing. (confidence: inferred) — minor counter to instrument-fit reframe.
5. [canon-librarian] The lifecycle row showing `value-proved: —` and `completed: —` is, per Heilmeier, a **frame-level defect** — no success exam was named that distinguishes "earns maintenance cost" from "sunk-cost monument." (confidence: inferred) — frame-level objection, must survive to panel.
6. [canon-librarian] Subagent-architecture passage *partially defends* the parser's per-subagent file walk (matches architectural intent) but reinforces the SRE point that the layout is host-controlled. (confidence: inferred)

## Authority-framed claims (stub entries — named but not quoted)

1. **Nygard, *Release It!* (2018)** — underlying claim: canonical on production instrumentation tradeoffs and steady-state / decay tail of operational tooling. Quote present in output: **no** (stub, paywalled-no-open-edition). Confidence: **unsupported**. Any panel reasoning citing Nygard on ship-then-decay maintenance tails is authority-citation, not passage-citation.
2. **Feathers, *Working Effectively with Legacy Code* (2004)** — underlying claim: canonical on coupling to internals / hidden seams (Hyrum's-Law-adjacent). Quote present in output: **no** (stub). Confidence: **unsupported**. The "undocumented layout" concern relies on SRE loose-coupling, not on Feathers.
3. **March 1991, "Exploration and Exploitation in Organizational Learning"** — underlying claim (paraphrase from README, not the paper body): "adaptive processes, by refining exploitation more rapidly than exploration, are likely to become effective in the short run but self-destructive in the long run." Quote present in output: **no** (stub, pdf-manual). Confidence: **unsupported**. Closest canon match for survival × use base rate; cannot be cited as a direct passage.

## Contradictions surfaced

- **Instrument-fit reframe (more instrumentation) vs. SRE Ch.6 §As Simple as Possible (prune unviewed signals).** A reviewer treating "missing data" as a defect is the failure mode SRE warns against.
- **JSONL-layout parser (couples to internal layout) vs. SRE Ch.6 §loose-coupling (integrate against formats stable over time, prefer APIs).** Canon says the parser should be replaced with a stable-API integration.
- **SOTA wishlist for per-step / per-phase timing vs. Building Effective Agents minimalism (ship simplest, add complexity only on observed failure).** Panel should demand operator-pain evidence before expansion.
- **Shipping v1 with sample-of-one dogfooding vs. multi-agent essay's ≥20 representative queries.** Some support for ship-and-iterate, but the gap is canonical.

## Subagent's own verdict (verbatim)

"Corpus coverage: Partial — the highest-relevance primary sources for this question (Nygard *Release It!* on instrumentation/internals, March 1991 on exploration/exploitation, Feathers on coupling to internals/seams) are all present in inventory but **stub** entries with no ingested body. They cannot be quoted."

## Gaps the subagent missed (or explicitly declared)

- **Self-measurement / dogfooding-as-confounder.** No full-body canon source. March 1991 (stub) is the closest match. Reframe is **canon-unsupported** and synthesis must mark it.
- **Coupling to internals / Hyrum's Law.** Feathers and Nygard both stubs; SRE loose-coupling carries the load alone — no Hyrum's-Law-class statement available.
- **Ships-then-decays maintenance tails for instrumentation.** Nygard would source it; not ingested. SRE covers forward-looking pruning, not longitudinal decay.
- **Survival × use base rate for internal tooling.** No canon coverage; must come from outside-view's WebSearch tier.
- **"Convention-enforced invariants" defense.** No canon surfaced; SRE simplicity argument is silent on whether convention review at every edit substitutes for structural enforcement.

## Token budget
~880 tokens.
