# Critics get the Write tool

> ⏸️ **PAUSED — 2026-04-27.** The 12-step run-through-repo workflow surfaced that the original plan (add `Write` to three critics + Defenses 1/2 + thin-index aggregate) does not survive review: loop 1 produced a convergent veto across all three lenses (architecture **reject** on role-fusion; operations and product **rework** on concurrency-step-change and operator-surface regression). Loop 2's revised candidate v2-C also returned 3× rework with concrete missing pieces. The motivating problem (orchestrator paraphrase loss in `critiques.md`) has **no measured incident on file** — the frame-challenger named v2-D (do nothing) as the legitimate null hypothesis, and synthesis proposed a cheap 4-session manual diff experiment to test it before paying any implementation cost. Pausing here is the honest output: the entry as filed is *not* the right implementation; whether *any* implementation should ship is itself unmeasured. The full findings, four candidate shapes (v2-A, v2-C, v2-C+, v2-D), and the experiment that would unblock are recorded below and in [session-artifacts/2026-04-27-critics-get-write-tool-impl/](../../.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/). Resume when (a) the experiment returns a measured paraphrase incident, or (b) upgrade #3 (PostToolUse verification hook) lands and changes the cost calculus on harness-level enforcement. **An independent meta-review of this run is filed at [session-artifacts/2026-04-27-critics-get-write-tool-meta-review/](../../.claude/session-artifacts/2026-04-27-critics-get-write-tool-meta-review/); its verdict (v2-D, with v2-A as the path-not-taken if the experiment fires) and calibration (`d_loop1 ≈ 0.15`, `d_loop2 ≈ 0.08`) are recorded there. The meta-review also proposes a *retrospective* form of the experiment (single-session diff against this very run, ~5 min) that dominates the synthesis's prospective 4-session form on cost, latency, and evidence quality.**

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
| 2026-04-26 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | — | — | — |

