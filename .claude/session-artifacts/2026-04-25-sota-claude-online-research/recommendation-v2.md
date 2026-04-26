# Generator — Candidate Recommendation v2 (post-critic rewrite)

## Position

The honest answer for almost every user is: **use a hosted Deep Research product as your default, attach a permanent unverified-output disclaimer, and only escalate to a local verification pipeline when (a) a specific output will drive a specific irreversible action and (b) you can name the consequence-tolerance.** "SOTA" is not an architecture; it is a *triage policy* — knowing when not to engineer is the larger half of the answer.

Concretely:

- **Default (≈90% of queries): Mode S.** Anthropic Research or OpenAI Deep Research, used directly. Outside-view places this at 40–55% joint success — at-base-rate by construction. No local primitives. Permanent ribbon: *"5–15% of citations may be fabricated; do not act on this without re-reading sources."* Time-to-first-result: ≈30 s. Setup cost: zero.

- **Opt-in escalation (≈8% of queries): Mode D.** The same `/research` command, invoked with `--audit`, runs the hosted engine **and** a separate on-disk-artifact verifier. The verifier is a *separate Claude Code session* reading the producer's `claims.jsonl` and writing `verification.jsonl`; the user sees both files plus a single-page summary. No hooks, no cycles, no gating. The verifier is opt-in per run, never the default.

- **Opt-in de-escalation (≈2% of queries): Mode P.** The same `/research` command, invoked with `--scout`, returns *only* "here are N ranked candidate sources with one-paragraph faithful summaries — synthesize them yourself." No autonomous synthesis, no verifier (because there is nothing to verify yet), no report. Used when the user knows the consequence is irreversible and the LLM's role is sourcing, not reasoning.

The S/D/P framing survives from v1 but is reshaped: it is no longer a *gate the user passes before getting an answer*; it is a *flag on the same command*. The default is S; escalation requires one extra word.

## Mode D — the only mode with engineering content

Mode D, redesigned to clear the architecture and operations vetoes:

1. **Entry**: `/research --audit <question>`. A single command, not a Socratic interrogation. If `--audit` is omitted, Mode S runs; the result includes a one-line footer: *"Run with `--audit` to verify citations (≈10× cost)."*

2. **Producer phase**: subagents fan out ≤3-wide, no nesting, each writes its compressed return as `subagent-N.md` into `.claude/session-artifacts/<id>/research/`. Each cited claim is emitted as `{claim_text, source_url, quoted_passage, claim_id}` into `claims.jsonl`. **Atomic claims only**; synthesis claims are emitted with `synthesis: true` and a list of upstream `claim_ids` they depend on, addressing the architecture critic's claim-atomicity gap.

3. **Verifier phase**: a *separate* `claude -p` invocation reads `claims.jsonl`, re-fetches each `source_url` via `WebFetch`, compares the `quoted_passage` to the live page content, and writes `verification.jsonl` with `{claim_id, fetch_status, semantic_match, snapshot_diff, verdict}`. Verdict is one of `verified`, `partial`, `unverifiable`, `producer_was_wrong`. **The verifier is not in a hook.** It runs as a follow-up step after the producer completes. Failure isolation is structural: producer's output is on disk before verifier starts. If verifier crashes, the user still sees the producer output, with a banner: *"verification did not complete; treat as Mode S."* This kills the architecture critic's cross-cutting-concern objection.

4. **Cross-family**: verifier *should* run on a different model family from producer, but this is **a strong recommendation, not load-bearing**. The architecture critic was right that LLM independence cannot be assumed. The artifact-on-disk pattern means the verifier's correlation with the producer is now a *quality* concern (how good is the verification) rather than a *correctness* concern (does verification happen at all). Document in the result header: *"verifier model: <X>; producer model: <Y>; if X∈Y's family, verifier independence is unverified."*

