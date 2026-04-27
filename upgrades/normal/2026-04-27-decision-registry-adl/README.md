# A decision registry (ADL) for claude-critic-stack — retrofitted from day 0, continued forward

| Field | Value |
|---|---|
| 📌 **title** | A decision registry (ADL) for claude-critic-stack — retrofitted from day 0, continued forward |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-27 |
| ⚡ **catalyst** | A research request on 2026-04-27: "I need a decisions registry, tracked about all decisions that are made for this repo, from day 0 when it didn't exist till today. Learn how decision registry should be formulated and what patterns it follows online." The research was performed via canon-librarian + WebSearch/WebFetch over the foundational ADR literature (Nygard 2011, MADR 4.0, Y-statements, Fowler bliki, Spotify, AWS, InfoQ critiques) and surfaced the global majority pattern, the genuinely contested design points, and the major failure modes. The operator then asked to file the result as a lab entry. |
| 💡 **essence** | This repo already produces decision-shaped artifacts every session (`requirement.md`, `frame.md`, `scope-map.md`, `challenges.md`, `critiques.md`, synthesis), but those artifacts expire with their session. A decision registry sits *adjacent* to that flow as the **durable consolidation layer** — the place a decision goes when it has crossed from "we discussed this once" to "this is now load-bearing for the repo." The registry's discipline (one record, one decision; immutable after acceptance; supersession not edit) is a different constraint than memory (timeless preferences) or session-artifacts (ephemeral working memory) or the lab (seeds of thought). |
| 🚀 **upgrade** | Future contributors and AI sessions can cite *why* a primitive exists (allowlist `.gitignore`, folder-shaped lab entries, ten-state lifecycle, distillation step, hard-gate on `scope-map.md` + `challenges.md`) instead of reverse-engineering rationale from commit messages and chat logs. The registry also forces "Considered Options" at decision time, which is the single MADR addition the field has converged on — a structural antidote to the workflow's known overdesign-when-told-to-underdesign failure mode. |
| 🏷️ **tags** | knowledge-management, audit-trail, governance, retrofit, foundation, canon-gap |
| 🔗 **relates_to** | 2026-04-26-rnd-lab, 2026-04-26-format-only-state-transition-gate |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-04-27 | — | — | — | — | — | — | — | — | — |

## Table of contents

