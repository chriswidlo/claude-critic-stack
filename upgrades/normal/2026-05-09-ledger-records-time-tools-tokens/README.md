# Ledger records time, tools, and tokens (per workflow session)

| Field | Value |
|---|---|
| 📌 **title** | Ledger records time, tools, and tokens (per workflow session) |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-09 |
| ⚡ **catalyst** | Surfaced during the `/explain` v6 redesign. The dashboard wanted to show "average session duration" and "total tokens spent" but the existing ledger schema records `agent-calls`, `artifacts`, `loops`, and warnings — no time, no tools, no tokens. The operator asked: "where did the time go?" "what cost the most?" and "are critics balanced?" None of those are answerable today without manual transcript spelunking. |
| 💡 **essence** | Per-session diagnostics live in the workflow-session directory alongside other artifacts but in their own `diagnostics/` subfolder for separation. Hooks capture timestamps and tool counts live (AI-blind). A post-session parser walks the Claude Code main transcript + `<uuid>/subagents/*.jsonl` files (each subagent is its own JSONL with sibling `.meta.json` for `agentType`) to attribute tokens to specific agents (canon-librarian, critic-architecture, etc.). Synthesis (step 12) inlines a `## Metrics` block in `ledger.md`. The `/explain` dashboard reads recent metrics to show real averages instead of stubs. **Implemented 2026-05-09 under operator approval via plan-mode; this entry is now the subject of a follow-up 12-step run-through-repo, not a forward-looking proposal.** |
| 🚀 **upgrade** | Implementation landed: 3 hook scripts + parser + ledger-render update + schema doc + dashboard wiring + `.gitignore` allow for `.claude/hooks/`. ~600 lines of code/docs across 9 files. AI-blind by design: hooks suppress stdout/stderr; only synthesis briefly reads `metrics.json` (~500 tokens) AFTER critic decisions are final. The run-through-repo (this entry as input) should validate that claim, find regressions, and surface SOTA improvements — see *Review brief* below. |
| 🏷️ **tags** | diagnostics, observability, ledger, hooks, tokens, performance |
| 🔗 **relates_to** | step-13-session-ledger, format-only-state-transition-gate, agentic-engineering-reference-library |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-05-09 | — | — | 2026-05-09 (plan-mode) | pending — *this entry is the subject* | 2026-05-09 | — | — |

## Table of contents

