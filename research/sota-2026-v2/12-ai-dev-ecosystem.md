# The AI-Assisted Development Tool Ecosystem — 2026 Survey

*Scope: every major AI coding tool in production use as of May 2026. Each entry covers what the tool does well, the idea most worth borrowing for any practitioner, and where the tool falls short. Cross-cutting patterns and community workflows follow the tool-by-tool section. Date-stamped because the field churns fast — by Q4 2026 half of these vendor claims will be obsolete or repositioned.*

---

## How to read this survey

The ecosystem has stratified into four bands by May 2026:

1. **Heavy production use** — Aider, Cursor, Cline, Codex CLI, GitHub Copilot, Sourcegraph Cody, Windsurf, CodeRabbit. These are deployed at scale, have observable usage telemetry from public benchmarks or vendor disclosures, and have survived at least one bad-press cycle.
2. **Narrower production use** — Continue, Goose, OpenCode, Plandex, Tabnine. Real users, real workloads, but skewed toward specific niches (regulated industries, terminal-first workflows, OSS-first orgs).
3. **Commercial with marketing-vs-delivery gap** — Devin. The product ships, the autonomy claims do not match independent measurements, and the $25B valuation talks are best read as a bet on the Windsurf install base rather than on Devin completion rates.
4. **Sunset** — Roo Code (shutdown May 15, 2026). The lessons it leaves behind are more durable than its install base.

Underneath all four bands sit two **emerging standards** that are not products themselves: **AGENTS.md** (now stewarded by AAIF) and **MCP** (also at AAIF). Treat them as the substrate, not as competitors to anything on the list.

---

## Tool-by-tool

### 1. Aider — terminal pair programmer, commit-per-prompt

Repo: `Aider-AI/aider`. Roughly 41.6k stars as of April 2026, steady commit cadence, top-tier representation on its own polyglot leaderboard with GPT-5 (high) at 88.0% on the 225-exercise benchmark.

**Two things it does well.** First, **architect/editor mode**: a strong reasoning model plans the change, a cheap precise model emits the diff in Aider's structured format. This two-pass split measurably reduces multi-file refactor errors versus single-model high-cost runs. Second, **git-commit-per-prompt** — every accepted change produces a commit, attributed and reversible. The audit trail is the value; "undo" is `git reset`.

**Idea worth borrowing for any practitioner.** Treat each AI edit as a commit-sized unit of work, named in the commit message by the prompt that produced it. Even if you do not adopt Aider, adopting the cadence (one prompt → one commit → one reviewable diff) makes review tractable and makes blame-with-AI an honest artifact rather than a quarterly retrospective. The polyglot leaderboard is itself worth bookmarking — it is one of the few benchmarks driven by working programmers rather than vendors.

**Watch-mode AI! comments** (`// AI! fix this`) let you stay in your editor and trigger Aider from a comment marker — niche but real for people who hate context-switching to a TUI. `/voice` exists for hands-free use; small audience, but accessible.

**Where it falls short.** No IDE chrome — if your team is anchored to VS Code or JetBrains UI affordances, Aider feels primitive. Conflict resolution on long-running branches is manual. The `.aider.conf.yml` is undermarketed and most users never touch it.

### 2. Cursor — IDE fork, agents-first as of Cursor 3

Cursor 3 shipped April 2, 2026. Biggest architectural shift since launch: an **Agents Window** as a standalone workspace running many agents in parallel — across local, git worktrees, remote SSH, and cloud. **Design Mode** lets you annotate UI elements directly in the browser to direct agent edits. **Best-of-N model comparison** is now native. Cloud↔local handoff means an agent started in the cloud can be pulled local without losing state. Composer 2 is Cursor's in-house code-editing model.

**Two things it does well.** First, **parallel agent ergonomics**: the Agents Window finally treats agents as first-class workspace citizens rather than chat windows. A `/worktree` command creates an isolated git worktree per agent so they do not stomp on each other — the same isolation pattern Plandex pioneered, now in an IDE. Second, **rules in `.cursor/rules/*.mdc`** — versioned, scoped, glob-matched rule files. The legacy `.cursorrules` single-file format is silently ignored in Agent mode (a footgun if you upgraded from Cursor 1.x without re-reading the docs).

**Idea worth borrowing.** **Parallel-agents-in-worktrees as the default unit of work** — once you treat agent invocations as concurrent rather than sequential, the natural shape of your work changes: every task is a worktree, every worktree gets an agent, the human role becomes triage and merge. This pattern is now visible in Cursor, GitHub Copilot App, Devin, and Roomote. It is the most consequential UI shift of 2026.

