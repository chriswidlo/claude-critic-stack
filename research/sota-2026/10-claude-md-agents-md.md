# Project-Level AI Instruction Files (2026 SOTA)

CLAUDE.md, AGENTS.md, .cursorrules, .clinerules, and the convergence story

---

## 1. The format wars: who reads what

Mid-2026 is the moment the project-instruction-file market finally fractured along two axes — *single-vendor file vs. shared standard*, and *flat-file vs. layered-directory*. The combinations:

| Tool | Primary file | Layered form | Reads others? |
|---|---|---|---|
| Claude Code (Anthropic) | `CLAUDE.md` | `.claude/CLAUDE.md`, subdir `CLAUDE.md`, `CLAUDE.local.md`, user-global `~/.claude/CLAUDE.md` | No native AGENTS.md (open issue #6235, "thousands of upvotes" as of April 2026) — `@import` workaround |
| OpenAI Codex / ChatGPT Codex | `AGENTS.md` | nested per-package | Native AGENTS.md, originated the convention |
| Cursor | `.cursor/rules/*.mdc` (modern); `.cursorrules` (legacy, silently ignored in Agent mode) | per-rule scope via YAML frontmatter (`alwaysApply`, `globs`, `description`) | AGENTS.md (added 2025) |
| Aider | `.aider.conf.yml` + `CONVENTIONS.md` (loaded via `read:` directive) | home + repo-root + cwd, last wins | No AGENTS.md auto-read; users symlink |
| Continue.dev | `config.yaml` + `.continue/rules/*.md` | rules folder, lexicographic ordering, `globs`/`regex` selectors | AGENTS.md supported |
| Cline | `.clinerules/` directory of `.md`/`.txt` files | conditional rules via YAML frontmatter | AGENTS.md supported (cline/clinerules repo) |
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/instructions/**/*.instructions.md` | per-glob via frontmatter | AGENTS.md supported (Copilot coding agent) |
| Gemini CLI, Devin, Jules, Amp, Warp, Goose, Factory, Windsurf, OpenCode | AGENTS.md primary | varies | AGENTS.md native |

Two observations matter:

1. **Every modern tool has migrated from a flat dotfile to a directory of scoped rules.** `.cursorrules` → `.cursor/rules/*.mdc`. Cline deprecated its custom-instructions text box in favor of `.clinerules/`. Copilot added `.github/instructions/**`. The reason is uniform: a flat file pays its token cost on *every* turn even when irrelevant; a directory with glob/description selectors pays only when the rule matches. The legacy file always still works for backwards compat, but the agentic modes prefer the layered form.

2. **The vendor-neutral file (`AGENTS.md`) won the cross-tool race, but did not displace the vendor file.** As of May 2026, AGENTS.md reports adoption by 60,000+ open-source projects and is read natively by 18+ agents — but Claude Code, the single largest coding-agent install base, still does not read it. The workaround is a symlink: `ln -s AGENTS.md CLAUDE.md`. One file on disk, two names, zero drift. Anthropic's Boris Cherny endorsed an `@AGENTS.md` import directive inside `CLAUDE.md` as an alternative.

## 2. The convergence story: AGENTS.md and the Agentic AI Foundation

AGENTS.md started as an OpenAI Codex convention in August 2025. By December 2025 it was contributed to the **Agentic AI Foundation** under the Linux Foundation, with founding members Anthropic, OpenAI, and Block; Microsoft and Google joined shortly after. The same foundation now stewards MCP (the Model Context Protocol Anthropic donated).

The current draft, **AGENTS.md v1.1** (proposal #135, January 8 2026), codifies four implicit conventions:

- **Hierarchical scope.** Nested AGENTS.md files cascade; "closest file to the edited file wins."
- **Precedence rules.** Explicit conflict resolution between layers.
- **Optional YAML frontmatter** (`description`, `tags`, `globs`) for **progressive disclosure** — so a harness can index without loading the full body.
- **Backwards compatible.** All existing AGENTS.md files remain valid; frontmatter is opt-in.

The spec is deliberately thin. Standard Markdown, no mandatory fields, file lives at repo root, monorepo-friendly via nesting. Common sections — overview, build/test commands, code style, security notes — are *suggested*, not required. This is the "README for agents" framing.

The takeaway for the convergence question: **the format war is over in spec, ongoing in implementation.** AGENTS.md is the de facto standard. CLAUDE.md is the de facto Anthropic-specific extension. The pragmatic 2026 setup writes AGENTS.md as the canonical file, and either symlinks or `@`-imports it from CLAUDE.md.

## 3. What goes in a project-instruction file (the load-bearing question)

Anthropic's own [Claude Code best-practices doc](https://code.claude.com/docs/en/best-practices) frames CLAUDE.md as "persistent context Claude cannot infer from code alone" and offers a single load-bearing test for every line: *"If I removed this, would Claude make a mistake?"* If no, delete.

The community consensus on what belongs:

- **Tech stack basics with versions.** Node 22, Python 3.12, Postgres 16 — things Claude cannot deduce from `package.json` without reading it.
- **Non-obvious commands.** `bun test` not `npm test`; `make canon-refresh` not a documented script.
- **Architecture *map*, not architecture *description*.** Names of the top-level dirs and one-sentence purposes. Not data-flow diagrams (those drift).
- **Hard rules / invariants.** "Never edit migrations after merge." "All HTTP calls go through `src/http/client.ts`."
- **Workflow rules.** Branch naming, commit conventions, whether to run tests before commit. (This stack's 12-step workflow is exactly this kind of rule — load-bearing because it changes default Claude behavior on every session.)
- **Domain terminology.** "User" means authenticated principal, "Account" means billing entity. Glossaries pay for themselves.

What does **not** belong, per [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [alexop.dev's progressive-disclosure post](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/), and Anthropic's own doc:

- **Anything the linter can enforce.** "Use 2-space indent" is verifiable by Prettier; writing it in prose wastes context. The slogan: *"Never send an LLM to do a linter's job."*
- **Anything the code can teach.** Function signatures, import patterns, class hierarchies. Claude reads code.
- **Anything `git log` can teach.** Recent change history, who-touched-what.
- **README recapitulation.** Project elevator pitch belongs in README.md, which Claude can read via `@README.md`.
- **Every dependency.** `package.json` is the source of truth.
- **Task-specific instructions.** Belong in a sibling doc the rule *points to*.

The empirical anchor: **frontier LLMs reliably follow only 150–200 instructions per session, and Claude Code's system prompt already consumes ~50.** That leaves a hard ceiling of roughly 150 instructions across CLAUDE.md, AGENTS.md, MCP tool descriptions, and the user turn combined. Every prose paragraph that the linter could enforce is a stolen instruction-slot.

The context-engineering framing makes this sharper: **CLAUDE.md is paid on every turn, before the user has typed a word.** A 5,000-token CLAUDE.md is a 5,000-token tax per assistant response — not just per session. The recurring cost dominates the lifetime budget of a long project.

## 4. Structural patterns

**Length.** Industry recommendations have tightened over 2026. The early consensus (200 lines) has shifted toward **80–120 lines for the "high-signal" body**, with overflow pushed into `@`-imported sibling files. HumanLayer's own production CLAUDE.md is under 60 lines. Andrej Karpathy's much-cloned 65-line file is the canonical "small is correct" example.

**Headings that work.** Short, imperative, scannable. `## Do not do these things`. `## Commands`. `## Architecture map`. Long narrative paragraphs fail; bulleted directives win. Use H2 to separate topics; H3 only when a topic has internal subdivisions.

**Inheritance / layering** (Claude Code specifically). Four levels, all combine simultaneously, more-specific overrides on conflict:

1. **User-global** — `~/.claude/CLAUDE.md`. Personal preferences across every project (commit message style, "prefer ripgrep over grep").
2. **Project** — `./CLAUDE.md`. Team-shared, committed to git.
3. **Subdirectory** — `./<dir>/CLAUDE.md`. Loaded on-demand only when Claude accesses files in that dir. This is the key feature: a 500-line backend-only CLAUDE.md does not tax frontend-only sessions.
4. **Personal/gitignored** — `./CLAUDE.local.md`. Local overrides not shared with the team.

**`@`-mention imports.** Inside any CLAUDE.md, `@path/to/file.md` inlines that file at session start. Recursive up to 5 hops. Paths resolve relative to the importing file. External imports trigger a one-time approval dialog. Known footgun: silent failure on paths containing spaces (anthropics/claude-code issue #56927). The practical use: keep the root file lean, `@`-import detailed runbooks only when needed (or use prose pointers and let Claude `Read` them on demand — the more disciplined pattern, because `Read` is lazy and `@` is eager).

**Updating cadence.** Three viable disciplines:

- **Living document.** Update at session boundaries when you discover a missing rule. Anthropic recommends this in their best-practices post: "we'll iterate on CLAUDE.md as we work."
- **Periodic checkpoint.** Quarterly review with a diff over the last 90 days, prune anything stale.
- **Linted.** Tools like [cclint](https://github.com/felixgeelhaar/cclint) validate CLAUDE.md against rules (line count, deprecated patterns, broken `@`-imports) in CI.

The drift failure mode: a stale CLAUDE.md is *worse* than no CLAUDE.md, because Claude reads it with the same authority as a fresh one. Architecture descriptions that no longer match the code are the most common offenders. The defense is to keep architecture descriptions abstract enough that they do not drift (top-level dir purposes, not module-level data flow), or replace prose with a pointer to an ADR directory.

## 5. High-quality public examples worth studying

- **[Andrej Karpathy's CLAUDE.md](https://github.com/forrestchang/andrej-karpathy-skills)** — 65 lines, 100K+ stars, four behavioral principles (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution). **Borrowable idea:** the entire file is *behavioral*, not factual. It changes how Claude thinks, not what Claude knows. Compare with the typical /init output, which is 90% factual recap.
- **[HumanLayer's own CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)** — under 60 lines, structured around WHAT (stack), WHY (purpose), HOW (workflow). **Borrowable idea:** three-question scaffold as a forcing function for brevity.
- **[abhishekray07/claude-md-templates](https://github.com/abhishekray07/claude-md-templates)** — stack-specific templates (Next.js, FastAPI, Rust). **Borrowable idea:** stack templates as starting points to subtract from, not add to.
- **[awesome-copilot/docs/README.instructions.md](https://github.com/github/awesome-copilot)** — GitHub's own catalogue of `.instructions.md` patterns by file type. **Borrowable idea:** per-glob instruction files as the path-scoped equivalent of subdir CLAUDE.md.
- **[cline/clinerules](https://github.com/cline/clinerules)** — community library of rules, skills, workflows, and AGENTS.md files. **Borrowable idea:** rules as shareable, reviewable artifacts, not buried in one-off `.cursorrules`.
- **[FlorianBruniaux/claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)** — production templates. **Borrowable idea:** "cheatsheet" framing — the file is a quick-reference, not a textbook.

## 6. Auto-generated vs hand-authored

The `/init` slash command scans the project structure, identifies the stack from config files, and produces a CLAUDE.md covering project overview, commands, architecture, and code style. If a CLAUDE.md already exists, `/init` updates rather than overwrites.

The split in the community is sharp:

- **Anthropic's official position:** start with `/init`, then iterate. The best-practices doc treats the auto-generated file as a baseline to refine over time.
- **HumanLayer's position:** never use `/init`. The file is "the highest leverage point of the harness" and auto-generation produces precisely the kind of factual recap (dependencies, file lists) that the model can derive from the code itself. Auto-generation pollutes the most expensive context budget you have.
- **2026 research (Gloaguen et al., 138 repos)** reports that LLM-generated context files *reduced* agent task success while increasing inference cost by 20%+. This is consistent with the HumanLayer view.

The pragmatic synthesis: `/init` is fine as a *one-time scaffolding step* if you then aggressively delete. Treat its output as a maximally-bloated draft and ask the "would Claude make a mistake without this line" question on every line. Commit only what survives.

**Version control.** Commit CLAUDE.md alongside code. Review changes in PR. Treat it as production configuration, because that is what it is. Personal overrides go in `CLAUDE.local.md` and `.gitignore` it.

## 7. Anti-patterns

- **Encoding style in prose** when the linter enforces it. ("Use single quotes." → ESLint rule.)
- **Stale architecture descriptions** that drift from code. Either keep architecture descriptions abstract (top-level dir purposes), or replace with pointers to ADRs that have their own update discipline.
- **Listing every dependency.** `package.json` is canonical.
- **Cargo-culting structure** from a famous CLAUDE.md without justifying each section against your project's actual failure modes. Karpathy's file works for Karpathy's style; copying it without removing what doesn't apply is the same mistake as copying it being auto-generated.
- **Treating CLAUDE.md as a runbook.** Long procedures belong in `@`-imported runbooks or skills, loaded on demand.
- **MCP token bloat alongside.** If MCP server tool descriptions consume 20K tokens, the CLAUDE.md budget is irrelevant — the whole context is already strained. Audit MCP loadout the same way.
- **No bypass.** Workflow rules with no escape hatch ("always run the 12-step workflow") block legitimate quick-take questions. The bypass clause should be in the file.

## 8. For this specific stack: questions to ask, not answers to copy

This repo's `CLAUDE.md` is 153 lines as of this writing — within the 200-line cap, above the 80–120 high-signal target. The honest questions to ask of it:

- **Does every section pass the "would Claude make a mistake without this" test?** The 12-step workflow does (it changes default behavior on every design question). The path-discipline rule does (the linter cannot enforce "no absolute paths in prose"). But does the "things you must not do" section overlap enough with the workflow section that one of them is redundant?
- **Is the architecture description abstract enough to resist drift?** The agent list and the workflow steps reference real files. When agents are renamed or steps reorganized, the file must be updated in the same PR. Is there CI to catch drift, or is it manual discipline?
- **Should sub-areas have their own CLAUDE.md?** `.claude/agents/` and `upgrades/` are large enough that a subdir CLAUDE.md loaded on-demand might reduce per-session token cost while improving local relevance.
- **Where does AGENTS.md fit?** If anyone on the team uses Cursor, Copilot, or Codex against this repo, an AGENTS.md (or symlink) reduces drift between tools. If everyone uses Claude Code, AGENTS.md is overhead with no consumer. The decision point is *known consumers*, not hypothetical future ones.
- **Is anything in CLAUDE.md actually a hook?** Path-discipline checks are scripted in `bin/check-path-discipline.sh` and there is a `path-check` skill. If the check is deterministic and the cost of a missed violation is high, the hook form catches it 100% of the time vs. CLAUDE.md's ~80%.

## 9. What five sections does a high-quality 2026 CLAUDE.md have?

Distilled from Anthropic guidance, the HumanLayer and alexop.dev posts, the Karpathy file, and the cclint linter's defaults:

1. **Project orientation (3–5 lines).** What this project is and is not. One alternative framing for what someone might assume incorrectly. Not a marketing pitch.
2. **Commands (5–15 lines).** Build, test, lint, run, deploy. Only the non-obvious ones; do not duplicate `package.json` scripts that are self-explanatory.
3. **Architecture map (5–15 lines).** Top-level directories and one-line purposes. No data flows, no module diagrams — those drift.
4. **Hard rules and invariants (10–30 lines).** Things Claude will get wrong by default that matter for this codebase. "Never edit migrations after merge." "All HTTP through `src/http/client.ts`." Workflow gates (e.g., the 12-step workflow's hard gate on `scope-map.md`).
5. **Pointers to deeper docs (5–15 lines).** `@`-imports for runbooks, or prose pointers to ADRs, contribution guides, and `~/.claude/` skills. The "if you need more, look here" section. Includes `AGENTS.md` if maintained.

Total budget: 30–80 lines of body, plus headings. Hard cap: 200. Anything beyond goes into the pointer section as a link, not inline.

## 10. Synthesis: top 10 patterns for project-instruction files in 2026

1. **Write AGENTS.md as the canonical file** for cross-tool teams, symlink or `@`-import from CLAUDE.md for Anthropic-tool teams. One source of truth, multiple filenames.
2. **Target 80–120 lines of body**, hard cap at 200. Every line passes the "would the agent make a mistake without this?" test.
3. **Prefer behavioral rules over factual recap.** Things that change how the agent thinks beat things the agent could read from the code.
4. **Never duplicate the linter.** If a tool can enforce it deterministically, do not write prose about it. Mention the tool, not the rule.
5. **Use layered files for scoped rules.** Subdir CLAUDE.md, `.cursor/rules/*.mdc`, `.github/instructions/**`, `.continue/rules/`, `.clinerules/`. Pay token cost only when the rule is relevant.
6. **Use `@`-imports sparingly; prefer prose pointers and lazy `Read`.** Eager import loads on every turn; lazy read loads on demand.
7. **Audit the full context loadout, not just CLAUDE.md.** MCP tool descriptions, skills, hooks, and agent system prompts all compete for the same 150-instruction budget.
8. **Commit project files; gitignore personal files.** `CLAUDE.md` and `AGENTS.md` are reviewed in PR. `CLAUDE.local.md` is per-developer.
9. **Lint the context file itself.** Tools like cclint catch broken `@`-imports, stale references, and over-length files in CI.
10. **Promote deterministic constraints to hooks.** CLAUDE.md is 80% reliable; hooks are 100%. If the cost of a 20% miss is high (security, formatting, paths leaving the repo), make it a hook and reference the hook from CLAUDE.md.

---

## Sources

- [Best practices for Claude Code (Anthropic docs)](https://code.claude.com/docs/en/best-practices)
- [How Claude remembers your project (Anthropic docs)](https://code.claude.com/docs/en/memory)
- [Explore the .claude directory (Anthropic docs)](https://code.claude.com/docs/en/claude-directory)
- [AGENTS.md homepage](https://agents.md/)
- [agentsmd/agents.md GitHub repo](https://github.com/agentsmd/agents.md)
- [AGENTS.md v1.1 proposal (Issue #135)](https://github.com/agentsmd/agents.md/issues/135)
- [OpenAI: Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [OpenAI Agentic AI Foundation announcement](https://openai.com/index/agentic-ai-foundation/)
- [Anthropic: Donating MCP and Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [TechCrunch: OpenAI, Anthropic, Block Linux Foundation](https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/)
- [HumanLayer: Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [alexop.dev: Stop bloating your CLAUDE.md (progressive disclosure)](https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/)
- [The Prompt Shelf: AGENTS.md vs CLAUDE.md (2026)](https://thepromptshelf.dev/blog/agents-md-vs-claude-md/)
- [The Prompt Shelf: .cursorrules vs .cursor/rules MDC (2026)](https://thepromptshelf.dev/blog/cursorrules-vs-mdc-format-guide-2026/)
- [Hivetrail: AGENTS.md vs CLAUDE.md cross-tool guide](https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard)
- [Morph: AGENTS.md and SKILL.md complete guide (2026)](https://www.morphllm.com/agents-md-guide)
- [Cursor Rules Complete .mdc Guide (Morph, 2026)](https://www.morphllm.com/cursor-rules-best-practices)
- [Aider: YAML config file docs](https://aider.chat/docs/config/aider_conf.html)
- [Aider: Specifying coding conventions (CONVENTIONS.md)](https://aider.chat/docs/usage/conventions.html)
- [Continue.dev: How to Create and Manage Rules](https://docs.continue.dev/customize/deep-dives/rules)
- [Cline: Rules documentation](https://docs.cline.bot/customization/cline-rules)
- [cline/clinerules community library](https://github.com/cline/clinerules)
- [GitHub Docs: Adding repository custom instructions for Copilot](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [GitHub Blog: 5 tips for writing better custom instructions for Copilot](https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/)
- [Miraflow: Karpathy CLAUDE.md, 100K stars](https://miraflow.ai/blog/karpathy-claude-md-100k-github-stars-ai-coding-2026)
- [SSW.Rules: Do you symlink AGENTS.md to tool-specific files?](https://www.ssw.com.au/rules/symlink-agents-to-claude)
- [Rushi's: Sharing AI agent configs between Cursor and Claude with symlinks](https://www.rushis.com/sharing-ai-agent-configs-between-cursor-and-claude-with-symlinks/)
- [Arize AI: Optimizing coding-agent rules across CLAUDE.md, AGENTS.md, .clinerules, .cursor/rules](https://arize.com/blog/optimizing-coding-agent-rules-claude-md-agents-md-clinerules-cursor-rules-for-improved-accuracy/)
- [The Prompt Shelf: CLAUDE.md token-budget optimization](https://thepromptshelf.dev/blog/claude-md-token-budget-optimization/)
- [Bijit Ghosh: The Complete Guide to CLAUDE.md (Medium, May 2026)](https://medium.com/@bijit211987/the-complete-guide-to-claude-md-memory-rules-loading-and-cross-tool-compression-97cc12ed037b)
- [Mandar Karhade: The .claude Folder Is Important (Towards AI)](https://pub.towardsai.net/the-claude-folder-is-important-and-youre-likely-ignoring-it-33fc97f6d9fa)
- [cclint: linter for CLAUDE.md context files](https://github.com/felixgeelhaar/cclint)
- [Vincent's Blog: Claude Code /init in 10 seconds](https://blog.vincentqiao.com/en/posts/claude-code-init/)
- [Tessl: Agents.md, an open standard for AI coding agents](https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/)
- [Augment Code: How to write good AGENTS.md files](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files)
- [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
