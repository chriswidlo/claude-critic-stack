# Frame — upgrades lab design

## Revision 1

### How the user posed the question (verbatim shape)

"What is the structure of `upgrades/` such that it is, from day one, a real R&D lab?" — followed by eight numbered sub-questions covering document types, disciplines, maturity ladder, cross-references, methods, failure archive, naming, integration. Plus: design for the mature future state, no phase-one-evolves-later, global view first, no compromises.

### What the user is implicitly optimizing for

**Total-rewrite-cost minimization.** The operator's stated frustration is "scope was too small, didn't zoom out, kept getting rewritten." So the optimization is: pay maximum upfront design cost in exchange for never rewriting the lab's structure later. Mature-from-day-one is a *cost-allocation strategy* — front-load it.

A close second: **structural coherence with the existing stack.** The lab is not free-standing; it is institutional memory for a system that already has CLAUDE.md, the seven-capability taxonomy, the workflow, the canon. The lab must fit this without reshaping it.

### Frame bias inherited from classifier (carry forward)

`new` already biases toward over-design; "mature from day one" doubles it. Honoring the operator's stated preference is correct — but the candidate must explicitly name which structural commitments are *reversible* (e.g., specific subfolder names) vs. which *lock in* (e.g., the maturity-ladder semantics, the document-type set). Reversible commitments can be made now without violating the no-rewrite constraint; locking commitments need the strongest justification.

### Alternative optimization the user is *not* naming

**Time-to-first-useful-entry** — i.e., how fast does the lab start accreting real R&D value, vs. how long does the structure-design itself absorb attention before the first observation lands. The operator's framing collapses this: they assume mature design has no time cost relative to the lab's eventual lifespan. That's true if the lab runs for years; it's false if the operator's own enthusiasm or the stack's relevance fades within months. The candidate should name the bet on the lab's longevity as an explicit assumption.

A second alternative: **epistemic rigor vs. creative free-form.** The operator earlier said the lab is "our R&D area" with "unlimitedly long doc and everyone is allowed to write anything they want." Free-form writing tension-loads against the schema/maturity-ladder/cross-reference machinery. A real R&D lab needs both — the lab notebook is unstructured, the published paper is rigorous — but the design must say where each lives, not collapse them.

### What "mature from day one" actually requires (decoded)

Not: every artifact at full polish, every discipline pre-populated.
Yes: the *structural commitments* (document types, maturity ladder, cross-reference primitives, failure-archive shape, integration touchpoints) defined and load-bearing, such that any future addition lands in a slot the structure already anticipates.

