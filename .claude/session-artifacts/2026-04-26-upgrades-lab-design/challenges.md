# Challenges — upgrades lab design

Session: `2026-04-26-upgrades-lab-design`. Frame-challenger output. Hard precondition for the generator.

## Frame as given

The orchestrator frames the question as *total-rewrite-cost minimization via mature-from-day-one structure*: pay maximum upfront design cost across all eight dimensions so that future entries land in slots the structure already anticipates. Reversibility is acknowledged only as a sub-distinction inside the frame ("which commitments lock, which don't"); the dominant verb remains *design the mature endpoint*. Coherence with the existing stack is a secondary optimizer.

## Alternative frame

**The lab is not a structure-to-design; it is a content-corpus that already partially exists, and the question is where it lives.** Twelve initial entries (A–L) plus the seven-capability taxonomy plus deferred items in `plans/` plus the operator's running notebook in `pages/`/`logseq/` already constitute a prior-content corpus. Under this frame the verb is *retrofit a structure onto extant content*, not *design a mature endpoint and wait for content*. This frame matters because outside-view condition (2) — "designer has prior-content corpus being retrofitted" — is the single condition that historically lifts top-down lab designs above their base rate, and the operator's frame *forecloses* claiming it. The optimization target shifts from "minimize future rewrites" to "make the existing 12+ items legible and queryable in their current form, then let the structure deform around what they actually need." Same no-rewrite goal; different verb; different first move.

## Condition under which the current frame is wrong

