# Decision log — `2026-04-27-critics-get-write-tool-impl`

## Step 10 verdict (loop 1)

| Lens | Verdict |
|---|---|
| Architecture | reject |
| Operations | rework |
| Product | rework |

## Step 11 routing decision (loop 1 → loop 2)

Step 10 verdict was architecture = reject (frame-level), operations = rework (frame + design), product = rework (frame + design); **replan**; routed to step 8 (re-run frame-challenger under the convergent-frame insight).

Reason: all three lenses produced frame-level objections that converge on a shared structural complaint — the candidate's `extend` framing treats a category change as an extension. Per Step 11 routing rules, when the veto is frame-level, return to step 7 or 8. Choosing step 8 (frame-challenger) because the new frame insight is sharp enough that re-running scope-mapper without re-challenging first would re-anchor on the old frame.

The new frame insight to carry into the re-challenge: **the panel is a parliament with a clerk, not a pipeline with a recorder.** This insight names a different optimization target (clerk-voter role separation) than the working frame (orchestrator parsimony) and reorders the candidate space:
- "Add Write to critics" becomes a *worse* answer because it fuses voter and clerk.
- "Structured-return + orchestrator-verbatim-write" becomes a *better* answer because it preserves the chokepoint.
- "Dedicated recorder agent" becomes the *strongest* answer because it makes the role separation explicit.

A new `## Revision 2` block will be appended to `frame.md` before the re-challenge.

## Step 10 verdict (loop 2)

| Lens | Verdict |
|---|---|
| Architecture | rework |
| Operations | rework |
| Product | rework |

Step 10 verdict was 3x rework on candidate v2-C; **synthesize per loop cap** (CLAUDE.md: cap at two full loops; past that, escalate to synthesis with the disagreements named). Routed to step 12.

The three loop-2 reworks are individually actionable (small, concrete, additive) and convergent on a shared shape: v2-C is closer to right than the loop-1 candidate, but ships an undefined byte-fidelity guarantee, no detection primitive, and an under-served operator surface. The five additive fixes named in `critiques.md` (index file; delimiter+encoding spec; content-addressed envelope; partial-read policy; concrete operator action) constitute a "v2-C+" candidate that the workflow's loop-cap precludes panel-testing. Synthesis presents this to the operator as a decision rather than a recommendation.
