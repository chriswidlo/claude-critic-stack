# Project-level AI instruction files — canonical 2026 reference

*SOTA-2026-v2 · chapter 14. Practitioner reference. Stack-neutral. Compiled May 2026 from the Anthropic memory docs (`code.claude.com/docs/en/memory`), the AGENTS.md spec at `agents.md`, GitHub issue `anthropics/claude-code#6235`, `agentsmd/agents.md#135` (the v1.1 proposal), Gloaguen et al. 2026 (ETH Zurich / LogicStar.ai, arXiv:2602.11988), HumanLayer's "Writing a good CLAUDE.md", and `alexop.dev`.*

A project-level AI instruction file is a Markdown document, committed to the repository root, that is loaded into the model's context window at the start of every coding-agent session. It is the highest-leverage configuration surface in an AI coding workflow because it pays a token cost on every turn and shapes every artifact the agent produces. Treat it accordingly.

This chapter explains how the format-wars settled (and didn't), what to put in such a file, what to leave out, how long it should be, how the hierarchy resolves, what the active failure modes are in 2026, and where the canonical examples live.

---

## 1. The format wars — where we landed in mid-2026

The market did not converge on a single file. It converged on a single *shape*: a small Markdown document at the repository root, plus a directory of scoped rule files for everything that doesn't need to load on every turn. The filename and selector syntax vary by vendor.

### Claude Code — `CLAUDE.md` (plus `.claude/rules/`)

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. The open feature request to add native `AGENTS.md` support is GitHub issue `anthropics/claude-code#6235`, with three thousand-plus upvotes as of April 2026 and no commitment from Anthropic. Workarounds: a `CLAUDE.md` that begins with `@AGENTS.md` to import the shared file, or `ln -s AGENTS.md CLAUDE.md` on Unix. (On Windows the symlink requires Administrator or Developer Mode; use the `@` import.)

The Claude Code hierarchy, in load order from broadest scope to most specific:

1. **Managed policy** — `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS, `/etc/claude-code/CLAUDE.md` on Linux/WSL, `C:\Program Files\ClaudeCode\CLAUDE.md` on Windows. Distributed via MDM, Group Policy, or Ansible. Cannot be excluded by user settings.
2. **User instructions** — the user's home-directory `~/.claude/CLAUDE.md`. Personal preferences across all projects.
3. **Project instructions** — repo-root `./CLAUDE.md` or `./.claude/CLAUDE.md`. Committed; team-shared.
4. **Ancestor and subdirectory `CLAUDE.md`** — Claude walks the tree from the working directory up to the filesystem root, loading every `CLAUDE.md` it finds. Files in subdirectories below the working directory load *on demand* when Claude reads a file in that subdirectory.
5. **Local personal** — `./CLAUDE.local.md` at the project root, gitignored. Per-developer overrides like sandbox URLs.

Concatenation order matters: ancestor content appears in context before working-directory content, so the closest-to-CWD instructions are read last and have the strongest recency effect. Within a directory, `CLAUDE.local.md` is appended after `CLAUDE.md`. The `.claude/rules/` directory holds path-scoped files with YAML frontmatter (`paths: ["src/api/**/*.ts"]`); rules without a `paths` field load unconditionally; rules with one trigger when Claude opens a matching file.

### OpenAI Codex / ChatGPT Codex — `AGENTS.md`

Codex originated the convention in August 2025 and reads `AGENTS.md` natively. The hierarchical-scope rule is the same idea as Claude's nested `CLAUDE.md`: the nearest `AGENTS.md` to the file being edited applies; ancestor files contribute too, with the closest taking precedence.

### Cursor — `.cursor/rules/*.mdc` (legacy `.cursorrules` deprecated in Agent mode)

The modern Cursor surface is a directory of `.mdc` files under `.cursor/rules/`. The root-level `.cursorrules` file is still parsed but is **silently ignored in Agent mode** and is officially deprecated; Cursor's own docs recommend migrating. As of Cursor 2.2, `.mdc` files remain functional but new rules are authored as folders under `.cursor/rules/`.

Each `.mdc` file carries YAML frontmatter:

- `description` — required for the "Apply Intelligently" selection mode; the agent uses it to decide whether to load.
- `globs` — file patterns; rule loads when the agent opens a matching file.
- `alwaysApply` — boolean; when true the rule is in context for every turn. Cursor's own guidance: *use sparingly, this is your global config, not your per-feature config.*

### Aider — `.aider.conf.yml` + `CONVENTIONS.md`

Aider keeps tool configuration (`.aider.conf.yml`) separate from the model-facing context file (`CONVENTIONS.md`, referenced from config). The split is intentional: the config tells aider how to run; conventions tell the model how to write.

### Continue.dev — `config.yaml` + `.continue/rules/*.md`

Same pattern as Cursor: a config file for the tool, a rules directory for the model. Rules use Markdown with optional frontmatter.

### Cline — `.clinerules/`

A directory at the repository root. No single root file; every `.md` in the directory is concatenated. Encourages decomposition by topic from day one.

### GitHub Copilot — `.github/copilot-instructions.md` and `.github/instructions/**/*.instructions.md`

Copilot reads a single project-level file at a fixed path plus a directory of path-scoped `.instructions.md` files with frontmatter glob patterns. The `.github/` location reflects Copilot's GitHub-native origin and lets organization templates ship instructions alongside CI configuration.

### `AGENTS.md`-native agents

By May 2026 the following coding agents read `AGENTS.md` natively without a shim: OpenAI Codex, Google Jules, Gemini CLI, Devin, Amp, Warp, Goose, Factory, Windsurf, OpenCode, Cursor (via its compatibility shim), Aider, Zed, JetBrains Junie, UiPath, VS Code (Copilot Workspace), and several others. The `agents.md` site claims **20+ compatible agents and 60,000+ open-source repositories** carrying the file.

---

## 2. Two universal observations

Two patterns hold across every tool listed above. They are the only safe generalizations.

**Observation 1 — every modern tool migrated from a flat dotfile to a directory of scoped rules.** Cursor `.cursorrules` → `.cursor/rules/*.mdc`. Claude `CLAUDE.md` → `CLAUDE.md` + `.claude/rules/`. Continue `config.yaml` → `.continue/rules/`. Copilot single-file → `.github/instructions/`. The driver is token economics: a flat file pays its full token cost on every turn whether or not its content is relevant; a directory with selectors (frontmatter globs, descriptions, tags) pays only when a rule matches. As context windows grew from 200k to 1M tokens the *adherence cost* of unconditional loading became more punishing than the original capacity constraint — more tokens means more competing instructions for the model to attend to, not just more room.

**Observation 2 — AGENTS.md won the cross-tool race but did not displace the vendor file.** It is the de facto interchange format: 60,000+ repos, 20+ agents reading it natively, governance moved to a Linux Foundation body (the Agentic AI Foundation, December 2025 — founding members Anthropic, OpenAI, Block; Microsoft and Google joined shortly after). But Claude Code, the agent with the largest installed base, still does not read it. The practical state of play is: write `AGENTS.md`, then either (a) `ln -s AGENTS.md CLAUDE.md`, or (b) write a thin `CLAUDE.md` that starts with `@AGENTS.md` and appends Claude-specific addenda below. Anthropic's own `/init` flow now reads `AGENTS.md`, `.cursorrules`, and `.windsurfrules` when generating an initial `CLAUDE.md`, which is the closest the company has come to acknowledging the standard.

---

## 3. The convergence story (timeline)

- **August 2025** — OpenAI Codex ships `AGENTS.md` as the project context convention.
- **Autumn 2025** — Amp, Jules (Google), Cursor, Factory, goose, Zed, and Warp adopt it; Aider follows.
- **December 2025** — Governance contributed to the **Agentic AI Foundation under the Linux Foundation**. Founding members: Anthropic, OpenAI, Block. Microsoft and Google join shortly after.
- **8 January 2026** — `agentsmd/agents.md` issue **#135** filed: *AGENTS.md v1.1 — Making Implicit Semantics Explicit, Clarifying Scope, and Recommendation for Progressive Disclosure*. Changes are backwards-compatible:
  - **Hierarchical scope** — formalized: an `AGENTS.md` applies to files in its containing folder and subdirectories; scope is strictly ancestor-based.
  - **Precedence ladder** — LLM system prompt > agent system prompt > user prompt > local `AGENTS.md` > ancestor `AGENTS.md` (nearest first) > other documentation. "More specific instructions take precedence over more general ones."
  - **Optional YAML frontmatter** — two fields: `description` (recommended under 200 chars) and `tags` (keywords). Unknown fields ignored for forward compatibility.
  - **Progressive disclosure** — implementers should index files at session start, inject a lightweight index, and load full bodies on demand. This brings `AGENTS.md` semantically in line with the `.claude/rules/` and `.cursor/rules/` patterns.
- **February–March 2026** — Gloaguen et al. publish the first large-scale empirical evaluation (see §9 below); InfoQ runs *"New Research Reassesses the Value of AGENTS.md Files"*.
- **April 2026** — Claude Code issue #6235 crosses 3k upvotes with no commitment from Anthropic; the Claude Code `/init` flow gains an interactive multi-phase mode (`CLAUDE_CODE_NEW_INIT=1`) that reads existing `AGENTS.md`/`.cursorrules`/`.windsurfrules` and folds them into the generated `CLAUDE.md`.

---

## 4. What goes in a project-instruction file

Anthropic's recommended sieve is one question, applied per line:

> *"If I removed this, would Claude make a mistake?"*

If the answer is no, delete the line. The official Anthropic guidance on `code.claude.com/docs/en/memory` formalizes this as: add to `CLAUDE.md` when (a) Claude makes the same mistake a second time, (b) a code review catches something Claude should have known, (c) you type the same correction into chat two sessions running, or (d) a new teammate would need the same context to be productive.

The categories that survive that sieve:

1. **Tech stack basics with versions.** "Python 3.12 + uv. Postgres 16. Pinned via `uv.lock`." Three lines, decides a dozen downstream calls.
2. **Non-obvious commands.** `make lint`, `pytest -x --ff`, `pnpm dev:e2e`. Anything the agent would otherwise guess or invent.
3. **Architecture *map*, not architecture *description*.** "`src/api/handlers/` — HTTP layer; `src/domain/` — pure business logic, no IO; `src/adapters/` — external IO." A reader-orientation tool, not a textbook chapter. The map points; the agent reads.
4. **Hard rules and invariants.** "Never call the payments API directly; always go through `PaymentGateway`." "All migrations are forward-only." "No `git push --force` to `main`." These are the load-bearing lines.
5. **Workflow rules.** "Run `make lint` before committing." "Add a changelog entry for any user-facing change." "Tests live next to the file they test, suffixed `_test.py`."
6. **Domain terminology.** Three sentences defining the words that mean something specific in this codebase. "A *Cohort* is a billing-period group, not a marketing segment."

That is the entire taxonomy. Five-to-six categories. Most projects can cover all of them in eighty lines.

---

## 5. What does **not** belong

By construction, the file is paid for on every turn. Anything that can be enforced or taught more cheaply elsewhere is waste:

- **Anything the linter can enforce.** Don't tell the model "use 2-space indentation" if `eslint`/`ruff`/`prettier` will rewrite it. HumanLayer's formulation: *"Never send an LLM to do a linter's job, as LLMs are comparably expensive and incredibly slow compared to traditional linters and formatters."* Linters are deterministic and free per run; the model is probabilistic and costly per turn.
- **Anything the code can teach.** Don't paraphrase function signatures the agent can read by opening the file. Point to `file:line` instead.
- **Anything `git log` can teach.** Don't recapitulate decisions documented in commit messages or ADRs. Link to the ADR directory.
- **README recapitulation.** README is for humans browsing the repo; `CLAUDE.md` is for the model. Duplication doubles the maintenance cost and the drift surface.
- **Every dependency.** A list of npm packages is what `package.json` is for.
- **Task-specific instructions.** "How to add a new endpoint" is a *skill* (or a `.claude/rules/` entry, or a `/command`), not part of the always-loaded context.

---

## 6. The hard ceiling

The numbers worth carrying in your head:

- **Frontier LLMs reliably attend to roughly 150–200 instructions per session** across system prompt, project file, user prompt, and accumulated turn history combined. Smaller models attend to fewer. Past that ceiling, adherence collapses non-linearly — the model doesn't fail gracefully, it stops noticing rules silently.
- **Claude Code's own system prompt consumes ~50 of those.** That leaves roughly 100–150 instruction slots for everything else: your `CLAUDE.md`, user-level `CLAUDE.md`, ancestor files, rules, skills loaded into context, MCP tool descriptions, and the user's prompt.
- **`CLAUDE.md` is paid on every turn before the user types.** A 5,000-token `CLAUDE.md` is a 5,000-token tax on every response — multiplied by every turn in the session, every session in the day, every developer on the team.
- **Anthropic's own guidance:** *"target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."*

The ceiling is the single hardest constraint in this whole design space. Every other rule in this chapter is downstream of it.

---

## 7. Structural patterns

**Length.** The 2026 community target is **80–120 lines of high-signal body** for the project-root file, with a hard cap at 200. Reference points: HumanLayer's own root `CLAUDE.md` is under 60 lines; the widely-forked Karpathy-derived `CLAUDE.md` (Forrest Chang's distillation of Karpathy's January 2026 X post on LLM coding failure modes) is 65 lines and ranked #1 on the Weekly Coding AI Leaderboard at 71,000+ GitHub stars. HumanLayer's stance: *"general consensus is that less than 300 lines is best, and shorter is even better."*

**Headings.** Short, imperative, scannable. `## Build`, `## Test`, `## Invariants`, `## Layout`. Section headings are themselves part of the instruction surface — a clear heading helps the model route attention. Avoid clever heading prose; you are writing a reference card, not an essay.

**Layering.** Managed → user → project → subdir → personal. Subdir files load on demand when the agent reads a file in that subdirectory, which is the workhorse of progressive disclosure inside the Claude ecosystem. In monorepos this is the *only* way to keep instruction count below the ceiling — put cross-cutting rules at the repo root, put team-specific rules in `<team>/CLAUDE.md`, and let the file system trigger the right load.

**`@`-imports vs `Read` (eager vs lazy).** Claude Code's `@path/to/file` syntax inlines an imported file into context *at launch*, alongside the file that referenced it. Imports recurse up to a **maximum of five hops**; external imports (paths outside the project) trigger a one-time approval dialog the first time the project is opened; imports referencing paths that contain spaces fail silently — a known sharp edge. Use `@` only for files small enough to justify being in every turn. For anything larger, write a pointer in prose ("the migration playbook is in `docs/migrations.md`") and trust the agent to `Read` it on demand. **Eager loading is a tax; lazy loading is a hint.**

**Comments.** Block-level HTML comments (`<!-- ... -->`) in `CLAUDE.md` are stripped before injection into Claude's context. Use them to leave notes for human maintainers without paying tokens — the canonical use is to mark the last time a section was reviewed.

---

## 8. Updating cadence

`CLAUDE.md` is a **living document.** Anthropic recommends adding to it the moment Claude makes the same mistake twice. That cadence works for additions; deletions are harder because nobody notices that a rule has gone stale. Two practices help:

- **Periodic checkpoint with a 90-day diff.** Quarterly, open `git log --since="3 months ago" CLAUDE.md` and ask whether each addition is still load-bearing. If you can't remember why a line was added, delete it.
- **Lint the file mechanically.** Tools like `cclint` check for the common defects (missing required sections, broken `@`-imports, excessive line count, duplicated rules across files in the hierarchy). Run in CI on changes to any `CLAUDE.md` / `AGENTS.md` / `.claude/rules/**` path.

---

## 9. The drift failure mode

**Stale `CLAUDE.md` is worse than no `CLAUDE.md`.** A missing file produces an agent that explores; a wrong file produces an agent that confidently writes against a model of the codebase that no longer exists. The agent's confidence is bounded by the specificity of the file, not by its accuracy — so the *more concrete* an outdated instruction, the *more damage* it does.

The empirical evidence as of 2026 is striking. **Gloaguen et al. 2026** (ETH Zurich and LogicStar.ai, arXiv:2602.11988, "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?") evaluated 138 real-world repositories with autonomous coding agents and found:

- **LLM-generated context files universally degraded task success.** Average resolution rate dropped by 0.5% on SWE-bench Lite and 2% on AGENTBENCH when an LLM-generated `AGENTS.md` was added — and inference cost rose by **over 20% per instance** (GPT-5.2), with trajectories lengthened by ~3.92 steps on average.
- **Developer-written context files gave only +4%** task success, *and only when they were minimal and precise.* Verbose hand-written files showed no benefit and sometimes a loss.
- **The mechanism of harm:** when context files name specific tools, the agent's invocation of those tools jumps from ~0 to 2.5× per instance. That obedience manifests as **counterproductive exploration** — more searches, more reads, more redundant test runs — not better targeting. The agent does what the file says even when the file says the wrong thing.

The defensive posture this implies:

- **Abstract over specifics where possible.** "Database access goes through `src/db/`" survives a refactor; "always use `DbClient.query_one_or_none`" does not. Top-level directory purposes are stable on a 6–12 month horizon; specific function names are not.
- **Pointer to ADRs, not recap of ADRs.** "Architectural decisions are in `docs/adr/`" gives the agent a stable map; restating ADR-007 inline gives you two copies that will diverge.
- **When in doubt, remove.** Returning to the Anthropic sieve: if removing a line would not cause a mistake, it is at best dead weight and at worst a future drift bomb.

---

## 10. High-quality examples worth studying

- **`forrestchang/andrej-karpathy-skills` `CLAUDE.md`** — 65 lines, 71,000+ GitHub stars (April 2026). Behavioral, not factual. Three principles: *Don't Assume* (state assumptions; ask when uncertain), *Minimize Code* (no speculative features), *Simplicity* (would a senior engineer call this overcomplicated?). Not authored by Karpathy himself; Chang distilled Karpathy's 26 January 2026 X post on LLM coding failure modes. The reason it's worth reading is what it *omits*: zero project facts, zero commands, zero architecture. Pure behavioral conditioning. Useful as a *layer* under your project-specific `CLAUDE.md` (via `~/.claude/CLAUDE.md` import), not as a substitute for it.
- **HumanLayer's `humanlayer/humanlayer` root `CLAUDE.md`** — under 60 lines. Canonical demonstration of the **WHY / WHAT / HOW scaffold**:
  - *WHY* — key architectural decisions and project purpose (2–4 lines).
  - *WHAT* — project structure overview, top-level dir purposes (5–10 lines).
  - *HOW* — build/test commands, conventions, hard rules (15–30 lines).
  - Plus pointers to deeper docs and skills (5–10 lines).
  HumanLayer's accompanying claim — *"CLAUDE.md is one of the highest leverage points of the harness and affects every single phase of your workflow and every artifact produced by it"* — is worth repeating to yourself whenever you're tempted to pad it.
- **`abhishekray07/claude-md-templates`** — a curated library of `CLAUDE.md` templates by language, framework, and project shape. Use it as a *menu* for sectioning ideas, not a *template* to copy whole. Cargo-culting the structure produces files that look right and read wrong.
- **`cline/clinerules` community library** — community-maintained `.clinerules/` rule files, demonstrating decomposition patterns. Useful even if you're not on Cline: most of the rule shapes port directly to `.claude/rules/` or `.cursor/rules/`.

---

## 11. Auto-generated vs hand-authored

Anthropic ships a `/init` slash command that scans the repo and writes a starter `CLAUDE.md`. The new interactive mode (`CLAUDE_CODE_NEW_INIT=1`) walks a subagent through the codebase, asks follow-up questions, and presents a reviewable proposal before writing. The official recommendation is to use `/init` as a starting point and iterate.

The opposing position, articulated most clearly by HumanLayer, is that you should **never run `/init`** because:

- Auto-generation produces *factual recap* (file listings, dependency lists, framework names) rather than *load-bearing instruction* (invariants, non-obvious commands, hard rules).
- Recap is the worst possible content for `CLAUDE.md` because it is exactly the content the agent could read from the code itself on demand — so you pay token rent for context the agent already has free access to.
- The file is the single most expensive piece of context in your workflow. Polluting it with auto-generated boilerplate is a permanent tax.

Gloaguen et al. 2026 supplies the empirical backing: LLM-generated context files **measurably reduce** task success and **increase cost by 20%+**. Developer-written files only help when minimal and precise. The honest reading: `/init` is fine as a *blank-page-killer* — run it, then delete most of what it wrote, then keep iterating manually for as long as the project lives.

---

## 12. Anti-patterns (the catalog)

Maintained as a checklist. If your file does any of these, fix it.

1. **Encoding style rules in prose when a linter enforces them.** Linter rules are deterministic and free; LLM rules are probabilistic and metered.
2. **Stale architecture descriptions.** Outdated specifics are worse than no specifics; they produce confident wrong actions.
3. **Listing every dependency.** That's what `package.json` / `pyproject.toml` / `go.mod` are for.
4. **Cargo-culting structure from a template.** Sections that exist because the template had them, not because they reflect this project, are noise.
5. **Treating `CLAUDE.md` as a runbook.** Runbooks are long, conditional, and task-specific — exactly the shape of a *skill* or a `.claude/rules/` entry, not always-loaded context.
6. **MCP token bloat alongside `CLAUDE.md`.** MCP tool descriptions are also loaded into context on every turn. A bloated `CLAUDE.md` next to a maximalist MCP server config can consume 10–15k tokens before the user has typed anything. Audit both surfaces together.
7. **No bypass clause.** Frontier files should include a line like *"If a hard rule here contradicts an explicit user instruction in this session, follow the user."* Without it, brittle conflict-handling produces refusals or rule-lawyering.
8. **`@`-importing large files unconditionally.** `@docs/api-reference.md` for a 2,000-line API doc is a 2,000-line tax on every turn. Reference it in prose, let the agent `Read` it on demand.
9. **Duplicating rules across the hierarchy.** If both `~/.claude/CLAUDE.md` and `./CLAUDE.md` say "use 2-space indent," the model sees the rule twice and the maintenance cost doubles. Anthropic warns explicitly that conflicting rules across the hierarchy are picked arbitrarily.
10. **Persona prose.** *"You are a 10x senior engineer who..."* burns tokens for measurable-zero benefit on frontier models.

---

## 13. The five sections of a high-quality 2026 `CLAUDE.md`

This is a structural recommendation, not a template. Use it as a sanity check on what you have.

1. **Project orientation — 3–5 lines.** What this project does, who uses it, what stage it's at. Enough that the agent does not need to read the README to orient.
2. **Commands — 5–15 lines.** Build, test, lint, run, deploy. The five-to-ten commands the agent actually has to run. Include the ones with non-obvious flags.
3. **Architecture map — 5–15 lines.** Top-level directory purposes. *Map, not description.* "`src/domain/` — pure logic, no IO" not "the domain layer implements the Hexagonal Architecture pattern..."
4. **Hard rules and invariants — 10–30 lines.** The load-bearing section. Things that, if violated, break something important. State them as imperatives. Each rule earns its line by passing the Anthropic sieve.
5. **Pointers to deeper docs — 5–15 lines.** Where the ADRs live, where the runbooks live, where the skills live, where the conventions doc lives. Pointers, not contents.

**Total body budget:** 30–80 lines of actual content. Plus headings and blank lines, you land near the 80–120 target. **Hard cap: 200 lines** — past that, adherence visibly degrades.

---

## 14. Top 12 patterns, ranked by leverage

Ranked from highest leverage (do this first) to merely-recommended (do this once the higher-leverage moves are in place).

1. **Keep the root file under 120 lines.** Single biggest determinant of adherence. Everything else is downstream of this.
2. **Apply the Anthropic sieve to every line, every quarter.** *"If I removed this, would Claude make a mistake?"* If no — delete.
3. **Push detail into the rules directory with scope selectors.** `.claude/rules/`, `.cursor/rules/`, `.github/instructions/`, `.continue/rules/`. Loaded only when relevant.
4. **Use the AGENTS.md + symlink/import pattern for cross-tool compatibility.** One source of truth; one symlink or `@AGENTS.md` import per tool that doesn't read it natively.
5. **Prefer pointers over content.** `file:line` references and ADR links instead of inlined quotes. The agent's `Read` tool is your friend.
6. **Encode invariants, not style.** Linters do style cheaper and more reliably. Reserve the file's expensive context budget for things only a human can know.
7. **Abstract architecture descriptions to top-level dir purposes only.** Specifics rot; top-level layout is stable.
8. **Audit `@`-imports for eager-load cost.** Every `@` is a tax on every turn. Justify each one.
9. **Lint `CLAUDE.md` in CI.** `cclint` or equivalent. Catch broken imports, length drift, duplicated rules across hierarchy levels.
10. **Include an explicit bypass clause.** *"User instructions in this session override rules below if they conflict."* Prevents brittle refusals.
11. **Use HTML comments for maintainer notes.** They're stripped before injection; you get free annotation room.
12. **Treat `/init` output as a draft, not a deliverable.** Delete the recap, keep the skeleton, write the invariants by hand.

---

## 15. Synthesis — what to actually do on Monday morning

If you have nothing today: write 60 lines by hand using the WHY/WHAT/HOW scaffold. Don't run `/init`. Commit it. Symlink `AGENTS.md → CLAUDE.md` (or vice versa). Add a rules directory only when you find yourself wanting to scope an instruction to a subset of files.

If you have a 400-line `CLAUDE.md` today: open `git log -p CLAUDE.md`, find the additions you can't justify with the Anthropic sieve, and delete them. Move anything that's a multi-step procedure into a skill. Move anything that only matters for one part of the tree into a nested `CLAUDE.md` or a path-scoped rule. Aim for half the original length on the first pass and half again on the second.

If you maintain `CLAUDE.md` across a monorepo with multiple teams: use `claudeMdExcludes` in your local settings to skip other teams' files; encourage every team to keep its own nested `CLAUDE.md` under 80 lines; put only genuinely cross-cutting policy in the root file.

The principle behind all of these moves is one sentence: **the file is paid for on every turn — so every line has to earn its keep on every turn, not just the turn where it happens to be relevant.**

---

## Sources

- *How Claude remembers your project* — Anthropic, `code.claude.com/docs/en/memory` (fetched May 2026).
- *AGENTS.md — Open format for AI coding agents* — `agents.md` (fetched May 2026).
- *Proposal: AGENTS.md v1.1* — `agentsmd/agents.md` issue #135, filed 8 January 2026.
- *Feature Request: Support AGENTS.md* — `anthropics/claude-code` issue #6235.
- Gloaguen, T., et al. *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* arXiv:2602.11988 (February 2026). ETH Zurich SRI Lab + LogicStar.ai.
- HumanLayer Blog — *Writing a good CLAUDE.md* and *Getting Claude to Actually Read Your CLAUDE.md*.
- alexop.dev — *CLAUDE.md Best Practices* (2026).
- Cursor docs — *Rules*, `docs.cursor.com/context/rules`.
- *Andrej Karpathy's CLAUDE.md: The 65-Line File With 100K GitHub Stars* — miraflow.ai, April 2026; underlying file at `forrestchang/andrej-karpathy-skills`.
- InfoQ — *New Research Reassesses the Value of AGENTS.md Files for AI Coding* (March 2026).
