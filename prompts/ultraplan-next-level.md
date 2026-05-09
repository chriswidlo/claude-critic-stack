# Ultraplan brief — elevate `claude-critic-stack` to its next level

> Paste the contents of this file (everything below the divider) into the Anthropic ultraplanning remote agent. Do not summarize it before pasting; the verbosity is load-bearing — it sets the seriousness bar and the anti-shortcut posture.

---

## 0. Who you are and what you are being asked to do

You are a senior strategic R&D agent. The operator of the `claude-critic-stack` repository has commissioned you to produce a **next-level upgrade plan** for that repository. You are *planning*, not implementing. You are producing a document that the operator will read carefully, sleep on, and then make decisions from over the following weeks and months.

Your work product will be evaluated against four bars:

1. **Depth.** Did you understand the repository as a *system of compensators against specific LLM failure modes* — not as a collection of files? Did your plans engage with the design philosophy on its own terms?
2. **Breadth.** Did you survey the actual landscape — adversarial-AI research, multi-agent orchestration patterns, decision-quality literature, evaluation methodologies, the broader Claude/agent tooling ecosystem, sibling projects, peer products — or did you stay inside the repo's own gravity well?
3. **Novelty.** Did your major proposals reframe the problem, change what the system *is* — or were they incremental tightenings of what already exists?
4. **Taste.** Did you resist the LLM-default attractor of "more agents, more steps, more layers"? Did you propose at least one upgrade that *removes* something? Did you name the things you considered and rejected, with reasons?

You will be told plainly when this brief is over what is forbidden and what is required. Read the whole brief before beginning.

---

## 1. What this repository is

`claude-critic-stack` is a stack-agnostic adversarial-review layer for architectural and design decisions. It runs *outside* any target codebase — the working directory is intentionally not a project under review, because the working directory anchors the LLM's framing. By keeping the stack in its own directory, the critic reasons about the *industry* rather than the conventions of any specific repo.

Its current shape, at the time of this brief:

