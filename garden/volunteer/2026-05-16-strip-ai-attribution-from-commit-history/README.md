# Strip AI-attribution from commit history

| Field | Value |
|---|---|
| 📌 **title** | Strip AI-attribution from commit history |
| 🎯 **category** | 🍀 volunteer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-05-16 |
| ⚡ **catalyst** | Audit on 2026-05-16 found 38 / 55 commits (69%) end with `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`. Pattern goes back to the earliest commits — source is Claude Code's default commit-template plus the system prompt instruction. Tracked artifacts (`*.md`, `*.json`, `*.yaml`, `*.sh`, `*.py`, `*.mjs`) are clean; only commit messages carry the noise. The new [CLAUDE.md](CLAUDE.md) rule prevents future violations; this entry handles the legacy cleanup. |
| 💡 **essence** | `git log` should read like a human-authored project diary. The trailer adds zero information per commit, fragments scanning, and confuses subsequent AI reads of the history. Forward-looking fix landed (CLAUDE.md rule on 2026-05-16); legacy 38 commits still carry the trailer. Mechanical rewrite. |
| 🚀 **upgrade** | One pass with `git filter-repo --message-callback` stripping the trailer (and the blank line above it) from every commit message in the repo's history. ~5 minutes wall-clock. Force-push to remote afterward; repo is solo + closed-world per README so no collaborator coordination is needed. |
| 🏷️ **tags** | history, hygiene, attribution, git, repo-cleanup |
| 🔗 **relates_to** | path-discipline rule (precedent for AI-output hygiene as a load-bearing repo norm) |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-05-16 | — | — | — | — | — | — | — |

## The fix

Single command (run from repo root, with a fresh `git filter-repo` install via `brew install git-filter-repo`):

```bash
git filter-repo --message-callback '
import re
# Strip "Co-Authored-By: ..." lines and the blank line above them.
# Re-uses the system-prompt template byte-for-byte, so this regex is exact.
cleaned = re.sub(
    rb"\n\nCo-Authored-By: [^\n]*<[^@]+@anthropic\.com>\s*",
    b"",
    message,
)
return cleaned.rstrip() + b"\n"
'
```

Then `git push --force-with-lease origin main`.

## What this touches

- **All 38 dirty commits** get new SHAs (cascade — every descendant SHA changes too, so realistically every commit's SHA changes back to the earliest dirty one).
- **Commit subject lines, bodies (minus trailer), authorship, dates** — all preserved verbatim.
- **No file content changes.** This is a metadata-only rewrite.

## Followups after the rewrite

1. **Force-push.** `git push --force-with-lease origin main`. Single remote, no collaborators.
2. **Delete any local clones outside the canonical one.** They'd diverge.
3. **Six upgrade entries record committed-SHAs in their bodies** ([critic-panel-correlated-by-default](upgrades/profound/2026-04-26-critic-panel-correlated-by-default/), [step-13-session-ledger](upgrades/normal/2026-04-26-step-13-session-ledger/), [hard-gates-as-harness-hooks](upgrades/normal/2026-04-26-hard-gates-as-harness-hooks/)). Those SHAs become stale. Two options:
   - **Re-record** — bulk-edit each entry to replace the old SHA with the new one (`git log --grep` matches the subject lines, derive the new SHA).
   - **Leave stale as historical fingerprint** — acceptable; the commit subject lines still identify the work, just not the exact post-rewrite SHA.
4. **Confirm CLAUDE.md rule is holding** by inspecting the next commit you make — should have no trailer.

## Why this is no-brainer tier

- **Mechanical**: one `filter-repo` command + force-push. No design decision, no critic review needed.
- **Reversible**: keep a tag (`pre-rewrite-2026-05-16`) on the current HEAD before running; if anything goes wrong, `git reset --hard pre-rewrite-2026-05-16` recovers.
- **Solo, closed-world repo** per README — force-push is acceptable. No external PRs or forks to coordinate with.
- **Forward-looking fix already in place** — the CLAUDE.md rule blocks new violations. This entry is *only* for legacy cleanup.

## Why this is not normal-tier

- Doesn't change behavior, doesn't add primitives, doesn't reshape any abstraction. It's a `sed`-equivalent over commit messages. Tier matches the cost.

## When to skip

- If the operator never reads `git log` and the trailers don't bother anyone — leave it. The CLAUDE.md rule alone is enough to keep `git log` clean going forward; the legacy noise becomes a 2026-and-earlier fingerprint that fades from relevance as the project grows.

## When to do it

- If the operator wants `git log` to read clean today, OR if the repo is about to be shown to others (renamed per the rename shortlist in [README.md](README.md), opened to external readers, published) — strip first.
