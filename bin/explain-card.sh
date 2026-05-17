#!/usr/bin/env bash
# Renders the /explain orientation card for claude-critic-stack.
# Reads live state from disk; pure stdout; no side effects.
# Invoked by .claude/skills/explain/SKILL.md

set -u

ROOT="."
SKILL_DIR=".claude/skills/explain"

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

# ── palette (tokyo-night) ───────────────────────────────────
FG=$'\033[38;2;192;202;245m'
DIM=$'\033[38;2;115;122;162m'
FAINT=$'\033[38;2;65;72;104m'
BLUE=$'\033[38;2;122;162;247m'
CYAN=$'\033[38;2;125;207;255m'
VIOLET=$'\033[38;2;187;154;247m'
GREEN=$'\033[38;2;158;206;106m'
YELLOW=$'\033[38;2;224;175;104m'
B=$'\033[1m'
I=$'\033[3m'
X=$'\033[0m'

# ── title ───────────────────────────────────────────────────
echo
TITLE=$(figlet -d "$SKILL_DIR/fonts" -f calvin-s -w 100 "Claude Critic" 2>/dev/null || echo "Claude Critic")
while IFS= read -r line; do printf "   ${VIOLET}%s${X}\n" "$line"; done <<< "$TITLE"
printf "   ${DIM}${I}adversarial review of design & architecture decisions${X}\n"

# ── pitch ───────────────────────────────────────────────────
echo
printf "   ${FG}You bring a design question. The stack reframes it, pulls evidence from${X}\n"
printf "   ${FG}a curated ${CYAN}canon${FG} + a ${CYAN}reference-class outside view${FG}, then runs three${X}\n"
printf "   ${FG}independent critic lenses ${DIM}(${VIOLET}architecture${DIM} · ${BLUE}operations${DIM} · ${CYAN}product${DIM})${FG} with${X}\n"
printf "   ${FG}minority-veto. You leave with a recommendation, its strongest dissent,${X}\n"
printf "   ${FG}three named uncertainties, and the cheapest experiment to settle them.${X}\n"
echo
echo

# ── ways to ask ─────────────────────────────────────────────
printf "   ${VIOLET}▎${X}  ${FG}${B}ways to ask${X}\n"
echo
printf "      ${FG}%-22s${X}  ${FAINT}→${X}  ${DIM}%-30s${X}  ${GREEN}%s${X}\n" "describe a decision"  "full 12-step review"        "$FULL_REVIEW_AVG"
printf "      ${FG}%-22s${X}  ${FAINT}→${X}  ${DIM}%-30s${X}  ${GREEN}%s${X}\n" '"skip the critic"'    "review without the panel"   "~7 min"
printf "      ${FG}%-22s${X}  ${FAINT}→${X}  ${DIM}%-30s${X}  ${GREEN}%s${X}\n" '"quick take: …"'      "one-paragraph answer"       "~20 sec"
printf "      ${FG}%-22s${X}  ${FAINT}→${X}  ${DIM}%-30s${X}  ${GREEN}%s${X}\n" "ask about a concept"  "canon lookup, no workflow"  "~5 sec"
echo
echo

# ── what's loaded ───────────────────────────────────────────
printf "   ${VIOLET}▎${X}  ${FG}${B}what's loaded${X}\n"
echo
printf "      ${GREEN}${B}%2d${X}  ${DIM}past sessions${X}    ${FAINT}·${X}    ${GREEN}${B}%2d${X}  ${DIM}exemplars${X}    ${FAINT}·${X}    ${DIM}last${X}  ${FG}%s${X}\n" "$SESSIONS" "$EXEMPLARS" "$LAST_DATE"
printf "      ${GREEN}${B}%2d${X}  ${DIM}canon entries${X}   ${FAINT}·${X}   ${DIM}expert writing on distributed systems, DDD, refactoring, ops${X}\n" "$CANON_TOTAL"
printf "      ${GREEN}${B}%2d${X}  ${DIM}upgrades${X}        ${GREEN}✓ %d${X} ${DIM}no-brainer${X}   ${BLUE}● %d${X} ${DIM}normal${X}   ${VIOLET}◆ %d${X} ${DIM}profound${X}   ${YELLOW}★ %d${X} ${DIM}outlandish${X}\n" "$UP_TOTAL" "$NB" "$NM" "$PR" "$OL"
echo
echo

# ── rename shortlist ────────────────────────────────────────
printf "   ${VIOLET}▎${X}  ${FG}${B}rename shortlist${X}   ${DIM}${I}(claude-critic-stack is a placeholder)${X}\n"
echo
printf "      ${CYAN}Purvapaksha${X} ${FAINT}|${X} ${CYAN}Sugya${X} ${FAINT}|${X} ${CYAN}Machloket${X} ${FAINT}|${X} ${CYAN}Resection${X} ${FAINT}|${X} ${CYAN}Trutina${X} ${FAINT}|${X} ${CYAN}Stretto${X} ${FAINT}|${X} ${CYAN}Mondo${X} ${FAINT}|${X} ${CYAN}Mu-mon${X} ${FAINT}|${X} ${CYAN}Rashnu${X}\n"
printf "      ${CYAN}Crux${X} ${FAINT}|${X} ${CYAN}Foil${X} ${FAINT}|${X} ${CYAN}Hossen${X} ${FAINT}|${X} ${CYAN}Kintsugi${X} ${FAINT}|${X} ${CYAN}Witan${X} ${FAINT}|${X} ${CYAN}Elenchus${X} ${FAINT}|${X} ${CYAN}Krisis${X} ${FAINT}|${X} ${CYAN}Aporia${X}\n"
echo
