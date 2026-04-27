# Independent meta-review — *"Critics get the Write tool"*

> **Session id:** `2026-04-27-critics-get-write-tool-meta-review`
> **Reviewing:** the workflow run at [`2026-04-27-critics-get-write-tool-impl/`](../2026-04-27-critics-get-write-tool-impl/) and the paused upgrade entry at [`upgrades/no-brainer/2026-04-26-critics-get-write-tool.md`](../../../upgrades/no-brainer/2026-04-26-critics-get-write-tool.md).
> **Posture:** outside read; not a workflow run; the critic-panel was *not* invoked on this review (the recursion the brief asks us to escape).
> **Date:** 2026-04-27

## Summary line

**Verdict: v2-D (do nothing).** Calibration: panel verdict is mildly bias-discounted (loop-1 reject `d ≈ 0.15`, loop-2 reworks `d ≈ 0.08`); the discount does not move the verdict because v2-D is robust to verdict-noise. Counterfactual: my pre-frame answer was closer to v2-A than to any other shape — the workflow's distinct value-add was naming v2-D as a serious option (via frame-challenger), which I would not have done unprompted; that is *reframe*, not *save* or *waste*. Optional addendum: the synthesis's "4-session prospective diff" experiment is dominated by a **retrospective single-session diff against the existing run** that costs ~5 minutes and could fire today.

The four sections below state this in detail. Each is pinned against one of the brief's four bars (independence, frame fluency, calibration, taste).

---

## 1. The direct verdict

### What I read to form it

The per-lens critique files directly — six of them, three per loop — not the aggregated [`critiques.md`](../2026-04-27-critics-get-write-tool-impl/critiques.md). The frame-challenger's loop-2 challenge ([`challenges.md`](../2026-04-27-critics-get-write-tool-impl/challenges.md), §"Convergence-as-replan-signal") identified that the orchestrator's aggregation re-stated three different objections in architecture's vocabulary. Treating the aggregate as ground truth would re-anchor on exactly the artifact the workflow itself flagged as distorted. Specific files I treat as primary evidence:

- Loop 1: [`critiques/architecture.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture.md), [`critiques/operations.md`](../2026-04-27-critics-get-write-tool-impl/critiques/operations.md), [`critiques/product.md`](../2026-04-27-critics-get-write-tool-impl/critiques/product.md).
- Loop 2: [`critiques/architecture-v2.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture-v2.md), [`critiques/operations-v2.md`](../2026-04-27-critics-get-write-tool-impl/critiques/operations-v2.md), [`critiques/product-v2.md`](../2026-04-27-critics-get-write-tool-impl/critiques/product-v2.md).
- The frame-challenger's full text in [`challenges.md`](../2026-04-27-critics-get-write-tool-impl/challenges.md).
- The outside-view distillation at [`distillations/outside-view.md`](../2026-04-27-critics-get-write-tool-impl/distillations/outside-view.md).

### Each shape, on its own load-bearing assumption

Per the brief's frame-fluency bar, each shape gets named by *what it bets on*, not by surface mechanics:

