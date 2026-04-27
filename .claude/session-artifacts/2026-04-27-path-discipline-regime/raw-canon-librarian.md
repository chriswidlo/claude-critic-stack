# Canon Librarian — raw retrieval

Question: solo-maintainer repo has a path-style rule with one factually-wrong stated reason; compliance is 50/50; weighing (A) keep rule + fix reason + patch slash-command enforcement, (B) flip to natural-grain style, (C) hybrid leading-slash for GitHub.

## Corpus coverage

**Partial.** Direct hits in the two Anthropic essays (`anthropic-building-effective-agents`, `anthropic-effective-context-engineering`) and in the Google SRE book (`google-sre-book`). The most canonically relevant works for this question — Fowler *Refactoring*, Beck *TDD*, Feathers *Working Effectively with Legacy Code*, Hunt & Thomas *The Pragmatic Programmer* (the broken-windows source), and any explicit style-guide / convention-decay literature — are either **stubs with no `source.txt`** or **absent from the corpus entirely**. I will not fabricate quotes from the stubs. See "Gaps" at the bottom for what to add.

## Supporting passages (for Option A — keep rule, fix the stated reason)

### 1. Anthropic, *Building Effective Agents* (Dec 2024), Appendix 2 — Prompt engineering your tools
File: `canon/corpus/anthropic-building-effective-agents/source.txt`, lines 247–249

> "While building our agent for SWE-bench, we actually spent more time optimizing our tools than the overall prompt. For example, we found that the model would make mistakes with tools using relative filepaths after the agent had moved out of the root directory. To fix this, we changed the tool to always require absolute filepaths — and we found that the model used this method flawlessly."

