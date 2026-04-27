# Critic — architecture lens

> Orchestrator-authored stand-in (no `Task` tool available). Written from the architecture-critic posture.

## Frame-level objection
The candidate puts the **schema in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md)**, the **citation pattern in [CLAUDE.md](CLAUDE.md) step 12 spec**, and the **example in [.claude/session-artifacts/exemplars/](.claude/session-artifacts/exemplars/)**. That's three coupled locations for one feature. If the schema changes, all three must move in lockstep, and there is no machine-readable link between them.

This is the same coupling smell as the format-only-state-transition-gate entry's "schema-in-README + slash-command-in-`.claude/commands/`" pattern. That entry mitigated it with an HTML-comment marker (`<!-- machine-read by ... -->`). This entry should adopt the same convention: an HTML-comment marker on the ledger-schema section identifying it as the load-bearing source.

## Weakest link
The "decision" definition. The candidate hand-waves it ("the explicit recommendation in synthesis, plus any explicitly-named alternatives the operator must choose between"). That definition is interpretable two ways: a session naming three alternatives = 4 decisions or 1 decision? The ratio depends on which way the orchestrator counts. Until the definition is sharper or until the count comes from a parsed structure (e.g., a `## Decisions` section in synthesis with bulleted items), this ratio is noisy.

## Invariants at risk
- **Source-of-truth singularity.** Three locations encode the schema; HTML-comment marker should mark the canonical one.
- **Referential integrity.** Synthesis cites ledger; if a session produces ledger.md but synthesis omits the citation, that is now a lifecycle violation with no detector. Worth a sentence in CLAUDE.md naming this.

## Specific actionable suggestions
1. Add an HTML comment to the ledger-schema section in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md): `<!-- machine-read source for ledger.md schema. CLAUDE.md step 13 and exemplar refer to this. do not change heading text without updating both. -->`
2. Tighten "decision" to: *"each bulleted item under the synthesis's `Recommendation` and `Uncertainties` sections"* — gives a parser-able count.
3. Add an explicit cross-link from CLAUDE.md step 13 to the schema section using a repo-root-relative link.

## Verdict
**rework** — directionally right; mitigations above are cheap and improve durability. The frame-level coupling concern is real but addressable.
