# Two-question disambiguation in the classifier (`blockers:` stanza)

| Field | Value |
|---|---|
| 📌 **title** | Two-question disambiguation in the classifier (`blockers:` stanza) |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective: *"I conflated two different user questions. You asked (a) 'what's the best research approach' and (b) 'how do I use MCPs, plugins, slash commands.' Those are different questions: one is research-quality, the other is 'I want to learn the agent stack.' Trying to satisfy both with one architecture is why every plan kept bloating. I should have disambiguated at step 1."* |
| 💡 **essence** | The classifier currently emits one primary label and an alternative classification. It does not emit "this looks like two questions" or "missing context blocks classification." Add a `blockers:` stanza and an `ambiguous-scope:` flag so questions that contain multiple decisions, or that lack required context, are surfaced before Step 2 reframes them. |
| 🚀 **upgrade** | The conflated-questions failure mode that led to "every plan kept bloating" gets caught at Step 1 instead of Step 12. Questions get answered as posed, not as the orchestrator's first-guess interpretation. The classifier becomes a real disambiguation layer rather than a default-pass-through. |
| 🏷️ **tags** | classifier, classification, ambiguity, methodology |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The new classifier outputs](#the-new-classifier-outputs)
- [Workflow integration](#workflow-integration)
- [Why this is normal, not no-brainer](#why-this-is-normal-not-no-brainer)

## The new classifier outputs

Two new stanzas added to the classifier's output format:

**`ambiguous-scope:`** — set when the question appears to contain multiple decisions or framings that should be answered separately. Format:

```
ambiguous-scope: yes
candidates:
  - <one-line summary of question A>
  - <one-line summary of question B>
recommended-action: <"split into two sessions" | "ask user which to address first" | "answer both with named separation">
```

**`blockers:`** — set when classification surfaces missing context that prevents proceeding. Format:

```
blockers:
  - severity: high | med | low
    description: <one-line description of what's missing>
    suggested-question: <one-line question to user that would unblock>
```

`high` blockers force a Step 1.5 surface-to-user before Step 2 proceeds. `med` and `low` blockers are noted in `requirement.md` for the orchestrator to weigh.

## Workflow integration

CLAUDE.md gains: between Step 1 (classification) and Step 2 (reframe):

> **1.5. Blocker check.** If the classifier emitted `blockers:` with any `severity: high` entries, the orchestrator must surface these to the user before reframing. Do not proceed to Step 2 until the user either answers the suggested question or explicitly says "proceed without that context."
> 
> If the classifier emitted `ambiguous-scope: yes`, the orchestrator must surface the candidate questions to the user and confirm which to address before proceeding.

Pairs naturally with Hook 3 from the "hard gates as harness hooks" entry — that hook automates the blocker-surfacing trigger.

## Why this is normal, not no-brainer

- The classifier prompt needs real redesign, not just an append. The classifier currently does six things; adding two more outputs without diluting the others requires careful prompt engineering.
- The schema for `blockers:` and `ambiguous-scope:` needs to be precise enough that the workflow can trigger on it deterministically.
- The CLAUDE.md addition needs to spell out what "user surface" looks like when a blocker is high — does the orchestrator pause and ask? Does it produce a partial requirement.md with the question raised?
- False positives are a real risk: a classifier that flags everything as ambiguous adds friction without value.

Several hours of design plus testing across varied questions. Real but bounded — normal tier.
