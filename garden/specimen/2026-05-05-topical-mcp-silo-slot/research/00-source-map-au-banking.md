# AU banking source map — federate vs build, by content class

_Researched 2026-06-01 - axis: first-instance source strategy (S2a). Four parallel regulator-capability probes, every verdict cited._

This file persists the S2a regulator-API capability check. It is the **domain instantiation** of the domain-agnostic architecture in [07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md): which AU-banking sources the tool *federates* (calls live) versus *ingests and self-versions*.

## Table of contents

- [Headline finding](#headline-finding)
- [The source map](#the-source-map)
- [Per-regulator evidence](#per-regulator-evidence)
- [What this means for the build](#what-this-means-for-the-build)
- [Caveat to carry to production](#caveat-to-carry-to-production)
- [Sources](#sources)

## Headline finding

**The federate-vs-build split is by content class, not by regulator.** Primary legislation and legislative instruments are authoritative, versioned, and point-in-time queryable on the Federal Register of Legislation via a real public API — so **federate** them. Regulator *guidance* (APRA prudential standards, ASIC regulatory guides, AUSTRAC guidance) has no API and no upstream version history — so **build and self-version** it by snapshotting + content-hashing at ingest.

This kills the "one big ingest pipeline" assumption. The slot needs **two arms**: a thin FRL federation client + a snapshot/version ingest pipeline.

## The source map

| Content class | Examples | Source | Strategy | Point-in-time |
|---|---|---|---|---|
| Primary legislation | Banking Act 1959, Corporations Act 2001, NCCP Act 2009 | legislation.gov.au | **Federate** | Free OData/REST API (`api.prod.legislation.gov.au`), `asAt`/`viewedAt` params, full dated compilation history |
| Legislative instruments | ASIC instruments, AML/CTF Rules | legislation.gov.au | **Federate** | Same API — authoritative versioned text |
| APRA prudential standards / PPGs | APS 110, CPS 230 | apra.gov.au | **Build + self-version** | No API/feed; history scattered across handbook `-superseded` pages + separate determinations → snapshot + hash |
| ASIC regulatory guides | RG 271, RG 36, RG 244 | asic.gov.au | **Build + self-version** | Current PDF only; prior versions *named* in document history but not hosted |
| AUSTRAC guidance | AML/CTF guidance | austrac.gov.au | **Build + self-version** | Mutable HTML/PDF; only RSS is media-release-only and being retired |

## Per-regulator evidence

**Federal Register of Legislation — FEDERATE (the clean win).** A public "Legislation Public API" (OpenAPI 3.0.1, v1) is live at `api.prod.legislation.gov.au`; a live query returned the Banking Act 1959 (title id `C1959A00006`) as structured JSON. Point-in-time is native: API params `asAt` ("The as at date for the version (yyyy-mm-dd)"), `viewedAt`, and `asAtSpecification` (`Latest`/`AsMade`/`Current`); the Act page shows 89 dated compilations back to assent (1959). This is the authoritative versioned source for primary law *and* for the legislative instruments that ASIC and AUSTRAC make.

**APRA — BUILD-AND-VERSION.** No RSS/API/bulk channel; standards are individual HTML/PDF pages. The "official version" lives on legislation.gov.au but APRA issues each revision as a *new separate determination* rather than a compiled series, so a given instrument can show "0" compiled versions — point-in-time requires hunting predecessor instruments. The digital handbook archives superseded editions at `-superseded` URLs with in-force date ranges, but there is no as-at-date selector. Reproducible point-in-time retrieval requires self-storing each edition's text + in-force range + predecessor/successor IDs at ingest. The sitemap and legislation.gov.au email alerts can drive change-detection.

**ASIC — SPLIT.** Legislative instruments → federate (they live on the FRL with dated point-in-time compilations). Regulatory guides / information sheets → build-and-version: asic.gov.au publishes only the current PDF; each RG's "Document history" *names* superseded versions by date (e.g. RG 271 names a July 2020 predecessor) but does not host the files. Snapshot each `published-<date>` PDF and hash it.

**AUSTRAC — SPLIT.** The AML/CTF Rules are a legislative instrument with full point-in-time versioning on the FRL (`F2025L01026`, current compilation `F2026C00274`) — federate. AUSTRAC's own guidance ships only as mutable HTML/PDF with no machine-readable feed (the single RSS channel is media-release-only and explicitly being retired) and no version history — build-and-version, seeded from the sitemap URL list.

## What this means for the build

- The **vertical slice (S1)** should exercise *both arms* so the hard part is proven early: e.g. a handful of APRA standards (APS 110, CPS 230) ingested + self-versioned, plus the Banking Act 1959 federated live via the FRL API. If point-in-time retrieval works across both arms against the gold set, the slot is proven.
- The **chunk/provenance metadata** (per [07-recommendation.md](garden/specimen/2026-05-05-topical-mcp-silo-slot/research/07-recommendation.md)) must carry `instrument_id, section, version/effective_date, source_url, retrieved_at` — non-negotiable for a regulated domain, and the FRL API supplies the first four directly for federated content.
- Change-detection feeds: APRA sitemap + FRL alerts (built arm); FRL API polling (federated arm).

## Caveat to carry to production

The FRL API is published with Swagger but I found **no official developer-portal page documenting rate limits, licensing, or stability/SLA guarantees** — and the ALRC's published DataHub was built by scraping the register, which suggests the API may be under-documented or recently introduced. **Confirm terms-of-use and SLA with the Office of Parliamentary Counsel before depending on it in production (S3).** Non-blocking for S1/S2 read use.

## Sources

- [Legislation Public API — Swagger UI](https://api.prod.legislation.gov.au/swagger/index.html) (live, 2026-06-01)
- [Banking Act 1959 — versions](https://www.legislation.gov.au/C1959A00006/latest/versions) (89 dated compilations, 2026-06-01)
- [APRA ADI prudential standards](https://www.apra.gov.au/industries/1/standards) (2026-06-01)
- [APRA handbook — APS 110](https://handbook.apra.gov.au/standard/aps-110) (2026-06-01)
- [ASIC regulatory guides index](https://www.asic.gov.au/regulatory-resources/find-a-document/regulatory-guides/) (2026-06-01)
- [ASIC RG 271 — Internal Dispute Resolution](https://www.asic.gov.au/regulatory-resources/find-a-document/regulatory-guides/rg-271-internal-dispute-resolution/) (2026-06-01)
- [AUSTRAC — AML/CTF Rules](https://www.austrac.gov.au/about-us/legislation/amlctf-rules) (2026-06-01)
- [AML/CTF Rules on FRL — F2025L01026](https://www.legislation.gov.au/F2025L01026/latest/text) (2026-06-01)
