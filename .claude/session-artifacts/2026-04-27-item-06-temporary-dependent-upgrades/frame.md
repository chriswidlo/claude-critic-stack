# Frame — item 06 temporary-dependent upgrades

## Revision 1

### How the user framed it

> Two upgrade entries reference a `temporary/` directory that exists only on a separate branch. Pick (a) restore, (b) mark superseded, or (c) park with `⏸️` and resume condition.

The user's framing is a **menu-of-three cleanup choice**. It treats item 6 as a discrete punch-list entry to be closed by selecting one option and committing the result. The pre-pipeline lean (c, with b close second) is offered as a prior to be tested, not a verdict.

### What the user is implicitly optimizing for

**Local consistency on `main`.** Every reference in `main`'s tree should resolve to something true: either the file exists, or the entry's body honestly says it doesn't. The optimization is reader-facing: a future reader of the LEDGER or either entry should never hit a dead reference without an explanation immediately adjacent.

This is a perfectly reasonable optimization, and (a)/(b)/(c) all satisfy it differently. But it is *one* optimization, not the only one.

### Alternative framing the user did not use

**The question is not "which of three options closes item 6," but "what does item 6 reveal about a missing convention in the lab itself?"**

Two upgrade entries depend on resources outside `main`. The lab has zero written rules about whether that's allowed, what it means, how it's tracked, or what the contract is between an entry and its dependencies. Item 6 is the first time the gap fires; it will fire again. Each future research session that lands on a worktree branch (the `agentic-engineering-research` precedent) and produces upgrade entries that reference its outputs reproduces this exact failure mode.

Under this frame, the right output of item 6 is **not** a choice between (a)/(b)/(c) but a written **dependency-contract rule** ("entries that reference resources outside `main` must declare the dependency in a structured field, and the LEDGER row's state must reflect the dependency's reachability") — applied retroactively to the two affected entries (which auto-resolves to whichever of (a)/(b)/(c) the rule prescribes), and forward to all future entries.

### What this alternative is implicitly optimizing for

**Failure-mode-recurrence prevention.** The lab tradition is *honest negation* — name what went wrong so it doesn't repeat. Picking one of (a)/(b)/(c) without surfacing the absent rule fixes today's symptom and leaves the next instance to be hand-resolved. Writing the rule fixes today's instance *and* the class.

The cost is real: writing a convention is a higher-effort move than picking from a menu, and it expands item 6's scope past what the punch list authored. There's an argument that the punch list's own structure (one self-contained item at a time, no scope creep) is itself a discipline worth preserving.

### Honest friction with the user's framing

The user's framing is not weak — it is *under-scoped*, deliberately or accidentally. The plan document explicitly says option (c) "was not on the punch list" and that this is "the first item where the honest-negation discipline is itself a frame variable." Both observations point at the alternative frame above without quite naming it. The plan is one inferential step from saying "this question is not about (a) vs (b) vs (c); it's about the dependency contract that the lab has never written down." The reframe makes that step explicit.

If the operator pushes back ("no, just close item 6, don't expand scope"), respect that — the local-consistency frame is legitimate, and the alternative frame can become its own future entry rather than swallowing this one. But the workflow has to surface the choice, not silently default to the user's framing.

### Provisional anchor for downstream steps

Both frames are live. Steps 3–8 should test which one the canon, the outside view, the scope-map, and the frame-challenger best support. Step 9 must explicitly address the frame-level objection: *if the recommendation is one of (a)/(b)/(c), why is writing a dependency-contract rule the wrong move; if the recommendation is to write the rule, why is closing item 6 with the rule's first application the wrong move.*

## Revision 2 (post-loop-1 replan)

### What loop 1 surfaced

Three lens critics independently rejected the candidate's bisection-into-mixed-mode approach (b′ — wrap migration sections in blockquote, leave executable text in place, keep `🌱` state). They converged on a sharper structural fact that Revision 1 did not name:

> **The LEDGER already has a partition for non-executable rows: Group E ("Observations — no immediate action"). The two affected entries (#18b agentic-engineering-reference-library, #18g living-poweruser-knowledge-module) sit in Group D ("Repo hygiene & conventions"), which is structurally executable. Either the entries belong in Group E (physical relocation), or they need to be physically removed (eviction / extraction / migration-section deletion). The candidate tried to invent a third governance regime inside Group D and that is what the panel rejected.**

### What the user is implicitly optimizing for — corrected

Not "make the row text accurate" (Revision 1's reading) but **"keep each LEDGER group internally consistent — Group D rows are executable; Group E rows are observational."** Under this reading, the question stops being "which token + prose combination is most truthful" and becomes "which group should each entry live in, and what does each entry's body look like in that group."

### The revised option set

The four loop-1 options (a/b/c/d) and the eviction/graduation frame all addressed *what to say about the entries*. Loop 2 reframes around *where the entries live and what gets physically removed*:

- **(e) Relocate to Group E.** Move both entries' LEDGER rows from Group D to Group E. Group E's contract ("no immediate action") natively absorbs the non-executability. Entry bodies still need editing — specifically, the migration-plan sections must be deleted or replaced with a one-paragraph negation note — because Group E rows do not carry phantom imperative prose either. But the *primary* move is the relocation.
- **(f) Extract-and-delete.** Split each entry: keep the parent-shape narrative as a new entry whose body has no `temporary/` dependency; delete the migration-plan-bearing entry entirely. Two entries become two entries with cleaner aggregates. More disruption than (e); strictly cleaner if the bodies cleave naturally.
- **(g) Delete-migration-sections-only, keep entries in Group D.** Per product critic's path-to-approve (ii): keep the entries where they are, but physically delete the migration sections (replace with one-paragraph negation note). Row 18b's `Implement as` cell rewrites to a Group-D-shaped imperative (e.g., "Re-derive migration plan when worktree branch graduates" — still imperative, still future-tense). The state cell stays `🌱`.

### The frame-level question loop 2 must resolve

Among (e), (f), (g): which best honors *both* the LEDGER-partition invariant *and* the operator's parent-narrative-preservation preference?

- (e) honors the partition cleanly; preserves narratives; minimal disruption to entry-bodies beyond migration-section removal.
- (f) is the architecturally purest move; highest disruption; loses the linkage between parent-shape and original-deposit context.
- (g) keeps the entries in Group D, requiring that Group D's executable-imperative invariant be honored — which it can be, *if* the new `Implement as` text is genuinely imperative (action against a future condition) rather than meta-narrative about the row's status.

### Carry-forward objection for loop 2 generator

The generator must not re-introduce mixed-mode bisection inside a single Group-D entry. The convergent panel-frame objection is: each entry, in whatever group it lives in, must satisfy that group's invariants without overloading the state vocabulary.
