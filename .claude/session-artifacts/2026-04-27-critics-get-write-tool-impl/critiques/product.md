# Critic — Product lens verdict

`2026-04-27-critics-get-write-tool-impl`

## 1. User-visible consequence

**The operator's Step 10 surface changes shape from "one file to read" to "four files to read" — and the file they previously read (`critiques.md`) silently changes meaning.** Today the operator opens `critiques.md` and sees the full critique bodies inline; tomorrow they open the same path and find a 3-row table of (lens · verdict · path). Every prior reading habit ("scroll to the verdict line in critiques.md") becomes wrong. The operator who skims rather than clicks now sees only a verdict label and must follow three additional links to recover the content they used to get in one read. That is a regression in *information-per-keystroke* on the panel-review surface, not an improvement, even if the audit chain is more faithful.

Secondary visible consequence: **the verdict label vocabulary across the three lenses is no longer normalized by an orchestrator paraphrase pass.** Today the orchestrator silently smooths "approve" / "Approve." / "approve | with conditions" into a uniform label when transcribing. Under the new contract, whatever the critic writes is what lands. The operator's grep over `critiques.md` (or any future tool that does so) will need to handle each lens's idiolect. Candidate Way-this-could-be-wrong #3 names this; it is real and operator-facing.

## 2. Commitments implied

Three new contracts, all load-bearing the moment a second consumer appears:

- **The path `<id>/critiques/<lens>.md` is now an authored artifact, not a derived one.** Anything that writes there from a non-critic source (an orchestrator rewrite-loop in Step 11, a manual operator edit, a future tool) is now a contract violation, not a convenience. The candidate explicitly punts on the v2 question (Explore Gap 3 / scope-map "named gap") — that is an unresolved commitment, not a deferred implementation detail. Once shipped, the next session that hits a Step 11 rewrite has to answer it under load.
- **The thin-index `critiques.md` is now a *schema* the operator and Step 12 read against.** Three rows, three columns, fixed labels. The candidate calls it "thin index" as if it were free-form, but Step 12 synthesis will now grep it for verdict labels. That is a schema. The candidate does not name it as one. Anyone who later wants to add a fourth lens, a sub-verdict, or a per-lens timestamp now has to migrate this format.
- **Per-lens output structure is frozen as divergent.** The candidate explicitly refuses a shared schema (Position §3 of "What is explicitly *not* added"). That refusal is itself a commitment: future readers — including future critic agents in the rewrite-loop — must accept that architecture has 6 sections, operations has 7, product has 6, and the verdict line is at different positions. Any future tool that wants to extract "the verdict" from all three uniformly inherits this divergence. That is a contract about *non-uniformity*, which is the most expensive kind.

## 3. Migration burden

Named, not hand-waved:

