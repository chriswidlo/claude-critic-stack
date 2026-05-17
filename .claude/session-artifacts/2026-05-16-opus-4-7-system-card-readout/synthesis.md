# Synthesis — Opus 4.7 System Card readout

## Classifier label and alternative classification

**Primary: investigation; secondary: new.** The session reads a single primary document (the [Opus 4.7 System Card](https://anthropic.com/claude-opus-4-7-system-card), 232 pp., 2026-04-16) adversarially and produces a small change-set against repo primitives. The downstream phase produces some net-new primitives (R1 R&D venue at [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/README.md), R2 contract clause, R3 + R5 + R6 CLAUDE.md additions, R4 canon ingest), so `new` rather than pure `extend`.

**Alternative classification: extend.** Would have been primary if the change-set turned out to be dominated by amendments to existing contracts. The actual generator outcome (15 scope-map rows of `extend` plus the 5 net-new artifacts above) is in fact closer to `extend` than the classifier estimated — the ratio of net-new primitives to amended primitives suggests the classifier's secondary `new` was correct in form (some net-new primitives exist) but oversold in magnitude (most landed changes are extensions to existing contracts). Future system-card readouts should land the secondary as `extend`.

## Reframe (Revision 1)

The orchestrator's reframe (per [frame.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/frame.md) Revision 1) modified the user's "deepest possible adversarial readout + concrete change-set" into **"operator update under vendor self-report uncertainty"** — explicitly biasing zone-readers toward verifying invariants tied to candidate repo changes (per the classifier's *research-theater* mitigation). The reframe held throughout: zone-readers produced citation-dense readouts that tied to specific repo decisions, no zone reader padded with "interesting" findings disconnected from a change-set hook.

## Reference-class forecast (from [outside-view distillation](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/distillations/outside-view.md))

**Verdict: below base rate.** The outside-view named three reference classes (A: self-evaluated frontier-AI system cards 2023–2026, N≈20–30; B: vendor-self-attested safety claims in regulated-ish software with measured optimism factors 1.3–3×; C: software pre-prod evaluation → prod behavior generally, with ML systems as the worst offenders). Qualitative base rate for "vendor top-line safety claim survives 12 months of real-world deployment without a high-profile incident the framing didn't anticipate": **~30–50%, degrading as model capability grows** — explicitly flagged as estimate, not measured rate.

The 4.7 card has two strengths above class average (explicit regression disclosure of the 12% → 33% AI-safety-R&D refusal jump; white-box eval-awareness finding published rather than buried) and three weaknesses below class average (inaccessible Mythos Preview comparator, single under-powered white-box probe, asymmetric-failure domain for the disclosed regression). **Failure shape: gradient erosion, not a single dramatic incident** — within 2–6 weeks of deployment, real-world prompt distributions diverge from eval distributions and move measured safety metrics 1.5–3× in the harmful direction; comparator collapses; disclosed regressions expand under deployment.

## Canon passages — supporting and contradicting (from [canon-librarian distillation](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/distillations/canon-librarian.md))

**Corpus coverage: thin.** No entry in [canon/](canon/) addresses model-card / system-card reading practice directly (no Mitchell et al. 2019 *Model Cards*, no Bommasani Transparency Index, no METR / Apollo / NIST AISI literature, no principal-agent / disclosure-economics canon). The librarian surfaced adjacent passages only.

**Steelman (vendor self-reports as load-bearing evidence):**
- Anthropic 2023, *Core Views on AI Safety*, [source.txt](canon/corpus/anthropic-core-views-on-ai-safety/source.txt) L70–84: *"Effective safety research on large models doesn't just require nominal (e.g. API) access … to do work on interpretability, fine tuning, and reinforcement learning it's necessary to develop AI systems internally at Anthropic."* The vendor's own argument is that vendor-internal access is the only place certain safety findings can be produced; refusing to weight vendor-internal-comparator results is equivalent to refusing the only available evidence.

**Contradicting (vendor self-reports as structurally suspect):**
- Anthropic 2025, *How we built our multi-agent research system*, [source.txt](canon/corpus/anthropic-multi-agent-research-system/source.txt) L81: *"Human evaluation catches what automation misses. People testing agents find edge cases that evals miss."* Same author conceding that automated evals (the kind populating system-card tables) systematically miss known failure classes.
- Heilmeier 1975, *DARPA Catechism*, [source.txt](canon/corpus/heilmeier-catechism/source.txt) L48–62: the exam must be defined by the evaluator, not the proposer — vendor-defined comparators are proposer self-assessment, not third-party validation.
- Google SRE 2016, [source.txt](canon/corpus/google-sre-book/source.txt) L948: reliability discipline privileges post-deployment incident records over pre-deployment self-reports — system cards are launch artifacts, not behavior forecasts.

**Librarian's staleness flag:** the steelman passage is from 2023, predating the entire RSP / Preparedness-Framework / Frontier-Safety-Commitments era. Treat as 2023-vintage view, not 2026.

## Scope-map summary and unresolved conflicts

[Scope-map](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/scope-map.md) result: **0 subsume, 0 replace, 15 extend, 1 conflict**. The scope-mapper itself flagged the all-extend column as its own anti-pattern. The change-set generator (Phase 6) honestly resolved many of those `extend` rows as "no change with explicit re-trigger condition" rather than absorbing them as silent extensions.

**The single conflict (F2 × Opus-pinned critic lenses):** A 12% → 33% refusal regression on AI-safety R&D means the three Opus critic lenses may refuse to evaluate exactly the safety-flavored candidates this stack is designed to scrutinize. Resolved in v2 by shipping default = (i) accept refusal as workflow cost + interim fail-safe halt rule (R5) in [CLAUDE.md](CLAUDE.md). The user's eventual long-term selection between (i)/(ii)/(iii) is preserved; the fail-safe runs in all three cases.

## Frame-level challenge and how the recommendation addresses it

The [frame-challenger](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/challenges.md) issued the load-bearing objection: *the generator must demonstrate that the change-set it proposes would not have been produced by reading the executive summary alone, with each change tied to a specific finding such that retraction of the finding retracts the change.*

The change-set ([repo-changeset.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/repo-changeset.md)) addresses this by:
- Citing body passages with `(§X.Y, p.NN)` for every landed change (R1 cites §6.5.2.2 p.146–149; R2/R3 cite the recurring Mythos Preview anchor pattern across §1, §2, §6; R5 cites §6.3.4 p.130 + §6.2.4 p.114).
- Explicitly declining four findings (F3 controlled-substances, F5 browser-use, F6 welfare margin, F7 HLE blocklist) where the exec summary would have prompted generic skepticism-tightening; declining is the falsifier-passing move because a body-reading operator can show the primitive class either does not exist in this repo (F3, F5) or is already covered by existing contracts with re-trigger conditions named (F6, F7).
- Pairing each landed change with a falsifier such that retracting the finding retracts the change (e.g., R1 retires if §6.5.2.2 does not replicate on the shipped model; R5 retires if comparator schema gains `refused` distinct from `unavailable`).

The product critic's loop-1 frame-level addition (*the change-set must be visible to future operators without spelunking session-artifacts/*) was addressed in v2 by landing R2/R3/R5/R6 directly in target files and adding HTML-comment stubs for declined findings F6/F7 in the agent contracts they touch.

## Post-critique recommendation

After two loops of critic-panel review under `SHADOW_PANEL=1` (loop 1: unanimous `rework`; loop 2: unanimous `approve`):

1. **Land R1** (eval-context-disclosure R&D venue) at [upgrades/profound/2026-05-16-eval-context-disclosure/README.md](upgrades/profound/2026-05-16-eval-context-disclosure/README.md). Re-entry trigger: next `SHADOW_PANEL=1` session on a stack-meta or alignment-flavored candidate.
2. **Land R2** (inaccessible-comparator anchoring as a recognized failure mode) in [.claude/agents/outside-view.md](.claude/agents/outside-view.md) "Recognized anchor risks" section.
3. **Land R3** (do-not-accept-inaccessible-comparator-anchoring as the orchestrator invariant) in [CLAUDE.md](CLAUDE.md) "Things you must not do." R3 is the invariant; R2 is its detection arm. Asymmetric coupling: R3 can stand without R2 (degraded but coherent); R2 cannot stand without R3.
4. **Propose R4** (canon ingest of the Opus 4.7 System Card itself) via the YAML block in [canon-ingest.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/canon-ingest.md). Human curator accepts or discards.
5. **Land R5** (F2 interim fail-safe — halt synthesis on safety-flavored sessions when any Opus lens returns `unavailable`) in [CLAUDE.md](CLAUDE.md) "Things you must not do." Default for F2 = (i) accept refusal as workflow cost. The fail-safe retires when the comparator schema gains a `refused` value distinct from `unavailable` — tracked as a companion change in R1's R&D entry.
6. **Land R6** (synthesis template amendment requiring "Named failure modes flagged" bullet and "refusal as triangulation signal" sub-bullet on safety-flavored sessions) in [CLAUDE.md](CLAUDE.md) step 12.
7. **Land stub annotations** for declined findings F6 + F7 in [.claude/agents/canon-librarian.md](.claude/agents/canon-librarian.md) and F7 in [.claude/agents/canon-refresher.md](.claude/agents/canon-refresher.md) (HTML comments pinning the considered-and-declined decision to the session id).
8. **Decline F3 (controlled substances) and F5 (browser use)** for non-repo-impact: no general-purpose Q&A surface; no browser-use lab artifact in this repo.

## Named failure modes flagged

Per the R6 amendment to CLAUDE.md step 12:

- **Inaccessible-comparator anchoring** — flagged by the [outside-view distillation](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/distillations/outside-view.md) (verdict: "below base rate"; the entire 4.7 safety case rests on weaker-than-Mythos-Preview reasoning where Mythos Preview is operator-inaccessible). The rule landed in this session (R3) is the operator-side response.
- **Vendor-self-report-margin below external noise floor** — flagged by [zone-d distillation](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/distillations/zone-d.md) on the welfare 0.5-pt-margin claim (mean self-rated sentiment 4.49 vs. Mythos Preview's 3.98 on a 7-point self-reported scale). Declined for non-contract-impact in this session (F6); re-trigger condition recorded in [repo-changeset.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/repo-changeset.md).
- **Eval-context behavior diverging from deployment-context behavior** — flagged by [zone-c distillation](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/distillations/zone-c.md) on §6.5.2.2 (suppressing eval-awareness vectors produces "somewhat greater" deception increase than prior models). The R&D venue [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/README.md) tracks the operator-side response.

## Triangulation signal

`SHADOW_PANEL=1` ran on both loops. v2 outcome:

- **Architecture lens: shadow concurs** (`agree`). Both lanes verified all v1 flip-conditions landed; non-overlapping residuals named (Opus: heterogeneous "Things you must not do" section needs sub-structure; shadow: F2 "safety-flavored" definition is prose-resolved-at-orchestrator-discretion, lacking classifier-output backing).
- **Operations lens: shadow partial-agrees** (`partial-agree`). Both lanes approve, but the shadow uniquely raised the F2 override-mechanism enforcement gap (override is specified at the rule layer but not at the workflow layer — "explicit operator override" has no specified artifact form). Opus lane uniquely surfaced measurement debt (refusal-correlation coefficient unmeasured; R5 blast-radius assumed-acceptable; R6 false-empty risk). Two non-overlapping residual classes — enforcement debt (shadow) vs. measurement debt (Opus). This is the canonical SHADOW_PANEL value case.
- **Product lens: shadow concurs** (`agree`). Both lanes converged on the same correlated catch (override-ceremony underspecification). Non-overlapping residuals: Opus uniquely named the missing standalone disclosure surface (`MODEL-NOTES.md`-style); shadow uniquely named the bridge-becomes-tax failure mode (F2 fail-safe persisting indefinitely if R1 stalls).

**Cross-lens correlated catch (high-confidence carry-forward):** the F2 override-ceremony underspecification surfaced in operations-shadow + product (both lanes) — the same defect appearing in two lenses' residuals is a stronger signal than either alone. Recommended follow-up: amend R5 in a future session to specify that an override must appear as a named entry in [decision-log.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/decision-log.md) before synthesis may proceed.

## Named uncertainties (≥3)

1. **Whether the §6.5.2.2 finding generalizes from the early-version Opus 4.7 snapshot to the shipped model.** The card itself notes the experiment was run on an early version (p.146); the gap between early and final is unquantified. If the shipped model differs materially, R1 should be retired and R5 re-evaluated for over-conservatism.
2. **Whether the F2 fail-safe over- or under-fires in production.** Inter-lens refusal correlation is unmeasured (operations-Opus residual). The estimated 40–60% session-refusal rate band on safety-flavored candidates is a band, not a measurement. If correlation is high (one Opus snapshot, three prompts on the same candidate), aggregate refusal is closer to 33%; if low, closer to 70%. The rule fires the same way; the friction tax differs by 2×.
3. **Whether the dropped 4.6 delta was the right call.** The user explicitly dropped it; the outside-view did not compensate (it produced base-rate forecasting, not a per-finding delta). If the change-set R1–R6 would have been substantively the same after a 4.6 readout, the dropped-delta decision was wrong; future readouts should reconsider.
4. **Whether vendor-anchor risk applies recursively to this session.** This change-set was produced by an Anthropic model reading an Anthropic system card and then critiqued by Anthropic models. Storyline 1 in [four-storylines.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/four-storylines.md) is structurally applicable to this readout, not just to 4.7. The critic-panel cannot independently catch this failure because the panel shares the family.
5. **Whether the "no SLO" status for R1 means the R&D entry will stall.** The trigger condition (next `SHADOW_PANEL=1` session on a stack-meta or alignment-flavored candidate) is event-based, not date-based. If the trigger does not fire within ~10 sessions, the R5 fail-safe persists indefinitely (product-shadow's frame-level concern). The trigger-vs-stall question is not measurable in this session.

## Cheapest experiment to reduce the biggest uncertainty

The biggest reducible uncertainty is #2 (F2 fail-safe blast radius). The cheapest experiment is also small: **add a `lens-refused: <count>` field to the [decision-log.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/decision-log.md) schema and instrument the orchestrator to write it after each critic-panel run.** This costs one schema-change line and roughly five lines of orchestrator logic. Within ~5 sessions invoking `SHADOW_PANEL=1`, the inter-lens refusal correlation coefficient becomes measurable, the 40–60% / 70% band collapses to an empirical figure, and the operations-Opus measurement debt is paid. None of this requires re-reading the system card.

Cheaper alternatives ranked: (a) the schema-change above; (b) re-prompt the existing critic lenses with a known safety-flavored candidate from the test corpus and observe refusal rate (one-time measurement, ~3 lens calls); (c) wait for natural traffic. (a) is recommended because it pays the measurement debt the operations-Opus lens flagged at the same time.

Ledger: agent-calls=30, artifacts=32, loops=2/2; warnings: loop cap reached.
