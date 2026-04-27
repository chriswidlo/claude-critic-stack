# Canon retrieval — critics get Write tool

## Corpus coverage

**Partial.** Strong coverage on multi-agent artifact patterns, tool-permission discipline, and audit/postmortem authorship from Anthropic engineering essays + Google SRE. Thin coverage on single-writer-vs-multi-writer file patterns at the OS/build-system level (no Helland body text — stub; no Hohpe EIP body retrieved here). No canon entry directly addresses "review-of-review" / self-modifying review systems — that's a real gap.

---

## Supporting passages (favor the proposal: critics get Write)

### 1. Anthropic, "How we built our multi-agent research system" (2025), Appendix — "Subagent output to a filesystem to minimize the 'game of telephone'"
*Confidence: verified (sha256 in citation.yaml; body_completeness: full).*

> "Direct subagent outputs can bypass the main coordinator for certain types of results, improving both fidelity and performance. Rather than requiring subagents to communicate everything through the lead agent, implement artifact systems where specialized agents can create outputs that persist independently. Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator. This prevents information loss during multi-stage processing and reduces token overhead from copying large outputs through conversation history. The pattern works particularly well for structured outputs like code, reports, or data visualizations where the subagent's specialized prompt produces better results than filtering through a general coordinator."

**Relevance:** This is the single most direct canon endorsement of the proposal. It names the failure mode ("game of telephone"), names the fix (subagent writes to filesystem; orchestrator gets a lightweight reference), and notes both fidelity *and* token overhead benefits. The current critic design is exactly the anti-pattern this passage warns against — verdicts filtered through orchestrator transcription.

### 2. Anthropic, "Effective context engineering for AI agents" (2025), §"Sub-agent architectures"
*Confidence: verified (full body).*

> "Sub-agent architectures provide another way around context limitations. Rather than one agent attempting to maintain state across an entire project, specialized sub-agents can handle focused tasks with clean context windows. The main agent coordinates with a high-level plan while subagents perform deep technical work or use tools to find relevant information. Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."

**Relevance:** Reinforces the "lightweight reference + persisted artifact" pattern. The orchestrator should receive a *distillation*, not a transcribed full verdict. Maps directly onto: critic writes full verdict to disk; returns one-line summary to orchestrator.

### 3. Anthropic, "Effective context engineering for AI agents" (2025), §"Context retrieval and agentic search" (just-in-time)
*Confidence: verified.*

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools. […] This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."

**Relevance:** Bears on the side question. The aggregated `critiques.md` becomes a *light index* — file paths to per-lens verdicts — rather than a transcribed copy. JIT retrieval supports keeping a thin index; orchestrator loads the full lens verdict only when needed (e.g., during step 11 replan).

### 4. Anthropic, "Building Effective Agents" (2024), §"Workflow: Parallelization" → Voting
*Confidence: verified.*

> "Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results. […] Voting: Running the same task multiple times to get diverse outputs. […] Reviewing a piece of code for vulnerabilities, where several different prompts review and flag the code if they find a problem."

**Relevance:** Frames the three critic lenses explicitly as a voting/parallel pattern. Voting depends on each voter's verdict being preserved verbatim — minority-veto doesn't survive aggregation through a single transcribing voice. This is a structural argument for per-voter persistence.

### 5. Google SRE Book (2016), Ch. 15 "Postmortem Culture: Learning from Failure" — definition of the artifact
*Confidence: verified (body_completeness: toc_plus_chapters).*

> "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring."

> "Our postmortem documents are Google Docs, with an in-house template (see Example Postmortem). Regardless of the specific tool you use, look for the following key features: Real-time collaboration / Enables the rapid collection of data and ideas. Essential during the early creation of a postmortem. An open commenting/annotation system…"

**Relevance:** Industry-standard analogue for the artifact-vs-transcription distinction. The postmortem *is* the document — not a manager's summary of the document. Multiple authors write into the same shared artifact directly. This argues for critics owning their own write surface, but note the model is *one shared doc with many writers* — not one file per writer (see complicating passage #2).

### 6. Google SRE Book (2016), Ch. 7 "The Evolution of Automation at Google" — least-privilege + audit trail
*Confidence: verified.*

> "A growing awareness of advanced, persistent security threats drove us to reduce the privileges SREs enjoyed to the absolute minimum they needed to do their jobs. We had to replace our use of sshd with an authenticated, ACL-driven, RPC-based Local Admin Daemon, also known as Admin Servers, which had permissions to perform those local changes. As a result, no one could install or modify a server without an audit trail. […] giving someone the access to install packages would not let them view colocated logs. The Admin Server logged the RPC requestor, any parameters, and the results of all RPCs to enhance debugging and security audits."

