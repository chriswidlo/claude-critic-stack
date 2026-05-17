#!/usr/bin/env python3
# bin/ingest-canon.py
#
# Populates canon/corpus/<slug>/ from canon/sources.yaml (the single source
# of truth — schema_version 2). Zero dependencies: Python 3.9+ stdlib only
# (urllib, hashlib, html, pathlib, json, re).
#
# Usage:
#   python3 ./bin/ingest-canon.py                 # ingest all auto-fetchable entries
#   python3 ./bin/ingest-canon.py --force         # refetch everything
#   python3 ./bin/ingest-canon.py --only=<slug>   # restrict to one slug
#
# Idempotent: skips slugs whose source.txt already exists unless --force.
# Entries with lifecycle: live-only or fetch_mode in {owned-book, pdf-manual, none}
# are skipped automatically (live-only is never snapshotted; owned-book/pdf-manual
# are curator-driven via bin/ingest-owned-book.py).

import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Argv
# ---------------------------------------------------------------------------
def parse_args(argv):
    out = {"force": False, "only": None}
    for a in argv:
        if a == "--force":
            out["force"] = True
        elif a.startswith("--only="):
            out["only"] = a[len("--only="):]
    return out


# ---------------------------------------------------------------------------
# Minimal YAML parser for canon/sources.yaml's restricted schema (v2).
# Handles: `key: value`, list items under `entries:` beginning with `- `,
# flow maps `{a: b, c: d}`, flow sequences `[a, b]`, quoted/unquoted scalars,
# numbers, booleans, comments. Does NOT handle anchors, block scalars,
# deep nesting beyond `entries: -` items.
#
# Top-level scalars (schema_version, etc.) above `entries:` are ignored —
# the parser only emits the list. If schema_version != 2, the caller fails.
# ---------------------------------------------------------------------------
def parse_sources_yaml(text):
    lines = text.split("\n")
    entries = []
    current = None
    in_entries = False
    schema_version = None

    for raw in lines:
        # strip whole-line comments
        if re.match(r"^\s*#", raw):
            continue
        # strip trailing comment: `  key: value  # note` -> `  key: value`
        raw = re.sub(r"(^|\s)#.*$", r"\1", raw).rstrip()
        if not raw.strip():
            continue

        # Capture schema_version at the top level (before entries:)
        if not in_entries:
            sv = re.match(r"^schema_version:\s*(\d+)", raw)
            if sv:
                schema_version = int(sv.group(1))
                continue

        if re.match(r"^entries:\s*$", raw):
            in_entries = True
            continue
        if not in_entries:
            continue

        # Block-sequence item: starts with `  - key: value`
        item = re.match(r"^(\s*)-\s+(.+)$", raw)
        if item:
            if current is not None:
                entries.append(current)
            current = {}
            kv = _parse_kv(item.group(2))
            if kv:
                current.update(kv)
            continue
        # Continuation field of current entry: `    key: value`
        kvm = re.match(r"^(\s+)(\w+):\s*(.*)$", raw)
        if kvm and current is not None:
            key = kvm.group(2)
            val = _parse_value(kvm.group(3))
            current[key] = val

    if current is not None:
        entries.append(current)
    return {"schema_version": schema_version, "entries": entries}


def _parse_kv(fragment):
    m = re.match(r"^(\w+):\s*(.*)$", fragment)
    if not m:
        return None
    return {m.group(1): _parse_value(m.group(2))}


def _parse_value(raw_in):
    raw = "" if raw_in is None else str(raw_in).strip()
    if not raw:
        return None
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    if raw.startswith("{") and raw.endswith("}"):
        inner = raw[1:-1]
        obj = {}
        for p in _split_top_level(inner, ","):
            idx = p.find(":")
            if idx == -1:
                continue
            k = p[:idx].strip().strip('"').strip("'")
            obj[k] = _parse_value(p[idx + 1:])
        return obj
    if raw.startswith("[") and raw.endswith("]"):
        parts = [_parse_value(p) for p in _split_top_level(raw[1:-1], ",")]
        return [v for v in parts if v is not None]
    if re.match(r"^-?\d+(\.\d+)?$", raw):
        if "." in raw:
            return float(raw)
        return int(raw)
    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw in ("null", "~"):
        return None
    return raw


