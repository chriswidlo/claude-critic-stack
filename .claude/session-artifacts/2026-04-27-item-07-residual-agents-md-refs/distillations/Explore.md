## Source agent
Explore

## Invocation summary
Orchestrator asked for an audit of residual `AGENTS.md` references in live-tracked files (excluding session artifacts). Explore returned 8 occurrences across 6 files, each with file:line, surrounding context, a quoted excerpt, and a per-occurrence Job classification (1–4), plus a classification summary and a "6 occurrences requiring change" total.

## Direct facts

1. [Explore] `AGENTS.md` does not exist at the repo root (verified). (confidence: direct)
2. [Explore] [.gitignore:21](.gitignore) contains `!AGENTS.md` as part of "Step 3: root-level files" allowlist, alongside `!CLAUDE.md` and `!README.md`. (confidence: direct)
3. [Explore] [CLAUDE.md:9](CLAUDE.md) names `AGENTS.md` inline in the path-discipline rule: "...not in CLAUDE.md, AGENTS.md, README.md, agents, prompts, workflows, upgrades, session artifacts, plans, temporary notes, anywhere." (confidence: direct)
4. [Explore] [prompts/ultraplan-next-level.md:39](prompts/ultraplan-next-level.md) reads `- README.md, CLAUDE.md, AGENTS.md (if present)` — the "(if present)" guard is present in source. (confidence: direct)
5. [Explore] [upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md:9](upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md) contains the catalyst-section quote: *"CLAUDE.md and AGENTS.md contain zero references to `upgrades/`, the lab..."* (confidence: direct)
6. [Explore] [upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md:38](upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md) restates the same diagnostic in the "What's actually missing in CLAUDE.md" section. (confidence: direct)
7. [Explore] [upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md:11](upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md): "CLAUDE.md/AGENTS.md drift becomes detectable (both should reference GOALS.md identically)." Located in a 🚀 upgrade-benefit section. (confidence: direct)
8. [Explore] [upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md:42](upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md): module-decomposition table row reads `| **orchestration** | CLAUDE.md, AGENTS.md, the workflow, gates |`. (confidence: direct)
9. [Explore] [upgrades/no-brainer/2026-04-26-git-strategy-documentation/README.md:11](upgrades/no-brainer/2026-04-26-git-strategy-documentation/README.md): "CLAUDE.md and AGENTS.md drift becomes commit-traceable." (confidence: direct)
10. [Explore] Total occurrences in scope: 8, across 6 distinct files. Excludes `.claude/session-artifacts/`. (confidence: direct)

## Inferred claims

1. [Explore] The `.gitignore:21` and `CLAUDE.md:9` references function as Job 1 (live constitutional/convention reference) — they treat `AGENTS.md` as a present, rule-governed artifact. (confidence: inferred)
2. [Explore] `prompts/ultraplan-next-level.md:39` is Job 1 but **guarded** by the "(if present)" qualifier; punch list already marks it leave-as-is. (confidence: inferred)
3. [Explore] The two `workflow-blind-to-the-lab/README.md` occurrences (lines 9 and 38) are Job 4 — historical narrative / catalyst — because they document a past grep diagnostic that motivated the upgrade. (confidence: inferred)
4. [Explore] `constitutional-layer-goals-modules/README.md:11` and `git-strategy-documentation/README.md:11` are Job 2 — forward-looking benefit claims whose framing presumes parity between CLAUDE.md and a (currently nonexistent) AGENTS.md. (confidence: inferred)
5. [Explore] `constitutional-layer-goals-modules/README.md:42` is Job 3 — module composition; it is structural (lists AGENTS.md as an owned artifact of the "orchestration" module) rather than narrative. (confidence: inferred)
6. [Explore] Job-2 occurrences are "the highest-judgment" because their benefit framing rests on parity that does not currently hold. (confidence: inferred)
7. [Explore] **Normative judgment — flag for orchestrator:** "The Job-4 catalyst occurrences must be preserved." This is a should-claim, not a fact; the orchestrator may overturn it (e.g., decide catalysts can be amended with a footnote, or that they should be rewritten if AGENTS.md is being permanently retired). (confidence: inferred)
8. [Explore] Total live-doc occurrences requiring change: **6** (the 8 total minus the guarded ultraplan line and the two catalyst lines). This count depends on accepting the Job-4-preserve normative call above. (confidence: inferred)

## Authority-framed claims

None. Explore did not invoke external authorities; all claims are first-person observation of repo files plus its own classification scheme.

## Contradictions surfaced

None within Explore's output. The classifications are mutually exclusive per occurrence and the underlying file evidence is non-overlapping.

Latent tension worth naming for the orchestrator: Job 1 (`CLAUDE.md:9`, `.gitignore:21`) treats AGENTS.md as a live artifact, while Job 2 occurrences treat parity as a *future* benefit not yet realized. These two framings are inconsistent about whether AGENTS.md presently exists or is aspirational — Explore reports both without reconciling them.

## Subagent's own verdict (verbatim)

"Total live-doc occurrences requiring change: **6** (excluding the guarded ultraplan line and the two catalyst lines)."

## Gaps the subagent missed

- No recommendation on **which direction** to resolve the inconsistency: create AGENTS.md to match the Job-1 references, or delete the Job-1 references to match the missing file. Explore enumerates but does not pick.
- No check whether `AGENTS.md` was ever tracked in git history (would inform whether this is residue of deletion vs. residue of an aspirational file that never existed).
- No survey of upstream/external conventions (e.g., whether AGENTS.md is a standard Claude Code convention the user may want to honor by creating the file).
- The Job-4 "must preserve" judgment is asserted without examining the alternative — a brief footnote in catalysts noting AGENTS.md was later retired would preserve narrative integrity without leaving a dangling reference.
- No examination of whether the `.gitignore:21` `!AGENTS.md` allowlist line is harmful (it is not — it admits a nonexistent file, which is inert) vs. merely cosmetic.

## Token budget

~720 tokens.
