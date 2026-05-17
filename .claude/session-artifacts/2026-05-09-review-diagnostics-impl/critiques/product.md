# Product-lens critique — review-diagnostics-impl

## Opening dissent (the thing the operator will notice and dislike)

The day this synthesis lands, the `/explain` dashboard gets *worse*, not better. Today the operator opens `/explain` and sees "~10 min" — a stub, but a number. Under the candidate's action 1 + action 7, that number is demoted, the per-step breakdown the operator literally asked for is deferred 6 months, and `verdicts` is deleted. Net product delta on the only operator-facing surface: one card goes blank, one card loses a field, zero cards gain anything. The operator asked "where did the 10 minutes go?" and the answer the synthesis hands back is "we removed the bad answer, come back in six months." That is a product regression dressed as canon discipline.

## 1. User-visible consequence

The `/explain` dashboard contracts. Specifically:

- The "average session duration" card either renders empty or carries a "no data yet" stub. Today it renders "~10 min." Operator-visible delta: a card that *suggested* an answer now visibly admits it has none.
- The `## Metrics` block in `ledger.md` loses the `verdicts` row. Operators who skim ledgers cross-session lose the at-a-glance "did this session converge?" column; they must open `critiques/*.md` per session to reconstruct it.
- Synthesis output (step 12) gains a Heilmeier-exam clause the operator must remember. That clause is a *new product surface* — a 6-month commitment baked into the upgrade-entry lifecycle row.

The candidate's own assumption #4 names this risk and waves it off ("vanity render"). The waving is unearned. The operator's catalyst question is the load-bearing input here; the candidate is overruling it on canon authority without operator consent.

## 2. Commitments implied

Once shipped, the operator is committed to:

