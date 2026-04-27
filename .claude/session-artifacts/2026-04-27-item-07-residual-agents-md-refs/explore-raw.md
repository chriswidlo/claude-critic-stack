# Explore raw return — item 7

**Verified:** `AGENTS.md` does NOT exist at the repo root.

## Complete audit of `AGENTS.md` occurrences

(Excludes `.claude/session-artifacts/` per project policy. Does NOT exclude `prompts/ultraplan-next-level.md` line 39, which is reported but flagged as already guarded.)

### 1. `.gitignore`:21 — `!AGENTS.md`

**Surrounding context.** Step 3 of the allowlist declares `!CLAUDE.md`, `!AGENTS.md`, `!README.md` as root-level files to be tracked.

**Job classification.** **Job 1 — Live constitutional/convention reference.** Active allowlist rule that explicitly admits a file that no longer exists. The comment structure ("Step 3: root-level files") treats it as a current artifact rule, not historical narrative.

### 2. `CLAUDE.md`:9

> **NEVER** write absolute filesystem paths or `~/`-prefixed paths in **any** artifact in this repo — not in CLAUDE.md, AGENTS.md, README.md, agents, prompts, workflows, upgrades, session artifacts, plans, temporary notes, anywhere.

**Surrounding context.** "Path discipline (privacy + clarity) — non-negotiable" section defining rules for all artifact types.

**Job classification.** **Job 1 — Live constitutional/convention reference.** CLAUDE.md names AGENTS.md as a live artifact governed by the path-discipline rule. The sentence structure ("in CLAUDE.md, AGENTS.md, README.md...") treats these as present files subject to the rule, not as a historical enumeration.

### 3. `prompts/ultraplan-next-level.md`:39

> `- README.md, CLAUDE.md, AGENTS.md (if present)`

**Surrounding context.** Step 5 of a planning workflow enumerating files to review.

**Job classification.** **Job 1 — Live constitutional/convention reference (guarded).** The "(if present)" guard acknowledges the file may not exist. Already flagged in the punch list as "leave as-is" — correctly guarded.

### 4. `upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md`:9

> Investigation findings: *"CLAUDE.md and AGENTS.md contain zero references to `upgrades/`, the lab..."*

**Surrounding context.** ⚡ catalyst section describing the diagnostic investigation that discovered the workflow gap.

**Job classification.** **Job 4 — Historical narrative/catalyst.** Past tense, descriptive. Quotes a grep finding from an investigation. Catalysts document *why* an upgrade was needed; this records a diagnostic moment.

### 5. `upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md`:38

> CLAUDE.md and AGENTS.md contain zero references to `upgrades/`, the lab, the `/upgrade` command...

**Surrounding context.** "What's actually missing in CLAUDE.md" section, restating the investigation finding.

**Job classification.** **Job 4 — Historical narrative/catalyst.** Same diagnostic statement; restates the grep finding that motivated the upgrade. Descriptive, not prescriptive.

### 6. `upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md`:11

> CLAUDE.md/AGENTS.md drift becomes detectable (both should reference GOALS.md identically).

**Surrounding context.** 🚀 upgrade section describing future benefits.

**Job classification.** **Job 2 — Forward-looking benefit claim.** Prescriptive future language: "both should reference GOALS.md identically" assumes both files exist and should be kept in sync. Frames drift-detection as a benefit *gained by the upgrade*.

### 7. `upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md`:42

> `| **orchestration** | CLAUDE.md, AGENTS.md, the workflow, gates |`

**Surrounding context.** Module decomposition table listing what the orchestration module "owns."

**Job classification.** **Job 3 — Module composition.** Lists AGENTS.md as a member of the "orchestration" module's owned artifacts. Structural grouping with CLAUDE.md as peers.

### 8. `upgrades/no-brainer/2026-04-26-git-strategy-documentation/README.md`:11

> CLAUDE.md and AGENTS.md drift becomes commit-traceable.

**Surrounding context.** 🚀 upgrade section describing future benefits.

**Job classification.** **Job 2 — Forward-looking benefit claim.** Future conditional: "drift becomes commit-traceable" assumes both files will exist and drift. Frames traceability as a benefit of the upgrade.

## Classification summary

**Job 1 — Live constitutional/convention reference (3 occurrences):**
- `.gitignore:21` — Active allowlist rule; file doesn't exist.
- `CLAUDE.md:9` — Treats AGENTS.md as a subject of the path-discipline rule.
- `prompts/ultraplan-next-level.md:39` — Already guarded "(if present)"; punch list says leave as-is.

**Job 2 — Forward-looking benefit claim (2 occurrences):**
- `upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md:11` — Claims drift-detection as a benefit. AGENTS.md doesn't exist; claim is moot unless the file is created.
- `upgrades/no-brainer/2026-04-26-git-strategy-documentation/README.md:11` — Claims commit-traceability of drift. Prescriptive future language conditioned on both files existing.

**Job 3 — Module composition (1 occurrence):**
- `upgrades/no-brainer/2026-04-26-constitutional-layer-goals-modules/README.md:42` — Module table lists AGENTS.md as owned. Structurally dependent on AGENTS.md existing.

**Job 4 — Historical narrative/catalyst (2 occurrences):**
- `upgrades/profound/2026-04-26-workflow-blind-to-the-lab/README.md:9, :38` — Both are diagnostic findings (catalyst and supporting section) documenting *why* the upgrade was created. Historical record; altering them rewrites the investigation narrative.

## Summary judgment

The `.gitignore` and `CLAUDE.md` references are the clearest Job-1 issues — they treat AGENTS.md as a live artifact. The upgrade entries mix narrative (preserve) with prescriptive benefits (revise or delete, depending on whether AGENTS.md will be recreated). The Job-2 cells (constitutional-layer:11 and git-strategy:11) are the highest-judgment occurrences because their *benefit framing rests on parity*. The Job-3 module-composition cell (constitutional-layer:42) is structural rather than narrative — must be revised. The Job-4 catalyst occurrences must be preserved.

Total live-doc occurrences requiring change: **6** (excluding the guarded ultraplan line and the two catalyst lines).
