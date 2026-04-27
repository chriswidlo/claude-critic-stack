# Product critique — item 13 (orphans fate)

Target: [candidate.md](../candidate.md)

The "user" of this repo is two-headed: (1) the maintainer (single-maintainer R&D repo), and (2) every future Claude Code session that reads CLAUDE.md and follows the 12-step workflow. Both are users.

## 1. User-visible consequence

**Maintainer:** the day this ships, `prompts/` is empty, `plans/` gains a backdated file `2026-04-24-phase-2-shipped.md` whose date precedes every other plan by three days, and CLAUDE.md grows a new step-9 sub-requirement. Most-noticed surface change is *the new step-9 obligation* — every future workflow run pays it.

**Next session-as-user:** the contract (CLAUDE.md) now demands a candidate-enumeration artifact at step 9. The existing generator structure does *not* naturally produce this. Behavioral change to every future session, not a one-time cleanup.

## 2. Commitments implied

- **CLAUDE.md step 9 now load-bears "≥3 candidate solutions."** Once a future session reads CLAUDE.md and produces three candidates, artifact shape has shifted; rolling it back means *removing* a step the workflow has started producing. Reversibility decays per session.
- **`plans/` convention now tolerates dated-shipped files.** The next maintainer reading `ls plans/` must now parse Status headers to distinguish in-flight from shipped. Parser-in-the-head is a contract.
- **Session-artifact directory is now load-bearing as a discoverability venue.** New affordance the directory was not previously asked to provide, committed-to without the directory's README being amended.
- **Empty `prompts/` directory becomes a "passive signal."** Future session sees an empty directory and must infer dormancy rather than absence — a contract on inference.

## 3. Migration burden

- **Every future Claude Code session** must produce ≥3 candidate solutions at step 9. Cost per session is non-trivial. Candidate amends CLAUDE.md without amending generator-step description in any agent file, without adding an example, and without updating any synthesis template. Next session discovers the requirement mid-flow.
- **Item 5's session** inherits O4. Pushing a punch-list item's closure into another punch-list item's session is the classic kicked-can: the punch-list grows a hidden dependency edge not represented in the punch-list itself.
- **The 6-month future-session test** is migration burden disguised as falsifier. Someone must remember to pose the test prompt in 6 months; candidate proposes no calendar mechanism, no agent invocation, no reminder. Not a test plan — an aspiration.
- **Any external link** that referenced `plans/ok-cool-this-is-warm-balloon.md` by path now breaks. Candidate's own §3 admits the dependency-direction grep was not done. Migration burden is unbounded until that grep is performed.

## 4. Product affordances

**Better:**
- `prompts/` no longer contains a 26 KB external-agent brief masquerading as reusable instruction.
- Warm-balloon design record stays in-tree, browseable from `ls plans/`. "I can see what alternatives Phase-2 rejected without `git log`-ing."
- Step 9 formally requires candidate enumeration, *if* honored.

**Worse / newly expensive:**
- `ls prompts/` returns an empty directory. To a fresh reader this reads as *forgotten cleanup*, not *intentional dormancy*. The candidate's framing is invisible to anyone who didn't read this session's artifact.
- `find . -name "*pressures*"` returns nothing. A future session that knows the term but not the storage location must guess to `ls .claude/session-artifacts/ | grep orphans`. Candidate's own falsifier admits this is the load-bearing risk.
- `plans/` is no longer parseable as "in-flight items." Anyone (human or LLM) who used the directory listing as a punch-list now has to filter on Status headers.
- Step 9's new requirement adds ceremony to every future session for an unmeasurable per-session benefit.

## 5. Frame-level objection

The candidate frames itself as "no new policy primitive" and uses that to claim it preserves contract simplicity. From product lens this is misleading: **the candidate ships three new contracts under cover of "no policy."**
1. New step-9 requirement in CLAUDE.md (workflow contract).
2. New `plans/` parsing convention (directory contract).
3. New role for `.claude/session-artifacts/` as discoverability venue (primitive contract).

"No new primitive" is being measured by *artifact count* (no new folder, no new file with "policy" in the name) rather than by *contract count*. From product lens, what the next session experiences is three unannounced contract changes, not a tidy refactor. The frame is the wrong unit. Right unit: "what does the next session-as-user have to do differently?" — answer: comply with three new things that aren't called policy.

Second frame-level objection: candidate treats the maintainer as the user but the harder user is the next session, which has no access to `.claude/session-artifacts/2026-04-27-item-13-orphans-fate/` *unless it knows to look*. Candidate's discoverability story collapses to "future session reads the synthesis," but the synthesis is itself only discoverable to a session that already knows item 13 happened. Circular discoverability claim; candidate does not break the circle.

## 6. Verdict

**`rework`.** Verdict flips to approve if the candidate (a) drops the CLAUDE.md step-9 amendment OR moves it to its own item with its own session, since slipping a workflow-contract change into a janitorial sweep is a product-surface bait-and-switch; (b) replaces "passive signal of dormancy" for empty `prompts/` with either deletion of the directory or a one-line `prompts/README.md` that says "intentionally empty pending next sweep" so the affordance is self-explanatory; and (c) names a concrete mechanism (calendar, scheduled canon-refresher invocation, punch-list re-open trigger) for the 6-month falsifier rather than treating "the maintainer remembers" as a product affordance.
