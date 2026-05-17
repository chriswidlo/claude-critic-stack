#!/bin/bash
# subagent-stop.sh — silently appends an agent_end event with usage data when an Agent invocation returns.
# This is the deterministic capture point for per-subagent duration + tokens — no transcript re-parsing needed.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
AGENT_ID=$(echo "$PAYLOAD" | jq -r '.agent_id // ""' 2>/dev/null)
AGENT_TYPE=$(echo "$PAYLOAD" | jq -r '.agent_type // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
TS_NS=$(date +%s%N 2>/dev/null)
case "$TS_NS" in
    *N) TS_NS=$(($(date +%s) * 1000000000)) ;;
esac
# Pass through any usage fields Claude Code includes in the SubagentStop payload.
# Field names align with OpenTelemetry gen_ai semantic conventions.
USAGE_JSON=$(echo "$PAYLOAD" | jq -c '{
    "gen_ai.usage.input_tokens": (.usage.input_tokens // 0),
    "gen_ai.usage.output_tokens": (.usage.output_tokens // 0),
    "gen_ai.usage.cache_read.input_tokens": (.usage.cache_read_input_tokens // 0),
    "gen_ai.usage.cache_creation.input_tokens": (.usage.cache_creation_input_tokens // 0),
    "duration_ms": (.duration_ms // null),
    "tool_uses_count": (.tool_uses // null)
}' 2>/dev/null)
[ -z "$USAGE_JSON" ] && USAGE_JSON="{}"
printf '{"ts_ns":%s,"event":"agent_end","gen_ai.operation.name":"invoke_agent","gen_ai.agent.id":"%s","gen_ai.agent.name":"%s","_usage":%s}\n' \
    "$TS_NS" "$AGENT_ID" "$AGENT_TYPE" "$USAGE_JSON" >> "$DIR/events.jsonl" 2>/dev/null
exit 0
