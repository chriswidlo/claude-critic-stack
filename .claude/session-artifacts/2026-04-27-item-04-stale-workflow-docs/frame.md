# Frame — item 4: stale top-level workflow docs

## Revision 1

### The user's implicit frame

The plan ([plans/2026-04-27-item-04-stale-workflow-docs.md](../../../plans/2026-04-27-item-04-stale-workflow-docs.md)) and the punch-list framing optimise for **correctness of what new readers absorb** — *"a reader landing on README.md reaches an accurate description of the current 12-step workflow within one click."* The recommendation falls out of that frame: ship the minimum delete-and-redirect now because it closes the correctness gap; defer the doc-design work because it is quality-of-life, not correctness.

That frame is honest and load-bearing — but it implicitly accepts two assumptions that are worth naming:

1. *"Pointing at `CLAUDE.md` plus `session-artifacts/README.md` is sufficient as the post-(a) reading order."* Treats the union of two existing docs as a coherent onboarding path. Whether it actually is, is not tested.
2. *"The unified-doc work is independent enough to defer."* Presumes the operator can choose later, with the same context, between (b) and (c) without the deferral cost (re-reading, re-deciding) eating the gain.

### Reframe — at least one alternative

**Alt frame A — Optimise for sustained doc/code coherence, not first-read accuracy.**

The actual failure mode this stack repeatedly hits is *drift*: a doc was correct when written and then the system moved past it. [`workflows/architecture-review.md`](../../../workflows/architecture-review.md) is not a one-time stale file; it is the second-order symptom of the question *"where does workflow-shape documentation live, and what makes it stay current?"* Under this frame, the live decision is not *"ship (a) now or bundle (b)/(c)"* but *"what is the minimum doc surface area whose update is forced whenever the workflow changes — and is `CLAUDE.md` already that surface, or do we need a second one?"*

A doc that is updated as part of every workflow change stays current. A doc that has to be remembered separately drifts. Under Alt frame A, option (b) (a separate `workflows/12-step-workflow.md`) is structurally suspect — it adds a second surface that has to drift in lockstep with `CLAUDE.md` and won't. Option (c) (expand `session-artifacts/README.md`) is structurally better only if the expansion lives close enough to the artifacts that breaking the workflow breaks visibly. Option (a) — *no new doc, just point at the doc that orchestrators already have to keep correct* — is the structurally most-stable shape, **not despite being minimum but because it is minimum.**

**Alt frame B — Optimise for the agent's onboarding, not just the human reader's.**

The README and `workflows/architecture-review.md` are read by *humans* arriving at the repo. But the docs that actually drive runtime behaviour are `CLAUDE.md` (read by Claude as the CLAUDE.md root) and the agent files in [.claude/agents/](../../../.claude/agents/) (loaded as subagent prompts). Under this frame, *"misrouting new readers"* covers two audiences with different stakes:

- **Human reader** — wrong mental model. Recoverable by re-reading. Cost: a few minutes of confusion.
- **AI orchestrator that read the file as part of context** — wrong runtime behaviour. *Not* recoverable without a fresh session. Cost: hours of off-spec work before someone catches it.

`CLAUDE.md` is loaded into the orchestrator's context automatically; `workflows/architecture-review.md` is not, but a sufficiently agentic loop ("read the workflow doc and follow it") *would* load it. The real-world risk under this frame is small but non-zero: an automation that follows `README.md` → `workflows/architecture-review.md` and then tries to invoke a `critic` agent that doesn't exist, with whatever runtime fallback the harness applies.

### What the user is implicitly optimising for

**First-read correctness for a human reader landing on `README.md`.**

### Alternative optimisation candidates

- **Doc/code coherence over time** — minimum surface that drifts the least.
- **Both human and AI reader correctness** — defends against agentic re-entry into a stale routing.
- **Decision-debt minimisation** — pick the smallest reversible move; defer the larger doc-design choice until it is actually needed.

### Does the reframe change the answer?

It does not flip *(a) alone vs. bundle (b)/(c)*: under all three reframes, **option (a) is still the right immediate move.** What changes is the framing of what (a) accomplishes. Under the user's frame, (a) is *partial* — closes correctness but leaves the unified-doc gap. Under Alt frame A, (a) may be *sufficient* — the unified doc is a maintenance liability, not a feature, and the *absence* of `workflows/12-step-workflow.md` is itself the right answer if `CLAUDE.md` is the orchestrator's source of truth. Under Alt frame B, (a) is *necessary urgently* — any agentic loop following the stale routing is a live correctness risk, not just a UX concern.

### Where this lands the workflow

The classifier's "preserve requires a stated reason" default still holds. The reframe sharpens the question for the scope-mapper and the frame-challenger:

- **Scope-mapper:** does the existing primitive (`workflows/architecture-review.md`) get *replaced* (option a — delete + re-point), *replaced-with-substitute* (option b — new file), or *subsumed* (option c — content folded into session-artifacts README)? The default is `replace`, but option (b) creates a fresh primitive that has to coexist with `CLAUDE.md`, which is itself a coupling decision worth challenging.
- **Frame-challenger:** the strongest devil's-advocate move is to challenge Alt frame A's preservation claim — *"is `CLAUDE.md` actually a good front-door doc, or are we offloading the gap onto a doc whose audience is the orchestrator, not a new human reader?"*
