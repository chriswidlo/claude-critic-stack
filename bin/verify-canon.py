#!/usr/bin/env python3
# bin/verify-canon.py
#
# Walks canon/corpus/ and verifies the integrity invariant that motivated
# garden/volunteer/2026-05-05-canon-body-bytes-missing.md:
#
#   For every entry whose citation.yaml claims body_completeness in
#   {full, toc_plus_chapters}, a non-empty source.txt MUST exist on disk
#   and its sha256 MUST match the recorded value.
#
# Exits non-zero on any drift. Designed to be wired into pre-commit or CI.
#
# Usage:
#   python3 ./bin/verify-canon.py            # check all entries; print one line per drift
#   python3 ./bin/verify-canon.py --quiet    # print only on failure (silent on success)
#
# Note: canon/corpus/*/source.txt is gitignored, so a freshly-cloned worktree
# reports every entry as missing until `python3 ./bin/ingest-canon.py` has been
# run. That state is indistinguishable from "ingester silently failed to write"
# — both are recoverable by running the ingester. Run the verifier AFTER an
# ingest pass to detect the real silent-failure mode.
#
# Not checked here (out of scope; would require parsing canon/sources.yaml):
#   - whether the slug appears in sources.yaml
#   - whether lifecycle/fetch_mode are coherent with the lockfile state
# Those are validated by bin/ingest-canon.py at fetch time.

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "canon" / "corpus"

# body_completeness values that REQUIRE bytes on disk
NEEDS_BODY = {"full", "toc_plus_chapters"}


def parse_citation(text):
    """Minimal extraction: body_completeness + sha256. Mirrors the lockfile shape
    bin/ingest-canon.py emits; not a general YAML parser."""
    out = {}
    m = re.search(r"^body_completeness:\s*(\S+)\s*$", text, flags=re.MULTILINE)
    if m:
        out["body_completeness"] = m.group(1)
    m = re.search(r'^sha256:\s*"([0-9a-f]+)"\s*$', text, flags=re.MULTILINE)
    if m:
        out["sha256"] = m.group(1)
    return out


def main():
    quiet = "--quiet" in sys.argv[1:]
    if not CORPUS.exists():
        print("canon/corpus/ not found at {}".format(CORPUS), file=sys.stderr)
        sys.exit(2)

    failures = []
    checked = 0

    for slug_dir in sorted(p for p in CORPUS.iterdir() if p.is_dir()):
        slug = slug_dir.name
        cite_path = slug_dir / "citation.yaml"
        if not cite_path.exists():
            # An entry directory without citation.yaml is a different defect; flag it.
            failures.append("{}: missing citation.yaml".format(slug))
            continue
        checked += 1
        cite = parse_citation(cite_path.read_text(encoding="utf-8"))
        completeness = cite.get("body_completeness")
        if completeness not in NEEDS_BODY:
            continue  # stub / abstract_only / fetch_blocked — bytes not required
        source_path = slug_dir / "source.txt"
        if not source_path.exists():
            failures.append(
                "{}: body_completeness={} but source.txt missing".format(slug, completeness)
            )
            continue
        size = source_path.stat().st_size
        if size == 0:
            failures.append(
                "{}: body_completeness={} but source.txt is 0 bytes".format(slug, completeness)
            )
            continue
        recorded = cite.get("sha256")
        if not recorded:
            failures.append("{}: body_completeness={} but no sha256 recorded".format(slug, completeness))
            continue
        actual = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual != recorded:
            failures.append(
                "{}: sha256 drift (recorded {} vs on-disk {})".format(
                    slug, recorded[:16], actual[:16]
                )
            )

    if failures:
        print("canon/corpus verification FAILED ({} drift, {} entries checked):".format(
            len(failures), checked
        ), file=sys.stderr)
        for f in failures:
            print("  {}".format(f), file=sys.stderr)
        sys.exit(1)

    if not quiet:
        print("canon/corpus verification ok ({} entries checked).".format(checked))


if __name__ == "__main__":
    main()
