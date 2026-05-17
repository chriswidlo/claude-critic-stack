#!/usr/bin/env bash
# Renders the /explain orientation card as a single bordered ASCII panel.
# No ANSI, no color — relies on layout discipline + box-drawing chars only.
# Output is the card body to be wrapped in a plain code fence by the skill.
#
# Width: 66 chars between vertical borders. Total line width = 70 chars (incl. 3-space indent + 2 borders).

set -u

ROOT="."

# ── live state ──────────────────────────────────────────────
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

# Use Python for precise width-padding with Unicode awareness.
python3 - "$SESSIONS" "$EXEMPLARS" "$LAST_DATE" "$CANON_TOTAL" "$NB" "$NM" "$PR" "$OL" "$UP_TOTAL" "$FULL_REVIEW_AVG" <<'PYEOF'
import sys, unicodedata

SESSIONS, EXEMPLARS, LAST_DATE, CANON_TOTAL, NB, NM, PR, OL, UP_TOTAL, FULL_REVIEW_AVG = sys.argv[1:11]

W = 96            # inner box width (chars between │ borders) — fills typical wide terminals
INDENT = ""       # no left indent — let the code-fence left edge be the box left edge

def w(s):
    """Display width: 2 for east-asian wide chars, 1 otherwise."""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)

def line(content=""):
    """Body line: │ content padded to W │"""
    pad = W - w(content)
    if pad < 0: pad = 0
    print(f"{INDENT}│{content}{' ' * pad}│")

def divider(left="├", right="┤", fill="─"):
    print(f"{INDENT}{left}{fill * W}{right}")

def centered(text):
    pad = (W - w(text)) // 2
    left = " " * pad
    right_pad = W - w(text) - pad
    print(f"{INDENT}│{left}{text}{' ' * right_pad}│")

def empty():
    line("")

# ── top border ─────────────────────────────────────────────
divider(left="╭", right="╮")

# ── title block (centered) ────────────────────────────────
empty()
centered("╔═╗┬  ┌─┐┬ ┬┌┬┐┌─┐  ╔═╗┬─┐┬┌┬┐┬┌─┐")
centered("║  │  ├─┤│ │ ││├┤   ║  ├┬┘│ │ ││  ")
centered("╚═╝┴─┘┴ ┴└─┘─┴┘└─┘  ╚═╝┴└─┴ ┴ ┴└─┘")
empty()
centered("adversarial review of design & architecture decisions")
empty()

# ── HOW IT WORKS ──────────────────────────────────────────
divider()
empty()
line("   HOW IT WORKS")
empty()
line("     1   you bring a design question")
line("     2   the stack reframes it before answering")
line("     3   evidence pulled from a curated canon and a")
line("         reference-class outside view")
line("     4   three critic lenses review with minority-veto")
line("            · architecture")
line("            · operations")
line("            · product")
line("     5   you leave with")
line("            · the recommendation")
line("            · its strongest dissent")
line("            · three named uncertainties")
line("            · the cheapest experiment to settle them")
empty()

# ── WAYS TO ASK ───────────────────────────────────────────
divider()
empty()
line("   WAYS TO ASK")
empty()
line(f"     describe a decision       full 13-step review     {FULL_REVIEW_AVG:>7}")
line( "     say \"skip the critic\"     13-step minus panel     ~7 min")
line( "     say \"quick take\"          one-paragraph answer    ~20 sec")
line( "     ask a factual question    canon lookup            ~5 sec")
empty()

# ── WHAT'S LOADED ─────────────────────────────────────────
divider()
empty()
line("   WHAT'S LOADED")
empty()
line(f"     sessions       {SESSIONS}")
line(f"     exemplars      {EXEMPLARS}")
line(f"     last session   {LAST_DATE}")
empty()
line(f"     canon entries  {CANON_TOTAL}")
line( "                    distributed systems · DDD · refactoring · ops")
empty()
line(f"     upgrades       {UP_TOTAL} total")
line(f"                    {NB} no-brainer · {NM} normal · {PR} profound · {OL} outlandish")
empty()

# ── RENAME SHORTLIST ──────────────────────────────────────
divider()
empty()
line("   RENAME SHORTLIST")
empty()
line("     claude-critic-stack is a placeholder")
empty()
line("     Purvapaksha · Sugya · Machloket · Resection · Trutina")
line("     Stretto · Mondo · Mu-mon · Rashnu · Crux · Foil · Hossen")
line("     Kintsugi · Witan · Elenchus · Krisis · Aporia")
empty()

# ── bottom border ─────────────────────────────────────────
divider(left="╰", right="╯")
PYEOF
