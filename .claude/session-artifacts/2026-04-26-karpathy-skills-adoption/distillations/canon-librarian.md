# canon-librarian distillation

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for corpus coverage on adopting a Karpathy-skills-style behavioral-instruction plugin into a coding agent's default file (CLAUDE.md or equivalent). Librarian returned partial coverage: three Anthropic essays (2024-2025) on context engineering and agent design; nothing on controlled studies of behavioral-instruction effectiveness, instruction-stacking interactions, convention-distribution mechanisms, or the Karpathy tweet itself.

## Direct facts
1. [Anthropic Applied AI Team, "Effective Context Engineering for AI Agents," Sep 29, 2025] System prompts should sit in a "Goldilocks zone" — neither vague nor over-engineered. (confidence: direct)
2. [same essay] Recommended workflow: "minimal set of information that fully outlines your expected behavior… start with a minimal prompt, add clear instructions based on failure modes." (confidence: direct)
3. [same essay] "Context must be treated as a finite resource with diminishing marginal returns. Every new token depletes attention budget." (confidence: direct)
4. [Schluntz & Zhang, "Building Effective Agents," Anthropic, Dec 19, 2024] "Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short." (confidence: direct)
5. [Hadfield et al., "How we built our multi-agent research system," Anthropic, Jun 13, 2025] "Short, vague instructions led to misinterpretation and duplicate work; explicit steering required." (confidence: direct)
6. [same essay] "Scale effort to query complexity. Agents struggle to judge appropriate effort, so we embedded scaling rules in the prompts… These explicit guidelines help… and prevent overinvestment in simple queries, which was a common failure mode in our early versions." (confidence: direct)
7. [same essay] "Our prompting strategy focuses on instilling good heuristics rather than rigid rules… decomposing difficult questions, evaluating source quality, adjusting based on new information." (confidence: direct)
8. [same essay] "In early agent development, changes tend to have dramatic impacts… A prompt tweak might boost success rates from 30% to 80%. With effect sizes this large, you can spot changes with just a few test cases." (confidence: direct)

## Inferred claims
1. [canon-librarian] Karpathy aphorisms sit at the "vague" end of the Goldilocks zone described in the Sep 2025 essay. (confidence: inferred)
2. [canon-librarian] Adopting the plugin wholesale "inverts" the failure-mode-driven-addition workflow recommended by the Sep 2025 essay. (confidence: inferred)
3. [canon-librarian] The diminishing-returns / attention-budget passage is the closest the corpus comes to supporting a "dilution" claim against added instructions. (confidence: inferred)
4. [canon-librarian] The multi-agent essay's effort-scaling example is a direct counterexample to the placebo theory of behavioral instructions: explicit heuristics moved behavior even though Claude "already knew" to scale effort. (confidence: inferred)
5. [canon-librarian] The multi-agent essay endorses the *pattern* of which Karpathy-skills is an instance (heuristic-based prompting). (confidence: inferred)

## Authority-framed claims
None. Librarian cited essays with author + date and produced verbatim quotes for each load-bearing claim. No persona-cosplay or unsupported "X would say" framings detected.

## Contradictions surfaced
- **Minimalism vs. explicit-steering:**
  - A: Sep 2025 Context Engineering essay + Dec 2024 Building Effective Agents essay → start minimal, add only on observed failure modes. Implies the prior ("drop all but one line") is the corpus-endorsed default.
  - B: Jun 2025 Multi-Agent Research System essay → vague instructions caused misinterpretation and duplicate work; explicit, even quantified, heuristics measurably moved behavior in production even where defaults nominally covered the case.
- **Token-budget cost vs. measured behavioral lift:**
  - A: "Every new token depletes attention budget" (Sep 2025) — duplicate-of-default content has cost without benefit.
  - B: 30%→80% success-rate jumps from prompt tweaks (Jun 2025) — effects are large enough that the correct response is to measure, not to reason from a token-cost prior.

## Subagent's own verdict (verbatim)
"Corpus coverage: partial."

One-line synthesis (verbatim): "Corpus supports minimalism and failure-mode-driven addition (favoring the prior), but contains direct production evidence from Anthropic that explicit, specific behavioral heuristics — even ones that 'duplicate' implicit defaults — measurably moved agent behavior. The honest answer: the prior recommendation 'drop all but one line' is under-evidenced in the same way the maximalist 'import the whole plugin' position would be. The corpus-endorsed move is to A/B the plugin on ~20 representative coding tasks before deciding."

## Gaps the subagent missed
The librarian explicitly declared its own gaps; none of these need re-invocation of the librarian, but the orchestrator should flag them in synthesis or route to outside-view / WebSearch:
- No empirical study of behavioral-instruction effectiveness in CLAUDE.md-style files.
- No literature on instruction-stacking or negative interaction effects between layered instructions.
- No coverage of convention-distribution as installable artifacts (linters, .editorconfig, eslint plugins as analogues).
- No Karpathy April 2026 tweet in corpus — currency gap, candidate for WebSearch.
- Staleness flag: 2024-2025 essays predate current Claude Code defaults; "what defaults cover" is a moving target. Librarian recommends re-testing rather than reasoning from memory — the orchestrator should not treat any "duplicates default behavior" claim as settled without an empirical check.
- Not addressed by librarian: whether the multi-agent-research-system findings (which involve orchestrator + subagent prompting) generalize to single-agent coding tasks. The transferability question is open.

## Token budget
~720 tokens.
