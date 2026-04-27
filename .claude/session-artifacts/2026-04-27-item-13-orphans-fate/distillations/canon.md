# Distillation — canon-librarian (orphans-fate)

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage on what to do with four "orphan" documents in a small R&D repo: invent a lifecycle/archive primitive (Position B, ADR / write-it-down) vs. handle ad-hoc and let a primitive emerge later (Position A, YAGNI / minimal-primitive). Librarian returned populated Anthropic + SRE passages on Position A and explicitly declined to fabricate Position B quotes because the natural sources are stubs.

## CRITICAL CORPUS GAP — read before weighting anything below
The librarian's return is **asymmetrically supported**. Position A (minimal-primitive / YAGNI / just-in-time) has four populated Anthropic passages that bear directly on the question. Position B (ADR / write-it-down) has **zero** ingested primary-source passages; the closest populated proxy is one Google SRE passage on living incident docs, which the librarian rates as *weak*. The four highest-value sources for this decision are stubs:
- `fowler-refactoring` (2018) — stub, paywalled. Carries Rule-of-Three / YAGNI.
- `nygard-release-it` (2018) — stub, paywalled. Nygard is also the originator of ADR practice (separate 2011 blog post, also not in corpus).
- `beck-tdd` (2018) — stub. "YAGNI" is canonically Beck/Cunningham/XP.
- `feathers-legacy-code` (2004) — stub. Doc-decay material.

Also missing entirely: Andy Matuschak (*evergreen notes*), Hunt & Thomas (*Pragmatic Programmer* "DRY for knowledge"), Gall, Conway, any ADR primary source. Orchestrator must not read the populated/absent ratio as evidence of where canon weight sits — it is evidence of what has been ingested.

## Direct facts (quoted from populated corpus)
1. [Anthropic, *Building Effective Agents*, 2024, "When (and when not) to use agents"] "we recommend finding the simplest solution possible, and only increasing complexity when needed … [Frameworks] often create extra layers of abstraction … make it tempting to add complexity when a simpler setup would suffice." (confidence: direct)
2. [Anthropic, *Building Effective Agents*, 2024, closing recommendations] "Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production." (confidence: direct)
3. [Anthropic, *Effective Context Engineering*, 2025, hybrid retrieval section] Claude Code uses CLAUDE.md up front plus glob/grep just-in-time, "effectively bypassing the issues of stale indexing … 'do the simplest thing that works' will likely remain our best advice." (confidence: direct)
4. [Anthropic, *Building a Multi-Agent Research System*, 2025, scaling rules] Embedded scaling rules prevent "overinvestment in simple queries, which was a common failure mode in our early versions." (confidence: direct)
5. [Anthropic, *Building a Multi-Agent Research System*, 2025, coordination cost] "Multi-agent systems have key differences … rapid growth in coordination complexity. Early agents made errors like spawning 50 subagents for simple queries." (confidence: direct)
6. [Google SRE book, Beyer et al., 2016, Ch.14 Managing Incidents] "The incident commander's most important responsibility is to keep a living incident document … Using a template makes generating this documentation easier." (confidence: direct)
7. [Google SRE book, 2016, Ch.5 Eliminating Toil] Systems engineering is "configuring production systems, modifying configurations, or documenting systems in a way that produces lasting improvements from a one-time effort." (confidence: direct)

## Inferred claims (librarian's synthesis, not source-asserted)
1. [canon-librarian] Four orphans is "the textbook situation" where a lifecycle/archive primitive *is* the extra abstraction layer Anthropic warns against. (confidence: inferred)
2. [canon-librarian] The Anthropic glob/grep passage is a "direct analog" for "if we invent an archive primitive, who maintains its accuracy?" — i.e., maintained indexes go stale. (confidence: inferred)
3. [canon-librarian] By analogy, "four orphan documents" maps to a small-N query where inventing a lifecycle primitive is the over-allocation failure mode. (confidence: inferred)
4. [canon-librarian] The same Anthropic glob/grep passage cuts both ways: glob/grep are themselves stable named primitives, so "no new primitive" can degrade into reinventing the wheel each time; the honest synthesis may be a *lightweight convention* rather than a *workflow*. (confidence: inferred)
5. [canon-librarian] The SRE "lasting improvement from one-time effort" frame, if taken seriously, *favors* codifying now; the case against a primitive must positively argue that recurring decision cost < primitive maintenance cost — that is "a claim, not a default." (confidence: inferred)
6. [canon-librarian] A named primitive (archive/deprecate/retire) is "exactly the kind of cheap coordination scaffold" that prevents N independent decision-makers (humans or future LLM sessions) from each inventing their own treatment; cost of *not* having a primitive scales with N decision-makers, and an R&D repo with LLM agents has more of those than it looks. (confidence: inferred)
7. [canon-librarian] Nygard's argument (paraphrased, no quote): decision context is most retrievable at the moment of decision; written records deteriorate quickly; therefore even a small policy is worth writing if there is any chance it recurs. (confidence: inferred — librarian explicitly notes it is not quoted)

