# Candidate recommendation — Revision 3 (final, post-R2 critique)

## Position (unchanged)

Reject in-workflow Context7 adoption in this repo. Closed-world trust model preserved.

## What ships (changed per R2 critiques)

Three minimal, coherent changes. No `decisions/` directory. No paperwork ritual. No global-install pointer in this artifact.

### 1. CLAUDE.md gets one bullet under "Things you must not do"

```
- Do not install vendor-live MCP retrieval tools (Context7, similar) in this
  repo's settings.json. The stack runs a closed-world trust model: curated canon
  + outside-view's bounded WebSearch. Vendor-live retrieval is not admitted.
  Revisit only if the workflow's question log shows ≥25% of recent design
  questions bottlenecked on current library-API specifics canon cannot serve.
```

That is the policy commitment. It lives where every orchestrator session reads it. No second policy surface.

### 2. `bin/check-mcp-allowlist.sh` — one small script

Run at workflow start (orchestrator step 0, added to CLAUDE.md routing). Enumerates active MCP servers via `claude mcp list` (or equivalent) and exits non-zero if any non-allowlisted server is present. Allowlist starts as `[]` (no MCP servers needed by the workflow). Fails closed.

This is the operational instrument the operations lens demanded. A concrete check, not prose. Detects the failure mode where a globally-scoped Context7 MCP leaks into this repo's session.

### 3. Nothing else.

- No `decisions/0001-...` (drops the architecture lens's "ADR registry under cover" objection).
- No `canon/trust-tiers.md` (drops the policy-framework precedent the product lens warned about).
- No global-install pointer in the synthesis (drops the product lens's "recommend without delivering" objection — the original briefing already told the user how to install Context7 globally; that's the right place for that information, not in this repo's deliverable).

## Frame-level objections — final accounting

- **Architecture (closed-world commitment lives in artifacts that *embody* it, not files that *declare* it):** addressed. CLAUDE.md is the artifact that embodies stack policy; the bullet sits there. The MCP allowlist script is the runtime embodiment. No declarative-only file is created.
- **Operations (boundaries enforced only by prose are non-existent):** addressed. The allowlist check is a runtime instrument that fails closed.
- **Product (don't recommend-without-delivering; don't create constitutional precedent):** addressed. No global-install recommendation in this artifact. No numbered decision file. One bullet, one script.

## Named tradeoffs

1. **The allowlist check is a small new operational primitive.** It must be maintained (kept compatible with whatever `claude mcp list` returns, kept honest about what's allowlisted). Cost: one script, one CLAUDE.md sentence telling the orchestrator to run it.
2. **The bullet in CLAUDE.md uses the word "vendor-live" without defining it.** Future contributors must infer the meaning from context. Mitigation: the surrounding rule names Context7 as the canonical example, which is enough for now. If a second similar tool comes up, that's the moment to define the term — not now.
3. **The script can be bypassed** by anyone who edits CLAUDE.md or skips workflow step 0. No mechanism prevents that. Acceptable: this stack is single-operator and the discipline is voluntary; the check is a guardrail, not a fortress.
4. **No paste-ready global-install doc ships.** The user gets the rejection clean and is left to their own global config. The product critic offered this as the alternative if the global-install pointer was dropped; we picked drop, not deliver.

## Named assumptions (≥3, flipping the recommendation)

1. **Single-operator discipline holds:** the allowlist script is voluntary; it works because the user runs it. *If wrong* (multi-operator, or the user routinely skips it), the rejection has no enforcement and the candidate degrades to R2-quality "boundary by prose."
2. **`claude mcp list` exists and returns parseable output** in the user's CLI version. *If wrong*, the script doesn't work and the operational instrument collapses; CLAUDE.md bullet alone remains.
3. **The base-rate evidence holds** — design questions in this stack rarely (<20%) bottleneck on current library-API specifics. *If wrong*, the rejection costs us those answers and the revisit-trigger in the bullet should fire sooner.

## Named ways this could be wrong

1. **The allowlist check may be theatre.** A user who wanted to use Context7 in-workflow would just edit the allowlist or remove the script call. The check exists to *make the violation visible*, not to *prevent* it. That is a real distinction but a thin one.
2. **The bullet in CLAUDE.md may go unread** because CLAUDE.md is long and people skim. The architecture critic claimed CLAUDE.md is the right home; that is true relative to a separate decisions directory, but it is not absolutely true.
3. **The "no global-install pointer" decision pushes work onto the user's recall** of the original briefing. If they forget the briefing existed (or another session reads only this artifact), they get the rejection without the alternative. Honest tradeoff for keeping this artifact clean.
4. **Adding bin/check-mcp-allowlist.sh as a new repo file** is a small primitive being introduced to enforce the absence of a different small primitive. There is asymmetry — adding code to enforce non-adoption — that is mildly absurd. A simpler alternative is "no script, just the CLAUDE.md bullet, accept the boundary is voluntary." The candidate ships the script because operations lens demanded an instrument; it could be defended either way.
