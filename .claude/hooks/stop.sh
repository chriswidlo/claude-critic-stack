#!/bin/bash
# stop.sh — fires per-turn. Lightweight: just appends a turn-end marker and refreshes end.ts.
# Heavy aggregation moved to session-end.sh (once per session, per Anthropic hooks guidance).
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
TS_NS=$(date +%s%N 2>/dev/null)
case "$TS_NS" in
    *N) TS_NS=$(($(date +%s) * 1000000000)) ;;
esac
printf '{"ts_ns":%s,"event":"turn_end"}\n' "$TS_NS" >> "$DIR/events.jsonl" 2>/dev/null
# Keep end.ts current — if SessionEnd never fires (e.g. user kills Claude Code),
# the last Stop becomes our best end-time estimate.
date +%s > "$DIR/end.ts" 2>/dev/null
exit 0
