# Candidate recommendation — Revision 2

## Position

**Reject in-workflow Context7 adoption in this repo. Document the rejection. Recommend the user install Context7 globally for ad-hoc code work in *other* directories.**

Concretely:
1. **Do not install Context7 MCP in this repo.** No entry in `settings.json`. No Skill. The cwd remains, per CLAUDE.md, "deliberately not a target codebase."
2. **Write `.claude/decisions/0001-no-vendor-tier.md`** — one page, dated 2026-04-26. States: this stack runs a closed-world trust model (curated canon + outside-view's bounded WebSearch). Vendor-live retrieval is not admitted. Names the conditions under which the decision should be revisited (the falsifiers below). Future contributors must overturn this explicitly to introduce any vendor-tier integration; the artifact is the gate, not a policy framework — it speaks to one decision.
3. **Globally** (outside this repo, in the user's general Claude Code config or in repos where they actually write code): install Context7 normally, with the auto-invoke rule from the original briefing. That is where the value lives.

## Why this shape, not the spike (shape α)

Both rejection (β) and time-boxed spike (α) were on the table after the panel. Spike-and-see is the more capability-friendly answer; rejection is the more discipline-friendly. The reasons rejection wins:

- **Architecture lens flagged retrieval-reproducibility as a stack-wide invariant.** A spike's subagent return is persisted to `distillations/library-docs.md` and cited downstream by the synthesis. Vendor-tier passages are unreplayable. Even a one-week spike pollutes the audit trail of every session it runs against. The spike is not as cheap as it looks because the artifact graph has no concept of "ignore this branch's outputs."
- **Outside-view base rate verdict was "below base rate for shapes C and E."** The spike is shape C with a kill criterion. Running a below-base-rate intervention to gather n=3 evidence is bad inference: the spike's failure to fire on three questions is not evidence the tool is unhelpful; the spike's firing once is not evidence it is. Three points against a categorical prior do not move the prior.
- **Product critic offered (a) or (b); the canon-librarian distillation tilted toward (b).** Anthropic's "Building effective agents" C1 ("simplest solution possible, only increase complexity when needed") and the corpus's silence on Skills-as-integration both lean toward not introducing the capability rather than introducing it provisionally.
- **The user's "upgrade" framing referred to global AI usage**, which the briefing addressed (the original answer told them how to install and use Context7). Adopting it *into the critic-stack repo specifically* is the question this workflow ran on, and the workflow's discipline says no. The "upgrade" is real and ships — just not in this directory.

## Frame-level objections — how this addresses them

- **Architecture (closed-world vs open-world):** Answered explicitly. The decision artifact commits the stack to closed-world. Not a deferral, not provisional. Revisitable, but the burden is on the next person to overturn.
- **Operations (no instruments to detect failure):** Avoided by not creating the failure surface. No vendor tool installed = no quota cliff, no leak detection needed, no rollback procedure required.
- **Product (don't quarantine-plus-paperwork; pick one coherent answer):** Picked. The single artifact is a one-page decision, not a policy framework. The Skill is not installed. The user is not asked to log questions. The repo behaves identically to yesterday.

## Named tradeoffs

1. **Cost of the false-negative.** If 25%+ of future design questions actually do bottleneck on current library-API specifics (the falsifier), the rejection costs us those answers. Mitigation: the decision artifact names the falsifier and the revisit trigger.
2. **The "upgrade" framing is partially refused.** The user said "add it as an upgrade" and the in-workflow answer is no. This is honest discipline-preservation; it is also a refusal. Mitigation: the global-install recommendation gives them the actual value where it actually applies.
3. **One more decision artifact to maintain.** `decisions/0001-no-vendor-tier.md` exists and must stay coherent with CLAUDE.md and `canon/sources.yaml`. Cost: one file, ~30 lines, one revisit trigger.
4. **Architecturally cheap, intellectually expensive.** Saying no requires defending the no for every future similar proposal (Linear MCP, Sentry MCP, etc.). The decision artifact is the defense, but it gets reread.
5. **No empirical evidence is gathered about whether Context7 *would* have helped.** The spike (α) at least produces n=3 data; rejection (β) produces zero. We are choosing prior over evidence, on the grounds that n=3 is not evidence anyway.

## Named assumptions (≥3, flipping the recommendation)

1. **The base-rate evidence from outside-view holds: shapes C/E are below base rate, A is the base rate.** *If wrong* — if a real reference class would actually rate vendor-doc retrieval in evaluative agent stacks above base — rejection is overcautious and the spike (α) becomes correct.
2. **Closed-world trust model is what makes this stack valuable.** *If wrong* — if the stack's value is the workflow shape (12 steps, distillation, critic-panel) and the trust model is incidental — then admitting a vendor tier costs nothing meaningful and rejection is rule-following without a reason.
3. **The user's actual code work happens in other directories, not this one.** *If wrong* — they routinely switch to writing implementation code in `claude-critic-stack/` itself — the global-install recommendation is unhelpful and the Skill (E) is the right answer.
4. **The artifact graph (session-artifacts, distillations) treats a one-week spike as permanent pollution.** *If wrong* — there is a way to scope or quarantine a branch's artifacts that the architecture lens missed — the spike's downside shrinks and α becomes more attractive.
5. **Future contributors will respect a `decisions/0001-no-vendor-tier.md` gate.** *If wrong* — the artifact is read once, ignored, and someone installs Context7 anyway — rejection has no enforcement and the right move was to spike-and-document rather than refuse-and-trust.

## Named ways this could be wrong

1. **The rejection may be the easy answer dressed as discipline.** Saying no costs nothing today and externalizes the work onto the future contributor who challenges it. That asymmetry — costless no, costly yes — is a known failure mode of opinionated systems. The candidate may be exhibiting it.
2. **The closed-world commitment may not survive the first really-library-specific design question.** If next month a question genuinely requires vendor-current information to answer, the user will install Context7 in a hurry and the decision artifact will read as embarrassing rather than principled.
3. **"Install it globally" assumes the user has a global Claude Code config they use for code work.** If their workflow is repo-by-repo, the global-install recommendation is hand-waving.
4. **Picking β over α because "n=3 is not evidence" is a sophistical move.** It is true, but it conveniently lets us avoid ever gathering evidence. The spike's value is not statistical — it is that running the candidate exposes failure modes the workflow could not predict. Refusing to spike on inference grounds may be refusing to learn.
5. **The artifact `decisions/0001-no-vendor-tier.md` may itself become the "policy framework" the product critic warned against.** A decision file numbered `0001` strongly implies `0002` and `0003`. The candidate creates the precedent it claimed to avoid.
