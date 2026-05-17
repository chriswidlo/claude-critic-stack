# Explore raw return — diagnostics surface audit

## 1. Hook scripts — AI-blindness and fail-open discipline

**`<target>/.claude/hooks/session-start.sh`** (16 lines)
- Stderr suppression: complete. Every command (jq, mkdir, date) ends with `2>/dev/null`.
- Fail-open: `set +e` on line 5. No exit code checks; exits 0 always.
- Staging-only writes: lines 9–14 write exclusively to `.claude/.metrics/staging/$SID/`. No session-artifacts pollution.
- Side effects: writes `current-session-uuid` sigil to `.claude/.metrics/` at line 14 for orchestrator handoff.
- Discipline met. ✓

**`<target>/.claude/hooks/post-tool-use.sh`** (13 lines)
- Stderr suppression: complete. jq, mkdir, date, printf all wrapped `2>/dev/null`.
- Fail-open: `set +e` on line 4. Exit 0 always.
- Staging-only writes: line 12 appends single-line JSON to `events.jsonl`.
- Discipline met. ✓

**`<target>/.claude/hooks/stop.sh`** (35 lines)
- Stderr suppression: complete.
- Fail-open: `set +e` on line 5. Both branches exit 0.
- Conditional branching (lines 17–34): if `workflow-id.txt` is missing, archives to `.claude/.metrics/orphan/$SID/` instead of session-artifacts. Correct isolation. ✓
- Parser invocation: lines 26–28 background the parser with `nohup ... >/dev/null 2>&1 &`. Fully detached.
- Discipline met. ✓

## 2. Parser — token attribution and regex looseness

**`<target>/bin/parse-session-metrics.py`** (257 lines)

**Subagent transcript discovery (lines 25–36):**
- Walks `~/.claude/projects/<encoded-cwd>/<claude-uuid>.jsonl` via glob (line 29).
- Searches for subagents in `transcript.parent/subagents/` (line 35).
- Hardcoded path dependency on undocumented Claude Code layout. If Claude Code moves transcripts or subagents, parser silently returns `transcript-missing` (line 30). No defensive probe; no fallback.

**Token attribution (lines 59–97, 100–127):**
- Main thread: skips `isSidechain=true` entries (line 75), sums main-thread tokens.
- Subagents: reads `.meta.json` sibling for `agentType`, matches to `.jsonl` via name substitution (lines 113–115).
- By-agent aggregation (lines 140–152): groups tokens under agent type string. Clean. ✓

**Verdict parsing (lines 170–185):**
- Regex: `r"verdict\s*[:=]\s*(\w+)"` (line 182) — looks for the word "verdict" followed by whitespace, colon-or-equals, whitespace, word chars. Reasonably tight, but **no word boundary prefix** — `myverdict:` would match. Should be tightened to `r"\bverdict\s*[:=]\s*(\w+)"`. Minor risk; metrics non-load-bearing.

**Loop counting (lines 188–196):**
- Regex: `r"\b(rewrite|replan)\b"` (line 196) — **correctly word-bounded.**
- Counts all matches, no structure enforcement.
- **Contradicts the upgrade entry**, which says "loop-count regex is also loose." The code does have word boundaries. Counter is not "explicit `## Loop N` header counting" — could false-match if prose discusses rewrite/replan. Acceptable v1; should be improved to count `## Loop N` headers.

**Error handling (lines 40–56, 233–246):**
- `OSError` caught with `pass`; JSON errors caught with `continue`; exceptions in `build_token_block` fall back to `parse-error: <ExceptionType>`. Fail-open met. ✓

## 3. Ledger-render skill — metrics read timing

**`<target>/.claude/skills/ledger-render/SKILL.md`** (95 lines)

- Step 12 = Synthesis (CLAUDE.md line 77).
- Step 10 = Critic-panel (CLAUDE.md line 52).
- Step 13 = Ledger (CLAUDE.md line 97).
- Ledger-render reads `metrics.json` at its own invocation (line 70: "If `.../diagnostics/metrics.json` exists, read it and append..."). Happens *after* synthesis (step 12), which is *after* critics write verdicts (step 10).
- Critic verdicts written to `critiques/*.md` by critic agents at step 10.
- The parser (which reads `critiques/*.md` post-session and produces `metrics.json`) runs as a background process started by the Stop hook. Ledger-render reads parsed result.
- **Critics write `critiques/*.md`, parser parses post-session, ledger-render reads parsed result.** Correct ordering: metrics derivative, read only after critique final. ✓

