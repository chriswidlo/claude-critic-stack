# State-table honesty discipline — when does "descriptive" become misleading?

| Field | Value |
|---|---|
| 📌 **title** | State-table honesty discipline — when does "descriptive" become misleading? |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | In session `2026-04-26-format-only-state-transition-gate`, the orchestrator advanced the format-only-state-transition-gate entry from `🌱 created` through `🔬 spiked` and `⚙️ run-through-repo` — three states — in roughly 30 minutes, on the same day the entry was created. The README explicitly permits this ("the lifecycle is descriptive, not prescriptive ... fill in both dates honestly"). But visually, an entry whose state table shows three filled cells looks like an entry with a long lifecycle, when in reality everything happened in one session. **Where is the line between "descriptive" and "misleading-by-compression"?** |
| 💡 **essence** | The state lifecycle was designed for entries that mature *over time* — a 🔬 spiked done in week 1, a 📋 prepared in week 3, a 🔨 implemented in week 8. When all transitions happen in one session, the state column compresses time-spread events into a single date and loses the signal it was supposed to carry ("how long has this idea been brewing"). The discipline question: should rapid same-session transitions be marked differently? Or should the state table be supplemented with something that preserves temporal structure? |
| 🚀 **upgrade** | The state column regains its signal when entries mature genuinely over time. The lab gains a vocabulary for "this entry advanced rapidly through states because the work was done in one session" vs "this entry has been on a multi-month journey." Without this discipline, every entry will end up looking like every other entry once the dates are filled — the visual progression flattens. |
| 🏷️ **tags** | lab, lifecycle, state-table, honesty, time-compression |
| 🔗 **relates_to** | 2026-04-26-format-only-state-transition-gate, 2026-04-26-workflow-overdesigns-when-told-to-underdesign |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The observation](#the-observation)
- [What "descriptive but misleading" looks like in practice](#what-descriptive-but-misleading-looks-like-in-practice)
- [Three possible disciplines](#three-possible-disciplines)
- [Why this is normal, not no-brainer](#why-this-is-normal-not-no-brainer)
- [Open questions](#open-questions)

## The observation

The format-only state-transition gate entry exists today with this state table:

```
| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | 2026-04-26 | — | — | 2026-04-26 | — | — | — |
```

Three filled cells, all the same date. A reader scanning the LEDGER for "entries that have made progress" might infer this entry is further along than it is. In reality:
- 🌱 was filled when the entry was first written (10am-ish).
- 🔬 was filled after a spike script ran successfully against three real entries (1pm-ish).
- ⚙️ was filled because the entry was put through the 12-step workflow (11am–12pm).

All in one ~3-hour stretch. The state column compresses that 3-hour stretch to a single date, identical to the entry's creation date. The visual signal ("how mature is this idea") is lost.

## What "descriptive but misleading" looks like in practice

Honest descriptive marking would say: *"these three states were reached today; the entry has not had time to accrue value or face revision."* The current state table cannot say that.

If many entries get rapidly advanced this way (e.g., every entry that gets a workflow run on the day it's created instantly gains three filled cells), the state column becomes vestigial — every recent entry looks "advanced," every old entry looks "advanced," the column carries no signal.

The lab's design intent was that the state column would scan-from-across-the-room as a maturity gradient. Rapid same-session advancement defeats that intent without anyone violating the explicit rule.

## Three possible disciplines

**A. Time-floor on advancement.** A state cannot be advanced within N hours (or N days) of the prior state. Mechanical to enforce; respects the "lifecycle is for time-spread events" intent. Cost: arbitrary threshold; over-restrictive when work genuinely is rapid.

**B. Two-color marking.** Same-session advancement uses a different visual marker (a `*` next to the date, or italic, or a separate row). Multi-session advancement uses the plain date. Cost: README edit; visual complexity; arbitrary "what counts as one session."

**C. Augment with a brief temporal note.** No structural change to the state table; instead, when an entry advances multiple states in one session, the body should include an `## Update history` section summarizing the rapid advancement and *why*. The format-only-state-transition-gate entry already does this informally (the blockquote under the state table). Formalize it as a convention.

C is cheapest and preserves the state table's existing shape. A and B add structure that may not justify its cost.

## Why this is normal, not no-brainer

- The discipline is not obvious — there's a real choice between A, B, and C, and the right answer probably depends on whether rapid same-session advancement is *common* or *exceptional* in the lab's evolved use.
- The discipline interacts with the format-only state-transition gate (which currently checks format, not temporal honesty).
- Validating the discipline requires the lab to run for some time so the actual frequency of rapid advancement becomes visible. Currently we have one data point (this very entry); not enough.
- The cheapest version (C) is ~30 minutes of README edit + a one-paragraph convention. Real but bounded.

## Open questions

- Is rapid advancement actually common, or is it just visible because we noticed it once? Need more data points.
- Should the format-only gate eventually check temporal-honesty (refuse advancement within N hours of prior state)? Or is that scope creep into idea evaluation that the gate explicitly refuses?
- Does the LEDGER's pickup-rank already implicitly down-weight entries that advanced rapidly (operator-judgment), or is the maturity signal of the state column genuinely lost?
- If discipline C is adopted (`## Update history` for multi-state-in-one-session entries), should the format-only gate look for it before allowing the second same-session advancement?
