# Critic — operations lens

> Orchestrator-authored stand-in.

## Frame-level objection
Manual orchestrator authorship of the ledger has a known operational failure mode: **end-of-session context exhaustion**. By the time step 12 synthesis is written, the orchestrator's context window has typically absorbed a session's worth of content. Step 13 happens at the moment the orchestrator is *least* reliable. Without hook automation, the modal failure isn't "wallpaper" (outside-view's prediction) — it's "ledger.md not written at all because the orchestrator forgot or ran out of room to format the table."

This makes the entry's dependency note on #14 more load-bearing than the candidate admits. The candidate says "explicit dependency note for entry #14"; operations says: **plan for #14 not landing on time and ship a fallback** — a tiny shell script `bin/ledger-from-session.sh <session-id>` that tallies counts from the session directory. Manual paste-and-fill remains the doc'd default; the script is a recoverable-from-context-loss escape hatch.

## Weakest link
**Division by zero.** A `quick take` bypass session has 0 decisions and 0 most-other-things. The candidate says "skip the ledger for bypassed sessions" — but that decision must be encoded somewhere the orchestrator will actually read. If it's only in the candidate.md, the next session won't know.

## Invariants at risk
- **Reproducibility.** If counts come from "orchestrator counts files in session dir" the count depends on *when* the orchestrator counts (before or after writing ledger.md itself counts as one file?). Define: *counts are taken before ledger.md is written*. Document this.
- **Failure visibility.** If ledger.md is missing from a session, what tells anyone? Currently nothing. Suggest: a sentence in [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md) saying "absence of ledger.md from a non-bypassed session is a workflow defect."

## Specific actionable pre-merge requirements
1. **Document the bypass cases explicitly** in the schema section: `quick take` → no ledger; pure factual question → no ledger; veto-stopped session → ledger required (loops counted, decisions=0, ratios=N/A).
2. **Define the count-taking moment.** "Counts are taken just before ledger.md is written. Ledger.md does not count itself."
3. **Add a one-line CLAUDE.md instruction:** *"If session was bypassed (quick take), no ledger is written. Otherwise ledger is required; absence is a workflow defect."*
4. **Optional but cheap:** the `bin/ledger-from-session.sh` fallback script. ~30 lines of bash, counts files and greps decision-log.md. Documented as "use if orchestrator needs assistance assembling counts."

## Operations symmetry note
Like the format-only-state-transition-gate entry, this is mostly **fails-to-safe**: a missing ledger doesn't break the workflow; the synthesis still ships. The downside is silent — no signal is generated. The bypass-case documentation above prevents the silent-failure mode from being mistaken for a successful run.

## Verdict
**rework** — pre-merge requirements 1–3 are non-negotiable from operations; #4 is recommended but not required.
