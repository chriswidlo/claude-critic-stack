# Master Synthesis — SOTA 2026 AI Workflow Setup

**For the claude-critic-stack: pre-launch readiness for 10 parallel worktrees + SOTA workflow upgrade plan.**

Vintage: 2026-05-17. Source: 13 deep-dive research reports under [research/sota-2026/](research/sota-2026/), totaling ~52,000 words of citation-heavy investigation. Each recommendation is grounded; per-recommendation pointers to the source report are at the end of each section.

---

## 0. Headline diagnosis

The stack you have is **structurally ahead of the 2026 industry on three axes** and **structurally behind on five.** Most "AI workflow SOTA" content is targeted at velocity-of-correct-looking-output; you've built an adversarial-review-of-design-decisions stack. The two communities have different anti-patterns; copying ecosystem ideas wholesale will harm you. Borrowing where the velocity tools have solved a problem you *also* have — checkpointing, resume, structural retrieval, role-splits, cost circuit breakers — without trading the adversarial posture is the right shape.

**Where you're ahead of industry:**
- **Anti-confirmation discipline in the retriever** (canon-librarian's "must return one contradicting passage"). Most production RAG selects *for* agreement; you select against it. Genuinely novel. [11-memory-rag.md §8]
- **File-artifact-driven shared state with consent-gated writes.** Industry is converging on what you already do — Anthropic explicitly recommends this in *Building Effective Agents* and *Effective Context Engineering*. [02 §2-3, 11 §8]
- **Critic panel with minority-veto + cross-model shadow lane** (`SHADOW_PANEL=1`). The literature catching up to this in 2026 (Petri 2.0, agent-as-judge surveys). [04 §3, 06 §4]

**Where you're behind:**
1. **No pre-launch readiness for 10 parallel worktrees.** Several silent-breakage classes will hit on first run. [08 §10]
2. **No cost circuit breaker.** The $47K / $30K / $87K runaway-loop cases in the literature are all you, missing exactly the same primitive. [12 §9]
3. **CLAUDE.md is over the 80-120 line high-signal target** (153 lines). Past ~150 instructions, frontier LLMs reliably follow only the first ones. [10 §3]
4. **No external-family shadow** (`EXTERNAL_SHADOW=1` reserved but inert). Same-family panels inherit family-correlated biases that the literature now treats as a known structural defect. [04 §3f]
5. **No golden-dataset / calibration set** for the critic panel. Without one, prompt edits to lenses are unsignedrade vs regress. [06 §10]

The good news: every one of these is fixable with files you already know how to write, in the existing aesthetic, without adopting a single SaaS platform.

---

## 1. Pre-launch readiness for 10 parallel worktrees

**This is the immediate blocker.** Without these, the first 10-worktree run will produce silent failures, runaway costs, or both. Ordered by severity.

### 1.1 — Must-do before any 10-worktree run

**P0-A. Per-worktree branch + naming convention.**
Every worktree gets its own branch (`agent/<session-id>` or `wt/<n>-<slug>`). Git's one-branch-one-worktree invariant is absolute; trying to share branches collides with `fatal: '<branch>' is already checked out`. [08 §1.3]

**P0-B. `.worktreeinclude` at repo root.**
List gitignored files that should propagate to each new worktree (`.envrc`, `mise.toml`, `.env.local`). Without it, each worktree starts from a cold `npm install` and zero env config. The diagnostics binding you just shipped lives in `.claude/.metrics/staging/` — that's user-global, fine — but per-worktree env (DB URL, port offset) is the missing piece. [08 §1.2, 1.7]

**P0-C. Cost circuit breaker.**
Per-worktree budget (e.g., $5), per-day org budget (e.g., $50), automated suspension on breach. Parse `cost_usd` from `--output-format json` of every headless invocation. The literature has documented $47K-$87K runaway-loop incidents from teams that exactly didn't have this. *"There is no circuit breaker. The first signal is the invoice."* [12 §9; 04 §4b]

**P0-D. Audit every existing hook for worktree-naivete.**
Any hook that writes to "the project root" must `git rev-parse --git-common-dir` first to find the canonical repo. `CLAUDE_PROJECT_DIR` in a worktree is the *worktree path*, not the parent repo. The diagnostics infrastructure I just landed got this right (each worktree produces its own `events.jsonl`); other hooks may not have. Concrete failure documented at [thedotmack/claude-mem#1276](https://github.com/thedotmack/claude-mem/issues/1276). [08 §2.3]

**P0-E. System limits.**
- `ulimit -n 65536` in shell rc — file descriptor limit. macOS default 256, Linux varies. 10 sessions + 10 dev servers + watchers easily chew 5-10k fds. [08 §4.2]
- On Linux: `fs.inotify.max_user_watches=524288`, `fs.inotify.max_user_instances=512` — file watcher limits. Default 8192 will saturate at 3 worktrees of a Vite project. [08 §4.3]
- 64 GB RAM is the floor. 128 GB is comfortable. [08 §4.1]

**P0-F. Disable `gc.auto` for the duration of the batch.**
`git config gc.auto 0` at repo level. Compaction races with concurrent writers. Run `git gc` once at end of batch. [08 §2.6]

**P0-G. Backup `~/.claude.json`** to a timestamped copy before launching. Rare but documented corruption under heavy parallel session start. [08 §7]

**P0-H. Per-worktree permission scoping via `.claude/settings.local.json`.**
The price of running 10 worktrees is that any one of them can do less damage than the unified workspace. Add deny rules per worktree class:
- Research worktrees: `deny: ["Edit", "Write", "Bash(git push:*)"]` — read-only.
- Codegen worktrees: `allow: ["Edit", "Write"]`, but `deny: ["Bash(rm:*)", "Bash(git push --force:*)", "Bash(sudo:*)"]`.
[12 §10]

**P0-I. Kill switch.**
A single command (or GitHub Actions workflow_dispatch) that terminates all running worktrees. Without it, a runaway is a 3am phone call. Concrete pattern: launch each worktree's Claude under a named tmux session; `tmux kill-server` becomes the kill switch. [08 §3.5; 12 §10]

### 1.2 — Highly recommended (silent-breakage prevention)

**P1-A. `.claude/worktrees/` in `.gitignore`, `.dockerignore`, ESLint/Ruff ignore.**
Claude Code defaults worktrees to `<repo>/.claude/worktrees/<name>`, *inside* the parent. Most file watchers, search tools, and CI scripts will see them. Exclude explicitly. [08 §2.1]

**P1-B. `~/.claude/projects/` cleanup in teardown.**
Each worktree's distinct path produces a distinct `~/.claude/projects/<encoded-path>/` subdir. Old worktree removal doesn't clean these; they accumulate forever, slowing `claude` startup. Add to teardown script. [08 §2.2]

**P1-C. Per-worktree DB isolation.**
The single biggest "silently broken" mode at 10 worktrees is one shared `DATABASE_URL`. 10 agents migrating + seeding + rolling back against one DB produces non-determinism and occasional schema corruption. Patterns: SQLite-per-WT (cheapest); named-DB-per-WT (e.g. `app_dev_${WT_NAME}`); container-per-WT (heaviest, cleanest). [08 §3.2]

**P1-D. Per-worktree port offsets.**
Hash worktree name → port base: `PORT=$((3000 + $(echo $WT | cksum | cut -d' ' -f1) % 1000))`. The Conductor/Workmux pattern. Deterministic, reproducible, simple. [08 §3.1]

**P1-E. Stagger session starts by ~5 seconds each.**
Anthropic 429s on burst even when sub-cap. Documented at [anthropics/claude-code#46037](https://github.com/anthropics/claude-code/issues/46037). [08 §4.4]

**P1-F. `bin/wt-aggregate <batch-id>` script.**
Walks `git worktree list --porcelain`, collects each worktree's most-recent `synthesis.md` and `ledger.md`, rejects sessions missing the `Ledger: ...` citation line, emits a single rollup. The ledger schema is the natural completeness sentinel — leverage it. [08 §8.5; 12 §10]

**P1-G. `bin/ledger-rollup` for batch-level cost.**
Current ledger is per-session. Across 10 parallel sessions, no rollup sums `agent-calls`, `artifacts`, total cost. If you care about "what did this batch cost," not just "what did session X cost," you need this. Trivial: `jq -s 'add'` over per-session `metrics.json` files. [08 §10.2]

### 1.3 — Concrete recipe: pre-launch checklist

```
[ ] System limits bumped (ulimit -n, inotify on Linux)
[ ] gc.auto disabled for the batch
[ ] ~/.claude.json backed up
[ ] .worktreeinclude written (.envrc, mise.toml minimum)
[ ] .claude/worktrees/ in .gitignore + .dockerignore
[ ] bin/wt-provision <slug> script tested on 1 worktree
[ ] Per-worktree DB convention chosen (sqlite | named-pg | container)
[ ] Per-worktree port offset scheme set up via direnv
[ ] .claude/settings.local.json template per worktree class
[ ] Cost circuit breaker: max $5/wt, $50/day; alarm wired to email/Slack
[ ] Kill switch tested: tmux kill-server or equivalent
[ ] Every hook in .claude/hooks/ audited for git-rev-parse use
[ ] bin/wt-aggregate <batch-id> script tested on 2-worktree dry run
[ ] bin/wt-teardown <slug> script cleans ~/.claude/projects/<key>/
```

The throughline of all of the above: **worktrees give you code isolation for free; you must build runtime isolation yourself, and at 10 it becomes load-bearing.** [08 throughout]

---

## 2. The 12 highest-leverage SOTA workflow upgrades

Across all 13 research reports, these are the 12 highest-impact upgrades that apply *because the stack is what it is*. Ranked by impact-per-effort, not by general industry leverage.

### Tier 1 — Land within 1 week

**1. Trim CLAUDE.md to 80-120 lines body (currently 153).**
Frontier LLMs reliably follow only ~150 instructions; Claude Code's system prompt already uses ~50. Every prose paragraph the linter could enforce is a stolen instruction slot. The "would Claude make a mistake without this line" test applied ruthlessly. Push detail into `.claude/rules/<scope>.md` files activated by `paths:` frontmatter (Cursor-style scoped rules — Claude Code supports the same shape). [10 §3, §4]

**2. Wire up `EXTERNAL_SHADOW=1`.**
The reserved env var for cross-family shadow lanes is the single highest-leverage critic-panel upgrade. Same-family panels (all Opus, or even Opus+Sonnet) inherit family-correlated bias documented across arXiv 2410.21819, 2508.06709, 2506.07962. A third lane on a different family (GPT via OpenRouter, or local Qwen) breaks family-correlation. The wrapper script primitive is the unblock. [04 §3f, #1; 06 §10 #8]

**3. Track cache hit rate per session in `ledger.md`.**
Currently absent. Add `cache_read_input_tokens` and `cache_creation_input_tokens` aggregates to the metrics schema; alarm on session-level hit rate <60%. The single most common silent killer of cache hits: a timestamp or request ID inserted *before* a cache breakpoint. At 10 worktrees this matters 10× more. [05 §3.2, §9 #2]

**4. Pin model versions per session.**
`claude-opus-4-7-YYYYMMDD` not `claude-opus-4-7`. Aliases roll forward silently — the April 23 postmortem documents exactly how silent model defaults caused weeks of degraded behavior. The `metrics.json` already captures `models_seen`; promote it to `ledger.md` as a load-bearing field. [06 §7, §10 #1; 02 §8]

**5. Promote path-discipline from CLAUDE.md prose to a PreToolUse hook.**
CLAUDE.md rules are ~80% reliable; hooks are 100%. Path-discipline is deterministic; the script exists; the cost of a miss is the privacy bug the rule exists to prevent. Promote: a PreToolUse hook hard-blocks `Edit`/`Write` when new content contains absolute path strings in markdown. The `path-check` skill stays as the human-invokable counterpart. [01 §1.3 adoption rec; 10 §10 #10; 09 §9 #4]

**6. Three deny rules in `.claude/settings.json`:**
- `deny: ["Read(**/.env*)", "Read(**/.aws/**)", "Read(**/.ssh/**)", "Read(**/id_rsa*)", "Read(**/.netrc)"]` — dotfile + credential paths.
- `deny: ["Bash(rm:*)", "Bash(git push --force:*)", "Bash(git reset --hard:*)", "Bash(sudo:*)"]` — destructive ops.
- `ask: ["WebFetch", "Bash(curl:*)", "Bash(wget:*)", "Bash(gh api:*)"]` — every egress prompts. (For 10 worktrees, scope these to specific hosts via wrapper scripts.)
[09 §9]

### Tier 2 — Land within 2-3 weeks

**7. Build the 20-item critic-panel calibration set.**
*Single highest-leverage eval artifact for this stack.* 20 candidate recommendations with human verdicts per lens (architecture, operations, product). Truth label = consensus of human reviewers. Without it, prompt edits to critic lenses are blind. With it, you have the eval-driven-development gate the broader industry treats as table stakes by 2026. [06 §9, §10 #2]

**8. Add cheap self-review pass between step 9 and step 10.**
Devin 2.2 pattern: a single-model self-critique pass catches own-goals before paying for 6 panel lenses. The expensive outer loop runs only on candidates that pass cheap inner review. Particularly load-bearing at 10 parallel worktrees, where panel cost × 10 dominates the bill. [07 #3, Devin 2.2; 04 #2]

**9. Untrusted-content tagging on every external fetch.**
`canon-librarian`, `outside-view`, `canon-refresher` all bring web bytes into context. Wrap fetched payloads in `<untrusted-source url="..." fetched-at="...">` envelope. The distiller-only orchestrator rule (after step 6) is structurally helpful — but the distillers must also treat their input as untrusted. Mitigates indirect prompt injection through fetched content, the dominant production-exploited channel in 2025-2026. [09 §1.3, §9 #1; 03 §3 Security]

**10. Critic agents emit structured `Verdict: / Confidence:` block.**
**Already landed in this session** as part of the diagnostics work. Worth flagging here because the calibration set (#7) needs it. The aggregator parses these into `judge_score` events; per-lens calibration becomes measurable. [06 §10 #2; 04 §3; this session's repo-changeset.md R5]

**11. Glob-scoped instruction files (`.claude/rules/<scope>.md`).**
Partition CLAUDE.md content into scoped rules activated by file globs. Preserves the ~150-instruction attention budget per scope. Cursor's `.cursor/rules/*.mdc` is the canonical reference; Claude Code supports the same shape via the rules system. [07 #1; 01 §1.9; 10 §10 #5]

**12. Cross-session episodic memory: `sessions-index.md`.**
*Missing memory primitive for the 12-step workflow.* Auto-generate from `ledger.md` files: a summary of the last 20-30 sessions' classifications, frames, recommendations. Lets the orchestrator detect "this looks like the question we answered three weeks ago" and either reuse or deliberately diverge. Today, each session re-reads `canon/corpus/` from scratch and has no awareness of recent sessions' outputs. Concrete, additive, doesn't require new infrastructure beyond the diagnostics aggregator that already exists. [11 §8, §10 #6]

### Tier 3 — Land within 1-2 months

**13. Petri-style judge with branching/rollback authority.**
Critics currently read at step 10 and vote once. Petri's auditor can branch, roll back, prefill, re-probe. A critic that can request a specific clarification from the generator before voting catches more defects than one-shot review. Most useful for high-stakes design decisions; not needed for routine sessions. [04 #2, §3a]

**14. Realism classifier on the generator's context.**
If the generator (step 9) knows the critic-panel is coming, it polishes for the rubric — exactly the eval-awareness pathology the Opus 4.7 system card §6.5.2.2 documented. Pre-step that rewrites step-9 prompts to remove "this will be reviewed" signal. Cheap to add. [04 #3; 05 §6.3; 06 §8]

**15. Architect/editor role split for the generator.**
Aider's signature pattern: strong reasoner produces candidate skeleton, cheap precise model fills in concrete citations and prose. Lets the orchestrator route reasoning effort honestly at step 9. [07 #5, Aider]

**16. Per-agent model + effort calibration.**
- `requirement-classifier`, `subagent-distiller`: pin Haiku 4.5 + `medium` effort. Short-in, short-out; Opus is wasted. [01 §1.5 adoption rec; 05 §5.4]
- `canon-librarian`: Sonnet 4.6 + `low` effort when query is pure retrieval; Opus + `high` when synthesis is needed.
- Critic lenses + comparator: Opus 4.7 + `xhigh`. Where deliberation matters most. [05 §5.3]
- **Pin one thinking mode per agent.** Switching adaptive ↔ disabled invalidates the message cache. [05 §3.5]

**17. Subagents-as-MCP-servers.**
Re-expose `canon-librarian`, `outside-view`, `frame-challenger`, the three critic lenses, and `critic-comparator` as MCP servers. Makes the critic stack portable to Cline, Cursor, Codex, Goose — not just Claude Code. The Goose pattern: MCP is *the* tool surface. [07 #9; 03 §5]

**18. Property-based testing on synthesis structure.**
`synthesis.md` has a contract (classifier label, reframe, outside-view, canon, scope-map, frame challenge, recommendation, ≥3 uncertainties, cheapest experiment, ledger citation). Write a parser that asserts every required section is present. Run as a pre-commit hook or CI gate. The markdown analogue of `exit 0`. [13 §9.1; 06 §10 #9]

**19. Adopt AGENTS.md as canonical, symlink `CLAUDE.md` to it.**
AGENTS.md is the de facto cross-tool standard (60,000+ projects). Claude Code doesn't read it natively (open issue #6235). `ln -s AGENTS.md CLAUDE.md` gives you one file on disk, two names, zero drift, cross-tool compatibility for free. Worth doing if anyone might ever run Cursor/Cline/Codex against the repo. [10 §1, §2, §10 #1]

**20. Nightly Routine for cross-session diagnostics aggregation.**
The single most natural Routines use case for this stack. Reads every `ledger.md` under `.claude/session-artifacts/`, computes warning rates, surfaces anomalous sessions, writes `cross-session-summary.md`. Never modifies session bodies. Pre-declare artifact path, cap work at last 30 days, forbid destructive ops. The DuckDB aggregator I just shipped becomes the engine. [12 §10; 11 §10 #6]

---

## 3. Things to explicitly NOT do (anti-patterns)

The research strongly recommends *against* these. Trust the field-tested no's.

**N1. Don't adopt MCP for everything.** Every MCP server in your config inflates the system prompt with tool descriptions, every one of which is a potential injection surface. Cloudflare's collapse pattern cut token cost 94%. This stack's value is on-disk artifact discipline, not external system reach. Most general-purpose MCP servers add little. [03 §5, §6]

**N2. Don't run full ultraplan/ultrareview as a CI gate on every PR.** Cost-prohibitive for a research/design stack, and methodologically suspect when the repo is itself an adversarial-review stack. [12 §11]

**N3. Don't add embeddings + vector search to canon/corpus yet.** Break-even is roughly when the corpus index stops fitting in Opus 4.7's 1M context budget for the librarian. Until then, embeddings add infrastructure and re-indexing cost without solving a real problem. When you cross the threshold, `sqlite-vec` co-located beats a dedicated store. [11 §8]

**N4. Don't enable `auto` permission mode for the orchestrator.** Too many workflow actions need explicit artifact confirmation. [01 §1.16]

**N5. Don't run the 12-step workflow headless** (except for narrow batch-grading historical decisions). The workflow's value depends on a human reading synthesis. [12 §10]

**N6. Don't use a daemon process for diagnostics.** JSONL append + DuckDB on demand is the right shape at this scale. Daemons add operational complexity for a single-developer stack. [Confirmed in this session's diagnostics design.]

**N7. Don't share `.env` / `DATABASE_URL` across worktrees.** The single biggest "silently broken" mode at 10 worktrees. [08 §3.2]

**N8. Don't trust LLM-self-reported confidence without external calibration.** Self-reported confidence is poorly calibrated and gets *worse* under sycophantic pressure. Use external signals (consistency across samples, agreement with another model, schema validation). The `Confidence:` field added in this session is useful *only* once it's measured against the calibration set (#7 above). [05 §8]

**N9. Don't put expert-persona priming in CLAUDE.md.** "You are a world-class X" damages factual accuracy on knowledge tasks (Wharton 2025 finding). State the role and stance; don't stack expertise adjectives. [05 §2.2]

**N10. Don't run unaudited community MCP servers with write scopes.** 5.5% of public MCP servers carry poisoned metadata (Invariant Labs measurement). The 2025-2026 incident list includes CVE-2025-49596, GitHub MCP heist (May 2025), postmark-mcp backdoor (Sep 2025), Anthropic Git MCP RCE chain (Dec 2025). [03 §3 Security; 09 §1]

---

## 4. Cross-cutting themes

Six patterns appear across multiple research reports as load-bearing — they're worth internalizing as principles, not just rules.

**T1. Hooks for invariants, MCP for stateful integrations, custom tools for project-local knowledge.** Anthropic's own decomposition. The temptation to reach for MCP-as-default fights it. [02 Q3; 03 §1]

**T2. Distillation as a discipline, not an optimization.** The orchestrator reading distillations rather than raw subagent output is what makes context-engineering work at the workflow level. You already enforce this at step 6 of the 12-step workflow. Don't relax it. [02 §3; 05 §1.4, §1.5; 11 §1]

**T3. Verification before completion.** Anthropic's *single highest-leverage* recommendation. Apply it to markdown deliverables the same way you'd apply it to code: schema-conformance check on artifacts, citation-existence check, cross-artifact consistency check. The `path-check` and `ledger-render` skills are the start; `synthesis-lint` is the missing piece. [02 §4a-c; 13 §4, §9.1]

**T4. Cost circuit breakers everywhere.** Every headless invocation. Every parallel worktree. Every scheduled Routine. The runaway cases in the literature all share one factor: no breaker. *"There is no circuit breaker. The first signal is the invoice."* [12 §9]

**T5. Cross-model verification for high-stakes review.** The model that wrote the candidate should not be the only one reviewing it. The `SHADOW_PANEL=1` triangulation is the design-review form; `EXTERNAL_SHADOW=1` extends to cross-family. The same principle applies to evals — disjoint judge families correct correlated biases. [04 §3f; 06 §4, §10 #8]

**T6. Length matters at the top, not in aggregate.** A 30k-token CLAUDE.md or system prompt is fine if it's all cached and ordered by priority (identity → principles → rules → bypasses). What kills adherence is buried instructions, not byte count. [05 §2.6; 10 §3]

---

## 5. What the research validated that you already do well

Don't undo these. Several of them are industry-leading.

- **The 12-step workflow as an evaluator-optimizer + orchestrator-worker composition.** Industry literature (Anthropic *Building Effective Agents*, Spring AI's taxonomy mirror) treats this as the right shape. You did it before the taxonomy crystallized. [04 §1; 02 §1]
- **File-artifact-driven shared state.** Anthropic's *Effective Context Engineering* explicitly recommends this as *the* pattern. [02 §3, Q2]
- **Distillation between step 6 and downstream steps.** Sub-agent context isolation is the canonical context-engineering primitive. [05 §1.5]
- **Frame-challenger as a hard gate before generator.** Pre-empts the eval-awareness pathology where the generator polishes for the rubric. [04 §3a; 06 §8]
- **Minority-veto critic panel.** PoLL (Panel of LLm-evaluators) literature catching up; veto bias toward type-I caution is the right bias for irreversible design commits. [04 §3c]
- **`SHADOW_PANEL=1` triangulation.** Diversity-of-thought debate literature validates this. The "voice not vote" framing is more disciplined than naive multi-agent debate. [04 §3e]
- **`canon-librarian` contradiction-required rule.** Industry-leading anti-confirmation discipline. Worth documenting as a transferable pattern. [11 §8]
- **`upgrades/` lab as a creative-ideas surface separate from session artifacts.** Aligns with the "creative + working" decomposition in mature R&D shops. [Inferred from memory + session usage; not directly in the research but consistent with its themes.]
- **Path discipline rule** (no absolute paths in artifacts). Privacy + portability + grep-discoverability. Hook promotion makes it 100% reliable. [10 §10 #10]

---

## 6. Where the research reports live (for deep-dive)

The 13 reports under [research/sota-2026/](research/sota-2026/) total ~52,000 words. Pointers by question:

| If you want to know about… | Read |
|---|---|
| Every Claude Code primitive + what's new in 2026 | [01-claude-code-platform.md](research/sota-2026/01-claude-code-platform.md) |
| What Anthropic explicitly recommends (verbatim quotes) | [02-anthropic-best-practices.md](research/sota-2026/02-anthropic-best-practices.md) |
| Model Context Protocol + supply-chain security | [03-mcp-ecosystem.md](research/sota-2026/03-mcp-ecosystem.md) |
| Multi-agent patterns (what works, what fails) | [04-multi-agent-patterns.md](research/sota-2026/04-multi-agent-patterns.md) |
| Context engineering + Opus 4.7 specifics + prompt caching | [05-context-prompt-engineering.md](research/sota-2026/05-context-prompt-engineering.md) |
| Evals, calibration, agent-as-judge, eval-aware models | [06-evals-testing.md](research/sota-2026/06-evals-testing.md) |
| What Aider/Cursor/Cline/etc. do that's worth borrowing | [07-ai-dev-ecosystem.md](research/sota-2026/07-ai-dev-ecosystem.md) |
| **Parallel worktrees — operational reality** | **[08-parallel-worktrees.md](research/sota-2026/08-parallel-worktrees.md)** |
| Prompt injection 2026 + safety/guardrails | [09-safety-guardrails.md](research/sota-2026/09-safety-guardrails.md) |
| CLAUDE.md / AGENTS.md / project-instruction file SOTA | [10-claude-md-agents-md.md](research/sota-2026/10-claude-md-agents-md.md) |
| Memory taxonomy + RAG 2026 + canon-librarian context | [11-memory-rag.md](research/sota-2026/11-memory-rag.md) |
| Headless Claude + Routines + CI patterns + cost | [12-ci-automation.md](research/sota-2026/12-ci-automation.md) |
| Verification-before-completion + TDD + spec-driven dev | [13-testing-tdd-spec.md](research/sota-2026/13-testing-tdd-spec.md) |

---

## 7. Recommended order of operations

Given the user's explicit priority — "10 worktrees soon, don't waste 10 sessions" — the path is:

**Week 1.**
1. Execute the §1.3 pre-launch checklist.
2. Land Tier 1 upgrades (#1-6 in §2) — trim CLAUDE.md, wire `EXTERNAL_SHADOW=1`, cache hit tracking, model version pinning, path-discipline-as-hook, safety deny rules.
3. Test on 2-worktree dry run.

**Week 2.**
4. Land Tier 2 upgrades (#7-12) — calibration set, self-review pass, untrusted-content tagging, scoped rules, sessions-index.
5. Test on 5-worktree run.

**Week 3+.**
6. Launch 10-worktree batch.
7. Land Tier 3 upgrades (#13-20) as the 10-worktree work surfaces gaps.

**Standing.**
- Run the nightly cross-session diagnostics Routine.
- Re-read this synthesis quarterly; re-baseline as Anthropic ships new primitives.

---

## 8. Honest assessment

The stack is in good shape. The diagnostics work just landed addresses the worst gap (no per-agent telemetry). The pre-launch worktree checklist is straightforward and well-documented in the research. Tier 1 upgrades are all small surgical edits. The calibration set is the one item that requires sustained effort (curating 20 historical sessions with human verdicts is a few hours of focused work).

The biggest *epistemic* risk: this entire synthesis was produced by Claude reading research produced by Claude. The same family-correlation problem that motivates `EXTERNAL_SHADOW=1` for the critic panel applies to this document. The cheapest mitigation: when you get to Tier 1 #2 (wire up external shadow), feed this document through the external lane and see what it catches. If nothing, the synthesis is probably sound. If something material, that's the signal to take seriously.

Final word: **the structure already exists; the work is sharpening it, not rebuilding.** Most of the recommendations above are 1-50 line additions. The expensive items (calibration set, EXTERNAL_SHADOW wrapper, daemon-mode orchestration) are one each, optional, and earn their keep when you cross a specific threshold. Until then, the existing artifact discipline + the diagnostics infrastructure that just landed + the pre-launch checklist + Tier 1 are sufficient for the 10-worktree milestone.
