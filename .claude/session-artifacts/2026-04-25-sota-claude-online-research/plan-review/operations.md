# Operations lens — plan v3 review

## Most likely incident

T+6 weeks: regime-3 user runs `/verify-research` on a 40-claim hosted output during a load-bearing decision; verifier returns `fetch-failed` on 32/40 claims because Cloudflare/anti-bot pages started returning 403 to the WebFetch user-agent overnight. Failure is *silent degradation* — `fetch-failed` is a category in the report, not a circuit-breaker — so the user sees a "completed" report with mostly-empty evidence and must re-do verification by hand at the worst possible moment.

## Blast radius

N=1, single-host, no downstream services. But within scope it is total: regime-3 user has, by definition, made the verifier load-bearing for 5+ irreversible decisions/week.

## Rollout / rollback

- Rollout: free, one Markdown file. Fine.
- Rollback: delete the global `verify-research.md` slash command file. Genuinely free. **Strongest operational property of the plan.**
- Two-systems period: none, regimes are exclusive. Good.

## Observability gap (major)

Zero longitudinal observability:
- No log of per-run cost. Plan asserts "cost guards" but does not name the ledger.
- No `fetch-failed` rate trendline.
- **No regime-drift signal.** User supposed to re-answer volume question quarterly but nothing counts actual `/verify-research` invocations. Regime-1 → regime-3 silent slide over six months has no metric.
- Snapshot directory size: not monitored.

Plan ships no telemetry primitive at all. Acceptable for N=1 only if user accepts that drift detection is by vibes.

## Cost at failure

- Per-run: ~30 Haiku calls × WebFetch + small reasoning. Order-of-magnitude $0.05–$0.30 per run; spikes 5–10× on long reports. No per-run abort threshold named.
- Storage: regime-3 ~5 reports/week × 30 citations × 50KB text = 7.5MB/week ≈ 400MB/year, 1.2GB/3yr. Tractable on disk; **not tractable for cloud-sync if the research-snapshots directory lands in iCloud/Dropbox.** Location semantics not specified.
- Human cost at the 3am incident: hours, no triage runbook (I previously demanded one; v3 dropped it).

## Build-cost honesty check

Plan claims "1–2 hours." Honest estimate for parallel `claude -p` fan-out + Markdown citation parser + dedup'd snapshots + graceful fetch-failed + composed report + *any* cost guard: **4–8 hours for first working version, plus a real debugging tail the first time the Markdown format shifts.**

## Frame-level objection

Plan frames regime selection as a **user-introspection problem.** Operational view: it is a **measurement problem the system should answer for the user.** Human recall over 8 weeks for "decisions I could not reverse within 24h" is not reliable enough to bind an architectural choice — it conflates salient with frequent, underweights the boring middle. Self-report-driven regime gate with no measurement loop is operationally equivalent to no gate.

## On the dropped quarterly Routine

I previously demanded it; v3 dropped it. **Re-imposing in weakened form.** Not as a model-deprecation control (snapshots address that), but as the only remaining drift-detection mechanism. Minimal acceptable: a Routine that quarterly counts `/verify-research` invocations from shell history and prints implied regime alongside stated regime. Diverge >1 regime → prompt re-evaluation.

## 3am scenario

Verifier reports `fetch-failed` on 80%. User has: no runbook, no fallback (regime-2 mental mode unused for months), no transient-vs-structural distinguisher, no partial-credit mode. Implicit answer: "fall back to manual" — but regime-3 user is regime-3 *because* manual doesn't scale. **Plan has no answer here. Single largest unmitigated operational risk.**

## Verdict: rework.

Approve if: (a) reinstate minimal quarterly Routine as measurement-not-policy; (b) name per-run cost ceiling and per-run `fetch-failed` ratio that triggers abort with clear error rather than "completed" report; (c) write the 3am runbook; (d) honest build-cost revised to 4–8 hours; (e) name research-snapshots directory location semantics (local-only, not cloud-synced) and a snapshot-retention default.
