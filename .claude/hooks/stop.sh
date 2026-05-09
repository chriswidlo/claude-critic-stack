#!/bin/bash
# stop.sh — silently stamps end time, resolves workflow ID, moves staging into the
# workflow-session diagnostics dir, triggers the metrics parser as a backgrounded process.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
STAGING="$PROJ_DIR/.claude/.metrics/staging/$SID"

# Stamp end time
date +%s > "$STAGING/end.ts" 2>/dev/null

# Resolve workflow id (written by orchestrator at step 1)
WORKFLOW_ID=$(cat "$STAGING/workflow-id.txt" 2>/dev/null | head -1 | tr -d '[:space:]')

if [ -n "$WORKFLOW_ID" ]; then
    # Move staging contents into the workflow-session diagnostics dir
    DEST="$PROJ_DIR/.claude/session-artifacts/$WORKFLOW_ID/diagnostics"
    mkdir -p "$DEST" 2>/dev/null
    cp -p "$STAGING/start.ts" "$DEST/" 2>/dev/null
    cp -p "$STAGING/end.ts" "$DEST/" 2>/dev/null
    cp -p "$STAGING/events.jsonl" "$DEST/" 2>/dev/null
    rm -rf "$STAGING" 2>/dev/null
    # Trigger parser to compute metrics.json (backgrounded, fully detached)
    if [ -x "$PROJ_DIR/bin/parse-session-metrics.py" ]; then
        nohup python3 "$PROJ_DIR/bin/parse-session-metrics.py" "$WORKFLOW_ID" "$SID" >/dev/null 2>&1 &
    fi
else
    # No workflow id — archive to orphan dir (no loss, no pollution of session-artifacts)
    ORPHAN="$PROJ_DIR/.claude/.metrics/orphan/$SID"
    mkdir -p "$(dirname "$ORPHAN")" 2>/dev/null
    mv "$STAGING" "$ORPHAN" 2>/dev/null
fi
exit 0
