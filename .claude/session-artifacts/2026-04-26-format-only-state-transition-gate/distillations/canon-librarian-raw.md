# canon-librarian raw return — 2026-04-26 format-only state-transition gate

## Corpus coverage

**Thin to partial.** The corpus is heavily weighted toward distributed-systems engineering (SRE, DDD, hexagonal, EIP), agent design (Anthropic 2024–2025), and software-design classics (Fowler, Beck, Feathers — most as `stub` entries with no body text). It contains **no direct treatment** of:

- Postel's law / robustness principle
- "Make illegal states unrepresentable" (Minsky / OCaml / Elm tradition)
- Pre-commit hooks vs. CI validation
- Markdown/YAML linter ecosystems (markdownlint, yamllint, ajv, JSON Schema)
- Workflow engines (BPMN, Temporal, XState)
- Personal-tool adoption dynamics / single-user productivity systems

The most directly applicable passage in the corpus is the SRE chapter on **out-of-band data validation**, which is squarely about validators, their failure modes, and the strict-vs-lax tradeoff. Hexagonal architecture supplies a frame for "format adapter at the boundary." The Anthropic agents posts supply the dominant *complicating* voice ("simplest thing that works; do not build a state machine when a single check suffices"). Everything else is adjacent at best.

## Single-source / ecosystem bias flagged

- **Three of the most relevant entries are Anthropic-authored** (building-effective-agents, effective-context-engineering, multi-agent-research-system). They share a house style and a strong "simplest-thing-that-works" prior. Treat their convergence as one voice, not three.
- **No entry from the Postel / IETF / protocol-design tradition.** The "tolerance principle" question cannot be answered from this corpus; you would need to add Jon Postel (RFC 760/761/793) or Eric Allman ("The Robustness Principle Reconsidered", ACM Queue 2011) to ground it.
- **No entry from the type-theory / "illegal states" tradition.** Yaron Minsky's "Effective ML" talks, Richard Feldman's "Making Impossible States Impossible" (Elm Conf 2016), and Scott Wlaschin's *Domain Modeling Made Functional* (2018) are the canonical references and are absent.
- **No entry on workflow modeling.** No BPMN, no XState docs, no Temporal/Cadence material, no Petri-net literature. The state-machine-as-overkill counterargument cannot be sourced from canon.
- **DDD/aggregate-invariant material is all stub.** Evans (2003), Vernon (2013), and Vernon-Jaskuła (2021) all have `body_completeness: stub` — they would be the natural home for "invariants enforced at aggregate boundary," but no body text is ingested. Do not invent quotes from them.

## Supporting passages

### 1. Google SRE team, *Site Reliability Engineering* (2016), Ch. 26 "Data Integrity," §"Out-of-band data validation"

> "Out-of-band data validation is tricky to implement correctly. When too strict, even simple, appropriate changes cause validation to fail. As a result, engineers abandon data validation altogether. If the data validation isn't strict enough, user experience–affecting data corruption can slip through undetected. **To find the right balance, only validate invariants that cause devastation to users.**"

> "Drive infrastructure developers were so invested in data integrity that they also enhanced their validators to automatically fix such inconsistencies. This safeguard turned a potential emergency 'all-hands-on-deck-omigosh-files-are-disappearing!' data loss situation in 2013 into a business as usual, 'let's go home and fix the root cause on Monday,' situation."

