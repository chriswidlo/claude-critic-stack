# Product critique — verdict: rework

Persisted by orchestrator from inline return (critic agents lack Write tool).

## Verdict
rework

## Lens-specific critique

The candidate is rigorously argued but it is a *structure*, not a *product*. From the operator's seat the day-1 lived experience is a sequence of small decisions before any text gets written.

- **§"Locking dimension 1 — Document type set"** ships a 7×4 matrix. Operator must internalize before first entry. Confusable pairs (`hypothesis` vs `position-paper`, `position-paper` vs `rfc`, `observation` vs raw hypothesis). Candidate hand-waves: "type is reversible per-entry until articulated" — but the operator hits picking-the-type at write-time, every entry. Decision cost is paid 100% of entries, not 0%.

- **§"Locking dimension 2 — Maturity ladder semantics"** is five states. Candidate admits in §Tradeoffs that "no one writes a real `tested` entry; everything stays at `articulated`" is a real risk. From product: that's not a tradeoff, that's the *expected outcome* for solo operator with no experimentation harness (item H is itself unbuilt). Ladder reduces to two used states (`raw`, `articulated`) and three theatre states by week three. Day-60 audit notices the failure but doesn't prevent the operator paying ladder-tax for 60 days.

- **§"Lab as not-a-backlog"** explicitly forbids `untriaged`. Combined with 7-type × 5-rung × discipline-tag write-time decision, operator cannot capture a fleeting thought in <60 seconds. §Cheapest experiment admits this: day-1 is "spend day-1 writing four entries by retrofitting" — that's a project, not a capture flow. Realistic operator failure: thought arrives, operator estimates 90 seconds metadata work, defers, writes in `pages/` instead, lab stays empty. **Mode A by a different route — not "structure absorbs commits" but "structure deters writes."**

- **§"Locking dimension 4 — Lab/workflow integration protocol"** introduces three ports including write port gating ALL writes through `lab-curator` agent that does not yet exist. Candidate hedges in §Tradeoffs — "manual writes for first ~10 entries." Hedge eats the whole port. From product: day-1 surface is "no write port exists, write manually like any other markdown." Locking-dimension-4 claim is largely paper.

- **§"Three time-box commitments"** (day 7 / 14 / 60) is a calendar imposed on operator. Candidate: "Adopting time-box and reversibility violates 'no compromises.' This is intentional." Honest and product-poor: operator asked for structure, got back a *regime* with deadlines, ratification gates, audits, falsifiers. Operator will read this as "the workflow told me what to do instead of answering what I asked," and the lab inherits that emotional valence.

- **§"On the seven-capability taxonomy ownership"** unilaterally decides MODULES.md owns it. Operator must now write/maintain *another* file the candidate created (MODULES.md, INDEX.md, PROMOTION.md, TIMEBOX.md) before any `lab/<entry>.md` exists. **Four meta-files for zero content files on day 1.** Exact 3:1 ratio the day-60 falsifier is supposed to catch — baked in at day 0.

- **§"Cross-reference vocabulary"** asks operator to distinguish `builds_on` / `refutes` / `supersedes` / `relates_to`. For an entry with two outgoing references: 4×4 = 16 framings to consider. Distinction is genuinely useful but it's the second-order tax operator pays during write.

## Weakest link

**Write-time metadata budget.** Per entry: 1 type from 7, 1+ disciplines from ~7 (inherited from as-yet-unwritten MODULES.md), 1 maturity rung from 5, 0–N references with 4 relationship types each, plus INDEX.md update. Minimum-viable lab entry is ~5 metadata decisions before first sentence of body. No "express path" for low-stakes captures. Failure mode (silent reversion to `pages/`) is invisible to day-60 ratio audit because no commits land in lab/ to count.

## What the operator experiences day 1

1. Reads `lab/2026-04-26-lab-design.md`. Recognizes the design they just received.
2. Realizes no MODULES.md yet — discipline taxonomy doesn't exist on disk. Authors MODULES.md first (more meta-work) or stubs `discipline: cross-cutting` for everything (defeats the field).
3. Authors `lab/INDEX.md`, `lab/PROMOTION.md`, `lab/TIMEBOX.md`. ~30–60 minutes of meta-file authoring before content.
4. Tries to retrofit backlog item A (hooks) into `hypothesis` or `rfc`. Hits real product question: hooks aren't a hypothesis, aren't an `rfc` either (no concrete spec). `position-paper` closest fit — but type-table says position-paper output excludes "concrete proposed change." Spends 10 minutes resolving type-pick.
5. Picks maturity `articulated`. Adds discipline. No falsifier natural for hooks proposal — type-table says hypothesis requires falsifier. Backs up, re-types as `rfc`. Now needs "specification implementable as-is," which operator does not have.
6. Net day-1: ~2 hours of structure work, ≤1 substantive entry on disk, mild operator frustration that structure is interrogating their content rather than receiving it.

