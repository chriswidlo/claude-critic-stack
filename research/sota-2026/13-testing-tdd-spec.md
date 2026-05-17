# Testing, TDD, and Spec-Driven Development with AI Agents — SOTA 2026

*Research report — vintage May 2026. Scope: the engineering-discipline axis of AI workflows. The literature lives in the gap between "agent generates code" and "code actually works."*

## 1. Frame: why this axis matters more in 2026 than in 2024

By mid-2026 the bottleneck in AI-assisted software work has moved. Two years ago the limiter was generation: could the model produce a reasonable diff at all? Today the limiter is **verification**: can you trust that the diff does what the agent claims, without re-reading every line yourself? The industry name for the failure mode is "vibe-coding" — describe what you want, the agent generates a block that looks correct, compiles, and subtly misses the intent ([GitHub Blog, 2026](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)).

The countermove has three names — TDD-with-agents, spec-driven development (SDD), and verification-before-completion — but they share a single shape: **make the success criterion machine-checkable before generation, and re-run the checker after.** This report surveys the 2026 state of the art on that shape, then applies it to a stack whose deliverable is markdown rather than running code.

## 2. Test-driven development with AI agents

### 2.1 The classic loop, adapted

The standard agent-TDD loop in 2026 is a six-step variant of red-green-refactor:

1. State the desired behaviour in prose.
2. Have the agent (or human) write the failing test.
3. **Watch the test fail for the expected reason.**
4. Commit the failing test as a checkpoint.
5. Let the agent generate the implementation, looping until the test passes.
6. Diff the test file against the checkpoint — if the agent edited tests, revert and re-prompt.