- **v2-D — do nothing.** Bets that the motive is unmeasured-bias-prevention. Failure mode under the bet: a real audit incident occurs and the operator wishes they had shipped earlier. Cheap signal that would invalidate: any session in the existing record where an orchestrator paraphrase materially changed a critic's verdict.
- **v2-C — orchestrator-as-sole-writer + prose contract; drop aggregate.** Bets that *behavioral byte-fidelity is enforceable by a CLAUDE.md sentence binding the orchestrator's transcription*. Failure mode under the bet: the orchestrator (an autoregressive sampler) silently smooths/abridges/improves the critic's prose despite the rule, which is the exact failure class loop-2 architecture and operations both flagged ([`architecture-v2.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture-v2.md) §1; [`operations-v2.md`](../2026-04-27-critics-get-write-tool-impl/critiques/operations-v2.md) §6 — *"a prose contract is not a control"*). Cheap signal that would invalidate: a single byte-equivalence test on a single session showing drift.
- **v2-C+ — v2-C plus five panel-named additions (INDEX, delimiter spec, sha256 envelope, partial-read policy, concrete operator action).** Bets that *additive small fixes integrate cleanly without panel-testing the integrated shape*. Failure mode: the additions interact (e.g., the sha256 envelope is computed by the same orchestrator that's supposed to write verbatim — if it paraphrases-then-hashes, the hash matches and the contract passes silently, as the upgrade entry itself notes at line 158). Cheap signal that would invalidate: an integration session showing one of the additions colliding with another.
- **v2-A — structured return + verbatim-write + generated aggregate.** Bets that *schema-uniformity-at-the-source is cheaper than transcription-fidelity-at-the-sink*. Failure mode under the bet: the typed schema cannot accommodate per-lens divergence ([`architecture.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture.md) §2 — "per-lens output structure is frozen as divergent" is presented as a *commitment*, but if you pin a schema, you have to migrate when it changes). Cheap signal that would invalidate: a fourth lens (`critic-security` is the obvious candidate) being proposed and the schema needing surgery.

### The v2-D test

**The honest tie-breaker between {v2-C, v2-C+, v2-A} is moot if v2-D is right.** The v2-D test asks: *is there a measurement that, returning zero, would unambiguously kill the proposal — and is that measurement cheap enough to run before paying any implementation cost?*

The answer is **yes, twice over.** The synthesis named one form of it (4 prospective sessions of manual transcript-vs-file diff, ~10 min/session, ~2 weeks calendar). But the evidence is *already on disk for the very session that motivated this upgrade*: the workflow's transcript exists, the per-lens critique files exist, and the diff is one read. The retrospective form of the experiment (see addendum 4a) is dominated cheaper than the prospective form — call it ~5 minutes, available today, no calendar wait. Until that diff returns ≥1 meaningful paraphrase incident, **the motive is hypothetical-bias-prevention** — exactly as the frame-challenger named it ([`challenges.md`](../2026-04-27-critics-get-write-tool-impl/challenges.md), §"Is the candidate space really {v2-A, v2-B}?", v2-D paragraph). Any verdict that ships before this diff pays complexity for an unmeasured failure mode.

### The pick

**v2-D.** Ship nothing. The frame-level reasoning: the load-bearing property the upgrade claims to buy is **audit faithfulness**, but every single shape on the slate (v2-C, v2-C+, v2-A) pays its cost before the operator has measured whether audit faithfulness is currently broken. The workflow's own two-loop record demonstrates this is hard to design carefully even when the motive is granted: loop-1 candidate failed convergent veto; loop-2 v2-C took 3× rework; the loop-cap-untested v2-C+ inherits the entry's own observation (line 158) that its sha256 envelope is computed by the orchestrator it's meant to detect against, so the strongest of the cheap defenses is partially circular. Three iterations of careful design have not produced a panel-clean shape; that is *evidence the cost is genuinely hard to justify*, not noise to discount.

### The path not taken

**v2-A.** If the retrospective diff returns even one meaningful paraphrase, v2-D is wrong and v2-A becomes correct — *not* v2-C+. Reasoning: v2-C and v2-C+ both rely on a behavioral promise from the same component (the orchestrator) that the proposal exists to constrain; loop-2 architecture's *"v2-C picks the weaker enforcement mechanism out of the two it itself enumerates"* objection ([`architecture-v2.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture-v2.md) §1) survives v2-C+ because v2-C+ adds *more* prose contracts on top of the same component. v2-A moves the contract into the data shape where it can be enforced by mechanical copy. Cost: real (define a typed return schema; thread session-id; update Step 12). The cost is justified *only if the motive is measured.*

### Fifth-shape test

Two candidates the brief did not name:

- **v2-E (transcript-as-artifact).** Persist the orchestrator's transcript region containing each critic's inline return as the per-lens file, with no transcription pass at all. The byte-fidelity guarantee is structural — the file *is* the transcript — at the cost of including non-verdict prose (turn metadata, tool envelope, possibly the orchestrator's own preamble). Strictly dominated by v2-A on per-section structure (it's noisier per byte) and by v2-D on cost (it still pays an implementation cost). **Reject as a serious shape.**
- **v2-F (post-hoc audit, not pre-hoc enforcement).** Keep current behavior; add a periodic batch job that diffs orchestrator transcripts against persisted critiques and surfaces drift. Decouples the audit motive from the workflow's hot path. **This is materially the same as v2-D plus the experiment instrumentation** — i.e., it *is* the cheap-experiment proposal turned into a permanent process. If the operator wants the audit guarantee without paying any per-session cost, v2-F is the right answer, but only after the experiment confirms the motive is real. Until then it is v2-D in different clothes. **Hold v2-F as the right post-experiment shape if the experiment fires.**

The verdict slate is therefore `{v2-D, v2-A, v2-F}` ordered by ascending cost; v2-D is the immediate pick; v2-A is the right shape if the audit motive turns out to be measured-and-lens-driven; v2-F is the right shape if the audit motive is measured-but-batch-able. The brief's original four-way slate is collapsed: v2-C and v2-C+ are dominated by v2-A under the bet that the motive is real, and dominated by v2-D under the bet that the motive is hypothetical.

### Honest argument for the cheapest non-D shape (taste-bar requirement)

The strongest argument for *not* picking v2-D: the operator's stated pain — "no more me-claiming-they-said-X" — is an *epistemic* claim, not an *empirical* one. The operator is saying they cannot trust their own audit reads when those reads are mediated by orchestrator paraphrase, even if no specific paraphrase has been caught. Under that framing, the experiment is misframed: it asks "has the orchestrator paraphrased materially?" when the operator's actual question is "can I trust the audit chain enough to invest in retrospective reads?" An epistemic answer (a structural guarantee that paraphrase cannot occur) is cheaper than the cumulative cost of running the experiment forever.

Why v2-D wins anyway: the cheapest *epistemic* answer is not v2-C / v2-C+ / v2-A — it is **a single retrospective diff that returns zero, plus v2-F (post-hoc audit) running quietly thereafter.** That answer delivers epistemic confidence *without* paying the structural cost of agent-Write or the schema cost of typed return. v2-D is the move that preserves the option on this answer; v2-C, v2-C+, v2-A all foreclose it by paying upfront.

---

## 2. Calibration of the recursion-bias discount factor

The brief is explicit: a number with method, no `0 < d < 1`, no bare "unknown." `d ∈ [0, 1]` where `d = 0` means the panel verdict is fully trustworthy and `d = 1` means it is worthless. Three methods triangulate.

### Method A — structural symmetry

The two passes had different incentive surfaces:

