# Frame — `2026-04-27-critics-get-write-tool-impl`

## Revision 1 — 2026-04-27 (orchestrator)

### The user's framing (what was asked)

"Add `Write` to three critics so they persist verdicts themselves; decide whether to keep `critiques.md` as a thin index."

This frames the question as a **tool-grant + artifact-shape** decision. It implicitly optimizes for **audit-trail integrity** — the verdict the operator reads in `critiques/<lens>.md` should be the verdict the model produced, byte-for-byte, not an orchestrator paraphrase.

### Implicit optimization target

**Audit faithfulness.** The proposal's whole thrust — entry essence, motivation, "no more me-claiming-they-said-X" — is that the artifact stored as a critic's verdict should be authored by the critic. Audit faithfulness is the metric being maximized.

### Alternative optimization 1 — Orchestrator parsimony

A different framing: this is a question about **what the orchestrator should NOT have to do**. Today the orchestrator must (a) capture each lens's inline return, (b) parse it for verdict label, (c) transcribe the full body into `critiques.md`, (d) reconcile any formatting drift across lenses, (e) carry that text in its working context until Step 12 synthesis. This is five jobs, all of which are paraphrase-shaped, and all of which compound the orchestrator's context with prose it didn't author.

Under this framing, the question is not "should critics get Write" but "**what subset of orchestrator work survives a critic that writes its own file?**" Possibly: only step (a/b) — read each file, extract the verdict line. Steps (c–e) collapse. The aggregate file becomes optional residue.

This frame would make the **drop the aggregate** answer obviously correct (it is orchestrator-paraphrase work that no longer needs doing), and would surface a separate question the user did not ask: **should the orchestrator's Step 10 work also be reduced to file-reading and verdict-extraction, with synthesis (Step 12) reading the per-lens files directly?** If yes, `critiques.md` is dead.

### Alternative optimization 2 — Boundary: who is allowed to write what, where

A second framing: this is a question about **the trust boundary between agent and orchestrator**. Today, agents return prose; the orchestrator decides what becomes a persistent artifact. That asymmetry is itself a feature — it means the orchestrator's CLAUDE.md path-discipline rules are enforced at one chokepoint, not at every agent.

Granting `Write` to three agents widens that chokepoint. Each critic now writes to a path the orchestrator constructs (`<id>/critiques/<lens>.md`). If the session-id is wrong, malformed, or stale, three agents now produce three orphaned files in the wrong place, and the orchestrator no longer has a transcription pass in which to catch it.

Under this framing, the question shifts to: **what is the harness contract that ensures agent writes land where they're supposed to?** Options span instruction-level (today's proposal — agent body says "write to this path"), prompt-level (orchestrator passes a fully-formed write tool call), or hook-level (a `PreToolUse` hook validates the path matches the active session-id). The user's framing assumes instruction-level is sufficient. That assumption is the load-bearing one.

This is also the frame where **upgrade #3 ("Subagents claim writes not on disk")** gets pulled into scope: that entry's verification hook is the natural complement to this one, and the two should ship together or neither.

### Alternative optimization 3 — Recursion / self-modification hygiene

A third framing: this is a question about **a system modifying its own review apparatus**. The critic-panel is the mechanism by which this stack catches its own design errors. A change to the critic-panel cannot be reviewed by the same critic-panel without a structural conflict-of-interest — the very lenses being modified are the lenses asked whether the modification is sound.

Under this framing, the question is not whether the change is good but **whether the workflow has any defense against critics rubber-stamping changes that expand their own surface**. The classifier's recursive-frame note already flagged this: "critics tend to approve self-improvements that increase their own authority/surface." The frame would push us toward an external check (operator override, a `replan` rule that fires automatically on self-modifying changes, or a second-opinion run via the as-yet-unbuilt shadow-comparator from upgrade #5).

### What the user is implicitly accepting

By framing this as **extend + tool-grant**, the user implicitly accepts:

- That instruction-level write-path scoping is sufficient (no hook needed).
- That session-id passing is a small implementation detail, not a contract.
- That a panel reviewing a change to itself is a legitimate review.
- That the aggregate `critiques.md` is reversible (keep-or-drop is XS-cost).

Each of these is challengeable. The frame-challenger should push on at least one of them in Step 8.

### Frame I will carry into Step 9 (generator)

