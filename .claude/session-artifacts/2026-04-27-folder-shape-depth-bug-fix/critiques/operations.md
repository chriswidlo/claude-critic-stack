# Operations critique — folder-shape depth bug fix (item 2)

## Verdict
**rework**

## Most likely incident
At time T (next click on a link in [`upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md`](upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md) — could be same-day, could be three weeks out): a `404` or silent navigation to wrong file caused by a hand-typed typo in a rewritten path (e.g., `claude/agents/...` instead of `.claude/agents/...`). Root cause: the candidate's verification step (`grep -rn '\.\./\.\./[^/.]'`) only checks for *residual chain pattern* and is structurally incapable of detecting typos in the *new* repo-root path — it greps for what was removed, not what was added.

## Blast radius
Bounded but not zero. 27 rewritten link bodies across 3 README files in the active `upgrades/` surface. Readers: the operator on click, future agents traversing links, external clones. No production system. On-call cost is *paid by the next reader*. Inbound-link blast radius is unknown — Explore explicitly flagged that check as not performed; scope-map carried the gap forward unresolved.

## Rollout / rollback
- **Rollout strategy:** none beyond "one commit." No canary, no flag — defensible *if* verification is sound; verification is not sound.
- **Rollback path:** `git revert <sha>` is clean. Bisectable per "one diff" framing. **Strongest operational property.**
- **Two-systems-running:** candidate treats cutover as atomic for the 3 files but explicitly leaves [`upgrades/profound/2026-04-27-r-and-d-lab-thesis/README.md`](upgrades/profound/2026-04-27-r-and-d-lab-thesis/README.md) in a known mixed state and 7 session-artifact occurrences as "broken-by-policy." That *is* a two-regimes-running period of indefinite duration. Cost: every future agent must know which directories follow which rule. Not named in tradeoff table.

## Observability gap
- No markdown-link-checker in CI (per requirement.md §gaps and scope-map primitive 9). Post-commit signal that a link is broken is *a human clicking it and noticing*. Not a control; a delayed user report.
- Proposed grep confirms absence of one *anti-pattern*. Does not confirm presence of *resolvable targets*. Different metrics.
- Mean-time-to-detection is unbounded.

## Cost at failure
- **Per-typo cost:** discovered weeks later, mid-task. Context-switch cost to diagnose "is this link wrong, or is the file gone?" is non-trivial in a repo where files *do* move (the whole reason this bug exists). 1-2 typos against 27 hand edits is the modal expectation, not a tail.
- **CI-hook cost (the road not taken):** one-time install of `lychee` / `markdown-link-check`; recurring cost ~seconds per commit. Candidate's reason for declining ("belongs to item 1") is an *ownership* argument, not an operational-cost argument.
- **Human on-call load:** zero pages. Cost shifted to the next reader. "Ship and grep" converts a synchronous one-time cost (CI hook) into an asynchronous N-time cost (every future click).

## Frame-level objection
The candidate frames this as a **content correctness problem solved by a one-shot commit + a one-shot grep**. The operations frame is that this is a **reader-facing surface with no mechanical health-check**. The relevant decision is not "what links should the 3 files contain" but "what is the standing verification regime for link health in this repo." Under the operations frame, shipping 27 hand edits with no link-checker is acceptable *only if* the link-checker is being installed in the same horizon — otherwise the proposal trades a known-broken state for an unknown-broken state, and unknown-broken is operationally worse because it removes the operator's ability to triage.

The candidate's answer ("the link-checker belongs to item 1") is an *ownership* claim that resolves cleanly only if item 1 actually commits. Per assumption #1, item 1's commit timing is the biggest uncertainty. **Item 2 is structurally coupled to item 1 not just for fix-form but for the entire post-ship verification regime, and that coupling is named in §coupling but not in §tradeoffs.**

Second objection: "session-artifact sanctity rule" excludes 7 broken-by-policy occurrences. From the operations lens, *broken-by-policy is still broken at click-time* — a reader cannot distinguish a sanctity-protected broken link from a typo. The candidate inherits a two-regime invariant and ships further into it without naming the operational cost.

## Flip-to-approve conditions
Verdict flips to `approve` if either (a) a markdown-link-checker invocation (lychee or `markdown-link-check`) is added to the verification step *for the 3 edited files specifically* — not a CI hook, just a one-shot resolution check the operator runs locally before commit, **or** (b) the candidate explicitly states item 1's link-checker hook is in the same operator session and item 2 will not commit until that hook is in place, making coupling-to-item-1 cover verification regime, not just fix-form.

## v2 review

**Verdict: approve**

### Flip-condition (a) — link resolution check on the 3 files
Addressed. v2 §step 5 adds `bin/check-path-discipline.sh --resolve <files>` and binds it fail-closed to the pre-commit gate. §step 2 specifies the mode resolves each link relative to repo root and verifies HEAD existence. Stronger than asked: a committed script rather than a one-shot local invocation, so the next operator inherits the check.

### Flip-condition (b) — coupling-to-item-1 covers verification regime
Addressed by inversion. I asked for item 2 to wait on item 1's hook; v2 inverts: item 2 *ships* the script item 1 will consume. Verification regime no longer depends on item 1 committing first.

### New operational risks introduced by v2
1. **Script-class failure replaces per-edit failure.** v2 names this. A pattern bug producing resolvable-but-wrong targets (e.g. the `../../README.md` ambiguity) passes `--resolve` and ships broken. Operations cost: same failure mode as v1, just relocated. No worse.
2. **Bisectability impact of mixed `bin/` + docs commit.** Future bisect implicating this commit must distinguish "script logic" from "doc edit." Mild — script behavior is verifiable in isolation by re-running `--resolve` against any sha. v2 does not name it.
3. **Coupling to item 1's plan author still exists, in reverse.** If item 1's author writes their own checker, protocol-drift returns. Orchestrator's only mitigation is procedural.
4. **Fail-closed gate is a script the operator must remember to run** — no CI hook installs this. If skipped on a hurried commit, v2 collapses to v1's failure mode. Same class of risk; v2 made the available control sharper, not eliminated.

### Residual operations gaps (not flip-blocking)
- The 7 broken-by-policy session-artifact occurrences acknowledged-and-shipped. My v1 §frame-objection-2 stands; v2 declines on operator-territory grounds.
- Post-commit MTTD for link rot remains unbounded — `--resolve` is pre-commit only.

### Verdict sentence
Approve. Verdict reverts to `rework` if the operator cannot commit `bin/` alongside doc edits (assumption #3 fails) and falls back to inline shell.
