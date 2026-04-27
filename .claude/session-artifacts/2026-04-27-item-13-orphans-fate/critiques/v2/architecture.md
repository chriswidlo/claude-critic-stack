# Architecture critique — item 13 (orphans fate), v2

Target: [candidate-v2.md](../../candidate-v2.md)

## 1. Weakest structural link

The `<dir>/RETIRED.md` contract is *defined* as one-per-directory with directory-lifetime, but the only *instance* shipped in this commit is `prompts/RETIRED.md`. A convention with a population of one is indistinguishable from a one-off file with a fancy spec. The structural risk: rule 4 ("updated, never replaced") and rule 5 ("removed when the directory itself is deleted") are write-side invariants with no enforcement surface — no agent owns them, no lint checks them, no test asserts them. The contract is in the candidate doc; the candidate doc is in a session artifact that v2 itself argues is *not* a discoverability venue. The contract is therefore more orphaned than the orphans it disposes of.

This is a real improvement over v1 (the primitive is named, lives where readers will look, and does not couple `plans/` to session-artifacts), but the contract's persistence layer is unstated.

## 2. Invariants at risk

1. **`RETIRED.md` filename uniqueness.** Future maintainers may spell it `retired.md`, `RETIRED`, `TOMBSTONE.md`, `DELETED.md`. Convention is one rename or typo away from fragmenting.
2. **`prompts/` does not later acquire a non-prompt file with `RETIRED` in its name.** Falsifier becomes ambiguous if `prompts/RETIRED-DRAFT.md` ever appears.
3. **Git-SHA references survive history rewrites.** Format mandates `git show <sha>:<path>`. Rebases/squashes/filters may make recorded SHAs unreachable.
4. **Item 07's plan accepts an inbound edit from item 13's commit.** Cross-work-item write coupling. Merge-conflict risk if item 07 is concurrently being edited.
5. **`prompts/RETIRED.md` is itself link-targetable.** Once it exists, other plans/canon may link to it. Rule 5 then creates link-rot risk the contract does not acknowledge.

## 3. Coupling and direction

- **Volatile → stable inversion: resolved.** CLAUDE.md amendment dropped.
- **Layering violation (`plans/` ↔ `session-artifacts/`): resolved.** No footer link added.
- **New coupling introduced: item-13 commit → item-07 plan.** Cross-work-item, unidirectional, unaudited from item 07's side. Small.
- **Item 13 → item 5 dependency: bounded.** Footer fallback gives item 13 a self-acting close-out.

## 4. Ignored architectural alternatives

1. **`prompts/.gitkeep` with header comment.** Achieves "directory stays non-empty" without inventing a `<dir>/RETIRED.md` convention with population of one.
2. **Commit-message-as-record.** `git rm` with structured commit message body. Discoverable by `git log --diff-filter=D --name-only -- prompts/`. No new file primitive.
3. **Inline retirement comment at top of related live files.** Co-location with actual readers, not with absence.

## 5. Frame-level objection (next-session, not blocking)

The "explicit > implicit primitive" frame was correctly metabolized — that is the loop-1 win. v2 surfaces a *new* frame question that loop 1 could not see: **does this repo need a "tombstone primitive" at all, or is it inventing infrastructure for an N=2 event?** Candidate's falsifier is for *this sweep*, not for whether `<dir>/RETIRED.md` should recur. If one-shot (assumption #4 tolerates this), then naming it as a "primitive with a contract" is overshoot. If recurring, contract needs an enforcement venue (an agent, CLAUDE.md rule, lint), which v2 explicitly refuses to add.

**Is `RETIRED.md` a primitive or a precedent?** Candidate treats it as a primitive (writes a contract) but ships it as a precedent (one instance, no enforcement, tolerates one-shot use). Pick one. If primitive, add the enforcement venue. If precedent, drop the contract section and ship as a one-off `prompts/RETIRED.md` with a comment explaining what the file is.

## 6. Verdict

**`approve`.**

Unambiguous approve from architecture lens. The frame-level objection above is a *next-session* concern (primitive-vs-precedent worth one paragraph in synthesis), not a blocker. Loop-1 architectural objections all cleanly resolved: new primitive named explicitly, located where readers will look; volatile→stable inversion gone; layering violation gone; rename-driven link-graph risk gone; inbound-link audit performed and documented.
