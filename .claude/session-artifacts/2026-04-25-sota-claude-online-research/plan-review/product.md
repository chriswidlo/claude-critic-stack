# Product lens — plan v3 review

## Frame-level objection

Plan's frame: "triage by self-reported volume." Product-lens load-bearing question is not *how much* — it is **what contract the tool makes about output trustworthiness.** v3 still ducks that.

Regime 1: "use Anthropic Research, attach a mental disclaimer." A mental disclaimer is not a product surface; it is the orchestrator off-loading the trust contract onto the user's working memory. The product question — "when Claude hands me a research result, what am I allowed to assume?" — gets the same answer as if the orchestrator had said nothing: *figure it out yourself.* That is a referral, not a SOTA recommendation.

## User-visible consequence

User asked "what is the SOTA way to do online research with Claude." The product they receive in regime 1 (the path the plan says is "almost certainly" theirs) is: a sentence telling them to open a different surface and remember a disclaimer. No Claude-Code-side artifact, command, hook, or output-shape change. **Product-shape delta from "do nothing": zero.**

## Commitments implied

- Anthropic Research's output format, citation behavior, and existence — without owning any. Format change → silent regime-3 breakage.
- "30-second self-survey" commits user to a self-classification ritual with no follow-up surface.
- "Load-bearing = irreversible within 24h" is undefined at edges (is "I sent this to my team" reversible?), no examples shipped.

## Migration burden

Named clients of this contract:
- **The user at query 50.** Will not open the checklist. By query 5 it's muscle memory or skipped; by query 50 skipped. No mechanism makes the checklist *present at query time.*
- **The regime-3 copy-paste dance.** Open Anthropic Research tab → run query → wait → copy output → save to file → switch to Claude Code → `/verify-research <path>` → wait again → read second report. **Step 4 (save-to-file with a path the slash command can find) is where this dies.** Every product requiring manual artifact-shuttling between two surfaces loses to the surface that does it inline.
- **Future-self auditing an old decision.** Snapshots on disk, no index, no command to look up "what did I verify on 2026-03-12," no link from decision back to its snapshot.

## Affordances

**Better:** regime 3 ships one real thing (verify slash command + snapshots). Snapshot move is a good answer to architecture critic.

**Worse / pruned:**
- No mode chooser. Prior critique flagged in loop 1 and loop 2; v3's response is "the user runs a 30-second mental survey once" — homework with no UI.
- No in-product disclaimer surface. Mental disclaimer is the worst possible affordance: invisible at moment of consumption, dependent on discipline, untestable.
- No "I don't know" branch. Most honest answer most users give to the volume question is "I don't know" and the plan gives them no fallback.

## Specific tests

- **Is regime 1 = "do nothing" in product shape?** Yes. Only difference: user has been told, in prose, that hosted Deep Research exists. If they already knew, plan delivered nothing. **Orchestrator under-promising to look humble; under-promise indistinguishable from non-answer.**
- **Does "honest about not solving" buy credibility?** Partly. Snapshot vs. producer-time gap is real intellectual honesty. But "honest I'm not solving the mode-chooser, the in-product disclaimer, the checklist-presence-at-query-time, or the copy-paste friction" is the dodge in different clothing — those are the things the user actually needed.
- **Checklist opened at query 50?** No. Plan ships no surface mechanism. A `/research-checklist` slash command that prints the four steps would cost 5 minutes and convert checklist from aspirational to present. Its absence is a product failure.
- **Copy-paste workflow survives users?** Doubt it. Should at minimum specify file location, naming convention, and ideally a `/research <query>` wrapper that runs the hosted call (if API-accessible) or templates the save path. As written, step 4 friction kills adoption.

## Verdict: rework.

Approve if: (a) regime 1 ships *one* in-product affordance — minimum a `/research` slash command that runs the hosted call and appends the disclaimer to the output, so the contract is in the artifact and not in the user's head; (b) regime 2's checklist becomes a slash command that prints at query time, not a file the user is asked to remember; (c) regime 3 names the copy-paste friction explicitly and either templates it or admits the workflow has a known abandonment point at step 4.
