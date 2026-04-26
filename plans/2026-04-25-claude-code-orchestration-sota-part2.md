# SOTA orchestration knowledge — Part 2 (sections 5–9)

> Continuation of `plans/2026-04-25-claude-code-orchestration-sota.md`. See part 1 for status, scope, terminology, and the four-mechanism-group mental model.

---

## 5. Cross-model orchestration as a separate axis

The first synthesis missed this entirely. The user pointed it out. The second synthesis over-corrected into "the 2026 evidence says don't bother." Both were wrong. Here is the rebalanced read.

### Why building cross-model in is defensible *even if benchmark parity holds*

1. **Vendor-risk hedging.** A single-vendor outage, pricing change, or policy shift breaks single-vendor stacks. Multi-vendor capability is a continuity property, not a quality property.
2. **Capability-gap insurance.** Frontier model strengths are non-uniform — long-context, math, structured output, code synthesis, multimodal. Single-vendor stacks inherit that vendor's weak spots.
3. **Cost-volatility hedging.** Token prices have shifted multiple times since 2024. Routing capability is optionality.
4. **Eval credibility.** Single-model judges have known correlation with the model being judged. Judge ensembles (Panel-of-LLMs, SE-Jury) are standard practice for evals where this matters.
5. **Regulatory / procurement pressure.** Some buyers require multi-vendor capability for procurement compliance.

### Where the 2026 empirical picture pushes back

All of the following are **directional, retrieved at snippet level, unverified at primary source in this pass.** The upgrade process should re-verify before committing infrastructure on any of them.

1. Several recent papers report matched-compute single-agent meeting or beating multi-agent on coding/reasoning under equal token budgets. Implication: much of the multi-agent quality lift in 2024–2025 was *extra compute*, not *architecture*.
2. "Self-MoA" (aggregating multiple samples from one strong model) has been reported to beat cross-vendor mixes on at least one instruction-following benchmark. Benchmark-specific result; do not over-extrapolate.
3. Adversarial-debater failure modes are documented: a single bad-faith debater can drag group accuracy down and *increase* consensus on wrong answers. The naive "more perspectives = better" frame is empirically wrong in the cases studied.
4. **Frontier compression.** Top-tier models converge in capability while diverging in cost. This makes architect-coder splits ("frontier plans, cheaper executes") increasingly a *cost-arbitrage* play rather than a *capability* play.

### Synthesis (labeled as such, not field consensus)

For runtime quality, **single-model with self-consistency at matched compute is competitive with most cross-model setups in 2026**. For non-quality reasons — vendor hedging, eval credibility, cost arbitrage, capability-gap insurance, procurement — **cross-model still earns its tokens**. Build it in if those reasons apply; don't build it for runtime quality alone.

### Patterns that still earn tokens cross-model in 2026

