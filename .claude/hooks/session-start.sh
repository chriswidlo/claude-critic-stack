#!/bin/bash
# session-start.sh — stamps start time, writes UUID sigil for the orchestrator's binding step
# (session-bootstrap skill 4b), and appends a structured session_start event.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
date +%s > "$DIR/start.ts" 2>/dev/null

# UUID sigil — session-bootstrap reads this to bind workflow-id at step 4b.
mkdir -p "$PROJ_DIR/.claude/.metrics" 2>/dev/null
echo "$SID" > "$PROJ_DIR/.claude/.metrics/current-session-uuid" 2>/dev/null

# Structured session_start event in OpenTelemetry-compatible schema.
TS_NS=$(date +%s%N 2>/dev/null)
case "$TS_NS" in
    *N) TS_NS=$(($(date +%s) * 1000000000)) ;;
esac
printf '{"ts_ns":%s,"event":"session_start","session_id":"%s"}\n' \
    "$TS_NS" "$SID" >> "$DIR/events.jsonl" 2>/dev/null
exit 0
