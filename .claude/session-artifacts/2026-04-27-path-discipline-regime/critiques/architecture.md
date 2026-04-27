# Architecture-lens critique — path-discipline regime (loop 1)

## Verdict: rework

## Frame-level objection

The candidate, the frame, and the frame-challenger all treat *"how do we enforce path style"* as the question. Architectural frame: **this repo has no architectural primitive for "policies that gate the agent loop."** The candidate invents that primitive by precedent — a `PostToolUse` hook with a bash script and an exclusion list. Whatever shape this first hook takes will become the template for every future gate (privacy redaction, secret scanning, citation discipline, output-shape validation). The decision being made is not "what enforces clause 2" — it is **"what is the gate-substrate of this stack."** That is bigger than the candidate scopes; the candidate ships a substrate-by-accident.

## Weakest link

The `PostToolUse` hook lives in the same process tree as the workflow it gates, and that workflow's own subagents (including this critic panel) call `Write` to produce session artifacts. The candidate's mitigation — exclude `.claude/session-artifacts/` from the hook's regex scope — is a *path-prefix exception inside the very gate that's supposed to be load-bearing*. Layering inversion: the enforcement primitive must know about the workflow's artifact taxonomy in order to not deadlock the workflow. **The exclusion list IS the coupling.**

## Invariants at risk (not named by the candidate)

1. **Hook idempotence under retry.** When an agent retries a rejected `Write`, the hook must produce the same verdict for the same input. Candidate assumes pure-function semantics; doesn't name them.
2. **Total-ordering of writes within a session.** Step 9 reads step 8's `challenges.md`. If step 8's `Write` is rejected, step 9 proceeds against a missing file unless the agent surfaces the rejection. Candidate names "agents can self-correct" (assumption 3) but not the orchestrator-level invariant that *partial writes do not silently advance the workflow*.
3. **Hook scope is a closed set.** The "active surfaces" list is enumerated; new top-level surfaces (`logseq/`, `pages/`, `temporary/`) inherit no default. Denylist-by-omission.
4. **Sweep atomicity.** Step 5 sweeps 7 active-surface files; if interrupted, partial-compliance state with no resume token.
5. **Hook-vs-LEDGER coherence.** Hook regex is whole-file; gate semantics is per-edit. A future LEDGER edit that touches an unrelated row is rejected because the *file* contains a violation, not because the *edit* introduced one.

## Coupling and direction

**Direction is wrong.** The hook (volatile — bash regex, settings.json wiring, exclusion list) is being made a dependency of the workflow runtime (stable — 12-step orchestration in [`CLAUDE.md`](CLAUDE.md)). Volatile-blocks-stable.

**Meta-repo soft coupling: yes, and load-bearing.** This repo's job is to review *other* repos' designs. Adding a `PostToolUse` hook that gates the repo's own outputs creates a self-referential feedback loop. Concretely: this critic-architecture agent writing a critique through `Write` will be subject to the path-discipline hook. If a future critique cites a relative path *as a critique target*, the hook rejects the critique-write itself. The system cannot distinguish "this Write contains a path-style violation as content" from "this Write is a path-style violation."

**"Active surfaces" vs "session artifacts" as a module boundary: doesn't hold.** Boundary is drawn by directory prefix, but the actual invariant is *mutability* (the longitudinal-record contract). Directory-prefix is a *proxy* that drifts. Clean boundary would be a per-file `# immutable: true` front-matter token.

**Option D rejection reasoning: unsound.** Candidate's reason (i) — operator-authored top-level docs aren't covered — is a non-sequitur. Option D distributes the *prose* rule; the hook (mechanical) is orthogonal and surface-agnostic. Reason (ii) — distribution multiplies sync points — inverts the actual coupling: a single CLAUDE.md clause + four places that must read it is *more* fan-out than four authoring-surface clauses with no orchestrator cost. Candidate confuses *textual centralization* with *coupling minimization*. **Option D plus the hook is strictly less coupled than Option A's CLAUDE.md-clause-plus-hook**, because the orchestrator prompt (a hot path) no longer carries authoring-output policy.

## Ignored architectural alternatives

1. **Per-file immutability/policy front-matter.** A small YAML token (`enforce-path-style: false`) on session-artifact files makes the hook read file-local policy. Decouples enforcement from path layout.
2. **Templated link generation primitive.** A `bin/repo-link <path>` helper or a Markdown preprocessor that emits canonical form. Authors and agents call the helper instead of writing raw links. **True poka-yoke** (canon §1, §2): the wrong form becomes unsayable, not just rejected.
3. **CI-side enforcement instead of `PostToolUse`.** Pre-commit / CI lint keeps the workflow runtime clean; pushes enforcement to a layer that doesn't share a process with subagents.

## What flips the verdict to approve

Either:
- (a) the candidate shows the hook is genuinely scoped to clause 2 forever and not the seed of a gate-substrate, OR
- (b) the candidate names the gate-substrate explicitly and ships clause 2 as the first instance of it.
