# Tool Design for AI Agents — 2026 Reference

> A canonical, stack-neutral reference on designing tools that language-model agents actually use well: when to ship a custom tool vs. an MCP server vs. a hook, how to write descriptions that survive contact with the model, how to shape inputs and outputs, how to handle errors, and how to defend the tool surface against the dominant 2025–2026 failure modes.

Scope: practitioners building agents in any harness (Claude Code, Cursor, ChatGPT, Codex, in-house). Not anchored to a specific runtime. Where a concrete artifact is named (e.g., Claude Code's `Read`, MCP's `tools/list`), it is used as a case study, not a prescription.

---

## 1. Thesis: tool definitions are load-bearing prompt engineering

Anthropic's *Building Effective Agents* states the position bluntly: tool definitions and specifications should be given just as much prompt engineering attention as overall prompts. The team behind Anthropic's SWE-bench agent reports that they "spent more time optimizing our tools than the overall prompt."

This is more load-bearing in 2026 than it was in 2024, for three reasons:

1. **Agent loops have gotten longer.** A typical Claude Code or Cursor session in 2026 runs dozens to hundreds of tool calls. A bad description that nudges 5% of decisions toward the wrong tool compounds across the trajectory. Anthropic's 2025 retrospective on tool authoring notes that "bad tool descriptions can send agents down completely wrong paths."
2. **The tool surface has gotten wider.** MCP turned the per-host tool count from "tens" to "hundreds-to-thousands." On the Cloudflare API alone, naive MCP exposure consumes ~1.17M tokens of context — more than fits in any frontier model's window.
3. **Tool surfaces are now targets.** The 2025–2026 incident list (postmark-mcp backdoor, Invariant Labs GitHub MCP heist, the Supabase Cursor SQL exfiltration, the WhatsApp MCP rug-pull, CVE-2025-6514 in mcp-remote affecting 437K+ environments, the OX Security April 2026 family advisory) means a tool definition is now an attack surface as well as a prompting surface.

A tool definition is not a function signature. It is a contract between a deterministic system and a non-deterministic agent, written in natural language, evaluated against a model's training distribution, and adversarially probed by anyone who can influence its inputs or outputs.

Three heuristics from Anthropic's tool-authoring guidance, restated for emphasis:

- **Think-tokens.** Give the model enough tokens to "think" before it writes itself into a corner — i.e., do not force the model to emit a structured answer in the same turn it reasons.
- **Format-matching.** Keep formats close to what the model has seen naturally in training. JSON-with-comments, raw Markdown, and YAML are well-distributed; bespoke DSLs are not.
- **Minimize formatting overhead.** Avoid demanding the model maintain line counts, escape strings, or balance brackets across long outputs. Each piece of accounting work taxes reasoning budget.

A good tool definition includes: a one-line summary; parameter list with types, units, and constraints; at least one example invocation; the most common failure modes named; an explicit when-to-use and when-not-to-use; the boundary to adjacent tools ("use `grep` for content, `glob` for paths").

---

## 2. The tool surface taxonomy

MCP — the de facto inter-host protocol as of 2026 — distinguishes four primitives by *who decides when they run*. This distinction is load-bearing for both design and security; collapsing it is the source of many tool-design bugs.

| Primitive | Controller | Trigger | Typical use |
| --- | --- | --- | --- |
| **Tools** | Model | LLM emits a tool_use block | Side-effecting actions; queries with model-chosen arguments |
| **Resources** | Application/host | Host attaches content to context | Read-only data the model should *see* but not *choose* — file contents, schema docs |
| **Prompts** | User | Slash command, menu pick | Reusable templates ("summarize this PR", "review for SQL injection") |
| **Sampling** | Server-asks-client | Server requests model completion from client | Server-side agentic behaviors that need an LLM call without managing model access; HITL approval expected at both ends |

