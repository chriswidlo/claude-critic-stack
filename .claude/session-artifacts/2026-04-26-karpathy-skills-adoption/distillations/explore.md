# Explore distillation — karpathy skills adoption

## Source agent
Explore

## Invocation summary
Orchestrator asked Explore to inventory the user's existing Claude Code configuration (global + project) and assess overlap/gaps against the four Karpathy principles being considered for adoption. Explore returned a filesystem inventory plus per-principle coverage assessment and one explicit correction of a prior orchestrator claim.

## Direct facts
1. [global `CLAUDE.md`] Exists but is 0 bytes / empty. (confidence: direct)
2. [global `settings.json`] Sets model=opus, alwaysThinking, high effortLevel, auto-permissions, and a `Bash(find:*)` allowlist; no hooks, no plugins. (confidence: direct)
3. [global `settings.local.json`] Contains only a single `Bash(find:*)` allowlist; no env vars, hooks, or plugin configs. (confidence: direct)
4. [global `installed_plugins.json`] Equal to `{"plugins": {}}` — no plugins installed. (confidence: direct)
5. [global agents directory] Seven global agents present: master-code-architect, solution-architect, code-refactoring-specialist, codebase-documentation-architect, contract-validation-architect, domain-design-specialist, quality-assurance-validator. (confidence: direct)
6. [project [`CLAUDE.md`](CLAUDE.md)] Defines the 12-step deliberation harness and explicitly disclaims being a target codebase. (confidence: direct)
7. [project [`.claude/`](.claude/)] Project-local critic-stack agents present (canon-librarian, scope-mapper, frame-challenger, critic-architecture, critic-operations, critic-product, etc.). (confidence: direct)
8. [global skills directory] Does not exist on disk. (confidence: direct)

## Inferred claims
1. [Explore] "Don't overcomplicate" is partially covered via KISS language inside master-code-architect and single-responsibility language inside code-refactoring-specialist — but only when those agents are explicitly invoked, not as standing instructions. (confidence: inferred)
2. [Explore] "Surgical changes" is partially covered by code-refactoring-specialist's "NEVER change functionality only structure" rule — again only when that agent is invoked. (confidence: inferred)
3. [Explore] "Ask before assuming" is partially covered by solution-architect's clarifying-questions posture, but coverage is inconsistent across the agent set. (confidence: inferred)
4. [Explore] "Test-first / verifiable success criteria" discipline is entirely absent from both global CLAUDE.md and the seven global agents. (confidence: inferred)
5. [Explore] No obvious conflicts between Karpathy four and existing agents; principles are orthogonal. (confidence: inferred)
6. [Explore] Karpathy file would specifically fill three gaps: (a) populate the currently-blank global CLAUDE.md, (b) add test-first/verifiable-success discipline, (c) provide always-on hygiene not gated on agent invocation. (confidence: inferred)

## Authority-framed claims
None. Explore did not invoke any external authority; all claims are grounded in filesystem inspection or its own synthesis.

## Contradictions surfaced
1. **Prior orchestrator claim vs. Explore finding.** Prior orchestrator recommendation said: "most of the karpathy file's content is already present in the default Claude Code system prompt AND the user's existing global CLAUDE.md." Explore directly corrects this: the user's global CLAUDE.md is empty (0 bytes); only the Claude Code defaults cover the principles, not the user's own file. This contradiction matters because the scope-map and recommendation depend on whether user-authored standing instructions already exist (they do not).

## Subagent's own verdict (verbatim)
No single verdict line. Closest to a verdict: "Conflicts: none obvious. Principles are orthogonal to existing agents." plus the CRITICAL CORRECTION noted above.

## Gaps the subagent missed
- Did not inspect what the Claude Code *default system prompt* actually contains, so the claim "defaults cover much of it" is asserted without evidence. Orchestrator may want to verify before relying on defaults as coverage.
- Did not check whether any of the seven global agents have invocation triggers (description fields) that would cause them to fire automatically on coding tasks vs. requiring explicit Agent-tool calls.
- Did not enumerate the contents of the seven agents beyond a one-line gloss; possible that test-discipline language exists inside quality-assurance-validator but was not surfaced.
- Did not check whether project-level CLAUDE.md files in *other* user repos already encode Karpathy-like guidance (relevant if the question is about global vs. per-project placement).
- Did not assess token-cost or always-on-context impact of adding standing instructions to a currently-empty global CLAUDE.md.

## Token budget
~620 tokens.
