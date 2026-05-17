#!/bin/bash
# session-end.sh — canonical once-per-session aggregation hook.
# Stamps end time, resolves workflow-id, moves staging to session diagnostics dir,
# runs the parser (synchronous now — single invocation per session, not per turn),
# renders the HTML report, optionally triggers cross-session aggregation.
# AI-blind: stdout/stderr suppressed; the workflow does not see this.
set +e
PAYLOAD=$(cat 2>/dev/null)
SID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"' 2>/dev/null)
PROJ_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
STAGING="$PROJ_DIR/.claude/.metrics/staging/$SID"

# Stamp end time (idempotent — Stop hook may have written this earlier)
date +%s > "$STAGING/end.ts" 2>/dev/null

# Resolve workflow id (written by orchestrator via session-bootstrap step 4b)
WORKFLOW_ID=$(cat "$STAGING/workflow-id.txt" 2>/dev/null | head -1 | tr -d '[:space:]')

if [ -n "$WORKFLOW_ID" ]; then
    DEST="$PROJ_DIR/.claude/session-artifacts/$WORKFLOW_ID/diagnostics"
    mkdir -p "$DEST" 2>/dev/null
    # Move (not copy) — staging is single-use; the canonical store is the session dir.
    for f in start.ts end.ts events.jsonl workflow-id.txt; do
        [ -f "$STAGING/$f" ] && mv "$STAGING/$f" "$DEST/" 2>/dev/null
    done
    rmdir "$STAGING" 2>/dev/null

    # Aggregate session metrics (synchronous — once per session, not per turn).
    if [ -x "$PROJ_DIR/bin/diagnostics/aggregate-session.py" ]; then
        python3 "$PROJ_DIR/bin/diagnostics/aggregate-session.py" "$WORKFLOW_ID" "$SID" >/dev/null 2>&1
    fi

    # Render HTML report (always, if renderer exists). Pure stdlib; cheap.
    if [ -x "$PROJ_DIR/bin/diagnostics/render-html-report.py" ]; then
        python3 "$PROJ_DIR/bin/diagnostics/render-html-report.py" "$WORKFLOW_ID" >/dev/null 2>&1
    fi

    # Cross-session aggregation (best-effort, optional DuckDB dep, non-blocking).
    if [ -x "$PROJ_DIR/bin/diagnostics/aggregate-cross-session.py" ]; then
        nohup python3 "$PROJ_DIR/bin/diagnostics/aggregate-cross-session.py" >/dev/null 2>&1 &
    fi
else
    # No workflow id — archive to orphan dir (no loss, no pollution of session-artifacts).
    ORPHAN="$PROJ_DIR/.claude/.metrics/orphan/$SID"
    mkdir -p "$(dirname "$ORPHAN")" 2>/dev/null
    mv "$STAGING" "$ORPHAN" 2>/dev/null
fi
exit 0
