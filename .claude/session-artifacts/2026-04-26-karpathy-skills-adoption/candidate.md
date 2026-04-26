# Candidate recommendation — karpathy-skills adoption (post-workflow)

## Position

The prior writeup's **direction** survives: do not install the plugin as a plugin; cherry-pick content into the user's existing setup. The prior writeup's **specific claim** that "most of the file is already in your global CLAUDE.md" was factually wrong — the global `CLAUDE.md` is empty (0 bytes, per Explore). That correction expands the action from "drop 1–2 lines" to "populate the currently-empty global `CLAUDE.md` with a measured 8–15 line subset, with Goal-Driven Execution as the highest-value single addition."

Final action set, ranked:
1. **Recommended (do this):** Add 8–15 lines to the global `CLAUDE.md` covering Goal-Driven Execution (failing-test-first / verifiable success criteria) plus a one-line standing version of "Think Before Coding" (clarify before assume). Skip Simplicity First and Surgical Changes — those are already covered by the default Claude Code system prompt and adding them is duplication that pays attention-budget cost without behavior change.
2. **Conditional (do this if assumption A1 is wrong):** If `quality-assurance-validator` already encodes test-first discipline, drop Goal-Driven Execution from the addition and add only Think Before Coding. Total addition: 2–4 lines.
3. **Rejected:** install the marketplace plugin. Replace label from scope-map: zero plugins installed, single-machine setup, opaque overlap with agents, no measured upside, maintenance asymmetry risk (outside-view distillation #4).
4. **Rejected:** Do nothing. The empty CLAUDE.md is a continuous opportunity-cost bleed (challenges.md falsifying condition); leaving it empty after Explore confirmed Goal-Driven Execution is *entirely absent* from the setup is harder to defend than adding 8–15 lines.

## Named tradeoffs

- **Specificity vs. parsimony.** Canon #6 (Anthropic multi-agent essay): explicit heuristics measurably moved behavior even where defaults nominally covered the case. Canon #2 (effective context engineering): minimal set, add only on demonstrated failure. These pull opposite directions. The recommendation splits them — add the principle that fills a verified gap (Goal-Driven Execution), skip the principles that duplicate.
- **Always-on coverage vs. agent-sprawl drift.** Standing instructions in CLAUDE.md fire on every session; the seven global agents fire only on invocation. Stacking both creates the silent overlap-induced drift outside-view named as the modal failure (challenges.md preservation challenge #1). This recommendation accepts that risk for Goal-Driven Execution because the gap is real; it rejects that risk for the other three principles.
- **Single-merged file under user version control vs. installed plugin with auto-update.** Single file gives explicit control and zero maintenance asymmetry; plugin gives auto-update at the cost of opaque drift. For a single-machine, no-plugin user, the file wins; for a team or multi-machine deployment, the plugin would win.
- **Acting before measuring vs. measuring first.** Canon #4: "with effect sizes this large, you can spot changes with just a few test cases." The corpus-endorsed move is to A/B before adopting. This recommendation acts without the A/B because the cost of the action is bounded (rollback = delete the lines) and the cost of waiting (continued empty-file state) is non-zero per the falsifying condition.

## Named assumptions (each would flip the recommendation if wrong)

**A1.** The `quality-assurance-validator` global agent does not already encode test-first / verifiable-success-criteria discipline. **Flip:** if it does, Goal-Driven Execution becomes duplication and the addition shrinks to 2–4 lines covering only Think Before Coding. Most decision-relevant unknown per scope-map.

**A2.** The Claude Code default system prompt currently in production covers Surgical Changes and Simplicity First with enough specificity that adding the karpathy lines for them is duplication, not extension. **Flip:** if the defaults are weaker than assumed (canon staleness flag — defaults are a moving target), the addition expands to include those two principles too, ~20–30 lines total. Validating this assumption requires reading the current default system prompt, which neither Explore nor canon did; this is an unsought-evidence gap.

**A3.** The user works across multiple repos on a single machine where a global CLAUDE.md is the correct layer for standing instructions. **Flip:** if the user works primarily in one repo with a rich project-level CLAUDE.md, the global file is the wrong layer and the addition belongs in project files instead.

**A4.** The four karpathy principles, as instruction text, actually move Claude Code behavior on the user's task distribution. **Flip:** if they are placebo (no behavior change against the user's task mix), the recommendation collapses to "do nothing." Canon #4 says A/B with ~5–20 test cases would resolve this; the workflow did not run that A/B; the recommendation is therefore *provisional* until the user runs the A/B or accepts the action under provisional confidence.

## Frame-level objection (from challenges.md) — addressed

The frame-challenger's objection: regret-minimization mechanically favors the cheapest action; the generator must name what evidence would have forced a recommendation *more expensive* than the prior, and whether that evidence was sought.

**What would force a more-expensive recommendation:**
- (a) Empirical A/B on the user's coding tasks showing karpathy lines move behavior measurably. **Sought?** No. Canon explicitly endorsed this move (#4) and it was not run. **Implication:** the recommendation is provisional, not final. If the user is willing to run a one-hour A/B on ~10 representative tasks, the recommendation can firm up or flip.
- (b) Plugin author having recognized-authority status for Claude Code conventions specifically. **Sought?** Partially. Outside-view flagged this as the verdict-pivot (community-config class 15–25% durable / canonical-from-authority class 50–70%). Karpathy is an authority on LLM coding pitfalls in general; the plugin packager (forrestchang) is not a recognized authority on Claude Code harness configuration. The contradicting class does not apply.
- (c) Active need to share conventions with collaborators across machines. **Sought?** Yes. Explore confirmed single-machine, no-plugins, no-skills-directory. The packaging-mechanism upside does not apply.

**Net:** One piece of evidence (A/B) was not sought. That is a real gap. The recommendation explicitly carries the gap forward as a named uncertainty rather than treating it as resolved.

## Ways this recommendation could be wrong

1. **Karpathy-as-source bias.** The four principles come from one tweet. The whole exercise may be premised on a hot take rather than a durable artifact. The fact that the workflow is being run on it does not validate the source.
2. **Meta-validation amplification.** The prior recommendation was already produced by this orchestrator. Running the same orchestrator's workflow on it risks confirmation by structural similarity rather than independent check (challenges.md alternative frame).
3. **Adding standing instructions while keeping seven global agents** stacks layers that overlap on the same coverage area, which is the modal failure mode outside-view named (#4) and which this recommendation pays for in exchange for filling the Goal-Driven Execution gap. Six months from now the user may not be able to attribute behavior to the right layer.
4. **The empty global CLAUDE.md may be empty by intent**, not by oversight. If the user deliberately keeps it empty as a "trust the defaults" stance, populating it contradicts that stance. The workflow did not check user intent.
