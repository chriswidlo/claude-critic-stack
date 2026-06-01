# Verdict

**Revise, not confirm — but the revision is sequencing and labeling, not a teardown.**

The prior architecture is directionally defensible and was produced by a process that fought
itself harder than the user's framing credits (unanimous critic veto, prescription demoted to
appendix, self-flagged thin canon). What it got wrong is real and fixable:

1. Its **evidence base is correlated** — a near-empty canon forced reliance on a single
   incentive class (retrieval-vendor marketing), anchored by one self-serving Anthropic
   benchmark on the wrong domain. Treat the component list as one estimate, not consensus.
2. Its **anti-hallucination claim (e) is mis-aimed** — it optimizes retrieval recall, which
   independent research (arXiv 2505.04847) shows barely predicts numeric faithfulness. This is
   the weakest of the five claims and the most consequential for banking.
3. It **violated its own eval-first principle (b)** by pre-committing the full stack before any
   eval point existed. BEIR says the BM25 baseline the user wanted is genuinely strong.
4. It **over-generalized "build the law" (c)** and **adopted MCP a consumer too early (d)**.

The better plan is the **earn-it ladder** in
[revised-plan.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/revised-plan.md):
Stage-0 eval+probe → Stage-1 structured/relational + BM25, in-process, citation-by-construction →
add hybrid / contextual / rerank / GraphRAG / MCP only as the eval and a real trigger earn them.
The most-missed alternative is **relational-first** ([alternatives.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/alternatives.md)):
point-in-time legal lookup is a database problem, not a semantic-retrieval one.

The original wins under exactly **one** condition: when the binding constraint is an external
audit/procurement **deadline**, not a quality target — legitimacy bought by a complete visible
artifact beats an eval curve an auditor won't wait for.

## Assumptions that would flip THIS critique (applying the rule to myself)

1. **The query mix is dominated by fuzzy semantic recall, not structured point-in-time lookup.**
   If most real queries are "explain the intent of the responsible-lending obligations" rather
   than "what was the LVR cap in APS 223 as at 2024-07," my relational-first alternative loses its
   edge and the original's semantic stack is closer to right. *Resolved by the Stage-0 gold set.*
2. **Numeric/tabular faithfulness turns out to be retrieval-bound after all for this corpus.**
   arXiv 2505.04847 is a general finding; if on AU regulatory text the dominant numeric error is
   "fetched the wrong/superseded chunk" rather than "misread the right one," then better retrieval
   *does* fix it and claim (e) is stronger than I rated. *Resolved by error-typing the eval failures.*
3. **An external audit/procurement deadline is in fact the binding constraint.** If so, my own
   steelman fires against me and the full-stack-now plan is correct. I am assuming correctness,
   not a deadline, is the objective — the user never stated which.
4. **A second consumer is imminent.** If the silo is genuinely about to be shared cross-team (the
   specimen's "slot" thesis), the MCP-for-one objection (d) weakens, because you'd pay the HTTP
   cost within weeks anyway.

If 1–4 are mostly true, the gap between my plan and the original narrows to "build the eval and
measure" — which both plans should do regardless.

## Process note

This was run as a **lean, orchestrator-direct critique**, not the full 13-step workflow — by
design (see [question.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/question.md)
"Methodological stance"): re-running the same machinery would reproduce the correlated-evidence
failure under audit. No sub-agents; independent academic/third-party sources were imported as the
anti-correlation control. The ledger below is hand-tallied (no diagnostics binding for a
non-workflow critique) and is informational only.

Ledger (informal): web-searches=5, web-fetches=1(403), artifacts=7, loops=0; sub-agents=0 (by design); warnings: evidence-base-correlated, FRL-API-unverified, single first-consumer-assumed.
