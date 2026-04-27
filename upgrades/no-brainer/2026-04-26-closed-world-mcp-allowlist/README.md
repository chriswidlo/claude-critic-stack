# Closed-world trust model + MCP allowlist check

| Field | Value |
|---|---|
| 📌 **title** | Closed-world trust model + MCP allowlist check |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | A user question — *"learn everything about Context7… then analyse and think if and how we must add it to this repo as an upgrade"* — routed through the full 12-step workflow at session `2026-04-26-context7-adoption-in-critic-stack`. Two critic loops; product lens rejected R1 (frame-level), all three lenses reworked R2 (design-level). Final synthesis: reject in-workflow adoption; harden the commitment so it isn't enforced by prose alone. |
| 💡 **essence** | The stack runs a **closed-world trust model** (curated canon + outside-view's bounded WebSearch) and that posture should be a stated invariant, not an unspoken default. Vendor-live MCP retrieval (Context7 and similar) is the first concrete external-source proposal this stack has had to evaluate; rejecting it is honest if and only if the rejection is enforced at runtime, not in prose. |
| 🚀 **upgrade** | Two surgical changes: one bullet under CLAUDE.md "Things you must not do," and `bin/check-mcp-allowlist.sh` that runs at workflow step 0 and fails closed if a non-allowlisted MCP server is present in any scope (project, user, enterprise). The first is the policy commitment; the second is the runtime instrument that makes it real. Together they (a) close the door on a category of silent failure (vendor-tier passages leaking into distillations, contaminating downstream synthesis with unreplayable content), and (b) establish the *template* for evaluating every future external-source MCP/Skill proposal against the same closed-world invariant. |
| 🏷️ **tags** | trust-model, mcp, retrieval, hygiene, context7, allowlist, closed-world, vendor-tier, librarian-first |
| 🔗 **relates_to** | 2026-04-26-citation-audit-as-canon-discipline (citation provenance is the same audit-chain concern at the librarian's other end) |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The decision](#the-decision)
- [The two changes](#the-two-changes)
- [Why this is no-brainer](#why-this-is-no-brainer)
- [What the workflow surfaced that's worth re-reading](#what-the-workflow-surfaced-thats-worth-re-reading)
- [Falsifier and revisit trigger](#falsifier-and-revisit-trigger)
- [Residual disagreements from the panel](#residual-disagreements-from-the-panel)

## The decision

The 12-step workflow evaluated five adoption shapes for Context7 (do nothing / raw tool / new subagent / extend canon-refresher / Skill out-of-workflow) and converged on **reject in-workflow adoption**. The path matters as much as the verdict:

- **Outside-view** placed shapes C and E *below* the base rate of "adding a workflow-A tool to a workflow-B stack." Shapes B and D *within tolerance*. Shape A (do nothing) is the base rate.
- **Canon-librarian** surfaced the sharp contradiction between Anthropic's *just-in-time tool-loaded retrieval* (favors adoption) and *bloated tool sets create ambiguous decision points* (against). Plus Cockburn's "two to four ports" pushing against a sibling retrieval agent.
- **Scope-mapper** found shape B has unresolved conflicts with canon-librarian and the librarian-first rule; shape D conflicts with the corpus's principle-level curation criterion; **shape B is dominated by shape C**; shape D answers a different question than Context7 was built for; shape E is orthogonal, not in competition.
- **Frame-challenger** reframed: *"is the fluid permitted in the building?"* — the trust-tier question is prior to the integration-shape question.
- **Critic panel R1**: product *rejected*, architecture and operations *reworked*. Convergent objection: candidate was a hybrid (install Skill + ban it from workflow + write trust-tiers.md + log questions for measurement) that satisfied no frame coherently.
- **Critic panel R2** on the rejection candidate: all three reworked with actionable demands. Architecture: drop the `decisions/0001-` ADR-registry-under-cover; the commitment must live in artifacts that *embody* policy, not files that *declare* it. Operations: replace prose-only boundary with a runtime instrument. Product: drop the recommend-without-delivering global-install pointer.
- **R3** (final, post-cap): one CLAUDE.md bullet + one allowlist script. Nothing else.

## The two changes

### CLAUDE.md bullet — under "Things you must not do"

> Do not install vendor-live MCP retrieval tools (Context7, similar) in this repo's `settings.json`. The stack runs a closed-world trust model: curated canon + outside-view's bounded WebSearch. Vendor-live retrieval is not admitted. Revisit only if the workflow's question log shows ≥25% of recent design questions bottlenecked on current library-API specifics canon cannot serve.

### `bin/check-mcp-allowlist.sh`

A small script (estimated ~15–20 lines bash) that runs at workflow step 0:

1. Enumerate active MCP servers via `claude mcp list` (or equivalent for the user's CLI version).
2. Compare against the allowlist (starts as `[]` — the workflow needs no MCP servers today).
3. Exit non-zero with a named diagnostic if any non-allowlisted server is present in any scope.

The check fails *closed*: a globally-scoped Context7 install (which a user might add to their global Claude Code config for code work in other repos) would be detected and refused before the workflow runs in this repo.

CLAUDE.md gains one line under the workflow steps section: *"Step 0 — run `bin/check-mcp-allowlist.sh`. If it fails, do not proceed; resolve the unexpected MCP server first."*

## Why this is no-brainer

- **XS effort.** One bullet edit + one short bash script + one workflow-section line. Estimated 30 minutes total.
- **Obvious value if you accept the closed-world frame.** The frame was tested by the full panel and survived (architecture and operations reworked R3 only on enforcement, not on the closed-world commitment itself).
- **The runtime check costs nothing on the happy path.** It runs once at step 0 and exits silently when the allowlist matches.
- **It establishes the template** for evaluating future external-source proposals (Linear MCP, Sentry MCP, a private wiki connector) against the same closed-world invariant — without having to re-run the full 12-step workflow each time. The bullet's revisit trigger names the falsifier; everything else falls back to "the bullet rules unless the falsifier fires."

## What the workflow surfaced that's worth re-reading

This entry's load-bearing value isn't the decision itself; the decision is just "no." The value is what the workflow demonstrated about *how this stack thinks about external-tool adoption*:

1. **Hybrids that try to satisfy multiple frames simultaneously fail every frame.** R1 was "install the Skill but quarantine it, write a policy artifact, schedule a measurement." Three lenses, three different objections — but they converged on *the same shape of error*: the candidate was being clever instead of committing. Worth remembering the next time a candidate feels like a clever middle path.

2. **Documentation is not architecture.** R2 was "write `decisions/0001-no-vendor-tier.md` and recommend global install." Architecture lens caught it: a file that declares a commitment is not the commitment. The commitment lives in the artifacts that embody policy — CLAUDE.md, agent prompts, runtime checks. This generalizes well beyond this question.

3. **Closed-world vs. open-world is a trust-model commitment, not a temporal deferral.** The original architecture critique. Worth re-reading whenever the stack is tempted to "provisionally adopt" anything — provisional adoption of a third-party retrieval source *is* open-world adoption with a fig leaf.

4. **Boundaries enforced only by prose are operationally non-existent.** The operations critic's R1 frame, sharpened in R2 ("if you remove the failure surface in one place and recreate it elsewhere, the boundary just relocated"). The allowlist script is the response — if there's a boundary, there's an instrument that detects violations of it.

5. **The user's "upgrade" framing was honest discipline-preservation refused.** Product critic R1: "bureaucratic refusal dressed as adoption." The honest response wasn't to soften the refusal — it was to make the refusal cleaner. The original briefing already taught the user how to install Context7 globally for code work; the in-repo answer is no, and that's the upgrade.

## Falsifier and revisit trigger

The bullet names a single, measurable falsifier: **≥25% of recent design questions bottlenecked on current library-API specifics canon cannot serve.**

This is honest only if the stack is actually counting. The cheapest-experiment from the synthesis (not implemented in this entry, but referenced for follow-up): augment orchestrator step 1 to append one line to `.claude/question-log.md` per session — `{date, session-id, classifier-label, names_library_and_version: Y/N}`. After ~20 sessions, compute the percentage. If ≥25%, this entry's revisit-trigger fires; re-open the decision with real evidence instead of priors.

That logger is itself a separate small upgrade and should probably get its own no-brainer entry (or be subsumed under the existing telemetry-shaped items in Group C of the LEDGER).

## Residual disagreements from the panel

Per CLAUDE.md's two-loop cap, R3 was not run through a third critic-panel pass. The synthesis named three residual disagreements that are worth carrying as known limitations of this entry:

- **Architecture would prefer no script at all** — just the CLAUDE.md bullet. R3 ships the script because operations demanded an instrument; architecture would prefer minimum new structure.
- **Operations would prefer source-tier provenance on distillations** *in addition to* the allowlist check, so post-hoc audits are possible if the script is bypassed. R3 ships only the check (the simpler half).
- **Product asked for either a paste-ready `docs/global-install-context7.md` *in this repo* or drop the global-install pointer entirely.** R3 picks drop; some users would prefer the deliverable. Rationale: the original briefing in the conversation already taught the global install; it doesn't need to live in the repo.

Each is a real critique. Each is a follow-up entry waiting to be written if the stress shows up.