**Where it falls short.** Pricing has drifted upward and is opaque under usage-based billing. The IDE is a Code fork, so VS Code extension parity drifts every few months. Heavy parallel agent use rapidly burns through subscription credit; cost-per-feature math is hard to track.

### 3. Continue — open IDE plugin, configuration-as-code

`continuedev/continue`. VS Code and JetBrains plugin. The defining trait is **configurability via `config.yaml`** at repo or user scope.

**Two things it does well.** First, **`@`-mention context providers** — context is named and explicitly requested (`@codebase`, `@docs`, `@terminal`, custom providers). This makes context a deliberate choice rather than an implicit slurp, which is exactly the discipline most AI-assisted workflows lack. Second, **slash commands as named prompt templates with per-task model routing** — your "review this PR" slash command can route to a stronger model than your inline completions, configured in one file.

**Idea worth borrowing.** **Named, requestable context providers**. Even if you build your own tooling, copy the `@source` pattern: context should be a noun the user invokes, not a hidden default the model receives. It pairs cleanly with rules files and makes prompt logs grep-able by the names of the context sources used.

**Where it falls short.** Continue's UX has always lagged Cursor and Cline. The hub/marketplace for shared configs is underused. Telemetry to compare "did this slash command actually help" is absent — you trust the configuration but cannot measure its effect.

### 4. Cline — VS Code sidebar (and now many more surfaces)

`cline/cline`, formerly Claude Dev. Roughly 61k stars, 5M+ installs, currently at v3.81. Originally a VS Code sidebar; in 2026 also shipping on JetBrains, Cursor (yes, as an extension inside the fork), Windsurf, Zed, Neovim, and a CLI preview for macOS and Linux. Cline absorbed the Roo Code user base after Roo's April 21 sunset announcement.

**Two things it does well.** First, **Plan/Act mode** — Plan reads and proposes; Act executes with per-step approval. The split is the entire point: it makes "read-and-think" cheap and "write-and-execute" deliberate. Second, **shadow-git checkpoints** — Cline maintains a parallel git repo separate from yours and snapshots after each tool use. Three restore modes: files only, task only, or both. Crucially, checkpoints capture untracked files too — the difference between "I lost a file" and "I lost nothing."

**Idea worth borrowing.** **Checkpointing in a shadow git repo is strictly better than relying on the user's working tree**. Your users will not `git stash` before they prompt; the agent must. Anyone building agent tooling should adopt this — it is cheap, durable, and resolves an entire category of "the agent ate my changes" support tickets.

**Where it falls short.** Per-step approval is correct but exhausting; the temptation to approve-all is real and undermines the model. MCP marketplace install UX is better than alternatives but still requires vetting servers individually. Token spend in Act mode on large tasks can be punishing.

### 5. Roo Code — sunset May 15, 2026 — lessons that outlive the product

`RooCodeInc/Roo-Code`. Co-founder Matt Rubens announced shutdown on April 21, 2026; all products (extension, Cloud, Router) end May 15. By shutdown the extension had crossed 3M VS Code Marketplace installs and ~23.9k GitHub stars. The team pivoted to Roomote, a cloud-only agent. Rubens' framing: *"not because Roo Code failed, but because the world it served would cease to exist."*

**Two things it did well that are worth preserving.** First, **named modes as personas with locked toolsets** — Architect, Code, Ask, Debug, etc., each a mode with a specific allowed tool set and prompt. This is a more disciplined version of Cline's Plan/Act and predates it; it forces you to name the role the agent is playing. Second, **diff-based editing** that the team measured at roughly 30% token savings versus full-file rewrites — a reminder that the format the model writes in is itself a cost lever.

**Idea worth borrowing.** **Modes-as-personas with toolset locks**. Most tools converge on a binary plan/act split; Roo's three-to-six-mode surface was richer and made the agent's current role legible. Even if you only adopt "Architect" and "Code" as two modes with distinct system prompts and tool whitelists, you get most of the value.

**Where it fell short.** The pivot rationale ("IDE era is over") is contested — Cursor 3 and Copilot App both bet against it. Roo's cloud product was not differentiated enough to survive on its own merits.

### 6. Codex CLI — OpenAI's terminal agent, mature as of May 2026

`openai/codex`. May 2026 broad release. The headline additions:

- **Persisted `/goal` workflows** — give Codex a high-level objective, walk away, come back later to a paused or completed run. State survives session close. TUI controls for create, pause, resume, clear.
- **MultiAgentV2** — explicit thread caps, wait-time controls, root/subagent hints, v2-specific depth handling. The orchestration story is now configurable rather than implicit.
- **Plugin marketplace** with remote bundle caching, remote uninstall, plugin-bundled hooks, hook enablement state.
- **External-agent session import** — bring sessions from other agents into Codex.
- **In-app browser**, expanded permission profiles, refreshed app-server APIs.

