# Session inputs

- **Session id:** `2026-05-09-review-diagnostics-impl`
- **Prepared by:** `critique-prep` skill
- **Date:** `2026-05-09`

## Design doc

- **Provenance:** repo-relative path `upgrades/normal/2026-05-09-ledger-records-time-tools-tokens/README.md`
- **Body sha256 (first 12 hex):** `eadb2dc11495` — change-detection across reruns

## Target repo

- **Identifier:** `https://github.com/chriswidlo/claude-critic-stack.git` (this repo — dogfooding)
- **Mode:** `local`
- **Local-path location:** `.local/target-path` (gitignored, present only in local mode)

## Grounding strategy

- **Strategy:** `user-named-subset`
- **Scope (target-repo-relative):**
  - `<target>/.claude/hooks/`
  - `<target>/bin/parse-session-metrics.py`
  - `<target>/.claude/skills/ledger-render/SKILL.md`
  - `<target>/.claude/skills/explain/SKILL.md`
  - `<target>/.claude/skills/explain/fonts/`
  - `<target>/.claude/session-artifacts/README.md`
  - `<target>/CLAUDE.md`
  - `<target>/.claude/settings.json`
  - `<target>/upgrades/normal/2026-05-09-ledger-records-time-tools-tokens/README.md`
- **Notes:** This is a dogfooding review — the target repo *is* the working repo. The implementation landed 2026-05-09 in this same checkout, so Explore should read the working tree (not a remote checkout). The review brief in the design doc names the questions Explore should be ready to answer: workflow pollution audit, regression check, degradation check, SOTA opportunities. Cross-reference recent session-artifacts (e.g. ledger.md / synthesis.md from sessions on or after 2026-05-09) to compare pre- vs post-implementation behavior.

## Path-rewrite contract for the workflow

When `critique-start` runs in a fresh session, it sources `.local/target-path` into `$CRITIC_TARGET`. Any subagent that reads from `$CRITIC_TARGET` must rewrite absolute paths in artifacts as `<target>/...`. The token `<target>` is stable across machines and forks; the absolute path is not, and would violate path discipline per [CLAUDE.md](../../../CLAUDE.md).

Special case for this session: because `<target>` *is* this repo, `<target>/foo` and `foo` (repo-root-relative) refer to the same files. Prefer `<target>/foo` in artifacts to keep the target-vs-stack distinction grep-able.
