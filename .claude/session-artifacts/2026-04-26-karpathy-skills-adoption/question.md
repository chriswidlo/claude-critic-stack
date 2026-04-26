# Question under review

The user has asked the orchestrator to validate its own prior writeup and recommendation about adopting `forrestchang/andrej-karpathy-skills` (a Claude Code marketplace plugin that ships a single ~2.4 KB CLAUDE.md with four behavioral principles: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution).

## Prior recommendation (the candidate being validated)

1. Do **not** install the plugin into `claude-critic-stack` (wrong layer — that repo is a deliberation harness, not a target codebase).
2. Most of the file's content is already present in the default Claude Code system prompt and the user's existing global CLAUDE.md.
3. The novel value is the **plugin packaging pattern** (distributing conventions as an installable marketplace plugin) more than the content.
4. Optionally drop 1–2 lines about "Goal-Driven Execution" (failing-test-first as default for non-trivial work) into the global `CLAUDE.md`, which is the only principle weakly represented in current defaults.
5. If installed at all, install globally (apply to repos where code is actually written), not into `claude-critic-stack`.

## Decision being made

What, if anything, the user should change in their Claude Code setup as a result of seeing this repo. Reframed: should the prior recommendation stand, get rewritten, or get replanned?

## Constraints / context provided by the prior conversation

- The user's working directory `claude-critic-stack` is a deliberation harness, not a target codebase (CLAUDE.md says so explicitly).
- The user already has a global `CLAUDE.md` (referenced via memory and the system prompt).
- The default Claude Code system prompt already contains: "don't add features beyond task", "default to no comments", "no error handling for impossible cases", "no backwards-compat shims", etc.
- The karpathy repo's plugin manifest exposes one skill (`karpathy-guidelines`) and registers a marketplace entry.
