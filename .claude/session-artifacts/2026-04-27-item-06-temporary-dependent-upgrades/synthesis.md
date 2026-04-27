# Synthesis — item 6 of cleanup punch list

## 1. Classifier label and alternative

- **Primary label:** `refactor`. Default frame: "what observable change would falsify 'behavior unchanged'?"
- **Alternative classification:** `migrate` (becomes primary if the recommendation is option (a), restoring `temporary/` to `main`). The classifier flagged the bias of letting (a) ride in under the refactor frame without surfacing that it crosses into migration.
- **Secondary label considered:** `investigation` — the workflow's job included stress-testing the operator's pre-pipeline lean (originally toward option (c), park-with-resume-condition).

## 2. Reframe (current revision)

- **Revision 1.** "This is a graduation question, not a state-token question. Should these entries even exist on `main`, given that their dependencies don't?" Surfaced as a counter-frame to the user's menu-of-three (a/b/c) cleanup framing.
- **Revision 2 (post-loop-1 panel veto).** **Partition-correction, not state-token gymnastics.** The LEDGER already has a partition for non-executable rows: Group E ("Observations — no immediate action"). The two affected entries (#18b agentic-engineering-reference-library, #18g living-poweruser-knowledge-module) sit in Group D ("Repo hygiene & conventions"), which is structurally executable. Either the entries belong in Group E (relocate), or they need to be physically removed (eviction / extraction / migration-section deletion). Loop 1's candidate tried to invent a third governance regime inside Group D; the panel rejected it.

## 3. Reference-class forecast (outside-view distillation)

Reference class: internal documentation entries that reference an asset preserved on a sibling branch / archive / sidecar location, in a low-stakes single-operator R&D repo, where the entries are at the earliest lifecycle stage.

Qualitative base rates the outside-view named for the original four options:

- (a) restore: ~60–70% resolve cleanly; ~30% zombie via two-copies divergence.
- (b) supersede with honest-negation pointer: ~70–80% resolve; low zombie rate (terminal).
- (c) park with `⏸️` and resume condition: ~20–30% resume; ~70% zombie (modal failure of personal-KB deferral mechanisms).
- (d) write a new dependency-contract rule: ~10–20% rule survives; ~80% rule-inflation failure ("process for a population of one").

Verdict: "Below base rate for (c) and (d). Within tolerance for (b). Mixed for (a)." The Revision-2 reframe to partition-correction (option (e)) was not on the outside-view's list — it is downstream of the convergent panel objection, not the outside-view's analysis.

**Caveat surfaced by the distiller:** the outside-view subagent's canon read failed mid-run; per-option percentages are qualitative estimates, not measured base rates.

## 4. Canon passages (supporting and contradicting)

**Supporting (toward partition-correction frame):**

- **Anthropic, "Core Views on AI Safety" (2023), §Portfolio Approach.** *"We anticipate that our approach and resource allocation will rapidly adjust as more information about the kind of scenario we are in becomes available."* Re-allocation is portfolio-coherent; relocating the entries when their preconditions changed is the portfolio behavior, not an exception.
- **Heilmeier Catechism (DARPA).** *"What are the mid-term and final 'exams' to check for success?"* An R&D entry that cannot answer the exam question is, by Heilmeier's discipline, a wish — Group E's contract honestly absorbs wishes.

**Contradicting / complicating:**

- **Google SRE Book (2016), ch. 26 §Backups vs. Archives.** *"The most important difference between backups and archives is that backups can be loaded back into an application, while archives cannot."* This is the strongest in-corpus argument *for* option (a) — if the worktree branch is being asked to do backup duty (live, restorable, expected to be drawn from), leaving it as a branch is mis-classified storage. Resolved by Revision 2 by making the branch reference a *citation* (archive-shaped), not a dependency edge.
- **Google SRE Book (2016), ch. 23 §Branching.** *"Branches… never merge changes from the branch back into the mainline."* Cuts directly against (c)'s parked-state and against (a)'s restore. Reinforces the partition-correction frame.

**Gaps the librarian flagged:** no ADR/RFC lifecycle source ingested (Nygard's "Documenting Architecture Decisions" is not in the corpus); no Hickey "Hammock-Driven Development" for the deferral debate; no Chesterton's-fence treatment for the rule-inflation question. The "honest negation" doctrine the operator cites has no in-corpus primary source.

## 5. Scope-map summary and unresolved conflicts

Eight existing primitives mapped. Notable rows:

- LEDGER lifecycle states: **extend** (option (e) does not redefine them; group movement reuses them).
- The two affected entries' bodies: **replace under (b)/(d), extend under (c), no-op under (a)**; *after Revision 2*, **replace under (e)** — the migration-plan sections are deleted; parent narratives extend.
- LEDGER row #18b's `Implement as` cell: **replace** (cell content materially false today).
- Cleanup punch list's binary (a)/(b) framing: **subsume** by the wider option set.
- Punch-list "no scope creep" discipline vs. workflow scope-expansion right: **conflict** — resolved in Revision 2 by accepting the punch-list discipline (no new lab-wide convention; (d) declined).

**Unresolved conflicts at the time of synthesis:**

- *Backup vs. archive role of `agentic-engineering-research`.* Resolved in Revision 2: the branch is treated as an archive (citation only). If the operator later decides to restore content to `main`, that is a separate decision that re-graduates the affected entries from Group E back to Group D.
- *Architecture's loop-2 conditions* (Group E intro amendment; `The proposed third path` audit) — incorporated into the recommendation below.

## 6. Frame-level challenge and how the recommendation addresses it

Two frame-level challenges arose:

1. **Frame-challenger (loop 1).** *"This is a graduation question, not a state-token question. The entries do not belong on `main` at all."* — addressed in Revision 2 by reframing to partition-correction: the LEDGER does have a non-executable partition (Group E) that the entries can legitimately occupy, so eviction is too severe; but the loop-1 candidate's bisection-into-mixed-mode (b′) was not a valid response to the challenge either.
2. **Convergent panel frame objection (loop 1, all three lenses).** *"The candidate preserves the LEDGER state vocabulary by overloading it; physical removal is the universal sticking point."* — addressed by candidate-v2 (option (e)): physical relocation + physical deletion of migration-plan sections + a clean `## Status` paragraph. No state-token overload, no blockquote-demoted imperatives.

## 7. Post-critique recommendation

**Resolve item 6 by option (e), with two small additions named by the architecture critic:**

### Edits to ship in one commit

1. **[`upgrades/LEDGER.md`](../../../upgrades/LEDGER.md):**
   - Remove rows #18b (`agentic-engineering-reference-library`) and #18g (`living-poweruser-knowledge-module`) from Group D.
   - Insert two rows in Group E (rank `19a`, `19b`), state `🌱`, `Implement as` = `—`.
   - **Amend Group E's section header text** (one sentence) to: *"This includes entries that originated as buildable proposals but lost their preconditions; their `## Status` section names what would unblock re-graduation."* (Architecture condition #1.)
   - *Optional additive (per product critic):* add one line to "How to read this" — *"`—` in Implement as means the entry is observational; no action against `main` is prescribed."*

2. **[`upgrades/normal/2026-04-26-agentic-engineering-reference-library/README.md`](../../../upgrades/normal/2026-04-26-agentic-engineering-reference-library/README.md):**
   - Delete `## Concrete migration plan` (lines 92–107).
   - **Edit `## The proposed third path`** (lines 82–90): rewrite the three numbered moves so they describe the *idea* the entry proposed, not the actions against `temporary/`. (Architecture condition #2.)
   - Replace deleted content with a `## Status` section: one paragraph naming the 2026-04-27 finding, the worktree branch + commit, and the re-graduation condition. Update the table-of-contents.

3. **[`upgrades/normal/2026-04-26-living-poweruser-knowledge-module/README.md`](../../../upgrades/normal/2026-04-26-living-poweruser-knowledge-module/README.md):**
   - Identify and delete the migration-prescriptive sections (the entry is more abstract than 18b; likely fewer cuts).
   - Insert `## Status` per the same shape.
   - Update table-of-contents.

4. **[`plans/2026-04-27-repo-cleanup-punch-list.md`](../../../plans/2026-04-27-repo-cleanup-punch-list.md):**
   - Append `✅ done <YYYY-MM-DD>` to item 6's heading. Do not delete.

### Verification before merge (10-minute re-read)

Verify that neither entry's parent-shape narrative substantively depends on the migration plan having been *executed* (rather than merely described). If either does, that section is also stale and (e) needs to escalate to (f) extract-and-delete for that entry.

## 8. Three named uncertainties

1. **Group E's partition contract is silent on the originate-vs-became distinction.** The candidate's assumption #1 names this as load-bearing; architecture's loop-2 condition #1 closes it by amending the intro. If that amendment fails to land for any reason, Group E silently absorbs a contract expansion that was never written.
2. **Worktree branch durability.** The `## Status` paragraph cites `agentic-engineering-research@13c09b0`. If the branch is force-pushed, rebased, or deleted, the citation becomes a historical note pointing at nothing. v2 makes this acceptable (the citation is archive-shaped, not dependency-shaped) but a future operator may want self-contained recoverability — e.g., a one-time copy of the registry's index into `canon/corpus/` as a stub.
3. **Group E inflation as parking-lot drift.** v2 grows Group E from 1 row to 3. If the next 1–2 research sessions land on worktree branches and produce further entries with out-of-`main` dependencies, Group E grows to 5–7 rows and starts to function as a parking lot rather than an observation shelf. The candidate's "ways this could be wrong" #2 names this; the operations critic flags it as the threshold to watch. The lab does not currently have a written rule for when Group E inflation should trigger writing the (d)-style dependency-contract convention.

## 9. Cheapest experiment to reduce the biggest uncertainty

The biggest uncertainty is #3 (Group E inflation). The cheapest experiment: **commit (e) as recommended, then watch the next two research sessions that produce upgrade entries.** If either session deposits an entry that ends up in Group E for the same reason (out-of-`main` source material), revisit the dependency-contract question with three data points instead of two — that crosses outside-view's "third instance" threshold for promoting per-instance to as-rule. If the next two sessions instead deposit entries into Group D normally, Group E inflation is not a recurring shape and the deferral was correct.

This experiment runs in the background of normal lab use; it costs zero new sessions and produces a binary signal at each future research session.
