# Critic — Architecture lens — item 06 temporary-dependent upgrades

## 1. Weakest structural link

The candidate's load-bearing premise — "LEDGER is reflective-narrative" — is anchor-rescue dressed as architectural analysis. Strip that premise and (b′) collapses into "demote some prose, leave the broken row pointer in place, call it done." The premise itself is supported by exactly one in-tree datum (row #19) which the candidate misreads: row #19 lives under Group E, titled "Observations (no immediate action)" — a structurally-designated bucket for non-buildable rows. That is not evidence the LEDGER tolerates non-executable rows in Groups A–D; it is evidence the LEDGER has a **separate sub-aggregate for the reflective-narrative case**, and that the two affected entries are not in it. The LEDGER's own README text says "Every entry, regardless of group or rank, still goes through the full upgrade lifecycle when worked on" and the State column enumerates execution states (`🌱 → 🔨 → 🩺 → 🔖 → 💎 → 🏁`). The structural reading is: the LEDGER is a **mixed aggregate** with one explicit non-executable partition (Group E). Entries 18b and 18g sit in Group D ("Repo hygiene & conventions"), which is firmly executable. The candidate has built (b′) on a frame the existing structure already refutes by partition.

## 2. Invariants at risk

1. **Group-membership invariant.** Each LEDGER row's *Group* is a structural commitment about what kind of row it is (executable vs. observation). (b′) leaves entries 18b/18g in Group D while editorially reclassifying them as "mixed-mode." That violates the group-as-partition contract — a future state-table parser (item 14a, format-only gate) iterating Group D rows will encounter entries whose `Implement as` text is meta-prose ("Migration plan superseded; see entry body") rather than an implementation directive. Either Group E expands, or a new group is created, or entries move — the candidate does none of these.
2. **State-token monotonicity.** `🌱` is the first state on a forward-only lifecycle (`🌱 → 🔬 → 📋 → ⚙️`). The candidate's "Update history block names *why* it is unlikely to advance from `🌱`" turns `🌱` into a *quasi-terminal* state for these two rows — which it isn't, structurally. A `🌱` row with an `Update history` block saying "won't advance until X" is functionally an `⏸️`-modified row, but written as if `⏸️` weren't a vocabulary item. The candidate explicitly rejects (c) and then smuggles `⏸️` semantics into `🌱` without the token. That's a violation of the lifecycle invariant by stealth.
3. **`Implement as` cell as imperative.** Row 18b's `Implement as` text is, in every other Group D row, an imperative shape ("Promote X + Y…", "Verify recursive loading…", "One CLAUDE.md bullet…"). The candidate's proposed cell — *"Migration plan superseded 2026-04-27…"* — is **declarative meta-prose about the row itself**, not an imperative. Other rows do not self-narrate their own status in the `Implement as` cell.
4. **Aggregate-root coherence of an entry folder.** Per item 18a, an upgrade entry is a *folder*. The candidate proposes an `Update history` block at the README top that points outside the aggregate (to `agentic-engineering-research@13c09b0`). That introduces a dependency edge from the entry-aggregate to a Git ref that is not part of any aggregate on `main`.
5. **Punch-list closure invariant.** A punch-list item closes when its symptom is gone. (b′) does not remove the symptom (broken pointer); it labels the symptom as known. A labeled broken pointer is still a broken pointer to a future reader who has to decide whether the label is current.

## 3. Coupling and direction

Dependency direction is **wrong**.

- **`main` → `agentic-engineering-research`@13c09b0.** Volatile (a worktree research branch with no published stability contract) is depended-upon by stable (`main`'s LEDGER and entry corpus). The candidate flags this in assumption 3 and immediately moves on. This is the invariant most likely to fire in 6 months and the candidate's mitigation is a footnote.
- **Cross-discipline coupling on un-ratified primitives.** (b′)'s `Update history` block borrows from punch-list item 18f, which is at `🌱`. Building the resolution of item 06 on item 18f's convention introduces a **cycle** in the punch-list dependency graph.
- **Two-way text reference cycle** between LEDGER row 18b cell and entry-body `Update history` block. Existing rows do not do this.

## 4. Ignored architectural alternatives

1. **Move the two entries from Group D to Group E.** Group E ("Observations — no immediate action") is the LEDGER's existing partition for non-executable rows. Cheap move: relocate them to the partition designed for that mode. Preserves parent narratives, removes executable-claim dishonesty, keeps the LEDGER's partition invariant intact, costs one re-rank.
2. **Promote a `dependency-context` field to the entry-folder schema (without writing a general rule).** Add one optional field — `dependency-context: requires-branch:agentic-engineering-research@13c09b0` — to the two affected entries only. No general rule, no state-token gymnastics, no body rewrite of executable prose. Strictly cleaner than (b′).

## 5. Frame-level objection

The candidate's frame-level move is to *bisect* each entry into "executable parts" and "narrative parts" and apply different disciplines to each. **That bisection is itself the architectural problem.** An entry is an aggregate with a single README; bisecting it into two governance regimes is a Frankenstein-shape that the entry-folder contract does not anticipate. The architecturally honest response is **separation**: extract the parent-shape narrative into an entry that can be executed against `main`, or move both entries to Group E where non-executability is native.

## 6. Verdict

`reject`.

Path to approve: drop the "reflective-narrative" claim and propose either (i) Group D → Group E relocation, or (ii) entry separation/extraction.
