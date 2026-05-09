# Critic — Operations lens (revision 2 re-review)

Prior verdict on revision 1: `rework`. Frame-level objection was "every move is prose-enforced on a stack whose existing prose-enforced contracts already operate on the honor system; before adding moves 2 or 3, name the detector." This re-review evaluates revision 2 against that objection and the v1 critique's specific exit criteria.

## 1. Most likely incident

At session-time T+N, a future orchestrator opens the candidate-shaping-probe upgrade entry intending to "just run the cheap probe" and authors a comparator-inverted shadow run against an undocumented baseline; symptom is a comparator agreement-class output that gets read as evidence and quoted in a downstream synthesis without the inversion warning carrying over. Root cause is that the upgrade entry is the only place the inversion is documented, and `upgrades/` entries are explicitly *allowed to be wrong* per `feedback_lab_is_creative_hub` memory — so the warning sits in a file the workflow does not require any future session to read before acting on it.

This is a real but narrow incident shape. It is materially smaller than v1's most-likely incident (a panel-wide silent default-allow drift on `$CRITIC_TARGET` opt-in logging), because v2 ships no runtime contract.

## 2. Blast radius

- **Per-incident:** one future session produces a measurement against an unstated baseline.
- **Cross-session amplification:** none from v2 itself. Footnote is additive prose; the three upgrade entries are inert until picked up. Categorical improvement over v1, where the new contract was global-by-default.
- **Trust radius:** smaller than v1. The footnote shifts a documented property; it does not retract a prior claim, so prior approves in the ledger are not retroactively recolored.

## 3. Rollout / rollback

- **Rollout strategy:** named and adequate. Move 1 (synthesis-only) ships immediately with no contract impact. Moves 2/3 (upgrade entries) ship as `upgrades/profound/` artifacts that the lab convention treats as *proposals*. Move 4 (footnote) is a single additive doc edit.
- **Rollback path:** `git revert` on move 4's footnote is a real rollback, not a forward-fix in disguise, because no session artifact downstream depends on the footnote's wording. v1's "rollback restores prose, not artifact state" objection — addressed.
- **Two-systems-running period:** **none.** v2 does not change the `critique-start` wording, does not change CLAUDE.md step 9, does not introduce a `$CRITIC_TARGET` per-lens table. There is no old-vs-new contract to straddle.

This section was the second-largest objection to v1. v2 collapses it cleanly.

## 4. Observability gap

- **Contract violation by a critic:** v2 introduces no new contract for a critic to violate. The existing situation is unchanged. v2's footnote *names* this situation accurately rather than obscuring it.
- **Decision-log opt-in becoming silent default-allow:** dropped. Schema collision and unenforced-discipline failure mode are both moot.
- **Candidate-composition discipline drift:** dropped. v2 explicitly declines the discipline note. The "no metric for paraphrased target content" gap remains, but v2 surfaces it as future work in the move-3 upgrade entry.
- **Metric to confirm "the thing went well":** the synthesis is the artifact this session produces; "well" means the synthesis names three diagnostic claims and three deferred follow-ups accurately. That is reviewable by reading the synthesis.

**Residual gap I want to name:** the move-4 footnote states "information independence between lenses is not enforced." After it lands, no detector exists for *future drift in the panel's claimed property*. If a future CLAUDE.md edit silently re-introduces "three independent critics" phrasing elsewhere in the doc, the footnote does not catch it. A grep-based linter on CLAUDE.md / README.md for the string "independent critic" with a require-co-located footnote rule would close this. Not blocking — additive doc accuracy with no behavior change is below the threshold where I demand a detector — but worth naming as residual.

## 5. Cost at failure

- **Steady-state cost when v2 holds:** approximately zero.
- **Failure-mode cost #1 — three upgrade entries are read as commitments rather than sketches.** Cost: a future session re-litigates a designed-but-not-chosen alternative. Tractable.
- **Failure-mode cost #2 — the probe in move 2's upgrade entry runs and produces a misleading signal.** Cost: one bad measurement in one upgrade entry. Bounded.
- **Failure-mode cost #3 — diagnosis-first reads as workflow theater.** Out of my lens.
- **Failure-mode cost #4 — the footnote is later contradicted by a different doc.** Cost: documentation accuracy degrades. Recoverable.
- **On-call load:** unchanged from baseline. v2 adds no recurring operator action.

## 6. Frame-level objection

I named v1's frame-level objection as: "the candidate frames this as a contract-design problem; the operational view is that it is an enforcement problem with no enforcement primitive proposed." v2 directly answers this by **not proposing a contract change.** I do not have a new frame-level objection against v2 from the operations lens.

If pressed for one: v2 frames "no contract change" as zero operational cost, but authoring three upgrade entries plus a footnote in one session is itself a session cost the ledger will reflect. This is a velocity concern, named by the candidate as W2, and is honestly out of my lens.

## 7. Verdict

**approve**

What would change the verdict back to rework: if move 2's upgrade entry were re-read by the orchestrator as a commitment to run the probe *this session* rather than as a deferred proposal, the v1 objection re-fires. As written, v2's text is unambiguous that the probe is deferred. The verdict holds as long as that deferral does not silently collapse during synthesis or step 13 ledger composition.