5. **Tool surface**: exactly three MCP servers wired by default — one general web (Tavily or Brave), one academic (Exa or ArXiv), one browser-render (Playwright). Each MCP's tool docstring is owned by the user (canon: 40% of completion-time variance). A starter docstring set ships with the recommendation as a copy-pasteable artifact.

6. **Result surface**: a single Markdown report with two visible affordances:
   - A header that states: *"Producer: Opus 4.7. Verifier: Haiku 4.5. N claims, V verified, P partial, U unverifiable. Cost: $X.XX. Wall-clock: T sec. Verifier independence: <known/unknown>."*
   - Per-claim badges only on `partial` and `unverifiable` claims (not `verified` — green checkmarks are the false-god surface the frame-challenger flagged). Each non-verified badge has a `[re-verify]` link that re-runs the verifier on that single claim.
   - **No critic-panel pass in the pipeline.** The critic-panel is available as a separate command (`/research-critique <session-id>`) the user invokes when they want the stack's framing applied. This breaks the cycle the architecture critic identified.

7. **Cost cap**: enforced by the **producer** at start of run, not by a hook. The first action of the producer is to compute an upper bound (3 subagents × 15× chat tokens × N citations × verifier multiplier), display it, and refuse to proceed if it exceeds a user-configured ceiling. Honest gap: *Claude Code does not expose a mid-run abort primitive*; if the run blows past the estimate, the user must Ctrl-C. This is named, not papered over.

8. **Shadow rollout**: first week, `--audit` runs in *log-only* mode — verifier produces `verification.jsonl` but the result is presented identically to Mode S. The user reads the verification file out of band and learns whether they trust the verifier before depending on it. Documented in the recommendation, not hidden.

9. **Rollback**: a single setting (`research.audit_enabled: false` in `.claude/settings.json`) disables the verifier phase. Documented as the first line of the runbook.

10. **Quarterly re-validation routine**: a Routine the user *must* enable when adopting Mode D. Re-runs a fixed reference query (one the user picks at adoption time) every 90 days and surfaces a diff against the prior run. If the diff is non-trivial, the user is prompted to re-validate the composition. This pairs Mode D with the lifecycle the operations critic demanded; without it, Mode D is not adopted.

## Mode P — sketch only

`/research --scout <question>` returns:
- 12 ranked candidate sources from B1 (`WebSearch`) + B2 (`WebFetch`) + the three MCPs.
- One-paragraph faithful summary of each (verbatim quote + citation, no synthesis).
- A footer: *"Synthesis is your job. The LLM's role here is sourcing only."*
- No verifier (nothing to verify; there are no claims yet).

This is a 30-line composition, not an architecture. It exists because some queries should never be autonomously synthesized.

## What is discarded from v1

- The user-self-classifies-mode-before-querying interaction (product critic).
- The post-tool-call hook as the verification mechanism (architecture critic).
- The cross-family-verifier-as-load-bearing assumption (architecture critic).
- The critic-panel-in-pipeline cycle (architecture critic).
- The "refuse to ship one-command Mode D" paternalism (product critic).
- The per-claim green-check badges on verified claims (frame-challenger's false-god risk; product critic's cognitive-load critique).
- LangGraph, CrewAI, smolagents, AutoGen, OpenDeepResearch as runtimes (scope-map).
- Multi-engine cross-checking (scope-map).

## Named tradeoffs

| tradeoff | what we give up | what we get |
|---|---|---|
| Mode S as default | The "we built something" satisfaction | Time-to-first-result of 30s; honest base-rate alignment |
| Verifier as opt-in (`--audit`) | A single trustworthy mode | Most queries don't pay verifier cost; users opt in when consequence demands it |
| Artifact-on-disk verifier (not hook) | Tight coupling that "feels" like a pipeline | Failure isolation; producer output survives verifier crash; no cycle |
| Cost cap pre-computed by producer | Real-time enforcement | Upfront estimate users can refuse; honest about Claude Code's lack of mid-run abort |
| Quarterly re-validation as condition of adoption | Frictionless onboarding | The composition does not silently rot under substrate churn |
| No green badges on verified claims | The reassuring single signal | Verifier signal surfaces only where action is required |
| Critic-panel as separate command | One-stop integration | Stable layer (the stack) does not depend on volatile layer (the pipeline) |