**Two things it does well.** First, **persisted long-horizon goals** as a first-class TUI primitive — Codex is one of the first CLI agents to admit that real work spans more than a single conversation. Second, **AGENTS.md as the native context file** — Codex did more than anyone to popularize the convention before donating it to AAIF.

**Idea worth borrowing.** **Goals as resumable state, not chat threads**. Most agents conflate "the conversation" with "the work." Decoupling them — making the goal a long-lived object with conversation threads attached — is a better model and matches how humans actually work.

**Where it falls short.** Long-running goals create state-management problems most users are not prepared for ("which goal was I on?"). The plugin marketplace, like most plugin marketplaces, will need a vetting story before enterprise adoption. Permission profiles are powerful but undocumented relative to their surface area.

### 7. Goose — block-built, now AAIF, multi-surface, all MCP

Now hosted at `aaif-goose/goose` after Block donated it to AAIF in December 2025 alongside MCP and AGENTS.md. ~44k stars before move (29k+ post-move on the new org per public reporting). 70+ documented MCP extensions; 15+ LLM providers; desktop, CLI, and embeddable surfaces.

**Two things it does well.** First, **MCP as the *only* tool surface** — Goose does not have first-class tools. Every capability is an MCP extension. This forced discipline produced an interoperable extension ecosystem that other tools' bespoke tool surfaces did not. Second, **multi-surface deployment** — the same agent runs as a desktop app, a CLI, or embedded in another product. Decoupling the engine from the surface is the right architectural call.

**Idea worth borrowing.** **MCP-only as a discipline**. If you are building agent tooling, resist the temptation to add a "just this one" built-in tool. Make everything an MCP server even if your codebase is the only consumer. The day you want to swap surfaces, federate with another agent, or hand a capability to a customer, you will be glad.

**Where it falls short.** The desktop UX is undermarketed and unfamiliar to developers anchored on IDE chrome. Discoverability of the 70+ extensions is poor; there is no first-rate marketplace surface as of May 2026. The AAIF move is the right governance call but slows shipping while project structure settles.

### 8. OpenCode — terminal-native Go TUI with a daemon split

`sst/opencode`. ~95k stars (claimed; verify against repo). Go-built TUI on Bubble Tea. Supports 75+ LLM providers. Architecturally distinct: **client/server split** — a persistent background daemon, with the TUI as one possible client. Sessions survive terminal disconnects, SSH drops, machine sleep. Future remote clients (mobile) are implied by the architecture.

**Two things it does well.** First, **LSP as the context source** — OpenCode integrates 40+ Language Server Protocol servers, surfacing diagnostics, hover, symbol lookups, go-to-definition, find-references, call hierarchy to the agent. This is the most under-appreciated context idea in the ecosystem: the LSP already knows your code structure; an agent should read from it rather than re-derive structure from raw text. Second, the **daemon split** — the agent is not coupled to the terminal session that started it.

**Idea worth borrowing.** **LSP-as-context-provider**. Every IDE has been investing in language servers for a decade. AI agents that ignore that investment and re-derive structure from regex or tree-sitter are leaving information on the floor. Even outside OpenCode, you can run a headless LSP and surface results to your own agent.

**Where it falls short.** Smaller community than Cline or Codex CLI. The Go TUI is fast but discoverability of commands lags chat-style interfaces. Daemon lifecycle management (restart on upgrade, log location, port conflicts) is a class of problems most users have not encountered before.

### 9. Devin (Cognition) — best read as marketing-vs-delivery in tension

Cognition raised $400M at $10.2B in mid-2025, acquired Windsurf in July 2025, and as of April 23, 2026 is reportedly in talks at $25B per Bloomberg. Devin 2.2 shipped February 24, 2026: desktop computer-use, **Devin Review** (self-reviewing PR system claimed to catch 30% more issues before human review), boot time from ~45s to ~15s, Linear integration.

**Two things it does well.** First, **the self-review loop** is a real architectural pattern even if Devin's autonomy claims overshoot — generate, then run a separate model pass that critiques the generation, then auto-fix. Second, **post-Windsurf, Cognition has the broadest install base in agentic coding** (Windsurf's user base is the actual asset that drove the $25B talks; Devin alone would not have got there).

**Idea worth borrowing.** **Self-critique passes as a routine step** — even a single extra model call that asks "what did I miss" before submitting a PR catches a meaningful share of obvious errors. This is the same pattern as multi-lens critic panels in adversarial-review stacks, applied to one's own output.

