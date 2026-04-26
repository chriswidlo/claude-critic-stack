# Experiment report — format-only state-transition gate spike

**Date:** 2026-04-26
**Duration:** ~25 minutes from "let's run it" to "report written"
**Constraints honored:**
- Only `upgrades/` files modified in the repo (the schema table in README).
- Prototype script lives in `.claude/session-artifacts/` (ephemeral, not a repo file).
- No git operations in the script (deferred until git strategy lands).
- No changes to CLAUDE.md, `.claude/commands/`, settings.json, or any other repo-shared infra.

## What was built

1. **Schema table** added to `upgrades/README.md` (~15 lines) under §"The state lifecycle". One row per non-`🌱-created` state, naming required body element + tolerant regex. Carries an HTML comment marker noting it is machine-read.
2. **Prototype script** at `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py` (~110 lines Python). Parses the README schema, reads an entry, detects current state from rightmost-filled column, checks regex against entry body, prints a warning report. **Read-only.**

The slash-command integration (`/upgrade advance`) was deliberately deferred — that requires editing `.claude/commands/upgrade.md` which is out of scope per the user's "no repo files" constraint.

## Test runs (all <2ms)

| # | Entry | Requested state | Expected | Actual | Verdict |
|---|---|---|---|---|---|
| 1 | rnd-lab | 💎 value-proved | WARN — no evidence heading | ✗ WARN, named missing element, suggested example headings | **correct** |
| 2 | format-only-state-transition-gate (this entry, before spike section added) | 🔬 spiked | WARN — no spike heading yet | ✗ WARN, named missing element, suggested example headings | **correct** |
| 3 | rnd-lab | 🔨 implemented | WARN — no SHA / `implemented_by` | ✗ WARN, named missing element | **correct** |
| 4 | rnd-lab | ⚙️ run-through-repo | WARN — entry was not run through workflow | ✓ PASS (matched `2026-04-26-subagent-claimed-writes-not-on-disk` in `relates_to:`) | **FALSE POSITIVE** |
| 5 | format-only-state-transition-gate | ⚙️ run-through-repo | PASS — entry IS being run through workflow now | ✓ PASS (matched same `relates_to:` reference) | **right answer for wrong reason** |

## Findings

### Finding 1 — Bug in markdown-table parsing (caught and fixed in spike)

The schema table's regex column contains `\|` (escaped pipe) for markdown rendering. The parser's naive `split("|")` shredded those rows. Result: 5 of 7 schema rows were silently dropped on first run. The script reported `Schema covers: ['✅ accepted', '⚙️ run-through-repo']` — only the two rows whose regex contained no pipes survived.

**Fix:** split on `(?<!\\)\|` (negative lookbehind), then `replace(r"\|", "|")` to restore the regex content. ~5 minutes.

**Lesson for productionization:** any script that parses markdown tables in this repo needs to handle backslash-escaped pipes. Worth a small note in the eventual GIT.md or constitutional-layer doc.

### Finding 2 — Regex specificity gap on `⚙️ run-through-repo` (real flaw, not yet fixed)

The regex `\d{4}-\d{2}-\d{2}-[a-z0-9-]+` correctly matches session-id strings, but it matches them **anywhere in the entry body** — including in `relates_to:` cross-references to other entries' session ids. Test 4 demonstrates this with rnd-lab: that entry was never run through the workflow, but its body contains a `relates_to:` reference to a session-id-shaped slug, so the gate falsely passes.

**This is the most important finding.** It validates the architecture critic's loop-1 invariant #2: *"body-section presence implies body-section truth — grep cannot tell coincidental SHA from load-bearing one."* The same class of bug is latent for `🔨 implemented` (a coincidental 7+ hex chars would falsely pass — though no entry currently has one).

**Possible fixes** (none ideal, all costlier than the regex they replace):
- Require the session-id to appear *under* a heading matching `/workflow run|synthesis/i` (compound condition — needs parser extension).
- Require the session-id to match a path that exists in `.claude/session-artifacts/`. Cheap shell call; couples the gate to filesystem state. Honest because that's what `⚙️ run-through-repo` actually means.
- Accept the false positive and rely on operator judgment when the gate passes (warning-only posture means false positives are friction, not corruption — but PASSES with no warning are the silent ones).

