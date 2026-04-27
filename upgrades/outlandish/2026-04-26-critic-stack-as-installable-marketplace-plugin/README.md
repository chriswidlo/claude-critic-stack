# Critic-stack as installable marketplace plugin

| Field | Value |
|---|---|
| 📌 **title** | Critic-stack as installable marketplace plugin |
| 🎯 **tier** | 🚀 outlandish |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The casual reply about forrestchang/andrej-karpathy-skills repeatedly noted that the *plugin packaging mechanism* — distributing CLAUDE.md content as an installable Claude Code marketplace plugin — was the more interesting lesson than the file's content. The workflow then ran its full course, and the observation kept reappearing: *we just spent eleven steps evaluating a tiny artifact whose distribution mechanism is more novel than its content. We have a 12-step adversarial-review stack. We have not packaged it as a plugin. The lesson we keep flagging in others is the lesson we have not applied to ourselves.* |
| 💡 **essence** | The claude-critic-stack — the 12-step workflow, the eight specialized agents, the canon corpus, the lab — is currently a single-user repo that operates only when the user `cd`s into this directory. Packaging it as an installable Claude Code marketplace plugin would let it run anywhere: on any user's machine, in any repo, invoked by anyone. The conventions that took months to develop become reusable. The workflow stops being one user's discipline and becomes a public artifact others can extend, fork, criticize. The mechanism the karpathy plugin demonstrated for a 50-line CLAUDE.md, applied to a substantively novel epistemic apparatus. |
| 🚀 **upgrade** | A long-arc project: refactor the repo into a marketplace-installable plugin. `.claude-plugin/plugin.json` declaring the agents, skills, and slash commands. A `marketplace.json` for distribution. Documentation that explains the workflow to a first-time user. A clear separation between user-specific content (the canon corpus, the lab, the session artifacts) and the redistributable workflow itself. The result: someone runs `claude plugin install <name>` and gets the 12-step workflow as a usable capability in any repo. |
| 🏷️ **tags** | distribution, plugin-mechanism, public-artifact, eat-our-own-dog-food |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The observation that triggered this](#the-observation-that-triggered-this)
- [What the plugin would contain](#what-the-plugin-would-contain)
- [What it would not contain](#what-it-would-not-contain)
- [The hard problems](#the-hard-problems)
- [Why this is outlandish, not no-brainer](#why-this-is-outlandish-not-no-brainer)
- [What success would look like](#what-success-would-look-like)
- [The risk of doing it](#the-risk-of-doing-it)

## The observation that triggered this

The user pointed at a community plugin (forrestchang/andrej-karpathy-skills) that bundles a tiny behavioral CLAUDE.md as an installable marketplace plugin. The orchestrator's casual reply repeatedly highlighted: *the packaging mechanism is the lesson, not the content*. The plugin mechanism is novel; the content is not.

Then the workflow ran. Eleven steps. Three subagents in parallel. A critic panel of three lenses. A rewrite loop. All of this lives in `claude-critic-stack/`, accessible only to the user, only when the user is in this directory. The workflow that produced eleven steps of careful evaluation cannot be invoked anywhere else.

The mismatch is sharp. The tiny artifact (karpathy file) has the distribution mechanism. The substantive artifact (this stack) does not.

This entry asks: what would it look like to flip that?

## What the plugin would contain

The Claude Code marketplace plugin format (per the karpathy repo's structure and what the user can fetch from current docs) supports:
- `.claude-plugin/plugin.json` — manifest declaring the plugin's name, version, description, included skills, included agents, and slash commands.
- `.claude-plugin/marketplace.json` — distribution metadata (owner, plugins listed, categories).
- `agents/` — agent definitions that get installed into the user's global agents directory (or invoked via plugin scope).
- `skills/` — skill definitions, each with a `SKILL.md`.
- `commands/` — slash commands the plugin exposes.
- Optional: hooks, MCP server declarations, custom statusline templates.

The critic-stack maps onto this cleanly:
- The eight specialized agents (`canon-librarian`, `outside-view`, `scope-mapper`, `frame-challenger`, `subagent-distiller`, `critic-architecture`, `critic-operations`, `critic-product`, plus `requirement-classifier`, `canon-refresher`) → `agents/`.
- The 12-step workflow's invocation logic → either a slash command (`/critic-stack` or similar) that the orchestrator triggers, or a top-level `CLAUDE.md` snippet the plugin ships and the user opts into.
- The `/upgrade` slash command and lab discipline → a separate optional skill the plugin ships.
- The `outside-view`, `canon-librarian` etc. dispositions → a `claude-critic-stack-guidelines` skill that loads when the user is doing design work.

A minimal first version could ship just the agents and the workflow's invocation logic, without the canon corpus or lab.

## What it would not contain

Several things in the current repo are user-specific and would not redistribute:
- The `canon/corpus/` content — this is a curated, user-specific knowledge base. Other users would have their own corpus. The plugin would ship the *librarian agent and corpus structure*, not the user's specific entries.
- The `upgrades/` lab — this is one user's research notebook. The plugin would ship the lab's *structure, README, and slash command*, not specific entries.
- The `.claude/session-artifacts/` — these are per-session and per-user.
- User-specific memory under `memory/`.

The clean separation: the plugin distributes *the apparatus*. Each user populates *the content* themselves.

## The hard problems

This is outlandish because several real problems sit in the way:

1. **Plugin scope vs. user agents.** The user already has seven global agents installed. A plugin that ships ten more agents creates name collisions, attribution confusion, and the silent-overlap-induced drift that the outside-view subagent has flagged as the modal failure of community-plugin adoption. The plugin needs a namespacing mechanism Claude Code may or may not provide cleanly.

2. **Workflow logic as plugin content.** The current workflow logic lives in this repo's `CLAUDE.md`. A plugin's CLAUDE.md is the user's project file, not Anthropic-supplied behavior. Either the plugin must ship a CLAUDE.md that the user explicitly merges, or the workflow must be invocable via a slash command that does not depend on the user's CLAUDE.md being modified. The latter is cleaner.

3. **The hard gates.** The workflow has hard gates ("don't proceed without scope-map.md and challenges.md"). Hard gates rely on file-system state under `.claude/session-artifacts/`. Whether a plugin can enforce this in another user's repo is open.

4. **Versioning and updates.** The plugin would ship to many users; updates would change agent contracts. This is the maintenance-asymmetry failure mode the outside-view named (the user must accept upstream changes silently, or pin a version and lose updates). The current repo's solution is that there are no users — the user is the maintainer. Distributing changes that.

5. **Audience and onboarding.** The current repo assumes the user has internalized the workflow's discipline ("do not be agreeable", "do not skip the outside view"). New plugin users will not have that internalization. The plugin needs an onboarding path that explains the discipline — which is currently 250 lines of CLAUDE.md prose. That does not transfer cleanly.

6. **Will anyone use it.** The market for "12-step adversarial-review workflows for design questions" is unknown. The plugin could ship and find that the audience is one (the original user). The cost of building is real; the cost of maintaining a published plugin is higher than maintaining a private repo.

## Why this is outlandish, not no-brainer

The packaging mechanism itself is not hard — the karpathy plugin is 7 small files. The hard part is everything around it: namespacing, onboarding, versioning, audience. These are months of work, not 30 minutes. The right tier is outlandish: ambitious, long-timeline, possibly impractical, exciting in scope.

The decision rule from the lab README ("when in doubt between two tiers, default to the lower one") would push toward `normal`. But the scope here is genuinely large — refactoring the repo's structure, separating apparatus from content, writing onboarding documentation, deciding on a public-facing identity, considering name collisions with existing community plugins. That is months, not days. Outlandish stands.

## What success would look like

In the success case:
- A user runs `claude plugin install claude-critic-stack` in a fresh repo.
- They invoke `/critic-review <design question>` and the workflow runs.
- The 12 steps execute, the critic panel runs, the synthesis appears.
- They get the same epistemic discipline this user gets, without having to read 8000 lines of CLAUDE.md and agent definitions.
- They begin populating their own canon corpus, their own lab, their own session artifacts — the apparatus is shared, the content is theirs.
- After a year, there is a small community of users running the workflow, contributing back to the agent definitions, finding edge cases.

In the modest-success case: the plugin exists, the original user uses it across multiple repos instead of having to `cd` into this one, and that single benefit alone is worth the work.

In the failure case: the plugin ships, no one uses it, the maintenance burden of a public artifact exceeds the value of the personal-use convenience, the project is archived. Cost: months of refactoring with limited downstream benefit.

## The risk of doing it

The deepest risk is that publishing the workflow changes how the workflow gets used. A workflow that is "my private discipline" is honestly tuned to the user's actual decision-making. A workflow that is "my published plugin" gets pressure toward audience-friendliness, marketing, simplification, scope reduction. The discipline gets sanded down to fit the plugin marketplace's idiom (small skills, clear use cases, "drop in and it works"). The thing that made the workflow valuable (its weight, its friction, its insistence on hard gates) is exactly what makes it hard to publish.

There is a version of this entry where the right answer is "do not publish; the workflow's value is preserved by it being personal." That version deserves to be considered.

There is also a version where the right answer is "publish, but accept the workflow will mutate, and that mutation is itself a valuable forcing function." That version also deserves consideration.

This entry does not resolve which. It just notes the question is real and deserves time.
