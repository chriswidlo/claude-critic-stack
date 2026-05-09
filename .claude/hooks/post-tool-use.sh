#!/bin/bash
# post-tool-use.sh — silently appends a tool-use event to the staging events.jsonl.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
TOOL=$(echo "$PAYLOAD" | jq -r '.tool_name // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
TS=$(date +%s)
printf '{"ts":%d,"tool":"%s"}\n' "$TS" "$TOOL" >> "$DIR/events.jsonl" 2>/dev/null
exit 0