- High-stakes verification with diverse checkers (the *pattern*, of which `/ultrareview` is one product instance).
- Judge ensembles for evals.
- Cost-routing fallback (cheap-first, escalate-on-low-confidence; OpenRouter is the mainstream substrate).
- Architect-coder cost split when token cost dominates (Aider, Roo Code).
- Confidence-weighted self-consistency on the same strong model (efficiency-focused descendants of Wang et al.'s self-consistency; ReASC / CISC / DeepConf style — directional).

---

## 6. Workload archetypes (shapes, not products)

Pick the archetype closest to your workload. Do not try to use all primitives. The modal practitioner failure in 2026 is *over-authoring* — kitchen-sink stacks that dilute tool-selection priors and multiply debug surface.

### Baseline — No orchestration

Lean `CLAUDE.md` + raw tool use. No authored skills, hooks, subagents, or plugins.

**When right:** workflows don't repeat; frontier-model one-shot reasoning is enough; the cost of authoring exceeds the cost of repeating yourself.

**Failure mode:** team grows, conventions drift, prompts diverge across developers — but this is a *future* failure, not a current one. Migrate when the failure actually starts showing up.

### A — Solo repetition

Lean `CLAUDE.md` + 3–10 skills (some user-invocable as `/cmd`s) + output style if persona matters + 2–3 hooks for invariants + MCP only at process boundaries + subagents on demand.

**When right:** single developer with named, repeating workflows.

**Authoring discipline:** structural criterion replacing the unsourced "≥3 times" heuristic — author a primitive only when the workflow has (a) stable inputs/outputs, (b) a name you'd say out loud, and (c) at least one execution where the absence of the primitive *demonstrably* hurt. Until all three hold, don't author — fatten `CLAUDE.md` instead.

### B — Adversarial review *(single observed instance: this stack)*

Fresh-context subagents per role (critic, librarian, outside-view, explorer), lean `CLAUDE.md` (routing rules), skills encode review heuristics, hooks gate destructive actions.

**When right:** decisions where the cost of an unchallenged answer exceeds the token cost of fresh-context review.

**Treat this as a documented case, not a general pattern.** n=1. The stack was authored by someone who already believed in this composition; using it as evidence of a pattern is confirmation bias.

### C — Team / polyrepo

Plugin-distributed bundle (CLAUDE.md fragments + skills + hooks) + per-repo `CLAUDE.md` for project specifics + shared MCP servers + Routines for team automation + Managed Agents for hosted long-running work.

**When right:** team of 3+ developers across 2+ repos with shared conventions.

**Failure modes:** governance becomes load-bearing (signed plugins, version pinning); 3-axis eval matrix per consumer team that nobody budgets for; upgrade blast radius is worst here.

### D — Regulated / audit

Hooks load-bearing for deterministic audit trail. `settings.json` permissions locked. MCP for compliance system integration. Skills/subagents subordinate to hook-driven trail.

**When right:** every state-changing action needs a deterministic record (financial, healthcare, regulated infrastructure).

**Failure mode:** hooks chosen for "reasoning required" tasks they cannot perform; audit trail looks complete but masks reasoning errors.

### E — Long-running async / scheduled

External orchestrator (Temporal, Airflow, custom DAG runner) **or** Anthropic Routines / Managed Agents. Local primitives thin. Model is one worker, not the orchestrator.

**When right:** unattended repeatable work; cron / webhook / API-triggered.

**Failure mode:** orchestrator-inside-the-model anti-pattern; trying to drive a DAG from an LLM context that has no durable state.

### F — High-stakes pre-commit verification with diverse checkers

Fan out parallel reviewers on different angles (logic / edges / security / perf), each finding *independently reproduced* before reporting.

**When right:** cost of a wrong answer dominates cost of verification (security review, financial PRs, public-facing product changes).

**`/ultrareview` is one productized instance.** The pattern is older than the product.

**Failure mode:** cargo-culted onto low-stakes PRs; pays 5–15× tokens for verification that's not load-bearing.

---

## 7. Decision aid: two-question intake before authoring anything

Before authoring any new primitive, answer:

1. **What is your dominant loop right now?**
   - Encoding always-on project rules → fatten `CLAUDE.md`
   - Repeated workflow with stable I/O and a name → Skill
   - Parallel research / large reads / role separation → Subagent
   - Correctness invariant that must always fire → Hook (first), not Skill
   - Crossing a process boundary (DB / API / browser / SaaS) → MCP (first), not Skill
   - Sharing a setup across repos / teammates → Plugin
   - Scheduled / triggered unattended execution → Routine
   - Hosted production deployment → Managed Agents

2. **Solo or team?**
   - Solo → archetype A or baseline; no plugin needed; CLAUDE.local.md for personal preferences
   - Team → archetype C; plugin distribution becomes load-bearing; governance matters

If you cannot answer the first question, **don't author anything**. Use the no-orchestration baseline and let the workload reveal itself.

---

## 8. Tradeoffs (carrying forward through both critic rounds)

1. **Authoring cost vs reuse horizon.** A primitive amortizes only if `invocations × savings > authoring + maintenance + debug-surface`. Most teams over-author.
2. **Debug surface multiplies per primitive.** Was it the hook? The skill description? The subagent's CLAUDE.md? The MCP schema? Each layer adds an attribution dimension.
3. **Eval matrix expands per primitive.** Each authored primitive needs its own fitness signal. Plugin-distributed bundles imply a 3-axis eval matrix per consumer team.
4. **Upgrade blast radius.** Layered stacks break in more places when the vendor ships a primitive change. The slash-commands → skills consolidation in 2025–2026 is the recent reference.
5. **Tool-selection-prior dilution.** Each new skill / MCP tool added lowers the prior probability the model picks the right one. Vercel's reported skill-undertrigger result is downstream of this.
6. **"Tokens" hides the real cost.** For many teams the bottleneck is human review time, latency, or blast radius. Token-matched comparisons obscure those.
7. **Mechanism vs pattern conflation.** A pattern is a *composition* of mechanisms. Mixing mechanism rows and pattern rows in a single table — as the first synthesis did — collapses the abstraction.
8. **Catalog completeness vs catalog usability.** First synthesis was incomplete; second was unreadable. Third grouped into four mechanism groups + separate sections. This residual tradeoff doesn't go away — every redo recovers more primitives, and the document gets longer.
9. **Empirical recency vs citation verifiability.** Reaching for 2026 papers to be current sacrifices verifiability when retrieval is snippet-only. A 2024 well-cited result beats a 2026 snippet-retrieved one for a design doc.
10. **Centering what the user asked vs centering what we think is correct.** When the user asks about cross-model orchestration, "well actually mostly don't" is defensible only if the framing is ironclad. It usually isn't.

---

## 9. Assumptions that would flip this synthesis

1. **Primitive set is stable for 12 months.** Demonstrably false in the trailing 12 months — slash commands collapsed into skills, Routines and Managed Agents shipped this month. Almost certainly false in the next 12.
2. **Frontier compression continues.** Probably yes; would further narrow cross-model *capability* arguments while leaving cross-model *risk-hedging* arguments intact.
3. **Token economics stays the binding constraint.** Could change with batch / cache pricing shifts or with frontier-model attention reliability improvements that make progressive disclosure unnecessary.
4. **Public practitioner stance reflects private practice.** Lagging signal at best. GitHub stars and X engagement are lagging indicators; silent subagent-heavy users aren't in the signal.
5. **Workloads are introspectable enough to pick an archetype.** Often false in practice; teams oscillate weekly. The two-question intake mitigates but doesn't solve this.
6. **Anthropic's official decision rubric reflects what works empirically, not what they prefer to promote.** Vendor docs are marketing-adjacent. Vercel-style empirical results have, in at least one snippet-retrieved 2026 result, contradicted vendor positioning.
7. **The "no orchestration" baseline is taken seriously.** First two synthesis passes underweighted it. For most users on most days, fattening `CLAUDE.md` and using raw tools is the highest-ROI move.

---

> Continued in `plans/2026-04-25-claude-code-orchestration-sota-part3.md` (sections 10–17: conditions, sources, destinations, open questions, residual uncertainty, experiments).
