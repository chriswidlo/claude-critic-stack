# Critic — Product lens — item 06 temporary-dependent upgrades

## 1. User-visible consequence

The morning after (b′) lands, a reader of [`upgrades/LEDGER.md`](../../../../upgrades/LEDGER.md) row #18b sees a **`State` cell that still reads `🌱`** next to an **`Implement as` cell that says "Migration plan superseded 2026-04-27 … advance from 🌱 only if/when worktree branch graduates."** The state column and the implementation column **disagree at the row level**. `🌱 created` carries the implicit affordance "this can be picked up and advanced"; the cell text revokes that affordance in prose.

A second reader, opening either entry body, sees the migration section wrapped in `> superseded — see Update history` blockquote whose interior is **eight numbered `git mv` steps that still parse as instructions**. This is *strikethrough-by-blockquote*: a typographic demotion of imperative content that remains imperative in voice. Documentation equivalent of leaving deprecated APIs with a `@deprecated` annotation but no compile error — careful readers route around, less-careful readers (and agents grepping for "git mv") still execute.

## 2. Commitments implied

(b′) ships three new product-surface contracts:

1. **Section-level supersession as a first-class lifecycle operation** — distinct from entry-level supersession. Once two entries demonstrate the pattern, a third partly-dead body will be expected to use it.
2. **`Update history` (borrowed from #18f, itself `🌱`) as load-bearing for negation** — extends 18f's native scope (multi-state advancement honesty) to body-section demotion. 18f never opted in.
3. **Cross-branch worktree commit references as durable LEDGER content** — `agentic-engineering-research@13c09b0` cited from `main` as a place readers should go.

None reversible by editing one file; each cited next time the question recurs.

## 3. Migration burden

- **Future operator advancing either entry past `🌱`** must read `Update history`, redact the blockquoted section mentally, decide whether the parent narrative still holds, then re-derive a migration plan. Load transfer, not load reduction.
- **`canon-librarian` and any future ranking subagent** today treats `🌱` as "candidate work item." After (b′), `🌱` no longer means that uniformly. Either the ranker learns a second signal (parse `Implement as` for "superseded"-style strings) or it silently ranks dead rows as live ones.
- **Reader of the sister entry** chasing a cross-reference lands on text whose authority is partially revoked, with no inbound signal about which parts.
- **Future writer of upgrade-entry conventions** inherits "is partial supersession a thing here?" with two precedents and no written rule.

## 4. Affordances better / worse

**Better:**
- Row #18b `Implement as` becomes strictly more informative than the current phantom migration cell.
- Parent narratives stay queryable on `main`; eviction would have made grep return nothing.
- One place — not two, not zero — for the demotion cause.

**Worse:**
- Advance affordance is **silently downgraded**, not removed. State cell still says `🌱`. No mechanical signal prevents an agent from picking up the entry and trying to execute the blockquoted plan. (b) full-supersede would have flipped the state cell, removing the affordance at the schema level.
- Lab loses the option to introduce `superseded` as a first-class state token cleanly. Two entries demoted *without* using a `superseded` token will face the question "do we retroactively flip those?" later.
- Skim-reading TOCs sees `## Concrete migration plan` at equal weight with the rest of the body. The supersession blockquote does not propagate to the TOC.

## 5. Frame-level objection

The candidate's defense — that LEDGER is "reflective-narrative" — is **product-surface revisionism**. It retroactively reframes what the state column means in order to fit the proposed treatment. After (b′), some `🌱` rows mean "live candidate" and some mean "paused on external worktree branch"; the only way to tell them apart is to read free-text prose in an adjacent cell. The candidate cites row #19 as evidence; row #19 is honestly labeled as an open question in its own body, sitting under Group E ("Observations"). It is not a row whose state cell *lies about the row's actionability*.

**(b′) preserves the LEDGER state vocabulary by overloading it.** The honest product moves are either (i) introduce a state token that means what (b′) wants `🌱` to mean for these rows (resolve assumption #4 first, not defer), or (ii) fully supersede with a state-cell flip, or (iii) relocate the rows to Group E. (b′) chooses the path that pushes interpretation cost onto every future reader.

## 5b. Punch-list rhythm

Items 1–5's resolutions are crisp: mechanical edits with named files, or a written rule. Item 6 in (b′) form produces wrapped sections, a rewritten cell, an `Update history` block bootstrapped from another `🌱` entry's not-yet-ratified pattern, and four named-but-unanswered assumptions. More baroque than items 1–5. Surgical hybrids of named options usually indicate the named options were closer to right than the surgical hybrid wants to admit.

## 5c. Honesty surface

Honest negation, applied strictly, would either delete the migration section (replace with a one-paragraph negation note) or commit to entry-level supersession. The blockquote-wrap is the doctrine's softest possible reading. A reader taking "honest negation" at face value will read (b′) as visible defection from the doctrine.

## 6. Verdict

`rework`

Path to approve: either (i) flip the state cell to a terminal token (full (b)) and accept losing the parent-shape narrative, **or** (ii) keep parent narrative but **delete the migration sections outright** and replace each with a one-paragraph negation note in the body, so the LEDGER row's `🌱` no longer fronts an executable-looking plan. Current "wrap in blockquote, keep all eight `git mv` steps" treatment is the worst of both options on the product surface.
