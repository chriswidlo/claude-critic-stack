# Distillation — canon-librarian

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon retrieval on the question of how to handle a stale workflow doc — delete (a), consolidate (b), or expand (c). Librarian returned `corpus coverage: partial` with 4 supporting and 3 complicating passages, plus 3 stub entries flagged as not-ingested.

## Direct facts (supporting the delete/consolidate frame)

1. [Beyer et al., *Site Reliability Engineering*, 2016, ch. 28] "In a rapidly changing environment, documentation can fall out of date quickly. Outdated documentation is less of a problem for senior SREs … Newbie SREs are much more in need of up-to-date documentation, but may not feel empowered or knowledgeable enough to make changes." (confidence: direct)

2. [Beyer et al., *SRE*, 2016, ch. 28] On-call docs work best "when designed with just the right amount of structure … an adaptable body of work" — new team members are tasked with "overhauling one or two of the most outdated sections." (confidence: direct)

3. [Anthropic, *Effective Context Engineering for AI Agents*, Sep 2025] "CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing." (confidence: direct)

4. [Anthropic, *Effective Context Engineering*, 2025] "You should be striving for the minimal set of information that fully outlines your expected behavior." (confidence: direct)

5. [Anthropic, *Effective Context Engineering*, 2025] "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use." (confidence: direct)

## Direct facts (contradicting / complicating)

6. [Beyer et al., *SRE*, 2016, ch. 28] The on-call learning checklist "becomes a social contract by which (upon mastery) the student joins the ranks of on-call. The learning checklist sets the standard that all team members should aspire to and uphold." (confidence: direct) — Google treats it as a *first-class dedicated onboarding artifact*, not a derivative.

7. [Heilmeier Catechism, DARPA c. 1975, retrieved 2026] First questions: "What are you trying to do? Articulate your objectives using absolutely no jargon … Who cares? If you are successful, what difference will it make?" (confidence: direct)

8. [Anthropic, *Effective Context Engineering*, 2025] "Runtime exploration is slower than retrieving pre-computed data … Without proper guidance, an agent can waste context by misusing tools, chasing dead-ends, or failing to identify key information." (confidence: direct)

## Inferred claims

1. [canon-librarian] Stale workflow doc misroutes *new* readers specifically; senior readers compensate from memory — so the harm is concentrated on the population least able to push back. (confidence: inferred, from fact #1)

2. [canon-librarian] For this stack's *primary reader (Claude itself)*, `CLAUDE.md` is already the canonical workflow surface; a separate workflow doc would be a second index requiring sync. (confidence: inferred, from fact #3)

3. [canon-librarian] Multiple overlapping workflow descriptions create "ambiguous decision points about which doc is authoritative" — generalization from Anthropic's tools-bloat warning to docs. (confidence: inferred, from fact #5)

4. [canon-librarian] By Heilmeier's standard, option (c) — expanding the layout-only README into per-step what-and-why — is the strongest play because it co-locates explanation with artifacts. (confidence: inferred)

5. [canon-librarian] Pure just-in-time retrieval (option a) imposes an exploration cost on every new reader; option (a)'s defense must argue the exploration cost is genuinely low for this stack's onboarding population. (confidence: inferred, from fact #8)

6. [canon-librarian] "Deferred docs work tends to never happen" is folklore the corpus does not anchor. (confidence: inferred — a meta-observation about corpus gaps)

## Authority-framed claims

None. The librarian quoted sources directly and labeled inferences as its own synthesis. No "as Fowler would say" ventriloquism. The stub entries (Fowler, Feathers, Evans) are flagged as not-ingested with explicit "do not invent quotes" notes — properly handled.

## Contradictions surfaced

- **A. Minimalism / collapse-to-canonical** (Beyer ch.28 doc-rot passage; Anthropic minimal-context; Anthropic tool-bloat) **vs. B. Dedicated first-class onboarding artifact** (Beyer ch.28 learning-checklist-as-social-contract). Same chapter, both views — Google's SRE book simultaneously warns about staleness *and* prescribes a dedicated onboarding doc. The orchestrator must not collapse this; it is the core frame tension between option (a) and option (b)/(c).

- **C. JIT retrieval bypasses stale indexing** (Anthropic, fact #3) **vs. D. JIT retrieval imposes exploration cost without up-front guidance** (Anthropic, fact #8). Same source, two passages — the trade-off is internal to Anthropic's own essay.

- **E. CLAUDE.md is the canonical surface** (librarian inference #2) **vs. F. CLAUDE.md is operator-facing and dense; doesn't answer 'what is this and why' for new readers** (librarian inference #4, via Heilmeier). Tension between machine-reader optimization and human-reader onboarding.

## Subagent's own verdict (verbatim)

"**Partial.**" (corpus coverage)

## Gaps the subagent missed / flagged

1. README-as-front-door patterns / open-source onboarding conventions (no Raymond, no GitHub docs guidance) — librarian flagged.
2. The "deferred docs never happen" claim — folklore, no canon anchor — librarian flagged.
3. Literate-programming / docs-co-located-with-code (Knuth not in corpus) — librarian flagged.
4. **Not flagged by librarian:** the corpus has nothing on *which audience* this repo's workflow doc is actually for (human contributors vs. Claude vs. forkers) — the audience question is upstream of the delete/consolidate/expand choice and the librarian did not surface it.
5. **Not flagged:** no canon material on *cost of consolidation* (the work to merge into `CLAUDE.md` vs. the README) — orchestrator will need to reason about this without canon support.

## Token budget
~750 tokens.
