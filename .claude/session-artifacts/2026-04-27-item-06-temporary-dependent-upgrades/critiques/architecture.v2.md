# Critic — Architecture lens v2 — item 06 (loop 2)

## 1. Weakest structural link

The relocation correctly addresses the partition-violation from loop 1, but it shifts the load-bearing question to a different seam: **the Group-E aggregate's invariants are themselves under-specified, and (e) is the second test case Group E has ever seen.** Group E currently contains exactly one row (#19, "memory and lab are the same primitive") whose `Implement as` is `—` and whose state is `🌱`. The candidate triples Group E in a single edit with two entries qualitatively different from #19: #19 originated as an open question; 18b/18g originated as concrete buildable proposals that lost their preconditions. The candidate treats Group E as a generic "non-executable bucket" without asking whether Group E's contract distinguishes **never-was-executable** from **was-executable-now-isn't**. (e) silently decides that distinction.

## 2. Invariants at risk

1. **Group-E originating-shape invariant (latent).** Group E's intro reads *"Entries that name a real thing but whose action is 'answer this with a future entry,' not 'build something now.'"* Forward-looking phrasing. 18b/18g satisfy it only after the `Status` paragraph rewrite. **(e) without a Group E intro amendment is an undocumented contract expansion.** The candidate's assumption #1 names this exact load-bearing claim and offers no falsification work beyond "find a written rule that contradicts it" — wrong burden of proof.
2. **Tier-cell honesty in Group E.** Row #19 is `💎 profound`. After relocation, Group E will contain a `💎` and two `🌿`s. Tier-`🌿` entries in Group E have unclear semantics — a normal-tier entry whose action is "answer with a future entry" reads as a routine open question, which the lab's [`upgrades/README.md`](../../../../upgrades/README.md) intro explicitly disclaims ("It is not a backlog. It is not a planning system."). The candidate does not address tier-cell coherence.
3. **Entry-folder TOC integrity under section deletion.** For 18b, deleting only `## Concrete migration plan` leaves `## The proposed third path` (lines 84–90) with two of its three numbered moves still describing actions against `temporary/`. The candidate's "delete migration sections, keep parent narrative" surgery is not as clean as v2 claims. Either `The proposed third path` is also edited, or assumption #2 ("parent narratives stand on their own") fails for 18b.

Carry-forward from loop 1:

4. Group-membership invariant — **RESOLVED** by physical relocation.
5. State-token monotonicity — **RESOLVED** (no `Update history` smuggling; `🌱` in Group E is honest).
6. `Implement as`-as-imperative — **RESOLVED** (Group E uses `—`).
7. Cross-aggregate Git-ref dependency — **NARROWED** from live coupling to historical citation. The branch can be deleted and the `Status` paragraph remains true.

## 3. Coupling and direction

Acceptable. Branch reference is a citation, not a dependency edge. Cross-discipline coupling on item 18f is gone (no `Update history` borrow). Two-way text reference cycle gone. One residual latent coupling: LEDGER Group E intro and entry `Status` sections — bounded.

## 4. Ignored architectural alternatives

1. **(e) + amend Group E's intro text in the same edit.** Add one sentence: *"This includes entries that originated as buildable proposals but lost their preconditions; their `Status` section names what would unblock re-graduation."* Closes the latent coupling, makes assumption #1 concrete, pre-empts next time. Strictly cleaner.
2. **Split fates: (e) on one entry, (g) on the other.** 18b has a concrete bounded migration plan whose preconditions vanished; 18g is more abstract whose original action was *creating a new module*, plausibly re-derivable without `temporary/`. The candidate treats them as a single block.

## 5. Frame-level objection

The Revision-2 frame correctly identifies the partition question. **But it still treats item 6 as cleanup, not as contract-evolution.** The fact that two entries moved Group D → Group E because their preconditions vanished is information about the lab's contract: groups can act as a state-machine. The architecturally honest move is land (e) **and** open a small follow-up entry capturing "groups are state-machines" conventions. Without that follow-up, the next time this fires, the operator re-derives the (e)-shape from scratch. This is a frame note, not a blocker — the next-instance cost is bounded.

## 6. Verdict

`approve` — conditional.

Conditions for unconditional approve:
1. Add a one-sentence amendment to Group E's intro text in [`upgrades/LEDGER.md`](../../../../upgrades/LEDGER.md) describing that Group E accepts entries that became observational post-filing.
2. Either edit `The proposed third path` in 18b consistently with the migration-plan deletion, or name that section as also edited (or surface why it survives).
