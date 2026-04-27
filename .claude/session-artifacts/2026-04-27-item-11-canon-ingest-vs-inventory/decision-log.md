# Decision log

## 2026-04-27 — Step 10 verdict triage

Step 10 verdicts: architecture = rework, operations = rework, product = rework.

All three vetoes are **design-level**, not frame-level. The frame ("close item 11; the YAML split is settled this session") is intact — the lenses do not require re-running the scope-mapper or frame-challenger. They require the candidate to:

1. relocate the fix from an ephemeral surface (punch-list) to a durable one (agent prompt and/or canon/README.md);
2. phrase the truth-about-retrieval to be invariant under a future fold of `sources.ingest.yaml` into `sources.yaml`;
3. name the architectural follow-on (the fold) so commit 92d9387 is recorded as a second-drift signal rather than closed as a one-off;
4. drop the "ask one question first" experiment (re-asks the user's own done-when) and replace with a checkable detection recipe.

**Decision: rewrite, not replan. Routed to step 9.** Loop count: 1 of 2.

## 2026-04-27 — Step 10 loop 2

All three lenses returned `approve` against [candidate-v2.md](candidate-v2.md). Minority-veto cleared. Proceeding to step 12 synthesis.
