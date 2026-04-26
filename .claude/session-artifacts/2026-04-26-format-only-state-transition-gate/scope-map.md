# Scope map — format-only state-transition gate

## Existing primitives touched

| primitive | source (where it was named) | relationship | one-line rationale |
|---|---|---|---|
| The 8-state lifecycle definition (`upgrades/README.md` §"The state lifecycle") | README §state-lifecycle; entry body §schema | extend | The eight named states stay; the gate adds a per-state required-elements schema on top — no state is renamed, removed, or merged. |
| The README sentence "There is no automation; it's a manual act of 'yes, this happened.'" (`upgrades/README.md` line 141) | README state-lifecycle paragraph | conflict | The gate introduces automation precisely where the README declares there is none. Both sentences cannot coexist; the README would have to be rewritten to say "automation is allowed via `/advance-upgrade`." User has not chosen. |
| The "manual edit the date" convention (`upgrades/README.md` line 141; entry §interaction Point B) | README + entry body | replace | Entry §interaction-model explicitly says "The operator never edits the table by hand; the slash command is the only path." That is replacement, not extension. |
| The state column / horizontal state table in entries (`upgrades/README.md` §"two prepended tables") | README §two-prepended-tables; entry §schema | extend | The state table's *shape* (eight columns, dates underneath, em-dashes for unreached) is preserved; the gate adds preconditions for *writing into* a column. Cell semantics ("rightmost filled = current state") unchanged. |
| `/upgrade` slash command (`.claude/commands/upgrade.md`) | command file; entry §interaction-model; classifier gaps | conflict | Entry proposes a sibling `/advance-upgrade` command. Frame Revision 1 explicitly flags the alternative: an `/upgrade advance` subcommand inside the existing command. Both shapes are live; user has not chosen between sibling-command and subcommand. |
| `/upgrade` command's step 5 ("Generate the state table with `created` filled in") (`.claude/commands/upgrade.md` lines 34–47) | command body | extend | The capture path remains — `/upgrade` still creates an entry at `🌱 created`. The gate only governs *transitions out of* `created`, not creation itself. |
| `upgrades/LEDGER.md` State column (`upgrades/LEDGER.md` lines 16, 32–91) | LEDGER table | extend | The ledger displays state per row but does not write it; the gate doesn't touch read paths. The ledger continues to mirror whatever the entry's state-table says. |
| `upgrades/LEDGER.md` "When `/upgrade` writes a new entry, also append a row" instruction (line 24) | LEDGER §how-to-add | extend | The ledger's append-on-create rule is unaffected by a gate that fires on *transitions*, not creations. No conflict, but worth naming so the generator doesn't accidentally bundle ledger-update into the gate. |
| Per-tier folder structure (`profound/`, `outlandish/`, `no-brainer/`, `normal/`) (`upgrades/README.md` §four-tiers) | README §four-tiers | extend | No interaction. Tier is idea-character; state is lifecycle progress. The gate reads files inside any tier folder identically. Stating explicitly per the user's request. |
| Anti-pattern "Grouping by status — `done/`, `in-progress/`" (`upgrades/README.md` line 73) | README §what-is-NOT-a-valid-grouping | extend | The gate enforces state via the in-entry table, never by moving files. Compatible with — and reinforces — the "state lives in the table, not the folder" rule. |
| Required meta fields (`title`, `tier`, `author`, `created`, `catalyst`, `essence`, `upgrade`) (`upgrades/README.md` §two-prepended-tables) | README §meta-table; entry §schema | extend | Entry §schema adds an optional `implemented_by:` meta row at the `🔨` transition. README's "Optional rows (append when they help)" already permits this; gate makes it conditionally required. |
| Entry §schema's "out-of-order advancement" rule (entry lines 52–53) vs README's "If a state is reached out of order ... fill in both dates honestly — the lifecycle is descriptive, not prescriptive" (README line 141) | README + entry body | conflict | README declares the lifecycle *descriptive*; the gate makes it *prescriptive* by requiring all skipped transitions' elements before allowing a skip. The two stances cannot both be true. User has not chosen. |
| Existing agents in `.claude/agents/` (`requirement-classifier`, `canon-librarian`, `outside-view`, `subagent-distiller`, `scope-mapper`, `frame-challenger`, `critic-architecture`, `critic-operations`, `critic-product`, `canon-refresher`) | CLAUDE.md §agents-available | extend | None of the existing agents currently does any part of state-transition validation for lab entries. The critic-panel evaluates *workflow design* not *lab lifecycle*; the lab has no agent today. The gate adds a new capability surface without overlap. |
| `canon-refresher` agent (CLAUDE.md §agents-available) | CLAUDE.md | extend | Closest analogue (it proposes corpus changes without writing). Pattern (script-deterministic + optional agent-assist for scaffolding) named in entry §implementation-choice mirrors `canon-refresher`'s "never writes to corpus" stance. No overlap; just precedent. |

## Deletion cost (for subsume/replace rows)

