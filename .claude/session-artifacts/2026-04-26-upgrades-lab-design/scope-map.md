# Scope-map — upgrades lab design

Session: `2026-04-26-upgrades-lab-design`
New requirement (compressed): design `upgrades/` at repo root as a mature-from-day-one R&D lab spanning eight dimensions (document types, disciplines, maturity ladder, cross-references, methods, failure archive, naming, workflow integration), seeded with 12 known initial entries (A–L).

Default per CLAUDE.md: `subsume` or `replace`. `extend` and preservation require a stated, substantive reason. `conflict` requires user decision.

---

## Existing primitives touched

| # | primitive | source | relationship | one-line rationale |
|---|-----------|--------|--------------|--------------------|
| 1 | `canon/` `body_completeness` enum (`stub \| full \| toc_plus_chapters \| abstract_only \| fetch_blocked`) | explore §direct-5 | **extend** | Field measures *ingestion completeness of an external work*, not *epistemic maturity of an internal idea*; one combined enum would conflate "we have the PDF" with "we believe the claim". Lab gets its own ladder; `body_completeness` stays in canon untouched. |
| 2 | `canon/` `stale: true\|false` flag | explore §direct-6 | **extend** | Same axis-mismatch as #1: `stale` answers "did the upstream world move past this entry?", lab maturity answers "where on the raw→integrated path is this idea?". Lab adds an analogous-but-separate `superseded_by` / `archived_at` field rather than reusing `stale`. |
| 3 | `.claude/session-artifacts/<id>/` ephemera + `exemplars/` promotion path | explore §direct-1, gap-3 | **subsume** | `exemplars/` is the only existing "matured artifact gets promoted out of ephemera" mechanism. The lab subsumes this role for upgrade-class artifacts: a matured lab entry IS the new home for what would have been promoted to `exemplars/`. `exemplars/` either becomes a redirect-only dir or is repurposed as workflow-quality reference traces (distinct from upgrade ideas). |
| 4 | `tests/regression/<scenario>.md` — failure archival by example | explore §direct-15 | **extend** | `tests/regression/` archives *workflow-correctness failures the stack must not repeat* (executable-ish guardrails). Lab failure-archive captures *killed upgrade hypotheses with reasoning trail*. Merging would force regression tests to carry research-postmortem prose, or force killed-idea writeups to fit a scenario-test template — both lossy. Two archives, named link primitive between them. |
| 5 | `plans/<plan>.md` deferred-capabilities list (C3/C6/C7/C12/C13 in `ok-cool-this-is-warm-balloon.md`) | explore §direct-17 | **subsume** | `plans/` is *de facto* a backlog of unworked ideas marked "deferred" — exactly what the lab is for, with weaker structure. Deferred items migrate into lab entries at the appropriate maturity rung; `plans/` either empties to zero or is restricted to in-flight, non-deferred multi-step plans. Keeping both = two backlogs. |
| 6 | Critic verdicts (`approve\|rework\|reject`) + `decision-log.md` | explore §direct-7, §direct-16 | **extend** | The verdict enum is workflow-internal (a critic's call on a candidate inside one session). The lab needs *maturity transitions* across time, written by the curator/operator, not by critics. Same vocabulary would mislead — "approve" on a critic ≠ "ready for integration" on a lab entry. Lab gets its own transition vocabulary; `decision-log.md` pattern (one-line transition record with reason) is reused as a *format*, not as the same file. |
| 7 | Frame revision pattern (`## Revision N`, append-not-edit) | explore §direct-12 | **extend** | Revisions are intra-document accretion within one frame's life. `supersede` / `builds-on` / `refutes` are inter-document edges across the lab graph. One primitive cannot do both: if `## Revision N` were stretched to inter-doc, a superseded entry would have to be physically merged into its successor, destroying the ability to read the killed reasoning standalone. Lab adopts the *append-don't-edit* discipline; adds new edge primitives for cross-doc. |
| 8 | Distillation confidence markers (`direct\|inferred\|unsupported`) | explore §direct-8 | **extend** | These are *claim-level epistemic provenance* (where did this assertion come from inside one doc). Lab maturity is *document/idea-level* (where is this idea in its lifecycle). A 'raw' lab entry can contain `direct` claims; an 'integrated' entry can contain `unsupported` ones. Different scopes; merging collapses them. Lab entries reuse the marker vocabulary verbatim at claim-level. |
| 9 | Frontmatter agent schema (`name`, `description`, `tools`) | explore §direct-3 | **extend** | The `upgrades-curator` agent (item E in the initial backlog) follows the existing schema as-is. No new fields required at the agent layer. The schema is for agents; lab entries are not agents — they are documents — so the schema is not stretched to cover them. |
| 10 | Naming convention (`<YYYY-MM-DD>-<slug>` for sessions, kebab-case throughout) | explore §direct-9, §direct-10 | **extend** | Lab entry names extend the convention with a discipline/document-type prefix or suffix (e.g., `<discipline>/<YYYY-MM-DD>-<slug>.md` or `<YYYY-MM-DD>-<doctype>-<slug>.md`). Pure session-style date-slug under-determines lab artifacts because the lab needs the doc-type readable from the path (per canon-librarian inferred-5: folder hierarchy and naming are load-bearing semantic primitives). |
| 11 | `CLAUDE.md` / `AGENTS.md` near-duplicate operating instructions | explore §direct-18, §inferred-7 | **conflict** (see Requires decision) | Adding lab references to operating instructions doubles the existing drift risk. Two paths exist (canonicalize one + path-substitute, or accept dual-write) and the user has not chosen. The lab's mere existence does not force the choice, but the lab's *integration touchpoints* (Step 14, curator agent, etc.) cannot be specified until this is resolved. |
| 12 | The seven-capability taxonomy (frame.md only; not on disk elsewhere) | explore §direct-19, frame §open-question-3 | **conflict** (see Requires decision) | The taxonomy can have exactly one canonical home: either it lives inside `upgrades/` (lab is the anchor; agents/canon link in) or it lives in a top-level `MODULES.md` / `TAXONOMY.md` that the lab references. Both-places = guaranteed drift on first divergence. User has not chosen the home. |
| 13 | Stack philosophy: "every decision routes through 12-step workflow; no backlog-of-unworked-ideas" | explore §inferred-4 | **replace** | The lab is a structural change to this philosophy by definition — the requirement is *exactly* "support a backlog of unworked ideas with structure." Replacing the philosophy means: workflow is for decisions-being-made-now; lab is for ideas-not-yet-decided; promotion path runs lab → workflow when an idea is ripe. No reason to preserve the old philosophy as-is — the user's stated requirement contradicts it. |
| 14 | `pages/`, `journals/`, `logseq/`, `.obsidian/` (uncommitted, present in working tree) | explore §gap-1, git-status | **conflict** (see Requires decision) | These dirs may already serve a free-form notebook role for the operator. If they do, the lab's "lab-notebook" document type duplicates them; if they do not (Logseq scratch only), the lab is net-new. User has not stated their role. |

## Initial backlog items (A–L) — net-new vs. overlapping with existing primitives

These are *contents* of the lab, not primitives the lab touches, but each must land in a slot the lab structure anticipates. Labels here = whether the item duplicates an existing stack primitive (and would be `subsume`/`replace` against it) or is net-new.

| item | lab-entry summary | relationship to existing stack |
|------|-------------------|-------------------------------|
| A | hooks (workflow-time interception points) | net-new — no current hook primitive in `.claude/agents/` or workflow |
| B | shadow comparator (run candidate twice, diff) | net-new — no shadow/AB primitive exists |
| C | security lens (4th critic) | extends critic-panel primitive (3 → 4 lenses); design-question, lives as lab entry until matured |
| D | epistemic lens (5th critic candidate) | same as C — extends critic-panel |
| E | `upgrades-curator` agent | extends existing agent set; uses agent frontmatter (#9) as-is |
| F | session ledger format | **subsume target = `decision-log.md`** (#6); session ledger is the generalized successor |
| G | classifier blockers (when to refuse to classify) | extends `requirement-classifier` agent contract |
| H | experiment-running (scripted A/B with measured outcomes) | net-new; tied to B (shadow comparator) and to lab "methods" dimension |
| I | research stack (alternative outside-view sources) | extends `outside-view` agent + canon-refresher |
| J | external shadow (run a separate model as critic) | net-new; tied to B/H |
| K | scope-projector / maturity-extrapolator | net-new; flagged in frame as self-referential evidence (would have changed *this* design) |
| L | git strategy (branch/commit policy for the stack itself) | net-new; no existing git-policy artifact |

Lab structure must accommodate all 12 items as initial entries at varying maturity rungs (most at "raw" or "triaged"; F/C/D plausibly at "designed" because they have already been discussed).

---

## Deletion cost (for subsume/replace rows)

- **#3 `exemplars/`** (subsume): callers = unknown; gitignore exception in `.claude/session-artifacts/.gitignore`; any agent or doc that references `exemplars/` by path needs redirection. Concrete blast radius: low (single tracked subdirectory, currently lightly populated per Explore). Migration: decide whether `exemplars/` is repurposed (kept, narrower meaning) or removed (contents migrated into lab as `integrated`-rung entries with provenance note). User decision required if removal.

- **#5 `plans/`** (subsume): callers = `plans/ok-cool-this-is-warm-balloon.md` is referenced from at least the prior session that produced it; deferred items C3/C6/C7/C12/C13 must each be read and migrated to lab entries at appropriate rungs. Config surface: any tooling (likely none; Explore did not surface tooling against `plans/`). Concrete blast radius: medium — content migration of the deferred items is real work; the directory itself can stay (narrower scope) or be removed.

- **#13 stack philosophy** (replace): callers = `CLAUDE.md` and `AGENTS.md` both encode the implicit "every decision → workflow → artifact" rule in their step descriptions and "Things you must not do" lists. Replacing the philosophy means editing both files to acknowledge a second routing path (lab-only, no workflow). Concrete blast radius: high in *prose-edit* terms (the two operating-instruction files), low in *agent-contract* terms (no agent currently enforces the old philosophy programmatically). Drift risk between the two files is amplified by this edit (see #11 conflict).

---

## Requires decision (conflicts)

- **#11 `CLAUDE.md` vs `AGENTS.md` drift** vs lab-introduces-new-references: both files must learn about `upgrades/`. Both cannot coexist as near-duplicates without a drift-management primitive. User has not chosen between (a) canonicalize `CLAUDE.md`, generate or path-substitute `AGENTS.md`, (b) accept dual-write with a lint check, or (c) merge to one runtime-agnostic file. The lab cannot specify its workflow-integration prose until this is decided.

- **#12 seven-capability taxonomy home**: the taxonomy must live in exactly one place. Candidates: (a) `upgrades/disciplines.md` or equivalent — the lab anchors it; (b) top-level `MODULES.md` or `TAXONOMY.md` — separate, lab references it; (c) inline in `CLAUDE.md` — colocated with workflow. User has not chosen. The lab's `disciplines` dimension cannot be designed concretely until this is decided, because the lab's discipline list is either *the* taxonomy or *a view of* the taxonomy.

- **#14 `pages/` `journals/` `logseq/` `.obsidian/` role**: if these are the operator's existing free-form notebook, the lab's lab-notebook document type subsumes them and they are redundant; if they are unrelated personal scratch, lab is net-new. User has not stated. Until stated, the lab cannot decide whether "free-form lab notebook" is a new document type or a pointer into an existing tool.

---

## Preserved primitives with stated reason (non-default)

None. Every primitive above is either being touched (subsume/replace/extend) or is a flagged conflict. No primitive is being preserved purely on "team continuity" or "different purpose" grounds — every `extend` carries a substantive reason why a single combined primitive would conflate axes.

---

## Primitives the distillations did not name but the query implies

Surface for orchestrator (may justify a follow-up Explore pass):

1. **`prompts/` directory schema** — Explore noted the dir exists (§direct-1) but did not characterize its contents or naming. Lab "methods" dimension may overlap with `prompts/` if `prompts/` already stores reusable prompt templates that act as methods. Check before designing the methods slot.

2. **Token-budget primitive** — Explore §inferred-6 notes ≤600 / ≤2k token budgets are prose-only, not schema. The lab's `methods` dimension may want to formalize budgets as a field; if so, this becomes a new primitive that should be reflected back into agent frontmatter (#9 extend would then become subsume).

3. **Implicit on-disk footprint of the seven-capability taxonomy** — Explore §gap-6 did not check whether agent descriptions cluster around the seven categories. If they do, the taxonomy is *partially* on disk already (latent), which strengthens condition-2 of the outside-view forecast (prior-content corpus being retrofitted) and changes the #12 conflict resolution.

4. **Integration touchpoint count** — Explore §gap-2 did not enumerate which of the 10 existing agents would need to *read* lab artifacts. The lab's "integration with the 12-step workflow" dimension cannot be sized without this count.

5. **`canon-refresher` agent contract** — named in CLAUDE.md, not surfaced in Explore distillation. Lab item I (research stack) and any "lab → canon promotion" path depend on `canon-refresher`'s existing intake shape.

6. **Existing `.claude/session-artifacts/.gitignore` semantics** — Explore noted `exemplars/` is the tracked exception; the exact ignore pattern (and whether `upgrades/` would inherit similar treatment if placed under `.claude/`) is not enumerated. Affects #3 and the question of whether the lab lives at repo root or under `.claude/`.

---

## Notes for the generator

- The default per CLAUDE.md is `subsume`/`replace`; this map produced two `subsume`, one `replace`, seven `extend`, three `conflict`. The high `extend` count is justified per-row by an axis-mismatch argument (different scopes / different writers / different lifecycles), not by politeness. The generator should still pressure-test each `extend` — if an axis-mismatch argument is weak, the row should fall back to `subsume`.
- The three `conflict` rows (#11, #12, #14) are *hard* preconditions for several lab dimensions. The generator must either (a) state assumptions the user must confirm, or (b) defer those dimensions to a follow-up. Do not silently pick.
- The deletion cost on #13 (stack philosophy replace) is the largest prose-edit blast radius and should be addressed in the generator's "named ways this could be wrong" section: replacing the philosophy without a clean lab→workflow promotion protocol risks ideas languishing in lab forever.
- Frame-challenger (next step) is required by CLAUDE.md to challenge any preserved primitive in this map. There are no preserved-without-touching primitives here (all `extend` rows touch the primitive), so the challenger's mandatory targets are the three `conflict` rows and the seven `extend` rationales — specifically whether each `extend` should collapse to `subsume`.