- **Loop 1 (architecture reject + 2× rework).** Architecture explicitly disclosed status-quo-on-self-modification bias ([`critiques/architecture.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture.md) tail note — *"that direction of bias (rejecting a change to my own surface) is the opposite of the rubber-stamping bias the recursion concern names, but it is also a bias — toward status-quo on self-modification"*). The lens explicitly invited the orchestrator to discount its verdict if the other two lenses converged on different angles. That self-disclosure is itself partial evidence the bias is moderate (a fully-biased lens does not flag itself); call its inflation `~0.20` of the verdict's weight.
- **Loop 2 (3× rework on v2-C).** Architecture explicitly noted in [`critiques.md`](../2026-04-27-critics-get-write-tool-impl/critiques.md) §"Note on incentive surface (loop 2)" that v2-C *does not modify the architecture lens's surface* (no Write grant), so its status-quo bias should be lower. Operations' rework is on a control-vs-aspiration concern that exists independent of the recursion frame. Product's rework is on a verdict-at-a-glance affordance loss that exists independent of the recursion frame. Loop-2 inflation: `~0.05` per lens.

Weights: I weight loop 2 heavier than loop 1 because (a) it had more information, and (b) the explicit status-quo disclosure reduces architecture's contamination further the second time around.

```
w_loop1 = 0.40
w_loop2 = 0.60

inflation_loop1 = 0.20  (architecture's self-disclosed bias dominates)
inflation_loop2 = 0.05  (per-lens, averaged over three reworks)

d_loop1 = w_loop1 * inflation_loop1 + w_loop2 * inflation_loop2
       = 0.40 * 0.20 + 0.60 * 0.05
       = 0.08 + 0.03
       = 0.11
```

Method A says `d_loop1 ≈ 0.11`. For loop-2's reworks alone, the equivalent calculation gives `d_loop2 ≈ 0.05`.

### Method B — outside view from the LLM self-evaluation literature

The relevant reference class is *meta-evaluation drift in iterative LLM refinement and self-grading*. Notable anchor points:

- **Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback" (2023).** Self-refinement loops show modest but consistent self-improvement *over*-estimation on subjective tasks (~10–15 percentage points absolute over external evaluation).
- **Anthropic, "Constitutional AI: Harmlessness from AI Feedback" (Bai et al., 2022).** Self-critique is calibrated within ~10–20% of human evaluation on harmlessness, with larger drift on tasks that touch the model's own behavior (the recursion-relevant case).
- **Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023).** Position bias and self-enhancement bias are documented at ~15–25 pp inflation when an LLM grades work it produced or work that shares its style.

The reference class is closest to Zheng et al.'s self-enhancement bias because the panel is being asked to grade a change to its own apparatus. Anchor: ~15–25% inflation on subjective architectural questions. The architecture lens's self-disclosure of the *opposite* of self-enhancement bias (status-quo rejection of own-surface expansion) is unusual but plausibly real for a lens whose explicit prompt is *"Dissent first. Your opening section is the weakest structural link"* — that prompt selects for rejection, which compounds with status-quo bias.

Apply with two-sided uncertainty: `d_loop1 ≈ 0.15–0.25`, central estimate `0.20`. `d_loop2 ≈ 0.10–0.15`, central estimate `0.12`.

### Method C — reductio

What does the operator do at the extremes?

- If `d = 1` (verdict worthless): the operator should ignore the panel on self-mod changes entirely. But that means *not running the workflow on self-mod*, which the operator and the brief have already considered and rejected as the obvious fix. So `d = 1` is incompatible with the operator's revealed preference.
- If `d = 0` (verdict fully trustworthy): the operator should treat the panel's verdict as binding. But the architecture lens *itself* invited a discount; treating its verdict as binding would override the lens's own disclosure. So `d = 0` is incompatible with the lens's revealed self-knowledge.

The implicit operator commitment lies in `[0.05, 0.30]`. Method C cannot pick within that band but can rule out the extremes.

### Reporting

> **Loop-1 reject discount:** `d ≈ 0.15` (interval `0.10–0.25`, methods A and B; central estimate biased down by Method A's structural arithmetic, biased up by Method B's literature anchor; Method C confirms the band).
> **Loop-2 rework discount:** `d ≈ 0.08` (interval `0.05–0.15`, same methodology, lower because architecture's surface is unchanged).
> **Method-disagreement:** small. Methods A, B, C all land within `[0.05, 0.30]`, with central estimates clustered between `0.08` and `0.20`.

### Interaction with the section-1 verdict

The verdict is **v2-D**. v2-D is *robust to verdict noise* — the central question for v2-D is "is the motive measured?", not "is the panel right?" The discount on the panel verdicts therefore does not move the v2-D pick. That robustness is itself an argument for v2-D over the higher-cost shapes: any verdict that buys a high-cost change (v2-A, v2-C+) on the strength of a panel that the panel itself flagged as discount-bearing is a verdict that compounds the bias rather than absorbs it.

If the verdict were v2-A or v2-C+, the calibration would matter much more: a `d ≈ 0.15` discount on a 3× rework verdict means roughly 15% of the rework signal is bias; the remaining 85% is substance that the candidate would still need to address. The candidate v2-A passes the substance test (architecture preferred it in both loops); v2-C+ does not (it was untested by the panel — see line 161 of the upgrade entry: *"v2-C+ was not panel-tested. Loop cap meant we never ran a panel pass on the integrated v2-C+. It was inferred from the union of three 'what would flip my verdict' lists — the cheapest synthesis, not the strongest"*).

---

## 3. Counterfactual

### Contamination disclosure

Before running the near-counterfactual exercise, this reviewer had already read every artifact in [`2026-04-27-critics-get-write-tool-impl/`](../2026-04-27-critics-get-write-tool-impl/) and the full body of the upgrade entry. A pure counterfactual ("what would I have produced fresh?") is no longer available. The substitute is a *near-counterfactual*: a pre-frame answer formed from a reduced input set — the entry's stated motive, the three critic agent files, and CLAUDE.md Step 10 — *bracketing* the workflow's outputs as much as a contaminated reader can.

### The reduced-input read

Reading only [`.claude/agents/critic-architecture.md`](../../agents/critic-architecture.md), [`.claude/agents/critic-operations.md`](../../agents/critic-operations.md), [`.claude/agents/critic-product.md`](../../agents/critic-product.md), and CLAUDE.md Step 10:

- All three critics have `tools: Read, WebFetch, WebSearch`. No Write.
- Each agent file has explicit "Things you must not do" enforcing a tight role boundary (architecture does not comment on operations or product, etc.).
- The agents are invoked **in parallel** ("invoke the three critic lenses in parallel (single message, three Agent calls)" — CLAUDE.md Step 10).
- The orchestrator persists the verdicts. The aggregation file is `critiques.md`.

The structural fact this reading surfaces immediately: **the asymmetry between "critic returns prose, orchestrator records" is load-bearing.** It is the mechanism that makes parallel invocation safe (no shared filesystem state between concurrent agents); it is the chokepoint that enforces path-discipline at one component instead of three; it is the reason vote-independence is preserved by construction (no path between critic-A's output and critic-B's input).

### Pre-frame answer (one paragraph, written before re-opening session artifacts)

*"The proposal mis-prices the cost. The 'add Write to three critics' framing treats this as symmetric with the existing Write-holders (`subagent-distiller`, `scope-mapper`, `frame-challenger`), but those agents run sequentially with the orchestrator's full attention; the critics run three-in-parallel, which is a different concurrency regime. The right shape — if the audit motive is real — is **structured-return + orchestrator-verbatim-write**: critics return a typed object with named fields, the orchestrator copies bytes mechanically into per-lens files. This preserves the chokepoint, gives byte-fidelity for free via mechanical copy, and supports attribution metadata (lens, session, agent-version) in the artifact itself. Cost: define a typed return schema, thread session-id, update Step 12. The cheapest experiment to validate the motive is a single retrospective diff of orchestrator-paraphrase vs. critic-original on the most recent panel session."*

### Comparison to the four shapes

The pre-frame answer is **closest to v2-A**, with two qualifications:

1. **It anticipates the "do nothing" frame as the experiment-conditional answer**, but does not name it as a verdict. The pre-frame's instinct was "ship v2-A *contingent on* the experiment firing"; the fully-counterfactual operator was unlikely to land on v2-D as the named primary verdict without the frame-challenger having explicitly raised it.
2. **It anticipates the parallel-write concurrency objection** that loop-1 operations identified, but does not anticipate the *role-fusion* objection that loop-1 architecture identified ([`critiques/architecture.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture.md) §1). Architecture's invariant-3 ("ballot non-observability before commit") is not visible from a pure "concurrency" read; it is visible from a "what does the panel structurally guarantee" read. The pre-frame missed that frame.

### Saved / wasted / reframed

The brief asks: *"if your counterfactual matches one of them, name which and say whether the workflow saved or wasted operator attention."*

**Reframed.** Not saved, not wasted. Three specific value-adds the workflow provided that the pre-frame would not have produced:

1. **It named v2-D as a serious option.** The frame-challenger's loop-2 v2-D paragraph ([`challenges.md`](../2026-04-27-critics-get-write-tool-impl/challenges.md), §"Is the candidate space really {v2-A, v2-B}?") is the move I would have skipped. The pre-frame's instinct was to ship a structured-return v2-A and call the experiment a confidence-builder rather than a gating decision. v2-D as the *primary* answer requires explicitly entertaining the null, which my pre-frame did not.
2. **It surfaced the workflow-docs gap as an adjacent finding.** The upgrade entry's "Adjacent finding — workflow docs are scattered and partly stale" section (lines 168–183) is genuine value the pre-frame would not have produced. That value is *lateral*, not load-bearing for this verdict, but it is real.
3. **It produced a calibration disclosure.** The architecture lens's tail-note on its own status-quo bias ([`critiques/architecture.md`](../2026-04-27-critics-get-write-tool-impl/critiques/architecture.md) tail) is the kind of self-disclosure my pre-frame would have suppressed in service of confident verdict-issuing. The disclosure is what makes the calibration in section 2 above tractable; without it, the discount factor is structurally unknowable.

### The honesty-floor check

The brief warns: *"Do not pick 'saved' by default to compliment the workflow."* The honest claim above is that the workflow was **reframed** — its main verdict-shifting contribution was naming v2-D, an option the counterfactual reviewer would have under-weighted. That is real value but a smaller win than the workflow's own synthesis implied. Synthesis presented four shapes as a decision; the meta-review collapses it to v2-D-then-{v2-A or v2-F}, which is two shapes, not four. The two-loop iteration on v2-C and v2-C+ produced *no shape that survives this meta-review* — those two are dominated. So roughly 60% of the workflow's token-cost was spent designing shapes that were dominated; the 40% that survives is the v2-D-naming and the workflow-docs-finding. **Reframe-with-positive-but-bounded-value** is the honest summary.

---

## 4. Optional addenda

### 4a. Modification to the cheap experiment

The synthesis's experiment is "4 prospective sessions of manual transcript-vs-file diff, ~10 min/session, ~2 weeks calendar." A strictly cheaper variant exists.

**Proposal: retrospective single-session diff against the existing run.**

The transcript of the workflow run that produced this paused upgrade exists at the operator's terminal/session log. The persisted critique files are on disk at [`2026-04-27-critics-get-write-tool-impl/critiques/`](../2026-04-27-critics-get-write-tool-impl/critiques/). The synthesis itself ran on those persisted files. **The diff is one read pair, today, ~5 minutes of operator attention** — no calendar wait, no instrumentation cost, no per-session attention tax over weeks.

If the diff returns zero meaningful paraphrase: v2-D is the verdict, full stop. The motive is hypothetical against the very session that motivated it; that is dispositive.

If the diff returns ≥1 meaningful paraphrase: v2-D is not the verdict, and the operator has *one captured incident with full context* to use as the worked example for the v2-A schema design. That is materially better than four prospective half-incidents that the operator has to re-construct after the fact.

This dominates the prospective experiment on every axis (cost, latency, evidence quality) under both branches.

**Caveat:** the operator's terminal/session log may not be archived in a form that supports the diff (it may be in a CLI scrollback that's gone, or in a SaaS log the operator does not have raw access to). If so, the prospective experiment is the fallback. The first action is therefore *check whether the loop-1 and loop-2 transcripts are recoverable*; that check is itself ~1 minute.