This distinction matters: the operator wants the *frame* mature, not the *content* mature. The first artifact (the lab's own design, per self-application) is allowed to be raw; the slot it lands in must be the right slot from day one.

### Open frame questions to surface in scope-map and challenges

1. The operator named four explicit gaps in the requirement (precedent? cadence? scale? failure-archive scope?). The candidate must address each.
2. The name `upgrades` is provisional. Naming itself is a frame question — the chosen name shapes what the operator perceives as belonging there. Frame-challenger should test the name.
3. The seven-category capability taxonomy was agreed in conversation but is not yet on disk anywhere except this session. The lab's relationship to that taxonomy (anchor? overlay? orthogonal?) is a frame decision the candidate must make.
4. The operator added a new item — `scope-projector / maturity-extrapolator` — which is itself the kind of capability that would have changed *this* design's trajectory if it had existed. That's a self-referential signal worth surfacing.

### What I am not yet committing to

The candidate. Per workflow, generation comes after canon, outside-view, repo-scan, distill, scope-map, frame-challenge.

## Revision 2

Triggered by Step 10 critic panel: all three lenses returned `rework`, with two frame-level objections (architecture, product) converging on a single underlying problem.

### What the panel converged on

**The previous frame designed too much new structure.** Architecture: the lab is structurally a capability-overlay on `.claude/session-artifacts/`, not a peer module. Product: the operator's problem is "have somewhere I can write that doesn't punish me for writing," not "design a structure that survives." Operations: the survival controls of the previous frame were uninstrumented and contradictory — paper rigor.

The convergent reading: **less new structure, more accommodation of what already happens; what little new structure does exist must have actually-running controls, not paper ones.**

### What the operator is implicitly optimizing for (revised)

The optimization target stays "no rewrite" — that has not changed. What changes is the *theory of how to achieve it*. Revision 1 said: design every dimension at full fidelity now to forestall future rewrites. Outside-view data and the panel say: that strategy fails at 85–95% over 24 months because rewriting becomes inevitable as content reveals structure-content mismatches.

Revised theory: **"no rewrite" is achieved by committing to as few primitives as possible, making those primitives extremely simple, ensuring every other apparent structure is a view over them, and instrumenting the controls that catch mismatches early enough to act on before they accumulate.** The locking-dimension count drops from 4 to 1–2; everything else (types, maturity ladder, disciplines, cross-reference vocabulary) becomes views/tags over the primitive — additive, not locking, not rewrite-forcing.

This honors the operator's "no compromises" constraint by interpreting it as "no rewrite of accumulated content" — not "no compromise on commitment count." Smaller commitment surface ≠ less commitment to durability; it is *how* durability is bought.

### The two locking dimensions under the revised frame

1. **Stable ID scheme.** Slug-based logical IDs decoupled from filesystem paths. Every entry gets a slug at creation; cross-references use slugs. Filenames, paths, subfolders are all reversible — slugs survive. Single primitive; designed once.

2. **Capture/promotion primitive.** Session-artifacts already have a promotion shape (exemplars/). The lab generalizes this: any session artifact, any inbox entry, any operator note can be promoted into the lab by a single operation that assigns it a slug, an entry type tag (initially small set), and a maturity tag (initially binary: `raw` vs `matured`). No new schema. The lab inherits session-artifact form.

Everything else — extended document types, fine-grained maturity ladder, cross-reference vocabulary, disciplines, naming conventions — is **declarative metadata layered on top**, additive without rewrites.

### Capture-first as a locking concern

Per product critique: the capture path must work in <30 seconds for low-stakes thoughts, otherwise the operator silently reverts to writing in `pages/` and the lab stays empty. Specifically: `lab/inbox/` (or equivalent) accepts entries with only a slug and a date. No type, no maturity, no discipline required at capture time. A separate promotion pass (curator agent or operator review) imposes structure later, *if and when* the entry earns it.

This dissolves the lab-vs-backlog tension: an inbox entry has been "processed" by virtue of being captured with a slug, but it has not been "structured." The structuring happens at promotion, not at capture.

### Operational controls as required design outputs

Per operations critique: the day-60 falsifier, the freeze break-glass, the curator-bootstrap path are *not* §Tradeoffs concessions; they are required deliverables of the next candidate. Specifically, the next candidate must include:

1. A named, runnable script for the meta-vs-content commit ratio.
2. A break-glass protocol for in-quarter revision of any locking dimension.
3. A decision (not a deferral) on the curator-bootstrap path: build it before any entries land, or commit to a manual write-protocol with no curator-as-locking, or write a minimal lint-check as bootstrap stand-in.

Without these three, the candidate is not approvable under the operations lens regardless of frame-level coherence.

### What the revised frame keeps from Revision 1

- The retrofit-onto-extant-content frame (12 backlog items + plans/ + frame revisions form prior corpus).
- The time-box (day 7, day 14, day 60) — but instrumented this time.
- The reversibility pre-commitment (quarterly review with named triggers).
- The self-application requirement (first lab entry is the lab's design itself).

### What the revised frame drops from Revision 1

- Document-type set as a locking dimension. Now a starter tag set (small, additive, reversible).
- Maturity ladder semantics as a locking dimension. Now a starter tag set with two states (raw/matured) and operator-or-curator-extensible per type.
- Cross-reference vocabulary as a locking dimension. Now a single primitive (`relates_to: [<slug>]`) with optional richer relationships layered on top — refute/supersede/builds-on become tag-on-relation, not separate field types.
- Three-port integration protocol. Now one operation: promote.
- The rename `upgrades/` → `lab/` as a Step-9 position. Now a Step-12 deferred decision per operator's earlier explicit naming-delegation, with a one-week trial proposed but not imposed.

### The frame-level objection the next candidate must address

**The lab's value comes from the slug primitive + capture-first surface, with everything else being commentary that can be refactored without rewriting accumulated content.** The next candidate must show that this is true — not just claim it — by demonstrating that adding a new document type, renaming the maturity ladder, or reorganizing disciplines does *not* require touching any prior entry's content. If the demonstration fails, the frame is wrong and another revision is needed.