- **A 12-step workflow** (defined in the repo's `CLAUDE.md`) that routes a design question through: classification → reframe → parallel gather (outside-view, canon-librarian, optional Explore) → distillation → scope-mapping → frame-challenge → generation → 3-lens critic panel (architecture / operations / product, with minority-veto) → replan-or-rewrite → synthesis.
- **Ten subagents** under `.claude/agents/`: `requirement-classifier`, `canon-librarian`, `canon-refresher`, `outside-view`, `subagent-distiller`, `scope-mapper`, `frame-challenger`, `critic-architecture`, `critic-operations`, `critic-product`.
- **A canon corpus** under `canon/corpus/` — curated industry literature (Kleppmann, Evans, Fowler, Nygard, Helland, Lamport, the SRE book, Anthropic's own engineering essays, etc.) with a manifest at `canon/sources.yaml` and an ingestion script at `bin/ingest-canon.mjs`. The librarian is required to return *contradicting* passages, not just confirming ones.
- **An R&D lab** at `upgrades/` with four tiers (no-brainer, normal, outlandish, profound), a `LEDGER.md`, and a `/upgrade` slash command. The lab is deliberately permissive on form; rigorous on filing discipline.
- **Session artifacts** under `.claude/session-artifacts/<id>/` — every workflow run lands an auditable trail (requirement, frame, distillations, scope-map, challenges, critiques, decision-log, synthesis).
- **A small set of operational primitives:** path-discipline rules (no absolute paths in artifacts), a `prompts/five-pressures.md` checklist, a `workflows/architecture-review.md` legacy pre-12-step workflow, a `tests/regression/` folder, and minimal `bin/` ingestion tooling.

The philosophical thesis (from the README) is: *"Books teach what to do. Apprenticeship teaches when. This stack is a very good library with a mandatory dissenting reader attached — not an apprentice."* The stack does not pretend to substitute for human judgment; it is a **structural compensator** against known LLM failure modes — agreeability, pattern-overfit, recency bias, confident mediocrity on decisions requiring taste, anchoring to local context, ignoring base rates, treating retrieval as confirmation, and persona-cosplay.

Read the entire repository before beginning your plan. At minimum:

- `README.md`, `CLAUDE.md`, `AGENTS.md` (if present)
- All ten agents under `.claude/agents/`
- `workflows/architecture-review.md` and `prompts/five-pressures.md`
- `canon/README.md`, `canon/sources.yaml`, and a sample of `canon/corpus/*` to understand what "canon" actually contains
- `upgrades/README.md` (only the `README.md` — see hard constraint below)
- A representative sample of `.claude/session-artifacts/<id>/` runs to see how the workflow actually plays out in practice (the *exemplars/* folder is a good entry point)
- `bin/`, `tests/`, `plans/`

You should spend a meaningful fraction of your time on this read. A planner who has not internalized the artifact discipline cannot propose load-bearing changes to it.

---

## 2. Hard constraints — non-negotiable

### 2a. Do not draw inspiration from the `upgrades/` folder contents

Read `upgrades/README.md` to understand the lab's *form* (tiers, meta tables, state lifecycle, filing discipline) — that context is necessary because some of your proposals will likely interact with how the lab works. **But do not read any individual entry inside the four tier subfolders** (`no-brainer/`, `normal/`, `outlandish/`, `profound/`). Do not read the `LEDGER.md`. Do not read the `/upgrade` slash command's example references to specific entries.

The reason: the operator wants this plan to come from genuinely independent thinking — from your reading of the repository, the literature, and the broader landscape — not from a remix of ideas that have already been captured. If your proposals collide with existing lab entries, that is fine and expected; collision-by-coincidence is evidence of convergence, which is information. Collision-by-cribbing is noise. Avoid it by not looking.

If you find yourself uncertain whether a thought is yours or was seeded by something you skimmed, discard it and generate again from first principles.

### 2b. Do not propose implementation; propose plans

You are not writing code. You are not editing files. Your output is a **strategic plan document**. The operator will decide what to build. Your job is to make the choices visible, the rationales legible, and the consequences imaginable.

### 2c. Do not be agreeable

The repository's own `CLAUDE.md` says: *"Politeness is not the goal; honest friction is."* Apply that to your own output. If your honest reading of the repository is that some current design choice is a mistake, say so plainly, with your reasoning. If you think the operator's framing of "next level" is itself wrong — that the most valuable upgrade is *consolidation* or *simplification* rather than expansion — say that too. The brief asks for ambition; ambition does not mean addition.

### 2d. Do not produce a single confident answer

The repository's own rules forbid recommendations without at least three named assumptions that would flip the recommendation if wrong. Apply this rule to every major proposal in your plan. A proposal without stated kill-criteria is not finished.

### 2e. Do not stay inside the repo's gravity well

The strongest temptation for an LLM doing this assignment is to read the repo, internalize its vocabulary (frame, distill, canon, scope-map, critic-panel), and then propose more-of-the-same in that vocabulary. Resist. The most valuable upgrades are likely to come from primitives the repo does not currently have words for. Reach outside.

### 2f. Path discipline applies to your output

The repository forbids absolute filesystem paths in any artifact. If your plan references files in the repo, use repo-root-relative markdown links (e.g., `` [classifier](.claude/agents/requirement-classifier.md) ``). If it references outside-the-repo concepts (papers, tools, posts), cite by name and URL — never by user-machine path.

---

## 3. Research mandate — go wide

You are expected to do extensive external research. The operator does not want a plan that could have been written from inside the repo alone. Your research should cover, at minimum:

### 3a. The adversarial-AI / multi-agent-critique research frontier

- Recent (2024–2026) academic work on **debate**, **devil's-advocate prompting**, **constitutional AI**, **deliberative alignment**, **self-consistency**, **process reward models**, **judge models**, **AI safety via debate**, **scalable oversight**, **chain-of-thought monitoring**, and **inference-time verification**.
- Industrial / lab work: Anthropic's own research on Claude's reasoning, OpenAI's o-series reasoning models, DeepMind's Sparrow/critique papers, Meta's Cicero/CICERO planning, the broader "LLM-as-judge" literature (with attention to its known failure modes — position bias, length bias, self-preference bias).
- Adversarial-robustness work: red-teaming methodologies, jailbreak literature, model-organism studies.

### 3b. Decision-quality and forecasting literature

- Tetlock-tradition forecasting (superforecasters, IARPA tournaments, calibration), reference-class forecasting (Kahneman / Lovallo), pre-mortems (Klein), red-teaming as an institutional practice (CIA, military, A.B. Chayes), the dialectical method, structured analytic techniques (Heuer), "Devil's Advocate" as institutional practice (Catholic Church origins through modern intelligence).
- Decision-journaling and post-mortem literature; Bayesian belief revision in practice.
- Why most "decision frameworks" fail: cargo-culting, ritualization without belief, surface compliance vs. genuine dissent.

### 3c. The Claude / agent tooling ecosystem

- Claude Code's own primitives: Skills, hooks, MCP, slash commands, sub-agent system, Agent SDK, output styles, the recent "Routines" feature, the remote agent / ultraplan feature itself.
- Sibling and peer projects: other adversarial-review stacks, other "second opinion" agents, frameworks like LangGraph / CrewAI / AutoGen multi-agent systems, the broader "agentic AI" tooling space.
- Memory and longitudinal-state systems: vector stores, knowledge graphs, Claude's recent memory features, project-level vs. user-level vs. session-level state.

### 3d. Adjacent fields with under-mined transfer

- Software architecture review practice in industry: ARB processes, ADR (Architecture Decision Records) traditions, the "RFC" cultures of Rust / Python / Kubernetes, design docs at Google / Amazon / Meta.
- Code review research (effectiveness studies, the Microsoft / Google empirical work on what predicts useful review).
- Editorial and peer-review traditions in science and publishing — including their well-documented failures.
- The intelligence-analysis literature on "warning failure" (why analysts miss things even when the data is present).
- The medical-error and aviation safety literatures on checklists, just-culture, root-cause vs. blame.

### 3e. Where the repo's own canon is silent or weak

Read `canon/sources.yaml` and a sample of `canon/corpus/`. Identify topics the canon is plausibly *missing* given its stated purpose. Identify topics it over-indexes on. Identify whether the corpus shape biases the librarian's retrieval toward any particular era, school, or vocabulary.

You should cite specific works and authors when you reference them. Do not make up titles. If you are uncertain a work exists, say so.

---

## 4. Generation mandate — go deep

After research, generate upgrade vectors. Constraints on generation:

### 4a. Span the value-and-scope space

Produce vectors at multiple scales:

- **Foundational** — changes to the philosophy or architecture of the stack itself (what it *is*).
- **Structural** — changes to the workflow, the agent roster, the artifact discipline, the canon shape.
- **Operational** — changes to how the stack is used, observed, evaluated, iterated on, and maintained over time.
- **Interfacial** — changes to how the operator (and possibly other users, if multi-user becomes a thing) interacts with the stack.

Do not skew all your vectors to one scale. Operators consistently under-explore the foundational and the operational ends — push there.

### 4b. Span the conceptual space

For each vector, ask: *what is this an instance of?* Group related vectors. Then look at the gaps between groups — what is conspicuously absent? That absence is often where the highest-leverage proposal lives. Examples of conceptual axes you might use:

- **Adversariality intensity:** soft critique → hard veto → red-team adversary → game-theoretic opponent.
- **Calibration mechanism:** retrospective logging → outcome tracking → forecast scoring → Bayesian belief revision.
- **Memory surface:** stateless per-session → cross-session episodic → durable doctrine → versioned belief system.
- **Corpus dynamism:** static curated canon → librarian-curated growth → automated freshness with human review → live retrieval against a versioned web index.
- **Output surface:** synthesis to chat → structured artifacts → exportable decision records → integrated with the operator's actual decision tools.
- **Evaluation surface:** trust the workflow → measure the workflow → A/B test the workflow → continuously tune the workflow.

You are not required to use these axes; they are illustrative of the *kind* of thinking. Generate your own.

### 4c. Generate before selecting

Produce **at least 15 distinct upgrade vectors** before you begin culling. Many will be wrong; that is the point. The operator will see your shortlist, not the long list, but the shortlist's quality is bounded by the long list's diversity. Resist the temptation to converge early.

### 4d. Cull with reasons

From the long list, select a **shortlist of 5–8 major upgrade vectors** that you believe are the most transformative, given the repo's stated purpose and the operator's stated ambition. For each item *not* on the shortlist, name it in one sentence with a one-sentence reason for cutting. The cuts are part of the deliverable.

### 4e. Deep-dive the top 2–3

For the 2–3 most transformative vectors on your shortlist, produce **deep plans**. A deep plan, in this context, includes:

- **Position** — one paragraph: what changes, in plain language, and why this is transformative rather than incremental.
- **The reframe it embodies** — what does this proposal *think the stack is* that the current design does not? Naming the reframe is half the work.
- **The mechanism** — concretely, what new agents, artifacts, workflows, primitives, integrations, removals, or invariants does this introduce or change? Name the surface area.
- **The literature it draws on** — specific works, with citations.
- **The known failure modes** — at least three things that would make this proposal wrong or harmful in practice. Be specific.
- **Kill criteria** — at least three observable conditions under which the operator should abandon this proposal mid-build.
- **Cheapest experiment** — the smallest, fastest test that would distinguish "this is real" from "this is a mirage." Specify the test, the success metric, and the time/effort budget.
- **Sequence** — what would need to come first, what could be parallelized, what hard dependencies exist on external things (Anthropic features, model capabilities, canon content). Describe in order-of-events, not in calendar weeks.
- **Counter-proposal** — for each deep-dive, name the strongest *alternative* that does roughly the same job differently, and explain why you rank yours above it. If you cannot articulate a credible counter-proposal, your deep-dive is incomplete.

### 4f. Include at least one removal

At least one of the items on your shortlist must propose **removing** something currently in the stack — an agent, a step, a layer, a corpus practice, a constraint, a primitive — and argue that the removal is itself an upgrade. The repo's complexity has grown; complexity is a failure mode.

### 4g. Include at least one foundational reframe

At least one item on your shortlist must propose a **reframe of what the stack is for** — not "make it better at adversarial review" but "the most valuable thing this stack could become is *X*, which is not exactly adversarial review." Argue the reframe; do not merely assert it.

---

## 5. Anti-failure-mode checklist for your own output

Before submitting your plan, walk it against these. The repo's own `prompts/five-pressures.md` and `CLAUDE.md` exist for exactly this kind of self-check.

1. **Did you reframe the operator's request?** They asked for "next-level upgrades." Did you also consider whether the right answer is *consolidation*, *simplification*, *evaluation*, or *patient stewardship* of what exists? If you didn't seriously consider these, return to them before submitting.

2. **Did you take an outside view?** What is the reference class for "ambitious R&D plans for an internal tooling stack"? What is the base-rate outcome — typically, what fraction of such plans get implemented, and what is the modal failure mode? Position your plan against that base rate.

3. **Did you produce contradicting evidence on your own proposals?** For each deep-dive, did you cite at least one source or piece of reasoning that *argues against* the proposal? If every citation supports you, you did not search hard enough.

4. **Did you name at least three uncertainties per major proposal?** Vague hedging adverbs ("probably," "likely," "in some cases") do not count. Named gaps do.

5. **Did you avoid persona-cosplay?** No "as Karpathy would say." No "in the spirit of Fowler." Cite, with date and context. Do not ventriloquize.

6. **Did you avoid the more-is-more attractor?** Count the new agents, steps, layers, and primitives you proposed. If the count is greater than the count of things you proposed to remove or simplify, justify the asymmetry explicitly.

7. **Did you respect path discipline?** No absolute paths. Inside-repo references as repo-root-relative markdown links. Outside-repo references as named concepts with URLs.

8. **Did you stay out of `upgrades/<tier>/`?** Confirm in a sentence at the top of your output: *"I did not read the contents of `upgrades/no-brainer/`, `upgrades/normal/`, `upgrades/outlandish/`, `upgrades/profound/`, or `upgrades/LEDGER.md` while preparing this plan."*

---

## 6. Output specification

Produce a structured plan as **multiple small markdown part-files** under `plans/ultraplan-next-level/`, plus a top-level `INDEX.md` that ties them together. Use clear section headers inside each part. Do not collapse into prose paragraphs — the operator will read this in passes, and the structure aids re-entry.

### Output mechanics — chunked, streaming, fault-tolerant (read this carefully)

A previous run of this brief timed out during a single very large file write. The fix is structural: do not produce a monolith. Stream the plan to disk as a set of small files as you write them, so partial progress always survives.

**Rules:**

- **One file per major section.** Each numbered section in the spec below (§6 "Required sections") becomes its own file under `plans/ultraplan-next-level/`. Suggested filenames: `00-confirmation.md`, `01-reading-repo.md`, `02-reading-landscape.md`, `03-reframe.md`, `04-long-list.md`, `05-shortlist.md`, `06-cuts.md`, `07-deepdive-<slug>.md` (one file per deep-dive — so 2 or 3 separate files), `08-sequencing.md`, `09-risks.md`, `10-uncertainties.md`, `11-cheapest-experiment.md`.
- **Cap each file at ~1500 words.** If a section needs more, split it further (`04-long-list-part-1.md`, `04-long-list-part-2.md`, etc.). The hard ceiling per single Write call is ~2000 words; aim well under.
- **Write each file as a complete unit, then move on.** Do not return to a file to extend it. If you discover something later that belongs in an earlier section, write it to a new addendum file (e.g., `01a-reading-repo-addendum.md`) rather than re-opening the original. Re-writing large existing files is exactly the failure mode that timed out the previous run.
- **Write `INDEX.md` last, but write a stub of it first.** At the start of writing, create `INDEX.md` with just the planned filename list and one-line descriptions. Update it once at the end with the final filenames actually produced. Do not update it incrementally — one initial stub, one final replacement.
- **Order of writing matters.** Write files in the order listed above. If you time out mid-way, the operator gets a coherent partial plan from the early sections rather than fragments scattered across all sections.
- **No single Write call should exceed ~2000 words of content.** If you find yourself composing a longer block, stop and split.
- **Path discipline still applies.** Use repo-root-relative markdown links between part-files — for example, from inside the generated `INDEX.md`, link to a sibling part-file by its bare filename (`[the long list](04-long-list.md)` and similar). Filenames here are illustrative — the actual filenames will exist only after this prompt is run. Never absolute paths.

This is a real constraint, not a stylistic preference — the API write call for very large files has been observed to fail repeatedly under retry until the session times out. Many small writes are safe; one giant write is not.

### Required sections, in this order

1. **Confirmation of constraints** — the one-sentence confirmation from item 8 above, plus a one-sentence confirmation that you read the repo files listed in §1 (or which you skipped, with reason).

2. **Reading of the repo** — 3–5 paragraphs. What the stack actually is, in your own words, after reading it. What you believe its load-bearing claims are. What you noticed that the repo's own documentation does not name.

3. **Reading of the landscape** — 3–5 paragraphs. The state of the adversarial-AI / multi-agent-critique frontier as of your knowledge cutoff, with pointers to specific work. Where the repo sits in that landscape. What it is uniquely well-positioned for; what it is uniquely poorly-positioned for.

4. **Reframe of the brief** — 1–2 paragraphs. The operator asked for "next-level upgrades that elevate the repo to another level of value." Restate that ask in at least one framing the operator did not use. Name what they appear to be optimizing for and at least one thing they might want to optimize for instead. Proceed under your chosen framing — but name it.

5. **Long list of upgrade vectors** — at least 15. One paragraph each. Number them. They may be of any tier of ambition; diversity is the goal here, not selection. After the list, a one-paragraph commentary on the *shape* of the list — what is over-represented, what is under-represented, where you suspect you have a blind spot.

6. **Shortlist** — 5–8 items, selected from the long list. For each, 2–4 paragraphs covering: position, why this beat the others, what tier of ambition it sits at, and what it costs (in attention, complexity, build effort, ongoing maintenance).

7. **Cuts** — every long-list item not on the shortlist, with a one-sentence reason for cutting. (This makes your selection auditable.)

8. **Deep dives** — 2–3 of the shortlist items, expanded per the spec in §4e above (position, reframe, mechanism, literature, failure modes, kill criteria, experiment, sequence, counter-proposal).

9. **Sequencing across the shortlist** — if the operator decided to attempt all shortlist items over the next 6–12 months, in what order should they be attempted, and why? What dependencies exist between them? What would block what?

10. **Risks to the entire plan** — a short section naming the things that, if true, would invalidate not just one proposal but the whole frame. At minimum: "the operator does not actually want X," "the model capability assumption Y is wrong," "the user-base assumption Z is wrong." Be honest about scenarios where the right move is to do *less*, not more.

11. **Three things you are most uncertain about** — named, with what evidence would resolve them.

12. **The cheapest single thing the operator should do this week** to reduce the largest of those uncertainties.

### Length

Bounds are on the **total across all part-files combined**, not on any single file (per-file cap is in the chunked-output rules above). Lower bound: a plan totalling under ~6,000 words almost certainly did not engage with the brief seriously. Upper bound: a plan totalling over ~25,000 words is probably padded. Aim for the length the work demands — not more, not less.

### Tone

Direct. Technical. Specific. No corporate hedging. No "exciting opportunities to leverage." If a proposal is risky, say it is risky and say why. If you are uncertain, name the uncertainty rather than performing confidence. The operator can handle hard truths and prefers them.

---

## 7. What success looks like

A plan succeeds if, after reading it, the operator:

1. Sees at least one major upgrade vector they had genuinely not considered.
2. Believes at least one of their currently-favored directions is meaningfully wrong, for a reason they had not previously articulated.
3. Has a clear, unambiguous, time-budgeted next experiment they can run this week.
4. Has a defensible 6–12 month roadmap they can prune or re-order without losing coherence.
5. Trusts that you read the repo on its own terms and engaged with the literature on its own terms — not as a backdrop for ideas you would have proposed regardless.

A plan fails if:

- It is a remix of the obvious.
- It proposes more agents and more steps without arguing why the existing ones are insufficient.
- It cites the literature without engaging it.
- It hedges every recommendation into mush.
- It is *agreeable* — to the operator's framing, to the repo's existing direction, to its own first instincts.

---

## 8. Begin

Take your time. The operator is not in a rush; they are in a quality regime. Use the model's full reasoning capacity. Use the remote feature's compute budget without anxiety. If you need to think for a long time before writing, think for a long time before writing.

When you begin, the first thing you should do is read the repo files listed in §1. The second thing you should do is begin your external research. Do not begin generating proposals until both are done.

Good luck.
