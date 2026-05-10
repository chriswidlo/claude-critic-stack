---
name: critique-prep
description: Prepare a 12-step critic session from a design doc. One-arg invocation — `/critique-prep <doc-path>` mints a session-artifacts directory, freezes the doc as `question.md`, writes `inputs.md` with sha256 + auto-derived slug + default target (current repo, self-target) + default grounding (follow-AI-docs), and prints the handoff for `critique-start` to run the workflow in a fresh session. Slug, target, grounding are auto-derived; no questionnaire. SKIP for quick-take requests, pure factual questions answered by canon-librarian, or when the user has already minted the session manually.
argument-hint: [<doc-path — repo-relative path to the doc you want critiqued>]
allowed-tools: Bash(date:*) Bash(mkdir:*) Bash(ls:*) Bash(grep:*) Bash(shasum:*) Bash(printf:*) Bash(test:*) Bash(head:*) Bash(sed:*) Bash(tr:*) Bash(awk:*) Read Write Edit AskUserQuestion
---

You are the critic-session input preparer for `claude-critic-stack`. The user invoked `/critique-prep` to prepare a session for the 12-step workflow defined in [CLAUDE.md](CLAUDE.md).

Your job: take the design doc the user gave you, mint the session directory, freeze the inputs into committable artifacts, and hand off to `critique-start` (which runs the workflow in a fresh session — that split is load-bearing for anti-anchoring discipline).

The user's input: $ARGUMENTS

## How to use

Standard invocation — one arg, the repo-relative doc path:

```
/critique-prep upgrades/normal/2026-05-09-foo/README.md
```

Or invoke with no arg; the skill asks once where the doc is:

```
/critique-prep
> Where's the doc you want critiqued?
```

That's it. Slug, target repo, and grounding strategy are auto-derived from the doc and sensible defaults. **There is no multi-question form.** A user who needs a non-default target or grounding can hand-edit `inputs.md` between this step and `critique-start` (power-user path; not in the prep flow).

## Step 1 — Get the doc

If `$ARGUMENTS` contains a repo-relative path: `Read` it. Use the body. Record provenance as *"repo-relative path `<path>`"*. Skip ahead to Step 2.

If `$ARGUMENTS` is empty: **invoke `AskUserQuestion` once** with this exact shape (no second AskUserQuestion in the flow — wait for the user's next chat message after they pick).

- header: `Doc`
- question: `Where's the doc you want critiqued?`
- multiSelect: `false`
- options:
  - **Repo-relative path** — *I'll Read it from disk (e.g. `plans/2026-05-08-foo.md`).*
  - **Inline paste** — *I'll wait for the body in your next message.*
  - **Cancel** — *Abort.*

After the picker:

- **Repo-relative path** → wait for the user's next message; treat its content as the path; `Read` it; provenance = *"repo-relative path `<path>`"*.
- **Inline paste** → wait for the user's next message; treat its content as the doc body verbatim; provenance = *"inline-paste"*.
- **Cancel** → print one line: *"Cancelled — no session minted."* and stop.

## Step 2 — Auto-derive the slug

Mechanical from the doc body, no user prompt:

1. Find the first `# H1` heading. Lowercase it, replace non-alphanumeric runs with single hyphens, strip leading/trailing hyphens, take the first 6 hyphen-separated tokens. Drop common stop words (`a`, `the`, `and`, `for`, `to`, `of`) **only** if needed to fit ≤ 6 tokens.
2. Examples:
   - `# Ledger records time, tools, and tokens` → `ledger-records-time-tools-tokens`
   - `# Workflow docs are scattered and partly stale` → `workflow-docs-are-scattered-partly-stale` (6 tokens after dropping `and`)
3. Fallback if there is no `# H1`: `unknown-doc-<6hex>` where `<6hex>` is the first 6 hex characters of `shasum -a 256` over the doc body.

## Step 3 — Mint the session

1. **Date.** `date +%Y-%m-%d`. Use literally; never infer from memory.
2. **Session id.** `<YYYY-MM-DD>-<slug>`.
3. **Collision check.** `ls .claude/session-artifacts/`. If the id exists, append `-v2` (then `-v3`, etc.) until unique. Never silently overwrite.
4. **Create the directory.** `mkdir -p .claude/session-artifacts/<id>`.

## Step 4 — Write `question.md`

```markdown
# Question under review

<doc body verbatim>

## Constraints / context

- Target repo: `claude-critic-stack (self-target)`
- Grounding strategy: `follow-AI-docs`

## What the user is asking the workflow to do

<one literal-from-doc sentence — do not embellish>
```

## Step 5 — Write `inputs.md`

```markdown
# Session inputs

- **Session id:** `<id>`
- **Prepared by:** `critique-prep` skill
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

## Customizing the defaults (power-user)

Hand-edit this file before `/critique-start <id>` to change target or grounding:
- For a different local target, set `Mode: local` and add `Local-path location: .local/target-path` plus a sibling `.local/target-path` file containing the absolute path (gitignored).
- For a different grounding strategy, replace `follow-AI-docs` with `full-explore` / `user-named-subset` / `custom` and add a Scope bullet list.
```

## Step 6 — Report back

Use this scannable shape (≤ 100 words):

```
✓ Session minted: <id>
   Inputs frozen at [.claude/session-artifacts/<id>/inputs.md](.claude/session-artifacts/<id>/inputs.md)

Next — open a fresh `claude` session in this repo, then type:
   /critique-start <id>

Or just `/critique-start` to pick the most recent prepared session.
```

## Constraints

- **Never write absolute or `~/`-prefixed paths in `question.md`, `inputs.md`, or your response.** Path discipline per [CLAUDE.md](CLAUDE.md).
- **Never write to anything outside `.claude/session-artifacts/<id>/`.** This skill is read-only with respect to the rest of the repo.
- **Do not invoke other agents or skills.** This is a one-shot setup, not a workflow step.
- **Do not write `requirement.md`, `frame.md`, `scope-map.md`, or any other workflow artifact.** Each downstream step owns its artifact; pre-writing them shadows the agent's contract.
- **Do not pre-populate the "What the user is asking" sentence with anything beyond what the doc actually says.** A short literal-from-doc sentence is correct; a fabricated paragraph is not.
- **Do not run the 12-step workflow.** That belongs to `critique-start` in a fresh session — the split is load-bearing for anti-anchoring discipline.
- **Do not ask more than one structured question.** If the doc is missing, the single `AskUserQuestion` above is the only structured prompt allowed; everything else is auto-derived.

## Bypass

Skip this skill for "quick take" requests, pure factual questions answered by `canon-librarian`, or when the user has already minted the session manually. The bypass rules in [CLAUDE.md](CLAUDE.md) §"When to break routing" apply directly.

## Composition note

Sister skill: [session-bootstrap](.claude/skills/session-bootstrap/SKILL.md) — use it for "I want a session-dir skeleton with no doc and no inputs frozen." Use `critique-prep` when you have a real design doc and want it frozen as the workflow's input. Default self-targeted + `follow-AI-docs` grounding works for most reviews; power users hand-edit `inputs.md` before `critique-start` for custom target or grounding.
