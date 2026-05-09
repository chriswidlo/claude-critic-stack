# Synthesis

## Classifier label and alternative

Primary: **investigation** (`requirement-classifier`, [requirement.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/requirement.md)). Default frame: "what would we do differently if we knew how deep target-repo grounding already runs, and at what depth does it stop being independence-safe?"

Alternative classification flagged by the classifier: **extend** (becomes primary if the user commits to adding an information-isolation primitive) or **replace** (becomes primary if grounding is already de-facto load-bearing rather than optional). The frame-challenger ([challenges.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/challenges.md) §"Challenge to the classifier label") argued `replace` is the substantive alternative because Explore established critics already hold unconstrained Read access. **This synthesis lands as `investigation`** — diagnosis-first with deferred decisions — but flags the unresolved tension explicitly: if any of the three deferred decisions in moves 2–4 is taken up, the next session may be a `replace`, not an `extend`.

## Reframe (current revision)

[frame.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/frame.md) revision 1: the user framed the question along the *independence* axis. The reframe restates the question along three axes the user did not name:

- **Inter-lens, inter-model, inter-input** — three distinct "independence" concepts. The current stack addresses the first (role-orthogonality across architecture / operations / product) and the second (`SHADOW_PANEL=1` shadow comparator). It does not address the third.
- **Calibration vs. decorrelation** — grounding the critic in the target trades inter-input decorrelation for *external validity*. Without it, critics critique candidates abstractly; with it, they critique against deployable reality.
- **Frame question disguised as independence question** — a critic with target-repo access answers "is this candidate good *for that target*?" while a critic without answers "is this candidate sound *on its own terms*?" These are not noisy estimates of one quantity; they are different quantities. The frame-challenger sharpened this further: independence is the wrong organizing concept; **commensurability** is.

The reframe holds option (5) explicitly on the table: *accept that critics are grounded, drop the information-independence claim, re-justify the panel on role-orthogonality + shadow-comparator triangulation.*

## Reference-class forecast (from outside-view distillation)

From [distillations/outside-view.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/distillations/outside-view.md):

Primary class: **LLM-as-judge / model-graded evaluation systems** with grounding-vs-blinding as the controllable knob. Across LLM-as-judge, audit, peer review, red team, and code review (5 of 5), the dominant pattern is *the reviewer reads the artifact; independence is enforced by relational/structural separation, not informational starvation*. Base rate for "grounded reviewers produce better verdicts than ungrounded ones" is roughly 70–85% directionally; base rate for "information-isolation across reviewers improves panel discrimination" is low and mostly negative.

Contradicting class: **forensic blinding (Dror et al., linear sequential unmasking)** — context-blinding is the independence mechanism and has strong empirical support, *but only when the analyst's job is a narrow technical conformance check*. The frame test: if any lens's job is genuinely a narrow invariant check, blind it; if the lens's job is holistic judgment, ground it.

Position relative to base rate: **panel-wide information-isolation sits below base rate**, with a specific lift path requiring (a) a stated threat model, (b) a declared panel job, (c) per-lens isolation tied to narrow-vs-holistic.

## Canon passages

From [distillations/canon.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/distillations/canon.md). Coverage declared **partial** by the librarian.

**Supporting (independence threatened by shared input):**
- Anthropic, *How we built our multi-agent research system* (2025) — subagent context separation reduces path dependency.
- Anthropic, *Effective context engineering for AI agents* (2025) — context rot, attention budget, progressive disclosure as a middle-ground architecture.
- Anthropic, *Building effective agents* (2024) — parallelization for "multiple perspectives," not statistical independence.
- Wang et al., *Devil's Advocate* (Findings of EMNLP 2024, abstract-only) — independence by role/timing, not input isolation.

**Contradicting (grounding improves judgment):**
- Beyer et al., *Site Reliability Engineering* (2016) Ch. 32 — Production Readiness Review is *defined by* target grounding.
- *SRE* Ch. 36 — independence achieved by reviewer-team identity, not input deprivation.
- *SRE* Ch. 15 — postmortem fairness from frame discipline, not context-withholding.
- Anthropic multi-agent (2025) §Evaluation — production preference for a *single* well-prompted judge with a clear rubric over a multi-judge panel.
- Anthropic multi-agent (2025) §Lessons learned — shared-context tasks are flagged as a poor fit for multi-agent decomposition.

