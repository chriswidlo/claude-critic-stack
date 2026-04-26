# Distillation — canon-librarian

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked canon to retrieve material on R&D-lab knowledge architecture: document-type taxonomies (ADR/RFC/lab notebook/position paper), maturity ladders for ideas, R&D org structure (Bell Labs/PARC/DeepMind/Anthropic), negative-results journals, zettelkasten cross-reference graphs, and "structure-first vs. accretion-first." Librarian returned **thin/partial coverage** — no direct entries on any primary topic; only adjacent material (SRE postmortems, Anthropic agent-orchestration, Cockburn ports-and-adapters). Returned a strong contradicting voice on "mature from day one."

## CORPUS BIAS WARNING (load-bearing for synthesis)
Librarian explicitly self-flags: corpus skews systems-engineering (DDD, hexagonal, EIP, SRE) and agent-orchestration (Anthropic trio, Reflexion). **Zero entries on research-process methodology, knowledge-management/PKB, or R&D org history.** Librarian's instruction to orchestrator: weight canon distillation lower than usual relative to outside-view; explicitly flag in synthesis that maturity-ladder semantics, doc-type taxonomy, and cross-reference vocabulary lack canonical anchoring (higher-uncertainty design moves). **This is the wrong corpus for this question.**

## Direct facts (quoted material)

1. [Google SRE Team, *Site Reliability Engineering* (2016), Ch. 15] "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring." Also: "It is important to define postmortem criteria before an incident occurs so that everyone knows when a postmortem is necessary." (confidence: direct)

2. [Google SRE 2016, same chapter] "Blameless postmortems are a tenet of SRE culture. […] When postmortems shift from allocating blame to investigating the systematic reasons why an individual or team had incomplete or incorrect information, effective prevention plans can be put in place." (confidence: direct)

3. [Google SRE 2016, same chapter] "Postmortem reading clubs: Teams host regular postmortem reading clubs […] often the postmortem being reviewed is months or years old!" (confidence: direct)

4. [Anthropic, *How we built our multi-agent research system* (2025)] "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information." (confidence: direct)

5. [Anthropic, multi-agent system 2025] "Subagent output to a filesystem to minimize the 'game of telephone.' […] specialized agents can create outputs that persist independently." (confidence: direct)

6. [Anthropic, *Effective Context Engineering for AI Agents* (2025)] "To an agent operating in a file system, the presence of a file named `test_utils.py` in a tests folder implies a different purpose than a file with the same name located in `src/core_logic/`. Folder hierarchies, naming conventions, and timestamps all provide important signals." (confidence: direct)

7. [Alistair Cockburn, *Hexagonal Architecture* (2005)] "The application communicates over 'ports' to external agencies. […] The protocol for a port is given by the purpose of the conversation between the two devices." (confidence: direct)

## Contradicting passages (PROMINENCE PRESERVED — load-bearing)

### Contradiction 1 — strongest contradicting voice
[Anthropic, *Effective Context Engineering for AI Agents* (2025)] "As model capabilities improve, agentic design will trend towards letting intelligent models act intelligently, with progressively less human curation. Given the rapid pace of progress in the field, **'do the simplest thing that works' will likely remain our best advice** for teams building agents on top of Claude." (confidence: direct)
- **Direct contradiction of the user's "mature from day one / no phase-one-evolves-later" frame.** From the same authors whose multi-agent paper the operator implicitly models on.

### Contradiction 2 — just-in-time / accretion
[Anthropic, *Effective Context Engineering for AI Agents* (2025)] "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers […] this approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems […] which grow with the material they index." (confidence: direct)
- Indexing systems **grow with material**; not designed top-down before first email. Direct counter to "global view first, no compromises."

### Contradiction 3 — generic simplicity warning
[Anthropic, *Building Effective Agents* (2024)] "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. […] [Frameworks] can also make it tempting to add complexity when a simpler setup would suffice." (confidence: direct)
- The lab is structurally a framework. Same warning applies.

