# Critics get the Write tool

| Field | Value |
|---|---|
| 📌 **title** | Critics get the Write tool |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The three critic agents (`critic-architecture`, `critic-operations`, `critic-product`) currently have `tools: Read, WebFetch, WebSearch` — no `Write`. Their verdicts come back inline; the orchestrator persists them. The audit trail is "me-claiming-they-said-X." Flagged in the operator's opening retrospective and confirmed during the upgrades-lab-design session when critique persistence was done by orchestrator paraphrase. |
| 💡 **essence** | Critics' verdicts should be persisted by the critics themselves. Their lack of `Write` means the only record of what each lens said is the orchestrator's transcription, which is structurally compromised — paraphrasing a model's verdict is a different artifact than the verdict itself. |
| 🚀 **upgrade** | Add `Write` to each critic's frontmatter `tools:` line, scoped (in instruction) to `.claude/session-artifacts/<id>/critiques/<lens>.md`. Add one line to each critic's body: *"Write your verdict to `critiques/<lens>.md`. Return only a one-line summary inline."* The audit trail becomes the agent's own writing. ~5 minutes of edits across three files. |
| 🏷️ **tags** | critique, audit, tool-permissions, frontmatter |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The fix](#the-fix)
- [Why this matters](#why-this-matters)
- [Why this is no-brainer rather than normal](#why-this-is-no-brainer-rather-than-normal)

## The fix

In each of `.claude/agents/critic-architecture.md`, `.claude/agents/critic-operations.md`, `.claude/agents/critic-product.md`:

- Frontmatter `tools:` line gains `Write`: `tools: Read, Write, WebFetch, WebSearch`.
- Body gains a sentence in the output-instructions section: *"Persist your full verdict to `.claude/session-artifacts/<session-id>/critiques/<lens>.md`. Return only a one-line summary inline (verdict + the single most important objection); the orchestrator reads the file for the full review."*

The orchestrator's CLAUDE.md instructions for Step 10 should be updated to expect this: *"Critics now write their own verdicts. Read `critiques/<lens>.md` rather than parsing inline returns."*

## Why this matters

The architecture-critic might point at a specific protocol surface. The operations-critic might cite a specific failure mode. The product-critic might trace a specific operator friction. When the orchestrator transcribes these into `critiques.md`, structure and emphasis are preserved by approximation, not by transmission. Across many sessions, the loss compounds.

For a stack whose value proposition is *adversarial review*, the artifact that most directly evidences the review should be authored by the reviewer. Anything else is — as the retrospective put it — "me-claiming-they-said-X."

This was caught in the upgrades-lab-design session itself: critic-panel verdicts were returned inline (per current frontmatter constraint) and the orchestrator persisted them. The persistence was faithful, but only because the orchestrator was actively trying. The structural fix removes "actively trying" from the critical path.

## Why this is no-brainer rather than normal

The change is mechanical: three frontmatter edits, three one-line body additions, one CLAUDE.md sentence updated. Total time: under fifteen minutes including the read of the existing files. The value is uncontroversial (the audit trail becomes real instead of approximated). There is no design uncertainty, no controversial trade-off, no migration cost.

This is the canonical no-brainer: small effort, obvious value, would-implement-immediately. It sits in this lab as the entry that should be the first to move to 🔨 `implemented`.
