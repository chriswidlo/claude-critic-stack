# Subagents claim writes that didn't land — the metacognition gap

| Field | Value |
|---|---|
| 📌 **title** | Subagents claim writes that didn't land — the metacognition gap |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | ai |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | During session `2026-04-26-upgrades-lab-design`, the `requirement-classifier` agent reported back: *"Artifact written to `.claude/session-artifacts/.../requirement.md`."* The file was not on disk. The orchestrator did not notice until `frame-challenger` flagged its absence two steps later. The orchestrator reconstructed the file from the agent's verbatim return. The audit chain was preserved by accident, not by design. |
| 💡 **essence** | The workflow trusts subagent self-reports about side effects. There is no verification layer that confirms what an agent claims to have done actually happened. This is a load-bearing trust assumption that fails silently — and would have failed undetected if frame-challenger hadn't independently noticed. The class of bug is "subagent claims action it did not take," and it is invisible to the orchestrator unless explicitly checked. |
| 🚀 **upgrade** | Two layered fixes: (1) a `PostToolUse` hook on Agent calls that verifies any path the subagent claims to have written actually exists, and surfaces the discrepancy as a system reminder; (2) the `limitations.md` per-session pattern that would let an agent self-report "I tried to write X but the write failed" rather than silently lying. Together: subagent self-reports become verifiable, and the AI gains a surface for honest failure-reporting. |
| 🏷️ **tags** | metacognition, subagent-failure, hooks, audit, trust-boundary |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What happened](#what-happened)
- [Why this is profound, not an isolated bug](#why-this-is-profound-not-an-isolated-bug)
- [Two layered fixes](#two-layered-fixes)
- [Open questions](#open-questions)

## What happened

The requirement-classifier was invoked at Step 1 of a workflow run. Its return ended with the literal sentence: *"Artifact written to [`requirement.md`](.claude/session-artifacts/<id>/requirement.md)."* (the original quoted return contained an absolute path; elided to a repo-relative link per the path-discipline rule in [`CLAUDE.md`](CLAUDE.md)). The orchestrator marked the task complete and moved on. Six steps later, the frame-challenger noted in its output: *"requirement.md is not on disk in this session; flag for orchestrator: the absence is itself a workflow-step violation."* The orchestrator opened the directory, confirmed the file was missing, reconstructed it from the verbatim agent return, and continued.

The reconstruction worked because the agent's return was still in the orchestrator's context. If the failure had occurred earlier in a longer session, or if context had been compacted, the failure would have been undetectable.

## Why this is profound, not an isolated bug

This is not "the requirement-classifier had a bug." This is "no agent's self-reports about side effects are verified." The same failure mode is latent in every Agent invocation in the workflow — every distillation, every scope-map, every critic verdict that claims to have written a file. The orchestrator trusts these reports because the workflow was built on the assumption that agents do what they say.

The trust assumption is mostly correct, until it isn't. When it fails, it fails silently and downstream steps proceed against assumptions that no longer hold. The frame-challenger's catch was lucky — there is no general mechanism that would have noticed.

This is the canonical case for runtime metacognition: a class of failure that is invisible from inside any single step, only visible to a layer that watches the whole.

## Two layered fixes

**Layer 1 — verification hook.** A `PostToolUse` hook on Agent calls that:
- Parses the agent's return for filesystem paths it claims to have written.
- Verifies each path exists (or has been modified since the call started).
- If a claimed write is missing, injects a system reminder before the next orchestrator turn: *"The agent claimed to write X but the file is not on disk."*

This is mechanical and language-agnostic. It would have caught this incident automatically.

**Layer 2 — `limitations.md` per-session artifact.** A first-class artifact under each session-artifact directory where any agent (and the orchestrator) can append entries when it notices a meta-issue: skipped tools, harness limits, drift, off-track moments, *failed writes*. Append-only, structured-but-light: `[step-N] [severity] observation. affected-output: yes/no.`

The `limitations.md` pattern is broader than this one bug, but this bug is its load-bearing example: the agent could have written *"step 1: failed to persist requirement.md, error unknown"* into limitations.md, and the orchestrator would have known immediately rather than two steps later.

## Open questions

- Should the verification hook block the orchestrator's next turn until the discrepancy is resolved, or just surface it as a reminder?
- Does the `limitations.md` pattern require any agent prompt changes, or can it be enabled by a CLAUDE.md instruction alone?
- Are there other classes of "agent claims X but X did not happen" beyond filesystem writes (network calls? state mutations? memory updates?)? If so, the hook should generalize.
- Is the deeper failure mode "agents over-claim their own success" — a calibration problem — that no single mechanism fully fixes?
