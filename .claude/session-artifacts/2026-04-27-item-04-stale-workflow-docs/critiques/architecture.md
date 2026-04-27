# Architecture-lens critique — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Lens.** Architecture (invariants, coupling, module boundaries, doc-surface as a system surface).
**Reads.** [candidate.md](../candidate.md), [frame.md](../frame.md), [challenges.md](../challenges.md), [scope-map.md](../scope-map.md), three distillations.

## 1. Weakest structural link

**The audience-declaration sentence is a third doc surface masquerading as a single line of prose.** The candidate's whole architectural defense rests on the claim that the post-(a) doc surface is *two* canonical surfaces with disjoint scope — [CLAUDE.md](../../../../CLAUDE.md) (behavioural) and [.claude/session-artifacts/README.md](../../README.md) (layout). The audience declaration is treated as "inline prose, not a new surface." This is wrong by structural test: the declaration carries semantics that nothing else in the repo carries — *who the workflow surface is for*. That semantic now lives on exactly one line in [README.md](../../../../README.md), with no inbound links, no test, no enforcement, and no shadow elsewhere. Any future doc decision (Heilmeier rewrite, forker-onboarding section, contributor doc) has to *consult that line* to remain coherent. A doc surface is not defined by file count; it is defined by *whether other artifacts must be kept in sync with it*. By that test the audience declaration is a third surface, undocumented as such, owned implicitly by README.md, and silently coupled to every future doc change.

## 2. Invariants at risk

The candidate names none. At least four are load-bearing and unstated:

1. **One-source invariant for the 12-step contract.** Post-(a), [CLAUDE.md](../../../../CLAUDE.md) is the *sole* place the 12-step / 10-agent / three-lens-panel shape is named. The README rewrite reintroduces a *parallel description* of that shape. If the README's paragraph drifts even by one count (12→13 steps, 10→11 agents, "three-lens" → "four-lens"), the invariant breaks silently.
2. **Inbound-link invariant on `CLAUDE.md`.** Its inbound-link count goes from ~0 (auto-loaded) to 1 human-facing inbound. That changes its *contract*: it must now read coherently from the top to a cold human reader, not just to an orchestrator with the file already in context. The candidate does not audit whether CLAUDE.md currently satisfies that contract.
3. **Trigger-observation invariant.** Trigger-based deferrals require *something that observes the trigger*. The candidate writes the trigger into the upgrade entry and stops. There is no scheduled re-read, no reverse pointer from CLAUDE.md, and no link from the README. The triggers are write-only.
4. **Scope-disjointness invariant for the two pointed-to docs.** The candidate's defense leans on *"tolerable when scopes are disjoint."* The candidate's gap statement names *what the union does not provide*; it does *not* name *what each one separately provides*. The disjointness is asserted, not labelled.

## 3. Coupling and direction

- README → CLAUDE.md: direction is correct.
- README → session-artifacts/README.md: README is now coupled to artifact-layout churn for reasons unrelated to the workflow. Direction suspect.
- **Audience declaration → everything else:** the audience sentence is *upstream* of every future doc decision but lives *inside* README.md, which is the most volatile doc. A stable contract embedded inside a volatile container is a layering violation. The audience declaration belongs in [CLAUDE.md](../../../../CLAUDE.md) (where the workflow contract already lives), *not* inside the README's mutable prose.
- **Trigger record → upgrade entry:** the trigger lives in an upgrade entry whose lifecycle row will be marked 🔨 implemented at the end of this PR. An "implemented" upgrade entry is exactly the kind of artifact that stops being read.

## 4. Ignored architectural alternatives

1. **Put the audience declaration in [CLAUDE.md](../../../../CLAUDE.md), not README.md.** Eliminates the third-surface drift risk entirely.
2. **Make the README a thin pass-through with a structural test.** Replace lines 7-13 with a *categorical* description that does not name counts at all, and add a CI-equivalent grep test.
3. **Delete README.md's workflow section entirely; replace with one sentence pointing at CLAUDE.md.** Honest about the audience the candidate already declared.
4. **Replace the empty `workflows/` directory with a single redirect file rather than deleting it.** Asymmetric: cost of keeping a stub is one file; cost of an external 404 is unrecoverable.

## 5. Frame-level objection

**The candidate inherits the frame-challenger's audience reframe but applies it as a content patch, not a structural one.** The candidate accepts the verb *declare* (good), but does not accept the *consequence* — that the doc shape should fall out of the declaration. It ships the prune **and** the declaration in the same PR with the doc shape unchanged. The frame-level objection is therefore *acknowledged*, not *addressed*.

A second frame-level objection: **the candidate treats "the maintainer + Claude" as a single audience, but they have orthogonal doc requirements.** Claude reads CLAUDE.md auto-loaded; the maintainer reads README.md on `git status`/`gh repo view`/IDE-open. They do not share a reading order, do not share a doc surface, and do not share failure modes. Bundling them as "the live audience" papers over the only architecturally interesting question.

## 6. Verdict

**rework.**

What would change the verdict: move the audience declaration out of README.md and into CLAUDE.md (or commit to a categorical, count-free README rewrite plus a structural test that prevents shape-drift), and add a concrete trigger-observation mechanism rather than a write-only trigger record in the deferred upgrade entry.