**Where it falls short.** Independent measurements continue to put Devin's complex-task completion in the single-digit to low-double-digit percent range, well below marketing claims. "Autonomous engineer" framing sets expectations the product cannot meet on real-world tickets. Pricing-to-value is hard to defend on tasks where a human-in-the-loop tool (Cursor, Cline) gets there faster with less cost.

### 10. GitHub Copilot Workspace / Copilot Agent / Copilot App

GitHub shipped autonomous multi-step background agents in March 2026: issue assignment → background agent → PR. The **Copilot App** entered technical preview on May 14, 2026 as a standalone desktop experience for Windows, macOS, and Linux.

**Three session modes** in the App: **Interactive** (step-by-step collaboration), **Plan** (agent proposes, you approve), **Autopilot** (fully autonomous). Each session gets its own git worktree, branch, and task state — parallel sessions out of the box. **Agent Merge** watches CI checks, downloads failure logs, resolves merge conflicts, addresses review comments, and pushes fixes until merge conditions are met.

**Two things it does well.** First, **three session modes named honestly** — most tools have these modes in practice but do not give the user a single dial to set the autonomy level. Naming them makes the autonomy contract explicit. Second, **Agent Merge** as the most complete "agent that gets the PR over the line" loop in the ecosystem — CI watching, log fetching, conflict resolution, comment addressing.

**Idea worth borrowing.** **A single autonomy dial with three positions**. Even if your tooling is bespoke, give the user one knob: "ask me everything" / "ask me at milestones" / "tell me when it's done." Burying autonomy controls in deep settings means users default to whatever ships, which is usually wrong for their context.

**Where it falls short.** Tied to the GitHub platform; users on GitLab or Bitbucket cannot adopt the Agent Merge story. Pricing under usage-based billing makes Copilot one of the harder products to estimate cost for at the team level. The App is still preview; bug tail will be long.

### 11. Sourcegraph Cody — the enterprise retrieval play

Pure enterprise as of 2026 — Cody Free and Cody Pro were terminated in July 2025; pricing starts at $59/user/month. Operates over monorepos exceeding 90GB and multi-repo setups crossing 300k repositories. Hybrid dense + sparse retrieval built on Sourcegraph's Code Search API; code-graph aware (definitions, references, types) rather than text-only.

**Two things it does well.** First, **structural retrieval on real codebase scale** — Cody is the only assistant that has demonstrated it works on the kinds of monorepos large enterprises actually run, with retrieval that uses the code graph rather than treating every file as a token blob. Second, **the indexed/fallback mode pattern** — when the index is current, you get semantic + graph search; when it is not, you degrade gracefully to keyword search. Most tools fail-hard on missing context; Cody degrades.

**Idea worth borrowing.** **Code-graph-aware retrieval over text-only retrieval**. If you have language servers, SCIP indexes, or any structured-symbol surface, prefer it over text chunks. The retrieval quality difference compounds on every prompt. Even small teams can build this with `ctags` or LSP `workspace/symbol`.

**Where it falls short.** Pricing pushes Cody out of reach for small teams. Setup and indexing for very large monorepos is a real engineering project, not a "install the extension" exercise. The killing of Free/Pro tiers stranded a small-team user base that has migrated elsewhere.

### 12. Tabnine and Windsurf — the regulated-enterprise and the Cognition-IDE-bet

**Tabnine** — the only major AI dev tool with credible **air-gapped, on-premise** deployment. Kubernetes cluster runs in the customer's private network with no external API calls, no cloud dependencies, no data egress. Supports BYO LLM (commercial, open-source, proprietary). February 2026 launched the Enterprise Context Engine — a continuously evolving model of an organization's software systems, documentation, and engineering practices.

**Two things Tabnine does well.** First, **the air-gap story is real**, not marketing — defense, healthcare, regulated finance can deploy it where they cannot deploy Copilot or Cursor. Second, **BYO LLM** means customers are not locked to a single frontier provider and can run models they have vetted.

**Idea worth borrowing.** **Decouple your AI tooling from any single LLM vendor.** If you cannot swap providers in a config change, you have built lock-in into your workflow that will hurt when pricing shifts or a model gets deprecated. Tabnine's architecture treats the LLM as configuration, not commitment.

**Windsurf** — now owned by Cognition (acquired July 2025). Ships **SWE-1.5** (claimed near-frontier code quality at 13× Sonnet 4.5 speed), **SWE-grep** (Fast Context retrieval claimed 10–20× faster than standard agentic search, >2,800 tokens/sec throughput), **Cascade** (the agent itself), and **Codemaps** (AI-annotated visual maps of code structure with grouped sections and trace guides — a UI no other tool currently matches). Cascade Hooks add SOC 2 audit logging, data sanitization, policy enforcement.

