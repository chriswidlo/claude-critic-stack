# outside-view raw return

## Canon-first declaration

Canon inventory ([canon/sources.yaml](../../../../canon/sources.yaml)) covers the *forecasting* methodology (Kahneman/Lovallo 1993, Flyvbjerg 2006, Tetlock 2015 — present as inventory entries; corpus body is gitignored so only inventory citations are available, not passages) and *operations* adjacent to it (Google SRE 2016; Nygard 2018 *Release It!*). Canon does not cover three of the four candidate reference classes for this review:

- AI-observability projects (multi-agent transcript instrumentation) — gap. Web result is from disler/claude-code-hooks-multi-agent-observability and Anthropic's hooks docs, not in canon.
- Hook-based instrumentation tied to undocumented internal layouts — gap. Closest analog is Hyrum's Law, also not in canon.
- Self-measurement / dogfooding traps — partial. March (1991, in canon inventory) speaks to organizational self-assessment distortion; not specific to instrumentation.

The canon stub for Flyvbjerg supports the method of this forecast; the canon does not supply the base rate for the relevant class. Web search was used for currency on the AI-observability gap and the developer-tooling-instrumentation gap.

## 1. Reference class

The proposal straddles four classes; ordered by predictive value:

1. (Most predictive) **Hook-based instrumentation parsing an undocumented internal data layout of a fast-moving host product.** Concretely: a parser that walks `<encoded-cwd>/<claude-uuid>/subagents/agent-<id>.jsonl` plus sibling `.meta.json`, where the upgrade entry itself notes "undocumented in current Anthropic refs." Class members include parsers of Chrome's Library profile internals, parsers of Slack's local cache, parsers of IDE plugin transcripts, browser-extension instrumentation against private DOM. The host changes; the parser breaks.
2. **Per-session AI-agent observability layers** (multi-agent transcript token attribution, 2025–2026). A real and active class — disler's claude-code-hooks-multi-agent-observability is a public exemplar — but young enough that its base rate is poorly attested.
3. **Internal dev-tooling instrumentation that ships and then must justify its maintenance tail.** Broad and well-attested: instrumentation projects routinely ship and then decay because nobody owns the dashboard.
4. **Self-measurement / dogfooding loops** — instruments that measure the system that built them. Known to produce sample-of-one validation that overfits the easiest run.

I treat (1) as primary because it is the most binding constraint on the artifact's lifespan — even if everything else goes well, a layout change in Claude Code silently zeros the parser. The other three classes shape the cost / value distribution, but (1) shapes the survival distribution.

## 2. Base rate

Definition of success used here: "the diagnostics layer is still producing usable data 6 months from now without an unscheduled rewrite, and the data is consulted at least once per month by a human." Two clauses: survival + use.

Numbers (flagged as estimates where unsourced):

- Hooks against undocumented internal layouts — 6-month survival without rewrite is, in qualitative estimate, ~40–60%. Variance driven by host-product release cadence; Claude Code is shipping fast in 2025–2026, which pushes toward the lower end. Estimate, not sourced.
- Internal instrumentation continued use after 6 months — well-attested class, with the typical figure being ~30–50% of internal dashboards going unconsulted within a year of ship.
- Joint survival × use — multiplying these, a defensible base rate is ~15–30% of such projects "succeed" by the stated definition at the 6-month mark. Estimate; flag as such.

If the success definition is loosened to "the layer ships and is technically functional on day 1," base rate climbs to ~80%+ — but that definition is not interesting because it elides the maintenance tail.

## 3. Position relative to base rate

Features that move this proposal **above** the class average:

- The author and the consumer are the same person. No adoption gap.
- The instrumentation is small and self-contained (~600 lines, gitignored output).
- Failure mode is loud-ish. Parser returns "transcript-missing" rather than corrupt data — recoverable rather than silent-bad.

Features that move it **below**:

- The undocumented layout dependency is explicit and acknowledged.
- Loose regexes for verdict and loop detection.
- Hook stderr suppression is fragile (convention-based).
- Dogfooding-as-validation. The first measured session is a review session — the easiest possible workload.
- Operator burden at step 1 (workflow-id.txt handoff). The bridge is enforced by prose in CLAUDE.md, not by code.

Net: features push this **slightly below** the base rate for the joint survival × use definition, **at or slightly above** the base rate for the loosened "ships and runs" definition.

## 4. Typical failure mode

For class (1) — hooks against undocumented internal layouts — the modal failure is:

> Six to nine months after ship, a host-product update silently changes the path or schema. The parser does not crash; it returns "transcript-missing" or attributes zero tokens. The dashboard keeps rendering, but the numbers go flat or wrong. The operator either notices weeks later (if lucky) or never (if unlucky and the dashboard had become decorative). The fix is a rewrite of the parser against the new layout, which costs ~50% of original implementation effort and is deferred because the diagnostics are not load-bearing for any decision.

Secondary failure mode (dogfooding):

> The first weeks of data look great because they were drawn from the easiest possible workloads (review sessions, small inputs). The operator forms a confident model of "this is what the workflow costs." When a real session runs hot — large inputs, several veto loops, expensive critic outputs — the dashboard's prior averages mislead the diagnosis. The instrument was honest; the sample was not.

Tertiary failure (decay):

> The instrument works fine. Nobody opens the dashboard. After three months, the only consumer is the operator running explain-skill out of habit. The layer is technically alive and functionally dead.

Note what is *not* the typical failure: the AI-blindness invariant breaking via hook stderr leak. That is possible but is not the modal failure for the class. The review's emphasis on AI-blindness may be over-indexed against the actual risk distribution.

## 5. Outside-view verdict

**Below base rate, narrowly**, on the joint survival × use definition. Within tolerance on the looser ships-and-runs definition.

What would lift it above the base rate:

- A canary that detects the modal failure mode — periodic check that the parser's token attribution sums to a non-zero, non-degenerate value, with a loud warning if it returns "transcript-missing" twice in a row. Converts silent failure into noisy failure.
- Tightening the verdict and loop regexes to anchored patterns. Cheap.
- A second, structural enforcement of AI-blindness — wrapper script `hook-exec.sh` that always redirects, called by every hook, so a future edit can't regress it.
- A non-dogfood workload sample. Run the diagnostics against a pre-existing real workflow session by replaying its transcripts.

## Cheapest experiment that would distinguish "above" from "at-or-below"

Pick **three existing session-artifact directories from before 2026-05-09** (sessions that ran without diagnostics). Replay their Claude Code transcript JSONL files through the parser in isolation (no hooks, just the parser against historical data). For each, compute: (a) does it produce a `metrics.json` at all, (b) does the by-agent token sum equal the transcript total within 5%, (c) do the verdict and loop counts match a hand-count of `critiques/*.md` and `decision-log.md`.

Cost: ~1 hour of operator time. Distinguishing power:
- Above-base-rate signal: all three sessions parse cleanly, token sums match, verdict/loop counts agree with hand-count.
- At-or-below-base-rate signal: one or more sessions fail silently, or a verdict regex false-positives, or token sums diverge by >5%.

Cheaper than waiting six months to see the modal failure. Stresses the exact fragility the upgrade entry self-identified. Breaks the dogfooding confounder by introducing samples the implementation has never seen.

---

Sources:
- Hooks reference — Claude Code Docs (code.claude.com/docs/en/hooks)
- claude-code-hooks-multi-agent-observability (disler/GitHub)
- Claude Code Hooks: Complete Guide (claudefa.st)
- anthropics/claude-code issue #43630
- Platform Engineering — measuring developer productivity (platformengineering.org)
- DX engineering metrics blog (getdx.com)