## Named assumptions (≥3 that flip the recommendation if wrong)

1. **Hosted Deep Research products' 40–55% joint success rate is acceptable for the user's typical query.** If the user's query distribution is dominated by load-bearing decisions, Mode S as default is wrong, and Mode D should be the default. The recommendation has no telemetry to detect this; the user must self-assess after a month of use and override the default if their `--audit` rate exceeds ~30%.

2. **The user has the discipline to use `--audit` exactly when they need it.** If users either (a) never opt in (over-trusting Mode S) or (b) always opt in (treating it as risk-free), the recommendation produces silent error or pure overhead. The shadow-mode week mitigates (b) by making the verifier output visible without being load-bearing; nothing in the recommendation mitigates (a) other than the disclaimer ribbon.

3. **An on-disk-artifact verifier produces useful enough verdicts to justify ≈10× cost when invoked.** This is unmeasured. The shadow-mode week is the cheapest experiment to test it (next-action note for synthesis).

4. **Hosted engines do not close the citation gap in 6 months.** If they ship per-claim verification themselves, Mode D's value collapses and the recommendation reduces to "use Mode S, ignore the rest."

5. **The user has at least one stable research workflow.** If research is genuinely one-shot, the entire setup (MCP servers, Routine, claims.jsonl convention) is wasted. Honest acknowledgment: for one-shot users, the recommendation is "use Anthropic Research in the browser; close this document."

## Named ways this could be wrong

- The artifact-on-disk verifier may underperform the in-pipeline hook on accuracy because it loses the producer's intermediate reasoning context (architecture critic's invariant #1, claim atomicity). The trade is: structural failure isolation in exchange for some semantic verification quality. May be the wrong trade for very synthesis-heavy domains.
- "Quarterly re-validation as condition of adoption" is a behavioural assumption; users will skip it. If skipped, Mode D rots silently and is worse than Mode S because the user trusts a stale verifier.
- The "5–15% citation hallucination" number from outside-view is from a 2026 benchmark that may not match the user's distribution. The disclaimer ribbon may be optimistic or pessimistic by ≈2× in either direction.
- Mode P is sketched, not designed. If users opt into it and find it useless ("just give me the answer"), the de-escalation path becomes vestigial.
- The recommendation still inherits the canon's Anthropic-source bias (librarian's missed gap). Architectural primitives endorsed here (orchestrator-worker, 5-axis rubric, just-in-time context) are one vendor's taste presented as best practice. Independent replication does not exist.

## Frame-level objection addressed (revised)

The frame-challenger's objection — *the recommendation must name which user it is for, or it is unfalsifiable* — is now addressed by **defaulting to the least-engineered mode (S)** and treating engineering effort (D, P) as opt-in escalation/de-escalation paths reachable from the same command. The user does not pre-classify; they choose a flag per-query, and the default is the answer for the median query.

The architecture critic's frame objection — *the architecture cannot deliver model-independence; it is a wager dressed as topology* — is addressed by demoting cross-family verification from load-bearing to a labelled-but-not-required quality property of the verifier. The artifact-on-disk pattern is what makes the verifier *exist*; whether it is *good* is a separate question the shadow-mode week is designed to answer per user.

The operations critic's frame objection — *Mode D is a lifecycle problem under a 60–90 day churn substrate, not a composition* — is addressed by pairing Mode D adoption with the quarterly re-validation Routine as a non-optional condition. If the user will not enable the Routine, the recommendation is "do not adopt Mode D; stay in Mode S."

The product critic's frame objection — *S/D/P is a product surface the system is forcing the user to render, with no chooser* — is addressed by collapsing the chooser into a flag (`--audit`, `--scout`) on a single command, with Mode S as the default. The user does not render the surface; they pick a verb.
