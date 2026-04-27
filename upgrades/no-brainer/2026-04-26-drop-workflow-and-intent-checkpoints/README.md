# `/drop-workflow` slash command + in-flight intent checkpoints

| Field | Value |
|---|---|
| 📌 **title** | `/drop-workflow` slash command + in-flight intent checkpoints |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective: *"I kept letting the workflow drive over your actual question. You wanted operational guidance; I gave you critic-panel theater. You had to explicitly say 'I don't know what I should do next, are you able to execute' before I shifted to handoffs and roles. That shift should have been my move at synthesis, not yours after synthesis."* Mid-session intent shifts are real and the workflow currently has no escape hatch. |
| 💡 **essence** | Two layered fixes: (1) a user-callable `/drop-workflow` slash command that writes a marker file the orchestrator reads as "abandon the workflow, reread my recent messages, answer directly"; (2) two prose checkpoints in CLAUDE.md (between Steps 6→7 and Steps 9→10) that instruct the orchestrator to verify the user's question hasn't shifted since the workflow started. |
| 🚀 **upgrade** | Operator gets explicit control to abandon a workflow that has stopped serving the question. Orchestrator gets two scripted moments to ask "is this still what they wanted?" without depending on its own drift-detection. The workflow stops being an unstoppable train. |
| 🏷️ **tags** | workflow, user-control, slash-command, intent, escape-hatch |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The two fixes](#the-two-fixes)
- [Why both, not one](#why-both-not-one)
- [Why no-brainer](#why-no-brainer)

## The two fixes

**`/drop-workflow` slash command.** Definition at `.claude/commands/drop-workflow.md`. When invoked, the command instructs the AI to: (a) write `session-artifacts/<id>/intent-pivot.md` containing the user's most recent message context; (b) immediately stop any in-progress workflow steps; (c) reread the user's last 3-5 messages; (d) answer the *current* question directly, dropping the workflow's accumulated state. The artifacts on disk remain (audit trail), but the orchestrator stops driving the workflow.

User-controlled. No model-detection burden. One typed command bails out.

**Two prose checkpoints in CLAUDE.md.** Inserted between Step 6 (distill) and Step 7 (scope-map), and between Step 9 (generator) and Step 10 (critic-panel). Each checkpoint adds two sentences to the workflow:

> Before proceeding, check if the user's last 2 messages have shifted the question since the workflow started. If yes (e.g., from "design this" to "just tell me what to do"), surface that and offer to drop the workflow. Continue only if the user is still asking the original question.

Weak as a single mechanism (depends on the model noticing) but free, and catches the easy cases.

## Why both, not one

The slash command is robust but requires the operator to notice and act. The prose checkpoints are weak but catch cases where the operator is also drifting along with the workflow without realizing. Together they cover both failure modes: operator-aware drift (slash command) and operator-unaware drift (checkpoint).

Don't try to detect drift via hooks. Hooks can't reliably classify intent from message content alone, and false positives are worse than the original problem.

## Why no-brainer

Both fixes are text-only:

- The slash command is a markdown file in `.claude/commands/` (~30 lines of instructions).
- The two checkpoints are sentence-additions to CLAUDE.md (one paragraph each).

Total time: ~30 minutes including writing the slash command. The value is uncontroversial — the operator explicitly named this gap as a top-level frustration in the retrospective. There is no design uncertainty.