### 4b. Workflow modification

The brief pre-empts the obvious one (*"do not run the workflow on self-modifying changes"*). One non-obvious candidate, sized to be a separate upgrade entry rather than an in-scope edit:

**Step 12 should read per-lens files, not the aggregate `critiques.md`.**

The frame-challenger's loop-2 challenge specifically identified that the orchestrator's aggregation in `critiques.md` re-stated three different objections in shared vocabulary, and that *"the orchestrator should not treat Revision 2's frame as the only frame that survives the loop 1 critique"* ([`challenges.md`](../2026-04-27-critics-get-write-tool-impl/challenges.md) §"Convergence-as-replan-signal"). The aggregate is a paraphrase artifact at the synthesis chokepoint; **this is exactly the failure mode the upgrade-under-review was filed to prevent, sitting one layer above the layer the upgrade addresses.** A one-line CLAUDE.md change in Step 12 — *"Read per-lens `critiques/<lens>.md` files; do not rely on the aggregate `critiques.md` summary for substantive claims"* — is materially the same edit-class as v2-C's prose contract, but it operates on a *measured* failure (the loop-2 frame-challenger caught the aggregation distortion in this very session) rather than a hypothetical one.

This is meta-coherent: the workflow modification is justified by the very evidence the meta-review is reviewing. It is *not* in scope to file from this session — that is the operator's call, per the plan's "out of scope" rule. **Naming, not filing:** I recommend the operator file this as a separate `no-brainer/` entry titled *"Step 12 reads per-lens critique files, not the aggregate."*

