# Product lens — loop 2

**Verdict:** `approve`

**One-line:** v2 ships a real gate-shaped affordance on day 1 with the contract preserved; the subcommand factoring and schema-in-README are honest tradeoffs and `--apply` is correctly opt-in.

## Day 1 reality
Operator gets `/upgrade advance <entry-path> <new-state>` that prints a one-screen line-cited report naming exactly which required body element is missing for the requested state, with the regex it matched and the suggested heading text. README gains one new advisory table (~15 lines). No existing sentence rewritten. No existing entry needs to change.

## Contract preservation
- README's "manual act of yes-this-happened" sentence: preserved.
- Descriptive-not-prescriptive stance: preserved.
- Zero-INDEX/zero-lint promise: preserved.
- 22 existing entries: zero changes required. Not retroactively "incorrect."

## Affordances
**Better:** day-1 affordance, line-cited specific warnings, single source of truth (gate-wrong = README-wrong), `--apply` convenience.

**Worse:** README has a documentation surface to maintain (regex tuning is now README-edit, not script-edit — honestly named). `/upgrade` overloaded across two speech acts (capture vs advance) — mitigated by reversibility.

## Watch-fors (not blocking)
- Future revision moving `--apply` toward default-on would resurrect v1's product objection.
- Future revision rewriting README's "manual act" sentence would flip the contract.
- `/upgrade help` (or header in `.claude/commands/upgrade.md`) should be added so the overloaded surface is discoverable.

## Frame note (residual)
"Warning-only" is fully responsive only because the candidate is honest about the limit (no surface in solo repo guarantees non-drift without becoming high-bypass). Escalation path stays open: ship the warning, watch whether AI sessions heed it, and if drift continues, the operator has data to ask for harder shape (e.g., CLAUDE.md instruction "if `/upgrade advance` reports missing elements, do not advance"). v2 didn't burn the contract; that escalation remains available.
