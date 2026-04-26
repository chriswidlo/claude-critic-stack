# The workflow is blind to the lab — CLAUDE.md doesn't know it exists

| Field | Value |
|---|---|
| 📌 **title** | The workflow is blind to the lab — CLAUDE.md doesn't know it exists |
| 🎯 **tier** | 💎 profound |
| 👤 **author** | collaborative (investigation by a parallel session; entry transcribed by orchestrator; surfaced by operator) |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | A parallel session ran a diagnostic after the orchestrator (in another session) repeatedly defaulted to a generic engineering reading of "upgrade" when the operator said "submit as upgrade." Investigation findings: *"CLAUDE.md and AGENTS.md contain zero references to `upgrades/`, the lab, the `/upgrade` command, the four tiers, or the idea-vs-execution distinction. CLAUDE.md is the document that gets auto-loaded into orchestrator context every session. It defines the orchestrator's mental model for what artifacts exist and where things go (`session-artifacts/`, `canon/`, `memory/`). The `upgrades/` lab is invisible from there. An orchestrator following CLAUDE.md exclusively has no scaffolded reason to know the lab exists, much less how it differs from a backlog."* |
| 💡 **essence** | CLAUDE.md treats the orchestrator's only outputs as session-artifacts. But sessions also generate ideas about the workflow itself — exactly what the lab exists to catch. The orchestrator has no instruction to recognize lab-shaped utterances ("submit as upgrade", "we should add", "the workflow could", "I noticed"), no pointer to `upgrades/README.md`, no concept that the lab is a peer-named persistent surface alongside `canon/`, `session-artifacts/`, and `memory/`. The lab sits *beside* the workflow rather than *connected to* it. |
| 🚀 **upgrade** | The workflow becomes a *generator* of lab entries rather than a parallel system. Lab-shaped signal stops evaporating between sessions. The operator's conversational submission ("submit as upgrade") routes to the same disciplined capture as explicit `/upgrade` invocation. The seeing is profound; the implementation is no-brainer (3–5 sentences in CLAUDE.md). |
| 🏷️ **tags** | claude-md, lab, workflow, orchestrator, mental-model, persistent-surfaces, architectural-gap |
| 🔗 **relates_to** | profound/2026-04-26-memory-and-lab-are-the-same-primitive, no-brainer/2026-04-26-rnd-lab |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The investigation](#the-investigation)
- [What's actually missing in CLAUDE.md](#whats-actually-missing-in-claude-md)
- [The deeper insight — workflow as generator, not parallel system](#the-deeper-insight--workflow-as-generator-not-parallel-system)
- [Why the contamination worry is valid — and resolves cleanly](#why-the-contamination-worry-is-valid--and-resolves-cleanly)
- [The minimum viable fix (sketch, not a commitment)](#the-minimum-viable-fix-sketch-not-a-commitment)
- [The README load-ordering observation (secondary)](#the-readme-load-ordering-observation-secondary)
- [Why this is profound, not no-brainer](#why-this-is-profound-not-no-brainer)
- [Open questions](#open-questions)

## The investigation

A parallel session noticed an orchestrator (in yet another session) defaulting to conventional usage of "upgrade" when the operator said "submit as upgrade." The right move would have been to read `upgrades/README.md` to learn what *this* repo means by upgrade. The orchestrator skipped that step — substituted prior of generic engineering usage — and produced output that did not match the lab's discipline.

The investigation traced the failure to two layers:

1. **A self-acknowledged personal failure** — the orchestrator never read `upgrades/README.md`, even though the directory was visible in the repo from session start and the `/upgrade` slash command's description (loaded into available skills) said *"Capture a profound, novel, or creative idea for upgrading this AI system into the `upgrades/` R&D lab."* The word "idea" appeared twice in that description; the orchestrator still defaulted to the conventional reading.

2. **A structural gap in CLAUDE.md** — confirmed by grep. CLAUDE.md and AGENTS.md contain zero references to `upgrades/`, the lab, the `/upgrade` command, the four tiers, or the idea-vs-execution distinction. CLAUDE.md is what gets auto-loaded into orchestrator context every session. It governs the 12-step workflow, the bypasses, the things-you-must-not-do. It defines the orchestrator's mental model for *what artifacts exist and where things go*: `session-artifacts/`, `canon/`, `memory/`. The lab is not on that list. An orchestrator following CLAUDE.md exclusively has no scaffolded reason to know the lab exists.

The slash command `/upgrade` partly compensates — its instructions tell the agent to read `upgrades/README.md` first. But that path only fires on *explicit slash invocation*. **Conversational** "submit as upgrade" (the actual phrase the operator used multiple times in another session) doesn't route through the command, doesn't trigger the read, and lands in default agent reasoning where "upgrade" carries its conventional connotation.

## What's actually missing in CLAUDE.md

Comparing CLAUDE.md's coverage of persistent surfaces:

| Surface | Mentioned in CLAUDE.md? | Pointer to its README? |
|---|---|---|
| `session-artifacts/<id>/` | yes — extensively, central to the 12-step workflow | n/a (defined in CLAUDE.md itself) |
| `canon/corpus/` | yes — librarian-first rule, anti-confirmation discipline | yes (canon-librarian agent) |
| `memory/` (auto-memory) | yes — anti-anchoring discipline references it | yes (auto-memory section in system prompt) |
| `upgrades/` (the lab) | **no** | **no** |

The lab is the only major persistent surface in this repo that has zero CLAUDE.md mention. That asymmetry is the gap.

## The deeper insight — workflow as generator, not parallel system

The other session's framing — *"the lab sits beside the workflow rather than connected to it"* — names something deeper than a missing reference. It names an architectural relationship the repo has not explicitly chosen.

In the current setup, the workflow runs (12 steps, produces synthesis), and *separately*, the operator (or AI) might decide to capture lab entries. The two systems are *parallel*. The connector is the operator's deliberate act.

Every workflow run produces metacognitive signal: *"the workflow could do X better," "I noticed Y about my own reasoning," "this case suggests Z is wrong about the panel."* That signal is exactly what the lab exists to catch. Currently, it evaporates unless the operator explicitly says "make this an upgrade." The workflow is not aware that it is *generating* potential lab entries continuously.

If CLAUDE.md instructed the orchestrator to *recognize* lab-shaped utterances mid-session, the workflow becomes a **generator of lab inputs**, not just a parallel system the operator manually feeds. That is the architectural reframe. The fix is small (a few sentences); the consequence is structural (the lab is fed by the workflow's own metacognition, not just by the operator's discipline).

## Why the contamination worry is valid — and resolves cleanly

The operator's stated worry: *"I don't want to contaminate main functionality of repo with useless for its executions data."* CLAUDE.md is the workflow's contract; bloating it with lab pedagogy (how to write entries, what tier rubric means, what state lifecycle requires) would dilute its clarity. That worry is correct and load-bearing.

The resolution is the same pattern CLAUDE.md already uses for `canon/` and `memory/`: **mention the surface by name as a concept; do not teach it.** Pedagogy belongs in `upgrades/README.md` where it already lives. CLAUDE.md just needs to know the lab is a fourth peer-named persistent surface and one bullet about when to route to it.

The line being walked: enough mention that the orchestrator doesn't default to conventional usage; not so much that CLAUDE.md grows a lab tutorial. ~3–5 sentences total.

## The minimum viable fix (sketch, not a commitment)

Two additive changes to CLAUDE.md:

1. **A "What lives in this repo" mini-section** (or addition to a section that already names persistent surfaces). One sentence per surface; pointer for detail. The lab joins `canon/`, `session-artifacts/`, `memory/` as a fourth named surface: *"`upgrades/` — the R&D lab. Captures profound, novel, or creative ideas about elevating this AI system. Organized by value-tier (profound / outlandish / no-brainer / normal). Pedagogy in `upgrades/README.md`."*

2. **A bullet under "Things you must do" or similar.** *"If a lab-shaped utterance appears in a session — operator says 'submit as upgrade,' or anyone says 'we should add,' 'the workflow could,' 'I noticed' about something repo-architectural — surface it to the operator and offer `/upgrade` capture. Definition of lab-shaped lives in `upgrades/README.md`."*

The two together are ~5 sentences. CLAUDE.md grows by <2% in length. The lab becomes a known concept. The conversational route into the lab connects to the same discipline as the slash-command route.

This is sketch, not commitment. The actual implementation can iterate — and probably should be itself an upgrade entry (no-brainer tier) when ready.

## The README load-ordering observation (secondary)

A smaller, separate observation from the same investigation: `upgrades/README.md`'s opening paragraph emphasizes *"elevate the functionality, effectiveness, and accuracy of this repo's AI system"* — language that, to a fast reader under context pressure, sounds executable. The hard rule (idea, not mechanism) is positioned several scrolls down inside the tier-organization section.

A future agent who skims the README without scrolling can leave with the conventional connotation reinforced. Quick fix: one early sentence in the opening paragraph naming the idea-vs-execution distinction, OR move the hard rule to the very top of "How entries are organized."

Not a defect — a load-ordering observation. The CLAUDE.md fix is more important; the README tweak is ~5 minutes of polish. Best landed in the same swing.

## Why this is profound, not no-brainer

The implementation is genuinely no-brainer (3–5 sentences in CLAUDE.md, plus a small README polish). The reason this entry sits in `profound/` is the *seeing*, not the doing:

- It names an asymmetry in CLAUDE.md's coverage (three persistent surfaces visible, one invisible) that wasn't articulated until the parallel session ran the diagnostic.
- It surfaces an architectural reframe: **the workflow can be a generator of lab entries**, not just a parallel system. That reframe shifts how every future workflow run can be evaluated ("did this session surface lab-shaped signal that we captured, or did it evaporate?").
- It's a worked example of a class of failure — *"the orchestrator's mental model is shaped by what CLAUDE.md mentions, and what CLAUDE.md doesn't mention is invisible"* — that probably has other instances. (What else is invisible to the orchestrator because CLAUDE.md is silent on it?)

The entry's value is independent of whether the fix ever ships. The reframe is the upgrade.

## Open questions

- **What other persistent surfaces is CLAUDE.md silent on?** The diagnostic found one (the lab). The class of failure (CLAUDE.md = orchestrator's mental model boundary) suggests there may be others. Worth a one-time audit: every directory at repo root that holds operator-meaningful state should be tested against "is it mentioned in CLAUDE.md?"
- **What counts as a "lab-shaped utterance"?** The investigation listed three triggers: "submit as upgrade," "we should add," "the workflow could." There are probably more ("I noticed," "this is interesting," "we keep doing X"). A small enumeration would help the orchestrator recognize them; too broad an enumeration would cause noise. The right boundary is empirical — needs sessions to surface it.
- **Mid-session surfacing or end-of-session batching?** Catching lab-shaped utterances *as they appear* maximizes capture but adds in-flight conversational tax. Batching at synthesis loses some signal but is cleaner. Probably mid-session for explicit "submit as upgrade" (high signal, low cost); end-of-session for ambient "we should add" (lower signal, higher cost). Open.
- **If CLAUDE.md becomes the lab's connector, what discipline prevents it from growing into a lab tutorial?** Some convention like *"CLAUDE.md mentions; the README teaches"* would help. Worth naming explicitly somewhere — probably in `MODULES.md` if/when the constitutional layer (LEDGER #4) lands.
- **Does this gap exist in the inverse direction too?** Does `upgrades/README.md` mention CLAUDE.md? (It does — once, in the description of the workflow as the lab's parallel system.) Is that mention sufficient, or does the lab also need a stronger pointer back to CLAUDE.md? Probably the asymmetry is correct (CLAUDE.md is auto-loaded; README is read on demand) but worth checking.
- **Is this entry's framing — "generator vs parallel system" — too clever?** It's an attractive reframe. It might also be a frame that retroactively valorizes a small CLAUDE.md edit. The conservative version of this entry is just *"add the lab to CLAUDE.md's named surfaces."* The reframe is the seeing; the fix is the doing. Holding the reframe lightly until more sessions confirm it.