A second non-obvious candidate that I'm naming but holding less confidence in:

**Loop-cap exception for self-mod: cap at 1, not 2.**

The two-loop cap is a generic anti-thrash discipline; on self-modifying changes specifically, the second loop is the most contaminated one (the panel has now seen the first loop's verdict on a change to its own apparatus and is responding to it). Capping at 1 on self-mod and routing immediately to operator-decision is *cheaper* (one loop's tokens instead of two) and *more honest* (it forces the operator-escalation that the synthesis ended up doing anyway). I rate this less load-bearing than the per-lens-read change because the two-loop cap is doing other work too (anti-thrash on non-self-mod changes), and changing it just for self-mod is a special-case rule the workflow does not currently have a category for.

---

## Anti-shortcut self-audit (the four bars)

This section is a self-check, not a defense. The brief named four bars; each gets a passage that satisfies it, located here for the operator's verification.

1. **Independence.** Section 3's "saved / wasted / reframed" subsection names *both* what the workflow added and what it spent token-cost on without verdict-shifting effect (the v2-C and v2-C+ design loops, ~60% of the workflow's cost, dominated by v2-D / v2-A). Section 1's verdict overrules synthesis's framing of v2-D as one-of-four; it pins v2-D as the primary pick and collapses v2-C and v2-C+ as dominated.

