# 07 — Deep dive: critic-panel collapse + ablation harness (S2 + S3 paired)

## Position

Two changes that only make sense together: collapse the three critic-lens files to one parametrised `critic` agent (S2), and build a small ablation-capable eval harness so the collapse — and every other future shrink — has a defensible empirical backing (S3). This is the **mandatory removal** per the brief, paired with the operational mechanism that turns *one* removal into *the precondition for many*.

Concretely:

1. Replace [critic-architecture](../../.claude/agents/critic-architecture.md), [critic-operations](../../.claude/agents/critic-operations.md), [critic-product](../../.claude/agents/critic-product.md) with one `critic.md` taking `--lens=architecture|operations|product` (or rotating internally across all three in one call). Run it 1–3 times in parallel as the orchestrator chooses; the orchestrator's lens-selection is a small added responsibility, possibly itself a 50-line decision rule.
2. Build `evals/` with N paired-scenario tests (each pair: same question with one altered detail that should change the answer) plus an `ablation` mode that disables a single agent or step and re-runs the suite. Tests grade two ways: by *artifact-feature pattern matching* (does `scope-map.md` contain a `replace` row for primitive X?) and by *grader-prompt scoring*.

The pair is non-negotiable: collapse without ablation is faith; ablation without collapse leaves the redundancy in place. Together they argue that *the stack should justify every primitive empirically and shed the ones that don't earn keep*.

## The reframe this embodies

The stack today is *additively maintained*. Every change in the recorded history of [plans/ok-cool-this-is-warm-balloon.md](../../plans/ok-cool-this-is-warm-balloon.md) — the move from 6-step to 12-step, the addition of the three-lens panel, the addition of the requirement-classifier and subagent-distiller — is *more*. Nothing has been removed since the original 6-step shape. There is no instrument the stack has used to decide that an addition was wrong, because there is no instrument at all.

This proposal reframes the stack as *empirically maintained*. Additions earn their keep against the eval suite; removals are defensible against the same suite. The minority-veto critic-panel becomes one configuration to test, not a fixed feature. The 12-step pipeline becomes a hypothesis. The shape that wins is the shape the suite blesses — within the operator's tolerance for surface area.

```
BEFORE                               AFTER
Add capability.                       Add capability and a paired eval scenario.
Trust prose discipline.               Trust prose discipline plus pattern-match grading.
Three lens files,                     One critic, three lens configurations,
fixed minority-veto.                   selectable per session.
Refactor by faith.                    Refactor against the suite; ablate to defend removals.
```

## Mechanism — what gets added, removed, or changed

**Added:**
- `evals/` directory at repo root.
- `evals/scenarios/<slug>/` per scenario, containing `question.md`, `expected-features.yaml` (artifact-pattern checks), and an optional `grader-prompt.md` for the LLM-graded part.
- `evals/run.mjs` — small zero-dep Node runner (matching the existing [bin/ingest-canon.mjs](../../bin/ingest-canon.mjs) style) that orchestrates: launch a fresh session against each scenario, capture artifacts, run pattern-match assertions, optionally invoke a grader.
- `evals/ablation.mjs` — wrapper that disables a single agent or workflow step (by renaming the agent file or skipping the step) and re-runs the suite, producing a delta report.
- `.claude/commands/promote-eval.md` — slash command to canonicalise a finished session as a new scenario.
- One unified `critic.md` agent file.

**Removed:**
- The three lens files: [critic-architecture](../../.claude/agents/critic-architecture.md), [critic-operations](../../.claude/agents/critic-operations.md), [critic-product](../../.claude/agents/critic-product.md). Their lens-specific content survives as sections inside the new `critic.md`.

**Changed:**
- Step 10 in [CLAUDE.md](../../CLAUDE.md) — replace "invoke the three critic lenses in parallel" with "invoke `critic` once per chosen lens; the orchestrator chooses 1–3 lenses based on the question's risk surface (defaulting to all three for hard-to-reverse decisions)."
- The [ark-mono regression test](../../tests/regression/ark-mono-connector-routing.md) becomes the first scenario in `evals/scenarios/`, with its acceptance criteria expressed as `expected-features.yaml`.

