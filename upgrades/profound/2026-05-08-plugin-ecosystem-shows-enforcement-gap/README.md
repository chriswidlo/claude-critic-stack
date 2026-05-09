# The Claude Code plugin ecosystem shows this repo's gap is enforcement, not thinking

| Field | Value |
|---|---|
| 📌 **title** | The Claude Code plugin ecosystem shows this repo's gap is enforcement, not thinking |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-08 |
| ⚡ **catalyst** | Operator asked: "research all valuable plugins to Claude Code, from Anthropic and any other bigger marketplace... what will make our repo SOTA? what we can just learn from some of them and would give more benefit than installing it." Three parallel research streams — Anthropic official, community marketplaces, individual high-value primitives — produced a clearer pattern than the question expected. The pattern is the entry. |
| 💡 **essence** | Surveying ~200 published Claude Code plugins reveals that the strong ones share three traits: named primitives instead of role lists, maintainer credibility outside Claude Code, READMEs that describe mechanism rather than outcomes. Cross-mapped against this repo, the comparison inverts the implicit assumption that the repo is "behind." On the rare/hard primitives — mandatory contradicting-source canon retrieval, outside-view discipline, frame-challenger gate, multi-lens minority-veto, shadow-comparator triangulation, ledger schema, lab state machine — this repo is *SOTA or unique*. The lag is on the *cheap* primitives — hooks, statusline observability, SessionStart recall, plugin-format distribution — that 90% of serious community plugins have built. The intellectual primitives are doing well; the enforcement primitives are the gap. |
| 🚀 **upgrade** | Reframe future filing: stop treating the lab's hooks/observability proposals as competing with the deeper canon/panel/comparator work. They are the *cheap correctives* to a known gap, not parallel ambitions. Three Tier-A entries (PreToolUse hard-gate hook, JSONL-dual-source ledger, statusline thresholds) become near-default filings; one Tier-B entry (port nyldn/claude-octopus's wrapper to unblock `EXTERNAL_SHADOW=1`) becomes the highest-leverage *strategic* move because cross-family shadow is the one quality lever the comparator cannot get any other way. |
| 🏷️ **tags** | meta, framing, ecosystem-survey, hooks, observability, plugin-distribution, sota |
| 🔗 **relates_to** | 2026-04-26-critic-panel-correlated-by-default, 2026-04-26-casual-output-is-workflow-unprotected, 2026-04-26-subagents-claim-writes-not-on-disk, 2026-04-27-r-and-d-lab-thesis |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-08 | — | — | — | — | — | — | — | — | — |

## Table of contents

