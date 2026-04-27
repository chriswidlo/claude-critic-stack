# Product critique — item 13 (orphans fate), v2

Target: [candidate-v2.md](../../candidate-v2.md)

## 1. User-visible consequence

**Maintainer:** the day this ships, `prompts/` contains exactly one file (`RETIRED.md`), `plans/` is unchanged in shape (O3 keeps its filename, gains a one-line Status header), CLAUDE.md is unchanged. Most-noticed surface change is that `ls prompts/` now returns a sentinel rather than an empty directory — *self-explanatory*, not a passive signal demanding inference.

**Next session-as-user:** the workflow contract (CLAUDE.md, agents, 12-step sequence) is unchanged. No new ceremony per session. Only new surface is the `RETIRED.md` convention, co-located with the absence it explains — discoverability is path-keyed where the artifact lived.

## 2. Commitments implied

- **`<dir>/RETIRED.md` becomes a (lightweight) repo convention.** Future sweeps in other directories will likely follow suit. Contract small (5-line file), reversibility local.
- **O3's filename is now load-bearing as a permalink to a design record.** Inbound links from immutable session-artifacts are now genuinely permanent.
- **`plans/` Status-header parsing is now load-bearing for O3 alone.** Smaller blast radius than v1's "all of `plans/` becomes mixed"; only one file requires the header.

These are real commitments but each is named, each is local, each is reversible without coordination. Compare v1's three unannounced contract changes — v2 ships one explicitly named convention.

## 3. Migration burden

- **Item 07's plan needs a one-line update** — named and in-scope. Bounded.
- **Future sessions** must learn the `RETIRED.md` convention only at the moment they encounter one — no per-session ceremony.
- **No 6-month aspirational test.** Replaced with commit-time sibling-session test. Migration-burden-disguised-as-falsifier from v1 is gone.
- **No external migration burden** — O3 is not renamed; O1 and O2 deletes have a documented inbound-link audit.

Burden is named, bounded, accounted for.

## 4. Product affordances

**Better than v1:**
- `ls prompts/` returns `RETIRED.md` — self-explanatory.
- Discoverability is path-keyed: future session looking for `five-pressures` runs `ls prompts/` and finds the answer in <30s.
- Falsifier is *runnable now*, not 6-month aspiration.
- No CLAUDE.md amendment — no per-session ceremony tax.

**Worse / newly expensive:**
- Pressure #2 left unaddressed in workflow. Named tradeoff (assumption #2). Maintainer accepts the gap explicitly.
- The `RETIRED.md` convention may not propagate — but v2 explicitly does not depend on propagation.

Honest, named tradeoffs rather than smuggled costs.

## 5. Frame-level objection

I retract my v1 frame-level objection. v2 measures by *contract count* (one named convention) rather than artifact count, and `RETIRED.md` is named explicitly with a written contract.

Remaining frame question worth flagging — not a veto, just a flag for synthesis: **the commit-time sibling-session falsifier is itself a contract.** It commits the maintainer to running the test before merge. If the test isn't actually run, v2 ships untested. Mitigation cheap, risk low.

## 6. Verdict

**`approve`.** v2 cleanly addresses every product-lens objection from loop 1: bait-and-switch is gone, empty-directory affordance is replaced with a self-explanatory sentinel, circular discoverability is broken, aspirational falsifier replaced with commit-time runnable test. Next-session and maintainer affordances are now aligned: both surfaces resolve in <30 seconds without reading this session's artifacts. **Approved unambiguously.**
