# 11 — The cheapest single thing the operator should do this week

## The move

Run the **S1 cheapest experiment**: hand-author a `decision.yaml` for the next three real workflow sessions, then revisit one of them on day 21 and answer four questions.

This is the single most informative experiment on the entire shortlist because it resolves [U1](10-uncertainties.md) — which is the largest uncertainty in the plan, and the spine of the foundational reframe in [03-reframe.md](03-reframe.md). It is also the cheapest, requiring no agent edits, no `CLAUDE.md` changes, no schema commitment, no new directory structure beyond a file written next to the existing session-artifacts.

## Mechanism, in detail

For the next three real workflow sessions:

1. Run the workflow normally — no changes, no skipping.
2. After step 12 (synthesis), spend ~20–30 minutes hand-writing a small YAML file at `.claude/session-artifacts/<session-id>/decision.yaml` with the following draft schema:

```yaml
id: <session-id>
question: <one paragraph>
classifier_label: <copy from requirement.md>
final_frame: <copy from frame.md latest revision>
recommended_path: <one paragraph>
rejected_alternatives:
  - alt: <one line>
    why_rejected: <one line>
named_uncertainties:
  - <one line>
  - <one line>
  - <one line>
kill_criteria:
  - <one line>
residual_disagreements: []   # populate from decision-log.md if cap-of-2 was hit
predicted_outcome:
  by_when: <date>
  observable_signal: <one line — what would tell us this worked?>
```

Three things to notice in the draft schema. First, `predicted_outcome` is the field most decision-records leave out and most calibration work depends on; if writing it feels uncomfortably speculative, that is a feature — that is the calibration signal showing up before there is calibration. Second, `residual_disagreements` should be populated with whatever `decision-log.md` actually says was unresolved at the cap; if it is empty for all three sessions, the gate work in S1 is solving a problem the operator does not have at this scale. Third, no field above is final — this experiment is partly *to find out which fields are missing* (uncertainty 3 in [10-uncertainties.md](10-uncertainties.md)).

After writing each `decision.yaml`, write one line in a personal scratch file: *"how long did that take?"* and *"what did I almost want to add but didn't have a field for?"*

## On day 21

Pick one of the three sessions — ideally the one whose `predicted_outcome.by_when` is closest to today, or, if all are far in the future, the one whose recommendation most actively drove operator behaviour. Re-read the `decision.yaml`. Spend ~30 minutes answering, in writing:

1. **Was the framing right?** Does the `final_frame` field still describe the question the way you would now? If not — what shifted, and was it because the world shifted or because the framing was wrong from the start?
2. **Was the recommended path taken?** Did you actually do what the synthesis recommended? If not, why not? If yes, what part of it most needed adjustment in execution?
3. **Did the predicted outcome materialise?** Specifically against `predicted_outcome.observable_signal` — did that signal appear, fail to appear, or remain ambiguous?
4. **Were any of the named uncertainties actually the live one?** Or did the recommendation fail (or succeed) for a reason that none of the three uncertainties had named?

## What this experiment will tell you

- Whether the by-hand authoring is sustainable (~30 min per session is the threshold I'd consider sustainable; ~60+ minutes is not).
- Whether the structured form *adds* value to your retrospective reading or merely re-states what the synthesis already said.
- Whether the schema fields are roughly right, or whether something obvious is missing.
- Whether the residual-disagreements field is empty in practice (in which case the hard-gate part of S1 is overkill) or routinely populated (in which case it is essential).
- Whether prediction-as-of-decision is a discipline the operator can actually sustain, or whether the future is too murky to commit to in writing.

## What it will *not* tell you

- Whether an *agent* can produce the `decision.yaml` as well as the operator can. That is the second experiment, after the schema is settled.
- Whether the calibration revisits, done at a 30/90 day cadence with multiple sessions in flight at once, are operationally sustainable. That requires multiple weeks of accumulated data.
- Whether the hard gate at step 12 is well-designed; that requires the gate to actually exist.

## Why this and not S3's cheapest experiment

The S3 experiment is also small (~3 hours) and would also produce useful data. I chose S1's experiment for the operator's first move for three reasons. First, S1 is the foundational reframe and S3 is operational; if the reframe is wrong, S3 is built on the wrong foundation and the time spent on it is partially wasted. Second, S1's experiment requires no software — only a text editor and operator attention — while S3's requires producing a runnable assertion file and standing up a runner. The lighter the first move, the more likely it actually happens. Third, the answer to U1 (will the operator sustain calibration work?) is the answer that most reshapes the entire plan if it comes back negative; getting it first means the rest of the plan can be re-prioritised before any sunk cost has accumulated.

If after three weeks the operator concludes the answer is "no, this is too much" — that is a finding, not a failure. The plan re-shapes around it.

## What to do with the result

If the experiment goes well — sustainable authoring, schema feels close to right, day-21 revisit produces signal that the original synthesis did not surface — proceed to Phase A of [08-sequencing.md](08-sequencing.md) without further deliberation.

If the experiment goes poorly — authoring is painful, schema feels wrong, day-21 revisit reveals nothing — read the [08-sequencing.md](08-sequencing.md) "re-ordering allowances" section: ship S6 (smallest), then S3 alone (build the harness without acting on it), then revisit. This is the path that does not require the operator to commit to retrospective discipline.

Either way, the result of this single experiment is the most valuable signal the operator can buy this week, and the next plan iteration is grounded in evidence rather than reasoning.
