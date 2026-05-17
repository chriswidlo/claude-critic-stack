# Question under review

The design document under review is the upgrades/normal entry [Ledger records time, tools, and tokens (per workflow session)](../../../upgrades/normal/2026-05-09-ledger-records-time-tools-tokens/README.md), which proposes — and as of 2026-05-09 has *implemented* — a per-session diagnostics layer (hook scripts capturing timestamps and tool calls; a post-session transcript parser attributing tokens by agent; a `## Metrics` block inlined into `ledger.md` at synthesis; dashboard wiring in the `/explain` skill).

The entry's body is reproduced below verbatim.

---

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

## The gap, named

The current ledger (per [`.claude/session-artifacts/README.md`](../../README.md) load-bearing schema) records four things: agent-call count, artifact count, loop count, and threshold warnings. None of these answer the operator's diagnostic questions:

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

## How hooks bridge Claude UUID → workflow ID

The Claude Code session UUID is known at `SessionStart`, but the workflow ID isn't assigned until step 1 of the workflow. The bridge:

1. Hooks initially write to `.claude/.metrics/staging/<claude-uuid>/`.
2. The orchestrator at step 1 (when it assigns the workflow ID) writes a single line to `.claude/.metrics/staging/<claude-uuid>/workflow-id.txt`.
3. The `Stop` hook reads that file, moves staged data into `.claude/session-artifacts/<workflow-id>/diagnostics/`, removes the staging dir.
4. If `workflow-id.txt` is missing (session aborted before step 1, or a `quick take` bypass), the Stop hook archives staged data to `.claude/.metrics/orphan/<claude-uuid>/`. Nothing is lost; nothing pollutes session-artifacts.

## Why this is AI-blind (zero disruption)

Three layers, only one of which involves the AI at all:

| Layer | Mechanism | AI sees it? | Cost |
|---|---|---|---|
| Live capture (start/end/tools) | bash hooks executed by Claude Code | no | 0 tokens |
| Token attribution | post-session Python parser, runs as `&` background | no | 0 tokens |
| Ledger inline | synthesis step (step 12) reads `metrics.json`, writes `## Metrics` block | yes, briefly | ~500 tokens, AFTER critic decisions are final |

Critics at step 5 are completely blind to instrumentation. The only AI involvement is at synthesis time, after every critique decision has been recorded. The metrics-write cannot influence verdicts.

## Implementation notes — what actually shipped

Landed 2026-05-09. Specifics worth recording for the review:

- **Subagent transcripts live in a separate location than initially assumed.** First parser draft looked for `isSidechain=true` entries inline in the main transcript. Discovered during smoke-test that current Claude Code stores subagents at `<encoded-cwd>/<claude-uuid>/subagents/agent-<id>.jsonl`, with sibling `agent-<id>.meta.json` carrying the `agentType`. Parser was rewritten to walk the subagents dir + read meta files. Undocumented in current Anthropic refs; if Claude Code changes the layout, the parser breaks silently (returns "transcript-missing").
- **Verdict regex is loose.** Current parser greps `verdict\s*[:=]\s*(\w+)` in `critiques/*.md`. Falsely matched `name:` in one critique file during smoke-test.
- **Loop-count regex is also loose.** Counts `\b(rewrite|replan)\b` in `decision-log.md` — false positives possible.
- **`workflow-id.txt` handoff requires the orchestrator to follow CLAUDE.md step 1.** If skipped, staged metrics route to `.claude/.metrics/orphan/` and never reach `diagnostics/`.
- **Hook stderr suppression is fragile.** Every hook command must end with `2>/dev/null`. A future edit that adds a debug `echo` without redirection would leak hook output to Claude.

## Review brief — what the 12-step run-through should examine

### 1. Workflow pollution audit (load-bearing)

The strongest claim of this implementation is **AI-blindness**. Critics should verify:

- Does the AI ever see hook output during a session?
- Does the synthesis-step `metrics.json` read happen *strictly after* critic verdicts are written?
- Does the `workflow-id.txt` write at step 1 add noticeable noise to the orchestrator's context?
- Could a malformed `metrics.json` trigger a parse error that surfaces to the user?

### 2. Regression check — critic decisions and gates

Did instrumentation change *any* observable behavior of the 12-step workflow?

- Are critic verdicts still recorded in `critiques/*.md` exactly as before?
- Does the hard gate at step 9 (scope-map.md + challenges.md required) still fire?
- Does the synthesis citation line at the bottom of `synthesis.md` still match the schema?
- Compare a pre-implementation session ledger to a post-implementation one — anything drift?

### 3. Degradation check — perceived speed and clutter

- Does the session feel slower? Hook execution adds ~50ms per tool call.
- Does the chat UI show any new artifacts that weren't there before?
- Is the operator's mental model of "what just happened" cluttered by the new diagnostics dir?

### 4. SOTA opportunities — diagnostic dataset, speed, accuracy

**Dataset richness.** What's missing that would actually help diagnose problems? Per-step duration, cache hit ratios, cost in $, critic verdict reasons, subagent prompt/response length distribution.

**Speed.** Where does the parser block? Currently `nohup &` — non-blocking on session end. But it walks every subagent JSONL synchronously; large sessions could take 10s+.

**Accuracy.** Where does attribution break? Nested subagents, tool-result tokens, loose verdict/loop regexes.

### 5. Cross-session aggregation (deferred but worth flagging)

V1 ships per-session diagnostics only. The natural next move is a `bin/metrics-summary.sh` that aggregates duration / tokens across the last N sessions, flags anomalies, and produces a leaderboard of "expensive agents."

## Open questions

1. **Should `metrics.json` be committed to git?**
2. **Should `events.jsonl` be committed?**
3. **Cross-session aggregation?** Deferred to follow-up.
4. **Token cost in $?**
5. **Hook layout durability.** What's our exposure if Claude Code changes the transcript path or subagent storage layout?
6. **Privacy boundary.** `events.jsonl` records every tool call by name. Should there be a `--privacy-mode`?

---

## Constraints / context

- Target repo: `https://github.com/chriswidlo/claude-critic-stack.git` (this repo — dogfooding)
- Grounding strategy: user-named-subset, scoped to the diagnostics surface (hooks, parser, ledger-render skill, explain skill, schema doc, CLAUDE.md step 1)
- The implementation has already shipped (2026-05-09); the review is run-through-repo, not pre-merge gate
- The review session itself will produce diagnostics on itself (dogfooding loop)

## What the user is asking the workflow to do

Run the 12-step adversarial review against the just-shipped diagnostics implementation in this repo: validate the AI-blindness claim, surface regressions or quality risks in what shipped, and identify SOTA upgrades worth queueing as follow-up work.
