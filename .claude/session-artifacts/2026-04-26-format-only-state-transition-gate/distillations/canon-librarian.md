# canon-librarian distillation — 2026-04-26 format-only state-transition gate

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked the corpus what it has on a format-only validation gate at state-transition boundaries (8-state lifecycle, 22-entry personal corpus). Librarian returned **partial coverage**: SRE 2016 ch. 26 on out-of-band validation is the load-bearing entry; Cockburn 2005 supplies a port-adapter frame; three Anthropic posts (2024–2025) supply both a steel-man and the dominant complicating voice.

## Bias flags (preserve verbatim)
- **Single-source dominance:** SRE 2016 ch. 26 is the only direct treatment of validator design; both supporting AND contradicting passages come from the same chapter. One source, one voice.
- **Ecosystem bias:** Three of the most-cited entries are Anthropic-authored (building-effective-agents, effective-context-engineering, multi-agent-research-system). Same house style, same "simplest-thing-that-works" prior. Treat as one voice, not three.
- **Stub-only:** Evans (2003), Vernon (2013), Vernon-Jaskuła (2021) all `body_completeness: stub`. No body text. Do not invent quotes from DDD on aggregate invariants.

## Direct facts (supporting the design)
1. [SRE 2016, ch.26 §"Out-of-band data validation"] **Load-bearing counter-claim:** "When too strict, even simple, appropriate changes cause validation to fail. As a result, engineers abandon data validation altogether." Prescription: "only validate invariants that cause devastation to users." (confidence: direct)
2. [SRE 2016, ch.26] Validation framed as velocity unlock not tax: "devoting engineering resources to data validation endows other developers with the courage to move faster in the long run … results in an overall acceleration." (confidence: direct; assumes multi-developer team)
3. [Cockburn 2005, *Hexagonal Architecture*] "As events arrive from the outside world at a port, a technology-specific adapter converts it into a usable procedure call … The application is blissfully ignorant of the nature of the input device." Port contract = shape, not semantics. (confidence: direct)
4. [Anthropic, *Effective Context Engineering* 2025, §Tools] "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better." Operational test for "format check vs. critic" boundary. (confidence: direct)

## Direct facts (contradicting / complicating)
1. [Anthropic, *Building Effective Agents* 2024] "We recommend finding the **simplest solution possible**, and only increasing complexity when needed … For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough." Direct support for "8-state machine + per-state validators is over-engineering for 22 entries." (confidence: direct)
2. [SRE 2016, ch.26] "Out-of-band validators can be expensive at scale. A significant portion of Gmail's compute resource footprint supports a collection of daily validators." Even Google defaults to **out-of-band** (post-hoc, batch) validation, not pre-commit gates. Audit-mode is a viable alternative shape to gate-mode. (confidence: direct)
3. [Anthropic, *Effective Context Engineering* 2025] "Folder hierarchies, naming conventions, and timestamps all provide important signals." Supports schema-implicit-in-convention: moving file from `inbox/` to `active/` IS the state transition; collapses 8-state machine to 1-state-per-folder. (confidence: direct)
4. [SRE 2016, ch.26] Effective validation "demands all of the following: Validation job management; Monitoring, alerts, and dashboards; Rate-limiting features; Troubleshooting tools; Production playbooks." Personal-tool gate has none of this scaffolding. (confidence: direct)

## Inferred claims (librarian's synthesis, not source-direct)
1. [librarian] The "too-strict-leads-to-abandonment" warning is the single most important passage for this question — a format gate firing on stylistic nits will be disabled within a week. (confidence: inferred)
2. [librarian] Format-only gate maps cleanly onto Cockburn's port-adapter pattern: contract is "shape of entry" not "quality of idea." (confidence: inferred)
3. [librarian] SRE's velocity-unlock claim weakens substantially in the single-user case. (confidence: inferred)
4. [librarian] The user's framing must defend the choice of *gate* over *audit* explicitly — both are valid shapes per SRE. (confidence: inferred)

## Authority-framed claims
None. Librarian quoted sources directly throughout; no ventriloquism detected.

## Contradictions surfaced (preserve sharp edges)
- **Validation as velocity unlock (SRE 2016)** vs. **simplest-thing-that-works / don't build a workflow engine (Anthropic 2024)**. Same artifact (validators) framed as enabler vs. premature complexity. Resolution depends on team-size and corpus-size assumptions neither source addresses for the personal-tool case.
- **Pre-commit gate (implicit in user's design)** vs. **out-of-band batch validation (SRE 2016 default)**. Both from the same chapter. Gate-mode is one of two viable shapes; audit-mode may be cheaper in friction.
- **Explicit state machine with per-state validators** vs. **schema-implicit-in-folder-convention (Anthropic 2025)**. Latter collapses the 8 states into directory-as-state with shape-checks at boundaries.
- **Strict validation catches corruption (SRE supportive passage)** vs. **strict validation gets abandoned (SRE warning passage)**. Both from the same chapter, same section. The contradiction is internal to the source.

## Subagent's own verdict (verbatim)
"**Thin to partial.**" Corpus coverage is partial; SRE ch.26 is the only direct treatment, Cockburn supplies a frame, Anthropic supplies the complicating voice. "Everything else is adjacent at best."

## Gaps the subagent missed (or explicitly flagged as out-of-corpus)
1. **Postel's law / robustness principle** — absent. Cannot adjudicate "fail closed on missing section" vs. "warn and continue." Need RFC 760/761/793 or Allman 2011.
2. **"Make illegal states unrepresentable"** (Minsky / Wlaschin 2018 / Feldman 2016) — absent. Strongest counter-argument to runtime validators (encode lifecycle in types/structure) cannot be sourced.
3. **Schema-vs-prose-spec drift** — no JSON Schema / OpenAPI / Protobuf treatment. User explicitly raised this; corpus silent.
4. **Workflow engines / state-machine library threshold** — no BPMN, XState, Temporal, Harel statecharts. "Is 8 states enough to justify a library?" unanswerable from canon.
5. **Personal-tool adoption dynamics** — no Norman, no Kidder, no productivity-tooling literature. The "single user disables it Saturday morning" failure mode is unsourced.
6. **Linter scope-creep as anti-pattern** — folklore only (ESLint, Rubocop, prettier-vs-eslint). No canonical written treatment.
7. **Markdown/YAML toolchain practice 2026** — no entry younger than 2025 on this. WebSearch territory after librarian-first.

## Staleness flags
- Anthropic 2024–2025: current.
- SRE 2016: 10 years old; tradeoffs durable, no shift in underlying argument.
- Cockburn 2005: 20 years old; ports-and-adapters not contested.

## Token budget
~880 tokens.
