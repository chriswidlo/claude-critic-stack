#!/bin/bash
# pre-tool-use.sh — silently appends a tool-start event to the staging events.jsonl.
# Pairs with post-tool-use.sh; the parser computes per-tool latency from the pair.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
TOOL=$(echo "$PAYLOAD" | jq -r '.tool_name // "unknown"' 2>/dev/null)
TOOL_USE_ID=$(echo "$PAYLOAD" | jq -r '.tool_use_id // ""' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
# Nanosecond-precision timestamp (BSD date doesn't support %N; fall back to seconds)
TS_NS=$(date +%s%N 2>/dev/null)
case "$TS_NS" in
    *N) TS_NS=$(($(date +%s) * 1000000000)) ;;
esac
printf '{"ts_ns":%s,"event":"tool_start","gen_ai.tool.name":"%s","gen_ai.tool.call.id":"%s"}\n' \
    "$TS_NS" "$TOOL" "$TOOL_USE_ID" >> "$DIR/events.jsonl" 2>/dev/null
exit 0
