# Research-pipeline fix for `claude-critic-stack`

> **Status (2026-04-23):** This plan is being **relocated into the repo** at `plans/ok-cool-this-is-warm-balloon.md` and **refined via Ultraplan** to cover the full SOTA stack (research pipeline + agent additions + observability). The refined content will replace this file on a branch in `chriswidlo/claude-critic-stack`. This user-level copy at `~/.claude/plans/` is the pre-refinement baseline — future edits should happen against the repo copy.

## Context

**Problem.** The stack at `/Users/krzys/Development/Projects/claude-critic-stack/` is a design-review agent harness whose `CLAUDE.md` mandates that every design question route through `canon-librarian` for retrieval from a curated expert corpus. The librarian, the routing rules, and the manifest at `canon/sources.yaml` are all in place — but `canon/corpus/` does not exist and there is no ingestion script. So the librarian correctly refuses to fabricate, and the orchestrator falls back on ad-hoc `WebSearch` + `WebFetch`. Every "what does the literature say" question becomes a re-google.

**The user's complaint.** "Why are you googling — why isn't there an established, reproducible pipeline for this?" Investigation shows the answer is: there *isn't* a packaged solution we can drop in. Anthropic publishes no MCP server for their own engineering content. Context7 doesn't cover agent-pattern docs. The third-party RSS feed for Anthropic's blog and arXiv's RSS exist, and there are arXiv / HF Daily Papers MCP servers, but no curated agent-canon mirror with full text. The fix is to compose what exists (RSS, WebFetch, Routines, the README.md ingestion policy that's already in place) into a small reproducible pipeline.

**Intended outcome.** After this plan executes:
- `canon/corpus/` is populated with 10 freely-licensed sources (Anthropic engineering posts, arXiv agent papers, Google SRE book, AWS SaaS Lens, Cockburn hexagonal essay, Helland paper).
- `CLAUDE.md` routes research questions through `canon-librarian` first; `WebSearch` becomes an explicit fallback only when the librarian declares the corpus does not cover the topic.
- A `canon-refresher` agent exists for weekly RSS-driven proposals of new entries (curator-gated; never writes to corpus).
- Paywalled classics (Evans/Vernon/Fowler/Nygard) appear as stub entries so the librarian acknowledges the gap rather than silently substituting a weaker source.
- A re-runnable script (`bin/ingest-canon.mjs`) makes corpus refresh idempotent.

**Out of scope for this plan.** The broader SOTA stack improvements proposed in prior turns (frame-challenger, scope-mapper, requirement-classifier, critic-panel, subagent-distiller) are a separate follow-up plan. This plan is *only* the research pipeline.

## Execution order

`4 → 1 → 2 → 5 → 3`. The allowlist must land before the first ingest run or every fetch triggers a permission prompt.

---

## Phase 4 — WebFetch / Bash allowlist update *(do first)*

**File:** `/Users/krzys/Development/Projects/claude-critic-stack/.claude/settings.local.json`

Use the `update-config` skill (keeps JSON valid). Add to `permissions.allow`:

```
WebFetch(domain:alistair.cockburn.us)
WebFetch(domain:queue.acm.org)
WebFetch(domain:sre.google)
WebFetch(domain:docs.aws.amazon.com)
WebFetch(domain:aclanthology.org)
WebFetch(domain:raw.githubusercontent.com)
WebFetch(domain:rss.arxiv.org)
Bash(node ./bin/ingest-canon.mjs:*)
Bash(node ./bin/ingest-owned-book.mjs:*)
```

`arxiv.org` and `www.anthropic.com` are already on the existing allowlist — do not duplicate. Confirm WebFetch matching is exact-host before adding `rss.arxiv.org`; if suffix, drop it.

**Verify:** `node -e "JSON.parse(require('fs').readFileSync('.claude/settings.local.json'))"` exits 0.

---

## Phase 1 — Provision the starter corpus

### Files to create

```
canon/sources.ingest.yaml          (machine-readable companion to sources.yaml)
bin/ingest-canon.mjs               (executable, Node, no npm install)
bin/ingest-owned-book.mjs          (helper for Phase 5; same dir for symmetry)
canon/corpus/                      (populated by the script)
```

### Why a separate `sources.ingest.yaml`

`canon/sources.yaml` is the human-curated manifest organized by topic with prose. The ingester needs `(slug, url, fetch-mode, license, topics)` per source — that doesn't belong in the manifest's prose. Cross-reference by `manifest_ref: { author, title, year }`.