**Relevance:** Directly endorses the design instinct behind a format-only gate — pick a small set of invariants whose violation is genuinely destructive (here: an entry that can't be advanced through the lifecycle because a downstream consumer assumes a section exists), and enforce only those. The "too-strict-leads-to-abandonment" warning is the single most important passage in the corpus for this question: a format gate that fires on stylistic nits will be disabled within a week.

### 2. Google SRE team, *Site Reliability Engineering* (2016), Ch. 26, §"Out-of-band data validation"

> "Shunting some developers to work on a data validation pipeline can slow engineering velocity in the short term. However, devoting engineering resources to data validation endows other developers with the courage to move faster in the long run, because the engineers know that data corruption bugs are less likely to sneak into production unnoticed. Similar to the effects enjoyed when units test are introduced early in the project lifecycle, a data validation pipeline results in an overall acceleration of software development projects."

**Relevance:** Frames validation as a *velocity unlock*, not a tax — exactly the steel-manning the design needs. Note this assumes a multi-developer team; the personal-tool case (single user, 22 entries) weakens the claim significantly.

### 3. Alistair Cockburn, *Hexagonal Architecture* (2005), §"The Pattern: Ports and Adapters"

> "As events arrive from the outside world at a port, a technology-specific adapter converts it into a usable procedure call or message and passes it to the application. The application is blissfully ignorant of the nature of the input device."

> "The protocol for a port is given by the purpose of the conversation between the two devices. The protocol takes the form of an application program interface (API)."

**Relevance:** A format-only gate is a *port adapter* between the markdown-authoring world and the lifecycle-state-machine world. The gate's contract is "shape of the entry," not "quality of the idea" — exactly the asymmetric concern Cockburn names. This is the cleanest architectural framing for the hard scope boundary the user wants to preserve.

### 4. Anthropic, *Effective Context Engineering for AI Agents* (2025), §"Tools"

> "Tools should be self-contained, robust to error, and extremely clear with respect to their intended use. Input parameters should similarly be descriptive, unambiguous, and play to the inherent strengths of the model."

> "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

**Relevance:** Reframed for this design: if a *human* author can't tell whether a given lint failure means "fix the format" or "rethink the idea," the gate has slipped from format-checker into critic. This is a useful operational test for the scope boundary.

## Contradicting or complicating passages

### 1. Anthropic, *Building Effective Agents* (2024), §"When and how to use frameworks"

> "When building applications with LLMs, we recommend finding the **simplest solution possible**, and only increasing complexity when needed. … Workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale. For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough."

> "These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice."

**Why this complicates the framing:** A 22-entry personal corpus with an 8-state lifecycle is the textbook case where this advice bites. An "8-state lifecycle with format-only gate" *sounds* small but is already a workflow engine in miniature — states, transitions, transition guards, validators per state. The contradicting position the user named — *"state-machine validators are over-engineering for a 22-entry corpus"* — has direct support here. The cheaper alternative ("a single check at one transition, no machine, no per-state schema") deserves a real comparison before the state machine is committed.

### 2. Google SRE team, *Site Reliability Engineering* (2016), Ch. 26, §"Out-of-band data validation"

> "Out-of-band validators can be expensive at scale. A significant portion of Gmail's compute resource footprint supports a collection of daily validators. … In one such refactoring effort, we cut the contention for disk spindles by 60% without significantly reducing the scope of the invariants they covered."

**Why this complicates the framing:** Even Google's SREs treat *out-of-band* (post-hoc, batch) validation as the default mode for data-integrity checks — not pre-commit gates. The implicit thesis ("validate at the moment of state transition") is one of two viable shapes; the other is "let drift happen, run a validator nightly, surface a report." For a single-user lab folder, the batch-rectification mode may be substantially cheaper in friction terms, even if it means stale state. The user's framing should defend the choice of *gate* over *audit* explicitly.

### 3. Anthropic, *Effective Context Engineering for AI Agents* (2025), §"Context retrieval and agentic search"

> "To an agent operating in a file system, the presence of a file named test_utils.py in a tests folder implies a different purpose than a file with the same name located in src/core_logic/. Folder hierarchies, naming conventions, and timestamps all provide important signals that help both humans and agents understand how and when to utilize information."

**Why this complicates the framing:** This is the "schema-implicit-in-code/convention" position the user listed as a counter-frame. If folder location and naming already carry the lifecycle state, a separate state-machine validator may be redundant — moving a file from `inbox/` to `active/` is itself the state transition, and the only invariant worth enforcing is "the file's *shape* matches what `active/` consumers expect." That collapses the 8-state machine into a 1-state-per-folder convention with shape-checks at directory boundaries, which is meaningfully smaller.

### 4. Google SRE team, *Site Reliability Engineering* (2016), Ch. 26, §"Out-of-band data validation"

> "Mature Google services provide on-call engineers with comprehensive documentation and tools to troubleshoot. … Effective out-of-band data validation demands all of the following: Validation job management; Monitoring, alerts, and dashboards; Rate-limiting features; Troubleshooting tools; Production playbooks."

**Why this complicates the framing:** Even the supportive passage carries a hidden cost: validators that are taken seriously require a substantial *operational surround* (playbooks, dashboards, troubleshooting). A personal-tool gate has none of that scaffolding. The likely failure mode is not "the gate stops me from advancing a bad entry" but "the gate fails opaquely on Saturday morning and I disable it." The design must price in the personal-tooling adoption dynamic that the corpus does not cover.

## Gaps the corpus does not answer

1. **Postel's law / tolerance in format design.** Should the gate be strict on output (what the lifecycle produces) and lenient on input (what the author writes)? The classical answer ("be liberal in what you accept") and its modern repudiation (Allman 2011, "The Robustness Principle Reconsidered") are both absent. Without these, the corpus cannot adjudicate "fail closed on missing required body section" vs. "warn and continue."

2. **"Make illegal states unrepresentable."** The type-theoretic alternative — encode the lifecycle in the file system / front-matter structure such that an invalid state literally cannot be expressed — is the strongest counter-argument to a runtime validator, and the corpus has nothing on it. Add Wlaschin (2018), Minsky's "Effective ML" lectures, or Feldman's Elm Conf 2016 talk if this thread matters.

3. **Schema vs. prose-spec drift.** The user's question explicitly raises "schemas duplicate prose specs and the prose decays first." The corpus has no treatment of schema-as-source-of-truth (JSON Schema, OpenAPI, Protobuf), nor of the maintenance-burden literature (Lutz Prechelt, "An Empirical Comparison of Seven Programming Languages" is the closest classical reference; absent here).

4. **State-machine library selection / overkill threshold.** No XState, no Temporal, no Statecharts (Harel 1987), no BPMN. The "is 8 states enough to justify a library?" question cannot be answered from canon.

5. **Personal-tool adoption dynamics.** Tracy Kidder, *The Soul of a New Machine*; Don Norman, *The Design of Everyday Things*; or any of the productivity-tooling literature would speak to "validators that the only user disables within a week." Not in corpus.

6. **Linter scope-creep as anti-pattern.** The "validator that grows into a critic" dynamic is folklore (ESLint plugin proliferation, Rubocop "cops" arguments, the prettier-vs-eslint split) but no canonical written treatment is in this corpus.

## Staleness flags

- The Anthropic posts (2024, 2025) are current; their advice reflects 2024–2025 agent-design consensus.
- The SRE chapter (2016) is ten years old, but the validator-design tradeoffs it names are durable; nothing has shifted in the underlying argument.
- Cockburn's hexagonal essay (2005, Web Archive snapshot) is twenty years old; the ports-and-adapters frame remains canonical and is not contested.
- **No entry younger than 2025 speaks to markdown/YAML toolchain practice.** If "what does the markdownlint/remark/ajv ecosystem actually look like in 2026" matters, the corpus cannot answer it — that is a `WebSearch` job after librarian-first.
