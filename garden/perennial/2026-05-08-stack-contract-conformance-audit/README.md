# Stack-contract conformance audit — May 2026 findings

| Field | Value |
|---|---|
| 📌 **title** | Stack-contract conformance audit — May 2026 findings |
| 🎯 **category** | 🌿 perennial |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-08 |
| ⚡ **catalyst** | Operator asked for a full review of the stack ("find things to fix, bugs, dead places and bad practices; consult SOTA"). Three parallel Explore lanes ran (workflow & structure, content hygiene, settings + external best practices), findings were verified against tracked files. The exercise produced an unexpected second-order result: most defects clustered into the exact failure modes the lab's existing *profound* entries had already named in the abstract. The audit is the first systematic empirical evidence for those entries. |
| 💡 **essence** | A snapshot survey of the stack's tracked state against its own documented contract finds **eleven distinct conformance gaps**, three of them novel and eight already named (or partly named) by prior lab entries. The pattern across all eleven is the same one the lab keeps re-discovering from different angles: **a contract enforced only by orchestrator instruction-following drifts silently**. The audit's value is not the punch-list; the punch-list is downstream. The audit's value is empirical pressure on the lab's already-filed-but-still-`created` entries that proposed mechanical enforcement. |
| 🚀 **upgrade** | Two effects, one immediate, one structural. **Immediate:** the eleven findings get a clear path to fix — three new sub-entries for the novel items, advancement evidence for the eight already-filed items, and a small mechanical cleanup pass for the items too trivial to live in the lab. **Structural:** the audit becomes a *recurring* lab artifact (quarterly or after major workflow edits) — a way the stack measures itself against itself instead of waiting for the next session to surface defects ad-hoc. |
| 🏷️ **tags** | audit, conformance, drift, repo-hygiene, evidence, meta |
| 🔗 **relates_to** | workflow-docs-scattered-and-stale, hard-gates-as-harness-hooks, casual-output-is-workflow-unprotected, subagents-claim-writes-not-on-disk, format-only-state-transition-gate, critic-panel-correlated-by-default |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 🩺 verified | 🔖 committed | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-08 | — | — | — | — | — | — | — | — | — |

## Table of contents

