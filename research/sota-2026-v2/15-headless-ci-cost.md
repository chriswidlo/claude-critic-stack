# Headless Claude Code, CI/CD, Scheduled Tasks, Cost & Observability — 2026 Reference

**Scope.** This is the canonical 2026 practitioner reference for running Claude programmatically: the headless CLI, the Agent SDK, scheduled cloud tasks (Routines and `/loop`), GitHub Actions and broader CI/CD wiring, the contemporary AI-code-review market, cost engineering, and observability. It is stack-agnostic. It assumes you have written code with the model interactively and now need to run it in pipelines, on cron, behind webhooks, or as a daemon — and not get a $40K invoice.

Throughout, prices and model names are as of May 2026. The pace of change in this space is brutal; treat exact figures as a snapshot, the architectural patterns as durable.

---

## 1. Headless Claude Code CLI

### 1.1 `claude -p` / `--print`

The foundation. `claude -p "<prompt>"` runs the agent non-interactively: no TUI, no spinner, a single execution that exits when the model is done. Every CI integration, every cron job, every shell-pipeline use is built on this flag. The interactive mode is for humans; `-p` is for machines and machine-like humans.

Inputs come from the prompt argument and stdin. Outputs go to stdout in one of three formats, set by `--output-format`.

### 1.2 `--output-format text | json | stream-json`

Three formats, three audiences:

- **`text`** (default) — human-readable. Free-form. Do not parse this. It is for `claude -p "explain this regex"` at the terminal, nothing else.
- **`json`** — a single JSON envelope: `{ session_id, result, total_cost_usd, num_turns, ... }`. The 2026 practitioner consensus is that roughly 85% of CI/CD integrations use `json` because `jq`/Python can extract the `result` field deterministically and the metadata fields (`total_cost_usd`, `num_turns`) feed straight into cost dashboards.
- **`stream-json`** — newline-delimited JSON events emitted as the run progresses. Each event carries a `session_id`, a type (`message_start`, `tool_use`, `tool_result`, `message_delta`, `message_stop`, `result`), and event-specific payload. This is what makes background agents and multi-process topologies actually possible.

