# Hard gates as harness hooks

| Field | Value |
|---|---|
| 📌 **title** | Hard gates as harness hooks |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | CLAUDE.md says "non-negotiable" four times when describing workflow gates — the loop cap, the Step-9 precondition gate (scope-map.md and challenges.md must exist before generation), the classifier-blocker surfacer. Zero of these gates exist in `settings.json` as hooks. The orchestrator enforces them against itself. The retrospective: *"a gate the orchestrator enforces against itself is not a gate."* |
| 💡 **essence** | Move three gates from prose enforcement to harness enforcement via Claude Code hooks. Each is a small `PreToolUse` hook that reads session-artifact state and either allows or blocks the next tool call. The hooks do not enforce content — they enforce *that the workflow has reached the right state* before the next step proceeds. |
| 🚀 **upgrade** | "Non-negotiable" actually becomes non-negotiable. The two-loop critic-panel cap stops being violatable by a model that decides this case is special. The Step-9 generator stops running against missing artifacts. The classifier's "blockers" stanza (when added) actually blocks. |
| 🏷️ **tags** | harness, hooks, enforcement, gates, settings |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The three hooks](#the-three-hooks)
- [Why this is normal, not no-brainer](#why-this-is-normal-not-no-brainer)
- [Risks](#risks)

## The three hooks

**Hook 1 — Step-9 precondition gate.** `PreToolUse` matching `Write` to paths containing `candidate.md` or `synthesis.md`. Reads `.claude/session-artifacts/<id>/`; denies if `scope-map.md` or `challenges.md` is missing. Env-var bypass: `CRITIC_STACK_SKIP_GATE=1`.

**Hook 2 — Loop-cap counter.** `PreToolUse` matching `Agent` calls to `critic-architecture | critic-operations | critic-product`. Counts `## Revision N` blocks in `frame.md` plus rewrite/replan entries in `decision-log.md`. Denies the third critic-panel call. Same env-var bypass; bypass usage is logged.

**Hook 3 — Classifier-blocker surfacer.** `PostToolUse` matching the `requirement-classifier` Agent. Reads the just-written `requirement.md`, greps for a `blockers:` stanza (when the classifier is updated to emit one — see "two-question disambiguation" entry), and if present, injects a system reminder telling the orchestrator to surface those gaps to the user before Step 2.

## Why this is normal, not no-brainer

The implementation is real engineering, not just documentation:
- Hook scripts must be precise on path-matching to avoid firing on unrelated tool calls.
- The loop counter requires deterministic state extraction from `decision-log.md` (small parsing risk).
- All three need env-var bypasses to prevent locking the session.
- Hook 3 depends on a separate upgrade (classifier blockers stanza) landing first.

Total work: ~3-5 hours of bash + testing. Real value but real effort. Normal-tier.

## Risks

- **A buggy hook can lock the session.** Mitigation: scope hooks narrowly (specific tool, specific path patterns); always include env-var bypass; test in a scratch session before enabling globally.
- **Hooks are silent failures if mis-matched.** A hook that should fire but doesn't (because matcher is wrong) gives false security. Mitigation: log every hook invocation to a debug file during initial rollout; verify hits and misses match expectations.
- **Bypass becomes habit.** If the env-var bypass becomes routinely set, the gate is again nominal. Mitigation: bypass usage is logged to a tracked file; periodic review surfaces over-use.

These risks are why this is normal-tier — the upside is real, and so is the surface area.
