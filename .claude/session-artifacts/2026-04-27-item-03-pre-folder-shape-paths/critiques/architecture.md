# Architecture critic — loop 1

**Verdict: rework.**

## Weakest structural link

Commit A's correctness depends on Commit B being a coherent unit, but Commit B's content is conditional on an operator answer that has no architectural carrier. The candidate names "commit B" as the policy decision's envelope, then defines its body as a branch on operator response (one sentence appended one way, four file edits the other way). That is not a commit envelope — it is two different commits sharing a placeholder name. Until the operator answers, Commit B has no schema, which means Commit A is shipping against a dependency whose shape is unknown. The "split commits" architecture is structurally indistinguishable from "one commit and a TODO" until the operator collapses the branch.

The deeper structural issue: the candidate routes a *policy decision* (binary, durable, scope-wide) and a *cleanup edit* (mechanical, local, reversible) through the same primitive — a git commit. Git commits are good carriers for the second and bad carriers for the first. A policy belongs in a file that names itself as policy ([`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md) or [`CLAUDE.md`](CLAUDE.md)), reachable by index, not buried in a one-sentence amend whose discoverability is git-log. The candidate inherits this category error from the plan and does not correct it.

## Invariants at risk

1. **Link-graph reachability under structural rename.** The candidate assumes that "the new targets are verified to exist on disk" makes Commit A safe. False — *display text* is preserved, but *anchor identity* under future refactors is not. If item 1 chooses a path style that requires anchors, the four lines edited in Commit A become a second-order migration target. **Falsification:** item 1 picks a style where today's `<slug>/README.md` is not a clean substring of the new form.

2. **Idempotency of the line-138 forwarding parenthetical.** The candidate adds a 5th edit that forwards a self-quoting reference. If the upgrade entry is itself ever migrated again (slug change, tier reshuffle, supersession by item 6), the parenthetical becomes a *second* stale reference inside the same sentence.

3. **Commit-parent semantics.** Naming `c2fe604` as the parent migration in Commit A's message presumes that git commit messages are read as a structural index. The repo has no convention establishing this; a future agent doing `git log --grep=c2fe604` may find the cleanup, but no tooling enforces or surfaces the link.

## Coupling and direction

Dependency direction is **inverted on the policy axis.** Commit A (concrete, low-volatility — four string substitutions) ships first; Commit B (policy, high-volatility — affects all future cleanup sweeps) ships second-or-never. The volatile module sits *downstream* of the stable one. That is the wrong direction for a policy primitive: stable-first means the policy frames the edits, not vice versa. The candidate inverts this by appealing to operator review cost, which is an operations concern, not an architecture one.

Commit C → Commit A is a **forward dependency on a not-yet-decided policy** (item 1's link-style choice). The candidate accepts a "known re-touch on the same 4 lines." That is a coupling cycle in disguise: A produces lines that C must rewrite; if C never lands, A is permanently in a known-stale style.

## Ignored architectural alternatives

1. **Make Commit A literally a `git revert --no-commit` of the offending lines from `c2fe604` plus a re-application that preserves the new paths.** That would let the commit's *parentage claim* be enforced by git, not by prose.

2. **A `redirects.md` primitive** (named in scope-map "Primitives the distillations did not name") that maps `<old-slug>.md` → `<slug>/README.md`. Edits 1–4 then become a single line in `redirects.md`, and the four READMEs need not be touched at all. The candidate dismisses option (b) from frame.md Reframe 1 without engaging it; that is the architectural alternative most directly motivated by the symptom class.

## Frame-level objection

**The candidate treats commits as the unit of architectural design.** The whole structure (A / B / C, "split commit envelope," parentage in commit messages) is a temporal-decomposition exercise. But the artifacts under discussion — link targets, policy declarations, README sentences — are *files in a graph*, not *deltas in a log*. The right architectural unit is the file-graph after the dust settles: which files reference which, which files declare policy, which files are immutable. Designing the end-state graph and then deriving the minimum commit sequence is the inverse of what the candidate does. By committing to the commit-as-unit frame, the candidate forecloses the file-graph alternatives (redirects file, policy-as-named-section, link-checker primitive) before they can be evaluated.

## What would change the verdict

Replace the three-commit temporal decomposition with a file-graph end-state design — name which files hold which roles after the change, then derive the minimum edit set; if the answer is still three commits, fine, but the derivation must come from the graph, not from the commit cadence.
