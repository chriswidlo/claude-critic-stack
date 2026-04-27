# Upgrades ledger — value-ranked, all tiers mixed

This is the single ranked queue across all four tier folders. Entries are ordered by **value of implementing now**, not by tier and not by effort. A no-brainer can sit below an outlandish if the outlandish unlocks more.

> **Groups here are pickup hints — not categorization.** The real categorization is the **tier folder** (`profound/`, `outlandish/`, `no-brainer/`, `normal/`) — see `README.md` for the placement rule. Groups in this ledger (Foundational, Correctness multipliers, Workflow control, etc.) are an *ordering convenience* for the operator: which entries to consider first. Group placement is fuzzy and re-rankable; tier placement is the entry's identity.
>
> Every entry, regardless of group or rank, still goes through the full upgrade lifecycle when worked on. The ledger is a reading aid, not a shortcut around the process.

## How to read this

| Column | Meaning |
|---|---|
| **#** | Implementation priority (1 = do first). Re-rank when adding. |
| **Title** | Linked to the entry file. |
| **Tier** | 💎 profound · 🚀 outlandish · ✅ no-brainer · 🌿 normal |
| **State** | 🌱 created · 🔬 spiked · 📋 prepared · ✅ accepted · ⚙️ run-through-repo · 🔨 implemented · 🩺 verified · 🔖 committed · 💎 value-proved · 🏁 completed · ⏸️ paused (modifier — applied alongside the highest reached state when an entry is deliberately not advancing pending an external condition; resume conditions live in the entry body) |
| **Effort** | XS (≤30 min) · S (≤3 h) · M (≤8 h) · L (≤2 d) · XL (weeks–months) |
| **Implement as** | Optional. `—` means no note; the entry README holds the plan. Use a single short sentence only when a current blocker, pairing, or paused-state note affects pickup order. |

State emoji `🌱` = not finalised (just captured). Anything past `🌱` = work has begun. `🔨` = work done in working tree. `🩺` = work globally verified. `🔖` = work committed to git (commit SHA recorded in entry). ⏸️ next to a state = entry is paused at that state pending a named condition.

## How to add a new entry

When `/upgrade` writes a new entry, also append a row to the appropriate group below — or open a new group if none fit. Re-number when the rank shifts. The rank is a judgment call (value × leverage × dependency-on/by-others), not a formula.

---

## Group A — Foundational (unlock everything else)

