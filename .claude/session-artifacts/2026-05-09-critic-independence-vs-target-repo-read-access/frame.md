# Frame

## Revision 1

### User's framing (restated)
"Letting critics read the target repo threatens their *independence*. We should diagnose how deep this influence already goes, and decide whether to preserve, restrict, isolate, or formalize the access."

### What the user is implicitly optimizing for
**Inter-lens decorrelation under a fixed set of priors.** The panel's job is to surface correlated error — three lenses converging on the same blind spot. The user is treating "shared exposure to target-repo content" as a new source of correlation between lenses, on top of the model-family correlation that the shadow comparator already addresses.

### One alternative optimization the user did not name
**Calibration of the panel against deployable reality.** A critic that has not read the target repo is forced to critique the candidate *in the abstract*. It will reject things that are infeasible *and* things that are merely unfamiliar; it will approve things that are elegant *and* things that contradict load-bearing constraints in the deployed system. Grounding the critic in the target repo trades some inter-lens decorrelation for *external validity* — the verdict, whatever it is, is at least about the right problem. Under this optimization, "no grounding" is the failure mode, not the safe default.

### A second alternative the user did not name
**This is a frame question disguised as an independence question.**

- A critic with target-repo access is answering: "*is this candidate a good move for this specific target?*" — judgment with priors.
- A critic without target-repo access is answering: "*is this candidate sound on its own terms?*" — judgment without priors.

These are two different jobs. The current stack does not state which job the panel is supposed to do. "Independence" only has a meaning *relative to a job*: the right question is not "how independent is the panel" but "what does each lens's verdict actually claim?"

If the answer is "lens A judges the candidate against the target, lens B judges it abstractly, and lens C is a coin flip depending on whether step 5 ran," then the panel's outputs are not commensurable — and adding more isolation will not fix that.

### Where the classifier's frame bias bites
Classifier flagged investigation as research-theater-prone. The user pre-enumerated four solutions (preserve, restrict, isolate, formalize). The frame must hold space for a fifth that the user did not list:

> **Accept that critics are grounded, drop the independence-of-information claim, and re-justify the panel on a different basis** — e.g., role-orthogonality (architecture vs. operations vs. product asks structurally different questions, so they decorrelate even on shared inputs) plus shadow-comparator triangulation (cross-model decorrelation on identical inputs).

This option is uncomfortable because it admits the current stack does not actually enforce information independence. The frame must not let comfort eliminate it.

### Hard questions the answer must address
1. **What is the threat model?** Without one, every recommendation is a guess. Candidates: (a) correlated lens approval driven by shared exposure to target-repo narrative; (b) sycophancy to existing code; (c) author-influence (target-repo's docs framing the critic's priors); (d) inability to detect designs that contradict deployed constraints.
2. **Is grounding currently load-bearing or optional?** Step 5 (`Explore`) is conditional. The `critique-prep` / `critique-start` skills route a target path forward. If the path leaks into critic prompts (directly or via inputs.md / question.md), grounding is *de facto* mandatory and "introducing the option" is a misnomer.
3. **What does each lens's verdict actually mean today?** If three lenses see different amounts of target-repo context, their verdicts are not the same kind of object — and the minority-veto rule is averaging incommensurable judgments.
4. **What does the existing shadow-comparator already buy us?** The comparator decorrelates on *model family* given identical inputs. It does not decorrelate on *inputs*. That distinction matters for this question and is not yet stated in CLAUDE.md.

### What this frame forbids the generator from doing
- Producing a diagnosis-only deliverable. Step 9 must commit to a decision rule, even if the rule is "do nothing, here's why."
- Treating the user's four-option menu as exhaustive.
- Treating "independence" as a single concept. There are at least three: inter-lens, inter-model, inter-input.
- Recommending more isolation without first naming what kind of independence it would add and at what calibration cost.
