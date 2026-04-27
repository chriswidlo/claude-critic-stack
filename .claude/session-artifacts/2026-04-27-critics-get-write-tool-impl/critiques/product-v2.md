# Critic — Product lens verdict (Loop 2)

`2026-04-27-critics-get-write-tool-impl` · v2-C

## 1. User-visible consequence

**The operator's panel-review surface goes from "open one file" to "open three files, with no index" — and the byte-fidelity guarantee is delivered by orchestrator self-discipline rather than by structure.** Today: open `critiques.md`, see all three lenses inline, scroll. Loop-1 candidate: open `critiques.md`, get a thin index, click through. v2-C: open the session directory, scan three filenames, open each in turn. The "verdict-at-a-glance" affordance — three verdict labels visible in one read — is *removed*, not merely relocated. There is no schema, no aggregate, no row of (lens · verdict · path); the operator must open at least one file (and for the dominant "did the panel approve" question, all three) to recover information that loop-1 made one read.

Secondary visible consequence: **the delimiter convention `<critique>…</critique>` becomes a user-visible artifact in the worst case.** If the orchestrator's transcription contract fails partially — pastes the delimiters along with the body, or misses the closing tag — the operator reads stray markup in `critiques/<lens>.md`. This is a new failure mode that loop-1's structured aggregate did not have.

## 2. Commitments implied

- **The per-lens file path `<id>/critiques/<lens>.md` is now the *sole* public surface of the panel.** No aggregate, no index, no synthesis row. Anything downstream — Step 12, future tooling, retrospective readers — must enumerate the directory or know the three lens names by convention. The directory listing *is* the schema. That is a contract about *discovery-by-convention*, which is weaker than a named index and weaker than a typed return.
- **The byte-fidelity prose contract on the orchestrator is a load-bearing rule with no enforcement surface.** CLAUDE.md prose binding LLM transcription behavior is the cheapest possible enforcement and the easiest to silently violate. Once shipped, every future session relies on a rule that has no harness, no hook, no test.
- **Per-lens divergence is frozen as policy, not accident.** Same as loop 1. v2-C makes it worse by removing even the thin-index normalization of the verdict label. Whatever each critic types is what lands.
- **"Operator-escalation" is now a named meta-property of every self-modifying run.** Synthesis must, going forward, emit a discount-factor disclaimer whenever the scope-map touches a critic-* file.

## 3. Migration burden

- **The operator** — must unlearn "read `critiques.md`" *and* unlearn loop-1's "read the thin index then click through." v2-C is a *second* habit-flip in one session for any operator who tracked loop 1.
- **Step 12 synthesis prose in CLAUDE.md** — must be re-pointed *twice*.
- **Two prior session directories** still contain the old aggregate-shape `critiques.md`. v2-C makes their interpretive gap worse than loop-1.
- **Every critic agent body** — gains one sentence about the `<critique>` delimiter convention. Each touch of that sentence is now a self-modifying change that triggers operator-escalation disclaimers in synthesis.
- **The operator who was waiting for the loop-1 thin-index migration to land** — now gets a different shape.

## 4. Product affordances better / worse

**Better:**
- **The `critiques.md` "silently changes meaning" objection from loop 1 is fully resolved.** v2-C removes the file rather than redefining it.
- **Defense 2's unconditional tax is gone.** The loop-1 affordance loss is restored. Operators can make small edits cheaply again.
- **The operator surface is now genuinely named.** v2-C says "the per-lens file is the operator-facing surface."
- **Per-lens debugging affordance preserved.**

**Worse:**
- **The "verdict-at-a-glance" affordance, which loop-1's thin index actually delivered, is *removed by v2-C*.** v2-C is *more aggressive than my loop-1 ask* and overshoots — I asked for the thin index to be pinned as a schema, not eliminated. v2-C trades one affordance loss for one objection resolution and calls it neutral; from the operator's reading habit, it is a net loss on the dominant skim path.
- **No normalization of verdict vocabulary.** Loop-1 thin-index could have pinned `approve | rework | reject` as the only legal labels. v2-C cannot.
- **Operator-escalation as a synthesis-step disclaimer is a new operator-facing affordance — a *worse* one.** It transfers decision-burden to the operator without giving the operator new tools to discharge it. That is workflow-evasion, not a product affordance.
- **No harness enforcement for byte-fidelity.** The operator's only verification path is manual transcript-diff.

## 5. Frame-level objection

**v2-C names the operator as a stakeholder but then *under-serves* them by removing the index-shaped affordance instead of pinning it.** The candidate treats the loop-1 product objection as "the aggregate silently changes meaning" and concludes "remove the aggregate." That is one valid reading; the *load-bearing* reading is "the operator's panel-review surface should be named, pinned, and at-a-glance." Removing the aggregate addresses the silently-changes-meaning sub-objection by deletion; it does not address the at-a-glance sub-objection at all.

Second frame-level objection: **escalating the recursion concern to the operator is a workflow-evasion dressed as honesty.** The candidate argues the panel cannot calibrate its own discount factor and therefore the operator must. That is true *and* incomplete. The orchestrator could deliver: a calibration mechanism (a checklist the operator runs against the verdict), a structural defense (shadow-comparator co-ship), or a softer routing rule (warn-but-not-block on self-modifying changes). "Tell the operator the panel is unreliable on this class and let them figure out what to do with that" is the *frame* that operator-escalation lives inside; it is not itself an affordance.

## 6. Verdict

**rework.**

Verdict flips to `approve` if the candidate (a) restores a *minimal* operator-facing index — not the loop-1 thin index, but a single `critiques/INDEX.md` (or one-line addition to `decision-log.md`) listing `lens · verdict-label · filename` with the verdict-label vocabulary pinned in CLAUDE.md to `approve | rework | reject`, preserving the at-a-glance affordance without re-introducing aggregate-redefinition risk; and (b) replaces the synthesis-time operator-escalation disclaimer with a *concrete operator action* — either a one-line checklist the operator runs against any self-modifying-change verdict, or a routing rule that warn-but-not-blocks (so the operator can override with one keystroke) — converting the escalation from "you decide" to "here is what to decide against."