These either close audit-chain gaps that compromise the stack's value prop, or define the contract every other upgrade tests against. Implement first.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 1 | [Critics get the Write tool](no-brainer/2026-04-26-critics-get-write-tool/README.md) | ✅ | ⚙️ ⏸️ | XS→? | Paused 2026-04-27; resume conditions in entry. |
| 2 | [`limitations.md` as first-class artifact](no-brainer/2026-04-26-limitations-md-as-first-class-artifact/README.md) | ✅ | 🌱 | S | — |
| 3 | [Subagents claim writes not on disk](profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md) | 💎 | 🌱 | S | Pairs with #2. |
| 4 | [Constitutional layer — GOALS / MODULES / per-module READMEs](no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md) | ✅ | 🌱 | S | — |
| 4a | [Workflow is blind to the lab — CLAUDE.md doesn't know it exists](profound/2026-04-26-workflow-blind-to-the-lab/README.md) | 💎 | 🌱 | XS | — |
| 4b | [Workflow as veto-validator, not action-generator](profound/2026-04-26-workflow-as-veto-validator-not-action-generator/README.md) | 💎 | 🌱 | L | — |
| 4c | [Canon coverage audit — corpus is less sophisticated than the workflow](normal/2026-04-26-canon-coverage-audit-and-priority-additions/README.md) | 🌿 | 🌱 | M | — |
| 4d | [Negative-value outputs are invisible — `prevented-shipping.md` artifact](profound/2026-04-26-negative-value-outputs-are-invisible/README.md) | 💎 | 🌱 | XS | — |
| 4e | [Lab needs a written thesis the graduation gates already silently appeal to](profound/2026-04-27-r-and-d-lab-thesis/README.md) | 💎 | 🌱 | M | Pairs with #4a, #19. |
| 4f | [Three-layer security module — mechanisms first](normal/2026-04-26-three-layer-security-module/README.md) | 🌿 | 🌱 | L | Operator priority. Pairs with #18, #8, #2. |
| 4g | [Canon R&D-lab-management expansion — deferred batch from thesis research](normal/2026-04-27-canon-r-and-d-lab-management-expansion/README.md) | 🌿 | 🌱 | M | Pairs with #4c, #4e. |

## Group B — Correctness multipliers (every session benefits)

These fix recurring failure modes the operator named in the opening retrospective. Each one improves *every subsequent run*.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 5 | [The critic panel is correlated by default — shadow comparator](profound/2026-04-26-critic-panel-correlated-by-default/README.md) | 💎 | 🌱 | L | — |
| 6 | [The workflow over-designs when told to under-design](profound/2026-04-26-workflow-overdesigns-when-told-to-underdesign/README.md) | 💎 | 🌱 | M | — |
| 7 | [Corpus-bias compensation as Step 6.5](no-brainer/2026-04-26-corpus-bias-compensation-step/README.md) | ✅ | 🌱 | XS | — |
| 8 | [Citation-audit as canon-librarian discipline](no-brainer/2026-04-26-citation-audit-as-canon-discipline/README.md) | ✅ | 🌱 | XS | — |
| 9 | [Wire `claude-code-guide` into parallel-gather](no-brainer/2026-04-26-wire-claude-code-guide/README.md) | ✅ | 🌱 | XS | — |
| 9a | [Casual orchestrator output is workflow-unprotected](profound/2026-04-26-casual-output-is-workflow-unprotected/README.md) | 💎 | 🌱 | XS | Pairs with #4a, #9b. |
| 9b | [Generator cited user-state from memory, not from Explore](no-brainer/2026-04-26-generator-cited-user-state-from-memory/README.md) | ✅ | 🌱 | XS | Specific instance of #9a. |
| 9c | [Empty config is a signal, not a vacancy — `preserve-as-empty` label](no-brainer/2026-04-26-empty-config-is-a-signal-not-a-vacancy/README.md) | ✅ | 🌱 | XS | — |
| 9d | [Posture-vs-content frame check](no-brainer/2026-04-26-posture-vs-content-frame-check/README.md) | ✅ | 🌱 | XS | Pairs with #9c. |
| 9e | [Quick-take off-ramp pre-check](no-brainer/2026-04-26-quick-take-off-ramp-pre-check/README.md) | ✅ | 🌱 | XS | — |
| 9f | [Author attribution for community plugins (outside-view contract)](normal/2026-04-26-author-attribution-for-community-plugins/README.md) | 🌿 | 🌱 | XS | — |

## Group C — Workflow control & user agency

Operator-controllable escape hatches and metacognitive surfaces. None foundational; all valuable when the workflow stops serving the question.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 10 | [`/drop-workflow` + intent checkpoints](no-brainer/2026-04-26-drop-workflow-and-intent-checkpoints/README.md) | ✅ | 🌱 | XS | — |
| 11 | [Step 12 — experiment-running branch](normal/2026-04-26-step-12-experiment-running-branch/README.md) | 🌿 | 🌱 | M | — |
| 12 | [Two-question disambiguation in classifier](normal/2026-04-26-two-question-disambiguation-classifier/README.md) | 🌿 | 🌱 | M | — |
| 13 | [Step 13 — session ledger format](normal/2026-04-26-step-13-session-ledger/README.md) | 🌿 | 🌱 | M | — |
| 14 | [Hard gates as harness hooks](normal/2026-04-26-hard-gates-as-harness-hooks/README.md) | 🌿 | 🌱 | M | — |
| 14a | [Format-only state-transition gate for upgrade entries](normal/2026-04-26-format-only-state-transition-gate/README.md) | 🌿 | ⚙️ | M | Spike done; productionization deferred. |
| 14b | [Convergent frame objections as replan signal](normal/2026-04-26-convergent-frame-objections-as-replan-signal/README.md) | 🌿 | 🌱 | XS | — |
| 14c | [Meta-validation lacks "prior-was-right" output mode](normal/2026-04-26-meta-validation-lacks-prior-was-right-output/README.md) | 🌿 | 🌱 | S | Could be subsumed by #4b. |

## Group D — Repo hygiene & conventions

Pure structural cleanups. Land any time; none unblock other work, but each makes the repo legible as it grows.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 15 | [Agent subdirectories by module](no-brainer/2026-04-26-agent-subdirectories-by-module/README.md) | ✅ | 🌱 | XS | — |
| 16 | [Git strategy documentation](no-brainer/2026-04-26-git-strategy-documentation/README.md) | ✅ | 🌱 | S | — |
| 17 | [The R&D lab itself](no-brainer/2026-04-26-rnd-lab/README.md) | ✅ | 🌱 | — | Already built; advance to 💎 once a second session uses it non-trivially. |
| 18 | [Closed-world trust model + MCP allowlist check](no-brainer/2026-04-26-closed-world-mcp-allowlist/README.md) | ✅ | 🌱 | XS | — |
| 18a | [Upgrade entries can grow into folders](no-brainer/2026-04-26-upgrade-entries-as-folders/README.md) | ✅ | 🌱 | XS | Precondition for #18b. |
| 18b | [Agentic-engineering reference library from session research](normal/2026-04-26-agentic-engineering-reference-library/README.md) | 🌿 | 🌱 | S | Source files live on `agentic-engineering-research`@13c09b0, not `main`; entry needs a fresh plan written in its own folder before pickup. |
| 18c | [Tighten `⚙️ run-through-repo` regex](no-brainer/2026-04-26-tighten-run-through-repo-regex/README.md) | ✅ | 🌱 | XS | — |
| 18d | [Draft / experimental status marker for README sections](no-brainer/2026-04-26-draft-status-marker-for-readme-sections/README.md) | ✅ | 🌱 | XS | — |
| 18e | [Markdown-table parser convention (`\|` escapes)](no-brainer/2026-04-26-markdown-table-parser-convention/README.md) | ✅ | 🌱 | XS | — |
| 18f | [State-table honesty discipline](normal/2026-04-26-state-table-honesty-discipline/README.md) | 🌿 | 🌱 | S | — |
| 18g | [Living module for AI power-user SOTA practice](normal/2026-04-26-living-poweruser-knowledge-module/README.md) | 🌿 | 🌱 | M | Parent of #18b. |
| 18h | [Workflow docs scattered and partly stale](normal/2026-04-27-workflow-docs-scattered-and-stale/README.md) | 🌿 | 🌱 | XS→M | — |

## Group E — Observations (no immediate action)

Entries that name a real thing but whose action is "answer this with a future entry," not "build something now."

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 19 | [Memory and lab are the same primitive](profound/2026-04-26-memory-and-lab-are-the-same-primitive/README.md) | 💎 | 🌱 | — | No build. |

## Group F — Long-term bets (outlandish — defer until foundation lands)

Each is months of work. None is wrong; each is wrong *now* because Groups A–C aren't done. Revisit after the foundation has been validated.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 20 | [Scope-projector capability](outlandish/2026-04-26-scope-projector-capability/README.md) | 🚀 | 🌱 | XL | — |
| 21 | [External shadow via OpenRouter](outlandish/2026-04-26-external-shadow-via-openrouter/README.md) | 🚀 | 🌱 | XL | Depends on #5. |
| 22 | [Research stack as sibling](outlandish/2026-04-26-research-stack-as-sibling/README.md) | 🚀 | 🌱 | XL | — |
| 22a | [Critic-stack as installable marketplace plugin](outlandish/2026-04-26-critic-stack-as-installable-marketplace-plugin/README.md) | 🚀 | 🌱 | XL | — |
| 22b | [Obsidian + Claude Code as substrate/derivative vault — greenfield design](outlandish/2026-04-26-obsidian-substrate-derivative-vault/README.md) | 🚀 | 🌱 | XL | — |

---

## Suggested first session

Five entries are XS effort and sit in Groups A or B. They can land in one short session and every subsequent run benefits:

- **#1** Critics get Write
- **#7** Corpus-bias Step 6.5
- **#8** Citation-audit markers
- **#9** Wire `claude-code-guide`
- **#10** `/drop-workflow` + checkpoints

After those, the next obvious move is **#2** + **#3** together (limitations.md + verification hook), since they pair structurally and both are S effort.

## When to re-rank

Re-rank this ledger when:
- A new entry lands and its rank is non-obvious (think where it slots; bump everything below).
- An entry advances state past `🌱` (the rank may matter less once it's underway).
- A session reveals that an upgrade we ranked low is actually unblocking a frustration that fires every run (promote it).
- Group F bets become more concrete (e.g., a benchmark exists for #20; a research-stack scaffold exists for #21).

The ledger is a snapshot of judgment, not a permanent ordering.
