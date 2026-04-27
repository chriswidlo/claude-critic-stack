## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage on path-discipline / broken-link cleanup decisions for session item-03 (pre-folder-shape paths). Librarian returned partial coverage — primarily SRE Book (2017) plus one Anthropic 2025 passage; most relevant works (Fowler, Feathers, Beck, Nygard) are stubs.

## Direct facts

1. [SRE 2017, Ch 9 "Simplicity," "Negative Lines of Code"] "every line of code changed or added to a project creates the potential for introducing new defects and bugs... Some of the most satisfying coding I've ever done was deleting thousands of lines of code at a time when it was no longer useful." (confidence: direct)

2. [SRE 2017, Ch 9, "I Won't Give Up My Code!"] On commenting-out or flag-gating code instead of deleting: "These are all terrible suggestions. Source control systems make it easy to reverse changes, whereas hundreds of lines of commented code create distractions and confusion." (confidence: direct)

3. [SRE 2017, Ch 9, continued] "code that is never executed, gated by a flag that is always disabled, is a metaphorical time bomb waiting to explode, as painfully experienced by Knight Capital..." (confidence: direct)

4. [SRE 2017, Ch 9, "Release Simplicity"] "Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously." (confidence: direct)

5. [SRE 2017, Ch 15 "Postmortem Culture"] "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring." Postmortems "added to a team or organization repository... Transparent sharing makes it easier for others to find and learn from the postmortem." (confidence: direct)

6. [SRE 2017, Ch 15, "Collaborate and Share Knowledge"] "Our postmortem documents are Google Docs, with an in-house template... Real-time collaboration enables the rapid collection of data and ideas." "An unreviewed postmortem might as well never have existed." (confidence: direct)

7. [SRE 2017, Ch 5 "Eliminating Toil"] "If you're performing a task for the first time ever, or even the second time, this work is not toil... If the task produced a permanent improvement... it probably wasn't toil, even if some grunt work — such as digging into legacy code and configurations and straightening them out — was involved." (confidence: direct)

8. [Anthropic, Effective Context Engineering for AI Agents, 2025] "primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees." Also: "Folder hierarchies, naming conventions, and timestamps all provide important signals that help both humans and agents understand how and when to utilize information." (confidence: direct)

## Inferred claims

1. [canon-librarian] Source-control already preserves prior shape, so leaving stale references in artifacts to "preserve history" is redundant with VCS — the cleanup-vs-preservation argument generalizes from dead code to dead links. (confidence: inferred)

2. [canon-librarian] A reference graph with 11 known-broken edges constitutes "stale indexing" in the Anthropic sense — a real cost to humans and agents, not a neutral artifact. (confidence: inferred)

3. [canon-librarian] The SRE postmortem genre prescribes blameless review and continued retrievability, NOT textual immutability — so framing session artifacts as "self-declared immutable" is a local choice, not industry default. (confidence: inferred)

4. [canon-librarian] Fixing 4 broken refs once is non-toil grunt cleanup; deciding whether every future migration leaves N broken refs IS the policy question, and a one-off ticket that silently sets that precedent is a category error. (confidence: inferred)

5. [canon-librarian] Bundling items 2+3 because "they share files" is weak under SRE's release-simplicity default; bundling needs affirmative justification when embedded decisions differ. (confidence: inferred)

6. [canon-librarian] Broken refs in "immutable" files act like Knight-Capital-style dormant-but-reachable artifacts: a future reader may follow a rotted link, resolve it incorrectly (e.g., new file with same slug, different meaning), and silently corrupt a downstream decision. (confidence: inferred)

7. [canon-librarian] Link-target is part of a record's FUNCTION, not its content; one can leave original prose untouched while fixing link targets (or adding forwarding stubs) without violating record-preservation. (confidence: inferred)

## Authority-framed claims

None present. The librarian quotes named sources directly (SRE Book authors via Beyer et al. 2017; Anthropic 2025) rather than ventriloquizing. No "as Fowler would say" patterns.

## Contradictions surfaced

- **Cleanup-as-positive-value (fact 1, 2) vs. preservation-of-historical-record framing.** SRE explicitly rejects "leave it in case we need it" reasoning; user's draft assumes leaving broken refs preserves something.

- **Atomic small releases (fact 4) vs. user's bundling of items 2+3.** SRE default is opposite of bundling.

- **"Immutable historical record" framing vs. SRE postmortem practice (fact 5, 6).** The corpus's closest analogue to "immutable record" — Google postmortems — are mutable, annotatable, reviewed Google Docs. Genre is built on enrichment, not freezing.

- **"Just leave the dead references" vs. Knight-Capital warning (fact 3).** Dormant-but-reachable artifacts surprise later; broken links are not benign.

- **One-off cleanup (fact 7, toil definition) vs. policy-by-precedent.** Fixing the refs is not-toil; but doing so without articulating the rule turns a one-off into silent policy.

## Subagent's own verdict (verbatim)

"Corpus coverage: Thin → partial."

## Gaps the subagent missed

The librarian itself flagged these gaps (carry forward):
1. Broken-window theory in software/docs — uncovered; biggest gap for the cleanup question.
2. Atomic-commits literature (Linus-style "one logical change per commit") — uncovered.
3. Cross-reference / wiki-graph integrity (Andy Matuschak evergreen-notes) — uncovered.
4. Rename/migration cleanup as a discipline — Fowler stub only.
5. Policy-by-precedent / Chesterton's fence — uncovered.
6. Recency caveat: directly-quoted material is from 2017 SRE; no post-2017 sources except the one Anthropic 2025 passage.

Stubs that would have been central if ingested: fowler-refactoring, feathers-legacy-code, beck-tdd, nygard-release-it, vernon-strategic-monoliths, evans-ddd, vernon-iddd.

Additional gap the librarian did not flag: no canon material on the *consent boundary* aspect of path-discipline (privacy/leaking machine-specific paths) — only on hygiene/cleanup. The orchestrator should not expect canon to speak to the privacy-rationale half of path-discipline regime.

## Token budget
~950 tokens.