**Relevance:** Directly on tool-permission scoping. Grants must be (a) minimal, (b) ACL-bound to a specific path/scope, (c) logged so authorship is recoverable. Translation to the proposal: a critic's `Write` grant should be scoped to `critiques/<lens>.md` (path-restricted), not unbounded `Write`. The harness should record provenance, not rely on the critic to self-attribute.

### 7. Google SRE Book (2016), Ch. 8 "Release Engineering" — audit trail as artifact, not as transcription
*Confidence: verified.*

> "During the release process, we re-run the unit tests using the release branch and create an audit trail showing that all the tests passed. […] Our automated release system produces a report of all changes contained in a release, which is archived with other build artifacts."

**Relevance:** Audit trails are *generated as artifacts alongside the work*, not transcribed from memory by a downstream summarizer. Generalizes: each critic should produce its own artifact at the moment of judgment; orchestrator's job is composition, not authorship.

### 8. Anthropic, "How we built our multi-agent research system" (2025), §"Production reliability"
*Confidence: verified.*

> "Adding full production tracing let us diagnose why agents failed and fix issues systematically. Beyond standard observability, we monitor agent decision patterns and interaction structures—all without monitoring the contents of individual conversations, to maintain user privacy."

**Relevance:** Per-lens artifacts on disk give exactly the structured trace this passage advocates for. With orchestrator transcription, a wrong verdict can be silently rewritten and you can't tell from the aggregate whether the lens was wrong or the transcription was wrong. Per-lens files cleanly separate the two failure modes.

---

## Contradicting or complicating passages

### 1. **Anthropic, "Effective context engineering" (2025), §"Tools" — bloated tool sets are a top failure mode**
*Confidence: verified.*

> "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better. As we'll discuss later, curating a minimal viable set of tools for the agent can also lead to more reliable maintenance and pruning of context over long interactions."

**Why this complicates the framing:** Adding `Write` to a critic that previously had only Read/WebFetch/WebSearch is tool-set expansion. Each new tool dilutes decision focus. A critic with `Write` may now ask itself *where* to write, whether to write supporting notes, whether to edit prior verdicts — not just *what verdict to issue*. The proposal must answer: is `Write` strictly path-pinned (single allowed target), or is it general? If general, this passage is a strong objection.

### 2. **Google SRE Book (2016), Ch. 15 — postmortems are *one* shared document, not N sibling files**
*Confidence: verified.*

> "Real-time collaboration / Enables the rapid collection of data and ideas. Essential during the early creation of a postmortem. An open commenting/annotation system / […] Once those involved are satisfied with the document and its action items, the postmortem is added to a team or organization repository of past incidents."

**Why this complicates the framing:** The industry-standard reference for "multi-author critical review" uses a *single shared document with multiple writers and an annotation layer*, not N files written in parallel by N authors. The SRE pattern would suggest one `critiques.md` that all three critics append to (with section headers naming each lens), with the orchestrator only assembling the final read — not three sibling files. The proposal's "drop the aggregate" arm runs *against* this pattern. Counter-argument the proposal must answer: why is per-lens isolation better than one shared review doc?

### 3. **Google SRE Book (2016), Ch. 6 "Monitoring Distributed Systems" — keep subsystems loosely coupled and *distinct***
*Confidence: verified.*

> "It can be tempting to combine monitoring with other aspects of inspecting complex systems, such as detailed system profiling, single-process debugging, tracking details about exceptions or crashes, load testing, log collection and analysis, or traffic inspection. While most of these subjects share commonalities with basic monitoring, blending together too many results in overly complex and fragile systems. As in many other aspects of software engineering, maintaining distinct systems with clear, simple, loosely coupled points of integration is a better strategy (for example, using web APIs for pulling summary data in a format that can remain constant over an extended period of time)."

**Why this complicates the framing:** This *supports* per-lens isolation (separate verdict files), but warns against blurring concerns. If critics are granted `Write`, do they also get tempted to write traces, scratch notes, intermediate retrievals into the same artifact tree? The integration point ("summary data in a format that can remain constant") suggests a *strict schema* — not free-form prose. Implication: per-lens files yes, but each must be schema-validated, not free-form Markdown a critic invents.

### 4. **Anthropic, "Building Effective Agents" (2024), §Summary — "maintain simplicity"**
*Confidence: verified.*

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. […] When implementing agents, we try to follow three core principles: Maintain simplicity in your agent's design. Prioritize transparency by explicitly showing the agent's planning steps. Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing."

