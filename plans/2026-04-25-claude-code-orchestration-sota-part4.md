# SOTA orchestration knowledge — Part 4 (destinations + open questions)

> Continuation. Sections 12 and 13 — the choices the Ultraplan upgrade process needs to make.

---

## 12. Possible destinations for this knowledge (for the upgrade process to choose)

This file deliberately does not pick a destination. Candidates the upgrade process should evaluate:

### Option 1 — New canon entries (extend `canon/sources.ingest.yaml`)

The canon manifest already has Anthropic engineering essays from 2024–2025. The natural extension is to add:

- *Equipping agents for the real world with Agent Skills* (Anthropic, 2025) — the Skills foundational essay; direct fetch returned 403 in this pass; may need alternative URL or owner-published mirror
- Vercel *AGENTS.md outperforms skills* (Jan 2026) — the empirical contrarian
- Anthropic *Plugins / marketplace* posts (2025–2026)
- Anthropic *Routines* and *Managed Agents* announcement posts (April 2026)

These would go through the existing `canon-refresher` workflow. The current `refresh-feeds.yaml` covers `anthropic-engineering` via a third-party RSS mirror; if those posts haven't propagated, they need explicit add to `sources.ingest.yaml` for one-shot ingestion.

**Pro:** Reuses existing infrastructure exactly. The librarian gains real coverage on Skills-era questions.
**Con:** Doesn't capture the *synthesis* — only the source material. The four-mechanism-group mental model and the workload archetypes don't live in any single source; they're synthesized across many.

### Option 2 — New `docs/sota/` folder

A new top-level documentation folder that this file (and future synthesis artifacts) lives in.

**Pro:** Separates *synthesized knowledge* from *retrieved canon*. The librarian retrieves; this folder explains.
**Con:** New top-level folder is a new abstraction; CLAUDE.md will need to point to it.

### Option 3 — Extended README with a SOTA section

Add a `## SOTA orchestration model (April 2026)` section to `README.md` that links to this plan file as the long form.

**Pro:** Discoverable on the GitHub landing page; no new abstractions.
**Con:** Bloats README; mixes "what this stack is" with "what we believe about the field."

### Option 4 — New workflow file

`workflows/orchestration-design-review.md` — a workflow specifically for "the user is asking how to architect their own Claude Code stack" rather than "the user is asking about a code-design decision." Would route through the same critic / librarian / outside-view triad but with this synthesis as a starting prior.

**Pro:** Operationalizes the synthesis. Future invocations of "what's the right Claude Code orchestration for X?" route through a consistent frame.
**Con:** Adds a workflow; the current single-workflow `architecture-review.md` is doing fine.

### Option 5 — All of the above, in stages

The likely correct answer. Sources to canon (Option 1) for retrieval credibility; synthesis to `docs/sota/` (Option 2) so it's discoverable without bloating README; README link to `docs/sota/` index; workflow file deferred until a second SOTA artifact accumulates and the abstraction is justified.

### Option 6 — Do nothing structural; this plan file alone is enough

Leave this file in `plans/`. Future readers find it via grep or by reading the plans index. No CLAUDE.md edits, no README edits, no canon entries.

**Pro:** Zero blast radius. Honest about the speculative status of much of the multi-model section.
**Con:** Discoverability is poor; the synthesis decays into folklore rather than living knowledge.

---

## 13. Open questions for the upgrade process

The Ultraplan refinement should answer or punt explicitly on each:

1. **Verifiability pass on the multi-model literature.** The arXiv IDs and percentage claims were retrieved at snippet level. Re-fetch primary sources. Either commit to specific IDs+numbers in the final artifact, or strip them entirely and keep only directional claims. *Don't keep them as snippet-precision in a published synthesis.*
2. **Decide the destination.** Pick from §12 or propose a different one. Document the decision.
3. **Decide whether to add canon entries.** If yes, add to `canon/sources.ingest.yaml` (not directly to `corpus/`); the existing ingest pipeline handles the rest.
4. **Decide whether to add a CLAUDE.md pointer.** If this synthesis becomes a discoverable artifact, the routing rules in `CLAUDE.md` may want to reference it for "the user is asking about Claude Code orchestration itself" questions — distinct from the general design-review routing.
5. **Decide on staleness policy.** This synthesis will be wrong by Q3 2026 in ways we can't predict. Mark it with a `valid_until:` date or a re-validation trigger (e.g., "re-validate at next Anthropic primitive release").
6. **Decide whether `/ultrareview` belongs as a primitive or a pattern instance.** This synthesis treats it as a productized instance of archetype F, not as a primitive. The upgrade process may disagree if `/ultrareview` becomes a stable user-authored target rather than just a hosted product.
7. **Decide on the eval-harness primitive.** This synthesis lifts eval harnesses (Promptfoo / judge ensembles / Panel-of-LLMs / SE-Jury) into Group C as a first-class mechanism. The community taxonomy hasn't done this yet. Is this synthesis ahead of practice, or eccentric? The upgrade research should pressure-test the claim.
8. **Decide on terminology adoption.** *Primitives* vs *extensions* vs *components* — pick one for this repo's prose and use it consistently. The librarian and critic agents will inherit the choice.

---

> Continued in `plans/2026-04-25-claude-code-orchestration-sota-part5.md` (sections 10 + 14–17: conditions, what doesn't change, residual uncertainty, experiments, end).
