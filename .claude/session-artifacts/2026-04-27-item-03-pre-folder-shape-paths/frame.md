# Frame — item 3 (pre-folder-shape `.md` references)

## Revision 1

### How the operator framed it (implicit)

*"Pick up the third critical item; write the plan you think is best; route through the pipeline."*

The operator's framing presumes:
1. Item 3 is a discrete unit of work, comparable in shape to items 1 and 2 (both already "picked up").
2. The right move is to *plan and execute* item 3, not to question whether item 3 is the right unit of work.
3. The pipeline is being asked to **stress-test the plan**, not to **re-examine the punch list**.

What the operator is implicitly optimizing for: **predictable, unsurprising, sequential closure of an enumerated cleanup list.** Punch list = bug tracker. Each item = ticket. The operator wants tickets closed, in order, with the pipeline catching mistakes in any individual ticket's plan.

### Reframe 1 — Substrate, not symptom

The 11 broken references are **not the bug**. They're the *symptom* of a pattern: *whenever the repo's structural conventions change (folder shape, path style, slug shape), every prior reference to a primitive becomes a stale path.* The folder-shape migration on `c2fe604` was a structural change; the punch-list items 2, 3, 5, 7, 8, 10, 12, 13 are all "downstream stale references from prior structural changes." They differ only in *which* change they're downstream of.

**Reframed question.** Is the right intervention here:
- (a) Patch the 4 active broken links from this particular structural change (the plan as drafted).
- (b) Add a structural primitive that prevents *this class* of stale-reference accumulation across future structural changes (a link-validity check, a slug-rename hook, a "redirects" file).
- (c) Both — patch *and* add the primitive, with item 3 used as the exemplar to motivate the primitive.

Option (b) reframes from *bug fix* to *primitive-introduction*. The plan as drafted is option (a). Option (a) and option (b) optimize for different things:
- (a) optimizes for **closing this specific ticket cleanly with minimum blast radius**. Predictable, fast, reversible.
- (b) optimizes for **not having a punch list of this kind ever again**. Slower, larger blast radius, harder to reverse.

The drafted plan defaults to (a) without naming (b) as an option. That's the frame-shift the user did not perform.

### Reframe 2 — The session-artifact policy is the actual decision

