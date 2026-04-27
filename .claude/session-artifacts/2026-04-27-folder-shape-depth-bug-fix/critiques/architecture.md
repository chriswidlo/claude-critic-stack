# Critic — Architecture Lens — Folder-shape depth bug fix (item 2)

## Verdict
**rework**

## Weakest structural link
The candidate elevates an ordering constraint between two punch-list lines into a hard sequencing dependency, but does not name the integration contract that would let item 2 be verified independently of item 1's commit. Item 2 is gated on item 1 ("do not proceed before item 1 commits") yet item 2's verification surface (a one-shot grep for `\.\./\.\./[^/.]`) is not a contract — it is a syntactic check that confirms the absence of a pattern, not the correctness of the rewrite. Under Option A, the correct invariant is "every link is repo-root-relative AND resolves to its intended target." The grep verifies the first half (path-style discipline) and entirely ignores the second half (resolution). The candidate has a **single-sided invariant check** masquerading as a definition-of-done. A proper contract: (a) zero `\.\./\.\.` chains in the three files AND (b) every rewritten link resolves to a path that exists on disk in HEAD. The "wrong-target-but-exists" failure mode (4 occurrences in [Explore.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/distillations/Explore.md)) demonstrates the failure class is real and silent.

## Invariants at risk (not already named by the candidate)
1. **Inbound-link integrity.** The candidate edits content but does not audit links *into* these files. The grep over `upgrades/*/*/README.md` does not see inbound references.
2. **Anchor stability under repo-root rewrite.** Per-line tables in Explore.md do not report whether the 27 links carry `#fragment` anchors. Mechanical hand-edit risks dropping or mistyping fragments.
3. **Rendering-context invariance.** Repo-root-relative paths render correctly in some markdown viewers and incorrectly in others. CLAUDE.md L7-16 mandates the form for *privacy and clarity*, not for click-resolution.
4. **Commit-bisectability under bundled item-2+item-3 diff.** A bisect lands on a commit that closes two punch-list lines; disentangling which of 27 edits caused a regression requires reading the diff.
5. **Ownership boundary between item 1 and item 2 around verification.** Both checks have to agree on the same regex contract. If item 1's eventual script uses a different pattern, the two checks diverge silently. The shared regex is a *protocol surface* the candidate does not name.

## Coupling and direction
- **Direction is wrong way.** Item 2 (content fix) currently depends on item 1 (rule decision). Healthy direction: rule depends on content (rule's text is shaped by cost of complying). Plan-before-evidence coupling.
- **Layering violation: bundling item 3 collapses two layers into one.** Item 2 is depth-arithmetic (`../../` → repo-root); item 3 is content-shape (flat `.md` → folder `README.md`). Different failure modes, different verifications.
- **Potential cycle via shared verification regex** between item 1 and item 2 with no single source of truth.

## Ignored architectural alternatives
1. **Generate the 27 rewrites mechanically with `sed`/`awk`** and review the diff, rather than hand-edit. Deterministic diff is its own falsifier.
2. **Ship `bin/check-path-discipline.sh` *with item 2*, not with item 1.** The script is the *contract* that makes item 2's done-condition machine-checkable. The test belongs with the first compliant artifacts, not the rule that authorizes them.
3. **Make item 2 a reversible *transformation* (a script in `bin/`)** rather than an *edit* to three files. Architecturally-correct unit-of-change is the converter, not the converted text.

## Frame-level objection
**The candidate treats "the punch-list" as the system boundary, but the punch-list is a transient operator artifact, not an architectural boundary.** The real system boundary is *the repo's link-graph*. Reasoning about item 2 as "27 links to rewrite" frames the work as bookkeeping over a list of strings; reasoning about it as "a node in a link graph that has stale outbound edges and possibly stale inbound edges" frames it as a graph-mutation with non-local effects. The architecturally honest frame: **"this is a graph-edit on a documentation graph; what edges are affected and what's the validation surface for each edge class."** Under that frame, the choice of which 3 files to touch is secondary to which *edges* are touched.

## Flip-to-approve conditions
The verdict flips to `approve` if the candidate adds (a) an inbound-link audit step before commit, (b) a resolution check (link target exists in HEAD) alongside the grep, and (c) a single source for the verification regex shared with item 1's plan — or alternately collapses the dependency by shipping `bin/check-path-discipline.sh` with item 2 and letting item 1's commit consume it.

## v2 review

**Verdict: approve**

### Flip conditions check
- (a) Inbound-link audit — addressed via `bin/check-path-discipline.sh --inbound` (v2 §step 2 third bullet, §step 6).
- (b) Resolution check — addressed via `--resolve`, fail-closed before commit (§step 5).
- (c) Single source for verification regex — addressed by shipping the script under item 2 and asking item 1's plan §Step 6 to consume it. Eliminates protocol-surface drift (invariant 5).

### New architectural risks introduced by v2
1. **Script-class risk.** Atomic per-line typo risk traded for batch-corruption risk. v2's mitigation (resolution check fires identically on script output) holds — the *failure-detection* surface is no larger; the *failure-shape* is correlated rather than independent. With `--resolve` fail-closed, fully-corrupted batches fail loudly. Acceptable.
2. **Cross-plan coupling to item 1's plan author accepting the script** (named in v2 §"could be wrong" bullet 2). Mitigation is procedural (orchestrator surfaces at synthesis), not architectural. Real residual risk; named and bounded.
3. **Assumption #2 (deterministic pattern table)** is the load-bearing new assumption. Four ambiguous `../../README.md` cases are correctly identified as failure trigger. v2's degradation path ("script + manual exceptions, both pass through `--resolve`") preserves the invariant.

### Is v2 worse-shaped on a different axis?
No. The work-product is now a reusable artifact (`bin/check-path-discipline.sh`) rather than three one-off edits — architecturally a better unit-of-change per my own §alternative 3.

The "direction is wrong way" frame objection from v1 is *still not addressed* — v2 declines to invert the dependency on operator-territory grounds (operator has not requested the demonstration). I do not re-veto on it. The frame objection stands as a recorded disagreement, not a blocker.

### Verdict sentence
Verdict would change to `reject` only if the operator decides authoring `bin/check-path-discipline.sh` is out of scope for item 2 (assumption #3 inversion), in which case the inline-snippet fallback re-introduces protocol-drift risk.