- [The gap, named](#the-gap-named)
- [What we collect](#what-we-collect)
- [Where it lives on disk](#where-it-lives-on-disk)
- [How hooks bridge Claude UUID → workflow ID](#how-hooks-bridge-claude-uuid--workflow-id)
- [Phased implementation](#phased-implementation)
- [Why this is AI-blind (zero disruption)](#why-this-is-ai-blind-zero-disruption)
- [Risks and mitigations](#risks-and-mitigations)
- [Implementation notes — what actually shipped](#implementation-notes--what-actually-shipped)
- [Review brief — what the 12-step run-through should examine](#review-brief--what-the-12-step-run-through-should-examine)
- [Why this is normal, not no-brainer](#why-this-is-normal-not-no-brainer)
- [Why this is normal, not profound](#why-this-is-normal-not-profound)
- [Open questions](#open-questions)

## The gap, named

The current ledger (per [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md) load-bearing schema) records four things: agent-call count, artifact count, loop count, and threshold warnings. None of these answer the operator's diagnostic questions:

- **"Where did the 10 minutes go?"** — no per-phase or per-agent timing
- **"What cost the most tokens?"** — no token tracking at all
- **"Are critics balanced?"** — no per-lens token or duration breakdown
- **"Did one agent dominate?"** — derivable in principle but not surfaced

These questions matter because the stack's value depends on rigorous critique, and rigorous critique can become **expensive** silently — one critic blowing up its context, a runaway gather phase, an unnecessary loop. Today the operator has to read transcripts manually to debug.

## What we collect

Per workflow session, written to a dedicated `diagnostics/` subfolder under the session-artifacts directory:

| Source | Captures | Goes to |
|---|---|---|
| `SessionStart` hook | start timestamp | `diagnostics/start.ts` |
| `PostToolUse` hook (every call) | `{ts, tool, sidechain}` per call | `diagnostics/events.jsonl` |
| `Stop` hook | end timestamp | `diagnostics/end.ts` |
| Transcript parser (post-session) | tokens per turn, sidechain flag, Agent name | `diagnostics/metrics.json` |
| Synthesis step (step 12) | critic verdicts, loop counts | `ledger.md` `## Metrics` block |

The `## Metrics` block in `ledger.md` is the human-readable summary of `diagnostics/metrics.json`. Schema:

```yaml
duration_seconds: 562
tokens:
  total: { input: 124530, output: 18920 }
  by_agent:
    canon-librarian:     { input: 22000, output: 3200, calls: 1 }
    critic-architecture: { input: 15000, output: 4500, calls: 1 }
    critic-operations:   { input: 14000, output: 4200, calls: 1 }
    critic-product:      { input:  5500, output: 4100, calls: 1 }
    subagent-distiller:  { input:  8000, output: 1100, calls: 5 }
tool_calls: { total: 23, Read: 8, Bash: 7, Agent: 5, Edit: 3 }
verdicts: { architecture: approve, operations: approve, product: rework }
loops: 1
```

## Where it lives on disk

Diagnostics belong to the **workflow session**, not the Claude Code session — they describe what happened during the design review. They live in their own subfolder for separation from business artifacts:

```
.claude/session-artifacts/<workflow-id>/
  requirement.md             ← business artifacts (existing)
  frame.md
  scope-map.md
  challenges.md
  distillations/
  critiques/
  decision-log.md
  synthesis.md
  ledger.md                  ← gains a `## Metrics` block at synthesis
  diagnostics/               ← NEW: dedicated subfolder
    start.ts
    end.ts
    events.jsonl
    metrics.json
```

The `.claude/session-artifacts/README.md` schema doc is updated to document the optional `diagnostics/` subdir. Existing load-bearing headings (`## Counts`, `## Derived ratios`, `## Warnings`, `## Notes`) stay untouched; the new `## Metrics` heading is additive and optional (older sessions without it remain valid).

## How hooks bridge Claude UUID → workflow ID

The Claude Code session UUID (e.g., `bd33f0ac-43e2-...`) is known at `SessionStart`, but the workflow ID (e.g., `2026-05-09-foo-bar`) isn't assigned until step 1 of the workflow. The bridge:

1. Hooks initially write to `.claude/.metrics/staging/<claude-uuid>/`.
2. The orchestrator at step 1 (when it assigns the workflow ID) writes a single line to `.claude/.metrics/staging/<claude-uuid>/workflow-id.txt`.
3. The `Stop` hook reads that file, moves staged data into `.claude/session-artifacts/<workflow-id>/diagnostics/`, removes the staging dir.
4. If `workflow-id.txt` is missing (session aborted before step 1, or a `quick take` bypass), the Stop hook archives staged data to `.claude/.metrics/orphan/<claude-uuid>/`. Nothing is lost; nothing pollutes session-artifacts.

The orchestrator's contribution is a single sentence in CLAUDE.md step 1 description: write `workflow-id.txt` to staging when assigning the session id. ~50 tokens of overhead, one time, per session.

## Phased implementation

| Phase | Files (NEW unless noted) | Time |
|---|---|---|
| **1. Hooks** | `.claude/hooks/session-start.sh` (~6 lines), `.claude/hooks/post-tool-use.sh` (~8 lines), `.claude/hooks/stop.sh` (~14 lines), `.claude/settings.json` (+~12 lines hooks block, MODIFIED), `CLAUDE.md` (+~3 lines step 1, MODIFIED) | 1–2 hrs |
| **2. Parser** | `bin/parse-session-metrics.py` (~80 lines) — reads `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl`, attributes tokens via `isSidechain` + Agent `tool_use` boundaries | 2–3 hrs |
| **3. Ledger inline** | `.claude/skills/ledger-render/SKILL.md` (MODIFIED) — emit `## Metrics` block at synthesis; `.claude/session-artifacts/README.md` (MODIFIED) — document `diagnostics/` subdir | 30 min |
| **4. Dashboard wiring** | `.claude/skills/explain/SKILL.md` (MODIFIED) — read recent `## Metrics` blocks, compute averages, replace stub time estimates | 30 min |
| **Total** | | **~half a day** |

## Why this is AI-blind (zero disruption)

Three layers, only one of which involves the AI at all:

| Layer | Mechanism | AI sees it? | Cost |
|---|---|---|---|
| Live capture (start/end/tools) | bash hooks executed by Claude Code | no | 0 tokens |
| Token attribution | post-session Python parser, runs as `&` background | no | 0 tokens |
| Ledger inline | synthesis step (step 12) reads `metrics.json`, writes `## Metrics` block | yes, briefly | ~500 tokens, AFTER critic decisions are final |

Critics at step 5 are completely blind to instrumentation. The only AI involvement is at synthesis time, after every critique decision has been recorded. The metrics-write cannot influence verdicts.

Hook design principles for safety:

- **Redirect stderr to /dev/null** — `2>/dev/null` on every command, otherwise hook errors leak into Claude's view
- **Fast (<100ms)** — hooks block tool calls until they return; just `date` + a single file append
- **Single events.jsonl, not many small files** — fewer fs ops, cleaner audit trail
- **Never modify session-artifact contents** — only write to `diagnostics/` (or staging); orchestrator-canonical artifacts stay untouched
- **Fail open** — `set +e`; if a hook crashes, the workflow continues unharmed

## Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| `CLAUDE_TOOL_NAME` env var not present in PostToolUse hook | medium | Phase 1 starts with a probe hook that logs `env`; falls back to parsing `$CLAUDE_TOOL_INPUT` JSON |
| Claude session UUID format differs from transcript filename | low | Parser walks recent transcripts in `~/.claude/projects/<encoded-cwd>/`, picks the one matching `start.ts` mtime if UUID lookup fails |
| Stop hook fires before transcript fully flushes | medium | Parser is idempotent and re-runnable; can also be invoked manually post-hoc |
| Hook stderr leaks visible to AI | high if uncareful | Every hook command wraps with `2>/dev/null`; `set +e` to fail open |
| `settings.json` hooks schema differs across Claude Code versions | low | Phase 1 verifies on the user's current version before phases 2–4 |
| Step 1 orchestrator forgets to write `workflow-id.txt` | low | CLAUDE.md step 1 update makes it part of the canonical step description |
| `quick take` bypass sessions create orphan staging dirs | medium | Stop hook archives to `.claude/.metrics/orphan/`; periodic cleanup is a future concern, not blocking |

## Implementation notes — what actually shipped

Landed 2026-05-09 in this session. Specifics worth recording for the review:

- **Subagent transcripts live in a separate location than I initially assumed.** First parser draft looked for `isSidechain=true` entries inline in the main transcript. Discovered during smoke-test that current Claude Code stores subagents at `~/.claude/projects/<encoded-cwd>/<claude-uuid>/subagents/agent-<id>.jsonl`, with sibling `agent-<id>.meta.json` carrying the `agentType`. Parser was rewritten to walk the subagents dir + read meta files. Worth flagging: this is undocumented in current Anthropic refs; if Claude Code changes the layout, the parser breaks silently (returns "transcript-missing"). A future-proofing concern.
- **Verdict regex is loose.** Current parser greps `verdict\s*[:=]\s*(\w+)` in `critiques/*.md`. Falsely matched `name:` in one critique file during smoke-test. Acceptable for v1 (verdicts are not load-bearing in `metrics.json` consumption), but flagged for tightening.
- **Loop-count regex is also loose.** Counts `\b(rewrite|replan)\b` in `decision-log.md` — false positives possible if the prose contains those words discussing other things. Should be replaced with explicit "Loop N" header counting (matching the existing ledger-render pattern).
- **`workflow-id.txt` handoff requires the orchestrator to follow CLAUDE.md step 1.** If the orchestrator skips writing it (e.g., a future AI version that doesn't read CLAUDE.md as carefully), staged metrics route to `.claude/.metrics/orphan/` and never reach `diagnostics/`. The existing CLAUDE.md edit says "run this once silently" — load-bearing.
- **Hook stderr suppression is fragile.** Every hook command must end with `2>/dev/null`. A future edit that adds a debug `echo` without redirection would leak hook output to Claude. Worth a `set -e` audit, or moving hooks to a more defensive pattern (write to file, never stdout).

## Review brief — what the 12-step run-through should examine

This entry is now the *subject* of a follow-up run-through-repo. The session that runs the workflow against this entry will produce diagnostics on itself — the implementation will measure its own first review. Dogfooding.

The review should specifically examine:

### 1. Workflow pollution audit (load-bearing)

The strongest claim of this implementation is **AI-blindness**. Critics should verify:

- Does the AI ever see hook output during a session? Inspect chat transcripts of a session with hooks enabled vs disabled.
- Does the synthesis-step `metrics.json` read happen *strictly after* critic verdicts are written? Examine the order in `ledger-render` SKILL.md.
- Does the `workflow-id.txt` write at step 1 add noticeable noise to the orchestrator's context? Measure tokens before/after.
- Could a malformed `metrics.json` trigger a parse error that surfaces to the user? Test deliberately corrupted input.

### 2. Regression check — critic decisions and gates

Did instrumentation change *any* observable behavior of the 12-step workflow?

- Are critic verdicts still recorded in `critiques/*.md` exactly as before?
- Does the hard gate at step 9 (scope-map.md + challenges.md required) still fire?
- Does the synthesis citation line at the bottom of `synthesis.md` still match the schema in `.claude/session-artifacts/README.md`?
- Compare a recent pre-implementation session ledger to a post-implementation one — anything drift?

### 3. Degradation check — perceived speed and clutter

Subjective but real. Operators sometimes notice friction even when load is theoretically zero:

- Does the session feel slower? Hook execution adds ~50ms per tool call; over 100 tool calls that's 5 seconds.
- Does the chat UI show any new artifacts (e.g., file-write notifications for hook output) that weren't there before?
- Is the operator's mental model of "what just happened" cluttered by the new diagnostics dir?

### 4. SOTA opportunities — diagnostic dataset, speed, accuracy

Three vectors for upgrade:

**Dataset richness.** Current `metrics.json` records: duration, tokens by agent, tool counts, verdicts, loops. What's missing that would actually help diagnose problems?
- Per-step duration (not just per-agent) — clusters events around artifact mtimes
- Cache hit ratios (already in the transcript `usage` field; not surfaced)
- Cost in $ (token counts × pricing — trivial follow-up)
- Critic verdict reasons (not just approve/reject — the frame objection itself)
- Subagent prompt + response length distribution (anomalies signal stuck agents)

**Speed.** Where does the parser block?
- Currently runs as `nohup &` from Stop hook — non-blocking on session end. Good.
- But it walks every subagent JSONL synchronously; large sessions (50+ agents) could take 10s+. Is incremental parsing worth it (resume from last checkpoint)?
- Could events.jsonl be replaced by a more compact binary log if size becomes an issue?

**Accuracy.** Where does attribution break?
- Nested subagents (subagent calling subagent) — current attribution puts those tokens under the OUTER subagent. Is that right?
- Tool-result tokens (the *result* of an Agent call returns to main thread; whose budget does that come from?) — currently undefined in our model.
- The verdict regex is loose (noted above). Tighter alternatives?
- Loop-count regex is loose (noted above). Better to count explicit "## Loop N" headers in decision-log.md?

### 5. Cross-session aggregation (deferred but worth flagging)

V1 ships per-session diagnostics only. The natural next move is a `bin/metrics-summary.sh` or `/cost-report` skill that:
- Aggregates duration / tokens across the last N sessions
- Flags anomalies (one critic 3× heavier than the others, sessions exceeding budget, sudden duration spikes)
- Produces a leaderboard of "expensive agents" so operators can prioritize optimization

Worth scoping as a follow-up `upgrades/normal/` entry once v1 has produced ≥10 sessions of data.

## Why this is normal, not no-brainer

A no-brainer would be a one-line change with obvious correctness — adding a single field to an existing struct, fixing a typo in a hook. This work touches five files in the system surface (hooks dir, settings, CLAUDE.md, schema doc, ledger-render skill) and introduces a new external dependency on Claude Code's hook lifecycle and transcript JSONL format. There are real edge cases (orphan staging, quick-take bypass, transcript flush timing) that need explicit handling. The cost is half a day, the value is real but not transformational. Normal tier is right.

## Why this is normal, not profound

A profound upgrade would change the operator's mental model of the system or unlock capability that wasn't possible before. This is instrumentation: it surfaces information the system already produces (every token used, every tool called, every agent invoked) but doesn't currently aggregate. It makes the existing system *measurable* without changing what the system does. Useful, sometimes load-bearing for capacity planning or anomaly detection, but not a model shift.

## Open questions

These questions land on the run-through-repo's plate. The 12-step workflow should answer or defer each explicitly.

1. **Should `metrics.json` be committed to git?** Pro: full audit history, longitudinal analysis. Con: noisy diffs, repo bloat over time. Default: yes (commit) but reconsider once size data exists.
2. **Should `events.jsonl` be committed?** Larger than `metrics.json`. Higher diff churn. Could be derivative-only (regenerate from transcript on demand). Lean toward NO — but the run-through should decide.
3. **Cross-session aggregation?** Deferred to follow-up. Worth flagging as priority-2 once v1 has run ≥10 sessions.
4. **Token cost in $?** Trivial multiply. Decide once Anthropic publishes a stable programmatic pricing endpoint or we hardcode latest known rates.
5. **Hook layout durability.** What's our exposure if Claude Code changes the transcript path or subagent storage layout? The parser silently produces `transcript-missing` if the layout shifts. Is that acceptable, or should we add a contract test?
6. **Privacy boundary.** `events.jsonl` records every tool call by name. If the operator runs a session that touches a private repo via WebFetch or Bash, the tool name leaks to the log. Names only — no payloads — but worth thinking about. Should there be a `--privacy-mode` that disables PostToolUse capture per session?
