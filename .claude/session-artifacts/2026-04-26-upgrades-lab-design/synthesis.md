# Synthesis — `upgrades/` lab design

Session: `2026-04-26-upgrades-lab-design`. Step 12. Workflow ran through two full critic-panel loops (cap per CLAUDE.md). Final post-critique recommendation below.

## 1. Classifier label and alternative

**Primary:** `new` — designing a directory and operational primitives that don't yet exist.
**Frame bias the label carries:** over-design before evidence. "Mature from day one" amplifies it.
**Alternative classification:** `extend` — would become primary if the question were "how does `upgrades/` integrate with the existing 12-step workflow," because the lab is also institutional memory over an existing stack. The classifier kept `new` because the question foregrounds internal structure.

## 2. Reframe (current revision: 2)

The user's framing was *total-rewrite-cost minimization via mature-from-day-one structure*. Under this framing, all eight named dimensions get full-fidelity design now, in exchange for never rewriting later.

The **revised frame** (after critic panel loop 1's convergent objection): the goal is still no-rewrite, but the *theory* of how to achieve it changes. Commit to as few primitives as possible; make those primitives extremely simple; ensure every other apparent structure is a *view* over them; instrument the controls that catch mismatches early enough to act on. Locking dimensions drop from 4 to 2; everything else becomes additive metadata.

The frame revision was triggered by two converging frame-level objections from the panel — the architecture lens said the lab should be a capability-overlay on existing session-artifact promotion (not a peer module); the product lens said the operator's actual problem is "have somewhere I can write that doesn't punish me for writing," not "design a structure that survives." Both reduced to: *less new structure, more accommodation of what already happens.*

## 3. Reference-class forecast (outside-view distillation)

Reference class: *solo-or-tiny-team knowledge structures designed top-down at full intended maturity before any meaningful content has been written, with the explicit intent that the structure be load-bearing for years.*

Base rates (qualitative, from practitioner literature):
- 6 months without significant restructuring: ~30–40%
- 12 months without significant restructuring: ~15–25%
- 24 months without significant restructuring with active content accretion: ~5–15%
- Abandoned because structure-design absorbed all the energy and no content ever landed: ~30–50%

The original frame satisfied **zero** of the five conditions historically lifting top-down lab designs above their base rate. The revised frame (Revision 2) satisfies three: (2) prior-content corpus to retrofit, (4) explicit reversibility pre-commitment, (5) time-boxed structure-design phase.

Diagnostic early signal: ratio of meta-structure commits to substantive-content commits over first 60 days. If >3:1 by day 60, structure-design is absorbing energy — the dominant failure mode (Mode A, ~30–50% of the class).

## 4. Canon passages — supporting and contradicting

**Supporting:**

- *Anthropic, How we built our multi-agent research system (2025):* "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." Used to specify document types as (objective + output + boundary) triples, not topic names.
- *Anthropic, multi-agent paper:* "Subagent output to a filesystem to minimize the 'game of telephone.'" Direct support for filesystem-native artifacts with lightweight references.
- *Anthropic, Effective Context Engineering (2025):* "Folder hierarchies, naming conventions, and timestamps all provide important signals." Used to argue naming itself is load-bearing semantic primitive.
- *Cockburn, Hexagonal Architecture (2005):* "The protocol for a port is given by the purpose of the conversation between the two devices." Used to frame lab/workflow boundary as ports-and-adapters; ultimately reduced to a single port (the promote operation).
- *Google SRE, Site Reliability Engineering (2016), Ch. 15:* postmortem template (trigger criteria defined in advance, template-driven format, review/publish as separate states), blameless framing, recurrence ritual. Used for failure-archive design (the `killed` type).

**Contradicting (flagged prominently):**

- *Anthropic, Effective Context Engineering (2025):* **"'do the simplest thing that works' will likely remain our best advice."** Direct contradiction of "mature from day one." The original frame fought this; the revised frame substantially adopts it.
- *Anthropic, Effective Context Engineering (2025):* "indexing systems grow with the material they index" — not designed top-down before the first email. Contradicts pre-designing the full taxonomy.
- *Anthropic, Building Effective Agents (2024):* "Frameworks make it tempting to add complexity when a simpler setup would suffice." The lab is structurally a framework; same warning applies.

**Corpus bias note:** the canon-librarian flagged the corpus as the *wrong* corpus for this question — heavy on systems-engineering and agent-orchestration, zero entries on R&D-process methodology, knowledge-management, or lab organizational history. The maturity-ladder semantics, document-type taxonomy, and cross-reference vocabulary in the recommendation are designed *without* canonical anchoring. Higher-uncertainty design moves than usual. A canon-refresher pass adding ADR/RFC literature, zettelkasten, TRL, GRADE, and Bell Labs/PARC histories was recommended.

## 5. Scope-map summary and unresolved conflicts

Scope-map labeled 14 existing primitives. Summary: 2 subsume (`exemplars/` promotion path, `plans/` deferred-capabilities), 1 replace (stack-philosophy "no backlog of unworked ideas"), 7 extend (`body_completeness`, `stale`, `tests/regression/`, critic verdicts + decision-log, `## Revision N`, distillation confidence markers, agent frontmatter, naming convention), and 3 conflict (CLAUDE.md/AGENTS.md drift, seven-capability-taxonomy ownership, role of `pages/`/`logseq/`).

The frame-challenger then challenged each `extend`. The strongest hits:
- `## Revision N` should be `subsume`/`replace`, not `extend` — the lab's transition vocabulary supersedes it for lab-entry purposes.
- Naming convention (extend with discipline path) is hostage to the unresolved seven-capability-taxonomy conflict (#12); encoding an unresolved taxonomy into pathnames is a rewrite trap.

**Unresolved conflicts carried into the recommendation:**
- The seven-capability taxonomy lives in `MODULES.md`. The lab references but does not own it. This is the recommendation's stance, but `MODULES.md` itself does not yet exist.
- CLAUDE.md/AGENTS.md drift remains unaddressed at the operating-instructions level. The recommendation does not require touching either; the lab can run under both.
- `pages/`/`logseq/`/`.obsidian/` are operator notebooks that already partly serve a "free-form capture" role. The recommendation introduces `upgrades/inbox/` as a structured-capture surface; the operator may continue using `pages/` for unstructured thought without contradiction (the inbox is for entries that *might* later be promoted; pages is for thinking that won't).

## 6. Frame-level challenge and how the recommendation addresses it

**The challenge (carried forward from challenges.md and re-affirmed by panel loop 1):**

> The frame commits to eight design dimensions when the only condition that historically saves top-down lab designs (condition 4: explicit reversibility pre-commitment) demands minimizing the locking-dimension count — name which dimensions are genuinely locking and design *only those* at full fidelity, leaving the rest reversible.

**How the recommendation addresses it:**

Locking dimensions reduced from 4 (after Revision 1) to **2** (after Revision 2):

1. **Slug-based stable IDs.** Every entry has a `<YYYY-MM-DD>-<short-kebab>` slug at creation. Cross-references use slugs, not paths. Renames, subfolders, restructures don't break references.
2. **The promote operation.** A single bash script: source artifact → assign slug → minimal frontmatter (slug, created, type, maturity) → move/link into `upgrades/` → INDEX update.

Document-type set, maturity-ladder semantics, cross-reference vocabulary, disciplines, naming-beyond-date-slug, and subfolder organization are all **additive metadata**, demonstrated through three worked examples (adding `experiment` type, renaming `matured` → `validated`, subfoldering by discipline) showing the changes don't require touching prior entries' content.

The capture-first surface (`upgrades/inbox/`) addresses the product lens's "operator's actual problem" reframe: 10-second `echo > inbox/<slug>.md` capture, no metadata required.

## 7. Post-critique recommendation

**Build `upgrades/` as a thin capability-overlay on existing session-artifact promotion + a capture-first inbox surface.** Two locking primitives only — slug-based stable IDs and the promote operation. Everything else (types, maturity, cross-references, disciplines, subfolders) is additive metadata.

**Day-by-day plan, incorporating product-lens v2 deltas as post-critique adjustments:**

**Day 1 (today, post-synthesis):** Write `bin/upgrades-promote.sh` (~30 lines bash) — the minimum tooling for the second locking primitive. Self-apply: promote this synthesis as the first lab entry. Retrofit one backlog item (e.g., backlog item A: harness hooks) as a `claim` entry, maturity `raw`. Capture one inbox entry to test the express path. **Day-1 deliverable: one script, three substantive entries.** Not four scripts, not pure infrastructure.

**Days 2–7 (pre-freeze):** Retrofit three more backlog items into `upgrades/`. Add `bin/upgrades-index.sh` (INDEX regeneration from frontmatter) when entry count exceeds 3. Add `bin/upgrades-lint.sh` (frontmatter validation) before day-7 ratification. Inline `SCHEMA.md`, `PROMOTION.md`, `TIMEBOX.md` content into the synthesis-as-first-entry to avoid implicit-meta-file references; extract them later if/when they outgrow the entry. **Default the lint pre-commit hook ON** with an `UPGRADES_LINT_HOOK=0` opt-out — capture-first durability requires it.

**Day 7 (ratification):** Three locking-dimension components must be on disk: `promote.sh`, `index.sh`, `lint.sh`, and the synthesis-as-first-entry with the schema content. The `ratio.sh` script is *not* a day-7 dependency — it lands later. Ratify the slug primitive and the promote operation. Freeze them until quarterly review (subject to break-glass).

**Day 14 (first-content milestone):** At least 4 substantive entries in `upgrades/` retrofitting at least 4 of the 12 backlog items.

**Day 30:** Add `bin/upgrades-ratio.sh`. Specify ratio baseline as **"meta vs content commits since the first content commit"** (not since session synthesis), so day-1 infrastructure work doesn't load the metric. Document this in the script's docstring.

**Day 60 (falsifier audit):** Run `./bin/upgrades-ratio.sh`. If ratio > 3:1, trigger procedure: write a `killed` entry naming what structural commitment was wrong; freeze meta-commits until ratio recovers below 2:1.

**Quarterly:** Review (a) ratio audit, (b) discipline-tag distribution (now that `MODULES.md` may exist), (c) promotion-criteria fit, (d) reversible-dimension cost reassessment.

**Specific frontmatter and schema adjustments** (folding architecture-lens v2 non-blocking edit + product-lens v2 fixes):

- The `discipline:` field is **optional until `MODULES.md` exists**. New entries omit it; old entries don't need batch-retag. When `MODULES.md` lands, new entries gain it; old entries can be backfilled lazily without violating the additive-metadata claim.
- The synthesis-as-first-entry uses `relates_to:` to point at the *session* (`.claude/session-artifacts/2026-04-26-upgrades-lab-design/`) in prose, not as a slug-resolving cross-reference. The frontmatter `relates_to:` field is empty for the first entry. **No self-supersedes**.
- The starter document type set is 4: `observation`, `claim`, `decision`, `killed`.
- The starter maturity set is 2: `raw`, `matured`.
- The starter cross-reference primitive is one field with optional richer relations.

**On the directory name:** the recommendation keeps `upgrades/` per the operator's earlier choice. The rename to `lab/` is flagged as an uncertainty (see below) and a one-week trial is the proposed cheapest experiment if the operator wants to evaluate it.

**Three product-lens disagreement-points carried forward as post-synthesis adjustments** (v2 product critique returned `rework`; the panel cap was hit; product's deltas are folded as adjustments to honor the lens without a forbidden third loop):

- Day-1 reduced to one script, not four (split scripts by day).
- Self-supersedes frontmatter removed from the model entry.
- Implicit meta-files inlined into the first entry.
- Ratio baseline specified as "since first content commit."
- Lint pre-commit hook defaults ON.

The two product-lens deltas the recommendation does *not* fully accept:
- Product asked for "default lint hook ON, with explicit opt-out" — accepted.
- Product asked to make day-1 just `promote.sh` + capture + first retrofit — accepted, with the small extension that `index.sh` and `lint.sh` land within day 1–7, not all on day 1.

## 8. Named uncertainties (≥3)

1. **Whether the additive-metadata claim survives MODULES.md creation.** The strongest stress-test of the load-bearing claim is the `discipline:` field migration. The recommendation defers `discipline:` until MODULES.md exists, sidestepping a forced batch-retag — but if the operator authors MODULES.md and decides every existing entry must have a discipline tag, the migration becomes real and the additive claim weakens. Severity: medium; frequency: probably once.

2. **Whether the operator can sustain the time-box discipline.** The recommendation requires the operator to (a) actually write the day-1 promote script, (b) actually run the ratio script around day 30/60, (c) actually use the break-glass protocol when locking primitives turn out wrong, and (d) actually do quarterly review. None of these are script-enforceable beyond the pre-commit hook. If discipline lapses, the lab silently falls back to mode A. Severity: high; frequency: cumulative; the dominant risk in the reference class.

3. **Whether the 4-type / 2-state starter set holds.** The recommendation claims under-specification at day 7 is a feature, with day-60 audit checking whether the under-spec held. If real entries consistently demand finer types (e.g., the operator wants to distinguish `hypothesis` from `position-paper` from `rfc` after 5 entries), the additive layer will start carrying water that the locking layer was supposed to hold. Severity: medium; frequency: detected at day-60 audit if at all.

4. **Whether `upgrades/` is the right name.** Per the original challenge: `upgrades` connotes additive improvements, forecloses negative results and theoretical work that doesn't ship. The recommendation keeps the operator's chosen name but flags this for a one-week trial against `lab/` if the operator wants to evaluate. The cheapest experiment below addresses this directly. Severity: low (rename is a one-line change); frequency: latent until the first negative-result entry feels misplaced.

5. **Whether the bash-vs-agent decision for tooling is the right frame commitment.** The architecture-lens v2 noted: a stack whose self-described purpose is "adversarial review automation" choosing manual scripts over agents for its own institutional memory deserves to be named as a frame commitment, not a tradeoff. The recommendation accepts bash scripts as the right primitive at this scale; an agent layer is the future expansion. If the operator's intuition disagrees, the frame should be re-examined before the lab accumulates content under the bash regime. Severity: low; frequency: latent.

## 9. Cheapest experiment

**Spend the first hour of day 1 doing exactly this: write `bin/upgrades-promote.sh` (~30 lines), self-apply this synthesis as `upgrades/2026-04-26-upgrades-lab-design.md` with the inlined schema content, and retrofit backlog item A (harness hooks) as a `claim`-type entry at maturity `raw`. Total cost: ~1 hour.**

What this experiment proves or disproves:

- If self-application holds (this synthesis fits the format), the slug primitive and the promote operation are right.
- If retrofit item A fits naturally as a `claim` without contortion, the 4-type starter set is sufficient for at least one real backlog item.
- If the inbox capture surface works in <30 seconds (test by capturing a passing thought), the capture-first frame is delivered.
- If any of the three fails — self-application requires schema gymnastics, item A doesn't fit `claim` cleanly, or inbox capture takes longer than 30 seconds — the candidate is wrong before day-7 ratification, and the synthesis is rewritten before any commitment freezes.

This is the load-bearing self-application test promised in the original requirement. It is also the cheapest experiment in dollars-and-time terms because it's a single hour of operator work that produces three concrete data points against the design's central claims.

If self-application succeeds, addressing uncertainty #2 (operator sustaining time-box discipline) becomes the dominant follow-up — and that one is not addressable by experiment, only by track record.

---

## Workflow self-observations (for `upgrades/` itself, when it exists)

This session surfaced three concrete observations the lab should capture as its first inbox or `observation` entries:

1. The `requirement-classifier` agent reported writing `requirement.md` to disk; the file was not on disk. The orchestrator caught this only because `frame-challenger` flagged it as a workflow-step gap. **This is exactly the failure mode the proposed `limitations.md` artifact catches.** Worth a `claim`-type entry under category 2 (metacognition) once the lab exists.

2. The critic agents lack `Write` tool. Their verdicts were returned inline and persisted by the orchestrator. The audit trail is "me-claiming-they-said-X." **Fixable by adding `Write` to critic frontmatter** — was already on the small-immediate list pre-this-session. Worth a `decision`-type entry once the lab exists.

3. The canon corpus is the wrong corpus for R&D-lab questions (canon-librarian self-flagged this). **Worth a `claim`-type entry under "corpus-gap" pointing at the recommended canon-refresher additions** (Henderson on ADRs, IETF RFC 2026, Ahrens *Smart Notes*, NASA TRL, GRADE, Gertner *The Idea Factory*, Hiltzik *Dealers of Lightning*).
