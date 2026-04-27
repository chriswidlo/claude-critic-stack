# Scope-map — `2026-04-27-critics-get-write-tool-impl`

## Existing primitives touched

| primitive | source (where it was named) | relationship | one-line rationale |
|-----------|-----------------------------|--------------|--------------------|
| `critic-architecture` agent frontmatter `tools: Read, WebFetch, WebSearch` | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 1 | extend | Add `Write` to existing tool grant; review contract unchanged. |
| `critic-operations` agent frontmatter `tools: Read, WebFetch, WebSearch` | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 2 | extend | Add `Write` to existing tool grant; review contract unchanged. |
| `critic-product` agent frontmatter `tools: Read, WebFetch, WebSearch` | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 3 | extend | Add `Write` to existing tool grant; review contract unchanged. |
| Critic agent body output sections (no persistence instructions) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct facts 1–3 | extend | Append Mandatory-behavior block naming target path + session-id contract; existing 6/7 sections preserved. |
| Established Write-pattern in `subagent-distiller`, `scope-mapper`, `frame-challenger` (frontmatter `Write` + body names `<session-id>`-templated path) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct facts 4–6, §Inferred 2 | extend | Apply same instruction-level scoping pattern to three more agents; pattern is the load-bearing convention. |
| Aggregate `critiques.md` artifact (orchestrator-authored full transcription) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct facts 7–8, §Inferred 5,7 | replace | Replaced by per-lens critic-authored files; surviving residue is a thin index (3-row: lens · verdict · path) authored by orchestrator post-panel. |
| CLAUDE.md Step 10 wording ("Aggregate verdicts into `critiques.md`") | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 7 | replace | "Aggregate verdicts into `critiques.md`" replaced with "Each lens writes `critiques/<lens>.md`; orchestrator reads files, builds thin index, applies minority-veto." Old wording cannot coexist — it instructs the orchestrator to do the paraphrase work the new contract removes. |
| session-artifacts [README](.claude/session-artifacts/README.md) listing of `critiques.md` as critic-panel aggregate (step 10) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 8 | replace | README description must shift from "aggregate" to "per-lens authored + thin index"; the old description is wrong under new contract. |
| Per-lens `critiques/<lens>.md` precedent (orchestrator-authored, 2 prior sessions) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct facts 9–10, §Inferred 3 | replace | Same path, new author. The artifact's *meaning* changes: critic-original, not orchestrator-paraphrase. Old precedent files remain on disk as historical record, but the contract going forward replaces them. |
| Absence of harness-level hooks (`.claude/settings.json` has no `hooks` block; no `hooks/` dir) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 11, §Inferred 4 | preserve | Preserved by default — instruction-level scoping is the established pattern (see Write-pattern row). No harness hook is added by this requirement. Stated reason below. |
| Upgrade #3 (PostToolUse hook to verify claimed writes — un-built) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 13, §Inferred 6 | preserve | Preserved as un-built upgrade. This requirement does **not** create a hard dependency on it — instruction-level scoping is sufficient under the established pattern. Stated reason below. |
| Upgrade #14 (hard gates as harness hooks — un-built) | [Explore.md](.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) §Direct fact 14 | preserve | Preserved as un-built upgrade. Orthogonal to this requirement; gate enforcement remains prose-level. Stated reason below. |

## Deletion cost (for subsume/replace rows)

- **Aggregate `critiques.md` (full transcription form):**
  - **Callers:** Step 12 synthesis (CLAUDE.md line ~78) reads "Critiques summary" — must be re-pointed to read per-lens files + thin index. Step 11 replan-vs-rewrite logic (CLAUDE.md ~lines 56–64) parses verdict labels — must read per-lens files. No external scripts or exports identified.
  - **Data migrations:** None for prior sessions (existing `critiques.md` files stay as historical artifacts). Going forward, sessions produce per-lens files + thin index instead. No format conversion needed.
  - **Config surface:** None. `critiques.md` is not referenced in `.claude/settings.json` allow/deny lists.

- **CLAUDE.md Step 10 wording:**
  - **Callers:** The orchestrator itself, every session. This is the single instruction that drives panel aggregation behavior.
  - **Data migrations:** None — instruction-text edit only.
  - **Config surface:** Step 10 is referenced from Step 11 (replan-vs-rewrite) and Step 12 (synthesis). Both must be re-checked for consistency after the rewrite. The minority-veto rule must be preserved verbatim under the new shape; only the *aggregation mechanism* changes.

- **session-artifacts README:**
  - **Callers:** Operator-facing documentation. Not parsed.
  - **Data migrations:** None.
  - **Config surface:** None.

