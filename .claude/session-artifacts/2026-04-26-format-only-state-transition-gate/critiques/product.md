# Product lens — critic-product

**Verdict:** `reject`

**One-line summary:** The candidate answers "should we build a gate?" when the operator asked "design the gate." Phase 0 ships zero gate-shaped affordance on day 1, leaving the named failure mode (AI drift on transitions) entirely unconstrained for the six-week observation window.

## Day-it-ships test
- **Day 1 of Phase 0:** operator gains a script that prints a Markdown table to stdout. README, entry format, advancement flow, `/upgrade` behavior — all unchanged. From the operator's seat, *nothing has happened*. The thing the operator asked for does not exist.
- **Day 1 of Phase 2 (if it ever ships):** README sentence "*There is no automation; manual act*" becomes false. "Lifecycle is descriptive not prescriptive" becomes false. Operator and AI must route every advancement through `/advance-upgrade`. Direct table editing — currently the *only* documented path — is silently obsoleted.
- **Worst part:** the AI agent the operator was worried about gets zero new constraints during Phase 0 and Phase 1. The named failure mode is exactly as unconstrained as before.

## Commitments implied
- Phase 0 commits to maintaining the audit script's schema as the lab's writing template evolves. Schema-in-script is still schema; calling it implementation does not absolve it.
- Phase 0 commits to "audit-first, defer feature" as a precedent. Next time the operator asks for X, the workflow has a worked example of "we audited, deferred, X never shipped" — which is the workflow-overdesigns failure mode one abstraction layer up.
- Phase 2 implies a permanent two-provenance regime in the corpus (pre-Phase-2 entries advanced by hand; post-Phase-2 entries advanced by command).

## Migration burden (Phase 2 if reached)
- README rewrite (line 141 + how-to-add list).
- `/upgrade` doc parallels with `/advance-upgrade` doc.
- 22 historical entries' state tables retroactively "incorrectly produced."
- Operator muscle memory: zero ceremony → command + entry-path arg + new-state arg.
- Every prior CLAUDE.md / session prompt that references manual advancement becomes stale.

## Affordances better / worse
**Better (Phase 0):** read-side capability "what state is everything in" in one command.
**Worse (Phase 2):**
- Lose smallest-possible-ceremony advancement (the lab's stated design value).
- Lose batch advancement (open N files, edit N dates).
- Lose AI-agent-as-side-effect advancement (advancing the state table in the same diff as implementation).
- Lose the **descriptive-not-prescriptive** stance the README explicitly defends — "honest negation" no longer first-class.

## Frame-level objection
**The candidate treats this as a process question (what phasing reduces risk?) when it is a contract question (what does the lab promise about state advancement?).** The lab today has a clear small contract: 8 states, dates row, manual edits, descriptive-not-prescriptive. Phase 0 preserves it; Phase 2 replaces it; the candidate gives itself permission to defer the choice for six weeks. That is not a phased rollout — it is a **deferred contract decision**, and contract decisions get more expensive to defer.

**Second frame objection:** the candidate treats "the operator might not need a gate" as a discoverable fact and "the operator asked for a gate" as a starting hypothesis to be falsified. The operator's stated ask is data about what the contract should say. Replying "let's measure whether you really want it" is the workflow doing what the operator filed the entry to constrain.

## What would flip to approve
A candidate that ships *something gate-shaped on day 1* — even minimal: the `/upgrade` command, when invoked with an existing entry path, runs a presence check on the body and **warns (not blocks)** about missing sections for the entry's current state. Responsive to the operator's literal ask, honestly format-only, no README rewrite, no retiring of manual-edit path, generates same Phase-1 evidence as a side effect of the gate working — not as precondition for the gate existing.
