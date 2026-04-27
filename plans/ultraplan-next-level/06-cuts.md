# 06 — Cuts

Every long-list item not on the shortlist, with a one-sentence reason for cutting. The shortlist (S1–S6) absorbed several long-list items; those absorptions are noted rather than cut.

## Absorbed (not cut)

- **#1 Decision-record-as-substrate** — into S1.
- **#2 Calibration revisit agent** — into S1.
- **#3 Critic-panel collapse** — into S2.
- **#5 Eval harness** — into S3.
- **#6 Promote-session-to-eval** — into S3.
- **#7 Inverted librarian** — into S4.
- **#8 Corpus-coverage map** — into S4.
- **#10 Pre-mortem mode** — into S6 (sole inhabitant).
- **#14 Retire requirement-classifier** — into S5.
- **#15 Hard-gate residual-disagreement contract** — into S1 (the gate is part of the substrate work).
- **#21 Ablation harness** — into S2 (gives the removal its evidence base).

## Genuinely cut

- **#4 Structured agent return contracts.** Cut for sequencing reasons, not principle: this is the right next move *after* S1+S3 land — once there is a calibration substrate and an eval harness, the case for tightening agent return contracts becomes empirical rather than aesthetic. Moving it ahead of those two would be a bet that the contract-shape is right *a priori*, which I cannot defend without the evidence S3 will produce.

- **#9 Operator-bias profile.** Cut as too-early. Without S1's calibration record, there is no reliable signal about an operator's *characteristic* failure modes, only operator self-report — which is exactly the data Tetlock-tradition forecasting evidence shows is least reliable. Revisit after S1 has produced two quarters of revisit data.

- **#11 Adversarial-debate variant of the critic panel.** Cut because it is *competing* with S2, not complementary, and S2 is cheaper. The Khan et al. (2024) evidence is suggestive but not yet decisive at the workflow scale the stack operates in (real design questions, not benchmark truthfulness). If S3's eval harness later shows S2 underperforming on a class of questions, this becomes the natural follow-up; running it before S3 means having no way to tell whether it actually wins.

- **#12 Cross-session retrieval.** Cut because it is the textbook case of *capability before measurement*: it adds a tempting affordance whose value cannot be evaluated without the calibration signal S1 produces. Revisit only after S1 + S3 have produced a well-typed substrate to retrieve over.

- **#13 Frame-versioning across artifacts.** Cut as small / cosmetic. Worth doing as part of S1's structured-record work (it falls out almost free if `decision.yaml` exists), but does not earn shortlist status on its own.

- **#16 Decision/recommendation tier.** Cut as premature. The Bezos *one-way-door* framing is right, but the mechanism — "do less for reversible decisions" — requires a calibrated sense of *what the workflow currently spends on each kind*, which S3 produces. Cuts cleanly into the post-S3 backlog.

- **#17 Outside-view memory (reference-classes library).** Cut as marginal. The [outside-view](../../.claude/agents/outside-view.md) agent re-derives base rates per session, which is wasteful but also keeps base rates from ossifying. The library would save tokens and lose freshness; net value is unclear. Worth a small spike post-S1, not shortlist-worthy.

- **#18 Synthesis-as-ADR export.** Cut as a feature for a use case (team-shared design records) that is not the stack's current configuration. If the stack's user base broadens to include teams, this jumps to shortlist; today it is solving a problem the operator does not have.

- **#19 Cost / latency budget as a workflow constraint.** Cut as solving a problem nobody has yet named as painful. The full 12-step is slow, but the operator chose that cost knowingly. If S3's eval harness later shows that some steps consume disproportionate budget for marginal value, this becomes the natural next move.

- **#20 Self-application of the five pressures.** Cut as the kind of meta-exercise that produces a good document once and then never gets re-run because the trigger is calendrical, not event-driven. Likely better delivered as an *occasional* operator-initiated session, not as a primitive.

## Notes on the cuts as a set

Most cuts are **deferral**, not rejection. The shortlist is shaped to *unlock* most of these items: once S1+S3 are in place, #4, #9, #12, #16, #17, #19 all become defensible to evaluate empirically. The cut list is not a graveyard; it is the post-shortlist backlog ordered implicitly by "what evidence S1 / S2 / S3 produce will tell us which to take next."

Three cuts are sharper. **#11 (adversarial-debate)** competes with the shortlist's S2, and only one of the two should be run; my reading of the evidence (Khan et al. 2024 at benchmark scale, no real evidence at workflow scale) is that compression now and revisit later is the better bet. **#18 (ADR export)** is a feature for a different stack — the team-shared variant — that I do not believe the operator is building toward in the next six months; if they are, push back. **#20 (self-application of five pressures)** is the cut I am least confident about — it might be the highest-leverage *cheapest* move in the entire long list, since it costs almost nothing and could surface frame-level errors that none of the others touch. I left it cut because it is naturally an operator-initiated session under the current stack; if the operator disagrees, promoting it is one paragraph of work.

If a reviewer wants to argue with the cuts file, the productive arguments are: (a) "you cut #11 prematurely; debate beats compression on the question class I actually care about" — which I cannot refute without S3; (b) "you cut #20 because it is convenient, not because it is wrong" — which is partly true; (c) "your shortlist is over-weighted on measurement and under-weighted on capability, and #4 should not have been deferred" — which is the strongest critique and the one I take most seriously.
