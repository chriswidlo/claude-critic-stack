## Source agent
outside-view

## Invocation summary
Orchestrator asked for a reference-class forecast on adopting a community-published Karpathy "skill" (small behavioral config bundle for Claude). Subagent chose the reference class of small community-published behavioral config files for tools users already configure (Cursor rules, shared ESLint configs, VSCode dotfile snippets) and returned a below-base-rate verdict for full adoption.

## Direct facts
1. [arxiv 2512.18925v3, Dec 2025] Cited as an empirical study on Cursor rules — used as nearest-analogue evidence for the chosen reference class. (confidence: direct — source named, but specific finding from the paper not quoted in the return)
2. [outside-view, self-flagged] The "15-25% still in active use at 6 months" base rate is explicitly labeled as an estimate, not measured. (confidence: direct — the flag itself is on the page)
3. [Kahneman & Lovallo 1993] Cited as the canon methodology source for outside-view reasoning. (confidence: direct — cited, but no quote provided)
4. [outside-view, canon coverage] Only Kahneman & Lovallo 1993 is in canon for this question; no corpus material exists on community prompt-bundle adoption. Declared as a gap. (confidence: direct)

## Inferred claims
1. [outside-view] Base rate of "still in active use, with user able to point to specific behavior changed, 6 months later" is 15-25% for the chosen reference class. (confidence: inferred — self-flagged as estimate)
2. [outside-view] The Karpathy skill sits slightly below base rate for full adoption, slightly above for partial cherry-pick, well above for ignore. (confidence: inferred)
3. [outside-view] Typical failure mode: silent overlap-induced drift — bundled CLAUDE.md and existing files load together; Claude follows whichever is more recent in context; user attributes resulting behavior to own harness and debugs the wrong thing. (confidence: inferred)
4. [outside-view] Secondary failure: maintenance asymmetry — community publisher updates the skill, user's overrides silently invalidated. (confidence: inferred)
5. [outside-view] Contradicting reference class — single high-quality canonical document from authoritative source (tsconfig/strict, React team ESLint config, Anthropic's prompting guide) — has base rate 50-70%. (confidence: inferred — also a flagged estimate)
6. [outside-view] If the marketplace plugin is from Anthropic or a recognized authority, the verdict flips. (confidence: inferred — conditional)
7. [outside-view] Regret-minimization move: read the 50 lines, diff against existing CLAUDE.md, port the 1-3 novel lines, do not install as a skill. Converts opaque overlap into explicit merge under user's version control. (confidence: inferred — recommendation)

## Authority-framed claims
None. Subagent named sources (Kahneman & Lovallo, Jason Collins blog, PMI, LogRocket, vscode-discussions #617, gocodeo) but did not ventriloquize any author. All claims are framed as the subagent's own reference-class reasoning citing sources, not as "X argues Y." Confidence: n/a.

## Contradictions surfaced
- Primary reference class (community behavioral configs, 15-25% base rate) vs contradicting reference class (canonical document from authoritative source, 50-70% base rate). The verdict depends entirely on which class the Karpathy skill belongs to. Subagent did not resolve which class applies — flagged as conditional on whether the publisher is Anthropic / recognized authority.

## Subagent's own verdict (verbatim)
"below base rate for full adoption"

Regret-minimization move (verbatim): "read the 50 lines, diff against existing CLAUDE.md, port the 1-3 lines that say something the user's setup does not, do not install the skill as a skill."

## Gaps the subagent missed
- Did not establish whether Karpathy himself counts as "recognized authority" for the contradicting reference class. Karpathy is a recognized authority in ML/AI broadly but not necessarily in Claude harness configuration specifically — this distinction matters and was skipped.
- No quoted finding from arxiv 2512.18925v3; the Cursor-rules paper is cited but its actual numbers are not surfaced. Re-invocation could ask for the specific empirical adoption/retention rate the paper reports.
- Did not address the cost side of the regret-minimization move (user time to read+diff+port) versus the cost of just installing and tolerating drift.
- No reference class for "config installed by a user who already runs an adversarial-review meta-stack" — the user's specific sophistication may shift the base rate in either direction and was not considered.
- Canon gap declared but no recommendation to route to canon-refresher or WebSearch for currency.

## Token budget
~620 tokens
