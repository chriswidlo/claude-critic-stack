# Candidate v2 — `2026-04-27-critics-get-write-tool-impl`

## Position

**Recommend v2-C: orchestrator-as-sole-writer with a byte-fidelity prose contract on the orchestrator's transcription behavior, no Write grant to critics, no new agent, per-lens file as the operator-facing surface, no aggregate `critiques.md`.**

This is a substantial pivot from the original entry's plan. The 12-step run-through-repo workflow surfaced — through loop 1's convergent panel veto and loop 2's frame-challenger pushback — that the original frame (`extend + tool-grant`) and the loop 1 candidate (add Write to critics + Defense 1 + Defense 2) both collapse a category change into precedent-by-analogy reasoning that breaks under parallel-write and self-modification. v2-C is the cheapest shape that addresses operations' and product's *actual* objections (concurrency posture, operator surface) without buying into the parliament metaphor that loop 2's frame-challenger argued is over-fitted to architecture's vocabulary.

The recommendation is conditional. Four shapes were evaluated; the operator may legitimately prefer a different one if the conditions named below shift.

## The four shapes evaluated

| Shape | What it is | Where the work goes | Audit trail provenance | Operator surface |
|---|---|---|---|---|
| **v2-A: Structured-return + orchestrator-verbatim-write** | Critics return typed structured object; orchestrator copies bytes mechanically. | Orchestrator (mechanical writer); critic (renders into typed shape). | Mechanical copy from typed return; structurally indistinguishable from paraphrase to a downstream reader without provenance metadata neither v2-A nor v2-B propose. | Per-lens files; format pinned by structured shape. |
| **v2-B: Dedicated `recorder` agent with `Write` only** | Critics return prose; new `recorder` agent persists each lens's bytes serially. | New agent. Critic returns prose. Recorder writes. | Recorder agent attribution; new primitive in stack. | Per-lens files; recorder-defined format. |
| **v2-C (recommended): Orchestrator-as-sole-writer + byte-fidelity prose contract** | Critics return prose; orchestrator persists bytes verbatim under a CLAUDE.md prose contract that forbids paraphrase, summary, or reformat between agreed delimiters. | Orchestrator (sole writer, contract-bound). Critic returns prose. | Orchestrator attribution + prose contract on transcription behavior. Provenance lives in the contract, not in the file. | Per-lens files (the operator surface). No aggregate. Step 12 reads per-lens files directly. |
| **v2-D: Null hypothesis (do nothing)** | Reject the user's motive as unmeasured. Keep current behavior. | Orchestrator (current behavior). | Orchestrator paraphrase as today. | Aggregate `critiques.md` as today. |

## Why v2-C wins under loop 1's actual lens objections

