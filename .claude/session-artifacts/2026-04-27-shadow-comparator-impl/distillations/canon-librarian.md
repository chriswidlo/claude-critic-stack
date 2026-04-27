# Canon librarian distillation — shadow comparator

## Supporting passages

- **Wisdom of crowds (Surowiecki, 2004)** — group judgment beats individual judgment when group members are independent, diverse, and decentralized. Same-family LLMs violate independence; the shadow pattern at least makes the violation visible by surfacing disagreement.
- **Ensemble diversity literature (Kuncheva, 2004 onward)** — diversity is a precondition for ensemble gains; methods that engineer diversity (bagging, random subspaces) yield more than methods that don't. Sonnet-as-shadow engineers some diversity (different scale, different RLHF generation) but not much.
- **Anthropic's own building-effective-agents guide** — recommends critic-style review, but does not specifically warn against same-model correlation as a failure mode of the critic pattern. The omission is itself evidence the pattern is under-examined in the literature this corpus draws from.

## Contradicting passage (mandatory by canon-librarian protocol)

- **Hendrycks et al. on adversarial robustness (~2020)** — within-family ensembles fail under shared distributional shift. If the failure mode the panel is meant to catch is itself out-of-distribution for the Opus training corpus, both Opus and Sonnet will miss it together. The shadow gives no protection against shared blind spots from training data overlap.

This contradicts the proposal's value: shadow comparison cannot triangulate failures the family as a whole inherits. The proposal's value is bounded to the subset of errors that happen to vary by model scale and RLHF generation, not to errors that are baked into the family's prior.

## What the librarian declines to say

The canon does not have a passage specifically on LLM-as-judge correlation rates between Opus and Sonnet on reasoning tasks. That is a gap. WebSearch could fill it post-corpus; the librarian flags it for the orchestrator's attention.
