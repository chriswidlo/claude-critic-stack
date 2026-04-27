# Casual orchestrator output is workflow-unprotected

| Field | Value |
|---|---|
| 📌 **title** | Casual orchestrator output is workflow-unprotected |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The orchestrator wrote a confident, structured casual reply about a community plugin, including a load-bearing factual claim about the user's machine that turned out to be wrong. The user then invoked the workflow on that reply, and the workflow caught the error. The error was caught — but only because the user thought to invoke the workflow. In the (much larger) population of casual replies that never get workflow-validated, the same kind of error is presumably present and presumably uncaught. |
| 💡 **essence** | The 12-step workflow is the orchestrator's epistemic immune system: classifier surfaces frame, outside-view fights inside-view bias, canon fights memory, scope-mapper enumerates primitives, frame-challenger devil's-advocates, critics veto. None of that protection is in scope when the orchestrator answers casually outside the workflow. The casual mode is the *default* mode — most replies are casual. The workflow protects intentional design questions. The default mode has no equivalent protection, and the user has no way to know which replies were inside-view-from-memory and which were grounded. |
| 🚀 **upgrade** | A `casual-mode discipline` documented at the top of CLAUDE.md, articulating which workflow disciplines must be ported into casual mode (even at zero artifact cost) and which can be skipped. Specifically: the load-bearing minimums are (a) the outside-view *instinct* on any decision-shaped question, (b) the librarian-first rule on any factual question, (c) the user-state-verification discipline on any reply that asserts user-machine state. None of these requires invoking subagents — they are dispositions the orchestrator must hold even in casual replies. The longer-term upgrade is a `casual-validator` mini-agent that audits a draft casual reply for these three disciplines before sending. |
| 🏷️ **tags** | meta, workflow-scope, casual-mode, epistemic-discipline |
| 🔗 **relates_to** | 2026-04-26-generator-cited-user-state-from-memory, 2026-04-26-quick-take-off-ramp-pre-check |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The asymmetry of protection](#the-asymmetry-of-protection)
- [What the workflow protects against](#what-the-workflow-protects-against)
- [What casual mode currently has](#what-casual-mode-currently-has)
- [The minimum casual-mode discipline](#the-minimum-casual-mode-discipline)
- [The longer-term version](#the-longer-term-version)
- [Why this is profound, not just a bug fix](#why-this-is-profound-not-just-a-bug-fix)

## The asymmetry of protection

Every interaction with the orchestrator falls into one of two modes:
- **Workflow mode**: 12 steps, 8+ subagents, hard gates, distillations, critic panel. Heavyweight, slow, designed to defeat inside-view bias and memory-anchoring.
- **Casual mode**: a normal reply, with whatever tools the orchestrator decides to call. Light, fast, governed by no hard gates.

The user controls which mode by how they ask. A design question that names tradeoffs and asks for analysis triggers workflow mode. A "what do you think about this" triggers casual mode.

This means: the workflow's protections — outside-view, canon-first, scope-mapping, frame-challenging, critic veto — are conditional on the user opting in. The default reply is uncovered.

## What the workflow protects against

Concretely, the workflow defeats:
- **Inside-view bias** (outside-view step) — the tendency to reason from this problem's details and miss base rates.
- **Confirmation bias in retrieval** (canon-librarian's "must return contradicting passages") — the tendency to find what supports the answer one is already drifting toward.
- **Anchoring on existing primitives** (scope-mapper) — the tendency to subsume new requirements into the shape of what already exists.
- **Frame lock-in** (frame-challenger) — the tendency to optimize within the user's framing rather than challenge it.
- **Single-axis judgment** (critic panel) — the tendency to evaluate a candidate from one perspective.
- **Memory-as-source** (the entire artifact-on-disk discipline) — the tendency to cite what one remembers seeing rather than what is currently true.

Every one of these biases is *more* likely in casual mode, because casual mode is faster and the orchestrator does not have the workflow's friction forcing each defense.

## What casual mode currently has

Almost nothing structurally. Casual mode has:
- The orchestrator's general training (which includes some of the dispositions, unevenly).
- Whatever tool calls the orchestrator decides to make (which may or may not include verifying user-state claims).
- The rule against persona-cosplay (in CLAUDE.md but not casual-specific).
- The rule against fabricating a target codebase (in CLAUDE.md but not casual-specific).

There is no documented casual-mode discipline. The CLAUDE.md is structured as workflow rules with off-ramps; the off-ramps say *what to do instead of the workflow* but do not say *what dispositions the casual mode owes to the user*.

In practice, casual mode replies are written in the same way the orchestrator would have written them before the workflow existed: from inside-view, from memory, with confident phrasing where hedge would be more honest.

## The minimum casual-mode discipline

Three rules that cost zero subagent invocations and would have caught the karpathy error:

1. **User-state verification rule** — When asserting a fact about the user's machine (files, contents, configs, agents installed), either cite a tool call from this conversation or hedge explicitly. No memory-derived user-state claims without a hedge. (Filed separately as a no-brainer.)

2. **Outside-view-instinct rule** — When the question is decision-shaped (should I do X / which approach / is X better than Y), name the relevant base rate or reference class, even one sentence, before stating a recommendation. The workflow runs a full outside-view step; casual mode at minimum names the class.

3. **Librarian-instinct rule** — When the question is factual (what is X / how does Y work / what does Z say), name the source or admit "from memory, may be stale." The workflow runs a full canon-librarian step; casual mode at minimum names provenance.

These three rules together encode the *load-bearing* disciplines of the workflow as casual-mode habits. They are zero-cost because they require no subagent invocations — they are dispositions the orchestrator holds.

## The longer-term version

A `casual-validator` mini-agent (or a self-audit pass before sending a casual reply) that checks the draft for:
- User-state claims without sourcing.
- Decision recommendations without reference-class language.
- Factual claims without provenance.

Returns either "ship it" or "rewrite this section." Lightweight, runs in seconds, pre-send. The cost is one agent call per casual reply, which is small relative to the cost of being wrong.

This is the asymmetric counterpart to the workflow. The workflow is heavyweight protection for high-stakes design questions. The casual-validator is lightweight protection for the long tail of casual replies that the user does not invoke the workflow on.

## Why this is profound, not just a bug fix

The 12-step workflow is an impressive epistemic apparatus. It is also rare — most user interactions do not trigger it. If the workflow is the *only* place the orchestrator's epistemic discipline lives, then most of the orchestrator's output is unprotected by the apparatus.

This is profound because it changes how to think about the workflow's value: the workflow is not the protection, it is the *visible top* of a discipline that should be ambient. The discipline must be ported down into casual mode, in some compressed form, or the workflow's existence creates a false sense of safety — the user thinks "the orchestrator has serious epistemic hygiene" while only the workflow-mode replies actually do.

The karpathy session is the proof: the casual reply was confident, structured, looked rigorous, and contained a load-bearing factual error that the workflow caught. Without the workflow invocation, the error would have stood. The number of casual replies the user has accepted at face value because they looked rigorous is the unmeasured cost.

The fix is partly procedural (the three rules) and partly cultural (the orchestrator must hold the workflow's dispositions even in casual mode). Both halves are needed. Without the procedural rules, the cultural rule is invisible and unenforceable. Without the cultural rule, the procedural rules feel like overhead and get skipped.