**Why this complicates the framing:** The current design (orchestrator transcribes prose) is simpler; the proposal adds (a) a tool grant, (b) a directory convention, (c) a side-question about whether the aggregate stays. Each is small but they compound. Strict reading of this principle says: prove the transcription loss is real (with examples) before adding mechanism. The "game of telephone" passage is suggestive but not specific — has the user observed actual paraphrase loss in this stack? If not, this is a speculative addition.

### 5. **Anthropic, "Building Effective Agents" (2024), Appendix 2 — Poka-yoke your tools / absolute paths**
*Confidence: verified.*

> "Poka-yoke your tools. Change the arguments so that it is harder to make mistakes. While building our agent for SWE-bench, we actually spent more time optimizing our tools than the overall prompt. For example, we found that the model would make mistakes with tools using relative filepaths after the agent had moved out of the root directory. To fix this, we changed the tool to always require absolute filepaths—and we found that the model used this method flawsly."

**Why this complicates the framing:** Granting `Write` without path-pinning is a poka-yoke failure. A critic agent that *could* write `critiques/architecture.md` could also write `critiques/operations.md` — overwriting another lens's verdict — or `frame.md`, or `decision-log.md`. The proposal must specify *harness-level* path enforcement, not just an instruction in the prompt. ("Please only write to your own file" is not enforcement.) This is a real risk to address before granting the tool.

### 6. **Google SRE Book (2016), Ch. 15 — "No Postmortem Left Unreviewed" / aggregation tools are valuable**
*Confidence: verified.*

> "An unreviewed postmortem might as well never have existed. To ensure that each completed draft is reviewed, we encourage regular review sessions for postmortems. […] With a large number of postmortems produced each month across Google, tools to aggregate postmortems are becoming more and more useful. These tools help us identify common themes and areas for improvement across product boundaries."

**Why this complicates the framing (side question):** Argues *against* dropping the aggregate. Per-lens verdicts that are never recombined or cross-read are postmortems "languishing in the bottom of a virtual filing cabinet" (Ch. 28). The aggregate — even as a thin index — is the surface where common themes across lenses become visible. Dropping it entirely loses cross-lens pattern recognition; keeping it as a thin verdict-index is the SRE-aligned choice.

---

## Gaps (canon-silent or thin)

1. **Self-modifying review systems / review-of-review.** No canon entry directly addresses the conflict-of-interest when a stack reviews changes to its own machinery. Adjacent: SRE Ch. 15 mentions postmortems on the postmortem process (surveys), but it's culture, not architecture. Recommend the user invoke `outside-view` or accept this as a known canon gap.

2. **Single-writer vs. multi-writer file patterns at OS/build-system level.** Helland (life-beyond-distributed-transactions, 2007) is the natural source for entity ownership / single-writer principles — but the entry is a stub (`body_completeness: stub`, fetch_blocked PDF). Honest gap; do not fabricate Helland quotes. The Anthropic "filesystem-as-artifact-store" passages cover the agent-system version of the question but not the deeper distributed-systems theory.

3. **Tool-permission scoping in agent harnesses (instruction-level vs. harness-level).** Anthropic essays argue for poka-yoke and clear ACIs but do not specifically discuss path-restricted Write tools as a primitive. The SRE Admin Server passage is the closest analogue (ACL-driven RPC), but it's general infrastructure, not LLM-specific. Real gap — worth a `WebSearch` for Anthropic's tool-permission docs (post-corpus) only after librarian-first rule is satisfied (it is).

4. **Aggregator/index file patterns.** No canonical treatment in this corpus of "when does an index file earn its keep vs. become dead weight." JIT-retrieval (Anthropic context-engineering) is adjacent but not specific. Inverted-index theory absent.

5. **Paraphrase loss in human/automated transcription.** The "game of telephone" passage is the only explicit canon hit. No experimental data on transcription fidelity in LLM orchestrator-to-subagent flows in this corpus.

6. **Staleness note.** Anthropic essays are 2024–2025 — current. SRE book is 2016, but the postmortem-authorship pattern it describes has not meaningfully shifted. No staleness flag warranted.

---

## Citation audit summary

| Source | Year | Confidence | Body completeness |
|---|---|---|---|
| Anthropic, "Multi-agent research system" | 2025 | verified | full |
| Anthropic, "Effective context engineering" | 2025 | verified | full |
| Anthropic, "Building Effective Agents" | 2024 | verified | full |
| Google SRE Book | 2016 | verified | toc_plus_chapters |
| Helland, "Life Beyond Distributed Transactions" | 2007 | n/a — stub | not ingested |
| Chen et al., "Devil's Advocate" | 2024 | verified abstract only | abstract on the landing page |
| Shinn et al., "Reflexion" | 2023 | verified abstract only | abstract_only |

No passages quoted from stub or abstract-only sources beyond what is genuinely present in the ingested text.