def _split_top_level(s, delim):
    out = []
    depth = 0
    in_str = None
    buf = []
    for ch in s:
        if in_str:
            if ch == in_str:
                in_str = None
            buf.append(ch)
        elif ch in ('"', "'"):
            in_str = ch
            buf.append(ch)
        elif ch in ("[", "{"):
            depth += 1
            buf.append(ch)
        elif ch in ("]", "}"):
            depth -= 1
            buf.append(ch)
        elif ch == delim and depth == 0:
            piece = "".join(buf)
            if piece.strip():
                out.append(piece)
            buf = []
        else:
            buf.append(ch)
    piece = "".join(buf)
    if piece.strip():
        out.append(piece)
    return out


# ---------------------------------------------------------------------------
# HTML → plain text. Regex-based; handles the common subset we need.
# ---------------------------------------------------------------------------
_NAMED_ENTITIES = {
    "amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'", "nbsp": " ",
    "ldquo": '"', "rdquo": '"', "lsquo": "‘", "rsquo": "’",
    "mdash": "—", "ndash": "–", "hellip": "…",
    "copy": "©", "trade": "™",
}


def decode_entities(s):
    s = str(s)

    def _num(m):
        return chr(int(m.group(1)))

    def _hex(m):
        return chr(int(m.group(1), 16))

    def _named(m):
        name = m.group(1).lower()
        return _NAMED_ENTITIES.get(name, m.group(0))

    s = re.sub(r"&#(\d+);", _num, s)
    s = re.sub(r"&#x([0-9a-f]+);", _hex, s, flags=re.IGNORECASE)
    s = re.sub(r"&([a-z]+);", _named, s, flags=re.IGNORECASE)
    # drop any remaining unknown named entities
    s = re.sub(r"&[a-z0-9]+;", "", s, flags=re.IGNORECASE)
    return s


def strip_inline(html):
    return decode_entities(re.sub(r"<[^>]+>", "", str(html)))


def strip_html(html):
    if not html:
        return ""
    # Remove full blocks we don't want (script/style/nav/footer/aside/header/head/noscript).
    # NOTE: `<form>` is intentionally NOT in this list — ASP.NET WebForms and other
    # legacy CMSes wrap the entire page body in a single <form>, so dropping form
    # blocks deletes all content. We instead strip form open/close tags below and
    # keep their children, which is the right behavior for content extraction.
    html = re.sub(
        r"<(script|style|nav|footer|aside|header|head|noscript)\b[^>]*>[\s\S]*?</\1>",
        "",
        html,
        flags=re.IGNORECASE,
    )
    # Remove HTML comments
    html = re.sub(r"<!--[\s\S]*?-->", "", html)

    # Headings
    def _heading(m):
        lvl = int(m.group(1))
        txt = strip_inline(m.group(2)).strip()
        return "\n\n{} {}\n\n".format("#" * lvl, txt)

    html = re.sub(r"<h([1-6])[^>]*>([\s\S]*?)</h\1>", _heading, html, flags=re.IGNORECASE)
    # Block elements → newlines
    html = re.sub(r"</(p|div|li|tr|blockquote|pre|section|article)>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<(p|div|li|tr|blockquote|pre|section|article)[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    # Strip remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Decode entities
    html = decode_entities(html)
    # Collapse whitespace
    html = re.sub(r"[ \t]+", " ", html)
    html = "\n".join(line.strip() for line in html.split("\n"))
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
UA = "Mozilla/5.0 (compatible; canon-ingest/1.0; +claude-critic-stack)"


def http_get(url, retries=2):
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                },
            )
            with urllib.request.urlopen(req) as res:
                charset = res.headers.get_content_charset() or "utf-8"
                data = res.read()
                try:
                    return data.decode(charset, errors="replace")
                except LookupError:
                    return data.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last_err = Exception("HTTP {} {} from {}".format(e.code, e.reason, url))
        except urllib.error.URLError as e:
            last_err = Exception("URL error {} from {}".format(e.reason, url))
        except Exception as e:
            last_err = e
        if attempt < retries:
            time.sleep(0.5 * (attempt + 1))
    raise last_err


