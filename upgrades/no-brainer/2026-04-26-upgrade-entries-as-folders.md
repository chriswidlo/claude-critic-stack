# Upgrade entries can grow into folders

| Field | Value |
|---|---|
| 📌 **title** | Upgrade entries can grow into folders |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session 2026-04-26 — a research session produced ~60 KB of structured material (`decision-registry.md`, a narrative playbook, four primary-source transcripts) that did not fit the single-file entry shape. The proposed entry referenced supporting artifacts via prose only, leaving them homeless in `temporary/`. The conversation that followed converged on a structural fix: let an entry be a folder. |
| 💡 **essence** | The current "one entry = one `.md`" rule silently assumes every idea is *prose-sized*. Some ideas come with artifacts — prototypes, transcripts, sample outputs, draft prompts, comparator data — and those artifacts *are* part of the idea, not separate from it. A lab notebook in real labs has stapled-in printouts and attached photographs; the file-system version of that is letting an entry be a folder when it wants to be. |
| 🚀 **upgrade** | Redefine an entry as a *folder*: `upgrades/<tier>/<YYYY-MM-DD>-<slug>/` containing one structured `<YYYY-MM-DD>-<slug>.md` (the upgrade doc — meta table, state table, TOC, body) plus any supporting files or sub-folders the upgrade chose to grow. The doc shares its parent folder's slug, so identity is stable from any path you look from. The lab keeps its single rule ("one entry = one folder") while ideas gain unlimited room to bring evidence with them. |
| 🔗 **relates_to** | agentic-engineering-reference-library, rnd-lab |
| 🏷️ **tags** | lab-structure, upgrade-pattern, conventions, self-hosting |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The current rule, and what it silently assumes](#the-current-rule-and-what-it-silently-assumes)
- [Three places the assumption breaks](#three-places-the-assumption-breaks)
- [The new rule](#the-new-rule)
- [Why folder-as-entry beats the sidecar variant](#why-folder-as-entry-beats-the-sidecar-variant)
- [The dogfood property — this entry migrates itself first](#the-dogfood-property--this-entry-migrates-itself-first)
- [Migration plan](#migration-plan)
- [README amendments](#readme-amendments)
- [What this does NOT change](#what-this-does-not-change)
- [Future growth this enables but does not require](#future-growth-this-enables-but-does-not-require)
- [Open question: LEDGER link rot](#open-question-ledger-link-rot)
- [What success looks like](#what-success-looks-like)

## The current rule, and what it silently assumes

The lab's `README.md` says:

> Create `upgrades/<tier>/<YYYY-MM-DD>-<short-kebab-slug>.md`. … Add H1 title, meta table, state table (with `created` filled in), TOC, body. Commit.

One entry, one file. The rule is clean and grep-able. It also silently assumes every idea is prose-sized — that an entry is a *piece of writing* and nothing else.

Most entries are. The 28 entries currently in the lab are all prose. But the assumption is fragile, and the friction shows up the moment an idea arrives with attached evidence.

## Three places the assumption breaks

1. **Research outputs.** This session produced a 60 KB sourced registry, a narrative playbook, and four full transcripts. The artifacts *are* the value of the idea; the prose just frames them. Forcing the prose to live in `upgrades/` and the artifacts to live elsewhere (`temporary/`, `references/`, scattered) gives the entry references that can rot.

2. **Prototypes and spikes.** The state lifecycle has a `🔬 spiked` state — *"someone did exploratory or prototype work"* — but no place for the prototype to live. Prototypes today land in `plans/` or `.claude/session-artifacts/<id>/`, disconnected from the lab entry that motivated them.

3. **Long-form designs.** Several existing entries (`critic-panel-correlated-by-default`, `external-shadow-via-openrouter`, `scope-projector-capability`) sketch agents and would benefit from carrying draft prompts, sample comparator outputs, or design diagrams as separate files. Today those would have to be inlined as code blocks or omitted.

In each case, the friction is the same: the *idea* has a body that's larger than prose, and the file-system convention does not honor that.

## The new rule

A single, uniform rule replaces the current one:

> An entry is a folder. Create `upgrades/<tier>/<YYYY-MM-DD>-<slug>/`. Inside, create one `<YYYY-MM-DD>-<slug>.md` — the upgrade doc, with H1 title, meta table, state table, TOC, body. Anything else inside the folder is supporting material, format-free, organized however the upgrade itself decides. The upgrade doc explains its own substructure.

Three crisp properties:

1. **Folder name = entry slug = doc filename.** The slug is the identity; it appears at every path level you might be looking from.
2. **One `.md` per entry, named after the slug.** It is unambiguous which file is the structured upgrade doc, even when the folder contains other markdown files (e.g. transcripts, design notes).
3. **Supporting material is unrestricted.** No naming convention, no required layout. The upgrade doc documents what's there. The lab does not prescribe; the entry decides.

## Why folder-as-entry beats the sidecar variant

An earlier draft of this thinking proposed a *sidecar* — keep entries as flat `.md`, optionally grow a same-named folder *next to* the file when supporting material is needed. That approach was rejected because:

- **Branching shape.** Some entries would be files, others would be file-plus-folder. Anyone walking `upgrades/` would have to know which shape they're looking at. Folder-as-entry gives every entry the same shape.
- **The "is this entry a file or a folder?" question recurs forever.** Folder-as-entry answers it once.
- **README.md collision.** If a sub-folder of supporting material wants its own README, the entry's `README.md` collides with that legitimate use. Naming the upgrade doc after the slug avoids the collision entirely.

The slug repeats in the path (`<slug>/<slug>.md`). That's a feature, not redundancy: identity should be visible at every level it might be referenced from.

## The dogfood property — this entry migrates itself first

This entry, written as a flat `.md` under the *current* rule, becomes the *first* migrated entry under the *new* rule when this idea reaches `🔨 implemented`. It is the lab's own self-hosting moment: the upgrade that changes the upgrade-entry shape is itself the first entry to live in the new shape. Anyone reading the migrated form will see the original creation as a flat file in `git log` and the migration as a single rename — a concrete demonstration that the new rule subsumes the old.

## Migration plan

Bounded, reversible, ~30 min of work:

| Step | Action |
|---|---|
| 1 | Update `upgrades/README.md` "Required format" and "How to add an entry" sections to reflect the new rule. |
| 2 | For each of the 28 existing entries, run `git mv upgrades/<tier>/<slug>.md upgrades/<tier>/<slug>/<slug>.md`. The folder is created implicitly by `git mv`. |
| 3 | Update `upgrades/LEDGER.md` link paths from `<tier>/<slug>.md` to `<tier>/<slug>/<slug>.md` (28 link rewrites — `sed`-able). |
| 4 | Update `.claude/commands/upgrade.md` (the `/upgrade` slash command) to write the new shape: create folder, place doc inside. |
| 5 | This entry's own state advances to `🔨 implemented`; it becomes the first entry to demonstrate the new shape. |

Effort: **XS**. No design uncertainty. The user explicitly agreed to the shape in conversation.

## README amendments

Three sections need editing in `upgrades/README.md`:

- **"Required format for every entry"** — reword so the H1 title, meta table, state table, TOC, body now describe the upgrade doc *inside* the entry folder, not the entry file.
- **"How to add an entry"** — replace the current single-line file-creation step with the two-line folder + doc creation.
- **A new short paragraph after "Required format"** — explain that any other files or sub-folders inside the entry folder are supporting material, format-free, with the upgrade doc as their manifest.

The `LEDGER.md` linking column changes mechanically; no prose edit needed there.

## What this does NOT change

- The four tiers (`profound`, `outlandish`, `no-brainer`, `normal`) are unchanged.
- The eight-state lifecycle is unchanged.
- The decision rule for tier placement is unchanged.
- The seven optional writing prompts are unchanged.
- `LEDGER.md` ordering, ranking, and group structure are unchanged.
- The `/upgrade` slash command's behavior from the operator's perspective is unchanged — they still dump a thought, the AI still files it. The AI's *output shape* changes; the input doesn't.

## Future growth this enables but does not require

The pattern keeps the door open without preempting the next step. Three observable signals to watch for:

- **Many entries growing identical sub-folders** (e.g. `prototype/`, `prompts/`, `samples/`) — at that point, the lab might formalize a *kind* of supporting sub-folder, or even spin off a sibling top-level directory like `experiments/` for prototypes that have outgrown lab-notebook scope. This is the "department of experiments" the catalyst conversation gestured at.
- **Entries advancing to `🔨 implemented` while still containing prototype code in their folder** — at that point, the lab might require that implementation artifacts move out before the state advances, to keep the lab from becoming a WIP branch.
- **Supporting material outliving its entry's relevance** — e.g. transcripts that become valuable independent of the upgrade idea that brought them in. At that point, those artifacts may want to be promoted out of `upgrades/` into `canon/`, `references/`, or wherever they belong as standalone resources.

None of these are problems today. The lab grows; we restructure when growth has actually happened. The methodology is *grow, then restructure to support growth, as value grows with it.*

## Open question: LEDGER link rot

`LEDGER.md` currently links each entry by its flat-file path. After migration, every link gains a `/<slug>` segment. This is a one-time mechanical rewrite, but worth flagging: the LEDGER is the most-often-referenced index, and its links must be updated atomically with the migration. A script (`bin/migrate-upgrade-shape.sh`) or a single manual sed pass works equally well.

A secondary question: should `LEDGER.md` itself live inside `upgrades/` (where it does today, and where it links from), or move to `upgrades/LEDGER/` to follow the new shape? Answer: no — `LEDGER.md` is *not* an entry. It is the lab's index. The folder-as-entry rule applies to entries, not to the lab's own meta-files (`README.md`, `LEDGER.md`).

## What success looks like

If this upgrade reaches `💎 value-proved`, the signals are:

- The next session that produces substantive supporting material (prototype, transcript, sample data) co-locates it inside its entry folder rather than scattering it into `temporary/`, `plans/`, or `.claude/session-artifacts/`.
- A reader walking `upgrades/<tier>/` sees a uniform shape — every directory is an entry — and reads the slug-named `.md` inside without having to think about which file is the doc.
- An entry that started as prose-only later acquires supporting material (a prototype, a draft prompt, a comparator output) without restructuring or moving locations. The folder grows in place.

If, six months later, every entry's folder still contains only the `.md` and nothing else, the pattern hasn't paid for itself — the prose-only assumption was correct, and this entry should be honestly demoted in its body. The lab tradition is honest negation.
