# Generator candidate v2 — ark-mono phantom fixture

**v1 was reworked.** All three lenses returned `rework`. Convergent themes:
- The exemplar contract must be authored **this session**, not deferred to item 5b. (operations explicit, product implicit, architecture cycle-cut compatible)
- No placeholder in [CLAUDE.md](CLAUDE.md). (architecture citation-style invariant + product primary-surface objection)
- Item 5b has no forcing function and would be a "second phantom." (all three lenses)
- The exemplar contract needs a home module, not floating prose. (architecture explicit)

v2 incorporates all four. The shape changes from "split-and-defer" to **"author-the-contract-and-substitute-now."** The deferred work (running the regression) is named separately but no longer treated as a punch-list row dependent on this session — it becomes an explicit, dated maintenance contract on the on-disk contract document itself.

## Position (v2)

Recommend **option (b'), a tightened variant of (b) — substitute-with-contract**, executed as four atomic edits in this session, in this order:

1. **Author [`tests/regression/EXEMPLAR-CONTRACT.md`](tests/regression/EXEMPLAR-CONTRACT.md)** as the named home module for promotion semantics. This is the architecture lens's missing module. Required content (drafted in this session, not deferred):
   - **Promotion semantics.** Whether `.claude/session-artifacts/<session>/` → `exemplars/<slug>/` is a copy, a hard-link, or a curated rewrite. Decision: **copy, no edits between source and copy**. This preserves the immutability norm flagged by the scope-map. If the source needs editing for clarity, the edit happens *to the source* before promotion (under the operator's named consent), not silently during promotion.
   - **Wrong-spec-vs-wrong-agent rule.** When a regression run produces output diverging from the test's acceptance criteria: the test is amended (spec was wrong) only if the divergence is in step structure (a step name, a missing step, a step ordering). The agent is amended (impl was wrong) if the divergence is in step *behavior* (a scope-mapper that defaults to `extend`, a critic-panel collapsing to one verdict). Mixed cases: the operator's call, recorded in `decision-log.md` of the failing run.
   - **Distiller-step coverage requirement.** Any regression test in `tests/regression/` must include an acceptance criterion for step 6 (distillation) of the workflow. Tests authored before the distiller step was inserted (currently: `ark-mono-connector-routing.md`) are flagged on this page as **out-of-coverage** until amended.
   - **Max-edits-before-failed-attempt.** A first-run exemplar attempt may be amended at most twice between authoring and acceptance. A third amendment downgrades the run from "exemplar candidate" to "draft session" — re-author the test or pick a different scenario.
   - **Maintenance schedule.** This contract document is reviewed every workflow change to `CLAUDE.md` step list. The review is gated on file-mtime: if `CLAUDE.md` mtime is newer than `EXEMPLAR-CONTRACT.md` mtime, a regression-discipline review is owed. This is the architecture lens's "owner module" answer and the operations lens's "forcing function" answer in one mechanism.

2. **Substitute the example slug in [CLAUDE.md](CLAUDE.md):20 and [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md):23 to a real, currently-existing session id: `2026-04-26-format-only-state-transition-gate`.** This is option (b)'s substitution path, but executed *with* the contract above already on disk, which mitigates the "norm-setting risk" the outside-view distillation called out for naked (b). Both citations now point at a real, navigable, on-disk artifact. The word-order divergence is gone; the placeholder problem (product lens) does not arise.

3. **Add to [CLAUDE.md](CLAUDE.md)'s path-discipline section** (where reasons (a)-(d) currently live) one sentence: *"Example session ids in this file and in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) must reference real on-disk session-artifact directories. Fabricated example slugs are a documentation defect."* This is the architecture lens's "rule, not polite note" requirement.

4. **Mark item 5 in [`plans/2026-04-27-repo-cleanup-punch-list.md`](plans/2026-04-27-repo-cleanup-punch-list.md) as `✅ done <date>`** and append a one-line reference: "exemplar contract at [`tests/regression/EXEMPLAR-CONTRACT.md`](tests/regression/EXEMPLAR-CONTRACT.md); regression run remains unscheduled — see contract's `## When the next run becomes owed` section." Do **not** create item 5b as a new punch-list row — the contract document is the home for that work, not the punch list. (This addresses operations' "second phantom" critique and architecture's "cycle" critique by relocating the deferred work into a forcing-function-equipped surface rather than a forcing-function-free one.)

The regression-discipline review-mtime mechanism in step 1 is the forcing function: any future change to `CLAUDE.md`'s step list (e.g., inserting a step 13, renaming a critic lens, splitting a step) makes mtime newer than the contract, surfaces an obligation, and that obligation prompts re-evaluation of whether to run the regression now. The empty `exemplars/` directory is no longer a free-rider; it is bonded to a forcing surface.

## How v2 addresses each lens's rework objection

**Architecture rework asked for:**
- Owner module for the contract → [`tests/regression/EXEMPLAR-CONTRACT.md`](tests/regression/EXEMPLAR-CONTRACT.md) (step 1).
- Cut the cycle between contract and audit → audit happens *as the contract is authored* (the distiller-coverage finding is recorded in the contract this session, not in 5b later).
- Placeholder rule into CLAUDE.md path-discipline → step 3.
**Architecture rework: addressed.**

**Operations rework asked for:**
- Named forcing function for the deferred work → mtime-gated review in the contract (step 1's "Maintenance schedule").
- Observable surface outside the punch-list → the contract document and its review-owed status.
**Operations rework: addressed.**

**Product rework asked for:**
- Drop the placeholder in CLAUDE.md → step 2 substitutes a real slug.
- Either author the contract this session OR acknowledge bespoke handling → step 1 authors it this session.
**Product rework: addressed.**

## How v2 addresses the original frame-level objection (challenges.md F4)

F4: *the menu (a)/(b)/(c) presupposes the regression-test spec is current; without a spec-currency audit before option selection, recommendation is generating against an unverified premise.*

v2 does the spec-currency audit and records its result in the contract document (step 1's "Distiller-step coverage requirement" — flagging `ark-mono-connector-routing.md` as out-of-coverage). The audit becomes a load-bearing part of the contract, not a precondition for it.

## Named tradeoffs (v2)

- **Operator attention this session is higher.** v2 authors a new file (the contract) and edits three existing files. v1 only edited two existing files. The trade is real and is the trade operations critic demanded.
- **Substituting a real session for the example slug is the option v1 (and outside-view) called "below base rate" because of norm-setting risk.** v2 mitigates this by pairing the substitution with the explicit rule in CLAUDE.md (step 3): real slugs only, fabrication is a defect. The norm being set is "real slugs," not "any slug."
- **The exemplars directory remains empty.** v2 does not run the regression. The mtime-forcing-function ensures this state is *bonded*, not *free*, but the empty directory is still on disk. The architectural alternative the architecture critic raised — "promote a stub exemplar" — is rejected: a stub exemplar would be a third citation style at the artifact level, mirror-image to v1's third-style problem at the citation level.
- **Item 5b is not created.** v2 deliberately does not grow the punch-list. Architecture, operations, and product all flagged that creating 5b would compound the original problem. The work is captured in the contract, which has its own forcing function.

## Named assumptions (≥3 that would flip the recommendation)

1. **Substituting `2026-04-26-format-only-state-transition-gate` as the example slug is acceptable to the operator.** That session is real and on-disk. If the operator considers it not exemplary enough to be the canonical example (e.g., it's mid-stack-evolution, or it has known incident-shaped issues), pick a different real session. The substitution is the load-bearing move; the specific session is a parameter.
2. **The mtime-based forcing function is reliable enough.** It assumes the operator runs `git status` or `ls -lt` on `tests/regression/` periodically, or that some pre-commit hook surfaces "contract older than CLAUDE.md." If neither, the forcing function degrades to "operator memory," which is what operations rejected. Cheap mitigation: a one-line `bin/check-regression-discipline.sh` that prints "review owed" if mtimes diverge — but adding scripts is out of scope for this item; **flag this as a follow-up if the basic mtime convention is insufficient**.
3. **Authoring the contract this session does not balloon.** The contract draft above has five sections, all writable in roughly the same time as v1's longer §Position. If the contract authoring discovers that any of its rules require deeper consensus (e.g., "wrong-spec-vs-wrong-agent" turns out to need a worked example to be unambiguous), the recommendation flips back toward v1's split-and-defer — but with the contract as the home and the punch-list still gaining a row 5b for the worked example.
4. **The architecture critic's "regression-discipline subsystem doesn't exist" objection is sufficiently addressed by naming a single owner module.** The critic suggested deeper restructurings (embed criteria in agent prompts; collapse two directories into one). v2 does the minimum that closes the immediate critique. If the operator finds the contract document still feels like ceremony-without-substance after authoring, the deeper restructuring is the next layer.

## Named ways v2 could be wrong

- **The contract document becomes ceremony-without-baseline itself.** It has no run behind it; it is asserting rules for runs that have not happened. Mitigation: the document is short, opinionated, and its own out-of-coverage flag is on it from day one (the distiller-coverage rule plus the explicit "ark-mono test is out-of-coverage until amended" annotation). It does not pretend to authority it lacks.
- **The substituted slug ages out.** `2026-04-26-format-only-state-transition-gate` is currently exemplary; if a future repo cleanup deletes it (unlikely — session artifacts are immutable per the README's stated norm), the citation breaks. Re-citation cost: low.
- **The mtime forcing function is a polite-note-disguised-as-mechanism.** Operations critic explicitly named "documentation, not a control" as a failure mode. mtime is technically a control (it is observable file metadata), but it requires the operator to know to look. If this is ineffective, the assumption-2 mitigation (a check script) becomes mandatory.
- **The "real slugs only" rule in CLAUDE.md (step 3) is not enforced by anything other than reading.** Same critique as above. Same mitigation path (a grep-based pre-commit). v2 ships the rule and accepts the enforcement gap, on the bet that the operator who authored the path-discipline regime in `5108ed3` reads CLAUDE.md carefully.

## Hard-gate verification

- [`scope-map.md`](.claude/session-artifacts/2026-04-27-ark-mono-phantom-fixture/scope-map.md) exists ✓
- [`challenges.md`](.claude/session-artifacts/2026-04-27-ark-mono-phantom-fixture/challenges.md) exists ✓
- v2 explicitly addresses the frame-level objection from challenges.md (F4 — spec-currency audit done in this session, recorded in the contract).
- ≥3 named assumptions that would flip the recommendation are above.
