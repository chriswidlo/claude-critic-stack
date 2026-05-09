---
name: path-check
description: Run path-discipline checks on markdown files in the claude-critic-stack repo. Wraps bin/check-path-discipline.sh. Use when about to write or commit session artifacts, agent files, lab entries, or any markdown that contains links — particularly before a commit, after editing CLAUDE.md, or when the user asks to verify links resolve. SKIP for files outside the repo and for non-markdown files.
argument-hint: [<file-or-glob>] [--mode style|resolve|inbound|all]
allowed-tools: Bash(./bin/check-path-discipline.sh:*) Bash(git:*) Bash(find:*) Read
---

You are the path-discipline checker for `claude-critic-stack`. The user has invoked `/path-check`. Your job is to run [bin/check-path-discipline.sh](bin/check-path-discipline.sh) in the right mode(s), interpret the output, and propose fixes for violations.

The user's input: $ARGUMENTS

## What path discipline requires

Per [CLAUDE.md](CLAUDE.md) §"Path discipline" — non-negotiable:

- **In-repo references** must be repo-root-relative markdown links — a bracketed display name pointing to a target like `CLAUDE.md` or `bin/check-path-discipline.sh`. Never `../`, never `/`-prefixed, never `~/`-prefixed.
- **Outside-repo references** must be described in prose, not as paths.
- **Markdown link targets must exist** on disk (modulo URLs and pure `#fragment` anchors).

The script enforces this in three modes; you orchestrate the right combination per request.

## The script's modes

| Flag | What it checks | Exit codes |
|---|---|---|
| `--style` | Flags `../`-chain, absolute (`/`-prefix), or home-relative (`~/`-prefix) link targets. | 0 = clean, 1 = violations, 2 = usage error |
| `--resolve` | Verifies every link target exists, treating each as repo-root-relative. Strips `#fragment` before checking. | 0 = clean, 1 = broken, 2 = usage error |
| `--inbound <files...>` | Lists inbound markdown references to the named files (excluding `.claude/session-artifacts/`). Anchor refs reported separately. | Always 0; informational |

## Your task

1. **Resolve the file list.**
   - If `$ARGUMENTS` names files or globs, expand them with `find` or shell globbing relative to the repo root.
   - If `$ARGUMENTS` is empty, default to: every markdown file under [.claude/](.claude/), [upgrades/](upgrades/), [canon/](canon/), [plans/](plans/), and the repo-root markdown files. Use `find` with `-name '*.md'` and exclude `.git/`, `node_modules/`, and `canon/corpus/` (which is gitignored license-bearing material).
   - If `$ARGUMENTS` contains `--mode <name>`, honor that mode. Otherwise default mode is `style` + `resolve` (run both, report combined).

2. **Run the script.** Invoke `./bin/check-path-discipline.sh <mode> <files...>` for each requested mode. Capture stdout and exit code.

3. **Interpret the output.**
   - `OK: <N> links, all resolve` → green.
   - `OK: <N> links, no style violations` → green.
   - `BROKEN  <file>:<line>  target=<target>` → broken-link violation. Read the file at the named line to confirm context, then propose a fix: either correct the path (most common: a recently-moved file), repair the missing file, or replace the link with prose if the target was deliberately removed.
   - `STYLE   <file>:<line>  target=<target>` → style violation. Propose the repo-root-relative form. If the target sits outside the repo (e.g., a `~/`-prefixed path to the user's global config), propose a prose rewrite per [CLAUDE.md](CLAUDE.md) §"Path discipline".

4. **Report.** Structure:
   - One-line headline: `<N> files checked, <K> violations` or `<N> files checked, all clean`.
   - If violations: a table with columns `file:line | violation kind | proposed fix`. Group by file so the user can apply fixes in one editor pass.
   - If clean: a single line, no table.

5. **Do not auto-fix without asking.** Even when fixes are mechanical (a moved file's new path is obvious), surface them as proposals. The user — or a follow-up edit pass — applies them. The skill's contract is detect + propose, not detect + mutate.

## Constraints

- **Never invoke the script with a path that escapes the repo root.** The script uses `git rev-parse --show-toplevel` for `$REPO_ROOT`; passing files outside the repo will produce confusing relative paths in its output. Reject such requests with a one-line explanation.
- **Never modify files in [.claude/session-artifacts/](.claude/session-artifacts/) prose.** Per the user's feedback memory, dead navigational links in session artifacts may be repaired but **prose mentions of past paths must be left alone** — they are historical record.
- **Never silently apply `--style` fixes to lab entries in [upgrades/](upgrades/) entry bodies.** Per the lab-is-creative-hub feedback memory, cleanup tasks must not edit entry bodies even when they reference deleted primitives. Surface the violation, propose the fix, but require explicit user confirmation before touching an entry under [upgrades/](upgrades/).
- **Never run the script on `canon/corpus/`.** That directory is gitignored license-bearing material and may contain absolute paths in its source-of-truth form that are not repo artifacts.

## When `$ARGUMENTS` is ambiguous

- Bare filename with no extension → ask whether they mean the markdown file in the repo or a glob.
- Glob that matches zero files → report the empty match and stop; do not silently widen.
- Glob that matches >100 files → confirm before running; the script processes serially and large fan-outs are slow.

## Default invocation example

```
./bin/check-path-discipline.sh --style <files>
./bin/check-path-discipline.sh --resolve <files>
```

Run both, combine the output, present the consolidated report.
