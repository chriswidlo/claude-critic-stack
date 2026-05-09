# Critic — Product lens

## Opening dissent

The single most user-noticeable change in this candidate is not "critics get a cleaner contract." It is that the panel publicly retracts a property it has been claiming. A user who has been telling colleagues "I run my designs through three independent critics" walks back to "I run my designs through three role-decorrelated lenses on a shared candidate." That is a marketing downgrade dressed as a clarification, and the candidate executes it without doing the product work of (a) choosing the replacement language carefully, (b) auditing where the old language already appears in user-facing artifacts, or (c) telling existing users what their previous sessions' verdicts now mean.

## 1. User-visible consequence

Three concrete surface changes a user will observe on day 1:

- **The panel's stated property in [CLAUDE.md](CLAUDE.md) changes wording.** Anyone who has read CLAUDE.md and internalized "minority-veto on three independent critics" now reads a smaller claim. Users who derived confidence from the larger claim get less confidence; users who derived skepticism from the larger claim get an honest answer. The candidate does not name which group it expects to retain.
- **The default behavior of `critique-start` step 10 changes from "critics may receive `$CRITIC_TARGET` if they verify facts (orchestrator's call)" to "critics receive `$CRITIC_TARGET` only if a `decision-log.md` entry names a fact that requires target verification."** A user running `critique-prep` with `full-explore` strategy on a real target previously had at least the *possibility* their critics saw the target. Now, by default, they don't — and they have to author a justification line to opt back in. This is a user-facing affordance change, not an internal cleanup.
- **A new session artifact requirement appears: an opt-in entry in `decision-log.md` per lens that gets `$CRITIC_TARGET`.** This is paper trail that didn't exist. Every session that wants grounded critics now produces a machine-grep-able record of *which* critic was grounded and *why*. That record is committed to git history.

## 2. Commitments implied

Once the candidate ships, the stack is committed to:

- **The smaller independence claim.** Reverting to "information-independent panel" later would require explaining the round trip to anyone reading the changelog, and the act of having retracted it once makes future re-claims read as marketing rather than property.
- **`decision-log.md` as a load-bearing artifact for grounding decisions.** Today `decision-log.md` is mentioned in CLAUDE.md step 11 as a place to record "step 10 verdict was X; rewrite vs. replan; routed to step Y." The candidate adds a second responsibility (logging per-lens target-pass-through reasons) without acknowledging the schema collision. The first time a user has both a step-11 routing decision *and* a step-10 grounding opt-in for the same session, the file's structure is ambiguous.
- **A semantic distinction between "invariants" and "narrative" in `explore.md`.** The scope-map proposed this labeling; the candidate does not adopt it but also does not reject it. If move (3) — candidate-composition discipline — is to mean anything, the orchestrator needs a way to know which target-repo facts are quotable as `<target>/...` references in the candidate body. That is a downstream artifact-schema commitment the candidate hand-waves.
- **The `<target>/...` reference becomes a contract, not just a path-rewrite hygiene rule.** Today `<target>/...` exists for path privacy ([CLAUDE.md](CLAUDE.md) Path discipline). After the candidate, `<target>/...` is also a *content-access boundary* — quoting via it is allowed, paraphrasing is not. A single token now carries two concerns.

## 3. Migration burden

Named users and what they have to change:

- **Any user mid-session at step 10 when the change lands.** The conditional clause in [`critique-start`](.claude/skills/critique-start/SKILL.md) lines 38–42 changes meaning under their feet. Sessions started under "if they verify facts" terminate under "default-no unless logged." The candidate does not specify whether in-flight sessions grandfather the old contract.
- **Users with existing `critique-prep` + `full-explore` workflows.** They have been operating under an assumption that critics may see the target. They now have to learn (a) that critics don't, by default, (b) that they can opt in via `decision-log.md`, (c) what counts as a "fact that requires target verification" worthy of opt-in. The candidate frames this as zero-friction; it isn't. It is a new mental model the user has to acquire to retain their previous capability.
- **Authors of `upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md`.** That entry pre-supposes the old independence claim as its problem statement. Per the lab-is-creative-hub memory, upgrade entries are not edited by cleanup — but a reader of that entry now reads it against a stack whose claim has shifted, and the entry's diagnosis ("Opus reading itself three times") makes more sense, not less, under the new claim. Mild discordance, not a blocker.
- **Future authors of `question.md`.** The scope-map flagged that question.md's "Constraints / context" block is an indirect leakage vector. If candidate-composition discipline (move 3) is real, question.md authors need a parallel discipline. The candidate addresses candidate.md but not question.md. A user who uses question.md to embed target framing has bypassed the discipline through a side door.

