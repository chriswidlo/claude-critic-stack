# Critic panel verdicts — shadow comparator implementation

Three lenses run in parallel (inline by the orchestrator under autonomous-execution constraints). Each verdict stands alone; minority-veto applies.

---

## Architecture lens

### 1. Weakest structural link

The comparator's output format is coupled to a not-yet-stable agreement taxonomy (`agree | partial-agree | disagree`). If usage reveals a fourth bucket ("agree on verdict, disagree on rationale"), every comparator output written to disk under the old taxonomy becomes lossy. The proposal does not version this taxonomy.

### 2. Invariants at risk

- **One verdict file per lens per session** — the shadow lane breaks this by writing a second `<lens>.shadow.md`. Downstream consumers that glob `critiques/*.md` now get inconsistent counts. Untriaged.
- **Agent names are stable identifiers** — three new shadow agents add to the registry; documentation that hardcodes "the three critic lenses" goes stale immediately.
- **Comparator runs after both lanes** — temporal invariant. If the harness fires the parallel batch and the comparator before either lane finishes writing, the comparator sees stale or missing files. The proposal does not specify the read-after-write barrier.

### 3. Coupling and direction

Comparator depends on lens output paths (concrete) — coupling points from stable to volatile. Should be the other way: lenses write to a known schema, comparator reads via a stable interface. The proposal puts concrete file paths in the comparator prompt, which is the wrong direction.

### 4. Ignored architectural alternatives

- **Comparator-as-hook** rather than agent: a `PostToolUse` hook on Agent invocations that processes verdict files. Eliminates the seventh agent invocation entirely.
- **Comparator-as-data-only**: emit structured JSON rather than markdown comparison documents; defer rendering to step 12 synthesis. Fewer files on disk.

### 5. Frame-level objection

The panel was advertised as "three lenses, minority veto." Adding a shadow lane silently makes it seven agents. The "three lens" frame is now misleading; the workflow's narrative coherence breaks. Either the framing has to change to "three lenses with optional triangulation layer" (and CLAUDE.md must say so) or the shadow lane is doing something the documentation conceals.

### 6. Verdict

**rework** — what would change the verdict: a structured comparison schema (table, not prose), a documented read-after-write barrier, and CLAUDE.md text that explicitly reframes the panel from "three lenses" to "three lenses + optional triangulation meta-lens."

---

## Operations lens

### 1. Most likely incident

At time T, an operator runs `SHADOW_PANEL=1` for the first time on a complex candidate and the parallel batch of seven Agent calls saturates the Claude Code rate limit, causing one or more lens invocations to fail silently. Root cause: the proposal does not specify retry behavior when one lane in the parallel batch errors.

### 2. Blast radius

Single user, single workflow run. No production system involved. The "blast" is a degraded review run, not user-facing. Bounded.

### 3. Rollout / rollback

- Rollout: opt-in via env var, off by default. Safe.
- Rollback: unset env var. Trivial.
- Two-systems-running period: never. The shadow is purely parallel; turning it off doesn't affect the Opus lane.

### 4. Observability gap

Comparator output isn't logged anywhere structured for retrospective analysis. To answer "is the shadow producing signal?" the operator has to manually grep across session-artifacts. No counter, no dashboard, no log line says "this session saw disagreement on lens X." This is the gap.

### 5. Cost at failure

Doubling of per-lens spend when enabled. No retry storms (single fan-out, no recursion). No human on-call (this isn't production). Cost is entirely API spend, bounded per session.

### 6. Frame-level objection

The frame treats this as a quality-of-review problem; the operations view is that without retrospective comparator-output logging, the system *cannot answer its own value-proof question* (does shadow disagreement carry signal?). The 💎 value-proved state is unreachable without the observability gap closed first.

### 7. Verdict

**approve** — what would change the verdict: nothing for now; the observability gap is real but is a follow-up entry's problem, not a blocker for this implementation. If the gap stayed open after three months of `SHADOW_PANEL=1` use, this verdict flips to `rework`.

---

## Product lens

### 1. User-visible consequence

In step 12 synthesis, the operator now sees "Triangulation signal" as an extra section. If the rendering convention is undefined, the operator may glance at it as decoration and miss the load-bearing case (Opus says approve, Sonnet shadow says reject). The shadow's value is entirely in *being read*; an unread shadow is dead code.

### 2. Commitments implied

Once shipped, the operator builds intuition that shadow outputs exist and can be checked retrospectively. Removing the shadow later (or changing comparator output format) breaks that intuition. The taxonomy-versioning issue from the architecture lens compounds here.

### 3. Migration burden

None for end-users (this is an internal review tool). Some for CLAUDE.md readers: the workflow's step 10 narrative now has a sub-clause about `SHADOW_PANEL`. Anyone reading CLAUDE.md as authoritative now has to learn the new env-var convention.

### 4. Product affordances better / worse

- Better: triangulation visibility for high-stakes reviews.
- Worse: the workflow's narrative simplicity ("three lenses, minority veto") is now compromised. The cost is documentation surface area.

### 5. Frame-level objection

The frame treats shadow as an *option* to flip on. Product-wise, options that are off-by-default and require an env var to discover have near-zero adoption. If the proposal wants the shadow to actually run, it needs a non-env-var trigger — e.g., automatic for entries tagged `high-stakes`. Otherwise this ships and rusts.

### 6. Verdict

**rework** — what would change the verdict: a documented synthesis-rendering convention for "Triangulation signal" (separate bullet, never folded into verdict), and either an auto-trigger condition or an explicit acceptance that the shadow is opt-in-only-for-power-users.

---

## Aggregate

| Lens | Verdict |
|---|---|
| architecture | rework |
| operations | approve |
| product | rework |

Two `rework`. Minority veto fires. Route to step 11 (replan-vs-rewrite). Both rework verdicts are *design-level* — comparator schema, synthesis rendering. Rewrite, not replan. Adjustments are documented in the entry's [Implementation — what was done](upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md#implementation--what-was-done) section.
