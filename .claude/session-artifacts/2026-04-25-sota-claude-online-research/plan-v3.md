# Plan v3 — leaner, frequency-conditional

## Position (one paragraph)

"SOTA Claude online research" is not an architecture — it is a **triage decision keyed on one variable the user knows about themselves: their weekly load-bearing research volume.** The right architecture is whichever one survives at *that* volume. There is no universal SOTA, and almost every prior recommendation in this stack failed because it tried to design an architecture before measuring the demand.

Three regimes, indexed by load-bearing-research-queries-per-week. "Load-bearing" = the output will drive an action the user cannot reverse within 24 hours.

## Regime 1 — <1/week (the default; almost certainly the user today)

**Use hosted Deep Research (Anthropic Research is the default for the Claude stack). Nothing else.**

- Time-to-first-result: ≈30 s.
- Setup cost: zero.
- Build cost: zero.
- Maintenance: zero.
- Re-validation routine: none.
- Disclaimer attached mentally: *"5–15% of citations may be fabricated; if this output drives an action I cannot reverse within 24h, I will re-read the cited sources before acting."*

This is the recommendation **if the user is unsure of their volume.** Outside-view's data places hosted Deep Research at 40–55% joint success — the highest of any class measured — and every additional engineering element trades real overhead for unmeasured upside.

## Regime 2 — 2–5 load-bearing queries/week

**Same default + a written manual-audit checklist. No code.**

The "agent" here is a Markdown file the user reads when they have a load-bearing query. Four steps:

1. **Re-fetch each cited URL.** Confirm it resolves and returns roughly the expected page.
2. **Verify quoted passages.** Open the page, ctrl-F for the exact quoted text. If the quote is paraphrased, mark the claim "paraphrase" and decide whether the paraphrase changes the meaning.
3. **Check date + source class.** Is the source primary, secondary, or aggregator? Is the date current relative to the claim's domain (medical research <2y; legal post-most-recent-ruling; tech post-current-major-version)?
4. **Note one omission risk.** What relevant body of work might the hosted engine have missed? (Adversarial prompt: *"What's the strongest published rebuttal to this report's main claim?"*)

This regime ships zero new code. The audit takes ~10 minutes per load-bearing query. At 2–5/week, that is 20–50 minutes weekly — bounded, predictable, and the user retains the judgment surface a verifier-LLM cannot replicate (omission detection, paraphrase-fidelity, domain-currency).

## Regime 3 — 5+ load-bearing queries/week

**Build exactly one thing: a verifier that runs over a hosted engine's output. Not a producer pipeline.**

This is the *only* build that survives the prior loops' critiques because the producer is the hosted engine — which already emits structured citations — and the verifier consumes its output as a read-only artifact. No `claims.jsonl` schema-coupling (the hosted engine owns its citation format and has no incentive to break it). No multi-agent fan-out. No hooks. No MCPs. No Routine. No new slash commands beyond one.

Concretely:

- One file: a `verify-research.md` slash command in the user's global Claude Code commands directory. A slash command that takes the path to a hosted-Deep-Research output (saved as Markdown) and:
  1. Parses cited URLs and the surrounding quoted text.
  2. Spawns one `claude -p --model claude-haiku-4-5` invocation per claim (in parallel, capped at 5-wide).
  3. Each verifier call: WebFetches the URL, **snapshots the page text to a local research-snapshots directory under user home, organized as `<date>/<hash>.txt`** (this addresses the live-URL non-reproducibility critique from the prior architecture lens), and returns one of `{verified, partial, unverifiable, currently-contradicts, fetch-failed}` with one quoted excerpt as evidence.
  4. Result composer assembles a one-page report: header (N claims, V verified, P partial, U unverifiable, X contradicts, F fetch-failed; cost; wall-clock; verifier model) + per-claim entries showing evidence excerpt only for non-verified claims.
- Snapshots are kept indefinitely so re-runs against historical research outputs are deterministic against the snapshot, not the live URL.
- Verifier model is **explicitly different family from the producer**, but the recommendation acknowledges (per prior architecture critic) that this is a quality property, not a correctness property. The on-disk-artifact pattern is what makes verification *exist*; cross-family makes it *better*.

What is **not** built in regime 3:

- No producer subagents. The hosted engine is the producer.
- No `claims.jsonl` schema we own. We parse the hosted engine's Markdown.
- No three MCP servers. No browser-render. No academic search. The hosted engine already searches.
- No quarterly re-validation Routine. Snapshots provide reproducibility; if the verifier-model deprecates, the snapshot lets us re-verify with whatever's current.
- No hooks. No plugins. No skills.
- No critic-panel pass on every research output. The critic-panel is a separate `/research-critique` invocation the user runs when they actually want it — once per important question, not per query.

## Decision protocol the user runs once

A single question, asked once, which the user can answer truthfully in 30 seconds:

> *"In the last 8 weeks, how many times did I make a decision I could not reverse within 24 hours that depended on online research I did with an LLM?"*

- 0–8 → Regime 1.
- 9–40 → Regime 2.
- 41+ → Regime 3.

The user can re-answer this question every quarter and step up or down. The transition cost between regimes is bounded: 1→2 is "write the checklist file" (15 min), 2→3 is "write `verify-research.md`" (1–2 hours), 3→2 is "stop running the slash command" (free), 2→1 is "stop reading the checklist" (free).

## What this plan is NOT

- Not a 5-stage chain. Stages 0, 3, 5 from the prior plan are dropped entirely. Stage 2 (experiment-runner) collapses into "run the 30-query Haiku test once before going 1→3 if you want." Stage 4 (full Mode-D pipeline) is dropped — replaced by the regime-3 verifier-only build.
- Not a multi-actor system. There is one user. Handoffs cost more than they save at N=1.
- Not vendor-lock. The verifier is hosted-engine-agnostic; the parser knows about Anthropic Research's Markdown format today, can be extended to OpenAI Deep Research's format if the user switches, but does not require multiple engines wired in parallel.
- Not aspirational. Every line is something the user could do this week if they chose the matching regime.

## What I'm honest about not solving

- **The "I want to learn how to build with MCPs and subagents" desire**, if the user has it, is a *separate question* from "how do I do good research" — and conflating them is what made prior plans bloated. The honest answer to that desire is: pick a small, low-stakes side project (a personal data MCP, a hobby aggregator), build it for the learning, do not call it your research workflow.
- **Whether the user's true volume is 0 or 50/week** — I don't know, and the recommendation is correct for any volume *given the user's honest answer to the one question*.
- **Whether snapshots-at-verifier-time fully addresses the architecture critic's reproducibility objection** — they make verification deterministic against the snapshot, but the producer fetched the live URL at an earlier time, so the snapshot may differ from what the producer saw. The honest framing: snapshots give *audit-time* reproducibility, not *producer-time* fidelity. For most claims this is enough; for breaking-news or rapidly-edited sources it is not, and the regime-3 user must know the difference.
- **Whether hosted engines will ship native per-claim verification in 6 months and obsolete regime 3.** They might. If so, regime 3 collapses back into regime 1 and the verifier-command can be deleted in 5 minutes.