- **The operator** (the only "user" of this surface). They must unlearn "read critiques.md to see what the panel said." The CLAUDE.md edit Step 10 wording is the prompt that retrains them, but only inside this stack — operator muscle memory across forks, copies, and the user's own historical mental model of the workflow has to flip. The candidate's tradeoff table treats this as zero. It is not zero.
- **Step 12 synthesis prose in CLAUDE.md** (orchestrator-as-itself, every session). The line in Step 12 that reads "Critiques summary" must be re-pointed. Scope-map names this; the candidate does not name *who* updates that text or when.
- **The session-artifacts [README](.claude/session-artifacts/README.md)** — operator-facing documentation describing what `critiques.md` is. Scope-map names it as `replace`. Migration is a doc edit, but it is a doc edit *on the same PR* or the README lies for one session.
- **Two prior session directories** (`2026-04-26-format-only-state-transition-gate`, `2026-04-26-upgrades-lab-design`) contain the *old* shape of `critiques.md` (full transcription, not thin index). The candidate says "existing files stay as historical artifacts." Fine — but anyone reading those sessions for precedent now has to know the contract changed on 2026-04-27 to interpret them correctly. That is a known unknown the candidate does not flag in the migration list.
- **The critic agents themselves** (under Defense 2's auto-replan-on-self-modification rule). The next time *any* critic-* agent is touched — typo fix, reword, new section, anything — the orchestrator auto-routes to replan regardless of panel verdict. Defense 2 hard-codes a session-length penalty on every future change to a critic. The candidate frames this as "rare" (Way-could-be-wrong #2, A3) but the migration burden is on every future operator who touches a critic file and now must accept the replan loop. **This is a tax on a future class of work, not a one-time migration.**

## 4. Product affordances better / worse

**Better:**
- Audit faithfulness on the per-lens file is genuinely a category improvement (A4) when the operator goes looking for *what one specific lens said*. Click the path in the thin index, get critic-original prose. That is a real affordance.
- The thin index is *cheaper to scan* than the old aggregate when the operator only wants verdicts (3 lines vs. ~200). For the dominant "did the panel approve" question, this is faster.
- Per-lens files cleanly separate "lens was wrong" from "transcription was wrong" (canon-librarian inferred #4) — a debugging affordance that did not exist.

**Worse:**
- The "read everything the panel said in one place" affordance is *pruned*. The candidate calls this a `replace`-with-residue; from the operator's lens it is a *removal* — the old aggregate's load-bearing affordance was inline-readability, not just presence-on-disk.
- The "edit-the-aggregate to fix a typo" affordance disappears. Today the operator can edit `critiques.md` directly. Tomorrow that file is auto-generated; edits there are silently overwritten next session. The operator must edit the per-lens file instead. This is exactly the divergence that confuses operators in CI emitter migrations (outside-view §2 distillation, 80% success rate).
- **Auto-replan-on-self-modification is a withdrawn affordance.** Today, a typo fix on a critic-* agent runs through the normal panel and ships. Tomorrow it is forced through frame-level replan. The operator loses the ability to make small changes to critic agents cheaply. The candidate accepts this as a tradeoff but does not name it as an affordance loss — it is one.
- The "no shared schema" decision *prunes* a future affordance: any cross-lens analysis tool the operator might build later must handle three different formats. Today a paraphrasing orchestrator gives that tool a uniform feed; tomorrow the tool inherits the divergence.

## 5. Frame-level objection

The candidate's frame is "orchestrator parsimony bounded by write-target boundary." Both Alt-1 (orchestrator parsimony) and Alt-2 (boundary) are *orchestrator-internal* frames. **Neither names the operator as a stakeholder of the artifact shape.** From the product lens, the panel's output is not an internal aggregation — it is the operator-facing surface that drives the entire Step 12 synthesis the operator reads. Reframing as "orchestrator parsimony" treats `critiques.md` as orchestrator-internal scratch when in practice it is the *single most-read panel artifact by the operator*. The candidate's tradeoff table never asks "what does the operator lose when this file changes meaning?" — it only asks what the *orchestrator* gains.

A second frame-level objection: **the candidate accepts Defense 2 (auto-replan-on-self-modification) without product-lens scrutiny of the operator-tax.** Defense 2 is sold as cheap because self-modifying changes are rare. But the operator surface is not "how often does this fire" — it is "what happens to the operator's flow the next time it fires." The next time anyone touches a critic-* file (which the upgrades ledger suggests will be soon: this session itself, plus #3, plus #14, plus the shadow-comparator from #5 are all critic-adjacent), the operator pays the replan cost. The candidate frames this as "structural defense"; from the product lens it is a *workflow tax with no opt-out*, instituted to defend against a recursion bias that is itself unmeasured (A3 is the most likely to flip). Instituting an unconditional tax to mitigate a hypothetical bias is a product decision, not an architecture decision, and the frame does not treat it as one.

## 6. Verdict

**rework.**

Verdict flips to `approve` if the candidate (a) names the thin-index format as a schema and pins it explicitly (3 columns, fixed verdict-label vocabulary, with a one-line spec in CLAUDE.md the operator and future tools can rely on), and (b) replaces Defense 2's unconditional auto-replan with a *softer* operator-facing affordance — e.g., a one-line warning at Step 10 ("self-modifying change detected; consider replan") that the operator can accept or override, preserving the cheap-edit affordance for typo-class changes while still flagging the recursion concern.