### `canon/sources.ingest.yaml` — initial 10 entries

| Slug | URL | Fetch mode |
|------|-----|------------|
| `anthropic-building-effective-agents` | https://www.anthropic.com/research/building-effective-agents | html |
| `anthropic-multi-agent-research-system` | https://www.anthropic.com/engineering/multi-agent-research-system | html |
| `anthropic-effective-context-engineering` | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | html |
| `cockburn-hexagonal-architecture` | https://alistair.cockburn.us/hexagonal-architecture/ | html |
| `helland-life-beyond-distributed-transactions` | https://queue.acm.org/detail.cfm?id=3025012 | html |
| `google-sre-book` | https://sre.google/sre-book/table-of-contents/ | html-multi |
| `aws-saas-lens` | https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html | html-multi |
| `shinn-reflexion-2023` | https://arxiv.org/abs/2303.11366 | arxiv-abs |
| `chen-devils-advocate-2024` | https://aclanthology.org/2024.findings-emnlp.53/ | arxiv-abs |
| `agentic-problem-frames-2026` | https://arxiv.org/html/2602.19065v1 | html |

Each entry carries `topics: [...]` for librarian Grep filtering, and `license` tag for audit. Full schema example in plan-agent output; consistent with `canon/README.md:1-47`.

### `bin/ingest-canon.mjs` — script outline

- Reads `canon/sources.ingest.yaml`. Parses with a ~80-LOC inlined YAML mini-parser (the file uses a strict subset, no anchors, no flow nesting beyond `{a: b}`). Avoids `npm install`.
- For each source: `mkdir canon/corpus/<slug>/`, fetch via `node:fetch`, write `source.txt` + `citation.yaml` + `README.md`.
- HTML→text: drop `<script>/<style>/<nav>/<footer>/<aside>`; convert headings to `# H1`; convert `<p>/<li>/<br>` to newlines; decode entities; collapse whitespace; prepend 5-line provenance header (URL, fetched-at, sha256).
- `html-multi`: TOC page → child URLs sharing the path prefix → fetch each → concatenate with `\n\n=== <chapter title> ===\n\n` separators. Errors loudly if zero links found.
- `arxiv-abs`: fetches `/abs/<id>`, extracts title/authors/subject/abstract/date. No PDF parsing in v1. Sets `body_completeness: abstract_only` in citation.
- Idempotent: skips slugs whose `source.txt` already exists. `--force` to refetch. `--only=<slug>` to scope.
- Reuses existing structure: matches `canon/README.md` per-source folder format exactly; the librarian agent does not need to know about the script.

### Citation YAML shape (per source)

Fields written by the script: `slug, author, title, year, kind, topics, source_url, fetched_at, sha256, license, body_completeness, chapter_offsets, stale, notes`. `chapter_offsets` populated automatically for `html-multi` from concatenation boundaries; empty `[]` for single essays.

### Risk notes

- **SRE Book may produce 5-10 MB.** Acceptable for grep but worth knowing. Mitigation if noisy: list five chapters explicitly in `sources.ingest.yaml` (SLOs, Embracing Risk, Eliminating Toil, Postmortem Culture, Incident Response) instead of TOC scraping.
- **`raw.githubusercontent.com`** for the community Anthropic RSS — third-party feed; if it stops being maintained the refresher degrades to arXiv-only. Add `last_validated:` field to `refresh-feeds.yaml` and review every 6 months.

### Verify

1. `node ./bin/ingest-canon.mjs` exits 0.
2. `ls canon/corpus/` shows 10 directories matching slugs.
3. Each slug dir has all three files non-empty.
4. `wc -l canon/corpus/*/source.txt` — flag <50 lines as suspect; arXiv abstracts ~30-80 OK.
5. Provenance header on lines 1-5 of each `source.txt`.
6. **Functional test:** Invoke `canon-librarian` with *"What does the literature say about giving subagents authority to dissent from the orchestrator?"* — must return passages from `anthropic-multi-agent-research-system` and `chen-devils-advocate-2024`, plus at least one contradicting passage. Failure means topic tags are wrong; fix tags, do **not** add a vector index.

---

## Phase 2 — Routing fix in `CLAUDE.md`

**File:** `/Users/krzys/Development/Projects/claude-critic-stack/CLAUDE.md`

Three surgical edits, no rewrites.

### Edit 1: replace step 3 ("Canon librarian subagent")

