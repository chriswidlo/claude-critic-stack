# Scope-projector — extrapolate any proposed idea to its mature future-state form

| Field | Value |
|---|---|
| 📌 **title** | Scope-projector — extrapolate any proposed idea to its mature future-state form |
| 🎯 **tier** | 🚀 outlandish |
| 👤 **author** | operator |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Mid-conversation, the operator demonstrated this capability themselves: they took the AI's "small immediate" framing of the upgrades folder and projected it forward to its full R&D-lab maturity, then named the projection as a new capability worth adding. The operator's exact instinct: *"add to list — a future prediction system that will extrapolate proposed idea into full fledged solution with future in mind in global context."* |
| 💡 **essence** | A meta-capability that takes any small or local proposal and asks: "if this idea were taken to its full mature form, with downstream implications and global context considered, what would it become?" The output reframes the proposal at its eventual scale, which often reveals that the proposal as stated is undersized — and which sometimes reveals the proposal was correct as-is and forward-projection adds noise. Either is useful. |
| 🚀 **upgrade** | Prevents the "scope was too small, kept getting rewritten" failure mode that the operator named as their dominant frustration. By forcing future-projection at proposal time, ideas land at the right scope from the start. Could be an agent invoked between classification and reframe (Step 1.5), or a discipline added to the frame-challenger. The capability is not just for design questions — it could project *any* upgrade entry in this lab forward to its mature form. |
| 🏷️ **tags** | scope, foresight, methodology, meta-capability, classification |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The shape of the capability](#the-shape-of-the-capability)
- [Why this is outlandish — and why outlandish is the right tier](#why-this-is-outlandish--and-why-outlandish-is-the-right-tier)
- [Two integration paths](#two-integration-paths)
- [Open questions](#open-questions)

## The shape of the capability

Given a proposal `P` (a sentence, a paragraph, a candidate from Step 9, or an entry in this lab), the scope-projector produces:

- `P` at its **mature form** — what would this proposal look like at full development? what does it become?
- The **downstream implications** that the proposal-as-stated does not name: what other parts of the system would change? what new capabilities would emerge or be required?
- The **global context** the proposal sits in: what trends in the surrounding system make this proposal more or less load-bearing five years from now?
- A **scope verdict**: is `P` correctly sized, undersized, or oversized for what it is trying to do?

This is *forward-projection*, the inverse of retrospective analysis. Most of the workflow's machinery looks at what *is*; this looks at what *could be* and reads back to what *should be done now*.

## Why this is outlandish — and why outlandish is the right tier

The implementation mechanics could be small (an agent with a focused prompt, invoked at a specific workflow step). The reasons this is outlandish:

- **The capability is generative, not analytical.** Most of the stack's existing agents critique, distill, or classify *given content*. Scope-projector *generates* a future state from a current proposal, which requires a different kind of reasoning the current agents do not have.
- **Calibration is hard.** Forward-projection is famously prone to over-extrapolation. Without ground truth from many cases, the scope-projector could systematically inflate every proposal into a moonshot, defeating its purpose.
- **It has compounding value.** Every other upgrade in this lab could be re-read through scope-projector and gain new shape. That is a deep capability, not a small one.
- **It requires its own design pass.** Unlike "wire claude-code-guide" or "give critics Write," this is not a frontmatter edit. It needs prompt design, calibration, integration choice, possibly its own training data.

This is months of work, not hours. Outlandish.

## Two integration paths

**Path A — scope-projector as a Step 1.5 agent.** Inserted between classification (Step 1) and reframe (Step 2). The classifier emits a label and a default frame; the scope-projector emits a future-projection of the question. The reframe step uses the projection as one of its alternative framings.

**Path B — scope-projector as a frame-challenger discipline.** Existing frame-challenger gains a required output: "the proposal as stated, projected to mature form, looks like X. Frame-challenge: is the proposal undersized?" No new agent; existing agent does more.

Path A is cleaner architecturally; Path B is lower-cost and easier to validate. Either could be the entry point; the full capability could grow from either.

## Open questions

- How does the scope-projector calibrate against over-extrapolation? Does it need a corpus of "proposals and their actual eventual forms" to anchor its projections?
- Should it run automatically on every workflow question, or only when invoked? Always-on adds value but also adds elaboration risk (related to the workflow-overdesigns failure mode).
- Could it be applied retroactively to existing entries in this lab — re-projecting each upgrade's mature form and surfacing where the lab is undersized?
- Is the right name "scope-projector" or something else (maturity-extrapolator, future-caster, scope-corrector)?
