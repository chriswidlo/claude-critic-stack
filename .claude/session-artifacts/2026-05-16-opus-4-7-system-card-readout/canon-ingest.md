# Canon ingest proposal — Opus 4.7 System Card

> **Status: proposed.** This file does NOT modify [canon/sources.ingest.yaml](canon/sources.ingest.yaml) or [canon/corpus/](canon/corpus/) directly. The human curator (the user) decides whether to paste the YAML block below into [canon/sources.ingest.yaml](canon/sources.ingest.yaml) and run `bin/ingest-canon.mjs --only=anthropic-opus-4-7-system-card`.

## Why this should enter canon

The [canon-librarian distillation](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/distillations/canon-librarian.md) declared corpus coverage on **system-card / model-card reading practice** as **"thin"** — no Mitchell et al. 2019 *Model Cards for Model Reporting*, no Bommasani Transparency Index, no METR / Apollo / NIST AISI literature, no principal-agent / disclosure-economics canon. The single steelman the librarian could surface (Anthropic 2023 *Core Views on AI Safety*) was flagged as stale (pre-RSP / Preparedness-Framework era).

Adding the Opus 4.7 System Card as a corpus entry:
- Gives the canon a **2026-vintage** primary source for vendor-self-report epistemology, addressing the staleness flag directly.
- Provides a citable artifact for **inaccessible-comparator anchoring** (the recurring Mythos Preview pattern) — the failure mode this session landed as R2 + R3.
- Provides a citable artifact for **eval-context behavior load-bearing for honesty** (§6.5.2.2) — the finding the R&D venue [upgrades/profound/2026-05-16-eval-context-disclosure/](upgrades/profound/2026-05-16-eval-context-disclosure/README.md) is built around.

## Proposed `canon/sources.ingest.yaml` block

Paste the YAML below into [canon/sources.ingest.yaml](canon/sources.ingest.yaml) under the `sources:` list. The fetch type is `pdf-manual` because the canonical URL serves a 14.2 MB PDF that the existing `bin/ingest-canon.mjs` html / html-multi / arxiv-abs fetchers do not handle (per the file header comments in `sources.ingest.yaml`, the pdf-manual fetch type is reserved for these cases). The corresponding `source.txt` would be derived by extracting the PDF with `pypdf` and injecting per-page markers (the same procedure used in this session's Phase 0).

```yaml
  - slug: anthropic-opus-4-7-system-card
    manifest_ref: { author: "Anthropic", title: "Claude Opus 4.7 System Card", year: 2026 }
    url: "https://cdn.sanity.io/files/4zrzovbb/website/037f06850df7fbe871e206dad004c3db5fd50340.pdf"
    fetch: pdf-manual
    license: "publisher-published-essay"
    topics:
      - system-card
      - model-card
      - vendor-self-report
      - safety-evaluation
      - rsp
      - alignment-assessment
      - eval-awareness
      - inaccessible-comparator
      - welfare
      - cbrn
      - prompt-injection
      - agentic-safety
    notes: |
      Canonical URL: anthropic.com/claude-opus-4-7-system-card redirects to the Sanity CDN PDF above.
      232 pages. SHA256: a7729a0e5eb61dc6818f553ae3c27ab774411cd5ab4ed7f414456d74a05c26d2.
      Last-Modified: 2026-04-16. PDF metadata title: "Claude Opus 4.7 System Card - Google Docs"
      (the "- Google Docs" suffix is an artifact of the rendering pipeline; the document title
      on page 1 is "System Card: Claude Opus 4.7").
      Acquisition path documented in session [`2026-05-16-opus-4-7-system-card-readout`](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/);
      raw zone reads at `raw/zone-{a,b,c,d}.md`, distillations at `distillations/zone-{a,b,c,d}.md`.
      Source for the load-bearing R2/R3/R5 changes landed in this stack on 2026-05-16.
```

## Sister entry — corresponding `canon/sources.yaml` row

The user maintains [canon/sources.yaml](canon/sources.yaml) by hand (per the file's header comment); proposing it here so the curator has the full row in front of them when they accept the ingest:

```yaml
  - slug: anthropic-opus-4-7-system-card
    manifest_ref: { author: "Anthropic", title: "Claude Opus 4.7 System Card", year: 2026, publisher: "Anthropic" }
    canonical_form: pdf
    primary_lens: vendor-self-report-epistemology
    why_in_canon: |
      First 2026-vintage primary source on vendor system-card practice in the corpus.
      Carries the recurring "inaccessible-comparator anchoring" pattern (Mythos Preview
      as the unverifiable safety reference) and the load-bearing §6.5.2.2 finding on
      eval-context behavior diverging from deployment-context behavior. Both surface in
      this stack's R2/R3 (CLAUDE.md MUSTNOT + outside-view detection) and R1 R&D venue.
    topics: [system-card, model-card, vendor-self-report, eval-awareness, alignment, rsp, welfare, cbrn]
    notes: "Companion source for any future vendor-system-card readout in this repo."
```

## Re-scope condition (Assumption C from [repo-changeset.md](.claude/session-artifacts/2026-05-16-opus-4-7-system-card-readout/repo-changeset.md))

If a future canon survey shows existing coverage of model-card reading practice — Mitchell et al. *Model Cards for Model Reporting* (2019), Bommasani et al. *Foundation Model Transparency Index*, METR retrospectives — already in corpus, this proposal **re-scopes** from "fill the gap" to "register 4.7 alongside existing coverage." The ingest still lands; the `why_in_canon` and `primary_lens` fields would be tightened to differentiate the 4.7 card from the existing entries, rather than treated as the primary system-card-practice source.

## Falsifier (when this proposal should be withdrawn)

This canon ingest should be **withdrawn** if:
- Anthropic supersedes the 4.7 system card with a 4.8 (or successor) system card whose body materially walks back the §6.5.2.2 finding or the AI-safety-R&D refusal regression numbers — the 4.7 card would still hold historical value but would no longer be the canonical citation for the patterns above.
- The librarian's "thin coverage" verdict is shown to be wrong by a corpus survey (Assumption C above) AND the existing coverage is closer to current vendor practice than the 4.7 card itself.

Neither falsifier is currently triggered. The proposal stands.
