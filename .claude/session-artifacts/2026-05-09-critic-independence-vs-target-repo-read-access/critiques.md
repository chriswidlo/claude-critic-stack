# Critic panel — aggregated verdicts

| Lens | Verdict | Lens-specific cut | Frame-level objection |
|------|---------|-------------------|-----------------------|
| architecture | **rework** | Move 3 places load-bearing inter-input invariant on orchestrator discipline at candidate-authorship time — same defect class as the clause it removes. Decision-log schema-creep, lens-isomorphism break, comparator semantics inverted by experiment. | Candidate is a *claim change* dressed as a *contract change*. Picks the architecturally weakest of three positions: smaller claim + same mechanism + unverifiable note. Pick (a) keep claim, remove veto; or (b) introduce typed-candidate / invariants-only / single-judge primitive. |
| operations | **rework** | No detector for any move. Decision-log opt-in is observation, not control. Step-10 invocation prompt is not archived → silent default-allow drift cannot be retro-audited. Rollback restores prose, not artifact state. | Every move is prose-enforced on a stack whose existing prose-enforced contracts already operate on the honor system. Before adding moves 2 or 3, name the detector. Logging is observation, not control. |
| product | **rework** | Marketing downgrade unhandled: no replacement handle for "three independent critics," no audit of where old phrasing leaks. Decision-log schema collision with step-11. Discipline note covers candidate.md but not question.md / explore.md. In-flight session grandfathering unspecified. | Move 1 is a product-copy change masquerading as a side effect. The load-bearing question is what story the stack tells users; the candidate treats that as architecture's job. "Decline the user's menu" is a posture choice and should be named, not smuggled. |

## Aggregate

**Unanimous rework. Three lenses, three vetoes.** No `approve` line.

Per CLAUDE.md step 11, any rework / reject veto routes to step 11. Three vetoes means three frame-level objections plus three lens-specific objections, all of which must be considered in the routing decision.

## Convergence

The three lenses converge on a single cross-cutting finding from different vantage points:

- **architecture says** the proposed primitives are not real primitives — they are prose.
- **operations says** there is no detector for whether the prose holds.
- **product says** the headline change (claim shrinkage) is being executed without product-level care for the existing claim's footprint.

All three identify the same defect class: **the candidate proposes contract changes that are not enforced and whose violations are not observable.** This is convergent across lenses, which under a strict reading of "minority-veto" is closer to a *unanimous structural objection* than to a minority-veto situation.

## Routing

The architecture and product objections are **frame-level** (architecture explicitly says move 1 is downstream of moves 2–4, not upstream; product explicitly says the panel's claim is not architecture's job to adjudicate). Operations is **design-level** but consistent with the frame-level reads (the design has no detectors *because* the frame conflates claim-change with contract-change).

This pushes the routing toward **replan**, not rewrite — return to step 7 (scope-mapper) or step 8 (frame-challenger) with the panel's actual options on the table:

- (a) keep the smaller claim, **remove minority-veto**, drop the panel-as-aggregator framing, accept that the three lenses produce three independent reports (no aggregation rule needed);
- (b) introduce one of the architectural primitives — typed candidate, invariants-only feed to operations, or single rubric judge — that would make a stronger claim true and verifiable.

Both directions are visible in the panel's critique. The candidate's middle path (smaller claim + same mechanism + discipline note) is what got vetoed.
