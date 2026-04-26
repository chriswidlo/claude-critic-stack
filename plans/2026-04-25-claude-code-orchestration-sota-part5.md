# SOTA orchestration knowledge — Part 5 (conditions + closers)

> Final continuation. Section 10 (conditions under which the synthesis is wrong) plus sections 14–17 (what doesn't change, residual uncertainty, experiments, end).

---

## 10. Conditions under which this synthesis is wrong

- **Primitive consolidation continues at trailing-12-month rate.** If Anthropic merges Skills + Subagents + Hooks into a unified "agent definition" primitive (plausible given the Routines / Managed Agents direction), the four-group catalog needs rewriting against the new surface.
- **Frontier-model attention reliability improves enough** that progressive disclosure stops mattering. Most of Group A's nuance deflates.
- **Workload is non-repetitive.** Use the no-orchestration baseline; everything above is overhead.
- **Authoring for portability across tools** (Cursor, Codex, Gemini CLI). Favor open standards (`SKILL.md`, MCP, `AGENTS.md`) over Claude-Code-specific primitives even when the local equivalent is more ergonomic. Claude Code reads `CLAUDE.md`, not `AGENTS.md`; if cross-tool portability matters, use `CLAUDE.md` that imports an `AGENTS.md` fragment via `@`.
- **Workload is single-tenant high-stakes verification.** Archetype F dominates; do not subordinate it to a "general" archetype A or C.

---

## 14. What this upgrade explicitly does NOT change

- No new `.claude/agents/` files.
- No edits to `CLAUDE.md` routing rules.
- No edits to `.claude/settings.json` or `.claude/settings.local.json`.
- No new skills, hooks, output styles, or MCP servers.
- No new `bin/` scripts.
- No edits to existing canon entries.
- No promotion of any web-cited source to canon by the act of citing it here.

If the upgrade process decides any of these *should* change after research, that is a separate plan and a separate change. This plan is documentation of the SOTA synthesis only.

---

## 15. Honest residual uncertainty (what this synthesis does not know)

1. **Whether the four-mechanism-group taxonomy survives the next primitive shipped by Anthropic.** Two new primitives shipped this month alone. The taxonomy's half-life is plausibly 6 months.
2. **Whether the workload archetypes are exhaustive.** Six archetypes is suspiciously round. Real-world workloads may need 10 or may collapse to 3.
3. **Whether the cross-model 2026 empirical results generalize beyond their reported benchmarks.** AlpacaEval, SWE-bench, and the matched-compute studies are benchmark-specific; lifting their results to "design principle" status is overreach.
4. **Whether silent practitioners (those not on GitHub stars / X engagement) hold different views.** Lagging indicators are downstream of who publicly publishes.
5. **Whether the no-orchestration baseline is being underweighted by the entire community.** Plausible. The first synthesis missed it; the rewrites partially restored it; even now this document spends more pages on layered stacks than on "fatten CLAUDE.md and use raw tools."
6. **Whether `/ultrareview`-style verification is durable** or whether it absorbs into a different abstraction (Managed Agents, a workflow primitive, something not yet shipped).
7. **Whether eval harnesses really belong in Group C as a first-class primitive,** or whether they belong in their own group, or whether they belong outside the Claude Code surface entirely.

These are the things the upgrade process is best-positioned to resolve through targeted research rather than synthesis.

---

## 16. Cheapest experiments to reduce the largest uncertainties

For the upgrade process, in roughly increasing cost:

1. **Re-fetch the multi-model arXiv papers at primary source.** Either confirm the snippet-level numbers or strip them. (~1 hour)
2. **Walk Anthropic's docs end-to-end** for any primitive mentioned here that didn't get a direct doc-link cite. (~2 hours)
3. **Run the Vercel `AGENTS.md` vs equivalent skill comparison** on a representative repo. Either reproduce the result or refute it locally. (~half-day)
4. **Pick one workload archetype and instrument it.** Author the minimum primitive set, run for two weeks, measure (a) authoring time, (b) invocation rate, (c) failure attribution by primitive. (~2 weeks)
5. **Ingest the candidate canon entries from §12 Option 1** and re-run the original "are subagents still SOTA" question through the librarian. See whether the librarian now returns Skills-era passages with contradictions, as it should.

Experiment 1 is mandatory before this synthesis is published anywhere outside `plans/`. The others are optional.

---

## 17. End

This file is the synthesis. It is wrong in places — the document itself names which places. The upgrade process is welcome to disagree with any of it; *should* disagree with the parts flagged as directional / unverified; and is the right venue for resolving the open questions in §13.

The single most important takeaway, restated bluntly:

> **There is no SOTA orchestration. There is a constraint-matching procedure across four mechanism groups, plus a separate cross-model axis, plus six workload archetypes. Most teams in 2026 should use *fewer* primitives, more deliberately, with eval harnesses treated as first-class. The "no orchestration" baseline is a serious option, not a fallback.**

---

**File index for this synthesis:**
- `plans/2026-04-25-claude-code-orchestration-sota.md` — part 1: status, terminology, mental model (sections 1–4)
- `plans/2026-04-25-claude-code-orchestration-sota-part2.md` — part 2: cross-model axis, archetypes, intake, tradeoffs, assumptions (sections 5–9)
- `plans/2026-04-25-claude-code-orchestration-sota-part3.md` — part 3: sources & verifiability (section 11)
- `plans/2026-04-25-claude-code-orchestration-sota-part4.md` — part 4: destinations + open questions (sections 12–13)
- `plans/2026-04-25-claude-code-orchestration-sota-part5.md` — part 5 (this file): conditions + closers (sections 10, 14–17)
