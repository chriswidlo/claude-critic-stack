# Candidate recommendation v2 — item 06 temporary-dependent upgrades

## Position

**Pick (e): relocate both entries from Group D to Group E in [`upgrades/LEDGER.md`](../../../upgrades/LEDGER.md), and physically delete the migration-plan sections from each entry body, replacing each with a one-paragraph negation note.** No `Update history` block, no blockquote demotion of executable prose, no new state token, no `superseded` modifier.

This is the convergent path-to-approve from all three critics: Group E relocation (architecture), eviction-of-executable-claims (operations), physical removal of imperative migration text (product). Each lens's objection is satisfied by the same physical move.

## Addressing the frame-level objection (convergent panel veto)

The loop-1 candidate was rejected because it preserved phantom imperative text in a structurally-executable LEDGER group while pretending prose annotation could neutralize the imperative. The convergent fix is: **honor each LEDGER group's invariant without overloading the state vocabulary.**

Group D ("Repo hygiene & conventions") rows are imperatives; their `Implement as` cell is an action directive; their entry bodies contain executable plans. Group E ("Observations — no immediate action") rows are non-actionable; their `Implement as` cell is `—`; their entry bodies are *narrative* about an open question or named-but-unsolved phenomenon.

The two affected entries fail the Group D contract today: their migration plans cannot be executed against `main`. They satisfy the Group E contract: they describe a phenomenon (the recurring shape of practitioner-knowledge research) and an open question (what the durable home for it should look like) without prescribing a specific action against `main`.

**Therefore: relocate.** The relocation is not a status-token gymnastics move; it is a partition-correction. The entries always belonged in Group E once their dependency moved off `main`; loop-1 candidate's mistake was treating Group D as the entries' fixed home.

## The (e) shape, concretely

### LEDGER edits ([`upgrades/LEDGER.md`](../../../upgrades/LEDGER.md))