Relevance: This is the closest direct precedent in the corpus. Anthropic chose a path *style* (absolute, in their case) **because it was mechanically reliable for an LLM agent**, not because it matched what the model produced naturally. It supports Option A: pick the rule for downstream-correctness reasons, then make the tool/interface enforce it. It also reframes the question — "what do authors produce naturally" (Option B's premise) is the wrong selection criterion when the consumer is an automated tool.

### 2. Anthropic, *Building Effective Agents* (Dec 2024), Appendix 2
File: `canon/corpus/anthropic-building-effective-agents/source.txt`, lines 241–247

> "Put yourself in the model's shoes. Is it obvious how to use this tool, based on the description and parameters, or would you need to think carefully about it? … Poka-yoke your tools. Change the arguments so that it is harder to make mistakes."

Relevance: "Poka-yoke" (mistake-proofing) is the explicit recommendation. A prose rule with a wrong stated reason is the opposite of poka-yoke — it depends on a human reading, believing, and complying. Option A's "patch the slash-command enforcement surface" is the poka-yoke move; the rule-text fix is secondary.

### 3. Google SRE Book (2016), Ch. 7 "The Evolution of Automation at Google", §Consistency
File: `canon/corpus/google-sre-book/source.txt`, lines 2788–2790

> "any action performed by a human or humans hundreds of times won't be performed the same way each time: even with the best will in the world, very few of us will ever be as consistent as a machine. This inevitable lack of consistency leads to mistakes, oversights, issues with data quality… In this domain — the execution of well-scoped, known procedures — the value of consistency is in many ways the primary value of automation."

Relevance: A 50/50 compliance rate is exactly the failure mode this section describes. The SRE conclusion is not "rewrite the procedure to match what humans do anyway" but "automate the procedure so the question of compliance dissolves." Supports Option A's enforcement-surface clause.

### 4. Google SRE Book (2016), Ch. 6 "Monitoring Distributed Systems"
File: `canon/corpus/google-sre-book/source.txt`, line 999

> "This trio of practices effectively minimizes the aggregate number of users and operations exposed to bad changes. By removing humans from the loop, these practices avoid the normal problems of fatigue, familiarity/contempt, and inattention to highly repetitive tasks. As a result, both release velocity and safety increase."

Relevance: "Familiarity / contempt / inattention" describes solo-maintainer drift on a self-imposed prose rule precisely. Argues that the durable fix is mechanical, not exhortative.

## Contradicting / complicating passages (against Option A's lean)

### 5. Anthropic, *Building Effective Agents* (Dec 2024), Appendix 2
File: `canon/corpus/anthropic-building-effective-agents/source.txt`, lines 231–237

> "Keep the format close to what the model has seen naturally occurring in text on the internet. … Make sure there's no formatting 'overhead' such as having to keep an accurate count of thousands of lines of code, or string-escaping any code it writes."

Why this complicates the framing: This is the canon's explicit "go with the grain" principle, and it cuts toward **Option B**. If the natural style — the one authors (and the model) produce by default — matches what tools on the internet have seen, switching to it removes a tax that is paid on every write. Option A pays that tax forever in exchange for a property whose justification is admitted to be wrong. The absolute-paths anecdote in passage #1 is a special case where naturalness conflicts with mechanical correctness; it is **not** a general license to pick the unnatural form.

### 6. Anthropic, *Effective Context Engineering* (Sep 2025), §"The anatomy of effective context"
File: `canon/corpus/anthropic-effective-context-engineering/source.txt`, line 51

> "At one extreme, we see engineers hardcoding complex, brittle logic in their prompts to elicit exact agentic behavior. This approach creates fragility and increases maintenance complexity over time."

Why this complicates the framing: A path-style rule that the maintainer themselves only follows half the time, defended with a wrong reason, is the smell this passage describes — brittle prose logic where a simpler default would do. The rule's existence is a maintenance liability independent of which style it picks. This is a vote against Option A *as currently stated* and toward whichever option leaves the smallest prose surface (B if the natural style is fine; or A only if the slash-command enforcement makes the prose rule obsolete).

### 7. Google SRE Book (2016), Ch. 8 "Release Engineering" / Configuration discussion
File: `canon/corpus/google-sre-book/source.txt`, line 3489

> "Some might protest, 'What if we need that code later?' 'Why don't we just comment the code out so we can easily add it again later?' or 'Why don't we gate the code with a flag instead of deleting it?' These are all terrible suggestions. … hundreds of lines of commented code create distractions and confusion (especially as the source files continue to evolve), and code that is never executed, gated by a flag that is always disabled, is a metaphorical time bomb…"

Why this complicates the framing: The general SRE prior is that *unenforced* artifacts (commented code, dormant flags, prose rules with no gate) are time bombs. A rule with a wrong stated reason that compliance has drifted on is exactly such an artifact. Option A's "fix the reason" half **does not by itself** address this; only the enforcement-surface half does. If the slash-command patch isn't actually feasible or maintainable, then Option A collapses into a documentation-only fix, and this passage says that's worse than no rule at all.

## Third-concern passages (a worry the operator may have missed)

### 8. Anthropic, *Effective Context Engineering* (Sep 2025), §"The anatomy of effective context"
File: `canon/corpus/anthropic-effective-context-engineering/source.txt`, line 57

> "you should be striving for the minimal set of information that fully outlines your expected behavior. (Note that minimal does not necessarily mean short; you still need to give the agent sufficient information up front to ensure it adheres to the desired behavior.) It's best to start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples to improve performance based on failure modes found during initial testing."

Third concern: **The operator hasn't named the consumer.** "Path-style rule" reads like it's for humans, but if the rule is in CLAUDE.md / agent instructions, the consumer is an LLM agent, and the right test is empirical: does the agent adhere when the rule is stated, vs. silently produce option B's natural style? None of the three options (A/B/C) are framed in terms of "test which one the agent actually follows." The corpus says: **measure first, then pick**. Without that, A vs. B is theology.

### 9. Anthropic, *Effective Context Engineering* (Sep 2025), §"The anatomy of effective context"
File: `canon/corpus/anthropic-effective-context-engineering/source.txt`, line 79

> "the metadata of these references provides a mechanism to efficiently refine behavior, whether explicitly provided or intuitive. To an agent operating in a file system, the presence of a file named test_utils.py in a tests folder implies a different purpose than a file with the same name located in src/core_logic/ Folder hierarchies, naming conventions, and timestamps all provide important signals…"

Third concern: Path **style** (leading slash, repo-root-relative, absolute) is a different axis from path **content** (which directory, what name). The contradicting-grain argument from passage #5 applies to *style*; the SWE-bench absolute-path fix in passage #1 applies to *resolution-correctness*. Option C (hybrid GitHub-leading-slash) is the only option that distinguishes the two — it picks one form for the URL-rendering consumer and may pick another for prose. The corpus implicitly endorses splitting by consumer; the operator should ask whether A vs. B is one decision or two.

### 10. Google SRE Book (2016), Ch. 7
File: `canon/corpus/google-sre-book/source.txt`, lines 2792–2796

> "Automation doesn't just provide consistency. … A platform also centralizes mistakes. In other words, a bug fixed in the code will be fixed there once and forever, unlike a sufficiently large set of humans performing the same procedure…"

Third concern: For a *solo* maintainer this passage's force is reduced (n=1, not "a sufficiently large set of humans"), but the centralization-of-mistakes point still bites: with one author, a wrong stated reason in prose **becomes the ground truth in the author's own head over time**. The 50/50 compliance number is a leading indicator that the author no longer believes their own rule. Fixing the prose reason without auditing what *other* prose rules in the same surface have similarly drifted is a local fix to a systemic problem.

## Gaps — what the corpus does not cover

The following directly-relevant works are **stubs** (`body_completeness: stub`, no `source.txt`):
- `canon/corpus/fowler-refactoring/citation.yaml` — Fowler 2018, would carry the canonical "code as communication" + comments-as-deodorant arguments.
- `canon/corpus/beck-tdd/citation.yaml` — Beck 2002, red/green/refactor as the model for "rules with mechanical gates."
- `canon/corpus/feathers-legacy-code/citation.yaml` — Feathers 2004, "characterization tests" as the move when documented behavior and actual behavior diverge (which is exactly the 50/50-compliance situation).

Not in the corpus at all (recommend adding):
- **Hunt & Thomas, *The Pragmatic Programmer*** — the broken-windows analogy for code originates here; directly relevant to "rule + drift = continued drift."
- **Google Engineering Practices / Google Style Guides** (open-source) — explicit treatment of style-guide rationale, including "rules whose justification has lapsed should be removed, not retained for tradition."
- **Hyrum's Law** as a primary source / blog post — "with a sufficient number of users… all observable behaviors will be depended on." Bears on Option C (the GitHub-leading-slash form is *already* observable in rendered links; flipping the rule changes that behavior).
- **Raymond, *The Cathedral and the Bazaar*** or any solo/small-team OSS maintenance essay — the corpus has nothing on single-maintainer governance specifically.
- **Any post-2020 LLM-era treatment of CLAUDE.md / AGENTS.md style files as load-bearing** — the corpus has the two Anthropic essays but no treatment of agent-instruction *drift* over time, which is the deepest version of the operator's question.

Sub-questions the corpus does not answer:
1. When the consumer of a rule is mixed (humans + an LLM agent + GitHub's URL renderer), how should style decisions be partitioned by consumer?
2. What is the empirically observed drift rate on prose rules in solo-maintainer repos, with vs. without mechanical gates? (The SRE consistency argument is asserted, not measured, in the retrieved passages.)
3. Is "the maintainer wrote a wrong reason and then half-followed the rule" diagnostic of a *deeper* problem (the rule never had a real reason) or a *local* problem (the reason got stale)? The corpus is silent.

## Staleness note

The Anthropic essays (Dec 2024, Sep 2025) are current. The Google SRE book (2016) is ten years old; on the specific question of "automated enforcement beats prose rules," the consensus has not shifted — if anything, it has hardened with the rise of pre-commit, conventional-commits, and LLM-readable agent files. No staleness flag needed for the supporting passages. The contradicting "go with the grain" passage (Anthropic Dec 2024) is current and reflects post-LLM thinking specifically.