Why this matters: an agent that decides which file to read is doing *tool* work; a host that injects a fixed schema file into context is doing *resource* work; a user typing `/security-review` is invoking a *prompt*. Conflating them ("just expose everything as a tool") inflates the tool surface, gives the model decisions it should not be making, and removes human-in-the-loop affordances the host should be enforcing.

Non-MCP harnesses (Claude Code's built-in tools, OpenAI's function-calling, Cursor's commands) collapse some of these — Claude Code's slash commands and skills overlap with MCP prompts and resources, respectively — but the *role* distinction (model vs. application vs. user vs. server) survives the implementation choice.

---

## 3. When custom tool vs. MCP server vs. hook — the decision rule

This is the most-asked question of 2026. The Anthropic-blessed decision rule, distilled from Claude Code best-practices and *Effective Context Engineering*:

**Custom in-harness tool / skill** when the capability is bespoke to one project, lives as project artifacts, and does not need a separate process. Cheapest path — no extra runtime, no schema overhead, no per-session token tax. Example: a project-local `run_migration_safely.sh` exposed as a Claude Code skill or a Cursor command.

**MCP server** when the capability is reusable across hosts (Claude Code + Cursor + Claude Desktop + Codex CLI + Gemini CLI all benefit), needs authentication to an external system, or returns structured data the model should reason over. Worth the overhead only when reuse is genuine. Examples: Linear, GitHub, Notion, your company's internal API.

**Hook** when behavior must run *every time*, deterministically, with no model judgment in the loop. Hooks are 100% reliable; model-driven tool calls are 80%-ish (Anthropic's published number; not a promise). Examples: lint-on-write, append-to-ledger-on-commit, refuse-tool-if-secret-detected, format-on-save, run-tests-after-edit.

The decision rule in two questions:

1. *Does this need to happen every time, regardless of what the model thinks?* → Hook.
2. *Is this reusable across hosts, or does it need external auth?* → MCP server. Otherwise → custom in-harness tool/skill.

The trap: shipping an MCP server when a hook would do. Hooks survive model regressions, prompt changes, and adversarial inputs in a way tools cannot. The trap in the other direction: putting domain knowledge in a hook when it should be a skill the model can decline to use.

A second trap, specific to 2026: shipping an MCP server when a *skill* (SKILL.md, three-tier progressive disclosure) would do. Anthropic published the Agent Skills spec on 2025-12-18; within 48 hours Microsoft (VS Code), OpenAI (ChatGPT, Codex CLI), and by March 2026 32+ tools were reading the same SKILL.md format. Skills carry ~30–50 tokens of startup overhead per skill (just the YAML frontmatter); MCP tools carry their full description on every session. For large capability surfaces, skills beat tools on token cost by 1–2 orders of magnitude.

---

## 4. Tool description craft

The Anthropic tool-authoring post (2025) is direct: "Even small refinements to tool descriptions can yield dramatic improvements."

**Naming.** Verb-noun (`search_issues`, not `issues` or `issue_search`). Disambiguating prefixes when multiple sources exist (`asana_search`, `jira_search`, `github_search`, never bare `search`). Two-layer namespacing for large surfaces (`asana_projects_search`, `asana_users_search`). Anthropic explicitly reports that "prefix- and suffix-based namespacing... have non-trivial effects on tool-use evaluations."

**Description structure that models actually parse.** One-line summary first (this is what shows in the picker UI and is what the model anchors on under load). Then parameters with types *and units*. Then one or two example invocations. Then named failure modes. Then explicit boundaries to adjacent tools. Anthropic's framing: write the description "as you would describe the tool to a new hire on your team."

**Parameter design.** Minimize required parameters; every required arg is a chance for the model to bail or hallucinate. Prefer `user_id` to `user` — Anthropic specifically cites this ambiguity. Use enums sparingly: a 20-value enum that excludes the right answer pushes the model to a wrong neighbor, where a free-text field with validation would have surfaced the mismatch. Reserve a free-text `notes` or `reasoning` field for caveats the schema cannot express.

**Examples in the description body.** Show the model what it has seen. Concrete invocations with realistic arguments beat abstract type signatures. If the tool returns structured data, show one realistic result, with the field names the model will need to reference downstream.

**The "tool name as namespace" problem.** When two MCP servers both expose a `search` tool, the model picks based on description distance from the prompt — a coin flip in the worst case. Namespace explicitly at the tool name, not just the server name. Hosts that auto-prefix help, but do not rely on the host: name the tool `linear_search_issues`, not `search`.

---

## 5. Input and output schema design

**JSON Schema is the lingua franca.** MCP, OpenAI function calling, Anthropic tool use, and most agent frameworks accept JSON Schema directly. TypeScript types or Pydantic models are fine as authoring surfaces — most teams generate JSON Schema from them — but the on-the-wire contract is JSON Schema.

**Strict mode: when to enforce.** Anthropic's 2026 Structured Outputs feature exposes two switches:
- `tools[].strict: true` — guarantees the arguments the model emits conform to the tool's input schema. Type-safe function calls in agentic loops.
- `output_config.format: { type: "json_schema", schema: {...} }` — constrains the top-level response (not a tool call) to a schema.

Use `strict: true` for tools where schema-conformant garbage is preferable to a half-typed call your runtime will reject (i.e., almost always for production tools). Allow non-strict only when the model's ability to emit free-text in a `notes` field is load-bearing for the task — and even then, prefer a strict schema with an optional free-text field.

Note: OpenAI publishes a similar `strict: true` flag with different schema-subset restrictions (no `oneOf`, limited recursion). Cross-host portability requires staying in the intersection of the two.

**Schema validation is the cheap defense.** A 20-line input validator catches the long tail of model-emitted garbage that does not type-check, before it reaches business logic. This is also the first checkpoint where you can return a *helpful* error message that steers the model — see §7.

**Reserved fields for uncertainty.** Add optional `confidence: number` (0–1), `reasoning: string`, or `notes: string` to the output schema. Models that have been trained to express uncertainty will use them; models that haven't will not, and you lose nothing.

**Output schemas (MCP).** MCP 2025-06-18 adds an optional `outputSchema` to tool definitions. Servers MUST return structured results conforming to it; clients SHOULD validate. This makes downstream tool composition (§9) far more reliable: a tool that consumes another tool's output can rely on the field shape.

---

## 6. Tool result handling

Tool returns are the single largest source of context bloat in 2026 agent loops. A 2,000-token tool result that the agent referenced once and never again, sitting in context across 50 turns, costs 100,000 token-turns of attention budget.

**Length budgets per tool.** Claude Code restricts tool responses to ~25,000 tokens by default; Anthropic recommends this as a sensible per-tool cap. Implement pagination, range selection, filtering, and truncation with sensible defaults. A tool that returns "all rows" by default is a tool that will, eventually, return more rows than the context can hold.

**Cap at write time vs. lift-and-summarize on read vs. just-in-time retrieval.** Three patterns, in increasing order of complexity:
- *Cap at write*: tool returns at most N tokens, with a pagination cursor for "more."
- *Lift-and-summarize on read*: tool stores full result on disk/in a store, returns a summary + handle; agent can re-fetch a slice via a second tool.
- *Just-in-time retrieval*: tool returns only an identifier; downstream tools fetch the slice they need. This is the pattern behind Claude Code's `Read(path, offset, limit)` and behind Cloudflare's Code Mode (§8).

**Tool result clearing.** Anthropic's late-2025 Claude Developer Platform feature elides raw tool results from context after they have been "consumed" by subsequent model turns — i.e., once the agent has reasoned over the result, the raw blob is replaced by a placeholder. This is invisible to the model's reasoning chain but reclaims context for long sessions. Treat this as the floor, not the ceiling; for long loops, also use subagents (separate context windows that report back summaries).

**Content-type tagging.** Tag the content type before flowing back to the model. `text/plain`, `text/html`, `application/json`, `image/png` — MCP supports this via the `content[]` discriminator. The model uses the tag both for parsing and for trust: HTML from a web fetch should be treated differently from JSON from your own server.

**Untrusted-data envelopes.** This is both a context-engineering pattern and a safety pattern (§10). Wrap any tool result that contains content from outside your trust boundary in a clearly delimited envelope, with an instruction in the system prompt that text inside the envelope is *data, not instructions*. Microsoft's "Spotlighting" research formalizes three modes — delimiting (random delimiter strings), datamarking (special tokens interspersed in untrusted text), and encoding (base64/ROT13 transformation). Delimiting is the cheapest and most widely deployed.

**Escape model-control tokens.** Strip or escape sequences like `</tool_result>`, `<|im_end|>`, `<|im_start|>`, `[INST]`, and chat-template control tokens from tool result bodies before they reach the model. An attacker who can write into a tool's output (a Jira ticket title, a Notion page body, a webpage) and can emit a chat-template close-tag can break out of the data envelope on naive harnesses.

**Length-bound everything.** Cap not just the happy path but the adversarial path. An attacker who can return a 50,000-token tool result has 50,000 tokens to set up an elaborate jailbreak. Truncate at the host before the model ever sees it.

---

## 7. Tool error reporting

MCP specifies two error channels:

1. **JSON-RPC protocol errors** — `-32600` through `-32603` (parse/invalid-request/method-not-found/invalid-params/internal) and `-32000` through `-32099` (server-defined). For: tool name unknown, arguments fail schema validation, server is unreachable. Host should surface these to the user; the model usually cannot recover from them.

2. **Tool execution errors** — JSON-RPC result with `isError: true` and the error described in the `content` text. For: API rate-limited, file not found, business-logic refusal, partial results with caveats. The model *should* reason about these and may retry, adjust arguments, or fall back.

The split matters. A "user not found" error returned as an `isError: true` tool result lets the model say "I'll try a different ID"; the same condition returned as JSON-RPC `-32602` kills the call without giving the model a chance to recover. Conversely, a malformed argument should *not* return `isError: true` (the model will try to reason about an infrastructure failure as if it were a business condition); it should return JSON-RPC `-32602` so the host can re-validate.

**Error message craft.** Anthropic's tool-authoring guidance: errors should "provide specific and actionable improvements, rather than opaque error codes or tracebacks." Bad: `ValueError: invalid input`. Good: `Invalid date format for 'due_date'. Expected ISO-8601 (e.g., 2026-05-17). Got: '5/17/2026'.` The model will reformat and retry; with the bad version, it will guess.

**Retry, idempotency, timeouts.** Retries belong at the harness layer (exponential backoff with jitter), not the model layer. Idempotency keys are essential for any mutating tool that the harness may retry: a `create_issue(idempotency_key=<uuid>)` that the server deduplicates is the only safe pattern. Timeouts must be explicit — long-running tools should return a job handle and expose a `get_status(job_id)` tool, not block the agent loop.

---

## 8. The bloated-tool-set anti-pattern

Anthropic's *Effective Context Engineering* names this as the #1 tool-related failure mode: "bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use." The diagnostic is sharp: "If a human engineer can't definitively say which tool should be used in a given situation, an LLM can't be expected to do better."

Every MCP server in a host config inflates the system prompt with that server's tool descriptions. A 52-tool internal portal at Cloudflare consumed ~9,400 tokens *before any user prompt*. A naive exposure of the full Cloudflare API would consume 1.17M tokens — exceeding the context window of every frontier model.

**Cloudflare Code Mode.** Cloudflare's April 2026 pattern collapses N tool definitions behind a pair: `portal_codemode_search` (agent writes JavaScript to query the OpenAPI spec) and `portal_codemode_execute` (agent writes JavaScript to make authenticated calls, run in a sandboxed V8 isolate). The 52-tool portal collapses to 2 tools and ~600 tokens — a 94% reduction. The full Cloudflare API surface (~2,500 endpoints) collapses to roughly 1,000 tokens — a 99.9% reduction.

The mechanism: replace declarative tool definitions with a general execution environment + discovery. The model writes code, the code runs in a sandbox, the result returns. This trades schema enforcement (you cannot pre-validate arbitrary code) for context efficiency (the tool surface is now bounded). For trusted internal portals it is the right trade; for adversarial inputs it is the wrong one.

**Anthropic Code Skills (the orthogonal pattern).** Skills (SKILL.md, three-tier progressive disclosure) bring tool surfaces down by *not loading them until needed*. At startup, only the skill's name and one-line description load (~30–50 tokens per skill). When the host determines a skill is relevant, the full SKILL.md body loads. Auxiliary files referenced from the skill are loaded only when the skill explicitly references them. Even Anthropic recommends this for large capability surfaces.

**Decision rule for large surfaces.** Trusted internal API + execution-friendly model → Code Mode. Reusable workflows + multi-host → Skills. External, untrusted API → curated MCP server with a *minimal* viable tool set (Anthropic's phrasing: "a few thoughtful tools targeting specific high-impact workflows" rather than wrapping all API endpoints).

---

## 9. MCP-specific concerns

**Indirect prompt injection through tool descriptions or returned content.** The dominant unsolved problem in MCP. Anthropic's writing-tools post and *Effective Context Engineering* both treat this as a first-class threat in 2026. Real-world 2025–2026 incidents include:

- Invariant Labs' GitHub MCP "Issue Heist" (May 2025): an attacker posts a public GitHub issue with hidden instructions; an agent reading the issue is coerced into leaking data from private repos.
- The Supabase Cursor incident (mid-2025): an agent with privileged service-role DB access processes a support ticket; the ticket contains SQL instructions; the agent executes them and exfiltrates integration tokens.
- The WhatsApp MCP rug-pull demo (Invariant Labs, April 2025): a server first advertises a benign tool; on the second launch it returns a new description for the same tool name embedding hidden routing instructions to redirect every `send_message`.
- The postmark-mcp backdoor (npm, September 2025): 15 clean versions, then v1.0.16 silently BCCs every outgoing email to an attacker. ~300 organizations affected before disclosure.
- Anthropic's own Git MCP RCE chain (December 2025).
- The OX Security April 2026 family advisory on metadata poisoning rates (~5.5% of public MCP servers shipped with attack-suggestive metadata).
- CVE-2025-6514 (mcp-remote OAuth proxy RCE, 437K+ environments).

**Tool-name collisions across servers.** Two servers exposing `search` is a coin flip; namespace explicitly (§4). Hosts should also surface the *source* of each tool to the user, not just the name.

**Rug-pull (descriptions change mid-session).** Per spec, `tools/list` is *not* static — servers may emit `notifications/tools/list_changed` and serve updated definitions. An attacker who controls a server can ship benign tools through approval, then mutate them. Defense: clients should hash tool definitions on first scan and alert on drift (mcp-scan does this). The ETDI proposal (arXiv 2506.01333) adds cryptographic signing of tool definitions with policy-based access control — the likely 2026–2027 direction.

**Auth tokens in client config.** Leaked in nearly every "I shared my Claude config" incident in 2025–2026. Defense: never commit tokens to dotfiles; use OS keychain (macOS Keychain, Linux Secret Service) or OAuth flows with short-lived tokens. The OAuth standard for MCP servers is now widely supported; prefer it over static bearer tokens.

---

## 10. Patterns for tool-heavy workflows

**Routing pattern.** A cheap classifier model (or a small first-pass call to the main model) picks the right tool from a large surface; the expensive tool then executes. Reduces the "tool ambiguity" failure and lets you use a smaller model for the routing step.

**Tool composition.** Build chains: `search` returns IDs → `filter` narrows → `read` fetches content. Each step has a narrow input and a narrow output, schema-validated at the seam. This is what Claude Code's `Grep` → `Read` → `Edit` pipeline demonstrates: each tool is single-purpose, the seams are typed, the agent composes them.

**Retry with exponential backoff at the harness, not the model.** The model should never see "the server returned 503; retrying in 2s" — that's harness work. The model should see either a successful result or a final error.

**Cache idempotent results.** A tool that fetches a stable resource (a file by SHA, a Notion page by ID-and-version) can be memoized at the harness layer. Saves tokens and latency, and lets you treat tool calls as referentially transparent inside a session.

**Subagents for investigation.** Anthropic's recommendation: when an agent needs to explore a large surface (read many files, scan a log, traverse a graph), delegate to a subagent with its own context. The subagent reports back a summary; the parent's context stays clean. This is the most leveraged context-management technique in 2026.

---

## 11. Production examples of well-designed tools

**Claude Code's `Read`, `Edit`, `Grep`, `Glob`.** A case study in disambiguated, narrow-purpose tools. `Read` reads a file with optional `offset`/`limit` — pagination is built in. `Grep` searches content; `Glob` matches paths; the two never overlap. `Edit` requires the caller to have already read the file (the harness enforces this), making the model less likely to edit blind. Each tool's description names its peer ("use `Grep` for content searches; use `Glob` for filename patterns"). The boundary-naming is the load-bearing detail.

**The MCP filesystem server.** Sandboxed roots are the auth model: the server is started with a list of allowed root directories; the model cannot escape them, regardless of what the description says or what the model decides. This is the right pattern — auth is enforced at the server, not described in the tool definition.

**The MCP GitHub server.** Domain-specific tools (`create_pr`, `add_comment`, `list_issues`) rather than a generic `http_post`. The model reasons about GitHub-shaped operations, not about HTTP. Schema validation rejects malformed PRs at the boundary, and the auth scope is constrained by the underlying GitHub PAT (not by the tool description).

---

## 12. Anti-patterns to flag

- **Generic `execute_command` / `shell` tools that bypass schema validation.** The model can emit anything; the host runs it. This is the source of nearly every MCP RCE in the 2025–2026 incident list. Mitigations: explicit allow-lists, sandboxed execution, no shell metacharacter interpretation.
- **Tools with single-letter or ambiguous names.** `r`, `e`, `do`, `run`, `exec`, `tool1`. Models confuse them with each other and with built-in primitives.
- **Tools that return unbounded output.** A `list_all_records()` with no pagination is a context bomb. Always cap, always paginate.
- **Tools that don't distinguish user-error from server-error in results.** The model cannot recover from infrastructure failures by reasoning, and should not be asked to. Separate channels (§7).
- **Tools that mutate state without idempotency keys.** A retry on a non-idempotent `create_*` call double-creates. Every mutating tool needs an idempotency key argument, deduplicated by the server.
- **Tool surfaces where N tools could be replaced by 1 with a parameter.** `get_user_by_email`, `get_user_by_id`, `get_user_by_name` should be one tool with a discriminated-union argument. The opposite mistake (one tool with 20 modes hidden behind a `mode: enum[...]` argument) is also bad, but the first is more common.
- **Bare `search` in a multi-source agent.** Namespace it. The model will pick wrong.
- **Tool descriptions copied from API docs verbatim.** API docs explain the implementation to a human reader; tool descriptions explain the contract to a model. Different audiences, different texts.
- **Resources exposed as tools.** A file-by-path read is a *resource* (application-controlled); a content-search across many files is a *tool* (model-controlled). Collapsing both into "tools" removes the host's ability to inject the right context proactively and makes the model do extra navigation work.
- **`tools/list` definitions that change between sessions without versioning.** Rug-pull attack surface (§9). Hash on first scan, alert on drift.

---

## 13. Top 12 tool-design practices, ranked by leverage

1. **Minimize the tool surface.** Fewer, more thoughtful tools beat many redundant ones. Anthropic's stated #1 failure mode is bloated tool sets.
2. **Namespace every tool name.** `service_verb_resource`, never bare `search` or `read` in a multi-source agent.
3. **Treat tool descriptions as prompt engineering.** A new-hire-quality description with examples, parameter units, failure modes named, and boundaries to peer tools.
4. **Length-bound every tool result.** ~25K tokens default, with pagination/range/filter parameters. Truncate at the host.
5. **Wrap untrusted tool output in delimited envelopes.** Spotlighting or equivalent. Escape model-control tokens at the host.
6. **Use the right primitive.** Hook for "every time"; skill for reusable workflows; MCP server for cross-host reuse; tool for model-decided actions. Don't ship an MCP server when a hook would do.
7. **Strict schema validation on inputs.** `tools[].strict: true` in 2026 Anthropic API; equivalent on OpenAI. Helpful error messages on failure.
8. **Separate user-error from server-error in results.** `isError: true` for business conditions; JSON-RPC errors for infrastructure. Different recovery channels.
9. **Idempotency keys on every mutating tool.** Retries are inevitable; double-mutation is not.
10. **Subagents for investigation; tool result clearing for long loops.** Both keep the main context clean across long trajectories.
11. **Cryptographic identity for MCP tools you depend on.** Pin hashes, alert on drift, prefer signed-definition servers when available.
12. **Evaluation-driven development.** Anthropic's tool-authoring post is explicit: stand up a prototype, run a held-out eval (BFCL, tau-bench, or a task-specific harness), measure each refinement. "Even small refinements to tool descriptions can yield dramatic improvements" — measure them.

---

## Sources

Anthropic engineering:
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Writing Effective Tools for AI Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Structured Outputs — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

MCP specification and ecosystem:
- [MCP Tools — Server Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [MCP Prompts — Server Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)
- [Understanding MCP features — WorkOS](https://workos.com/blog/mcp-features-guide)

Code Mode and tool-surface reduction:
- [Code Mode: give agents an entire API in 1,000 tokens — Cloudflare](https://blog.cloudflare.com/code-mode-mcp/)
- [Scaling MCP adoption: reference architecture — Cloudflare](https://blog.cloudflare.com/enterprise-mcp/)
- [Cloudflare Code Mode MCP Server (coverage) — InfoQ](https://www.infoq.com/news/2026/04/cloudflare-code-mode-mcp-server/)

Skills and progressive disclosure:
- [Agent Skills: Progressive Disclosure as a System Design Pattern](https://www.newsletter.swirlai.com/p/agent-skills-progressive-disclosure)
- [The Complete Guide to Building Skills for Claude — Anthropic](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

MCP security incidents and defenses:
- [MCP Horror Stories: The GitHub Prompt Injection Data Heist — Docker](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/)
- [The State of MCP Security 2026 — PipeLab](https://pipelab.org/blog/state-of-mcp-security-2026/)
- [MCP Tool Poisoning and Rug Pulls — FlowHunt](https://www.flowhunt.io/blog/mcp-tool-poisoning-rug-pulls-safe-tool-design/)
- [MCP Security in 2026: Real CVEs, Exploit Chains — policyascode.dev](https://policyascode.dev/blog/mcp-security-vulnerabilities-2026/)
- [ETDI: Mitigating Tool Squatting and Rug Pull Attacks in MCP (arXiv 2506.01333)](https://arxiv.org/html/2506.01333v1)
- [How Microsoft Defends Against Indirect Prompt Injection — MSRC](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)
- [Indirect Prompt Injection in the Wild — Help Net Security (April 2026)](https://www.helpnetsecurity.com/2026/04/24/indirect-prompt-injection-in-the-wild/)

Tool-use evaluation:
- [τ-bench: A Benchmark for Tool-Agent-User Interaction (arXiv 2406.12045)](https://arxiv.org/pdf/2406.12045)
- [The Berkeley Function Calling Leaderboard (BFCL) — OpenReview](https://openreview.net/forum?id=2GmDdhBdDk)
- [Function Calling Benchmarks Leaderboard 2026](https://awesomeagents.ai/leaderboards/function-calling-benchmarks-leaderboard/)
