# Frame — Step-13 session ledger

## Revision 1

The user's framing: *"add a Step 13 that writes a ledger.md after synthesis, with counts, ratios, and warnings."* This is implementation-flavored — it presupposes the answer is "yes, write a file."

**Honest reframe:** the underlying question is *"how does this workflow produce its own audit trail without human-time/money estimates?"* The user has already proposed one answer (a file at step 13). The reframe asks whether that's the right shape.

### What the user is implicitly optimizing for
- **Self-diagnosis** — sessions where the workflow over-elaborates become detectable mechanically, not anecdotally.
- **AI-native units** — agent calls and artifacts (things the AI actually does) instead of money or human-hours (units that don't translate cleanly).
- **Low marginal cost** — the orchestrator already has the data; writing it down should be ~free.

### One alternative optimization the user did NOT name
**Cross-session pattern detection.** A single ledger per session is anecdote; the value compounds when you can scan a directory of ledgers and see *trends* (is the workflow drifting toward more loops? are critic vetoes getting more frequent?). Optimizing for this would push toward:
- Stable schema (so future scans don't re-parse different shapes).
- Plain-text grep-friendly format (markdown table over prose paragraph).
- Filename + location predictable enough that `find ... -name ledger.md` works.

The user's framing is consistent with this but doesn't name it. The synthesis should make the cross-session aggregation case explicit and design for it from the start, even if no aggregator script ships in this entry.

### Friction-honest observation
The proposed thresholds in the entry (10 / 8 / 2) are guesses without empirical grounding. The entry acknowledges this ("starting heuristics; the day-90 review should empirically calibrate"). That is fine — but it should not become an excuse to ship a schema that is hard to revise. The schema's first job is to be *cheaply revisable* once real data shows the thresholds are off.

### Where the framing might be weak
- Treating "decisions" as countable. A synthesis can name 1 recommendation but contain 5 sub-decisions (which agents to invoke, which tier the entry should be in, etc.). The ledger should probably count *the explicit recommendation* as 1 — anything else is over-counting.
- "Loops to convergence" pretends convergence is binary. A session that hits the loop cap (2/2) and synthesizes-with-disagreement is a different beast from one that converges naturally at loop 1. The ledger needs a loop-cap-reached flag, not just a count.