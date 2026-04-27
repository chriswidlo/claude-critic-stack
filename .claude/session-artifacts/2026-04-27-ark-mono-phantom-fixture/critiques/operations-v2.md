# Critique — Operations lens (v2)

Session: `2026-04-27-ark-mono-phantom-fixture` — loop 2.

## 1. Most likely incident

At T+60 days, an operator amends [CLAUDE.md](CLAUDE.md) — say, splits step 6 into 6a/6b — and commits without touching [`tests/regression/EXEMPLAR-CONTRACT.md`](tests/regression/EXEMPLAR-CONTRACT.md). Nothing pages, nothing fails CI, the mtime divergence sits silently in the working tree; six commits later it's buried under unrelated mtime churn (a `chmod`, a re-save, a merge). Root cause: v2's forcing function is observable only by an operator who already remembers to run `ls -lt` — i.e., the same operator-memory channel that loop-1 rejected, dressed in filesystem metadata.

## 2. Blast radius

- The contract drifts behind CLAUDE.md silently.
- The "distiller-step coverage requirement" — itself the spec-currency audit v2 leans on — becomes stale.
- The empty exemplars/ directory remains empty; the *justification* for its emptiness ("bonded to a forcing surface") evaporates. The bond is unilateral.
- Single-operator stack: the radius is "the one operator, who is also the author of the forcing function." Worst possible radius for a forcing function — zero independence.

## 3. Rollout / rollback

Clean. Four atomic edits. All revert cheaply. **Two-systems-running period: infinite by construction** — the contract and CLAUDE.md are permanently coupled by mtime; no end state where the coupling is retired.

## 4. Observability gap

- **Whether mtime divergence has occurred.** Observable in principle (`stat`, `git log`). Observable in practice only if the operator runs the check. No scheduled check, no CI hook, no pre-commit. v2 explicitly defers the check-script to a follow-up under assumption 2.
- **mtime carries noise** — `git mv`, re-save, merge — bumping it without semantic change.
- **"Real slugs only" rule** enforced by reading. v2 explicitly accepts the gap.

## 5. Cost at failure

- **Cost when noticed:** authoring a re-review — bounded by contract's brevity. Lower than loop-1's "5b rots forever."
- **Cost when not noticed:** the contract becomes a museum piece; empty exemplars/ loses its bond; "regression discipline" claim erodes one indirection deeper than loop-1 worried about.
- **Compounding factor:** the contract asserts `ark-mono-connector-routing.md` is out-of-coverage based on current CLAUDE.md state. If CLAUDE.md changes and the contract doesn't, the out-of-coverage flag becomes a false claim, not just outdated.

## 6. Frame-level reading

**mtime is documentation-disguised-as-mechanism.** Technically observable file metadata, real improvement over "operator memory" — but the discipline gate is enforced by the operator reading the contract, remembering the rule, and choosing to run the comparison. Closer to a checklist than a forcing function.

That said, v2 is *honest* about this in two places: assumption 2 names the script as a follow-up; "ways v2 could be wrong" names "polite-note-disguised-as-mechanism" verbatim.

The frame-level question: is honest documentation-as-mechanism good enough for a single-operator stack where the operator is also the contract's author? Loop 1 said no. v2's bet is that the *artifact's existence* (contract + rule in CLAUDE.md + dated mtime evidence) shifts this from "wish" to "norm."

That bet is **defensible but weak**. Materially stronger than v1 because:
- Contract exists this session, not deferred.
- Rule lives in CLAUDE.md (primary surface).
- mtime is at least *checkable* — a future audit can answer "is the contract stale?" with a deterministic command.
- v2 names the gap explicitly.

It remains weak because:
- Single-operator stack with operator authoring own forcing function — no independence.
- Check is not automated; assumption 2 acknowledges and defers.
- mtime carries noise.

The honest reading: v2 has converted "no forcing function" into "weak forcing function with named upgrade path." For a single-operator research/methodology stack, that is plausibly the right strength of mechanism.

## 7. Verdict

`approve` — would downgrade to `rework` if this stack were multi-operator or if the contract document made claims that were costly when wrong. As a single-operator methodology-stack artifact with explicit honesty about the enforcement gap and a named upgrade path, the mtime convention is acceptable as a v1 of the discipline.