- [What this entry is](#what-this-entry-is)
- [Method](#method)
- [The findings — eleven gaps, three classes](#the-findings--eleven-gaps-three-classes)
  - [Class A — novel (no existing entry)](#class-a--novel-no-existing-entry)
  - [Class B — empirical evidence for existing entries](#class-b--empirical-evidence-for-existing-entries)
  - [Class C — too small for the lab (mechanical sweep)](#class-c--too-small-for-the-lab-mechanical-sweep)
- [SOTA gaps surfaced but not filed here](#sota-gaps-surfaced-but-not-filed-here)
- [What this audit reveals about the lab itself](#what-this-audit-reveals-about-the-lab-itself)
- [Proposed graduation path](#proposed-graduation-path)
- [Why this is normal, not no-brainer or profound](#why-this-is-normal-not-no-brainer-or-profound)

---

## What this entry is

This is **not** a backlog of fixes. The lab is explicit that backlogs do not belong here ([upgrades/README.md](upgrades/README.md)). This is an *observation* entry — a dated snapshot of how the stack's tracked state compared to its documented contract on **2026-05-08**, what defects the comparison surfaced, and how those defects map onto the lab's existing thinking. The findings will age. The pattern they expose probably will not.

The entry is filed as `🌿 normal` because the audit's central insight — *that contracts enforced only by instruction-following drift silently* — is **not novel** in this lab. It has been articulated already, from different angles, by several `💎 profound` entries. What is novel is **the empirical evidence**: a population-scale count of contract violations in the live tracked tree, including the canonical exemplar cited from [CLAUDE.md](CLAUDE.md). Empirical evidence supporting an existing insight is creative work but not new conceptual ground; that is normal-tier territory.

## Method

Three Explore lanes ran in parallel, each scoped to a different angle:

- **Lane A — workflow & structure.** Audited [.claude/agents/](.claude/agents/), the 12-step workflow contract in [CLAUDE.md](CLAUDE.md), the path-discipline regime, the `SHADOW_PANEL` / `EXTERNAL_SHADOW` wiring, and recent commit trajectory.
- **Lane B — content hygiene.** Audited [canon/corpus/](canon/corpus/), [upgrades/](upgrades/), and [.claude/session-artifacts/](.claude/session-artifacts/) for completeness, broken refs, drift, and missing artifacts.
- **Lane C — settings + external SOTA.** Read [.claude/settings.json](.claude/settings.json) and the local override; fetched current Anthropic / Claude Code documentation (Subagents, Hooks, Skills, Settings, Building Effective Agents) for cross-reference.

Findings were re-verified directly against tracked files — subagent reports were treated as a starting point, not as ground truth. The full plan record lives outside the repo per path discipline; the verified findings are reproduced inline below.

## The findings — eleven gaps, three classes

### Class A — novel (no existing entry)

These three were not previously named in any lab entry, session-artifact, or tracked plan. They warrant their own dedicated entries (`/upgrade` follow-ups suggested below) so each can graduate the lifecycle independently.

**A1. `outside-view` agent has an unenforceable mandatory rule.**
[.claude/agents/outside-view.md](.claude/agents/outside-view.md):4 grants tools `WebSearch, WebFetch, Read`. Mandatory section #0 in the same file (lines 13–15) says: *"Before any `WebSearch` or `WebFetch`, `Grep` `canon/corpus/` for the authors and works that define this reference class."* The agent **cannot run `Grep`** — it is not in its tool allowlist. The most-cited bias-correction rule in the stack ("canon-first") is structurally unenforceable for `outside-view`: the agent can only `Read` paths it already happens to know about, which silently degrades the rule to "read whatever you remember." [.claude/agents/canon-librarian.md](.claude/agents/canon-librarian.md) deserves the same audit.

**A2. The shared `settings.json` embeds one operator's machine paths.**
[.claude/settings.json](.claude/settings.json):4-6 contains absolute paths (`Read(//Users/krzys/Development/Projects/claude-critic-stack/**)`, same for `Glob` and `Grep`). [CLAUDE.md](CLAUDE.md):7-16 forbids absolute and `~/`-prefixed paths in *any* artifact and explicitly states the rule applies retroactively when editing existing files. The double-slash `//Users/...` form additionally silently no-ops on every other clone — the rules grant nothing on a fresh checkout. [.gitignore](.gitignore):40-42 explicitly distinguishes `settings.json` (tracked, shared) from `settings.local.json` (per-developer override), so there is no escape hatch in calling these "personal" settings.

**A3. Population-scale contract non-compliance in `session-artifacts/`.**
Counted on 2026-05-08, of 22 session subdirectories under [.claude/session-artifacts/](.claude/session-artifacts/):

- **14** lack `synthesis.md` entirely.
- **21** lack `ledger.md` (only `2026-04-27-step13-ledger-impl` has one).
- Of the **8** with `synthesis.md`, **7** are missing the required `Ledger:` final-line citation that [CLAUDE.md](CLAUDE.md) step 12 declares load-bearing.
- Most damning: the canonical exemplar `2026-04-26-format-only-state-transition-gate` — cited in [CLAUDE.md](CLAUDE.md):22 as the worked example of the workflow — does **not** pass its own contract.

The artifacts-README ([.claude/session-artifacts/README.md](.claude/session-artifacts/README.md):94) says explicitly: *"Absence of `ledger.md` from a non-bypassed session is a workflow defect."* But there is **no marker convention distinguishing bypassed sessions from incomplete ones** — a future auditor cannot tell which of the 14 lack synthesis because they were quick-takes, factual answers, or impl-task sessions, versus which lack synthesis because the workflow was abandoned mid-step.

### Class B — empirical evidence for existing entries

These eight findings were already named (in part or in whole) by prior lab entries that have stayed at `🌱 created`. The audit promotes them from *plausible* to *measured* — useful evidence for advancing those entries through the lifecycle.

| # | Finding | Existing entry it evidences |
|---|---|---|
| **B1** | [README.md](README.md):29 still routes readers to the deleted `workflows/architecture-review.md`. | [workflow-docs-scattered-and-stale](upgrades/normal/2026-04-27-workflow-docs-scattered-and-stale/) — line-level evidence already there; this is the same finding, re-confirmed. |
| **B2** | [.gitignore](.gitignore):84-86 allowlists the same nonexistent `workflows/` directory. | Same as B1; sub-piece of the cleanup. |
| **B3** | [README.md](README.md):33 says corpus is gitignored; [.gitignore](.gitignore):57-59 says inventory is tracked, only `source.txt` is excluded. Front-door doc contradicts reality. | Same family as B1 (front-door staleness). |
| **B4** | [README.md](README.md):7-11 describes the Phase-1 three-subagent shape; the stack now ships 14 agents in a 12-step workflow with three-lens critic panel + optional shadow lanes. | Same family as B1. |
| **B5** | The hard gate at step 9 is enforced by orchestrator instruction-following only; A3 above is direct evidence of silent drift. | [hard-gates-as-harness-hooks](upgrades/normal/2026-04-26-hard-gates-as-harness-hooks/) — proposed three concrete hooks; this audit is empirical pressure to advance. |
| **B6** | A3's count of unmarked-bypassed vs incomplete sessions is the same gap [casual-output-is-workflow-unprotected](upgrades/profound/2026-04-26-casual-output-is-workflow-unprotected/) names: casual / impl / off-ramp output is workflow-unprotected and indistinguishable from incomplete-workflow output. | The profound entry; this audit gives it 14 concrete instances. |
| **B7** | A2 is structurally identical to the pattern [subagents-claim-writes-not-on-disk](upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk/) describes — a documented constraint that has no closed-loop verifier. The settings file *claims* path-discipline applies; nothing checks it. | The profound entry, generalised to settings + agent-tool frontmatter. |
| **B8** | [EXTERNAL_SHADOW=1](CLAUDE.md):60 is documented as inert; setting it today silently degrades to no-shadow. | [critic-panel-correlated-by-default](upgrades/profound/2026-04-26-critic-panel-correlated-by-default/) — already tracked; this is a reminder that until the wrapper exists, the orchestrator should emit a clear error rather than degrading. |

### Class C — too small for the lab (mechanical sweep)

Three items are house-cleaning, not ideas. They do not deserve their own entries — they belong in a single mechanical-sweep commit, scoped narrowly:

- **C1.** [.claude/settings.local.json](.claude/settings.local.json):4 has a verbatim `Bash(xargs -I {} bash -c 'echo "=== {} ===" && head -30 {}')` allow rule that matches only that exact string — accidental capture of a one-off command, not an intentional permission.
- **C2.** Three orphan worktrees on disk in `.claude/worktrees/` (untracked, ignored — privacy hygiene only): `agent-a51228d6`, `agent-a6ac8cdc`, `review-critic-write-upgrade-WGvh2`.
- **C3.** Stale on-disk artifacts: `upgrades/LEDGER.md.bak` (untracked older copy) and `.DS_Store` at repo root (untracked).

These three are flagged here *only* so they are not lost; they should not become lab entries.

## SOTA gaps surfaced but not filed here

Cross-referencing current Anthropic / Claude Code documentation surfaced four forward-looking gaps that are **not** defects in the current contract — they are upgrades to the contract itself. Each warrants its own dedicated `/upgrade` rather than being bundled into this audit. Three are already in the lab.

| Gap | Status |
|---|---|
| Cache-aware structuring of the 6-lane shadow panel for prompt-cache reuse. | Not filed. Candidate `/upgrade`. |
| Skills as a complement to subagents (e.g. `requirement-classifier` could be a skill, not a subagent). | Session [2026-04-26-karpathy-skills-adoption](.claude/session-artifacts/2026-04-26-karpathy-skills-adoption/) ran but no lab entry exists. |
| `EXTERNAL_SHADOW=1` wrapper script. | Filed: [critic-panel-correlated-by-default](upgrades/profound/2026-04-26-critic-panel-correlated-by-default/). |
| Live workflow-step status (statusline / output style surfacing "step 7 of 12"). | Not filed. Candidate `/upgrade`. |

## What this audit reveals about the lab itself

Two patterns surfaced unexpectedly while doing the audit, both worth naming.

**1. The lab is forecasting well.** Eight of eleven findings already exist as lab entries, several of them filed weeks before the audit was conceived. The lab's profound-tier entries about *unenforced contracts* described the failure mode in the abstract; the audit found exactly that failure mode in the concrete. This is what an R&D lab should do — name the abstract pattern before its instances accumulate enough to make the pattern undeniable.

**2. But the lab cannot graduate its own entries.** Of the eight evidenced entries, **all are still at `🌱 created`**. The lab successfully captured the thinking; nothing has acted on it. That is a known feature of the lifecycle (graduation is hard on purpose), but the audit makes the cost legible: each `🌱 created` entry that proposed mechanical enforcement is one entry's worth of latent defects accumulating in the live tree. The accumulation is invisible until something like this audit forces a count.

This is itself a candidate observation for the lab — that *the gap between filing and graduation has compounding cost when the entries describe enforcement gaps*. Filing it would be recursive; recording it here is enough for now.

## Proposed graduation path

This entry's own next state would be `📋 prepared` — detailed enough to act on. Three concrete acts would qualify:

1. **Three new `/upgrade` follow-ups** for the Class A novel findings. Each entry stands alone with its own lifecycle: A1 (outside-view tool/contract mismatch), A2 (settings.json absolute paths), A3 (bypassed-vs-incomplete session marker — likely subsumed by [casual-output-is-workflow-unprotected](upgrades/profound/2026-04-26-casual-output-is-workflow-unprotected/) but worth checking before filing).
2. **Advancement notes on the Class B entries.** This audit becomes citable evidence in the body of each B-class entry — *not by editing existing entry bodies* (per the lab's own discipline; entries are historical record), but by appending a "2026-05-08 audit reference" line if the operator chooses to advance any of them to `📋 prepared` or beyond.
3. **A single mechanical-sweep commit for Class C** — touched by a session, not by an entry. Three lines of cleanup.

The audit itself, as a recurring artifact, is a separate question — would it benefit from being a routine? The case for: contract drift accumulates between audits, and a quarterly snapshot would surface the accumulation early. The case against: routinizing it risks turning the lab into a backlog. Defer the decision; re-run this audit manually once or twice more before deciding.

## Why this is normal, not no-brainer or profound

**Not no-brainer** — this is not "30 minutes of obvious work." Each Class A finding has design surface (especially A3, where the bypassed-marker convention has implications for the artifacts-README, the lifecycle of impl-task sessions, and the ledger-bypass exemption rule). Each Class B finding requires deciding whether to edit existing entries (forbidden by lab discipline), append references, or supersede them. The aggregate cost is real engineering plus real lab curation.

**Not profound** — the central insight (*contracts enforced only by instruction-following drift silently*) is **already filed**, multiple times, by entries that are themselves profound. Adding empirical evidence for an existing insight is creative work but not a new frame. Filing this as profound would inflate the tier; the lab's discipline is to default to the lower tier in doubt ([upgrades/README.md](upgrades/README.md)).

Normal it is.
