# Outside-view raw return

## 1. Reference class

**Primary:** "Internal documentation entries that reference an asset preserved on a sibling branch / archive / sidecar location, in a low-stakes, single-operator R&D repo, where the entries themselves are at the earliest lifecycle stage (captured, not yet acted on)."

**Adjacencies, in order of predictive value:**
1. **Deferred / dormant decisions in personal knowledge bases** (Zettelkasten "incubator" notes; Hammock-Driven Development pre-work piles). Most predictive — same scale, same stakes, same operator.
2. **ADR / RFC handling of dropped or "proposed but not accepted" entries.** Established conventions exist (Superseded, Deprecated, Rejected statuses).
3. **Dataset / artifact deprecation with surviving references** ("zombie datasets," Corry et al. 2021). Closest *formal* study; over-applies because their stakes are downstream-harm, yours are tidiness.
4. **Dormant feature flags / dead-code-with-comments.** Different domain (production code) but the same accumulation dynamic.

The personal-KB and ADR classes dominate. Dataset-deprecation is a stretch — invoke for failure modes, not base rates.

## 2. Base rate per option

No published rates exist for this micro-class. Estimates below are qualitative, anchored to what's known about ADR practice and personal-KB hygiene; flag as estimates.

| Option | Estimated rate of "actually resolved cleanly" | Estimated rate of "becomes zombie state" |
|---|---|---|
| (a) Restore directory to `main` | ~60–70% resolve | ~30% — because now the asset exists in two places and the branch divergence question is unresolved |
| (b) Mark superseded with honest-negation pointer | ~70–80% resolve | low — `superseded` is a terminal state in ADR practice; entry stops generating work |
| (c) Park with `⏸️` and resume condition | ~20–30% ever resume | ~70% — dormant items in personal KBs overwhelmingly stay dormant; "resume condition" is rarely tripped or noticed |
| (d) Write a new dependency-contract rule | ~10–20% the rule survives in practice | ~80% — single-instance rules in solo repos tend to be forgotten or routed-around within months |

The Heuer / Tetlock observation applies: explicit deferral mechanisms ("park", "watch list") are *underused as terminal states*. People put things on the list; the list grows; nothing comes off. ADR's "Superseded" is more honest precisely because it's terminal.

The "zombie datasets" paper (Corry et al. 2021, web-found, not in canon) makes the structural point: **the persistence of references after the underlying artifact has moved is the source of harm, not the move itself.** Their prescription is *active* communication of deprecation, not passive parking.

## 3. Position relative to base rate

**Features pulling toward resolution:**
- Single operator — no coordination cost on whichever option is chosen.
- Source material is preserved (not lost); the decision is purely about reference hygiene.
- Entries are at `🌱 created` — lowest sunk cost; cheap to terminate.
- The stack already has lifecycle states, so a terminal "superseded" mark is native, not a new convention.

**Features pulling away:**
- Solo R&D lab → no external pressure to close out items → high tolerance for accumulating state. This is the dominant risk.
- Two upgrade entries already in this state suggests a pattern, not a one-off.
- Option (d) is itself an instance of the class it's trying to govern (a new rule introduced to manage one broken reference) — meta-risk.

## 4. Typical failure modes by option

- **(a) Restore:** the duplicated asset diverges between `main` and the worktree branch. Six months later you don't know which is canonical. The original problem (cross-branch reference) recurs in inverted form.
- **(b) Supersede:** rare failure. Worst case: the negation note is too terse and future-you can't reconstruct *why* it was superseded. Mitigated by writing one sentence of context.
- **(c) Park with resume condition:** the entry sits at `⏸️` indefinitely. The resume condition is never checked because no process checks resume conditions. This is the **modal failure of personal-KB deferral mechanisms** — Hickey's "Hammock" works only when the hammock is actively revisited; in practice, items put down stay down.
- **(d) Write a new convention to fix one broken reference:** the canonical failure mode is **rule inflation** — the convention is written, applied to the two existing entries, then never invoked again because the situation is rare. The repo accumulates governance for situations that don't recur. In ADR practice this is called "process for a population of one." The rule outlives its trigger and confuses future readers about what's load-bearing.

The Heilmeier catechism (in your ingest queue) bites option (d) directly: *"What are the midterm and final exams?"* — a one-shot rule has no exam.

## 5. Outside-view verdict

**Below base rate for options (c) and (d). Within tolerance for (b). Mixed for (a).**

- Option (c) ⏸️-park is the **highest zombie risk**. Personal-KB deferral mechanisms have a poor track record of producing resumption. If chosen, it should carry a calendar-bound resume condition (date, not event), not an open-ended one.
- Option (d) is **rule-inflation-shaped**. Writing a dependency-contract for two entries in a solo repo is governance overhead disproportionate to recurrence. Defensible *only* if you expect ≥5 more cross-branch references in the next 6 months; otherwise it's process for a population of one.
- Option (b) supersede-with-negation is **closest to ADR's terminal-status convention** and has the best base rate of actual resolution. The honest-negation note is the load-bearing part — it converts the entry from "open question" to "closed decision," which is what actually clears state.
- Option (a) restore is **defensible only if the asset is genuinely needed on `main` for reasons independent of these two entries**. If the only reason to restore is to fix the references, you've solved a documentation problem with a structural change — wrong tool.

What would lift (c) above base rate: a date-bound (not condition-bound) resume trigger, plus a default-to-supersede rule if the date passes untouched. What would lift (d): evidence of recurrence (third instance), not anticipation of it.

Sources:
- *The Problem of Zombie Datasets: A Framework For Deprecating Datasets* (Corry et al., arXiv 2021) — not in canon; web-found; supports the failure-mode analysis for options (a) and (c).
- *Detecting Outdated Code Element References in Software Repository Documentation* (arXiv 2022) — empirical evidence that outdated references are the modal state, not the exception.
- Reference class forecasting — method anchor.

Canon stubs invoked from memory (not Grep-verified this run because corpus directory read failed): Hickey "Hammock-Driven Development" (deferral works only with active revisit); Heuer (explicit terminal states beat implicit watchlists); Heilmeier catechism (one-shot rules have no exam) — Heilmeier flagged as ingest-queue per note.