**Metrics block error handling (line 71):** "If `metrics.json` is missing ... silently skip — do not write a placeholder, do not error." Graceful, no user-visible parse error surface. ✓

## 4. Explain skill — dashboard metrics reading

**`<target>/.claude/skills/explain/SKILL.md`** (201 lines)

- Reads from `glob.glob(.../session-artifacts/*/diagnostics/metrics.json)` (line 33).
- Validates `ds = d.get('duration_seconds')` (lines 36–38).
- Falls back to `~10 min` if fewer than 3 sessions have valid `duration_seconds` (line 45).
- The "~10 min" on the user's recent explain card aligns with this fallback. Robust. ✓

## 5. Fonts directory

**`<target>/.claude/skills/explain/fonts/`** — `calvin-s.flf` present (2651 bytes). ✓

## 6. Session-artifacts README — schema documentation

**`<target>/.claude/session-artifacts/README.md`**

- Load-bearing headings (`## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`) present and untouched (lines 106–127).
- Diagnostics schema section (lines 163–200): `diagnostics/` subfolder documented as optional; `## Metrics` block "additive, optional"; older ledgers without it remain valid. Additive contract preserved. ✓

## 7. CLAUDE.md — step 1 workflow-id handoff

**`<target>/CLAUDE.md`** (lines 24–31)

- "Diagnostics handoff (one-time, at step 1)" placed *before* step 1 enumeration (line 33). Part of the "Default behavior (12-step workflow)" preamble.
- Documented as part of canonical step 1 description, not buried. Code block (lines 26–29) shows the exact command. Clear. ✓

## 8. Settings.json — hooks configuration

**`<target>/.claude/settings.json`** (lines 19–42)

- `SessionStart` (lines 20–25): runs `session-start.sh`.
- `PostToolUse` (lines 27–33): matcher `.*` (all tools), runs `post-tool-use.sh`.
- `Stop` (lines 35–40): runs `stop.sh`.
- Three hooks wired correctly. No other hooks. Permissions block (lines 2–18) allows Read/Glob/Grep + specific Bash; denies `rm` and `git push`. ✓

## 9. Upgrade entry vs. code

| Claim | Code reality | Status |
|-------|--------------|--------|
| Hooks suppress stdout/stderr | `2>/dev/null` on every command, `set +e` fail-open | ✓ verified |
| Subagent transcripts at `~/.claude/projects/<uuid>/subagents/*.jsonl` | parser lines 35, 115 | ✓ verified (undocumented dependency) |
| Verdict regex is loose | `r"verdict\s*[:=]\s*(\w+)"` — no word boundary prefix | ⚠ slightly tighter than claimed but still loose |
| Loop-count regex is loose | `r"\b(rewrite\|replan)\b"` — HAS word boundaries | **Contradicts upgrade entry** |
| Metrics read after critic verdicts | step 13 after step 12 after step 10 | ✓ verified |
| `workflow-id.txt` in CLAUDE.md step 1 | line 24 preamble + code block | ✓ verified |

## 10. Existing sessions with diagnostics

`find .claude/session-artifacts -type d -name "diagnostics"` returns **empty.** No completed workflow session yet has a populated `diagnostics/` subfolder. The hooks were deployed 2026-05-09 but have not been active in any completed workflow session yet.

## 11. Staging and orphan directories

**`<target>/.claude/.metrics/staging/`**: 4 subdirectories (session UUIDs). One has `workflow-id.txt`; others lack it (will route to orphan on Stop).

**`<target>/.claude/.metrics/orphan/`**: 4 subdirectories, all with `end.ts` and `events.jsonl`, no `workflow-id.txt`. Sessions aborted before step 1, archived correctly. ✓

## 12. Pre-2026-05-09 sessions (replay candidates)