## Inferred claims (librarian's synthesis from direct material)

1. [canon-librarian, from SRE Ch. 15] Three load-bearing primitives lab can borrow: trigger criteria defined in advance; template-driven format; review and publication as separate states. Maps to maturity ladder where "draft → reviewed → published → integrated" is structural, not just status. (confidence: inferred)

2. [canon-librarian, from SRE blameless framing] Failure-archive entries should explain why a killed idea seemed reasonable given information at the time, otherwise operator under-writes/sanitizes. (confidence: inferred)

3. [canon-librarian, from SRE reading-clubs] Archive is dead unless it has recurrence ritual. (confidence: inferred)

4. [canon-librarian, from Anthropic multi-agent] Discipline divisions should be defined by (objective + output format + boundary), not by topic naming. A "discipline" = (what question?) + (what artifact?) + (what's not in scope?). (confidence: inferred)

5. [canon-librarian, from Anthropic context-engineering] Folder hierarchy and naming themselves are load-bearing semantic primitives. Names that imply false equivalence actively mislead. (confidence: inferred)

6. [canon-librarian, from Cockburn] Lab/workflow boundary is a ports-and-adapters problem. Naming the *protocols* between lab and workflow is the load-bearing move, not just directory structure. (confidence: inferred)

7. [canon-librarian, from filesystem-artifacts passage] Durable artifacts on disk + lightweight references beat in-context summaries; passage does **not** specify cross-reference vocabulary. (confidence: inferred)

## Authority-framed claims
None. Librarian cited authors with quoted passages; no ventriloquism detected.

## Contradictions surfaced (sharp edges to preserve)

- **"Mature from day one / global view first" (user frame)** vs. **Anthropic 2025 "do the simplest thing that works"** + **Anthropic 2025 just-in-time indexing grows with material** + **Anthropic 2024 simplest solution, increase complexity only when needed.** Three independent direct quotes from the operator's own implicitly-modeled source contradict the operator's frame.
- **SRE: "define criteria before an incident"** (pro-upfront-structure) vs. **Anthropic: "indexing systems grow with the material they index"** (pro-accretion). Both are direct quotes; both apply.

## Subagent's own verdict (verbatim)
"thin / partial." Also: "Wrong corpus for this question. Orchestrator should weight canon distillation lower than usual relative to outside-view, and explicitly flag in synthesis that maturity-ladder semantics, doc-type taxonomy, and cross-reference vocabulary lack canonical anchoring (higher-uncertainty design moves)."

## Gaps the subagent missed / declared
Librarian explicitly declares (corpus does NOT cover):
1. Document-type taxonomies in research operations (ADRs/RFCs/design-docs/position-papers/lab-notebooks). Closest = SRE postmortems (one type, not a taxonomy).
2. Maturity ladders for ideas/claims (TRL/GRADE/hypothesis-progression).
3. R&D org structure (Gertner/Hiltzik/AI-lab divisions).
4. Cross-reference grammar (ADR superseded-by chains, zettelkasten Folgezettel).
5. Methods/methodology slot.
6. Naming as frame-shaping.

Recommends canon-refresher pass adding: Henderson on ADRs; IETF RFC 2026; Ahrens *How to Take Smart Notes*; NASA TRL; GRADE; Gertner *The Idea Factory*; Hiltzik *Dealers of Lightning*. Also flags many adjacent entries are stubs (`fowler-refactoring`, `vernon-strategic-monoliths`, `evans-ddd`, `vernon-iddd`, `feathers-legacy-code`, `nygard-release-it`, `helland-life-beyond-distributed-transactions`, `fowler-poeaa`, `meszaros-xunit`, `hohpe-eip`, `beck-tdd`) and `shinn-reflexion-2023` is abstract_only.

Orchestrator-side gap not addressed by librarian: no canon evidence on whether labs that started "mature" outperformed labs that accreted. Outside-view should carry this.

## Token budget
~1050 tokens.
