# Operations critique v2 — `2026-04-27-critics-get-write-tool-impl`

## 1. Most likely incident

At T+~12 sessions after rollout, an operator running a multi-loop session (Step 11 rewrite or Step 10 mid-stream) sees `critiques/operations.md` overwritten by the orchestrator with content that *looks* faithful but has had bullet ordering changed, a hedged sentence smoothed, and one section header renamed — none of which the operator notices because the per-lens file is read in isolation and there is no diff against the inline return. Root cause was Assumption A1 — the orchestrator (an autoregressive sampler) cannot reliably honor a prose-only "do not paraphrase between delimiters" contract when the bytes pass through its own context as text rather than as an opaque blob, and the contract has no enforcement primitive; v2-C's claim that the failure is "detectable in the orchestrator's transcript" presumes an operator who actually performs the diff, which is not a control, only a possibility.

## 2. Blast radius

- **Per-incident scope:** one critique file per session, three at panel-replay time. Lower fan-out than loop 1's parallel-write design (good — that was the loop 1 objection), but the failure mode now lives at every Step 10 invocation, not at session-id-mismatch boundaries. Frequency goes up; per-incident magnitude goes down.
- **Cross-session contamination:** **eliminated** vs. loop 1. The orchestrator writes only to the active session's directory; there is no parallel-write path that can stale-session-leak. This is the genuine win of v2-C and I name it directly.
- **Loop 1's modal failure (stale-session/wrong-path writes):** **structurally resolved.** No parallel writers, no session-id propagation across agents-with-Write, no TOCTOU window between critic-Write events. The concurrency-posture concern from loop 1 is correctly dissolved, not patched.
- **New radius (paraphrase-by-orchestrator):** every panel run. The badness is bounded per-incident (one file's prose drifts) but unbounded over time (the audit ledger accumulates orchestrator-shaped paraphrases that look like critic prose). I cannot estimate drift rate — there is no measurement primitive in the candidate.
- **Self-modifying-class amplification:** still present. The orchestrator paraphrasing a critic's verdict on a self-modifying change is exactly the class the user's stated motive ("no more me-claiming-they-said-X") was built to prevent. v2-C does not eliminate this — it relocates it from "orchestrator paraphrases at compose-time" to "orchestrator paraphrases at transcribe-time," and trusts a prose contract to forbid the latter.

## 3. Rollout / rollback

- **Rollout strategy:** flag-day swap of CLAUDE.md Step 10 + Step 12 wording + critic body sentences + session-artifacts README, all simultaneously. **No canary** (the contract either binds the orchestrator or it doesn't). **No shadow traffic.** **No flag.** The cost of canary here is genuinely lower than loop 1 (no concurrency surface to canary across), but the absence of a shadow period is unforced.
- **Rollback path:** revert four prose changes. Lower cost than loop 1 because there are no critic-authored files in disk that downstream consumers have anchored to — only orchestrator-authored files in a renamed shape. **Rollback is genuinely a rollback, not a forward-fix.** This is a real improvement over loop 1.
- **Two-systems-running cost:** **not named, but lower-risk than loop 1.** During transition, sessions running pre-change produce `critiques.md` aggregate; sessions running post-change produce per-lens files with no aggregate. Step 12 must handle both shapes for the duration. The candidate does not state how long this period lasts or whether mid-flight sessions get mixed shapes.

## 4. Observability gap

- **What goes invisible:** the *delta* between the critic's inline return and the persisted per-lens file. Today, the orchestrator paraphrases at compose-time and the critic's raw prose lives in the transcript only; under v2-C, the orchestrator paraphrases at transcribe-time and the critic's raw prose *also* lives in the transcript — but only the persisted file is read at Step 12. The diff between those two surfaces is the new observability gap. It is *available* (the transcript exists) but not *surfaced* (no diff is computed, no operator workflow consumes it).
- **Metric that would confirm "the thing went well":** byte-equivalence between the bytes between `<critique>...</critique>` in the orchestrator's transcript and the bytes in `critiques/<lens>.md`, for every Step 10 invocation. **I do not know whether this metric is collected. I believe it is not.** A1's detection claim is correct that the data exists; it is wrong that this constitutes a control. Diff-on-demand by an operator under load is not a control.
- **Specifically missing:** (a) automated byte-equivalence check between transcript-delimited region and persisted file; (b) any signal at Step 12 that the synthesis is reading paraphrased-rather-than-verbatim prose; (c) any record of *whether* the orchestrator honored the contract on a given run.

The candidate's claim — "v2-C's failure mode is detectable in the orchestrator's transcript, unlike loop 1's parallel-write failure mode" — is **technically true and operationally meaningless under realistic operator load.** The same operator-as-on-call I flagged in loop 1 must now diff multi-kilobyte prose blocks across transcript and disk, per lens, per session, with no tooling. Detection-available is not detection-performed. Contracts without enforcement are aspirations.

## 5. Cost at failure

- **Retry storms / amplification:** **none.** This is a genuine improvement. Sequential single-writer means one bad write per failure, no fan-out.
- **Human on-call load:** the failure mode shifts from "operator must reconstruct what the critic said by going to disk across multiple session directories" (loop 1) to "operator must diff transcript-region against persisted-file to notice paraphrase, every time, with no tooling alert" (v2-C). The cost is **lower per-incident** but **higher in cumulative attention-tax**.
- **Cost of A1 failing once vs. cost of A1 failing chronically-and-mildly:** loop 1's A1 was binary-catastrophic. v2-C's A1 is continuous-and-mild (paraphrase drift accumulates). The latter is harder to detect, easier to live with, and worse for the user's stated motive.
- **Cost of dropping the aggregate `critiques.md`:** Step 11's replan-vs-rewrite decision loses its single-file anchor for the decision-log entry. The decision-log now references three files where it used to reference one. Operationally minor; named for completeness.

## 6. Frame-level objection

The candidate frames byte-fidelity as enforceable via a prose contract on the orchestrator because "the chokepoint already exists." The operations frame is that **a prose contract is not a control, regardless of where the chokepoint lives.** Controls have three properties: a forcing function, a detection primitive, and a recovery primitive. v2-C provides none of the three:

- **Forcing function:** the contract is text in CLAUDE.md instructing the orchestrator (an LLM) not to paraphrase. This is the same class of instruction as "do not hallucinate." Compliance is probabilistic.
- **Detection primitive:** the candidate claims the transcript provides this. Transcripts are evidence, not detection. A detection primitive is a thing that *fires* when the contract is violated. Nothing fires.
- **Recovery primitive:** none named. If paraphrase is detected post-hoc, what is the recovery — re-run the panel? Edit the file? Annotate the drift? The candidate does not say.

The deeper frame objection: **the candidate has substituted a structural problem (orchestrator-as-paraphraser) with a behavioral promise (orchestrator-promises-not-to-paraphrase) and called this a resolution.** The same orchestrator that paraphrases critic verdicts at compose-time today is being asked to transcribe them verbatim at write-time tomorrow. The mechanism doing the work is unchanged; only the instruction has changed.

A second frame-level objection: **dropping the aggregate `critiques.md` is operationally fine but creates a synthesis-step asymmetry the candidate has not stress-tested.** Step 12 today reads one file to extract three verdicts; under v2-C it reads three files to extract three verdicts. This is a 3x file-handle increase at the synthesis chokepoint — and means Step 12 has a partial-read failure mode (one file missing or empty) that did not exist under the aggregate. The candidate's "Ways v2-C could be wrong" §3 names this exactly and then shrugs.

## 7. Verdict

**rework**

The verdict would change to `approve` if the candidate added one of: (a) a byte-equivalence check primitive — even a single shell-level `diff` invocation comparing the transcript-delimited region against the persisted file, run as part of Step 10 closure and logged to `decision-log.md` — converting the prose contract into something with a detection primitive, or (b) an explicit Step 12 partial-read policy ("if any of the three `critiques/<lens>.md` files is missing or empty, halt synthesis and re-invoke the missing lens; do not proceed on N-of-3") that resolves the dropped-aggregate's partial-read failure mode by construction.