**Idea worth borrowing from Windsurf.** **Visual code maps as a first-class agent surface** — a small but durable UI insight. The orientation problem ("where am I in this repo?") is real for both humans and agents; annotating it visually is a better answer than text search. Worth borrowing even if you build the map by hand for a single critical service.

**Where each falls short.** Tabnine — UX trails Cursor and Copilot by a full generation; small-team pricing is not competitive. Windsurf — model claims need independent verification; Cognition's roadmap collision between Windsurf and Devin is not yet resolved (which IDE is canonical, which agent backbone wins).

### 13. Plandex — terminal agent for very large tasks

`plandex-ai/plandex`. Handles **2M tokens of direct context** (~100k per file) and can index **20M+ token directories** via **tree-sitter project maps** across 30+ languages. **Cumulative diff sandbox** keeps AI-generated changes separate from project files until the human is ready to apply. **Plan branches** let you explore multiple solution paths in parallel — like git branches but for agent plans.

**Two things it does well.** First, **the cumulative diff sandbox** — work piles up reviewably, you apply or reject in bulk, and your working tree stays clean until you decide. Second, **plan branches** — exploring two alternative implementations side-by-side without throwing one away to try the other is how humans think about hard design problems, and Plandex is the only mainstream tool that exposes it.

**Idea worth borrowing.** **Plan branches as a primitive** — most tools force linear "try, undo, try again" workflows. Letting an agent fork its own plan and compare results is closer to how careful engineering actually happens. Even a manual version (two worktrees, two prompts, side-by-side diff) is worth adopting.

**Where it falls short.** Smaller community than Aider or Codex CLI. The TUI is functional but unflashy. Pricing and provider configuration is more setup than most users want for a first run.

---

## Cross-cutting patterns

These show up in three or more tools and have crossed the threshold from novelty to convention.

**Plan mode** — Cline (Plan/Act), Plandex (plan + apply), Cursor (Agents Window with read-then-act), Claude Code (plan tool), Copilot App (Plan session mode), Codex (`/goal`). Pattern: separate read-and-think from write-and-execute, gate the transition explicitly. Convergence is near-total in 2026; treat it as the floor, not the ceiling.

**Context providers** — Continue `@`-mentions, Cody structural retrieval, Cursor `@` syntax, Cline mentions. The discipline is: **context is named and requested, not implicitly slurped**. Even agents that default to whole-repo context now let users override that default by naming sources.

**Rules files** — Cursor `.cursor/rules/*.mdc`, Aider `.aider.conf.yml`, Continue `.continue/rules/`, Cline `.clinerules/`, Claude Code `CLAUDE.md`, Codex `AGENTS.md`. The cross-tool convergence point is **AGENTS.md** (donated to AAIF December 2025). The practical convention is: shared instructions in `AGENTS.md`, tool-specific tweaks in tool-specific files.

**Checkpoint/undo** — Cline shadow git, Cursor edit history, Plandex diff sandbox. Pattern: the user's working tree is sacred; the agent's experiments live elsewhere until accepted. This is the right invariant and every tool will converge to it.

**Voice** — Aider `/voice`. Niche but real for hands-free use and accessibility. Few other tools have meaningful voice surfaces yet.

**Git-commit-per-edit** — Aider's signature, now reflected in Cursor 3's per-agent worktree-and-commit pattern. The audit trail is the value; review-by-diff is how humans review.

**MCP as tool surface** — Cline, Continue, Goose, Codex, Cursor, OpenCode. AAIF formalization in December 2025 made MCP the de facto standard. Tools that have not adopted MCP by mid-2026 are paying a compatibility tax.

**Self-correction loops** — Devin Review (self-reviewing PR), Copilot Agent Merge (review→fix→merge), Plandex auto-debug, Cline iterative re-prompt on tool failure. Pattern: one model call generates, a second critiques, a third applies the critique. This is the same shape as adversarial-review stacks, applied to the agent's own output.

---

## Community workflow patterns

**Test-driven development with AI** — works when the test is a precise specification (input/output, structural invariant, property). Fails when the test was the hard part — if you cannot specify the test, the AI cannot solve the problem; you have moved the difficulty rather than removed it. Adopt TDD-with-AI for well-specified pieces; avoid the cargo cult that says "always write the test first" regardless of whether you can write one.

**Explore → Plan → Code** — Anthropic's Claude Code canonical practice. Variants: Cline Plan/Act, Codex `/goal`, Copilot App Plan mode, Plandex plan branches. The discipline: do not let the agent start writing until it has read enough and proposed a plan you accepted. The frame is consistent across tools because the failure mode of skipping it is consistent: confident generation against an under-explored problem.