# ---------------------------------------------------------------------------
# Fetch modes
# ---------------------------------------------------------------------------
# Cap on how many child chapters html-multi / aws-docs will follow from a TOC.
# Prevents runaway ingestion if a TOC links to every page on a large doc site.
# 100 covers AWS SaaS Lens (~50 sections) fully; SRE Book will be capped at 100.
# Raise per-source in sources.yaml (future: add per-entry `max_chapters` field).
HTML_MULTI_MAX_CHAPTERS = 100
NAV_NOISE = re.compile(
    r"^(home|back|next|previous|search|menu|contents|index|about|contact|help|subscribe|login|sign\s*up)$",
    re.IGNORECASE,
)


def fetch_and_extract(src):
    fm = src.get("fetch_mode")
    if fm == "html":
        return strip_html(http_get(src["source_url"]))
    if fm == "html-multi":
        return fetch_html_multi(src)
    if fm == "arxiv-abs":
        return fetch_arxiv_abs(src)
    if fm == "aws-docs":
        return fetch_aws_docs(src)
    if fm == "pdf-manual":
        # Explicit signal: source is a PDF and must be ingested via
        # bin/ingest-owned-book.py after local pdftotext conversion.
        raise Exception(
            "pdf-manual: this source is a PDF; convert with pdftotext and run bin/ingest-owned-book.py. Not fetched automatically."
        )
    if fm == "owned-book":
        # Curator owns the book; ingest via bin/ingest-owned-book.py <slug> <text-path>.
        raise Exception(
            "owned-book: run bin/ingest-owned-book.py <slug> <text-path>. Not fetched automatically."
        )
    if fm == "none":
        # lifecycle: live-only — should have been filtered out before this function.
        raise Exception("fetch_mode=none should be filtered before fetch_and_extract (live-only lifecycle)")
    raise Exception("unknown fetch_mode: {}".format(fm))


# AWS docs: TOC is a JSON file (toc-contents.json) listing href to each chapter.
# URL should point directly at the JSON endpoint; we walk recursively through `contents`.
def fetch_aws_docs(src):
    toc_raw = http_get(src["source_url"])
    toc = json.loads(toc_raw)
    parsed = urllib.parse.urlparse(src["source_url"])
    base_path = re.sub(r"[^/]+/?$", "", parsed.path)
    base = "{}://{}{}".format(parsed.scheme, parsed.netloc, base_path)

    flat = []

    def walk(items):
        if not isinstance(items, list):
            return
        for it in items:
            if isinstance(it, dict) and it.get("href"):
                flat.append({"title": it.get("title", ""), "href": it["href"]})
            if isinstance(it, dict) and isinstance(it.get("contents"), list):
                walk(it["contents"])

    walk(toc.get("contents", []))

    if not flat:
        raise Exception("aws-docs: no entries found in {}".format(src["source_url"]))

    limited = flat[:HTML_MULTI_MAX_CHAPTERS]
    parts = ["AWS documentation — {} sections (ingesting first {})".format(len(flat), len(limited))]
    for ch in limited:
        ch_url = urllib.parse.urljoin(base, ch["href"])
        try:
            body = http_get(ch_url)
            parts.append("\n\n=== {} ===\n{}\n\n{}".format(ch["title"], ch_url, strip_html(body)))
        except Exception as e:
            parts.append("\n\n=== {} ===\n{}\n\n[FETCH ERROR: {}]".format(ch["title"], ch_url, e))
    return "".join(parts)


_LINK_RE = re.compile(r"""<a[^>]+href=["']([^"']+)["'][^>]*>([\s\S]*?)</a>""", re.IGNORECASE)


