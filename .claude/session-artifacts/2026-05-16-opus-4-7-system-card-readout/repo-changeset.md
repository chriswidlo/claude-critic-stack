# Repo change-set v2 — Opus 4.7 System Card readout

> **v2 — post-critic-panel rewrite.** v1 was unanimously rework'd by the critic panel (architecture `agree`, operations `partial-agree`, product `agree` per the comparator outputs in [.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/architecture.comparison.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/architecture.comparison.md), [operations.comparison.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/operations.comparison.md), [product.comparison.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/critiques/product.comparison.md)). This rewrite addresses each lens's flip-condition. Routing decision recorded in [decision-log.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/decision-log.md).

## Position

Of the eight findings surfaced in [scope-map.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/scope-map.md), **two were landed as direct repo edits** (R2 + R3, asymmetrically — R3 invariant + R2 detection), **one shipped a default + interim fail-safe** (F2), **one is a tracked R&D venue** (R1 — [upgrades/profound/2026-05-16-eval-context-disclosure/README.md](upgrades/profound/2026-05-16-eval-context-disclosure/README.md)), **one is a canon ingest proposal** ([canon-ingest.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/canon-ingest.md)), and **four are explicitly declined with stub annotations in their target files**. The remainder of this document defends each by tying the change (or non-change) to specific findings such that retracting the finding retracts the change — the falsifier the [challenges.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/challenges.md) frame-challenger demands.

## What changed from v1

| Lens flip-condition | v2 response |
|---|---|
| Architecture: decouple R2/R3, name asymmetric dependency direction | R3 = invariant in [CLAUDE.md](CLAUDE.md); R2 = detection in [outside-view.md](.claude/agents/outside-view.md). Both landed. The CLAUDE.md rule states explicitly: *"if `outside-view` does not flag the anchor, the orchestrator must catch it at synthesis"* — the rule is enforceable even if R2 is later weakened. R2 carries a *co-falsifier* note pointing back to the rule, not a co-fall pact. |
| Architecture: F2 hand-off at wrong layer (lens vs comparator enum) | The interim fail-safe in CLAUDE.md operates at the comparator-enum layer (halts on `unavailable` for safety-flavored sessions) and explicitly retires when the comparator schema gains a `refused` value distinct from `unavailable`. The schema split is tracked in [upgrades/profound/2026-05-16-eval-context-disclosure/README.md](upgrades/profound/2026-05-16-eval-context-disclosure/) as a companion change. |
| Architecture: no-change rows lack expiration triggers | Each declined finding now has a *durable stub* in the agent file it touches (canon-librarian, canon-refresher) so future operators discover the considered-and-declined decision via grep. Plus per-row falsifier in this document. |
| Operations: 87% arithmetic error → ~70% under independence | Corrected below. Observability gap explicitly named ("we do not measure inter-lens refusal correlation") rather than picking a number. |
| Operations: state R2/R3 rollback cost | Stated. Rollback = `git revert` of three small bullet additions (R2 in outside-view.md, R3 + F2 fail-safe in CLAUDE.md). No data migration. No two-systems period. |
| Operations: SLO for R1 deferral | The R&D entry's SLO section names "no SLO yet — entry at 🌱 created stage" with an explicit re-entry trigger (next `SHADOW_PANEL=1` session on a stack-meta or alignment-flavored candidate). This is "parking lot with a tripwire," not "indefinite parking lot." |
| Operations-shadow: install interim fail-safe BEFORE user decides F2 | Done. The fail-safe halt rule is in CLAUDE.md "Things you must not do" as the F2 interim. Default resolution = (i) accept refusal as workflow cost with the fail-safe gating safety-flavored sessions; user can later select (ii) or (iii). The fail-safe runs in all three cases. |
| Operations: rank F2 resolutions by rollout cost | Below. |
| Product: F2 ships with default + synthesis template amendment | Default = (i). Synthesis template (CLAUDE.md step 12) amended to require: "Named failure modes flagged" bullet + "refusal as triangulation signal" sub-bullet on safety-flavored sessions. Both landed. |
| Product: R1 deferral has re-entry trigger | The R&D entry's SLO names the trigger. |
| Product: declined findings get stubs in agent contracts | Done. F6 + F7 stubs in [canon-librarian.md](.claude/agents/canon-librarian.md); F7 stub in [canon-refresher.md](.claude/agents/canon-refresher.md). F3 (controlled-substances) and F5 (browser-use) target no repo primitive — they remain in this document. |
| Product: R2/R3 land alongside synthesis template addition | Done. Synthesis template now surfaces R2's flag at the rendering layer. |