**Recommendation:** when productionized, switch `⚙️ run-through-repo` to the second option (verify the session-id directory exists). The other states' regexes are safer because the things they look for (`## Spike` heading, `accepted by` line, git SHA, `## Plan` heading) are less likely to appear coincidentally.

### Finding 3 — The tightened `💎 value-proved` regex worked

I noticed *before running* that the naive regex `value|evidence|outcome` would falsely match the rnd-lab heading "Why organize by value-tier." Tightened to `value (proved|evidence)|outcome|demonstrated` before the first run; Test 1 confirmed the tightening prevented the false positive. This is direct evidence of the schema-in-README pattern working: I could see the regex, predict the false positive, and tune it in one place — no script edit, no second source of truth.

### Finding 4 — Warning messages are actionable

Each warning names the missing element with the regex it looked for and example headings the operator could add. Sample (Test 2):

```
Schema for 🔬 spiked (from upgrades/README.md):
  element: A heading naming the spike work (e.g. `## Spike`, `## What I tried`, `## Probe`).
  regex:   ^#+\s+.*(spike|tried|probe|explored)

  ✗ not found
```

The operator knows exactly what to add and where to look (the README's schema table) if they disagree with the requirement. No vague "missing required element" — there's a regex they can read and tune.

### Finding 5 — Speed is fine

Each check runs in 1–2ms. Even with READMEs 10x larger this would not become a friction point. The "<30 seconds" target from the synthesis is met by three orders of magnitude.

## Uncertainties retired vs uncertainties remaining

From the synthesis's named uncertainties:

- **#1 (operator/AI invocation rate):** *Not addressed by spike.* This needs real ongoing usage; can only be measured after productionization.
- **#2 (schema correctness):** *Partly retired.* The first-pass schema is roughly right for 4 of 7 states; `⚙️ run-through-repo` needs the directory-existence fix; the others (🔬, 📋, 🔨, 💎, 🏁) work as intended on the first try. Tunability via README-edit was demonstrated to work.
- **#3 (warning carries enough signal to be acted on):** *Partly retired.* Output is specific and actionable. Whether AI sessions actually heed it can only be measured after productionization.
- **#4 (subcommand factoring):** *Not addressed.* Spike used a standalone script, not a slash-command subcommand.
- **#5 (README-as-machine-readable survives revisions):** *Partly retired.* Loud failure on the first run (zero rows parsed — wait, actually it parsed *some* rows silently, which is worse than loud failure — schema parser should error if any row in a table that matched the section header fails to parse). Worth fixing in productionization.

## What this spike validates

1. **The schema-in-README pattern is workable.** Markdown-table-as-config is parseable, tunable in one place, and surfaces immediately when the schema is wrong.
2. **Warning-only is responsive on day 1.** A 25-minute spike produced something the operator can run against any entry and get a usable answer.
3. **The 8-state lifecycle survives the schema definition step** — designing the regexes did not surface "wait, this state doesn't make sense" for any of them. (One soft signal: `📋 prepared` and `✅ accepted` have similar enough requirements that the frame-challenger's collapse-to-3-5 challenge has some teeth in practice. Not load-bearing yet.)

## What this spike falsifies

Nothing in the candidate v2 design was falsified. The closest was finding #2 — the `⚙️ run-through-repo` regex is too loose — but that is a tunable in the README, not a structural problem.

## Recommended next steps (not committed work)

1. **Tighten `⚙️ run-through-repo` regex** to verify the session-id corresponds to a real directory. Edit the README; the gate updates.
2. **Productionize as `/upgrade advance` subcommand** when slash-command infra changes are in scope (out of scope today per user constraint).
3. **Add silent-row-drop detection** to the schema parser: if a row in the schema table fails to parse, error loudly rather than skip silently. (Loop-2 architecture critic's point about loud failure over silent drift.)
4. **Add the `--apply` flag** with the operations critic's pre-merge condition (refuse on dirty tree OR show `git diff --stat`) **after** git strategy lands.
5. **Add invocation logging** (operations critic's optional improvement) so silent disuse becomes detectable.

## Files touched in this experiment

- `upgrades/README.md` — added §"Required body elements per state" (~15 lines + HTML marker comment).
- `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/check-transition.py` — prototype script (~110 lines).
- `.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/experiment-report.md` — this file.

(About to also update `upgrades/normal/2026-04-26-format-only-state-transition-gate.md` to add a `## Spike` section documenting this experiment and advance the state to `🔬 spiked` — demonstrating the gate's own state advancement.)
