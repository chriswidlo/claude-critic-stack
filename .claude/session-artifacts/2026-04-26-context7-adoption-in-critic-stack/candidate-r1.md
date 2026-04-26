# Candidate recommendation — Revision 1

## Position

**Adopt shape E now (Context7 as a Claude Code Skill, out-of-workflow). Defer all in-workflow shapes (B/C/D) pending two cheap prerequisite artifacts. If those prerequisites resolve in favor of admission, the in-workflow shape is subsumption-as-second-adapter (challenger's preferred shape) — Context7 becomes a backend that canon-librarian itself can call, with a tier field on returned passages.**

Concretely, today:
1. **Install Context7 as a Skill** (`npx ctx7 setup --claude`) and add an MCP server entry to `settings.json`. The Skill is invoked on demand by the user during ad-hoc code work in this directory and is **explicitly off-limits to the 12-step workflow agents**. CLAUDE.md gets one new sentence under "Things you must not do": *"Workflow agents (steps 3–9) must not call the Context7 Skill. Library-doc retrieval is not part of the in-workflow trust model until a trust-tiers policy admits it."*
2. **Write `canon/trust-tiers.md`** (one page, ~30 minutes). Names the existing tiers (`curated-canon`, `web-currency`) and explicitly leaves a placeholder for `vendor-live` marked *"not admitted; admission requires…"*. This is the artifact the challenger's frame-level objection demands.
3. **Do the measurement** — over the next ~10 design questions routed through the stack, log whether the question names a specific library + version. If ≥20% do, re-open the in-workflow integration question. If <20%, close it explicitly and document why in `decision-log.md`.

If and only if the measurement crosses threshold AND the trust-tiers policy admits a `vendor-live` tier, **then** implement subsumption: extend `canon-librarian` to call Context7 as a second adapter, label every returned passage with `tier:`, and extend the contradiction-required rule to demand a cross-tier check when a curated passage exists on the same topic.

## Frame-level objection — how this addresses it

The challenger's frame-level objection: *"Defend why the trust-tier policy question is not prior to the integration-shape question — why we are choosing pipes before deciding whether the fluid is admitted to the building."*

Answer: it is prior, and this candidate makes it prior. The trust-tiers artifact is step 2; no in-workflow integration shape (B/C/D) is on the table until that artifact admits a `vendor-live` tier. The Skill (E) is *not* an in-workflow integration — it is a user-facing capability outside the workflow's trust model — which is why it can ship now without the policy in place. The candidate refuses to choose pipes before admitting the fluid; it only opens a side faucet for the human's own use.

## Named tradeoffs

1. **Speed vs. discipline.** Just installing shape C today would be faster (one new agent, drop into parallel-gather). The candidate trades speed for the ability to preserve canon-first as a hard rule. If the user values shipping over rule integrity, this is wrong.
2. **Two-artifact prerequisite friction.** A 30-minute trust-tiers doc + a 10-question measurement period delays in-workflow adoption by days-to-weeks. The friction is real and disproportionate to the value if library-bottleneck questions are common.
3. **Subsumption is operationally heavier than C.** Rewriting canon-librarian to support a second backend is a meaningful lift compared to standing up a sibling subagent. If the measurement says "yes admit," the implementation cost is higher under subsumption than under C — bought in exchange for one retrieval port instead of two (Cockburn S5/C6 alignment).
4. **E backdoors what the workflow refuses.** Allowing the user to invoke Context7 via Skill while denying workflow agents access is a coherent split — but it relies on the user honoring the boundary. If the user pastes Skill-fetched library docs into a design-question prompt, the workflow agents see them anyway, and the trust-tier separation is fictional.
5. **Measurement is informal.** "Log the next 10 questions" is not a statistically meaningful base rate. It is the cheapest possible signal, and the candidate accepts that — but a real telemetry primitive (named in scope-map as missing) would be better and is not built here.

## Named assumptions (≥3, flipping the recommendation)

1. **Design questions in this stack rarely bottleneck on current library-API specifics.** Estimated <20% of questions name a specific library + version. *If wrong* (≥25%), the candidate flips: adopt subsumption-as-second-adapter immediately; the trust-tiers doc is still required but it is a one-day blocker, not a "wait for measurement" gate. The frame-challenger explicitly named this falsifier (the >25% condition).
2. **The canon-librarian contradiction-required rule can be coherently extended to cross-tier checks.** I.e., "a vendor passage must be cross-checked against a curated passage when one exists" is a meaningful operation. *If wrong* (vendor and curated material talk past each other and cross-tier checks generate noise rather than signal), then subsumption is incoherent and the only viable adoption is permanent shape E. The in-workflow door closes for good.
3. **The user actually does ad-hoc code work in this directory.** *If wrong* — the cwd is strictly the critic stack, no other use ever happens here — shape E has zero consumers and step 1 of the candidate is cargo-cult installation. The recommendation collapses to pure shape A (do nothing) plus the two prerequisite artifacts.
4. **Vendor-authored docs are persuasive enough that injecting them into adversarial-review agents would degrade critique quality.** This is the central anti-anchoring premise. *If wrong* (the critic-panel absorbs vendor-tone material without bias — perhaps because the lens prompts are strong enough), the trust-tier policy is much lower-stakes; shape B (raw tool on every agent) becomes acceptable and the candidate is overcautious.
5. **Context7's per-query cost stays inside the workflow's token/latency budget.** ~3.3k tokens, ~15s per call (per the 2026 architecture rewrite). *If wrong* — the parallel-gather slot blows past budget when library-docs fires often, or Context7's quota model interrupts mid-run — staged rollout is mandatory regardless of which shape is chosen, and the candidate's "implement subsumption directly upon admission" path needs a feature flag.

## Named ways this could be wrong

1. **"Trust-tier policy first" may be procrustean delay.** The right move could be to just spike C in a branch, run it on five real questions, and learn faster than any policy doc would teach. Ship-then-measure, not policy-then-measure.
2. **The recommendation may overweight architectural symmetry.** Cockburn-style "one port, multiple adapters" is pretty, but the operational truth is canon-librarian is a *small* agent with a specific job. Bolting a vendor backend onto it might just make a clean small thing into a messy small thing for marginal architectural gain. A separate library-docs subagent (shape C) is uglier on paper but easier to delete if it doesn't pay off.
3. **The Skill / workflow boundary may be theatrical.** If the user habitually drafts design questions while the Skill is loaded and pastes Skill output into the prompt, workflow agents see vendor docs anyway via the user prompt — the boundary exists in the agent prompts but not in the user's workflow. Either accept that the Skill *will* leak into design-question contexts, or don't install the Skill in this directory at all.
4. **"Investigation" may have been the right classifier label all along** (challenger's classifier-challenge). If so, the candidate's "do the 10-question measurement" is a fig leaf for refusing to do the actual investigation now, and the right artifact today is a longer measurement plan, not a Skill install plus a one-page policy.
5. **Shape D may be more defensible than the scope-map admits.** The scope-map called D "answers a different question," but if the canon-refresher is repurposed to ingest only the *stable* subsets of Context7's index (e.g., LTS framework versions, deprecated-API lists used to flag legacy code) into canon as principle-adjacent reference material, D could be coherent — and would be the only shape that strengthens canon rather than competing with it. The candidate dismisses D too quickly.
