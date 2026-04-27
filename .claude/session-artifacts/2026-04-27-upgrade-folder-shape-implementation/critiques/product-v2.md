# Product lens — loop 2

**Verdict:** `rework` (lone holdout — architecture and operations both approved)

**One-line:** v2 cleanly addresses both my flip conditions (slug decided, three open questions reduced to one), but the orchestrator overcorrected — silently revises what the operator accepted (batch+`bin/` script) into a strangler that changes day-1 product reality without flagging that as a re-accept event.

## Loop-1 flip-conditions
- (a) Slug-vs-README.md decided NOW: yes, binding recommendation in v2.
- (b) Three open questions → one: yes.

If the critique stopped at loop-1's text, this is approve. It does not.

## Day-1 reality the operator gets vs what they accepted

**Accepted:** "run a script, one Sunday afternoon, ~30 min, lab is uniformly shaped."

**v2 ships:** "lab is mixed-shape for weeks-to-months (or forever for cold entries); gate refuses per-entry as you touch them; you migrate by hand each time; you remember a `find` one-liner to know your migration state."

These are *qualitatively different products*. Both can be defended. Only one was accepted.

## Commitments v2 makes that v1 did not
- Gate gains a third concern (path-shape) — once gate is migration enforcement surface, peeling that back later strands entries.
- Mixed-shape becomes long-lived steady state, not transient. Anything reading `upgrades/` handles both shapes indefinitely for entries that never advance past 🌱.
- The `find` one-liner becomes the operator's only window into "where is the migration." That's a contract: "to know your state, type this."

V2 trades a one-time script-shaped commitment for a permanent contract-shaped commitment. Candidate calls it "smaller surface" — on code-line count, yes; on contract surface, not obviously.

## Pruned affordances v2 doesn't credit
- **Lab uniformity given up indefinitely**, not "for one sitting." Candidate undersells duration ("weeks/months" — for cold entries, *forever*).
- **Operator loses the "I am done with the migration" moment.** v1 had a clear terminal state; v2 has none.
- **Gate becomes a forcing function for unrelated work** — operator wants to advance an old flat entry to 🔬 spiked → must first do a `git mv` they didn't intend to do this session. v1's batch separated these concerns; v2 entangles them.

## Frame-level objection
**The candidate frames the rewrite as "smaller surface, more honest commitments," but the operator-felt frame is "you changed what I accepted without telling me I'm being asked to re-accept."** Unit of change is not lines of code or directories created — it is the *experience contract* the operator pressed accept on.

**Second frame:** the orchestrator escalated the wrong decision. Slug-vs-README.md got presented as the single open question. Strangler-vs-batch is *also* a binding decision in v2 but is silently adopted. The single open question should arguably have been "do you still want batch, or do you accept strangler?" not slug-vs-README.

## What would flip to approve
Surface the strangler-vs-batch revision as the headline operator-facing question (alongside or instead of slug-vs-README.md), and explicitly name that v2 is asking the operator to revise their accept rather than implementing what they accepted.