- **Per-lens `critiques/<lens>.md` precedent (authorship contract):**
  - **Callers:** None directly — but Step 11's "rewrite" loop in two prior sessions produced `<lens>-v2.md` files (Explore §Direct fact 9). The new contract must answer: does the critic re-invoked in step 11 write `<lens>-v2.md` itself, or does it overwrite `<lens>.md`? This is a **named gap** the generator must resolve. Explore §Gap 3 flagged it.
  - **Data migrations:** None on disk; convention change only.
  - **Config surface:** None.

## Requires decision (conflicts)

None. No primitive cannot coexist with the new requirement once the orchestrator's paraphrase work is replaced. The would-be conflict — "old Step 10 instructs the orchestrator to aggregate, new contract instructs critics to author" — is resolved by the `replace` of the Step 10 wording itself; both cannot stand, and the user has chosen by raising the requirement.

## Preserved primitives with stated reason (non-default)

- **Absence of harness-level hooks (`.claude/settings.json` has no `hooks`):** Preserved because the established stack-wide convention for `Write` scoping (already in use by `subagent-distiller`, `scope-mapper`, `frame-challenger`) is instruction-level. Adding harness enforcement *for the critics specifically* would create asymmetric enforcement — three agents under hook discipline, three (the existing Write-holders) not — which is a worse failure mode than uniform instruction-level discipline. Concrete cost of *not* preserving: building the hook is upgrade #3's full scope, which is tagged `profound` and not yet specified. Forcing it as a precondition couples this requirement to an un-built primitive of much larger scope.
  - **Caveat that the frame-challenger and outside-view both flag:** the outside-view distillation places this proposal **below base rate (~40–50%) for clean transition** specifically because the load-bearing artifacts (session-id propagation contract, shared schema, reversibility plan) are missing. Preserving "no hooks" is the right call for *this* requirement's scope, but it concentrates the burden on instruction-level prose to do the work a hook would otherwise do. The generator must address this concentration explicitly.

- **Upgrade #3 (PostToolUse verification hook):** Preserved as un-built. Stated reason: same as above — it is the natural complement, not a hard dependency. Shipping this requirement without #3 is reversible (XS cost per Explore §Inferred 8); shipping #3 without this requirement is also coherent. The two should ship together *if* outside-view's stale-session/wrong-path-write risk surfaces in the first ~20 sessions, but absence of #3 does not block this requirement.

- **Upgrade #14 (hard gates as harness hooks):** Preserved as un-built. Stated reason: orthogonal. This requirement does not invoke the hard-gate mechanism (Step 9's gate on `scope-map.md` + `challenges.md` is unaffected). No hard dependency.

## Primitives the distillations did not name but the query implies

The orchestrator should treat these as follow-up Explore prompts before generation if the generator chooses to address them:

- **Session-id propagation mechanism.** How `<session-id>` is currently passed to subagents (env var, prompt arg, prose convention) is not documented in the Explore return (Explore §Gap 2). Outside-view §Inferred 5 names this as the **modal failure mode** of the proposal. Any instruction-level scoping in the critic agents will template a path against `<session-id>`; if the orchestrator's invocation prompt does not reliably pass it, all three critics produce orphaned files in parallel.
- **Step 10 inline-return parsing.** Whether the orchestrator's current Step 10 prose parses the inline critic return for verdict label (and if so, in what format) is not surveyed (Explore §Gap 1). Reversibility of the change depends on this.
- **`v2` rewrite-loop convention.** Whether a critic re-invoked under Step 11 writes `<lens>-v2.md` itself or overwrites `<lens>.md` (Explore §Gap 3). This is a contract gap, not a fact gap — the generator must *decide*, not merely *survey*.
- **Shared output schema across the three lenses.** Outside-view §Inferred 6 names schema drift as the second-priority failure; canon-librarian §Inferred 7 calls for schema-validated writes. The current critic agents have *similar but not identical* output sections (Explore §Direct facts 1–3 note 6 vs 7 sections, verdict at line 42 vs 47). Whether to enforce a shared schema is not in the requirement but is implied by the failure-mode analysis.
- **`.claude/settings.json` allow/deny enforcement on `Write` paths.** Explore §Gap 4 — whether path scope is enforceable via deny rules even without a full hook is unexamined. This is the cheapest possible harness-level defense and was not in scope of the Explore return.
- **`WebFetch`/`WebSearch` retention alongside `Write`.** Explore §Gap 5 — canon-librarian §Inferred 5 warns of decision dilution from tool-set expansion. Whether the critics *need* `WebFetch`/`WebSearch` at all (currently granted; usage unknown) is a slim-the-tool-grant question the requirement implicitly raises.