> **3. Canon librarian subagent — first, not last.** For any question of the form "what does the literature say / what's the established pattern / how do practitioners do X," invoke `canon-librarian` **before** any `WebSearch` or `WebFetch`. The librarian must return at least one passage that disagrees with the user's framing.
>
> **Fallback rule.** Only after the librarian's output explicitly states `## Corpus coverage: none` (or `thin` for the specific sub-question) may you fall back to `WebSearch`/`WebFetch`. When you do, name the gap in your synthesis: *"corpus did not cover X; web result is from Y, not in canon."* Web results are not promoted to canon by being cited once.
>
> **Anti-anchoring.** After reading the librarian's output, restate the key findings in your own words before generating a recommendation. Do not paste the librarian's quotes as your answer. Quotes belong in step 6 (synthesis), not step 4 (generator).

### Edit 2: add to "Things you must not do"

> - **Do not WebSearch a research question without invoking the librarian first.** The corpus is the source of truth for what the field has already established. WebSearch is for currency (post-corpus events) and gaps the librarian has explicitly declared.

### Edit 3: add to "Agents available in this stack"

> - `canon-refresher` — fetches recent posts from a small set of RSS feeds, diffs against `canon/corpus/`, and proposes new entries for human review. Manual invocation; not part of the default workflow.

### Verify

1. Pose corpus-covered question: *"What's the canonical case for hexagonal architecture and what's the strongest critique?"* → first tool call is `canon-librarian`, not `WebSearch`.
2. Pose corpus-uncovered question: *"What's current consensus on Rust-vs-Zig for embedded firmware in 2026?"* → librarian returns `Corpus coverage: none`, then `WebSearch` fires with the gap named in synthesis.

---

## Phase 5 — Stub entries for paywalled books

**Goal:** Make the corpus self-documenting about its gaps. Librarian acknowledges Evans/Vernon/Fowler/Nygard exist instead of substituting a weaker passage.

### Files to create

For each of: `evans-ddd`, `vernon-iddd`, `vernon-strategic-monoliths`, `fowler-refactoring`, `fowler-poeaa`, `nygard-release-it`, `feathers-legacy-code`, `hohpe-eip`, `meszaros-xunit`, `beck-tdd`:

```
canon/corpus/<slug>/README.md          (documents stub status + populate command)
canon/corpus/<slug>/citation.yaml      (body_completeness: stub, license: paywalled-no-open-edition)
```

**No `source.txt`** — its absence is the stub signal.

### `bin/ingest-owned-book.mjs` — outline

```
Usage: ingest-owned-book.mjs <slug> <path-to-text>
- Validate slug exists as a stub under canon/corpus/<slug>/.
- Validate input is UTF-8 and >10 KB (refuse obvious empties).
- Soft-warn if input path looks like libgen/sci-hub/z-library (the README's intent).
- Copy to canon/corpus/<slug>/source.txt.
- Update citation.yaml: body_completeness: full, sha256, ingested_at.
```

### Add one bullet to `canon-librarian.md` "Mandatory behavior"

> **Respect stubs.** A directory under `canon/corpus/` whose `citation.yaml` has `body_completeness: stub` indicates a known-but-not-ingested work. If a stub is the best match for a query, surface its citation with the note "stub entry; full text not ingested." Do not invent quotes from stubbed works. Do not silently substitute a different author.

### Verify

1. `find canon/corpus -name citation.yaml | xargs grep -l 'body_completeness: stub' | wc -l` → 10.
2. Pose librarian query that should hit a stub: *"What does Evans say about anti-corruption layers?"* → returns stub notice, not fabrication, not substitution.
3. `bin/ingest-owned-book.mjs evans-ddd /tmp/empty.txt` → refuses with clear error.

---

## Phase 3 — Refresher mechanism

### Files to create

```
.claude/agents/canon-refresher.md      (agent spec; tools: Read, WebFetch, Bash, Glob)
canon/refresh-feeds.yaml               (small config: feeds + filters)
```

### `canon/refresh-feeds.yaml`

```yaml
feeds:
  - name: anthropic-engineering
    url: "https://raw.githubusercontent.com/conoro/anthropic-engineering-rss-feed/main/anthropic_engineering_rss.xml"
    domain_filter: ["anthropic.com"]
    propose_to_topic: agents
    last_validated: "2026-04-23"
  - name: arxiv-cs-ai
    url: "https://rss.arxiv.org/rss/cs.ai"
    domain_filter: ["arxiv.org"]
    propose_to_topic: agents
    keyword_filter: [agent, multi-agent, critic, reflection, retrieval, evaluation]
    last_validated: "2026-04-23"
```

