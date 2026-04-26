## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on building a SOTA Claude-based online research pipeline. Subagent returned a three-class taxonomy (hosted Deep Research SaaS, Claude-Code-native, open-source orchestrator), base-rate ranges for each, and a conditional verdict.

## Direct facts
1. [canon/sources.yaml line 170] Canon has methodological anchors (Kahneman/Lovallo 1993, Flyvbjerg 2006, Tetlock 2015) but a declared gap on AI/ML system design coverage. (confidence: direct)
2. [DRBench, via DeepResearchEval arXiv 2026] Citation accuracy on hosted Deep Research benchmarks: 78–94%. (confidence: direct)
3. [DeepResearchEval arXiv 2601.09688v1; DeepHalluBench arXiv 2601.22984] 3–13% of cited URLs are fabricated even with web grounding. (confidence: direct)
4. [2026 audit of ACL/NAACL/EMNLP papers] Hallucinated-reference rate jumped >10×: 0.28% (2024) → 2.59% (2025). (confidence: direct)
5. [Gartner, Mar 2025] Projects 40% of agentic AI projects cancelled or scaled-back by 2028. (confidence: direct)
6. [Fortune 100 case, cited via dev.to AI agent failure analyses 2026] Agent code accounts for 18% of system; infra accounts for 82%. (confidence: direct)
7. [Redwerk LangGraph-vs-CrewAI 2026] LangGraph beats CrewAI on production survival via stateful checkpointing and recursion limits; CrewAI characterized as a prototyping tool. (confidence: direct)

## Inferred claims
1. [outside-view] Joint success rates (quality≥4/5 AND 90-day durability): Hosted 40–55%; Claude-Code-native 20–30%; Open-source orchestrator 10–20%. Subagent flags "estimates not measured." (confidence: inferred)
2. [outside-view] Hosted Deep Research is "at base rate by construction"; above-class only if domain matches training distribution (general web, news, public academia). (confidence: inferred)
3. [outside-view] Claude-Code-native pipelines inherit Claude Code update cadence — feature for durability, risk for reproducibility. (confidence: inferred)
4. [outside-view] Dominant quality failure across all three classes is citation hallucination, not reasoning errors or retrieval misses. (confidence: inferred)
5. [outside-view] The pipeline that wins has the strongest per-claim citation verifier regardless of substrate. (confidence: inferred)
6. [outside-view] Lifters above base rate for build options: deterministic citation-verifier as hard gate, frozen model+harness version pinning, 90-day re-run test in acceptance criteria. (confidence: inferred)
7. [outside-view] Hosted-class failure mode: opaque retrieval and plausible fabricated citations user can't audit; output 5–15% wrong invisibly; silent vendor behavior changes between runs. (confidence: inferred)
8. [outside-view] Claude-Code-native failure mode: 60–90 day window before Claude Code release changes subagent semantics / MCP protocol / default tool behavior, causing silent degradation; subagent fan-out blows context budget on long tasks. (confidence: inferred)
9. [outside-view] Open-source failure mode: stalls in "Valley of Death" — missing eval harness, tracing, retries, cost guards, prompt versioning, secret rotation; requires dedicated maintainer if shipped. (confidence: inferred)

## Authority-framed claims
None. The subagent cited sources by name and arXiv ID rather than ventriloquizing authors.

## Contradictions surfaced
- Verdict is conditional, not unitary: if success = "trustworthy reports for own consumption, low volume," hosted is within tolerance and build options (10–30%) sit well below it (40–55%). If success = "asset others invoke, audited, reproducible," all three classes fall below bar absent a citation-verification layer. The same option (e.g., hosted) can be above or below base rate depending on which success criterion the orchestrator picks.
- Claude Code update cadence is named simultaneously as a durability feature and a reproducibility risk.

## Subagent's own verdict (verbatim)
"Reference class unclear, conditionally below base rate for build options."

## Gaps the subagent missed
- No estimate for cost-multiplier of build vs hosted (token spend, infra cost) — only quality and durability rates.
- No reference class for "internal Claude Code stacks specifically used for adversarial review / decision support" (the user's actual context per CLAUDE.md), only generic research/report generation.
- Did not address what fraction of citation hallucinations are caught by existing per-claim verifiers (effectiveness of the proposed mitigation is unquantified).
- No base rate for the "frozen model+harness version pinned" mitigation — is pinning empirically feasible on Claude Code given the subagent's own claim that the harness changes every 60–90 days?
- No discussion of human-in-the-loop / review-gated pipelines as a fourth class.
- Source list is arXiv-heavy and 2026-dated; no triangulation against pre-2025 agentic-system literature or non-academic post-mortems beyond dev.to.

## Token budget
~720 tokens.