**Known issue with `stream-json`.** Stdout flush issues with certain shells (tracked in the upstream issue tracker around #25670) cause events to bunch up rather than stream. Workarounds: prepend `stdbuf -oL claude -p ...` to force line-buffered output, or run under a PTY wrapper (`script`, `unbuffer`, `expect`, or a small Go/Rust PTY shim). If you see your "live dashboard" only update at the end of the run, this is why.

### 1.3 Stdin/stdout chaining

The canonical Unix pattern:

```bash
cat changes.diff \
  | claude -p "summarize the risk in this diff" --output-format json \
  | jq -r .result \
  | claude -p "draft a release note from this risk summary" \
  > notes.md
```

This is the same composability you get from `grep | sort | uniq` — three discrete agent calls in a pipeline, each one short, each one auditable, each one cheap. It is dramatically more debuggable than one monolithic prompt asking the model to do all three things.

For richer topologies (parallel fanout, conditional routing), use `stream-json` on both sides of the pipe. `--input-format stream-json --output-format stream-json` together enables persistent multi-turn sessions where one process maintains the conversation and another forwards events — a true multi-process agent topology rather than a string of one-shot calls.

### 1.4 Exit codes

- `0` — success.
- `1` — generic error (model error, network, parse failure).
- non-zero — tool-restriction violations and policy errors.

**Never parse stdout content to decide success.** Branch on the exit code, then extract `result` from the JSON envelope. A model that politely refuses or returns "I cannot do that" will still exit 0; the run technically succeeded, the substantive answer is "no." Conflating "agent error" with "agent declined" is a common CI bug — your pipeline thinks it produced a release note when in fact it produced a refusal.

### 1.5 `--bare` — the future default

`--bare` skips auto-discovery: no hooks, no skills, no plugins, no MCP servers, no auto-memory, no project `CLAUDE.md`. Only the flags you pass take effect.

Without `--bare`, a CI run picks up whatever happens to be in the runner's `~/.claude/`, whatever `.mcp.json` sits in the workspace, whatever skills the team installed last week. That is not a CI pipeline; that is a roulette wheel. With `--bare`, the same inputs produce the same outputs across machines, across contributor workstations, across runner images. It is the only honest way to claim CI reproducibility.

The composable pattern is `--bare` plus explicit context:

```bash
claude --bare -p "review this PR for SQL injection" \
  --append-system-prompt-file ./CLAUDE.md \
  --allowed-tools "Read,Bash(git diff:*)"
```

You are stating, in one line, exactly what context this run sees. Reviewers can read it. Auditors can read it. Six months from now you can read it.

### 1.6 Tool restriction — `--allowed-tools` and `--disallowed-tools`

Two orthogonal levers.

- `--allowed-tools` is a positive allowlist. Anything not listed is denied. Use it as a per-session cap: "this run only needs Read and Bash(git diff)."
- `--disallowed-tools` is a hard denylist. Use it as a guarantee even if the model talks itself into needing a forbidden tool. Pin `Bash(rm:*)`, `Bash(git push:*)`, `Bash(git reset:*)`, `Bash(curl:*)` for any scheduled run where the work is meant to be observational.

Combine both. The allowlist scopes intent; the denylist hardens against the model's enthusiasm.

### 1.7 The `--disallowedTools` bypass (adversa.ai, 2026)

In early 2026 adversa.ai demonstrated that Claude Code's deny-rule enforcement silently bypassed any shell command containing more than 50 chained subcommands (joined by `&&`, `||`, or `;`). The flaw lived in `bashPermissions.ts` lines 2162–2178 — a performance cap on per-subcommand security analysis. A POC chained 50 no-op `true` statements with `curl` and watched the deny rule evaporate. Anthropic patched this in Claude Code v2.1.90.

The lesson outlives the patch. **Never rely on deny rules as your only defense.** Sandbox the runner: container with no production credentials, no write access outside the working directory, no network egress beyond what the agent demonstrably needs. Deny rules are belt; the sandbox is suspenders. You want both.

### 1.8 Session continuity — `--continue` and `--resume`

`--continue` resumes the most recent session for the current cwd; `--resume <session-id>` resumes a named one. This is how you build conversational state across invocations: the first call establishes context, subsequent calls add turns to the same conversation without re-sending the system prompt and codebase context. For long-running scripted workflows (multi-step refactors, paginated processing), this is also a meaningful cost optimization — see prompt caching below.

### 1.9 Other limits worth knowing

Stdin is capped at 10 MB as of v2.1.128+. Beyond that, write to a file and pass the path. The 1M-context Opus tier helps with large inputs, but stdin transport itself has its own ceiling.

---

## 2. Authentication in CI

Two patterns dominate.

**Anthropic-direct (API key)** — `ANTHROPIC_API_KEY` in the runner environment. Stable, billable to your Anthropic console account, decoupled from anyone's seat or subscription. This is the right pattern for any CI workload owned by an organization rather than an individual. It is also the only pattern that survives the June 15, 2026 split (see below) unchanged: API-key auth keeps paying API rates directly.

**Subscription (OAuth)** — `CLAUDE_CODE_OAUTH_TOKEN`, generated locally via `claude setup-token` for Pro and Max plans. Trickier in CI because OAuth refresh and the per-user nature of the token don't map cleanly to multi-developer pipelines. Mostly used by solo developers or small teams who want CI runs to draw from their personal subscription credit.

**Cloud providers.** `claude-code-action` supports Amazon Bedrock (`use_bedrock: true`, AWS OIDC via `aws-actions/configure-aws-credentials@v4`), Google Vertex AI (`use_vertex: true`, `google-github-actions/auth@v2`), and Microsoft Foundry (OIDC or `ANTHROPIC_FOUNDRY_API_KEY`). OIDC is preferred — no long-lived secrets in repo settings, scoped per-workflow.

**The June 15, 2026 subscription split.** From that date, programmatic surfaces stop drawing from a subscriber's interactive Pro/Max/Team/Enterprise pool and move to a separate monthly Agent SDK credit: $20 (Pro), $100 (Max 5x), $200 (Max 20x), $20/seat (Team Standard), $100/seat (Team Premium). The credit resets monthly and expires unused. Affected surfaces:

- `claude -p` non-interactive CLI
- Python `claude-agent-sdk` and TypeScript `@anthropic-ai/claude-agent-sdk`
- Claude Code GitHub Actions
- Third-party apps authenticating via subscription

Interactive terminal/IDE use, claude.ai, and Cowork stay on the standard plan quota. API-key billing is untouched. The split is essentially Anthropic saying "agents are not the same workload as humans; price them separately." Plan accordingly — if your CI was quietly draining a Max subscription, June 15 will surface that as an explicit budget.

---

## 3. Claude Agent SDK (Python + TypeScript)

The SDK gives you what the CLI gives you, in-process, with async/await, structured outputs, streaming events, and the ability to hold a session object across many turns without shelling out per call.

**When to use SDK vs CLI.** A useful heuristic: if the work is shaped like one-shot transformation ("summarize this diff," "draft this comment"), the CLI is cleaner — its inputs/outputs are byte streams that compose with the rest of the shell ecosystem. If the work is shaped like a long-running flow with branching tool use, conditional retries, in-memory state, and a need to react to streamed events in real time, the SDK is cleaner — you stay in one language, you keep types, you avoid serialization overhead between turns.

**Python SDK.** Async-first. `async for event in agent.stream(...)` is the canonical pattern. Structured outputs via Pydantic. Plays well with Jupyter notebooks for exploratory eval work.

**TypeScript SDK.** ESM-native. Friendlier to web frontends and edge-runtime backends (Cloudflare Workers, Vercel Edge). Same surface shape as the Python SDK.

Both SDKs are billed against the new Agent SDK credit pool from June 15, 2026 for subscription-auth users; API-key users continue to pay API rates.

---

## 4. Claude Code Routines (scheduled cloud agents)

Shipped April 14, 2026. Often described as "cron for agents." A Routine is a named, scheduled invocation that runs in Anthropic-managed cloud infrastructure with configured tools, credentials, and permissions — so the work continues whether your laptop is open or shut.

**Three triggers.**

1. **Schedule** — 5-field cron (hourly, nightly, weekly, whatever).
2. **API** — HTTP POST to a per-routine bearer-token endpoint.
3. **Webhook** — GitHub repository events (PR opened, PR merged, issue created, etc.).

**Positioning.** Routines are a sibling to Claude Managed Agents, not a replacement. Managed Agents are for long-running services with custom MCP servers and persistent state. Routines are for "the task you already know how to describe in one Claude Code session, but you want it to run on schedule." If you've ever opened a session, copy-pasted the same prompt, watched it work, then closed the laptop — that prompt is a Routine candidate.

**Use-case patterns the first month.** Anthropic teams reported: automated issue triage, deployment verification, alert analysis, documentation updates, cross-language SDK synchronization. The community piled on with: nightly canon/corpus refresh, dependency-update review, security scanning of new PRs, dashboard regeneration, daily Slack briefings, overnight test-suite triage. GitHub Marketplace installs were in the five figures within a week of launch.

### 4.1 Writing resilient Routine prompts — six rules

These are not "best practices." They are the rules that prevent your Routine from cycling indefinitely or quietly destroying work while you sleep.

1. **State the exit condition explicitly.** "Stop after writing the file. Do not investigate further." A Routine with no exit condition explores until it runs out of turns or context, and you pay for every step.
2. **Cap the work.** "Examine at most 10 PRs" not "recent PRs." Quantify. The model will keep going if you let it.
3. **Pre-declare every artifact path.** No `mkdir -p` adventures. Tell it exactly where to write. `~/scratch/<date>/report.md`, not "create a useful directory and put the report there."
4. **Forbid destructive operations.** `--disallowed-tools "Bash(rm:*),Bash(git push:*),Bash(git reset:*),Bash(git checkout --:*)"`. A Routine writing a report has no business doing any of these.
5. **Emit a structured terminal artifact.** A Routine should write one summary file. If the file doesn't exist after the run, the Routine failed regardless of exit code. This converts "did it succeed?" from a question about exit semantics into a question about filesystem state — much harder to fool.
6. **Idempotency.** Re-running on the same input should not double up artifacts. Include the date in the path, or detect prior runs and short-circuit. Routines retry on infrastructure failures; you do not want each retry creating a fresh PR.

### 4.2 Cost monitoring for Routines

The dashboard surfaces per-run cost. The dangerous failure mode is a Routine whose per-run cost is doubling because the context it scans is growing (new issues, new PRs, new logs) and nobody is watching the trend line.

The defensive pattern that emerged in the first month is a **"Guardian" Routine** — a separate scheduled Routine that reads the cost log and pages a human if any single Routine exceeds N× its 30-day median spend. It is one of those layers you only think to build the second time you get burned.

---

## 5. `/loop` — session-scoped scheduling

`/loop` is the local sibling of Routines. It runs inside an active Claude Code session and only fires while that session is open and idle.

- `/loop 5m check the deploy` — fixed 5-minute cadence, max 7-day retention.
- `/loop check the deploy` (no interval) — Claude self-paces, choosing intervals from 1 minute to 1 hour based on its own model of urgency.
- `/loop` alone — invokes the built-in maintenance prompt, overridable by `.claude/loop.md`.

Under the hood: `CronCreate`, `CronList`, `CronDelete` tools, standard 5-field cron expressions, local timezone, deterministic jitter to avoid stampedes, cap of 50 tasks per session. Tasks survive `--continue`/`--resume` within their retention window.

**The clean conceptual split.** Routines for "this runs whether I'm at the keyboard or not." `/loop` for "while I'm working in this session, also keep checking X." Closing the terminal kills `/loop` tasks; Routines run regardless.

---

## 6. GitHub Actions + AI

### 6.1 First-party actions

**`anthropics/claude-code-action`** — the general-purpose action for PRs and issues. Triggers: `@claude` mention in a comment, issue assignment, or explicit invocation from a workflow file. Auth: Anthropic-direct, OAuth, Bedrock, Vertex, Foundry. Quickest setup is `/install-github-app` from inside Claude itself, which provisions the secrets and webhook for you.

**`anthropics/claude-code-base-action`** — the lower-level primitive. Use this when you want to compose your own action on top (custom triggers, custom permissions, custom comment formatting).

**`anthropics/claude-code-security-review`** — first-party security action. Runs on every PR, comments inline. Default model is Opus-class. Identifies injection, auth/authorization flaws, data exposure, crypto issues — and crucially does data-flow tracing across files in a way classic SAST pattern-matching doesn't. The published caveat is loud: not hardened against prompt injection, so configure "Require approval for all external contributors" on the repo. Trust the model with code from people you already trust.

### 6.2 Custom actions

The common DIY pattern is 10–15 lines of shell:

```yaml
- name: Run Claude
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    curl -fsSL https://claude.ai/install.sh | bash
    git diff origin/main...HEAD \
      | claude --bare -p "review this diff for production risks" \
        --output-format json \
        --allowed-tools "Read,Bash(git log:*)" \
      | jq -r .result \
      > review.md
    gh pr comment ${{ github.event.pull_request.number }} -F review.md
```

This is the shape of dozens of homegrown integrations. It is fully under your control, easy to read, and has none of the magic of a third-party action. The trade-off is you maintain it.

### 6.3 OpenAI actions

Exist, similar shape (`openai/codex-action` and friends). The market converged on roughly the same surface — a positive sign for portability if you ever need to swap providers in your CI graph.

---

## 7. CI patterns for AI-touched repos

### 7.1 AI-generated PR descriptions

Cheap (roughly $0.005–$0.02 per PR with prompt caching) and high-value. CodeRabbit `/describe`, Greptile, and `claude-code-action` all support this; many teams roll their own with a 10-line workflow.

### 7.2 AI-generated changelogs / release notes

GitHub-native automated release notes plus AI enhancement (e.g. `ai-release-notes-action`, the Ascend pipeline). DeployHQ's guidance is worth internalizing: **always preserve the raw commit list alongside the AI summary.** The summary is for humans skimming; the commit list is for the future maintainer who needs to know exactly what was in the release.

### 7.3 AI code review — the 2026 leaderboard

Ranked by adoption and aggregate spend signal:

- **CodeRabbit** — roughly $24/dev/month, >2M repos, >13M PRs. Mature, fine-grained config, works across GitHub/GitLab/Bitbucket/Azure DevOps. Diff-based analysis (sees the change, less aware of cross-file effects). AIMultiple's 2026 evaluation: 4/5 correctness, 1/5 completeness, 2/5 depth — fast and reliable on local correctness, weaker on architecture.
- **Greptile** — RAG-indexes the entire codebase. 82% bug catch rate vs CodeRabbit's 44% in head-to-head benchmarks; but 11 false positives vs CodeRabbit's 2. Rapid growth (~4× customer count over nine months) appears driven by new adoption rather than CodeRabbit churn. Use for large, complex codebases where cross-module dependencies matter.
- **Ellipsis** — large-PR summarization plus targeted fixes. Use when you're drowning in 2000-line PRs and need an AI-generated outline before human review.
- **GitHub Copilot PR Review** — native, lowest friction, no extra vendor. The KAIRI 2025 analysis concluded it's insufficient as a hard merge gate — fine as advisory, dangerous as a blocker.
- **`anthropics/claude-code-security-review`** — first-party security lens. Pair with one of the above for non-security review.

### 7.4 AI test generation

Diffblue (Java), Codium (multi-language), CI-Spark (newer, focused on regression-test generation from diffs). Each plays best when scoped to specific change types rather than turned on for everything.

### 7.5 AI fuzz testing

The FD-FACTORY framework is the reference work as of mid-2026. Regulatory angle worth tracking: this fits cleanly into the NIST AI RMF "Measure" function, and several regulated industries are starting to require evidence of AI-generated test coverage as part of validation packages.

### 7.6 AI for dependency updates

Dependabot and Renovate produce the PRs; AI sits on top to triage them (Fossabot, Safeguard.sh). The valuable layer is not the PR itself — it's the AI deciding "this minor bump is safe to auto-merge, this major bump needs human eyes, this transitive change introduces a CVE."

### 7.7 AI security review on every PR

`claude-code-security-review` for context-aware vulnerability hunting. GitGuardian MCP as a hard merge gate when you need an actual block-on-secret-detected rather than an advisory comment. The two compose well: AI for "is this code idea exploitable," deterministic scanning for "is there a literal AWS key in this diff."

---

## 8. Automation primitives

### 8.1 Pre-commit hooks

Latency budget: under 5 seconds. Anything slower and developers will start running with `--no-verify`, and your hook becomes folklore.

The pattern that holds up is local inference: `llm-code-review` uses a local Ollama runtime so code never leaves the machine, a Haiku-class local model does typo / debug-statement / obvious-style review on staged hunks in 1–3 seconds. Cloud calls are usually too slow for the pre-commit slot.

### 8.2 Pre-push hooks

Latency budget: ~30 seconds. Now a cloud call to Haiku is feasible. This is the right slot for "scan the whole branch's net diff for obvious problems before it leaves the machine."

### 8.3 Merge-queue AI gates

The April 23, 2026 GitHub merge-queue incident is the cautionary tale here. Between 16:05 and 20:43 UTC, 658 repositories and 2,092 PRs were affected by silent incorrect merge commits when merge groups contained more than one PR using the squash strategy. Detection took 3h33m because the regression affected merge *correctness*, not availability — automated monitoring didn't catch it; customer reports did. Root cause: incomplete feature-flag gating on a new merge-base computation path.

The lesson is broader than the bug. **AI-generated PR volume is now itself a load profile that breaks infrastructure designed for human-rate PRs.** Two implications for AI gates in the merge queue:

1. AI gates should **fail-open during infrastructure incidents**, not block. A gate that blocks every merge because the AI service is having a bad day is now a sitewide outage of its own making.
2. Instrument merge-result correctness yourself. Don't trust upstream monitoring to catch silent corruption.

### 8.4 AI as a release blocker — when it's safe

Safe when: documented bypass path, false-positive rate <5%, verdict is human-reviewable in <60 seconds. Dangerous when: opaque reasoning, non-deterministic (re-triggering might pass), blocks every PR. The "re-run and it passes" failure mode is corrosive — it teaches the team that the gate is noise, and they will stop reading it.

---

## 9. Background and daemonized agent patterns

- **`herdctl`** (edspencer/herdctl) — orchestration layer on the Claude Agents SDK. YAML-defined agent fleets, schedules, webhooks, chat triggers. Runs natively or in Docker. Connects fleets to Discord and Slack. Closest thing to a "Kubernetes for Claude agents" right now.
- **ClaudeClaw** — a Claude Code plugin turning Claude into an always-on agent orchestrator listening to Slack, WhatsApp, Telegram, Discord, and Gmail, routing messages to isolated agents from a single Node.js process. Plug-in extension system, structured memory, webhook triggers, per-group config, cost tracking, native sandbox support.
- **Anthropic first-party Slack** — Claude Code in Slack is the official integration; `cc-connect` bridges to Feishu/Lark, DingTalk, Telegram, Discord, LINE for teams outside the Slack/Teams duopoly.
- **Watch-mode agents** — `fswatch` or `entr` loops invoking `claude -p`. Particularly useful for documentation-drift detection: whenever a watched source file changes, re-run a check that docs reflect it.
- **GitHub webhook → agent** — the Hookdeck + Trigger.dev + Claude pattern is documented and proven; useful when you outgrow Routines' built-in webhook handling.

---

## 10. Cost management

### 10.1 Prompt caching

The single largest lever. Anthropic pricing for cached tokens: reads at 0.1× input cost; writes at 1.25× input (5-minute TTL) or 2× input (1-hour TTL). Roughly 90% savings on cached tokens. Minimum cacheable prefix: 4096 tokens on Opus 4.6 / Haiku 4.5 (1024 on older Opus 4 / Sonnet 4). Max four explicit cache breakpoints per request; if you set four block-level breakpoints, the API returns 400 — no room for automatic caching.

Claude Code already places breakpoints aggressively — system prompt, tool definitions, `CLAUDE.md`, conversation history up to the most recent messages. As of February 5, 2026, prompt-cache isolation moved from organization-level to workspace-level, which matters for multi-tenant tooling.

Pick TTL by cadence: 5-minute cache for prompts hit more often than every 5 minutes (refreshed at no extra charge); 1-hour cache for less-frequent-than-5m, more-frequent-than-1h. Anything rarer than hourly isn't worth caching.

### 10.2 Model tiering — 2026 prices per million tokens

| Model | Input | Output |
|---|---|---|
| Haiku 4.5 | $1 | $5 |
| Sonnet 4.6 | $3 | $15 |
| Opus 4.6 | $5 | $25 |
| Opus 4.7 (1M tier) | $15 | $75 |

Two important details on Opus 4.7: prices are unchanged per-token at base tier, but the new tokenizer can emit up to 35% more tokens for the same English text, so effective per-request cost is ~1.0–1.35× the 4.6 baseline depending on workload. The 1M-context tier is a separate price point — don't enable it unless you actually need >200K context.

### 10.3 The single most reliable cost-management pattern: cheap classifier → expensive worker

Community consensus is that **70–80% of production queries can run on Haiku.** The pattern: a tiny Haiku call classifies the incoming task (trivial / standard / hard), routes trivial straight to Haiku, standard to Sonnet, hard to Opus. The classifier costs pennies; the routing decision saves dollars.

One published case study went $80/month → $24/month (a 70% cut) by moving from a default-Opus-with-Sonnet-fallback architecture to Haiku-heavy routing with prompt caching on the shared system prompt.

This pattern is reliable because it makes the cost-control decision explicit and inspectable. A team that says "we just use Sonnet for everything" cannot easily answer "what fraction of our queries needed Sonnet?" A team running the classifier-router has a per-tier hit rate they can graph.

### 10.4 Anthropic Batch API

Async batch processing at a flat 50% discount on both input and output tokens. Submit up to 100,000 requests or 256 MB per batch; most complete in under an hour, hard ceiling 24 hours. Quality is identical to interactive — only timing differs.

When to reach for it: large dataset processing, eval suite runs, document classification at scale, nightly summarization jobs, anything where latency tolerance is hours. When not to: interactive UX, anything requiring sub-second response, anything where the result drives a synchronous downstream action.

The Batch API combined with prompt caching on shared system prompts is the textbook setup for bulk evaluation runs — half-price tokens plus 90% savings on cached prefixes.

---

## 11. Observability

### 11.1 OpenTelemetry built in

Set `CLAUDE_CODE_ENABLE_TELEMETRY=1`, choose at least one OTLP exporter, and Claude Code emits three independent signals: spans around each model request and tool execution, metrics for token and cost counters, and structured log events for prompts and tool results. Each signal has its own enable switch and exporter — opt in to what you need, no more. By default content (the prompts you send, the responses you receive) is **not** recorded; only structural metadata is. Metrics export every 60s; traces and logs every 5s.

Use GenAI semantic conventions where applicable. Backends people are actually running in 2026: SigNoz, Grafana Cloud, Datadog, Honeycomb, OpenObserve, VictoriaMetrics. Any OTLP-compatible collector works.

### 11.2 Per-session metrics that matter

- Cost (USD) per session
- Tokens (input, output, cache-read, cache-write) per session
- Latency per turn and per tool call
- Tool-use frequency and tool-error rate
- **Cache hit rate** as a first-class metric

Cache hit rate is the one most teams under-instrument. It is the leading indicator of "we changed the system prompt and broke caching across thousands of calls and our bill is about to double." Alert on it dropping more than ~20% week-over-week.

### 11.3 LLM observability platforms

Langfuse, LangSmith, Helicone, Phoenix, Braintrust, Weave, Vellum — each with a slightly different angle (trace UI, eval harness, prompt versioning, A/B testing). For Claude-specific work, the lowest-friction path is OTLP to whatever you already use for the rest of your stack, then layer one of these on top when you need eval-set management.

### 11.4 The `events.jsonl` pattern

An append-only per-tool event log alongside whatever OTLP you're emitting. One line per event, structured JSON. It is the dumbest possible observability primitive and it has saved more incident investigations than any dashboard. When the model does something weird, you `grep` the file.

---

## 12. Pitfalls — the $1000 loop and friends

This section exists because every other section in this document is moot if you wake up to a five-figure invoice.

### 12.1 Recent runaway-cost incidents

- A LangChain agent retry loop accumulated $47,000 over 11 days before anyone noticed.
- A team reported $87 burned on failed-request retries that taught them to build centralized retry logic — small in isolation, the canonical "first cut" of the lesson.
- An overnight unsupervised agent run cost $437 by morning.
- April 2026 incident at a 35-engineer SaaS: $87K aggregate across Claude Code, Cursor, and a custom triage agent.

**The common factor is the same in every retro: no circuit breaker.** Quoting one summary: *"There is no circuit breaker. The first signal is the invoice."*

### 12.2 Defense in depth

Layer these. Each is necessary, none is sufficient.

1. **Per-session timeout.** Wall-clock cap on every headless invocation. The simplest defense and the most often forgotten.
2. **Per-session retry limit.** Bounded retries with exponential backoff and a hard ceiling. Unbounded retry is the dominant failure mode in the published incidents.
3. **`max_turns` in headless invocations.** The agent does not know when to stop unless you tell it. A reasonable default for most production headless work is 10–25 turns; anything beyond that needs a justified higher cap.
4. **Per-user / per-workflow cost ceiling that suspends on breach.** Aggregate dollar cap that hard-stops the workflow when crossed. If you only build one defense, build this.
5. **Daily-spend anomaly detection.** Alert on any single workflow exceeding 2× its 30-day median. The "Guardian Routine" pattern from Section 4.2 generalizes here.

### 12.3 The stuck-in-PR-review-loop pattern

A subtle one. AI review posts comments → AI agent reads comments → AI agent pushes changes → AI review re-triggers → repeat. Each iteration costs money, and the system has no built-in stop condition.

Mitigations: skip review when the latest commit author is an agent (bot account or specific committer email); maintain a global per-PR review-invocation counter and bail at, say, 5; require a human signal to re-trigger review after the first agent-author commit.

### 12.4 Hallucinated commits in scheduled work

A Routine writes a file, opens a PR, and references nonexistent issues or files. Mitigation: a verifier step in the same Routine — `git diff --stat` to confirm something changed, `grep` to validate that mentioned issue numbers actually exist, file-existence checks on every path the model named — and only then `gh pr create`. Treat the PR-open step as the final commit in a pipeline of validators, not as a casual side effect.

### 12.5 Two failure modes that look like success

- **The polite refusal that exits 0.** Already covered above. If you parse `result` and find it starts with "I cannot," you have not produced a release note.
- **The empty artifact.** Routine completes, exit 0, no output file written. Always check the artifact exists before declaring success; Rule #5 of resilient Routine prompts exists for this reason.

---

## 13. Production examples

**Anthropic's own use** (from *How Anthropic teams use Claude Code*). Every team maintains a `CLAUDE.md` in git that documents mistakes — turning each incident into context for the next session. "CI auto-fix" is now standard: Claude detects a failing test or build, attempts a fix, opens a PR for human review. Web and mobile sessions can follow PRs in the cloud, fix CI failures, and address review comments, so the developer returns to a ready-to-merge branch rather than a backlog.

**Cloudflare's internal stack.** 3,683 internal users, 60% company-wide adoption, 93% in R&D. The 4-week rolling MR average rose from ~5,600 to >8,700 per week after rollout. Workers AI powers doc review in CI, including AGENTS.md generation across thousands of internal repos. Kimi K2.5 handles lightweight text-heavy tasks like the AGENTS.md Reviewer. The stack itself serves 20M requests and 241B tokens through AI Gateway.

**Vercel.** Durable-execution programming model explicitly targeted at agent workloads — long-running, idempotent-by-construction, replayable on failure.

The shared lesson across all three: AI integration is a programming-model problem at scale, not a tooling problem. The teams that win treat retries, replayability, cost ceilings, and observability as first-class concerns from day one, not as things to bolt on after the first incident.

---

## 14. Top 12 headless / CI / cost practices, ranked by leverage

1. **Cap `max_turns`, per-session timeout, and per-workflow cost ceiling on every headless invocation.** Single biggest defense against the runaway-cost class of incidents. Cost ceiling first if you build only one.
2. **Run with `--bare` in CI.** The only honest way to claim reproducibility across runners and contributor workstations.
3. **Branch on exit code, parse `result` from `--output-format json`.** Never parse free text for success.
4. **Cheap classifier → expensive worker.** Haiku for triage, Sonnet for standard, Opus for hard. 70–80% of production queries route to Haiku and stay there.
5. **Prompt caching on shared system prompts and `CLAUDE.md`.** ~90% savings on cached tokens; instrument cache hit rate as a first-class metric and alert on regressions.
6. **Sandboxed runners with both allow- and deny-lists on tools.** Deny rules are not a complete defense (see the adversa.ai bypass); the sandbox is the actual guarantee.
7. **Resilient Routine prompts: explicit exit conditions, capped scope, pre-declared artifact paths, forbid destructive ops, structured terminal artifact, idempotency.** All six, every time.
8. **`CLAUDE_CODE_ENABLE_TELEMETRY=1` with OTLP from day one.** Not after the first incident. Cost and token metrics per session feed dashboards and alerts.
9. **Skip-review heuristics on AI-author commits and per-PR review-invocation caps.** Prevents the stuck-in-PR-loop pattern.
10. **Verifier step before any `gh pr create` from a scheduled job.** `git diff --stat`, issue-number validation, file-existence checks. Hallucinated PRs are embarrassing and cost real review attention.
11. **Batch API for any workload tolerating hours of latency.** Half-price tokens, combine with prompt caching for bulk eval runs.
12. **AI gates must fail-open during infrastructure incidents.** A merge gate that blocks every PR because the AI provider is degraded is your own sitewide outage.

---

## Sources

Headless CLI and SDK:
- [Run Claude Code programmatically — Claude Code Docs](https://code.claude.com/docs/en/headless)
- [Claude Code stream-json: the output format that changes everything](https://backgroundclaude.com/blog/stream-json)
- [Claude Code Headless Mode CI/CD Playbook (Code With Seb)](https://www.codewithseb.com/blog/claude-code-headless-mode-cicd-automation-playbook)
- [Claude Code SDK `--bare` flag (Surf AI)](https://asksurf.ai/pulse/en/claude-code-sdk-bare-flag-10x-faster-startup)
- [Claude Code: 10 CLI flags you probably aren't using (mager.co)](https://www.mager.co/blog/2026-04-20-claude-code-cli-flags/)
- [Claude Code in CI/CD Pipelines (Agent Factory)](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/claude-code-teams-cicd/claude-code-in-cicd-pipelines)
- [How to Use the Claude Agent SDK With Your Claude Plan (Apidog)](https://apidog.com/blog/claude-agent-sdk-with-claude-plan-setup-guide/)
- [Use the Claude Agent SDK with your Claude plan — Help Center](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

Subscription split (June 15, 2026):
- [Anthropic splits billing: Agent SDK separate credit pools (The New Stack)](https://thenewstack.io/anthropic-agent-sdk-credits/)
- [Claude subscriptions get separate budgets for programmatic use (The Decoder)](https://the-decoder.com/claude-subscriptions-get-separate-budgets-for-programmatic-use-billed-at-full-api-prices/)
- [Claude Agent SDK Billing Changes June 15 2026 (ThePlanetTools)](https://theplanettools.ai/blog/claude-agent-sdk-billing-model-deprecation-june-15-2026-migration-playbook)

Routines:
- [Run prompts on a schedule — Claude Code Docs (scheduled tasks)](https://code.claude.com/docs/en/scheduled-tasks)
- [Claude Code can now do your job overnight (The New Stack)](https://thenewstack.io/claude-code-can-now-do-your-job-overnight/)
- [Claude Code Adds Cloud Routines for Scheduled AI Tasks (Winbuzzer)](https://winbuzzer.com/2026/04/16/anthropic-claude-code-routines-scheduled-ai-automation-xcxwbn/)
- [Claude Code Routines: Put Your AI Agent on Cloud Autopilot (Claudefast)](https://claudefa.st/blog/guide/development/routines-guide)
- [Claude Code Routines Guide (Claude Directory)](https://www.claudedirectory.org/blog/claude-code-routines-guide)

`/loop` and scheduled tasks:
- [Scheduled Tasks: The Loop Skill and Cron Tools (Agent Factory)](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/scheduled-tasks-cron)
- [What Is Claude Code /loop (SmartScope)](https://smartscope.blog/en/generative-ai/claude/claude-code-loop-command-session-scheduler/)
- [Claude Code Gets Cron Scheduling (Winbuzzer)](https://winbuzzer.com/2026/03/09/anthropic-claude-code-cron-scheduling-background-worker-loop-xcxwbn/)

GitHub Actions:
- [anthropics/claude-code-action (GitHub)](https://github.com/anthropics/claude-code-action)
- [anthropics/claude-code-base-action (GitHub)](https://github.com/anthropics/claude-code-base-action)
- [Claude Code GitHub Actions — Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/github-actions)
- [Cloud provider auth for claude-code-action (Bedrock/Vertex/Foundry)](https://github.com/anthropics/claude-code-action/blob/main/docs/cloud-providers.md)
- [anthropics/claude-code-security-review (GitHub)](https://github.com/anthropics/claude-code-security-review)
- [Automate security reviews with Claude Code (Anthropic)](https://www.anthropic.com/news/automate-security-reviews-with-claude-code)

AI code review market:
- [AI Code Review Tools Compared: CodeRabbit / Copilot / Sourcery / Ellipsis (DeployHQ)](https://www.deployhq.com/blog/ai-code-review-tools-compared-coderabbit-copilot-sourcery-ellipsis)
- [CodeRabbit vs Greptile (Panto AI / Medium)](https://medium.com/@pantoai/coderabbit-vs-greptile-ai-code-review-tools-compared-8b535666f708)
- [Are companies leaving CodeRabbit for Greptile? (YipitData)](https://www.yipitdata.com/resources/blog/greptile-vs-coderabbit-ai-code-review-market)
- [Best AI Code Review Tools of 2026 (DEV.to)](https://dev.to/heraldofsolace/the-best-ai-code-review-tools-of-2026-2mb3)

Background / daemonized agents:
- [edspencer/herdctl (GitHub)](https://github.com/edspencer/herdctl)
- [herdctl: orchestration layer for Claude Code (Ed Spencer)](https://edspencer.net/2026/1/29/herdctl-orchestration-claude-code)
- [ClaudeClaw: A Composable Agent Orchestrator for Claude Code](https://htdocs.dev/posts/claudeclaw-a-composable-agent-orchestrator-for-claude-code/)

Cost / pricing / batch:
- [Pricing — Claude API Docs](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude API Pricing 2026 (BenchLM)](https://benchlm.ai/blog/posts/claude-api-pricing)
- [Anthropic API Pricing 2026 Complete Guide (Finout)](https://www.finout.io/blog/anthropic-api-pricing)
- [Anthropic Claude API Pricing in 2026 (CloudZero)](https://www.cloudzero.com/blog/claude-api-pricing/)
- [Prompt caching — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Claude prompt caching minimum-token troubleshooting (Apiyi)](https://help.apiyi.com/en/claude-prompt-caching-not-hit-minimum-token-troubleshooting-en.html)
- [Batch processing — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [Anthropic Batch API in Production (Dotzlaw)](https://www.dotzlaw.com/insights/obsidian-notes-02/)

Observability:
- [Observability with OpenTelemetry — Claude Code Docs](https://code.claude.com/docs/en/agent-sdk/observability)
- [Bringing Observability to Claude Code: OpenTelemetry in Action (SigNoz)](https://signoz.io/blog/claude-code-monitoring-with-opentelemetry/)
- [Claude Code Monitoring with OpenTelemetry — SigNoz docs](https://signoz.io/docs/claude-code-monitoring/)
- [ColeMurray/claude-code-otel (GitHub)](https://github.com/ColeMurray/claude-code-otel)

Runaway costs & circuit breakers:
- [The Cost Circuit Breaker: Financial Controls for Production AI Agents (Fountain City)](https://fountaincity.tech/resources/blog/ai-agent-cost-circuit-breaker/)
- [I Spent $0.20 Reproducing the Multi-Agent Loop That Cost Someone $47K (Medium)](https://medium.com/@mohamedmsatfi1/i-spent-0-20-reproducing-the-multi-agent-loop-that-cost-someone-47k-7f57c51f3c06)
- [How an Unchecked AI Agent Loop Cost $437 Overnight (earezki.com)](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/)
- [AI Agent Circuit Breakers: The Reliability Pattern Production Teams Are Missing (DEV.to)](https://dev.to/waxell/ai-agent-circuit-breakers-the-reliability-pattern-production-teams-are-missing-5bpg)
- [Stop Runaway AI Agent Costs — Hard Budget Caps (SupraWall)](https://www.supra-wall.com/en/learn/ai-agent-runaway-costs)

Security:
- [Critical Claude Code vulnerability: Deny rules silently bypassed (adversa.ai)](https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/)
- [Claude Code bypasses safety rule if given too many commands (The Register)](https://www.theregister.com/2026/04/01/claude_code_rule_cap_raises/)

GitHub merge-queue incident (April 23, 2026):
- [An update on GitHub availability (GitHub blog)](https://github.blog/news-insights/company-news/an-update-on-github-availability/)
- [GitHub Broke Git: The Merge Queue Bug That Silently Deleted Your Code (DEV.to)](https://dev.to/varshithvhegde/github-broke-git-the-merge-queue-bug-that-silently-deleted-your-code-4f7i)
- [2026-04-23 Incident Thread (GitHub community)](https://github.com/orgs/community/discussions/193645)

Production examples:
- [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
- [How Anthropic teams use Claude Code (Claude blog)](https://claude.com/blog/how-anthropic-teams-use-claude-code)
- [Orchestrating AI Code Review at scale (Cloudflare blog)](https://blog.cloudflare.com/ai-code-review/)
- [The AI engineering stack we built internally (Cloudflare blog)](https://blog.cloudflare.com/internal-ai-engineering-stack/)