- **"Manual edit the date" convention (replace):**
  - Callers: any human or agent that has ever opened a lab entry and typed a date into the state table. Today that is the operator (≤ 22 entries × possibly multiple transitions, but state tables are mostly em-dashes today, so concrete edit count is low — likely < 30 historical edits).
  - Data migrations: none. Existing dates stay valid; only the *write path* for future dates changes.
  - Config surface: README §state-lifecycle paragraph (line 141) must be rewritten — the sentence "There is no automation; it's a manual act" becomes false. Also the README §how-to-add list (lines 146–151) is silent on advancement and stays correct, but a new section on "How to advance an entry" must be added or the README is incomplete.
  - Documentation drift risk: the entry's §interaction-model contradicts the README today; ship without rewriting the README and the lab has two contradictory sources of truth.

## Requires decision (conflicts)

- **README's "no automation" sentence vs the gate's existence.** Both cannot coexist. Either the README is rewritten to say "advancement is automated via `/advance-upgrade`; manual edits are deprecated/forbidden," or the gate is downgraded to advisory-only (warns but does not block, README sentence stands). User has not chosen.

- **`/upgrade` (existing) vs `/advance-upgrade` (proposed sibling) vs `/upgrade advance` (subcommand inside existing).** Three live shapes:
  - sibling command (entry §interaction-model preference);
  - subcommand inside existing `/upgrade` (frame Revision 1's flagged alternative);
  - keep `/upgrade` for capture-only and reject any advancement command (do nothing — leave advancement manual).
  User has not chosen between command-shape options. Picking is a user decision because the slash-command UX surface is operator-facing and irreversible-ish (renaming commands later is awkward).

- **Lifecycle as descriptive (README) vs prescriptive (entry's gate schema).** README explicitly says "the lifecycle is descriptive, not prescriptive"; the gate's "all skipped transitions' elements must be present" rule makes it prescriptive. Either the README sentence stays and the gate must accept skips without backfill, or the gate's rule stays and the README is rewritten. User has not chosen. This is the load-bearing philosophical conflict — adopting the gate flips the lab's stance on its own lifecycle.

## Preserved primitives with stated reason (non-default)

- **The 8-state lifecycle (extend, not replace):** preserved because the user's framing words ("a gate so the AI that handles upgrades doesn't get confused and all upgrades follow the same pattern") presume the existing lifecycle is the contract being enforced. Replacing the lifecycle would invalidate the gate's purpose.
- **The state column in entries (extend, not replace):** preserved because the canon-librarian distillation surfaced Anthropic 2025's "folder hierarchies, naming conventions, and timestamps" passage as a viable alternative shape (folder-as-state collapses the 8-state machine to 1-state-per-folder). The user has not chosen this alternative; their framing presumes the in-entry state table stays. Concrete cost of replacing it: every existing entry would need its state-table stripped and the entry physically moved on each transition, contradicting the README's anti-pattern §"Grouping by status."
- **`/upgrade` slash command's capture path (extend, not replace):** preserved because the user's classifier `gaps` section answers its own question — the existing `/upgrade` exists and handles creation. The gate addresses transitions only; nothing in the entry suggests removing the capture path. Concrete cost of replacing: every operator-typed `/upgrade <thought>` invocation would break.
- **Per-tier folder structure (extend, no interaction):** preserved because tier and state are orthogonal axes (idea-character vs lifecycle progress) and the README's §four-tiers explicitly defends this orthogonality. No reason to touch it; stating explicitly per user's request.

## Primitives the distillations did not name but the query implies

- **`limitations.md` artifact** — the entry §open-questions asks "Should the gate emit a `limitations.md` entry when it denies?" `limitations.md` is itself a not-yet-implemented upgrade entry (LEDGER #2). The gate's denial-emission behavior depends on a primitive that does not exist yet. Worth a follow-up Explore or a frame-challenger note.
- **The `subagents-claim-writes-not-on-disk` PostToolUse hook** (LEDGER #3, listed in the entry's `relates_to`) — same status: a planned-but-unbuilt primitive the gate's interaction model leans on. Not surfaced by Explore (which did not run; this is a `new`/sketch-exists requirement with no target codebase exploration). Worth naming so the generator doesn't assume the hook exists.
- **A schema-source-of-truth file** — frame Revision 1's "schema-first" alternative posits a `upgrades/.transition-schema.yaml` or equivalent. No such file exists. The README §state-lifecycle prose is the closest thing to a schema today. Generator should treat this as a primitive-to-be-created, not a primitive-to-extend.
- **Pre-commit hook infrastructure** — the entry §interaction-model Point A presumes a git pre-commit hook surface. The repo has none today (no `.husky/`, no `.pre-commit-config.yaml`, no `.githooks/` registered). Adding one is itself a primitive-creation, not a primitive-extension.
- **Existing test fixtures for lab entries** — the entry says "Testing across the existing 21 entries is required." There is no test harness for lab content today. The gate's validation logic would be the first such harness.
