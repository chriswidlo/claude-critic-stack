# Research brief — scripting *for* and *with* AI in this repo

Session: 2026-04-26-ai-scripting-safety-gates
Mode: research-only (no recommendation yet; user will discuss after reading).

This is a synthesis of three parallel research streams (canon-librarian, outside-view, claude-code-guide) plus a direct read of the repo's two scripts and AI docs. It is deliberately structured as *findings + tensions + open questions*, not as a proposal. The user wants to chat about framing before any design.

---

## 0. The actual question, restated

The user said: "we have AI docs, but we also have scripts, but no guidelines or safety and security gates."

That sentence smuggles a frame: *governance is missing and should be added*. I'm going to surface the frame and also the alternative frames the research turned up, because the most defensible move may not be "add governance."

Three candidate framings:

- **(F1) Governance-shaped hole.** Add SCRIPTS.md, schema/lint hooks, frontmatter, tighter permissions. Make the guidelines explicit so that humans and agents both follow them. *This is the user's framing.*
- **(F2) Tool-shape problem.** The scripts are doing too much. The right move is not to govern them but to narrow their capabilities until they can't misbehave (poka-yoke). Governance disappears when the surface shrinks. *This is what Anthropic's own essays argue for.*
- **(F3) Wrong attack surface.** The scripts are the visible risk; the *ingested corpus* is the live attack surface (RSS-fed text becomes the librarian's ground truth). Hardening `/bin/` will pass its own tests and miss the breach class that's actually happening in 2025. *This is the outside-view's strongest finding and the punchline of the brief.*

I am not picking between these in this brief. The point of this section is that the user's question contains a frame, and the research suggests at least two other frames worth considering.

---

## 1. What's actually in the repo (inside-view inventory)

So we ground the rest in facts, not vibes.

**Scripts (3, not 2):**
- `bin/ingest-canon.mjs` — 544 LOC. Fetches arbitrary HTML/JSON/RSS from URLs in `canon/sources.ingest.yaml`, strips it, writes `source.txt` + `citation.yaml` + `README.md` into `canon/corpus/<slug>/`.
- `bin/ingest-owned-book.mjs` — 119 LOC. Reads any user-supplied filesystem path, copies it into `canon/corpus/<slug>/source.txt`.
- `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py` — 137 LOC. A Python "spike" that escaped from `/bin/` into a session-artifacts directory. **It is not gitignored** (the gitignore wildcard is `.claude/session-artifacts/*/` but this is a directory match for tracking, the file is currently untracked but could easily be committed). This is *itself* the governance gap the user is describing.

**AI docs (the governance surface that does exist):**
- `CLAUDE.md` — workflow contract. Strict, well-formed.
- `AGENTS.md` — **broken.** It is a stale near-duplicate of `CLAUDE.md` with `.Codex/` paths and references "Codex-critic-stack." Either an aborted dual-tooling fork or a copy-paste error. Currently misleading any agent or human that reads it.
- `.claude/agents/*.md` — 10 subagent contracts. Vary in tool-restrictiveness; `canon-refresher` declares `Bash` despite only needing `Read, WebFetch, Glob`.
- `.claude/settings.json` — allow: Read/Glob/Grep/4 read-Bash. Deny: `rm`, `git push`. Shallow.
- `.claude/settings.local.json` — WebFetch domain allowlist (12 domains), explicit allow for the two `node ./bin/...` invocations.

**Concrete latent vulnerabilities I noticed reading the code** (not exhaustive, illustrative):
1. `ingest-canon.mjs:504` — `join(ROOT, 'canon', 'corpus', src.slug)` with `src.slug` validated only as "string." `slug: ../../../etc` would resolve outside the corpus. (Consequence depends on which slug source is trusted; YAML editing is currently human-only, so low-immediate but a real footgun.)
2. [`ingest-owned-book.mjs:62`](bin/ingest-owned-book.mjs) — `resolve(inputPath)` accepts any path. If an agent is ever given authority to invoke this script with a path it computed, sensitive system files (e.g. user SSH keys, system password files) are valid arguments. The "libgen substring warn" is theatre; it warns but doesn't block, and the warn is on the path, not the contents.
3. `ingest-canon.mjs` `fetchHtmlMulti` — follows up to 100 child links per source, restricted only by URL-prefix string match (`abs.startsWith(base)`). SSRF-adjacent if a source URL ever points at an internal address.
4. `canon-refresher` — pulls RSS, then quotes feed text *verbatim* into the model context. Text in arXiv titles or RSS descriptions is attacker-controlled. **Indirect prompt injection vector.**
5. The corpus has no signature/checksum verification at *read* time. The librarian trusts whatever bytes are at `canon/corpus/<slug>/source.txt`. If the refresher (or a future agent, or a typo) writes garbage or hostile text there, every downstream recommendation is poisoned.
6. Settings deny list is 2 entries. Things not denied: `curl`, `wget`, `chmod`, `git config`, `git rebase`, arbitrary `node`, arbitrary `python`, `ssh`, `gh`, sourcing untrusted shell scripts, etc. The implicit "if it's not allowed, ask" mode catches some of this — but the user is the one being asked, every time, with no policy memory.

These aren't bugs to file. They're the inside-view evidence that the user's instinct ("we have a gap") is correct on the *facts*. What the research disputes is what to *do* about it.

---

## 2. The threat model — what we are actually defending against

Two distinct categories. They have different threat-actors and different countermeasures.

**Category A: Scripts that the AI runs (or that the AI is asked to write).**
- Blast radius from a Claude session executing a script with arguments it computed (path, URL, slug).
- Side effects beyond the declared scope (writing outside the corpus, deleting things, mutating git history, posting to external services).
- Provenance loss (a script gets edited mid-session, no record of why).
- Scripts that escape `/bin/` and lose review entirely (the Python file in session-artifacts is the existence proof).

**Category B: Untrusted data that the AI reads.**
- Indirect prompt injection from RSS feeds, fetched HTML, ingested book text, even from canon citations.
- Corpus poisoning: the librarian's "ground truth" is writable by the refresher and by `ingest-canon.mjs`. Once poisoned, every recommendation is wrong in the same direction.
- The "lethal trifecta" framing (Simon Willison): private data + untrusted content + external comms in the same agent = exfil channel. This repo has all three latent (filesystem read + RSS ingest + WebFetch).

Most of the user's instinct is pointing at Category A. The 2025 incident wave (per outside-view: mcp-remote CVE-2025-6514, GitHub MCP prompt-injection exfil, Postmark MCP BCC, Supabase Cursor SQL-exfil) is overwhelmingly Category B. **This asymmetry is the most important finding in the brief.**

---

## 3. What canon says (supporting and contradicting)

The canon-librarian returned both halves on purpose. I'm listing both because they don't agree, and I think the disagreement is the actual content.

### Supporting "add safety gates" — but specifically as *constraints in the tool*, not policy docs

- **Google SRE Book, Ch. 17 — "treat your own config as hostile input."** Schema validation at load, bounded runtime, fail-fast on unknown shapes. Maps directly onto `ingest-canon.mjs` parsing user-edited YAML. Citation: SRE book lines 6163–6169.
- **SRE Ch. 17 again — "defense in depth": a second tool whose only job is to notice the first one misbehaving.** A schema check / hash diff / content-sanity check that runs *separately* from the ingest script is canon-blessed.
- **Cockburn, *Hexagonal Architecture* (2005).** Each adapter (network, filesystem) owns the validation contract for its boundary. The two ingest scripts are exactly two adapters; the validation should live in the adapter, not in the core or in a doc.
- **Anthropic, *Building Effective Agents* (2024), Appendix 2 — "poka-yoke your tools."** Explicit example: tools that took relative paths failed; tools rewritten to require absolute paths "worked flawlessly." This is the architectural answer to `ingest-owned-book.mjs` accepting arbitrary paths — narrow the API until misuse is impossible.

### Contradicting — push back on the governance reflex

- **SRE Ch. 9, "Simplicity."** "Every new line of code written is a liability." A SCRIPTS.md + frontmatter + lint hooks + provenance check together can easily exceed the surface area of the two scripts they govern. Canon's frame: *delete options, don't add ceremony.*
- **SRE Ch. 5, "Eliminating Toil."** Process is overhead, not engineering. "If a human operator needs to touch your system during normal operations, you have a bug." A governance layer that requires the author to remember rules is adding toil, not removing it.
- **Anthropic, *Building Effective Agents* (2024), opening.** "Find the simplest solution possible. Only increase complexity when needed." And: "frameworks create extra layers of abstraction that obscure the underlying prompts and responses, making them harder to debug." Direct shot at the "let's add governance" reflex.
- **Cockburn, *Hexagonal Architecture* — the "promised layer" trap.** "The attempted solution, repeated in many organizations, is to create a new layer in the architecture, with the promise that this time, really and truly, no business logic will be put into the new layer. However, having no mechanism to detect when a violation of that promise occurs, the organization finds a few years later that the new layer is cluttered." A SCRIPTS.md without a *mechanism* that detects violation is exactly this trap.
- **SRE — break-glass mechanisms must exist and be loud.** Even Google's gated process anticipates "I need to bypass this *now*." A governance design that doesn't anticipate the bypass will be routed around silently and become theatre.
- **Bonus: SRE "Managing Incidents" — the whitelist itself caused an outage.** A security scanner interacting with an allowlist-creation bug generated thousands of allowlist entries. Direct evidence that "we have an allowlist" is not a safety claim; it's an additional surface.

**Canon gaps the librarian flagged explicitly (do not invent quotes here):**
- Indirect prompt injection / lethal trifecta — zero coverage.
- Capability-based / object-capability security — zero coverage.
- Supply-chain provenance / SLSA / sigstore for ingested content — zero coverage.
- Helland on contract framing, Nygard on stability patterns — *stub entries, body not ingested*. These would be the natural sources for several arguments above.

The librarian's honest summary: canon supports "narrow the tool surface" much more strongly than it supports "add a governance layer." The two are not the same move.

---

## 4. Outside view — base rate for this kind of effort

Reference class chosen: solo/small-team developer-tooling repos that bolt on a `CONTRIBUTING.md`-style governance layer absent external pressure (closest fit), with an assist from "early-MCP/agent-framework projects retrofitting safety after a public incident class emerged" (rising in relevance since 2025).

**Forecast for "small team retrofits a governance/safety layer onto an AI-adjacent tooling repo, behavior actually changes 6 months later":**
- Gets written and ignored: ~40%
- Collapses under ceremony (author works around their own rules): ~20%
- Replaced by a heavier framework (you adopt someone else's): ~15%
- Succeeds quietly: ~25%

This repo's positioning relative to that base rate:
- **Above:** the agent is one of the readers (genuinely unusual lever — agents re-read the conventions every invocation), minimal scaffolding already exists, single author, small surface.
- **Below:** no incident pressure, self-policing (author grades the rules they wrote), no fail-closed default exists yet, and frontmatter for 2 scripts is a high ceremony-to-asset ratio (modal failure shape #2).

Three failure shapes named explicitly:
1. **Decorative SCRIPTS.md.** Doc ships, next 3 scripts ignore it, author rewrites the doc instead of fixing the gap. Diagnostic: scripts authored after `SCRIPTS.md` lands that conform without the author manually checking.
2. **Frontmatter tax.** 100% schema conformance, 0% semantic accuracy. Fields become noise. Diagnostic: pick a random script's `blast-radius:` field and check whether it matches actual code paths.
3. **"Just this once" allowlist creep.** Allowlist gets widened for one debug session, never narrowed. Modal for single-operator setups.

**The non-obvious finding from outside-view (this is the one the inside view misses):** the inside-view sees scripts and agents as the things being governed; the 2025 incident pattern says it's the *ingested data channel* that's the breach surface. Frame F3 from §0.

---

## 5. Harness-native surfaces (what we don't have to reinvent)

Claude Code's own primitives that are relevant — listed because the most common failure mode of governance retrofits is reinventing what the harness already does.

- **Permissions: deny-first precedence.** Deny rules win. There is a `defaultMode: dontAsk` that auto-denies anything not in the allowlist (deny-by-default mode). Currently we use the implicit "ask the user" mode, which has no policy memory.
- **Bash command-shape matching.** `Bash(node ./bin/ingest-canon.mjs:*)` matches that exact script-prefix. We can pin scripts by full path. Compound commands are decomposed before matching, so `git status && rm foo` is matched per-subcommand.
- **Read deny rules don't block Bash.** `Read(.env)` deny does not stop `cat .env` in Bash. This is a footgun. Sandboxing is the OS-level fix.
- **Hooks: PreToolUse, PermissionRequest, UserPromptSubmit can block (exit 2).** A PreToolUse hook can inspect Bash commands and reject `node` invocations of paths outside `/bin/`. PostToolUse cannot block; it's audit-only.
- **Sandboxing.** macOS Seatbelt / Linux bubblewrap. Restricts Bash filesystem writes to the working dir and routes network through a domain-allowlist proxy. Off by default.
- **Worktree isolation.** Subagents can declare `isolation: worktree` to run in an isolated git worktree. Worktrees are preserved until manually deleted (audit trail).
- **MCP allowlisting.** `allowManagedMcpServersOnly: true` exists at managed-settings level. **No deny-by-default mode at user/project level — gap.**
- **Subagent `tools:` field narrows what the agent can call.** Parent permissions still filter on top. `canon-refresher` declaring `Bash` is broader than it needs.
- **Observability.** OpenTelemetry exporter exists for tool invocations and hook firings. **No built-in file-based audit log** — would need a PostToolUse hook to a local file, or full OTel pipeline.

The two largest harness-native levers we're not using: **`defaultMode: dontAsk`** (deny-by-default) and **PreToolUse hooks** (programmatic gates that the agent can't talk its way past).

---

## 6. Tensions the user will need to resolve

These are the points where the research returns conflict, and where I will not pretend they don't.

1. **"Add gates" vs "narrow the tool surface."** Anthropic and Cockburn say the second; SRE says either, depending on category. If we narrow `ingest-owned-book.mjs` to read only from a `inbox/` directory, the path-traversal threat disappears and the gate becomes unnecessary. If we add a gate on top of the current free-form path, the gate has to be perfect forever. *Question for user: are you optimizing for a defensive perimeter, or for fewer things to defend?*

2. **Doc-shaped vs mechanism-shaped governance.** SCRIPTS.md is a doc. A pre-commit hook that rejects scripts outside `/bin/` is a mechanism. Canon (Cockburn explicitly) says docs decay; mechanisms hold. *Question for user: how much of what you want is "I want to know the conventions" vs "I want the conventions enforced even when I forget"?*

3. **Scripts vs corpus as attack surface.** Outside view says corpus is where the breaches happen in 2025; user's instinct points at scripts. *Question for user: is the felt anxiety about "scripts could do dangerous things" or "I want to trust what comes out of the librarian"? These are different problems.*

4. **Universal vs context-specific gates.** A gate that fires on every script invocation has very different cost than a gate that fires only on `ingest-owned-book.mjs`. *Question for user: are you imagining a per-script contract, or a universal lint?*

5. **Pre-incident discipline vs over-engineering.** Outside-view base rate says pre-incident retrofits ossify into shelfware ~40% of the time. The strongest predictor of survival is whether the *first* artifact is a fail-closed enforcement mechanism (the agent literally cannot violate it), not a doc. *Question for user: what's the smallest enforcement-mechanism that, if it shipped tomorrow, would change tomorrow's behavior?*

---

## 7. Things I noticed that are worth flagging regardless of frame

These exist independently of how we resolve the framing question. They look like cleanup, not strategy.

- **`AGENTS.md` is broken.** It's a stale duplicate of `CLAUDE.md` with `.Codex/` paths. Any tool/agent that reads `AGENTS.md` (and several do, by convention) is reading a misleading contract. Either delete it or restore it as a real document.
- **The Python script in `.claude/session-artifacts/...` is the user's exact problem in miniature.** A script was authored, lives outside `/bin/`, has no companion citation in any doc, is not covered by the gitignore rule the user might assume covers it. This is what "no governance" looks like, observable today.
- **The `canon-refresher` subagent declares `Bash` but doesn't need it.** Cheapest possible governance move: drop `Bash` from its tool list. Single line.
- **`canon/corpus/*/source.txt` is gitignored** (good — prevents large blobs and license issues), **but there is no signature manifest** that says what the corpus *should* contain. If a refresher writes a new `source.txt`, no downstream check notices that the bytes don't match an expected hash. The `citation.yaml` has a `sha256` field but no enforcement that the body matches it at read-time.
- **`.claude/settings.json`'s 2-entry deny list is not a security boundary.** It blocks accidental `rm` and accidental `git push`. It does nothing about the actual blast-radius vectors (`curl | sh`, `chmod`, arbitrary `node`/`python`, `git rebase`, `gh api`, `ssh`).

---

## 8. What I would want to ask before recommending anything

For the chat after this brief:

1. Which of the three frames (F1 governance, F2 narrow-the-tools, F3 corpus-as-surface) feels closest to the actual worry? The frame determines the work.
2. Is the worry *future scripts that don't exist yet* (a convention problem) or *the two that do exist* (a hardening problem)?
3. What's the smallest enforcement mechanism that would make you stop worrying tomorrow? (Forcing-function for §6.5.)
4. Is the agent expected to author scripts in this repo, or only invoke them? If the former, the convention has a different reader than if the latter.
5. Are you willing to delete the `AGENTS.md` duplicate and the escaped Python spike as a no-cost prelude? These are cleanup, not strategy, but they affect the inventory we're talking about.

---

## Appendix: research provenance

- Canon-librarian return — full output saved with this session. 13 cited passages across 5 corpus entries (google-sre-book, cockburn-hexagonal-architecture, anthropic-building-effective-agents, anthropic-effective-context-engineering, anthropic-multi-agent-research-system). 6 explicit canon-gap declarations.
- Outside-view return — reference class A (solo dev tooling governance) primary, B (post-2025 MCP incidents) rising. Cited 8 web sources for currency on the 2025 MCP breach class.
- Claude-code-guide return — pulled current docs for permissions, hooks, sandboxing, sub-agents, MCP, security, monitoring, CLI reference. 9 doc URLs.
- Direct repo read — 2 scripts, 1 escaped Python, 10 agent contracts, 2 settings files, gitignore, 2 AI-doc files (`CLAUDE.md`, `AGENTS.md`).

Workflow note: the 12-step pipeline was *not* run end-to-end. The user explicitly asked for research, not a recommendation. Steps 3–6 (parallel gather, distill) ran in compressed form; steps 7–12 (scope-map, frame-challenger, generator, critic-panel, synthesis) deliberately skipped pending the user's chat. The frame-questions in §6 are the input to whichever subset of those steps we run next.
