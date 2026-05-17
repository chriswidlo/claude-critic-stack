#!/bin/bash
# post-tool-use-failure.sh — silently records tool-call errors.
# Errors are otherwise invisible to events.jsonl. AI-blind.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
TOOL=$(echo "$PAYLOAD" | jq -r '.tool_name // "unknown"' 2>/dev/null)
TOOL_USE_ID=$(echo "$PAYLOAD" | jq -r '.tool_use_id // ""' 2>/dev/null)
ERROR_TYPE=$(echo "$PAYLOAD" | jq -r '.error.type // .error_type // "unknown"' 2>/dev/null)
ERROR_MSG=$(echo "$PAYLOAD" | jq -r '.error.message // .error_message // ""' 2>/dev/null | head -c 200 | tr -d '\n')
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
TS_NS=$(date +%s%N 2>/dev/null)
case "$TS_NS" in
    *N) TS_NS=$(($(date +%s) * 1000000000)) ;;
esac
# Use jq to safely escape the error message for JSON.
ERR_JSON=$(jq -c -n --arg t "$ERROR_TYPE" --arg m "$ERROR_MSG" '{"error.type":$t,"error.message":$m}' 2>/dev/null)
[ -z "$ERR_JSON" ] && ERR_JSON='{"error.type":"unknown","error.message":""}'
printf '{"ts_ns":%s,"event":"tool_error","gen_ai.tool.name":"%s","gen_ai.tool.call.id":"%s","_err":%s}\n' \
    "$TS_NS" "$TOOL" "$TOOL_USE_ID" "$ERR_JSON" >> "$DIR/events.jsonl" 2>/dev/null
exit 0