Sessions without diagnostics folders, suitable for retrospective parser replay (per outside-view's cheapest experiment):

1. `2026-04-24-repo-upgrade-research` — has requirement.md, frame.md, scope-map.md, no synthesis (incomplete)
2. `2026-04-27-critics-get-write-tool-impl` — full workflow, has synthesis.md, decision-log.md (complete, suitable)
3. `2026-04-25-sota-claude-online-research` — has artifacts, suitable

Oldest session 2026-04-24 (16 days pre-2026-05-09). Sufficient history for replay validation.

## 13. Structural enforcement of AI-blindness invariant

Convention-based with partial structural enforcement:
1. `set +e` in all three hooks.
2. `2>/dev/null` on every command (redirects stderr only).
3. Stop hook outputs nothing; background parser uses nohup redirect.
4. Ledger-render reads metrics, only writes `ledger.md`.
5. Explain skill reads metrics from disk, no transcript pass-through.

No wrapper or guard that *guarantees* a hook cannot accidentally echo. A future edit adding `echo "DEBUG: ..."` without redirection would leak. Risk: moderate. Mitigation: code-review discipline + test on a hook-enabled run.

## 14. Synthesis order in ledger-render

**Race condition possible but pragmatically safe:**
- Stop hook backgrounds parser with `nohup ... &` (fire-and-forget).
- If ledger-render (step 13) is invoked immediately after Stop, parser may still be running and `metrics.json` may not exist yet.
- Ledger-render handles this: "If `metrics.json` is missing ... silently skip — do not write a placeholder."
- Parser is "fast (<100ms)" per upgrade entry, so in practice it finishes before the user invokes ledger-render manually.
- If a future orchestrator auto-invokes ledger-render immediately after Stop, the race could manifest.
- Worth documenting in CLAUDE.md or adding a polling loop in ledger-render. Not a blocker for v1.

## Summary table

| Aspect | Finding | Risk |
|---|---|---|
| Hook stderr suppression | complete on all commands | low |
| Hook fail-open | `set +e` on all three | low |
| Staging isolation | no session-artifacts pollution | low |
| Orphan handling | sessions without workflow-id route correctly | low |
| Parser subagent discovery | hardcoded undocumented Claude Code layout | **medium** — silent failure if layout changes |
| Verdict regex | loose (no word boundary prefix) | low |
| Loop-count regex | upgrade entry mischaracterizes; code has `\b...\b` | negligible (doc error) |
| Metrics read timing | after critics final | low |
| Ledger-render error handling | graceful fallback | low |
| Explain dashboard fallback | renders ~10 min stub if <3 sessions | low |
| Schema documentation | load-bearing untouched, additive only | low |
| Step 1 workflow-id.txt handoff | documented in canonical step 1 | low |
| Settings hooks | three lifecycle events wired | low |
| AI-blindness enforcement | convention-based, not structural | **low-medium** |
| Metrics race (parser vs ledger-render) | possible but pragmatically safe | low (acceptable v1) |

## Critical finding: no existing session diagnostics

The implementation landed 2026-05-09 but **no completed workflow session yet has a populated `diagnostics/` folder.** The hooks have been wired but have not measured a real workflow. This session will be the first real dogfood run. The outside-view forecast's concern about "silent attribution drift from undocumented-layout dependency" is **not yet empirically validated.**

## Contradictions between upgrade entry and code

1. **Loop-count regex looseness**: upgrade says "regex is also loose" but code has `\b...\b` word boundaries. Code is correct; upgrade entry mischaracterizes.
2. **Verdict regex `name:` false-match**: upgrade entry claims this happened in smoke-test, but the regex as written should not match `name:`. Either the false match was in different prose (e.g., a discussion of verdicts), or the upgrade entry was written from a different version of the code.

## Findings for critics

1. **Undocumented Claude Code layout is load-bearing.** Recommend: (a) add a contract test, (b) document the assumption in a comment, or (c) add a fallback path probe.
2. **Metrics read race condition is low-risk but worth hardening.** Ledger-render gracefully skips if metrics missing, but a future auto-invoke could miss them. Worth a 1-second polling loop.
3. **AI-blindness is convention-enforced, not structural.** All hooks follow `2>/dev/null` pattern but a future maintainer could break it. Worth a lint check or wrapper that enforces redirects.
4. **Diagnostics folders will start populating once this audit completes.** The implementation is live but untested on real workflows.
