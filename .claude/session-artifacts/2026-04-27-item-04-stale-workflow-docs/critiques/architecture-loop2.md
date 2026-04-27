# Architecture-lens critique (Loop 2) — item 4: stale top-level workflow docs

**Session id.** `2026-04-27-item-04-stale-workflow-docs`
**Lens.** Architecture.
**Loop.** 2 (prior verdict on v1: rework).

## 1. Weakest structural link

**The pre-commit hook is a regex-based oracle for a categorical invariant, mounted on a write surface ([README.md](../../../../README.md)) that has no other tests, and bypassable per-commit.** The whole "shape-drift cannot happen silently" defense in v2 hinges on `grep -E '\b(12|10|three|3)[- ](step|agent|lens|lenses)\b' README.md`. That regex catches *the specific tokens v1 used*, not the structural property "README does not name counts." `"twelve-step"`, `"ten agents"`, `"3-lens panel"`, `"the panel of three lenses"`, `"a dozen steps"`, numerals followed by linebreak before the noun, or any future count drift to e.g. `13`/`11`/`four` are silent passes. Combined with the candidate's own admission that `--no-verify` is acceptable and the hook is "a prompt to think, not a hard constraint," the hook is *decorative-by-design*. That is a downgrade from v1's "no mechanism" only in that it now *looks* enforced.

This is a new weakest-link introduced by v2; v1's weakest-link (audience-as-third-surface) is genuinely retired by move #3.

## 2. Invariants at risk

1. **Hook-completeness invariant.** Denylist of four token shapes ≠ invariant "no count expression appears." A whitelist (parse README, fail if any number-word or numeral appears within N tokens of `step|agent|lens|critic|gate`) would be closer.
2. **Audience-symmetry invariant for [CLAUDE.md](../../../../CLAUDE.md).** Move #3 places the *Audience* section "just under the existing introduction" — does not specify byte offset. If the *Audience* section lands after the path-discipline block, the human-reader half of the audience claim is structurally below the fold.
3. **Redirect-stub freshness invariant.** `workflows/README.md` becomes a permanent redirect to CLAUDE.md. If the contract location ever moves, the stub becomes a *second* stale-routing case — exactly the class of bug item 4 was opened to fix. v2 introduces an artifact whose only failure mode is the same failure mode v2 is fixing.
4. **Trigger-observation invariant (still partly unaddressed).** The pre-commit hook is the observation mechanism for *count drift*; the deferred (b)/(c) revisit is still trigger-by-implicit-observation for *concept drift*.

## 3. Coupling and direction

- README → CLAUDE.md: still correct.
- **CLAUDE.md → README.md** (new, via *Audience* section's "that is in [README.md]"): introduces a back-edge. The contract doc now references the marketing doc. Direction is *volatile-pointed-from-stable*, the reverse of healthy.
- `workflows/README.md` → CLAUDE.md (new redirect): correct direction, low cost.
- `.githooks/check-readme-shape.sh` → README.md: hook is coupled to README's *vocabulary*, not its *structure*. Volatile coupling.
- Pre-commit hook → repo config: requires every clone to opt in. New contributors and new clones do not get the hook unless they run the config command. Per-clone-discipline, not per-repo-enforcement.

No new cycles. One new back-edge.

## 4. Ignored architectural alternatives

1. **CI check instead of pre-commit hook.** GitHub Actions step running the same grep on PRs would be repo-enforced and survive `--no-verify`. v2 chose the cheaper, weaker mechanism without naming the trade.
2. **Whitelist-style structural test.** Parse-and-assert the README's *What this is* section contains zero numeric tokens.
3. **Inline the *Audience* section at the *top* of CLAUDE.md.** Trivial structural choice, materially changes invariant 2.
4. **Make the CLAUDE.md → README.md pointer indirect** (anchor `README.md#what-is-this-and-why`). Anchors fail loudly; whole-file references fail silently.

## 5. Frame-level objection

v2 retires the v1 frame objection (audience-as-content-patch) cleanly: move #3 puts the declaration in CLAUDE.md, move #5 picks a single audience per doc, move #2 makes the README structurally count-free. Those are real structural responses, not content patches.

**New frame-level observation, not a veto:** *the candidate now treats "structural enforcement" and "a committed bash script that grep-matches a regex" as the same thing.* They are not. The architectural move v2 actually wants — "the README cannot drift in shape because something independent of the author's discipline catches drift" — is a *property of the build*, not a *property of a hook the author can bypass on the same commit that introduces the drift*. v2's structural answer is a discipline answer wearing a script costume. In a single-maintainer, no-CI repo, *habitual* may be the genuine maximum strength of a structural test. Either name that ceiling honestly or add CI.

## 6. Verdict

**approve.**

v2 addresses every specific approve-condition from loop 1 (audience moved to CLAUDE.md, count-free categorical README rewrite, concrete trigger-observation mechanism, redirect stub instead of deletion, single audience per doc). New architectural problems introduced by v2 are bounded and enumerable rather than frame-breaking.
