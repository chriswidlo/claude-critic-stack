---
name: critique
description: One-shot adversarial review of a design document. Invoke as `/critique <doc-path>` — the skill mints a session-artifacts directory, freezes the doc as `question.md` + `inputs.md`, then begins step 1 of the 13-step workflow defined in CLAUDE.md. Synthesis is presented in the same session, typically 5–15 minutes later. Slug auto-derived from the doc's H1; target defaults to current repo (self-target); grounding defaults to follow-AI-docs. No questionnaire, no fresh-session split. SKIP for `quick take` requests, pure factual questions answered by canon-librarian, or when the user has already minted the session manually.
argument-hint: <doc-path — repo-relative path to the doc you want critiqued>
allowed-tools: Bash(date:*) Bash(mkdir:*) Bash(ls:*) Bash(grep:*) Bash(shasum:*) Bash(printf:*) Bash(test:*) Bash(head:*) Bash(sed:*) Bash(tr:*) Bash(cat:*) Bash(awk:*) Read Write Edit AskUserQuestion
---

You are the one-shot critic-review skill for `claude-critic-stack`. The user invoked `/critique <doc-path>` to run an adversarial review of a design document.

This skill replaces the older `/critique-prep` + `/critique-start` pair. The two-skill split existed to deliver a fresh context window for the workflow ("anti-anchoring insurance"), but that property is redundant given the **distillation discipline at step 6** of the workflow (per [CLAUDE.md](CLAUDE.md) §"Things you must not do" — *do not read raw subagent output after step 6*). The distillation rule is the actual anti-anchoring mechanism; the session-boundary split was paying for redundant insurance with one full quit/reopen per review. Merged.

The user's input: $ARGUMENTS

## How to use

```
/critique garden/perennial/2026-05-09-foo/README.md
```

One argument, the repo-relative doc path. The skill auto-derives the slug from the doc's first H1, defaults target=`current repo` and grounding=`follow-AI-docs`, mints the session, writes the input artifacts, and **immediately begins step 1 of the 13-step workflow** per [CLAUDE.md](CLAUDE.md). You read the synthesis at the end. No questions asked unless `$ARGUMENTS` is empty.

A user who needs a non-default target or grounding can hand-edit `inputs.md` between Phase A and Phase B — but the skill body runs through both automatically, so this is only possible by interrupting the skill manually. For routine use, the defaults suffice.

## Phase A — Prepare inputs (mint the session)

### A.1 Get the doc

If `$ARGUMENTS` contains a repo-relative path: `Read` it. Use the body. Record provenance as *"repo-relative path `<path>`"*. Skip to A.2.

If `$ARGUMENTS` is empty: invoke `AskUserQuestion` once with this exact shape — no second AskUserQuestion in the flow.

- header: `Doc`
- question: `Where's the doc you want critiqued?`
- multiSelect: `false`
- options:
  - **Repo-relative path** — *I'll Read it from disk (e.g. `plans/2026-05-08-foo.md`).*
  - **Inline paste** — *I'll wait for the body in your next message.*
  - **Cancel** — *Abort.*

After the picker:

- **Repo-relative path** → wait for the user's next chat message; treat its content as the path; `Read` it; provenance = *"repo-relative path `<path>`"*.
- **Inline paste** → wait for the user's next chat message; treat its content as the doc body verbatim; provenance = *"inline-paste"*.
- **Cancel** → print one line: *"Cancelled — no review started."* and stop.

### A.2 Auto-derive the slug

Mechanical from the doc body, no user prompt:

1. Find the first `# H1` heading. Lowercase, replace non-alphanumeric runs with single hyphens, strip leading/trailing hyphens, take the first 6 hyphen-separated tokens. Drop common stop words (`a`, `the`, `and`, `for`, `to`, `of`, `on`, `in`) **only** if needed to fit ≤ 6 tokens.
2. Examples:
   - `# Ledger records time, tools, and tokens` → `ledger-records-time-tools-tokens`
   - `# Workflow docs are scattered and partly stale` → `workflow-docs-are-scattered-partly-stale` (6 tokens after dropping `and`)
3. Fallback if there is no `# H1`: `unknown-doc-<6hex>` where `<6hex>` is the first 6 hex chars of `shasum -a 256` over the doc body.

### A.3 Mint the session

1. **Date.** `date +%Y-%m-%d`. Use literally; never infer from memory.
2. **Session id.** `<YYYY-MM-DD>-<slug>`.
3. **Collision check.** `ls .claude/session-artifacts/`. If the id exists, append `-v2` (then `-v3`, etc.) until unique. Never silently overwrite.
4. **Create the directory.** `mkdir -p .claude/session-artifacts/<id>`.

### A.4 Write `question.md`