## What the operator experiences day 60

Day-60 falsifier check. Two product-surface problems:

1. **No operator-facing affordance for "what is my current ratio?"** Candidate names metric, no surface displays it. Operator runs `git log --stat` and counts manually, builds tooling (more meta-work, exacerbating ratio), or eyeballs. None is a product. Mode A could be in progress on day 30 with no signal.

2. **Remediation is "hard stop on schema."** Operator's seat: "you have failed; stop one of the two things you can do." No "you are 60% toward the threshold, here are entries that would re-balance." Day-60 surface is binary verdict, not gradient feedback.

Concrete day-60: operator reads TIMEBOX.md, runs `git log -- lab/`, manually buckets, gets some number. If 3.5:1, must decide whether 3:1 threshold is calibrated correctly — candidate provides no anchor. Audit is operator-as-self-judge, same surface that produced "no compromises" framing — known to be biased.

## Friction surface

1. Type-picking at write-time (every entry, ~30–120 sec, sometimes blocking)
2. Maturity-rung selection (every entry, plus deciding when to bump it)
3. Cross-reference relationship choice (`builds_on` vs `relates_to` daily; `refutes` vs `supersedes` rarer-but-load-bearing)
4. INDEX.md maintenance (load-bearing for read port; auto-generated or hand-maintained unspecified)
5. MODULES.md does not yet exist — discipline tags unanchored on day 1
6. **No express-capture path** — no-`untriaged` rule means even 10-second thought needs type, rung, discipline. Result: thought lands in `pages/`, invisible to lab.
7. Time-box guilt — day-7 and day-14 deadlines operator did not request and now must track or visibly fail
8. `lab/` rename — operator said `upgrades`; candidate said `lab` with reasoning correct on semantic merits. But operator will continue to *say* "upgrades" in conversation for weeks. Reasoning is right; override is still an override.

## Frame-level objection

**Candidate has framed the operator's problem as "design a structure that survives" when from product the operator's problem is "have somewhere I can write that doesn't punish me for writing."** Different products. Structure-that-survives optimizes for corpus integrity over years; place-to-write optimizes for marginal next entry. Candidate chose the former, treats latter as tradeoff. Legitimate frame *only if* operator's failure mode is "wrote too much un-structured content." Actual failure mode (per the meta-conversation: "kept getting rewritten, scope was too small") is *structural rewriting*, not capture failure — but remediation isn't necessarily more structure up-front. Could be: any structure that lets capture happen, plus curator pass that imposes structure post-hoc. Candidate forecloses that frame by making structure load-bearing at write-time.

Restated: candidate delivers a *publication system*. Operator asked for *R&D lab* — historically includes lab notebook, dirty whiteboard, half-formed margin note. Candidate has no surface for those. **R&D lab without a lab-notebook surface is a journal**, and a journal has different write-cadence than a lab. Frame should make capture-affordance a locking dimension and let publication-affordances be reversible — candidate has it the other way around.

## What would make this approve

1. **Add an express-capture path.** `lab/inbox/` (or any name) where entries land with only `type: observation` and a date. No discipline, no rung, no references required. Periodic curator pass (or operator pass) promotes inbox entries when they earn the ceremony. Capture in inbox *is* the processing.
2. **Reduce locking dimension count from 4 to 2 or 3.** Collapse 7-type set to smaller starter (e.g., `observation`, `claim`, `decision`, `killed-idea`); rest are reversible additions. Locking 7 types is not justified by canon (explicit gap territory) and forces commitment where reversibility is cheap.
3. **Show the day-60 ratio as a surface, not a check.** Either script operator can run (`./lab/ratio`) or one-line section in INDEX.md updated each commit.
4. **Honor the operator's name preference at least conditionally.** Offer `upgrades/` with note that `lab/` is the proposed rename pending one-week trial — make the rename a Step-12 *uncertainty*, not a Step-9 *position*.

Verdict moves to approve when there is a capture-without-ceremony path operator can use in 30 seconds. Without that, structure is correct in the abstract and silently bypassed in practice.