- [The reframe — intellectual SOTA with an enforcement gap](#the-reframe--intellectual-sota-with-an-enforcement-gap)
- [Methodology](#methodology)
- [The Anthropic ecosystem in one section](#the-anthropic-ecosystem-in-one-section)
  - [Three marketplaces, one schema](#three-marketplaces-one-schema)
  - [The plugin format (what an installable plugin actually is)](#the-plugin-format-what-an-installable-plugin-actually-is)
  - [Anthropic-authored plugins worth knowing exist](#anthropic-authored-plugins-worth-knowing-exist)
- [The community ecosystem — bimodal](#the-community-ecosystem--bimodal)
- [The seven that matter](#the-seven-that-matter)
  - [1. nyldn/claude-octopus — direct prior art for `EXTERNAL_SHADOW=1`](#1-nyldnclaude-octopus--direct-prior-art-for-external_shadow1)
  - [2. vanzan01/claude-code-sub-agent-collective — hooks-as-invariants](#2-vanzan01claude-code-sub-agent-collective--hooks-as-invariants)
  - [3. ryoppippi/ccusage — passive ledger from JSONL](#3-ryoppippiccusage--passive-ledger-from-jsonl)
  - [4. obra/superpowers — the closest cultural match](#4-obrasuperpowers--the-closest-cultural-match)
  - [5. wshobson/agents — `comprehensive-review` and PluginEval](#5-wshobsonagents--comprehensive-review-and-plugineval)
  - [6. disler/claude-code-hooks-mastery — the canonical hooks reference](#6-dislerclaude-code-hooks-mastery--the-canonical-hooks-reference)
  - [7. Anthropic `explanatory-output-style` — the distribution primitive](#7-anthropic-explanatory-output-style--the-distribution-primitive)
- [Honorable mentions](#honorable-mentions)
- [Anti-patterns to refuse](#anti-patterns-to-refuse)
- [Comparison matrix — ours vs. ecosystem](#comparison-matrix--ours-vs-ecosystem)
- [What would make this repo SOTA](#what-would-make-this-repo-sota)
- [What to learn from the ecosystem without installing anything](#what-to-learn-from-the-ecosystem-without-installing-anything)
- [Open questions](#open-questions)
- [Why this is profound, not normal](#why-this-is-profound-not-normal)
- [Sources](#sources)

## The reframe — intellectual SOTA with an enforcement gap

The honest reading of the question "what will make our repo SOTA" assumes the repo is currently *behind* the ecosystem. The research disconfirms that assumption.

On the primitives the repo cares most about — the ones encoded in [CLAUDE.md](../../../CLAUDE.md) as non-negotiable — the public Claude Code ecosystem has no equivalent. No surveyed plugin or marketplace mandates contradicting-source retrieval; no surveyed plugin runs an outside-view reference-class step before generation; no surveyed plugin uses minority-veto across independent lenses with frame-level objections; no surveyed plugin pairs a same-family shadow lane with a comparator that emits agreement-class verdicts without overriding the primary panel; no surveyed plugin enforces a gate-on-disk-state for generation. On these primitives the repo is genuinely SOTA, and the rarity is not accidental — these primitives are *epistemically expensive* to design and *low-status to implement* compared to the visible flash of "100+ agents" or "1,400+ skills."

The repo's lag is on different primitives entirely — primitives that *are* widely shipped in the public ecosystem, that are *cheap* to build, and that the repo has explicitly noted but not prioritised. Hooks are the canonical example: at least four of the most-cited community projects (`disler/claude-code-hooks-mastery`, `vanzan01/claude-code-sub-agent-collective`, `nizos/tdd-guard`, the entire Anthropic `hookify` plugin) treat hooks as the *enforcement layer* for invariants. The repo's invariants — the step-9 hard gate, the path-discipline rule, the ledger writeback — are currently enforced by orchestrator obedience to prose. The script for path-discipline already exists at [bin/check-path-discipline.sh](../../../bin/check-path-discipline.sh) and is not hooked. The lab has filed adjacent observations (`casual-output-is-workflow-unprotected`, `subagents-claim-writes-not-on-disk`, `format-only-state-transition-gate`) which are all symptoms of the same general gap: *the repo trusts prose where the ecosystem trusts hooks.*

The reframe this entry proposes is: **the lab has been treating hook/observability proposals as competing with the deeper canon/panel/comparator work**, when in fact they are corrective rather than parallel. The deeper work has built the right primitives; the cheap work would make those primitives un-bypassable. Once seen this way, three filings the lab has been treating as future *normals* should be near-default *no-brainers*, and one filing (cross-family shadow) should be elevated as the highest-leverage *strategic* move because it is the one quality lever the same-family Opus/Sonnet shadow cannot reach.

## Methodology

Three research streams ran in parallel:

1. **Anthropic official** — what Anthropic itself ships, in which marketplaces, with what plugin format. Source coverage: `docs.claude.com`, `code.claude.com`, `github.com/anthropics/{claude-code,claude-plugins-official,claude-plugins-community,skills,life-sciences,knowledge-work-plugins}`.
2. **Community marketplaces** — major aggregators with quality triage. Source coverage: `wshobson/{agents,commands}`, `davila7/claude-code-templates` (aitmpl.com), `obra/superpowers-marketplace`, `disler/*`, `bmad-code-org/BMAD-METHOD`, `ruvnet/ruflo`, `EveryInc/compound-engineering-plugin`, `hesreallyhim/awesome-claude-*`, plus the long tail of star-inflated AI-slop repos.
3. **Notable individual primitives** — `chongdashu/cc-statusline`, `RonitSachdev/ccundo`, `ryoppippi/ccusage`, `nyldn/claude-octopus`, `GMaN1911/claude-cognitive`, `coleam00/claude-memory-compiler`, `mann1x/claude-hooks`, `vanzan01/claude-code-sub-agent-collective`, `nizos/tdd-guard`, `parcadei/Continuous-Claude-v3`, `thedotmack/claude-mem`, `trailofbits/skills-curated`, plus the Sequential Thinking MCP and Microsoft's Playwright MCP for primitive-shape comparison.

Quality signal weighted, in order: **maintainer credibility** outside Claude Code (a known committer, a real company, a published author), **README specificity** (named abstractions vs. role lists), **recent commit cadence**, **issue activity quality**. Star counts were treated as noise: the 2026 ecosystem contains multiple repos with implausible stars-per-day curves (`affaan-m/everything-claude-code` at 170k for a recent repo; `forrestchang/andrej-karpathy-skills` at 102k stars for a single CLAUDE.md file). Discounting these is not optional; including them is misleading.

## The Anthropic ecosystem in one section

### Three marketplaces, one schema

`claude-plugins-official` is the curated user-facing directory — auto-available at startup, surfaced in the `/plugin` Discover tab, and indexed at `claude.com/plugins`. Roughly 171 plugins total, 18 Anthropic-authored. `claude-plugins-community` is a read-only mirror with security-scanned community submissions via `clau.de/plugin-directory-submission`. The bundled-with-CLI marketplace lives inside the `claude-code` repo at `plugins/` with 13 plugins, all Anthropic-authored. A vertical marketplace exists for life sciences. Reserved marketplace names are spec-locked: third parties cannot squat them.

### The plugin format (what an installable plugin actually is)

A plugin is a directory tree with an optional `.claude-plugin/plugin.json` manifest where only `name` is required. Component types are skills (`skills/<name>/SKILL.md`, auto-invoked by description-match), commands (flat-file legacy form), agents (with frontmatter restrictions — plugin agents cannot define `hooks`, `mcpServers`, or `permissionMode`, by design, so a plugin can't escalate via its agents), hooks (`hooks/hooks.json` over ~13 lifecycle events), MCP servers (`.mcp.json`), LSP servers, output styles, monitors (persistent background processes), themes, and `bin/` executables added to `$PATH`.

The schema has a few sharp edges worth knowing. Versioning is two-mode and footgunny: setting `version` once means every release thereafter must bump it or users silently never update. The keychain budget for `sensitive` userConfig is ~2 KB *shared with OAuth tokens*. Plugin disable mid-session does NOT stop already-running monitors. Of the 171 official-directory plugins, ~10% have no listed `category`, so Discover-tab discoverability depends on tags that aren't always set. The schema URL referenced in `marketplace.json` (`anthropic.com/claude-code/marketplace.schema.json`) is a 404; the working URL is `json.schemastore.org/claude-code-marketplace.json`.

Install paths: `/plugin marketplace add <git-url-or-path>` then `/plugin install <name>@<marketplace>`. Or scriptable: `claude plugin install <plugin> [-s user|project|local|managed]`.

### Anthropic-authored plugins worth knowing exist

Not for installation here — most are general-purpose code-help and don't fit a no-target-codebase frame — but for **comparison** when designing in this repo. Two stand out:

- `code-review` deploys five parallel Sonnet reviewers with confidence-scored false-positive filtering. It's a different *shape* of multi-agent review than this repo's three-lens minority-veto panel. The repo's panel is shaped for *design* questions (architecture / operations / product); `code-review` is shaped for *code* artifacts (CLAUDE.md compliance / bugs / historical context / PR history / inline comments). The interesting question this raises is not "should we adopt their decomposition" — it's "have we thought clearly about what *kind* of review three-lens minority-veto is, and what kind it is not?"
- `explanatory-output-style` is a SessionStart-hook plugin that *replaces* the system prompt to inject educational commentary. It demonstrates that an entire workflow can be packaged as a single output-style + skill bundle. This is the cleanest distribution primitive in the Anthropic catalog and is the only viable mechanism for distributing the 12-step workflow itself to other repos.

The other Anthropic plugins (`commit-commands`, `feature-dev`, `frontend-design`, `hookify`, `learning-output-style`, `pr-review-toolkit`, `plugin-dev`, `ralph-loop`, `security-guidance`, `skill-creator`, plus a stack of LSP plugins) are useful tools, none of which alter how this repo operates.

## The community ecosystem — bimodal

The community side splits cleanly into a small high-signal set and a large noise floor.

**High-signal set:**
- `wshobson/agents` (~34.5k stars, active) — 184 agents, 16 workflow orchestrators, 150 skills, 98 commands across 78 single-purpose plugins, with a three-tier model strategy (Opus 4.7 / Sonnet 4.6 / Haiku 4.5) declared in the README. Single-author quality, named abstractions, real users.
- `davila7/claude-code-templates` (aitmpl.com, ~26.5k stars) — aggregator with web UI, CLI installer, live analytics, conversation monitor, health check. Trendshift-listed, sponsored. A real product, not a repo.
- `obra/superpowers-marketplace` + `obra/superpowers` — Jesse Vincent's curated workflow skills with Socratic brainstorming. Officially accepted into Anthropic's marketplace January 2026. Closest *cultural* match to this repo.
- `disler/claude-code-hooks-mastery` (~3.6k stars) and the companion `claude-code-hooks-multi-agent-observability` (~1.4k stars) — canonical hook-event reference and a real-time observability dashboard.
- `ryoppippi/ccusage` (~13.6k stars, very active) — pure local CLI that parses Claude Code JSONL transcripts for cost and token usage. The serious user's usage tool.
- `nyldn/claude-octopus` (~3.2k stars) — fans a coding task to up to 8 different AI models in parallel. Cross-family shadow triangulation as a plugin. Highest direct relevance to this repo's deferred work.
- `EveryInc/compound-engineering-plugin` (~15.9k stars) — Every's "Compound Engineering" methodology, cross-tool (Claude Code, Codex, Cursor). Methodology backed by a media outfit; useful as outside-view comparison against the 12-step workflow.
- `trailofbits/skills-curated` — small (~379 stars), but Trail of Bits curates. Trust signal worth borrowing simply by reading their inclusion/exclusion criteria.
- `bmad-code-org/BMAD-METHOD` and `SuperClaude-Org/SuperClaude_Framework` — heavy SDLC frameworks; methodology-rich, structurally similar to this repo's artifact-handoff approach. Worth skimming, not installing.

**Noise floor — explicit anti-patterns:** `VoltAgent/awesome-claude-code-subagents` (~18.8k stars) and `VoltAgent/awesome-agent-skills` (~19.5k stars), both kitchen-sink role-list collections; `rohitg00/awesome-claude-code-toolkit` ("135 agents, 35 skills, 42 commands, 176+ plugins, 20 hooks, 15 rules, 7 templates"); `alirezarezvani/claude-skills` ("232+ skills... 8 more coding agents"); `jeremylongshore/claude-code-plugins-plus-skills` ("423 plugins, 2849 skills, 177 agents"); `sickn33/antigravity-awesome-skills` ("1,400+ skills"); `affaan-m/everything-claude-code` (170k stars, recent — botted); `forrestchang/andrej-karpathy-skills` (102k stars for a single CLAUDE.md — botted); `JuliusBrussee/caveman` (a meme repo at 51k). These are the AI slop pattern this repo's CLAUDE.md was written against. The ecosystem evidence supports that warning: the strongest community plugins all *refuse* role-list breadth. Generic role lists ("frontend-developer", "backend-developer", "marketing-c-level-advisor") are not primitives.

The `ruvnet/ruflo` (formerly `claude-flow` / `hive-mind`) repo deserves a separate mention. It is not slop — there is real engineering — but its central primitive (peer-to-peer agent messaging between specialized workers) is exactly the failure mode the shadow-comparator is trying to *detect*. Importing it would correlate the lenses by design. This is a case where the ecosystem's most ambitious project is, for *this* repo's frame, an explicit anti-pattern.

## The seven that matter

Rank-ordered by relevance to *this* repo's frame. Each is investigated against three questions: what does it do, what would it change here, install / steal / skip.

### 1. nyldn/claude-octopus — direct prior art for `EXTERNAL_SHADOW=1`

The plugin fans a coding task to up to 8 different AI models in parallel — across families (OpenAI, Google, Anthropic, local) — and surfaces blind spots and disagreements. This is **literally cross-family shadow triangulation as a plugin**. The deferred work in [`upgrades/profound/2026-04-26-critic-panel-correlated-by-default/`](../2026-04-26-critic-panel-correlated-by-default/README.md) names this gap explicitly: the comparator is currently same-family (Opus + Sonnet) and same-family models are correlated by training data, so the comparator's "shadow disagreement" signal is structurally bounded. Cross-family shadow is the one quality lever same-family cannot reach.

It is plausible that octopus has already solved the wrapper-script primitive that's currently blocking `EXTERNAL_SHADOW=1`. The frame doesn't transfer — octopus's "one task, eight implementations, pick best" frame is incompatible with this repo's "one decision, three lenses, minority-veto" frame — but the *plumbing* (how to invoke a non-Anthropic model from inside an Agent run with safe credential handling) is exactly what this repo needs.

**Verdict: Steal — read the source carefully, port the wrapper-script primitive, do not install.** This is the single highest-leverage steal in the entire research set. It unblocks an entry that has been deferred for months because of one missing primitive.

### 2. vanzan01/claude-code-sub-agent-collective — hooks-as-invariants

A routing-agent with 30+ TDD-enforcing specialists, with hooks at SessionStart (load behavioral rules), PreToolUse (directive enforcement), and post-task (TDD validation). The primitive worth stealing is *hooks-as-invariants*: their RED/GREEN/REFACTOR cycle is enforced by hook, not by prompt. The repo can ignore the TDD layer entirely (wrong primitive — there is no target codebase here, tests are not the artifact) and adopt the meta-pattern: convert soft prose-enforced gates into hard disk-state-enforced hooks.

Concretely, the repo has at least three soft gates that should be hooks: the step-9 generator gate (require `scope-map.md` and `challenges.md` on disk), the path-discipline check (the script already exists at [bin/check-path-discipline.sh](../../../bin/check-path-discipline.sh) and is not hooked), and ledger writeback after synthesis. None of these requires deep design — they require one `hooks.json` and three short shell wrappers.

**Verdict: Steal the meta-pattern, build a small `.claude/hooks/hooks.json` with the three entries.** This is what the lab has been calling Tier-A or *no-brainer* work.

### 3. ryoppippi/ccusage — passive ledger from JSONL

The CLI parses local Claude Code JSONL transcripts and computes per-session and per-day cost and token usage. Pure local, no API key, no daemon. The insight: the JSONL transcripts already contain ground truth for cost and token counts. The repo's `ledger.md` is hand-counted at step 13 by the orchestrator. Dual-sourcing — one count from orchestrator memory, one count from JSONL — turns disagreement itself into a quality signal. If the two counts agree, the orchestrator-counted ledger is validated. If they disagree, either the orchestrator is miscounting or the JSONL is being mis-parsed; either case is informative.

**Verdict: Install for personal use, steal the JSONL-parsing approach as a second source for the ledger.** Lowest-cost / highest-ROI combination in the report — a one-evening spike that produces a verifiable artifact and a falsifiable result.

### 4. obra/superpowers — the closest cultural match

Jesse Vincent curates ~20 composable skills plus brainstorm/plan/execute commands, a skills-search tool, and SessionStart context injection. The standout skill is **Socratic brainstorming**: the agent refuses to write code until multiple-choice intent-disambiguation questions are answered, producing a design doc that the user approves before any implementation begins.

The repo's reframe step (step 2) restates the user's question in a new framing — but never *asks* the user. A bounded multi-choice interrogation **before classification** could sharpen weak requirements in a way reframe alone cannot. This is not a duplicate of reframe; it is a complement. Reframe is the orchestrator's challenge to the user's framing; Socratic interrogation is the orchestrator's request for the user's clarification. Different jobs.

**Verdict: Steal the multi-choice interrogation pattern — wire it as an optional opt-in pre-step-1 surface.** Also: the SessionStart context-injection primitive is not used anywhere in the repo and is the natural mechanism for the SessionStart-recall pattern (see [Honorable mentions](#honorable-mentions)).

### 5. wshobson/agents — `comprehensive-review` and PluginEval

The `comprehensive-review` plugin in this catalog is the closest direct analog to this repo's three-lens panel — an architect-review + code-reviewer + security-auditor trio. Comparing their lens decomposition against (architecture / operations / product) is a free outside-view check on whether the repo's lenses are well-chosen. The honest read: the wshobson trio is closer to the natural axes of *code* review (structure / correctness / safety); the repo's trio is the natural axes of *design* review (invariants / cost-and-blast-radius / user-experience-of-the-decision). These are different jobs. But the question deserves an explicit lab investigation rather than an assumption.

The repo could also borrow **PluginEval**, wshobson's 10-dimension plugin evaluation rubric, as a basis for evaluating which plugins to install — and possibly adapt it as a self-evaluation rubric for this repo's own `upgrades/` entries before they advance to `accepted`.

**Verdict: Steal — borrow the `comprehensive-review` decomposition as a reference; consider PluginEval as a self-evaluation rubric.** Do not install: 184 agents in one repo violates the "tight, named primitives" discipline this repo enforces.

### 6. disler/claude-code-hooks-mastery — the canonical hooks reference

Tutorial repo demonstrating all ~13 hook lifecycle events with working examples — UserPromptSubmit validation, TTS feedback, dangerous-command blocking, hook-event logging, transcript extraction, Builder/Validator team-validation. The companion `claude-code-hooks-multi-agent-observability` repo is a real-time dashboard over hook events.

The repo has zero hooks today, so the mastery tutorial is the right reference when entry #2 (hooks-as-invariants) lands. The observability dashboard is interesting but should be sequenced *after* the hooks themselves: dashboards over zero hook events are not useful.

One disler primitive deserves separate attention: **UserPromptSubmit as a pre-classifier**. The bypass-routing decisions in this repo (`quick take`, `skip-critic`, factual question) currently happen inside the orchestrator's reasoning. Moving them to a deterministic UserPromptSubmit hook would make routing un-bypassable and audit-loggable. This is a smaller version of the same hooks-as-invariants pattern.

**Verdict: Read both; build the three-hook minimum first; layer observability later.**

### 7. Anthropic `explanatory-output-style` — the distribution primitive

A SessionStart-hook plugin that replaces the system prompt to inject educational commentary. The mechanism — *output style replacement* — is distinct from skills (additive) and CLAUDE.md (additive). Output styles *replace* default behaviour. The 12-step workflow could be repackaged as a single output-style + skill bundle, installable as one plugin into another repo's `~/.claude/`. The cleanest possible distribution surface for this stack.

**Verdict: Steal — file a future Tier-C entry investigating workflow-as-output-style packaging.** Not urgent. But the only viable mechanism for the workflow to spread.

## Honorable mentions

`GMaN1911/claude-cognitive` and `coleam00/claude-memory-compiler` show how Stop and SessionStart hooks turn Claude Code into a state machine over a vector store. The repo has session-artifacts (write-once) but no automatic recall on session start. A Stop hook fingerprints `synthesis.md` (label + frame + decision). A SessionStart hook surfaces the top-3 prior sessions matching the current `requirement.md` classification *as canon-passages, never as conclusions*. Decay model from claude-cognitive prevents stale anchoring (older decisions weigh less in retrieval). This makes session-artifacts compounding rather than write-once. Worth a future Tier-B entry — tightly scoped to "recall as canon, not as authority."

`chongdashu/cc-statusline` is a low-cost statusline showing context %, session cost, model, git, token analytics. Surfaces ledger thresholds *during* a session, not only after. Direct extension of the existing ledger work.

`parcadei/Continuous-Claude-v3` is a "ledger and handoffs" plugin. Reading their ledger schema against [.claude/session-artifacts/README.md](../../../.claude/session-artifacts/README.md) is a free outside-view check on this repo's ledger design.

`thedotmack/claude-mem` and `bmad-code-org/BMAD-METHOD` are higher-volume; both repay skimming, neither repays installing. BMAD's "Scrum Master story embedding" — expanding plans into stories that contain *all* upstream context inline — is a stronger version of what this repo's distillations do at step 6, and worth examining if distillations ever feel too lossy.

The Sequential Thinking MCP and Microsoft's Playwright MCP are mentioned for completeness only. Sequential Thinking duplicates the `## Revision N` blocks already in `frame.md`; Playwright requires a browser surface this repo doesn't have.

## Anti-patterns to refuse

The research surfaced four explicit anti-patterns that should *not* be imported, named here so the lab can refuse them later without re-deriving the reasoning.

**Peer-to-peer agent messaging** (`ruvnet/ruflo`, hive-mind topologies). Correlates lenses by sharing context between independent reviewers. Defeats the entire shadow-comparator design. The strength of independent critic lenses comes from non-communication.

**TDD-style RED/GREEN/REFACTOR enforcement** (`vanzan01`, `nizos/tdd-guard`, `obra/superpowers` tdd skills). Wrong primitive for this repo. There is no target codebase; tests are not the artifact. Importing TDD enforcement here would impose a vocabulary that has no referent.

**Generic memory MCPs** (Mem0, Zep, MemPalace). Extract "facts" from conversations and re-inject as bullet points. The unit here is "decision under a frame," not "fact." A purpose-built session-recall MCP that surfaces past `synthesis.md` documents matching the current classifier label would be more valuable than a generic fact-extractor. **Caution flag:** MemPalace went viral in April 2026 then was debunked — LongMemEval gains traced to its underlying vector store, not the "Palace" architecture. The community is currently noisy on memory benchmark claims; default to skepticism through 2026.

**Swarm orchestration** (`claude-swarm`, ruflo's swarm patterns). The workflow is sequential-with-parallel-fan-out by design. Swarms add coordination cost without quality gain on a single decision-question. The 12-step workflow already does the only kind of parallelism that's useful here (independent fan-out of subagents in steps 3–5 and 10).

## Comparison matrix — ours vs. ecosystem

| Primitive | This repo | Best ecosystem analog | Status |
|---|---|---|---|
| 12-step orchestrated workflow | Live, prose-enforced | EveryInc compound, BMAD, SuperClaude | **SOTA** — leading on rigour (hard gates, mandatory contradiction, outside-view) |
| Multi-lens minority-veto | 3 lenses, Opus | wshobson `comprehensive-review` (3 specialists) | **Comparable** — frame-level objection requirement is unique here |
| Shadow-model triangulation (same-family) | Opus + Sonnet + comparator | None known at this shape | **SOTA / unique** |
| Cross-family shadow | Reserved as `EXTERNAL_SHADOW=1`, inert | nyldn/claude-octopus (8-way fan-out) | **Different shape — gap** |
| Mandatory contradicting canon | Live, librarian-first | None known | **Unique — likely a moat** |
| Outside-view reference-class | Live, non-negotiable step | None known | **Unique** |
| Per-session ledger | Hand-counted at step 13 | parcadei (different schema); ryoppippi ccusage (passive) | Equivalent; **dual-sourcing extends the lead** |
| R&D idea lab with state machine | Live, un-automated | None at this granularity | **Unique** |
| Hooks | None | disler, vanzan01, Anthropic hookify | **Behind — should adopt** |
| Live observability | None | chongdashu cc-statusline, davila7 analytics, disler dashboard | **Behind — should adopt** |
| SessionStart prior-session recall | None | claude-cognitive, claude-memory-compiler | **Gap — worth filing** |
| Plugin-format distribution | None | All ecosystem | **Strategic gap** |

The asymmetry is the entry's thesis. SOTA on the rare/intellectual primitives; behind on the cheap/enforcement primitives.

## What would make this repo SOTA

Three tiers, in order of leverage. Each maps to a concrete future filing.

**Tier A — install/build now (highest ROI, lowest cost, all should-be no-brainers).**

A1. **Three hooks: PreToolUse hard-gate, pre-commit path-discipline, post-synthesis ledger.** Convert the three soft-enforced disciplines into hooks. The path-discipline script already exists; wire it. Reference: vanzan01 + disler.

A2. **Dual-source the ledger from JSONL.** Add a small script (`bin/ledger-from-jsonl.sh` or `.js`) that parses the session's JSONL transcript and emits the count fields. Compare against the orchestrator-counted version. Disagreement is signal. Reference: ryoppippi/ccusage.

A3. **Statusline showing context %, session cost, loop count, ledger warnings.** Surface ledger thresholds during the session, not only after. Reference: chongdashu/cc-statusline.

**Tier B — design and prepare (highest strategic value).**

B1. **Solve `EXTERNAL_SHADOW=1` by porting nyldn/claude-octopus's wrapper primitive.** The deferred work in [`upgrades/profound/2026-04-26-critic-panel-correlated-by-default/`](../2026-04-26-critic-panel-correlated-by-default/README.md) becomes feasible if their plumbing is reusable. Cross-family shadow is the single largest quality lever the comparator can have — same-family shadows are correlated by training data; cross-family disagreement is a different signal class.

B2. **SessionStart classification-matched recall, as canon-passages.** A Stop hook fingerprints `synthesis.md`. A SessionStart hook surfaces the top-3 prior sessions matching the current classification *as canon-passages, never as conclusions*. Decay model prevents stale anchoring. Reference: claude-cognitive + claude-memory-compiler.

B3. **Pre-classifier Socratic interrogation (opt-in).** Bounded multi-choice intent disambiguation before step 1 fires, for weak/ambiguous requirements. Reference: obra/superpowers brainstorming skill.

**Tier C — strategic, defer.**

C1. **Repackage the workflow as a distributable Anthropic-marketplace plugin.** The `explanatory-output-style` plugin shape is the model. Distribution = audience = correction signal.

C2. **Cross-session ledger aggregator.** A small script that walks `.claude/session-artifacts/*/ledger.md` and surfaces drift trends. Reference: disler observability dashboard.

## What to learn from the ecosystem without installing anything

The hardest-earned insight from the survey is that *most* "Claude Code plugins" are role-list slop. The good repos share three traits: named, specific primitives instead of role lists; maintained by individuals with reputation outside Claude Code; READMEs that describe *mechanism*, not *outcomes*. The CLAUDE.md discipline against generic agent collections is correct; the ecosystem evidence supports it.

Six lessons absorbable without installing anything:

1. **Hooks are the right enforcement layer for invariants.** Prompt-obedience is a soft gate; hooks are a hard gate. The lab has filed this observation in adjacent forms (`casual-output-is-workflow-unprotected`, `subagents-claim-writes-not-on-disk`); the ecosystem confirms it generally.
2. **Transcripts are forensic ground truth.** The ledger should at least cite transcript line ranges where useful, not only counts. Possibly a future small entry.
3. **Output styles replace, skills add, CLAUDE.md guides** — three distinct distribution primitives. This repo uses only the third.
4. **"Memory" claims are noisy in 2026.** Check whether reported gains come from architecture or underlying vector store. MemPalace's debunking is the canonical recent example.
5. **Star counts are noise.** Maintainer credibility, README specificity, and recent commit cadence are the actual signals. Bot-inflated repos are common enough now to require deliberate filtering.
6. **Anthropic's `code-review` plugin uses 5 parallel Sonnet reviewers with confidence-scored FP filtering** — a different shape of multi-agent review than minority-veto. The interesting lab question this raises is *what kind of review minority-veto is good for, and what kind it is not.*

## Open questions

1. **Is `comprehensive-review` (architect / code-reviewer / security-auditor) a better lens decomposition than (architecture / operations / product)?** Outside-view says they're for different jobs (code review vs. design review). But the repo has not actually run the comparison. Worth a future investigation entry rather than a default assumption.
2. **Does cross-family shadow surface different signal than same-family shadow?** The hypothesis behind `EXTERNAL_SHADOW=1` is unfalsified until the wrapper exists. Cheapest experiment: run 5–10 sessions in `SHADOW_PANEL=1` mode side-by-side with a manual GPT-4 / Gemini lens and measure agreement-class distribution.
3. **Will hooks degrade orchestrator agency in unintended ways?** vanzan01's hook-driven TDD enforcement is famously rigid. The repo's hard gate must enforce *the gate* without enforcing *the path through the gate* — needs design care in A1.
4. **Should the canon library systematically ingest Claude Code plugin manifests as research material?** I.e., is there a frame under which the ecosystem itself becomes a source the canon-librarian queries, rather than an external comparison target? Possible future entry.
5. **What is the minimum-viable distributable package?** If the workflow ever ships as a plugin, what is the smallest unit that preserves its discipline? Whole 12 steps? Just the panel? Just the canon-librarian? The answer is non-obvious.

## Why this is profound, not normal

Filed at profound rather than normal because the value of the entry is in **the seeing** — the reframe that the repo's lag is enforcement, not thinking — and that reframe changes how future lab filings should be evaluated. Multiple already-filed observations (`casual-output-is-workflow-unprotected`, `subagents-claim-writes-not-on-disk`, `format-only-state-transition-gate`) are visibly the same shape once the reframe is named: each is a case of prose-enforcement that should be hook-enforcement. The reframe makes them legible as a class, not as isolated observations. That is the kind of seeing-shift profound is for.

The proposals downstream (the three Tier-A no-brainers, the three Tier-B strategics, the two Tier-C deferrals) are *consequences* of the reframe, not the entry's primary value. Some of them will be filed as their own entries; some will be absorbed into existing entries; some will be quietly dropped. The reframe stands either way.

## Sources

**Anthropic official:**
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community)
- [anthropics/claude-code (bundled plugins)](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
- [anthropics/skills marketplace.json](https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json)
- [anthropics/life-sciences](https://github.com/anthropics/life-sciences)
- [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- [Plugins reference docs](https://code.claude.com/docs/en/plugins-reference)
- [Plugin marketplaces docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Skills docs](https://docs.claude.com/en/docs/claude-code/skills)
- [Hooks reference](https://code.claude.com/docs/en/hooks)
- [explanatory-output-style](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)

**Community Tier 1:**
- [wshobson/agents](https://github.com/wshobson/agents)
- [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)
- [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) · [obra/superpowers](https://github.com/obra/superpowers)
- [obra/superpowers brainstorming SKILL.md](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md)
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) · [disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)
- [ryoppippi/ccusage](https://github.com/ryoppippi/ccusage)
- [nyldn/claude-octopus](https://github.com/nyldn/claude-octopus)
- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)

**Community Tier 2:**
- [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
- [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- [ruvnet/ruflo](https://github.com/ruvnet/ruflo)
- [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
- [nizos/tdd-guard](https://github.com/nizos/tdd-guard)
- [parcadei/Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3)
- [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated)
- [vanzan01/claude-code-sub-agent-collective](https://github.com/vanzan01/claude-code-sub-agent-collective)
- [chongdashu/cc-statusline](https://github.com/chongdashu/cc-statusline)
- [GMaN1911/claude-cognitive](https://github.com/GMaN1911/claude-cognitive) · [coleam00/claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler) · [mann1x/claude-hooks](https://github.com/mann1x/claude-hooks)
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)
- [RonitSachdev/ccundo](https://github.com/RonitSachdev/ccundo)

**Concept references:**
- [Sequential Thinking MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
- [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- [Anthropic Skills as open standard (Dec 2025)](https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/)
- [Mem0 vs Zep vs LangMem 2026](https://dev.to/anajuliabit/mem0-vs-zep-vs-langmem-vs-memoclaw-ai-agent-memory-comparison-2026-1l1k)
- [Mem0 Claude Code integration](https://docs.mem0.ai/integrations/claude-code)

**Internal references:**
- [upgrades/profound/2026-04-26-critic-panel-correlated-by-default](../2026-04-26-critic-panel-correlated-by-default/README.md) — the deferred `EXTERNAL_SHADOW=1` work this entry maps prior art onto
- [upgrades/profound/2026-04-26-casual-output-is-workflow-unprotected](../2026-04-26-casual-output-is-workflow-unprotected/README.md) — same-shape prose-enforcement observation
- [upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk](../2026-04-26-subagents-claim-writes-not-on-disk/README.md) — same-shape disk-vs-claim observation
- [upgrades/profound/2026-04-27-r-and-d-lab-thesis](../2026-04-27-r-and-d-lab-thesis/README.md) — the thesis this reframe is consistent with
- [.claude/session-artifacts/README.md](../../../.claude/session-artifacts/README.md) — ledger schema, the comparator-target for A2
- [bin/check-path-discipline.sh](../../../bin/check-path-discipline.sh) — the un-hooked enforcement script named in A1
- [CLAUDE.md](../../../CLAUDE.md) — the prose-enforcement layer the reframe argues against
