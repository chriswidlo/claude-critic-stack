# Critic — Architecture lens (revision 2)

## 1. Weakest structural link

The weakest structural link in revision 2 is **move 2 — the probe upgrade entry — left in a state where it documents the comparator-semantics inversion but does not require the comparator's protocol surface be amended before the probe runs.** The candidate states (W3) that the probe "asks the comparator's protocol surface be updated *before* the probe runs," but this is an aspiration in the candidate body, not a precondition baked into the upgrade entry's acceptance criteria. The architectural defect from v1 (feeding differing inputs to a comparator designed for identical inputs and reading agreement-class as inter-input correlation) is now *named* but not *gated*. If the upgrade entry is later picked up by someone who reads it as a runnable experiment without reading this candidate.md, the inversion runs unaddressed.

This is materially smaller than v1's weakest link (which was the self-checking-author defect at orchestrator candidate-authorship time). v2 does not introduce new self-checking authorship; it defers all such moves to upgrade entries that explicitly state the choice has not been made. The remaining structural risk is a documentation-coupling risk in a single upgrade entry, not a runtime-contract risk in CLAUDE.md.

## 2. Invariants at risk (not named in the candidate)

1. **Upgrade-entry-as-sketch vs. upgrade-entry-as-spec.** Memory says lab entries are allowed to be wrong and cleanup tasks must not edit entry bodies. v2 leans on this — three upgrade entries are authored as designed-but-not-chosen sketches. The invariant at risk: a future reader cannot tell from an upgrade entry's body whether it is a *sketch* or a *commitment*. v2 does not require entries to declare their own type. Break: the probe upgrade entry gets executed as if it were a spec, the inverted-semantics warning notwithstanding.

2. **Synthesis-as-decision vs. synthesis-as-diagnosis.** The 12-step workflow's step 12 is documented as "Synthesis" with a labeled "post-critique recommendation." v2's recommendation is "ship nothing structural; open three upgrade entries." This is a valid output, but the workflow's invariant — that synthesis ends with a decision the user can act on — is being reinterpreted to mean "a decision to defer." Break: a future ledger-render or audit tool counting "decisions made per session" cannot distinguish "deferred decision" from "no decision." v2 does not propose a synthesis-output type that names this.

3. **Three-upgrade-entries as a load-bearing-but-undeclared coupling.** Moves 2, 3, and 4 are each independent upgrade entries, but the candidate's logic *requires their conjunction*: the probe (move 2) feeds into the choice among the three primitives (move 3), and the footnote (move 4) is the documentation accuracy hedge that makes the deferral defensible. If any one of the three is not authored (or is authored and later deleted), the recommendation's structure collapses. v2 does not declare the cross-entry dependency. Break: someone deletes one entry per `feedback_lab_is_creative_hub` ("entries are allowed to be wrong"), and the synthesis citation in `synthesis.md` now points at a structure that no longer exists.

## 3. Coupling and direction

- **Coupling reduction (improvement over v1):** v1 introduced a back-edge from `decision-log.md` into the step-10 invocation contract, and a coupling reversal where CLAUDE.md's stable claim depended on a per-session env var. v2 drops both. CLAUDE.md is untouched except for an additive footnote (move 4); `decision-log.md` retains its current type. This is the right direction.
- **Coupling introduced (new in v2):** The three upgrade entries form an implicit DAG — probe → mechanism choice → footnote-revisit-if-needed — that is not represented anywhere structural. The dependency is in the candidate.md prose only.
- **Coupling avoided correctly:** v2 explicitly declines to introduce candidate-composition discipline as CLAUDE.md prose, citing the architecture lens's v1 critique. This is the correct read of the v1 objection. The architecture lens's preferred primitive (typed candidate) is named in move 3's upgrade entry rather than smuggled into prose.

## 4. Ignored architectural alternatives

1. **A "decision-deferred" artifact type, distinct from `synthesis.md`.** A `deferral.md` artifact alongside `synthesis.md` that explicitly declares "this session's output is N deferred decisions, each tracked in upgrade entry X" — making the deferral a typed object rather than prose inside synthesis.

2. **Probe-before-upgrade vs. upgrade-before-probe ordering.** Run the probe *in this session* as a retrospective read of existing shadow-comparator artifacts, if any. Collapses the probe from "future experiment requiring contract change" to "retrospective read of existing artifacts."

## 5. Frame-level objection

v2's frame is "diagnosis-first, defer all structural choices." This addresses my v1 frame objection directly: v2 no longer makes a claim change while pretending to make a contract change.

The residual frame objection is narrower: **v2 treats "open three upgrade entries" as a low-cost action, but the act of authoring three entries that each describe an unchosen architectural alternative produces a *menu* in `upgrades/profound/` that future sessions will read as a backlog.** Specifically, the typed-candidate / invariants-only / single-judge triple in move 3's upgrade entry forecloses a fourth option (e.g., "remove minority-veto and accept role-orthogonality as the only claim," which the panel aggregation [critiques.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/critiques.md) §"Routing" option (a) explicitly named). v2's move 3 enumerates three primitives and omits option (a) — the option of *removing the veto* rather than introducing an enforcement primitive. This is a frame-narrowing artifact disguised as a frame-preserving deferral.

The fix is small: move 3's upgrade entry should include "(d) remove minority-veto, accept role-orthogonality as the only claim" as a fourth designed-but-not-chosen alternative.

## 6. Verdict

**approve with residual objection.**

What would change the verdict to unconditional approve: move 3's upgrade entry includes the fourth alternative — *remove minority-veto, keep role-orthogonality as the panel's only claim* — as a designed-but-not-chosen option alongside the typed-candidate / invariants-only-feed / single-rubric-judge triple, so the deferred menu is not pre-narrowed.

Residual objection for synthesis to carry forward: the three-upgrade-entry deferral is structurally sound but creates an undeclared cross-entry dependency (probe → mechanism choice → footnote-revisit) and pre-narrows the mechanism menu by omitting option (a) from [critiques.md](.claude/session-artifacts/2026-05-09-critic-independence-vs-target-repo-read-access/critiques.md) §Routing; synthesis should name both before closing.