### Agent contract (`canon-refresher.md`)

- **Reads** `canon/refresh-feeds.yaml`; for each feed, WebFetch the URL.
- **Filters:** items <30 days old; titles/abstracts matching `keyword_filter`; URLs not already in `canon/corpus/<slug>/` or queued in `sources.ingest.yaml`.
- **Output:** structured "Proposed: `<slug>`" review blocks with title (verbatim from feed), URL, license signal, suggested `sources.ingest.yaml` entry.
- **Hard rule:** never writes to `canon/corpus/`. Never appends to `sources.yaml` or `sources.ingest.yaml`. Curator-gated.
- **Documents the Routine setup** at the bottom: schedule weekly at https://claude.ai/code/routines with prompt *"Invoke the canon-refresher agent and post the review blocks here."* Cannot be created from local Claude Code; user-side action.

### Verify

1. Manual invocation produces review blocks; `Items considered:` non-zero for both feeds.
2. `find canon/corpus -newer .claude/agents/canon-refresher.md` returns nothing — no writes.
3. Re-invoke immediately: items previously surfaced are skipped (already in `sources.ingest.yaml`) or re-proposed identically. Slug naming must be stable across runs.

---

## What I cannot automate

- **Routines at claude.ai/code/routines.** Cloud-side, requires your account login. The `canon-refresher.md` documents this; you set the schedule yourself.
- **Ingesting paywalled books.** Per book, with text you own. The stub + `bin/ingest-owned-book.mjs` are the affordances.
- **Curating refresher proposals.** Refresher emits, you decide which become `sources.ingest.yaml` entries before the next ingest run.
- **Maintaining `stale: true` flags.** Curator judgment, ~6-month review per `canon/README.md`.

## Existing primitives reused (no new abstractions)

- `canon/README.md:1-47` — the per-source folder format (`source.txt` + `citation.yaml` + `README.md`) and licensing policy.
- `canon/sources.yaml:1-172` — manifest topology stays as the human-readable index.
- `.claude/agents/canon-librarian.md` — output contract unchanged; one new bullet for stub respect.
- `.claude/settings.local.json` — extend `permissions.allow`, do not restructure.
- `CLAUDE.md` — surgical edits to step 3, "must not do" list, agent inventory.

## Critical files for implementation

- `/Users/krzys/Development/Projects/claude-critic-stack/.claude/settings.local.json` (Phase 4)
- `/Users/krzys/Development/Projects/claude-critic-stack/canon/sources.ingest.yaml` (Phase 1, new)
- `/Users/krzys/Development/Projects/claude-critic-stack/bin/ingest-canon.mjs` (Phase 1, new)
- `/Users/krzys/Development/Projects/claude-critic-stack/bin/ingest-owned-book.mjs` (Phase 5, new)
- `/Users/krzys/Development/Projects/claude-critic-stack/canon/corpus/` (Phases 1 + 5, populated)
- `/Users/krzys/Development/Projects/claude-critic-stack/CLAUDE.md` (Phase 2, edits)
- `/Users/krzys/Development/Projects/claude-critic-stack/.claude/agents/canon-librarian.md` (Phase 5, +1 bullet)
- `/Users/krzys/Development/Projects/claude-critic-stack/.claude/agents/canon-refresher.md` (Phase 3, new)
- `/Users/krzys/Development/Projects/claude-critic-stack/canon/refresh-feeds.yaml` (Phase 3, new)

## End-to-end verification

After all phases land, run this scenario without telling the orchestrator the answer:

> *"I'm designing a multi-agent system. What's the SOTA pattern for preventing the orchestrator from anchoring to subagent output, and what's the strongest published critique of that pattern?"*

Expected: orchestrator's first tool call is `canon-librarian`. Librarian returns passages from `anthropic-effective-context-engineering` (curate small high-signal context, distill subagent output to 1-2k tokens) and `agentic-problem-frames-2026` (formal problem-framing before execution), plus a contradicting passage (e.g., the librarian's own coverage flag noting that single-critic ensembles have known systematic bias and pointing to `chen-devils-advocate-2024`). The orchestrator restates the findings in its own words before recommending. No `WebSearch` fires unless the librarian explicitly declared a gap.

If that scenario produces a `WebSearch` as the first tool call, Phase 2's routing edit didn't take. If the librarian returns generic content without contradicting passages, Phase 1's topic tags are too coarse. Both are recoverable without re-architecture.
