# Operations critique v2 — `2026-05-09-review-diagnostics-impl`

## 1. Most likely incident

At time T (a Stop hook firing on a workflow session whose parser crashes between writing `parser.lock` and writing `metrics.json`), every subsequent ledger-render in that target's tree polls the stale `parser.lock`, times out at 2s, and writes `_parser-still-running at ledger-render time_` into the ledger; the lock is never aged out, so the loud-skip is permanent across N future sessions. Root cause: the rewrite's lock sigil has no liveness — it encodes presence-of-lock, not presence-of-running-parser, and the operator has no documented recovery procedure beyond reading the SKILL and inferring that `rm <target>/.claude/session-artifacts/<id>/diagnostics/parser.lock` is safe.

Reading the lock as per-session (it lives in the session's `diagnostics/`), the cumulative-loud-skip framing above is wrong on cross-session contamination — but the *single-session* equivalent is: a one-off parser crash leaves the *current* session permanently loud-skipped with no re-render path, and the operator's session ledger ships with `_parser-still-running_` as the literal final state of metrics. The forensic staging dir survives (good, that fix landed) but the artifact the human reads says "still running" forever.

## 2. Blast radius

- **Per-session radius:** one ledger entry, but with an actively misleading state string ("still running") rather than absence. That is louder than v1's silent-skip, which is the intended improvement; the cost is that the string is wrong (the parser is not running, it crashed).
- **Cumulative radius:** if the crash is layout-drift-induced (the assumption-3 worry the rewrite explicitly names), every future session in this target hits the same crash class, and every ledger ships `_parser-still-running_`. Detection lag = first time the operator reads a ledger and notices.
- **Cross-target radius:** unchanged from v1. Layout-drift is still global; one Anthropic-side change zeros every machine. The split-on-tripwire posture (deferred item) means defense is reactive.
- **Staging dir:** the fix lands. Forensic surface preserved on parser crash. Real improvement.
- **Phase A wrapper window:** during the ≥5-session two-systems-running, both inline `2>/dev/null` and `hook-exec.sh` redirect the same streams. If the wrapper materially differs (assumption #4's flip condition), the inconsistency is per-hook-script, not per-target — bounded to the three hook scripts. Acceptable.

## 3. Rollout / rollback

- **Rollout for action 2a (wrapper):** the rewrite picks up the additive rollout. Phase A → Phase B with a tagged commit as rollback artifact. This is the right shape.
- **Phase A threshold of "≥5 sessions":** picked by intuition. The operational property that matters is *what is observed during Phase A*, not how many sessions. Five is plausibly fine for a single-operator stack where each session is hand-reviewed; it would be inadequate for a fleet. Defensible for this stack's operator-cadence.
- **Phase A → Phase B promotion gate ("confirms Phase A works"):** the rewrite's weakest sentence. Phase A is invisible by construction — the wrapper redirects what the inline already redirects. The rewrite names no observable metric for wrapper correctness. The honest answer is that Phase A is a vibes-check unless the operator runs the unit test on every Phase A session, which is not stated. **Specific gap:** name what the operator looks at to declare Phase A done. Suggested: "the staging hook log under `<target>/.claude/.metrics/staging/<uuid>/` contains exactly one entry per wrapped command across ≥5 sessions, and `git diff` of three hook scripts shows no inline-redirect change between Phase A entry and Phase B cutover." Without a named observation, "≥5 sessions confirm" is vibes.
- **Rollback for action 1 (schema):** the rewrite does not name a rollback. Schema validation that fails writes `metrics.json.invalid` and the consumer silent-skips — that *is* a graceful-degradation property, but if the schema itself is wrong (over-constrained), every session ships `metrics.json.invalid` until the schema is patched. Rollback path: revert the schema commit. Acceptable for a single-file rollback, but unnamed.
- **Rollback for action 2b (lock sigil):** unnamed. If the lock-sigil approach itself is wrong, rolling back means reverting the parser, ledger-render skill, and Stop hook in one commit. Reversible but not named.

## 4. Observability gap

The rewrite closes one gap (silent-skip is now loud-skip) and opens two new ones:

- **Stale-lock detection.** The rewrite's lock-sigil is presence-only, no timestamp, no PID liveness check. The poll knows "lock exists for >2s" but cannot distinguish "parser is running slowly" from "parser crashed leaving lock behind." A future ledger-render run on the *same session* (if re-rendered) will again loud-skip on the same stale lock. **Proposed minimum fix:** the parser writes `parser.lock` containing its PID and start timestamp; ledger-render's poll, on timeout, checks (a) is the PID alive, (b) is the lock older than e.g. 60s — and treats either as a crashed-parser signal that promotes loud-skip to "_parser-crashed at <ts>, lock stale_" so the operator's recovery action (delete the lock, optionally re-run parser) is unambiguous.
- **Re-rendering.** The rewrite makes loud-skip *permanent* in the ledger because ledger-render is treated as one-shot. A crashed parser, even if re-run successfully later by hand, leaves the ledger artifact lying. **Question for the candidate:** is ledger-render re-runnable to fill in metrics post-hoc? If it does not exist, the lock-sigil's loud-skip is a one-way door per session.
- **Phase A correctness.** Named above. Phase A produces no observable signal that the wrapper redirected what it was supposed to redirect.
- **Loud-skip rate as a feedback signal.** The rewrite's assumption #3 says reconsider synchronous-parser if loud-skip rate exceeds 1 in 10. The *rate* is not collected; the operator would have to grep ledgers. **Suggested:** if loud-skip is going to be a control variable, count it. A one-line append to a file under `<target>/.claude/.metrics/loud-skip-log` from inside the SKILL would suffice.

## 5. Cost at failure

- **Parser crashes during lock-held window:** one session's ledger ships with `_parser-still-running_` (incorrect — parser crashed), forensic staging dir survives (good), operator has no in-band signal that the lock is stale, and on next session the parser writes a *new* lock in a new session dir. Recovery cost: read SKILL, infer `rm <session>/diagnostics/parser.lock` is the action, optionally hand-run the parser. ETA-to-recovery: 5–15 minutes per *known* incident, indefinite for the *unknown* incident (operator never notices the loud-skip string is wrong).
- **Parser routinely takes >2s on real workloads (assumption #3 flip):** every ledger fills with loud-skip notices. Cost: ledger pollution that conditions the operator to dismiss the string, which destroys the loud-skip as a signal.
- **Schema over-constrains the parser:** every session writes `metrics.json.invalid`, no consumer reads it, ledger-render silent-skips because no `metrics.json` exists. This is *exactly* the v1 silent-skip failure mode the rewrite claims to close. The rewrite's named mitigation is logically self-contradictory — re-read named-ways-this-could-be-wrong bullet 1; it is muddled. **Specific request:** name which side wins on schema-vs-parser-version-skew. My read: the parser version should write per its native shape and let the *consumer's* schema validation decide whether to silent-skip; a producer-side schema check that rejects the parser's own output is a bootstrap failure.
- **Phase A wrapper bug masked by inline redirect:** during Phase A, if the wrapper is broken, the inline redirect catches the leak, *and the operator sees nothing*. Phase B cutover then ships the broken wrapper and only at that moment does the failure surface — across all three hooks. The Phase A → B promotion gate is the only thing standing between this and a real incident. **This is the single most important unaddressed cost.**

## 6. Frame-level objection

The rewrite addresses the synchronization-as-frame objection from loop 1 — that part landed. New frame-level objection at loop 2: **the lock-sigil is a presence primitive masquerading as a liveness primitive.** A two-process synchronization contract requires liveness, not just sequencing — the consumer must be able to distinguish "producer running" from "producer dead." A lock file with no PID, no timestamp, no heartbeat, is a sequencing primitive. The rewrite accepts this implicitly by treating loud-skip as the terminal state and not naming a recovery procedure. The operationally-correct shape is `parser.lock` containing `{pid, start_ts}`, with a polling consumer that checks PID liveness and lock age and emits distinct signals for "running-slow" vs "crashed-stale-lock." That is ~5 extra lines of parser and SKILL and is the difference between a control and a tripwire.

A second frame objection on retention: the rewrite **moves cleanup, does not add retention**. Cleanup-on-success in the parser tail solves the forensic-evidence-destroyed problem, which is the v1 fix I demanded. It does not solve the steady-state accumulation problem in `<target>/.claude/.metrics/staging/` and `<target>/.claude/.metrics/orphan/` from sessions where the workflow-id handoff didn't happen. A separate trim job is still needed; the rewrite implicitly assumes "every parser run ends in success-tail-cleanup" closes the question, and it does not — orphan dirs come from sessions that never had a parser run pointed at them. **Specific request:** a retention rule on staging/orphan dirs (e.g., "subdirs older than 14 days, trimmed by a session-start guard or a manual `bin/trim-staging.sh`"), even if deferred-with-tripwire, is needed.

## 7. Verdict

**rework**

Specific changes that would change the verdict to `approve`:

1. **Make the lock a liveness primitive, not a presence primitive.** The parser writes `parser.lock` containing PID and start timestamp; ledger-render's poll, on timeout, checks PID-alive and lock-age and emits distinguishable strings — `_parser-running-slow_` vs `_parser-crashed-stale-lock_`. Five lines of parser, five lines of SKILL.
2. **Name the Phase A → Phase B promotion gate as an observable.** "≥5 sessions" without an observed property is a vibes check. The minimum: the operator confirms via `git diff` that no inline redirect was inadvertently removed during Phase A, and the staging hook log shows wrapper invocations at the expected count.
3. **Name a re-render path or accept that loud-skip is permanent for the session.**
4. **Add a retention rule for `<target>/.claude/.metrics/staging/` and `<target>/.metrics/orphan/`.** Even a deferred-with-tripwire entry is acceptable, but the question must be named, not silently dropped.
5. **Resolve the schema-vs-parser-version-skew muddle in named-ways-this-could-be-wrong bullet 1.** Name which side wins.

Per CLAUDE.md step 11, this is loop 2; rework escalates to synthesis-with-disagreements. The rewrite is a real improvement on v1 and addresses the binding loop-1 objections in shape. The five gaps above are concrete, small, and operationally load-bearing — synthesis should name them as the disagreements, not paper over them.
