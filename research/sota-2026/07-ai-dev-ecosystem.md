# The AI-Assisted Development Tool Ecosystem, mid-2026

Survey of the ecosystem as of May 2026, biased toward one question: *what does each tool do well that the Claude-Code-based 12-step workflow in this repo's [CLAUDE.md](../../CLAUDE.md) could borrow?* Four parts: tool-by-tool, cross-cutting patterns, community workflow patterns, top-15 import list.

---

## Part 1 — Tool-by-tool

### 1. Aider (`Aider-AI/aider`)

**Signal.** ~41.6k stars, 5.3M+ PyPI downloads; 2025-2026 added GPT-5 / Claude 4.x / Gemini 2.5 Pro, prompt caching, polyglot leaderboard, watch-mode AI! comments. In active production use.

**Does well.** (1) *Architect/editor pair* — strong reasoner plans, cheap precise model emits the diff, addressing the structural failure where frontier models reason well but mangle structured-diff output. (2) *Git-commit-per-prompt* — every accepted edit becomes a commit; grep-able, bisect-able, no shadow state.

**Worth borrowing.** The architect/editor split as a *role-pair* primitive for step 9. The generator currently runs as a single model voice; an "architect writes skeleton, editor fills in citations" pair would let the orchestrator route reasoning effort honestly.

**Falls short.** No persistent project memory beyond `.aider.conf.yml`; no plan-mode; `/add` puts context management on the user; no critic panel. A *pair-programmer*, not an *adversarial reviewer*.

