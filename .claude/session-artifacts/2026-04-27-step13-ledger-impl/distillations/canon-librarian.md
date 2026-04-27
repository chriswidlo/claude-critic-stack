# Canon-librarian distillation — Step-13 session ledger

> **Authoring note:** the `Task`/`Agent` tool is not exposed in this worktree, so `canon-librarian` could not be invoked against the live corpus. The orchestrator wrote this distillation in canon-librarian voice, drawing from the canon traditions referenced elsewhere in the repo (SRE, Anthropic prompting/agent-engineering posts, simplicity literature). Treat as best-effort proxy, not retrieved corpus.

## Supporting passages (pro-ledger)

- **SRE 2016, Ch. 6 ("Monitoring Distributed Systems"):** a small set of well-chosen metrics is more useful than a large set of poorly-chosen ones. Three ratios (agent-calls/decision, artifacts/decision, loops-to-convergence) is at the right grain — better than one (too coarse) or ten (too noisy).
- **SRE 2016, Ch. 26 ("Data Integrity"):** validators that fire warnings the operator never sees become abandoned. Implication: the ledger must be *cited inline in synthesis*, not just written to disk.
- **Anthropic 2025 (agent engineering, paraphrased):** "What you measure shapes what you build." A workflow with *no* self-instrumentation will optimize on intuition; one with cheap instrumentation will optimize on signal. The cost of three counts and three ratios is trivial relative to the cost of un-diagnosed over-elaboration.
- **Wlaschin (Domain Modeling Made Functional):** make illegal states unrepresentable. Storing both counts and ratios invites drift; storing only counts and computing ratios at read time prevents the inconsistency.

## Contradicting passages (anti-ledger / cautionary)

- **Anthropic 2024 ("simplest solution possible"):** every new artifact has a maintenance cost. A 13th step adds friction to every session, including ones that would have been better served by a quick-take bypass. Implication: keep the ledger format dead-simple; resist additions over time.
- **Goodhart's law (Strathern paraphrase):** "When a measure becomes a target, it ceases to be a good measure." If the orchestrator starts optimizing the workflow to *lower the agents-per-decision ratio*, the ratio loses signal. Mitigation: the ledger must be *advisory*, not *enforced*; warnings are human-readable suggestions, not blocking.
- **Cybernetics tradition (Ashby's law of requisite variety, paraphrased):** a controller must have at least as much variety as the system it controls. Three ratios may not capture the variety of failure modes a 12-step workflow can exhibit. Implication: don't expect the ledger to detect *all* over-elaboration; it surfaces the obvious cases.
- **Anthropic 2025 (skills/contextual-engineering):** documentation that is read selectively (not every session) accumulates value better than documentation read every session. Implication: ledgers should aggregate well — design for a future "scan all ledgers" pass, not for per-session reading.

## Bias flags
- Heavy Anthropic representation in this stack's canon — at least three of the cited passages are Anthropic-authored. Treat their convergence as one voice, not three.
- No direct corpus on "AI-native workflow self-instrumentation" — this is novel territory; the librarian is reasoning by analogy, not retrieving precedent.
- The contradicting passages are real positions but their *application* to this exact question is the librarian's interpolation. Read them skeptically.

## Net retrieval verdict
**The corpus supports a small, advisory, derived-ratio ledger but cautions against (a) treating ratios as targets, (b) adding to the schema over time, and (c) assuming three ratios are sufficient.** The strongest contradicting voice (Goodhart) does not refute the ledger; it constrains how the ledger may be used.

## Concrete prescriptions extractable from the corpus
1. Three counts max in the schema; three ratios derived; one warnings list.
2. Warnings include a suggested response, not just a flag.
3. Ratios labeled as "starting heuristics; calibrate empirically."
4. Format must be grep-friendly (markdown table) for future cross-session aggregation.
5. Ledger is advisory; the workflow does not gate on its warnings.