1. **Remove rows #18b and #18g from Group D.** Renumber remaining Group D rows if the operator wants contiguous numbering; renumbering is not strictly required.
2. **Insert two rows in Group E.** Reuse the existing Group E table format (the one row #19 currently uses):
   - Row for `agentic-engineering-reference-library`: rank `19a` or similar; tier `🌿`; state `🌱`; effort `—`; `Implement as` = `—`; with a brief group-introductory sentence noting that the parent-shape narrative survives but the original migration plan is dead because its source material lives only on the worktree branch.
   - Row for `living-poweruser-knowledge-module`: same shape; rank `19b`.
3. Leave row #19 (memory-and-lab) where it is. Group E now has three rows.

### Entry-body edits

For each of the two entries:

1. **Delete** the `## Concrete migration plan` section (in the reference-library entry) or equivalent migration-prescriptive sections (in the living-poweruser-knowledge-module entry).
2. **Replace** with a single short paragraph in a new section titled `## Status` (no need for the borrowed `Update history` shape from item 18f):
   > As of 2026-04-27, the source material this entry's migration plan referenced (`temporary/decision-registry.md`, etc.) lives only on the `agentic-engineering-research` branch (commit `13c09b0`), not on `main`. The migration plan was deleted because it described actions that cannot be executed against `main`'s tree. The parent-shape narrative below remains the entry's substantive claim. If the source material is ever brought to `main` via a separate decision, this entry will need to be re-graduated to a Group D shape with a fresh migration plan written against the world that exists at that time.
3. **Keep** every other section (table-of-contents, parent-shape narrative, open questions, what-success-looks-like, etc.).
4. Update the entry's table-of-contents to remove the deleted sections and add `Status`.

### Punch-list update ([`plans/2026-04-27-repo-cleanup-punch-list.md`](../../../plans/2026-04-27-repo-cleanup-punch-list.md))

Append `✅ done <YYYY-MM-DD>` to item 6's heading. Do not delete the item per the punch list's own procedure (line 263).

## Why this satisfies each lens's objection

- **Architecture.** Group E relocation is the lens's first path-to-approve. Group-membership invariant is honored. State-token monotonicity is preserved (`🌱` in Group E means "captured observation," which is an honest read for both entries). `Implement as` cell is `—` per Group E convention, removing the imperative-vs-meta-prose conflict. No mixed-mode bisection — the entries become single-discipline narratives, full stop.
- **Operations.** Pointer rot risk is bounded: the `Status` paragraph mentions the worktree branch by name and commit, but the entry no longer *depends* on the branch being reachable for any actionable purpose. If the branch is later deleted, the `Status` paragraph still reads correctly as a historical note ("the source material *was* preserved on a branch that has since been pruned"). Recurrence cost still exists for future cross-branch entries, but each future occurrence is now a Group E placement decision, not a Group D rescue.
- **Product.** State cell and `Implement as` cell agree (`🌱`/`—`). No reader-interpretation cost about whether the row is live. No phantom `git mv` instructions sitting under a typographic demotion. Honest negation applied: the dead plan is gone, not blockquoted-out. Punch-list rhythm matches items 1–5 (mechanical edit with named files).

## Named tradeoffs

- **(e) vs. (f) extract-and-delete.** (e) keeps each entry as a single aggregate; (f) splits each into two new entries (parent-shape + dead-migration). Cost of (e): the LEDGER's Group E grows from 1 row to 3 rows. Cost of (f): four entry-folder operations, plus the question of whether the parent-shape entries belong in Group D, E, or somewhere else. (e) is cheaper and reaches the same partition-honoring end-state.
- **(e) vs. (g) delete-sections-keep-in-Group-D.** (g) requires an imperative `Implement as` against a future condition ("Re-derive migration plan when worktree branch graduates"). That phrasing is imperative-shaped but its action target is conditional on an event that has no calendar trigger — it is operationally indistinguishable from "do nothing right now," which is exactly the Group E contract. (g) is (e) wearing a Group D costume.
- **(e) vs. doing nothing.** Doing nothing leaves the broken references and the partition violation. (e) closes the symptom and the structural issue together.

## Named assumptions (each one would flip the recommendation if wrong)

1. **Group E is structurally available for entries that originate as Group D-shaped ideas but lose their Group D viability.** Group E's introductory text says "Entries that name a real thing but whose action is 'answer this with a future entry,' not 'build something now.'" The two affected entries fit this description after the dependency loss, even if they did not originate this way. **How to falsify:** find a written rule (anywhere in [`upgrades/README.md`](../../../upgrades/README.md) or LEDGER) that says Group E is for entries that originated as observations, not for entries that *became* observational.
2. **Deleting the migration-plan sections does not destroy operator-endorsed thinking the parent-shape sections do not capture.** I'm assuming the parent-shape narratives stand on their own. **How to falsify:** the operator re-reads each entry and identifies a migration-plan paragraph that contains thinking not present in the parent-shape sections; that paragraph would need to be quoted into the `Status` paragraph or moved up before deletion.
3. **The worktree branch reference in the `Status` paragraph is durable enough for the lab's purposes.** Even if the branch is later deleted, the historical note remains accurate ("source material *was* preserved on a branch named X"). **How to falsify:** if the operator wants the `Status` paragraph to be self-contained even under branch-deletion, the source material's existence-history would need to be captured another way (e.g., a one-time copy of the registry's index into `canon/corpus/` as a stub entry citing the branch).
4. **Renumbering Group D rows is optional, not mandatory.** I'm assuming the operator tolerates either contiguous (#18a, #18b removed → renumber #18c→#18b, etc.) or gap-bearing (#18a, #18c, ...) numbering. **How to falsify:** check whether anything in the lab parses LEDGER row numbers as sequential.

## Named ways this could be wrong

- **Operator may want the entries killed entirely, not relocated.** (f) extract-and-delete with deletion of the parent-shape entries too is a stricter form of honest negation. (e) preserves more than the strictest reading of the doctrine would. If the operator's actual stance is "if the migration is dead, the parent narratives that depended on the migration's existence are also stale," (e) leaves dead thinking on `main`.
- **Group E may be more crowded than intended.** Today it has one row. After (e), three rows. If the operator's mental model is that Group E should remain very small (a "bench" rather than a "shelf"), (e) inflates it. Mitigation is small: the operator can split Group E later if it grows.
- **Group D parsers (item 14a hard-gate, future format-only checks) may not handle row removal cleanly.** I'm assuming row removal from a group is a reversible text edit. If any tooling reads pre-edit row numbers and assumes their persistence, removal could break it. Item 14a is at `⚙️` (run-through-repo) so it has at least partial implementation; this should be checked before merge.
