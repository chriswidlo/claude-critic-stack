#!/bin/bash
# session-start.sh — silently stamps start time to staging dir keyed by Claude session UUID,
# and writes a sigil file the orchestrator reads at step 1 to know which staging dir to point at.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
DIR="$PROJ_DIR/.claude/.metrics/staging/$SID"
mkdir -p "$DIR" 2>/dev/null
date +%s > "$DIR/start.ts" 2>/dev/null
# Sigil for orchestrator: the active Claude session UUID
mkdir -p "$PROJ_DIR/.claude/.metrics" 2>/dev/null
echo "$SID" > "$PROJ_DIR/.claude/.metrics/current-session-uuid" 2>/dev/null
exit 0
