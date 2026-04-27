# Requirement classification — item 06 temporary-dependent upgrades

## Primary label
`refactor`

## Default frame (from label)
"What observable change would falsify 'behavior unchanged'? The three options all claim the underlying capability (the upgrade ideas + the source material on the worktree branch) is preserved — pick the option whose reader-facing state most accurately represents that preservation, and name the test that would catch a behavior change sneaking in."

## Known frame bias
Calling a behavior change a refactor — specifically, option (a) is *not* a pure refactor (it materially adds files to `main` and re-establishes a directory whose own narrative says it should be transient); the workflow must not let (a) ride in under the refactor frame without surfacing that it crosses into `migrate`.

## Secondary label (if any)
`investigation` — the user has already collected the option set and stated a soft lean; the workflow's job is to stress-test the lean, which is partly meta-investigation of the lab's own conventions (`honest negation`, `🌱 ⏸️` precedent).

## Alternative classification
`migrate` — becomes primary if the recommendation is option (a). Restoring `temporary/` from `agentic-engineering-research` onto `main` is a cross-branch migration with a real two-systems-running period (the worktree branch keeps existing) and a real rollback question (delete-the-restored-tree). Under (a), the operative bias is *underestimating the parallel-run cost* — specifically, the cost of two copies of the source material drifting.

## User's framing words
- "Should item 6 of the cleanup punch list be **resolved**" — frames the question as cleanup, not as a substantive lab-doctrine choice; risks understating the frame-level stakes the plan itself names.
- "(a) **restoring** `temporary/`" — presumes the restore is recoverable/clean; doesn't surface that the directory's own internal narrative said it should be temporary.
- "(b) marking both entries **superseded** with an **honest-negation** note" — invokes the lab's own doctrine; the classifier cannot resolve whether *honest negation* is correctly applied here, but flags that the user has already named the doctrine, which is itself a bias toward (b).
- "(c) **parking** both entries with an explicit `⏸️` resume condition" — presumes a state-machine vocabulary the lab has used exactly once before (item 1, Critics-get-Write); precedent of N=1 is weak grounding.
- The plan document records a soft lean for (c) with (b) close second. The classifier flags this lean as the user's prior, not a finding — the workflow should be willing to land on (a) or (b) if the panel pushes that way.

## Gaps
- Whether the operator intends to advance the agentic-engineering migration soon (the plan flags this as the condition that flips the lean toward (a)). Without a near-term answer, (c) is defensible; with one, (a) is.
- Whether the LEDGER reader's experience is a first-class concern. (b) reads as "resolved"; (c) reads as "ambiguous-but-tracked." If LEDGER is primarily an operator dashboard, (b) wins on legibility; if it's a faithful state record, (c) wins on accuracy.
- Whether the lab has a written rule about `🌱` entries depending on resources outside `main`. If yes, this question is mechanical, not frame-level. If no, item 6 is also implicitly proposing such a rule — which would make it `new` (a new lab convention) rather than `refactor`.
- The cost of the two-copies-running period under (a): is `agentic-engineering-research` deleted after restore, kept as audit trail, or rebased? The plan does not say.