**Surface area.** Larger than S1: a small Node runner, two slash commands, one new agent, three deletions, several `CLAUDE.md` edits. This is the most invasive shortlist item. It is also the one that *earns the right to do everything else* — without it, S1, S4, S5, and S6 are faith-based.

## Literature this draws on

- Zheng, Chiang, et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (2023; arXiv:2306.05685) — the canonical reference for **position bias**, **length bias**, and **self-preference bias** in LLM-as-judge configurations. Directly applicable: the three same-model lenses are three same-model judges; the eval suite must include grader-prompt sanity checks (re-grade with shuffled position; re-grade with shuffled length).
- Panickssery, Bowman, Feng, *LLM Evaluators Recognize and Favor Their Own Generations* (2024; arXiv:2404.13076) — tightens the self-preference result. Implication: the grader prompt for `evals/` should be authored to *suppress* the easy positive grade; pattern-match grading is the safer half of the harness.
- Khan, Hughes, Valentine, et al., *Debating with More Persuasive LLMs Leads to More Truthful Answers* (2024 ICML; arXiv:2402.06782) — provides one of the few real workflow-scale comparisons of single-judge vs. multi-judge vs. debate configurations. The eval harness should support these as alternative configurations to test.
- Anthropic, *How we built our multi-agent research system* (2025; in canon at [anthropic-multi-agent-research-system](../../canon/corpus/anthropic-multi-agent-research-system/)) — explicit on the importance of *evaluation* as the bottleneck for multi-agent system iteration. Confirms that without an eval harness, multi-agent system development is largely opinion.
- The xUnit / Beck *TDD by Example* tradition (Beck, 2002, in canon manifest as a stub) — the test-first move applies to workflow design as much as to code. The proposal makes the workflow test-able where today it is only inspectable.

**Contradicting evidence I am required to surface.** Eval suites for LLM systems have a known half-life: the suite was authored against a model snapshot; subsequent model upgrades silently change the score distribution; the suite gives confident verdicts on a moving target. (The MT-Bench, AlpacaEval, and Chatbot-Arena teams have all published versions of this concern between 2023 and 2025.) Implication: a suite that grades the workflow today may be measuring noise in six months; the harness must include a "re-baseline" step on every model upgrade. If that step is skipped, the harness is more dangerous than no harness — false confidence in unchanged behaviour.

A second contradiction: Klein's *naturalistic decision-making* tradition explicitly warns that *measuring* a judgmental process can degrade it (the *measurement induces optimisation toward the measure* failure, sometimes called Goodhart's law). The eval harness will measure pattern-features in artifacts; agents will, over time, drift toward producing those features whether or not the underlying reasoning is sound. The harness must include adversarial examples where the *features* are present but the *reasoning* is wrong, and the harness must score those as failures. This is hard.

## Known failure modes (≥3, named)

1. **Goodhart on the pattern-feature checks.** Agents (or the operator editing prompts) drift toward producing the patterns the harness checks for. After six months, the suite tells you the patterns are still produced; it does not tell you the reasoning is still sound.
2. **Grader prompts inherit self-preference bias.** The grader is the same model family as the orchestrator. Panickssery et al.'s result applies. Mitigation: the grader prompt should be authored to default-low and require positive evidence; alternate-model graders if available; track inter-grader agreement when re-running.
3. **The eval suite ossifies into the operator's initial imagination.** The promote-eval command exists exactly to combat this, but operators don't use it because canonicalising an in-progress session feels like premature commitment. If promote-eval has zero invocations after three months, the suite is reflecting the operator-from-the-past, not the operator-now.
4. **Ablation results are noisy at low N.** With only ~10 scenarios, removing a single agent may produce an ambiguous delta (1–2 scenarios shift, hard to attribute). The honest move is to refuse to remove anything based on N=10 results; the temptation will be to remove anyway because the work has been done.

## Kill criteria (≥3, observable)