**Spec-driven development** — AWS **Kiro** (Requirements → Design → Tasks, with neurosymbolic Requirements Analysis as of May 2026 — an SMT solver that proves contradictions, ambiguities, or gaps in requirements before any code is written). **GitHub Spec-Kit** (~90k stars, `/specify`, `/plan`, `/tasks` commands, packaged as templates + CLI + prompts for Copilot, Claude Code, Gemini CLI). The bet: AI agents are most useful against a precise spec, so invest in the spec rather than in prompt engineering.

**Vibe-coding debate (2026)** — Salesforce Ben's "year of technical debt thanks to vibe-coding" prediction; InfoWorld's "end of vibe coding, already" piece; citations of roughly 3× faster tech-debt accumulation and a widely-quoted $1.5T projected AI-code-debt figure by 2027 (Forrester, plus various analyst reports). Independent studies cite 45% of vibe-coded output containing security vulnerabilities, 48% increase in code duplication, 60% drop in refactoring activity, and maintenance costs reaching 4× traditional levels by year two. **Emerging synthesis:** vibe-mode is fine for throwaway prototypes and exploration; for anything that lives past the week, explore → plan → code → commit with review is the only defensible workflow. The interesting wrinkle is that vendors who marketed "just vibe" in 2024 are quietly rebranding around plan-mode in 2026.

**AI for git operations** — Commit messages (everywhere, table stakes), PR descriptions (Copilot, CodeRabbit, every IDE-native tool), conflict and CI resolution (Copilot Agent Merge is the most complete). The pattern: agents are good at the textual work around code (messages, descriptions, conflict prose) before they are good at the code itself. Adopt early on the textual surface; adopt cautiously on the code surface.

**AI for code review** — **CodeRabbit** leads commercial deployments (PR summaries, line-by-line review, 1-click fixes, generated tests; **Issue Planner** launched February 10, 2026 with Linear/Jira/GitHub Issues/GitLab integration; **Multi-Repo Analysis** March 6, 2026). **Greptile** is the recall leader at ~82% bug catch rate in independent benchmarks but with ~11 false positives per run vs CodeRabbit's ~2 — Greptile sees more but cries wolf more. **Ellipsis**, **GitHub Copilot review**, and Anthropic's `claude-code-security-review` round out the surface. The practical call: Greptile for security-critical code where missed bugs are catastrophic; CodeRabbit for general PR throughput where false-positive fatigue would kill adoption.

---

## Recent 2026 developments worth knowing

- **MCP, Goose, AGENTS.md donations to AAIF** (December 2025). These three together signal that agentic tooling is moving to a foundation-stewarded standards model, the same trajectory as Kubernetes/CNCF. Treat anything that does not interoperate with these three as adding lock-in tax.
- **Cursor 3** (April 2, 2026) — agent-first IDE; the Agents Window pattern will be copied.
- **Roo Code shutdown** (May 15, 2026) — preserves the lesson that "modes as personas with locked toolsets" is worth taking forward into your own workflow even though the product is gone.
- **Devin 2.2 + $25B valuation talks** (February 2026 release, April 2026 funding talks) — Devin Review (self-review pattern) is the durable idea; the autonomy claims are not.
- **Windsurf acquired by Cognition** (consummated July 2025; key product output SWE-1.5, Codemaps, SWE-grep through late 2025 into 2026).
- **Codex CLI broad May 2026 release** — persisted `/goal`, MultiAgentV2, plugin marketplace, external-agent import. Goals-as-resumable-state is the durable idea.
- **GitHub Copilot App** (technical preview May 14, 2026) — three honest autonomy modes, Agent Merge as the most complete close-the-PR loop.
- **CodeRabbit Issue Planner** (February 10, 2026) and **Multi-Repo Analysis** (March 6, 2026).
- **Kiro Neurosymbolic Requirements Analysis** (May 2026) — SMT-solver-backed contradiction detection on requirements; the first mainstream agentic tool that treats requirements as a formal object subject to mathematical proof rather than informal text.
- **GitHub Spec-Kit** (~90k stars by May 2026) — the fastest-rising developer tooling repository of the cycle; signals real demand for spec-driven workflows.

---

## Production-vs-demo annotation

**Heavy production use** (deployed at scale, telemetry observable, survived bad-press cycles): Aider, Cursor, Cline, Codex CLI, GitHub Copilot, Sourcegraph Cody, Windsurf, CodeRabbit.

**Narrower production use** (real users, niche skew): Continue (configurability-first orgs), Goose (OSS-and-MCP-first), OpenCode (terminal-native, multi-provider), Plandex (very-large-task terminal workflows), Tabnine (regulated and air-gapped).

