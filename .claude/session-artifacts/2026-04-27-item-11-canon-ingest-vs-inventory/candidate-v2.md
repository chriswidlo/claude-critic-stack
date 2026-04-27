# Candidate recommendation v2 — item 11

Rewritten in response to three rework verdicts. Decision-log entry at [decision-log.md](decision-log.md).

## Position

Land four edits in a single commit, in order of durability of the surface they touch.

1. **[`.claude/agents/canon-librarian.md`](../../../.claude/agents/canon-librarian.md) — most durable.** Add one short "Retrieval surface" line near the top of the body (right after the existing `canon/corpus/` mention on line 9). Schema-agnostic phrasing: *"Retrieval surface is the directory tree at `canon/corpus/`. YAML files in `canon/` are catalogs and fetch queues, not retrieval indexes — do not query them at retrieval time."* This puts the truth at the agent that performs the work. Survives a future fold of `sources.ingest.yaml` into `sources.yaml` because it does not name a file count.

2. **[`canon/README.md`](../../../canon/README.md):3 — next durable.** Replace *"The curated corpus the `canon-librarian` agent retrieves from."* with *"The curated corpus the `canon-librarian` agent retrieves from. Retrieval is over the `corpus/` directory tree; `sources.yaml` is the human inventory and `sources.ingest.yaml` is the auto-fetch queue (a strict subset of the inventory) used by `bin/ingest-canon.mjs` — neither YAML is read at retrieval time."* This is the lifecycle paragraph the punch-list's done-when offered as exit (b), kept to one sentence so it does not gold-plate the shape.

3. **[`plans/2026-04-27-repo-cleanup-punch-list.md`](../../../plans/2026-04-27-repo-cleanup-punch-list.md) — ephemeral.** (a) Append `✅ done 2026-04-27` to the heading at L213. (b) Replace L222–223 with one sentence that points at the durable fix, not at the false claim: *"Closed: the three entries were added to `sources.yaml` in commit 92d9387 (research_and_innovation category). The lifecycle is now stated at [`canon/README.md`](../canon/README.md) and at [`.claude/agents/canon-librarian.md`](../.claude/agents/canon-librarian.md)."* No retraction prose, no quoting of the false claim — the truth lives at the durable surfaces, the punch-list points at them.

4. **New punch-list item 14** (or any free slot) — *open, not close*: *"Evaluate folding `canon/sources.ingest.yaml` into `canon/sources.yaml` with a `fetchable:` field. Trigger evidence: commit 92d9387 patched a class of drift between the two files manually; this is the second incident against the denormalization (folder-shape was the first). Fix sketch: one inventory file, ingest script filters at read time. Cheaper than maintaining the strict-subset invariant by discipline."*

## Frame-level objections addressed

- **Architecture lens** asked for either (a) move the mechanism truth to the agent prompt or (b) open a follow-on for the fold. I am taking **both**. (a) is edit #1; (b) is edit #4.
- **Operations lens** asked for either schema-agnostic phrasing or a checkable detection recipe. I am taking schema-agnostic phrasing (edit #1's "YAML files in `canon/`" without naming a count) so the prose survives the fold proposed in edit #4. The detection-recipe alternative is not taken: once the fold is on the queue as a tracked item, the recurring-audit cost is unjustified — the architectural fix is cheaper than the operational instrument.
- **Product lens** asked to drop the "ask one question first" experiment and land the fix at a durable surface. The experiment is dropped. The fix lands at two durable surfaces (edits #1 and #2) before touching the ephemeral one (edit #3). The punch-list edit is reduced from an embedded fact-bearing assertion to a pointer.

## Named tradeoffs

1. **Multi-surface edit vs. single-surface edit.** Editing four locations in one commit is more change than v1's two-line edit. Cost: larger blast radius if the four edits drift in tone. Benefit: each surface holds the part of the truth that fits its lifecycle (mechanism at the agent, lifecycle at the README, closeout at the punch-list, follow-on as a new item).
2. **Stating the strict-subset invariant in prose vs. enforcing it in `bin/ingest-canon.mjs`.** Edit #2 says *"strict subset"* but no code enforces it. Architecture lens flagged this as a discipline-not-enforcement issue. The right enforcement lives inside the proposed fold (edit #4), not as a separate guard now — adding a guard now would harden the two-file shape against the very refactor edit #4 proposes.
3. **Opening item 14 vs. just noting the fold in edit #2's prose.** Item 14 makes the follow-on a tracked piece of work; an inline note buries it. Cost of item 14: one more open punch-list row. Benefit: visibility, ranked alongside items 12–13.

## Named assumptions (any one wrong → recommendation flips)

1. **The librarian agent prompt is the right place for a "retrieval surface" line.** If the user's mental model is that agent prompts should describe behavior in terms of inputs/outputs only and never describe a *negative* ("do not query the YAMLs"), edit #1 violates that convention and should move into a comment block at the top of [`canon/sources.yaml`](../../../canon/sources.yaml) instead.
2. **The fold (edit #4) is a defensible follow-on rather than a rejected alternative.** If the user has already considered and rejected the one-file-with-`fetchable:` shape (e.g., because `bin/ingest-canon.mjs` is intentionally minimal and parsing the larger inventory file is undesired), opening item 14 is noise and should be dropped.
3. **The punch-list pointer (edit #3 substitution) is a cleaner closeout than restating the corrected fact.** If precedent in the punch-list is to embed the resolution in the item body (not point at another file), edit #3 should restate the lifecycle inline, accepting some duplication with edit #2.

## Named ways this could be wrong

- **The four-surface edit is over-engineered for a low-stakes closeout.** The product lens asked for a durable-surface fix; it did not ask for two durable surfaces plus a new tracked item. A reader reviewing the commit may see scope creep.
- **The schema-agnostic phrasing protects against the fold but reads obliquely today.** *"YAML files in `canon/` are catalogs and fetch queues, not retrieval indexes"* is precise but vague-by-construction. A reader who does not already know the two YAMLs may not learn enough from the agent-prompt line alone — they would need to consult the README. That is the intended layering, but it is also a documentation latency.
- **Opening item 14 may starve the cleanup queue.** The punch-list is at 13 items; adding a 14th tied to a refactor (rather than a cleanup) shifts the punch-list's center of gravity from "tidy what is broken" toward "evolve what is ugly." If the user wants the punch-list to stay strictly cleanup-shaped, the fold should live in [`upgrades/`](../../../upgrades/) instead.

## Cheapest experiment (not a user round-trip)

Before committing, run two greps as a sanity check:

```
grep -rn "sources\.yaml\|sources\.ingest" --include="*.md" .       # confirm no live doc still asserts the librarian queries a YAML
grep -rn "retriev" .claude/agents/canon-librarian.md               # confirm the new "Retrieval surface" line is the only retrieval-mechanism statement in the prompt, no contradictions
```

If either grep surfaces a contradiction, fix it in the same commit. Cost: 30 seconds of grep, no user round-trip, replaces v1's stalling experiment.
