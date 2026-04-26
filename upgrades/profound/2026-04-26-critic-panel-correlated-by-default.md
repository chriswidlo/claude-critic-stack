# The critic panel is correlated by default — shadow comparator as the fix

| Field | Value |
|---|---|
| 📌 **title** | The critic panel is correlated by default — shadow comparator as the fix |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective on the stack flagged that all three critic lenses (architecture, operations, product) run on the same Opus model. "Minority veto across three lenses" is, in practice, one model talking to itself in three voices. The architecture lens's own correlated-error objection lands on the panel before it lands on any candidate. |
| 💡 **essence** | Adversarial review with three lenses on the same model is style-diverse, not model-diverse. Real triangulation needs a different model family. The shadow-comparator pattern keeps Opus authoritative (preserves quality) while running smaller or external models in parallel as triangulation signal — disagreement is surfaced as a yellow flag, not a verdict change. The panel becomes triangulating instead of multi-voiced. |
| 🚀 **upgrade** | Within Anthropic: shadow each Opus lens with a Sonnet run; comparator agent assesses agreement; disagreement surfaces to the user. Cross-family (via OpenRouter or local Ollama): same pattern, different model entirely. Both gated by env var so they run only when stakes warrant the cost. The panel's value as adversarial review survives instead of laundering into self-confirmation. |
| 🏷️ **tags** | critique, panel, model-diversity, adversarial-review, correlated-error |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The problem](#the-problem)
- [Why shadow comparison is the right shape](#why-shadow-comparison-is-the-right-shape)
- [Concrete sketch](#concrete-sketch)
- [Open questions](#open-questions)

## The problem

The critic panel runs `critic-architecture`, `critic-operations`, `critic-product` in parallel. None of the three frontmatter files pin a model — all inherit Opus from the orchestrator. So three lenses on the same candidate become Opus reading itself three times under different prompts. Disagreements between lenses are real but bounded — none surface failure modes that *the model itself* doesn't see.

This was never a deliberate design choice; it is what happens when no one specifies otherwise. The cost is that adversarial review, the stack's value proposition, has correlated blind spots that no minority-veto can catch.

## Why shadow comparison is the right shape

The naive fix — pin different models to different lenses (Opus / Sonnet / Haiku) — has a real cost: the smaller-model lens may quietly miss what only Opus would catch, *for that specific lens*. That trades correlated error for unevenly-distributed error.

The shadow pattern preserves Opus on every lens and adds a parallel Sonnet (or external) run as *signal*, not vote. Both outputs persist (`critiques/<lens>.md` and `critiques/<lens>.shadow.md`). A `critic-comparator` agent assesses: agree, partial-agree, disagree. Disagreement surfaces as a yellow flag — *"architecture lens: Opus says rework on protocol; Sonnet shadow says approve but flags coupling concern"* — not as a verdict change.

Opus retains authority. The shadow gets a voice, not a vote. Disagreement becomes visibility, not noise.

## Concrete sketch

- Each critic agent stays on Opus by default.
- Behind env var `SHADOW_PANEL=1`, each lens fires twice in parallel: Opus + Sonnet (same prompt, same candidate).
- New agent `critic-comparator` reads both, writes `critiques/<lens>.comparison.md`.
- For non-Anthropic shadowing, separate env var `EXTERNAL_SHADOW=1` triggers a Bash wrapper that calls OpenRouter (or local Ollama) with the lens prompt; comparator handles three-way comparison.
- Off by default; opt-in for high-stakes decisions.

The cost is a doubling (or tripling) of per-lens spend when enabled. The value is genuine triangulation when stakes matter.

## Open questions

- Does shadow disagreement carry signal in practice, or does it produce noise (every lens disagrees on something, attention dilutes)?
- Should the shadow be Sonnet (similar training, smaller variance) or Haiku (smaller, possibly higher variance, more diverse signal)?
- Could the comparator itself be a smaller model — a Haiku diff-checker — to keep cost down?
- Is there a class of decisions where shadow is mandatory (security-touching changes, model migrations, harness changes) versus optional?
