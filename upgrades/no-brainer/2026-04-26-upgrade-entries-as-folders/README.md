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
| 2026-04-26 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | 2026-04-27 | — | — |

> **Update history (most recent first).** Entry advanced through six lifecycle states in one ~2-day window (created 2026-04-26; spike → implemented all on 2026-04-27). The state-table-honesty discipline (LEDGER #18f) flags rapid same-session advancement; this entry is a worked example of that pattern. The cluster fired because each state's output (spike findings, prepared survey, accept decision, workflow critique, implementation) directly informed the next state's work — no asynchronous "wait for evidence" gap between states.
>
> **Operator chose option 3 ("tidy by hand")** at the post-workflow decision point — neither v1's batch script nor v2's strangler. Reasoning: scripts can become blockers; for N≈45 by-hand `git mv` with eyes on each diff is cleaner. Accept (Option C, batch script, `bin/`) was explicitly revised; what shipped is closer to the challenger's original "tidy" frame. **Coordination strategy in effect:** slash-command edit landed first (so all NEW entries arrive correctly), all existing entries migrated by-hand in one session, no script created, no `bin/` directory, no gate rule.

## Table of contents

- [Spike — 2026-04-27](#spike--2026-04-27)
- [Prepared — 2026-04-27](#prepared--2026-04-27)
- [Accepted — 2026-04-27](#accepted--2026-04-27)
- [Run-through-repo — 2026-04-27](#run-through-repo--2026-04-27)
- [Implemented — 2026-04-27](#implemented--2026-04-27)
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

## Spike — 2026-04-27

Spike performed by an orchestrator session at the operator's request to advance this entry through the lifecycle. Per `upgrades/README.md`'s state lifecycle, 🔬 spiked filters infeasible ideas — *does the basic mechanism even work?*

### What was spiked

A throwaway test entry was created at `upgrades/no-brainer/test-folder-spike-2026-04-27/test-folder-spike-2026-04-27.md` (folder-shaped, per the new rule this entry proposes). Four checks were run:

| # | Check | Result |
|---|---|---|
| 1 | Format-only state-transition gate (`.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py`) reads a folder-shaped entry without modification. | ✓ Pass — gate ran in 1ms, parsed the meta + state tables correctly, returned the expected verdict against the schema. |
| 2 | Same gate, different requested state (💎 value-proved against an entry without a value-evidence heading). | ✓ Pass — gate produced the expected WARN report. Folder shape did not affect the gate's logic. |
| 3 | git status correctly identifies the folder-shaped entry as untracked content. | ✓ Pass — `git status -s` showed `?? upgrades/no-brainer/test-folder-spike-2026-04-27/` (folder-as-unit). |
| 4 | Coexistence: flat `.md` entries and folder-shaped entries in the same parent directory. | ✓ Pass — `ls upgrades/no-brainer/` shows both shapes side by side. **Migration can be incremental, not all-or-nothing.** |

### Findings

1. **The mechanism works.** The format-only gate, git, and the filesystem all tolerate folder-shaped entries without modification. The new rule the entry proposes is not blocked by any existing primitive. *Infeasibility hypothesis falsified.*

2. **Migration can be incremental.** The original migration plan ("for each of the 28 existing entries, run `git mv`") implied a big-bang migration. The spike confirms that flat and folder shapes coexist cleanly — incremental migration is supported. This is a useful design freedom the entry's body should be updated to name (deferred to PREPARE state).

3. **The gate's regex matches the H1 line incidentally.** TEST 1 above matched the H1 title (which contained the word "spike") rather than an `## H2` heading. This is a pre-existing false-positive class in the gate's `🔬 spiked` regex (any heading level can match), unrelated to folder-shape. **Out of scope for this spike**; flag for follow-up — possibly subsumed by `tighten-run-through-repo-regex` (`#18c` in LEDGER) or its own follow-up entry on regex strictness.

### Consumers that need explicit updates (not part of spike — for PREPARE state)

The spike verified the gate; it did NOT verify other consumers. The PREPARE state should enumerate them:

- `.claude/commands/upgrade.md` (the `/upgrade` slash command) currently writes new entries as `<tier>/<slug>.md`. Needs updating to write `<tier>/<slug>/<slug>.md`.
- `upgrades/LEDGER.md` currently links entries as `<tier>/<slug>.md` (43+ rows). All links need rewriting at migration time.
- `upgrades/README.md` "How to add an entry" section names the path. Needs updating.
- Inter-entry `relates_to` field references (variable across entries — some use slugs, some use paths). Audit needed.
- Concurrent sessions may write entries in the OLD shape during/after migration. Coordination strategy needed (the current entry body does not address this).

### Spike artifacts left on disk

The throwaway test entry at `upgrades/no-brainer/test-folder-spike-2026-04-27/` was not deleted (operator declined `rm` permission during the spike turn). It is untracked, so it does not pollute git history. The operator may delete it manually, leave it as evidence that the spike happened, or repurpose it.

### Verdict for state advancement

🔬 spiked — the basic mechanism works; the entry is not infeasible. **Ready for PREPARE state**, which will:
- Enumerate misfit / duplication / wrong-shape risks against existing primitives.
- Detail the implementation plan for each consumer named above.
- Surface coordination strategy for concurrent sessions.
- Test against the lab's principles (closed-world trust, librarian-first, anti-anchoring) for belongingness.

Operator authorization required before PREPARE proceeds (per the lab's discipline).

## Prepared — 2026-04-27

Per the README's lifecycle, 📋 prepared filters *misfit, duplication, and wrong-shape implementations — does this entry survive contact with the rest of this repo's primitives, principles, and existing capability?* This section answers that question concretely. It is a checkpoint, not a commitment to implement.

### Survey of consumers (current state vs new shape)

A grep across the repo and a read of every meta-file produced this list. Each consumer is something that either reads or writes entry paths today.

| # | Consumer | Path | Current behavior | Migration impact |
|---|---|---|---|---|
| 1 | `/upgrade` slash command | `.claude/commands/upgrade.md` | Step 8 writes `upgrades/<tier>/<slug>.md`. Step 4 says "Filename will be `<slug>.md`." Step 5 also has a pre-existing bug: shows the state table as vertical, but the README enforces horizontal. | **Needs explicit edit.** Outside `upgrades/`; previously declared out-of-scope by operator. May need to be operator-driven or explicitly re-authorized. |
| 2 | `upgrades/LEDGER.md` | (in `upgrades/`) | 43+ rows linking entries by `<tier>/<slug>.md` markdown link. | **Needs link rewrite.** Mechanical (single `sed` over the LEDGER, or script-driven). Self-contained edit; safe. |
| 3 | `upgrades/README.md` | (in `upgrades/`) | "How to add an entry" lists `Create upgrades/<tier>/<YYYY-MM-DD>-<short-kebab-slug>.md`. "Required format" describes a flat `.md`. | **Needs prose update.** Two short edits. The Principles section already mentions folder-shaped entries as allowed; that line becomes the canonical rule rather than the exception. |
| 4 | `relates_to` meta field across entries | various | **Heterogeneous.** Three styles in use: bare slug (`agentic-engineering-reference-library`), bare slug with date (`2026-04-26-rnd-lab`), full path (`profound/2026-04-26-memory-and-lab-are-the-same-primitive`). | **Soft impact.** Slug-based references continue to work (the slug is preserved). Path-based references break for migrated entries. **Nothing currently parses this field**, so the impact is informational only. Normalization is "nice to have," not a blocker. |
| 5 | Format-only state-transition gate | `.claude/session-artifacts/.../check-transition.py` | Takes an explicit path argument; reads the `.md` file. | **No change needed.** Spike confirmed the gate works regardless of path shape. |
| 6 | Filesystem / git | n/a | Both tolerate flat and folder shapes side by side. | **No change needed.** Spike confirmed coexistence. |
| 7 | Concurrent sessions writing entries | n/a | At least one parallel session has already adopted the folder shape (`normal/2026-04-26-living-poweruser-knowledge-module/`) without the migration being done. Other sessions still write flat. | **Coordination concern.** See §Coordination strategy below. |
| 8 | Subagent prompts (`.claude/agents/*.md`) | various | Spot-grep for `upgrades/` reveals zero references. | **No change needed.** The lab is invisible to subagents (this is itself the subject of LEDGER #4a). |
| 9 | Canon, session-artifacts, memory directories | various | Independent persistence surfaces. | **No change needed.** Orthogonal to the lab's structure. |

**Conclusion of survey:** four consumers need updating (`/upgrade`, `LEDGER.md`, `README.md`, `relates_to` if normalized). Two need no change (the gate, the filesystem). One needs a coordination strategy (concurrent sessions). Two are not affected at all.

### Risks

Ranked by likelihood × blast radius:

1. **`/upgrade` slash command edit is out of scope per prior session boundary.** The operator previously declared `.claude/commands/` off-limits without explicit re-authorization. Without updating the slash command, *new entries continue to land in flat shape post-migration*, immediately reintroducing the inconsistency the migration is meant to eliminate. **Mitigation:** explicitly raise this in the ✅ accepted state. Either the operator authorizes the `.claude/commands/upgrade.md` edit, or the migration ships partially (existing entries migrate; new entries arrive in flat shape and need retroactive migration).

2. **LEDGER link rot during migration.** The LEDGER currently has ~30+ link rewrites needed. If any links are missed, those rows have broken markdown links until repaired. **Mitigation:** scripted rewrite + verification step (grep for any `<tier>/<slug>.md` patterns in LEDGER post-migration; should return zero matches).

3. **`relates_to` path-style references breaking.** Several entries reference others by full path. After migration these point at non-existent paths. **Mitigation:** scripted rewrite to normalize all `relates_to` to bare slug-with-date format. Or accept the transient broken state; nothing currently parses the field.

4. **Concurrent sessions writing entries during migration.** A session running while migration is in progress may write a flat-shape entry that the migration script has already passed by. **Mitigation:** §Coordination strategy below.

5. **The migration itself is reversible if botched.** All changes are `git mv` and prose edits — `git reset --hard <commit>` recovers the prior state. Blast radius is bounded.

6. **The pre-existing `/upgrade` slash command bug** (vertical state table at step 5) is unrelated to migration but lives in the same file. **Mitigation:** fix in the same edit; flag as bonus, don't make it block migration.

7. **The H1-line gate-regex false positive** noted in the spike is unrelated to migration. **Mitigation:** carry forward to a separate follow-up entry; not a migration blocker.

### Implementation plan (per consumer, in execution order)

Each step is reversible with `git reset --hard` if the next step fails.

| Step | Consumer | Action | Estimated effort |
|---|---|---|---|
| 1 | `upgrades/README.md` | Update "Required format" + "How to add an entry" sections to make folder-shape the canonical rule. The Principles section's "Folder-shaped entries" bullet promotes from "allowed" to "the rule." Add a one-paragraph note: "during the migration window, both shapes coexist; new entries should use folder shape." | XS (~10 min) |
| 2 | `.claude/commands/upgrade.md` | **Operator-authorization-gated.** Update step 4 (slug becomes folder-name + filename), step 8 (write path becomes `<tier>/<slug>/<slug>.md`). Bonus fix: step 5's vertical state-table bug → match horizontal README convention. | XS (~10 min) |
| 3 | `bin/migrate-upgrade-shape.sh` (new) | A small bash script that: (a) for each `upgrades/<tier>/<YYYY-MM-DD>-<slug>.md`, runs `git mv` to nest into a folder; (b) updates LEDGER links via `sed`; (c) optionally normalizes `relates_to` references; (d) prints a verification report listing any remaining flat-shape entries and any unresolved LEDGER links. | S (~1-2 h, including testing on one entry first) |
| 4 | Run script against ONE entry first | Migrate `upgrades/no-brainer/2026-04-26-upgrade-entries-as-folders.md` (this entry — the dogfood) and verify all four consumers handle it correctly. | XS (~5 min) |
| 5 | Run script against remaining entries | Batch-migrate the rest. Verification: `find upgrades/ -maxdepth 2 -name "*.md" -not -name "README.md" -not -name "LEDGER.md"` should return zero results (every entry now in a folder). | XS (~5 min) |
| 6 | Verify the format-only gate still works | Run `check-transition.py` against 3-5 random migrated entries. | XS (~2 min) |
| 7 | Update this entry's state-table | Mark `🔨 implemented` with today's date. | XS (~1 min) |

**Total committed effort if all steps proceed:** ~2-3 hours of bounded engineering.

### Coordination strategy for concurrent sessions

The original entry's body did not address this; the spike surfaced it as a gap. Three options, ordered by complexity:

- **Option A — eventual consistency.** Migrate now; accept that concurrent sessions writing in flat shape during/after migration will create new inconsistencies. A weekly reconciliation pass (this same script, run periodically) catches them. Cheap, slightly messy.

- **Option B — operator-coordinated migration.** Operator pauses other sessions for the ~30-minute migration window, then unpauses. Cleanest. Requires operator coordination overhead.

- **Option C — slash-command edit lands first.** Update `.claude/commands/upgrade.md` to write folder shape *before* migrating existing entries. After this lands, all *new* entries from any session land in folder shape automatically. Migration of existing entries can then proceed at any pace. **Preferred** — converts the coordination problem into a one-time slash-command edit.

Option C requires the slash-command edit (step 2 above) to be authorized first.

### Belongingness test (per the lab's graduating criteria)

The README's "What turns a seed into a real upgrade" section names four criteria. Testing this entry:

- ✅ **Tangible value.** Specific class of failure prevented: supporting artifacts (transcripts, prototypes, sample outputs) currently live in `temporary/` or `.claude/session-artifacts/` and get orphaned from the entry that motivated them. The folder shape co-locates artifact and entry. Concrete: at least one entry (`agentic-engineering-reference-library`) explicitly cannot complete without this.
- ✅ **Demonstrably better than alternatives.** The entry's existing body justifies folder-as-entry over the sidecar variant. Spike confirmed the alternative ("sidecar — file plus optional folder") creates branching shape; folder-as-entry gives every entry the same shape. Smaller alternative ("just dump artifacts in `temporary/`") is what's currently failing — `temporary/` files become orphaned.
- ✅ **Belongs in this repo specifically.** Pairs with at least three concrete pending entries: `agentic-engineering-reference-library` (consumes this), `state-table-honesty-discipline` (could include update-history blockquote in folder), `format-only-state-transition-gate` (has supporting spike script that today lives in `.claude/session-artifacts/` — could move into the folder).
- ✅ **No better-existing solution.** Survey confirmed no existing primitive subsumes this. The lab's current "one entry = one .md" rule does not solve the artifact-orphaning problem.

All four criteria pass.

### Comparator analysis (vs. doing nothing, smaller version, subsumption)

- **Vs. doing nothing.** Cost continues to grow as more entries surface needing supporting artifacts. The first such entry (`agentic-engineering-reference-library`, ~60KB of structured material in `temporary/`) is already orphaned. Each subsequent one repeats the failure.
- **Vs. smaller version.** A purely-additive sidecar pattern was considered and rejected in the entry's body for branching-shape reasons. The smallest-meaningful version *is* this one.
- **Vs. subsumption.** No existing entry contains this proposal. Closest is `agentic-engineering-reference-library` (which depends on this) and `rnd-lab` (which sets up the lab structure but does not address artifacts).

### Concurrent-session evidence (post-spike)

Between spike and prepare, a new entry appeared at `upgrades/normal/2026-04-26-living-poweruser-knowledge-module/2026-04-26-living-poweruser-knowledge-module.md` — already in folder shape. This is empirical evidence:
- Other sessions are reading the upgrade-entries-as-folders entry and acting on it.
- The folder shape is being adopted organically, ahead of formal migration.
- Coexistence is already the lab's reality.

This makes the migration *less* about "rolling out a change" and more about *catching up to a state that's already partially implemented*.

### Verdict for state advancement

📋 prepared — implementation plan is concrete, risks are named with mitigations, coordination strategy is identified, belongingness test passes, no better alternative exists.

**Ready for ✅ accepted.** What operator acceptance means at this state:
1. Authorize the `.claude/commands/upgrade.md` edit (step 2 above) — without this, new entries continue to arrive in flat shape and the migration is partial.
2. Authorize creation of `bin/migrate-upgrade-shape.sh` (step 3) — the migration script.
3. Pick the coordination strategy (A, B, or C above; recommend C).
4. Pick a window for the migration to run (~30 minutes of operator attention).

**What operator acceptance does NOT mean:**
- Does not commit the operator to running the 12-step adversarial workflow on the implementation choices (that's ⚙️ run-through-repo, a separate state).
- Does not commit to specific `.claude/commands/upgrade.md` rewording — that detail is part of implementation, not acceptance.
- Does not commit the operator to migrating *all* entries immediately — partial migration is allowed (spike confirmed coexistence works).

### Acceptance criteria — how we'd know if this was wrongly accepted

If, after one month of migrated state:
- No entry has actually used the folder shape for supporting artifacts (every entry remains a single `.md` inside its folder), the prose-only assumption was correct, the migration cost was wasted, and this entry should be honestly demoted in its body.
- Conversely, if at least one entry has acquired supporting artifacts and at least one orphan in `temporary/` would have been prevented by the new shape, the upgrade has earned its keep.

The lab tradition is honest negation. If wrong, the entry says so.

## Accepted — 2026-04-27

Operator accepted the prepared plan with the following explicit choices, presented in chat and recorded here as the binding accept:

1. **`.claude/commands/upgrade.md` edit authorized.** The previous out-of-scope boundary is lifted for this specific edit (step 4 + step 8 of the slash command, plus the bundled fix to step 5's vertical-state-table bug).
2. **`bin/migrate-upgrade-shape.sh` authorized.** First script in `bin/`; first time the repo gets that directory.
3. **Coordination strategy: Option C.** Slash-command edit lands first so all new entries from any session arrive in folder shape automatically. Existing entries migrate at any pace afterwards (incremental migration is supported per the spike).
4. **Migration window TBD by operator.** Not gating subsequent states; the implementation can be designed and critiqued independent of when it ships.

The adoption decision is now binding. Subsequent states (⚙️ run-through-repo, 🔨 implemented, 💎 value-proved, 🏁 completed) operate on the implementation, not on whether to do this at all.

**Next state:** ⚙️ run-through-repo. Per the README: *"the original 12-step (if any) judged the adoption decision; this state judges the implementation."* The implementation choices to be critiqued by the workflow are listed in the orchestrator's chat handoff (slug-as-folder-name-and-filename redundancy, Option C as right choice, bash vs Python for the migration script, error handling and partial-migration recovery, `relates_to` normalization timing, slash-command bug-fix bundling).

## Run-through-repo — 2026-04-27

The narrowed 12-step workflow (Option 2 from the orchestrator's earlier handoff: classifier + parallel-gather + frame-challenger + critic-panel + synthesis, skipping reframe and scope-map since PREPARE did them) was run on the implementation choices in session `2026-04-27-upgrade-folder-shape-implementation`. Full audit trail at `.claude/session-artifacts/2026-04-27-upgrade-folder-shape-implementation/` (gitignored): requirement.md, distillations of outside-view + canon-librarian, challenges.md, candidate v1 + v2, six critic verdicts across two loops, decision-log, synthesis.

### Path through the workflow

- **Classifier:** `refactor` primary, `extend` alternative. Frame bias flagged: items 4 (`relates_to` normalization) and 6 (slash-command bug fix bundling) are *behavior changes hiding inside a refactor*.
- **Outside-view:** above base rate (~75–85% joint success), primarily because tooling-first sequencing converts the migration from a deadline to a backlog. Modal failure: `sed` regex misses an edge-case link form. Failure mode #3 (partial migration becomes permanent) is *enabled* by the chosen Option C.
- **Canon-librarian:** SRE 2016 single-source. Direct hits on bundling (don't bundle), grab-bag (don't combine), idempotency cautionary half (don't pretend). Fowler stub: refactoring is by definition behavior-preserving.
- **Frame-challenger:** alternative frame "tidy not migrate" (by-hand checklist, no script). Steel-manned README.md inside folder. Steel-manned splitting bug fix from path-shape edit. Proposed Option D (deadlined commitment) and Option C-prime (LEDGER counter).
- **Generator → loop 1 candidate:** kept the script + adopted Option C-prime + split bug fix + deferred slug-vs-README.md as open question.
- **Critic panel loop 1:** all three lenses returned `rework`. Convergent insight: *the candidate accretes structure (counter, script, deferred decisions) that looks like discipline but actually defers the load-bearing decisions*.
- **Generator → loop 2 candidate v2:** dropped the script (strangler-style instead), dropped the LEDGER counter, dropped `bin/`, made slug-vs-README.md a binding recommendation (README.md), kept bug-fix split.
- **Critic panel loop 2:** architecture `approve`, operations `approve`, **product `rework`** — lone holdout. Product objection: v2 silently revises what the operator accepted (batch + `bin/` script → strangler) without flagging it as a re-accept event. Orchestrator escalated wrong decision (slug-vs-README.md instead of strangler-vs-batch).

### Cap reached, disagreement preserved

Per CLAUDE.md's two-loop cap, escalated to synthesis with the disagreement named. Product critic's loop-2 objection is fair and the synthesis adopts it: surface strangler-vs-batch as the headline operator-facing decision rather than implementing v2's silent revision.

### Headline decision returned to operator

**Choose: BATCH (PREPARE/v1 plan, what was originally accepted) or STRANGLER (v2 plan, what loop-2 candidate proposed).**

|  | **Batch** (originally accepted) | **Strangler** (v2 proposal) |
|---|---|---|
| Day-1 reality | Lab uniformly shaped after one sitting | Lab mixed-shape weeks/months (or forever for cold entries) |
| New surface | `bin/migrate-upgrade-shape.sh` + `bin/` directory | Path-shape rule added to format-only gate |
| Failure mode | Script bugs; operator stalls mid-migration | Cold entries never migrate (called "right outcome") |
| Terminal state | Yes, clear "done" moment | No, asymptotic; `find` one-liner for status |
| Conditional approvals | architecture + operations approvals conditional on lift conditions being implemented | architecture + operations approvals stand for v2 as written |

If batch: revert to v1 with the four lift conditions (idempotency three-state, `--status` mode, pre-flight case-collision check, post-migration verification grep), counter dropped, `bin/` location decided.
If strangler: v2 stands; three documentation tasks added (gate's README, flat-shape-tail-at-🌱 doc in `upgrades/README.md`, `find` one-liner promoted into `upgrades/README.md`).

The slug-vs-README.md decision rides along: README.md recommended in both options.

### What the workflow earned its keep on

The workflow's preventive value here was twofold:
1. **Loop 1 caught the over-engineering** (counter, script with elaborate lift conditions, deferred decisions). Without the panel, v1 would have shipped and likely hit the modal failure mode (`sed` regex misses) or failure mode #3 (partial migration permanent).
2. **Loop 2 caught the silent-revision** (v2 quietly changed what was accepted). Without the product critic holding out, the operator would have been handed strangler-as-decided-by-orchestrator rather than strangler-as-choice.

The implementation cannot proceed under either v1 or v2 without the operator's batch-vs-strangler answer.

**Next state:** 🔨 implemented — blocked on operator choosing batch or strangler. Once chosen, implementation proceeds per the chosen plan.

## Implemented — 2026-04-27

Operator chose **option 3 ("tidy by hand")** — a third option that neither v1 (batch + script) nor v2 (strangler + gate rule) fully captured. Reasoning given: *"scripts can become blockers, unless they are super clean and helpful. short info on structure is enough for agent to understand what it must do to follow the pattern."* This is closest to the challenger's original "tidy not migrate" frame from `challenges.md`.

### What changed (chronological)

1. **`upgrades/README.md`** — three additive edits:
   - "How to add an entry" updated: entry path is now `upgrades/<tier>/<slug>/README.md` (was `upgrades/<tier>/<slug>.md`); added "Why folder + README.md" rationale paragraph.
   - "Folder-shaped entries" bullet under Principles promoted from "when a single .md isn't enough" (allowed-when-needed) to "the canonical shape" (always).
   - No deletions; the lab Principles section, the four tiers, the security boundaries, and the state lifecycle all unchanged.

2. **`.claude/commands/upgrade.md`** — three edits to the `/upgrade` slash command:
   - **Bug fix** (was step 5 in the slash command spec): state table changed from vertical (`| State | Reached |`) to horizontal (8 columns, single date row) — matches the README's enforced format. *This was a pre-existing bug unrelated to migration but lived in the same file; surfaced during the prepare-state survey and fixed in the same edit pass.*
   - **Path-shape change** (step 4): "Filename will be `<slug>.md`" → "The slug becomes the entry's folder name; the doc inside is named `README.md`."
   - **Path-shape change** (step 8): "Create `upgrades/<tier>/<slug>.md`" → "Create `upgrades/<tier>/<slug>/README.md`. The entry is a folder named with the slug; the canonical doc inside is `README.md`."
   - **Constraints section**: explicit "do not write flat `<slug>.md` files; folder shape is canonical."

3. **45 entry migrations via `git mv`** — every flat-shape entry under `upgrades/{no-brainer,normal,outlandish,profound}/` moved into a folder named with its slug, with the doc renamed to `README.md`. By tier:
   - `no-brainer/`: 19 entries migrated.
   - `normal/`: 13 entries migrated.
   - `outlandish/`: 5 entries migrated.
   - `profound/`: 8 entries migrated.
   - **Total: 45 entries.** All `git mv` operations succeeded for tracked files; one untracked file (`2026-04-26-living-poweruser-knowledge-module/<slug>.md`, written by a parallel session and not yet committed) was renamed via plain `mv` since `git mv` requires the source to be tracked.

4. **One existing folder-shape entry renamed** to the new convention: `upgrades/normal/2026-04-26-living-poweruser-knowledge-module/2026-04-26-living-poweruser-knowledge-module.md` → `.../README.md`. Its sibling supporting file (`seed-research.md`) was preserved untouched — first concrete demonstration that the folder shape carries supporting artifacts as designed.

5. **`upgrades/LEDGER.md`** — 43 link rewrites via `sed`, pattern `(<tier>)/<slug>.md` → `\1/<slug>/README.md`. All rewrites verified clean (zero remaining old-style links via grep). Sed left a `LEDGER.md.bak` in place; not removed because the operator declined the cleanup `rm` permission. Backup file is safe to delete by hand.

6. **One throwaway test folder left in place**: `upgrades/no-brainer/test-folder-spike-2026-04-27/test-folder-spike-2026-04-27.md` (created during the spike state earlier in this session). Operator declined `rm` permission then and again now. Untracked; can be deleted by hand. Has zero impact on the lab.

### Verification

- `find upgrades/ -maxdepth 2 -type f -name "*.md" -not -name README.md -not -name LEDGER.md` returns empty. **Zero flat-shape entries remain.**
- `find upgrades/ -mindepth 3 -name "README.md" | wc -l` returns 46 (45 migrated + 1 originally folder-shaped).
- `grep -oE "\]\((no-brainer|normal|outlandish|profound)/[^)]+\.md\)" upgrades/LEDGER.md | grep -v "/README.md)"` returns empty. **Zero stale LEDGER links.**
- The format-only state-transition gate (`.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py`) was not re-tested in this implementation pass, but the spike state already verified it works against folder-shaped entries.

### What did NOT happen (and why)

- **No `bin/` directory created.** The migration script that PREPARE authorized (`bin/migrate-upgrade-shape.sh`) was not built. By-hand migration via `git mv` in batches of ~10 was sufficient for N≈45 and avoids the architectural commitment to a top-level `bin/` directory that a future re-evaluation would have to revisit.
- **No format-only gate rule added** for path-shape (the v2 strangler proposal). The slash command's path-shape change is the forcing function for new entries; existing entries are all migrated in this session, so no enforcement gap exists. If a future entry slips through in flat shape, the operator catches it on review (same trust model as everything else in the lab).
- **No LEDGER counter** added (the v1 amendment). The architecture critic's "LEDGER is index, not dashboard" objection survives.
- **No `relates_to` normalization** performed. Architecture invariant unchanged: nothing currently parses the field; deferral remains correct.

### What's still pending after this implementation

- The `LEDGER.md.bak` and `test-folder-spike-2026-04-27/` artifacts from this session sit on disk untracked. Operator can `rm` both at their convenience.
- Concurrent sessions running between the slash-command edit and now may have written flat-shape entries that need retroactive migration. None observed during this session, but a future session should grep for `find upgrades/ -maxdepth 2 -type f -name "*.md"` and migrate any stragglers.
- The state-table-honesty discipline (LEDGER #18f) is now relevant: this entry is a worked example. A future entry should probably extract the pattern observed here ("rapid same-session lifecycle traversal when each state's output directly feeds the next") into the discipline's body.

### Verdict for state advancement

🔨 implemented — the migration is done, the format change is on disk, the slash command writes the new shape, the LEDGER points at the new locations, the verification grep returns clean. **Ready for 💎 value-proved** once a future entry actually uses the folder-as-entry shape to carry supporting artifacts (the agentic-engineering-reference-library entry, LEDGER #18b, is the immediate test case — its `temporary/` artifacts can now move into its entry folder as the shape was built to enable).

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
