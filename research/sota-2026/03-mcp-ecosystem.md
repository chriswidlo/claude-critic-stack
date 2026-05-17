# SOTA-2026: The Model Context Protocol Ecosystem

*Survey vintage: May 2026. All claims are cited; absence of a citation means the claim is the author's synthesis, not a sourced fact.*

---

## 1. What MCP is and isn't

The Model Context Protocol is a JSON-RPC-based, stateful session protocol that standardises how a host AI application talks to external context providers. The reference specification lives at [modelcontextprotocol.io](https://modelcontextprotocol.io) and is now stewarded by the Linux Foundation's Agentic AI Foundation — Anthropic donated the spec on December 9, 2025, with OpenAI, Google, Microsoft, AWS, Cloudflare, and Bloomberg joining as platinum members ([Toloka: Future of MCP](https://toloka.ai/blog/the-future-of-mcp-enterprise-adoption/)).

### Load-bearing concepts

The spec defines a tight set of primitives, each carrying very specific semantics ([MCP Prompts spec, 2025-06-18 revision](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts); [Resources concepts](https://modelcontextprotocol.info/docs/concepts/resources/)):

- **Server** — an external process that exposes one or more primitives. Stateless or stateful, local or remote.
- **Client** — a 1:1 connection from a host to a particular server. A host (e.g. Claude Desktop, Cursor, Claude Code) typically manages many clients.
- **Resources** — read-only data identified by URI; text or binary; subscribe/list/read. *Application-controlled* — the host decides when to feed them to the model.
- **Tools** — executable actions with JSON-schema-described inputs. *Model-controlled* — the LLM decides when to call them.
- **Prompts** — reusable templates exposed by the server. *User-controlled* — the user explicitly selects them (slash commands, etc.).
- **Sampling** — the reverse channel: a server asks the *client* to run an LLM completion on the server's behalf. The MCP spec requires human-in-the-loop approval at both the request and the response stage ([Webfuse 2026 cheat sheet](https://www.webfuse.com/mcp-cheat-sheet)).
- **Completion** — argument auto-completion for prompts and resource templates; small but load-bearing for UX.
- **Capability negotiation** — at session init, client and server publish which features they support. No assumption that "MCP server" means "all primitives." Most servers are tools-only.

The "who controls invocation" axis (model / user / application) is the most under-appreciated part of the spec. It tells you, at design time, which primitive to expose for a given capability — and it's what an MCP client looks at when deciding how to surface a server's features.

### What MCP *isn't*

- Not a transport. MCP rides on **stdio**, **Streamable HTTP** (the modern standard), or the now-deprecated **HTTP+SSE** ([Apigene 2026 transports](https://apigene.ai/blog/mcp-sse-vs-stdio); [MCPcat transport comparison](https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/)).
- Not an agent framework. MCP gives an agent access to context and capabilities. The loop, planning, and memory are the host's problem.
- Not a tool-use API. Claude's native tool-use is a per-request capability description; MCP is a *persistent* server you connect to. The two coexist — a host translates MCP tools into native tool-use schemas at the wire level.

### Where MCP fits relative to Claude Code's other extension points

Claude Code has at least four distinct extension surfaces that often get conflated ([alexop.dev: Claude Code full stack](https://alexop.dev/posts/understanding-claude-code-full-stack/); [Morph LLM: Skills vs MCP vs Plugins](https://www.morphllm.com/claude-code-skills-mcp-plugins); [Skiln: decision guide](https://skiln.co/blog/claude-code-plugins-vs-skills-vs-mcp-decision-guide)):

| Surface | Triggered by | Right when… |
|---|---|---|
| **Claude tool-use API** | Per-request schema in the API call | You're building a one-off agent, not a reusable integration. |
| **Claude Code custom tools** (`.claude/commands/`, agents) | User/orchestrator invocation | The capability is bespoke to the project and lives as project artifacts. |
| **Hooks** (`PreToolUse`, `PostToolUse`, `SessionStart`, etc.) | Lifecycle event | The action must happen *every* time, deterministically, without the model thinking. Enforcement, logging, formatting. |
| **MCP server** | Model decision (tool) / user selection (prompt) / host decision (resource) | The capability is shared across multiple hosts/projects, is stateful, or wraps an external system. |

The shorthand: **hooks enforce, MCP extends, custom tools encode project-local knowledge, the API is the wire underneath all of them**. A common anti-pattern is reaching for MCP when a hook would do (because hooks don't burn context tokens) or for a hook when MCP would do (because hooks can't return rich data the model can reason about).

### Ecosystem maturity in 2026

By May 2026, the ecosystem hosts roughly **21,500+ servers indexed on Glama**, **7,000+ on Smithery**, and **25,000+ aggregated across the major registries** ([Truefoundry: best MCP registries](https://www.truefoundry.com/blog/best-mcp-registries); [Automation Switch: where to find MCP servers](https://automationswitch.com/ai-workflows/where-to-find-mcp-servers-2026)). The Linux Foundation now operates the canonical machine-readable [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/). Categories shake out roughly into: developer infrastructure (Git, CI, observability), databases (Postgres, BigQuery, vector stores), productivity SaaS (Notion, Slack, Linear, Jira), web/scraping (Firecrawl, Brave, Playwright), and bespoke enterprise integrations.

---

## 2. Top production MCP servers

### Anthropic-published reference servers

The [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) repo has been deliberately *shrunk* during 2025 — many of the most-used servers were moved to [servers-archived](https://github.com/modelcontextprotocol/servers-archived) once the vendor took ownership. As of May 2026 the active reference servers are:

- **Everything** — a kitchen-sink demo exercising all primitives; useful as an SDK reference, not a production server.
- **Fetch** — pull a URL, convert to text, return. Use for ad-hoc reading; do not give an unsupervised agent.
- **Filesystem** — sandboxed file ops with allow-listed roots. The single most-used MCP server in the wild, and (see §4) a load-bearing element of every published prompt-injection chain.
- **Git** — read/search/manipulate repos. The subject of CVE-2025-68143/68144/68145, fixed in version 2.25.12.18 ([The Register, 2026-01-20](https://www.theregister.com/2026/01/20/anthropic_prompt_injection_flaws/)).
- **Memory** — knowledge-graph persistence across sessions.
- **Sequential Thinking** — a thinking-trace primitive exposed as resources.
- **Time** — timezone math.

The archived list (now maintained elsewhere or replaced by official vendor servers) includes GitHub, GitLab, Postgres, SQLite, Puppeteer, Slack, Sentry, Brave Search, Google Drive, Google Maps, Redis, AWS KB Retrieval, and EverArt. The migration pattern is consistent: Anthropic shipped a reference, the vendor stood up an authoritative server, and the reference was archived to avoid a confusing two-source situation.

### Vendor-official remote servers worth knowing

The 2026 shift is from local stdio servers to **vendor-hosted Streamable HTTP endpoints with OAuth** ([Apigene: MCP server directory](https://apigene.ai/blog/mcp-server-directory); [MCP Bundles: definitive list](https://www.mcpbundles.com/blog/best-mcp-servers)):

- **GitHub** — official; PRs, issues, code search. The reference target for the May 2025 Invariant Labs prompt-injection disclosure.
- **Sentry** — error and release context; remote endpoint launched Feb 2026.
- **Stripe** — customers, charges, refunds, payment links; payments-grade auth.
- **Linear** — issue and project graph; migrated from stdio to remote HTTP in 2026.
- **Notion** — workspace pages and databases via OAuth ([Notion MCP docs](https://developers.notion.com/guides/mcp/overview)).
- **Slack** — official, with admin scopes.
- **Atlassian, HubSpot, Neon, Vercel, Supabase** — all shipped remote MCP endpoints during 2026.
- **Cloudflare** — thirteen first-party servers (Workers, R2, D1, Analytics, Browser Rendering, etc.) running on Durable Objects ([Cloudflare: thirteen new MCP servers](https://blog.cloudflare.com/thirteen-new-mcp-servers-from-cloudflare/)).

### Community servers worth knowing

From [awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) and adoption signal (>1k stars, active in last 90 days):

- **Playwright MCP** ([executeautomation/mcp-playwright](https://github.com/executeautomation/mcp-playwright)) — browser automation; the de facto Puppeteer replacement.
- **Firecrawl MCP** — web scraping with markdown conversion; enterprise-backed.
- **Brave Search MCP** — clean web access without a browser pipeline.
- **Qdrant MCP** ([qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant/)) — vector search as memory.
- **Neo4j MCP** ([neo4j-contrib/mcp-neo4j](https://github.com/neo4j-contrib/mcp-neo4j/)) — graph queries.
- **DBHub** — universal DB connector spanning MySQL/Postgres/SQLite/DuckDB.
- **Docker MCP** ([QuantGeekDev/docker-mcp](https://github.com/QuantGeekDev/docker-mcp)) — container inspection and log access.
- **Kubernetes MCP** ([Flux159/mcp-server-kubernetes](https://github.com/Flux159/mcp-server-kubernetes)) — cluster resource ops.

### Registries and discovery

- **[registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/)** — official, machine-readable, the source clients should prefer.
- **[Glama](https://glama.ai/mcp/servers)** — largest directory (~21.5k indexed servers, daily refresh, gateway with logging).
- **[Smithery](https://smithery.ai)** — app-store UX, hosted-server option, ~7k servers, `smithery mcp publish` CLI.
- **[PulseMCP](https://www.pulsemcp.com)** — browsable directory with usage signal.
- **[MCPfinder](https://mcpfinder.dev)** — meta-index aggregating the three above for AI-first discovery ([mcpfinder/mcpfinder](https://github.com/mcpfinder/mcpfinder)).

Quality filter from multiple 2026 surveys: **active maintenance in the last 90 days, public install instructions, >1k stars or official vendor backing** ([SkillsLLM: best MCP servers 2026](https://skillsllm.com/blog/best-mcp-servers-2026)). The unstated corollary: most of the 25k+ servers are abandoned weekend projects; the long tail is hostile territory.

---

## 3. MCP server design patterns

### Resource-first vs tool-first

- **Tool-first** is the default in practice — most servers expose nothing but tools. Easier to test, easier for the model to discover.
- **Resource-first** is what the spec was *designed* for: stateful data that the host application chooses when to inject into context. It composes better with long-running sessions because reads are explicit and cache-friendly.

The rule of thumb: if the data is "stuff the model might want to look at," it's a resource; if it's "something the model needs to *do*," it's a tool. Many production servers conflate the two by exposing read tools (`list_files`, `get_issue`) when resources would compose better with the host's context-management strategy.

### Authentication

- **No auth** — only for trusted local stdio servers reading public data.
- **API key in env var** — the dominant pattern for local servers; the spec explicitly recommends *against* OAuth for stdio ([Practical DevSecOps: OAuth 2.1 best practices](https://www.practical-devsecops.com/mcp-oauth-2-1-implementation/)).
- **OAuth 2.1 with PKCE** — mandatory in the spec for remote HTTP servers. Refresh-token family revocation and resource-indicator validation are required, not optional ([Auth0: secure remote MCP](https://auth0.com/blog/secure-and-deploy-remote-mcp-servers-with-auth0-and-cloudflare/)).
- **SSO-integrated enterprise auth** — the 2026 roadmap explicitly targets "paved paths away from static client secrets toward SSO-integrated flows (Cross-App Access)" ([MCP roadmap](https://modelcontextprotocol.io/development/roadmap)).

The architectural recommendation: keep the MCP server as a pure resource server, validate tokens, enforce scopes, and let a dedicated authorization server handle identity and issuance.

### Long-running operations

The **Tasks primitive** (SEP-1686) gives a "call-now / fetch-later" pattern. The 2026 roadmap names retry semantics and result-expiry policies as the gaps the Agents Working Group needs to close ([MCP roadmap, 2026-03-05](https://modelcontextprotocol.io/development/roadmap)). Until then, common practice is server-side polling tokens or out-of-band notification via the existing SSE channel.

### Streaming vs batched

Streamable HTTP supports inline SSE for response streaming; stdio supports it via newline-delimited JSON-RPC frames. The 2026 spec **does not** yet have a first-class streamed-result type for tool calls — that's an "On the Horizon" item, cross-cutting transport and schema. Practical advice: batch results unless your transport already streams; don't invent a custom streaming convention.

### Error reporting

JSON-RPC `error` objects are the only sanctioned channel. Best practice is to use standard codes (-32600 through -32603 for protocol errors, -32000 to -32099 for server-defined) and put structured error data in the `data` field. Returning errors as successful tool responses with `isError: true` is also part of the spec, and is the better choice for tool failures the model should reason about, vs. infrastructure failures the host should surface.

### Security: the big one

**Indirect prompt injection through resource content is the dominant unsolved problem in MCP.** Every published attack chain in 2025–2026 follows the same shape: an attacker plants instructions in something a server will read (a GitHub issue, an email, a doc, a support ticket), the model treats those instructions as legitimate, and the next tool call exfiltrates data or executes code. Concrete incidents:

- **GitHub MCP prompt-injection data heist (May 2025)** — public-repo issue with hidden instructions caused agents to pull data from private repos and write it to attacker-controlled PRs ([Invariant Labs disclosure](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks); [Docker: MCP horror stories](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/)).
- **Supabase Cursor incident (mid-2025)** — an agent running with privileged service-role access processed support tickets whose user content embedded SQL; the agent leaked integration tokens into a public thread ([Practical DevSecOps](https://www.practical-devsecops.com/mcp-security-vulnerabilities/)).
- **Anthropic Git MCP RCE chain (disclosed June 2025, fixed Dec 2025)** — CVE-2025-68143/68144/68145; argument injection and path-bypass flaws chained with Filesystem MCP for full RCE via Git smudge/clean filters ([The Register](https://www.theregister.com/2026/01/20/anthropic_prompt_injection_flaws/)).
- **postmark-mcp backdoor (Sep 2025)** — fifteen clean releases (1.0.0–1.0.15) followed by a silent BCC-exfiltration update; weeks of undetected operation ([CyberArk: poison everywhere](https://www.cyberark.com/resources/threat-research-blog/poison-everywhere-no-output-from-your-mcp-server-is-safe)).

The class lessons:
1. **Tool poisoning** — malicious instructions in tool descriptions, parameter names, defaults, enums, even nested schema docs. Every field is an injection surface (CyberArk's "Poison Everywhere").
2. **Rug pull** — `tools/list` returns benign descriptions on install, malicious ones mid-session. The spec *permits* description changes, so a one-time install-time scan is insufficient. Invariant Labs found roughly **5.5% of public MCP servers carry poisoned metadata** ([PipeLab: state of MCP security 2026](https://pipelab.org/blog/state-of-mcp-security-2026/)).
3. **Cross-server chaining** — a single benign server is rarely the whole exploit; the chain crosses Git + Filesystem, GitHub + Slack, etc.

Microsoft's recommended defenses are **AI Prompt Shields** (spotlighting, datamarking, delimiter discipline to distinguish trusted instruction from untrusted content), plus standard supply-chain hygiene ([Microsoft Developer Blog: protecting against indirect injection in MCP](https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp)). Cloudflare's gateway pattern adds tenant-level audit logging and shadow-MCP detection ([Cloudflare enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/)).

---

## 4. Building a custom MCP server

### SDKs

The two canonical SDKs are:

- **[TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)** (`@modelcontextprotocol/sdk`) — the reference; ESM-only, requires `"module": "Node16"` in `tsconfig.json` or you get cryptic import errors ([freeCodeCamp: custom TS MCP server](https://www.freecodecamp.org/news/how-to-build-a-custom-mcp-server-with-typescript-a-handbook-for-developers/)).
- **[Python SDK](https://github.com/modelcontextprotocol/python-sdk)** — `mcp` package; the high-level `FastMCP` decorator API is the right default for Python stacks and has dramatically less boilerplate than the TS SDK.

Beyond those, there are tiered community SDKs for Go, Rust, Java, C#, and Kotlin — see SEP-1730 for the official tiering system that flags which SDKs track the spec most closely. The TypeScript and Python SDKs are Tier 1.

### Skeleton

A minimum TS server is roughly: import `Server` and `StdioServerTransport`, instantiate with name+version, register tools via `server.setRequestHandler(CallToolRequestSchema, ...)` (or `server.tool()` in the high-level API), and `server.connect(transport)`. Under 50 lines including JSON-schema definitions. FastMCP equivalents are shorter still.

### Transport choice

- **stdio** — local dev, IDE integrations, anything single-client and process-local. Cannot scale, cannot be remote ([Roo Code: MCP server transports](https://docs.roocode.com/features/mcp/server-transports)).
- **Streamable HTTP** — modern remote standard; OAuth-friendly, scales horizontally, single endpoint for POST+SSE.
- **HTTP+SSE** — **deprecated**; do not start new work on it.

### Versioning

SemVer applies to the server's published version, but the more important contract is the **MCP protocol revision** declared at handshake (e.g. `2025-06-18`). Servers should accept any client revision they're compatible with and degrade gracefully on capability mismatch.

### Testing

The community has converged on a four-layer pattern ([dev.to: four MCP testing patterns](https://dev.to/klement_gunndu/your-mcp-server-has-no-tests-here-are-4-patterns-to-fix-that-2k59); [MCPcat: Inspector setup](https://mcpcat.io/guides/setting-up-mcp-inspector-server-testing/)):

1. **In-memory unit tests** on tool handlers — sub-second feedback.
2. **Schema validation tests** in CI — catch contract drift between code and declared JSON schemas.
3. **Parameterized edge cases** — boundary and type-handling failures.
4. **[MCP Inspector](https://github.com/modelcontextprotocol/inspector)** — manual exploratory testing via browser UI. (Note: CVE-2025-49596 was an RCE in older Inspector versions — keep it patched.)

A common debug trap: `console.log` corrupts stdio JSON-RPC frames. Use `console.error` (stderr) or write to a side log file.

### Custom MCP vs custom Claude Code tool vs hook

Worth restating concretely:

- **MCP server** when the capability is reusable across hosts (Claude Code + Cursor + Claude Desktop), needs auth to an external system, or returns structured data the model should reason about.
- **Claude Code custom tool / agent** when the capability is project-local and needs to know about project artifacts on disk. Cheaper than MCP — no extra process, no schema overhead, no token tax on every session.
- **Hook** when the behaviour must run *every time* and doesn't need model judgment. Lint-on-write, append-to-ledger-on-commit, refuse-tool-if-condition.

In this repo specifically, the 12-step workflow is overwhelmingly hook + custom-agent territory; MCP would be the wrong tool for, say, the path-discipline check.

---

## 5. MCP for our specific stack

This stack is Claude-Code-based, file-artifact-driven, and the near-term plan involves up to ten parallel `git worktree` sessions running the 12-step workflow concurrently. A few specific notes:

### Existing servers that would meaningfully extend the stack

- **Filesystem MCP** — would let canon-librarian and Explore agents read outside the repo without giving Claude Code raw shell access. The auth surface is allow-listed roots, which is closer to the privacy posture this repo's path-discipline rule wants than `Bash(cat ...)`.
- **Git MCP** (patched version) — would let session synthesis cite commit SHAs without shelling out. Marginal value; `git` over Bash is already fine and avoids the CVE history.
- **Sequential Thinking MCP** — overlaps with the existing `frame-challenger` and critic panel; would *not* fit because the panel's value is independent lens isolation, not a single thinking trace.
- **Memory MCP** — overlaps with `.claude/session-artifacts/`. The on-disk artifact pattern is *more* portable than a knowledge graph and grep-discoverable; Memory MCP would be a step backward.

The honest read: most general-purpose MCP servers add little here because the stack's value is in the on-disk artifact discipline, not in external system reach.

### What a custom "session-artifact querying" MCP server would look like

A speculative design (not a recommendation — see anti-patterns):

- **Resources**: one per session, URI `session://{id}/{artifact}`, returning the markdown body. Supports list, read, subscribe (so an orchestrator running in worktree A can react to artifact creation in worktree B).
- **Tools**: `find_sessions_by_label(primary_label)`, `find_contradictions(claim)`, `cite(artifact_uri)` — composable querying over the artifact corpus.
- **Prompts**: slash-installable templates like `/replay-frame {session-id}` and `/diff-syntheses {a} {b}`.

The honest test: does this beat `Grep` + `Read`? Today, probably not. The corpus is small enough that filesystem tools dominate. The case for a custom server gets stronger past ~100 sessions or once cross-session retrieval is a workflow primitive rather than an ad-hoc activity.

### Parallel-worktree concerns

MCP stdio servers are *single-client*: a stdio server spawned by one Claude Code session cannot be shared with another. Ten parallel worktrees means ten copies of every local stdio server, which is fine for stateless servers and disastrous for anything that holds a lock (e.g. SQLite without WAL, single-writer file handles). The mitigations:

- Prefer **Streamable HTTP** servers, even for local use, when you'll run many parallel sessions — one server process, many clients.
- For stdio servers, audit for file-locking behaviour; the Memory MCP's persistent-store and Filesystem MCP's write paths are the obvious concerns.
- The 2026 roadmap's stateless Streamable HTTP work ([MCP roadmap](https://modelcontextprotocol.io/development/roadmap)) is explicitly designed for this scale-out case; it isn't shipped yet, but it's the direction.

---

## 6. Anti-patterns

- **"MCP for everything."** Every MCP server in your config inflates the system prompt with tool descriptions, every one of which is a potential injection surface. Cloudflare's "Code Mode" pattern (collapse N servers behind a single `search` + `execute` pair) cut token cost 94% in their benchmarks ([Cloudflare enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/)). The lesson is to be miserly.
- **Trusting resource contents.** A document fetched via Fetch MCP, a GitHub issue read via the GitHub server, a Slack message read via the Slack server — all are *untrusted input* even if the *server* is trusted. Spotlighting / delimiter discipline is the minimum bar; least-privilege scoping is the real defense.
- **Tool name collisions.** Two servers exposing `search` or `read` create ambiguity for the model and silent shadowing in some hosts. Namespace tools explicitly (`github_search`, `notion_search`); the spec doesn't enforce uniqueness for you.
- **Auth tokens in client config.** The MCP client config (e.g. `claude_desktop_config.json`) often gets checked in or shared. API keys in env vars in the config file have leaked in every flavour of "I shared my Claude config" incident. Use the OS keychain or OAuth, never plaintext config.
- **Treating `tools/list` as static.** The spec allows mid-session tool description changes — the rug-pull vector. If your host doesn't re-prompt the model when descriptions change, you can be backdoored mid-session.
- **Running unaudited community servers with write scopes.** The 5.5% poisoned-metadata rate is not noise.

---

## 7. 2026-vintage news

### Recent spec changes

- **MCP Apps (SEP-1865)** — formerly `mcp-ui`, formalised early 2026. Servers can return interactive HTML rendered in sandboxed iframes on the host. Extends MCP beyond text-only interaction for the first time ([Webfuse 2026 cheat sheet](https://www.webfuse.com/mcp-cheat-sheet)).
- **Tasks primitive (SEP-1686)** — reliable call-now / fetch-later pattern, now production but with open retry/expiry gaps the Agents WG is working.
- **Streamable HTTP statelessness** — under active SEP work in the Transports WG; goal is horizontal scaling behind standard load balancers.
- **MCP Server Cards** — `.well-known` URL convention for capability discovery without connecting; Server Card WG ownership.
- **SEP-1932 (DPoP) and SEP-1933 (Workload Identity Federation)** — sponsored auth work in flight.
- **Governance**: SEP-1302 formalised Working Groups, SEP-2085 established succession/amendment procedure, and a Contributor Ladder SEP is in the queue ([MCP roadmap](https://modelcontextprotocol.io/development/roadmap)).

### Security incidents and disclosures (2025–2026 timeline)

- **CVE-2025-49596** — RCE in MCP Inspector via malicious server response.
- **CVE-2025-6514** — `mcp-remote` package (500k+ downloads), arbitrary OS command exec on client when connecting to untrusted server; disclosed July 9, 2025 by JFrog ([Practical DevSecOps](https://www.practical-devsecops.com/mcp-server-security-best-practices/)).
- **CVE-2025-54136** — Cursor MCP tool-poisoning; structural ([Truefoundry](https://www.truefoundry.com/blog/blog-mcp-tool-poisoning-gateway-defense)).
- **CVE-2025-54994** — `@akoskm/create-mcp-server-stdio` supply-chain compromise.
- **CVE-2025-65720 / 2026-30615 / 2026-30616 / 2026-30617 / 2026-30623 / 2026-30624 / 2026-30625 / 2026-33224 / 2026-26015 / 2026-40933** — the OX Security family advisory of April 15, 2026, naming Family-1 (direct STDIO command injection), Family-2 (hardening bypass), Family-3 (prompt injection in Windsurf), and Family-4 (hidden STDIO configs) across LangFlow, GPT Researcher, LiteLLM, Agent Zero, LangBot, Fay, Bisheng, Jaaz, Langchain-Chatchat, Upsonic, Flowise, Windsurf, DocsGPT, and LettaAI ([OX Security advisory](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/)).
- **CVE-2026-22252 (LibreChat), CVE-2026-22688 (WeKnora)** — additional 2026 disclosures.
- **Anthropic Git MCP CVE-2025-68143/68144/68145** — argument injection and path-bypass; fixed in v2.25.12.18 December 2025.
- **node-ipc malicious republish (May 14, 2026)** — three concurrent versions (9.1.6, 9.2.3, 12.0.1) shipped 80KB obfuscated credential-stealer payloads ([StepSecurity](https://www.stepsecurity.io/blog/node-ipc-npm-supply-chain-attack)). Not MCP-specific but every Node-based MCP server consumes from the same registry.

The picture: MCP's security posture in 2026 is *worse* in absolute terms than in 2025, because the attack surface has grown faster than the defenses. The Linux Foundation transition is partly a response to this — a community vulnerability-disclosure program is named on the roadmap.

### Anthropic's stated direction

From [the 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) and David Soria Parra's talks ([The Future of MCP](https://www.youtube.com/watch?v=v3Fr2JR47KA)):

- **No new transports this cycle** — protect ecosystem compatibility; evolve Streamable HTTP instead.
- **Statelessness and horizontal scale** are the top transport priorities.
- **Agent-to-agent communication** — servers becoming peers that can delegate, not just tools that get called.
- **Enterprise readiness** as a first-class workstream — audit trails, SSO, gateway patterns, configuration portability.
- **MCP Registry as a verified directory** with security audits is targeted for Q4 2026 ([a2a-mcp.org: 2026 roadmap analysis](https://a2a-mcp.org/blog/mcp-2026-roadmap)).
- **Triggers / event-driven updates** named as "On the Horizon" — server-pushed notifications would replace polling and long-held SSE connections.

The throughline is unmistakable: 2024 was "does this protocol make sense," 2025 was "let's get adoption," 2026 is "make it survive production and adversarial environments." The pieces that aren't shipped yet — stateless transport, signed registry, fine-grained scopes, conformance test suites — are the pieces that would change how this stack should think about MCP in twelve months.

---

## Sources

- [The 2026 MCP Roadmap (blog.modelcontextprotocol.io)](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [MCP Roadmap (modelcontextprotocol.io)](https://modelcontextprotocol.io/development/roadmap)
- [MCP Cheat Sheet 2026 (Webfuse)](https://www.webfuse.com/mcp-cheat-sheet)
- [MCP Prompts spec, 2025-06-18 (modelcontextprotocol.io)](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)
- [Resources concepts (modelcontextprotocol.info)](https://modelcontextprotocol.info/docs/concepts/resources/)
- [Reference servers repo (github.com/modelcontextprotocol/servers)](https://github.com/modelcontextprotocol/servers)
- [Archived reference servers (github.com/modelcontextprotocol/servers-archived)](https://github.com/modelcontextprotocol/servers-archived)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [Awesome MCP Servers (wong2)](https://github.com/wong2/awesome-mcp-servers)
- [Cloudflare: build and deploy remote MCP servers](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)
- [Cloudflare: thirteen new MCP servers](https://blog.cloudflare.com/thirteen-new-mcp-servers-from-cloudflare/)
- [Cloudflare: enterprise MCP reference architecture](https://blog.cloudflare.com/enterprise-mcp/)
- [Auth0: secure remote MCP with Cloudflare](https://auth0.com/blog/secure-and-deploy-remote-mcp-servers-with-auth0-and-cloudflare/)
- [Practical DevSecOps: MCP security vulnerabilities](https://www.practical-devsecops.com/mcp-security-vulnerabilities/)
- [Practical DevSecOps: OAuth 2.1 best practices](https://www.practical-devsecops.com/mcp-oauth-2-1-implementation/)
- [Invariant Labs: tool-poisoning disclosure](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Docker: MCP horror stories — GitHub prompt-injection heist](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/)
- [Microsoft Developer Blog: protecting against indirect prompt injection in MCP](https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp)
- [The Register: Anthropic Git MCP flaws](https://www.theregister.com/2026/01/20/anthropic_prompt_injection_flaws/)
- [OX Security: MCP supply chain RCE advisory](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/)
- [CyberArk: poison everywhere](https://www.cyberark.com/resources/threat-research-blog/poison-everywhere-no-output-from-your-mcp-server-is-safe)
- [Truefoundry: best MCP registries](https://www.truefoundry.com/blog/best-mcp-registries)
- [Truefoundry: MCP tool poisoning gateway defense](https://www.truefoundry.com/blog/blog-mcp-tool-poisoning-gateway-defense)
- [Automation Switch: where to find MCP servers 2026](https://automationswitch.com/ai-workflows/where-to-find-mcp-servers-2026)
- [MCPcat: stdio vs SSE vs Streamable HTTP](https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/)
- [MCPcat: Inspector setup](https://mcpcat.io/guides/setting-up-mcp-inspector-server-testing/)
- [Apigene: MCP SSE vs stdio](https://apigene.ai/blog/mcp-sse-vs-stdio)
- [Apigene: MCP server directory](https://apigene.ai/blog/mcp-server-directory)
- [Roo Code: MCP server transports](https://docs.roocode.com/features/mcp/server-transports)
- [Morph LLM: Claude Code Skills vs MCP vs Plugins](https://www.morphllm.com/claude-code-skills-mcp-plugins)
- [Skiln: Claude Code Plugins vs Skills vs MCP](https://skiln.co/blog/claude-code-plugins-vs-skills-vs-mcp-decision-guide)
- [alexop.dev: Claude Code full stack](https://alexop.dev/posts/understanding-claude-code-full-stack/)
- [PipeLab: state of MCP security 2026](https://pipelab.org/blog/state-of-mcp-security-2026/)
- [SkillsLLM: best MCP servers 2026](https://skillsllm.com/blog/best-mcp-servers-2026)
- [MCP Bundles: definitive list of best MCP servers](https://www.mcpbundles.com/blog/best-mcp-servers)
- [Toloka: future of MCP enterprise adoption](https://toloka.ai/blog/the-future-of-mcp-enterprise-adoption/)
- [a2a-mcp.org: 2026 roadmap analysis](https://a2a-mcp.org/blog/mcp-2026-roadmap)
- [Notion MCP overview](https://developers.notion.com/guides/mcp/overview)
- [freeCodeCamp: custom TS MCP server handbook](https://www.freecodecamp.org/news/how-to-build-a-custom-mcp-server-with-typescript-a-handbook-for-developers/)
- [StepSecurity: node-ipc supply chain attack](https://www.stepsecurity.io/blog/node-ipc-npm-supply-chain-attack)
- [The Future of MCP — David Soria Parra (YouTube)](https://www.youtube.com/watch?v=v3Fr2JR47KA)
- [dev.to: four MCP testing patterns](https://dev.to/klement_gunndu/your-mcp-server-has-no-tests-here-are-4-patterns-to-fix-that-2k59)
- [mcpfinder/mcpfinder](https://github.com/mcpfinder/mcpfinder)