- **Zero `/promote-eval` invocations in the first three months.** The self-growth mechanism failed; the suite is now a museum piece. Either re-author the trigger (perhaps automatic on session close) or accept that the suite will not grow and keep it small.
- **Ablation runs produce non-significant deltas on every removal candidate.** This either means the harness is too coarse to detect real differences (rebuild it with more scenarios or sharper checks), or means most of the agents are doing nothing measurable (in which case the stack should shrink dramatically). Either is actionable; *neither* is the kill — sitting in this state for six months without choosing is the kill.
- **The grader prompt's inter-run agreement on the same scenario is below ~80%.** The harness is producing noise; verdicts are not reproducible; ship-or-don't-ship decisions made on the basis of the harness are unsafe.
- **The harness becomes the bottleneck for shipping changes** — measured by "wall-clock time to commit a `CLAUDE.md` change has gone from minutes to hours, and the operator now resists making changes." The instrument has become a brake. Reduce the scenario count or run a pre-commit subset.

## Cheapest experiment

**One week, one scenario, one ablation.** Take the existing [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md) and convert its acceptance criteria to a machine-runnable `expected-features.yaml`. Run the workflow against it twice: once normally, once with `critic-product` renamed (i.e. with two-of-three lenses ablated). Compare the seven acceptance criteria on each run. If two-of-three lenses still passes the test, the third lens is doing nothing detectable on this scenario — evidence (weak, n=1) for collapse. If the ablation breaks specific criteria, those are the criteria the third lens earned its keep on, and the harness now has its first real signal.

Total time: ~3 hours of operator time (writing `expected-features.yaml`, running the two sessions, reading the diffs). Success metric: a clear directional signal (passes / fails) plus a concrete list of which features broke under ablation. Reject metric: the conversion of acceptance-criteria-to-feature-checks turns out to be ambiguous (the existing prose criteria don't translate cleanly), suggesting the harness's pattern-match approach is not actually crisp enough to grade the workflow's outputs.

## Sequence

1. Convert [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md) to a single `evals/scenarios/ark-mono/` with `expected-features.yaml`.
2. Build a 100-line `evals/run.mjs` that takes a scenario, runs the workflow against it (out-of-band Claude session — manual or scripted), and grades the produced artifacts against the YAML feature checks.
3. Run the cheapest experiment above; decide go/no-go on the collapse.
4. If go: write the unified `critic.md`; delete the three lens files; update step 10 in [CLAUDE.md](../../CLAUDE.md). Re-run the eval; compare against pre-collapse baseline.
5. Add `evals/ablation.mjs` and run ablations against every other agent in turn, recording deltas.
6. Add `/promote-eval` slash command; canonicalise the next ~5 real sessions as new scenarios.
7. After ~3 months and ~10 scenarios: run the kill-criteria check; decide whether the harness is a tool or a brake.

External dependency: a way to run a Claude Code session non-interactively (the `claude` CLI in headless or piped mode). If this is not viable, the harness is operator-driven, which weakens the self-growth story but does not kill it.

## Counter-proposal

The strongest alternative is *do not collapse the critic panel; add a fourth `critic-meta` lens that audits the panel's self-preference bias.* This keeps the redundancy but makes its bias visible. I rank it below the proposal above for two reasons. First, it is *additive* (one more agent), which doubles down on the failure mode the long list and reframe argued against — more agents, more steps, more layers without measurement. Second, its diagnostic value is bounded by the lens whose bias it is auditing — same model, same training, the meta-lens is structurally vulnerable to the same self-preference. Compression plus eval-harness-with-grader-checks is honest about the bias rather than wrapping more lenses around it.

A weaker counter-proposal: *keep the three lens files; build only the eval harness.* This is the most operationally conservative move and might be the right one if the operator's gut says the lenses are pulling weight in ways the cheapest-experiment will not detect. The cost is keeping the surface area; the benefit is preserving prompt-level pressure between the lens files. If the cheapest experiment shows ablation breaks specific criteria, this becomes the decision the harness has earned.