def fetch_html_multi(src):
    toc_html = http_get(src["source_url"])
    parsed = urllib.parse.urlparse(src["source_url"])
    # Strip the last path segment (with or without trailing slash):
    #   /a/b/c/      → /a/b/
    #   /a/b/c.html  → /a/b/
    base_path = re.sub(r"[^/]+/?$", "", parsed.path)
    base = "{}://{}{}".format(parsed.scheme, parsed.netloc, base_path)

    seen = set()
    chapters = []
    for m in _LINK_RE.finditer(toc_html):
        href, inner = m.group(1), m.group(2)
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
            continue
        try:
            abs_url = urllib.parse.urljoin(src["source_url"], href)
        except Exception:
            continue
        # strip query/fragment for dedup
        abs_url = re.sub(r"[#?].*$", "", abs_url)
        if not abs_url.startswith(base):
            continue
        if abs_url == src["source_url"] or abs_url == src["source_url"] + "/":
            continue
        if abs_url in seen:
            continue
        title = re.sub(r"\s+", " ", strip_inline(inner).strip())
        if not title or NAV_NOISE.match(title) or len(title) < 3:
            continue
        seen.add(abs_url)
        chapters.append({"url": abs_url, "title": title})
        if len(chapters) >= HTML_MULTI_MAX_CHAPTERS:
            break

    if not chapters:
        # Fall back to just the TOC page
        return strip_html(toc_html)

    parts = []
    parts.append(strip_html(toc_html))
    parts.append("\n\n=== TABLE OF CONTENTS END ===\n")

    for ch in chapters:
        try:
            body = http_get(ch["url"])
            parts.append("\n\n=== {} ===\n{}\n\n{}".format(ch["title"], ch["url"], strip_html(body)))
        except Exception as e:
            parts.append("\n\n=== {} ===\n{}\n\n[FETCH ERROR: {}]".format(ch["title"], ch["url"], e))
    return "".join(parts)


def fetch_arxiv_abs(src):
    # Normalize URL to /abs/ form
    abs_url = src["source_url"].replace("/html/", "/abs/").replace("/pdf/", "/abs/")
    abs_url = re.sub(r"v\d+(/|$)", r"\1", abs_url)
    abs_url = re.sub(r"\.pdf$", "", abs_url)
    html = http_get(abs_url)

    def pick_meta(name):
        pattern = r"""<meta[^>]+name=["']""" + re.escape(name) + r"""["'][^>]+content=["']([^"']+)["']"""
        m = re.search(pattern, html, flags=re.IGNORECASE)
        return m.group(1) if m else None

    title = pick_meta("citation_title") or pick_meta("og:title") or ""
    date = pick_meta("citation_date") or pick_meta("citation_online_date") or ""
    authors = [
        m.group(1)
        for m in re.finditer(
            r"""<meta[^>]+name=["']citation_author["'][^>]+content=["']([^"']+)["']""",
            html,
            flags=re.IGNORECASE,
        )
    ]

    abs_block = re.search(
        r"""<blockquote[^>]*class=["'][^"']*abstract[^"']*["'][^>]*>([\s\S]*?)</blockquote>""",
        html,
        flags=re.IGNORECASE,
    )
    abstract = strip_html(abs_block.group(1)) if abs_block else strip_html(html)[:3000]
    abstract = re.sub(r"^Abstract:?\s*", "", abstract, flags=re.IGNORECASE).strip()

    subj_block = re.search(
        r"""<td[^>]*class=["'][^"']*tablesubjects[^"']*["'][^>]*>([\s\S]*?)</td>""",
        html,
        flags=re.IGNORECASE,
    )
    subject = strip_html(subj_block.group(1)).strip() if subj_block else ""

    # Guard against 404-as-200 and other soft-fail responses. A hallucinated or
    # dead arXiv ID can return HTML that superficially looks like an abstract
    # page but has no citation metadata. Without this check, bin/ingest-canon.py
    # writes a clean-looking source.txt + citation.yaml with a real sha256 over
    # a fake body — silent correctness failure. See Phase-2 plan C1/C2.
    if not title or len(title) < 5:
        raise Exception("arxiv-abs: title missing or <5 chars at {} (likely 404-as-200 or dead ID)".format(abs_url))
    if not abstract or len(abstract) < 200:
        raise Exception("arxiv-abs: abstract missing or <200 chars at {} (likely placeholder page)".format(abs_url))

    lines = [
        "Title: {}".format(title),
        "",
        "Authors: {}".format(", ".join(authors)),
        "",
        "Submitted: {}".format(date),
        "",
        "Subject: {}".format(subject) if subject else "",
        "",
        "Source: {}".format(abs_url),
        "",
        "Abstract",
        "--------",
        "",
        abstract,
    ]
    return "\n".join(l for l in lines if l is not None)


