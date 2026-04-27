# Canon retrieval — stale workflow doc: delete vs. consolidate vs. expand

**Session:** `2026-04-27-item-04-stale-workflow-docs`

## Corpus coverage

**Partial.** The corpus has direct hits on (a) doc rot in fast-changing systems and (b) just-in-time vs. up-front context retrieval — both highly relevant analogies. It has no direct treatment of "single source of truth for prose docs" or README hygiene. Several adjacent works (Fowler *Refactoring*, Beck *TDD*, Feathers *Legacy Code*, Evans *DDD*) are **stub** entries with full text not ingested; quoting them would be fabrication.

## Supporting passages

### 1. Beyer et al., *Site Reliability Engineering* (2016), ch. 28 "Accelerating SREs to On-Call and Beyond" — *Documentation as Apprenticeship*

> "In a rapidly changing environment, documentation can fall out of date quickly. Outdated documentation is less of a problem for senior SREs who are already up to speed, because they keep state on the world and its changes in their own heads. Newbie SREs are much more in need of up-to-date documentation, but may not feel empowered or knowledgeable enough to make changes."

**Relevance:** Names exactly the failure mode here — a stale workflow doc misroutes *new* readers (the only readers who can't compensate from memory). Supports option (a): removing the misleading artifact is higher-value than leaving it in place hoping someone updates it.

### 2. Beyer et al., *Site Reliability Engineering* (2016), ch. 28

> "When designed with just the right amount of structure, on-call documentation can become an adaptable body of work that harnesses newbie enthusiasm and senior knowledge to keep everyone fresh. […] As the new team member arrives, we point them to the overall learning checklist, but also task them with overhauling one or two of the most outdated sections."

**Relevance:** Counsels structural minimalism over volume — a single authoritative checklist that gets pruned and overhauled, not a proliferation of parallel docs. Aligns with consolidating around `CLAUDE.md` + `session-artifacts/README.md` rather than adding a third.

### 3. Anthropic, *Effective Context Engineering for AI Agents* (Sep 2025), §"Context retrieval and agentic search"

> "Claude Code is an agent that employs this hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees."

**Relevance:** Direct evidence that, *for this stack's actual primary reader (Claude itself)*, `CLAUDE.md` is already the canonical workflow surface; a separate `workflows/12-step-workflow.md` would be a second index that has to stay in sync with the one that's actually loaded into context.

### 4. Anthropic, *Effective Context Engineering* (2025), §"The anatomy of effective context"

> "You should be striving for the minimal set of information that fully outlines your expected behavior. (Note that minimal does not necessarily mean short; you still need to give the agent sufficient information up front to ensure it adheres to the desired behavior.)"

> "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

**Relevance:** Generalizes from tools to docs — multiple overlapping workflow descriptions create ambiguous decision points about *which doc is authoritative*. Supports (a): collapse to fewer canonical surfaces.

## Contradicting / complicating passages

### 5. Beyer et al., *SRE* (2016), ch. 28 — *Documentation as Apprenticeship*, on the on-call learning checklist

> "This doc helps establish the boundaries of the system their team supports. By studying this list, the student gains a sense of what systems are most important and why. […] The doc becomes a social contract by which (upon mastery) the student joins the ranks of on-call. The learning checklist sets the standard that all team members should aspire to and uphold."

**Why this complicates the framing:** Google explicitly advocates for a *dedicated, structured onboarding artifact* — not "point new readers at two existing authoritative docs and let them assemble the picture." Under this view, option (b) (a unified workflow doc) is the right target and option (a) is a regression. The plan's deferral of (b)/(c) is the kind of move that, in practice, never gets undone — note that the SRE chapter treats the checklist as a *first-class onboarding artifact*, not a derivative of operator docs.

### 6. Heilmeier Catechism (DARPA, c. 1975; DARPA institutional page, retrieved 2026)

> "What are you trying to do? Articulate your objectives using absolutely no jargon. How is it done today, and what are the limits of current practice? […] Who cares? If you are successful, what difference will it make?"

**Why this complicates the framing:** The catechism's first question is *jargon-free articulation for someone who doesn't already know the system*. `CLAUDE.md` is operator-facing and dense; `session-artifacts/README.md` is layout-only. Neither answers "what is the 12-step workflow and why does it exist" in plain language for a new reader. By Heilmeier's standard, option (c) — expanding the README from layout-only into per-step what-and-why — is the strongest play, because it grounds the explanation next to the artifacts a reader will actually encounter, satisfying the "minimal documentation that lives close to what it documents" principle without creating a new free-floating doc. The (a)-now recommendation arguably leaves the "who cares / why" question unanswered for the audience that needs it most.

### 7. Anthropic, *Effective Context Engineering* (2025), §"Context retrieval and agentic search"

> "Of course, there's a trade-off: runtime exploration is slower than retrieving pre-computed data. Not only that, but opinionated and thoughtful engineering is required to ensure that an LLM has the right tools and heuristics for effectively navigating its information landscape. Without proper guidance, an agent can waste context by misusing tools, chasing dead-ends, or failing to identify key information."

**Why this complicates the framing:** Pure just-in-time retrieval (option a: "go read the two authoritative docs") imposes an exploration cost on every new reader — human or agent. A small amount of *opinionated up-front context* (option b or c) can pay for itself many times over. The plan's defense of (a) needs to argue that the exploration cost is genuinely low for *this* stack's onboarding population.

## Stub / fetch-blocked entries that *would* be relevant if ingested

- **Fowler, *Refactoring* (2018)** — likely has direct material on "comments as deodorant" / when prose explanation signals a missing abstraction. Stub; full text not ingested. Do not invent quotes.
- **Feathers, *Working Effectively with Legacy Code* (2004)** — likely treats stale documentation as a legacy-code analogue. Stub.
- **Evans, *Domain-Driven Design* (2003)** — ubiquitous-language and document-as-conversation themes. Stub.

## Gaps

The corpus does not directly cover:

1. README-as-front-door patterns or open-source onboarding doc conventions (no Raymond, no GitHub docs guidance).
2. The specific "deferred docs work tends to never happen" claim — this is folklore the corpus does not anchor.
3. Literate programming / docs-co-located-with-code arguments (Knuth not in corpus).

**Staleness note:** SRE *Book* is 2016; the doc-rot chapter remains widely cited and current consensus has if anything strengthened. Anthropic context-engineering essay is Sep 2025, current.
