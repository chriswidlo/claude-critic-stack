# Generator cited user-state from memory, not from Explore

| Field | Value |
|---|---|
| 📌 **title** | Generator cited user-state from memory, not from Explore |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The casual prior writeup made a load-bearing claim — *"most of the karpathy file's content is already present in your existing global CLAUDE.md"* — without ever reading the file. When the workflow's Explore step actually opened the global `CLAUDE.md`, it was 0 bytes. The prior writeup was wrong on that specific clause and the rest of its reasoning then had to be retraced under the corrected fact. |
| 💡 **essence** | The orchestrator treats user-state assertions ("your file does X", "your setup has Y") as cheap to make. They are not — they anchor every downstream argument. When the assertion comes from inferred memory rather than from a tool call against the user's actual state, it is structurally indistinguishable from a hallucination. |
| 🚀 **upgrade** | A discipline (or a sentinel pattern in the orchestrator's own pre-flight): every claim in a casual reply about user state — files the user has, contents of those files, what their existing setup covers — must either be marked "unverified, may be wrong" or be backed by a recent tool call. Not a workflow change; a casual-mode discipline. The workflow already has Explore for this; the casual mode does not. |
| 🏷️ **tags** | discipline, casual-mode, hallucination, anti-patterns |
| 🔗 **relates_to** | 2026-04-26-casual-output-is-workflow-unprotected |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The specific failure](#the-specific-failure)
- [Why the discipline is small](#why-the-discipline-is-small)
- [What the rule should say](#what-the-rule-should-say)

## The specific failure

The user asked about a community plugin. The reply was confident and structured: a tradeoff table, a per-principle assessment, a recommendation. One claim in that reply was: *most of the karpathy file's content is already in the default Claude Code system prompt and the user's existing global CLAUDE.md*.

The first half (defaults) is plausible from public knowledge. The second half (the user's CLAUDE.md) is a fact about the user's machine. The orchestrator had no source for it. It came from the unstated assumption that someone running Claude Code has a populated global config. The user's file was empty.

The cost was small here — the workflow caught it within an hour. The cost in other sessions where the workflow does not run is the relevant number, and it is unmeasured.

## Why the discipline is small

The fix is one habit: when about to assert a user-state fact, ask "did I read this in the last few turns, or am I inferring it?" If inferring, hedge or read.

The rule is small because the rate of user-state assertions per casual reply is low — maybe one to three per substantive answer. Adding "read first" or "hedge" to those few claims is cheap.

The rule is high-value because user-state assertions tend to be load-bearing — once made, the rest of the reply is reasoning *from* them. A wrong premise here invalidates a confident-looking argument.

## What the rule should say

> When a casual reply contains a claim about the user's machine state (files they have, contents of those files, agents installed, recent commits, configuration values), either: (a) cite the tool call that established it within this conversation, (b) hedge explicitly ("if your file looks like the typical pattern…"), or (c) read the artifact before finalizing the reply. Memory-derived user-state claims are not allowed without a hedge.

This is a discipline for the orchestrator's own behavior in casual mode, not a workflow step. It is the casual-mode equivalent of what Explore does inside the workflow.
