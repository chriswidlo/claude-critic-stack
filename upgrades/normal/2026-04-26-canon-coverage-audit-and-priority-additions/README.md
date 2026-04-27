# Canon coverage audit — the library is less sophisticated than the workflow that consumes it

| Field | Value |
|---|---|
| 📌 **title** | Canon coverage audit — the library is less sophisticated than the workflow that consumes it |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | A user-initiated audit: *"there is corpus folder in this repo. and library, with links please review the links of all are legal and point to real places and are not dangerous. then tell me in what situatian repo will download data from internet from library to corpus?"* and a follow-up *"What do you think about this library? Is it state of art? Is content well suited for this repo job?"* The first pass confirmed all 11 ingestion URLs are legitimate (no malicious targets, only one third-party trust point at `raw.githubusercontent.com/conoro/...` for a community-maintained Anthropic RSS) and that downloads only happen when a human runs `bin/ingest-canon.mjs`. The second pass — the real one — found that the corpus is well-curated for engineering classics but **structurally under-equipped for three of the workflow's twelve steps** (product critique, frame challenge, reframe). The repo's own `corpus-bias-compensation-step` and `citation-audit-as-canon-discipline` upgrades (both no-brainer, both filed today) already touch the same wound from different angles; this entry is the broader coverage analysis. |
| 💡 **essence** | The corpus is curated to a noticeably lower level of sophistication than the workflow that consumes it. The 12-step workflow assumes a librarian that can produce frame-level contradictions on any design question; the corpus only really delivers that on architectural-classics-of-the-2010s questions. Three workflow steps — product critique, frame challenge, and reframe — are running on near-empty corpus support, which means each new workflow refinement has to draw on the same shallow well. Closing the corpus gap produces a bigger quality lift than further workflow refinement. |
| 🚀 **upgrade** | Add ~10 high-leverage entries (Tier 1 + Tier 2 in the body) that fill the structural gaps the workflow leans on hardest — Heuer for the frame-challenger and critic stack, Klein's premortem for frame challenge, Snowden's Cynefin for the classifier, Shape Up for the empty product-critic chair, Conway/Parnas/Team Topologies for module-boundary critique. Each addition unsticks one or more workflow steps by name. After this round, also revisit the AI-agent literature (Tier 3) so the repo cites the field it is reinventing. |
| 🏷️ **tags** | canon, corpus, retrieval, librarian, critic-panel, frame-challenger, product, coverage, methodology |
| 🔗 **relates_to** | 2026-04-26-corpus-bias-compensation-step, 2026-04-26-citation-audit-as-canon-discipline |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [What the library exists to do](#what-the-library-exists-to-do)
- [The audit method](#the-audit-method)
- [Coverage map — workflow step vs. corpus support](#coverage-map--workflow-step-vs-corpus-support)
- [What is good and should be left alone](#what-is-good-and-should-be-left-alone)
- [Is it state-of-the-art? Verdict by genre](#is-it-state-of-the-art-verdict-by-genre)
- [Tier 1 additions — fixes structural gaps the workflow leans on hardest](#tier-1-additions--fixes-structural-gaps-the-workflow-leans-on-hardest)
- [Tier 2 additions — fills under-covered foundational areas](#tier-2-additions--fills-under-covered-foundational-areas)
- [Tier 3 additions — the modern agent literature this repo is reinventing](#tier-3-additions--the-modern-agent-literature-this-repo-is-reinventing)
- [Tier 4 additions — fills genre gaps the manifest already names](#tier-4-additions--fills-genre-gaps-the-manifest-already-names)
- [What I would not add](#what-i-would-not-add)
- [The meta-observation](#the-meta-observation)
- [Relation to other open upgrades](#relation-to-other-open-upgrades)
- [Suggested next concrete step](#suggested-next-concrete-step)

---

## What the library exists to do

`canon/corpus/` is not "books I like." It serves three load-bearing functions in the 12-step workflow defined by `CLAUDE.md`:

1. **Grounds `canon-librarian`** — the primary retrieval agent, with the contract that every query must return at least one *contradicting* passage. This only works if the corpus actually contains contradictions on the topic asked.
2. **Grounds `outside-view`** — must consult canon before any `WebSearch` (its Mandatory #0). So the corpus has to contain reference-class and base-rate material, not only architectural classics.
3. **Indirectly grounds the three critics and the frame-challenger.** They don't query canon directly, but the librarian's distillation flows into the candidate the critics review. Whatever's missing from canon is missing from the orchestrator's working context after Step 6, by design.

So the right evaluation question isn't "are these good books?" — it's **"does the corpus give every workflow step something to grip on, including contradictions?"**

## The audit method

I read:

- `canon/sources.yaml` (28 entries, the human manifest)
- `canon/sources.ingest.yaml` (11 entries actually fetched by the script)
- `canon/refresh-feeds.yaml` (2 RSS feeds the refresher polls)
- `canon/corpus/` (21 ingested slugs on disk)
- `bin/ingest-canon.mjs` (the only writer to corpus)
- `.claude/agents/` (especially `canon-librarian.md`, `outside-view.md`, the three critic lenses, `frame-challenger.md`)
- The existing upgrade tickets that touch the canon (`corpus-bias-compensation-step`, `citation-audit-as-canon-discipline`)

Then walked the workflow step-by-step asking *"if a design question landed on this step, what in the corpus would the librarian have to offer?"* The table below is the result.

## Coverage map — workflow step vs. corpus support

| Step | What the step needs from canon | What canon offers today | Verdict |
|---|---|---|---|
| 1 Classify | Frames for new / replace / extend / migrate / refactor / investigation | Refactoring (Fowler, Feathers), Strangler Fig | **Adequate** for refactor / migrate; nothing for *investigation* as a class |
| 2 Reframe | Cognitive material on framing, alternative optimization functions, anchoring | None directly. Kahneman / Tetlock cover judgment but not framing per se | **Thin** |
| 3 Outside-view | Reference-class forecasting, base rates | Kahneman & Lovallo 1993, Flyvbjerg 2006, Tetlock 2015 | **Strong skeleton, narrow** — three entries to ground every base-rate claim |
| 4 Librarian (broad) | Coverage with contradictions on tap | DDD, hexagonal, SRE, EIP, Nygard, Kleppmann, agents | **Strong on architecture-of-the-2010s; thin on product, security, cost, team topology** |
| 5 Explore | n/a (not corpus-backed) | — | — |
| 7 Scope-map | "Subsume vs replace vs extend" prior art | Feathers, Strangler Fig | **Adequate** |
| 8 Frame-challenger | Premortem, structured analytic techniques, devil's advocacy methodology | Chen 2024 (Devil's Advocate paper, LLM context) | **Critically thin.** One supporting entry — and it's about LLM agents, not how humans have done structured frame challenge for decades |
| 9 Generate | Concrete patterns | Strong (DDD, hexagonal, EIP, Nygard, Kleppmann) | **Strong** |
| 10a Critic-architecture | Module boundaries, coupling, invariants, dependency direction | Cockburn, Evans, Vernon, Helland | **Adequate** but missing Parnas, Conway, Brooks |
| 10b Critic-operations | SLO, error budget, blast radius, rollout, observability | Nygard, Google SRE, Allspaw | **Adequate** |
| 10c Critic-product | User contract, migration burden, affordance | **None** | **Empty.** Product critic has zero canonical material to ground its objections |

That table is the headline finding. **Three steps run on near-empty: product critique, frame challenge, and reframe.**

## What is good and should be left alone

- **Classical foundations are well chosen and largely uncontested.** Kleppmann, Evans, Vernon, Fowler, Hohpe, Nygard, Beck, Meszaros, Feathers — these are the right books, not "trending right now."
- **Outside-view triumvirate is correct.** Kahneman & Lovallo (the *origin* of the outside-view technique), Flyvbjerg (reference-class forecasting in practice), Tetlock (calibration). If you had to pick three, these are the three.
- **Honest provenance discipline.** sha256, fetched_at, license tag, body_completeness enum, stale flag, fetch-mode validation, schema validator that fails fast on typos. Better than most "RAG" setups in industry.
- **Dead/blocked sources are handled honestly.** Cockburn served from Wayback Machine with a `notes:` explaining why; Helland marked `pdf-manual` so the script doesn't pretend; the hallucinated `agentic-problem-frames-2026` was caught and removed with a tombstone comment. This is excellent discipline.
- **Counterweights are deliberately included.** Vernon's *Strategic Monoliths and Microservices* sits in the manifest with the explicit note "Essential counterweight to microservices enthusiasm." That's the librarian-must-contradict rule encoded into the manifest itself.
- **Recent agent literature is real, not vibes.** The three Anthropic engineering essays, Shinn's Reflexion (2023), Chen's Devil's Advocate (2024) — all real, all relevant, all properly cited.

## Is it state-of-the-art? Verdict by genre

**Not as a whole.** Coherent and opinionated, but SOTA varies wildly by genre:

| Genre | SOTA verdict |
|---|---|
| Engineering classics (DDD / refactoring / data-intensive / messaging / resilience) | **Near-SOTA.** What a senior engineer would name unprompted. |
| Structured analytic techniques (which is what the workflow actually is, methodologically) | **Far from SOTA.** The single most-cited canonical text on adversarial analysis methodology — Heuer's *Psychology of Intelligence Analysis* (CIA, free PDF) — is absent. So is Klein's *Sources of Power* (premortem). So is Snowden's Cynefin. So is Wardley Maps. The workflow re-implements these techniques without citing them. |
| AI agent design 2024–2026 | **Half-SOTA.** Has Reflexion, Devil's Advocate, three Anthropic essays. Missing the rest of the foundational set: ReAct (Yao 2022), Self-Refine (Madaan 2023), Constitutional AI (Bai 2022), Tree of Thoughts (Yao 2023), Multi-Agent Debate (Du et al. 2023), LLM-as-Judge (Zheng 2023). The repo IS an agent system; it should know its own field's literature. |
| Product / strategy / org | **Basically empty.** The `# Topics not yet well-covered` comment in `sources.yaml` already names this gap (Team Topologies, Accelerate, security, ML system design). None of those have been added since the comment was written. |

## Tier 1 additions — fixes structural gaps the workflow leans on hardest

Ranked by *which addition unsticks the most workflow steps*, not by fame. Open-access where possible (the ingester only handles `html`, `html-multi`, `arxiv-abs`, `aws-docs`; PDFs route through `pdf-manual` + `bin/ingest-owned-book.mjs`).

| # | Work | Author / year | Why it's high-leverage | Fetch mode |
|---|---|---|---|---|
| 1 | *Psychology of Intelligence Analysis* | Richards Heuer, CIA, 1999 (free PDF) | **Single highest-leverage add.** The book is the original methodology text on Analysis of Competing Hypotheses, key-assumptions check, devil's advocacy, structured self-critique. The entire critic-stack is engineering-flavored Heuer. Unsticks frame-challenger and all three critics. | `pdf-manual` |
| 2 | "Performing a Project Premortem" | Gary Klein, HBR 2007 (~3 pp) | The frame-challenger step exists to do exactly this and has nothing to cite. The HBR original is short; widely-summarized open-access versions also exist. | `html` (where licensed) |
| 3 | "A Leader's Framework for Decision Making" (Cynefin) | Dave Snowden & Mary Boone, HBR 2007 | The classifier step labels requirements; Cynefin is the canonical sense-making frame for "obvious / complicated / complex / chaotic" problem types. Would directly improve Step 1. | `html` |
| 4 | *Shape Up* | Ryan Singer, Basecamp, 2019 (free HTML book) | **Fills the empty product-critic chair.** Concrete on appetite, scoping, de-risking, betting table — exactly the language the product critic needs to make objections that aren't hand-waving. | `html-multi` |
| 5 | "How Do Committees Invent?" + Skelton & Pais summary essays of *Team Topologies* | Conway 1968 + Skelton/Pais 2019 essays | Module-boundary critiques without Conway's Law are unmoored. Architecture critic needs this. | `html` |

## Tier 2 additions — fills under-covered foundational areas

| # | Work | Author / year | Why |
|---|---|---|---|
| 6 | "On the Criteria to Be Used in Decomposing Systems into Modules" | David Parnas, 1972 | The original module-boundary paper. Fowler/Evans cite it; canon should have the source. |
| 7 | "No Silver Bullet" | Fred Brooks, 1986 | Outside-view material on why architectural improvements rarely deliver 10x productivity gains. |
| 8 | *Accelerate* + DORA reports | Forsgren, Humble, Kim, 2018 + ongoing DORA | Operations critic currently can't cite the empirical base for "deploy more often = higher reliability." Public DORA reports are open-access. |
| 9 | "How Complex Systems Fail" | Richard Cook, 1998 (~5 pp, free PDF) | Allspaw cites it constantly; canon should have the original. |
| 10 | *Wardley Maps* | Simon Wardley, free Medium book | Strategic positioning lens for architecture decisions; would beef up the reframe step. |

## Tier 3 additions — the modern agent literature this repo is reinventing

The repo IS an agent system; it should cite its own field. All on arXiv or ACL Anthology, both already supported by ingest modes.

| # | Work | Author / year | Why |
|---|---|---|---|
| 11 | ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al., 2022 | The foundational reasoning-and-acting agent paper. |
| 12 | Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al., 2023 | The base self-critique loop the stack reimplements. |
| 13 | Constitutional AI: Harmlessness from AI Feedback | Bai et al., 2022 | Critique-and-revise as a principle. |
| 14 | Improving Factuality and Reasoning in Language Models through Multiagent Debate | Du et al., 2023 | The repo's three-critic minority-veto is essentially this; should cite the antecedent. |
| 15 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | Zheng et al., 2023 | Foundational on whether LLMs can critique each other reliably. **Would give the critic-panel an honest base rate to reason against.** |
| 16 | Generative Agents: Interactive Simulacra of Human Behavior | Park et al., 2023 | Multi-agent role-play patterns. |
| 17 | "LLM Powered Autonomous Agents" essay | Lilian Weng, 2023 | Most-cited overview of the field; good librarian fodder. |

## Tier 4 additions — fills genre gaps the manifest already names

The `# Topics not yet well-covered` comment in `sources.yaml` predicted these. They're still gaps.

| # | Work | Author / year | Why |
|---|---|---|---|
| 18 | *Security Engineering*, 3rd ed. | Ross Anderson, free online | Security critique invariants. Critic-architecture currently cannot ground a security objection. |
| 19 | *Refactoring Databases* (excerpts on author site) | Pramod Sadalage | Schema/data migration patterns. |
| 20 | AWS Well-Architected Cost Optimization pillar | AWS | Already ingest the SaaS Lens via the same `aws-docs` mode; cost pillar would add ~10 lines to `sources.ingest.yaml`. |

## What I would not add

- **More books just because they're famous.** *Design Patterns* (GoF) would add noise — the workflow doesn't ask design-pattern questions.
- **Microservices-pro books to "balance" Vernon.** The librarian-must-contradict rule is supposed to surface contradictions from *within existing entries* (Newman vs. Vernon, Helland vs. Kleppmann), not require a paired counterpart for every book.
- **More from Anthropic's blog right now.** The `corpus-bias-compensation-step` upgrade already names the Anthropic-source skew. The `refresh-feeds.yaml` will keep proposing more without intervention. **Net Anthropic count should probably go down, not up,** at least until the rest of the corpus catches up.

## The meta-observation

The repo is sophisticated about its own workflow — twelve steps, distillations, minority-veto, hard gates, replan-vs-rewrite — but the **library is curated to a noticeably lower level of sophistication than the workflow that consumes it.**

The workflow assumes a librarian that can produce frame-level contradictions on any design question. The corpus only really delivers that on architectural-classics-of-the-2010s questions. So when a question lands outside that center of mass — anything product-shaped, anything that needs a structured premortem, anything about LLM agent design — the librarian falls back on what's there, which biases the candidate, which the critics then have to catch from cold.

This is why closing the corpus gap produces a bigger quality lift than further workflow refinement: every workflow step still has to draw on the same shallow well, no matter how cleverly the workflow routes the water.

The diagnosis is broader than any single existing upgrade. `corpus-bias-compensation-step` says "act on the bias flags the librarian raises." This entry says "the bias is structural — the librarian is raising it correctly because the corpus actually doesn't have the material." `citation-audit-as-canon-discipline` says "mark each citation verified / asserted / cached." This entry says "yes, and many of the citations the workflow needs would have to be `asserted` because canon doesn't carry them."

## Relation to other open upgrades

| Upgrade | How this entry relates |
|---|---|
| `2026-04-26-corpus-bias-compensation-step` (no-brainer) | Adds a Step 6.5 that *acts* on bias flags. This entry says the bias is structural — fixing it at the corpus level reduces how often Step 6.5 has to fire. Complementary, not redundant. |
| `2026-04-26-citation-audit-as-canon-discipline` (no-brainer) | Adds verified/asserted/cached markers to citations. This entry would *raise the share of verified citations* by giving the librarian more material to ground claims in. Complementary. |
| `2026-04-26-author-attribution-for-community-plugins` (normal) | Touches the same trust-boundary surface (the `conoro` RSS feed is the closest existing case). Adjacent. |

## Suggested next concrete step

If only one thing is done from this entry: **ingest Heuer's *Psychology of Intelligence Analysis* as a `pdf-manual` entry.** That one book changes what the frame-challenger and all three critics are able to say, because the entire critic-stack is engineering-flavored Heuer that currently has no source to cite. Mechanics:

1. Add a `heuer-psychology-of-intelligence-analysis` entry to `canon/sources.ingest.yaml` with `fetch: pdf-manual` and a URL to the CIA's hosted PDF.
2. Add a corresponding entry in `canon/sources.yaml` under a new `analytic_methodology:` topic group.
3. Locally run `pdftotext` on the PDF and use `bin/ingest-owned-book.mjs` to populate `canon/corpus/heuer-.../source.txt` + `citation.yaml` + `README.md`.
4. Verify with a librarian test query on "competing hypotheses" or "premortem" — expect the passage to come back with citation.

Everything else in this entry can follow the same pattern, batched in groups of 3–5 ingests at a time.