```markdown
# Question under review

<doc body verbatim>

## Constraints / context

- Target repo: `claude-critic-stack (self-target)`
- Grounding strategy: `follow-AI-docs`

## What the user is asking the workflow to do

<one literal-from-doc sentence — do not embellish>
```

### A.5 Write `inputs.md`

```markdown
# Session inputs

- **Session id:** `<id>`
- **Prepared by:** `critique` skill
- **Date:** `<YYYY-MM-DD>`

## Design doc

- **Provenance:** `<"inline-paste" | "repo-relative path `<path>`">`
- **Body sha256 (first 12 hex):** `<shasum -a 256 over doc body, first 12 chars>` — change-detection across reruns

## Target repo

- **Identifier:** `claude-critic-stack (self-target)`
- **Mode:** `self-target` (default)

## Grounding strategy

- **Strategy:** `follow-AI-docs` (default)
- **Notes:** Explore (step 5 of the workflow) reads the target's `CLAUDE.md` / `AGENTS.md` / `docs/ai/` to derive scope.
```

### A.6 Diagnostics handoff

Per [CLAUDE.md](CLAUDE.md) §"Diagnostics handoff", write the assigned workflow id to the diagnostics staging dir so the `Stop` hook routes metrics into the workflow-session dir at end of session:

```bash
SID=$(cat .claude/.metrics/current-session-uuid 2>/dev/null)
[ -n "$SID" ] && echo "<id>" > ".claude/.metrics/staging/$SID/workflow-id.txt"
```

Silent, AI-blind otherwise.

## Phase B — Run the 13-step workflow

After Phase A completes, **print a single short ack line** (≤ 25 words):

```
▶ Session minted: <id>. Beginning 13-step review.
```

Then **begin step 1 of the workflow** per [CLAUDE.md](CLAUDE.md). From here on, follow the workflow exactly:

1. **Step 1 — Classification.** Invoke `requirement-classifier`.
2. **Step 2 — Reframe.** You (orchestrator) restate the question in at least one framing the user did not use.
3. **Steps 3–5 — Parallel gather.** `outside-view`, `canon-librarian`, and optionally `Explore`.
4. **Step 6 — Distill.** Invoke `subagent-distiller` per returned subagent. After this, you read only distillations.
5. **Step 7 — Scope-map.** Invoke `scope-mapper`.
6. **Step 8 — Frame-challenger.** Invoke `frame-challenger`.
7. **Step 9 — Generator.** You produce a candidate. Hard gate: `scope-map.md` + `challenges.md` must exist.
8. **Step 10 — Critic panel.** Invoke `critic-architecture`, `critic-operations`, `critic-product` in parallel. Minority-veto.
9. **Step 11 — Replan-vs-rewrite** if any lens vetoed.
10. **Step 12 — Synthesis.** Present the structured synthesis per the schema in CLAUDE.md step 12.
11. **Step 13 — Ledger.** Write `ledger.md` via the [ledger-render](.claude/skills/ledger-render/SKILL.md) skill.

**This skill body does not replicate the workflow's internal logic.** [CLAUDE.md](CLAUDE.md) is the source of truth for steps 1–13, hard gates, must-nots, and agent contracts. If the workflow evolves, only CLAUDE.md changes; this skill's Phase B simply hands off.

## Constraints

- **Never write absolute or `~/`-prefixed paths in `question.md` or `inputs.md`.** Path discipline per [CLAUDE.md](CLAUDE.md).
- **Never modify the target repo.** This review is read-only with respect to the doc and the target.
- **Do not pre-populate `requirement.md`, `frame.md`, or any other workflow artifact in Phase A.** Each downstream step owns its artifact; pre-writing them shadows the agent's contract.
- **Do not ask more than one structured question.** The single `AskUserQuestion` in A.1 is the only structured prompt allowed; everything else is auto-derived.
- **Do not invoke subagents during Phase A.** Phase A is mechanical setup; agent invocations begin only in Phase B step 1.
- **Do not skip steps 1–13.** Each step's artifact is load-bearing per [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md). The hard gate at step 9 will refuse to proceed without `scope-map.md` and `challenges.md`.

## Bypass

Skip this skill for:
- `quick take` requests (one-paragraph answers bypass the workflow)
- Pure factual questions (route to `canon-librarian` directly)
- Cases where the user has already minted a session by hand (proceed against the existing session — do not re-mint)

The bypass rules in [CLAUDE.md](CLAUDE.md) §"When to break routing" apply directly.

## Composition note

Sister skill: [session-bootstrap](.claude/skills/session-bootstrap/SKILL.md) — for "I want a session-dir skeleton with no doc and no workflow." Use `critique` when you have a real design doc and want the workflow to run end-to-end in one command.
