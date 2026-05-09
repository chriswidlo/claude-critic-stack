## Source agent
Explore (orchestrator-conducted target-repo / repo-state read; not an Agent invocation per CLAUDE.md step 3–5)

## Invocation summary
Orchestrator asked Explore to audit critic agent definitions, workflow orchestration, skills routing, and any evidence of target-repo influence reaching the critic panel. Explore returned an 11-section report with file:line citations, a tool-permission matrix, a 5-layer flow analysis, and three indirect-leakage vectors.

## Direct facts

### Critic agent tool grants
1. [`.claude/agents/critic-architecture.md` line 4] Tools granted: `Read, WebFetch, WebSearch`. Model not pinned (inherits Opus). (direct)
2. [`.claude/agents/critic-operations.md` line 4] Same tool grant: `Read, WebFetch, WebSearch`. (direct)
3. [`.claude/agents/critic-product.md` line 4] Same tool grant: `Read, WebFetch, WebSearch`. (direct)
4. [`.claude/agents/critic-architecture-shadow.md` lines 4–5, 11, 42] Tools identical to Opus lane; `model: sonnet` pinned in frontmatter; output redirected to `critiques/architecture.shadow.md`. (direct)
5. [`.claude/agents/critic-operations-shadow.md` lines 4–5, 43] Same pattern; output to `critiques/operations.shadow.md`. (direct)
6. [`.claude/agents/critic-product-shadow.md` lines 4–5, 42] Same pattern; output to `critiques/product.shadow.md`. (direct)
7. [`.claude/agents/critic-architecture-shadow.md` lines 37–40] "Do not coordinate with the Opus lane — you are the shadow precisely because you reason independently." (direct)
8. [`.claude/agents/critic-comparator.md` line 4] Tools granted: `Read, Write` only. No WebFetch, no WebSearch. (direct)
9. [`.claude/agents/critic-comparator.md` line 66] "Do not WebSearch. You compare two on-disk files; that is the entire job." (direct)
10. [`.claude/agents/critic-comparator.md` lines 17–25] Comparator inputs are `critiques/<lens>.md` and `critiques/<lens>.shadow.md` for each lens in `{architecture, operations, product}`. (direct)
11. [all six critic agent files] None of the six lens agents contains any explicit instruction permitting or forbidding target-repo Read access. (direct — absence verified across files)

### Target-repo flow through critique-prep / critique-start
12. [CLAUDE.md lines 1–5] "The working directory is **deliberately not a target codebase**. Do not look for one." (direct)
13. [CLAUDE.md lines 28–31] Step 3–5 lists Explore as conditional: "**only** if the user has provided repository context or named a target codebase. Otherwise skip." (direct)
14. [CLAUDE.md line 33] "After this step, the orchestrator reads **only** the distillations going forward; raw subagent output stays on disk." (direct)
15. [`.claude/skills/critique-prep/SKILL.md` lines 60–67] Target validated as one of: absolute path on disk (verified via `test -d "<path>/.git"`), git-remote-URL-only mode, or prompt-only mode. (direct)
16. [`.claude/skills/critique-prep/SKILL.md` lines 60–63] Grounding strategy options: `full-explore | user-named-subset | follow-AI-docs | custom`. (direct)
17. [`.claude/skills/critique-prep/SKILL.md` line 120] "Write `.local/target-path` only in local-path mode. A single line, the absolute path, no extra content. This file is gitignored — it never enters git history." (direct)
18. [`.claude/skills/critique-prep/SKILL.md` lines 115–118] `.gitignore` must include `.claude/session-artifacts/*/.local/`. (direct)
19. [`.claude/skills/critique-start/SKILL.md` lines 23–26] Reads `.local/target-path` into session-memory variable `$CRITIC_TARGET`; "Never echo it into a committed artifact." (direct)
20. [`.claude/skills/critique-start/SKILL.md` lines 38–42] Path-rewrite reminder is conditionally injected for "Explore in step 5, scope-mapper in step 7, critics in step 10 **if they verify facts**." (direct)
21. [`.claude/skills/critique-start/SKILL.md` lines 38–42] Required prompt sentence: any path under `$CRITIC_TARGET` must appear as `<target>/...` in agent output. (direct)
22. [CLAUDE.md lines 43–48] Step 10 invocation spec names only the three lens agents and "the candidate"; does not specify whether `$CRITIC_TARGET`, question.md, scope-map.md, or challenges.md are passed to critics. (direct — by absence)

### What shadow-comparator measures vs. doesn't
23. [`.claude/agents/critic-comparator.md` lines 11–12, 31–37, 52–56] Comparator measures verdict agreement between Opus lane and Sonnet shadow lane per lens, with classes `agree | partial-agree | disagree | unavailable` (`disagree` = verdict labels two notches apart). (direct)
24. [`upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md` lines 32–36] Problem statement: "All three frontmatter files pin a model — all inherit Opus from the orchestrator. So three lenses on the same candidate become Opus reading itself three times." (direct — note: contradicts itself; says "pin a model" then "all inherit" — preserved verbatim)
25. [`upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md` lines 46–54] Shadow-panel sketch: each lens fires twice in parallel (Opus + Sonnet, same prompt, same candidate); comparator reads both. (direct)
26. [`.claude/settings.json`] Permits Read/Glob/Grep scoped to the claude-critic-stack repo path; no `hooks` section present. (direct)

### Indirect leakage vectors (factually located, interpretation-flagged below)
27. [question.md template implied by CLAUDE.md / critique-prep] question.md may include a "Constraints / context" block naming target-repo identifier and grounding strategy. (direct — template structure)
28. [`upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md` line 3] Status: "PAUSED — 2026-04-27." (direct)

