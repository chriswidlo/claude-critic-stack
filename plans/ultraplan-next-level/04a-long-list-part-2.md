# 04a — Long list (part 2 of 2)

Continued from [04-long-list.md](04-long-list.md).

## 12. Cross-session retrieval

A small retrieval primitive over `.claude/session-artifacts/*/` such that a new question can surface relevantly-similar past sessions. The risk (named in the reframe, §03) is that this is a tempting addition that produces noise unless coupled to a calibration signal — *which* past sessions are valuable? Without #2 (calibration revisit), this vector probably should not ship. Listed for completeness so the cuts file can argue the case. (Operational.)

## 13. Frame-versioning across artifacts

Today, [frame.md](../../.claude/session-artifacts/2026-04-26-context7-adoption-in-critic-stack/frame.md) accumulates `## Revision N` blocks but downstream artifacts do not declare which revision they were produced under. Add a `frame_revision: N` header to each artifact. Enables a `frame-history` view: which artifacts survived a frame change, which got rewritten. Cheap, mostly cosmetic; useful if combined with #4 (structured returns). (Structural.)

## 14. Retire the requirement-classifier

The classifier produces a label and a frame bias; the reframe step (step 2, performed by the orchestrator) can do both jobs without a separate agent. Removing the agent saves a hop and tightens the reframe's accountability — the orchestrator owns both label and frame. Risk: losing the explicit `## User's framing words` capture, which is genuinely useful in the [ark-mono regression](../../tests/regression/ark-mono-connector-routing.md). Solution: fold that section into the reframe artifact. (Structural; removal candidate alongside #3.)

## 15. Hard-gate the residual-disagreement contract

The replan loop today is capped at 2 with a prose escalation ("name the residual disagreements"). Promote this to a hard gate: synthesis refuses to run if `decision-log.md` contains an unresolved `residual_disagreement:` block and no `synthesis_addressed: true` field. This is the *one* visible silent-failure mode I observed in actual artifacts. Cheap fix. (Structural.)

## 16. Decision/recommendation tier

Most decisions are not equal. A two-line `tier:` field on each decision-record (e.g. `reversible | hard-to-reverse | one-way-door`, after Bezos' framing) lets the workflow do less for reversible decisions and more for one-way doors. Today the workflow does the same amount for everything. (Interfacial.)

## 17. Outside-view memory

Today the [outside-view](../../.claude/agents/outside-view.md) re-derives the reference class on every invocation. A small `reference-classes/` library (one file per class with name, base rate, source, notes) lets the agent retrieve and refine instead of re-deriving. Builds slowly. Has obvious failure mode: stale base rates ossify into received wisdom. Mitigation: every retrieval includes the date the base rate was last verified, and stale ones force re-derivation. (Structural.)

## 18. Synthesis-as-ADR export

The synthesis (step 12) is currently a chat-shaped wall of structured prose. Add an export mode that emits the synthesis as a Nygard-shaped ADR (context, decision, status, consequences) suitable for paste into the *target* repo's ADR directory. The stack thereby produces an artifact the operator's *team* can review, not just the operator. (Interfacial.)

## 19. Cost / latency budget as a workflow constraint

Each workflow run today has no declared cost ceiling. Add an optional `--budget` parameter (token, time, or both) and let the orchestrator skip the most expensive optional steps (Explore, the third lens, the full distillation pass) when over budget. Cheap; addresses the operational reality that the full 12-step takes real wall-clock time. (Operational.)

## 20. Self-application of the five pressures

The stack has [prompts/five-pressures.md](../../prompts/five-pressures.md) — a checklist applied to recommendations the stack *produces*. Apply the same checklist to *the stack itself*, periodically. *Reframe-before-answer* (does the workflow's framing of "design question" exclude valid kinds of question?), *enumerate-before-select* (have we enumerated alternative workflow shapes?), *outside-view-first* (what is the base rate of agentic-tooling projects that drift into ceremony?), *name-your-uncertainty* (what do we not know about the stack's actual usefulness?), *consequence-imagine* (what does it look like when the stack succeeds vs. fails over five years?). A meta-review entry, scheduled once a quarter. (Operational.)

## 21. Ablation harness for the stack itself

Coupled with #5 (eval harness): an ablation mode that can disable any single step or any single agent and re-run the eval suite. Tells you which agents/steps actually pull weight. The most likely outcome is that 2–3 steps do the heavy lifting and the rest could be removed without measurable loss. Without this, the stack can only grow; with it, the stack can defensibly shrink. (Operational; fuses with #3 + #14 as the empirical basis for any removal.)

## Commentary on the shape of this list

**Over-represented:** *measurement-and-loop-closing* vectors (1, 2, 5, 6, 17, 20, 21). This is partly because the reframe in [03-reframe.md](03-reframe.md) biases me there, and partly because the underlying observation — the stack has no calibration record — is genuinely the largest gap. A reviewer who rejects the reframe should expect to also discount these vectors proportionally.

**Under-represented:** *interfacial / human-experience* vectors (only 9, 16, 18). The stack is currently a one-operator tool used in a terminal; multi-user, team-shared, async-async workflows are barely touched here. If the stack's actual user base over the next 12 months will include teammates, this whole axis is undervalued in the long list and the reviewer should push back.

**Conspicuously absent:** *security and adversarial-input* vectors. Nothing here addresses what happens when the *user input* is itself adversarial — prompt injection in pasted-in design questions, malicious canon entries, model-organism behaviour. The omission is honest (I do not have a strong proposal here) but worth flagging as a blind spot.

**Conspicuously absent #2:** *non-architecture decisions*. The stack is shaped for software-architecture decisions; design questions in product, hiring, policy, capital allocation are real and could plausibly use the same machinery. Not a single vector here proposes generalising the stack outside software. That is either correct (stay focused) or a missed opportunity (the discipline transfers); I have not formed a confident view.

**Suspected blind spot:** I have over-indexed on *the stack as it is*, and may be missing vectors that come from *what users want from a critic-stack* but the stack does not currently provide. The clearest evidence I have for this blind spot is that none of the vectors above came from a user complaint — they came from reading the repo. A serious operator should run §11 (cheapest experiment) precisely to surface what is missing from this list.

These twenty-one go forward to the shortlist ([05](05-shortlist.md)) and the cuts file ([06](06-cuts.md)).