- [Why this belongs in this repo specifically](#why-this-belongs-in-this-repo-specifically)
- [The global majority pattern — distilled](#the-global-majority-pattern--distilled)
- [How a decision registry differs from the four primitives this repo already has](#how-a-decision-registry-differs-from-the-four-primitives-this-repo-already-has)
- [A concrete proposed structure for this repo](#a-concrete-proposed-structure-for-this-repo)
- [Backfill scope — what classes of decisions exist in this repo's history](#backfill-scope--what-classes-of-decisions-exist-in-this-repos-history)
- [Retrofit policy — how to write retrospective ADRs honestly](#retrofit-policy--how-to-write-retrospective-adrs-honestly)
- [Integration with the 12-step workflow and session-artifacts](#integration-with-the-12-step-workflow-and-session-artifacts)
- [Genuinely contested design points](#genuinely-contested-design-points)
- [Open questions and ways this could be wrong](#open-questions-and-ways-this-could-be-wrong)
- [The cheapest experiment that would validate or kill this idea](#the-cheapest-experiment-that-would-validate-or-kill-this-idea)
- [Canon-gap remediation as a prerequisite](#canon-gap-remediation-as-a-prerequisite)
- [Sources](#sources)

---

## Why this belongs in this repo specifically

This repo is unusual. It runs a deliberately heavy 12-step adversarial-review workflow on every design question, producing eight to ten artifacts per session under `.claude/session-artifacts/<id>/`. Each session is, in effect, a *decision-making episode* that already generates a structured paper trail: classifier label, reframe, distillations of canon and outside-view, scope-map, challenges, candidate, three-lens critique, synthesis. The workflow knows how to *make* a decision; what it does not know how to do is **persist the decision after the session closes**.

Today, when a session ends, the synthesis lands in chat and the artifacts sit on disk. If the decision is acted on, the trail is:

```
.claude/session-artifacts/<id>/synthesis.md
        ↓
   git commit message ("Run upgrade #1 through 12-step workflow")
        ↓
   ?
```

The "?" is the gap. There is no canonical place where, six months from now, somebody (operator, AI, future contributor) can ask "*why* does this repo's `.gitignore` use allowlist mode instead of denylist mode?" and get a structured answer. The information exists — it's in `.claude/session-artifacts/2026-04-27-gitignore-allowlist/` and in commit `c3cdb77` — but it's split across two places, neither of which is named "the durable record of why this is the way it is."

A decision registry fills that gap with one specific discipline: **one record per consequential decision, append-only, immutable after acceptance, with explicit supersession.** It is not memory (preferences), not session-artifacts (working notes), not the lab (seeds of thought), not commits (implementation events). It is the *consolidated rationale* layer.

Two specific repo characteristics make this fit unusually well:

1. **The workflow already produces the inputs.** A new ADR for a workflow-decided question is not a new writing task — it's a 5-field synthesis of artifacts that already exist on disk. The ADR is a *projection* of the session, not a parallel document.
2. **The repo is principle-heavy.** Every commit is more likely to encode a principle than to ship a feature. `.gitignore` allowlist mode is a principle. Folder-shaped lab entries are a principle. The hard gate on `scope-map.md` + `challenges.md` before the generator step is a principle. Principles are exactly the class of decision the ADR pattern was designed to capture — Nygard's original example was "Deployment on Ruby on Rails 3.0.10," which is structurally identical to "lab entries are folders, not flat files."

## The global majority pattern — distilled

From the research brief, the convergent shape across the field (Nygard, MADR, Fowler, AWS, Spotify, GDS, Bennett Institute):

| Aspect | Majority pattern |
|---|---|
| Vocabulary | **ADR** = one record. **ADL** = the collection (the "registry"). |
| Storage | Inside the repo, alongside the code it governs. Path: `doc/adr/` or `docs/adr/`. |
| Filename | `NNNN-kebab-slug.md`, 4-digit padded, sequential, never reused. |
| Required fields | Title · Status · Context · Decision · Consequences (Nygard floor) **+** Considered Options (MADR addition that's now near-universal). |
| Recommended fields | Date · Deciders · Decision Drivers · Confirmation · Links. |
| Lifecycle | `proposed → accepted → (superseded \| deprecated \| rejected)`. Immutable after acceptance. |
| Length | One to two pages. Brevity is itself a discipline. |
| Granularity | Architecturally significant, OR anything that — undocumented — will be re-litigated by a future contributor. |
| Index | Auto-generated TOC. |
| Y-statement (compact form) | *"In the context of `<context>`, facing `<concern>`, we decided for `<option>` and neglected `<alternatives>`, to achieve `<benefits>`, accepting that `<drawbacks>`."* — one sentence, six slots, fits inside the Decision section of a richer ADR. |

What the field genuinely **disagrees** about (worth surfacing, not papering over):

- **Mutability.** Fowler / AWS / Nygard-spirit say strict immutability after acceptance — supersede, don't edit. A pragmatic minority says "living document" with date-stamped insertions. Most teams compromise: immutable for *Decision* and *Context*; living for *Consequences* and *Confirmation* (because outcomes accumulate after the fact).
- **Granularity.** Fowler narrow ("architecturally significant only"); Spotify broad ("almost always"); Zimmermann split-the-log ("if every decision is architectural, no decision is architectural — separate logs by category").
- **Numbering vs slugs.** Henderson's catalog allows imperative-verb slugs without numbers (`choose-database.md`); the rest of the field uses `NNNN-slug`. Numbers help with reference (`see ADR-0007`); slugs help with grep.

## How a decision registry differs from the four primitives this repo already has

```
                       lifecycle             shape           who writes
─────────────────────────────────────────────────────────────────────────
auto-memory            forever              short, atomic   AI on the fly
session-artifacts      ephemeral            many files      AI in workflow
upgrades/ (lab)        accreting forever    long, prose     anyone, any time
canon/corpus/          curated, slow        reference       human curator
                                                            via canon-refresher
─────────────────────────────────────────────────────────────────────────
decision registry      append-only,         short, fielded  AI or operator
(proposed)             immutable after                      at decision-acceptance
                       acceptance                           time
```

The registry is the only primitive whose **per-record discipline is immutability**. Memory mutates as preferences shift. Session-artifacts mutate freely within the session. Lab entries mutate as a seed matures (and explicitly do not commit to a final shape). Canon mutates by curated re-ingestion. None of them encode "this decision is closed; if we change our mind, we write a new one and link forward."

That immutability is exactly the property a registry needs to be *citable in arguments* — "ADR-0007 says we use folder-shaped lab entries; if we want to change that, we write ADR-0023 superseding it." Without immutability, "the registry says X" decays to "the registry currently says X," which is the same epistemic status as code, and code is already self-describing.

## A concrete proposed structure for this repo

This is a **proposed** structure, not a finished spec. Names and paths are negotiable.

### Location and filenames

```
docs/
└── decisions/                            ← chosen over `doc/adr/` because this
    ├── README.md                         ← repo writes `docs/`-style throughout
    ├── 0000-template.md                  ← MADR-derived template
    ├── 0001-use-decision-registry.md     ← the meta-ADR that establishes the registry
    ├── 0002-allowlist-gitignore.md       ← retrospective; original date 2026-04-26
    ├── 0003-folder-shaped-lab-entries.md ← retrospective; original date 2026-04-26
    └── ...
```

Why `docs/decisions/` and not `doc/adr/`:
- The repo already uses `docs/` plurals (`canon/corpus/`, `upgrades/`, `prompts/`). Match the local convention.
- "Decisions" is more honest than "ADR" — this repo will record process and product decisions alongside architectural ones (the InfoQ critique's "split-the-log" is *not* the right call for a small single-person repo where one folder is sufficient and the granularity tag handles category).

### Frontmatter and field set

A small superset of MADR-mandatory plus three retrofit-specific fields. YAML-style header for machine-readability:

```yaml
---
id: 0007
title: Folder-shaped lab entries
status: accepted
date: 2026-04-26
recorded-on: 2026-04-27       # only present when retrofitted
retroactive: true             # only present when retrofitted
deciders: operator
category: process             # architectural | process | product | security
supersedes: []
superseded-by: null
relates-to: [0001]
session: 2026-04-26-folder-shape-migration   # link to .claude/session-artifacts/<id>/ when applicable
commit: c2fe604               # short SHA of the commit that landed this
---
```

Body sections (mandatory in **bold**):

- **`## Context`** — the forces at play, value-neutral. For retrospective ADRs: written from artifact evidence (commits, README diffs, chat), not from memory.
- **`## Decision`** — full sentence, active voice, "We will…".
- **`## Considered Options`** — for fresh ADRs only. For retrofits, this section is **omitted** rather than fabricated, because the field's own retrofit literature is explicit that fabrication is the dominant retrofit failure mode. Replace with a single line: *"Retrospective record; alternatives at original decision time were not preserved."*
- **`## Consequences`** — including negative ones; this is where Nygard's quality bar bites.
- `## Confirmation` (optional) — how a future review can verify the decision is still being honored. Useful for repo principles ("`.gitignore` is in allowlist mode" is testable: any pattern not on the allowlist should be ignored).
- `## Links` (optional) — to the session-artifact, to commits, to lab entries, to canon passages.

### Lifecycle

The straight majority state machine, with one repo-specific twist:

```
proposed ──► accepted ──► superseded-by:NNNN
                  │
                  ├──► deprecated     (no longer relevant, no replacement)
                  │
                  └──► (rejected)     (caught by review before acceptance)
```

The repo-specific twist: the **trigger to write a new ADR** is the moment a session synthesis is acted on (i.e., a commit lands that implements the synthesis). The ADR is *not* a precondition of the workflow's synthesis step — that would re-architect the workflow. It is a precondition of *taking the synthesis seriously enough to commit*. In effect, the ADR is the bridge from "we decided" to "the repo now reflects this."

### Numbering

Sequential `0001…0999`. Numbers track the order ADRs are *written*, not the chronology of the decisions themselves — this matters for retrofits, where the original decision date may be older than the ADR number. The `date:` field carries chronology; the number carries identity.

### Index

A `docs/decisions/README.md` listing all ADRs by number, with status, title, and a one-line summary. Generated by hand in the v1 — small enough that the cost is trivial and the script is more code than the directory it indexes. If the registry grows past ~50 entries, a 20-line shell script using `grep -h '^title:'` would automate it.

## Backfill scope — what classes of decisions exist in this repo's history

The honest answer to *"how far back do we go?"* is: **don't try to be exhaustive**. The retrofit literature converges on a single principle — backfill only when the absence of the record is *currently* causing pain (re-litigation in PR review, new contributor confusion, AI sessions re-deriving the same rationale).

That said, this repo's history is short and principle-dense, so a reasonable initial backfill scope can be named. Looking at recent commits and current state:

| Decision class | Likely ADR | Evidence source | Retrofit value |
|---|---|---|---|
| `.gitignore` in allowlist mode | ADR: *"Allowlist `.gitignore` over denylist"* | commit `c3cdb77` | High — non-obvious choice, will be re-asked. |
| Folder-shaped lab entries (not flat `.md`) | ADR: *"Lab entries are folders containing `README.md`"* | commit `c2fe604`, `upgrades/README.md` | High — affects every new lab entry. |
| Ten-state lifecycle | ADR: *"Ten-state entry lifecycle with file-based change tracking"* | commit `c2fe604`, `upgrades/README.md` | Medium — well-documented in `upgrades/README.md` already, ADR adds little. |
| Hard gate on `scope-map.md` + `challenges.md` before generator | ADR: *"Hard-gate the generator step on scope-map and challenges artifacts"* | `CLAUDE.md`, workflow design | High — load-bearing for workflow correctness; rationale lives in chat-only. |
| Three-lens critic-panel with minority-veto | ADR: *"Replace single critic with three-lens panel; any lens can veto"* | git history, agent definitions | High — major architectural choice, rationale not durable. |
| Distillation step (anti-anchoring) | ADR: *"Read distillations, not raw subagent output, after step 6"* | `CLAUDE.md`, `subagent-distiller` agent | High — counter-intuitive constraint, will be questioned. |
| Librarian-first rule | ADR: *"Invoke canon-librarian before WebSearch on research questions"* | `CLAUDE.md` | Medium — codified in CLAUDE.md, but the *why* (anti-confirmation-bias) isn't. |
| Path discipline (no absolute paths in artifacts) | ADR: *"All in-repo references are repo-root-relative markdown links"* | `CLAUDE.md` | Medium — well-explained in CLAUDE.md; ADR is duplicative. |
| Critic agents got `Write` tool | ADR: *"Critics persist verdicts via Write tool"* | `upgrades/no-brainer/...critics-get-write-tool/` | Low — already covered by lab entry; ADR is duplicative. |

The first-pass backfill should target the **High** items, ~6 ADRs total. Medium items can be deferred or absorbed into related High items. Low items are already covered by other primitives and adding an ADR would be the InfoQ "Any Decision Record" failure mode.

A sensible batch strategy:

1. Write `0001-use-decision-registry.md` first — the meta-ADR that establishes the registry. Self-application: the registry's own existence is the first decision recorded by it.
2. Write the 6 High-value retrofits in one sitting, dated to the original decision but `recorded-on: 2026-04-27`, marked `retroactive: true`.
3. Stop. Do not chase Medium or Low. Re-evaluate after a month of fresh ADRs to see whether the bar held.

## Retrofit policy — how to write retrospective ADRs honestly

The dominant retrofit failure mode in the literature is "*the ADR becomes a justification for what you already built instead of a record of how you thought through the problem.*" The mitigations:

- **Mark retrospective explicitly.** `retroactive: true` and `recorded-on:` fields in the frontmatter.
- **Drive from artifacts, not memory.** A retrospective ADR's *Context* should be reconstructable from commit history, READMEs, and chat archives — not invented. If the artifact trail is too thin to write *Context* honestly, that itself is the signal: don't write the ADR.
- **Skip *Considered Options* on retrofits.** Replace with: *"Retrospective record; alternatives at original decision time were not preserved."* This is the field's recommended honest move; fabricating considered options is a literal lie.
- **Keep retrofits shorter than fresh ADRs.** A fresh ADR can be 1–2 pages. A retrofit should aim for a paragraph per section; total under one page. Less rope to hang oneself with.
- **Order by writing time, not decision time.** ADR-0002 might describe a decision dated 2026-04-26 while ADR-0007 describes one dated 2026-04-15. The number is identity; the date is chronology.

## Integration with the 12-step workflow and session-artifacts

The registry should not become a 13th step. The workflow already does too much; adding a step would be the "overdesign when told to underdesign" failure mode applied to this proposal. The integration is lighter:

```
.claude/session-artifacts/<id>/synthesis.md
                 │
                 ├── if synthesis is acted on (operator commits)
                 │      └── new ADR is written, references session id
                 │
                 └── if synthesis is shelved (operator does not commit)
                        └── no ADR; synthesis stays in session-artifacts
                            as the historical workshop record
```

Concretely:

- **No new agent.** Drafting an ADR from a synthesis is well within the orchestrator's competence; a dedicated agent is overkill until the registry has 30+ entries and a real specialization signal emerges.
- **No new workflow step.** The trigger is at *commit time*, not at synthesis time. This keeps the workflow's surface unchanged.
- **A new optional `committed_in:` field** on the lab's state table already points the same direction — the lab-entry-to-commit linkage is partly built. The registry-to-session linkage adds a `session:` field on the ADR side.
- **The session id format `YYYY-MM-DD-slug` is reused** as the value of `session:` in ADR frontmatter, so cross-references are grep-able.

The cleanest mental model: **ADRs are the synthesis artifact's afterlife.** The session ends; the synthesis is acted on; the durable summary of what was decided lives in `docs/decisions/NNNN-slug.md`, with a `session:` pointer for anyone who needs to dig into the workshop.

## Genuinely contested design points

Three places where the field disagrees and this repo will have to take a position:

1. **Single log vs split log.** Zimmermann's "Any Decision Record" critique is real: if every decision is architectural, no decision is architectural. But the split-log solution (separate folders for architecture / product / process / security) introduces classification overhead at filing time, which is exactly the ceremony this repo's lab explicitly rejects. **Tentative position:** single folder, `category:` field in frontmatter, allow split if and only if the registry grows past 30 entries and one category dominates.

2. **Mutability.** Strict immutability is cleaner; "living document" is more honest about how decisions actually accrue context. **Tentative position:** Decision and Context are immutable after acceptance; Consequences and Confirmation accept date-stamped append-only additions ("2026-09-01: this decision held under load test X"). No silent edits.

3. **Granularity threshold.** Spotify "almost always" produces a sprawling registry; Fowler "architecturally significant only" risks the registry being too sparse to be useful. **Tentative position:** the trigger is *commit-worthiness*. Anything that produces a commit which encodes a principle (not a feature, not a bug fix) deserves an ADR. This collapses to "every commit that changes how the repo works, not what it does."

These positions are tentative because they are exactly the things a `📋 prepared` state should harden.

## Open questions and ways this could be wrong

Honest list of ways this proposal could be wrong, in declining order of probability:

1. **The registry duplicates the lab.** The lab's `🔖 committed` state already records SHA + path + `committed_in:`. If we extend the lab's per-entry artifact set with a "decision" sub-document, we may not need a separate `docs/decisions/` folder at all. The registry might be a sub-feature of the lab, not a sibling. This is the strongest "ways this could be wrong" argument and deserves the cheapest experiment (next section) to settle.
2. **Solo operator + AI doesn't need a registry.** ADRs were popularized in multi-team, multi-year codebases where the cost of forgetting why-things-are-this-way is high. A single-operator repo with active AI session memory may not have the same forgetting curve. The registry might solve a problem this repo doesn't have — yet.
3. **The retrofit produces fiction.** Even with the strict retrofit policy above, retrospective ADRs may decay into post-hoc justification. The mitigations help but do not eliminate the failure mode.
4. **The registry becomes a write-only graveyard.** The InfoQ failure mode. Mitigation: the ADR-from-synthesis flow makes new entries cheap (the synthesis is the draft); the citation discipline ("see ADR-0007") makes them re-readable. Both are conjecture.
5. **Format drift.** The lab already has a format; the canon has a format; the session-artifacts have a format. Adding another format is friction. Mitigation: the proposed ADR format is deliberately MADR-aligned, so external tooling (`adr-tools`) works without modification — the repo borrows convention rather than inventing.
6. **The `commit:` field becomes a cross-reference graveyard.** Once a referenced commit is squash-merged or rebased away, the SHA becomes a dangling pointer. Mitigation: this repo doesn't squash much, and the ADR's own immutability means a stale SHA is no worse than a stale source citation in canon.

## The cheapest experiment that would validate or kill this idea

> **Write `0001-use-decision-registry.md` and three retrofit ADRs from the High-value list (allowlist `.gitignore`, folder-shaped lab entries, and the distillation step). Stop. Re-read after one week.**

The experiment costs maybe 90 minutes. It produces:

- Direct evidence on whether the format holds for this repo's decision shape.
- A working reference for whether the lab-entry / ADR distinction is meaningful in practice (failure mode #1 above gets settled by reading the four files side-by-side with the corresponding lab entries and asking "*is this duplication, or are these doing different work?*").
- A small enough corpus that abandoning costs nothing — four files in `docs/decisions/` can be deleted without the rest of the repo noticing.

What would constitute success: re-reading the four files a week later, the operator finds at least one piece of rationale they had already half-forgotten. That's the registry's whole value proposition in miniature.

What would constitute failure: re-reading the four files, every one of them is either (a) a worse version of the corresponding lab entry, or (b) a worse version of the commit message. Both modes mean the registry is duplicative and the right answer is to fold the registry's discipline into one of the existing primitives rather than spawn a new one.

## Canon-gap remediation as a prerequisite

The canon-librarian explicitly flagged on this question: *"the corpus has no direct ADR coverage."* The closest canon material is `google-sre-book` on postmortems and design docs, which is structurally adjacent (same field-shape: context, decision/action, consequences, follow-ups) but not ADR literature.

Before promoting this entry past `📋 prepared`, two canon entries should be ingested:

1. **Nygard, *Documenting Architecture Decisions* (2011)** — the foundational essay. Currently absent. The existing `nygard-release-it` corpus entry is a stub; the 2011 essay is a separate work. Source: `https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions`.
2. **MADR project README + template (4.0)** — the de-facto modern template, with the `Considered Options` mandatory addition that defines the field's evolution since Nygard. Source: `https://github.com/adr/madr` and `https://adr.github.io/madr/`.

Optional but recommended:

3. **Zimmermann, *Y-statements* (Medium)** — the compact form. Useful for the *Decision* field of richer ADRs.
4. **InfoQ, *Has Your ADR Lost Its Purpose?*** — the strongest critique. Required for the `canon-librarian`'s "must return at least one contradicting passage" rule to function on this topic.

Without these ingestions, any future workflow run on a registry-related question will be web-grounded, not canon-grounded — which is the exact failure mode the librarian-first rule is designed to prevent. The remediation is small (4 ingestions) and unblocks any future deepening of this entry.

## Sources

Primary literature:

- [Nygard — Documenting Architecture Decisions (Cognitect blog, 2011-11-15)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [adr.github.io — canonical ADR site](https://adr.github.io/)
- [MADR — Markdown Any Decision Records](https://adr.github.io/madr/)
- [MADR template repository](https://github.com/adr/madr)
- [Fowler — bliki: Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- [Joel Parker Henderson — ADR templates catalog](https://github.com/joelparkerhenderson/architecture-decision-record)

Compact form:

- [Zimmermann — Y-statements (Medium)](https://medium.com/olzzio/y-statements-10eb07b5a177)
- [Zimmermann — MADR Template Primer](https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html)

Enterprise / process variants:

- [AWS Prescriptive Guidance — ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [AWS Architecture Blog — ADR best practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Microsoft Azure Well-Architected — ADRs](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)

Granularity / when-to-write:

- [Spotify Engineering — When Should I Write an Architecture Decision Record (2020)](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record)

Critiques and failure modes:

- [InfoQ — Has Your Architectural Decision Record Lost Its Purpose?](https://www.infoq.com/articles/architectural-decision-record-purpose/)
- [Zimmermann — Any Decision Records](https://ozimmer.ch/practices/2021/04/23/AnyDecisionRecords.html)

Public-sector practice:

- [GDS Way — Documenting architecture decisions](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- [Bennett Institute — Recording technical decisions using ADRs (2024)](https://www.bennett.ox.ac.uk/blog/2024/07/recording-technical-decisions-using-adrs/)

In-repo references:

- [upgrades/README.md](../../README.md) — the lab's own format and lifecycle, with which this entry shares a state-table pattern.
- [The R&D lab entry](../../no-brainer/2026-04-26-rnd-lab/README.md) — the canonical example of a well-formed lab entry; this entry is shaped to its conventions.
- [Format-only state-transition gate entry](../../normal/2026-04-26-format-only-state-transition-gate/README.md) — the gate this entry's lifecycle table will be checked against if/when it advances.

---

## A closing note on confidence

This is a `🌱 created` entry. The proposed structure is a position, not a settled design. The strongest argument *against* this proposal — that it duplicates the lab — has not been refuted, only deferred to the cheapest experiment. The strongest argument *for* it — that this repo encodes principles in commits, and principles are exactly what ADRs were designed to capture — is real but not decisive. Honest confidence: ~60% that some version of this lands; ~30% that the right version is "fold into the lab" rather than "new sibling folder"; ~10% that this repo simply doesn't need a registry at solo-operator scale.

The next state to earn is `🔬 spiked` via the four-file experiment named above.
