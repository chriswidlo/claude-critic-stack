# Critic-panel aggregate — Step-13 session ledger

| Lens | Verdict | Pre-merge requirements |
|---|---|---|
| architecture | rework | HTML-comment marker on schema; tighten decision definition; cross-link CLAUDE.md → schema |
| operations | rework | document bypass cases; define count-taking moment; CLAUDE.md instruction on ledger-required-or-bypassed |
| product | approve | adopt operations' 1–3 + citation-pattern-as-required-language |

## Minority-veto status
Two `rework`, one `approve`. **Veto fires.** Route to step 11.

## Frame-level objections (one per lens)
- **Architecture:** schema is replicated across three locations with no machine-readable link. Mitigate via HTML-comment marker convention (already used by the format-only state-transition-gate entry).
- **Operations:** orchestrator authorship at end-of-context is the *least reliable* moment in a session. Plan for #14 not landing on time; ship a fallback escape hatch.
- **Product:** ship-the-minimum risk: the rework requests, while correct, can slow this entry into competition with entry #14 — at which point #14 supersedes it. Pre-merge only the silent-failure preventers.

## Aggregate diagnosis
Both `rework` verdicts are **design-level, not frame-level**. The candidate's frame is intact (ship a paste-and-fill template, derive ratios, cite in synthesis). What's needed is tightening: counted items, bypass behavior, count-taking moment. Per CLAUDE.md step 11: *rewrite* (return to step 9 with objections in hand), not *replan* (no need to re-run scope-mapper or frame-challenger).

## Required next step
Loop 1 → loop 2: orchestrator rewrites candidate.md → candidate-v2.md addressing:
1. (architecture) HTML-comment marker on the schema section.
2. (architecture) Tighter "decision" definition.
3. (operations) Document bypass cases inline in schema.
4. (operations) Define the count-taking moment.
5. (operations) CLAUDE.md instruction on ledger-required-or-bypassed.
6. (product) Citation-pattern-as-required-language in CLAUDE.md.

Architecture's third item (cross-link CLAUDE.md → schema) and operations' optional `bin/ledger-from-session.sh` fallback are deferred (not pre-merge).

## Loop 2 (after candidate-v2)

| Lens | Verdict |
|---|---|
| architecture | approve |
| operations | approve |
| product | approve |

All three approve. Minority-veto does not fire. Proceed to step 12 (synthesis).
