# canon-librarian return — orphans-fate

## Corpus coverage

**thin.** The decision sits at the intersection of (a) documentation lifecycle / ADR practice and (b) YAGNI / Rule-of-Three / minimal-primitive design. **The four highest-value sources for this question are stubs in the corpus and have no ingested body text:**

- `fowler-refactoring` (Fowler, *Refactoring*, 2018) — body_completeness: **stub**, paywalled, no open edition. Would carry the Rule-of-Three and YAGNI material.
- `nygard-release-it` (Nygard, *Release It!*, 2018) — body_completeness: **stub**, paywalled. Nygard is also the originator of the ADR practice (separate 2011 blog post, *not* in corpus); his "documentation as a journal of decisions" framing is the clearest counter to YAGNI here.
- `beck-tdd` (Beck, *TDD*, 2018) — stub. "You aren't gonna need it" is canonically Beck/Cunningham/XP; not retrievable here.
- `feathers-legacy-code` (Feathers, *Working Effectively with Legacy Code*, 2004) — stub. Would carry doc-decay material.

No entry on Andy Matuschak / *evergreen notes*, no entry on Hunt & Thomas (*Pragmatic Programmer*, "DRY for knowledge"), no entry on Gall, no Conway entry. The corpus has no ADR primary source at all.

I am not substituting other authors for these works. What follows are passages from populated entries that bear *obliquely* on the decision — they are weaker than the absent primary sources would be.

## Supporting passages

### Position A — "do not invent the primitive yet" (YAGNI / minimal-primitive design)

1. **Anthropic, *Building Effective Agents* (2024), §"When (and when not) to use agents".**
   > "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. … [Frameworks] often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice."

   Relevance: a four-orphan instance is the textbook situation where introducing a "lifecycle/archive primitive" *is* the extra abstraction layer — solve the four cases first, see whether a primitive falls out of the fifth.

2. **Anthropic, *Building Effective Agents* (2024), closing recommendations.**
   > "Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production."

   Relevance: argues against premature codification of process; "basic components" here maps to "decide ad-hoc per orphan."

3. **Anthropic, *Effective Context Engineering* (2025), §on hybrid retrieval.**
   > "Claude Code is an agent that employs this hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees. … 'do the simplest thing that works' will likely remain our best advice."

   Relevance: explicit instance of preferring just-in-time retrieval over a maintained-index primitive specifically because the maintained primitive *goes stale*. Direct analog to "if we invent an archive primitive, who maintains its accuracy?"

4. **Anthropic, *Building a Multi-Agent Research System* (2025), §scaling rules.**
   > "Scale effort to query complexity. Agents struggle to judge appropriate effort for different tasks, so we embedded scaling rules in the prompts. Simple fact-finding requires just 1 agent with 3-10 tool calls … These explicit guidelines help the lead agent allocate resources efficiently and prevent overinvestment in simple queries, which was a common failure mode in our early versions."

   Relevance: by analogy, "four orphan documents" is a small-N query; inventing a lifecycle primitive is the over-allocation failure mode.

### Position B — "write the policy down now while the decision context is fresh" (ADR / Nygard school)

**No ingested passage.** The natural sources are:
- Michael Nygard, "Documenting Architecture Decisions" (2011 blog post — *not in corpus*).
- *Release It!* 2nd ed. (2018) — **`nygard-release-it` entry is a stub**; full text not ingested.

The Nygard argument, summarized in prose without quotation: a decision's *context* is most retrievable at the moment the decision is made; written records deteriorate in fidelity quickly; therefore even a small policy is worth writing if there is any chance it recurs. **I am declining to fabricate a quote.** If this position needs to be load-bearing, populate `nygard-release-it` per the README instructions, or fetch the 2011 ADR post via WebFetch with explicit user consent.

The closest *populated* passage that gestures toward this position:

5. **Google SRE book (Beyer, Jones, Petoff, Murphy, 2016), Ch.14 "Managing Incidents", on the living incident document.**
   > "The incident commander's most important responsibility is to keep a living incident document. … This living doc can be messy, but must be functional. Using a template makes generating this documentation easier, and keeping the most important information at the top makes it more usable."

   Relevance: *weak* support for the "write the policy down" side — argues that templates pay off even for transient artifacts. Does not directly address "should you invent a new template after only four instances."

## Contradicting or complicating passages

1. **Anthropic, *Effective Context Engineering* (2025) — same passage as Supporting #3, read against itself.**
   > "… effectively bypassing the issues of stale indexing …"

   Why this complicates the framing: the passage cuts both ways. It argues that *maintained* primitives (an archive index) go stale — favoring ad-hoc. But it also implies that *the primitive itself* (glob, grep) is a stable, named, reusable abstraction. So "no new primitive" can degrade into "everyone reinvents the orphan-handling wheel each time," which is the very failure ad-hoc-ism produces. The honest read: a *lightweight retrieval-style* primitive (a convention, not a workflow) may be the synthesis.

2. **Google SRE book (2016), Ch.5 "Eliminating Toil", definition of *systems engineering*.**
   > "Systems engineering: Involves configuring production systems, modifying configurations, or documenting systems in a way that produces lasting improvements from a one-time effort."

   Why this complicates the framing: SRE explicitly valorizes "one-time effort that produces lasting improvement" — i.e., codify-the-policy-now. If an archive primitive is genuinely 30 minutes of work and removes recurring "what do we do with this?" decisions, the SRE frame says invent it. The frame *against* a primitive must argue that the recurring decision cost is lower than the primitive's maintenance cost — a claim, not a default.

3. **Anthropic, *Building a Multi-Agent Research System* (2025), §on coordination cost.**
   > "Multi-agent systems have key differences from single-agent systems, including a rapid growth in coordination complexity. Early agents made errors like spawning 50 subagents for simple queries …"

   Why this complicates the framing: a *named* primitive ("archive", "deprecate", "retire") is exactly the kind of cheap coordination scaffold that prevents the four humans (or four future-LLM-sessions) operating on this repo from each inventing their own treatment. The cost of *not* having a primitive scales with the number of independent decision-makers — and an R&D repo with LLM agents in the loop has more of those than it looks.

## Gaps

The corpus does not answer:

1. **What N is the Rule of Three for *documentation* primitives?** (Fowler's "three" was for *code* duplication; whether documents follow the same exponent is unargued in the populated corpus.)
2. **Decay rates of unmaintained ADRs / process docs** in small (<5-person) R&D repos. No empirical entry.
3. **The specific case of "shipped phase plans"** — i.e., docs whose factual content remains true but whose *function* (driving in-flight work) has expired. This is the most interesting of the four orphans and the corpus has nothing on it.
4. **Conway's Law as applied to documentation conventions** in solo / small-team repos — no entry.
5. **Andy Matuschak's *evergreen notes* / Hunt & Thomas's "DRY for knowledge"** — no entry. Both are the canonical modern treatments of "reference vs. ephemeral artifacts." Recommend `canon-refresher` consider these as candidates.

## Staleness flag

The two most relevant *populated* sources are 2024–2025 (Anthropic) and 2016 (SRE book). The 2016 SRE material on documentation predates the modern docs-as-code / ADR-explosion era; weight it accordingly. The Fowler/Beck/Nygard stubs are 2018 — not stale on their topics, but not retrievable here.
