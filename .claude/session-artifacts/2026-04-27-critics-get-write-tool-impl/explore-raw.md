# Explore — repo state for critics-get-write-tool

## 1. Three Critic Agent Files — Current Tools & Output Format

All three identical:

- `.claude/agents/critic-architecture.md` line 4: `tools: Read, WebFetch, WebSearch`. 6-section output ending with verdict at line 42. No persistence instructions.
- `.claude/agents/critic-operations.md` line 4: `tools: Read, WebFetch, WebSearch`. 7-section output ending with verdict at line 47. No persistence instructions.
- `.claude/agents/critic-product.md` line 4: `tools: Read, WebFetch, WebSearch`. 6-section output ending with verdict at line 42. No persistence instructions.

**Divergence between the three: zero.**

## 2. Agents with Write Tool — Established Path Scoping Pattern

- **subagent-distiller**: `tools: Read, Write`. Body line 28: "Write the distillation to disk. Target path: `.claude/session-artifacts/<session-id>/distillations/<source-agent>.md`."
- **scope-mapper**: `tools: Read, Write, Grep, Glob`. Body line 34: "Write `scope-map.md` to disk. Target path: `.claude/session-artifacts/<session-id>/scope-map.md`."
- **frame-challenger**: `tools: Read, Write`. Body line 25: "Write `challenges.md` to disk. Target path: `.claude/session-artifacts/<session-id>/challenges.md`."

**Established pattern:** frontmatter grants `Write`; body names the exact target path templated with `<session-id>`; under `.claude/session-artifacts/<session-id>/`. **No hook-level validation; scoping is instruction-level.**

## 3. References to `critiques.md` and `critiques/<lens>.md`

- **CLAUDE.md line 46 (Step 10):** "Aggregate verdicts into `critiques.md`. **Minority-veto:** if any lens returns `rework` or `reject`, proceed to step 11."
- **Session-artifacts README line 17:** "├── critiques.md            # critic-panel aggregate (step 10)"
- **Upgrade entry line 35:** Body proposal naming new contract.
- **Frame.md (current session):** Multiple references to keep/drop the aggregate.

## 4. Existing Session-Artifacts Directories

Sample showing precedent:

```
2026-04-26-format-only-state-transition-gate/
  ├── critiques.md
  ├── critiques/
  │   ├── architecture.md, architecture-v2.md
  │   ├── operations.md, operations-v2.md
  │   ├── product.md, product-v2.md

2026-04-26-upgrades-lab-design/
  ├── critiques.md (3.2 KB aggregate summary)
  ├── critiques/
  │   ├── architecture.md (8 KB)
  │   ├── architecture-v2.md (3.2 KB)
  │   ├── operations.md (6.9 KB), operations-v2.md (3.8 KB)
  │   ├── product.md (9.6 KB), product-v2.md (6.3 KB)
```

**Precedent: per-lens files already exist and are persistent — but currently written by the orchestrator, not the critic.**

## 5. CLAUDE.md Step 10–11 verbatim

Step 10 (lines 41–46):
```
10. **Critic-panel.** Invoke the three critic lenses in parallel (single message, three Agent calls):
    - `critic-architecture`
    - `critic-operations`
    - `critic-product`

    Aggregate verdicts into `critiques.md`. **Minority-veto:** if any lens returns `rework` or `reject`, proceed to step 11. Only if all three return `approve` may you skip to step 12. Each lens must produce at least one frame-level objection in addition to its lens-specific critique.
```

## 6. Hooks & Path Validation Precedent

`.claude/settings.json` has only allow/deny lists. **No `hooks/` directory exists. Settings.json has no hook definitions. Path validation is currently zero — no precedent in this repo for harness-level path enforcement on Write calls.**

Upgrade #14 ("Hard gates as harness hooks") names this as a future need. Upgrade #3 ("Subagents claim writes not on disk") proposes a `PostToolUse` hook to verify writes — directly relevant.

## 7. Upgrade Entry Plan section

(Quoted verbatim — see entry at [`upgrades/no-brainer/2026-04-26-critics-get-write-tool.md`](../../upgrades/no-brainer/2026-04-26-critics-get-write-tool.md), lines 65–79.)

## 8. Related Upgrade Entries

- **#3 ("Subagents claim writes not on disk")** — 💎 profound. PostToolUse hook to verify claimed writes exist + per-session limitations.md. **Directly relevant: load-bearing if critics write their own verdicts.**
- **#18a ("Upgrade entries can grow into folders")** — ✅ no-brainer. Redefine entry as folder. Not directly relevant.
- **#14 ("Hard gates as harness hooks")** — 🌿 normal. Move three gates from prose to hooks. **Relevant: a path-validation hook here could prevent orphaned files from wrong session-ids.**

## How These Primitives Relate

- **Audit chain fragility.** Currently critic-prose → orchestrator-paraphrase → critiques.md. Proposal: critic-write → orchestrator-read. Risk: if session-id passing fails, critics write to orphaned locations. Upgrade #3 hook is the complement.
- **Aggregate file decision.** Per-lens files already exist; orchestrator currently writes them. Real question: is `critiques.md` a thin index or obsolete?
- **Write-tool surface.** Three other agents (distiller, scope-mapper, frame-challenger) already follow instruction-level pattern. Zero hook enforcement. Proposal assumes this is sufficient.
- **Self-modification.** Frame.md Alt 3 named the recursive concern. Critics tend to approve self-improvements that expand their own surface.

## Reversibility

- Keep/drop aggregate: XS reversible (one-line edit).
- Add Write to critics: reversible if no agent outside the three depends on inline returns.
- Path naming: zero cost.
- Session-id passing: depends on orchestrator pattern.
