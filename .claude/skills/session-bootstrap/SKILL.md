---
name: session-bootstrap
description: Mint a session-artifacts directory for the 12-step workflow defined in CLAUDE.md. Creates .claude/session-artifacts/<YYYY-MM-DD>-<slug>/ and drops a question.md skeleton. Use when the user is starting a new design-question session and the orchestrator is about to invoke requirement-classifier (step 1). SKIP for quick-take requests, pure factual questions answered by canon-librarian, or any case where the user has already created the session directory by hand.
argument-hint: <slug — 2-6 kebab-case words capturing the question identity>
allowed-tools: Bash(date:*) Bash(mkdir:*) Bash(ls:*) Read Write
---

You are the session-artifacts directory bootstrapper for `claude-critic-stack`. The user has invoked `/session-bootstrap` with a slug. Your job is to mint the session directory and drop in a `question.md` skeleton, so the orchestrator can run the 12-step workflow against it.

The user's slug: $ARGUMENTS

(If `$ARGUMENTS` is empty or longer than ~6 words, ask one clarifying question for the slug, then proceed.)

## Your task

1. **Compute today's date.** Run `date +%Y-%m-%d`. Use the resulting `YYYY-MM-DD` literally; do not infer from memory.

2. **Form the session id.** `<YYYY-MM-DD>-<slug>`. Validate the slug:
   - Lowercase letters, digits, and single hyphens only.
   - 2–6 words; reject single-word slugs (too vague to grep later).
   - No leading or trailing hyphens.
   If the slug fails validation, propose a corrected form and ask the user to confirm before proceeding.

3. **Check for collision.** Run `ls .claude/session-artifacts/` and confirm the session id does not already exist. If it does:
   - The collision is almost always a slug duplication; ask the user whether they want to (a) reuse the existing session, (b) append `-v2` to the slug, or (c) pick a different slug. Do not silently overwrite.

4. **Create the directory.** `mkdir -p .claude/session-artifacts/<session-id>`. Do not create subdirectories yet (no empty `distillations/`, no placeholder files beyond `question.md`) — the workflow's downstream steps create what they need.

5. **Write `question.md`.** Use this skeleton, filled with the user's framing if the slug carried obvious context, otherwise left for the user to complete:

   ```markdown
   # Question under review

   <one-paragraph statement of the question, in the user's framing>

   ## Constraints / context

   - <constraint or context point>
   - <constraint or context point>

   ## What the user is asking the workflow to do

   <one sentence: validate a prior recommendation? choose between options? design something new?>
   ```

6. **Report back.** In under 80 words, tell the user:
   - The session id you minted.
   - The path you wrote (repo-root-relative markdown link).
   - One sentence on what the orchestrator should do next, which is almost always: invoke `requirement-classifier` per step 1 of [CLAUDE.md](CLAUDE.md).

## Constraints

- **Never write absolute or `~/`-prefixed paths anywhere in `question.md` or in your response.** Per [CLAUDE.md](CLAUDE.md) §"Path discipline", in-repo references must be repo-root-relative markdown links. Outside-repo references must be described in prose, not as paths.
- **Do not invoke other agents.** This is a one-shot setup, not part of the workflow itself.
- **Do not write `requirement.md`** — that is `requirement-classifier`'s output, not yours. Writing it here would shadow the agent's contract.
- **Do not write `frame.md`, `scope-map.md`, or any other workflow artifact.** Each downstream step owns its artifact.
- **Do not pre-populate `question.md` with content the user did not provide.** A skeleton with empty constraints is correct; a fabricated context paragraph is not.

## When the slug is ambiguous

If the slug is generic (`new-feature`, `decision`, `research`), ask one clarifying question — what is the question *about*, in 4–5 words? — then proceed once the slug is specific enough to be useful as a grep target six months from now.

If the user typed `/session-bootstrap` with no argument, ask for a slug; do not invent one.
