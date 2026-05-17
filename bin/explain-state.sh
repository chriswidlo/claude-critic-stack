#!/usr/bin/env bash
# Emits live state for the /explain markdown card as KEY=value lines.
# Invoked by .claude/skills/explain/SKILL.md
# Output is short (~10 lines) so Claude Code does not fold it.

set -u

ROOT="."

SESSIONS=$(ls -1 "$ROOT/.claude/session-artifacts/" 2>/dev/null | grep -Ev '^(README|exemplars)' | wc -l | tr -d ' ')
EXEMPLARS=$(ls -1 "$ROOT/.claude/session-artifacts/exemplars/" 2>/dev/null | grep -v '^README' | wc -l | tr -d ' ')
LAST_DATE=$(ls -1t "$ROOT/.claude/session-artifacts/" 2>/dev/null | grep -Ev '^(README|exemplars)' | head -1 | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || echo '—')
CANON_TOTAL=$(ls -1 "$ROOT/canon/corpus/" 2>/dev/null | wc -l | tr -d ' ')
NB=$(ls -1d "$ROOT/upgrades/no-brainer/"*/ 2>/dev/null | wc -l | tr -d ' ')
NM=$(ls -1d "$ROOT/upgrades/normal/"*/ 2>/dev/null | wc -l | tr -d ' ')
PR=$(ls -1d "$ROOT/upgrades/profound/"*/ 2>/dev/null | wc -l | tr -d ' ')
OL=$(ls -1d "$ROOT/upgrades/outlandish/"*/ 2>/dev/null | wc -l | tr -d ' ')
UP_TOTAL=$((NB + NM + PR + OL))

FULL_REVIEW_AVG=$(python3 - "$ROOT" <<'PYEOF' 2>/dev/null
import json, os, glob, sys
root = sys.argv[1] if len(sys.argv) > 1 else '.'
durations = []
for path in glob.glob(os.path.join(root, '.claude/session-artifacts/*/diagnostics/metrics.json')):
    try:
        d = json.load(open(path))
        ds = d.get('duration_seconds')
        if isinstance(ds, int) and ds > 0: durations.append(ds)
    except Exception: pass
print(f'~{sum(durations)//len(durations)//60} min' if len(durations) >= 3 else '~10 min')
PYEOF
)
FULL_REVIEW_AVG="${FULL_REVIEW_AVG:-~10 min}"

printf 'SESSIONS=%s\nEXEMPLARS=%s\nLAST_DATE=%s\nCANON_TOTAL=%s\nNB=%s\nNM=%s\nPR=%s\nOL=%s\nUP_TOTAL=%s\nFULL_REVIEW_AVG=%s\n' \
    "$SESSIONS" "$EXEMPLARS" "$LAST_DATE" "$CANON_TOTAL" "$NB" "$NM" "$PR" "$OL" "$UP_TOTAL" "$FULL_REVIEW_AVG"