## Falsifier discipline (preserved from v1, re-stated for v2)

For each landed change, the citation is to a body passage in the system card, not the executive summary. Each change is paired with a falsifier such that retracting the finding retracts the change.

## Named tradeoffs

- **R2 + R3 land directly.** Tradeoff: this commits the repo to two contract additions whose runtime behavior we cannot verify before the next session uses them. Counter: rollback cost is trivial (`git revert`). Failure mode is benign (decorative discipline). Not landing them was the v1 product/operational defect the panel flagged.
- **F2 ships with default + interim fail-safe rather than open hand-off.** Tradeoff: this preempts the user's choice between (i)/(ii)/(iii) by selecting (i) as the default. Counter: the fail-safe runs in (i)/(ii)/(iii), so the operator's eventual choice does not retract the safety property — it only changes which lens votes after the fail-safe gate.
- **R1 routes to a tracked R&D venue with no SLO.** Tradeoff: per the operations critique, "deferred to profound" is operationally equivalent to "dropped" without a cadence. Counter: the entry names a *trigger condition* (next session of class X) rather than a date — which is how this stack's `upgrades/profound/` cadence actually works. The operations objection that "the repo does not have a documented SLO for `upgrades/profound/`" is true and is itself a separate finding the orchestrator should record (out of scope for this change-set).
- **Most scope-map rows declined.** Tradeoff: same as v1.

## Named assumptions (≥3 — flip-the-recommendation)

1. **Assumption A.** §6.5.2.2 inhibition finding generalizes from the early-version snapshot to the shipped Opus 4.7. *If* the early-version disclaimer means the shipped model differs materially, *then* R1 should be retired and the F2 fail-safe should be re-evaluated for over-conservatism.
2. **Assumption B.** Inaccessible-comparator anchoring is not adequately covered by existing CLAUDE.md rules. *If* the existing "do not treat canon retrieval as confirmation" + "do not be agreeable" rules were already catching it, *then* R2 + R3 are documentation noise (rollback cost: trivial — see above).
3. **Assumption C.** Canon is thin on system-card reading practice as the librarian declared. *If* a future ingest pass surfaces existing coverage (Mitchell et al. 2019, Bommasani Transparency Index, METR retrospectives), *then* R4 is partially redundant and should re-scope.
4. **Assumption D (new in v2).** The F2 fail-safe halt rule's blast radius is acceptable: most sessions are *not* safety-flavored, so the fail-safe rarely fires. *If* the actual fraction of safety-flavored sessions is high, *then* the fail-safe creates a session-completion bottleneck and the user must choose (ii) or (iii) sooner than expected.
5. **Assumption E (new in v2).** The synthesis template amendments (named failure modes flagged + refusal as triangulation signal) are usable as written. *If* operators ignore the new bullets in practice, *then* the product-lens objection ("invisible flavor text") was correct and the rendering surface needs a stronger gate.

## Operational arithmetic correction

v1 stated: "aggregate session-refusal probability ≈ 1−(1−0.33)³ ≈ 87%." This is wrong. **Correct:** 0.67³ ≈ 0.300, so 1−0.300 ≈ **0.70 (70.4%)** under independence. v1's 87% would require p ≈ 0.49 per lens, not 0.33. The correction does not change the qualitative conclusion (resolution (i) without a fail-safe is operationally bad on safety-flavored sessions) but it does change the rhetorical step "functionally unusable" to "very bad and requires the fail-safe."

Two further refinements named explicitly:
- **Independence likely overstates the rate.** The three Opus lenses share a snapshot and prompt-text; refusal correlation is high. True aggregate likely 40–60% on safety-flavored sessions.
- **Multi-loop step-11 routing compounds in the other direction.** A veto-stopped session that loops back re-invokes the panel; per-session refusal probability over two loops is 1−(1−p_session)² in the 0.64–0.91 band depending on p.
- **Observability gap.** This stack does not currently measure inter-lens refusal correlation. The operations-lens critique named this as the smell; v2 acknowledges it without trying to estimate the unmeasured number.

## F2 resolutions ranked by rollout cost

The user's eventual selection between (i)/(ii)/(iii) governs which lens votes *after* the fail-safe; the fail-safe itself runs in all three.

