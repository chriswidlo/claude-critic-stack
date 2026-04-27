#!/usr/bin/env bash
# bin/check-path-discipline.sh
#
# Verification-only script for path discipline (non-destructive, read-only).
#
# Authored under cleanup punch-list item 2 (folder-shape depth bug fix).
# Consumed by item 1's plan §Step 6 as the regression check on Option A
# (repo-root-relative discipline). Single source of truth for the verification
# regex, eliminating the protocol-surface drift risk between items 1 and 2.
#
# Modes:
#   --resolve <files...>   Verify every markdown link target in <files> exists
#                          on disk, treating each target as repo-root-relative
#                          (Option A form per CLAUDE.md L7-16). Skips URLs and
#                          pure anchor (#frag) targets. Strips #fragment before
#                          checking existence. Exits 1 if any link is broken.
#
#   --inbound <files...>   List inbound markdown references to <files> from
#                          elsewhere in the repo, excluding .claude/session-artifacts/
#                          (those files are historical record per commit 5108ed3
#                          and must not be modified). Reports anchor references
#                          separately so anchor-stability can be checked manually.
#                          Always exits 0; informational.
#
#   --style <files...>     Flag any markdown link target that uses a ../-chain,
#                          absolute (/-prefix), or home-relative (~/-prefix) form.
#                          Exits 1 if any style violation is found.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

extract_links() {
  awk '
    {
      line = $0
      while (match(line, /\[[^]]*\]\([^)]+\)/)) {
        link = substr(line, RSTART, RLENGTH)
        display = link
        sub(/^\[/, "", display)
        sub(/\].*/, "", display)
        target = link
        sub(/.*\(/, "", target)
        sub(/\)$/, "", target)
        printf "%d\t%s\t%s\n", NR, display, target
        line = substr(line, RSTART + RLENGTH)
      }
    }
  ' "$1"
}

is_skippable_target() {
  case "$1" in
    http://*|https://*|mailto:*|"#"*) return 0 ;;
    *) return 1 ;;
  esac
}

mode_resolve() {
  local broken=0 checked=0
  for f in "$@"; do
    if [ ! -e "$f" ]; then
      echo "ERROR: file not found: $f" >&2
      exit 2
    fi
    while IFS=$'\t' read -r lineno _display target; do
      if is_skippable_target "$target"; then continue; fi
      local path="${target%%#*}"
      if [ -z "$path" ]; then continue; fi
      checked=$((checked + 1))
      if [ ! -e "$REPO_ROOT/$path" ]; then
        echo "BROKEN  $f:$lineno  target=$target"
        broken=$((broken + 1))
      fi
    done < <(extract_links "$f")
  done
  if [ "$broken" -gt 0 ]; then
    echo "FAIL: $broken broken / $checked checked"
    exit 1
  fi
  echo "OK: $checked links, all resolve"
}

mode_inbound() {
  for f in "$@"; do
    if [ ! -e "$f" ]; then
      echo "ERROR: file not found: $f" >&2
      exit 2
    fi
    local abs
    abs="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
    local rel="${abs#"$REPO_ROOT/"}"
    echo "=== Inbound references to $rel ==="
    local hits
    hits=$(grep -rn --include='*.md' \
      --exclude-dir='.claude' \
      --exclude-dir='.git' \
      --exclude-dir='node_modules' \
      -F "$rel" "$REPO_ROOT" 2>/dev/null \
      | grep -v "^${REPO_ROOT}/${rel}:" || true)
    if [ -z "$hits" ]; then
      echo "  (none outside .claude/)"
    else
      echo "$hits"
    fi
    local frag_hits
    frag_hits=$(grep -rn --include='*.md' \
      --exclude-dir='.claude' \
      --exclude-dir='.git' \
      -E "\(${rel}#[A-Za-z0-9_-]+\)" "$REPO_ROOT" 2>/dev/null || true)
    if [ -n "$frag_hits" ]; then
      echo "--- Anchor references (verify anchor stability after rewrite) ---"
      echo "$frag_hits"
    fi
    echo ""
  done
}

mode_style() {
  local violations=0 checked=0
  for f in "$@"; do
    if [ ! -e "$f" ]; then
      echo "ERROR: file not found: $f" >&2
      exit 2
    fi
    while IFS=$'\t' read -r lineno _display target; do
      if is_skippable_target "$target"; then continue; fi
      checked=$((checked + 1))
      case "$target" in
        ../*|/*|"~/"*)
          echo "STYLE   $f:$lineno  target=$target"
          violations=$((violations + 1))
          ;;
      esac
    done < <(extract_links "$f")
  done
  if [ "$violations" -gt 0 ]; then
    echo "FAIL: $violations style violation(s) / $checked checked"
    exit 1
  fi
  echo "OK: $checked links, no style violations"
}

usage() {
  cat <<'EOF'
Usage: bin/check-path-discipline.sh <mode> <files...>

Modes:
  --resolve  Verify every link target exists (repo-root-relative interpretation)
  --inbound  List inbound markdown references to the given files (excl. .claude/)
  --style    Flag ../-chain, absolute, or ~/-prefixed link targets

Exit codes: 0 OK, 1 violations found, 2 usage / file-not-found.
EOF
  exit 2
}

if [ $# -lt 2 ]; then usage; fi

case "$1" in
  --resolve) shift; mode_resolve "$@" ;;
  --inbound) shift; mode_inbound "$@" ;;
  --style)   shift; mode_style "$@" ;;
  -h|--help) usage ;;
  *) usage ;;
esac
