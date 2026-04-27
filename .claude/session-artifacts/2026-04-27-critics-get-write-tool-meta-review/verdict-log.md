# Verdict log — meta-review of *"Critics get the Write tool"*

> One-screen tabular summary. Long-form reasoning lives in [`meta-review.md`](meta-review.md).

## Pick

| Field | Value |
|---|---|
| **Verdict** | **v2-D — do nothing** |
| **Conditional on?** | Operator running the cheapest version of the experiment (retrospective single-session diff against the existing run) and finding zero meaningful paraphrases. |
| **What flips it** | A single captured paraphrase incident in the existing or any future panel session. Then the verdict shifts to **v2-A** (structured-return + verbatim-write), not v2-C+. |
| **Dominated shapes** | v2-C, v2-C+ — both rely on a behavioral promise from the orchestrator they exist to constrain. v2-A moves the contract into the data shape; v2-D defers the cost entirely. |
| **Held-as-post-experiment shape** | v2-F (post-hoc audit job, not pre-hoc enforcement) — the right answer if the motive is measured-but-batch-able. |

## Calibration

| Pass | Discount factor `d` | Interval | Method |
|---|---|---|---|
| Loop 1 (architecture reject + 2× rework) | `~0.15` | `0.10–0.25` | A: structural symmetry (`0.40·0.20 + 0.60·0.05 = 0.11`); B: outside view (Madaan/Anthropic CAI/Zheng anchors, ~15–25%); C: reductio brackets to `[0.05, 0.30]` |
| Loop 2 (3× rework on v2-C) | `~0.08` | `0.05–0.15` | Same methodology; lower because architecture's surface is unchanged under v2-C |

`d = 0` means panel verdict fully trustworthy; `d = 1` means worthless. Method-disagreement: small.

**Interaction with verdict:** v2-D is robust to verdict noise; the discount does not move the pick. If the verdict were v2-A or v2-C+, the discount would matter materially.

## Counterfactual

| Question | Answer |
|---|---|
| Pre-frame answer | Closest to **v2-A**, conditional on the experiment firing. v2-D would not have been the named primary pick. |
| Saved / wasted / reframed | **Reframed.** The workflow's verdict-shifting contribution was naming v2-D as a serious option (frame-challenger). The two-loop iteration on v2-C/v2-C+ was largely token-cost on dominated shapes. |
| Workflow value-add (in priority order) | (1) Naming v2-D; (2) workflow-docs-gap adjacent finding; (3) calibration disclosure from architecture's tail-note. |

## Recommended next operator action

1. **First**, check whether the loop-1 and loop-2 panel-invocation transcripts are recoverable (~1 minute).
2. **If yes**, run the retrospective diff on the existing session (~5 minutes). Report a single number: meaningful-paraphrase incidents found, where "meaningful" means *changed structure, omitted hedge, renamed section, or substantive abridgement* (not whitespace or markdown rendering).
3. **If zero**, accept v2-D and resolve the upgrade entry with a closure note pointing to this meta-review.
4. **If ≥1**, re-open the entry with v2-A as the candidate and a worked example from the captured incident.
5. **If no**, fall back to the synthesis's prospective 4-session experiment, but consider the recommended workflow-modification (Step 12 reads per-lens, not aggregate) as an independent upgrade entry — it is justified by evidence already on disk regardless of how the audit-faithfulness experiment resolves.

## Files this meta-review produced

- [`meta-review.md`](meta-review.md) — long-form reasoning across four sections.
- [`verdict-log.md`](verdict-log.md) — this file.

## Files this meta-review did not modify

- The session-artifacts under [`2026-04-27-critics-get-write-tool-impl/`](../2026-04-27-critics-get-write-tool-impl/) — append-only history.
- The three critic agent files — implementation belongs to a separate session if the operator approves.
- `CLAUDE.md` — workflow-modification proposals are proposals only; the operator decides.
