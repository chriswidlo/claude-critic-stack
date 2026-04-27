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
| **Implement as** | One-line concrete shape. The entry body has the full plan. |

State emoji `🌱` = not finalised (just captured). Anything past `🌱` = work has begun. `🔨` = work done in working tree. `🩺` = work globally verified. `🔖` = work committed to git (commit SHA recorded in entry). ⏸️ next to a state = entry is paused at that state pending a named condition.

## How to add a new entry

When `/upgrade` writes a new entry, also append a row to the appropriate group below — or open a new group if none fit. Re-number when the rank shifts. The rank is a judgment call (value × leverage × dependency-on/by-others), not a formula.

---

## Group A — Foundational (unlock everything else)

These either close audit-chain gaps that compromise the stack's value prop, or define the contract every other upgrade tests against. Implement first.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 1 | [Critics get the Write tool](no-brainer/2026-04-26-critics-get-write-tool/README.md) | ✅ | ⚙️ ⏸️ | XS→? | **Paused 2026-04-27** after run-through-repo: convergent panel veto on the original plan; loop-2 candidate v2-C also reworked. Motive (orchestrator paraphrase loss) has no measured incident on file — frame-challenger named `do nothing` as legitimate null. **Resume when** (a) cheap experiment (4 sessions of manual transcript-vs-file diff) returns a measured paraphrase incident, or (b) [#3](profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md) lands. Four candidate shapes (v2-A / v2-C / v2-C+ / v2-D) recorded in entry body. **Independent meta-review filed 2026-04-27 at [session-artifacts/2026-04-27-critics-get-write-tool-meta-review/](../.claude/session-artifacts/2026-04-27-critics-get-write-tool-meta-review/); verdict: v2-D (do nothing); proposes a cheaper retrospective form of the experiment that could fire today.** |
| 2 | [`limitations.md` as first-class artifact](no-brainer/2026-04-26-limitations-md-as-first-class-artifact/README.md) | ✅ | 🌱 | S | New CLAUDE.md "things you must do, in flight" section; per-session `limitations.md` path convention; optional Stop hook. |
| 3 | [Subagents claim writes not on disk](profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md) | 💎 | 🌱 | S | `PostToolUse` hook on Agent calls that greps the return for claimed paths and verifies they exist. Pairs with #2. |
| 4 | [Constitutional layer — GOALS / MODULES / per-module READMEs](no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md) | ✅ | 🌱 | S | Three docs at root + READMEs per module. The seven-capability taxonomy lives here. |
| 4a | [Workflow is blind to the lab — CLAUDE.md doesn't know it exists](profound/2026-04-26-workflow-blind-to-the-lab/README.md) | 💎 | 🌱 | XS | Add `upgrades/` to CLAUDE.md's named persistent surfaces (alongside `canon/`, `session-artifacts/`, `memory/`). One bullet under "Things you must do" naming lab-shaped utterances ("submit as upgrade", "we should add") that route through the lab. ~5 sentences total. **Pedagogy stays in `upgrades/README.md`; CLAUDE.md only mentions the surface.** Plus a one-sentence README load-ordering tweak. |
| 4b | [Workflow as veto-validator, not action-generator](profound/2026-04-26-workflow-as-veto-validator-not-action-generator/README.md) | 💎 | 🌱 | L | Add a `validate-mode` to the workflow: same agents, different output contract. Step 9 becomes orchestrator-restates-user-candidate; synthesis becomes verdict (confirmed/corrected/overturned), not recommendation. Maps onto PR review, design-doc review, meta-validation. Structural reframe of how the workflow is invoked. |
| 4c | [Canon coverage audit — corpus is less sophisticated than the workflow](normal/2026-04-26-canon-coverage-audit-and-priority-additions/README.md) | 🌿 | 🌱 | M | The library is the bottleneck for 3 of 12 workflow steps (product critique, frame challenge, reframe). Add ~10 high-leverage canon entries; **start with Heuer's *Psychology of Intelligence Analysis* (CIA, free PDF) — single highest-leverage add, unsticks frame-challenger and all three critics**. Then Klein's premortem, Cynefin, Shape Up, Conway/Parnas, then Tier 3 agent literature (ReAct, Self-Refine, Constitutional AI, LLM-as-Judge). |
| 4d | [Negative-value outputs are invisible — `prevented-shipping.md` artifact](profound/2026-04-26-negative-value-outputs-are-invisible/README.md) | 💎 | 🌱 | XS | One new artifact at end of every workflow run: `session-artifacts/<id>/prevented-shipping.md` with four sections (what would have shipped casually, what shipped after workflow, the delta, counterfactual cost). Makes the workflow's preventive value visible — without it the workflow looks like ceremony around outputs the orchestrator could have produced anyway. |
| 4e | [Lab needs a written thesis the graduation gates already silently appeal to](profound/2026-04-27-r-and-d-lab-thesis/README.md) | 💎 | 🌱 | M | New `upgrades/THESIS.md`: mission (forever-true) + worldview (annual cadence) + 3–7 named bets (quarterly) + method commitments + non-goals + cadence + explicit `🃏 wildcard` off-thesis valve. Graduation gates' "belongingness in this repo specifically" criterion becomes "consistent with THESIS or named-wildcard." Synthesis of Bell Labs / PARC / DARPA Heilmeier Catechism / Google X kill-metrics / Anthropic Core Views / March 1991 exploration-vs-exploitation; entry body contains a draft v0 and ~45 cited sources. Pairs structurally with **#4a** (workflow blind to lab) and **#19** (memory and lab same primitive). |

## Group B — Correctness multipliers (every session benefits)

These fix recurring failure modes the operator named in the opening retrospective. Each one improves *every subsequent run*.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 5 | [The critic panel is correlated by default — shadow comparator](profound/2026-04-26-critic-panel-correlated-by-default/README.md) | 💎 | 🌱 | L | `SHADOW_PANEL=1` env var; each lens fires twice (Opus + Sonnet); new `critic-comparator` agent writes `critiques/<lens>.comparison.md`. Off by default. |
| 6 | [The workflow over-designs when told to under-design](profound/2026-04-26-workflow-overdesigns-when-told-to-underdesign/README.md) | 💎 | 🌱 | M | Start with the cheapest path: pre-synthesis "could this be 10% of itself?" check in CLAUDE.md. If that doesn't bite, escalate to a minimalist panel lens. |
| 7 | [Corpus-bias compensation as Step 6.5](no-brainer/2026-04-26-corpus-bias-compensation-step/README.md) | ✅ | 🌱 | XS | CLAUDE.md addition between Step 6 and Step 7; optional `PostToolUse` hook on distiller writes for bias keywords. |
| 8 | [Citation-audit as canon-librarian discipline](no-brainer/2026-04-26-citation-audit-as-canon-discipline/README.md) | ✅ | 🌱 | XS | Two agent file edits: every cited source carries `verified` / `asserted` / `cached` marker. |
| 9 | [Wire `claude-code-guide` into parallel-gather](no-brainer/2026-04-26-wire-claude-code-guide/README.md) | ✅ | 🌱 | XS | One CLAUDE.md paragraph in Steps 3–5 section. Trigger heuristic on Claude Code primitive keywords. |
| 9a | [Casual orchestrator output is workflow-unprotected](profound/2026-04-26-casual-output-is-workflow-unprotected/README.md) | 💎 | 🌱 | XS | Three zero-cost casual-mode disciplines added to CLAUDE.md: (a) user-state-verification rule, (b) outside-view-instinct rule, (c) librarian-instinct rule. The workflow's epistemic protections become ambient, not workflow-conditional. Pairs structurally with **#4a** (CLAUDE.md silence) and **#9b** (specific case). |
| 9b | [Generator cited user-state from memory, not from Explore](no-brainer/2026-04-26-generator-cited-user-state-from-memory/README.md) | ✅ | 🌱 | XS | Discipline rule in CLAUDE.md: every claim about user-machine state must cite a tool call from this conversation OR hedge explicitly. Specific instance of the casual-mode gap **#9a** names. |
| 9c | [Empty config is a signal, not a vacancy — `preserve-as-empty` label](no-brainer/2026-04-26-empty-config-is-a-signal-not-a-vacancy/README.md) | ✅ | 🌱 | XS | Add a 5th label to scope-mapper: `preserve-as-empty` (or `preserve-as-default`). Forces the candidate to either justify the change or treat the slot as occupied. Mechanical, additive. |
| 9d | [Posture-vs-content frame check](no-brainer/2026-04-26-posture-vs-content-frame-check/README.md) | ✅ | 🌱 | XS | One sentence in `frame-challenger.md`: when candidate edits an existing configuration layer, produce a challenge of the form "the current state of this layer is the chosen state." Pairs with **#9c**. |
| 9e | [Quick-take off-ramp pre-check](no-brainer/2026-04-26-quick-take-off-ramp-pre-check/README.md) | ✅ | 🌱 | XS | One-paragraph addition to orchestrator default behavior: before invoking step 1, check the documented off-ramps (factual / quick-take / meta-validation). Asymmetric default: workflow runs unless an off-ramp applies. |
| 9f | [Author attribution for community plugins (outside-view contract)](normal/2026-04-26-author-attribution-for-community-plugins/README.md) | 🌿 | 🌱 | XS | Append to `outside-view.md`: when forecasting community-plugin adoption, disambiguate content-origin from packaging-entity. Two-attribution disambiguation prevents collapsing distinct credibility signals into one. |

## Group C — Workflow control & user agency

Operator-controllable escape hatches and metacognitive surfaces. None foundational; all valuable when the workflow stops serving the question.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 10 | [`/drop-workflow` + intent checkpoints](no-brainer/2026-04-26-drop-workflow-and-intent-checkpoints/README.md) | ✅ | 🌱 | XS | New `.claude/commands/drop-workflow.md`; two CLAUDE.md sentence-additions between Steps 6→7 and 9→10. |
| 11 | [Step 12 — experiment-running branch](normal/2026-04-26-step-12-experiment-running-branch/README.md) | 🌿 | 🌱 | M | New Step 12.5 in CLAUDE.md: classify named experiment as runnable-here / needs-user / not-runnable; offer to run if under ~20 agent-calls. |
| 12 | [Two-question disambiguation in classifier](normal/2026-04-26-two-question-disambiguation-classifier/README.md) | 🌿 | 🌱 | M | Classifier prompt redesign to emit `ambiguous-scope:` and `blockers:` stanzas; new Step 1.5 in CLAUDE.md to surface high-severity blockers. |
| 13 | [Step 13 — session ledger format](normal/2026-04-26-step-13-session-ledger/README.md) | 🌿 | 🌱 | M | Orchestrator writes `session-artifacts/<id>/ledger.md` after synthesis: agent calls, artifacts, loops, derived ratios, threshold warnings. |
| 14 | [Hard gates as harness hooks](normal/2026-04-26-hard-gates-as-harness-hooks/README.md) | 🌿 | 🌱 | M | Three `PreToolUse` / `PostToolUse` hooks: Step-9 precondition gate, loop-cap counter, classifier-blocker surfacer. Env-var bypass on each. |
| 14a | [Format-only state-transition gate for upgrade entries](normal/2026-04-26-format-only-state-transition-gate/README.md) | 🌿 | ⚙️ | M | Warning-only subcommand of `/upgrade` that reads schema from a table in `upgrades/README.md`. Spike done; ran through workflow on 2026-04-26 (loop 2 approved). Productionization (slash-command integration, `--apply`, log) deferred until git strategy. |
| 14b | [Convergent frame objections as replan signal](normal/2026-04-26-convergent-frame-objections-as-replan-signal/README.md) | 🌿 | 🌱 | XS | Step 11 addition: before deciding rewrite vs. replan, summarize each lens's frame-level objection in one sentence. If the three converge on a shared insight, route to `replan` regardless of whether design fixes are individually actionable. Convergence is the signal. |
| 14c | [Meta-validation lacks "prior-was-right" output mode](normal/2026-04-26-meta-validation-lacks-prior-was-right-output/README.md) | 🌿 | 🌱 | S | Synthesis-template variant when input *is* a prior recommendation: headline = "prior verdict + corrections" instead of new recommendation. Cleaner version of **#4b** (validate-mode), restricted to the specific case of meta-validating a prior. Could be subsumed by #4b if that lands. |

## Group D — Repo hygiene & conventions

Pure structural cleanups. Land any time; none unblock other work, but each makes the repo legible as it grows.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 15 | [Agent subdirectories by module](no-brainer/2026-04-26-agent-subdirectories-by-module/README.md) | ✅ | 🌱 | XS | Verify recursive loading with a test agent; `mv` files into six subdirectories mirroring MODULES.md. |
| 16 | [Git strategy documentation](no-brainer/2026-04-26-git-strategy-documentation/README.md) | ✅ | 🌱 | S | New `GIT.md` covering commit conventions, capability tagging in commits, lab-to-commits link via `implemented_by:` field. |
| 17 | [The R&D lab itself](no-brainer/2026-04-26-rnd-lab/README.md) | ✅ | 🌱 | — | Already built. Entry's state should advance to 💎 `value-proved` once a second session uses the lab non-trivially. |
| 18 | [Closed-world trust model + MCP allowlist check](no-brainer/2026-04-26-closed-world-mcp-allowlist/README.md) | ✅ | 🌱 | XS | One CLAUDE.md bullet under "Things you must not do" rejecting vendor-live MCP retrieval; `bin/check-mcp-allowlist.sh` runs at workflow Step 0 and fails closed if a non-allowlisted MCP server is present in any scope. |
| 18a | [Upgrade entries can grow into folders](no-brainer/2026-04-26-upgrade-entries-as-folders/README.md) | ✅ | 🌱 | XS | Redefine an entry as a folder containing one slug-named `.md` (the doc) plus any supporting files. Migrate the 28 existing entries via `git mv`. Update `upgrades/README.md` and `/upgrade` slash command to write the new shape. Precondition for #18b. |
| 18b | [Agentic-engineering reference library from session research](normal/2026-04-26-agentic-engineering-reference-library/README.md) | 🌿 | 🌱 | S | Promote `temporary/decision-registry.md` + playbook into the entry's own folder (consumes #18a); route the four transcripts through `canon-refresher` as primary-source proposals; one paragraph in CLAUDE.md describing the migrated reference. |
| 18c | [Tighten `⚙️ run-through-repo` regex](no-brainer/2026-04-26-tighten-run-through-repo-regex/README.md) | ✅ | 🌱 | XS | One README cell update + ~10 lines parser extension to verify matched session-id corresponds to a real `.claude/session-artifacts/<slug>/` directory. Closes the documented false positive from the format-only gate spike. |
| 18d | [Draft / experimental status marker for README sections](no-brainer/2026-04-26-draft-status-marker-for-readme-sections/README.md) | ✅ | 🌱 | XS | Convention: blockquote at top of any README section documenting a contract whose tool isn't yet built. Apply immediately to the schema table that the gate reads. |
| 18e | [Markdown-table parser convention (`\|` escapes)](no-brainer/2026-04-26-markdown-table-parser-convention/README.md) | ✅ | 🌱 | XS | One paragraph + 5-line helper. Lands in MODULES.md or GIT.md when those exist; until then this entry is the canonical reference. |
| 18f | [State-table honesty discipline](normal/2026-04-26-state-table-honesty-discipline/README.md) | 🌿 | 🌱 | S | When same-session advancement crosses ≥2 states, append an `## Update history` blockquote naming what happened and why. Format-only gate eventually checks for the blockquote when ≥2 cells are filled with the same date. |

## Group E — Observations (no immediate action)

Entries that name a real thing but whose action is "answer this with a future entry," not "build something now."

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 19 | [Memory and lab are the same primitive](profound/2026-04-26-memory-and-lab-are-the-same-primitive/README.md) | 💎 | 🌱 | — | No build. Open question to be answered by a future entry once the lab has run for ~10 sessions and the convergence/divergence becomes visible. |

## Group F — Long-term bets (outlandish — defer until foundation lands)

Each is months of work. None is wrong; each is wrong *now* because Groups A–C aren't done. Revisit after the foundation has been validated.

| # | Title | Tier | State | Effort | Implement as |
|---|---|---|---|---|---|
| 20 | [Scope-projector capability](outlandish/2026-04-26-scope-projector-capability/README.md) | 🚀 | 🌱 | XL | Start with Path B (frame-challenger gains a "projected mature form" output). Promote to its own agent (Path A) only if Path B carries signal. |
| 21 | [External shadow via OpenRouter](outlandish/2026-04-26-external-shadow-via-openrouter/README.md) | 🚀 | 🌱 | XL | `bin/external-critic.sh` wrapper; `EXTERNAL_SHADOW=1` env var; comparator extended to three-way. Depends on #5 landing first. |
| 22 | [Research stack as sibling](outlandish/2026-04-26-research-stack-as-sibling/README.md) | 🚀 | 🌱 | XL | Sibling `claude-research-stack` repo; talks to this stack only via shared `canon/corpus/`. Months of design + scaffolding. |
| 22a | [Critic-stack as installable marketplace plugin](outlandish/2026-04-26-critic-stack-as-installable-marketplace-plugin/README.md) | 🚀 | 🌱 | XL | Refactor the repo into a Claude Code marketplace-installable plugin. `.claude-plugin/plugin.json` + `marketplace.json`. Apparatus distributed; content (canon, lab, session-artifacts) stays user-specific. Honest about hard problems: namespacing, versioning, audience, and that publishing changes how the workflow gets used. |
| 22b | [Obsidian + Claude Code as substrate/derivative vault — greenfield design](outlandish/2026-04-26-obsidian-substrate-derivative-vault/README.md) | 🚀 | 🌱 | XL | Two-vault topology (substrate/derivative split), four bounded operations, provenance frontmatter, dated context, embeddings via Smart Connections. Notes the **isomorphism** with critic-stack's own canon/distillations pattern — substrate/derivative may be a universal AI-integration principle worth a profound entry of its own. Long entry; phased rollout (Phase 0 = two-week trial). |

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
