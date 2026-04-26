# Distillation — outside-view

## Source agent
`outside-view`

## Invocation summary
Orchestrator asked for a reference-class forecast on "designing `upgrades/` lab at full intended maturity from day one, solo operator, no-compromises framing, no rewrites later." Subagent returned a forecast placing the proposal *moderately below base rate*, with explicit canon-access gap, named failure modes with percentages, and five conditions under which top-down design has historically worked.

## Canon access status (preserved verbatim from source)
> "Canon access gap. Could not introspect `canon/corpus/` from agent context. Forecast leans on named canonical works confirmed via web sources rather than retrieved from local corpus."

This is a load-bearing caveat: the outside-view forecast was produced *without* local corpus introspection. Treat downstream as web-sourced reference-class reasoning, not canon-grounded.

## Direct facts

1. [outside-view §2] Reference class chosen: "solo-or-tiny-team knowledge structures designed top-down at full intended maturity before any meaningful content has been written, with the explicit intent that the structure be load-bearing for years." (confidence: direct)
2. [outside-view §2] Sub-classes explicitly ruled out as base-rate-inflating: ADR repos (control group, structurally minimal), GitLab-style large-org handbooks (grew incrementally, retrofitted), funded R&D divisions (external forcing, full-time staff). (confidence: direct)
3. [outside-view §2] Base rate estimates (qualitative, not measured): 6-month survival without restructuring ~30–40%; 12-month ~15–25%; 24-month with active accretion ~5–15%; abandoned because structure-design absorbed all energy ~30–50%. (confidence: direct)
4. [outside-view §4] Failure-mode percentages: Mode A (structure absorbs energy, no content) ~30–50%; Mode B (content reveals taxonomy assumption wrong within 3–6mo) ~25–35%; Mode C (structure suppresses the content it was meant to enable) ~10–20%. (confidence: direct)
5. [outside-view §4] **Diagnostic early signal:** "ratio of meta-structure commits to substantive-content commits over first 60 days. If >3:1 by day 60, mode A is in progress." (confidence: direct)
6. [outside-view §3] "8 pre-specified design dimensions: with even 70% per-dimension survival rate, joint survival is ~5%" (numerical claim about the proposal's commitment surface). (confidence: direct)
7. [outside-view §5] Five named conditions under which top-down has historically worked (preserved):
   - (1) External forcing function (regulator, grant, multi-party collab).
   - (2) Designer has already run system manually; has prior-content corpus being retrofitted.
   - (3) Structure is dimensionally minimal — one template, one folder convention, one cross-reference primitive (ADR canonical example).
   - (4) Structural commitments explicitly made reversible via pre-committed quarterly review with trigger conditions.
   - (5) Time-boxed structure-design phase with hard deadline + pre-committed first-content milestone non-substitutable by structural work.
   (confidence: direct)
8. [outside-view §5] **Load-bearing finding (flag prominently):** "Operator's frame as stated satisfies ZERO conditions." Frame.md concedes only conditions 4 and 5 are partially recoverable. (confidence: direct)

## Inferred claims

1. [outside-view §3] "External-anchor advantage" (claude-critic-stack already exists, structure constrained not vacuum-designed) is the "single biggest divergence from typical reference-class member" — moves above base rate. (confidence: inferred)
2. [outside-view §3] "No compromises" framing is "a textbook inside-view tell" predicting 2–10× overestimation of structural durability. (confidence: inferred; rests on Kahneman & Lovallo authority frame, see below)
3. [outside-view §3] Self-reference in frame.md (scope-projector capability "added mid-design") is "direct evidence against the premise that mature future state can be specified now." (confidence: inferred)
4. [outside-view §3] Net placement: "moderately below base rate for survives 24 months without restructuring; approximately at base rate for softer yields-useful-structure-even-if-rewritten." (confidence: inferred)
5. [outside-view §4] Mode C is "most relevant to operator's tension between free-form, anyone can write anything and the maturity-ladder machinery." (confidence: inferred)
6. [outside-view verdict-block] To lift to "within tolerance": either hard time-box on structure-design with non-substitutable first-content deadline, OR explicit pre-commitment splitting reversible vs. truly-locking dimensions with locking subset minimized. (confidence: inferred)

## Authority-framed claims

1. "Most-cited canonical contrarian: Luhmann himself — 'a system based on content would mean making a decision that would bind them to a certain order for decades in advance, which would necessarily lead to problems of placement if the system and the person were capable of development.'" — underlying claim: predesigned content taxonomies become misfit as the designer/system develops. Quote present in output: yes. Confidence: direct.
2. "Kahneman & Lovallo 1993: planners adopting maximally ambitious framings underestimate completion time, overestimate structural durability by factors of 2–10×" — underlying claim: ambitious-framing planners miss durability by 2–10×. Quote present in output: no (paraphrase, no direct quote). Confidence: unsupported (authority-framed without quote).
3. "(How GitLab handbook actually came to be.)" — underlying claim: GitLab handbook was retrofitted to existing content rather than designed top-down. Quote present in output: no. Confidence: unsupported.
4. "Fowler bliki on ADRs" / "Microsoft Azure ADR guidance" cited as evidence ADR is the canonical dimensionally-minimal example — underlying claim: ADRs are the canonical control-group structure. Quote present in output: no. Confidence: unsupported (named source, no extracted text).

## Contradictions surfaced

- **Above-base-rate features vs. below-base-rate features (named in same forecast):**
  - Above: external anchor (claude-critic-stack); operator named prior failure mode (commitment device); time-to-first-useful-entry already named in frame.
  - Below: "no compromises" framing; 8 design dimensions (~5% joint survival); solo operator no forcing function; maturity ladder is most fragile commitment type; self-referential scope-projector evidence.
  - Subagent resolves to "moderately below base rate" but does not collapse the tension; both lists carried forward.
- **Hard verdict vs. softer verdict:** "below base rate for 24-month no-restructuring" vs. "approximately at base rate for yields-useful-structure-even-if-rewritten." Two different success criteria yield two different placements.

## Subagent's own verdict (verbatim)
> "Below base rate as currently framed. Reference class has poor longitudinal survival; dominant failure mode (Mode A) is amplified by 'no compromises' framing. External-anchor advantage real but does not cover 8-dimensional commitment surface."

## Gaps the subagent missed

1. No quantitative base rate from a measured study — all percentages flagged as qualitative practitioner-literature estimates. Orchestrator should treat numbers as ordinal, not cardinal.
2. Canon access gap means *local* corpus passages on PKM/zettelkasten/ADR were not retrieved — relies on canon-librarian distillation to fill.
3. No discussion of what the *first 60 days* should look like operationally (only the diagnostic ratio is given, not the prescription).
4. Reference class excludes "internal tooling repos at small AI/ML teams" — possibly a closer analog than zettelkasten, not considered.
5. Does not address whether the seven-capability taxonomy (named in frame.md as not-yet-on-disk) counts as a "prior-content corpus being retrofitted" (condition 2) — could partially satisfy condition 2 if argued.

## Token budget
~950 tokens.