## Inferred claims

1. [Explore] "Explore" in step 3–5 is not an Agent invocation but an orchestrator-conducted manual read step that produces `distillations/explore.md`. (inferred — based on CLAUDE.md absence of an Explore agent file plus session-artifact precedent)
2. [Explore] Critics do not directly receive the Explore distillation; they receive the candidate, and possibly question.md, frame.md, scope-map.md, challenges.md — but step 10 spec does not enumerate these. (inferred — by absence in CLAUDE.md step 10)
3. [Explore] Critics may receive target-repo context indirectly via three vectors: (a) candidate.md narrative shaped by target-repo constraints, (b) question.md metadata naming target-repo identifier, (c) WebFetch on a GitHub URL appearing in candidate. (inferred)
4. [Explore] In `2026-04-26-format-only-state-transition-gate` (a no-target-repo session), critics demonstrably reference candidate.md and question.md content but not target-repo content; this is sample-of-one and does not prove critics would refrain when a target is in scope. (inferred from `critiques/architecture.md` lines 5, 10–11, 14–17 and `critiques/product.md` lines 7–9, 20–22)
5. [Explore] The shadow-comparator measures **model-family correlation** (Opus vs. Sonnet on identical inputs) but does not measure **input-shared correlation** — i.e., both lanes see the same candidate, and if the candidate is shaped by target-repo framing, both lanes inherit that shared prior. (inferred)
6. [Explore] critique-start's wording "critics in step 10 **if they verify facts**" leaves the pass-through decision to orchestrator runtime, creating an unspecified contract. (inferred)
7. [Explore] If a global (outside-repo) settings.json grants broader Read, the only protection against critics reading the target-repo is agent-side instruction; there are no runtime hooks enforcing path discipline on Read calls. (inferred)
8. [Explore] WebFetch/WebSearch is a loophole rather than a backdoor — not forbidden in any critic agent file; a critic could fetch a public target-repo URL named in the candidate. (inferred)
9. [Explore] The "critics get write tool" pause is orthogonal to target-repo access; it concerns who persists the verdict, not what critics may read. (inferred)
10. [Explore] No session in this repo has yet exercised critique-prep + critique-start end-to-end with a real target, so there is no empirical sample of critics-with-target behavior. (inferred from absence)

## Authority-framed claims
None. The report is structurally a citation index; no "as X argues" framing appears. (Note: Explore does quote CLAUDE.md and skill files verbatim — these are repo-internal authority, treated here as direct facts.)

## Contradictions surfaced

1. **Tool-grant intent vs. prohibition intent.** CLAUDE.md preamble (lines 1–5) tells the orchestrator the working directory is "deliberately not a target codebase. Do not look for one." But critic agents have unconstrained `Read` and `WebFetch`/`WebSearch` (lines 4 of each agent file) and no agent-file-level prohibition on target-repo access. The preamble binds the orchestrator; the critic agents are not bound by it.
2. **critique-start conditional vs. CLAUDE.md silence.** critique-start lines 38–42 list "critics in step 10 **if they verify facts**" as conditionally receiving `$CRITIC_TARGET`; CLAUDE.md step 10 (lines 43–48) names only the three lens agents and "the candidate" with no mention of `$CRITIC_TARGET` pass-through. The two contracts are silent on the same question and produce divergent reader expectations.
3. **Upgrade README internal contradiction (preserved verbatim).** `upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md` lines 11–12 vs. 32–36: one passage says "None of the three frontmatter files pin a model — all inherit Opus"; another says "All three frontmatter files pin a model — all inherit Opus." Verified directly: agent files do not pin a model (line 4 of each is the tools line). The "all three frontmatter files pin a model" wording in the upgrade README appears to be an editing error.
4. **Designed independence vs. actual independence.** Three lenses are designed for *aspect* independence (architecture / operations / product); the shadow comparator addresses *model* correlation; neither addresses *shared-input* correlation from candidate.md or target-repo framing.

## Subagent's own verdict (verbatim)
Explore did not emit a single verdict line. The report's closing summary in section 10 states: "Critic exposure to target-repo: Permitted indirectly via candidate.md, question.md metadata, and WebFetch; not explicitly via dedicated `$CRITIC_TARGET` prompts." The truncation note in section 12 declares the audit complete for critic agents, CLAUDE.md, critique-prep/critique-start, and three spot-checked sessions.

## Gaps the subagent missed

1. **Exact step-10 prompt structure.** Explore notes the ambiguity but does not retrieve any concrete sample of an actual step-10 invocation prompt from session history. A grep across `decision-log.md` files might reveal what orchestrators have historically passed.
2. **Whether `$CRITIC_TARGET` has ever been passed to critics in practice.** Section 4.1 notes no session has used critique-prep + critique-start, but does not check whether any earlier ad-hoc session passed a target path to critics by other means.
3. **Behavior of Sonnet shadow under target-repo exposure.** The shared-input correlation argument (section 5.2) is asserted but not tested; the subagent did not propose a probe.
4. **Outside-repo settings precedence.** Section 7.2 raises the global-settings.json question but does not resolve it (correctly, per path discipline); orchestrator should treat this as an open variable.
5. **Whether scope-map.md / challenges.md ever quote target-repo content verbatim.** This would be a fourth indirect leakage vector into critics if those artifacts are passed at step 10. Not audited.
6. **No measurement of how often candidate.md actually embeds target-repo narrative.** The "shared-input correlation" claim depends on candidate-shaping frequency, which is not quantified.

## Token budget
~1850 tokens.
