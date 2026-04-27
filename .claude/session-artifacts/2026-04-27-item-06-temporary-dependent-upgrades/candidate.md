# Candidate recommendation — item 06 temporary-dependent upgrades

## Position

**Pick a hybrid of (b) — call it (b′) — applied surgically:** mark only the *executable migration sections* of each entry as superseded with a brief honest-negation note pointing to the worktree branch; preserve each entry's parent-shape narrative; rewrite LEDGER row #18b's `Implement as` cell to a one-line redirect to the entry body's "Status" header rather than a phantom migration plan.

Reject (a), (c), (d), and the graduation-frame eviction. Reasoning per option below.

## Addressing the frame-level objection (graduation frame)

The frame-challenger asserts: *the entries do not belong on `main` at all, because their dependencies do not resolve from `main`*. This is a serious challenge. I am answering it, not deflecting it.

The graduation frame is correct **if and only if** the LEDGER is contractually a *canonical-executable* index — every row must be actionable from `main`'s tree alone. It is wrong if the LEDGER is a *reflective-narrative* index — rows record ideas whose execution may live elsewhere or in the future.

Evidence from the existing repo argues for the reflective-narrative reading:

1. [`upgrades/LEDGER.md`](../../../upgrades/LEDGER.md):3 self-describes as *"the single ranked queue across all four tier folders"* — a *queue*, i.e. a holding structure for not-yet-executed work, not an executable index.
2. The lifecycle states `🌱 created` and `🔬 spiked` exist precisely to admit captured-but-not-executable ideas. Row #1 (Critics-get-Write) currently sits at `⚙️ ⏸️` — captured, partially advanced, paused on an external condition. The LEDGER already tolerates non-executable rows.
3. Many entries on the LEDGER reference future work, hypothetical dependencies, or conditions outside the repo (e.g. row #19 *"Memory and lab are the same primitive"* explicitly says *"No build. Open question to be answered by a future entry"*). If the canonical-executable reading governed, row #19 would also be evictable; clearly nobody intends that.

Therefore: the LEDGER is reflective-narrative; the graduation frame is built on a false invariant; eviction is the wrong response.

**However**, the frame-challenger's deeper point survives the rebuttal: even in the reflective-narrative reading, the *current entry bodies* on `main` are dishonest in a way row #19 is not — they describe specific filesystem operations against paths that do not exist on `main`. That dishonesty is what (b′) targets surgically: rewrite the *executable* parts (which the canonical-executable reading would govern) to match reality, while leaving the *narrative* parts (which the reflective-narrative reading admits) intact. The graduation-frame objection is dissolved by recognizing that these entries are mixed-mode — partly canonical-executable (the migration plan), partly reflective-narrative (the parent shape) — and applying the correct discipline to each part.

## Why not (a)

- Outside-view base rate: ~30% zombie risk because the asset would now exist in two places. Flagged explicitly: *"defensible only if the asset is genuinely needed on `main` for reasons independent of these two entries. If the only reason to restore is to fix the references, you've solved a documentation problem with a structural change — wrong tool."*
- Canon: SRE ch. 23 (branching policy) — *"branches in this discipline don't merge back."* Restoring `temporary/` from the worktree branch onto `main` is the explicit anti-pattern.
- Source-of-truth ambiguity: `agentic-engineering-research` is the branch's name for a reason; merging its content back without first deciding whether the branch becomes archive-only invites the divergence problem the librarian named.

## Why not (c)

- Outside-view base rate: ~70% zombie risk. *"Personal-KB deferral mechanisms have a poor track record of producing resumption."*
- Structural mismatch: the `⏸️` modifier sits on top of a *reached* state ("⚙️ ⏸️" = paused while running through repo). Both target entries are at `🌱`. A `🌱 ⏸️` row reads as "captured, then immediately paused" — semantically empty. The lab has one `⏸️` precedent (item #1, at `⚙️`); generalizing to a captured-and-paused row over-extends a thin convention.
- Canon: SRE branching policy frames the parked-state as the position the discipline *refuses to recognize* — either the work belongs on main or the references must be cut. (c) is the position SRE explicitly rejects.

## Why not (d)

- Outside-view base rate: ~80% the rule does not survive — *"single-instance rules in solo repos tend to be forgotten or routed-around within months."*
- Canon: Anthropic portfolio principle — *"approach and resource allocation will rapidly adjust"* — pushes against locking in a general convention from a sample size of two.
- Punch-list discipline conflict (per scope-map): the punch list explicitly says *"tackle one item at a time"*. (d) writes a new convention; that is scope creep by the punch list's own definition. Honoring (d) requires the operator to override their own punch-list discipline, which is a heavier lift than the cleanup item is worth.

## Why not graduation-frame eviction

- The LEDGER is reflective-narrative (evidence above), so the invariant the eviction relies on does not exist.
- Eviction destroys the parent-shape narratives, which the operator has consistently flagged as load-bearing across the punch list and plan document.
- Eviction also conflicts with the lab's stated *honest negation* doctrine — the doctrine asks for ideas to be *named-as-dead* rather than *deleted*. Eviction is the more aggressive cousin of (d): it solves the problem with structural change rather than a content edit.

## The (b′) shape, concretely

For each of the two entries:

1. Add an `## Update history` block (per the existing state-table-honesty discipline named in punch-list item 18f) at the top, naming:
   - The 2026-04-27 finding that `temporary/` lives only on `agentic-engineering-research`@13c09b0.
   - That the migration plan as written is no longer executable.
   - That the parent-shape narrative is preserved and the entry remains at `🌱` (not advanced to `superseded`).
2. Wrap the §Concrete-migration-plan / equivalent §Seed-research blocks in a `> superseded — see Update history` blockquote prefix. The prose stays; the executable claim is visibly demoted.
3. Do not change the state-table cell. The entry is still `🌱`. The `Update history` block names *why* it is unlikely to advance from `🌱` until the dependency question is settled.

For [`upgrades/LEDGER.md`](../../../upgrades/LEDGER.md):88, rewrite row #18b's `Implement as` cell to: *"Migration plan superseded 2026-04-27 (temporary/ lives only on `agentic-engineering-research`@13c09b0); see entry body Update history. Parent shape survives; advance from 🌱 only if/when worktree branch graduates."*

This is **not** option (b) as the punch list named it. The punch list's (b) said *"mark both entries as superseded in their bodies."* I am rejecting whole-entry supersession because the parent ideas are not dead. (b′) is targeted supersession of the migration sections only.

## Named tradeoffs

- **(b′) vs. (b) full-supersede.** (b′) preserves the parent narratives; full (b) discards them. Cost of (b′): two readers will have to read the `Update history` block to understand why the migration section is demoted. Cost of full (b): the parent-shape thinking captured on 2026-04-26 has to be re-derived if/when the dependency lands. (b′) trades a small reader-cognition cost for a moderate idea-preservation gain. Rate of decay if (b′) is *misapplied* (too liberal use of "supersede only this section"): the entry becomes a Frankenstein of dead and live sections, harder to read than full (b). Mitigated by the targeted scope (one section per entry, named explicitly).
- **(b′) vs. graduation-eviction.** (b′) keeps the parent narratives on `main`; eviction moves them to a separate branch. Cost of (b′): `main`'s tree carries two entries whose migration plans are dead. Cost of eviction: parent narratives become invisible to anyone reading `main` alone, including future agents that might consult the LEDGER. (b′) trades minor `main`-clutter for narrative discoverability.
- **(b′) vs. doing nothing more than this session.** Doing nothing leaves the references broken; (b′) closes the symptom. The punch list's whole purpose is to close such symptoms.

## Named assumptions (each one would flip the recommendation if wrong)

1. **The LEDGER is reflective-narrative, not canonical-executable.** I argued this above from existing repo behavior. If the operator's actual intent is canonical-executable — every row must be actionable from `main`'s tree — then graduation-frame eviction becomes correct, and (b′) is a half-measure that re-anchors the dishonesty rather than removing it. **How to falsify cheaply:** ask the operator outright; or, look for any existing rule in [`upgrades/README.md`](../../../upgrades/README.md) that asserts every row must be executable.
2. **The parent-shape narratives in both entries are still endorsed by the operator.** The entries were authored on 2026-04-26 — yesterday. I am assuming the thinking has not aged out in 24 hours. If the operator now disagrees with either entry's parent narrative (independent of the migration question), then (b′) preserves dead thinking; full-supersede or deletion becomes correct. **How to falsify cheaply:** the operator re-reads the parent-shape sections and either confirms or marks each as no-longer-endorsed.
3. **The worktree branch will not be deleted in the near term.** (b′) routes future readers to `agentic-engineering-research@13c09b0`. If that branch is going to be force-pushed, rebased, or deleted within a quarter, (b′) becomes a footnote pointing at nothing. **How to falsify cheaply:** check whether any standing convention or routine deletes worktree branches after some interval.
4. **The lab does not need a written `superseded` LEDGER state token at this time.** (b′) deliberately leaves the entries at `🌱` because adding a new state token to the lab's vocabulary is itself an item-1-style decision that should not be made as a side-effect of a cleanup action. If the operator has been wanting `superseded` as a first-class state, doing (b′) without adding it is a missed coupling. **How to falsify cheaply:** check whether a `superseded` state has been informally used in any other entry body or LEDGER row.
5. **Punch-list scope discipline outranks workflow scope-expansion when they conflict on cleanup items.** (b′) honors the punch list's "tackle one item at a time" rule by refusing (d). If the operator's actual preference is the inverse — let the workflow expand scope when it surfaces a frame-level gap — then (d) becomes correct and (b′) is the wrong shape. **How to falsify cheaply:** the operator says explicitly which discipline wins.

## Named ways this could be wrong

- **The "Update history" mechanism is borrowed from punch-list item 18f, which is itself at `🌱`.** I am building on a state-table-honesty convention that has not yet been ratified. If item 18f is later abandoned or reshaped, (b′)'s `Update history` block becomes a one-off pattern.
- **The LEDGER cell rewrite is text, not enforced.** Nothing prevents a future writer from re-introducing a phantom migration plan into row #18b. Without item 14 (hard gates as harness hooks), the discipline is honor-system. (b′) does not solve the recurrence question that the alternative-frame option (d) was trying to solve — that question is still on the table.
- **I am partly trusting outside-view's qualitative base rates.** The outside-view distillation flagged its own canon read as failed; the (a/b/c/d) percentages are estimates. If those estimates are systematically biased toward "supersede looks safe because terminal states are tidy," (b′) inherits that bias.
- **The graduation frame may be more correct than I credited.** I dissolved it by appeal to the LEDGER's reflective-narrative reading. A critic-architecture review may rebuild it on a different invariant (e.g. *every entry must declare its dependency tier — in-main, in-canon, in-history, in-future — and entries with `in-history` dependencies must explicitly opt-in to a different lifecycle*). That version of the frame would force a real choice and (b′) would be revealed as ducking it.
