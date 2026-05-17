# AI-Readable Documentation & Folder READMEs — SOTA Research

**Vintage:** 2026-05-17.
**Volatility tier:** fast (90-day review cadence; AI tooling docs change weekly).
**Next review by:** 2026-08-15.
**Status:** active.

Combined synthesis of two research turns (2026-05-17) investigating how AI-agent repositories should author root and folder-level documentation. All findings are source-cited; extrapolations are flagged explicitly.

---

## Why this exists

The `claude-critic-stack` repo has accumulated SOTA references and best-practice quotes across multiple sessions. The "ratchet forward, never sideways" operating principle (see [README.md](README.md) §"Operating principle") binds us to documented practice, not opinion. This document is the canonical reference for what the literature actually says — so future work can cite it without re-running the research.

It is structured to support five recurring questions:
1. How should root-level documentation (CLAUDE.md, README.md) be authored for AI consumption?
2. How should subdirectory READMEs differ from the root?
3. When are diagrams (mermaid, ASCII) worth including?
4. When is a single registry better than multiple?
5. How does the field defend against documentation staleness?

---

## 1. The auto-load vs lazy-load distinction (load-bearing)

The single most important architectural distinction in agent-doc design.

### Definite

Anthropic memory docs ([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)) describe two tiers explicitly:

> "CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence... target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."

> "Claude also discovers CLAUDE.md and CLAUDE.local.md files in subdirectories under your current working directory. Instead of loading them at launch, they are included when Claude reads files in those subdirectories."