> **Update history.** On 2026-04-27, advanced 🔬 spiked → 📋 prepared → ✅ accepted → ⚙️ run-through-repo in one session. The first three states were mechanical (the entry was specified at filing). The run-through-repo state is the substantive one: session id [`2026-04-27-critics-get-write-tool-impl`](../../.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/) ran the full 12-step workflow. Loop 1 returned a convergent veto (architecture reject, operations + product rework) on the original entry's plan; the orchestrator routed to replan under a new frame. Loop 2 produced candidate v2-C (orchestrator-as-sole-writer + byte-fidelity prose contract; drop aggregate) which received 3x rework with five small actionable additions. Synthesis presented four shapes (v2-A, v2-C, v2-C+, v2-D) to the operator as a decision rather than a recommendation. **Acceptance scope on 2026-04-27 was on the original entry's plan, which the workflow then said was wrong.** The acceptance is preserved as the date the operator accepted *the question*, not *the implementation* — the implementation is now an open operator decision recorded in the synthesis. Per [#18f state-table-honesty-discipline](../normal/2026-04-26-state-table-honesty-discipline.md). The `🔨 implemented` cell remains empty pending the operator's choice across the four shapes.

## Table of contents

- [The fix](#the-fix)
- [Why this matters](#why-this-matters)
- [Why this is no-brainer rather than normal](#why-this-is-no-brainer-rather-than-normal)
- [Spike](#spike)
- [Plan](#plan)
- [Acceptance](#acceptance)
- [Run-through-repo decision](#run-through-repo-decision)
- [Run-through-repo outcome](#run-through-repo-outcome)
- [The four candidate shapes](#the-four-candidate-shapes)
- [Why v2-C+ is not the obvious answer](#why-v2-c-is-not-the-obvious-answer)
- [Adjacent finding — workflow docs are scattered and partly stale](#adjacent-finding--workflow-docs-are-scattered-and-partly-stale)
- [Resume conditions](#resume-conditions)

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

## Spike

Read on 2026-04-27 of [`critic-architecture.md`](../../.claude/agents/critic-architecture.md), [`critic-operations.md`](../../.claude/agents/critic-operations.md), [`critic-product.md`](../../.claude/agents/critic-product.md), and the Step 10 section of the project's `CLAUDE.md`.

Findings:

- **Frontmatter is uniform across all three critics.** Each has `tools: Read, WebFetch, WebSearch`. Adding `Write` is a single-word edit per file. No structural divergence to reconcile.
- **No harness conflict.** Other agents in this stack (`subagent-distiller`, `scope-mapper`, `frame-challenger`) already hold scoped `Write` permission and write to `.claude/session-artifacts/<id>/`. The pattern is established.
- **Path convention.** The entry proposes `.claude/session-artifacts/<session-id>/critiques/<lens>.md` (plural `critiques/` directory). This composes cleanly with the existing aggregate `critiques.md` referenced in CLAUDE.md Step 10 — either as a sibling summary or as a deprecated artifact (see [Plan](#plan), open question 1).
- **One implementation question surfaced.** Critic agents do not currently receive the session-id; their invocation prompts will need to include it explicitly. This is an orchestrator-side change, not an agent-side change, but the entry's body should name it so the implementer doesn't miss it.
- **No blockers.** Spike confirms the change is mechanical and the value chain is intact.

## Plan

Concrete edits, in dependency order:

1. **Three agent frontmatter edits.** In `.claude/agents/critic-architecture.md`, `.claude/agents/critic-operations.md`, `.claude/agents/critic-product.md`: change `tools: Read, WebFetch, WebSearch` → `tools: Read, Write, WebFetch, WebSearch`.

2. **Three agent body edits.** Add to each critic's "Required structure of your output" or a new "Output persistence" section: *"Persist your full verdict to `.claude/session-artifacts/<session-id>/critiques/<lens>.md`, where `<lens>` is `architecture`, `operations`, or `product` to match this agent's name. The session-id will be provided in your invocation prompt. Return only a one-line summary inline (verdict + the single most important objection); the orchestrator reads the file for the full review."*

3. **CLAUDE.md Step 10 update.** Replace *"Aggregate verdicts into `critiques.md`"* with *"Each critic writes its full verdict to `critiques/<lens>.md`. Read those files for the full reviews; the inline returns are one-line summaries only. Pass the session-id to each critic in its invocation prompt."*

4. **Open question — aggregate `critiques.md`.** Decide whether the orchestrator still produces an aggregate `critiques.md` summary (one-line-per-lens index of verdicts) or drops it now that the per-lens files are authoritative. Default proposal: **keep the aggregate as a thin index** — orchestrator writes a 3-row table (lens · verdict · path-to-file) so synthesis (Step 12) has a single read for the panel result. Explicitly *not* the place where verdicts live.

5. **Smoke test.** After edits, invoke any one critic agent with a trivial prompt and a fake session-id; verify the file lands at the expected path. Confirms the harness honors the new tool grant.

Estimated effort: 15 minutes for steps 1–3, 5 minutes for step 4 if defaulting to "keep aggregate as index," 5 minutes for step 5. Total ~25 minutes.

## Acceptance

Accepted by operator on 2026-04-27.

The operator selected this entry from a five-candidate first-session menu and instructed the orchestrator to walk it through the lifecycle. The acceptance is on the entry *as designed* — the three frontmatter edits, the body sentence, the CLAUDE.md update, and the proposal to keep an aggregate `critiques.md` as a thin index. If the implementation diverges from this shape (e.g., dropping the aggregate, or scoping the Write tool more tightly via a hook), the divergence is a re-acceptance question, not an editorial choice.

## Run-through-repo decision

The `⚙️ run-through-repo` state filters design-level critique on the *implementation choices* (per the lifecycle definition in `upgrades/README.md`). For this entry, the implementation surface is:

- 3 frontmatter additions (`Write`)
- 3 short body sentences
- 1 CLAUDE.md sentence
- 1 small open design choice (aggregate `critiques.md`: keep / drop)

The argument for **invoking the 12-step workflow**: the small design choice (aggregate keep/drop) and the question of *whether* the per-lens write contract should be enforced by hook rather than agent-side instruction — these are the kind of things a critic-panel would surface. There's also recursive value: the panel reviewing a change to itself is a useful self-test.

The argument for **skipping with a note**: the implementation is mechanically specified. The aggregate keep/drop is XS reversible. Running a 12-step on this would consume more tokens than the implementation itself, and the panel's most likely contribution is "looks fine."

This decision is left for the operator. Default if not stated: **skip with a note**, recording in `decision-log.md` (or in this section) that the run-through-repo state was deliberately skipped because the implementation is fully mechanical and any failure-class the panel would surface is XS reversible.

## Run-through-repo outcome

**Operator chose to run the 12-step workflow on 2026-04-27.** Session id: [`2026-04-27-critics-get-write-tool-impl`](../../.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/). The default-skip reasoning above was wrong — the workflow surfaced significant frame-level objections that the entry as-filed did not anticipate.

### What the workflow surfaced

**Loop 1.** Convergent panel veto on the original entry's plan:
- **Architecture: reject.** Role-fusion — granting Write to critics collapses the reviewer + author-of-record roles onto the same agent in the same invocation, dissolving the orchestrator chokepoint that today enforces path-discipline by construction.
- **Operations: rework.** Concurrency posture is a step-change, not an extension — the Write-holder precedent (`subagent-distiller`, `scope-mapper`, `frame-challenger`) runs sequentially; critics run three-in-parallel. Modal failure mode under outside-view: stale-session/wrong-path writes.
- **Product: rework.** Operator surface regresses (`critiques.md` silently changes meaning); thin-index is an unnamed schema; Defense 2 (auto-replan-on-self-modification) is an unconditional workflow tax to mitigate an unmeasured bias.

Routed to replan under new frame (parliament-with-clerk separation).

**Loop 2.** Candidate v2-C (orchestrator-as-sole-writer + byte-fidelity prose contract; drop aggregate; escalate recursion to operator) received 3x rework with five small actionable additions:
1. `critiques/INDEX.md` with pinned verdict vocabulary (product).
2. Delimiter-escaping rule + encoding/normalization spec (architecture).
3. Content-addressed envelope (sha256 header) for mechanical paraphrase detection (architecture).
4. Step 12 partial-read policy (operations).
5. Concrete operator action on self-modifying changes, replacing escalation-disclaimer (product).

Loop cap reached (2/2). Synthesis presented four shapes to the operator: v2-A (structured-return + verbatim-write), v2-C (the loop-2 candidate as-is), v2-C+ (v2-C with the five panel-named additions), v2-D (do nothing — null hypothesis named by frame-challenger).

### Decision pending

**The original entry's plan (loop-1 candidate) is not the right implementation.** Workflow surfaced this and the operator now has a four-way choice (see synthesis in [session artifacts](../../.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/)). The `🔨 implemented` cell remains empty pending that decision.

The honest finding the workflow produced about itself: the orchestrator's loop-1 routing collapsed three different lens-objections into architecture's vocabulary; the loop-2 frame-challenger caught this; the loop-2 recommendation (v2-C) is justified by per-lens objection-resolution rather than by the parliament metaphor. The recursion-bias discount factor on every panel verdict in this run is unknown — architecture explicitly disclosed status-quo bias on loop 1, and loop 2 may run the other way (toward approving changes that leave the architecture lens's surface alone).

### Cheapest experiment named in synthesis

To reduce the biggest uncertainty (whether the audit-faithfulness motive is unmeasured-bias-prevention): instrument three or four upcoming sessions with a manual diff between the orchestrator's transcript region and the persisted `critiques.md`. If zero meaningful paraphrases are found across four sessions, **v2-D (do nothing) is the right answer**. If even one is found, the motive is validated and **v2-C+ or v2-A** becomes the right answer. Cost: ~10 minutes of operator attention across four sessions over the next two weeks. No code change.

## The four candidate shapes

The workflow surfaced four distinct implementation shapes. The original entry's plan (loop-1 candidate) is *not* among them — it was rejected on frame.

| Shape | What it is | Loop-2 panel verdict | Cost | When to pick |
|---|---|---|---|---|
| **v2-D — do nothing** | Reject the motive as unmeasured-bias-prevention. Keep current orchestrator-paraphrase behavior. | Not panel-tested; named by frame-challenger as legitimate null hypothesis. | Zero. | If the cheap experiment returns zero meaningful paraphrases across 4 sessions. |
| **v2-C — orchestrator-as-sole-writer + byte-fidelity prose contract; drop aggregate** | Critics return prose between `<critique>...</critique>` delimiters; orchestrator persists bytes verbatim under a CLAUDE.md prose contract; per-lens file is the operator surface; no aggregate `critiques.md`. | 3× rework. Closer to right than loop-1 candidate but ships an undefined byte-fidelity guarantee. | One CLAUDE.md sentence + 3 short critic body sentences. | If you accept that byte-fidelity is enforced *behaviorally* and you want the minimum-cost change. |
| **v2-C+** | v2-C plus five panel-named additions: (1) `critiques/INDEX.md` with pinned verdict vocabulary, (2) delimiter-escaping + encoding/normalization spec, (3) sha256 envelope on each per-lens file, (4) Step 12 partial-read policy, (5) concrete operator action on self-modifying changes. | **Untested by panel** (loop cap reached). Inferred from the union of three "what would flip my verdict" lists. | ~4× v2-C. | If the cheap experiment validates the motive and you want the minimum-cost change *that addresses the loop-2 panel's actionable list*. |
| **v2-A — structured-return + verbatim-write + generated aggregate** | Critics return a typed structured object (verdict label + named sections); orchestrator writes per-lens files mechanically from the typed return; aggregate is a deterministic projection. | Not panel-tested directly; architecture lens preferred this in both loops. | Same scope as v2-C+ but with structured-return contract instead of prose contract. Strongest enforcement mechanism the panel surfaced. | If you want the strongest version, willing to define a typed return shape, and want provenance metadata to live in the artifact itself. |

## Why v2-C+ is not the obvious answer

The most tempting response to "v2-C got 3× rework, here are the five small fixes" is to ship v2-C+ and move on. Reasons that's not as cheap as it looks:

1. **Specification surface grows.** Five additions × small-but-real cognitive load = the orchestrator is holding more rules in context every Step 10. Each rule is itself a small prose contract that can drift, fail under attention pressure, or interact unexpectedly with the others. Loop-2 architecture's frame objection — *"byte-fidelity is a stack of properties (encoding, escaping, normalization, transcription, attribution); v2-C addresses one and leaves the rest undefined"* — applies *more*, not less, to v2-C+ because v2-C+ defines several layers explicitly and creates new contracts at each.

2. **The contract is still behavioral, not harness-enforced.** The sha256 envelope is the closest thing to a control (orchestrator computes hash, writes header), but *the same orchestrator* that's supposed to copy bytes verbatim is computing the hash. If it paraphrases-then-hashes, the hash matches and the contract passes silently. To be a real control, the hash check would need to run in a `PostToolUse` hook on the Write call — which is exactly upgrade [#3](../profound/2026-04-26-subagents-claim-writes-not-on-disk.md), which we deliberately did not co-ship. So v2-C+ is roughly *"v2-C with one more sentence we hope the orchestrator follows."*

3. **v2-C+ was not panel-tested.** Loop cap meant we never ran a panel pass on the integrated v2-C+. It was inferred from the union of three "what would flip my verdict" lists — the cheapest synthesis, not the strongest. Emergent issues from combining the additions are unmeasured.

4. **~4× the cost of v2-C, paying for a possibly-hypothetical problem.** If the cheap experiment (4 sessions of manual transcript-vs-file diff) returns zero meaningful paraphrases, v2-C+ is mitigation against an unmeasured failure mode. The frame-challenger's v2-D challenge stands.

5. **Modestly more files in the session.** One new INDEX file per session, plus a sha256 header line on each per-lens file. Ignorable in itself; named for completeness.

The honest summary: **v2-C+ is the right answer if the motive is real but you don't want to introduce a new agent (v2-A's recorder pattern), and you accept that the byte-fidelity contract is still behavioral until upgrade #3 lands.** Pausing without committing to it is the sound move.

## Adjacent finding — workflow docs are scattered and partly stale

Surfaced during the post-synthesis review of "where is the 12-step process documented?" The repo has partial docs across multiple files, no single source of truth, and one stale conflict that the top-level README still treats as authoritative:

| Doc | Purpose | Gap |
|---|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Authoritative 12-step spec — each step's action, hard gates, off-ramps, do/don't list. | An *instruction file for the orchestrator*, not a reader's README. No diagrams, no per-step "what it produces / what it filters for" breakdown. |
| [.claude/session-artifacts/README.md](../../.claude/session-artifacts/README.md) | Physical artifact layout — which file each step writes, lifecycle, the hard gate on Step 9. | Doesn't explain *why* each step exists or what failure-class it filters; just where outputs land. Tree diagram is also missing the loop-2 critique-rewrite shapes that show up in real sessions. |
| [workflows/architecture-review.md](../../workflows/architecture-review.md) | **A stale 7-step workflow that conflicts with CLAUDE.md's 12-step.** References a single `critic` agent (now the three-lens panel). | Wrong-and-tracked. Should be deleted or folded into a single workflow README that supersedes it. |
| [README.md](../../README.md) (top-level) | High-level pitch (three subagents, philosophy). | Predates the 12-step expansion. Says "a critic subagent" (singular). Points readers to the stale workflows file. |
| Agent files in `.claude/agents/*.md` | Each agent's individual contract — inputs, output shape, must/must-not. The *boundary* definitions per step. | Read individually they're rigorous; there is no map showing how they compose into the workflow. |

**The gap, named:** there is no single doc that, in one read, gives a reader *step → purpose → produces → reads → boundary with adjacent steps → which agent owns it*. CLAUDE.md is the closest but it is prescriptive, not descriptive.

This is a candidate for its own upgrade entry (a "workflow README that supersedes the stale workflows file and unifies what's currently scattered across CLAUDE.md, session-artifacts/README.md, and the agent files"). Captured here so it isn't lost; not in scope of this entry's resume.

## Resume conditions

This entry resumes (state advances past `⚙️ run-through-repo`) when **either** of:

1. **The cheap experiment returns a measured paraphrase incident.** Run the manual transcript-vs-file diff against the orchestrator's `critiques.md` output in 3–4 upcoming sessions over the next two weeks. If even one session shows the orchestrator paraphrased, abridged, or restructured a critic's verdict in a way that materially changed it, the motive is validated and the choice between v2-C+ and v2-A becomes live. Until then, the motive is hypothetical-bias-prevention.

2. **Upgrade [#3](../profound/2026-04-26-subagents-claim-writes-not-on-disk.md) (PostToolUse verification hook) lands.** If a harness-level write-verification primitive exists, the cost calculus on this entry shifts — the byte-fidelity contract gets a real detection primitive, and v2-C+ stops being "one more sentence we hope the orchestrator follows."

Resuming without one of those is paying complexity cost against a problem the workflow itself surfaced as unmeasured. The lab-as-discipline says don't.