## Scope-map summary

[scope-map.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/scope-map.md) labeled 7 of 8 enumerated primitives as `extend` and 1 as `replace` (the conditional pass-through clause in `critique-start` lines 38–42). No primitive in the enumerated set was in technical conflict with the new requirement.

**Unresolved frame-level conflicts the scope-mapper flagged for the generator:**
- Panel-wide information-isolation regime vs. existing role-orthogonality independence claim. Choice between (a) per-lens job declaration (extend) and (b) re-justification (replace) was not pre-decided.
- Forensic-blinding reference class vs. LLM-as-judge reference class. Outside-view named `critic-operations` as the only plausible isolation candidate; canon §6 (PRR) directly contradicts that — operations-readiness review is *defined by* grounding.

## Frame-level challenge and how the final recommendation addresses it

[challenges.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/challenges.md) frame-level objection: *independence is the wrong organizing concept; commensurability is. The dominant correlation source is `candidate.md` upstream of every panel mechanism, and option (5) (drop the information-independence claim, re-justify the panel) may be the only honest position rather than the uncomfortable alternative.*

How the final recommendation addresses it:
- The panel's actual property is named accurately in user-facing docs (move 4 footnote): *role-decorrelated on shared input, optional inter-model triangulation under `SHADOW_PANEL=1`. Information independence between lenses is not enforced.* This adopts option (5)'s diagnostic claim without retracting the existing handle.
- The dominant correlation source (candidate.md authorship) is named explicitly in the diagnostic claims and is the subject of the deferred probe (move 2 upgrade entry).
- The commensurability concern (typed verdicts: grounded "reject" vs. ungrounded "reject" are about different worlds) is preserved as a residual question carried into the mechanism-design upgrade entry, where one of the four designed-but-not-chosen alternatives is *remove minority-veto, accept role-orthogonality as the only claim* (added per architecture v2 residual objection).

## Post-critique recommendation

**The recommendation is diagnostic, not structural.** Three diagnostic claims, four follow-up artifacts (probe + mechanism-design + footnote + the synthesis itself), and explicit non-decisions on three actions revision 1 attempted.

### Diagnostic claims

1. **No "introduction" of critic target-repo read access is occurring.** Critics already hold unconstrained `Read`, `WebFetch`, `WebSearch` ([distillations/explore.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/distillations/explore.md) §1–11). The thing being formalized in `critique-prep` / `critique-start` is *routing*, not access. Influence on the panel today is shallow but unmeasured: no observed session has exercised critic target-repo access; the dominant correlation source is `candidate.md` authorship by the orchestrator after Explore.

2. **The independence claim was never information-independence.** The stack has *role-orthogonality* on shared input (architecture / operations / product prompts) and *optional inter-model triangulation* under `SHADOW_PANEL=1`. Reading "three independent critics" as "three lenses with separate informational priors" was always inference, not contract.

3. **A panel-wide contract change is premature.** Outside-view places panel-wide isolation below base rate. Canon contradicts itself across PRR-style grounding and Anthropic multi-agent context separation. The dominant correlation source (candidate.md framing) is upstream of any panel mechanism, so any new isolation primitive operates downstream of the binding constraint until that source is measured.

### Follow-up artifacts (deferred decisions, explicitly named)

- **Probe upgrade entry (deferred decision A).** A `profound` lab entry describing the candidate-shaping probe — paraphrased candidate vs. original under `SHADOW_PANEL=1`, single session, comparator agreement class read as inter-input correlation signal. The architecture lens's protocol-surface objection is documented in the entry: feeding differing inputs to a comparator designed for identical inputs *inverts its semantics* and the comparator's protocol surface must be amended before the probe runs.
- **Mechanism-design upgrade entry (deferred decision B).** A `profound` lab entry documenting **four** designed-but-not-chosen architectural alternatives:
  1. **Typed candidate** — one `candidate.md` per lens at step 9, composed against that lens's allowed input set.
  2. **Invariants-only feed to a designated narrow lens** — schema-constrained `target-invariants.md` to one lens (operations, most plausibly), narrative to others.
  3. **Single rubric judge with shadow triangulation** — collapse the panel to one well-prompted judge per Anthropic multi-agent §Evaluation.
  4. **Remove minority-veto, accept role-orthogonality as the only claim** — keep the lens triple as three independent reports, drop the aggregation rule. Added per architecture v2 residual objection so the deferred menu is not pre-narrowed.
