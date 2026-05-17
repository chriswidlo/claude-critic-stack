# Running Multiple AI Coding Agents in Parallel — Worktrees, Isolation, and the 10-Session Recipe

*SOTA-2026 / 08 — operational reference for parallel Claude Code sessions on a single repo.*

This is the practical layer: what breaks, what holds, what to set up before launching ten Claude Code sessions simultaneously on the same codebase. Most "git worktree + AI" guides are aimed at two to four concurrent agents. Ten is the regime where the gaps between **code isolation** (worktrees give you this for free) and **runtime isolation** (you have to build it) become load-bearing. Anything you "get away with" at three agents bites at ten.

The report is organised top-down: git worktree fundamentals → Claude Code's native worktree surface → process and environment isolation → resource contention → coordination → existing tooling → failure modes from production reports → a concrete recipe for ten parallel sessions → anti-patterns → and a stack-specific checklist for this repo.

Throughout I distinguish **well-documented operational practice** (cite-able in [git-scm.com docs](https://git-scm.com/docs/git-worktree), [code.claude.com docs](https://code.claude.com/docs/en/worktrees), or production blog posts) from **theoretical / extrapolated** (reasoning from primitives, not from a deployment report). Pay attention to the markers.

---

## 1. Git worktrees as the foundation

### 1.1 The basics

`git worktree add <path> [<branch>]` creates a second working tree from the same `.git` object store. `git worktree list` enumerates them; `git worktree remove <path>` tears one down. The main repo and every linked worktree share `.git/objects` (commits, blobs, trees), `.git/refs` (branches, tags), `.git/config`, and `.git/hooks`. Each linked worktree has its own `index`, `HEAD`, working-directory files, and a tiny per-worktree state directory under `.git/worktrees/<name>/` ([git-worktree(1)](https://git-scm.com/docs/git-worktree)).

What this buys you: cloning a 500 MB repo five times costs roughly 2.5 GB of `.git` objects plus 2.5 GB of working files. Five worktrees of the same repo cost ~500 MB of objects (shared) plus 2.5 GB of working files. The object store is shared; the checked-out files are not. (Well documented.)

What it does *not* buy you: any form of runtime isolation. Worktrees solve "two branches checked out at once." They do not solve "two `npm run dev` instances both want port 3000."

### 1.2 `.gitignore` interactions

`.gitignore` is tracked content; it applies identically in every worktree. The interesting cases are *un*tracked files you want in each worktree:

- `.env`, `node_modules/`, build caches, `.venv/` — these are gitignored, and they do not magically appear in new worktrees.
- Claude Code addresses this with a `.worktreeinclude` file at the project root: any gitignored path that matches a `.worktreeinclude` pattern is copied into the new worktree at creation time ([Claude Code worktree docs](https://code.claude.com/docs/en/worktrees)). Only gitignored files match — tracked files are never duplicated.
- Without this file, every new worktree starts from `npm install` (or equivalent). At ten worktrees that's ten cold installs unless you cache.

### 1.3 Branch ownership per worktree

A given branch may be checked out in **at most one worktree at a time**. Attempting a second checkout fails with `fatal: '<branch>' is already checked out at '<path>'` ([git-worktree(1)](https://git-scm.com/docs/git-worktree); confirmed across numerous production reports). The reason is correctness: two worktrees on one branch would have independent indexes and could create divergent staging states the refs cannot reconcile.

Practical consequence for parallel agents: every agent needs its own branch. The cheapest convention is `agent/<session-id>/<slug>` or `wt/<n>-<slug>`. Branch-naming discipline is not aesthetics here — it's a precondition for the worktree commands not failing.

The escape hatch `--force` exists; do not use it for parallel agents. It silently breaks the invariant Git relies on.

### 1.4 Stash is per-worktree

`git stash` operates on the current worktree's index and working tree only. Stashes are stored in `refs/stash` *inside the worktree's per-worktree refs namespace*; they do not propagate ([git-stash(1)](https://git-scm.com/docs/git-stash)). For agents this is almost always what you want — one agent's mid-task stash should not be visible to another — but it does mean "I'll stash and check in the main worktree" is not a recovery path if the agent is in a linked worktree.

### 1.5 Submodule gotchas

Submodule support in worktrees is **explicitly documented as incomplete** ([git-worktree(1)](https://git-scm.com/docs/git-worktree) carries the warning). Concretely:

- Each new linked worktree starts with empty submodules. You must `git submodule update --init --recursive` per worktree.
- Submodule working trees are not shared across worktrees, so ten worktrees with a 200 MB submodule cost an extra ~2 GB.
- `git worktree remove` of a worktree containing initialised submodules typically requires `--force`.
- Submodule `.git/modules/<name>` storage *is* shared via the parent's `.git`, but the working copies are not.

If your repo uses submodules heavily, budget the extra disk and the extra wall-clock per worktree provisioning. (Well documented; see [git-lfs#2270](https://github.com/git-lfs/git-lfs/issues/2270) for the related LFS angle.)

### 1.6 LFS gotchas

Git LFS state lives in `.git/lfs/` (shared across worktrees) but LFS smudge/checkout happens per-worktree. Two documented sharp edges:

- **Double download.** Updating an LFS-tracked submodule in a new worktree has historically re-downloaded all LFS objects from the server rather than reusing the existing local cache ([git-lfs#2270](https://github.com/git-lfs/git-lfs/issues/2270)). State of fix varies by LFS version; verify before launching ten worktrees against an LFS-heavy repo.
- **`git lfs install --worktree` is missing.** LFS hook installation is per-repo, not per-worktree ([git-lfs#4152](https://github.com/git-lfs/git-lfs/issues/4152)). For most workflows this is fine; in mixed-hook environments it is a foot-gun.

### 1.7 Disk-space efficiency vs full clones

Best summarised as: **objects are shared, working trees are not**. Ten worktrees of a 500 MB repo with a 1.5 GB `node_modules` cost roughly:

- `.git/objects` shared: ~500 MB
- 10 × checked-out source files: ~5 GB
- 10 × `node_modules` (if not symlinked or cached): ~15 GB

That's ~20 GB for ten worktrees vs ~70 GB for ten full clones. The dominant cost is *not* git — it's `node_modules`, `target/`, `.venv`, browser test caches, and similar. A shared package cache (`pnpm store`, `uv cache`, `cargo` target shared via `CARGO_TARGET_DIR`) is the single highest-leverage disk optimisation. (Well documented; see [gitcheatsheet.dev](https://gitcheatsheet.dev/docs/advanced/worktrees/disk-space-management/).)

### 1.8 The `--detach` pattern for ephemeral worktrees

`git worktree add --detach <path> <commit>` creates a worktree with detached HEAD at a specific commit, owning no branch. Two uses:

- **Read-only inspection.** "Check out v1.4.2 and run the perf suite" without consuming a branch slot.
- **Throwaway agent runs.** When an agent is exploring (not committing), detached HEAD is cleaner: nothing to clean up in refs, just `git worktree remove`.

For ten parallel *productive* sessions you almost always want named branches (so the work is recoverable), but for an *eleventh* read-only "inspector" worktree the detached pattern is ideal.

---

## 2. Worktree + Claude Code specifically

### 2.1 Native `EnterWorktree` / `ExitWorktree`

Claude Code shipped built-in worktree primitives in v2.1.72: the model-callable tools `EnterWorktree` and `ExitWorktree`, plus the corresponding CLI `-w` flag and a `WorktreeCreate` hook event ([Claude Code worktrees](https://code.claude.com/docs/en/worktrees); [anthropics/claude-code#29436](https://github.com/anthropics/claude-code/issues/29436)).

Behaviour, in plain terms:

- `EnterWorktree` with `name`: creates a worktree under `<repo>/.claude/worktrees/<name>` on a new branch, switches the session's CWD into it. If no name given, generates one.
- `EnterWorktree` with `path`: switches the session into an existing worktree (the path must appear in `git worktree list`).
- `ExitWorktree` with `action: "keep"`: returns the session to the original CWD, leaves the worktree on disk.
- `ExitWorktree` with `action: "remove"`: returns and runs `git worktree remove`.

The default location `<repo>/.claude/worktrees/<name>` matters: it means the worktree is *inside* the parent repo's directory. Most file watchers, search tools, and CI scripts walking the repo will see those worktrees. Add `.claude/worktrees/` to `.gitignore`, `.dockerignore`, ESLint/Ruff/etc. ignore lists, and your editor's exclude list. (Well documented; common source of pain.)

Critical scope note: `EnterWorktree` is a **single-session** operation. It moves *the current session's* CWD into a worktree. It does **not** spawn a new Claude Code process. Ten parallel agents = ten separate `claude` processes, not ten `EnterWorktree` calls inside one process.

### 2.2 Per-worktree vs shared `.claude/`

This is the bit that trips up everyone. There are two `.claude/` directories that matter:

- `<repo-root>/.claude/` — project settings, agents, hooks, session-artifacts. **Per-worktree** in the sense that each worktree has its own copy of files on disk, but they originate from the same git history and so they are identical at branch-out time. Worktree-local edits to `.claude/settings.local.json` or session artifacts are per-worktree.
- `~/.claude/` — user-global config, OAuth credentials, MCP server configs (user scope), and *crucially* `~/.claude/projects/<encoded-path>/<session-uuid>.jsonl` transcript files. **Globally shared**. ([Claude Code settings docs](https://code.claude.com/docs/en/settings).)

For ten worktrees of the same repo, the `~/.claude/projects/` directory key is derived from the absolute path. Each worktree's CWD is a different absolute path (`<repo>/.claude/worktrees/<name>`), so each worktree's Claude session writes its transcripts into a *different* project directory. The session UUIDs do not collide because they are unique per Claude process. The directory tree under `~/.claude/projects/` does balloon — one subdirectory per worktree path — which is fine until you decide to garbage-collect old worktrees and forget to clean up the matching `~/.claude/projects/` entry. (Documented; see [thedotmack/claude-mem#1276](https://github.com/thedotmack/claude-mem/issues/1276) for a worktree-CWD-normalisation bug class.)

### 2.3 Hook execution context in worktrees

A hook fires with these environment hints ([Claude Code hooks reference](https://code.claude.com/docs/en/hooks)):

- `cwd` (input field): the session's current working directory — i.e. the worktree path when running in a worktree.
- `CLAUDE_PROJECT_DIR` (env var): the project root as Claude sees it. In a worktree this is **the worktree path**, not the parent repo.
- `session_id`, `transcript_path`, `hook_event_name`, plus v2.1.69+ `agent_id`/`agent_type` for subagent context.
- `WorktreeCreate` event payload includes the worktree `name` and the parent `cwd`.

Implication for diagnostics tooling: if your hook computes "where do I write session artifacts," `CLAUDE_PROJECT_DIR` gives you the worktree, not the canonical repo. For a worktree-aware diagnostic surface (which this repo has), this is exactly right — each worktree gets its own `.claude/session-artifacts/`. For something like a shared lockfile or a shared metric counter, you must intentionally walk *up* from `CLAUDE_PROJECT_DIR` to the parent repo, using `git rev-parse --git-common-dir` to find the shared `.git` and from there the parent worktree (`git worktree list --porcelain` and pick the entry without `bare` and without a worktree path equal to `CLAUDE_PROJECT_DIR`).

A documented production failure pattern from [thedotmack/claude-mem#1276](https://github.com/thedotmack/claude-mem/issues/1276): a `Stop` hook hardcoded `CLAUDE_PROJECT_DIR` as the place to write state, then errored when it found itself inside `.claude/worktrees/<name>` instead of the canonical repo. The fix is exactly the walk-up described above.

### 2.4 MCP server scoping per worktree

MCP servers have three scope levels ([Claude Code settings](https://code.claude.com/docs/en/settings); [developersdigest MCP scopes guide](https://www.developersdigest.tech/guides/mcp-installation-scopes)):

- **User scope** — `~/.claude.json`. Loaded everywhere, including every worktree. Stateful MCP servers in user scope are shared across all ten sessions and serialise/contend accordingly.
- **Project scope** — `.mcp.json` at repo root, committed to git. Identical in every worktree.
- **Local scope** — `~/.claude.json`, keyed by project path. Because every worktree has a distinct absolute path, local-scope MCPs are *de facto* per-worktree.

Practical guidance: anything stateful (a database-backed MCP server, a server that holds file locks, a server that owns a port) must either be configured local-scope so each worktree spins up its own copy, or designed to be safely concurrent. The default of user-scope works for read-only or stateless MCPs and fails for the others.

### 2.5 Session UUID per Claude Code instance

Each `claude` process gets its own session UUID. Transcripts live at `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl`. Ten parallel sessions = ten UUIDs = ten jsonl files. The files do not collide because UUIDs are globally unique; the *directory* may be shared (if two sessions ran in the same CWD sequentially) or distinct (if each ran in its own worktree). For ten worktrees the directories are distinct.

For aggregation: `find ~/.claude/projects -name '*.jsonl' -newer <timestamp>` gives you every session that ran since you started the batch.

### 2.6 Conflicts when worktrees touch shared canonical locations

Anywhere two sessions write to the same path is a race:

- `~/.claude.json` — Claude Code does mediate concurrent writes, but a corrupted file is a documented (rare) failure mode under heavy parallel session start. Take a backup before launching the batch.
- `~/.claude/projects/<shared-dir>/` — same dir is fine, same UUID is not (and won't happen).
- `.git/objects` — Git's pack writer is concurrent-safe for adds; aggressive `git gc` from one worktree while others are writing is not. Disable `gc.auto` during a parallel run (`git config gc.auto 0` at the repo level), run `git gc` once at end.
- `.git/index.lock` — per-worktree, not contended.
- `.git/HEAD` — per-worktree.
- `.git/packed-refs` — shared and under a lock. Ten concurrent branch creations are fine; sustained ref churn under thousands of concurrent updates is the kind of edge case you'd only hit in CI bot fleets.

---

## 3. Process and environment isolation patterns

Worktrees give you code isolation. The rest you build.

### 3.1 Port collisions

The single most common failure mode in parallel-agent setups ([Penligent: runtime isolation](https://www.penligent.ai/hackinglabs/git-worktrees-need-runtime-isolation-for-parallel-ai-agent-development/); [Augusto Chirico, "Claude Code Loves Worktrees. Your Infrastructure Doesn't"](https://dev.to/augusto_chirico/claude-code-loves-worktrees-your-infrastructure-doesnt-kfi)). Patterns:

- **Hash worktree name → port offset.** Conductor and Workmux use this; deterministic, reproducible, simple. `PORT=$((3000 + $(echo $WT | cksum | cut -d' ' -f1) % 1000))`.
- **`port-selector` / dynamic claim.** A small daemon (or even a per-worktree `direnv`-loaded shell function) picks the next free port in a range, holds it for a freeze window so parallel starts don't both pick the same one. (Well documented; see [dapi/port-selector](https://github.com/dapi/port-selector).)
- **Bind to `0` and discover.** Have the dev server bind to ephemeral port and write the chosen port to a worktree-local file the test runner reads.

### 3.2 Database isolation

Three regimes:

- **SQLite file-per-worktree.** Trivial isolation. The path goes in `.env`, which is per-worktree (via `.worktreeinclude` or `direnv`).
- **Shared Postgres / shared MySQL.** One DB per worktree, named `app_dev_wt_<name>`. A provisioning script runs `CREATE DATABASE` on worktree creation and `DROP DATABASE` on teardown. Cheap until ten parallel runs of "drop and reload fixtures" thrash the WAL.
- **Container-per-worktree DB.** Docker Compose with `${WT_NAME}` in the service names. Heaviest isolation, cleanest teardown, most resource cost. Worth it at ten worktrees for anything other than SQLite.

The anti-pattern is the trivial one: **one shared `.env` with one shared `DATABASE_URL`**. Ten agents migrating, seeding, and rolling back against the same database produce non-deterministic test results and, occasionally, schema corruption. This is the single biggest "silently broken" mode.

### 3.3 Test runner conflicts

- **pytest** — `tmp_path` and `tmp_path_factory` are per-test, but `--basetemp` defaults to a shared location; set `PYTEST_DEBUG_TEMPROOT` per worktree or accept that tmpdirs are auto-isolated by PID.
- **jest** — snapshots are committed (good), but `--cache` defaults to `/tmp/jest_*` keyed by Jest's hash of config + node version + CWD. Distinct CWDs (one per worktree) means distinct cache dirs, so usually safe. The failure mode is custom resolvers that bake in absolute paths.
- **Playwright / browser tests** — every browser instance wants its own port for the test server *and* the inspector. Without isolation, ten parallel Playwright runs fight over ports 9222–9229. Use `PWDEBUG=0` and pass `--port=0` or hash-derived ports.
- **Hot-reload watchers** — `webpack-dev-server`, `vite`, `next dev` all open inotify watches.

### 3.4 Environment variable inheritance

Each Claude Code process inherits the launching shell's env. If you launch ten sessions from one terminal session, they share env at start. After that, each is independent.

The clean pattern: `direnv` or `mise` per worktree, so `cd <worktree>` triggers a load of worktree-specific env. The `.envrc` or `mise.toml` is gitignored and templated by your provisioning script. ([mise-en-place](https://mise.jdx.dev/) is the 2026 incumbent for this; direnv is the older battle-tested option.)

### 3.5 Background process management

Orphaned `npm run dev` processes from a terminated agent session are *the* long-tail problem at ten worktrees. The agent terminates; the dev server it started keeps holding port 3413 and a chunk of memory. After a day of iteration you have 40 zombie node processes and 3 GB of leaked memory.

Mitigations:

- Launch dev servers under a process supervisor (`tmux` window, `pm2`, `systemd --user`) keyed by worktree name. Teardown kills the named group.
- `setsid` + a tracked PID file in `.claude/worktree-state/<name>.pids`.
- The Claude Squad model: each agent runs inside a tmux session named for the worktree; `tmux kill-session -t <name>` cleans everything ([smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)).

### 3.6 Container / Docker per worktree

Heaviest isolation, cleanest. One Docker Compose project per worktree, project name set from the worktree name (`docker compose -p <wt> up`). Networks, volumes, container names all namespaced. Trade-offs: ten Compose stacks costs noticeable RAM (each Postgres easily 200 MB+ resident), and Docker Desktop on macOS has documented file-watch / bind-mount perf cliffs that hit hard with ten concurrent stacks.

[DevTree](https://github.com/pwrmind/DevTree) and Conductor both lean into this model. The [devcontainers/cli#796](https://github.com/devcontainers/cli/issues/796) issue is the canonical "devcontainers + worktrees has rough edges" tracker — main pain is that worktrees use a `.git` file (pointer) rather than a `.git` directory, and some devcontainer setups assume the latter.

### 3.7 direnv / asdf / mise per-worktree activation

Strong recommendation: use one of these. Pin tool versions, env vars, and port offsets per worktree. The `.envrc` / `mise.toml` is gitignored and emitted at provisioning time from a template. The single biggest source-of-truth file looks like:

```
WT_NAME=feat-search-rerank
WT_PORT_BASE=3140
DATABASE_URL=postgresql://localhost/app_dev_${WT_NAME}
REDIS_URL=redis://localhost:6379/3
PLAYWRIGHT_BROWSERS_PATH=$XDG_CACHE_HOME/playwright
```

`PLAYWRIGHT_BROWSERS_PATH` is the kind of thing you push *out* of the worktree (to a shared cache) to save disk. `DATABASE_URL` you keep *in* the worktree (per-WT isolation). Knowing which is which is the entire isolation game.

---

## 4. Resource contention

### 4.1 CPU + memory

Ten Claude Code sessions, each potentially holding a couple-hundred-thousand-token context plus a transcript, plus ten dev servers, plus a test runner per worktree, plus maybe a browser per worktree — easily 32 GB RAM at idle, way more under test load. Empirical reports converge on **"5+ concurrent sessions on a large codebase becomes hard to review"** ([codewithseb](https://www.codewithseb.com/blog/parallel-claude-code-sessions-git-worktrees-guide), [mindstudio](https://www.mindstudio.ai/blog/claude-code-git-worktree-parallel-branches)). For ten you want a machine where 64 GB is the floor.

CPU contention is less of a binder because LLM calls are mostly waiting on the API, not on local CPU. Test runs and builds are the CPU killers. Stagger them (don't `npm test` in all ten worktrees at the same instant) and you stay alive.

### 4.2 File descriptor limits

macOS default `ulimit -n` is 256 (per process) and 4864 (system). Linux defaults vary. Ten Claude sessions + ten dev servers + ten Postgres clients + watchers can collectively chew 5–10k fds without trying hard. `ulimit -n 65536` in your shell rc, or per-session, is cheap insurance. (Well documented across Node/Playwright communities.)

### 4.3 Inotify limits (Linux)

The default `fs.inotify.max_user_watches` on many distros is 8192, with `max_user_instances` typically 128 ([Watchexec inotify limits reference](https://watchexec.github.io/docs/inotify-limits.html); [Baeldung on inotify](https://www.baeldung.com/linux/inotify-upper-limit-reached)). Limits are per-user, not per-process. Ten worktrees × Vite watcher × ~3000 files per project saturates 30k watches; you'll see "ENOSPC: System limit for number of file watchers reached" from the file watchers. Bump to 524288:

```
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
echo fs.inotify.max_user_instances=512 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

On macOS the equivalent is FSEvents, which doesn't have the same hard cap but has its own scaling cliffs around the count of watched paths. Excluding `.claude/worktrees/` from editor watchers helps.

### 4.4 API rate limits

Per the May 2026 [Anthropic post on rate-limit increases](https://letsdatascience.com/news/anthropic-increases-claude-code-and-api-usage-limits-735fd0ac), Claude Opus Tier 1 went from 30k input tokens/min to ~348k. At ten parallel sessions averaging ~50k context per call and a call every ~15s, you're at roughly 200k input TPM — comfortably under Tier 1 post-increase, tight on pre-increase Tier 1. Output limits scaled similarly.

The remaining failure mode is **burst** — ten sessions all firing a first call within the same second. The Anthropic 429 backoff is well behaved if your tooling respects it. See [anthropics/claude-code#46037](https://github.com/anthropics/claude-code/issues/46037) for documented bursting issues with multiple parallel sessions under sub-cap usage. Stagger session starts by a few seconds each and the bursting goes away.

### 4.5 Disk I/O contention

Ten cold `npm install` runs are an I/O event. Use `pnpm` with a shared store, `uv` with shared cache, or `nix`/`devbox` for fully shared toolchain. The npm-style "every project gets its own `node_modules`" model is the worst case at ten worktrees.

---

## 5. Coordination patterns

Most of the time you want **none**. The win of parallel agents is independence. When coordination is unavoidable:

- **Lock files** — `flock(1)` on a path under `<repo>/.claude/locks/<resource>`. Stale-lock hygiene matters (write PID + timestamp; expire on stale PID).
- **Shared state** — push into a single MCP server with its own concurrency model, not into the filesystem. Filesystem-based coordination between ten agents on the same repo race in subtle ways.
- **Conflict detection at merge time** — let agents conflict in their own branches, resolve at merge. Cheap. Modern PR queues (Aviator, Mergify, GH merge queue) handle the batching.
- **Branch-naming conventions** — `wt/<n>-<short-slug>` keyed by session. Prevents two agents grabbing the same branch name on race.

A useful convention from [Conductor](https://www.conductor.build/) and [Claude Squad](https://github.com/smtg-ai/claude-squad): **scope worktrees by module, not by task.** Two tasks both editing `src/auth/` go in *one* worktree, sequentially. Two tasks editing disjoint modules go in two worktrees, in parallel. This pushes merge-conflict probability toward zero, at the cost of some serialisation.

---

## 6. Existing tooling for parallel AI worktree workflows

The 2026 ecosystem clusters into four camps:

**TUI multi-session managers (open source).** [Claude Squad (smtg-ai/claude-squad)](https://github.com/smtg-ai/claude-squad) — Go-based TUI, tmux for terminal isolation, git worktrees for code, supports Claude Code / Codex / Aider / Gemini. ~6.8k GitHub stars at time of writing. Dashboard for spawn / monitor / pause / resume / merge. The closest-to-production option for "manage ten agents from one screen." Has an open feature request ([smtg-ai/claude-squad#260](https://github.com/smtg-ai/claude-squad/issues/260)) for environment setup hooks (per-worktree `.env`, port isolation) — confirming that even the leading TUI tool punts the runtime-isolation problem to the user.

**Mac-native orchestrators (commercial-feeling, free).** [Conductor (Melty Labs)](https://www.conductor.build/) — macOS app from the YC S24 team that built Melty. Automates git worktree management end-to-end, generates per-workspace `.env.local`, supports checkpoints/rollback, multi-model mode (Claude + Codex on same prompt for comparison), spotlight testing to sync back to main repo. Trade-off: gave up a chunk of community goodwill in mid-2025 over GitHub permissions scope ([BigGo News coverage](https://biggo.com/news/202507210115_Conductor_App_GitHub_Permissions_Controversy)), worth knowing if you care about the supply chain.

**Multi-agent orchestration frameworks.** [ccswarm (nwiizo/ccswarm)](https://github.com/nwiizo/ccswarm) — Rust-native, specialised agent pools (Frontend / Backend / DevOps / QA / Security), Master-Claude proactive task generation, Git worktree isolation throughout. Heavier-weight than Squad; aimed at teams running structured multi-role workflows rather than ten parallel features.

**Adjacent / smaller.** [bucket-robotics/claude-worktree](https://github.com/bucket-robotics/claude-worktree) (TUI for plain `git worktree` mgmt, Claude-Code-flavoured). [raine/workmux](https://github.com/raine/workmux) (worktrees + tmux windows, per-worktree port allocation via direnv). [Upsun's devcenter post](https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/) on hosting parallel agents on PaaS environments. GitHub Codespaces + devcontainer-per-worktree is *possible* but practical limitations from [devcontainers/cli#796](https://github.com/devcontainers/cli/issues/796) remain.

For "I want to start tomorrow with ten worktrees of one local repo," the **realistic 2026 picks** are:

1. **Roll-your-own with native Claude Code `EnterWorktree` + tmux + direnv + a provisioning script.** Most control, least magic.
2. **Claude Squad** — saves writing the TUI; you still write the per-worktree env hooks.
3. **Conductor** — most polish if you're macOS-only and OK with the trust trade-off.

---

## 7. Failure modes from production reports

Distilled from blog posts, issue trackers, and `claude-code` issues:

**Two worktrees editing the same file at the same time** — does *not* corrupt the repo (each worktree has its own working copy and index), but it produces silent divergence: agent A and agent B both edit `src/auth/session.ts`, both commit, both branches merge cleanly into main individually. The merge of B into main after A creates the conflict. The failure is **late detection**, not data loss. Mitigation is module-scoped worktree assignment (§5) plus a pre-merge `git fetch && git rebase main` in every worktree.

**Conflicting branch creation** — two simultaneous `EnterWorktree` calls with no name argument occasionally generated the same random name in older Claude Code versions; fixed by v2.1.72+. With explicit names (recommended), not a problem.

**Stale-cache effects** — Jest `--cache`, Vite dep optimiser cache, Next.js `.next/`, Vitest cache, all key on CWD + config hash. Usually safe across worktrees because CWDs differ. The exception is *shared* caches you set up intentionally (e.g. `CARGO_TARGET_DIR=/shared/target`) — at ten concurrent builds these are the easiest way to corrupt artifacts. Either use a shared cache that supports concurrent access (sccache, ccache, pnpm store) or keep build outputs per-worktree.

**Memory exhaustion from N concurrent LLM streams** — Claude Code's transcript writer is streaming, not buffered-in-RAM, so per-session memory is bounded. The risk is *N × dev-server-with-watcher* under test load. Reports from heavy users converge on "10 worktrees on 32 GB is unstable, 64 GB is fine, 128 GB is comfortable."

**`~/.claude.json` corruption under heavy parallel writes** — rare, documented in scattered issues, mitigated by Claude Code's internal locking but worth a backup before launching a ten-session batch.

**Hook context-confusion in worktrees** — e.g. [thedotmack/claude-mem#1276](https://github.com/thedotmack/claude-mem/issues/1276), where a `Stop` hook hardcoded the parent project dir and failed when CWD was inside `.claude/worktrees/<name>`. Pattern: any hook that writes to "the project root" must `git rev-parse --show-toplevel` first to find the worktree root, and walk up via `git rev-parse --git-common-dir` if it wants the canonical repo.

---

## 8. Concrete recipe: ten Claude Code sessions on one repo

This section is the "if you implement nothing else, implement this" minimal recipe.

### 8.1 Pre-flight

Before launching the batch:

1. **Bump system limits.** `ulimit -n 65536` in shell rc. On Linux, `fs.inotify.max_user_watches=524288`, `fs.inotify.max_user_instances=512`.
2. **Disable repo-level auto-gc during the batch.** `git config gc.auto 0`.
3. **Back up `~/.claude.json`** to a timestamped copy.
4. **Provision shared caches.** `pnpm config set store-dir ~/.cache/pnpm`, `CARGO_TARGET_DIR=~/.cache/cargo-target` (if all branches are compat), `PLAYWRIGHT_BROWSERS_PATH=~/.cache/playwright`.
5. **Confirm API rate-limit headroom.** Tier ≥ 1 with the May 2026 increases is fine for ten sessions; lower tiers will throttle.
6. **Create a `.worktreeinclude`** at repo root listing the gitignored files each new worktree should inherit (typically `.env`, `.envrc`, `mise.toml`).

### 8.2 Worktree provisioning script template

```bash
#!/usr/bin/env bash
# bin/wt-provision <slug>
set -euo pipefail
slug="${1:?slug required}"
name="wt-${slug}"
branch="agent/${slug}"
repo_root=$(git rev-parse --show-toplevel)
wt_path="${repo_root}/.claude/worktrees/${name}"

# Hash-derived port base (collision-resistant for ~hundreds of worktrees)
port_base=$((3000 + 0x$(printf '%s' "$name" | md5sum | cut -c1-4) % 1000))

git worktree add -b "$branch" "$wt_path"

# Per-worktree env (gitignored)
cat > "$wt_path/.envrc" <<EOF
export WT_NAME="${name}"
export PORT="${port_base}"
export DATABASE_URL="postgresql://localhost/app_dev_${name}"
export REDIS_URL="redis://localhost:6379/$((port_base % 16))"
export PLAYWRIGHT_BROWSERS_PATH="\$HOME/.cache/playwright"
EOF

# Per-worktree DB
createdb "app_dev_${name}" 2>/dev/null || true

# Install deps (pnpm uses the shared store)
(cd "$wt_path" && direnv allow && pnpm install --prefer-offline)

# Launch under a named tmux window
tmux new-window -n "$name" -c "$wt_path" "direnv exec . claude"
```

Call this ten times with ten slugs. Each call: ~5–15 seconds for `git worktree add` + `createdb` + `pnpm install` (with warm pnpm store). Cold install dominates.

### 8.3 Per-worktree environment isolation

Layout that holds at ten:

```
<repo>/
  .claude/
    worktrees/                  # gitignored; provisioning target
      wt-feat-search-rerank/
        .envrc                  # generated per wt
        .git                    # pointer file
        ...working files...
    locks/                      # cross-wt flock targets
    worktree-state/             # per-wt PID files, port reservations
  .worktreeinclude              # tells Claude what to copy in
  mise.toml                     # tool versions (shared)
```

`~/.cache/` holds: pnpm store, cargo target, Playwright browsers, uv cache. Shared, read-write, but only one writer per package — pnpm/cargo handle this.

### 8.4 Cleanup / teardown

```bash
#!/usr/bin/env bash
# bin/wt-teardown <slug>
set -euo pipefail
slug="${1:?slug required}"
name="wt-${slug}"
repo_root=$(git rev-parse --show-toplevel)
wt_path="${repo_root}/.claude/worktrees/${name}"

# Kill the tmux window (kills dev server, watchers, the claude process)
tmux kill-window -t "$name" 2>/dev/null || true

# Drop the per-wt DB
dropdb "app_dev_${name}" 2>/dev/null || true

# Remove worktree (force only if you're sure)
git worktree remove "$wt_path" || git worktree remove --force "$wt_path"

# Clean ~/.claude/projects/ entry for this worktree
project_key=$(printf '%s' "$wt_path" | tr '/' '-')
rm -rf "$HOME/.claude/projects/${project_key}"
```

The `~/.claude/projects/` cleanup is the one most people miss; it accumulates indefinitely otherwise.

### 8.5 Aggregation: merging findings from ten worktrees back to main

The minimum pipeline:

1. **Each worktree's session writes its artifacts under `<wt>/.claude/session-artifacts/<session-id>/`.** Per the 12-step workflow in this repo, this includes a `synthesis.md` and a `ledger.md`.
2. **A `bin/wt-aggregate` script** walks every worktree (`git worktree list --porcelain`), collects each worktree's latest `synthesis.md` + `ledger.md` into a single `aggregate/<batch-id>/` directory on a dedicated `agent-batch/<batch-id>` branch on the main worktree.
3. **For code changes:** each worktree's branch is independent. A merge queue (GH merge queue, Aviator, Mergify) batches them. Pre-merge, every branch rebases on `main` to surface conflicts early. Branches that fail rebase block on a human; the rest auto-merge.
4. **For diagnostics / metrics** (if you have a `.claude/.metrics` surface as this repo does): a final `bin/wt-metrics-aggregate` step sums per-worktree metric files into a single rollup on `main`. This is a glorified `jq -s 'add'` if your metric files are arrays.

The aggregation script is independent of the agent layer. It runs on the main worktree, with no agent in the loop, after all ten sessions have written `synthesis.md`. That separation is load-bearing: an agent merging its own work into main is the documented worst category of agent failure.

---

## 9. Anti-patterns

In rough order of badness at ten worktrees:

- **One shared `.env` with one `DATABASE_URL` across all worktrees.** Tests are non-deterministic; schema corruption is possible; you will not realise for hours.
- **Letting test ports collide.** Cascade of false-negative test failures, intermittent in a way that defeats `--rerun-failed`.
- **Forgetting `~/.claude/projects/<encoded-cwd>/` accumulates.** After a month of ten-worktree runs you have hundreds of MB of `.jsonl` and a slow `claude` startup.
- **Running `git worktree add --force` to bypass branch-conflict errors.** You wanted the error; it told you two agents were about to fight.
- **Letting `gc.auto` run during a parallel batch.** Compaction races with concurrent writers.
- **Hooks that hardcode the parent repo path.** They break for *every* session running in a worktree. Use `git rev-parse --show-toplevel`.
- **Sharing a single user-scope MCP server that holds writable state.** Ten sessions, one server, no isolation.
- **Mounting `node_modules` shared across worktrees via symlink.** Two branches with divergent `package.json` will silently use each other's deps.
- **Skipping the pre-merge rebase.** "It merged cleanly individually" is not "it merges cleanly together."
- **Running ten dev-server `watch` modes without raising inotify limits on Linux.** Failure looks like the watcher silently stops noticing changes.

---

## 10. For this stack — checklist

This repo runs the 12-step `claude-critic-stack` workflow, with a worktree-aware `.claude/` diagnostics surface that already uses `git worktree list` for per-worktree counts. Specific guidance for the ten-worktree launch:

### 10.1 Five things that MUST be set up before launch

1. **Per-worktree branch convention.** `agent/<session-id>` or `wt/<n>-<slug>`. Without this the second `EnterWorktree` of the day collides.
2. **`.worktreeinclude` at repo root** listing `.envrc`, `mise.toml`, and any session-config-style files that should propagate into new worktrees but stay gitignored.
3. **Per-worktree DB/port/env via `direnv` or `mise`.** Hash worktree name → port base. One `DATABASE_URL` per worktree. Non-negotiable.
4. **Bumped system limits.** `ulimit -n 65536`, plus inotify bumps on Linux. Cheap; prevents the most opaque failure class.
5. **An aggregation script** in `bin/` that walks `git worktree list --porcelain`, picks up each worktree's `synthesis.md` and `ledger.md`, and emits a single rollup. The diagnostics surface is already worktree-aware; the aggregator closes the loop.

### 10.2 Three things that will silently break if not addressed

1. **Hooks that write to `CLAUDE_PROJECT_DIR` assuming it's the parent repo.** In a worktree, `CLAUDE_PROJECT_DIR` is the worktree path. A hook that wants the canonical repo must `git rev-parse --git-common-dir` and walk to the parent worktree. Audit every hook in [`.claude/`](.claude/) before launch.
2. **`~/.claude/projects/<encoded-cwd>/` accumulating.** Every worktree is a new encoded CWD. Add a teardown step that removes the matching `~/.claude/projects/` entry when a worktree is destroyed, or accept slow `claude` startup and disk creep within weeks.
3. **The ledger schema in [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md) treats `agent-calls` as a session-local count.** Ten parallel sessions each producing a ledger entry is fine *per session*, but no rollup currently sums them into a batch-level cost. If you care about "what did this batch of ten agents cost me" — not just "what did session X cost" — you need a `bin/ledger-rollup` that aggregates per-session ledgers into a batch ledger. Without it, the per-session honesty is preserved but the batch-level cost is invisible.

### 10.3 Minimum aggregation pipeline

A single `bin/wt-aggregate <batch-id>` script that:

1. `git worktree list --porcelain` → list of worktrees.
2. For each, locate the most-recent `.claude/session-artifacts/<id>/synthesis.md`. Reject any session missing the `Ledger: ...` citation line on the last line of `synthesis.md` (per the schema in [`.claude/session-artifacts/README.md`](.claude/session-artifacts/README.md)); that is a sentinel for an incomplete session and should not silently roll up.
3. Copy each `synthesis.md` and `ledger.md` into `aggregate/<batch-id>/<wt-name>/` on the main worktree's `agent-batch/<batch-id>` branch.
4. Emit `aggregate/<batch-id>/ROLLUP.md`: per-worktree one-line summary (slug, post-critique recommendation headline, ledger totals), plus a batch-level `Total: agent-calls=<sum>, artifacts=<sum>, sessions=<N>`.
5. Commit the rollup branch. Do *not* auto-merge per-worktree code branches; that's a separate decision per branch and belongs to a human or a merge queue.

That's the floor. Anything richer (cross-session conflict detection, semantic dedup of recommendations, automatic invocation of `critic-comparator` across sessions) is gravy.

---

## Sources

Primary documentation:

- [git-worktree(1)](https://git-scm.com/docs/git-worktree) — canonical reference for worktree commands, submodule/LFS caveats.
- [Claude Code: Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees) — `-w` flag, `.worktreeinclude`, `worktree.sparsePaths`.
- [Claude Code: Hooks reference](https://code.claude.com/docs/en/hooks) — `CLAUDE_PROJECT_DIR`, hook input fields, `WorktreeCreate` event.
- [Claude Code: Settings](https://code.claude.com/docs/en/settings) — MCP scopes, `~/.claude.json` layout.
- [Anthropic API rate limits](https://platform.claude.com/docs/en/api/rate-limits).

Tooling:

- [Claude Squad (smtg-ai/claude-squad)](https://github.com/smtg-ai/claude-squad) — TUI multi-session manager.
- [Conductor (Melty Labs)](https://www.conductor.build/) — macOS parallel-agent orchestrator. [The New Stack review](https://thenewstack.io/a-hands-on-review-of-conductor-an-ai-parallel-runner-app/). [GitHub permissions controversy coverage](https://biggo.com/news/202507210115_Conductor_App_GitHub_Permissions_Controversy).
- [ccswarm (nwiizo/ccswarm)](https://github.com/nwiizo/ccswarm) — multi-agent orchestration framework with role specialisation.
- [bucket-robotics/claude-worktree](https://github.com/bucket-robotics/claude-worktree) — TUI for git-worktree mgmt.
- [raine/workmux](https://github.com/raine/workmux) — git worktrees + tmux + direnv port allocation.
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/tool-description-enterworktree.md) — extracted `EnterWorktree` tool description.
- [anthropics/claude-code#29436](https://github.com/anthropics/claude-code/issues/29436) — `ExitWorktree` design discussion.

Operational reports / blog posts:

- [Code With Seb: Parallel Claude Code Sessions with Git Worktrees](https://www.codewithseb.com/blog/parallel-claude-code-sessions-git-worktrees-guide).
- [MindStudio: Parallel Agentic Development With Git Worktrees](https://www.mindstudio.ai/blog/parallel-agentic-development-git-worktrees).
- [Augusto Chirico: Claude Code Loves Worktrees. Your Infrastructure Doesn't](https://dev.to/augusto_chirico/claude-code-loves-worktrees-your-infrastructure-doesnt-kfi).
- [Penligent: Git Worktrees Need Runtime Isolation for Parallel AI Agent Development](https://www.penligent.ai/hackinglabs/git-worktrees-need-runtime-isolation-for-parallel-ai-agent-development/).
- [Upsun: Git worktrees for parallel AI coding agents](https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/).
- [htek.dev: Git Worktree — The Infrastructure That Unlocks Agentic Development](https://htek.dev/articles/git-worktree-unlocks-agentic-development/).
- [Nicholas Henry: Building Isolated Phoenix Workspaces for AI Agents with Conductor](https://nicholasjhenry.medium.com/building-isolated-phoenix-workspaces-for-ai-agents-with-conductor-a438d161f191).
- [Addy Osmani: Conductors to Orchestrators — The Future of Agentic Coding](https://addyosmani.com/blog/future-agentic-coding/).
- [gitcheatsheet.dev: Disk Space Management for Git Worktrees](https://gitcheatsheet.dev/docs/advanced/worktrees/disk-space-management/).

Known failure-mode tickets:

- [git-lfs/git-lfs#2270](https://github.com/git-lfs/git-lfs/issues/2270) — LFS double-download in worktrees with submodules.
- [git-lfs/git-lfs#4152](https://github.com/git-lfs/git-lfs/issues/4152) — missing `git lfs install --worktree`.
- [anthropics/claude-code#46037](https://github.com/anthropics/claude-code/issues/46037) — 429 under multiple parallel sessions below cap.
- [thedotmack/claude-mem#1276](https://github.com/thedotmack/claude-mem/issues/1276), [#1235](https://github.com/thedotmack/claude-mem/issues/1235) — Stop-hook failures when running in a worktree.
- [smtg-ai/claude-squad#260](https://github.com/smtg-ai/claude-squad/issues/260) — worktree environment setup hook feature request.
- [devcontainers/cli#796](https://github.com/devcontainers/cli/issues/796) — devcontainer + worktree compatibility.

System-limits references:

- [Watchexec: Linux inotify limits](https://watchexec.github.io/docs/inotify-limits.html).
- [Baeldung: inotify upper limit reached](https://www.baeldung.com/linux/inotify-upper-limit-reached).
