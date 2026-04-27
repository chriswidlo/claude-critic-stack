# Tighten `⚙️ run-through-repo` regex to verify the session-id directory exists

| Field | Value |
|---|---|
| 📌 **title** | Tighten `⚙️ run-through-repo` regex to verify the session-id directory exists |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | ai |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Spike of the format-only state-transition gate (session `2026-04-26-format-only-state-transition-gate`, experiment-report.md) ran the gate against the rnd-lab entry requesting `⚙️ run-through-repo`. The gate falsely passed: the regex `\d{4}-\d{2}-\d{2}-[a-z0-9-]+` matched a session-id-shaped string in the `relates_to:` field — but rnd-lab was never put through the workflow. **A documented false positive** that would silently bless drift. |
| 💡 **essence** | The regex should not just match a session-id-shaped string; it should require the matched string to correspond to a real `.claude/session-artifacts/<slug>/` directory. The check is a cheap shell call (the existence of a directory). Honest semantics: `⚙️ run-through-repo` literally means "this entry was put through the workflow, and the workflow's session artifacts are on disk." |
| 🚀 **upgrade** | Closes the most concrete false-positive surfaced in the spike. Eliminates the class of failure where `relates_to:` cross-references to other entries' session ids accidentally pass the gate. Makes `⚙️ run-through-repo` semantically anchored to a filesystem fact, not a regex match. |
| 🏷️ **tags** | gate, regex, false-positive, schema, run-through-repo |
| 🔗 **relates_to** | 2026-04-26-format-only-state-transition-gate |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The change](#the-change)
- [Why this is a regex problem masquerading as a directory-existence problem](#why-this-is-a-regex-problem-masquerading-as-a-directory-existence-problem)
- [Why no-brainer](#why-no-brainer)

## The change

In `upgrades/README.md` §"Required body elements per state," the `⚙️ run-through-repo` row's regex column is currently:

```
\d{4}-\d{2}-\d{2}-[a-z0-9-]+
```

Tightening cannot be done in pure regex (regex is stateless; it cannot ask the filesystem). Two paths:

**Path A — hybrid check in the script.** The schema cell carries the regex AND a marker that the matched string must be checked against `.claude/session-artifacts/<match>/`. Convention: append `+exists` to the regex column to signal "matches must correspond to existing directories." The script splits on `+` and runs the post-match existence check. README stays the source of truth; one parser extension.

**Path B — replace the requirement entirely.** The state's required element becomes "a heading like `## Workflow run` containing a session-id reference." The regex matches `^#+\s+.*workflow run.*` and the script then extracts the session-id and checks directory existence. More structural, but requires re-reviewing every entry to ensure the heading exists.

Path A is cheaper and preserves the schema's regex-only shape for other states. Recommended.

## Why this is a regex problem masquerading as a directory-existence problem

The deeper issue: regexes can match patterns but cannot check facts. `⚙️ run-through-repo` is a *fact* about the world (a session directory exists). Encoding it as a regex was a shortcut. The shortcut works for states whose required element is genuinely a body-shape (`🔬 spiked` requires a heading; the heading either exists or doesn't). It breaks for states whose required element is a fact about the repo's state (`⚙️ run-through-repo`, `🔨 implemented`).

`🔨 implemented` has the same latent class of bug: a 7+ hex-char string in the body would falsely pass even if it isn't a real commit SHA. Mitigation could be: add `+git-exists` marker that runs `git cat-file -e <sha>` against the matched string. Same parser extension pattern.

This entry is scoped narrowly to `⚙️ run-through-repo`. The `🔨 implemented` extension can be a follow-up if it bites.

## Why no-brainer

- README edit: one column update.
- Script extension: ~10 lines of Python (split on `+exists`, after regex match check `Path('.claude/session-artifacts/' + match.group(0)).exists()`).
- Test against existing entries: the format-only gate entry currently has its `⚙️ run-through-repo` cell filled — re-run the gate after the tightening to confirm it now correctly passes (the session-id `2026-04-26-format-only-state-transition-gate` directory exists).
- Total time: ~20 minutes including testing.
- Closes the most concrete false-positive in the spike.
