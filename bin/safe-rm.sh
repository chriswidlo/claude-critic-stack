#!/usr/bin/env bash
# safe-rm.sh — refuse to delete anything outside this git repository.
#
# Reasoning: deletes inside the repo working tree are reversible via git
# (the file lives in HEAD or in a recent commit; checkout brings it back).
# Deletes outside the repo are not. This script is the only authorized
# destructive path for the agent — see .claude/settings.json: direct rm
# is denied, this wrapper is allowed.
#
# Usage: bin/safe-rm.sh <path> [<path>...]

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <path> [<path>...]" >&2
  exit 2
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"

for target in "$@"; do
  if [[ ! -e "$target" && ! -L "$target" ]]; then
    echo "safe-rm: refusing nonexistent path: $target" >&2
    exit 1
  fi

  if [[ -d "$target" ]]; then
    abs="$(cd "$target" && pwd -P)"
  else
    abs="$(cd "$(dirname "$target")" && pwd -P)/$(basename "$target")"
  fi

  case "$abs" in
    "$REPO_ROOT"/*) ;;
    *)
      echo "safe-rm: refusing path outside repo root ($REPO_ROOT): $abs" >&2
      exit 1
      ;;
  esac

  if [[ "$abs" == "$REPO_ROOT" ]]; then
    echo "safe-rm: refusing to delete the repo root itself" >&2
    exit 1
  fi

  case "$abs" in
    "$REPO_ROOT/.git"|"$REPO_ROOT/.git"/*)
      echo "safe-rm: refusing to delete inside .git/: $abs" >&2
      exit 1
      ;;
  esac

  rm -rf "$abs"
  echo "safe-rm: deleted $abs"
done