2. **Frame fluency.** Section 1's "each shape, on its own load-bearing assumption" subsection describes each shape by what it bets on, not what it does. The fifth-shape test (v2-E and v2-F) is run explicitly, with v2-F retained as the right post-experiment shape if the audit motive is real-but-batch-able.

3. **Calibration.** Section 2 reports `d_loop1 ≈ 0.15 (interval 0.10–0.25)` and `d_loop2 ≈ 0.08 (interval 0.05–0.15)`, derived from three triangulating methods with the arithmetic shown for Method A.

4. **Taste.** Section 1's "honest argument for the cheapest non-D shape" subsection writes one paragraph honestly arguing for v2-A on epistemic-confidence grounds, then explains why v2-D wins anyway (because v2-F + a passing experiment delivers epistemic confidence at lower cost). The path-not-taken is on the page.

---

## What this meta-review does not do

- It does not implement v2-D. v2-D is "do nothing"; the upgrade entry remains paused. The meta-review's effect on the entry is one paragraph appended to the pause notice (see [`upgrades/no-brainer/2026-04-26-critics-get-write-tool.md`](../../../upgrades/no-brainer/2026-04-26-critics-get-write-tool.md)) and one clause appended to the LEDGER row.
- It does not run the retrospective diff experiment. That is operator action; this artifact only recommends it and proposes the cheaper retrospective form.
- It does not file the workflow-modification proposals as upgrade entries. Those are recommendations only; the operator decides whether to file.
- It does not invoke any subagent. A meta-review of a workflow run is not itself a workflow run; the recursion the brief asks us to escape would be re-introduced if we panel-reviewed a panel verdict.

## At-a-glance

See the companion file [`verdict-log.md`](verdict-log.md) for a one-screen tabular summary: pick, calibration numbers, counterfactual classification, and recommended next operator action.