Reading the per-lens loop-1 files directly (per loop 2's frame-challenger insistence that the orchestrator was over-reading "convergence") shows operations' and product's frame objections are *not* clerk-voter-separation objections. They are:

- **Operations:** concurrency posture is a step-change, not extension. Modal failure mode is stale-session/wrong-path writes under parallel invocation. **v2-C resolves this entirely** — there is no parallel write because there are no parallel writers; the orchestrator writes serially after reading each return. The objection's surface area collapses.
- **Product:** the frame is orchestrator-internal; the operator-facing artifact is unnamed; the thin-index `critiques.md` is an unnamed schema; Defense 2 is an unconditional tax. **v2-C resolves operator-surface naming** by making the per-lens file the operator surface (no aggregate to silently change meaning). It eliminates the unnamed schema (no thin index). Defense 2 is dropped (see "What is *not* added" below).
- **Architecture:** role-fusion / parliament-vs-pipeline. **v2-C resolves role-fusion** — the orchestrator is the sole writer (clerk); critics never touch Write (voters). But it does so *without adopting the parliament metaphor as a frame* — the resolution is "preserve today's chokepoint and add a transcription contract," which is parsimonious in primitives, not in metaphors.

The frame-challenger's pushback in loop 2 was that the orchestrator collapsed three different lens-objections into architecture's vocabulary. v2-C respects that pushback by addressing each lens-objection on its own terms.

## What v2-C ships

1. **No frontmatter changes to the three critic agents.** They keep `tools: Read, WebFetch, WebSearch`.

2. **CLAUDE.md Step 10 update.** Replace *"Aggregate verdicts into `critiques.md`"* with:

   > *"Each critic returns its verdict as prose, framed by `<critique>` and `</critique>` delimiters. Persist each lens's bytes verbatim to `.claude/session-artifacts/<session-id>/critiques/<lens>.md` — copy the bytes between the delimiters with no paraphrase, summary, or reformat. Read those files for the panel's full reviews and apply minority-veto. **Do not produce an aggregate `critiques.md`** — the per-lens files are the operator-facing surface and Step 12 reads them directly."*

3. **One sentence added to each critic's body output-instructions.** Single sentence: *"Frame your verdict between `<critique>` and `</critique>` delimiter lines on their own lines. The orchestrator persists everything between the delimiters verbatim; you control the bytes the operator reads."*

4. **CLAUDE.md Step 12 update.** Replace *"Critiques summary"* with *"Per-lens critiques (read `critiques/<lens>.md` for each)."*

5. **Session-artifacts README update.** Description shifts from "`critiques.md` aggregate" to "per-lens `critiques/<lens>.md` files; no aggregate."

## What v2-C does *not* ship (vs. loop 1 candidate)

- **No Write tool grant to critics.** The frontmatter stays as-is. This is the structural answer to architecture's role-fusion objection.
- **No Defense 2 (auto-replan-on-self-modification).** Product objected on operator-tax grounds; v2-C drops the rule. The recursion concern is escalated to operator (see "Operator-escalation" below) instead of patched at the routing layer.
- **No Defense 1 (instruction-level no-sibling-read).** Not needed: critics never have Read access to `critiques/<lens>.md` — the orchestrator writes them after the panel completes. Vote-independence preserved by construction.
- **No thin-index `critiques.md`.** The aggregate is dropped, not preserved-as-residue. Step 12 reads three files directly. This eliminates the unnamed-schema objection.
- **No shared output schema across lenses.** Same as loop 1 candidate; per-lens divergence preserved deliberately.
- **No co-ship with upgrade #3 or #14.** Same reasoning as loop 1 candidate, but stronger: v2-C's failure mode is "orchestrator paraphrases despite the contract," which is detectable by reading the orchestrator's transcript — not silent. The need for harness-level enforcement is materially lower than under loop 1's parallel-write design.

## Conditions under which the operator should pick a different shape

- **Pick v2-A** if attribution metadata becomes a load-bearing requirement (i.e., the operator wants downstream tooling to assert "this file's bytes were produced by agent X, not orchestrator Y" cryptographically or structurally). v2-A's structured-return is the cheapest shape that supports per-section attribution.
- **Pick v2-B** if a future need arises to persist artifacts produced by *many* agents (not just three critics) under uniform contract. v2-B's `recorder` agent generalizes; v2-C's prose contract does not.
- **Pick v2-D** if the operator concludes the user's original motive is hypothetical-bias prevention with no measured incident on file. The frame-challenger named this honestly: there is no audit incident in this stack's session record where an orchestrator paraphrase mis-represented a critic's verdict. v2-D ships under the null hypothesis until measurement justifies a change.

## Operator-escalation (the recursion frame)

The frame-challenger argued in loop 2 that the recursion concern is structurally unresolvable inside the panel — any verdict on a self-modifying change is discounted by an unknown factor that the panel itself cannot calibrate. **The orchestrator agrees.**

The candidate names this as a meta-property of the run, not as one of three named uncertainties at the end of synthesis. Whatever the loop 2 panel returns:

- If the loop 2 panel approves v2-C, the synthesis tells the operator: *"panel approved v2-C; this approval is on a self-modifying change; the discount factor is not zero and the panel cannot tell you what it is. The architecture lens disclosed status-quo bias on self-modification in loop 1. Operator should weight accordingly."*
- If the loop 2 panel rejects v2-C, the synthesis tells the operator: *"panel rejected twice across loops 1 and 2; the rejection may be status-quo bias on self-modification (the same bias architecture disclosed in loop 1); the operator must adjudicate, not the panel."*

This is *not* an evasion. It is the honest output: the panel's verdict is structurally weaker on self-modifying changes than on any other class, and the cap-at-two-loops rule is the workflow's existing acknowledgment of that.

## Tradeoffs (named)

| Tradeoff | Direction (v2-C) | Rationale |
|---|---|---|
| **Audit faithfulness via author-attribution vs. via prose-contract on transcription** | Accept prose-contract. | The architecture lens explicitly argued these are equivalent on every property except attribution metadata; the operator's stated motive ("no more me-claiming-they-said-X") is closer to byte-fidelity than to attribution. v2-C delivers byte-fidelity at lower cost. |
| **Single-writer chokepoint preserved vs. orchestrator parsimony lost** | Preserve chokepoint. | Loop 1's frame ("orchestrator parsimony") was demoted by loop 2's frame-challenger as over-fitted to architecture's vocabulary. The chokepoint is the cheapest enforcement surface for path-discipline, session-id binding, and write-once-per-lens — all surfaced as invariants-at-risk in loop 1's architecture lens. |
| **Aggregate `critiques.md` dropped vs. operator habit-cost** | Drop. | Product's objection on the aggregate silently changing meaning is resolved by removing it entirely rather than redefining it as a thin index. Operators read per-lens files directly. The habit-cost is one CLAUDE.md sentence's worth of retraining. |
| **Defense 2 dropped vs. recursion concern unaddressed at routing layer** | Drop, escalate to operator. | The recursion concern is structurally unresolvable inside the panel; a routing patch is decoration. Naming the discount factor in synthesis (and in this candidate) is the honest acknowledgment. |
| **No co-ship with #3/#14 vs. outside-view's "below base rate" forecast** | Accept; v2-C's failure mode is detectable in the orchestrator's transcript, unlike loop 1's parallel-write failure mode. | The forecast was anchored to parallel-write risks. v2-C eliminates parallel-write. The "below base rate" verdict was on a different shape. |

## Assumptions (the recommendation flips if any are wrong)

**A1 (v2-C). The orchestrator can reliably honor a prose contract that forbids paraphrase, summary, or reformat between agreed delimiters.**
*Flips if wrong:* If the orchestrator routinely fails the contract (silently rephrasing, abridging, or "improving" the critic's prose despite the rule), v2-C is no improvement over today. Detection: the operator can compare the orchestrator's transcript (which contains the critic's raw return inline) against the persisted file. This detection is *available today* — unlike loop 1's wrong-path-write detection, which required an un-built hook. **This is v2-C's strongest claim.**

**A2 (v2-C). Per-lens divergence in output structure is acceptable to Step 12 synthesis without a shared schema.**
*Flips if wrong:* If Step 12 synthesis ends up doing schema-normalization work to read three different lens formats, the orchestrator-paraphrase-loss problem returns under a new name. v2-A would be the right answer in that case (structured-return forces uniformity at the source).

**A3 (v2-C). The recursion concern is genuinely unresolvable inside the panel and must be escalated to operator rather than patched at the routing layer.**
*Flips if wrong:* If a structural defense exists that v2-C is missing (the frame-challenger named "external second-opinion via shadow-comparator" as the strongest defense — it is un-built), the candidate ships under operator-discount when it could have shipped under structural-defense. The candidate accepts this gap honestly.

## Frame-level objections from loop 2 challenges — addressed

- **"Parliament frame may be over-fitted to architecture's vocabulary."** Addressed: v2-C does not adopt the parliament frame. The recommendation is justified by per-lens objection-resolution, not by metaphor.
- **"v2-C is the hidden shape the orchestrator's narrowing was concealing."** Addressed: v2-C is now the recommendation.
- **"v2-D (do nothing) is the null hypothesis the orchestrator has not entertained."** Addressed: v2-D is named as a legitimate operator choice if the motive is judged hypothetical.
- **"Convergence-as-replan-signal may be artifact, not signal."** Addressed: the loop 2 candidate is justified by per-lens objection resolution (operations' concurrency, product's surface, architecture's role-fusion) rather than by aggregated "convergence." The frame-challenger's reading is honored.
- **"Recursion concern should be escalated to operator, not synthesized through."** Addressed: operator-escalation is named as a meta-property of the run, included in the candidate itself, not deferred to synthesis-uncertainties.

## Ways v2-C could be wrong

1. **The byte-fidelity prose contract is not enforceable in practice.** Orchestrators (LLMs) routinely fail to honor prose-level "do not paraphrase" instructions when transcribing structured prose between delimiters; the orchestrator's autoregressive sampling may "improve" the critic's text despite the rule. If A1 fails detection-after-the-fact, v2-C ships a different paraphrase problem than today.

2. **Operator-escalation is a workflow hot-potato.** The candidate punts the recursion concern to the operator. If the operator has no calibrated way to handle "panel approved but discounted by unknown factor," the escalation is just a relocation of the same problem.

3. **The drop-the-aggregate decision frustrates Step 12.** If Step 12 synthesis is materially harder reading three files than reading one, the aggregate may need to come back as a thin index — at which point product's "unnamed schema" objection returns.

4. **The frame-challenger's "v2-D is the null hypothesis" challenge may be the right answer, and v2-C is paying complexity for a hypothetical bias.** v2-C's defense is that the prose-contract change is one CLAUDE.md sentence and three small additions — much cheaper than v2-A or v2-B, and reversible by deleting the sentence. But it is still a change; v2-D is still cheaper.

5. **Status-quo bias on architecture's loop-1 verdict may be doing more work than the architectural argument.** Architecture explicitly invited this discount. The orchestrator has not measured whether loop 2's recommendation is contaminated by it.