## 4. Product affordances better / worse

**Better / newly possible:**

- A user can now read CLAUDE.md and know *what claim the stack is making*. Before, "three independent critics" implied properties the stack does not enforce; the smaller claim is at least operationally honest. This is a real product win for users who care about epistemic accuracy of the tool's self-description.
- A user who *wants* a grounded operations critique can now declare it explicitly via `decision-log.md`, rather than relying on the orchestrator's silent judgment of "if they verify facts." Surfacing the decision is a usability improvement for the subset of users who want grounded critique and currently can't tell if they're getting it.
- The `<target>/...` reference becomes a clearer affordance: candidate authors know what they may quote and what they may not.

**Worse / pruned:**

- **The default path to grounded critique gets longer.** Previously, the orchestrator could pass `$CRITIC_TARGET` at step 10 inline; now it requires a `decision-log.md` entry. For users whose sessions routinely benefit from grounded critique (operations-heavy decisions on real targets — exactly the case the canon PRR passage supports), this is friction.
- **A class of session — "I want all three critics grounded against this real codebase" — becomes verbose.** That's three `decision-log.md` entries. Achievable, but the friction will push users toward "I'll just leave them ungrounded," which is the failure mode the outside-view's primary reference class names.
- **The marketing language "three independent critics" is harder to use honestly.** That phrase, however imprecise, was a usable handle for talking about what the stack does. Replacing it with "three role-decorrelated lenses on a shared candidate, optionally inter-model triangulated under SHADOW_PANEL=1" is more accurate and less communicable. The candidate does not propose a replacement handle.

## 5. Frame-level objection

The candidate frames itself as "decline the user's solution menu (preserve / restrict / isolate / formalize)" and substitutes a fifth move. From the product lens, declining the user's menu is not neutral — it is a posture choice. The user came to the stack with a specific decision in mind; the candidate tells them their decision space was wrong. There are cases where that is the right move (the user genuinely framed badly), and there are cases where it reads as the tool refusing to let the user buy what they came to buy. The candidate does not distinguish. Specifically: a user who *has* a threat model in mind ("I worry the critics rubber-stamp anything they recognize from the target") is told their menu was based on a flawed presupposition and offered an experiment-before-mechanism path instead. That user wanted a mechanism. Telling them "measure first" is a product choice, and it is the choice that says "the stack's correctness comes before the user's velocity." That is defensible but it should be named, not smuggled in under "decline the menu."

A second frame-level objection: the candidate treats this as a contract-formalization decision (architecture lens) and a measurement decision (operations lens). From the product lens, the load-bearing question is *what story does the stack tell users about what it does*. Move (1) is a product-copy change. Treating it as a side effect of the contract change is a category error — the wording in CLAUDE.md is the user-facing surface that determines whether the rest of this work is perceived as honest course-correction or as quiet capability removal.

## 6. Verdict

**rework**

What would change the verdict to approve: (a) the candidate names the replacement marketing handle for "three independent critics" and audits user-facing artifacts (README, CLAUDE.md, upgrade entries) for places the old phrasing leaks, (b) move (2) specifies in-flight session grandfathering and resolves the `decision-log.md` schema collision with step 11's existing use, and (c) move (3) extends candidate-composition discipline to question.md and explore.md (invariants vs. narrative labeling) rather than addressing only candidate.md.
