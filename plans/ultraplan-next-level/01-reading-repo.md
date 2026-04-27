# 01 — Reading of the repo

## What the stack actually is

`claude-critic-stack` is a **stateless adversarial-review pipeline**, externalised from any target codebase, that wraps a single design question in a sequence of structured frictions and writes the trail of those frictions to disk. The pipeline is the product. The artifacts on disk are the receipt. The recommendation that comes out the bottom is, in the operator's own words from [README.md](../../README.md), explicitly *not* the point — the point is that the recommendation has survived a series of named anti-patterns: agreeability, anchoring to local context, treating retrieval as confirmation, persona-cosplay, single-confident-answer-without-named-flip-conditions.

The 12-step routing in [CLAUDE.md](../../CLAUDE.md) is best read not as a workflow but as a **set of compensators against specific LLM failure modes**, each step gated by an artifact that the next step refuses to proceed without. That gating is the most important architectural decision in the stack. Steps 7 (scope-mapper) and 8 (frame-challenger) are *hard preconditions* for step 9 (generator); the orchestrator refuses to generate if `scope-map.md` or `challenges.md` is missing. The hard gate is the closest thing the stack has to a *type system*: it is the place where prose discipline crosses over into mechanical correctness.

The agent roster has converged on three recognisable shapes: **classifier/labelers** (requirement-classifier), **retrievers** (canon-librarian, outside-view, optional Explore), **transformers** (subagent-distiller), **scope-and-frame primitives** (scope-mapper, frame-challenger), and **judges** (the three critic lenses). Each agent is one-shot and largely write-only; none reads cross-session. This is by design — see [.claude/session-artifacts/README.md](../../.claude/session-artifacts/README.md) — but the design choice has consequences I will return to in the long list.

The lab at [upgrades/](../../upgrades/) is structurally separate from the workflow. It is a *notebook tradition*, not a backlog: free-form authoring with one rigid filing discipline (four tiers, eight-state lifecycle, meta + state tables). The form-vs-content split in the lab's design is the single most internally consistent piece of the repo: discipline lives in the *filing*, not the *authoring*. The lab and the workflow do not currently exchange data — no mechanism feeds session insights into the lab, and the `⚙️ run-through-repo` state on lab entries is operator-driven rather than automated.

## Load-bearing claims I believe the stack is making

1. **Anti-anchoring is structural, not exhortatory.** Telling Claude "do not anchor" does not work. Putting Claude in a working directory that is *not* the target codebase does. The directory is the anchor; you change the anchor by changing the directory. This is the cleverest single move in the stack and would lose its force if it were ever wrapped in a Skill or invoked from inside the target repo.

2. **Retrieval-must-contradict beats retrieval-is-relevant.** [canon-librarian](../../.claude/agents/canon-librarian.md) is required to return a contradicting passage every time. This is structurally a more ambitious claim than RAG-as-fact-grounding: retrieval is being asked to perform *adversarial* lookup, not *supporting* lookup. Most retrieval systems do not even have a "find me a counterexample" mode.

3. **Reframing is the orchestrator's job, not a subagent's.** Step 2 (reframe-before-answer) is performed by the main Claude. The stack treats the orchestrator's frame as the highest-leverage and most-compromised primitive — high-leverage because everything downstream is shaped by it; most-compromised because the orchestrator has the most context and therefore the most pull toward the user's framing. Putting reframing on the orchestrator (rather than delegating it) is a deliberate refusal to outsource the bias.

4. **Critique has minority-veto, not majority rule.** Any one of the three lenses can `reject` or `rework` and the orchestrator must replan or rewrite. This is unusual — most multi-agent debate systems aggregate critic outputs (judge-model, voting, weighted score). The minority-veto choice says *"a single specific frame-level objection is more valuable than three vague approvals."*

5. **Decision-quality discipline is mostly imported from outside software.** The outside-view agent leans explicitly on Kahneman/Lovallo, Flyvbjerg, Tetlock — forecasting and judgment literature, not engineering literature. The repo treats software architecture decisions as *a special case of human judgment under uncertainty*, which is conceptually right and uncommon in engineering tooling.

## What I noticed that the documentation does not name

- **The corpus is mostly aspirational.** Of the ~20 manifest entries in [canon/sources.yaml](../../canon/sources.yaml), only ~7 are `body_completeness: full` in [canon/corpus/](../../canon/corpus/) (the Anthropic engineering essays, Cockburn's hexagonal-architecture essay, Chen's *Devil's Advocate* abstract, Shinn's *Reflexion* abstract, Google SRE TOC, AWS SaaS lens). The "books" by Evans, Vernon, Fowler, Kleppmann, Nygard, Beck, Meszaros, Feathers are stubs the librarian is instructed to surface honestly but cannot quote from. The README's "very good library with a mandatory dissenting reader attached" is currently more aspiration than reality; the *functional* library is heavily Anthropic-authored agent-design literature. The librarian retrieving *from* the agent-design corpus *about* agent-design questions is a feedback loop the librarian cannot detect from inside its own retrieval.

- **Path discipline is currently broken inside the repo itself.** [.claude/settings.json](../../.claude/settings.json) contains four `/Users/krzys/...` allow-list entries — a violation of the rule [CLAUDE.md](../../CLAUDE.md) declares "non-negotiable" for every artifact. Either Claude Code's harness writes that file (in which case the rule needs an exemption) or the rule has eroded. Either way it has not been noticed.

- **The replan-loop cap is silent on residual disagreements in machine-readable form.** The Context7 session's [decision-log](../../.claude/session-artifacts/2026-04-26-context7-adoption-in-critic-stack/decision-log.md) reads: *"Cap of two full loops reached after R3 generator output… escalate to synthesis with residual disagreements named."* The contract that synthesis *will* name them is a prose promise with no mechanical check. The hardest-gate failure mode the workflow has is *exactly* this one — a candidate ships with unresolved frame-level objections — and there is no test for it.

- **The generator step is the orchestrator itself, with no agent file and no artifact discipline.** Every other step is a subagent or produces a named file; step 9 is just the orchestrator emitting prose under three required headings. The single step where bias matters most has the *least* structural compensation. This is interesting and slightly suspect.

- **The lab-to-workflow bridge is one-way.** The workflow can produce session-artifacts; the lab can be promoted to `⚙️ run-through-repo`; but no agent reads lab entries when answering a design question, and no agent writes back to the lab from a session. The lab is write-only from the workflow's vantage point.

- **The "quick take" and "skip the critic-panel" exemptions are magic-string parsing in prose, not modal state.** The orchestrator looks for those exact phrases in user input. This works until it doesn't — there is no `mode` field anywhere in the session-artifacts.

These observations are the substrate of the long list and the deep dives. They are the things you only see by reading the repo as a system, not as documentation.