# ---------------------------------------------------------------------------
# Emitters — source.txt provenance header, citation.yaml, README.md
# ---------------------------------------------------------------------------
def _iso_now():
    # Match Node's `new Date().toISOString()` format: YYYY-MM-DDTHH:MM:SS.sssZ
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + "{:03d}Z".format(now.microsecond // 1000)


def sha256_short(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def provenance_header(src, body):
    return "\n".join([
        "---",
        "slug:         {}".format(src["slug"]),
        "source_url:   {}".format(src["source_url"]),
        "fetched_at:   {}".format(_iso_now()),
        "sha256_short: {}".format(sha256_short(body)),
        "fetch_mode:   {}".format(src["fetch_mode"]),
        "license:      {}".format(src["license"]),
        "---",
        "",
    ])


def completeness_for(fetch_mode, source_path):
    """Decide body_completeness; refuse to claim 'full' unless source.txt is on disk.

    Belt-and-suspenders against the silent-failure mode documented in
    garden/volunteer/2026-05-05-canon-body-bytes-missing.md: a previous ingester
    wrote citation.yaml with body_completeness=full while no body file ever
    landed, leaving the librarian honoring its no-paraphrase rule against an
    empty corpus and silently returning nothing. The gate here enforces the
    invariant *in code*: the 'full' claim requires the bytes on disk.
    """
    if fetch_mode == "arxiv-abs":
        return "abstract_only"
    if fetch_mode == "html-multi":
        return "toc_plus_chapters"
    # html, aws-docs, owned-book, pdf-manual → 'full' must be backed by bytes
    if not source_path.exists():
        raise Exception(
            "body_completeness=full refused: source.txt missing at {}. "
            "fetch_mode={} requires bytes on disk before lockfile can claim full.".format(
                source_path, fetch_mode
            )
        )
    size = source_path.stat().st_size
    if size == 0:
        raise Exception(
            "body_completeness=full refused: source.txt at {} is zero bytes. "
            "Fetch returned empty content; refusing to record full completeness over nothing.".format(
                source_path
            )
        )
    return "full"


def build_citation_yaml(src, source_text, source_path):
    sha = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    # Cross-check: the bytes we're hashing must match the bytes on disk. If
    # they diverge, the write was partial or the file was tampered with between
    # write and citation generation — fail loudly rather than record a lie.
    on_disk = source_path.read_bytes()
    on_disk_sha = hashlib.sha256(on_disk).hexdigest()
    if on_disk_sha != sha:
        raise Exception(
            "sha256 drift: in-memory body hashes to {} but on-disk {} hashes to {}. "
            "Refusing to write citation.yaml with a sha that does not match the file.".format(
                sha[:16], source_path, on_disk_sha[:16]
            )
        )
    completeness = completeness_for(src["fetch_mode"], source_path)
    notes_line = ""
    if src.get("notes"):
        notes_line = "  " + str(src["notes"]).replace("\n", "\n  ")
    lines = [
        "# Generated by bin/ingest-canon.py. Do not hand-edit — run the ingester.",
        "# Schema (lockfile) documented in canon/README.md §\"citation.yaml schema\".",
        "slug: {}".format(src["slug"]),
        'fetched_at: "{}"'.format(_iso_now()),
        'sha256: "{}"'.format(sha),
        "body_completeness: {}".format(completeness),
        "chapter_offsets: []",
        "stale: false",
        "fetch_notes: |",
        "  Fetched by bin/ingest-canon.py ({} mode).".format(src["fetch_mode"]),
        notes_line,
        "",
    ]
    return "\n".join(l for l in lines if l != "") + "\n"


def build_readme(src):
    return "\n".join([
        "# {}".format(src["slug"]),
        "",
        "**Author:** {}".format(src.get("author") or ""),
        "**Title:** {}".format(src.get("title") or ""),
        "**Year:** {}".format(src.get("year") if src.get("year") is not None else ""),
        "**Source:** {}".format(src["source_url"]),
        "**License:** {}".format(src["license"]),
        "**Lifecycle:** {}".format(src["lifecycle"]),
        "**Volatility:** {}".format(src["volatility"]),
        "**Fetched:** {}".format(_iso_now()[:10]),
        "**Fetch mode:** {}".format(src["fetch_mode"]),
        "",
        "## Provenance",
        "",
        "Fetched by `bin/ingest-canon.py` from the URL above. HTML stripped,",
        "headings preserved as Markdown-style `#` lines. No editorial changes.",
        "",
        "## How to refresh",
        "",
        "```",
        "python3 ./bin/ingest-canon.py --only={} --force".format(src["slug"]),
        "```",
        "",
    ])


# ---------------------------------------------------------------------------
# Schema validation — fail fast on bad entries instead of mid-loop runtime
# errors. A typo like `fech_mode: html` instead of `fetch_mode: html` would
# otherwise throw `unknown fetch_mode: undefined` mid-ingestion after other
# entries had already been written.
#
# Enums must match canon/README.md §"Strict enums". If you add a value here,
# update canon/README.md in the same commit.
# ---------------------------------------------------------------------------
ALLOWED_FETCH = {"html", "html-multi", "arxiv-abs", "aws-docs", "pdf-manual", "owned-book", "none"}
ALLOWED_LIFECYCLE = {"snapshot-only", "snapshot+refresh", "live-only"}
ALLOWED_VOLATILITY = {"durable", "slow", "fast", "volatile"}
ALLOWED_KIND = {"book", "paper", "essay", "talk", "standard", "docs"}
LAST_VERIFIED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
YEAR_RE = re.compile(r"^\d{4}$")


def validate_sources(entries, schema_version):
    if schema_version != 2:
        raise Exception(
            "canon/sources.yaml: expected schema_version 2, got {}. Migration required.".format(schema_version)
        )
    errors = []
    seen_slugs = set()
    for s in entries:
        slug = s.get("slug") if isinstance(s.get("slug"), str) else "<no-slug>"
        errs = []
        if not isinstance(s.get("slug"), str) or not s.get("slug"):
            errs.append("missing or non-string slug")
        elif s["slug"] in seen_slugs:
            errs.append("duplicate slug: {}".format(s["slug"]))
        else:
            seen_slugs.add(s["slug"])
        if not isinstance(s.get("author"), str) or not s.get("author"):
            errs.append("missing or non-string author")
        if not isinstance(s.get("title"), str) or not s.get("title"):
            errs.append("missing or non-string title")
        if s.get("year") is None:
            errs.append("missing year")
        elif not YEAR_RE.match(str(s["year"])):
            errs.append("year must be 4 digits, got: {}".format(s["year"]))
        if not isinstance(s.get("category"), str) or not s.get("category"):
            errs.append("missing or non-string category")
        if s.get("kind") not in ALLOWED_KIND:
            errs.append("kind must be one of {{{}}}, got: {}".format(", ".join(sorted(ALLOWED_KIND)), s.get("kind")))
        if not isinstance(s.get("topics"), list) or len(s["topics"]) < 1:
            errs.append("topics must be a list with at least 1 entry")
        if not isinstance(s.get("source_url"), str) or not s.get("source_url"):
            errs.append("missing or non-string source_url")
        if not isinstance(s.get("license"), str) or not s.get("license"):
            errs.append("missing or non-string license")
        if s.get("lifecycle") not in ALLOWED_LIFECYCLE:
            errs.append(
                "lifecycle must be one of {{{}}}, got: {}".format(", ".join(sorted(ALLOWED_LIFECYCLE)), s.get("lifecycle"))
            )
        if s.get("volatility") not in ALLOWED_VOLATILITY:
            errs.append(
                "volatility must be one of {{{}}}, got: {}".format(", ".join(sorted(ALLOWED_VOLATILITY)), s.get("volatility"))
            )
        lv = s.get("last_verified")
        if lv is None or not LAST_VERIFIED_RE.match(str(lv)):
            errs.append("last_verified must be YYYY-MM-DD, got: {}".format(lv))
        if s.get("fetch_mode") not in ALLOWED_FETCH:
            errs.append(
                "fetch_mode must be one of {{{}}}, got: {}".format(", ".join(sorted(ALLOWED_FETCH)), s.get("fetch_mode"))
            )
        # Cross-field invariant: live-only must use fetch_mode=none
        if s.get("lifecycle") == "live-only" and s.get("fetch_mode") != "none":
            errs.append("lifecycle=live-only requires fetch_mode=none, got fetch_mode={}".format(s.get("fetch_mode")))
        if s.get("lifecycle") != "live-only" and s.get("fetch_mode") == "none":
            errs.append("fetch_mode=none is only valid when lifecycle=live-only")
        if errs:
            errors.append("  [{}] {}".format(slug, "; ".join(errs)))
    if errors:
        raise Exception("canon/sources.yaml failed validation:\n" + "\n".join(errors))


# Filter: only entries the auto-fetcher can handle.
# Skipped silently: live-only (never snapshotted) and owned-book/pdf-manual
# (curator-driven; use bin/ingest-owned-book.py).
def is_auto_fetchable(src):
    if src.get("lifecycle") == "live-only":
        return False
    if src.get("fetch_mode") in ("owned-book", "pdf-manual", "none"):
        return False
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def _fmt_int(n):
    return "{:,}".format(n)


def main():
    args = parse_args(sys.argv[1:])
    sources_path = ROOT / "canon" / "sources.yaml"
    text = sources_path.read_text(encoding="utf-8")
    parsed = parse_sources_yaml(text)
    schema_version = parsed["schema_version"]
    entries = parsed["entries"]
    validate_sources(entries, schema_version)

    ok = 0
    skipped = 0
    failed = 0
    filtered = 0
    failures = []

    for src in entries:
        if args["only"] and src.get("slug") != args["only"]:
            continue
        if not src.get("slug"):
            print("skip entry without slug: {}".format(json.dumps(src)[:120]), file=sys.stderr)
            continue

        # Skip entries the auto-fetcher does not handle (live-only, owned-book, pdf-manual)
        if not is_auto_fetchable(src):
            if args["only"]:
                print(
                    "skip    {}  (lifecycle={}, fetch_mode={}; not auto-fetchable)".format(
                        src["slug"], src.get("lifecycle"), src.get("fetch_mode")
                    )
                )
            filtered += 1
            continue

        slug_dir = ROOT / "canon" / "corpus" / src["slug"]
        source_path = slug_dir / "source.txt"

        if not args["force"] and source_path.exists():
            print("skip    {}  (already ingested)".format(src["slug"]))
            skipped += 1
            continue

        try:
            slug_dir.mkdir(parents=True, exist_ok=True)
            sys.stdout.write("fetch   {}  ({}) ... ".format(src["slug"], src["fetch_mode"]))
            sys.stdout.flush()
            body = fetch_and_extract(src)
            full = provenance_header(src, body) + body + "\n"
            source_path.write_text(full, encoding="utf-8")
            (slug_dir / "citation.yaml").write_text(build_citation_yaml(src, full, source_path), encoding="utf-8")
            (slug_dir / "README.md").write_text(build_readme(src), encoding="utf-8")
            print("ok ({} chars)".format(_fmt_int(len(full))))
            ok += 1
        except Exception as e:
            print("FAILED")
            print("  ↳ {}".format(e), file=sys.stderr)
            failures.append({"slug": src["slug"], "error": str(e)})
            failed += 1

    print("")
    print(
        "--- {} ok, {} skipped (already present), {} filtered (not auto-fetchable), {} failed ---".format(
            ok, skipped, filtered, failed
        )
    )
    if failures:
        print("")
        for f in failures:
            print("  FAIL {}: {}".format(f["slug"], f["error"]))
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(2)