If the ratio of meta-structure commits to substantive-content commits exceeds 3:1 by day 60 (outside-view's diagnostic for failure mode A), the frame has already failed — and the design that produced that ratio was wrong from the moment it specified eight dimensions instead of one.

## Challenges to scope-map preservations (one per `extend`, weakest hit hard)

The scope-map declared zero strict preservations but seven `extend` rows. Per CLAUDE.md and the orchestrator's instructions, each is challenged for axis-mismatch validity vs. rationalization.

- **#1 `body_completeness` enum**: stated reason — different axis (ingestion completeness of external work vs. epistemic maturity of internal idea). Challenge is weak-medium: the axis distinction is real, but extending implies the lab will *itself* coin a parallel enum, which doubles the vocabulary the operator must hold in working memory. **Bias: vocabulary proliferation, where every "different axis" gets its own bespoke enum instead of one well-named generic.** Pressure-test: could a single `state` enum with namespaced values (`canon:stub`, `lab:raw`) serve both?

- **#2 `stale` flag**: same axis-mismatch argument as #1. Same vocabulary-proliferation bias. The argument that lab needs `superseded_by` / `archived_at` rather than `stale` is sound on naming, but the *primitive* (a boolean-or-timestamp indicating "this is no longer the live version") is identical. Bias: treating naming differences as semantic differences.

- **#4 `tests/regression/`**: the axis-mismatch is real (executable-ish guardrails vs. research postmortem prose). Challenge: the scope-map invokes a "named link primitive between them" as the resolution, but adding a cross-archive link primitive is itself a new dimension the lab is committing to. **Bias: dimension creep disguised as preservation.**

- **#6 critic verdicts + `decision-log.md`**: stated reason — verdicts are workflow-internal, lab transitions are operator-written across time. Reasonable axis distinction. Bias: format-reuse-without-vocabulary-reuse means readers must learn two transition vocabularies; if the lab's transition vocabulary is poorly chosen (and there is no canonical anchor for it per librarian), the reuse-of-format-only is cosmetic.

- **#7 `## Revision N` pattern** *(weakest justification — challenged hard)*: the stated reason is that intra-document revisions cannot stretch to inter-document edges without destroying readability of superseded entries. **This is a strawman.** Nothing about adopting `## Revision N` for in-document accretion *prevents* a separate edge primitive; the scope-map presents the choice as binary when it is not. The real question is whether the lab needs `## Revision N` *at all*. Lab entries, unlike frame.md, are not iteratively rewritten by an orchestrator across a single session — they are written, matured, superseded. The append-don't-edit discipline is a *workflow* convention for live-document drafting; a maturing lab entry that is being edited 11 times across 11 separate review passes is, by outside-view's mode-A signal, a failed entry. **This row should be `subsume` or `replace`, not `extend`. The lab's transition vocabulary (raw → triaged → designed → integrated) replaces `## Revision N` for lab-entry purposes; `## Revision N` stays inside frame.md and the workflow, full stop. Preserving it for the lab biases toward treating lab entries as living drafts rather than as artifacts that mature and stabilize — exactly the failure mode (Mode A) outside-view flagged at 30–50%.**

- **#8 distillation confidence markers**: scope-mismatch argument (claim-level vs. doc-level) is genuine and well-argued. Lowest-risk extend in the set. Bias: minor — consistent vocabulary across scopes is a feature, not a flaw.

- **#9 agent frontmatter schema**: the schema is for agents and lab entries are documents, so it doesn't apply. This isn't an `extend`; it's a non-touch. The label is mostly a paperwork artifact. Bias: none.

- **#10 naming convention**: `extend` adds discipline/doc-type to the date-slug. Reasonable. Bias: assumes the discipline taxonomy is stable enough to live in the path — but the scope-map itself flags the seven-capability taxonomy as a `conflict` (#12, unresolved). **Encoding an unresolved taxonomy into pathnames is a rewrite trap.** This row is hostage to #12; if #12 resolves to a different shape, every lab path coined before resolution is wrong. Bias: locking-in-by-pathname before the underlying primitive is decided.

## Challenge to the classifier label

N/A — `requirement.md` is not on disk in this session; I cannot compare classifications. Flag for orchestrator: the absence of `requirement.md` is itself a workflow-step violation and should be addressed before generation. If the classifier output were available, the candidate label `new` would be challenged against the alternative `extend` (since the operator describes the lab as "fitting" an existing stack with twelve known initial entries — i.e., the work has the shape of extending the stack with a new module, not greenfielding a discipline).

## Cross-cutting frame challenges

**On "no compromises":** the operator's stance forecloses the only two conditions outside-view names as historically lifting top-down lab designs above their base rate — time-boxing (condition 5) and explicit reversibility pre-commitment (condition 4). Both are "compromises" only in the operator's framing; in the reference-class data, they are the *features* that make mature-from-day-one designs survive at all. Refusing them is not rigor — it is the inside-view tell that predicts 2–10× durability overestimation. The frame must be rewritten to treat time-boxing and reversibility as *load-bearing components of the no-rewrite goal*, not as concessions against it.

**On the lab as backlog vs. operating-knowledge-base:** scope-map row #13 labeled the stack philosophy `replace`. The replacement is presented as "workflow is for now-decisions, lab is for not-yet-decided ideas" — which describes a backlog. An alternative frame: every lab entry has *already been processed at some level* (raw observation, triaged hypothesis, replicated finding, integrated upgrade), and the entry's maturity rung *is* the artifact-landing the philosophy demands. Under this frame the lab does not *replace* the no-backlog rule; it is the artifact-discipline applied to slower-moving knowledge work. This is materially different from a backlog, and it is the frame that lets the operator honestly answer "no, I did not violate the philosophy." Worth surfacing because it changes what counts as a valid lab entry (must have a maturity rung from creation, not "to be triaged later").

**On the name `upgrades`:** the name connotes additive improvements to an existing system — it forecloses negative results, falsified hypotheses, and theoretical work that does not produce an upgrade. Per librarian inferred-5, naming is a load-bearing semantic primitive; misnaming actively misleads. Candidates grounded in the actual function: `lab/` (matches the operator's own R&D framing, no directional commitment), `inquiries/` (preserves the question-led shape and admits negative results), `r-and-d/` or `rd/` (explicit), `studies/` (each entry is a study at some maturity rung). `upgrades/` should be challenged on the grounds that 30–50% of failure-mode A material is *killed ideas*, and the directory name should not imply that killed ideas don't belong there.

**On self-referential evidence:** the operator added `scope-projector / maturity-extrapolator` (item K) mid-design — a capability that, by frame.md's own admission, would have changed this design's trajectory had it existed. This is direct evidence that the mature future state cannot be specified now: the design is being modified by reasoning that did not exist when the design started. The implication is not "abandon the design" but "treat the eight-dimension commitment surface as evidence that at least one capability the lab will need is currently unimaginable." That should reduce the locking-dimension count, not justify designing all eight at full fidelity.

## Frame-level objection the orchestrator must carry forward

**The frame commits to eight design dimensions when the only condition that historically saves top-down lab designs (condition 4: explicit reversibility pre-commitment) demands minimizing the locking-dimension count — the candidate must name which dimensions are genuinely locking (rewrite-forcing if changed) and design *only those* at full fidelity, leaving the rest reversible and explicitly so; failing to do this means the candidate is generating against an un-survived frame.**
