# Candidate recommendation v2 — karpathy-skills adoption (post-rework)

## Summary of what changed since v1

- v1 framed the question as "which 8–15 lines to add to the empty global CLAUDE.md." Three lenses returned `rework` because the actual decision is a **posture choice** (trust-defaults vs. explicit-hygiene-layer), not a content choice.
- A1 was resolved by reading the global `quality-assurance-validator` agent definition: it is a **post-hoc validation** agent (build-and-test-after-implementation, regression, edge-cases), **not** a test-first discipline. So Goal-Driven Execution is, in fact, the only one of the four karpathy principles that fills a real verified gap. But this finding does *not* unlock the v1 recommendation, because the rework objections were not principally about which lines to add.

## Position (v2)

**Do nothing. Recommend the user keep the global `CLAUDE.md` empty.** Surface the posture choice as the user's decision, not the orchestrator's.

The prior writeup's *direction* — "the karpathy file mostly duplicates defaults; the plugin packaging mechanism is the lesson; the only candidate addition is one line on test-first" — survives the workflow nearly unchanged. The workflow's value here was negative: it stress-tested the v1 expansion ("populate the empty file with 8–15 lines") and surfaced that expansion was over-corrective. The v2 recommendation reverts toward the original prior, with the following added precision:

1. Do not install the marketplace plugin. (Unanimous: scope-map `replace`, outside-view below-base-rate, three lens reworks all incidentally compatible.)
2. Do not populate the global CLAUDE.md without first making an explicit posture choice. The empty file is a deliberate configuration; treating it as vacant real estate is itself a product change that the workflow has no authority to make on the user's behalf.
3. Goal-Driven Execution (test-first) is the only karpathy principle that fills a verified gap (A1 resolved). If the user explicitly chooses the explicit-hygiene posture, this is the one line to add. If they keep the trust-defaults posture, it stays out.
4. Before any addition, run the canon-endorsed A/B (canon #4: ~10 representative tasks with and without the proposed line). The workflow did not run this and that is a real, named gap.

## Action items handed back to the user

- **Confirm posture intent.** Was the global `CLAUDE.md` left empty deliberately ("trust the defaults; rely on agent invocation for depth") or by oversight ("never got around to it")? The recommendation depends on this; the workflow cannot.
- **If "deliberately empty":** ship nothing. The prior writeup stands as final.
- **If "by oversight" and willing to add hygiene layer:** run the one-hour A/B over ~10 representative coding tasks (5 with a one-line "before coding, write a failing test that captures the success criterion; make it pass" instruction in CLAUDE.md, 5 without). If behavior change is observable, ship the one line. If not, ship nothing and the empty file is now also the *measured* choice.

## Named tradeoffs

- **Honesty about workflow output vs. perceived value.** Producing "the prior recommendation was directionally right, do nothing" is a low-signal output for an 11-step workflow. The temptation to manufacture an action item is real and was the actual failure mode of v1. Naming this is the cost of being honest.
- **Posture choice as user-facing surface vs. orchestrator-resolvable.** Surfacing posture to the user costs a round-trip; resolving it inside the workflow risks imposing an opinion the user did not ask for. v2 chooses the round-trip.
- **Acting without measurement vs. measuring before acting.** v1 acted; v2 names the A/B as the gating step. The cost of measuring is one hour; the cost of acting without measuring is the silent-overlap-drift outside-view #3 named.

## Named assumptions (each would flip the recommendation)

**A1 (now resolved).** `quality-assurance-validator` does post-hoc validation, not test-first. Goal-Driven Execution is therefore a real gap-fill if added. Resolution does not unlock v1 because v1 was rejected on posture/detection grounds, not on gap-fill grounds.

**A2 (unresolved, named explicitly).** The Claude Code default system prompt currently in production covers Surgical Changes, Simplicity First, and Think Before Coding with enough specificity that the karpathy lines for those would be duplication. Workflow did not inspect the current default prompt. Canon #5 (staleness flag) says reasoning from memory here is unsafe. **Flip:** if defaults are weaker than assumed, the addition expands; if stronger, even Goal-Driven Execution becomes a candidate for "covered, leave empty."

**A3 (unresolved, named).** The user is on a single machine with multiple repos. **Flip:** if multi-machine or if shared with collaborators, the marketplace plugin packaging mechanism becomes more attractive (but the content is still the user's choice).

**A5 (new, surfaced by product critic).** The empty global CLAUDE.md is a deliberate "trust the defaults" posture rather than oversight. **Flip:** if the user confirms it was oversight and they want explicit hygiene, the recommendation moves to "run the A/B, then add 1 line if it moves behavior."

## Frame-level objections (from critiques.md) — addressed

- **Architecture (coupling regret, not edit regret; volatile→stable wrong direction):** v2 does not commit any volatile content to the stable layer. The empty file stays empty until a posture choice is made; if a line is added, the recommendation requires it to have passed an A/B — i.e., to no longer be "volatile" (a tweet) but "demonstrated-on-user-tasks" (an artifact). Coupling direction is honored.
- **Operations (detection cost, not rollback cost):** v2 makes detection the precondition, not the afterthought. The A/B *is* the detection mechanism — it answers "does this line do anything" before shipping. No standing instruction is added in absence of a detection result.
- **Product (posture, not content):** v2 names the posture choice explicitly and hands it back to the user. The candidate stops trying to make a product configuration decision the user has not requested.

## Ways v2 could still be wrong

1. **The A/B is itself prompt-engineering theater.** A 10-task A/B by the same user, on tasks the user picks, is not a controlled experiment. It is one step better than reasoning from memory but it is not science. Outside-view's contradiction (canonical-from-authority class, 50–70% durable) does not apply to user-run A/Bs either. v2 calls this "measurement" but it is closer to "informed gut-check."
2. **"Do nothing" is the safest verdict the workflow can issue, which means the workflow is biased toward it after a triple veto.** The replan vs. rewrite choice was made on convergence grounds; it is possible a replan to step 7 under a different frame would surface a more substantive recommendation. Loop cap (2 of 2) prevents testing this.
3. **The user's actual question may have been "tell me whether my prior writeup was good," not "tell me what to do."** v2 still produces an action set; if the user wanted only an audit verdict, the right output is shorter: "the prior writeup was directionally right; the specific claim about your global CLAUDE.md being already populated was wrong; nothing else needs changing." The workflow does not have a mode for this and accreted action items by structural default.
4. **Karpathy-as-source bias persists.** v2 still treats the four principles as worth evaluating individually rather than asking whether the source (one tweet) merits the workflow at all. The honest answer may be "below substance threshold for the workflow; should have been a quick-take from the start."
