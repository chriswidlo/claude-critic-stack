# Corpus-bias compensation as Step 6.5

| Field | Value |
|---|---|
| 📌 **title** | Corpus-bias compensation as Step 6.5 |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective: *"I inherited the corpus's Anthropic-source bias without compensating. The librarian flagged it explicitly. Every plan I produced reflected Anthropic's architectural preferences."* Confirmed during the upgrades-lab-design session, where canon-librarian flagged "the corpus skews systems-engineering and agent-orchestration; zero entries on R&D-process methodology" — and the orchestrator proceeded without doing any compensating WebSearch. |
| 💡 **essence** | The canon-librarian already detects and flags single-source dominance, single-ecosystem bias, and other corpus skews. But the workflow has no step that *acts* on these flags. The orchestrator can read the warning in the distillation and proceed anyway. The flag is information without an action. |
| 🚀 **upgrade** | A new mandatory step between current Steps 6 (distill) and 7 (scope-map): if any distillation flags a single-source dominance, single-ecosystem bias, or convergent-source warning, the orchestrator must either (a) invoke a targeted WebSearch or canon-librarian sub-query for an explicitly-out-of-ecosystem contradiction, or (b) state in the synthesis that no out-of-ecosystem source is available and mark it as a known bias. Non-negotiable for design questions where the candidate will reflect the corpus's center of mass. |
| 🏷️ **tags** | workflow, canon, bias, retrieval, methodology |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What the new step looks like](#what-the-new-step-looks-like)
- [Why this is no-brainer](#why-this-is-no-brainer)
- [Optional pairing with a hook](#optional-pairing-with-a-hook)

## What the new step looks like

Added to CLAUDE.md, between Steps 6 and 7:

> **6.5. Bias-compensation pass.** If any distillation in `distillations/` flags a single-source dominance, single-ecosystem bias, convergent-source warning, or wrong-corpus declaration, the orchestrator must do one of:
> 
> (a) Invoke a targeted WebSearch or `canon-librarian` sub-query for an explicitly-out-of-ecosystem contradiction. The result lands as a sub-distillation under `distillations/bias-compensation.md`.
> 
> (b) State in writing (and surface in synthesis) that no out-of-ecosystem source is available and mark this as a known bias affecting the candidate.
> 
> This step is non-negotiable for design questions where the candidate will reflect the corpus's center of mass. Skip permitted only if the librarian distillation explicitly declared no bias warning.

## Why this is no-brainer

- The mechanism (read the librarian distillation, look for bias flags, act) is mechanical.
- The change is a CLAUDE.md addition, not a code change.
- The value is concrete: in the upgrades-lab-design session, the librarian explicitly named "wrong corpus" and the orchestrator built the candidate against the wrong-corpus's biases anyway. With Step 6.5 in place, that session would have either produced an out-of-ecosystem WebSearch or declared the bias as a known limitation. Either is better than what happened.
- The trigger condition is well-defined: a flag in the librarian distillation. Not subjective.

## Optional pairing with a hook

Can be reinforced with a `PostToolUse` hook on `subagent-distiller` writes: grep the just-written distillation for keywords like `bias:`, `single-source`, `wrong corpus`, `coverage gap`. If present, inject a system reminder before the orchestrator's next turn: *"Distillation flagged a corpus bias. Step 6.5 applies."*

The hook is small (~20 lines bash) and removes the dependency on the orchestrator remembering to look. Optional because the prose-only version is also fine; the hook is an upgrade-of-an-upgrade.
