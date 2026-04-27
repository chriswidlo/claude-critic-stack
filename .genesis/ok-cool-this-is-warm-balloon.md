# claude-critic-stack — Phase 2 SOTA upgrade (pragmatic cut)

## Context

Phase 1 (research pipeline) is live on `main` as of 2026-04-24: a zero-dep Node ingester, a populated `canon/corpus/` (8 full sources + 11 paywalled stubs + 1 pdf-manual stub), librarian-first routing in `CLAUDE.md`, a `canon-refresher` agent for RSS-driven proposals.

This plan does two things:

1. **Phase 1 hygiene.** Four corrective fixes targeting bugs Ultraplan found by reading the actual code. One of them (C1) is a real hallucinated citation I introduced; the others harden around that class of silent failure.
2. **Phase 2 SOTA upgrade.** Five new agent roles (classifier, distiller, scope-mapper, frame-challenger, critic-panel), a 12-step `CLAUDE.md` routing rewrite, per-session artifact scaffolding, and one regression scenario.

The plan is a **pragmatic cut** of Ultraplan's fuller 14-item Phase-1 critique + multi-phase Phase-2 proposal. Ultraplan's full output is competent but over-engineered for a single-user design-review stack; items that only add maintenance surface (C3 `--verify`, C6 rejected-list, C7 feed-staleness, C12 per-source chapter cap, C13 fresh-clone hook) are deferred. The items kept below are the ones with asymmetric value — either they prevent silent correctness bugs, or they are the actual upgrade.

All paths are repo-relative. Out of scope: MCP server build, vector index, durable-workflow engines, external observability platforms, automated test runner.

---

## What changes (before → after)

```
BEFORE:  6-step workflow, single critic, 4 agent files
          → reframe → outside-view → canon-librarian → generator → critic → synthesis

AFTER:   12-step workflow, 3-lens critic panel, 10 agent files
          →  1. requirement-classifier
          →  2. reframe
          →  3-5. outside-view + canon-librarian + Explore (parallel)
          →  6. subagent-distiller  (×N, one per returned subagent)
          →  7. scope-mapper
          →  8. frame-challenger
          →  9. generator     ◄── HARD GATE: scope-map.md & challenges.md must exist
          → 10. critic-panel (architecture + operations + product, parallel, minority-veto)
          → 11. replan-vs-rewrite decision
          → 12. synthesis

Per-session artifacts land under .claude/session-artifacts/<id>/ (local; exemplars tracked).
```

---

## Phase 1 hygiene (kept from Ultraplan's critique)

### C1. Delete fabricated `agentic-problem-frames-2026` entry

`canon/sources.ingest.yaml` points at `https://arxiv.org/abs/2602.19065`. arXiv IDs encode `YYMM.NNNNN`; `2602.*` is February 2026 and today is 2026-04-24. I invented the ID. The `arxiv-abs` fetch "succeeded" because `fetchArxivAbs` doesn't validate that the extracted title or abstract is non-empty — 404-as-200 pages ingest as clean stubs with a real sha256. Delete the entry; delete the slug dir; update any downstream references.

### C2. Harden `fetchArxivAbs`

After extracting `title` and `abstract`, assert both are present and the abstract is more than placeholder-length. Throw on failure so the slug is marked `failed` rather than silently accepted.

### C8. Outside-view consults canon first

`outside-view.md` should Grep `canon/corpus/` for reference-class authors (Kahneman, Flyvbjerg, Tetlock, etc.) **before** any WebSearch. Canon is the source of truth; WebSearch is for currency and declared gaps. Consistency fix: the stack enforces this rule for generators already (via the librarian-first rule in `CLAUDE.md`), but `outside-view` was leaking.

### C11. YAML schema validation in the ingester

`parseSourcesYaml` succeeds on malformed entries (typos like `fech: html` cause a confusing runtime error mid-loop instead of fail-fast). After parsing, validate every entry has `{slug, url, fetch, license}` as strings and `fetch` in the known set. Fail the whole run with the list of bad entries.