## Authority-framed claims (flagged)
1. "Nygard is also the originator of the ADR practice (separate 2011 blog post, *not* in corpus)" — underlying claim: Nygard originated ADRs. Quote present in output: no. Confidence: unsupported (within this return; widely attested elsewhere but the librarian did not retrieve it).
2. "'You aren't gonna need it' is canonically Beck/Cunningham/XP" — underlying claim: YAGNI attribution. Quote present: no. Confidence: unsupported within this return.
3. "The Nygard argument, summarized in prose without quotation: …" — underlying claim: ADR rationale (context decays, write it down). Quote present: no — librarian explicitly says "I am declining to fabricate a quote." Confidence: unsupported (and self-flagged as such by the librarian, which is the correct discipline).
4. "Andy Matuschak's *evergreen notes* / Hunt & Thomas's 'DRY for knowledge' … the canonical modern treatments of 'reference vs. ephemeral artifacts.'" — underlying claim: these two are the canonical modern treatments. Quote present: no. Confidence: unsupported.

## Contradictions surfaced
- **A vs B, structural:** Anthropic's "simplest solution / basic components / do the simplest thing that works" (Facts 1, 2, 3) vs. SRE's "lasting improvement from one-time effort" (Fact 7). The same evidence base contains both "don't codify early" and "codify when one-time effort yields recurring savings." The decision turns on whether four orphans counts as recurring.
- **Fact 3 read against itself:** Anthropic praises glob/grep precisely because they are *named, stable primitives* that avoid stale indexes — so the passage simultaneously argues against new maintained abstractions *and* in favor of having stable named primitives at all. Librarian flags this as the synthesis hint (lightweight convention, not workflow).
- **Fact 5 (coordination cost) cuts both ways:** "spawning 50 subagents for simple queries" warns against over-coordination, but the librarian inverts it to argue named primitives *prevent* uncoordinated reinvention by N decision-makers. Same passage, opposite implications depending on whether the primitive is treated as coordination overhead or coordination scaffold.

## Subagent's own verdict (verbatim)
"**thin.**" (corpus coverage). Plus: "What follows are passages from populated entries that bear *obliquely* on the decision — they are weaker than the absent primary sources would be." And: "If this position needs to be load-bearing, populate `nygard-release-it` per the README instructions, or fetch the 2011 ADR post via WebFetch with explicit user consent."

## Gaps the subagent missed
The librarian named its own gaps explicitly and well; the orchestrator should carry these forward:
1. What N is Rule-of-Three for *documentation* primitives? (Fowler's three was for code.)
2. Decay rates of unmaintained ADRs / process docs in small (<5-person) R&D repos. No empirical entry.
3. The specific case of "shipped phase plans" — docs whose factual content stays true but whose *function* has expired. Most interesting orphan; corpus silent.
4. Conway's Law applied to documentation conventions in solo / small-team repos.
5. Matuschak evergreen-notes; Hunt & Thomas "DRY for knowledge." Recommend `canon-refresher` consider.

Additional gap the librarian did not name:
6. The librarian did not address the *cost of removing* a wrongly-introduced primitive vs. the cost of *introducing* one late. The asymmetry of those reversal costs is load-bearing for the YAGNI-vs-ADR call and is unargued from canon.

## Staleness flag (from librarian)
Populated sources: Anthropic 2024–2025, SRE 2016. SRE doc material predates the modern docs-as-code / ADR-explosion era; weight accordingly. Fowler/Beck/Nygard stubs are 2018 — topically current but unretrievable.

## Token budget
~1050 tokens.