This is the load-bearing fact:
- **Auto-loaded** (every session's context, every turn): root `CLAUDE.md`, `.claude/rules/` matching path globs, `@`-imports.
- **Lazy-loaded** (only when AI actually reads files in the folder): subdirectory `CLAUDE.md`, folder `README.md`, `.claude/skills/<skill>/SKILL.md`.

Anthropic's *Effective Context Engineering* (2025) reinforces: *"CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing."*

### Implications

- Every byte in `CLAUDE.md` taxes every turn. Cut ruthlessly.
- Every byte in a folder README costs ~zero until consulted. Be thorough.
- Mermaid diagrams in `CLAUDE.md` = auto-load cost. In folder READMEs = free until consulted.
- Length targets differ by tier (see §3).

---

## 2. The "what + when" description discipline

### Definite

Anthropic skill best-practices ([platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)):

> "The `description` field enables Skill discovery and should include both what the Skill does and when to use it."

Anthropic subagent docs ([code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)) echo: descriptions like *"Use proactively after writing authentication, authorization, or data-handling code"* are the canonical pattern.

### Implications

- Every agent / skill / hook file should declare what it does AND when to invoke it.
- Folder READMEs containing N files should map "when invoked" per file (table column or per-entry block).
- This bleeds into the "Read this when / Skip if" preamble pattern — see §6 for the honest status.

---

## 3. Length targets — what's documented vs extrapolated

### Definite (Anthropic-published)

| File type | Target | Source |
|---|---|---|
| `CLAUDE.md` (auto-loaded) | <200 lines | [Anthropic memory docs](https://code.claude.com/docs/en/memory) |
| `SKILL.md` body | <500 lines | [Anthropic skill best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| HumanLayer aspiration | <60 lines (CLAUDE.md only) | [humanlayer.dev/blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
| Anthropic's own MEMORY.md description field | <200 chars | [agents.md v1.1 proposal #135](https://github.com/agentsmd/agents.md/issues/135) (mirrors Anthropic practice) |

### Extrapolation (not documented — flag honestly)

| File type | Reasoned target | Basis |
|---|---|---|
| Folder README | ≤300 lines | Between CLAUDE.md's 200 (lower bound; folder READMEs are smaller scope than SKILL.md) and SKILL.md's 500 |
| Subdirectory `CLAUDE.md` | <200 lines | Apply root rule unless documented otherwise |

No published Anthropic number for folder READMEs specifically. The ≤300 figure is judgment; do not present as SOTA.

### Anti-pattern

[Anthropic best-practices](https://code.claude.com/docs/en/best-practices): *"If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."*

Bloat is not abstract — it has documented behavioral consequences.

---

## 4. Pointer over paste — the @-import trap

### Definite

HumanLayer ([humanlayer.dev/blog/writing-a-good-claude-md](https://www.humanlayer.dev/blog/writing-a-good-claude-md), Nov 25 2025):

> "Don't @-mention extensive documentation files in your CLAUDE.md, as this bloats the context window; instead, mention the path and pitch the agent on why and when to read the file."

Anthropic memory docs confirm implicitly: *"imported files still load and enter the context window at launch."*

### Implications

- `@path/to/doc.md` is **not** free — it expands at launch into the context window.
- The right pattern: link as bracketed prose with a one-line reason to read it.
- This bleeds directly into the folder-README strategy: CLAUDE.md should *point to* folder READMEs, not duplicate their content.

---

## 5. AGENTS.md per-directory pattern

### Definite

AGENTS.md spec ([agents.md](https://agents.md)):

> "Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree, so the closest one takes precedence and every subproject can ship tailored instructions."

Concrete example cited: *"the main OpenAI repo has 88 AGENTS.md files."*

Anthropic's nested CLAUDE.md mechanism is the same shape: *"Claude pulls in child CLAUDE.md files on demand when working with files in those directories"* ([Anthropic best-practices](https://code.claude.com/docs/en/best-practices)).

### Emerging — AGENTS.md v1.1 (issue #135, open, not merged)

Opened January 8 2026. Formalizes three concepts:

> "**Jurisdiction:** An AGENTS.md file applies to all files and subdirectories within its containing folder."
> "**Accumulation:** Guidance accumulates as you traverse the directory tree...rather than replacing it entirely."
> "**Progressive disclosure via optional YAML frontmatter** with `description` (under 200 chars) and `tags` fields, enabling agents to build a lightweight index before loading full files."

Source: [github.com/agentsmd/agents.md/issues/135](https://github.com/agentsmd/agents.md/issues/135). Status as of 2026-05-17: still open, not merged. **Do not bet our format on v1.1 frontmatter conventions yet.**

### Implications for us

- For each subdirectory containing AI-load-bearing files (`.claude/agents/`, `.claude/skills/`, `.claude/hooks/`), a folder README serves the AGENTS.md-per-directory role.
- We use `README.md` not `AGENTS.md` because Claude Code reads CLAUDE.md / READMEs, not AGENTS.md, by default.
- The nested-discovery pattern is documented Anthropic behavior — we can rely on it.

---

## 6. The "Read this when / Skip if" preamble pattern

### Status: extrapolation, not documented SOTA

The research turn searched explicitly for *"when to read this" preamble agent documentation* and returned **zero results**. The pattern is a reasonable extension of:

- SKILL.md `description` discipline (what + when)
- Subagent triage rule (*"Use this subagent when [condition]. It returns [output shape]"*)
- AGENTS.md v1.1 `description` frontmatter (gives AI a discovery hint without loading the full file)

But no source documents *"Read this when: …"* / *"Skip this if: …"* as an established preamble for folder READMEs.

### Recommendation

Use the pattern in our folder READMEs. Label it as our convention, not as industry SOTA. The cost is two lines per README; the benefit is the AI can decide whether to descend into the folder without parsing the full document.

---

## 7. Mermaid vs ASCII vs prose for AI-consumed diagrams

### Definite (token-efficiency)

Alessio Michelini ([dev.to/darkmavis1980](https://dev.to/darkmavis1980/why-mermaid-is-the-best-way-to-document-your-architecture-in-the-ai-era-2dgb), Feb 25 2026): ASCII required 55 tokens vs 10 for the equivalent mermaid; mermaid avoids *"extra noise that makes understanding harder for models"* and reduces hallucination risk.

CodeBoarding ([blog.brightcoding.dev](https://www.blog.brightcoding.dev/2026/02/16/codeboarding-ai-powered-interactive-diagrams-for-codebases), Feb 16 2026): ships mermaid as their README-embed format because GitHub renders it natively and LLMs parse it cheaply.

### Emerging (use cases)

Multiple practitioner posts argue mermaid is net-positive *for both human readers and AI* because:
- It is text — survives token-efficiently
- It renders in GitHub / GitLab / VS Code natively
- It is structured — LLMs parse the relationships, not just the visual

### Honest gap

No source specifically addresses *folder-level* READMEs (vs root or architecture docs). The strongest defensible claim: mermaid is cheap and lazy-loaded folder READMEs cost nothing until consulted; therefore the cost-benefit is net-positive for any folder where genuine flow exists. This is a deductive synthesis, not a cited recommendation.

### Anti-pattern

Diagrams in auto-loaded `CLAUDE.md` directly trade against the <200 line target. Keep them in lazy-loaded files.

---

## 8. Progressive disclosure — index + load-on-demand

### Definite (multi-source convergence)

This pattern appears under multiple names across the literature:

- **SKILL.md best-practices**: *"SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide"* ([Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))
- **Microsoft agent-skills wiki**: progressive disclosure as architecture pattern ([deepwiki.com/microsoft/agent-skills/3.3](https://deepwiki.com/microsoft/agent-skills/3.3-progressive-disclosure))
- **Ardalis on optimizing agents**: index-then-load ([ardalis.com/optimizing-ai-agents-with-progressive-disclosure](https://ardalis.com/optimizing-ai-agents-with-progressive-disclosure/))
- **AGENTS.md v1.1 proposal**: same architecture, formalized in spec language

### Implications for folder READMEs

- A folder containing N files SHOULD have a table of contents enumerating them (the "index").
- The README itself is the index; the files are loaded on demand.
- This converts the folder from "N opaque files" into "1 navigable surface."

---

## 9. Diataxis reference architecture — structure mirrors content

### Definite

Diataxis framework ([diataxis.fr](https://diataxis.fr/)):

> "The architecture of reference documentation should reflect the structure or architecture of the thing it's describing."

> "Isolating reference material makes everything else better."

### Implications

- For a folder containing 14 agents, the README's table of contents IS the list of agent files — not a free-form prose summary.
- Reference docs (folder READMEs of inventories) should be visually skim-able, not narrative.
- Tables, lists, and code blocks beat paragraphs for reference content.

---

## 10. Tables, structured formats, XML vs markdown

### Definite (Anthropic)

Anthropic *Effective Context Engineering*:

> "We recommend organizing prompts into distinct sections (like `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`, etc) and using techniques like XML tagging or Markdown headers to delineate these sections, although the exact formatting of prompts is likely becoming less important as models become more capable."

Anthropic best-practices docs use tables heavily (include/exclude tables, strategy/before/after comparisons).

### Status: model-dependent, magnitude disputed

- Eugene Yan ([eugeneyan.com/writing/prompting](https://eugeneyan.com/writing/prompting/), May 2024): *"For Claude, XML tags work particularly well while other LLMs may prefer Markdown."*
- 2025 benchmarks ([improvingagents.com](https://www.improvingagents.com/blog/best-nested-data-format/)): XML required ~80% more tokens than markdown for equivalent data; format choice impacts model performance up to 40%.
- BUT: these are *data-format* studies (nested structured data), not *instruction-format* studies. Generalizing from "JSON vs YAML vs XML for data payloads" to "markdown vs XML for instructions" is a frequent unforced error.

### Recommendation

- Markdown with H2/H3 headings is fine for Claude Opus 4.7.
- Tables for enumerable content (inventories, enum values, comparisons).
- XML tags optional — no longer required for adherence on 4.x models.

---

## 11. Single source of truth — Apply when, federate when

### Definite (multi-source)

The unified-registry pattern dominates in the closest reference classes:

- **Schema registries** (Kafka/Confluent/Solace): centralized + per-entry compatibility metadata is the documented pattern; decentralized fragmented registries are named cost drivers ([Confluent: Schema Management Costs](https://master.www.confluent.io/blog/schema-management-costs/))
- **Agent corpora** (LangChain, CrewAI, DSPy): one catalog dispatched by source-type field; no surveyed framework splits ([LangChain document_loaders](https://reference.langchain.com/python/langchain-community/document_loaders), [CrewAI Knowledge](https://docs.crewai.com/en/concepts/knowledge), [DSPy multi-stage](https://www.rajapatnaik.com/blog/2025/10/23/langgraph-dspy-gepa-researcher))
- **Library science** (MARC, Dublin Core): one catalog faceted by type, not separate catalogs per format ([LoC MARC→DC crosswalk](https://www.loc.gov/marc/marc2dc.html))

### Contested

- **Data-mesh federation** (Dehghani via [martinfowler.com](https://martinfowler.com/articles/data-mesh-principles.html)): rejects monolithic SSOT — BUT explicitly because of *organizational scale and domain ownership*. The argument does not transfer to single-team, single-repo contexts.

### Failure modes — the named ones

**Split registries fail by** (from Kafka schema-registry literature + production RAG):
- Silent divergence of schema fields
- Cadence-induced staleness asymmetry
- Consumer routing ambiguity ("which file do I consult for X?")
- Migration friction when entries change category

**Unified registries fail by** (slower, more recoverable):
- Enum bloat
- Humans omit policy field; only validator catches it
- Orthogonal axis emerges → compound enum values become unparseable

### Recommendation

For single-team / single-repo agent docs: unified-with-per-entry-policy beats split-by-content-kind. Federation is justified only by organizational fragmentation, which doesn't apply.

The canon SSOT rewrite (canon/sources.yaml + canon/corpus/<slug>/citation.yaml, eliminating canon/sources.ingest.yaml) executes this finding.

---

## 12. Defending against documentation staleness

### Definite

The strongest staleness defense is **architectural, not editorial**.

- Google SRE Book Ch. 23: *"We deliberately avoided an in-depth discussion about specific algorithms, protocols, or implementations in this chapter. Distributed coordination systems and the technologies underlying them are evolving quickly, and this information would rapidly become out of date, unlike the fundamentals that are discussed here."*
- Anthropic Effective Context Engineering: *"CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing."*

**Reading:** don't try to keep volatile content fresh — exclude it from durable docs and route to live fetch.

### Empirical (Cochrane 2025 LSR study)

Even funded continuous-review programs miss >50% of declared cadence ([De Silva 2025 mixed-methods study](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70024)). Promising "review monthly" without tooling guarantees broken promise.

### Documented mitigations

- **`As of <date>` markers as queryable index** — Wikipedia `{{As of|YYYY}}` template auto-categorizes statements ([en.wikipedia.org/wiki/Template:As_of](https://en.wikipedia.org/wiki/Template:As_of))
- **HTTP `Sunset` header (RFC 8594)** — formalized machine-readable expiration ([datatracker.ietf.org/doc/html/rfc8594](https://datatracker.ietf.org/doc/html/rfc8594))
- **Source-tiering by volatility** — DataHub "Continuous Context" framing: declared/derived/observed, each with its own cadence ([datahub.com/blog/continuous-context](https://datahub.com/blog/continuous-context/)) — single-vendor advocacy, not multi-source consensus

### Implications for us

- Use `lifecycle: live-only` for volatile content (Claude Code docs, AGENTS.md spec). The canon rewrite already does this.
- Date-stamp every claim with `last_verified`. The canon rewrite already does this.
- Tier by volatility (durable/slow/fast/volatile). The canon rewrite already does this.
- DO NOT promise calendar cadences we won't keep without tooling support.

---

## 13. The synthesized folder-README template

Built from §§2-9 above, with extrapolations flagged.

```markdown
# <folder-name>/

<one-sentence purpose: what lives here, why>

**Read this when:** <2-3 conditions>   ← extrapolation; our convention
**Skip if:** <1-2 conditions>          ← same

## Inventory                            ← Diataxis reference + progressive disclosure
| File | Purpose | When invoked |
|---|---|---|

## How these compose                    ← mermaid where flow exists (Michelini)
[mermaid diagram OR ordered list of interactions]

## Conventions specific to this folder  ← Anthropic anti-duplication
[only what differs from root CLAUDE.md]

## Maintenance                          ← canon/README pattern
[how to add, edit, retire items in this folder]
```

Length: 150-250 lines per folder README (extrapolation; no Anthropic figure).

---

## 14. Anti-patterns — what NOT to do

Sourced from [Anthropic best-practices](https://code.claude.com/docs/en/best-practices) and the empty-`scripts/README.md` case study in humanlayer/humanlayer:

1. **Empty placeholder.** `# scripts` + generic install commands. Provides no signal an AI can act on.
2. **Duplicating root content.** Anthropic: *"Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions...if two rules contradict each other, Claude may pick one arbitrarily."*
3. **Missing inventory in folders-of-files.** A folder with 12 agents and no table of contents forces the AI to either glob+read all or guess from filenames.
4. **Vague descriptions.** Anthropic skill docs enumerate bad examples: *"Helps with documents," "Processes data," "Does stuff with files."*
5. **Deeply nested references.** *"Claude may partially read files when they're referenced from other referenced files...Keep references one level deep from SKILL.md."* Same principle for folder READMEs.
6. **Time-sensitive prose.** *"Don't include information that will become outdated"* — folder READMEs accumulate "as of [date]" notes that rot. Use `last_verified` field instead.
7. **Bloat.** *"If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."* Applies to any markdown Claude reads.
8. **AI attribution / "Generated by AI" footers.** Repo-specific anti-pattern per [CLAUDE.md](CLAUDE.md).
9. **Adding fields "just in case."** From canon/README.md anti-bloat rule: every additional field is auto-loaded surface and a maintenance burden on every entry.

---

## 15. Where this stack stands

Cross-referenced with [research/sota-2026-v2/14-project-instructions.md](research/sota-2026-v2/14-project-instructions.md) (CLAUDE.md / AGENTS.md SOTA) and the current repo state:

| Practice | Status | Notes |
|---|---|---|
| Auto-load vs lazy-load discipline | ✅ understood | CLAUDE.md is auto-loaded, READMEs lazy |
| <200 line CLAUDE.md target | ⚠️ violated | Currently 154 lines (target ≤120 per house style) |
| Pointer-over-paste | ✅ followed | CLAUDE.md uses bracketed-prose links, not `@`-imports |
| Per-directory READMEs | ⚠️ partial | canon/, session-artifacts/, upgrades/, .genesis/ have them; .claude/agents/, .claude/skills/, .claude/hooks/ do not |
| "What + when" descriptions | ✅ followed | All `.claude/agents/*.md` files have descriptive frontmatter |
| Single source of truth | ✅ followed | canon SSOT rewrite executed 2026-05-17 |
| Volatility tiering | ✅ followed | canon schema_version 2 has lifecycle/volatility/last_verified |
| Mermaid in lazy-loaded files | ❌ missing | No folder README currently uses mermaid |
| Progressive disclosure / inventory tables | ⚠️ partial | canon/README has it; others are prose |
| Diataxis reference structure | ⚠️ partial | Some READMEs are narrative where tabular would parse better |

---

## Sources (combined across both research turns)

### Anthropic (definite)
- [Anthropic — Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Anthropic — How Claude remembers your project (memory)](https://code.claude.com/docs/en/memory)
- [Anthropic — Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic — Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

### Cross-tool standards
- [AGENTS.md spec — Agentic AI Foundation](https://agents.md)
- [AGENTS.md v1.1 proposal (issue #135)](https://github.com/agentsmd/agents.md/issues/135) — opened 2026-01-08, status open
- [OpenAI Codex — Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

### Expert practitioners
- [HumanLayer — Writing a good CLAUDE.md (Nov 25 2025)](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Eugene Yan — Prompting Fundamentals (May 2024)](https://eugeneyan.com/writing/prompting/)
- [Ben Houston — Crafting READMEs for AI (Mar 28 2025)](https://ben3d.ca/blog/crafting-readmes-for-ai)
- [Eric Ma — How to teach your coding agent with AGENTS.md (Oct 4 2025)](https://ericmjl.github.io/blog/2025/10/4/how-to-teach-your-coding-agent-with-agentsmd/)
- [Simon Willison — Agentic AI Foundation (Dec 9 2025)](https://simonwillison.net/2025/Dec/9/agentic-ai-foundation/)
- [Simon Willison — A quote from Claude Docs (Oct 25 2025)](https://simonwillison.net/2025/Oct/25/claude-docs/)

### Diagrams in AI-consumed docs
- [Alessio Michelini — Why Mermaid is the Best Way to Document Architecture (Feb 25 2026)](https://dev.to/darkmavis1980/why-mermaid-is-the-best-way-to-document-your-architecture-in-the-ai-era-2dgb)
- [CodeBoarding — AI-Powered Interactive Diagrams (Feb 16 2026)](https://www.blog.brightcoding.dev/2026/02/16/codeboarding-ai-powered-interactive-diagrams-for-codebases)
- [Mermaid diagrams: AI meets documentation — Awesome Testing (Sep 2025)](https://www.awesome-testing.com/2025/09/mermaid-diagrams)

### Progressive disclosure
- [Microsoft agent-skills — Progressive Disclosure (DeepWiki)](https://deepwiki.com/microsoft/agent-skills/3.3-progressive-disclosure)
- [Steve Smith / Ardalis — Optimizing AI Agents with Progressive Disclosure](https://ardalis.com/optimizing-ai-agents-with-progressive-disclosure/)

### Documentation framework
- [Diátaxis — Start here](https://diataxis.fr/)
- [Sequin — We fixed our documentation with the Diátaxis framework](https://blog.sequinstream.com/we-fixed-our-documentation-with-the-diataxis-framework/)

### Library science (single-vs-split catalogs)
- [MARC to Dublin Core crosswalk (Library of Congress)](https://www.loc.gov/marc/marc2dc.html)
- [UT Austin — Cross-disciplinary metadata standards](https://guides.lib.utexas.edu/metadata-basics/general-standards)
- [Wikipedia — Single source of truth](https://en.wikipedia.org/wiki/Single_source_of_truth)
- [Scott Ambler — The One Truth Above All Else Anti-Pattern](https://agiledata.org/essays/onetruth.html)
- [Zhamak Dehghani / Fowler — Data Mesh Principles](https://martinfowler.com/articles/data-mesh-principles.html)
- [Alation Data Radicals — Zhamak Dehghani: Multiple Sources of Truth](https://www.alation.com/podcast/episodes/multiple-sources-of-truth-zhamak-dehghani/)

### Format comparisons (XML/markdown/YAML)
- [Improving Agents — Best nested data format benchmarks](https://www.improvingagents.com/blog/best-nested-data-format/)

### Agent framework patterns
- [LangChain document_loaders reference](https://reference.langchain.com/python/langchain-community/document_loaders)
- [CrewAI Knowledge concepts](https://docs.crewai.com/en/concepts/knowledge)
- [CrewAI Knowledge Sources (DeepWiki)](https://deepwiki.com/crewAIInc/crewAI/5.1-knowledge-sources)
- [DSPy multi-stage agentic researcher (Raja Patnaik, 2025)](https://www.rajapatnaik.com/blog/2025/10/23/langgraph-dspy-gepa-researcher)
- [HumanLayer — github.com](https://github.com/humanlayer/humanlayer)
- [HumanLayer hld/README.md](https://github.com/humanlayer/humanlayer/blob/main/hld/README.md)
- [Tiberriver256 — Skills catalog indexing AI context](https://tiberriver256.github.io/ai%20and%20technology/skills-catalog-part-1-indexing-ai-context/)

### Schema registries (single-vs-split background)
- [Confluent — Schema Management Costs](https://master.www.confluent.io/blog/schema-management-costs/)
- [Conduktor — Schema Evolution Best Practices](https://www.conduktor.io/glossary/schema-evolution-best-practices)
- [Solace — Schema Registry Best Practices](https://docs.solace.com/Schema-Registry/schema-registry-best-practices.htm)
- [Confluent — Schema Registry Deployment Architectures](https://docs.confluent.io/platform/current/schema-registry/multidc.html)

### RAG / freshness
- [RisingWave — RAG Architecture in 2026](https://risingwave.com/blog/rag-architecture-2026/)
- [Particula — When to cache LLM responses](https://particula.tech/blog/when-to-cache-llm-responses-decision-guide)
- [Chitika — RAG Production Guide 2025](https://www.chitika.com/retrieval-augmented-generation-rag-the-definitive-guide-2025/)
- [APXML — Monitoring Drift in Retrieval Components](https://apxml.com/courses/optimizing-rag-for-production/chapter-6-advanced-rag-evaluation-monitoring/monitoring-retrieval-drift-rag)

### Documentation staleness
- [Cochrane LSR guidance](https://community.cochrane.org/review-development/resources/living-systematic-reviews)
- [De Silva 2025 mixed-methods study on LSR cadence failure](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70024)
- [Wikipedia — Template:As_of](https://en.wikipedia.org/wiki/Template:As_of)
- [RFC 8594 — Sunset HTTP header](https://datatracker.ietf.org/doc/html/rfc8594)
- [DataHub — Continuous Context](https://datahub.com/blog/continuous-context/)

---

## Honest gaps (no SOTA answer found)

1. **Folder README length target** — no Anthropic-published figure. ≤300 lines is judgment.
2. **"Read this when / Skip if" preamble** — zero direct evidence; reasonable extension of skill-description discipline.
3. **Mermaid in folder READMEs specifically** — cost-benefit clear, but no source addresses this exact case.
4. **Relative vs absolute markdown link AI parsing** — our path-discipline rule is reasoned (privacy + portability) but unbenchmarked.
5. **No public Claude Code repo ships a fully-realized folder-README pattern** — humanlayer is the most active reference and their subdirectory docs are inconsistent. We're authoring the convention.

Per the operating principle, items 2-5 must be labeled as our convention, not industry SOTA, when used.

---

## Revision history

| Date | Change | By |
|---|---|---|
| 2026-05-17 | Initial combined synthesis of 2 research turns | Authored from research lanes triggered in two turns of the canon-rewrite session |