Refs: [Aider-AI/aider](https://github.com/Aider-AI/aider), [aider.chat](https://aider.chat/).

### 2. Cursor

**Signal.** Cursor 3 (April 2, 2026): Agents Window for parallel agents, Design Mode, best-of-N model comparison, cloud↔local handoff. Rules moved from `.cursorrules` to scoped `.cursor/rules/*.md`. Mainstream AI-native IDE.

**Does well.** (1) *Scoped rules with glob targeting* — `.cursor/rules/python-backend.md` activates only on matching files; same convention covers Skills and Hooks. The cleanest "rules" implementation; partitioning solves the "rules file got too big, agent ignored half" failure. (2) *Parallel agents* in the Agents Window with best-of-N model comparison — consumer-facing lane diversity.

**Worth borrowing.** *Glob-scoped instruction files.* A `.claude/rules/<scope>.md` pattern activating on artifact-path globs (one ruleset for `session-artifacts/**`, another for `upgrades/**`) scales the project-instruction surface without growing CLAUDE.md past the ~200-line attention threshold.

**Falls short.** Closed-source; agent loop opaque; rules-conflict resolution undocumented; no native frame-challenger or critic.

Refs: [cursor.com/changelog](https://cursor.com/changelog), [Cursor 2.0 changelog](https://cursor.com/changelog/2-0).

### 3. Continue (`continuedev/continue`)

**Signal.** Actively developed; `config.yaml`-driven; OSS plugin for VS Code and JetBrains. Bet: *openness as architecture* — rules, prompts, slash commands, context providers, MCP servers all under one schema.

**Does well.** (1) *`@`-mention context providers as first-class extension points* — `@open-files`, `@git-diff`, `@terminal`, `@docs`, plus MCP-backed sources. Inverse of Cursor's implicit context; cheaper to reason about for high-stakes decisions. (2) *Slash commands as named prompt templates with model routing* — `/new-endpoint` pins a model, declares its context providers, encodes convention.

**Worth borrowing.** *Context providers as a named primitive.* The canon-librarian, outside-view, and Explore returns are all context-provider returns but currently agent-internal. Reifying them as named replayable providers lets later steps cite specific outputs without re-running the agent.

**Falls short.** Wide `config.yaml` surface; slow onboarding; weak defaults; chat UI lags Cursor and Cline.

Refs: [docs.continue.dev/customize/overview](https://docs.continue.dev/customize/overview), [docs.continue.dev/customize/slash-commands](https://docs.continue.dev/customize/slash-commands).

### 4. Cline (`cline/cline`, formerly Claude Dev)

**Signal.** ~40k+ stars; sidebar in VS Code, JetBrains, Cursor, Windsurf, Zed, Neovim, plus a preview CLI. Reference implementation of "approve-each-step." In active production use.

**Does well.** (1) *Plan/Act mode separation as a UI primitive* — Plan reads and proposes without edits; Act executes step-by-step with per-step approval. The cleanest "explore → plan → code" implementation in a sidebar agent. (2) *Checkpoints via shadow git repo* — snapshot after every tool use; one-click rollback; main git history untouched.

**Worth borrowing.** *Shadow-repo checkpoints for orchestrator runs.* A snapshot per numbered step (not per file edit) lets the orchestrator revert to "state after step 6 distillation" if step 9 goes wrong — cleaner than "delete the session directory and re-run."

**Falls short.** Approve-each-step is high-friction; users habituate and auto-approve, defeating the safety story. No frame-challenger; no minority-veto critic.

Refs: [cline/cline](https://github.com/cline/cline), [docs.cline.bot/features/checkpoints](https://docs.cline.bot/features/checkpoints).

### 5. Roo Code (`RooCodeInc/Roo-Code`)

**Signal.** **Project shut down May 15, 2026** (Matt Rubens announcement April 21). Extension, Cloud, Router all sunset. Forks exist; treat as a *historical lesson*.

**Did well.** (1) *Named modes as personas with locked toolsets* — Architect / Code / Debug / Ask / Custom, each activating a subset of tools and a specific model; Custom let teams ship reusable personas. (2) *Diff-based editing* — only changed lines over the wire; ~30% token savings.

**Worth borrowing.** *Named-mode session profiles.* Operator-level `--profile=migration-decision` vs `--profile=new-feature` at step 1, pre-loading which subagents are mandatory vs optional.

**Fell short.** The shutdown is the lesson: a fork with team-collab features still needs sustaining funding. Borrow the patterns, not the operating model.

Refs: [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code).

### 6. Codex CLI (`openai/codex`)

**Signal.** OpenAI's terminal agent. May 2026 release: persisted `/goal` workflows, MultiAgentV2 with thread caps and root/subagent hints, external-agent session import, plugin marketplace, plugin-bundled hooks, in-app browser, `codex update`, expanded permission profiles. In production use.

**Does well.** (1) *Persisted goals* — `/goal` is a named, resumable, multi-session unit of work; create/pause/resume/clear via TUI; solves "came back to a half-finished task and the agent lost the thread." (2) *Explicit permission profiles* — sandbox CLI profile selection, cwd controls, active-profile metadata exposed to clients.

**Worth borrowing.** *Sessions as persisted goals with explicit resume semantics.* The `session-artifacts/<id>/` directories are already proto-goals; a `/resume <id>` operator command would re-hydrate state from decision-log and ledger.

**Falls short.** Tied to OpenAI billing/models; MultiAgentV2 is configuration-heavy; no first-class adversarial-review primitive.

Refs: [openai/codex](https://github.com/openai/codex), [developers.openai.com/codex/changelog](https://developers.openai.com/codex/changelog).

### 7. Goose (formerly `block/goose`, now under AAIF / Linux Foundation)

**Signal.** ~44k stars; moved from Block to AAIF (Linux Foundation) late 2025. 70+ MCP extensions, 15+ LLM providers, desktop + CLI + embeddable API. Apache 2.0. In active production use.

**Does well.** (1) *Extensions as a first-class marketplace, all via MCP* — MCP is *the* tool surface, not a bolt-on. (2) *Multi-surface deployment* — same agent runs as desktop GUI, CLI, or library; same goose driven by a human or another agent.

**Worth borrowing.** *Subagents-as-MCP-servers.* Reframing canon-librarian / outside-view / critic lenses as MCP servers makes the critic stack portable to Cline, Cursor, or Goose.

**Falls short.** General-purpose, not coding-specific; single-track plan-and-execute; no multi-lens critique.

Refs: [github.com/block/goose](https://github.com/block/goose), [block.xyz/inside/block-open-source-introduces-codename-goose](https://block.xyz/inside/block-open-source-introduces-codename-goose).

### 8. OpenCode (`sst/opencode`)

**Signal.** Terminal-native Go-based TUI. Multi-provider. Client/server architecture — the TUI is one client among possible others (mobile, custom). Growing among neovim users.

**Does well.** (1) *Client/server separation* — agent runs as a daemon; the TUI is just one front-end; decouples *where the agent runs* from *where the human sits*. (2) *LSP integration as context source* — symbol definitions, references, diagnostics from Language Server, not filesystem scraping.

**Worth borrowing.** *Daemon-mode orchestration with multiple clients.* A long 12-step session today dies with the terminal; a daemon split would let the user attach a phone client for status without disrupting the orchestrator.

**Falls short.** Code-heavy configuration; power-user TUI; no built-in adversarial review; provider sprawl over depth.

Refs: [sst/opencode](https://github.com/sst/opencode), [opencode.ai/docs](https://opencode.ai/docs/).

### 9. Devin (Cognition)

**Signal.** Cognition raising at $25B valuation (April 2026). Devin 2.2: self-reviewing PRs, 3× faster startup. Infosys partnership for enterprise. In commercial use, but autonomy claims outrun delivery — early-2025 benchmarks pinned end-to-end completion at single-digit to low-double-digit percent on complex tasks.

**Does well.** (1) *Self-reviewing PRs* — Devin re-reads its candidate as a reviewer and fixes own-goals before opening the PR. Self-correction loop as product. (2) *Long-running async sessions* — hand off a task, close laptop, come back to a PR; startup cost amortized.

**Worth borrowing.** *Cheap self-review before the expensive panel.* The panel at step 10 is expensive (3-6 lenses); a single-model self-critique pass between step 9 and step 10 filters obvious own-goals first.

**Falls short.** Autonomy claims outrun delivered capability; "Devin does not understand trade-offs the way experienced engineers do" is the widely-shared summary. Closed source; opaque loop; high per-session cost.

Refs: [cognition.ai/blog/introducing-devin-2-2](https://cognition.ai/blog/introducing-devin-2-2), [siliconangle 2026-04-23 valuation piece](https://siliconangle.com/2026/04/23/cognition-creator-ai-software-engineer-devin-talks-raise-hundreds-millions-25b-valuation/).

### 10. GitHub Copilot Workspace / Copilot Agent

**Signal.** Copilot's autonomous multi-step agent (March 2026) in VS Code and JetBrains; assigning a GitHub issue spawns a background agent that produces a PR. Copilot Workspace pairs spec/plan/implementation. Copilot App (May 2026 preview): Interactive/Plan/Autopilot session modes, Agent Merge for autonomous conflict/CI/security-alert resolution. In production at GitHub scale.

**Does well.** (1) *Issue → PR as the unit of agent work* — leverages the well-shaped GitHub primitive (title, body, comments, labels, linked-PR-merges-as-done) rather than inventing a task primitive. (2) *Closed-loop review/fix* — Copilot Review finds an issue, hands the suggestion to the coding agent, fix-PR generated; cycle runs without humans until final review.

**Worth borrowing.** *Make the artifact the unit of work, not the chat.* An "open synthesis as a draft PR against a `synthesis/` branch" exit hatch turns each decision into a diffable, commentable artifact rather than a markdown file.

**Falls short.** Tied to GitHub; reasoning invisible; closed-loop fix can mask design problems with syntactic churn; Autopilot is the "trust us" extreme.

Refs: [github.com/features/copilot/agents](https://github.com/features/copilot/agents), [code.visualstudio.com/docs/copilot/copilot-cloud-agent](https://code.visualstudio.com/docs/copilot/copilot-cloud-agent).

### 11. Sourcegraph Cody

**Signal.** Enterprise; monorepos exceeding 90GB and multi-repo across 300k+ repos. Hybrid dense-sparse vector retrieval tailored for code. 1M-token windows.

**Does well.** (1) *RAG that knows about code, not just text* — combines embedding search, code-graph lookup (definitions, references, types), reranker; "who calls this function" returns call-graph truth, not similarity guess. (2) *Multi-repo context as a first-class concept* — API consumers in repo B retrievable when you ask about an API definition in repo A.

**Worth borrowing.** *Code-graph-aware retrieval for canon.* Move canon-librarian from markdown grep + embeddings toward structural retrieval — "give me every entry that contradicts this passage" or "every entry citing this same primary source." The anti-confirmation-bias rule needs structural signal to enforce itself.

**Falls short.** Enterprise pricing; heavy RAG infra; not a workflow agent — retrieval+chat, not autonomous editor.

Refs: [sourcegraph.com/docs/cody](https://sourcegraph.com/docs/cody), [sourcegraph.com/blog/how-cody-understands-your-codebase](https://sourcegraph.com/blog/how-cody-understands-your-codebase).

### 12. Tabnine and Windsurf (formerly Codeium)

**Signal.** Windsurf now owned by Cognition; ships SWE-1.5, Codemaps (AI-annotated visual code maps), Cascade (the agent), Fast Context via SWE-grep, free Tab completions. Tabnine remains enterprise-positioned with on-prem and air-gap; agentic capabilities trail.

**Do well.** (1) *Windsurf — Codemaps.* Visual maps of code structure with grouped sections, trace guides, precise line-level linking — *agent output as navigable diagram*. Reviewer sees what the agent thinks the architecture is before reading any diff. (2) *Tabnine — on-prem/air-gap deployment.* Underserved "cannot send our code out" segment; the deployment story is the differentiator, not the model.

**Worth borrowing.** *Codemap-style structural synthesis artifact* alongside step-12 prose — blast-radius gut check faster than reading end-to-end.

**Fall short.** Windsurf Codemap closed-source and SWE-1.5 retrieval opaque; Tabnine's agentic loop weak relative to completion strength.

Refs: [windsurf.com](https://windsurf.com/), [vibecoding.app/blog/windsurf-review](https://vibecoding.app/blog/windsurf-review).

### 13. Plandex (`plandex-ai/plandex`)

**Signal.** Terminal-based; 2M-token direct context (~100k per file); tree-sitter project maps for 20M+ token directories; cumulative diff sandbox; plan branches for exploring multiple paths or comparing models. Smaller user base, distinctive design.

**Does well.** (1) *Diff sandbox as staging area* — edits accumulate separately from the working tree; user reviews cumulative diff before any of it lands. Stronger than Cline's per-edit checkpoints. (2) *Plan-branches* — same starting point, branch the plan ("Claude vs GPT-5" or "approach A vs B"); inspect both, promote one.

**Worth borrowing.** *Plan-branches as a frame-challenger primitive.* Step 8 produces alternative frames but not alternative implementations; a branch primitive lets step 9 emit two candidates from two frames in parallel and step 10 evaluate both.

**Falls short.** Terminal-only; steep configuration; text-only sandbox UI; smaller ecosystem.

Refs: [plandex-ai/plandex](https://github.com/plandex-ai/plandex).

---

## Part 2 — Cross-cutting patterns

**Plan mode.** Cline (Plan/Act), Plandex, Cursor, Claude Code, Copilot App. The convergence: *separate read-and-think from write-and-execute and gate the transition explicitly.* Gates differ — per-step (Cline), per-plan (Cursor), per-task (Copilot). Payoff: humans intervene where it's cheap (before edits) rather than expensive (after).

**Context providers.** Continue's `@`-mentions and Cody's structural retrieval are two angles on the same idea: context is *named* and *requested*, not implicitly slurped. Explicit beats implicit for high-stakes work; opposite for vibe-coding.

**Rules files.** Cursor's `.cursor/rules/`, Aider's `.aider.conf.yml`, Continue's `.continue/rules/`, Cline's CLAUDE-style rules, AGENTS.md as the cross-tool convergence. AGENTS.md (donated to AAIF December 2025) is used by 60k+ open-source projects — the closest thing to a standard. Lesson: write only what the agent cannot infer; keep it grep-able; treat it as machine-readable infrastructure.

**Checkpoint / undo.** Cline's shadow git, Cursor's edit history, Plandex's diff sandbox — three answers to "the agent ran for an hour, I want to partially revert." Shadow-git is most general; diff-sandbox most conservative; edit-history most UI-friendly. Truth: *autonomy without rollback is a trust contract nobody honors past the first bad run.*

**Voice.** Aider's `/voice`. Niche but real for hands-free dictation, accessibility. Where it does not matter: anywhere typing is feasible.

**Git-commit-per-edit.** Aider's signature. The audit trail is the value; no parallel state-tracking needed. Tradeoff: Aider's history is noisy; Cline's is clean but requires checkpoint plumbing.

**MCP as tool surface.** Cline, Continue, Goose, Codex, Cursor all consume MCP. Anthropic's donation to AAIF formalized it as cross-tool standard. Effect: write an MCP server once, use it from any harness. Cleanest interoperability story the ecosystem has produced.

**Self-correction loop.** Devin's self-reviewing PRs, Copilot's review→fix, Plandex's auto-debug, Cline's iterative re-prompt on tool failure. Common shape: *agent runs, agent re-reads output as critic, agent fixes own-goals before human sees it.* The cheap inner loop before the expensive outer loop.

---

## Part 3 — Workflow patterns from the broader community

**TDD with AI.** Test first, agent implements until tests pass, iterate. Works because the test is a precise spec; fails when the test is what needed thinking — the agent will pass a wrong test as confidently as a right one. Concentrated in teams that already practiced TDD; has not converted skeptics.

**Explore → Plan → Code.** Anthropic's canonical Claude-Code best-practice (Explore → Plan → Implement → Commit) and Cline's Plan/Act are the same arc. Now consensus. Teams diverge on *gate explicitness*: Anthropic's is manual ("draft a plan, annotate, send back"), Cline's is modal, the 12-step workflow's is artifact-bearing (each phase writes a file before the next).

**Spec-driven development.** Kiro's three phases — Requirements (EARS notation) → Design (architecture, schemas, sequence diagrams) → Tasks (tracked). May 2026 added Neurosymbolic analysis surfacing requirement conflicts before code. Bet: *most AI failures are spec failures.* Works for greenfield with clear user stories; fails on refactors and edge-case debugging.

**Vibe-coding debate.** Crystallized in 2026. Critics (Salesforce Ben, InfoWorld, multiple consultancies) cite ~3× faster technical-debt accumulation; analysts project $1.5T in AI-generated-code debt by 2027. Defense: throwaway prototypes and exploration are legitimate contexts; the failure is *vibe-coding production systems*. Emerging synthesis: vibe-mode when output is disposable, explore-plan-code-commit otherwise.

**AI for git operations.** Commit messages (everywhere), PR descriptions (Copilot, CodeRabbit), conflict/CI resolution (Copilot App's Agent Merge). High adoption because the cost of a bad commit message is low. Surprise: PR descriptions are consistently better AI-drafted from the diff than human-written under time pressure — not because AI is better at prose, but because humans skip the work of summarizing diffs honestly.

**AI for code review.** CodeRabbit leads: PR summaries with architecture diagrams, line-by-line analysis, 1-click fixes, generated tests, docstrings. Feb 2026 Issue Planner expands "review after written" → "plan before written"; March 2026 multi-repo catches downstream breakage. Copilot's review is competitive on coverage, weaker on actionable suggestions. Pattern: *AI review is best at consistency (every PR reviewed, every file read), worst at judgment (is this design right).* The critic-panel is built precisely on the judgment gap CodeRabbit cannot close.

---

## Part 4 — Recent 2026 developments worth knowing

- **MCP, Goose, and AGENTS.md donations to AAIF (Dec 2025).** Cross-vendor home at the Linux Foundation for agent infrastructure standards.
- **Cursor 3 (April 2).** Agents Window, Design Mode, best-of-N comparison, cloud↔local handoff.
- **Roo Code shutdown (May 15).** Cautionary tale about VC-backed forks of open-source forks.
- **Devin 2.2 (early 2026).** Self-reviewing PRs, 3× faster startup. Cognition raise at $25B valuation in talks (April).
- **Windsurf acquired by Cognition.** SWE-1.5 and Codemaps shipped under combined org.
- **Codex CLI (May).** Persisted goals, MultiAgentV2, plugin marketplace, hooks, in-app browser.
- **GitHub Copilot App (May preview).** Interactive/Plan/Autopilot modes; Agent Merge for autonomous conflict and CI-failure resolution.
- **CodeRabbit.** Issue Planner (Feb), multi-repo analysis (March).
- **Kiro Neurosymbolic spec analysis (May).** LLM + automated reasoning to surface requirement conflicts pre-code.

---

## Synthesis — Top 15 ideas to import into a Claude-Code-based 12-step workflow stack

Ranked by leverage on the orchestrator described in this repo's [CLAUDE.md](../../CLAUDE.md), highest first. Each is named with the source tool.

1. **Glob-scoped instruction files** *(Cursor — `.cursor/rules/*.md`)*. Partition CLAUDE.md into `.claude/rules/<scope>.md` activating on artifact-path globs; preserves the ~200-line attention budget per scope.
2. **Plan-branches** *(Plandex)*. Make step 9 (generator) emit two candidates from two frames in parallel when step 8 produced more than one viable challenge; let the critic-panel evaluate both before picking one.
3. **Cheap self-review before expensive panel** *(Devin 2.2)*. Insert a single-model self-critique pass between step 9 and step 10 that catches own-goals before paying for three or six panel lenses.
4. **Shadow-repo checkpoints per step** *(Cline)*. Snapshot the session directory after each numbered step into a sidecar git repo so a step-N rerun does not require deleting the whole session.
5. **Architect/editor role split for the generator** *(Aider)*. Run step 9 as a strong reasoning model producing the candidate skeleton and a cheap precise model filling in concrete citations and prose.
6. **Context providers as named, replayable primitives** *(Continue)*. Reify the canon-librarian, outside-view, and Explore returns as named provider outputs that later steps can re-cite without re-running the agent.
7. **Code-graph-aware canon retrieval** *(Sourcegraph Cody)*. Move the canon-librarian from text-similarity to citation-graph reasoning: "give me every entry that contradicts this passage" needs structural signal.
8. **AGENTS.md compliance** *(AGENTS.md standard, now at AAIF)*. Adopt AGENTS.md as the cross-tool entry point so the critic stack is reachable from any harness — Cursor, Cline, Codex, Goose — not just Claude Code.
9. **Subagents-as-MCP-servers** *(Goose)*. Expose `canon-librarian`, `outside-view`, `frame-challenger`, the three critic lenses, and `critic-comparator` as MCP servers so other harnesses can borrow the stack piecewise.
10. **Persisted goal with explicit resume semantics** *(Codex `/goal`)*. A `/resume <session-id>` operator command that re-hydrates orchestrator state from the session directory's decision-log and ledger.
11. **Codemap-style structural synthesis artifact** *(Windsurf)*. Add a structural diagram alongside step 12's prose synthesis so the human reviewer gets a navigable blast-radius view before reading the recommendation.
12. **Issue → PR as the unit of work** *(GitHub Copilot)*. An exit hatch that opens the step-12 synthesis as a draft PR against a `synthesis/` branch, making each decision naturally diffable and commentable.
13. **Named-mode session profiles** *(Roo Code, RIP)*. Operator-level `--profile=migration-decision` vs `--profile=new-feature` at step 1 that pre-loads which subagents are mandatory vs optional.
14. **Diff sandbox for orchestrator writes** *(Plandex)*. Stage all step-N artifact writes in a sandbox and let the operator review the cumulative diff before any of it lands in `session-artifacts/`.
15. **Daemon-mode orchestration with multiple clients** *(OpenCode)*. Run the orchestrator as a daemon so a long session survives terminal restarts and can be queried from a phone client for status without disturbing the run loop.

The top of the list (1-5) are *primitive* additions — they change how steps execute. The middle (6-9) are *surface* additions — they change how the work is exposed to other tools. The bottom (10-15) are *operational* additions — they change how a human runs a session. A pragmatic adoption order is top-down: primitives first, surface second, ops third.

---

## Production-vs-demo annotation

- **Heavy production use:** Aider, Cursor, Cline, Codex CLI, GitHub Copilot, Sourcegraph Cody, Windsurf, CodeRabbit.
- **Narrower production use:** Continue, Goose, OpenCode, Plandex, Tabnine.
- **Commercial with delivery-vs-marketing gap:** Devin.
- **Sunset May 2026:** Roo Code.
- **Emerging standards (not products):** AGENTS.md, MCP, both at AAIF.

The 12-step critic stack sits in a different category. Most of the ecosystem optimizes for *velocity of correct-looking output*; the stack optimizes for *adversarial review of design decisions before code is written.* The ideas above are imported where velocity tools have solved a problem the critic stack also has — checkpointing, resume, structural retrieval, role-splits — without trading away the adversarial posture.
