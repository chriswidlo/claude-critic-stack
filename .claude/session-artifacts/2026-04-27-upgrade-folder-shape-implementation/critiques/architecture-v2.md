# Architecture lens — loop 2

**Verdict:** `approve`

**One-line:** v2 cleared all three loop-1 flip-conditions (counter dropped, `bin/` eliminated, LEDGER's "what is it" sidestepped honestly via no-write commitment); strangler rule introduces a real but acceptable mixed-concern in the gate.

## Loop-1 flip-conditions
- (a) Counter out of LEDGER: yes, eliminated entirely.
- (b) Top-level `bin/` justified or eliminated: eliminated.
- (c) "What is LEDGER.md?" sidestepped honestly via "tooling does not write to LEDGER" commitment.

## Residual concerns (non-blocking)
1. **Gate gains second concern** (path-shape on top of body schema). Strict reading violates "format-only" identity; generous reading defends it. Needs documentation in gate's own README.
2. **README.md filename collision** between `upgrades/README.md` (lab overview) and `upgrades/<tier>/<slug>/README.md` (entry doc). Tools that recurse `find -name README.md` mix them.
3. **Permanent flat-shape tail at 🌱** — entries that never advance never migrate. v2 calls this "right outcome"; should be documented in `upgrades/README.md`.
4. **Validator → policy enforcement point semantic shift** (frame-adjacent). Real but becomes a problem at rule #3 or #4, not rule #2.

## What would flip to reject
A second operator joining the lab (voluntary enforcement breaks); any future rule added to the gate inheriting policy-enforcer framing without flagging the accretion.
