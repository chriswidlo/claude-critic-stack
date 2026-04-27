# Explore — path-discipline empirical audit (raw)

## 1. Compliance breakdown by author class

| Author Class | Files with Links | File-Relative (Violations) | Repo-Root Compliant | Violation Rate |
|---|---|---|---|---|
| **Operator** | 3 | 1 | 2 | 33% (1/3) |
| **Slash-command** | 7 | 35 | 1 | 97% (6/7 files) |
| **Session-artifact** | 5 | 19 | 4 | 40% (2/5) |
| **Agent contracts** | 0 | 0 | 0 | N/A |
| **Command contracts** | 0 | 0 | 0 | N/A |

Slash-command entries are the primary violator class: 6 of 7 use file-relative paths exclusively. The single compliant slash-command entry is [`upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md`](upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md).

[`upgrades/LEDGER.md`](upgrades/LEDGER.md) has 43 repo-root links + 1 file-relative violation (single line citing a session-artifact path).

## 2. Drift timeline: pre-rule vs. post-rule

Rule commit: `5108ed3`, 2026-04-26.

| Cohort | Files | Violations | All Post-Rule? |
|---|---|---|---|
| Slash-command | 6 violating | 35 | ✅ All 6 created 2026-04-27 |
| Session-artifact | 2 violating | 19 | ✅ Both created 2026-04-27 |

**100% of file-relative violations post-date the rule.** No pre-rule drift exists — the drift is exclusively in agent-generated content authored after the rule was added.

## 3. Slash-command audit ([`.claude/commands/upgrade.md`](.claude/commands/upgrade.md))

**Zero mentions** of path style, link format, file-relative vs. repo-root in 45 lines. Instructions cover folder location (line 6), meta-table fields (lines 23-30), prose quality (lines 44-45), output path (line 96). None constrain link format.

## 4. Agent-prompt audit ([`.claude/agents/`](.claude/agents/))

| Agent | Write tool? | Path-discipline mentioned? | Produces path refs? |
|---|---|---|---|
| `canon-librarian` | ❌ | ❌ | ❌ |
| `canon-refresher` | ❌ | ❌ | ❌ |
| `critic-architecture` | ❌ | ❌ | ❌ |
| `critic-operations` | ❌ | ❌ | ❌ |
| `critic-product` | ❌ | ❌ | ❌ |
| `frame-challenger` | ✅ Write | ❌ | ✅ writes `challenges.md` with cross-refs |
| `outside-view` | ❌ | ❌ | ❌ |
| `requirement-classifier` | ❌ | ❌ | ❌ |
| `scope-mapper` | ✅ Write+Grep+Glob | ❌ | ✅ writes `scope-map.md` with primitive paths |
| `subagent-distiller` | ✅ Write | ❌ | ✅ writes distillations citing sources |

**Three agents with Write access produce path references; none mention the path-discipline rule.**

## 5. Risk surface — Option B (flip to file-relative)

| File | Type | Rewritable? |
|---|---|---|
| [`upgrades/LEDGER.md`](upgrades/LEDGER.md) | Operator | ✅ |
| [`upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md`](upgrades/profound/2026-04-26-subagents-claim-writes-not-on-disk/README.md) | Slash-command | ✅ |
| [`.claude/session-artifacts/2026-04-26-karpathy-skills-adoption/distillations/explore.md`](.claude/session-artifacts/2026-04-26-karpathy-skills-adoption/distillations/explore.md) | Session-artifact | ❌ locked |
| 3 more session-artifact files | Session-artifact | ❌ locked |

**6 currently-compliant files would need rewriting; 4 are off-limits.** Net: Option B forces a divergence between editable surfaces (rewritten) and locked surfaces (still repo-root) — produces a *worse* split than the current state.

## 6. Risk surface — Option A (keep rule + patch enforcement)

| Author Class | Files | Violations | Action |
|---|---|---|---|
| Slash-command | 6 | 35 | Rewrite cross-references when entries are next edited |
| Session-artifact | 2 | 19 | **Locked — do not edit** (per commit `5108ed3`) |
| Operator ([`upgrades/LEDGER.md`](upgrades/LEDGER.md)) | 1 | 1 | One-line manual fix |

**Surgical fix:** patch 4 agent surfaces (3 Write-capable agents + the slash command) with one path-discipline sentence each. Rewrite ~7 active files. Leave session-artifacts as historical record per the longitudinal-record contract.

## 7. Privacy sanity check

`grep -rE "(/Users/|/home/[a-z]|~/[A-Za-z])" --include="*.md"` (excluding `.git/` and `.claude/worktrees/`) — **zero hits.**

The rule's primary purpose (privacy) is fully achieved. The compliance issue is purely about *style*, not *privacy*.

## Synthesis

1. The rule's privacy work is done — zero leaks.
2. Style violations are 100% post-rule and 100% in agent-authored output.
3. The enforcement surface is silent: slash-command, no path mention; 3 Write-capable agents, no path mention.
4. The fix scope is small if the rule stays: ~4 prompt patches + ~7 file rewrites.
5. Flipping the rule (Option B) creates a *new* split between locked session artifacts and editable surfaces.

The operator's lean toward Option A is empirically supported. The dominant cause is enforcement-surface silence, not rule unsoundness.