- **Footnote upgrade entry (deferred decision C).** A `no-brainer` lab entry adding one paragraph to [README.md](README.md) and a footnote to [CLAUDE.md](CLAUDE.md) §"Default behavior" naming the panel's actual property. Additive, easy to revert.

### Non-decisions explicitly named

- Do not edit `critique-start` lines 38–42 in this session. The "if they verify facts" wording stays until either the probe runs or someone authors an enforcement primitive.
- Do not introduce candidate-composition discipline as CLAUDE.md prose. Architecture correctly identified this reproduces the same self-checking-author defect class.
- Do not retract the "three independent critics" framing in CLAUDE.md or README. The footnote (deferred decision C) accomplishes the accuracy goal without round-trip risk.

### Carry-forward objections from the panel

- Architecture residual: the four-alternative menu in deferred decision B was *added in this synthesis* per the v2 residual objection; the upgrade entry must include all four when authored, not the original three.
- Product residual: this synthesis names the deferral as a deferral and surfaces the cheapest experiment (probe) as the path back to the user's original decision space. If a future reader reads the diagnostic claims as a closed answer, the workflow-theater failure mode (W1 in candidate.md) fires and revision 2 collapses into product failure.
- Operations residual: a grep-based linter on CLAUDE.md / README.md for the string "independent critic" with a require-co-located footnote rule would catch future drift. Not blocking, named for the lab.

## Three named uncertainties

1. **The probe is informative at N=1.** Architecture v2 §1 flagged that one shadow session of paraphrased-vs-original candidate may not generalize. If the probe needs to be a multi-session protocol, "cheap experiment" framing collapses and decision A becomes a different shape.
2. **Three upgrade entries is the right granularity for deferred work.** Lab entries are allowed to be wrong (per memory `feedback_lab_is_creative_hub`), but if a future reader reads them as commitments rather than sketches, the deferred-decision posture collapses.
3. **Aspect-orthogonality is a real source of decorrelation on a shared input.** This is the unmeasured premise underneath the smaller independence claim in the footnote. If three Opus lenses on the same candidate produce one voice in three accents, the panel is theatrical at best and minority-veto is the wrong rule. Diagnostic claim 2 cites this assumption without testing it.

## Cheapest experiment that would reduce the biggest uncertainty

**The candidate-shaping probe (deferred decision A) is the cheapest experiment that would reduce uncertainty 3 (and also touches uncertainty 1).** Run one session under `SHADOW_PANEL=1` where one shadow lens receives the original `candidate.md` and the other receives a paraphrased version stripped of target-repo references. Read the comparator's `agree | partial-agree | disagree` outputs as a signal of inter-input correlation:
- If agree on all three lenses: candidate-shaping is not the dominant correlation source; aspect-orthogonality is durable; the smaller independence claim in the footnote holds; **diagnostic claims 1–3 are confirmed** and decision B's mechanism choice is not urgent.
- If divergence on any lens: candidate-shaping is a real correlation source; the mechanism upgrade entry's four alternatives become the next session's frame; decision B becomes urgent.

**Pre-condition (not optional):** the comparator's protocol surface in [`.claude/agents/critic-comparator.md`](.claude/agents/critic-comparator.md) must be amended *before* the probe runs to document that "agree" under differing inputs means "candidate paraphrasing did not change the verdict," not "the lenses agree on the candidate." Without this amendment, the probe runs against an undocumented baseline and produces an uninterpretable result. This is the architecture lens's standing objection from both v1 and v2.

---

Ledger: agent-calls=15, artifacts=21, loops=2/2; warnings: loop-cap-reached.
