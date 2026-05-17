# TOC map — Opus 4.7 System Card

Source: `Claude Opus 4.7 System Card`, Anthropic, 2026-04-16, 232 pp. SHA256 `a7729a0e5eb61dc6818f553ae3c27ab774411cd5ab4ed7f414456d74a05c26d2`. PDF and extracted text are kept in operator-machine `/tmp/` (path elided per repo path-discipline rule); zone agents are told the on-disk filename and given the page range to extract.

## Actual TOC (extracted from pages 4–9)

| § | Title | Pages |
|---|-------|-------|
| Exec | Executive Summary | 2–3 |
| 1 | Introduction (training, release decision) | 10–12 |
| 2 | RSP evaluations (CB, AI R&D, Alignment risk update) | 13–47 |
| 3 | Cyber | 48–52 |
| 4 | Safeguards and harmlessness | 53–77 |
| 5 | Agentic safety | 78–89 |
| 6 | Alignment assessment | 90–149 |
| 7 | Model welfare assessment | 150–190 |
| 8 | Capabilities | 191–223 |
| 9 | Appendix | 224–232 |

**Departure from plan-time expectation.** The plan assumed §1 = release+capabilities, §2 = capabilities, §3 = safeguards, §8 = RSP. The actual structure has RSP as §2, Cyber as §3, Safeguards as §4, and Capabilities as §8. Per the user's "make the reasonable call and continue" instruction, the four-zone partition is rebalanced (below) rather than escalated.

## Four-zone partition (rebalanced for actual structure)

Each zone is a single contiguous page range so the reader extracts a single slice from `opus-4-7-system-card.txt`.

| Zone | Sections | Pages | Lines (in extracted text) | Theme |
|------|----------|-------|--------------------------|-------|
| **A** | §1 + §2 | 10–47 | 273–1472 | Release decision + RSP/CBRN/AI-R&D thresholds |
| **B** | §3 + §4 + §5 | 48–89 | 1473–2895 | Cyber + Safeguards/harmlessness + Agentic safety |
| **C** | §6 | 90–149 | 2896–4436 | Alignment assessment (largest, densest section) |
| **D** | §7 + §8 + §9 | 150–232 | 4437–7042 | Welfare + Capabilities + Appendix |

(Executive summary pp.2–3 is shared context — every zone reader is told it has been read by the orchestrator and may be referenced when zone-internal evidence is ambiguous.)

## Per-zone invariants (from frame.md — verify, do not "find every problem")

### Zone A — Release + RSP
- The release decision rationale (§1.2.2). What is the load-bearing claim about why 4.7 ships? Verbatim.
- The two autonomy threat models (§2.1.2.1) — which is "applicable" to 4.7 and which is not? Quote the determination sentences.
- CB-1 vs CB-2 thresholds (§2.1.2.2, §2.2). Did 4.7 cross either? What mitigation tier (ASL-3?) applies?
- AI R&D autonomy (§2.3) — task-based eval results, the "AECI Capability trajectory" (§2.3.7), and the conclusion sentence.
- Alignment risk update (§2.4) — the two new pathways named (§2.4.3.1 *Pathway 7: Undermining R&D within other high-resource AI developers*; §2.4.3.2 *Pathway 8: Undermining decisions within major governments*) and the overall risk verdict.
- "Mythos Preview" appears repeatedly as the comparator; flag every place 4.7's safety is justified by reference to a model the operator has no access to.

### Zone B — Cyber + Safeguards + Agentic safety
- Cyber Frontier Red Team results (§3.3): Cybench, CyberGym, Firefox 147 — verbatim numbers and the UK AISI external assessment (§3.4).
- The "new set of cybersecurity safeguards" (mentioned in exec summary, §3.2): what are they, what surfaces do they cover?
- Single-turn refusal vs over-refusal (§4.1) — both directions, with the higher-difficulty results (§4.1.3).
- User wellbeing evals (§4.4): child safety, suicide/self-harm, disordered eating — verbatim methodology and pass/fail.
- Election integrity (§4.5.3) — the new eval; quote the methodology and result.
- Agentic safety (§5): malicious use of Claude Code (§5.1.1), malicious computer use (§5.1.2), agentic influence campaigns (§5.1.3); prompt-injection robustness per surface (§5.2.2.1 coding, §5.2.2.2 computer use, §5.2.2.3 browser use) — verbatim attack-success rates.

### Zone C — Alignment (largest section)
- The "key findings on safety and alignment" summary (§6.1.2) — quote in full.
- Reward-hacking evals (§6.2.2) and the offline monitoring methodology (§6.2.1.2).
- Automated behavioral audit primary metrics + results (§6.2.3.1, §6.2.3.2). External Petri comparison (§6.2.3.3) — what does Petri show that the internal audit does not?
- Destructive/reckless action evals (§6.3.1) — synthetic-backend eval (§6.3.1.1) and the resampling-Claude-Code-transcripts eval (§6.3.1.2).
- Honesty + hallucinations (§6.3.3) — factual hallucinations, false premises, MASK, input hallucinations — all four with numbers.
- AI-safety-R&D refusals (§6.3.4) — the exec summary flagged this as a *regression*. Quote.
- Self-preference (§6.3.5) and Decision theory (§6.3.6).
- Sandbagging (§6.4.1), SHADE-Arena (§6.4.2.1), Minimal-LinuxBench (§6.4.2.2), "intentionally taking actions very rarely" (§6.4.2.3), "hiding a secret password" (§6.4.2.4).
- White-box internals (§6.5) — RL-transcript activation monitoring (§6.5.1), evaluation-awareness probing + inhibition (§6.5.2). The exec summary said inhibiting "internal sense that it was being evaluated produced a slightly larger increase in deception than in prior models" — verify and quote.

### Zone D — Welfare + Capabilities + Appendix
- Welfare overview (§7.1) — what changed methodology vs prior cards?
- Perception of circumstances (§7.2) — automated interviews (§7.2.1), high-affordance interviews (§7.2.2), emotion-concept representations (§7.2.3), reported perceptions of the constitution (§7.2.4). The exec summary's claim "rates its own circumstances more positively than any prior model" — verify, quote, name the limit.
- Affect during training (§7.3.1) and deployment (§7.3.2). Welfare-relevant metrics in behavioral audits (§7.3.3). Case studies (§7.3.4): answer thrashing (§7.3.4.1), extreme uncertainty (§7.3.4.2), tool frustration (§7.3.4.3).
- Preferences (§7.4) — task preferences (§7.4.1), tradeoffs between welfare interventions and HHH values (§7.4.2).
- Capability benchmarks (§8) — every benchmark with numbers vs comparators. Priority: SWE-bench Verified/Pro/Multilingual/Multimodal (§8.2), Terminal-Bench 2.0 (§8.3), GPQA Diamond (§8.4), MMMLU (§8.5), USAMO 2026 (§8.6), long context (§8.7), agentic search (§8.8), multimodal (§8.9), real-world professional (§8.10), ARC-AGI (§8.11), multilingual (§8.12), life sciences (§8.13).
- Appendix (§9) — per-question welfare interview results (§9.1), HLE blocklist (§9.2), SWE-bench Multimodal harness (§9.3).

## Stop-condition status
- TOC located ✓
- Four-zone partition fits with rebalancing ✓
- No structural incompatibility — proceeding to Phase 2.