**Commercial with delivery-vs-marketing gap:** Devin. The product ships; autonomy claims overshoot independent measurement. The Cognition bet is the Windsurf install base, not Devin's completion rate.

**Sunset May 2026:** Roo Code.

**Emerging standards (not products):** AGENTS.md, MCP — both at AAIF. Treat as substrate, not competition.

---

## Top 15 ideas to borrow across the ecosystem — ranked by leverage

Each named with the source tool that implements it most clearly. "Leverage" means: change in outcome per unit of adoption effort.

1. **Plan/Act split with explicit gate** — *Cline*. Cheapest, highest-impact workflow change. Most tools converge here; the discipline transfers regardless of tool.
2. **Shadow-git checkpoints capturing untracked files** — *Cline*. Eliminates an entire class of "the agent ate my work" failures.
3. **Architect/editor model pair (strong planner, cheap precise diff emitter)** — *Aider*. Cost and accuracy improvement on multi-file refactors.
4. **Self-critique pass before submission** — *Devin Review*. One extra model call catches a meaningful share of obvious errors at trivial marginal cost.
5. **Named, requestable context providers (`@source` syntax)** — *Continue*. Makes context a deliberate noun rather than an implicit slurp.
6. **Goals as resumable state, not chat threads** — *Codex CLI `/goal`*. Decouples the work from the conversation; matches how humans actually work.
7. **Parallel agents in isolated worktrees as the default unit of work** — *Cursor 3 Agents Window / Copilot App parallel sessions*. The most consequential UI shift of 2026.
8. **Three-position autonomy dial named honestly (Interactive / Plan / Autopilot)** — *Copilot App*. Replaces a dozen hidden settings with one user-facing knob.
9. **Code-graph-aware retrieval over text-only retrieval** — *Sourcegraph Cody*. Retrieval quality compounds on every prompt; structure beats tokens.
10. **LSP as a context source for agents** — *OpenCode*. Free leverage off a decade of language-server investment most agents ignore.
11. **Cumulative diff sandbox with plan branches** — *Plandex*. Exploring two alternative implementations side-by-side without throwing one away.
12. **Modes-as-personas with locked toolsets** — *Roo Code (lesson preserved)*. Makes the agent's current role legible and constrained.
13. **MCP-only as a discipline** — *Goose*. Every capability is an MCP server, even if you are the only consumer; pays off the day you want to federate.
14. **AGENTS.md as the cross-tool shared rules file** — *AAIF (formerly OpenAI Codex)*. Shared instructions in `AGENTS.md`, tool-specific tweaks elsewhere.
15. **Spec-driven development with formal requirements analysis** — *Kiro Neurosymbolic (May 2026) + GitHub Spec-Kit*. The frontier: SMT-solver proof that requirements are consistent before any code is generated. Even without the solver, the Requirements → Design → Tasks staging discipline is a major leverage gain.

---

## What to actually do

If you adopt nothing else from this survey, adopt three things:

1. **A plan/act split with an explicit gate.** Pick any tool that supports it; the workflow discipline matters more than the tool.
2. **Shadow-git checkpoints or per-edit commits.** The agent's experiments should never be able to destroy your working tree.
3. **`AGENTS.md` at the root of your repo, even if you only use one AI tool today.** Free option value for the day you swap tools; trivial cost to write.

If you adopt three more, add:

4. **Named context providers in your prompts.** Even outside Continue, prefer `read this file, this symbol, this directory listing` over `figure out what you need.`
5. **A self-critique pass before any agent-generated PR.** One extra model call.
6. **Parallel agents in worktrees** the first time you have two independent tasks. Not because parallelism is fashionable, but because the isolation is genuinely cheap and the merge is genuinely tractable.

Everything else on the list of fifteen is real leverage but more situational. Start where the floor is, raise it, and reassess in six months. The half-life of specific tool claims in this market is short; the half-life of the underlying workflow ideas is years.