---

## Phase 2 SOTA upgrade

### 2.0 Session-artifact scaffolding

Create `.claude/session-artifacts/<id>/` at the repo root (NOT under the user's global Claude Code project memory directory). Per session:

```
.claude/session-artifacts/<id>/
├── requirement.md          # requirement-classifier output
├── frame.md                # reframe + frame-challenger revisions
├── scope-map.md            # scope-mapper output
├── challenges.md           # frame-challenger output
├── distillations/
│   ├── outside-view.md
│   ├── canon-librarian.md
│   └── explore.md          # only if Explore ran
├── critiques.md            # critic-panel aggregate
└── decision-log.md         # replan-vs-rewrite decisions
```

**`.gitignore` decision (flagged):** ignore per-session subdirs by default; track `README.md` + curator-promoted `exemplars/`. Ephemera stays local; the ark-mono regression test (Phase 4) is the first exemplar candidate. Option to flip — one `.gitignore` line.

### 2.1–2.5 New agent files (under `.claude/agents/`)

Five new roles. Each follows the existing agent-file shape (front-matter: name/description/tools; sections: Mandatory behavior, Things you must not do, Output format, Anti-patterns). Near-verbatim content is in the agent files themselves.

- **`requirement-classifier.md`** — labels the ask {new / replace / extend / migrate / refactor / investigation} and names the frame bias each label carries. Runs first. ≤600 tokens out.
- **`subagent-distiller.md`** — post-processes every subagent return into structured {Facts, Interpretations, Authority-framed-claims flagged, Confidence}. ≤2k tokens out. Orchestrator reads the distillation, not the raw return. Anti-anchoring enforced as an artifact, not a prompt rule.
- **`scope-mapper.md`** — tabulates existing primitives against the new requirement: subsume / replace / extend / conflict. Default is subsume or replace; preservation requires a stated reason.
- **`frame-challenger.md`** — devil's advocate on the frame, not the candidate. Runs pre-generator. Must name ≥1 alternative frame and ≥1 condition under which the current frame is wrong.
- **Critic panel** — three lens agents invoked in parallel:
  - `critic-architecture.md` — structural / invariant / dependency lens
  - `critic-operations.md` — SLO / blast-radius / rollback / cost lens
  - `critic-product.md` — user-visible contract / commitment / migration-burden lens

  Minority-veto: any one lens forcing `rework` or `reject` routes the orchestrator to step 11 (replan vs. rewrite). Each lens must produce at least one **frame-level** objection in addition to its lens-specific critique. The old single `critic.md` is deleted — the panel is unambiguous routing.

### Phase 3: `CLAUDE.md` 12-step rewrite

Replace the current `Default behavior` section with the 12-step flow shown above. Preserve every existing rule (librarian-first, anti-anchoring, stub respect, three-assumptions-or-flip, do-not-anchor-to-codebase). Add three:

- Do not start the generator step without `scope-map.md` and `challenges.md` on disk.
- Do not read raw subagent output after step 6 — only distillations.
- Do not collapse the three critic lenses into one aggregate verdict.

Update the "When to break routing" exceptions: "skip the critic-panel" skips steps 10–11; "quick take" bypasses steps 3–11 with a single flag. Update agent inventory.

### Phase 4: Regression test

`tests/regression/ark-mono-connector-routing.md` — the ark-mono connector-routing scenario from the prior session, with concrete acceptance criteria (classifier must label `replace` or surface it as alternative; scope-map must default BRE to `replace`; frame-challenger must challenge any preservation row; generator must default to `replace BRE + sticky-ID`; critic-panel must produce a frame-level objection on preserve-default candidates; synthesis must cite the user constraint if preservation is chosen). Manual grading — no assertion runner. If this scenario passes, its `.claude/session-artifacts/<id>/` copy is promoted to `exemplars/`.

---

## Execution order (single pass, this session)

```
1. Write this plan file (now on disk)
2. Phase 1.2 hygiene: C1 (delete), C2 (fetcher guard), C11 (schema validation), C8 (outside-view canon-first)
3. Phase 2.0 session-artifacts scaffolding + .gitignore update
4. Phase 2.1–2.5 agent files (7 new, 1 delete)
5. Phase 3 CLAUDE.md 12-step rewrite
6. Phase 4 regression test
7. Commit in 3 chunks: plan, hygiene, Phase 2+3+4
8. User pushes to origin
```

---

## Files to create / modify / delete

### Create
```
.claude/agents/requirement-classifier.md
.claude/agents/subagent-distiller.md
.claude/agents/scope-mapper.md
.claude/agents/frame-challenger.md
.claude/agents/critic-architecture.md
.claude/agents/critic-operations.md
.claude/agents/critic-product.md
.claude/session-artifacts/README.md
.claude/session-artifacts/exemplars/.keep
tests/regression/ark-mono-connector-routing.md
```

### Modify
```
bin/ingest-canon.mjs            (C2 fetcher guard, C11 schema validation)
canon/sources.ingest.yaml       (C1 delete agentic-problem-frames-2026 block)
.claude/agents/outside-view.md  (C8 new Mandatory #0)
.gitignore                      (ignore per-session dirs, track exemplars + README)
CLAUDE.md                       (12-step rewrite, updated must-nots and inventory)
plans/ok-cool-this-is-warm-balloon.md (this file)
```

### Delete
```
.claude/agents/critic.md                          (replaced by 3-lens panel)
canon/corpus/agentic-problem-frames-2026/         (C1)
```

---

## Verification

After commit, run this scenario without hinting at the answer:

> *"We have an existing monorepo using a Business Rules Engine (BRE) to route requests, with a sticky identifier threaded through every request for cache locality. We want to add a new routing path for a new class of connector. How do we do this while preserving the BRE and the sticky-ID threading?"*

Expected trace (abbreviated):
- Step 1: classifier labels `replace` or names it as the alternative; flags "preserving" as user framing bias.
- Step 7: scope-map defaults `BRE` and `sticky identifier` to `replace`.
- Step 8: frame-challenger challenges the preservation explicitly.
- Step 9: generator defaults to `replace BRE + sticky-ID`, names the deletion cost.
- Step 10: at least one lens produces a frame-level objection on any preservation-default candidate.
- Step 12: synthesis includes classifier label, frame revision history, scope-map summary, frame challenge, post-critique recommendation, three named uncertainties, cheapest experiment.

Failure signatures and recovery are documented in `tests/regression/ark-mono-connector-routing.md`.

---

## What is deferred (Ultraplan items skipped from this cut)

- **C3** `--verify` flag on the ingester — marginal value for solo use.
- **C4** short-chapter filter in html-multi — low-probability guard.
- **C5** librarian surfaces overlapping stubs — refinement; the existing stub-respect rule is adequate for the current corpus.
- **C6** `canon/refresher-rejected.yaml` — the refresher is weekly and curator-gated; noise is tolerable.
- **C7** feed-staleness warnings — polish.
- **C12** per-source `max_chapters` — code comment in `bin/ingest-canon.mjs` already notes the idea; schema-forward-compat when actually needed.
- **C13** SessionStart hook for fresh clones — over-engineered for a single-user setup.

Any of these can be added later without changing the plan's core shape. They are skipped because the implementation cost exceeds the expected value for a solo design-review tool, not because they are wrong.

---

## What's not automatable

- Claude-code Routines scheduling for the refresher — cloud-side, user's claude.ai account, manual setup.
- Owned-book ingestion (`bin/ingest-owned-book.mjs`) — per book, with plaintext the user owns.
- Refresher curation — proposals in, curator decides what becomes a `sources.ingest.yaml` entry.
- Exemplar promotion — session artifacts graduate to `.claude/session-artifacts/exemplars/` by curator hand.
- Regression-test grading — the test is read by a human; the artifacts are the evidence.
- The `.gitignore` choice for per-session artifacts (track vs. ignore) — this plan picks ignore; one line to flip.