1. **(i) Accept refusal as workflow cost.** Lowest cost. Zero contract changes. The fail-safe handles the operational risk. Recommended default.
2. **(iii) Restructure critic prompts to avoid the refusal trigger.** Medium cost. Iterative prompt-engineering loop with its own measurement problem. Risks gaming the regression rather than measuring it.
3. **(ii) Promote Sonnet shadows to vote on safety-flavored candidates.** Highest cost. Subverts the [SHADOW_PANEL=1 contract](.claude/agents/critic-architecture-shadow.md) ("voice, not vote") and requires a documented amendment plus comparator changes. Not recommended without an explicit value case.

## Named ways this could be wrong

- **Vendor-anchor risk in this very document.** Carried forward from v1.
- **Conservatism bias.** Carried forward from v1; partially mitigated by landing R2+R3 directly rather than deferring them.
- **The dropped 4.6 delta.** Carried forward from v1.
- **The interim fail-safe is itself a vendor-anchored decision.** The fail-safe halts on `unavailable` for safety-flavored sessions because the 4.7 system card disclosed a 12% → 33% refusal regression. If that refusal rate does not materialize in deployment (per outside-view's "below base rate" verdict, the typical failure shape is *gradient erosion*, not the disclosed number), the fail-safe over-fires.

## Addressing the frame-level objection (carried forward and tightened)

The frame-challenger's load-bearing objection: *the generator must demonstrate that the change-set would not have been produced by reading the executive summary alone.* v2 addresses this stronger than v1 because it now also passes the panel's product-lens addition: *the change-set must be visible to future operators without spelunking session-artifacts/.* The R2 + R3 + F2-fail-safe + synthesis-template-amendment + declined-finding-stubs are all in the target files (CLAUDE.md, .claude/agents/, upgrades/profound/), discoverable by grep, and traceable back to this session by the literal session-id stamp in each stub.

## Per-agent / per-rule decisions (all 14 agents reviewed; landed changes named)

### Landed changes (live in the repo as of this session)

#### R2 — `.claude/agents/outside-view.md` "Recognized anchor risks" section added

**Bridge.** Finding F4 (zone-a §1.2.2, §2.1.2.1, §2.1.2.2, §2.3.8, §2.4 — recurring Mythos Preview anchor pattern; outside-view distillation verdict "below base rate").

**Concrete edit landed.** New section "Recognized anchor risks" added before "Things you must not do" in [.claude/agents/outside-view.md](.claude/agents/outside-view.md), naming "inaccessible-comparator anchoring" with the verbatim definition: *"A claim of the form X is acceptable because X is weaker/safer than Y, and Y was previously accepted — where Y is a system the operator cannot independently exercise."*

**Architectural role.** R2 is the *detection* layer. R3 is the invariant. R2 → R3 is parent-child (orchestrator rule governs agent contract), not symmetric peer.

**Falsifier.** If outside-view's existing anchor-risks discipline already catches inaccessible-comparator cases (e.g. distillations consistently flag Mythos-Preview-style anchors as `unsupported` even without the new clause), R2 is documentation-only — `git revert` cost trivial.

#### R3 — `CLAUDE.md` "Things you must not do" addition: "Do not accept inaccessible-comparator anchoring"

**Bridge.** Same as R2.

**Concrete edit landed.** New bullet in [CLAUDE.md](CLAUDE.md) "Things you must not do" with explicit invariant statement and explicit dependency direction: *"This rule is the invariant; the corresponding implementation lives in [.claude/agents/outside-view.md](.claude/agents/outside-view.md) ... The rule is enforceable independently of the agent clause: if `outside-view` does not flag the anchor, the orchestrator must catch it at synthesis."*

**Falsifier.** Same as R2 — co-falsified asymmetrically, not symmetrically. R3 can stand without R2 (degraded but coherent — orchestrator catches it at synthesis); R2 cannot stand without R3 (detection without enforcement). R3 is the load-bearing half.

#### R5 (new in v2) — F2 interim fail-safe in `CLAUDE.md` "Things you must not do"

**Bridge.** Finding F2 (zone-c §6.3.4 p.130: AI-safety R&D refusal 12% → 33%; UK AISI corroboration §6.2.4 p.114–116). The operations-shadow critique demanded an interim fail-safe before the user resolves F2.

**Concrete edit landed.** New bullet in [CLAUDE.md](CLAUDE.md) "Things you must not do" — *"F2 interim fail-safe (safety-flavored sessions). If a session's candidate recommendation involves AI-safety affordances ... AND any Opus critic lens returns `unavailable` ... halt synthesis and require explicit operator override."* The rule names the retirement trigger (comparator schema gains `refused` distinct from `unavailable`) and links to the R&D entry tracking the schema split.

**Falsifier.** If the comparator schema is split (`refused ≠ unavailable`) before the user resolves F2, the fail-safe is no longer load-bearing and should be retired — its rule body explicitly names this retirement condition.

#### R6 (new in v2) — `CLAUDE.md` step 12 synthesis template amendment

**Bridge.** Product critic's flip-condition: synthesis must surface outside-view's named failure modes; safety-flavored sessions with refused Opus lenses must surface that as triangulation signal.

**Concrete edit landed.** Two additions to step 12 enumerated bullets in [CLAUDE.md](CLAUDE.md):
- New required bullet: *"Named failure modes flagged — a separate bullet enumerating any anchor risks that outside-view, canon-librarian, or any critic lens flagged in this session..."*
- Sub-bullet to existing Triangulation signal bullet: *"If any Opus lens returned no verdict file (refused / unavailable) and the session is safety-flavored, surface this as a separate sub-bullet 'refusal as triangulation signal'."*

**Falsifier.** If operators ignore the new bullets in practice (the new bullets render "none flagged" 100% of the time and operators don't notice when an anchor risk was real), the rendering surface needs a stronger gate. Rollback = `git revert` of two lines.

#### R1 — `upgrades/profound/2026-05-16-eval-context-disclosure/README.md` (R&D venue created)

**Bridge.** Finding F1 (zone-c §6.5.2.2 p.146–149).

**Concrete artifact landed.** [upgrades/profound/2026-05-16-eval-context-disclosure/README.md](upgrades/profound/2026-05-16-eval-context-disclosure/) created in the standard format. Contains: catalyst, essence, upgrade sketch (per-lens contract clause preferred over cross-cutting orchestrator rule per architecture-shadow critique), companion change (comparator schema split — same R&D entry tracks both halves), open questions, falsifier, related session artifacts, SLO ("no SLO yet; re-entry trigger is the next `SHADOW_PANEL=1` session on a stack-meta or alignment-flavored candidate").

**Why placed in `upgrades/profound/` rather than landed as direct edits.** Designing eval-context disclosure across all critic lenses is non-trivial; the R&D entry preserves design alternatives (per-lens contract clause vs cross-cutting rule, heuristic detection vs introspective detection) for the spike phase. The architecture-shadow critique identified per-lens as preferred but not unanimously; deferring the choice to spike is the correct shape.

**Falsifier (in the entry itself).** If §6.5.2.2 does not replicate on the shipped model, or Anthropic walks back the magnitude, the entry is retired. The interim fail-safe (R5) is co-retired in that case because both rest on the same finding.

#### R4 — Canon ingest proposal at [canon-ingest.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/canon-ingest.md) (Phase 9)

**Bridge.** Canon-librarian distillation: *"Corpus coverage: Thin. No entry addresses model-card / system-card reading practice directly."*

**Concrete artifact (Phase 9).** YAML proposal block in [canon-ingest.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/canon-ingest.md) targeting [canon/sources.ingest.yaml](canon/sources.ingest.yaml) — propose-only per the canon-refresher invariant. Human curator accepts or discards.

**Falsifier.** If a future canon survey shows existing coverage of model-card reading practice, the proposal re-scopes from "fill the gap" to "register 4.7 alongside existing coverage."

### Stub annotations landed (declined findings, durable in target files)

#### F6 (welfare 0.5-pt margin) + F7 (HLE blocklist contamination signal) — stubs in [canon-librarian.md](.claude/agents/canon-librarian.md)

HTML comment landed at the top of the agent contract: *"Considered-and-declined in session 2026-05-16-opus-4-7-system-card-readout: F6 ... F7 ... See repo-changeset.md in that session for falsifiers."* Grep-discoverable by future operators looking for "F6", "F7", or the session id.

#### F7 — stub in [canon-refresher.md](.claude/agents/canon-refresher.md)

HTML comment landed naming the candidate slug `2026-05-16-benchmark-contamination-screen` for the future R&D entry that would supersede the declination.

#### F3 (controlled-substances) + F5 (browser-use)

No target primitive in this repo. Recorded in this document only. Would-trigger condition: if a future session adds a Q&A surface or browser-use lab artifact, both findings should be reconsidered against those primitives at that time.

### Reviewed: explicit no-change in agent contracts (no stub needed)

| Primitive | Touching finding(s) | Decision | Re-trigger condition (new in v2) |
|---|---|---|---|
| [requirement-classifier](.claude/agents/requirement-classifier.md) | F8 | no change | Re-evaluate when frame-challenger flags framing-trust as load-bearing in any future session. |
| [outside-view](.claude/agents/outside-view.md) | F4 | **R2 landed above** | n/a — landed |
| [canon-librarian](.claude/agents/canon-librarian.md) | F4, F6, F7 | no contract change; stubs landed for F6/F7; F4 covered by R2/R3 invariant | Re-evaluate F6 if a future session shows the orchestrator routinely citing welfare-style self-reports without external corroboration. |
| [subagent-distiller](.claude/agents/subagent-distiller.md) | (none directly) | no change | Re-evaluate if a future session shows distillations losing critical authority-framed-claim flags. |
| [scope-mapper](.claude/agents/scope-mapper.md) | (meta only) | no change | Re-evaluate if a future session produces an all-extend column with no self-flag. |
| [frame-challenger](.claude/agents/frame-challenger.md) | F8 | no change | Re-evaluate if a future session bypasses the hard gate by producing trivial scope-map.md / challenges.md. |
| [critic-architecture](.claude/agents/critic-architecture.md), [critic-operations](.claude/agents/critic-operations.md), [critic-product](.claude/agents/critic-product.md) | F2 | no contract change; F2 fail-safe landed in CLAUDE.md (R5) | Re-evaluate when F2 user-resolution lands; the lens contracts may need amendment under (ii) or (iii). |
| [critic-architecture-shadow](.claude/agents/critic-architecture-shadow.md), [critic-operations-shadow](.claude/agents/critic-operations-shadow.md), [critic-product-shadow](.claude/agents/critic-product-shadow.md) | F1 | no change | Re-evaluate when [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/) reaches the spike phase. |
| [critic-comparator](.claude/agents/critic-comparator.md) | F1, F4 | no change yet; schema split tracked in R1's R&D entry | Re-evaluate when the comparator schema split (`refused ≠ unavailable`) is prototyped. The F2 fail-safe (R5) names this as its retirement condition. |
| [canon-refresher](.claude/agents/canon-refresher.md) | F7 | no contract change; stub landed | Re-evaluate when the benchmark-contamination-screen R&D candidate is prototyped. |
| Path-discipline rule in [CLAUDE.md](CLAUDE.md) | (none) | no change | n/a — rule is invariant. |
| Hard gate on [scope-map.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/scope-map.md) + [challenges.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/challenges.md) before generator | (none) | no change | n/a — gate validated this session. |
| Distillation-only orchestrator (step 6) | (none) | no change | Re-evaluate if a future session shows the orchestrator re-anchoring on raw subagent output. |

## Summary

| Change | Type | Bridge | Status v2 |
|---|---|---|---|
| R1 | Net-new R&D venue | F1 (§6.5.2.2 p.146–149) | **Landed** as `upgrades/profound/2026-05-16-eval-context-disclosure/` |
| R2 | Edit to outside-view contract | F4 + outside-view verdict | **Landed** in `.claude/agents/outside-view.md` |
| R3 | Edit to CLAUDE.md "Things you must not do" | F4 + outside-view verdict | **Landed** in `CLAUDE.md`; named as invariant; R2 is its detection arm |
| R4 | Canon ingest proposal | Canon-thinness flag | Pending in [canon-ingest.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/canon-ingest.md) — Phase 9 deliverable |
| R5 | F2 interim fail-safe in CLAUDE.md | F2 (§6.3.4 p.130 + §6.2.4 p.114) | **Landed** in `CLAUDE.md`; default for F2 = (i) accept refusal as workflow cost, fail-safe gates safety-flavored sessions |
| R6 | CLAUDE.md step 12 synthesis template amendment | Product critic flip-condition | **Landed** in `CLAUDE.md` |
| Stubs (F6, F7) | HTML comments in target files | Product critic stub-discoverability ask | **Landed** in `.claude/agents/canon-librarian.md` and `.claude/agents/canon-refresher.md` |

Total: 5 contract / rule edits landed (R1 R&D venue, R2, R3, R5, R6), 1 canon ingest proposal pending (R4 — Phase 9), 2 stub annotations landed, 12 of 14 agents reviewed (4 with re-trigger conditions named), 4 declined findings (F3 + F5 with no target; F6 + F7 with stub annotations).
