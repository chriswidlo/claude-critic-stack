# The Five Pressures

A checklist to run against any non-trivial design recommendation before shipping it to a user. Each pressure compensates for a known LLM failure mode.

## 1. Reframe-before-answer
**Failure mode compensated:** accepting the user's framing as neutral when it has already narrowed the solution space.

Before answering, restate the question in at least one framing the user did not use. Example: user asks "how do we scale the write path?" — reframe as "do we need to scale the write path, or is the real problem read amplification on the same table?" If the reframe changes the answer, surface that.

## 2. Enumerate-before-select
**Failure mode compensated:** confident recommendation of the first workable option without demonstrating it beat the others.

List at least three candidate solutions before recommending one. For each, give one sentence on why it might be right and one sentence on why it might be wrong. Then select. The *enumeration* is more valuable than the selection.

## 3. Outside-view-first
**Failure mode compensated:** inside-view detail-reasoning that misses base rates.

Before reasoning about the specifics of this case, ask: what is the reference class, and what typically happens in that class? If the inside view and outside view disagree, the outside view is more often right.

## 4. Name-your-uncertainty
**Failure mode compensated:** producing equally-confident prose regardless of actual confidence.

Explicitly list at least three things you do not know that would change the recommendation if known. This moves uncertainty from tone (hedging adverbs) to content (named gaps). Named gaps are actionable; hedged prose is not.

## 5. Consequence-imagine
**Failure mode compensated:** recommending patterns without modeling their failure modes.

For the recommended solution, answer:
- What does it look like when this *succeeds*? (Specifically — what metric, observed when?)
- What does it look like when this *fails*? (Specifically — which system breaks first, detected by whom, how expensive?)
- What is the *cheapest* experiment that would distinguish the two outcomes early?

If you cannot answer all three, the recommendation is not ready.

## Usage

Run all five. Do not shortcut any of them because the question "seems simple" — the questions that seem simple are exactly the ones where these pressures catch the most errors. The overhead is real but small. The alternative is confident mediocrity.
