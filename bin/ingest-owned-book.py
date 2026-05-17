#!/usr/bin/env python3
# bin/ingest-owned-book.py
#
# Populates a paywalled-book stub at canon/corpus/<slug>/ from a LOCAL plaintext
# file that the user has legitimately obtained (OCR of an owned ebook, plain-text
# export from an O'Reilly / Manning / Pragmatic subscription, etc.).
#
# Usage:
#   python3 ./bin/ingest-owned-book.py <slug> <path-to-text> [--force]
#
# The stub entry (citation.yaml with body_completeness: stub, README.md)
# must already exist at canon/corpus/<slug>/. This script:
#   1. Refuses if source.txt already exists (use --force to overwrite).
#   2. Refuses if <path> is empty or smaller than 10 KB.
#   3. Soft-warns if <path> looks like libgen/sci-hub/z-library to
#      encourage the user to pause; does NOT block.
#   4. Copies the text to canon/corpus/<slug>/source.txt and updates
#      citation.yaml (body_completeness: full, sha256, ingested_at).

import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_BYTES = 10 * 1024


def die(msg, code=1):
    print("error: {}".format(msg), file=sys.stderr)
    sys.exit(code)


def soft_warn(msg):
    print("warning: {}".format(msg), file=sys.stderr)


def _iso_now():
    # Match Node's `new Date().toISOString()` format: YYYY-MM-DDTHH:MM:SS.sssZ
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + "{:03d}Z".format(now.microsecond // 1000)


def _fmt_int(n):
    return "{:,}".format(n)


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    positional = [a for a in argv if not a.startswith("--")]

    if len(positional) < 2:
        die("usage: python3 ./bin/ingest-owned-book.py <slug> <path-to-text> [--force]")
    slug, input_path = positional[0], positional[1]

    slug_dir = ROOT / "canon" / "corpus" / slug
    source_path = slug_dir / "source.txt"
    citation_path = slug_dir / "citation.yaml"

    if not slug_dir.exists():
        die("stub not found: {}\nCreate a stub first (citation.yaml + README.md) or check the slug.".format(slug_dir))
    if not citation_path.exists():
        die("stub missing citation.yaml: {}".format(citation_path))
    if source_path.exists() and not force:
        die("{} already exists; pass --force to overwrite.".format(source_path))

    abs_input = Path(input_path).resolve()
    if not abs_input.exists():
        die("input file not found: {}".format(abs_input))

    size = abs_input.stat().st_size
    if size < MIN_BYTES:
        die(
            "input file is suspiciously small ({} bytes < {}). Refusing to ingest.".format(size, MIN_BYTES)
        )

    lower_path = str(abs_input).lower()
    red = [k for k in ("libgen", "z-library", "zlibrary", "sci-hub", "scihub") if k in lower_path]
    if red:
        soft_warn(
            "input path contains keyword(s) {}. canon/README.md requires text you are licensed to have on your machine. Proceeding — please verify your source is legitimate.".format(
                ", ".join(red)
            )
        )

    data = abs_input.read_bytes()
    text = data.decode("utf-8", errors="replace")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    now = _iso_now()

    # Build a provenance header consistent with bin/ingest-canon.py
    header = "\n".join([
        "---",
        "slug:         {}".format(slug),
        "source_url:   null",
        "ingested_at:  {}".format(now),
        "sha256_short: {}".format(sha[:16]),
        "fetch_mode:   owned-local",
        "license:      owned-book",
        "---",
        "",
    ])

    body = text if text.endswith("\n") else text + "\n"
    source_path.write_text(header + body, encoding="utf-8")

    # Patch citation.yaml: flip body_completeness to full, record sha256 + ingested_at.
    citation = citation_path.read_text(encoding="utf-8")
    citation = re.sub(r"body_completeness:\s*\w+", "body_completeness: full", citation)
    if re.search(r"^sha256:", citation, flags=re.MULTILINE):
        citation = re.sub(r"^sha256:.*$", 'sha256: "{}"'.format(sha), citation, flags=re.MULTILINE)
    else:
        citation += '\nsha256: "{}"\n'.format(sha)
    if re.search(r"^ingested_at:", citation, flags=re.MULTILINE):
        citation = re.sub(r"^ingested_at:.*$", 'ingested_at: "{}"'.format(now), citation, flags=re.MULTILINE)
    else:
        citation += 'ingested_at: "{}"\n'.format(now)
    citation_path.write_text(citation, encoding="utf-8")

    print("ok  {}  ({} bytes, sha {}…)".format(slug, _fmt_int(size), sha[:12]))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(2)
