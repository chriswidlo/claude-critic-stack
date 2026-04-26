# External shadow via OpenRouter — non-Anthropic adversarial review

| Field | Value |
|---|---|
| 📌 **title** | External shadow via OpenRouter — non-Anthropic adversarial review |
| 🎯 **tier** | 🚀 outlandish |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's question about whether non-Anthropic models could participate in the panel led to a discussion of Claude Code's lack of native multi-provider support and the available paths (OpenRouter wrapper, direct provider APIs, local Ollama). The deeper motivation: even within-Anthropic shadow comparison (Opus + Sonnet) shares training data; genuine cross-family adversarial review needs a model from a different ecosystem. |
| 💡 **essence** | A bash wrapper script invokes OpenRouter (or local Ollama) with the same critic prompt the panel uses. Output lands in `critiques/<lens>.external-shadow.md`. The comparator agent reads Opus + Sonnet shadow + external shadow and assesses three-way agreement. Disagreement involving the external model is a stronger signal than within-Anthropic disagreement because the failure modes are less correlated. |
| 🚀 **upgrade** | Genuinely cross-family adversarial review. The panel's value as triangulation survives a class of failure that no Anthropic-only setup can address: shared training data producing shared blind spots. The cost surface is real (per-token billing on OpenRouter, slower responses) but bounded by env-var gating — the external shadow runs only when the stakes warrant it. |
| 🏷️ **tags** | shadow-comparator, external-models, openrouter, adversarial-review, model-diversity |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The integration shape](#the-integration-shape)
- [Why this is outlandish, not no-brainer](#why-this-is-outlandish-not-no-brainer)
- [Variants by external provider](#variants-by-external-provider)
- [Open questions](#open-questions)

## The integration shape

A small bash script `bin/external-critic.sh` takes a prompt + a candidate path and POSTs to OpenRouter (or a local Ollama endpoint). The script handles auth (API key in env), retries, and JSON parsing. It returns the model's verdict and reasoning to stdout.

The critic agents are extended with an optional shadow path: when env var `EXTERNAL_SHADOW=1`, after the Opus run completes, the orchestrator (or the comparator) invokes `external-critic.sh` with the same prompt and candidate. Output lands in `critiques/<lens>.external-shadow.md`.

The `critic-comparator` agent reads up to three outputs per lens (Opus, Sonnet shadow, external shadow) and produces `critiques/<lens>.comparison.md` with: agreement matrix, divergence summary, where external diverges most.

## Why this is outlandish, not no-brainer

The mechanics are small (a shell wrapper, an env var, a comparator extension). The reasons it is outlandish:

- **Operationally non-trivial.** API key management, billing surface, rate limit handling, error semantics across providers, response-time variance — these add real surface area.
- **The value is contingent on an unproven claim.** Cross-family disagreement *might* surface failure modes that within-Anthropic agreement masks; or it might just produce noise from models with weaker reasoning. We don't know until we run it on real cases.
- **Maintenance.** Each provider's API drifts; OpenRouter is a convenient abstraction but not free.
- **Trust calibration.** When external and Opus disagree, which is right? Without operator skill in calibrating model strengths, disagreement may resolve to "ignore the weaker model" — which is the same as not running it.

These are not blockers; they are the work that makes this outlandish rather than no-brainer.

## Variants by external provider

| Provider | Pro | Con |
|---|---|---|
| OpenRouter (proxy to many) | One API, choice of GPT-4o / Gemini / Llama / etc. | Adds an intermediary, marginal cost markup |
| Direct OpenAI / Google / etc. | Lower cost; direct error semantics | One wrapper per provider |
| Local Ollama | Free, no rate limits, private | Slower, weaker models, host hardware required |
| GitHub Models | Free tier with rate limits | Limited model selection, terms-of-service constraints |

OpenRouter is the natural starting point: lowest setup cost, broadest model selection. Local Ollama is the natural follow-up if cost or privacy becomes a concern.

## Open questions

- Which model should the external shadow default to? GPT-4o is closest in capability; Gemini 2.5 is most architecturally different from Claude; Llama is the most genuinely open.
- Should the comparator weight external disagreement higher (it's the most independent signal) or treat all three opinions equally?
- Is there a small benchmark of "known disagreements between model families" that could calibrate the comparator's interpretation of disagreement strength?
- Should the external shadow be opt-in per-session (env var at invocation) or opt-in per-lens (some lenses always run external, others never)?
