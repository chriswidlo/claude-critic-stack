# Living module for AI power-user SOTA practice

| Field | Value |
|---|---|
| 📌 **title** | Living module for AI power-user SOTA practice |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session 2026-04-26 (this conversation). Operator asked the orchestrator to research the best Claude Code status bar and the most-helpful tools and commands across web, GitHub, and X. The orchestrator returned a ~600-line cited synthesis. The operator then asked how to preserve and add value to the repo, and explicitly framed the answer as a *mechanism* for keeping AI power-user SOTA knowledge alive within some module — abstract first, sub-upgrades later. This entry is that abstract parent. |
| 💡 **essence** | The repo curates an engineering canon and a session-memory but has no module for the *adjacent* knowledge domain it most operates on — agentic engineering and Claude Code practice itself — as a *living* resource. Research sessions on this topic happen repeatedly (today is the second deposit in two weeks) and their output decays in `temporary/` or in chat history. The fix is not another one-shot migration; it is naming the *recurring shape* so subsequent depositions accrue against a known target instead of being re-invented each time. |
| 🚀 **upgrade** | Establish a single named module in this repo (working name `references/agentic-engineering/`) whose responsibility is to hold curated power-user knowledge as a *living* resource — written by the operator and AI together, refreshed on a cadence, queryable by `claude-code-guide` and by the operator directly. This entry is the abstract proposal. Concrete sub-upgrades — refresher cadence, schema, retire-stale rule, claude-code-guide integration, dissent sourcing — will spawn from it as each question becomes concrete enough to write. |
| 🔗 **relates_to** | agentic-engineering-reference-library, wire-claude-code-guide, canon-coverage-audit-and-priority-additions, citation-audit-as-canon-discipline, corpus-bias-compensation-step |
| 🏷️ **tags** | reference, claude-code, agentic-engineering, living-module, parent-entry, mechanism |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The seed and the gap](#the-seed-and-the-gap)
- [What this entry proposes — and what it does not](#what-this-entry-proposes--and-what-it-does-not)
- [Relationship to the agentic-engineering-reference-library entry](#relationship-to-the-agentic-engineering-reference-library-entry)
- [Why "living" is the operative word](#why-living-is-the-operative-word)
- [Sub-upgrade shapes likely to spawn from this one](#sub-upgrade-shapes-likely-to-spawn-from-this-one)
- [The seed research, preserved](#the-seed-research-preserved)
- [Open questions deliberately left open](#open-questions-deliberately-left-open)
- [What success looks like](#what-success-looks-like)

## The seed and the gap

Today's session began with a flat operator prompt: research the best Claude Code status bar and the most-helpful tools and commands across web, GitHub, and X — and "do not stop until your guidelines are revolutionary and SOTA." The orchestrator went out, hit the GitHub API for star counts on the top status-bar repos, fetched the official statusline docs, pulled distillations of the top community guides (including Boris Cherny's public workflow and the builder.io and Anthropic Help Center power-user pieces), and returned a cited synthesis: a ranked status-bar pick, a tier-list of slash commands, the keyboard shortcuts that change a working day, hooks, subagents, skills, MCP, plugins, and the half-dozen workflow patterns that the most-cited public Claude Code users actually run.

The session was useful. The session was also the *second* such session in two weeks — the earlier one (the one that produced the 409-entry decision registry, the 327-line playbook, and four podcast transcripts now sitting in `temporary/`) is the same shape, with different content. It will not be the last; Claude Code is the fastest-moving piece of infrastructure this repo depends on, and the operator's research instinct will return to it on a cadence that no one has yet named.

The gap the two sessions together expose: this kind of artifact has nowhere durable to live in this repo. Today's research was almost lost — it would have decayed inside the conversation transcript. The operator's framing (*"i just want this whole body of work as one upgrade … upgrade itself will either span sub-upgrades or do it in one, but it will have to discover the value in your research"*) is a recognition that the *individual* artifact is not the upgrade. The mechanism is.

## What this entry proposes — and what it does not

**Proposes:** a single named module in this repo whose responsibility is to hold curated agentic-engineering and Claude Code power-user knowledge as a *living* resource. Read by the operator. Read by [`claude-code-guide`](../../no-brainer/2026-04-26-wire-claude-code-guide.md) when it is wired into parallel-gather. Refreshed on a cadence by a refresher pattern. Queryable. Diffable. Pruneable.

**Does not propose:** a specific path on disk, a specific schema, a specific cadence, a specific retire-stale rule, or a specific contract with the canon librarian. Those are sub-upgrades. This entry's job is to make the *mechanism* a named thing — so that subsequent design questions can route through the 12-step workflow against a concrete target instead of inventing the target each time the operator asks "where does this go?"

This is the abstract parent. It is allowed to be light on mechanics by design.

## Relationship to the agentic-engineering-reference-library entry

The earlier `[agentic-engineering-reference-library](../2026-04-26-agentic-engineering-reference-library.md)` entry proposes the *first migration into* the module: lift `temporary/decision-registry.md` and `temporary/claude-code-expert-playbook.md` to `references/agentic-engineering/`, route the four transcripts through `canon-refresher`, delete `temporary/`. That entry is one-shot; it ends when the migration completes.

This entry is about the *recurring* shape — what the module is *for*, why it must be living rather than static, and how subsequent depositions accrue without re-litigating. The two entries should be read as **parent and first-instance**. If both reach `🔨 implemented`, this one's implementation is "the module exists, has a refresh discipline, and has a documented role in the agent stack"; the other one's is "the first batch of content is in it."

There is honest overlap. A future critic could reasonably argue that the recurring shape concern should be absorbed into the existing entry rather than spawned as a sibling. That's a fine outcome — both are normal-tier and the merge is cheap. The reason to name them separately *now* is that the maintenance and refresh question is the explicit `Open question #4` in the existing entry, and pulling it out gives it room to mature before being collapsed back in.

## Why "living" is the operative word

A static reference for Claude Code dies fast. The October 2025 session's tip list and the April 2026 session's tip list disagree on at least seven specifics — `/effort max`, the `--bare` flag, the existence of certain slash commands, the recommended status-bar tool, the Shift+Tab cycle order. A frozen artifact misleads more than it informs once it has aged six months.

A living module needs three properties a one-shot migration does not:

1. **A refresh cadence.** Something — a `canon-refresher`-shaped subagent on a `/schedule` routine, a manual operator habit, or a hybrid — that produces new deltas on a known clock. The cadence does not have to be fast; it has to *exist*.

2. **A retire-stale rule.** Something that demotes or removes claims when their primary source contradicts them, ideally with the contradiction recorded as part of the entry's history rather than silently overwritten. The lab tradition of *honest negation* applies here: a stale claim is more useful with its replacement annotated than it is silently deleted.

3. **A clear ownership boundary versus canon.** The canon librarian retrieves *engineering canon* — essays, books, papers with multi-year stability. The module retrieves *practitioner knowledge* — transcripts, threads, blog posts, tip compilations with multi-month decay. The two have different decay rates and different anti-confirmation needs. Co-locating them collapses the distinction and weakens both. The module needs prose, not just folder separation, that names which questions go to which.

This entry stops at *naming* the three properties. The shape of each is a sub-upgrade.

## Sub-upgrade shapes likely to spawn from this one

None of these are commitments — they are predictions of what the module will need once it exists. Each is a future entry, written when the prior question is concrete enough to deserve one.

- **Refresher pattern, mirrored from canon-refresher.** A subagent or routine that proposes deltas to the module from a small curated feed set (Anthropic engineering blog, Claude Code release notes, IndyDevDan / Sankalp / Cherny channels). Author-policy is read-only with respect to the module — it proposes, the operator accepts. The existing `canon-refresher` is the template; the differences are around feed sources and acceptance criteria, not architecture.

- **Schema for entries.** The current `temporary/decision-registry.md` is a flat table; the playbook is narrative; the transcripts are verbatim. The module probably wants all three shapes plus metadata each shape carries (source, source-date, claim, confidence, last-verified-date, supersedes-which-prior-claim). The schema entry is the one that makes "living" mechanically possible — without per-claim source-date metadata, there is nothing to retire.

- **Integration contract with `claude-code-guide`.** The local-first vs. WebFetch-first decision (open question #2 in the reference-library entry). Probably "local for canon-stable patterns, web for product-surface specifics" — but writing it down is its own entry, and the boundary is sharper than it sounds: a Boris Cherny workflow pattern is canon-stable in a way that the current set of slash commands is not.

- **Dissent sourcing.** The librarian's anti-confirmation rule applies to this module too. A sub-upgrade specifically about finding contradicting voices on agentic engineering — production failures, skeptic posts, "vibe coding considered harmful" critiques, post-mortems of multi-agent setups that did not pay off — and giving them placement equal to the bullish material. Without this, the module becomes a confirmation-bias vending machine for whatever the operator already believes.

- **Retire-stale ritual.** A periodic pass — possibly via `/loop` — that flags claims where the primary-source date is older than N months *or* where a newer source contradicts. Non-blocking; surfacing a list, not auto-deleting. The retire-stale ritual is the difference between a module that lives and a module that just accumulates.

The order in which these sub-upgrades land is not fixed. The schema probably has to come first because the others are structurally downstream of it. The dissent-sourcing entry can land at any time and is independently valuable.

## The seed research, preserved

The full power-user guide produced in this session is preserved as a supporting file in this entry's folder: [seed-research.md](./seed-research.md). It is the second concrete deposit (after `temporary/decision-registry.md` and the playbook) of the type of artifact this module would hold. Reading the two together is the cleanest way to see the *shape variety* the module needs to absorb — one is a long, structured registry; the other is a tighter opinionated synthesis with rankings and citations. The module's schema must accommodate both without collapsing them into one.

The seed file is preserved verbatim, including the ranked status-bar section that was de-prioritized in the conversation's final user-facing version. The pruning was correct for the conversation; preservation is correct for the lab. Future readers — human or agent — can decide which subset is still current at the moment they read it.

## Open questions deliberately left open

These are the points where the 12-step workflow should bite if this entry advances to `⚙️ run-through-repo`:

1. **Is the module's home `references/agentic-engineering/` (sibling to `canon/`) or `canon/agentic-engineering/` (sub-folder)?** Inherits open question #1 from the reference-library entry. Lean toward sibling because the retrieval semantics differ (operator-read with optional agent-read, vs. librarian-read with anti-confirmation discipline), but a critic-architecture review might disagree on coupling grounds.

2. **Should this entry actually exist, or should the reference-library entry simply absorb the recurring-shape concern?** The honest version of this entry is "I think the parent is worth naming separately, but a critic-product review might call it over-articulation." If the critic-panel later concludes this is over-articulation, merge — and lose nothing, because the body of this entry is content the absorbed version would carry anyway.

3. **What is the trigger condition for new content arrival?** Operator-driven (each research session deposits explicitly), AI-driven (the refresher proposes), or both? The two have different governance models — the AI-driven path needs an acceptance ritual; the operator-driven path needs a deposition ritual. The answer is probably "both, with different write paths," but writing it down is the sub-upgrade.

4. **What is the failure mode of having a living module of practitioner knowledge alongside an engineering canon?** Specifically: does the librarian start citing practitioner posts when the operator wants engineering essays? The boundary needs explicit prose, not just folder separation. Without it, the librarian's discipline weakens by accretion rather than by decision.

5. **Is the cadence question the same as the cadence question for canon-refresher, or is it different?** Canon refreshes slowly (book-shaped knowledge), this module refreshes fast (tip-shaped knowledge). If they share a refresher infrastructure, the cadence parameter has to be per-module. If they don't, the duplication has to be justified.

## What success looks like

If this entry reaches `💎 value-proved`, the signal is:

- A third research session on Claude Code or agentic patterns (whenever it occurs) deposits its output into the module without anyone re-asking "where does this go?" — the question is settled.
- The librarian or `claude-code-guide` cites the module at least once during a 12-step run with a verified marker, distinct from a canon citation.
- At least one claim in the module has been *retired* or *superseded* with the supersession recorded — proving the living-ness is mechanical, not just aspirational.
- The reference-library entry's `temporary/ → references/` migration completed cleanly and at least one sub-upgrade from this entry's predicted-shapes list has been written and acted on.

If, six months later, the module has accumulated content but nothing has ever been retired, *that is also a signal* — a signal that the retire-stale ritual was never built, and the module is on its way to the same fate as a static doc. The honest move at that point is to either build the ritual or demote the entry honestly in the body. The lab tradition is not pretending things worked when they did not.
