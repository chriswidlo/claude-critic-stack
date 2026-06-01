# Adversarial review — AU-banking KB / topical-MCP-silo architecture

**Date:** 2026-06-01
**Mode:** adversarial. The instruction was *break it, don't confirm it.* Honest friction over politeness.
**Run as:** a lean orchestrator-direct critique — deliberately **not** a full 13-step re-run. See "Methodological stance" below.

## What was asked

1. Judge whether the prior research's "convergence" is real field consensus or correlated
   self-confirmation produced by one operator's parallel sub-agents. Cite outside sources.
2. Stress-test five claims and rank the weakest:
   - **(a)** hybrid-RAG + MCP + 3-layer grounding is right for a regulated, agent-consumed,
     point-in-time legal/financial corpus.
   - **(b)** build the full stack vs start from a BM25-only baseline and let an eval set earn
     each added component.
   - **(c)** BUILD rather than FEDERATE the law (the Federal Register of Legislation API is said
     to give point-in-time text free).
   - **(d)** MCP is the right interface for a single first consumer.
   - **(e)** the chosen anti-hallucination stack actually reduces hallucination on regulatory
     numeric/tabular claims.
3. Name ≥1 alternative architecture the research did not seriously consider.
4. Produce a concrete BETTER plan, or — if it can't be beaten — the strongest steelman of the
   leading alternative and the single condition under which it would win.

## Scope discrepancy (frozen as a finding, not silently corrected)

The request cited paths that **do not exist on disk**:
- `garden/specimen/2026-05-05-topical-mcp-silo-slot/research/` — there is no `research/` subtree.
  The specimen is a **single file**: [topical-mcp-silo-slot.md](garden/specimen/2026-05-05-topical-mcp-silo-slot.md).
- `research/07-recommendation.md` and `research/anti-hallucination/06-recommendation.md` — absent.
- numbered "axis files" and an entry `README.md` — absent.
- a literal "anti-hallucination stack" / "3-layer grounding" artifact — **zero** repo-wide hits
  (`grep -ri "anti-hallucination" / "3-layer grounding"` returns nothing).

The real research under review is the prior 13-step session
[2026-04-25-au-banking-kb-sota](.claude/session-artifacts/2026-04-25-au-banking-kb-sota/synthesis.md)
plus the specimen that generalized it. Claim 2(a)/(e)'s "3-layer grounding / anti-hallucination
stack" is therefore mapped to the architecture's **actual** components: Layer 3 (hybrid +
contextual retrieval + rerank), Layer 5 (citation + audit), and structured/table-aware ingestion.

**Why this matters as a finding:** an architecture being defended under a name
("3-layer grounding") that does not appear in its own artifacts is a sign the claim has drifted
from the evidence. The critique scopes itself to what is auditably on disk.

## Methodological stance — this is itself the answer to question 1

Re-running the full 13-step workflow (same base model, same near-empty canon, same vendor-blog
web corpus) to audit a 13-step output would **reproduce the exact correlated-self-confirmation
failure under examination.** The correct response to "is this real consensus?" is to import
**independent outside sources the original did not cite** — academic IR benchmarks and
faithfulness studies, not more retrieval-vendor marketing. That is what this review does.

## Artifacts in this review

- [inputs.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/inputs.md) — what was actually read
- [convergence-audit.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/convergence-audit.md) — question 1
- [claim-stress-test.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/claim-stress-test.md) — question 2
- [alternatives.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/alternatives.md) — question 3
- [revised-plan.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/revised-plan.md) — question 4
- [verdict.md](.claude/session-artifacts/2026-06-01-au-kb-stack-adversarial-review/verdict.md) — bottom line + steelman + self-flip conditions
