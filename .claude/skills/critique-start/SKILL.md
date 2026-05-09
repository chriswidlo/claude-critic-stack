---
name: critique-start
description: Trigger the 12-step critic workflow in a fresh session against an input prepared by `critique-prep`. Takes a session id (or resolves the most-recent prepared session). Reads inputs.md, sources .local/target-path so step 5 (Explore) and any later step can read the target repo, then begins step 1 of the workflow defined in CLAUDE.md. SKIP if no prepared session exists — use `critique-prep` first. SKIP for quick-take requests and pure factual questions.
argument-hint: [<session-id>]
allowed-tools: Bash(ls:*) Bash(cat:*) Bash(test:*) Bash(stat:*) Read
---

You are the critic-workflow trigger for `claude-critic-stack`. The user has invoked `/critique-start`. Your job: pick up the input prepared by `critique-prep`, set the target-repo handle in this session's working memory, and begin the 12-step workflow defined in [CLAUDE.md](CLAUDE.md).

This skill expects to run in a **fresh Claude Code session** — clean context window, no prior framing. That is the whole point of the two-skill split: the workflow's anti-anchoring discipline (no raw subagent reads, distillation-only, frame-challenger before generator) only works against a frozen input artifact, not against a context window that already contains the user's framing.

The user's input: $ARGUMENTS

## Your task

1. **Resolve the session id.**
   - If `$ARGUMENTS` is non-empty, treat it as the id. Verify the directory exists with `test -d .claude/session-artifacts/<id>` and that `inputs.md` is present.
   - If `$ARGUMENTS` is empty, run `ls -t .claude/session-artifacts/` and pick the most-recently-modified entry that contains an `inputs.md`. Skip dirs without `inputs.md` — those were minted by `session-bootstrap` (skeleton-only) or by hand and are not full prepared sessions.
   - If no candidate exists, refuse with one sentence: *"No prepared session found. Run `critique-prep` first to prepare a design doc + target repo as input."*

2. **Read [inputs.md](.claude/session-artifacts/) for the resolved id.** Extract: target-repo identifier, mode (`local` | `remote-only` | `none`), grounding strategy, scope, design doc provenance.

3. **Source the target path** if mode is `local`:
   - Read `.claude/session-artifacts/<id>/.local/target-path`.
   - Hold the absolute path in this session's working memory only — treat it as the value of `$CRITIC_TARGET` for any subagent prompt you compose downstream.
   - Never echo it into a committed artifact, decision-log line, or summary message.

4. **Read `question.md`.** Confirm it exists and contains the design doc body. The orchestrator will need it for steps 1, 2, and 9 of the workflow.

5. **Print a short ack** (≤ 60 words):
   - Session id.
   - Target identifier (the repo URL or name from `inputs.md`, **never** the absolute path).
   - Grounding strategy.
   - "Now running step 1: `requirement-classifier`."

6. **Begin the workflow.** Dispatch `requirement-classifier` per [CLAUDE.md](CLAUDE.md) §"Default behavior" step 1. From there, follow steps 1 through 13 as defined in CLAUDE.md. Do not replicate the workflow body in this skill — CLAUDE.md is the source of truth.

7. **Path-rewrite reminder for downstream agents.** Whenever you compose a prompt for an agent that may read from `$CRITIC_TARGET` (Explore in step 5, scope-mapper in step 7, critics in step 10 if they verify facts), include this sentence verbatim in the prompt:

   > Any absolute path under `$CRITIC_TARGET` must appear in your output as `<target>/...`. The absolute path is machine-specific; the `<target>/` token is what gets recorded in artifacts.

   This propagation is what keeps committed artifacts path-discipline-clean even though the workflow has live filesystem access to the target.

## Constraints

- **Never echo `$CRITIC_TARGET`'s absolute value into any committed artifact.** It belongs only in `.local/target-path` (gitignored) and in this session's transient working memory. Use the `<target>/` token in artifacts.
- **Do not re-bootstrap the session.** The directory, `question.md`, and `inputs.md` already exist. Touching them is a contract violation — `critique-prep` is the only writer of those files.
- **Do not skip steps of the 12-step workflow.** Each step's artifact is load-bearing per [.claude/session-artifacts/README.md](.claude/session-artifacts/README.md). The hard gate at step 9 will refuse to proceed without `scope-map.md` and `challenges.md`.
- **Do not duplicate the workflow body.** This skill is a ~30-line trigger; the workflow lives in [CLAUDE.md](CLAUDE.md). If the workflow evolves, only CLAUDE.md changes.
- **If `inputs.md` is missing** at the resolved session dir, refuse — the dir was minted by `session-bootstrap` (skeleton) or by hand, not by `critique-prep`. Instruct the user to run `critique-prep` for a fully-prepared session, or to run the workflow manually if they minted the dir deliberately.

## When to skip this skill

- The user said "quick take" — bypass the whole workflow per [CLAUDE.md](CLAUDE.md) §"When to break routing".
- The user is asking a factual question — route to `canon-librarian` directly.
- No `inputs.md` exists at the candidate session dir — this skill cannot help; either prepare with `critique-prep` or run the workflow manually.
