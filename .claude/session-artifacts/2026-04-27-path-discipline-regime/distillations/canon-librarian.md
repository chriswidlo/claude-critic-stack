## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon retrieval on a solo-maintainer repo's path-style rule (one wrong stated reason, 50/50 compliance) weighing options A (keep + fix reason + enforce), B (flip to natural-grain), C (hybrid leading-slash for GitHub). Librarian returned `corpus coverage: partial`, with hits in two Anthropic essays and the Google SRE book; flagged the most canonically relevant works (Fowler, Beck, Feathers, Hunt & Thomas) as stubs or absent.

## Direct facts

### Supporting Option A (keep rule + enforce)

1. [anthropic-building-effective-agents, lines 247–249] Anthropic's SWE-bench agent made mistakes with relative filepaths after moving out of root; they changed the tool to require absolute filepaths and the model "used this method flawlessly." (confidence: direct)

2. [anthropic-building-effective-agents, lines 241–247] Explicit recommendation: "Poka-yoke your tools. Change the arguments so that it is harder to make mistakes." (confidence: direct)

3. [google-sre-book, lines 2788–2790] "any action performed by a human or humans hundreds of times won't be performed the same way each time… the value of consistency is in many ways the primary value of automation." (confidence: direct)

4. [google-sre-book, line 999] Removing humans from the loop "avoid[s] the normal problems of fatigue, familiarity/contempt, and inattention to highly repetitive tasks." (confidence: direct)

### Contradicting / complicating

5. [anthropic-building-effective-agents, lines 231–237] "Keep the format close to what the model has seen naturally occurring in text on the internet… no formatting 'overhead'." (confidence: direct)

6. [anthropic-effective-context-engineering, line 51] "engineers hardcoding complex, brittle logic in their prompts… creates fragility and increases maintenance complexity over time." (confidence: direct)

7. [google-sre-book, line 3489] On commented-out code / disabled-flag code: "These are all terrible suggestions… code that is never executed, gated by a flag that is always disabled, is a metaphorical time bomb." (confidence: direct)

### Third-concern

8. [anthropic-effective-context-engineering, line 57] "start by testing a minimal prompt with the best model available… then add clear instructions and examples to improve performance based on failure modes found during initial testing." (confidence: direct)

9. [anthropic-effective-context-engineering, line 79] "Folder hierarchies, naming conventions, and timestamps all provide important signals" — distinguishes path content from path style. (confidence: direct)

10. [google-sre-book, lines 2792–2796] "A platform also centralizes mistakes… a bug fixed in the code will be fixed there once and forever, unlike a sufficiently large set of humans performing the same procedure." (confidence: direct)

## Inferred claims

1. [canon-librarian] The SWE-bench absolute-path anecdote is a *special case* where mechanical correctness conflicts with naturalness; not a general license to pick the unnatural form. (confidence: inferred)

2. [canon-librarian] A prose rule with a wrong stated reason is the opposite of poka-yoke — it depends on a human reading, believing, and complying. (confidence: inferred)

3. [canon-librarian] 50/50 compliance is a leading indicator the author no longer believes their own rule; fixing the prose reason alone is a local fix to a systemic problem. (confidence: inferred)

4. [canon-librarian] Option A's "fix the reason" half does not address the unenforced-artifact-as-time-bomb concern; only the enforcement-surface half does. If slash-command patch isn't feasible, A collapses to documentation-only and the SRE passage says that's worse than no rule. (confidence: inferred)

5. [canon-librarian] Option C is the only option that distinguishes path *style* (leading slash, root-relative, absolute) from path *content* (directory, name); the corpus implicitly endorses splitting by consumer. (confidence: inferred)

6. [canon-librarian] The operator hasn't named the consumer; if the rule is in CLAUDE.md/agent instructions, the right test is empirical (does the agent adhere?) — without measurement, A vs. B is theology. (confidence: inferred)

7. [canon-librarian] For a solo maintainer the centralization-of-mistakes point is reduced (n=1) but still bites: a wrong stated reason becomes ground truth in the author's own head over time. (confidence: inferred)

## Authority-framed claims

None. Librarian cited works by file/line and quoted directly; no "as X argues" ventriloquism in the return.

## Contradictions surfaced

- **Poka-yoke / absolute paths (passage 1, 2)** vs. **Go with the grain (passage 5)**: both from the same Anthropic essay (Dec 2024). Passage 1 picks the unnatural form for mechanical reliability; passage 5 says match what the model produces naturally. Librarian flags this as a real tension, not a contradiction to collapse.

- **Automate the procedure (passages 3, 4)** vs. **Don't hardcode brittle logic (passage 6)**: SRE says enforcement dissolves compliance questions; Anthropic Sep-2025 says complex prose logic is fragility. Both can be true if "enforcement" means a mechanical gate (slash-command patch) rather than more prose. The two cut against each other if Option A's enforcement half is just more prose.

- **Rule + enforcement is durable (passages 3, 4)** vs. **Unenforced artifact is a time bomb (passage 7)**: not a contradiction within the corpus, but together they imply Option A is only viable if the enforcement clause is actually mechanical — the prose-only version of A is worse than B.

## Subagent's own verdict (verbatim)

"**Partial.**" (corpus coverage)

"No staleness flag needed for the supporting passages. The contradicting 'go with the grain' passage (Anthropic Dec 2024) is current and reflects post-LLM thinking specifically."

## Gaps the subagent missed

The librarian itself enumerated gaps thoroughly (Fowler/Beck/Feathers stubs; Hunt & Thomas, Google Style Guides, Hyrum's Law, Raymond, post-2020 CLAUDE.md drift literature absent). Sub-questions the librarian flagged as unanswered by corpus:

1. When consumers are mixed (humans + LLM + GitHub renderer), how should style decisions be partitioned by consumer?
2. Empirical drift rate on prose rules in solo-maintainer repos with vs. without mechanical gates? (SRE argument is asserted, not measured.)
3. Is "wrong reason + half-compliance" diagnostic of a *deeper* problem (rule never had a real reason) or a *local* problem (reason got stale)?

Additional gap the librarian did not flag:
- No retrieval addressed the **cost of the flip itself** (rewrite churn, link-rot in existing artifacts) — relevant to B and C but absent from canon hits.

## Token budget
~850 tokens.
