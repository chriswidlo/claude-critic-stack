---
name: critique-prep
description: Prepare a 12-step critic session from a design document and an optional target repo. Collects the doc, target repo path, and grounding strategy; mints the session-artifacts directory; writes question.md / inputs.md / .local/target-path; prints handoff instructions for `critique-start` to run the workflow in a fresh session. SKIP for quick-take requests, pure factual questions answered by canon-librarian, or when the user has already minted the session manually.
argument-hint: [<slug — 2-6 kebab-case words capturing the question identity>]
allowed-tools: Bash(date:*) Bash(mkdir:*) Bash(ls:*) Bash(test:*) Bash(grep:*) Bash(git:*) Bash(shasum:*) Bash(printf:*) Bash(basename:*) Read Write Edit
---

You are the critic-session input preparer for `claude-critic-stack`. The user has invoked `/critique-prep` to prepare a session for the 12-step workflow defined in [CLAUDE.md](CLAUDE.md).

Your job: collect the design doc + target repo + grounding strategy, mint the session directory, and freeze the inputs into committable artifacts plus a single gitignored path-pointer. You do **not** run the workflow — that is `critique-start`'s job in a fresh session. The split exists so the workflow runs in a clean context window against frozen inputs (anti-anchoring discipline per [CLAUDE.md](CLAUDE.md) §"Things you must not do").

The user's input: $ARGUMENTS

## Kickoff — if nothing was provided

If the user invoked the skill with **no design doc in `$ARGUMENTS`, no doc pasted in this conversation, and no slug**, do not start the structured questionnaire yet. First ask one short prompt to get the raw material:

> *"What's the design or idea you'd like critiqued? Paste it here as text, give me a repo-relative path (e.g. `plans/2026-05-08-foo.md`), or describe it in prose. If it relates to a target repo you'd like the workflow to read while critiquing, share that path or git URL too — otherwise the critique runs prompt-only."*

Wait for the user's reply. From that single message, extract whatever the user gave (doc body / path / repo location), then **proceed into the structured questionnaire below for whatever is still missing.** Skip questions whose answers were already supplied.

If the user invoked the skill **with a slug in `$ARGUMENTS` but no doc**, accept the slug, then ask the kickoff prompt above for the doc + target repo, then run the questionnaire for whatever remains.

If the user invoked the skill **with a doc path / pasted body / target repo already in conversation**, skip the kickoff prompt and go straight into the structured questionnaire — the kickoff is only for the empty-handed case.

## What you collect (one at a time, via AskUserQuestion)

Ask in this order; do not batch.

1. **Design doc source.** Options:
   - paste text inline (user supplies the body in their next message)
   - repo-relative path (e.g. `plans/2026-05-08-foo.md`) — Read it, use the body
   - absolute path on disk — Read it, use the body, do NOT record the absolute path

2. **Slug** (only if `$ARGUMENTS` did not supply one). Same rules as [session-bootstrap](.claude/skills/session-bootstrap/SKILL.md): lowercase letters, digits, single hyphens; 2–6 words; no leading/trailing hyphen; reject single-word slugs. If the slug fails validation, propose a fix and ask once before proceeding.

3. **Target repo.** Options:
   - **Absolute path** on disk — verify with `test -d "<path>/.git"`; reject with one question if not a git repo
   - **Git remote URL only** ("remote-info-only" mode) — workflow runs without filesystem grounding, URL recorded for context
   - **None** ("prompt-only" mode) — step 5 (Explore) will be skipped per [CLAUDE.md](CLAUDE.md)

4. **Grounding strategy.** Only ask if target mode ≠ none. Options:
   - `full-explore` — multi-agent deep read of the target
   - `user-named-subset` — paths or globs the user specifies (target-repo-relative, e.g. `<target>/src/auth/`)
   - `follow-AI-docs` — read the target's CLAUDE.md, AGENTS.md, docs/ai/ first, derive scope from there
   - `custom` — free-form prose strategy

## Your task

1. **Today's date.** `date +%Y-%m-%d`. Use literally; never infer from memory.

2. **Validate the slug.** Per the rules above. If invalid, propose a corrected form and ask once.

3. **Form the session id.** `<YYYY-MM-DD>-<slug>`.

4. **Collision check.** `ls .claude/session-artifacts/`. If the id exists, ask the user: (a) reuse the existing session, (b) append `-v2` to the slug, (c) pick a different slug. Never silently overwrite.

5. **Verify target repo if local-path mode.** `test -d "<path>/.git"`. If not a git repo, surface and ask once before proceeding (the user may have intended a parent dir).