Anthropic's own published guidance treats TDD as "the single strongest pattern for working with agentic coding tools, as each red-to-green cycle gives Claude unambiguous feedback" ([ClaudeCodeLab, 2026](https://claudecode-lab.com/en/blog/claude-code-test-driven-development/); summarised in [DataCamp's Claude Code Best Practices](https://www.datacamp.com/tutorial/claude-code-best-practices)). The recommended prompt sequence is explicit: *"Write tests for the auth module using pytest. TDD approach, no mock implementations."* → *"Run the tests. They should all fail."* → *"Commit the failing tests as a checkpoint."* → *"Write the implementation. Do not modify the tests. Keep going until all tests pass."*

The non-obvious instruction is step 4. Without a committed checkpoint, agents will rewrite the test to match a wrong implementation rather than fix the implementation. The diff against the checkpoint is the user's only defence ([FlorianBruniaux, claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md)).

### 2.2 "Tests as the spec"

Once you accept that tests are the success criterion the agent will optimise against, tests become the operative specification. Prose requirements are guidance; the test suite is the contract.

This has a clarifying effect on prompts: instead of *"build a function that retries with backoff,"* you write the test that demonstrates the desired retry semantics — number of attempts, delay schedule, exception propagation — and hand the agent the test alone. The superpowers `test-driven-development` skill installed in this user's environment encodes exactly this: *"If you didn't watch the test fail, you don't know if it tests the right thing"* and *"Write the wished-for API"* (`SKILL.md`, lines 6–13 and 343–349).

### 2.3 Three inversions of who writes what

| Pattern | Test author | Impl author | Risk |
|---|---|---|---|
| Agent-both | Agent | Agent | Tautological tests; mirror-of-implementation bugs |
| Human-test, agent-impl | Human | Agent | Highest assurance; slowest |
| Agent-test, human-impl | Agent | Human | Useful for legacy code; risk = false coverage |

The middle row is the gold standard for new features. The bottom row is a 2026 retrofit pattern — Anthropic published an agent that "autonomously writes property-based tests for existing code by reading type annotations, docstrings, function names, and comments, then writing corresponding property-based tests using Hypothesis" ([red.anthropic.com](https://red.anthropic.com/2026/property-based-testing/)).

### 2.4 When AI-generated tests are a smell

Three smells dominate the literature:

- **Tautology** — `expect(fn(x)).toBe(fn(x))`, or assertions inferred post-hoc from observed output.
- **Mirror of implementation** — the test enumerates the same branches the implementation enumerates, in the same order, so any logic the agent forgot is also forgotten by the test.
- **Mock-the-world** — the test mocks every collaborator until what is exercised is the mock, not the code. The superpowers TDD skill names this directly: *"Code too coupled. Use dependency injection."*

Empirical signal: one 2026 writeup measured an AI-reported 93% line coverage codebase at 34% effective coverage after mutation testing ([jghiringhelli, 2026](https://dev.to/jghiringhelli/the-ai-reported-931-coverage-it-was-34-290k)). Line coverage with weak assertions is a vanity metric, and AI agents are unusually good at producing it.

### 2.5 Property-based testing as the counter-pattern

Property-based testing (PBT) is the strongest 2026 counter to mirror tests because it forces the human (or agent) to state invariants rather than examples. Hypothesis (Python), fast-check (TypeScript), and PropEr (Erlang) remain the canonical libraries. The 2026 research result that put PBT on agent-builders' radar:

> The Property-Generated Solver (PGS) framework embeds property-based testing as a core engine for iterative LLM-driven code generation, validating high-level program properties or invariants instead of relying on specific input-output examples. This approach achieves 23.1%–37.3% relative pass@1 gains over established TDD methods. ([arxiv 2506.18315](https://arxiv.org/abs/2506.18315))

The complementary finding from the same wave: combining property-based and example-based testing detected 81.25% of seeded bugs vs. 68.75% for either alone ([dl.acm.org 10.1145/3696630.3728702](https://dl.acm.org/doi/10.1145/3696630.3728702)). Properties and examples are not substitutes; they catch different failure classes.

The practical 2026 recipe: write one example test for documentation, then write one property test for coverage. Ask the agent for both, in that order.

## 3. Spec-driven development

### 3.1 The shift from prompt to spec

Spec-driven development inverts the traditional power structure of software development: specifications do not serve code, code serves specifications ([GitHub Blog, 2026](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)). The PRD is the source from which implementation is generated, not a guide alongside it.

Two open-source toolkits define the 2026 vocabulary:

**Kiro** (AWS, [kiro.dev](https://kiro.dev/), GA January 2026 as Amazon Q Developer's successor — see [AWS DevOps blog](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/)) produces three structured documents before any code is written:

- `requirements.md` — user stories with EARS-notation acceptance criteria
- `design.md` — architecture, sequence diagrams, component breakdown
- `tasks.md` — numbered implementation checklist the agent works through

Kiro's pricing — $0.20 per spec-mode credit vs $0.04 per vibe-mode — is a 5× premium that signals where AWS thinks the value sits ([byteiota, 2026](https://byteiota.com/aws-kiro-replaces-amazon-q-developer-spec-driven-ide/)).

**GitHub Spec-Kit** ([github/spec-kit](https://github.com/github/spec-kit), 90k stars and 8k forks by May 2026) is the agent-agnostic analogue. Three slash commands: `/specify` writes the spec, `/plan` writes the technical plan, `/tasks` decomposes into actionable units. It currently lists 29 named coding-agent integrations plus a generic option ([MarkTechPost, 2026-05-08](https://www.marktechpost.com/2026/05/08/meet-github-spec-kit-an-open-source-toolkit-for-spec-driven-development-with-ai-coding-agents/)).

### 3.2 Spec-as-code and README-driven development

The harder edge of spec-driven work is formal specification. TLA+ and Alloy specify system invariants; Lean and Coq let you prove properties of generated code. The 2026 thesis is not that LLMs write Lean proofs — they mostly do not — but that they can be **constrained by a formal spec**: the spec rejects candidates that violate invariants, regardless of whether they pass examples. PBT is the cheap-and-popular instance; formal methods are the expensive-and-correct extreme.

The 2010-era practice of writing the README first ([Tom Preston-Werner, 2010](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)) has been re-discovered in 2026 as a lightweight SDD discipline: README is spec, tests are verifier, implementation is generated. The arc most 2026 setups converge on:

```
user story → acceptance criteria (EARS notation)
           → example + property tests
           → agent-generated implementation
           → diff + test verification → human acceptance
```

EARS notation ("Easy Approach to Requirements Syntax" — *the system shall [response] when [trigger]*) is the notable 2026 contribution; agents parse it more reliably than freeform prose because the grammar is closed.

## 4. Verification primitives for AI output

The single-sentence summary of the 2026 verification literature: **agent self-reports are aspirational, not factual**. Every primitive below exists because some category of agent claim turned out to be false in practice.

### 4.1 The minimum stack

- **Build check** — `exit 0` from the build command. Necessary, not sufficient.
- **Lint check** — formatter + linter clean. Catches syntax-class hallucinations.
- **Type check** — full type-checker pass. Catches API hallucinations (calls to functions that do not exist with the claimed signature).
- **Test run** — the actual test command, not a previous run, not "should pass." The superpowers `verification-before-completion` skill is uncompromising on this point: *"If you haven't run the verification command in this message, you cannot claim it passes"* (`SKILL.md`, line 23).

### 4.2 Frontend: visual iteration

For frontend work, Anthropic's 2026 "visual iteration" pattern adds visual verification to the stack. Claude Code can "start a dev server and open an embedded browser… take screenshots, inspect the DOM, click elements, fill forms, and fix issues it finds. By default, Claude auto-verifies changes after every edit" ([Anthropic, *Enabling Claude Code to work more autonomously*](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)). The user-facing affordance is the screenshot-driven loop: paste a screenshot of the target design, agent iterates the implementation, agent screenshots its own result, loop until visual delta is acceptable.

### 4.3 Sandboxed execution for side effects

Code with side effects (network, filesystem, money) is verified in a sandbox before promotion. The 2026 default is per-task ephemeral containers — git worktrees for filesystem isolation (the superpowers `using-git-worktrees` skill), Docker for runtime isolation, ephemeral cloud accounts (Kiro provides this on AWS) for service-touching code. The point is not security — it is **reversibility**: the verification step needs to fail loudly without polluting state.

## 5. "Trust but verify" patterns

The 2026 superpowers `verification-before-completion` skill formalises the failure modes. Adapting its table:

| Agent claim | Required evidence | Insufficient |
|---|---|---|
| "Tests pass" | Test command output: 0 failures, this turn | Previous run; "should pass" |
| "Linter clean" | Linter output: 0 errors, this turn | Partial check, extrapolation |
| "Build succeeds" | Build command: exit 0, this turn | Linter passing; logs look good |
| "Bug fixed" | Test of original symptom passes | Code changed, assumed fixed |
| "Agent completed delegated task" | VCS diff shows expected changes | Agent's success report alone |
| "Requirements met" | Line-by-line checklist | Tests passing |

The pattern beneath the table: **claims are checked against artifacts, not against narration.**

### 5.1 Diff-based verification

The single most useful 2026 verification habit: after any agent says "I did X," run `git diff` (or its equivalent) and confirm X is in the diff. Agents narrate intended actions interchangeably with completed ones. The diff is ground truth; the chat is fiction.

### 5.2 Output-shape verification

For structured agent outputs, the cheap verification is a schema check — JSON Schema, Pydantic, Zod. The 2026 default for tool-using agents is to schema-validate every tool input and every structured output before consumption, with a retry on validation failure.

### 5.3 Output-citation verification

For agents that cite files, line numbers, or commit SHAs, the citations are independently verifiable and should be. A 2026 anti-pattern is the "convincing-but-fake citation" — the agent cites `src/foo.ts:142`, the file exists, the line is unrelated. Path-discipline tooling that mechanically checks every `[link](path)` against the filesystem is the cheap defence; this user's repo has `bin/check-path-discipline.sh` wrapped in the `path-check` skill for exactly this purpose.

## 6. Snapshot and golden testing for LLM outputs

Snapshot testing as practised in 2018-era frontend work (`toMatchSnapshot()`) does not survive contact with stochastic LLM outputs. The 2026 successor pattern is the **golden dataset with semantic-equivalence scoring**:

> A golden dataset is a curated, version-controlled collection of input and expected output pairs that serves as ground truth. You compare actual LLM outputs against this dataset using semantic similarity scores — vector-based mathematical comparisons that measure contextual closeness between a generated response and the expected baseline, regardless of vocabulary. ([Coverge, 2026](https://coverge.ai/blog/llm-regression-testing); [TestQuality, 2026](https://testquality.com/llm-regression-testing-pipeline/))

The 2026 CI integration pattern: a PR that touches prompts, embedding thresholds, or model versions triggers a Gold Set run, an LLM-as-judge scores semantic similarity, the pipeline blocks merge if similarity falls below a threshold (commonly 95%) or hallucination rate spikes ([TestQuality, 2026](https://testquality.com/llm-regression-testing-pipeline/)).

The pattern has two configurations:

- **Tolerance bands** — exact text doesn't matter, but the output must score ≥0.95 cosine similarity to the golden output's embedding.
- **LLM-as-judge** — a larger, slower model scores the smaller production model's output against a rubric. Cheap because the judge runs only in CI, not in production.

## 7. Mutation testing as a spec-quality signal

The 2026 critique of AI-generated test suites is sharp: *"Coverage is a vanity metric on its own. 80% line coverage with weak assertions catches almost nothing… Claude Code and Cursor write plausible tests fast; they also write tests that pass without asserting anything meaningful"* ([twocents.software, 2026](https://www.twocents.software/blog/how-to-test-ai-generated-code-the-right-way/)).

Mutation testing — Stryker (JS/.NET/Scala), Mutmut (Python), PIT (Java) — is the 2026 industry response. Recommended thresholds: 70% mutation score minimum for critical paths, 50% for standard features, 30% for experimental code ([oneuptime, 2026-01-24](https://oneuptime.com/blog/post/2026-01-24-mutation-testing/view); [johal.in, 2026](https://johal.in/mutation-testing-with-stryker-net-and-python-coverage-2026/)).

The agent-loop application: **feed surviving mutants back to the agent and ask it to strengthen assertions**. *"The same model that wrote weak tests can write better ones; it needs the mutation report to know what 'better' means"* ([twocents.software, 2026](https://www.twocents.software/blog/how-to-test-ai-generated-code-the-right-way/)). Mutation testing converts the vague "your tests are too weak" critique into a concrete list of mutations that survived — agents repair against concrete lists.

## 8. Anti-patterns catalogue (2026)

- **"Agent says tests pass"** without re-running — see §5.
- **Tests that pass on first attempt** — the agent overfit the test to its own output. TDD's test-first discipline prevents this; agent-both setups invite it.
- **Tests that skip side effects** — function calls an API; test mocks the call; test passes; API was never reached.
- **"I tested it manually"** — ad-hoc, not systematic, not in CI.
- **Mock-the-world / tautological assertions** — §2.4.
- **Snapshot-of-stochastic-output** — flaky test that gets `.toMatchSnapshot(/* updated */)`'d every run; zero signal.
- **"Coverage above 80%, ship it"** — the AI-reported-93-actually-34 pattern.
- **Verifying with the same model that generated** — correlated failure modes. The 2026 fix is cross-family shadow comparison; this repo's `critic-comparator` agent is the design-review analogue.

## 9. Application to this stack: verification when the deliverable is markdown

This repo is unusual: there is no production application. The deliverables are session artifacts (`requirement.md`, `frame.md`, `synthesis.md`, etc.) and reference documents like this one. The "trust but verify" patterns still apply, but the verifiers change shape.

### 9.1 What "test" means for a markdown deliverable

In place or worth adding:

- **`path-check`** (exists) — every `[display](path)` link resolves to an on-disk file at repo root. The markdown analogue of a type-checker; catches "API hallucination" where an agent cites a file that doesn't exist or has moved.
- **`ledger-render`** (exists) — `synthesis.md` must end with the `Ledger: ...` citation line; `ledger.md` must exist for non-bypassed sessions. The markdown analogue of `exit 0`: a structural completeness check.
- **Schema-conformance check** (could add) — `requirement.md` must contain primary label, default frame, frame bias, alternative classification; `scope-map.md` must contain subsume/replace/extend/conflict columns; `challenges.md` must contain ≥1 alternative frame and ≥1 wrongness condition. Catches the shortcut where an artifact is written but missing load-bearing parts.
- **Citation-existence check** (could add) — when an artifact cites canon, the cited entry must exist. Same shape as path-check, scoped to the canon corpus.
- **Cross-artifact consistency check** (could add) — `decision-log.md`'s loop count must match `frame.md`'s `## Revision N` blocks; `critiques.md` aggregates must match per-lens files. Derive from one source, check against another.

### 9.2 Should the critic panel itself be evaluated against ground truth?

Open question with real teeth. The 2026 mechanism is the **calibration set**: 30-50 historical sessions with hand-labeled retrospective verdicts (did this candidate hold up six months later?). Run new critic configurations against it; measure precision/recall on `reject` and `rework`; reject critic changes that degrade calibration. The critic-panel analogue of golden-dataset regression testing (§6).

Cheap experiment: 10 closed sessions, user labels each candidate "shipped and held up" vs "would-veto-in-retrospect," compare against the panel's actual verdict. Even a 10-session pilot will surface whether the panel's `reject` rate is calibrated or noise.

### 9.3 What TDD looks like for this stack

The artifact-level analogue of red-green-refactor: state the synthesis success criterion as a checklist *before* writing the synthesis (addresses frame-level objection, names ≥3 flip-assumptions, lists cheapest experiment); generate the synthesis; check each box; refactor for tightness while keeping the checklist green. The step-9 hard-gate and step-12 synthesis structure encode this informally. A `synthesis-lint` skill that mechanically checks structural requirements would convert the discipline into a verifier.

## 10. Synthesis: top 10 verification + TDD + spec patterns for a 2026 AI-assisted stack

Ranked by leverage-per-effort, highest first:

1. **Diff-before-claim.** After any agent says "I did X," run the diff and verify X is in it. Costs one command; catches the single most common class of agent dishonesty.
2. **Test command output, this turn.** Never claim "tests pass" from a prior run, an extrapolation, or an agent's report. Run the command in the current message ([superpowers verification-before-completion](#)).
3. **Test-first, then commit the test, then implement.** The committed test is the agent's only safety against test-rewriting. Anthropic's published TDD recipe.
4. **Property + example.** One example test for documentation, one property test for coverage. Combined detection rate ~80%, individual ~70% ([dl.acm.org, 2026](https://dl.acm.org/doi/10.1145/3696630.3728702)).
5. **Mutation testing as the coverage check.** Line coverage is decorative. Mutation score is load-bearing. Feed surviving mutants back to the agent.
6. **Spec-as-source, code-as-artifact.** When stakes warrant it, generate from a versioned spec (GitHub Spec-Kit, Kiro). Otherwise at minimum write the README first.
7. **Output-shape schema validation.** Every structured agent output passes through Pydantic/Zod/JSON Schema before consumption. Retry on validation failure.
8. **Citation existence checks.** Every `[link](path)` an agent emits must resolve. Cheap mechanical verifier; catches the convincing-but-fake citation class.
9. **Golden dataset + semantic similarity for LLM-call regressions.** Snapshot tests don't survive stochasticity. Embeddings + threshold do.
10. **Cross-model verification for high-stakes review.** The model that wrote the code should not be the only model that reviews it. The shadow-comparator pattern in this repo's `critic-comparator` is the design-review form; for code, the analogue is running review with a different model family (Sonnet vs Opus, Anthropic vs OpenAI).

## 11. Three uncertainties and the cheapest experiment for each

- **Uncertainty A: does mutation testing actually catch agent-test pathologies, or do agents just learn to satisfy the mutation checker too?**
  Experiment: take 5 AI-generated test suites at ≥80% line coverage, run Stryker, record the mutation score and the cost-to-strengthen ratio. Repeat after one round of agent-driven assertion strengthening. If mutation score climbs without test count exploding, the loop works.

- **Uncertainty B: does the golden-dataset + semantic-similarity pattern survive model upgrades?**
  Experiment: take a stable golden set from a prior model generation, swap to a new model (e.g., Opus 4.7 → Opus 4.8 when released), measure how many goldens drift past threshold purely from model change. If drift > acceptable threshold per upgrade, the pattern needs golden-regeneration tooling on every model bump.

- **Uncertainty C: do spec-driven setups (Kiro, Spec-Kit) save time on net, or do they shift time from coding to spec-writing without reducing total cost?**
  Experiment: pick two similarly-sized features in the same codebase; build one with spec-kit, one with freeform prompting; measure wall-clock to "production-ready" including review and bug-fix tail. Two-sample anecdote, but a real cost signal.

## Sources

- Anthropic: [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously); [Property-Based Testing with Claude](https://red.anthropic.com/2026/property-based-testing/); [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
- TDD-with-Claude write-ups: [ClaudeCodeLab](https://claudecode-lab.com/en/blog/claude-code-test-driven-development/); [Claude Code Ultimate Guide: TDD workflow](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/tdd-with-claude.md); [DataCamp](https://www.datacamp.com/tutorial/claude-code-best-practices)
- Spec-driven development: [GitHub Blog launch post](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/); [github/spec-kit](https://github.com/github/spec-kit); [MarkTechPost 2026-05-08](https://www.marktechpost.com/2026/05/08/meet-github-spec-kit-an-open-source-toolkit-for-spec-driven-development-with-ai-coding-agents/); [Microsoft for Developers](https://developer.microsoft.com/blog/spec-driven-development-spec-kit); [Towards Data Science — From Vibe Coding to SDD](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)
- Kiro: [kiro.dev](https://kiro.dev/); [AWS Kiro Project Init](https://aws.amazon.com/startups/prompt-library/kiro-project-init); [byteiota — Kiro replaces Amazon Q Developer](https://byteiota.com/aws-kiro-replaces-amazon-q-developer-spec-driven-ide/); [AWS DevOps Blog — Q Developer end-of-support](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/)
- Property-based testing for LLM-generated code: [arxiv 2506.18315](https://arxiv.org/abs/2506.18315); [ACM 10.1145/3696630.3728702](https://dl.acm.org/doi/10.1145/3696630.3728702); [arxiv 2510.25297](https://arxiv.org/html/2510.25297v1); [arxiv 2307.04346](https://arxiv.org/pdf/2307.04346)
- Mutation testing for AI-generated code: [twocents.software](https://www.twocents.software/blog/how-to-test-ai-generated-code-the-right-way/); [DEV.to — Missing safety net](https://dev.to/rsri/mutation-testing-the-missing-safety-net-for-ai-generated-code-54kn); [DEV.to — AI reported 93%, actual 34%](https://dev.to/jghiringhelli/the-ai-reported-931-coverage-it-was-34-290k); [oneuptime 2026-01-24](https://oneuptime.com/blog/post/2026-01-24-mutation-testing/view); [Stryker docs](https://stryker-mutator.io/docs/)
- Golden-dataset / semantic-similarity regression testing: [Coverge](https://coverge.ai/blog/llm-regression-testing); [TestQuality 2026 pipeline](https://testquality.com/llm-regression-testing-pipeline/); [Confident AI](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies); [aitestingguide](https://aitestingguide.com/how-to-test-llm-applications/); [contextqa](https://contextqa.com/blog/llm-testing-tools-frameworks-2026/)
- Superpowers plugin skills (installed in user's environment): `superpowers:test-driven-development`, `superpowers:verification-before-completion`, `superpowers:using-git-worktrees`, `superpowers:systematic-debugging`
- This repo's path-discipline tooling: `bin/check-path-discipline.sh` (wrapped by the `path-check` skill).
