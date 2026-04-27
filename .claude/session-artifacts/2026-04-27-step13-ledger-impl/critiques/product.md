# Critic — product lens

> Orchestrator-authored stand-in.

## Frame-level objection
The candidate is solving the right problem (workflow self-diagnosis) with a reasonable solution (counts + ratios + warnings). My frame-level concern is the opposite of architecture's: **this is good enough; do not add anything before shipping.** The architecture critic wants HTML-comment markers and tighter decision-counting. The operations critic wants bypass-case documentation and a fallback script. Both are correct in their lens, but together they risk this entry sliding from a "ship now" state to a "wait until #14 is shipped, the schema-as-types is added, and the example is rendered" state — at which point the entry has been replaced by entry #14.

The product judgment is: **ship the minimum coherent thing now; let real sessions tell us which additions matter.** The entry currently *has* the minimum coherent thing. The mitigations from architecture and operations are good additions, but only ones that prevent silent failure (operations #1, #2, #3) are pre-merge. The rest can ship later.

## Weakest link from a user-value perspective
**The ratios are not the product; the warnings are.** A user (operator) reading "agent-calls=14, artifacts=22, loops=2/2" and "warnings: artifacts-per-decision above threshold (consider whether documentation is exceeding decisions)" cares about the second clause — the warning that suggests an action. The counts and ratios are the receipt; the warning is the work product.

The candidate's `## Warnings` schema is good — the warnings are written in actionable language ("consider whether..."). But the *thresholds* that drive the warnings are guesses. The first 3-5 sessions will likely either (a) all trigger warnings, making them noise, or (b) trigger no warnings, making the system silent. Either way, the operator must be ready to tune.

## Specific actionable suggestions
1. **Ship the entry now** with operations' pre-merge items 1–3. Defer architecture's HTML-comment marker to a follow-up edit (cheap, but not pre-merge).
2. **Write the threshold-tuning instructions inline** in the schema section: "After 5 ledgers, review the distribution; if all sessions trigger warnings, raise thresholds; if no sessions trigger, lower."
3. **Make the synthesis citation pattern *required-and-checked*.** A sentence in CLAUDE.md: *"The final line of synthesis.md must be in the form `Ledger: ...`. A session without this line is incomplete."* Without enforcement-as-language, citation will be the first thing to drift.
4. **Resist all other additions until 5 ledgers exist.** The entry's value is mostly in the *first 5 sessions of data*; over-designing before that data exists is the failure mode the entry is meant to detect (workflow-overdesigns-when-told-to-underdesign).

## Verdict
**approve** — with a strong recommendation to incorporate operations' pre-merge items 1–3 and product's recommendation 3 (citation-pattern-as-required-language). Architecture's HTML-comment marker is a clean follow-up but not pre-merge. Defer all schema enrichment until 5 real ledgers exist.