The plan presents itself as 4 mechanical edits. But its load-bearing move is the second-order one: **declaring** that "session artifacts are inviolable except for privacy" is the binding rule. That is a policy with implications far beyond item 3:
- It binds item 2 (depth bugs in session artifacts can't be fixed).
- It binds future items (items 7, 12 mention session-artifact occurrences and explicitly leave them).
- It binds *all future* mechanical-error sweeps.

If the policy decision is the real ask, item 3 is a **terrible carrier** for it — too small, too local, framing-buried in the appendix of a plan focused on link targets. The right carrier would be a top-level rule, written into [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md) or [`CLAUDE.md`](CLAUDE.md), reviewed and committed as a constitutional change rather than an implementation detail.

**Reframed question.** Is the right intervention:
- (i) Bake the strict policy into item 3 silently (plan as drafted).
- (ii) Pull the policy out of item 3 entirely; do the 4 mechanical edits without taking a stance; queue the policy decision as a separate constitutional question.
- (iii) Make item 3 *primarily* about the policy decision; the 4 edits are the consequence, not the goal.

The drafted plan does (i). The classifier flagged this as "refactor with hidden replace inside it." The frame-bias is real.

### What the user is implicitly optimizing for, named

**Closure.** "First and second critical has been picked up. Pick up third." The verb is *pick up* — a worklist verb. The operator wants the worklist to advance.

### Alternative optimization

**Avoid laundering policy decisions through implementation tickets.** A worklist-advance frame treats every item as the same shape; but item 3 carries a policy decision in its plan body that items 1 and 2 do not. Recognizing that asymmetry costs cycle time on item 3 in exchange for not silently committing to a rule the operator hasn't approved.

### Frame I'm carrying into the rest of the workflow

A *split* frame — and I'm naming the split rather than collapsing it:

- **For the 4 active-surface edits:** mechanical refactor frame is correct. Apply the behavioral check the classifier asks for (post-edit links resolve to intended targets).
- **For the session-artifact restraint:** treat as an open policy question. Don't bake the strict reading into item 3's done-conditions. Either (a) operator-confirms the strict reading explicitly before this commits, or (b) item 3's plan stops short of declaring the policy and instead names "session artifacts not touched in this commit; policy on whether they ever should be is item-N." Either is fine; both are better than silent baking.

This is the frame the generator (step 9) must produce against. The frame-challenger (step 8) must challenge whether even *this* split is wrong — e.g., whether the policy is so trivially settled by `5108ed3` that pulling it into a separate question is overhead.

### Note on operator's "best you think" wording

"Write your plan how its best you think to approach this item" is permissive — operator invites my judgment, not just my execution. That permission is exactly what makes the reframe legitimate. If the wording had been "execute item 3 per the plan I gave you," reframing would be insubordinate. Here, it's responsive.

## Revision 2

### Why a revision is needed

Loop 1's candidate was vetoed convergently by all three critic lenses (architecture, operations, product) — see [`critiques.md`](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/critiques.md). The convergent frame-level objection: **the candidate over-engineered a 4-line cleanup into a multi-commit choreography that bills the operator for findings the workflow generated.**

This is the failure mode upgrade [#11 convergent-frame-objections-as-replan-signal](upgrades/normal/2026-04-26-convergent-frame-objections-as-replan-signal/README.md) names. Three lenses agreeing at the frame level is high signal that the *frame*, not the candidate, is wrong.

### What was wrong about Revision 1's frame

Revision 1's "split frame" claimed to discriminate between substance (4 mechanical edits) and policy (session-artifact immutability) and route them to different mechanisms. The critics jointly demonstrated that:

- The split was **a deferral dressed as discrimination** ([challenges.md](.claude/session-artifacts/2026-04-27-item-03-pre-folder-shape-paths/challenges.md) already named this; loop 1 attempted to honor the challenge by inventing commit B but that just *moved* the deferral into a new artifact class).
- The right unit of analysis is not commits-over-time but **the file graph after the dust settles** (architecture lens).
- The right operational frame is **WIP accounting**: don't add WIP to close WIP (operations lens).
- The right product frame is **respond to the actual ask**: a 5-word "pick up the third critical" warrants a 5-edit response, not a 3-commit + open-question response (product lens).

### Revision 2 — the collapsed frame

**Item 3 is a 4-edit cleanup. The orchestrator's job is to ship the 4 edits cleanly and surface, but not deliver, the policy concern that the workflow noticed.**

Concretely:
1. **Substance.** Apply the 4 link-target edits to the 2 active-surface files. Single commit. Reverts cleanly.
2. **The line-138 parenthetical, the "child of `c2fe604`" commit-message framing, the 5th edit, the freeze test, the redirect file** — all are workflow-generated scope. Drop all of them.
3. **Done-when #5 is deleted** (it was doing hidden policy work); its absence is named in the commit message in one sentence — *not* as a policy declaration, *as a note that the workflow surfaced a question the operator may want to address separately*.
4. **The session-artifact policy question goes back to the punch list as a new line item** (the operator chose the punch list as the intake surface; respect it). The orchestrator does not convert the concern into a deliverable on the operator's desk.
5. **Item 1's pending restyle** is acknowledged in one sentence in the plan's revision history but not architected against. If item 1 lands and the 4 lines need restyling, item 1's session does the restyle; item 3 does not pre-defer it as "commit C."
6. **No new tooling.** The outside-view's modal-failure prediction is acknowledged; no mitigation is added in this commit. If the prediction comes true within 3 months, the punch list will reflect it as a new item.

### What this frame is implicitly optimizing for

**Operator closure with honest minimum surface.** The operator asked for an item to be picked up. The frame returns: 4 edits applied, plan corrected, one new punch-list line item that they can ignore or pick up later. Nothing else.

### What this frame is *not* optimizing for

- "Architectural cleanliness" of the commit graph (architecture lens's preferred frame is honored only insofar as it doesn't add work).
- "Risk-reduction against fence leakage" (operations lens's preferred frame is acknowledged; mitigation declined as out of scope).
- "Constitutional clarity" of the immutability rule (product lens correctly observed: the workflow can name the question; only the operator can decide it).

### Frame I'm carrying into the rest of the workflow

A **collapsed frame** — single commit, minimum surface, workflow-generated concerns surfaced as new punch-list items rather than as deliverables. This is the frame the v2 candidate at step 9 must produce against.

### Why this revision should not be vetoed for "ignoring valid critic concerns"

The critics' lens-specific concerns are valid; the candidate's response is to **route them to the right surface**, not to incorporate them into this commit. The redirects-file alternative, the link-checker tooling, and the policy declaration are real ideas that deserve their own tickets. Treating them as new punch-list items is responsive; absorbing them into commit A is what loop 1 did wrong.
