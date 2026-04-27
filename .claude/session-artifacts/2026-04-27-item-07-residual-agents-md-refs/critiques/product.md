# Product-lens critique — item 7 (residual AGENTS.md references)

## 1. User-visible consequence

Day-of: the orchestrator agent loads a path-discipline rule whose enumeration is silently shorter. A future operator who searches for *"why isn't AGENTS.md enforced under path-discipline"* finds nothing — the deletion is silent. Regression in *traceability of the contract*.

The bigger user-visible artifact is the rewritten benefit cells. After rewrite they read:
- *"CLAUDE.md drift against GOALS.md becomes detectable."*
- *"CLAUDE.md drift becomes commit-traceable."*

A reader comparing those cells to peers in the same `🚀 upgrade` column will notice they are **structurally thinner** than peer cells (which make multi-clause arguments). The rewritten cells now make a single-clause claim. That is the half-claim look the prompt warned about — a reader who didn't know the original cell existed reads them as oddly under-argued; a reader who did reads them as *"something was deleted out of this."*

## 2. Commitments implied

- **Treating upgrade-entry bodies as in-place mutable** when a referenced primitive disappears. This is a precedent — the next time a constitutional doc gets retired, the same surgical-rewrite pattern will be invoked because item 7 set it.
- **A non-exhaustive reading of the path-discipline list.** The rule's text terminates with `anywhere`, which carries illustrative-not-exhaustive force. So the assertion is correct *as the rule reads today*. But removing a named item without re-anchoring the list's generality leaves the rule's generality load-bearing on `anywhere` alone — fragile.
- **The lifecycle markers being decorative.** Both edited entries are 🌱-marked (created, not yet 🔨/🔖). So the "🔖-committed" framing in the prompt is slightly off — these entries are *not* yet committed as finalized state. This weakens (does not remove) the historical-revision objection.

## 3. Migration burden

- **Orchestrator agent** (auto-loads CLAUDE.md): zero burden.
- [`prompts/ultraplan-next-level.md`](../../../../prompts/ultraplan-next-level.md):39: zero burden — already guarded.
- **Future critic agents performing meta-review or supersession analysis on the two rewritten entries.** Adaptation required: they must read git history (not the live entry) to see the original parity-based benefit claim. **A critic agent doing supersession analysis cannot, by inspection of the entry alone, see that the benefit claim was scoped down — they must `git log -p` the README.** That is a real burden the plan minimizes by calling it *"git history survives."*
- **The follow-up upgrade entry** has a small but real circular dependency: its evidence is precisely the damage item 7 did. Cleaner answer: defer the rewrites until the supersede convention exists.

## 4. Affordances better/worse

**Better:**
- A new operator landing on CLAUDE.md no longer sees a phantom file in the path-discipline rule.
- `git status` no longer shows a `.gitignore` line for a non-existent file.
- Module-decomposition row at `:42` describes the actual current shape.

**Worse:**
- **Capability newly pruned:** *"what did this entry originally claim?"* Today, `git log -p` answers — but only if the reader knows to look. Yesterday, the entry itself answered. The affordance moves from *in the document* to *in git archaeology*.
- **Capability newly absent:** a "premise revised" lifecycle marker. Plan flags this and pushes to follow-up. But shipping the rewrite *before* the marker exists means the rewritten entries' lifecycle row is **visibly silent** about an event that happened to the entry post-creation.
- **The footnote in `workflow-blind-to-the-lab`.** Plan places it *"at the bottom of the body section"* — the wrong place. A reader who follows a backlink to the catalyst row reads the catalyst and either acts or scrolls. A footnote thirty lines below is invisible to the reader who needs it.

## 5. Frame-level objection

**The frame treats this as an internal documentation-cleanup decision; from a product lens, the decision is about what the upgrade canon's contract says about mutability.**

Every entry under `upgrades/` carries a YYYY-MM-DD slug, a creation-date row, and a lifecycle-state row. Together those signals form a *contract with the future reader*: this entry was authored on date D, has progressed through states S₁...Sₙ, and a reader at D+T can reason about what was claimed at D versus what is claimed now. **In-place rewriting of body cells without advancing the lifecycle row violates that contract.** The plan's *"Follow-up filed by this plan"* section acknowledges the gap and proposes a separate upgrade entry, *which is precisely the reason the rewrites should not ship before the fix.*

## 6. Verdict

`rework`.

**Smallest change to approve:**
1. Move the catalyst footnote in `workflow-blind-to-the-lab` immediately adjacent to the catalyst row (not "at the bottom").
2. Split the commit into two — ship the live-contract edits (CLAUDE.md, .gitignore, the `:42` module-composition row, which is structural fact) now, and **defer** the three benefit-cell rewrites until the follow-up "supersede-don't-edit" upgrade entry has decided whether they should be in-place rewrites or strikethrough+footnote.
3. If the operator insists on shipping the benefit-cell rewrites in this PR, add a one-line erratum row to each affected entry's lifecycle table (e.g., a "🔁 premise-revised <date>" cell) so the entry's state visibly advertises the post-creation event.
