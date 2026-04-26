# Architecture lens — plan v3 review

## Weakest structural link

**The regime-3 verifier has no defined input grammar.** Plan says "parses cited URLs and quoted text" from Anthropic Research's Markdown. No schema, no version pin, no parse-failure semantics, no contract. Markdown is a *presentation format* — no SemVer, no deprecation policy, no changelog. The verifier will fail open (parse zero claims, report "0/0 verified") far more often than it fails closed.

v2 critique: `claims.jsonl` had no owner. v3 response: let the vendor own it. That converts a self-owned schema into a **vendor-owned schema with no contract and no notification channel** — strictly worse on stability-under-change and detectability-of-breakage.

## Invariants at risk (not named in the plan)

1. **Parser totality / fail-closed on parse drift.** Required: extracted-claim-count cross-checked against footnote-marker heuristic; abort on mismatch.
2. **Snapshot-set monotonicity under verifier-model change.** Snapshots must be content-addressed by (URL, fetch-time) and write-once.
3. **Producer-time vs verifier-time divergence is bounded.** Plan acknowledges but does not bound. Need: "fetch within T minutes of producer-fetch-time, else mark `stale-snapshot`."
4. **Synthesis-claim closure.** "X and Y therefore Z" produces three citations + Z without a URL → Z silently dropped. Same false-comfort failure as v2.
5. **Concurrency cap correctness.** "5-wide" — no per-host rate-limiting, no snapshot-write contention, no dedup on same-URL parallel fetches.

## Coupling and direction

Stable→volatile, the wrong way. User's verifier (intended stable) depends on Anthropic Research's Markdown (volatile, vendor-controlled, undocumented as interface). Mitigation "extend to OpenAI's format" makes it worse — coupling to N vendors' presentation formats with independent drift schedules.

No cycle introduced (v2 stack↔pipeline cycle is genuinely killed; credit where due).

## Ignored architectural alternatives

1. **Use the hosted engine's API/structured output, not its Markdown.** Both Anthropic Research and OpenAI Deep Research expose programmatic interfaces with structured citation objects. Removes the screen-scraper problem entirely. Obviously correct if regime 3 is built at all.
2. **Verifier-as-prompt, not verifier-as-pipeline.** Hand whole report + snapshot directory to one Haiku call with rubric. Lower wall-clock, no parser, no concurrency design, same artifact-on-disk reproducibility.
3. **Snapshot-as-service decoupled from verification.** Dumb snapshot daemon that archives every cited URL on a hook off "I saved a research output." Verification becomes optional and async; reproducibility preserved even if verifier never built.

## Frame-level objection

**Weekly-volume is a proxy for at least three orthogonal axes the plan conflates:** (a) consequence-magnitude per query, (b) domain-volatility (medical vs. tech vs. legal have different snapshot half-lives), (c) error-correlation between producer and verifier on the user's actual query distribution. The single triage question asks about (a) only and uses the answer to decide on machinery whose value depends on (b) and (c).

A user with one load-bearing query/month in oncology benefits from regime-3 snapshotting more than one with ten/week in JS framework news. **Volume sets the budget for engineering, not the kind of engineering needed.** The frame "pick the regime by volume" is a category error.

Secondary: plan's "no universal SOTA" stance is correct but it then proposes a universal triage protocol. Same mistake one level up.

## Verdict: rework.

Approve if regime 3 is specified against the hosted engine's structured API (not Markdown), with write-once snapshot store decoupled from verifier runtime, fail-closed parse semantics, explicit synthesis-claim disposition, and the triage protocol either expanded to cover consequence × volatility × correlation or honestly narrowed to "this protocol assumes your queries are roughly uniform on those axes."
