# Operations critique — verdict: rework

Persisted by orchestrator from inline return (critic agents lack Write tool).

## Verdict
rework

## Lens-specific critique

**Day-60 falsifier is unmonitored.** The frame-survival mechanism is uninstrumented. Specified as a ratio: "meta-structure commits to substantive-content commits ≤ 3:1" but no script, hook, scheduled query, or operator routine is named that produces this ratio on day 60. Operators do not run unscheduled diagnostic archaeology — universal post-mortem finding for any "we'll check it later" control. Cost of making it real is small (~20-line script) but candidate does not name the cost or place ownership. Cite: §"Three time-box commitments", item 3.

**Rollback by vibes.** Remediation is "hard stop to writing new schema until ratio recovers." Three gaps: who declares freeze (operator, implied, not named); whether content writes during freeze are allowed/encouraged/blocked (unspecified); what signal declares "recovered" (same ratio, recomputed when?). Real operational rollback specifies trigger, action, duration policy, recovery signal. None present.

**Curator-agent gating is a protocol contradiction.** Locking dimension 4: "Only the `lab-curator` agent writes." Tradeoffs: "manual operator writes for the first ~10 entries; curator agent designed against observed entry shapes." Locking dimension is suspended for the first ~25% of the lab's first quarter. Hand-written entries diverge from whatever curator codifies — repair work follows, not named as a cost. Day-7 freeze locks the protocol *before* the first 10 entries, but day-14 milestone (≥4 entries) means hand-writing during the supposedly-frozen period.

**No emergency-revision protocol for locking dimensions.** "After day 7, four locking dimensions are frozen until quarterly review." If a locking dimension is wrong on day 12, options are: wait ~75 days accumulating malformed entries, or violate the freeze. Any freeze without break-glass gets violated quietly and stops meaning anything.

**Chicken-and-egg between schema and curator.** Lab depends on curator; curator depends on lab schema being stable. Resolution (manual writes for ~10 entries, then build curator) implicitly says schema is stable enough on day 7 to be hand-followed for ~10 entries — unverified. If a hand-written entry surfaces a schema bug on entry 3: fixed in schema (violates day-7 freeze), tolerated with comment (malformed corpus), or deferred to quarterly (3 ages with bug)? Specify or push back.

**Per-entry friction at growing N.** Each entry: choose 1 of 7 types, discipline tag(s), 1 of 5 maturity rungs, type-specific structure (falsifier + prior-art for hypothesis), optional cross-references with 4-vocabulary frontmatter. Acceptable at N=4 (day-14 milestone). At N=40 requires operator to know taxonomy by heart and read INDEX.md without typos. At N=400 it's a job. Candidate names no friction-reduction primitive (templates, slash-commands); curator's existence is itself unbuilt.

## Weakest link

**The day-60 falsifier as an unmonitored control.** The candidate's entire frame-survival argument routes through this falsifier. If the falsifier is not actually computed, the frame is not actually survivable; it just *says* it is.

## Operational cost at steady-state

Per `articulated` entry: 10–20 minutes (type selection + falsifier + prior-art check + frontmatter + cross-references). At one entry per week, sustainable. At three entries per week (rate implied by 4-entry day-14 milestone plus continued accretion), friction is real.

Quarterly review unestimated. Half-day to full-day for ratio audit + discipline distribution + promotion-criteria fit + reversible-dimension cost reassessment. Not budgeted.

If operator runs out of attention, day-60 ratio audit fails first (nothing prompts it), then quarterly review fails (nothing schedules it), then time-box becomes nominal.

## Operational cost at failure

- **Mode A (silent decay):** operator stops writing because friction > value. Lab graveyards with no audit ever run because no one was on the hook. Failure invisible from inside.
- **Mode B (forced restructuring at quarterly):** maturity ladder doesn't fit. If ladder *names* need changing (locking), every entry's `maturity:` field must be rewritten. Cost (entry count × rewrite time) and absorption mechanism unnamed.
- **Mode C (curator never built):** item E remains backlog forever. Manual writes past 10 entries. "Locking" write-port permanently nominal. Candidate has no fallback if curator is never built.

Candidate names the falsifier (mode A) but not the operational cost of *acting on* it.

## Frame-level objection

**Frame is operationally tractable only if** time-box is instrumented (it is not), locking/reversible split has break-glass for in-quarter discovery (it does not), curator-or-not protocol is decided before day 7 rather than implicitly suspended for 10 entries (it is not). Candidate has produced a paper commitment to operational rigor without supporting controls. Frame should be either (a) extended with three named operational primitives (falsifier-script, freeze-break-glass, curator-bootstrap-protocol) before ratifying, or (b) honestly downgraded to "we will *try* to enforce this and the day-60 audit is best-effort." Current candidate sits in unviable middle: load-bearing controls that are not instrumented are worse than no controls — they license false confidence.

**Second frame-level objection:** candidate frames curator's nonexistence as a §Tradeoffs concession ("can begin with manual writes"). Operationally it is the *primary* dependency — locking dimension defining who-may-write is unenforceable until item E ships. Frame should treat curator-bootstrap as a locking dimension at parity with the other four, not as a tradeoff bullet.

## What would make this approve

1. **Instrument the falsifier.** Specify the script/hook computing meta-vs-content commit ratio, where it lives, what cadence runs it (pre-commit hook prints current ratio; weekly reminder), what operator does on trigger. Name the time cost (~1 hour) and place it on the day-7 critical path.
2. **Specify rollback semantics + day-7 break-glass.** For day-60: who declares freeze, what writes blocked vs. allowed, what computed signal declares recovery. For day-7: break-glass allowing in-quarter revision of locking dimension, costs (resets day-60 audit clock; requires `killed-idea` entry naming what was wrong), bound on frequency.
3. **Decide curator-bootstrap path before day 7.** Either (a) build minimal curator before any entries land (slips day-14, enforces protocol from entry 1), (b) accept manual writes as steady-state for some named period and stop calling write port "locking" until curator ships, or (c) write a one-page lint-check validating entry frontmatter and maturity transitions, runnable on demand, as bootstrap stand-in.