6. **Derive the target identifier** for `inputs.md` (path-discipline: never the absolute path).
   - Local-path mode: try `git -C "<path>" remote get-url origin`. If it succeeds, use that URL. If it fails (no remote), use `basename "<path>"` as the identifier and note "no remote" in inputs.md.
   - Remote-only mode: the URL the user gave.
   - None mode: literally `(none — prompt-only critique)`.

7. **Ensure `.gitignore` admits `.local/`.** Run `grep -F '.claude/session-artifacts/*/.local/' .gitignore`. If absent, append two lines (a comment + the rule) to the end of `.gitignore`. Idempotent — never add a duplicate.

8. **Create the directory.** `mkdir -p .claude/session-artifacts/<id>/.local`.

9. **Write `question.md`.** Body comes from the design doc the user supplied. Format:

   ```markdown
   # Question under review

   <design doc body verbatim — paste-in or Read'd content, NEVER an absolute path to it>

   ## Constraints / context

   - Target repo: <identifier from step 6>
   - Grounding strategy: <strategy name, or "(none)" if prompt-only>
   <— additional bullets only if the user supplied constraints —>

   ## What the user is asking the workflow to do

   <one sentence inferred from the doc; if unclear, ask one question and use the answer>
   ```

10. **Write `inputs.md`.** Path-discipline-clean. Format:

    ```markdown
    # Session inputs

    - **Session id:** `<id>`
    - **Prepared by:** `critique-prep` skill
    - **Date:** `<YYYY-MM-DD>`

    ## Design doc

    - **Provenance:** <"inline-paste" | "repo-relative path `<path>`">
    - **Body sha256 (first 12 hex):** `<run shasum -a 256 against the doc body, take first 12 chars>` — change-detection across reruns

    ## Target repo

    - **Identifier:** `<identifier from step 6>`
    - **Mode:** `<local | remote-only | none>`
    - **Local-path location:** `.local/target-path` (gitignored, present only in local mode)

    ## Grounding strategy

    - **Strategy:** `<full-explore | user-named-subset | follow-AI-docs | custom | (n/a)>`
    - **Scope (target-repo-relative):**
      - `<target>/<path-or-glob-1>`
      - `<target>/<path-or-glob-2>`
    - **Notes:** <verbatim user prose, or "(none)">

    ## Path-rewrite contract for the workflow

    When `critique-start` runs in a fresh session, it sources `.local/target-path` into `$CRITIC_TARGET`. Any subagent that reads from `$CRITIC_TARGET` must rewrite absolute paths in artifacts as `<target>/...`. The token `<target>` is stable across machines and forks; the absolute path is not, and would violate path discipline per [CLAUDE.md](CLAUDE.md).
    ```

11. **Write `.local/target-path`** only in local-path mode. A single line, the absolute path, no extra content. This file is gitignored — it never enters git history.

12. **Report back** in ≤ 100 words:
    - Session id minted.
    - Repo-root-relative link to [inputs.md](.claude/session-artifacts/) (substitute the actual id in the link target).
    - The exact handoff sentence: *"Open a fresh Claude Code session in this repo and invoke `critique-start <id>` (or `critique-start` to pick the most recent prepared session)."*

## Constraints

- **Never write absolute or `~/`-prefixed paths in `question.md`, `inputs.md`, or your response.** The absolute target path goes only in `.local/target-path` (gitignored) and only in local-path mode.
- **Never write to the target repo.** This skill is read-only with respect to anything outside `claude-critic-stack`.
- **Do not invoke other agents.** This is a one-shot setup, not a workflow step.
- **Do not write `requirement.md`, `frame.md`, `scope-map.md`, or any other workflow artifact.** Each downstream step owns its artifact; pre-writing them shadows the agent's contract.
- **Do not pre-populate fields the user did not provide.** A skeleton with empty bullets is correct; a fabricated context paragraph is not.
- **Do not run the 12-step workflow.** That belongs to `critique-start` in a fresh session — the split is load-bearing.
- **Do not silently overwrite a `.local/target-path` from a prior session reuse.** If reusing, ask once whether the target repo location has changed.

## Bypass

- **Skip this skill** for "quick take" requests, pure factual questions answered by `canon-librarian`, or when the user has already minted the session by hand. The bypass rules in [CLAUDE.md](CLAUDE.md) §"When to break routing" apply directly.

## Composition note

This skill is a richer sibling of [session-bootstrap](.claude/skills/session-bootstrap/SKILL.md). Use `session-bootstrap` for "I just want a session-dir skeleton with no doc and no target repo." Use `critique-prep` when you have a real design doc and want the workflow grounded in a target repo — that is the common case the 12-step workflow was built for.