I will carry **Alternative 1 (orchestrator parsimony)** as the working frame, with the **boundary** concern (Alternative 2) named as the constraint that prevents Alternative 1 from being applied naively. In short: the question is not "should critics write" — it is "what orchestrator paraphrase work goes away when critics write, and what new boundary-enforcement work appears in its place."

The user's audit-faithfulness framing is preserved as a sub-goal: it is the *reason* the new shape is worth its boundary cost.

## Revision 2 — 2026-04-27 (orchestrator, post-loop-1)

### Why revision 2

Loop 1's critic-panel produced 1 reject (architecture) + 2 reworks (operations, product), with **convergent frame objections** across all three lenses. The convergence — not any individual verdict — is the signal that Revision 1's frame is wrong. Per Step 11 routing, frame-level vetoes go to replan; the architecture lens explicitly named the frame as wrong.

### The frame insight from loop 1

**The critic-panel is a parliament with a clerk, not a pipeline with a recorder.** A parliament's load-bearing property is *vote-independence among voters*, with a *recording clerk who is structurally distinct from any voter*. The pipeline frame (Revision 1) optimizes for paraphrase-fidelity-and-throughput; the parliament frame optimizes for vote-independence-and-clerk-separation. These are different verbs (record vs. isolate) and they pick different solutions.

Specifically, the three convergent lens-objections in loop 1 all point at this single insight from different angles:

| Lens | Convergent complaint | Parliament-frame restatement |
|---|---|---|
| Architecture | Role-fusion: the same agent is both reviewer and author-of-record. | Voter and clerk should not be the same person. |
| Operations | Sequential-Write-holder precedent does not transfer to parallel-Write critics. | A clerk taking three votes in parallel is a different mechanism than a clerk taking one vote at a time. |
| Product | The frame is orchestrator-internal; the operator-facing surface is unnamed. | The clerk's record is the public-facing artifact; its shape is a stakeholder concern, not internal scratch. |

### What the user is implicitly accepting (revised)

By framing this as **extend + tool-grant**, the user implicitly accepts:
- That instruction-level write-path scoping is sufficient (no hook). **Loop 1 challenged this; operations rated A2 the most load-bearing assumption.**
- That session-id passing is a small implementation detail, not a contract. **Loop 1 challenged this; outside-view rated this the modal failure mode.**
- That a panel reviewing a change to itself is a legitimate review. **Loop 1 challenged this; no defense in current frame; Defense 2 in candidate was a patch, not a frame fix.**
- That the aggregate `critiques.md` is reversible (keep-or-drop is XS-cost). **Loop 1 challenged this; product flagged the file silently changing meaning.**
- **(NEW, surfaced loop 1)** That the audit artifact's *author* is a meaningful property worth optimizing for at all, vs. the audit artifact's *byte-for-byte fidelity to the agent's reasoning*. The architecture lens explicitly argued these are equivalent on every property except attribution metadata.

### Frame I will carry into Step 9 (loop 2 generator)

**Parliament-with-clerk separation, optimizing for vote-independence-and-byte-fidelity.** The question is no longer "should critics get Write" — it is "**given that vote-independence and byte-fidelity are both load-bearing, what is the cheapest shape that delivers both, and where does the work of recording go?**"

This frame admits two strong candidates and rejects the original:
- **Candidate v2-A: Structured-return + orchestrator-verbatim-write.** Critics return a typed structured object (e.g., named sections + verdict label, returned as the inline message). The orchestrator persists the bytes verbatim with no paraphrase. Vote-independence preserved by construction (no filesystem path between critics). Byte-fidelity preserved by mechanical copy.
- **Candidate v2-B: Dedicated `recorder` agent (Write-only) + critics return prose.** Three critics run in parallel and return prose; a serial `recorder` agent reads the orchestrator's record of each return and persists each lens's bytes to its own file. Voter ≠ clerk by agent identity. Reuses the Write-holder precedent (single-author per file, sequential).
- **Original candidate (loop 1): rejected on frame.** Granting Write to critics fuses voter and clerk; defenses are instruction-level patches on a structural problem.

The audit-faithfulness motive from Revision 1 is preserved as a sub-goal: it is the *reason* the new shape is worth its complexity. The clerk-voter separation is the *mechanism* that delivers it without the parliament-frame failure modes.

### Two-loop cap reminder

Per CLAUDE.md, two full loops max. After loop 2's panel, the orchestrator must synthesize regardless of verdict. If loop 2 panels also veto, the synthesis names the disagreements rather than continuing.
