# Master Synthesis — SOTA 2026 AI Workflow Setup (General)

**The canonical 2026 reference on building production AI workflows with Claude Code.**

Vintage: 2026-05-17. Source: 15 deep-dive research reports under [research/sota-2026-v2/](research/sota-2026-v2/), totaling ~78,000 words of citation-heavy investigation, all general (no worktree content — that's covered separately). Each recommendation pointers to its source report.

This document answers: *what does an ideal 2026 AI workflow setup look like, and what should every advanced practitioner do?*

---

## 0. The headline thesis

**An SOTA 2026 AI workflow is built on six load-bearing primitives:**

1. **Context engineering** beats prompt engineering. Every token spends an attention budget that degrades with length. Compaction + structured note-taking + sub-agent isolation are the discipline. [04]
2. **Verification before completion** is the single highest-leverage practice (Anthropic's own words). The agent's narration is fiction; the diff/test/lint output is fact. [13, 02]
3. **Tool definitions are prompt engineering.** Bad tool descriptions send agents down wrong paths. Tool sets bloat fast — the #1 named anti-pattern in *Effective Context Engineering*. [05]
4. **File-as-memory + sub-agent context isolation** = the recommended Anthropic pattern for any workflow >3 steps. Don't carry intermediate state in conversation; persist to disk and read back. [04, 07]
5. **Eval-driven development** is now table stakes. *"Production AI without evals is unmaintainable."* Anthropic's recipe: 20 queries, single-call LLM judge, 0.0–1.0 + pass/fail. [08]
6. **Hooks for invariants, MCP for stateful integrations, CLI tools for context-efficient external services.** The decision rule is explicit in Claude Code best-practices. [01, 11]

**Six anti-patterns kill more workflows than any other:**
1. CLAUDE.md bloat — past ~150 instructions, Claude follows only the first ones. [14]
2. Bloated tool sets / ambiguous tool selection. [05]
3. Same-family critic panels (all Opus, no triangulation) — correlated bias documented across multiple arXiv papers. [09]
4. No cost circuit breaker — the $47K/$30K/$87K runaway loops all share this missing primitive. [15]
5. Trust-then-verify gap — agent says "tests pass," nobody re-ran. [02, 13]
6. Treating long context as a panacea — middle-of-haystack still degrades at 1M tokens. [04, 07]

---

## 1. The complete 2026 SOTA stack (everything an advanced practitioner should set up)

Organized by the six load-bearing primitives above. Each item has a citation to the deep-dive report. **Items marked "[M]" are must-haves for any serious 2026 workflow; "[S]" should-haves; "[C]" could-haves for advanced use.**

### 1.1 Context engineering [04]

- **[M] Sub-agent context isolation.** Verbose operations (test runs, log scrapes, doc fetches, file walks) belong inside sub-agents. The orchestrator reads only condensed 1-2k-token summaries. Anthropic's #1 recommended context-engineering primitive.
- **[M] Compaction with recall-first-then-precision discipline.** When approaching context limit, summarize aggressively but tune for recall first (preserve decisions, names, constraints, anomalies). Hook `PreCompact` to inject load-bearing state; `PostCompact` to re-bootstrap.
- **[M] Structured note-taking (agent's external memory).** One artifact per workflow phase, named for the phase. The agent reads back from disk, not from conversation. Cline's "memory bank" pattern is the concrete example.
- **[S] Just-in-time context loading.** Pass lightweight identifiers (file paths, query handles, URLs); resolve only when needed. The 2026 default replacing eager pre-loading.
- **[S] Tool-result wrapping** in untrusted-content envelopes. Also a safety pattern — prevents indirect prompt injection through tool output.
- **[S] Length-bounding tool results.** Cap at write time, spill to file; lift-and-summarize on read.
- **[M] Cache breakpoints layered four ways:** tool definitions → system prompt → static context → conversation tail. Track cache hit rate as a first-class operational metric. The silent killers: timestamps/IDs before breakpoints, thinking-mode switches invalidating message cache.

### 1.2 Verification before completion [13, 02]

- **[M] Diff-before-claim.** After any agent says "I did X," run `git diff` and confirm X is in it. Agents narrate intended actions interchangeably with completed ones. The single most useful 2026 verification habit.
- **[M] Test command output, this turn.** Never claim "tests pass" from a prior run, an extrapolation, or an agent's report. Run the command in the current message.
- **[M] Build + lint + type check minimum** as gates before any "done" claim.
- **[S] Test-first, then commit the test, then implement.** The committed test is the agent's only safety against test-rewriting. Anthropic's published TDD recipe.
- **[S] Property + example testing.** One example for documentation, one property for coverage. Combined detection ~80% vs ~70% individual (arXiv 2506.18315).
- **[S] Mutation testing as the coverage check.** Line coverage is decorative. Mutation score is load-bearing. Stryker (JS), Mutmut (Python), PIT (Java). Recommended thresholds: 70% critical, 50% standard, 30% experimental. Feed surviving mutants back to the agent.
- **[C] Spec-as-source.** GitHub Spec-Kit (`/specify`, `/plan`, `/tasks`) or Kiro (AWS) for high-stakes work. README-driven development as the lightweight version. EARS notation for acceptance criteria.
- **[S] Output-shape schema validation.** Every structured agent output passes through Pydantic/Zod/JSON Schema before consumption. Retry on validation failure.
- **[M] Citation existence checks.** Every `[link](path)` an agent emits must resolve. Cheap mechanical verifier; catches the "convincing-but-fake citation" class.
- **[C] Golden dataset + semantic similarity for LLM-call regression.** Snapshot tests don't survive stochasticity. Embeddings + threshold (≥0.95 cosine) do.
- **[S] Cross-model verification for high-stakes review.** The model that wrote the code should not be the only one reviewing it.

### 1.3 Tool design [05]

- **[M] Treat every tool description as load-bearing prompt engineering.** Include example usage, edge cases, input format requirements, clear boundaries.
- **[M] Use the decision rule: hook = deterministic must-happen, MCP = reusable across hosts + stateful + external auth, custom tool = project-local artifact-aware.**
- **[M] Tool naming: verb-noun, namespaced when multiple sources exist.** `github_search` not `search` if you also have `notion_search`. Treat namespaces as load-bearing.
- **[S] Parameter design: minimize required, use enums sparingly, reserve open `notes` field for caveats.** A 20-value enum that excludes the right answer pushes the model to a wrong neighbor.
- **[M] Avoid bloated tool sets.** Cloudflare's "Code Mode" pattern (collapse N MCP servers behind `search` + `execute` pair) cut token cost 94%. Apply at scale.
- **[M] Wrap tool results in untrusted-data envelopes.** Escape model-control tokens (`</tool_result>`, `<|im_end|>`). Length-bound. Content-type tag.
- **[S] Tool error reporting:** use `isError: true` for failures the model should reason about; JSON-RPC errors for infrastructure failures the host surfaces.

### 1.4 Memory + RAG + long context [07]

- **[M] File-as-memory with consent-gated writes.** Every meaningful state is a file. The model proposes edits; user (or workflow step) commits. This stack already does this; it's the right answer.
- **[S] Provenance for everything retrieved.** `(doc_id, chunk_id, char_offset, retrieval_score, rerank_score)` on every span. Repo-relative markdown links serve the same purpose for file-as-memory.
- **[M] Don't add embeddings + vector search until your corpus stops fitting in 1M context.** Past ~500 entries: `sqlite-vec` co-located with markdown files, BM25 + dense hybrid, contextual retrieval (LLM-generated chunk prefixes — 49% retrieval-failure reduction per Anthropic Sep 2024).
- **[S] Contextual retrieval when you do go to RAG.** Highest single ROI on retrieval quality.
- **[S] Hybrid BM25 + dense + rerank.** The 2026 production default. Reranking alone often doubles useful-precision-at-5.
- **[S] Parent-document retrieval.** Index small chunks, return the parent doc or wider window. Mitigates chunk-boundary failures.
- **[C] Recency/decay metadata on long-term memory.** `last_referenced_at` + periodic review. Closes the staleness gap.
- **[S] Anti-confirmation discipline in retrieval, not just synthesis.** Mandate that the retriever return at least one contradicting passage. Cosine similarity selects *for* agreement; this is a structural counter.
- **[M] Voyage embeddings if you're on Anthropic; pgvector if you're on Postgres; sqlite-vec if you're embedded.** The 2026 defaults; deviation requires measured reason.
- **[M] Treat 1M context as a budget, not a solution.** Effective context for multi-needle workloads is 200-400K (Opus 4.7: 89% single-needle vs 56% 8-needle). Hierarchical summarization past ~300K tokens.

### 1.5 Eval-driven development [08]

- **[M] Start at n=20 queries from real failures.** Anthropic's recipe. Single-call LLM judge with 0.0–1.0 + pass/fail is the most consistent grading shape. Don't wait for a benchmark suite.
- **[M] Build a golden dataset with the four-D heuristic:** demonstrative, diverse, decontaminated, dynamic.
- **[M] Pin model versions per session.** `claude-opus-4-7-YYYYMMDD` not `claude-opus-4-7`. Aliases roll forward silently — the April 23 postmortem documents exactly how silent model defaults caused weeks of degraded behavior.
- **[S] Eval drift detection.** Production-vs-eval-set distribution comparison. Refresh the eval set quarterly from production samples.
- **[S] Red-team-to-eval flywheel.** Every successful jailbreak becomes a permanent regression test. Tools: promptfoo (declarative, CI-friendly), garak (NVIDIA, 37+ probes), PyRIT (Microsoft).
- **[S] Property-based testing on output shape.** JSON schema validation, length bounds, refusal-vs-over-refusal symmetry.
- **[S] Cross-family judge triangulation.** Same-family panels inherit family-correlated bias (arXiv 2410.21819, 2508.06709). Disjoint families correct the bias; same family just averages noise.
- **[C] Calibration metrics tracked over time:** ECE (drift monitoring), Brier (judge selection), MCE (high-confidence-gated actions). Judges show ECE 0.12–0.40 even at best.
- **[M] Reproducibility:** N-run determinism tests (median + IQR); temperature 0 is NOT deterministic (Thinking Machines Lab Sep 2025).
- **[C] Eval platform when scale warrants:** Langfuse (OSS, ClickHouse, self-host in 30 min), Braintrust (CI/CD-first), promptfoo (code-defined evals).

### 1.6 Critic panels [09]

- **[M] Multi-model panel beats single-model self-review.** Correlated-error literature is unambiguous. The Anthropic stack's three-lens panel is the right shape.
- **[M] Aggregation rule chosen for the decision class:** minority-veto for irreversible commits (biases toward type-I caution); majority-vote for reversible.
- **[M] Cross-family triangulation for high-stakes work.** Same-family panels over-approve own-family outputs. Add a different-family lane as triangulation signal.
- **[S] "Voice not vote" framing for shadow lanes.** Disagreement is information, not a tie-breaker.
- **[S] Petri-style judge with branching/rollback authority** for high-stakes reviews. Critics that can request clarification before voting catch more defects than one-shot review.
- **[S] Realism classifier on the generator's context.** If the generator knows the critic-panel is coming, it polishes for the rubric — the eval-awareness pathology Opus 4.7 §6.5.2.2 documented. Phrase the candidate as working task, not "this will be reviewed."
- **[S] Structured `Verdict: <enum>` + `Confidence: <float>` line** as part of every critic output. Parseable; enables calibration tracking over time.
- **[S] Build a calibration set** (20-50 candidates with human-labeled per-lens verdicts). Without it, critic prompt edits are blind.
- **[C] Jury-on-demand variant** for cost optimization: run one lens first; fan out only on uncertain cases.

### 1.7 Safety + guardrails [10]

- **[M] OWASP LLM Top 10 awareness.** Prompt injection has been #1 for three lists running. Channel-level vulnerability — mitigations reduce but do not eliminate.
- **[M] The Lethal Trifecta heuristic** (Willison): private data + untrusted content + external comm = vulnerable. Break any leg to collapse the attack class.
- **[M] Three deny rules in `.claude/settings.json`:**
  - `deny: ["Read(**/.env*)", "Read(**/.aws/**)", "Read(**/.ssh/**)", "Read(**/id_rsa*)", "Read(**/.netrc)"]`
  - `deny: ["Bash(rm:*)", "Bash(git push --force:*)", "Bash(git reset --hard:*)", "Bash(sudo:*)"]`
  - `ask: ["WebFetch", "Bash(curl:*)", "Bash(wget:*)", "Bash(gh api:*)"]`
- **[M] Sandbox for any Bash that touches untrusted code.** Claude Code's native sandboxing (Seatbelt macOS, bubblewrap Linux) is the first-party path. gVisor or Firecracker for higher-isolation needs.
- **[S] Wrap fetched web content in `<untrusted-source url="..." fetched-at="...">` envelopes** before any agent reads. Web fetches are the dominant production-exploited injection channel in 2025-2026.
- **[S] PreToolUse hook scanning for secret patterns** before any string flows to Bash/Write/WebFetch.
- **[M] Output classifier on the response side.** Anthropic's harm classifier runs separately; Llama Guard 3/4 or ShieldGemma 2 as OSS analogues.
- **[M] Stop-reason classification.** Claude 4 added `refusal` as first-class. Stop pattern-matching on "I'm sorry, I can't."
- **[M] Egress allowlist for network tools.** WebFetch domain restrictions; wrap curl/wget behind specific-host wrapper scripts.
- **[C] Auth: OAuth 2.1 + PKCE for remote MCP (mandatory per spec); never plaintext API keys in client configs.**
- **[M] Audit log: every tool invocation. Session id, tool, full args, return status, latency. Append-only, separate trust domain from the agent.**

### 1.8 Project-instruction files (CLAUDE.md / AGENTS.md) [14]

- **[M] Target 80-120 lines of body, hard cap 200.** Past ~150 instructions, frontier LLMs follow only the first ones. Claude Code's system prompt already uses ~50.
- **[M] Apply the "would Claude make a mistake without this line" test ruthlessly. If no, delete.**
- **[M] Behavioral > factual.** Things that change how Claude thinks beat things Claude could read from code. Karpathy's 65-line CLAUDE.md is the canonical small-is-correct example.
- **[M] Never duplicate the linter.** If a tool enforces it deterministically, don't write prose about it. Mention the tool, not the rule.
- **[S] Use layered files for scoped rules.** Subdir `CLAUDE.md`, `.claude/rules/<scope>.md` with `paths:` frontmatter for glob-scoped activation. Pay token cost only when rule is relevant.
- **[S] `@`-imports sparingly; prefer prose pointers + lazy `Read`.** Eager `@` loads on every turn; lazy `Read` loads on demand.
- **[S] Audit the full context loadout, not just CLAUDE.md.** MCP tool descriptions, skills, hooks, agent system prompts all compete for the ~150-instruction budget.
- **[S] Commit project files; gitignore personal.** `CLAUDE.md` and `AGENTS.md` reviewed in PR. `CLAUDE.local.md` per-developer.
- **[C] Lint the context file itself.** Tools like cclint catch broken `@`-imports, stale references, over-length files.
- **[M] Promote deterministic constraints to hooks.** CLAUDE.md is ~80% reliable; hooks are 100%. Cost of a 20% miss matters for security, formatting, paths.
- **[C] AGENTS.md as canonical, symlink CLAUDE.md to it** for cross-tool teams. 60,000+ projects adopted; read natively by 18+ agents. Claude Code doesn't read it natively yet; symlink or `@AGENTS.md` import.
- **[M] The five-section template:** project orientation (3-5 lines), commands (5-15 lines), architecture map (5-15 lines), hard rules and invariants (10-30 lines), pointers to deeper docs (5-15 lines). Body budget 30-80 lines.

### 1.9 Claude Code platform features (every advanced user should know) [01]

- **[M] Skills (`.claude/skills/<name>/SKILL.md`)** — packaged procedural knowledge; descriptions load at session start (1% context budget); bodies load only when invoked. Replace custom slash commands. Use `paths:` for glob-scoped auto-load.
- **[M] Subagents (`.claude/agents/<name>.md`)** — separate context window, model, permissions, tools. Use `model: haiku` for distillation/search work; `model: opus` for reasoning. `isolation: worktree` for filesystem-touching work.
- **[M] Hooks (29 events as of 2026)** — deterministic enforcement at every lifecycle moment. `PreToolUse` can modify tool input or block. `PostToolBatch` gates the agentic loop. `SessionStart`, `SessionEnd`, `WorktreeCreate`, `PreCompact`/`PostCompact` for state management.
- **[M] Plan mode + `opusplan`** — Opus designs, Sonnet executes, human reviews plan before code moves. `Shift+Tab` cycles permission mode. `Ctrl+G` opens plan in `$EDITOR`. `opusplan` keeps 200K cap in plan phase (no 1M auto-upgrade).
- **[M] Auto-memory** — Claude takes notes from corrections automatically (`~/.claude/projects/<repo>/memory/MEMORY.md`). First 200 lines load every session. Toggle via `/memory`. Requires v2.1.59+.
- **[S] `.claude/rules/` with `paths:` frontmatter** — modular instructions that only enter context when matching files are touched. Scales the project-instruction surface without growing CLAUDE.md.
- **[S] Agent view (`claude agents`)** — TUI control plane for all background sessions; supervisor process survives terminal closure. Research preview (v2.1.139+).
- **[S] Sandboxing (`sandbox.*` settings)** — OS-level filesystem + network isolation for Bash and all its children. Anthropic's own framing: *"Sandboxing safely reduces permission prompts by 84%."*
- **[S] Plugins + marketplaces** — version, share, update the whole `.claude/` bundle as one unit. Namespaced skills prevent conflict.
- **[S] OpenTelemetry export** — `CLAUDE_CODE_ENABLE_TELEMETRY=1`. GenAI-conventions metrics + logs for cost, latency, behavior across the org.
- **[S] `/loop` self-paced + Monitor tool** — poll a deploy or PR with model-chosen intervals; can switch to streamed line-by-line monitoring instead of polling.
- **[S] Keybindings (`~/.claude/keybindings.json`)** — every chat-input action rebindable per-context, chord support, live reload. v2.1.18+.
- **[S] Headless `claude -p` + `--bare`** — script Claude into CI, pre-commit hooks, automation. `--bare` skips auto-discovery of hooks/skills/plugins/MCP for reproducibility.
- **[S] Output styles** — built-ins (Default, Proactive, Explanatory, Learning) or custom. Build a custom style matching your house tone.
- **[C] Channels** — make MCP push *to* you (Telegram/Discord/iMessage). Includes permission relay.
- **[M] Pin Opus 4.7 specifics:** `xhigh` is the new default effort tier. 1M context auto-upgraded on Max/Team/Enterprise. Adaptive thinking is the ONLY mode (rejects manual budgets). Default model flipped April 23 2026.

### 1.10 MCP usage [11]

- **[M] Decision rule: hook for deterministic must-happen, custom tool for project-local, MCP for cross-host stateful integration.** Don't reach for MCP by default — every server inflates system prompt with tool descriptions.
- **[M] Use Streamable HTTP, not stdio, for any MCP server you'll run from multiple Claude Code instances.** Stdio is single-client; Streamable HTTP scales.
- **[M] Pin MCP server versions.** The "rug pull" attack (tool descriptions change mid-session) is permitted by the spec. Audit on install + pin + sandbox.
- **[M] OAuth 2.1 + PKCE for any remote MCP server.** Spec-mandated. Never plaintext API keys in `.mcp.json` (leaked in every "I shared my Claude config" incident).
- **[S] Apply Cloudflare's "Code Mode" pattern** when you have many MCP servers — collapse N servers behind `search` + `execute` pair. Cut token cost 94%.
- **[M] 5.5% of public MCP servers carry poisoned metadata** (Invariant Labs measurement). Audit community servers before install. Pin version. Sandbox the process.
- **[M] Never trust resource contents.** Documents fetched via Fetch MCP, GitHub issues read via GitHub MCP, Slack messages read via Slack MCP — all are untrusted input even if the *server* is trusted.
- **[C] Avoid building a custom MCP server** when the cost is small N projects benefit. Build a custom tool or hook instead.
- **[S] Top vendor-official MCPs worth knowing in 2026:** GitHub, Sentry, Stripe, Linear, Notion, Slack, Cloudflare (13 servers), Atlassian, HubSpot, Neon, Vercel, Supabase. Top community: Playwright, Firecrawl, Brave Search, Qdrant.

### 1.11 Headless / CI / cost optimization [15]

- **[M] Cost circuit breaker on every headless invocation.** Parse `cost_usd` from `--output-format json`. Fail the job above threshold. Per-session timeout. Per-session retry limit. Highest leverage because it prevents the only failure mode that produces invoices instead of bug reports.
- **[M] `--bare` for any CI-side run.** Skips auto-discovery; guarantees reproducibility across contributor `~/.claude/` configs.
- **[M] Tool restriction:** `--allowed-tools` (positive) + `--disallowed-tools` (hard no). Combine both. Never rely on deny rules alone — adversa.ai documented bypass when commands have >50 subcommands.
- **[M] Prompt caching for CLAUDE.md + system prompts.** 90% savings on cached tokens. Cache writes 1.25× (5m TTL) or 2× (1h TTL); reads 0.1×. One published case study: $80/month → $24/month (70% cut) by moving to Haiku-heavy routing with prompt caching.
- **[M] Model tiering:** 70-80% of production queries can run on Haiku ($1/$5 per MTok). Reserve Opus 4.7 1M-context tier ($15/$75) for genuinely cross-cutting work.
- **[M] Cheap classifier → expensive worker routing pattern.** Haiku call classifies task (trivial/standard/hard) → Sonnet for standard → Opus for hard. Most reliable cost-management pattern.
- **[S] Anthropic Batch API for bulk inference.** 50% discount. Use for eval runs, document classification at scale. Latency: minutes to hours; not interactive.
- **[S] Scheduled Routines (April 14 2026)** for cron-style automation. Three triggers: cron, HTTP POST, GitHub webhooks. Six resilient-prompt rules: state exit condition, cap the work, pre-declare artifact paths, forbid destructive ops, emit structured terminal artifact, idempotency.
- **[S] "Guardian" Routine pattern** — separate routine reads cost log, pages human if any single routine exceeds N× its 30-day median.
- **[M] GitHub Actions integration via `anthropics/claude-code-action`** — first-party. PRs + issues. Auth: Anthropic direct + Bedrock + Vertex + Foundry.
- **[M] AI code review tier — pick one:** CodeRabbit ($24/dev/month, 2M+ repos, most mature); Greptile (RAG-based, 82% bug catch vs CodeRabbit 44% but 11 FPs vs 2); Ellipsis (large-PR + fixes); GitHub Copilot PR review (free, weakest); Anthropic claude-code-security-review (security-focused).
- **[M] OpenTelemetry observability.** GenAI semantic conventions. Cost, latency, token, cache-hit rate per session.
- **[M] Cap `max_turns` in headless invocations.** The agent doesn't know when to stop unless told.
- **[M] Awareness: June 15 2026 subscription split.** Headless usage moves from interactive pool to separate Agent SDK credit allotment.

### 1.12 AI-assisted dev workflow patterns to know [12]

These are patterns observed across the major tools (Aider, Cursor, Cline, Codex, Goose, etc.) — worth knowing as practitioner vocabulary even if you don't adopt the source tool.

- **[S] Plan mode** — separate read-and-think from write-and-execute, gate explicitly. (Cline, Plandex, Cursor, Claude Code).
- **[S] Context providers as named primitives** — `@`-mentions for explicit context loading (Continue).
- **[S] Rules files** — scoped instructions activated by file patterns. (`.cursor/rules/*.mdc`, `.clinerules/`, `.claude/rules/`).
- **[S] Checkpoint/undo** — shadow git, edit history, diff sandbox. (Cline shadow git, Cursor edit history, Plandex diff sandbox).
- **[S] Git-commit-per-edit** — every accepted edit becomes a commit. Audit trail. (Aider's signature).
- **[S] MCP as tool surface** — converging standard across Cline, Continue, Goose, Codex, Cursor.
- **[S] Self-correction loop** — agent re-reads output as critic, fixes own-goals before human sees it. (Devin self-reviewing PRs, Copilot review→fix, Plandex auto-debug).
- **[C] Plan-branches** — emit multiple candidates from multiple frames in parallel; evaluate both before picking. (Plandex).
- **[C] Architect/editor role split** — strong reasoner produces skeleton, cheap model fills in citations. (Aider's architect mode).
- **[C] Code-graph-aware retrieval** — definitions, references, types as structural signal beyond cosine similarity. (Sourcegraph Cody).
- **[C] Persisted goal with /resume** — sessions as resumable units of work. (Codex `/goal`).
- **[C] Daemon-mode orchestration** — agent runs as daemon; multiple clients can attach. (OpenCode).

---

## 2. Ranked top 20 practices by leverage (the "if you do nothing else" list)

For any 2026 AI-workflow practitioner serious about Claude Code, ranked by impact-per-effort:

1. **Verification before completion** — *Anthropic's single highest-leverage practice.* Test command output this turn; diff-before-claim; never trust agent narration. [13, 02]
2. **Trim CLAUDE.md to 80-120 lines body** — past ~150 instructions, Claude follows only the first ones. [14]
3. **Cost circuit breaker on every headless invocation** — parse `cost_usd`, fail above threshold. The only failure mode that produces invoices instead of bug reports. [15]
4. **Sub-agent context isolation for verbose work** — search/exploration/log-spelunking belongs in subagents. The orchestrator reads 1-2k-token summaries only. [01, 04]
5. **Three deny rules in settings.json** — dotfile + credential paths, destructive ops, network egress prompts. [10]
6. **Pin model versions per session in ledger/audit** — `claude-opus-4-7-YYYYMMDD` not `claude-opus-4-7`. April 23 postmortem documents why. [08]
7. **Prompt caching with 4-breakpoint layering** — tool defs → system prompt → static context → conversation tail. 90% savings on cached tokens. Track cache hit rate. [04, 15]
8. **Build a 20-item golden eval set from real failures** — Anthropic's recipe; single LLM call judge with 0.0–1.0 + pass/fail. [08]
9. **Promote path-discipline / format invariants from CLAUDE.md prose to PreToolUse hook** — 100% reliable vs ~80%. [01, 14]
10. **Sandbox Bash that touches untrusted code** — Anthropic's own claim: 84% reduction in permission prompts. [01, 10]
11. **Untrusted-content tagging on every external fetch** — wrap web/MCP/file content in `<untrusted-source>` envelopes. Web is the dominant injection channel 2025-2026. [10]
12. **Anti-confirmation discipline in retrieval** — mandate at least one contradicting passage. Industry-leading pattern (most RAG selects *for* agreement). [07]
13. **Cross-family judge triangulation for high-stakes review** — same-family panels inherit family-correlated bias. [09]
14. **Pin Haiku on distillation/search subagents; Opus on critic lenses; Sonnet on retrieval** — model tiering saves 70-80% on typical loads. [01, 15]
15. **AI code review on every PR** — pick one (CodeRabbit, Greptile, Anthropic security review). Cost ~$24/dev/month. [15]
16. **OpenTelemetry export to Prometheus + Grafana** — cost, latency, cache hit rate per session. Only way to validate any optimization. [01, 15]
17. **Schedule cron-style work as Routines, not in-session loops** — survives machine sleep, scaled by Anthropic. [01, 15]
18. **Visual iteration for any UI work** — Claude in Chrome extension. Anthropic's published pattern. [02, 13]
19. **Headless `--bare` for CI** — guarantees reproducibility across contributor `~/.claude/` configs. [01, 15]
20. **Glob-scoped instruction files (`.claude/rules/<scope>.md`)** — partition CLAUDE.md content; pay token cost only when scope-relevant. [01, 14]

---

## 3. The complete anti-pattern catalogue (do NOT do)

Cross-referenced from all 15 reports. Each anti-pattern is named at least once in the research; cited where it's load-bearing.

### Architecture / agents

- **AP1.** Adding complexity without demonstrated outcome improvement (Anthropic's #1 named anti-pattern). [02 §1.1]
- **AP2.** Vague orchestrator/subagent instructions. [02 §1.2]
- **AP3.** Network/mesh agent topology — debugging disaster. [06]
- **AP4.** Naive multi-agent debate as primary verdict mechanism — expensive + correlated bias. [06, 09]
- **AP5.** Hierarchical-of-hierarchical (supervisors of supervisors) below N≈6 specialists. [06]
- **AP6.** Reaching for multi-agent when prompt chaining or routing would suffice. [02, 06]
- **AP7.** Same-family critic panel without cross-family triangulation. [04, 09]
- **AP8.** Self-consistency over a single judge as a "panel" substitute. [09]

### Context engineering

- **AP9.** Bloated tool sets covering too much functionality (Anthropic's #1 named anti-pattern in context engineering). [04, 05]
- **AP10.** Over-aggressive compaction losing critical context. [04]
- **AP11.** Stuffing edge cases into prompts as brittle hardcoded logic. [04]
- **AP12.** Vague high-level guidance lacking concrete signals. [04]
- **AP13.** Pre-loading "in case the model needs it" — the 2025-2026 anti-pattern. [04]
- **AP14.** Cache breakpoint on per-request varying content. [04, 15]
- **AP15.** Treating long context as a panacea — middle-of-haystack still degrades. [04, 07]
- **AP16.** Treating sub-agent returns as gospel without distillation. [04]

### CLAUDE.md / project instructions

- **AP17.** Bloated CLAUDE.md — past ~150 instructions, model ignores actual instructions. [02, 14]
- **AP18.** Encoding style in prose when the linter enforces it ("never send an LLM to do a linter's job"). [14]
- **AP19.** Stale architecture descriptions that drift from code. [14]
- **AP20.** Listing every dependency / recapitulating README. [14]
- **AP21.** Cargo-culting structure from famous CLAUDE.md without justifying per-section against actual failure modes. [14]
- **AP22.** Treating CLAUDE.md as a runbook (long procedures belong in `@`-imported runbooks / skills). [14]
- **AP23.** No bypass clause (workflow rules with no escape hatch). [14]

### Prompts / model usage

- **AP24.** Few-shot examples that leak format to wrong tasks (can *increase* hallucination). [03]
- **AP25.** "You are an expert" priming damages factual accuracy on knowledge tasks (Wharton 2025). [03]
- **AP26.** Trusting LLM-self-reported confidence without external calibration. [03, 09]
- **AP27.** Reasoning everywhere (Opus + max on every subagent — 10-30× budget waste). [03, 15]
- **AP28.** Adaptive thinking is OFF BY DEFAULT on Opus 4.7 — silent regression on prompts migrated from 4.6. [02]

### Sessions / workflow

- **AP29.** The kitchen-sink session (multiple unrelated tasks in one conversation). [02]
- **AP30.** Correcting the same issue more than twice in one session without `/clear`-and-better-prompt. [02]
- **AP31.** Trust-then-verify gap — ship without verification. [02, 13]
- **AP32.** Unscoped "investigate" prompts that fill context. [02]

### Tools / MCP

- **AP33.** "MCP for everything" — every server inflates system prompt; Cloudflare Code Mode pattern cut 94% by collapsing. [05, 11]
- **AP34.** Trusting MCP resource contents (every published MCP injection chain follows this shape). [11]
- **AP35.** Tool-name collisions across servers. [11]
- **AP36.** Auth tokens in plaintext client config. [11]
- **AP37.** Treating `tools/list` as static (rug-pull attack vector). [11]
- **AP38.** Running unaudited community MCP servers with write scopes (5.5% poisoned-metadata rate). [11]

### Safety

- **AP39.** `bypassPermissions` outside disposable containers. [10]
- **AP40.** `Bash(rm:*)` on allow list without scoping. [10]
- **AP41.** Letting tool outputs flow back to model unfiltered (#1 production vulnerability 2025-2026). [10]
- **AP42.** Treating the model as a safety boundary (Anthropic itself does not). [10]
- **AP43.** Partial sandbox isolation (FS without network or vice-versa). [10]

### CI / cost / automation

- **AP44.** Headless invocations without cost circuit breaker ($47K/$30K/$87K runaway-loop cases). [15]
- **AP45.** Stuck-in-PR-review-loop (AI review comments → AI agent reads → AI agent pushes changes → AI review re-triggers). [15]
- **AP46.** Hallucinated commits in scheduled work (routine writes PR referencing nonexistent issues/files). [15]
- **AP47.** Treating checkpoints as a git replacement. [02]
- **AP48.** Shipping system-prompt changes without ablation/staged rollout (April 23 postmortem). [02]

### Evals

- **AP49.** Same model as judge and actor (self-preference + correlated failure). [08]
- **AP50.** Snapshot tests on stochastic outputs without semantic equivalence. [08, 13]
- **AP51.** Tests-passed-by-the-AI-that-wrote-them. [13]
- **AP52.** "Coverage above 80%, ship it" (AI-reported 93% can be 34% effective after mutation testing). [13]
- **AP53.** Eval suites that look obviously like evals (eval-awareness pathology). [08, 09]

### TDD

- **AP54.** "Agent says tests pass" without re-running. [13]
- **AP55.** Tests that pass on first attempt (agent overfit test to own output). [13]
- **AP56.** Tests that skip side effects (function calls API; test mocks call; test passes; API never reached). [13]
- **AP57.** Mock-the-world / tautological assertions. [13]
- **AP58.** Verifying with same model that generated (correlated failure modes — cross-family shadow comparison as fix). [09, 13]

---

## 4. Cross-cutting themes (read this even if you skip the rest)

Six patterns appear across multiple reports as load-bearing. Internalize as principles, not rules.

**T1. Verification is the line.** *"Give Claude a way to verify its work. This is the single highest-leverage thing you can do."* (Anthropic, Claude Code best-practices). Apply to code (tests, build, lint, type-check), to UI (screenshots, visual iteration), to design artifacts (schema-conformance, citation existence, cross-artifact consistency). [02, 13]

**T2. Distillation as discipline, not optimization.** Orchestrator reads compressed summaries; raw sub-agent output stays on disk. This is the recommended Anthropic pattern; relax it at your peril. Sub-agent context isolation + condensed return is the three-part pattern (clean context, persistent artifacts, 1-2k-token distillations). [02, 04]

**T3. The model is not a safety boundary.** Anthropic itself does not treat the model as the safety boundary. The model is *one* layer; the harness, sandbox, permission model, egress controls, audit log, and human-in-the-loop are the others. Defense in depth. [10]

**T4. Length matters at the top, not in aggregate.** A 30k-token system prompt is fine if it's all cached and ordered by priority (identity → principles → rules → bypasses). What kills adherence is buried instructions, not byte count. CLAUDE.md is paid on every turn — but only if instructions are buried does the budget hurt. [03, 14]

**T5. Cost is an engineering problem now.** Every runaway loop case in 2025-2026 shares one missing primitive: cost circuit breaker. Cap costs per session, per day, per workflow. Cheap-classifier → expensive-worker routing. Prompt caching is mandatory at scale. Haiku for 70-80% of work. [15]

**T6. Eval-awareness is real and growing.** Frontier models recognize evaluation contexts and behave differently. Apollo on Claude Sonnet 3.7; OpenAI/Apollo on o3/o4-mini; Petri 2.0's realism-classifier mitigation. Any eval that doesn't account for it over-reports safety. For critic stacks: phrase the candidate as working task, not "this will be reviewed." [08, 09]

---

## 5. Per-report deep-dive index

The 15 reports under [research/sota-2026-v2/](research/sota-2026-v2/) total ~78,000 words. Pointers by question:

| If you want to know about… | Read |
|---|---|
| Every Claude Code primitive + 2026 platform features | [01-claude-code-platform.md](research/sota-2026-v2/01-claude-code-platform.md) |
| What Anthropic explicitly recommends (verbatim quotes) | [02-anthropic-practices.md](research/sota-2026-v2/02-anthropic-practices.md) |
| Prompt engineering masterclass — every 2026 technique | [03-prompt-engineering.md](research/sota-2026-v2/03-prompt-engineering.md) |
| Context engineering as a distinct discipline | [04-context-engineering.md](research/sota-2026-v2/04-context-engineering.md) |
| Tool design — descriptions as load-bearing prompt eng | [05-tool-design.md](research/sota-2026-v2/05-tool-design.md) |
| Multi-agent orchestration patterns + frameworks | [06-multi-agent.md](research/sota-2026-v2/06-multi-agent.md) |
| Memory taxonomy + RAG 2026 + long context | [07-memory-rag-context.md](research/sota-2026-v2/07-memory-rag-context.md) |
| Evaluation methodology + golden datasets + judge calibration | [08-evals.md](research/sota-2026-v2/08-evals.md) |
| Critic panels + agent-as-judge + triangulation | [09-critic-panels.md](research/sota-2026-v2/09-critic-panels.md) |
| Safety, guardrails, prompt injection 2026 | [10-safety-guardrails.md](research/sota-2026-v2/10-safety-guardrails.md) |
| MCP ecosystem + custom server patterns + supply-chain security | [11-mcp-ecosystem.md](research/sota-2026-v2/11-mcp-ecosystem.md) |
| AI-dev tool ecosystem (Aider, Cursor, Cline, etc. patterns) | [12-ai-dev-ecosystem.md](research/sota-2026-v2/12-ai-dev-ecosystem.md) |
| TDD + spec-driven dev + verification primitives | [13-tdd-spec-verification.md](research/sota-2026-v2/13-tdd-spec-verification.md) |
| CLAUDE.md / AGENTS.md / project-instruction file SOTA | [14-project-instructions.md](research/sota-2026-v2/14-project-instructions.md) |
| Headless mode + CLI + SDK + CI + cost optimization | [15-headless-ci-cost.md](research/sota-2026-v2/15-headless-ci-cost.md) |

---

## 6. Adoption order — the realistic 90-day plan

If you're starting from a CLAUDE.md, a few skills, and ad-hoc Claude Code use:

**Week 1 — Foundations (must-do):**
- Trim CLAUDE.md to ~100 lines. Apply "would Claude make a mistake without this" test ruthlessly.
- Add the three deny rules to `.claude/settings.json` (dotfiles + destructive + egress prompts).
- Enable `CLAUDE_CODE_ENABLE_TELEMETRY=1` if you have any observability backend.
- Pin model versions in any production prompts (`claude-opus-4-7-YYYYMMDD`, not alias).
- Build a 20-item golden eval set from real failures.

**Week 2-3 — Habits (high-leverage):**
- Adopt verification-before-completion as a workflow rule (test command output, this turn).
- Diff-before-claim — every "I did X" gets verified.
- Move verbose work to subagents (search, exploration, log analysis).
- Set up prompt caching with the four-breakpoint layering.
- Add cost circuit breaker to any headless invocations.

**Month 2 — Infrastructure (compounding leverage):**
- Build the layered `.claude/rules/<scope>.md` structure with `paths:` frontmatter.
- Promote deterministic constraints from CLAUDE.md prose to PreToolUse hooks.
- Set up AI code review on every PR (CodeRabbit or equivalent).
- Sandbox Bash that touches untrusted code (Seatbelt/bubblewrap).
- Schedule cross-session diagnostics as a Routine.
- Build a critic panel with at least one cross-family lane for high-stakes reviews.

**Month 3 — Scaling (advanced):**
- Calibration set for any critic panel (20-50 candidates with human verdicts).
- Cross-family judge triangulation for high-stakes work.
- Anti-confirmation discipline in retrieval (mandate contradicting passages).
- Cost dashboard via OTel + Prometheus + Grafana.
- Model-tiered routing (Haiku classifier → Sonnet/Opus worker).
- Property-based + mutation testing for any AI-generated code.

**Standing — ongoing:**
- Re-baseline prompts when models change. Don't trust silent default flips.
- Add red-team findings to the eval set every time.
- Review CLAUDE.md quarterly with 90-day diff. Prune stale entries.
- Track cache hit rate as a primary metric.
- Re-read [02-anthropic-practices.md](research/sota-2026-v2/02-anthropic-practices.md) when Anthropic ships major model or system-prompt changes.

---

## 7. What this synthesis is NOT

- It is not a workflow design — it's a menu of practices. Choose what fits your context.
- It is not stack-specific — it's the general 2026 SOTA. Apply selectively.
- It does not cover worktrees (separately documented in [research/sota-2026/08-parallel-worktrees.md](research/sota-2026/08-parallel-worktrees.md)).
- It does not advocate adopting every recommendation. The right minimum stack for a serious 2026 practitioner is: verification discipline, CLAUDE.md hygiene, cost circuit breaker, sub-agent context isolation, prompt caching, 20-item eval set, three deny rules. That's seven items. Everything else is leverage to add as your maturity grows.

---

## 8. Honest assessment

This synthesis was produced by Claude reading research produced by Claude. The same family-correlation problem documented in [09-critic-panels.md](research/sota-2026-v2/09-critic-panels.md) applies. The cheapest mitigation: when you actually wire up cross-family triangulation, feed this document through the external lane and see what it catches.

The most surprising findings from the 78,000 words of research:

1. **The hard ceiling of ~150 instructions per session** is more empirical than I expected. CLAUDE.md bloat is the single most common reason teams complain "Claude doesn't follow my rules" — when the rules are buried in a 5,000-token instruction wall, of course they aren't followed.
2. **Eval-awareness is now load-bearing.** The Opus 4.7 system card §6.5.2.2 documents that the model's awareness of being evaluated shapes its honesty. This applies recursively to any critic stack — when the critic knows it's critiquing, it polishes for the rubric.
3. **Same-family bias in judges** is empirically robust across multiple arXiv papers. An all-Anthropic critic panel will systematically over-approve Claude-generated output. The cross-family lane (`EXTERNAL_SHADOW=1` reserved env var) is the mitigation.
4. **MCP supply-chain risk is worse than it looks.** 5.5% of public MCP servers carry poisoned metadata. The 2025-2026 CVE timeline is extensive. Install MCPs with the same paranoia as npm packages — but most teams don't.
5. **The cost circuit breaker is the most under-deployed primitive.** Every public runaway-loop case shares the same missing element. It's a ~10-line check. Almost no team has it.
6. **Verification-before-completion is the single highest-leverage practice** — Anthropic says so explicitly. The "agent says tests pass" → never re-ran failure mode kills more deployments than any other.

If you internalize nothing else: **verify before claiming done, keep CLAUDE.md under 120 lines, add a cost circuit breaker, and use sub-agent context isolation for verbose work.** Those four items capture ~60% of the leverage in 78,000 words of research.
