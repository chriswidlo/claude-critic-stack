# Critic panel — aggregate verdict

Session: `2026-04-26-upgrades-lab-design`. Step 10. Three lenses ran in parallel; full critiques persisted in `critiques/<lens>.md`.

## Verdicts

| Lens | Verdict |
|---|---|
| architecture | **rework** |
| operations | **rework** |
| product | **rework** |

Per CLAUDE.md minority-veto: any rework routes to step 11. Three rework verdicts mean we cannot proceed to synthesis under the current candidate.

## Convergent frame-level objections

The three lenses approached the candidate from independent angles but converged on a single underlying problem: **the candidate over-builds new structure when the operator's actual problem and the existing repo's actual structure both call for less.**

Specifically:

- **Architecture (frame-level objection):** the lab is structurally a *capability-overlay on `.claude/session-artifacts/`*, not a peer module. Every "lab entry" is in form a session-artifact that has outlived its session. Recommendation: lab should be a promotion target with the same structure as session-artifact directories, governed by the same conventions. Locking-dimension count drops from 4 to 1 (the promotion rule); integration protocol drops from 3 ports to 1 (the promote operation).

- **Product (frame-level objection):** the candidate has framed the operator's problem as "design a structure that survives" when from product the problem is "have somewhere I can write that doesn't punish me for writing." Candidate is a publication system, not a lab. R&D lab without a lab-notebook surface is a journal. Frame should make capture-affordance a locking dimension and let publication-affordances be reversible.

- **Operations (frame-level objection):** the frame's load-bearing controls (day-60 falsifier, day-7 freeze, curator-as-monopoly) are uninstrumented and contradictory. Either extend the frame with three named operational primitives (falsifier-script, freeze-break-glass, curator-bootstrap-protocol) before ratifying, or honestly downgrade to "best effort." Current candidate sits in unviable middle: load-bearing controls that are not instrumented are *worse* than no controls — they license false confidence.

## Convergent reading

Architecture and product are saying the same thing from different angles: **less new structure, more accommodation of what already happens.** The operator already writes in `.claude/session-artifacts/`, in `pages/`, in `plans/`, in `tests/regression/`. The lab should not impose a parallel publication-grade structure; it should overlay a thin promotion/capture pattern on what already exists.

Operations adds: even the thin structure that *does* get committed must have its survival controls actually instrumented, or it is theatre.

## Routing decision (Step 11)

**Replan, not rewrite.**

Two of three frame-level objections (architecture, product) point at the frame itself. The candidate is generated against a frame that the panel rejects. Rewriting the candidate under the same frame would not address the convergent objection. The frame must be revised first.

Specifically, return to step 8 (frame-challenger) under a revised frame:
- Lab as capability-overlay on existing session-artifact + capture-first surface, not peer-module + publication system.
- Reduce locking dimensions to the minimum that actually requires fidelity-design (likely 1–2: the promotion rule, and a slug-based stable-ID scheme).
- Make the inbox/express-capture path a locking dimension (per product), and let document-type taxonomy and maturity ladder be views/tags over the same primitive.
- Operations controls (falsifier instrumentation, break-glass, curator-bootstrap) become required design outputs of the next pass, not §Tradeoffs concessions.

Frame revision will be appended to `frame.md` as `## Revision 2`. New candidate written under that frame.

This is loop 1 of 2 per the CLAUDE.md cap. If the next pass also produces convergent rework, synthesis must escalate with disagreements named.
