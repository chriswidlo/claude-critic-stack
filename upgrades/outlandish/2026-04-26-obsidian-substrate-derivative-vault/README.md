# Obsidian + Claude Code as a substrate/derivative vault — a greenfield design

| Field | Value |
|---|---|
| 📌 **title** | Obsidian + Claude Code as a substrate/derivative vault — a greenfield design |
| 🎯 **tier** | 🚀 outlandish |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | A conversation that began as a curiosity question — *do people actually use Obsidian with Claude Code, is it real, can it bring something innovative?* — was answered with a deep web-research pass across roughly fifteen sources spanning enthusiastic guides (Starmorph, MindStudio, whytryai, DEV.to), MCP plugin repos (iansinnott, MarkusPfundstein), the Obsidian forum's Agent Client plugin announcement, and explicit skeptics (Viget, Code With Seb, Tech & AI Guild). The research surfaced four distinct integration patterns conflated in the popular write-ups, and four hard failure modes the popular write-ups understate. The operator then asked for a *best-possible greenfield plan*, explicitly waiving fit to the current repo. This entry is that plan, captured into the lab so the design survives the conversation. |
| 💡 **essence** | The load-bearing innovation in any serious AI-augmented PKM is the **substrate/derivative split** — separating what the human writes (sacred, append-only, the source of truth) from what the agent generates (regenerable, gitignored, carrying provenance back to the substrate). Every "second brain" guide currently in circulation conflates these two concerns into a single vault, which is why every guide ends up either disabling autonomous writes or quietly accepting the blast radius. |
| 🚀 **upgrade** | Adopted, this design would give any AI-augmented knowledge system a durable substrate that Claude cannot damage, a derivative layer that Claude can regenerate freely, scope-bounded operations that prevent the unbounded-synthesis hallucination failure mode, and a provenance layer that turns the Obsidian graph view into an audit trail of how every derived note was built. The same primitives map onto this repo's existing canon/distillations/session-artifacts structure — the design is more general than its initial framing as "Obsidian." |
| 🏷️ **tags** | obsidian, pkm, mcp, knowledge-management, vault-design, provenance, second-brain, retrieval, scope-discipline |
| 🔗 **relates_to** | 2026-04-26-rnd-lab |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [Why this entry exists](#why-this-entry-exists)
- [What the field actually does today — four patterns, conflated](#what-the-field-actually-does-today--four-patterns-conflated)
- [What the field gets wrong — four failure modes the guides understate](#what-the-field-gets-wrong--four-failure-modes-the-guides-understate)
- [The five design principles](#the-five-design-principles)
- [Topology — two vaults, not one](#topology--two-vaults-not-one)
- [The four operations Claude is allowed to perform](#the-four-operations-claude-is-allowed-to-perform)
- [Context strategy — the CLAUDE.md replacement](#context-strategy--the-claudemd-replacement)
- [Retrieval strategy — the keyword-blindness fix](#retrieval-strategy--the-keyword-blindness-fix)
- [Provenance — the killer feature nobody is doing well](#provenance--the-killer-feature-nobody-is-doing-well)
- [Tooling stack — concrete picks and explicit skips](#tooling-stack--concrete-picks-and-explicit-skips)
- [What makes this innovative versus the blog-post second brains](#what-makes-this-innovative-versus-the-blog-post-second-brains)
- [Phased rollout if pursued](#phased-rollout-if-pursued)
- [Mapping back onto the critic-stack — the unexpected isomorphism](#mapping-back-onto-the-critic-stack--the-unexpected-isomorphism)
- [Honest uncertainties](#honest-uncertainties)
- [The cheapest experiment that would refute the whole design](#the-cheapest-experiment-that-would-refute-the-whole-design)
- [Open questions left for future entries](#open-questions-left-for-future-entries)

---

## Why this entry exists

The conversation that produced this design started in the worst possible register: *show me what other people are doing*. That register, left to itself, produces inventories — lists of plugins, lists of MCP servers, lists of "10x your thinking" testimonials. None of that is a design. It is a survey of the space within which a design might exist.

The design itself emerged when the operator pushed past the survey: *don't care what is currently in repo, I want best possible*. That instruction is the actual catalyst, because it gave the AI permission to ignore the strongest anchor — the existing critic-stack — and reason about the problem from first principles. The result is a design that turns out, by the end, to also describe the critic-stack's own substrate/derivative pattern; but it had to be reasoned greenfield to find that.

This entry captures the design before the conversation closes, and elevates it from "answer to a question" to "candidate upgrade for any AI-augmented PKM." It is filed as **outlandish** because the full vision — substrate vault, derivative vault, four-operation surface, provenance frontmatter, drift audit, regenerable indexes, embedding-augmented retrieval — is months of work if pursued seriously, and several phases involve unknowns that no single sitting can de-risk.

## What the field actually does today — four patterns, conflated

The popular write-ups treat "Obsidian + Claude Code" as a single thing. It is four things, and the differences matter:

| # | Pattern | What it actually is | Maturity |
|---|---|---|---|
| 1 | **Vault-as-cwd** | Open Claude Code in your vault folder; it reads/writes markdown directly. No plugin, no MCP. | Mature — works because vault is just `.md` files |
| 2 | **MCP server in Obsidian** | A plugin (e.g. `iansinnott/obsidian-claude-code-mcp`, 261★, last release Jun 2025; or `MarkusPfundstein/mcp-obsidian`) exposes vault operations as MCP tools. Lets Claude query without being the cwd. | Workable — older MCP spec (2024-11-05 SSE), setup friction |
| 3 | **Claude Code embedded in Obsidian UI** | The newer "Agent Client" plugin (announced 2025-11-27, in BRAT, not yet in community store as of late Jan 2026) puts Claude Code, Codex, and Gemini CLI in a sidebar with `@notename` mention syntax. | Immature — no parallel sessions, no model switching, limited streaming detail |
| 4 | **Skill / framework patterns** | `eugeniughelbur/obsidian-second-brain` (Claude Code skill turning a vault into a "living" second brain with autonomous writes); `huytieu/COG-second-brain` (17 skills, 6 worker agents, gstack-inspired). | Experimental — most ambitious, least battle-tested |

Most "second brain" articles describe pattern 1, dress it as pattern 4, gesture at pattern 2 as future state, and ignore pattern 3 entirely. The conflation is what produces the breathless register.

## What the field gets wrong — four failure modes the guides understate

These are the failure modes the skeptical sources surface clearly and the enthusiastic sources gloss:

1. **Keyword-blindness on conceptual search.** One published test of ten conceptual questions found Claude missed >60% of relevant notes because the user used different vocabulary across sessions. Plain `grep`-style retrieval is incompatible with how a real PKM actually grows.

2. **Hallucinated cross-note synthesis.** When asked to synthesize across notes without an explicit "do not include anything I didn't write" constraint, the model fabricates connections that read as plausible. The hallucinations are *worse* than in pure code synthesis because the human substrate is more forgiving of plausibility.

3. **`CLAUDE.md` drift.** The guide-recommended pattern of an "Active Context" section in `CLAUDE.md` rots quickly. The model reads the stale section as current and gives confidently wrong answers calibrated to a version of the work that no longer exists.

4. **Autonomous-write blast radius.** Claude reorganizing folders, renaming notes, or normalizing frontmatter can break the graph view, break wiki-links, and corrupt years of substrate. Without a revert mechanism (git on the whole vault, which most users don't set up), the damage is one-way.

The five design principles below are constructed specifically to make each of these failure modes structurally impossible, not merely manageable.

## The five design principles

```
1. Two vaults, not one.
   └─ Separate the substrate from the derivatives.

2. Bounded scope is a first-class concept.
   └─ Every Claude operation names its folder. No unbounded queries.

3. Generated notes carry provenance.
   └─ Graph view becomes an audit trail, not decoration.

4. Context is dated, not "active."
   └─ No mutable CLAUDE.md sections. Staleness becomes visible.

5. Skills > MCP > plugins.
   └─ In that order of durability across Claude Code versions.
```

Each principle is a direct response to one or more of the four failure modes. Two-vault topology kills failure mode 4 outright. Bounded scope makes failure modes 1 and 2 manageable (a folder is small enough to actually fit in context; a folder is bounded enough that "do not invent connections" is enforceable). Provenance makes failure mode 2 detectable post-hoc. Dated context kills failure mode 3 by design. The tooling-durability principle is a hedge against the immaturity of patterns 2 and 3 above.

## Topology — two vaults, not one

```
brain/                      (a top-level vault directory under user home)
├── raw/                    ← Vault A — you write, Claude reads. Append-only by convention.
│   ├── inbox/              quick capture
│   ├── daily/              YYYY-MM-DD notes
│   ├── projects/<slug>/    bounded scopes — every project is its own folder
│   ├── people/, books/, refs/
│   ├── .claude/
│   │   └── CLAUDE.md       stable conventions, rarely edited
│   └── .obsidian/
│
└── derived/                ← Vault B — Claude writes, regenerable, gitignored from raw.
    ├── syntheses/          one note per synthesis run, with frontmatter provenance
    ├── indexes/            generated MOCs, tag rollups, "what changed this week"
    ├── distillations/      compressed summaries Claude pulls into context cheaply
    ├── _provenance.json    machine-readable map of derived → source notes + SHAs
    └── .obsidian/          (separate Obsidian config, can be opened as its own vault)
```

The split is not just folder hygiene; it is a **permission boundary**. Claude Code is configured (via `.claude/settings.json` permission rules) with read-only access to `raw/` and write access only to `derived/`. The autonomous-write blast radius collapses to: *Claude can damage anything in `derived/`*, which is gitignored and regenerable.

Two consequences fall out:

- **`raw/` can be safely git-versioned without Claude's autonomous churn polluting history.** Commits in `raw/` are human commits. The diff log is meaningful.
- **`derived/` can be wiped at any time without loss.** If a synthesis run produces something bad, `rm -rf derived/syntheses/2026-*` and rerun.

A subtle but important detail: `derived/` should be opened as a *separate Obsidian vault*, not as a subfolder of `raw/`. Two vaults, two graph views. The substrate's graph stays clean of generated nodes; the derivative's graph stays focused on what Claude has built. Cross-vault links via wiki-links are still possible (Obsidian supports vault-to-vault links via URI), but they're explicit, not implicit.

## The four operations Claude is allowed to perform

Everything else is friction. Every operation is a slash command or a Claude Code skill. The discipline is the API:

| Operation | What it does | Scope |
|---|---|---|
| `/process-inbox` | Move & tag items from `raw/inbox/` into the right folder. Never deletes; only moves. | `raw/inbox/` only |
| `/synthesize <folder>` | Bounded cross-note synthesis → writes one note in `derived/syntheses/` with frontmatter listing every source note + commit SHA + prompt hash. | named folder only |
| `/distill <folder>` | Compress N notes into a ≤2k-token summary in `derived/distillations/` for cheap future context injection. | named folder only |
| `/audit-drift` | Read `derived/_provenance.json`; flag derived notes whose source notes have changed (by SHA) since generation. | `derived/` |

There is no `/synthesize-everything`. There is no `/ask-my-vault`. The discipline of the API is the product. Operators familiar with the "second brain that thinks for you" framing will find this restrictive at first; the restriction is the whole point. An operation that names its scope cannot accidentally become an unbounded query, and an unbounded query cannot accidentally hallucinate across the whole vault.

The operations are deliberately few because each one carries real semantics. Adding a fifth operation should require an entry in this lab justifying it.

## Context strategy — the CLAUDE.md replacement

The drift problem is structural, not cosmetic. Fix it structurally:

- **`raw/.claude/CLAUDE.md`** is **stable, rarely-edited.** It contains vault conventions, folder semantics, frontmatter schema. Things that are true for years. No "Active Context" section, no daily updates.
- **`raw/daily/<YYYY-MM-DD>.md`** is today's working context. Claude Code reads today + yesterday automatically (a hook injects them). Never edits them.
- **`derived/distillations/`** is where compressed long-term context lives. Cheap to inject by reference; regenerable when stale.

The result: context is *dated*, so staleness is visible by inspection. Compare with the `CLAUDE.md`-with-Active-Context pattern, where staleness is invisible because the section keeps the same heading regardless of whether anyone has updated it. A dated daily note from three weeks ago obviously isn't current; an "Active Context" section from three weeks ago looks current at a glance.

This is a small change with large compounding consequences over months of vault life.

## Retrieval strategy — the keyword-blindness fix

The 60%-miss problem on conceptual search is the real ceiling. Solutions, in cost order:

1. **Smart Connections plugin** — local embeddings, runs in Obsidian, free. First line of defense. Closes most of the keyword-vocabulary gap with minimal infrastructure.

2. **Frontmatter discipline.** Every note in `raw/` has `tags:`, `aliases:`, and `concepts:` fields enforced by Templater. Claude greps these structured fields *before* the body. Cheap, deterministic, complementary to embeddings.

3. **Generated `indexes/` regenerated weekly.** MOCs (maps-of-content) Claude builds from frontmatter, plus tag rollups, plus a "what changed this week" rollup. Become a cheap "table of contents" Claude reads first to decide *which* folder to scope to.

Skip the full RAG / ChromaDB / external vector store pipeline until 1–3 demonstrably fail at scale. It is the most common over-engineering in this space; one published guide builds a complete RAG pipeline before measuring whether Smart Connections is sufficient. Solve cheap problems first.

## Provenance — the killer feature nobody is doing well

This is the load-bearing innovation. None of the surveyed guides do this; many wave at "the AI will know what it built" without making the knowledge mechanically accessible.

Every derived note has frontmatter:

```yaml
---
generated_by: claude-code
generated_at: 2026-04-26T14:22:00Z
operation: synthesize
sources:
  - raw/projects/can-bus/2026-03-12-arbitration.md@sha:a3f
  - raw/projects/can-bus/2026-04-01-error-frames.md@sha:b71
  - raw/refs/iso-11898-1.md@sha:c44
prompt_hash: sha256:...
model: claude-opus-4-7
---
```

This buys three things, each non-trivial:

- **Graph view becomes an audit trail.** With the right Dataview query, you can render a graph that shows derived notes as one shape, raw notes as another, and provenance edges as connections — *which derived note came from which raw notes* is visible at a glance.
- **`/audit-drift` is mechanically possible.** Compare current SHA of each `sources:` entry to the `@sha:` in the frontmatter. If different, the source note changed after generation; flag the derived note as potentially stale. Without provenance frontmatter, drift is silent.
- **Regeneration is safe and diff-able.** Run `/synthesize raw/projects/can-bus/` again; produce a new synthesis. Diff against the prior one. See what changed. Without provenance, "rerunning the synthesis" is a black box; with it, the synthesis becomes a deterministic-ish function of inputs that can be regression-tested.

The provenance file (`derived/_provenance.json`) is the machine-readable mirror of the per-note frontmatter, kept in sync, used by `/audit-drift`. Belt and suspenders.

## Tooling stack — concrete picks and explicit skips

**Picks:**

- **Obsidian** as the UI. Local. Two vaults configured (`raw/` and `derived/`). No Obsidian Sync to start; add only if mobile capture matters.
- **Claude Code** run from the `brain/` vault as cwd. Permission rules in `.claude/settings.json` enforce read-only on `raw/` and write-only on `derived/`.
- **Smart Connections** plugin. The one community plugin worth installing day one.
- **Templater** plugin for daily-note scaffolding (frontmatter schema enforcement).
- **Dataview** plugin for ad-hoc queries the indexes don't cover.
- **Git** on `raw/` only. `derived/` is gitignored — it's a build artifact.

**Explicit skips:**

- **MCP servers** — not initially. The `cwd`-based approach handles every workflow listed above. Adopt MCP only if a concrete pain point emerges that `cwd` cannot solve. The 261★ `obsidian-claude-code-mcp` plugin is workable but adds a moving part (port management, MCP transport version, plugin lifecycle) you don't need on day one.
- **Agent Client plugin** — too immature. Re-evaluate in three months when it's been through more iterations.
- **Skill frameworks** (`obsidian-second-brain`, `COG-second-brain`) — interesting but unproven and they bring opinionated worldviews that conflict with this design's discipline. Build the four operations first; consider importing patterns from frameworks later.
- **Obsidian Sync, Obsidian Publish** — out of scope. Different problem.

## What makes this innovative versus the blog-post second brains

Most write-ups treat the vault as one undifferentiated blob and Claude as a magic synthesizer. The differences here, in order of importance:

1. **Substrate/derivative split.** No surveyed guide does this. It is the single biggest blast-radius reduction available. It also makes git-versioning the substrate genuinely useful, since the diff log isn't polluted by autonomous Claude churn.

2. **Provenance as a first-class artifact.** Turns "trust the AI" into "audit the AI." Makes drift detectable. Makes regeneration diff-able. Makes the graph view actually informative about derivation, not just connection.

3. **Bounded-scope discipline enforced at the API surface.** There is no `/synthesize-everything`; the command set itself prevents the most common hallucination failure mode. This is not a guideline, it is the API.

4. **Dated context replaces mutable context.** Drift becomes visible by inspection. The `CLAUDE.md` rot problem is killed structurally, not by discipline.

5. **Skills, not plugins, as the integration layer.** Durable across Claude Code versions and across machines. MCP plugins and Obsidian plugins are stratigraphically below skills in the durability hierarchy.

A reader who has used Obsidian + Claude Code in the conventional way and sees this design might react: *this is a lot of discipline for a knowledge system*. That reaction is the right calibration. The discipline is the price of avoiding the four failure modes. Skipping the discipline and pretending the failure modes don't exist is the dominant mode in the popular write-ups.

## Phased rollout if pursued

The temptation when adopting an ambitious greenfield design is to build it all at once. Resist:

- **Phase 0 (one evening).** Create `raw/` and `derived/`. Install Obsidian + Smart Connections + Templater. Point Claude Code at the `brain/` vault with read-only permission on `raw/`. Use it normally for a week — no slash commands yet, no provenance, no skills. Find out what you actually do.

- **Phase 1 (one weekend, after Phase 0 has been used a week).** Write `/process-inbox` and `/synthesize` as Claude Code skills. Add provenance frontmatter to every `/synthesize` output. Initialize git on `raw/`.

- **Phase 2 (when Phase 1 has produced 30+ derived notes).** Add `/audit-drift` and weekly regeneration of `indexes/`. This is when provenance starts to pay off — before this point, there is too little derivation history for drift detection to find anything.

- **Phase 3 (only if needed, probably never).** MCP plugin or Agent Client. The signal that triggers Phase 3 is a *concrete pain point* the cwd-based approach cannot solve, not a general feeling that the setup could be more sophisticated.

Each phase is gated by *use*, not by calendar. Phase 1 cannot start until Phase 0 has been used enough to know what slash commands actually want to exist. Phase 2 cannot start until there is enough derivation history to make drift audit non-trivial.

## Mapping back onto the critic-stack — the unexpected isomorphism

The greenfield design was reasoned without reference to this repo. Then, by the end, the structure turned out to be the same:

| This design | This repo |
|---|---|
| `raw/` (substrate) | `canon/corpus/` + operator-authored content |
| `derived/distillations/` | `.claude/session-artifacts/<id>/distillations/` |
| `derived/syntheses/` | `.claude/session-artifacts/<id>/synthesis.md` |
| `derived/_provenance.json` | distillation files cite their source agent + raw return |
| Bounded-scope operations | Each session is scoped to one design question |
| `raw/.claude/CLAUDE.md` (stable) | `CLAUDE.md` (stable) |
| Daily dated context | session-id naming convention |

This isomorphism is itself a finding. The critic-stack already implements the substrate/derivative pattern at the workflow level; the Obsidian design proposes implementing it at the knowledge-base level. The patterns rhyme because the underlying problem rhymes — *how do you let an AI generate without letting it damage what you have built*.

The honest implication: if this design is right for Obsidian, then the critic-stack is also implicitly endorsing the same principles, and any future critic-stack upgrade should be evaluated against whether it preserves or violates them. A future entry should make this principle-set explicit as a stack-wide invariant.

## Honest uncertainties

1. **Whether you'll actually use it.** Most second-brain setups die from maintenance overhead, not from technical limits. The two-vault topology adds discipline cost. A Phase 0 trial is essential before committing to Phase 1.

2. **Whether bounded-scope discipline survives contact with real use.** The temptation to ask "what do I know about X" across the whole vault is strong. If the discipline cracks repeatedly, either the operator has uncovered a missing operation that should be added (with care), or the discipline itself is wrong for the operator's actual workflow.

3. **Whether Smart Connections embeddings stay good enough as the vault grows past ~5k notes.** May need to migrate to a real vector store eventually. The migration is non-trivial; it should not be premature.

4. **Whether the Agent Client plugin (or its successors) makes the cwd-based approach obsolete within twelve months.** If the Obsidian-native UI becomes mature, the design's "skip plugins" stance may need revision. Re-evaluate quarterly.

5. **Whether `derived/` should be one vault or several.** A single derived vault is simpler; multiple derived vaults (one per project, perhaps) is more scalable but adds management overhead. The right answer probably emerges only after Phase 1.

## The cheapest experiment that would refute the whole design

Skip every piece of this design. Open Obsidian on an empty folder. Capture into it daily for two weeks with Claude Code in the same folder, no plugins, no skills, no provenance.

If at the end of two weeks you have not actually been using it — if the capture habit didn't form, if Claude's involvement didn't help, if the vault stayed mostly empty — then the entire design above is theater. The discipline of the design is wasted on a knowledge base that doesn't exist.

If at the end of two weeks the vault has real content and you've felt one or more of the four failure modes (keyword-blindness, hallucinated synthesis, `CLAUDE.md` drift, autonomous-write damage), then the design becomes *concrete answers to felt problems* rather than theoretical answers to surveyed problems. Build Phase 1.

This experiment costs two weeks and risks nothing. It should be the first thing tried if this entry advances past 🌱 created.

## Open questions left for future entries

These are deliberately not resolved here; they need their own entries when the substrate exists to inform them:

1. **What is the right granularity of `/synthesize`?** A whole project folder, a date-bounded slice, a tag-bounded slice? The answer probably depends on note density.

2. **Should the provenance frontmatter include the *prompt* used, not just its hash?** Including it makes provenance fully self-describing but may bloat frontmatter past readability. Hash-only is auditable but requires keeping prompts in a side file.

3. **Should `/audit-drift` propose regeneration, or only flag?** Auto-regeneration is convenient and dangerous (drift might be intended; the substrate may have updated *because the synthesis was wrong*). Flag-only is safe but creates a maintenance burden.

4. **Is this design also right for the critic-stack itself?** The isomorphism noted above suggests yes; but the workflow's needs (adversarial review, multi-lens critique) are different from a PKM's needs (synthesis, navigation, recall). The mapping may break in places worth investigating.

5. **What is the right relationship between `derived/` and the canon corpus?** Could `derived/distillations/` *be* canon entries, or do they live in different durability tiers? This relates directly to the lab's earlier open question about whether memory and the lab are the same primitive.

---

## A closing note on tier choice

This entry sits in 🚀 `outlandish` rather than 🌿 `normal` because the full vision — substrate vault, derivative vault, four-operation surface, provenance frontmatter, drift audit, regenerable indexes, embedding-augmented retrieval, phased rollout, isomorphism with the critic-stack — is genuinely months of work if pursued, with multiple unknowns that no single sitting can de-risk. The Phase 0 trial alone is two weeks; the full design through Phase 2 is realistically a quarter.

It is not 💎 `profound` because the *seeing* here is the substrate/derivative split, which is real but not revolutionary — it is good engineering applied to a domain (PKM) where most practitioners haven't applied it yet. The profound version of this entry would be the one that argues *substrate/derivative is the same pattern as the critic-stack's distillation pattern is the same pattern as Anthropic's tool-use isolation* — that the principle is universal across AI integration, and that any AI-augmented system that doesn't apply it is accumulating technical debt by default. That entry has not been written yet; this one is its prerequisite.

It is not ✅ `no-brainer` because the operator did not ask for it to be implemented; they asked for the best-possible plan. The implementation decision is downstream and uncertain.
