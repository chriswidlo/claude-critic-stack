# Question 4 — The better plan (an "earn-it" ladder)

The revised plan keeps what survived the stress-test (provenance contract, structured metadata,
hybrid *as an option*) and removes what didn't (full-stack-up-front, MCP-for-one, retrieval-depth
as the anti-hallucination story). The organizing principle is the one the research stated and
then abandoned: **build the eval first, then make every component earn its place on that eval.**

## The ladder

```
 Stage 0  EVAL + PROBE (days, not weeks)
   - 200-pair version-anchored gold set: (query, instrument, section, version, expected answer)
   - >= 30% of pairs are NUMERIC/TABULAR with a faithfulness check (exact value, not "relevant")
   - 1-day API-capability probe: FRL / APRA / ASIC / AUSTRAC -- point-in-time queryable? (y/n)
        |
        v
 Stage 1  STRUCTURED + BM25, IN-PROCESS  (the baseline that must be beaten)
   - relational store keyed by (instrument, section, version, effective_date, supersedes)
   - point-in-time = WHERE clause; "what changed" = diff query; tables stored as cells
   - BM25/FTS as a column for fuzzy clause-finding
   - citation-by-construction: verbatim spans + byte offsets; numbers quoted, never paraphrased
   - exposed as an in-process tool / in-stack Agent (the canon-librarian shape). NO vector DB, NO MCP server.
   - legislation subset: federate from FRL IFF Stage-0 probe confirmed a point-in-time API; else ingest
   - MEASURE on the Stage-0 eval. This is the number every later stage must beat.
        |
        v
 Stage 2  ADD DENSE HYBRID  (only for query classes Stage 1 misses)
   - dense + RRF over BM25, added only where the eval shows semantic-recall misses
   - re-measure; keep only if the lift clears a pre-set threshold
        |
        v
 Stage 3  ADD ON DEMAND, EACH GATED BY A NAMED EVAL GAP + A REAL TRIGGER
   - contextual retrieval ......... iff Stage-2 still misses on cross-reference context
   - cross-encoder rerank ......... iff precision@k is the measured bottleneck
   - GraphRAG ..................... iff eval shows >= 20% multi-hop/supersession-chain queries
   - MCP-over-HTTP ................ iff a SECOND, out-of-process consumer becomes real
```

## What this changes vs the original (claim-by-claim)

- **(e):** numeric faithfulness is handled by Stage-1 citation-by-construction + a Stage-0 eval
  metric that *measures* it — not by retrieval-stack depth. The anti-hallucination claim becomes
  testable instead of asserted.
- **(b):** the full stack is no longer pre-committed; each component is admitted only by beating
  the Stage-1 baseline on the eval. The principle the research stated is now actually enforced.
- **(c):** "build vs federate the law" becomes a Stage-0 *fact* (the probe), not a default. The
  legislation subset federates only if a point-in-time API exists; everything else builds.
- **(d):** in-process first; MCP-over-HTTP is a Stage-3 trigger tied to a second consumer, not a
  day-one cost.
- **(a):** preserved — provenance contract and structured metadata are *in Stage 1*, where they
  do the most regulated-text work for the least cost. Hybrid is kept, but demoted from "floor you
  must build past" to "Stage-2 option you earn."

## What it preserves from the critics' fold-ins

The architecture-critic's `Instrument`-as-aggregate-root, the ACL between regulator taxonomy and
agent tool names, and content-hashed citations
([critiques.md](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/critiques.md)) all land
naturally in the Stage-1 relational schema. The operations-critic's quarantine/superseded/
retracted state machine *is* a column set + status enum in that schema, not a bolt-on. The
relational-first frame makes those fold-ins cheaper, not more expensive.

## Steelman of the original (full-stack-now) + the single condition under which it wins

**Steelman:** if the consuming agent is a high-value compliance/legal workbench (not retail
Q&A), the corpus is dominated by cross-instrument multi-hop defined-term resolution, and the
organization must present a single answerable "source of truth" noun to a regulator on a fixed
date, then the incremental eval-driven ladder is *too slow*: it optimizes retrieval accuracy
while the actual binding constraint is organizational/regulatory legitimacy delivered by a
deadline. In that world, building the provenance-rich catalog + hybrid + rerank + MCP surface up
front is rational, because "we are still earning components on an eval" is not an answer you can
give an auditor in week 3.

**The single condition under which the original beats my ladder:**
> **When the binding constraint is an external audit/procurement deadline, not a quality target.**

If success is "pass the audit / win the funding by date D" rather than "answer queries correctly,"
build-it-all-now wins, because legitimacy is bought by the *visible, complete artifact*, not by
the eval curve. Absent that deadline — i.e., whenever correctness is the real objective — the
earn-it ladder dominates on cost, faithfulness, and reversibility.
