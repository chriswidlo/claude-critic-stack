# Critic — Product lens (revision 2 review)

## Opening dissent

Revision 2 trades the marketing-downgrade hazard for a different product hazard: **the user came with a decision request and is leaving with a diagnosis plus three sketches.** From the product lens, the most user-noticeable change is not what the stack ships — it is what the stack *did with the user's question*. The user asked "how should we approach critic target-repo read access"; revision 2 answers "we shouldn't approach it yet, here are three artifacts that describe what approaching it would look like." That is a defensible product posture, but it must hold up as one. Whether it does depends on whether the user's question can be honestly answered without a structural commitment today. I read the question as diagnostic-acceptable — not contract-required — so the posture holds. But it holds *narrowly*, and W1 is the right thing to flag.

## 1. User-visible consequence

What the user observes from this session, on day 1:

- **A synthesis containing three diagnostic claims**, no edits to [CLAUDE.md](CLAUDE.md), no edits to [`critique-start`](.claude/skills/critique-start/SKILL.md). The user-facing claim of "three independent critics" is *not* retracted in the headline; it is *footnoted* additively (move 4) — the headline reads the same, with an additional accuracy note. No round-trip risk on the marketing handle.
- **Three new entries under `upgrades/`**: one `profound` for the candidate-shaping probe, one `profound` for typed-candidate vs. invariants-only-feed vs. single-rubric-judge, one `no-brainer` for the doc-accuracy footnote. Per the lab-is-creative-hub memory, these are sketches and are allowed to be wrong.
- **No change to step 10's contract.** A user running `critique-prep` + `full-explore` today gets exactly what they got yesterday.

The user-visible delta on day 1 is: a footnote, three new files in `upgrades/`, and a synthesis. That is a small, honest day-1 footprint.

## 2. Commitments implied

- **The footnote (move 4) is a public commitment to "role-decorrelated on shared input, optional inter-model triangulation under SHADOW_PANEL=1"** as the panel's stated property, alongside the existing handle. This is additive; it does not retract.
- **Three upgrade entries become part of the corpus of designed-but-not-chosen options.** The commitment is "these options exist in writing"; the stack is not committed to executing any of them.
- **The diagnostic claims in synthesis become quotable.** If the probe later contradicts them, the synthesis is wrong on record. This is a real but acceptable epistemic commitment.

Notably absent: no commitment to a load-bearing artifact schema; no commitment to a candidate-composition discipline rule; no in-flight session migration story is required.

## 3. Migration burden

- **Existing `critique-prep` + `full-explore` users.** Zero change. Step 10 contract is untouched.
- **Mid-session users at step 10 when synthesis lands.** Zero change.
- **Readers of [CLAUDE.md](CLAUDE.md)** acquire one new sentence (the footnote).
- **Readers of `upgrades/`** see three new entries. Burden is zero unless they choose to engage.

The migration burden under v2 is order-of-magnitude smaller than v1.

## 4. Product affordances better / worse

**Better:**
- The user gets an honest answer to a diagnostic question.
- The footnote (move 4) makes the panel's actual property readable in CLAUDE.md without rewriting the headline.
- The probe upgrade entry (move 2) names a cheap experiment the user can run later. The user leaves with a path back to the decision, not a closed door.

**Worse:**
- **The user does not leave with a mechanism.** A user who came expecting a structural commitment gets none. The candidate names this in W1 and asks synthesis to address it head-on; that is the correct mitigation, but the affordance loss is real.
- **Authoring three upgrade entries is session-cost the user did not ask for.** W2 names this. The ledger will reflect it.
- **The handle "three independent critics" remains in active use** — better for continuity, worse for the precision-seeker. Move 4 mitigates this through addition rather than replacement.

## 5. Frame-level objection

Revision 2's posture is "answer the decision question as a diagnosis." This is acceptable *if and only if* the user's question is honestly answerable as a diagnosis. The candidate asserts it is — three diagnostic claims fit, and the structural commitment would be premature. I agree, narrowly, with one caveat:

The candidate frames the session as "user came with a decision request and leaves with a diagnosis + three follow-up artifacts + one footnote" and treats this as a feature. From the product lens, it is a feature *only if synthesis names the deferral as a deferral.* If synthesis presents the three diagnostic claims as a complete answer without flagging that the user's original decision space is still open, the posture reads as workflow theater. The candidate's W1 anticipates this and asks synthesis to mitigate by naming the deferred decisions and the cheapest experiment that re-opens them. That is the correct mitigation. The frame-level objection is not against the candidate — it is a load-bearing dependency on synthesis executing W1's mitigation. **If synthesis omits the deferral language, revision 2 fails as product even though it succeeds as candidate.**

A second frame-level read: the candidate declines three actions (don't edit `critique-start`, don't add candidate-composition prose discipline, don't retract the marketing handle). v2 *names* the decline (move 5) and explains why each was right not to do. This is the correction my prior review demanded. Frame objection from v1 is addressed.

## 6. Verdict

**approve**

What would change the verdict to reject: synthesis fails to name the deferred decisions as deferred, or fails to surface the cheapest experiment (the candidate-shaping probe) as the path back to the decision the user came with. If synthesis presents the three diagnostic claims as a closed answer, revision 2 collapses into the workflow-theater failure mode W1 names — and at that point the verdict flips on the synthesis, not on the candidate.