- **A schema conformance contract** (action 4). The moment the README declares `tokens.by_agent` and `tokens.total` as *required* fields with consumer fallback rules, downstream consumers (ledger-render, `/explain`, future cross-session aggregator) become entitled to assume those fields exist. That is a contract, not a doc note. Reversing it later means breaking consumers. This commitment is good; flag it as a commitment, not a doc tweak.
- **A 6-month removal-review clock** (action 5). The Heilmeier exam is a *promise to the future operator*: at month 6, justify or remove. The product implication is that the diagnostics layer now has an expiration date stamped on it. If the operator runs <20 sessions in 6 months (the candidate's own assumption #1), the layer ships with a near-certain removal verdict baked in.
- **A canary warning surface** (action 6). The `/explain` invocation gains a one-line warning when 3 consecutive sessions report no data. This is a new operator-facing string that must be designed (wording, threshold, dismissal). The candidate sketches it in one sentence; that's not enough product specification for a string the operator will see repeatedly.
- **A removed `verdicts` field**. Once deleted, any future cross-session "verdict pattern by lens" analysis (named in the candidate's "ways this could be wrong" #1) must re-extract from `critiques/*.md`. The candidate concedes this. The commitment is: closing a door that was open in v1.

## 3. Migration burden

The candidate names this poorly. Concretely:

- **`/explain` skill** must be edited to (a) drop the `verdicts` read path, (b) drop or rephrase the duration card, (c) gain the canary warning render. Three coordinated changes, all on the only operator-visible surface.
- **`ledger-render` skill** must be edited to drop the `verdicts` column from the `## Metrics` block. The candidate says "consumers read `critiques/*.md` directly if they need verdicts" — that's a *new read path* in `ledger-render`, not a removal. Migration is "implement the new path before deleting the old field," not "delete and ledger-render adapts."
- **The schema doc** (`<target>/.claude/session-artifacts/README.md`) gains a new "Metrics conformance" section. Anyone writing future skills against `metrics.json` now has a contract to read and conform to. The candidate prices this at 30 min; the actual cost is the *ongoing* discipline of keeping the section honest as fields evolve.
- **The operator** must read this synthesis, internalize 7 actions, choose to enact them, sequence them correctly (action 4 must precede or accompany action 1, or `ledger-render` reads a deleted field), and remember the Heilmeier clock. That is a non-trivial cognitive migration the candidate prices at zero.
- **Future upgrade-entry authors** must learn the Heilmeier-exam pattern as a new lifecycle expectation. If the exam is good, generalize it; if it's a one-off, it confuses the lifecycle schema.

"Operator will adapt" is the missing-name; the operator is `chriswidlo`, the only consumer of this stack today, and the burden lands entirely on that one person across 7 distinct edits.

## 4. Product affordances — better and worse

**Newly possible:**

- A `/explain` invocation that *honestly admits* it has no data (if action 6 lands and the card is rewritten to match). This is a real product win — replacing a stub with truth.
- A schema-conformant `metrics.json` that future skills can read defensively. Affords building cross-session aggregators without re-discovering field semantics.
- A clean Heilmeier-style exit ramp for instrumentation that doesn't earn its keep. Affords *not* accumulating dead diagnostics — a real long-term product hygiene win.

**Newly harder or pruned:**

- **"Where did the time go?" is no longer answerable, even badly.** Today the dashboard at least *gestures* at a duration. Tomorrow, under action 1 + action 7, it doesn't. The catalyst question is retired without replacement. That is not "simpler product"; it is "less product."
- **Cross-session verdict pattern analysis** is closed. The candidate concedes this. From the operator's seat: "I might want to know if `critic-architecture` rejects 80% of sessions" is a real future analysis; killing the parsed field today means re-extracting later. This is a pruned capability dressed as a regex cleanup.
- **The dashboard's information density drops.** Removing `verdicts` from `## Metrics` and demoting `duration_seconds` from the explain card means the operator's at-a-glance summary shrinks. The candidate frames this as "kill more than ships"; from a product lens it is "ship fewer answers to the same questions."

## 5. Frame-level objection

**The frame treats the diagnostics layer as an instrumentation/observability decision; from a product lens, this is a decision about what the `/explain` dashboard *promises the operator*.** The candidate inherits the frame's "validate-and-prune" posture and applies canon §As Simple as Possible to *internal* fields (`verdicts`) and *operator-facing* surfaces (`duration_seconds` on the explain card) with the same hand. They are not the same kind of thing. Killing an internal parsed field is a backend change; demoting a card on the only operator-visible surface is a product change. Conflating them under one "kill" verdict is a frame error.

A second frame-level objection: **the dogfooding-as-confounder reframe was a frame choice, not a discovery.** The operator explicitly positioned dogfooding as a feature ("the implementation will measure its own first review"). The frame.md treated it as a risk. The candidate inherits that posture and uses it to discount the only existing data point. From a product lens, if the operator only ever runs review-shaped sessions on this stack — which is plausibly true for a solo-operator design-review tool — then dogfooding samples *are* representative. The panel rejected the operator's own use-case framing and substituted "below-base-rate small-tools-die" pessimism. That deserves explicit operator consent, not silent inheritance.

A third: **the Heilmeier exam imports an industrial R&D-portfolio frame onto a one-operator workflow.** Heilmeier was designed for DARPA program managers selecting among competing projects. Applying it to a solo operator's diagnostics layer creates a deadline that the operator imposed on themselves via canon ventriloquism. Month-5-week-3 is not a productive deadline; it is artificial pressure manufactured by the panel and presented as canon discipline. The product question — "should this tool exist in 6 months?" — is real, but the answer "set a removal-review deadline" is one product policy among several, and the candidate picks it without naming alternatives (e.g., "review at next major workflow change," "review when session count crosses 20," "no clock, kill on first observed harm").

## 6. The catalyst answered honestly

Walking the candidate against the operator's literal questions:

| Catalyst question | v1 answer | Post-candidate answer |
|---|---|---|
| Where did the 10 min go? | partial (total) | none (demoted, deferred 6mo) |
| What cost the most? | yes (`tokens.by_agent`) | yes (preserved) |
| Are critics balanced? | yes (`tokens.by_agent`) | yes (preserved) |
| Did one agent dominate? | yes | yes (preserved) |

The candidate strictly subtracts from question #1 and is neutral on #2–4. There is no question on which the operator is *better off* on the day this ships. That is the product test the candidate fails to apply to itself.

The right product move is not "demote `duration_seconds`" but "tell the truth on the card": render *"no diagnostics data yet — populate by running ≥3 sessions"* in place of the "~10 min" stub, while leaving `duration_seconds` collected and rendered from the moment data exists. That preserves the catalyst answer's *trajectory* (it will get answered as data accumulates) without the dishonesty of the stub. The candidate skipped this option.

## 7. Seven actions is not a product-shaped recommendation for a review

The frame's "honest friction" mandate cuts both ways. Seven ranked actions, each with sub-rationale, named tradeoffs, and assumptions, is not honest friction — it is a backlog disguised as a verdict. The operator can act on three at most before the next session; the other four become a queue with no owner, which is exactly the research-theater failure mode the frame promised to counter-pressure. A product-shaped recommendation picks the load-bearing one (action 2: structural wrapper for AI-blindness, the actual safety property under review) and a small companion (action 4: the schema conformance contract, because it gates everything downstream), and rejects the rest as not-yet-justified by name. Seven actions queued is the panel doing what the frame told it not to do.

## 8. What the operator experiences the day this ships

1. Open `/explain`. The duration card is blank or stubbed differently. Mild surprise. (-)
2. Open the most recent `ledger.md`. The `## Metrics` block has one fewer row. Reach for `critiques/*.md` to reconstruct verdicts. (-)
3. Try to remember whether the new schema conformance contract requires a parser change before the next session, or whether the existing `metrics.json` already conforms. Open the README. (cost)
4. Notice the Heilmeier line in the upgrade entry. Internalize a 6-month deadline. Mild anxiety. (cost)
5. Run a session. Observe nothing has changed in *what* the layer measures, only what is exposed. The session that motivated the catalyst question still doesn't answer it. (-)

There is no "+" in this walk-through. The wins (structural AI-blindness wrapper, schema contract, canary) are *latent* — they pay off on a future failure that may never arrive. The losses are immediate and visible.

## 9. Verdict

**rework**

Single change that flips the verdict: replace action 1's "demote `duration_seconds`, kill `verdicts`" with **"tell the truth on the explain card and ledger render — render 'no data yet' explicitly when data is thin, but keep both fields visible the moment data exists"**, and cut the seven actions to two (the wrapper and the schema contract) with the rest explicitly declared *deferred-with-named-re-entry-condition* rather than ranked-but-unowned. That preserves the operator's catalyst questions as live product surfaces, lands the only two structural wins that justify the review, and stops the candidate from selling subtraction as progress.

What I'd watch if this rework lands: the wording of the "no data yet" stub on `/explain` and `## Metrics`. The operator will read that string every session until ≥3 sessions accumulate. If it reads as apology ("we couldn't measure this") it depresses confidence in the layer; if it reads as forecast ("this fills in after 3 sessions") it carries the product story honestly. That string is the smallest, most-visible product surface in the whole proposal, and the candidate did not specify it.
