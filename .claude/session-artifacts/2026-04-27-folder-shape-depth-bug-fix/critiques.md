# Critic panel aggregate — folder-shape depth bug fix (item 2)

| Lens | Verdict | Frame-level objection (one-line) |
|------|---------|----------------------------------|
| Architecture | **rework** | The candidate frames this as bookkeeping over punch-list strings; the architecturally honest frame is graph-edit on a documentation graph with edges that need per-edge-class validation. |
| Operations | **rework** | Candidate treats this as content correctness solved by one commit + one grep; the operational frame is "no standing verification regime for link health in this repo," and ship-and-grep converts a one-time CI cost into an N-time async cost. |
| Product | **rework** | Operator attention is the product; the apparatus's own self-disclaimer ("won't run on items 4-13") concedes it is not the right tool, and adding r-and-d-lab-thesis as a new punch-list line mutates the punch-list from finite contract to open backlog. |

## Aggregate
**Three lenses, three reworks.** Per CLAUDE.md step 11: any rework triggers replan-vs-rewrite decision. All three objections are design-level (specific, actionable lens-objections with named flip-to-approve conditions), not frame-level — so the route is **rewrite**, returning to step 9 with the lens objections in hand.

## Common thread
The three reworks converge on **verification weakness + scope mutation that pushes cost downstream**:

- All three lenses identify the verification step as inadequate (architecture: single-sided invariant; operations: no resolution check; product: implicit reliance on operator's later click as the validator).
- Two of three (architecture, operations) name the same fix: a real link-resolution check shipped with this commit, either as a one-shot run or as `bin/check-path-discipline.sh` co-shipped with item 2 instead of routed to item 1.
- Two of three (product, architecture) name the punch-list-as-contract concern: product objects to appending r-and-d-lab-thesis; architecture objects to bundling item 3 with item 2 even though scope-map endorsed it.

## Lens-specific flip-to-approve conditions (combined)
1. **Resolution check shipped with item 2.** Either (a) one-shot link resolver run locally before commit *for the 3 files* (operations + architecture), or (b) `bin/check-path-discipline.sh` co-shipped with item 2 to give item 1 a tested artifact (architecture preferred path).
2. **Inbound-link audit before commit** (architecture).
3. **Single source for the verification regex** shared between item 1 and item 2 (architecture).
4. **R-and-d-lab-thesis disposition decided cleanly:** include in sweep OR truly defer with no punch-list mutation (product).
5. **Bundling-by-colocation declared one-time** in the commit message and on the punch-list line itself, not precedent (product).

## Decision
**Rewrite.** Return to step 9 with these conditions as the rewrite brief.

## Loop 2 — v2 panel review

| Lens | v1 verdict | v2 verdict | Notes |
|------|-----------|-----------|-------|
| Architecture | rework | **approve** | All three flip conditions met. Frame objection ("direction is wrong way") not addressed; recorded as disagreement, not blocker. |
| Operations | rework | **approve** | Both flip conditions met (resolution check shipped; verification regime decoupled from item 1 by inversion). New script-class risk acknowledged and bounded. |
| Product | rework | **approve** | Both flip conditions met. Deferral surface for r-and-d-lab-thesis is acknowledged-weak (commit message). |

**All-approve.** Proceed to step 12 (synthesis).