Sources:
- [Cursor 3 changelog](https://cursor.com/changelog/3-0)
- [Cursor 3 launches Agents Window and Design Mode (TestingCatalog)](https://www.testingcatalog.com/cursor-launches-cursor-3-with-agents-window-and-design-mode/)
- [Codex changelog (OpenAI Developers)](https://developers.openai.com/codex/changelog)
- [Codex updates by OpenAI - May 2026 (Releasebot)](https://releasebot.io/updates/openai/codex)
- [OpenAI `/goal` vs Claude Code Agents (DevToolPicks)](https://devtoolpicks.com/blog/codex-goal-command-vs-claude-code-agents-2026)
- [Sunsetting Roo Code (Extension, Cloud, Router)](https://roocode.com/blog/sunsetting-roo-code-extension-cloud-and-router)
- [Roo Code pivots to cloud-based agent (The New Stack)](https://thenewstack.io/roo-code-cloud-ides-ai-coding/)
- [Cognition $25B valuation talks (TechFundingNews)](https://techfundingnews.com/cognition-ai-25b-valuation-funding-talks-devin-software-engineer/)
- [Cognition's acquisition of Windsurf](https://cognition.ai/blog/windsurf)
- [Introducing Devin 2.2 (Cognition)](https://cognition.ai/blog/introducing-devin-2-2)
- [GitHub Copilot App technical preview changelog](https://github.blog/changelog/2026-05-14-github-copilot-app-is-now-available-in-technical-preview/)
- [GitHub Copilot App is now in Technical Preview (DevOps Journal)](https://devopsjournal.io/blog/2026/05/14/github-copilot-app)
- [Greptile benchmarks](https://www.greptile.com/benchmarks)
- [CodeRabbit vs Greptile (Panto AI)](https://www.getpanto.ai/blog/coderabbit-vs-greptile-ai-code-review-tools-compared)
- [Aider Polyglot leaderboard](https://aider.chat/docs/leaderboards/)
- [Aider Guide 2026 (DeployHQ)](https://www.deployhq.com/guides/aider)
- [Cline Plan & Act Mode docs](https://docs.cline.bot/core-workflows/plan-and-act)
- [Cline for VS Code 2026 setup guide (DeployHQ)](https://www.deployhq.com/guides/cline)
- [Linux Foundation announces AAIF (PR Newswire)](https://www.prnewswire.com/news-releases/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation-aaif-anchored-by-new-project-contributions-including-model-context-protocol-mcp-goose-and-agentsmd-302636897.html)
- [Goose moves to AAIF](https://goose-docs.ai/blog/2026/04/07/goose-moves-to-aaif/)
- [Plandex on GitHub](https://github.com/plandex-ai/plandex)
- [Sourcegraph Cody remote repository awareness](https://sourcegraph.com/blog/how-cody-provides-remote-repository-context)
- [Sourcegraph Cody Review 2026 (WeavAI)](https://weavai.app/blog/en/2026/04/30/sourcegraph-cody-review-2026-enterprise-ai-at-59-mo/)
- [Continue config.yaml reference](https://docs.continue.dev/reference)
- [How to Configure Continue](https://docs.continue.dev/customize/deep-dives/configuration)
- [Kiro Specs docs](https://kiro.dev/docs/specs/)
- [AWS Kiro neurosymbolic AI (SiliconANGLE)](https://siliconangle.com/2026/05/12/aws-kiro-accelerates-software-development-proving-code-correctness-gets-work/)
- [GitHub Spec-Kit](https://github.com/github/spec-kit)
- [Spec-driven development with Kiro, Spec-Kit, Tessl (Martin Fowler)](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [2026 Predictions: Year of Technical Debt (Salesforce Ben)](https://www.salesforceben.com/2026-predictions-its-the-year-of-technical-debt-thanks-to-vibe-coding/)
- [Is vibe coding the new gateway to technical debt? (InfoWorld)](https://www.infoworld.com/article/4098925/is-vibe-coding-the-new-gateway-to-technical-debt.html)
- [It's the end of vibe coding, already (InfoWorld)](https://www.infoworld.com/article/4093942/the-end-of-vibe-coding-already.html)
- [Vibe Coding Hangover: $1.5T Debt Warning (byteiota)](https://byteiota.com/vibe-coding-hangover-2/)
- [OpenCode on GitHub](https://github.com/sst/opencode)
- [OpenCode LSP integration (DeepWiki)](https://deepwiki.com/sst/opencode/5.4-language-server-protocol-(lsp))
- [Windsurf changelog](https://windsurf.com/changelog)
- [Cognition: Introducing SWE-1.5](https://cognition.ai/blog/swe-1-5)
- [CodeRabbit Issue Planner docs](https://docs.coderabbit.ai/issues/planner)
- [CodeRabbit Multi-Repo Analysis](https://www.coderabbit.ai/blog/Coderabbit-multi-repo-analysis)
- [Tabnine Enterprise Context Engine launch (GlobeNewswire)](https://www.globenewswire.com/news-release/2026/02/26/3245668/0/en/Tabnine-Launches-Enterprise-Context-Engine-Introducing-the-Missing-Layer-for-Reliable-Enterprise-AI.html)
- [Tabnine air-gapped platform](https://www.tabnine.com/blog/the-only-airgapped-ai-software-development-platform/)
- [AGENTS.md](https://agents.md/)
- [Custom instructions with AGENTS.md (OpenAI Developers)](https://developers.openai.com/codex/guides/agents-md)
- [Anthropic donates MCP, establishes AAIF](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
