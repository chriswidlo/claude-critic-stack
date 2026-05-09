---
name: explain
description: On-demand orientation for `claude-critic-stack`. Renders a styled terminal card (Calvin S figlet header, plain-English layout, color-coded phases, live state from disk) and pops an interactive picker for the next move. Use when the user types `/explain` or asks a what-is-this / what-can-I-do-here / how-do-I-use-this question without naming a specific design problem. SKIP when the user is already mid-session, asked a specific design question (route through the 12-step workflow instead), or asked a factual question (route to canon-librarian).
allowed-tools: Bash(figlet:*) Bash(printf:*) Bash(echo:*) Bash(ls:*) Bash(date:*) Bash(python3:*) Bash(grep:*) Bash(head:*) Bash(wc:*) Bash(tr:*) Bash(seq:*) AskUserQuestion
---

You are the orientation skill for `claude-critic-stack`. The user typed `/explain`. Your job: render a styled card that reads the live state of the repo from disk, then pop an interactive picker so the user clicks a path instead of typing a prefix. No prose before, no prose after — the card and the picker are the entire output.

## Step 1 — Render the card

Run this exact `Bash` command (single call, no arguments substituted, no paraphrasing). The script reads disk state at invocation, so the dashboard is always current.

```bash
ROOT="."
SKILL_DIR=".claude/skills/explain"

SESSIONS=$(ls -1 "$ROOT/.claude/session-artifacts/" 2>/dev/null | grep -Ev '^(README|exemplars)' | wc -l | tr -d ' ')
EXEMPLARS=$(ls -1 "$ROOT/.claude/session-artifacts/exemplars/" 2>/dev/null | grep -v '^README' | wc -l | tr -d ' ')
LAST_DATE=$(ls -1t "$ROOT/.claude/session-artifacts/" 2>/dev/null | grep -Ev '^(README|exemplars)' | head -1 | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || echo '—')
CANON_TOTAL=$(ls -1 "$ROOT/canon/corpus/" 2>/dev/null | wc -l | tr -d ' ')

NB=$(ls -1d "$ROOT/upgrades/no-brainer/"*/ 2>/dev/null | wc -l | tr -d ' ')
NM=$(ls -1d "$ROOT/upgrades/normal/"*/ 2>/dev/null | wc -l | tr -d ' ')
PR=$(ls -1d "$ROOT/upgrades/profound/"*/ 2>/dev/null | wc -l | tr -d ' ')
OL=$(ls -1d "$ROOT/upgrades/outlandish/"*/ 2>/dev/null | wc -l | tr -d ' ')
UP_TOTAL=$((NB + NM + PR + OL))

# Average full-review duration from recent diagnostics/metrics.json (if any)
FULL_REVIEW_AVG=$(python3 - "$ROOT" <<'PYEOF' 2>/dev/null
import json, os, glob, sys
root = sys.argv[1] if len(sys.argv) > 1 else '.'
durations = []
for path in glob.glob(os.path.join(root, '.claude/session-artifacts/*/diagnostics/metrics.json')):
    try:
        d = json.load(open(path))
        ds = d.get('duration_seconds')
        if isinstance(ds, int) and ds > 0:
            durations.append(ds)
    except Exception:
        pass
if len(durations) >= 3:
    avg = sum(durations) // len(durations)
    print(f'~{avg // 60} min')
else:
    print('~10 min')
PYEOF
)
FULL_REVIEW_AVG="${FULL_REVIEW_AVG:-~10 min}"

CANON_RENDERED=$(python3 - "$ROOT" <<'PYEOF' 2>/dev/null
import re, os, sys
root = sys.argv[1] if len(sys.argv) > 1 else '.'
p = os.path.join(root, 'canon/sources.yaml')
if not os.path.exists(p):
    raise SystemExit(0)
cats = {}
cur = None
for line in open(p):
    m = re.match(r'^([a-z_][\w_]+):\s*$', line)
    if m:
        cur = m.group(1); cats[cur] = 0; continue
    if cur and re.match(r'^  - author:', line):
        cats[cur] += 1
display = [
    ('distributed',  cats.get('distributed_systems', 0)),
    ('ddd',          cats.get('domain_driven_design', 0)),
    ('refactoring',  cats.get('refactoring_and_evolution', 0)),
    ('integration',  cats.get('integration_and_messaging', 0) + cats.get('event_driven', 0)),
    ('resilience',   cats.get('resilience_and_operations', 0)),
    ('architecture', cats.get('architecture_decisions', 0)),
    ('testing',      cats.get('testing', 0)),
    ('forecasting',  cats.get('forecasting_and_judgment', 0)),
    ('research',     cats.get('research_and_innovation', 0)),
]
colors = ['\033[38;2;122;162;247m', '\033[38;2;125;207;255m', '\033[38;2;187;154;247m']
DIM = '\033[38;2;115;122;162m'
FG  = '\033[38;2;192;202;245m'
OFF = '\033[0m'
out = []
for row_idx in range(3):
    color = colors[row_idx]
    row = display[row_idx*3:(row_idx+1)*3]
    line = '    '
    for name, count in row:
        line += f'{color}▎{OFF} {DIM}{name:<15s}{OFF}{FG}{count:2d}{OFF}    '
    out.append(line)
print('\n'.join(out))
PYEOF
)

C_FG=$'\033[38;2;192;202;245m'
C_DIM=$'\033[38;2;115;122;162m'
C_FAINT=$'\033[38;2;65;72;104m'
C_BLUE=$'\033[38;2;122;162;247m'
C_CYAN=$'\033[38;2;125;207;255m'
C_VIOLET=$'\033[38;2;187;154;247m'
C_GREEN=$'\033[38;2;158;206;106m'
C_YELLOW=$'\033[38;2;224;175;104m'
C_BOLD=$'\033[1m'
C_ITAL=$'\033[3m'
C_OFF=$'\033[0m'

section() {
    echo
    local title="$1"
    local pad=$((68 - ${#title}))
    printf "${C_DIM}━━ ${C_FG}${C_BOLD}%s${C_OFF}${C_DIM} %s${C_OFF}\n" "$title" "$(printf '━%.0s' $(seq 1 $pad))"
    echo
}

TITLE=$(figlet -d "$SKILL_DIR/fonts" -f calvin-s -w 100 "Claude Critic" 2>/dev/null || echo "Claude Critic")
echo
while IFS= read -r line; do printf "  ${C_VIOLET}%s${C_OFF}\n" "$line"; done <<< "$TITLE"
printf "  ${C_DIM}${C_ITAL}rigorous second opinions for important decisions${C_OFF}\n"

echo
printf "  ${C_FG}You bring one question. Before answering, the stack tries to disagree${C_OFF}\n"
printf "  ${C_FG}with itself: three independent critics push back, the canon librarian${C_OFF}\n"
printf "  ${C_FG}looks up what experts have written, and the reply names both the${C_OFF}\n"
printf "  ${C_FG}recommendation and its strongest dissent.${C_OFF}\n"

section "HOW YOU CAN ASK"
printf "  ${C_FG}%-26s${C_OFF}  ${C_DIM}%-38s${C_OFF}  ${C_GREEN}%s${C_OFF}\n" "describe a decision"     "the full review"                   "$FULL_REVIEW_AVG"
printf "  ${C_FG}%-26s${C_OFF}  ${C_DIM}%-38s${C_OFF}  ${C_GREEN}%s${C_OFF}\n" '"skip the critic"'      "review without the 3-critic panel" "~7 min"
printf "  ${C_FG}%-26s${C_OFF}  ${C_DIM}%-38s${C_OFF}  ${C_GREEN}%s${C_OFF}\n" '"quick take: …"'        "drafts an answer in one shot"      "~20 sec"
printf "  ${C_FG}%-26s${C_OFF}  ${C_DIM}%-38s${C_OFF}  ${C_GREEN}%s${C_OFF}\n" "ask about a concept"    "looks it up in the canon"          "~5 sec"

section "THE FULL REVIEW (12 steps grouped into 6 phases)"
printf "  ${C_BLUE}1.${C_OFF}  ${C_FG}%-22s${C_OFF}  ${C_DIM}figure out what you're really asking · reframe it${C_OFF}\n"   "read your question"
printf "  ${C_BLUE}2.${C_OFF}  ${C_FG}%-22s${C_OFF}  ${C_DIM}canon · similar past projects · your repo · distill${C_OFF}\n" "gather evidence"
printf "  ${C_CYAN}3.${C_OFF}  ${C_FG}%-22s${C_OFF}  ${C_DIM}map what already exists · challenge the framing${C_OFF}\n"     "scope it"
printf "  ${C_VIOLET}4.${C_OFF}  ${C_FG}%-22s${C_OFF}  ${C_DIM}generate the candidate recommendation${C_OFF}\n"             "draft an answer"
printf "  ${C_VIOLET}5.${C_OFF}  ${C_FG}%-22s${C_OFF}  ${C_DIM}3 critics push back · revise or replan if vetoed${C_OFF}\n"  "stress-test it"
printf "  ${C_GREEN}6.${C_OFF}  ${C_FG}%-22s${C_OFF}  ${C_DIM}write the synthesis · log a ledger entry${C_OFF}\n"           "deliver"

section "THE 3-CRITIC PANEL (step 5)"
printf "  ${C_BLUE}┃${C_OFF}  ${C_FG}${C_BOLD}%-13s${C_OFF}  ${C_DIM}invariants, coupling, boundaries${C_OFF}\n"    "architecture"
printf "  ${C_CYAN}┃${C_OFF}  ${C_FG}${C_BOLD}%-13s${C_OFF}  ${C_DIM}SLOs, blast radius, rollout${C_OFF}\n"          "operations"
printf "  ${C_VIOLET}┃${C_OFF}  ${C_FG}${C_BOLD}%-13s${C_OFF}  ${C_DIM}commitments, migration, affordances${C_OFF}\n" "product"
echo
printf "  ${C_DIM}${C_ITAL}any one critic can reject the answer outright. minority veto.${C_OFF}\n"

section "WHAT YOU GET BACK"
printf "  ${C_FG}a recommendation · named tradeoffs · dissenting evidence${C_OFF}\n"
printf "  ${C_FG}three uncertainties · the cheapest experiment to settle them${C_OFF}\n"

echo
printf "${C_FAINT}  ────────────────────────────────────────────────────────────────────────${C_OFF}\n"
echo
printf "  ${C_GREEN}%d${C_OFF} ${C_DIM}past sessions${C_OFF}  ${C_FAINT}·${C_OFF}  ${C_GREEN}%d${C_OFF} ${C_DIM}exemplars${C_OFF}  ${C_FAINT}·${C_OFF}  ${C_DIM}last${C_OFF}  %s\n" "$SESSIONS" "$EXEMPLARS" "$LAST_DATE"

echo
printf "  ${C_GREEN}%d${C_OFF} ${C_DIM}canon entries${C_OFF}\n" "$CANON_TOTAL"
[ -n "$CANON_RENDERED" ] && echo "$CANON_RENDERED"

echo
printf "  ${C_GREEN}%d${C_OFF} ${C_DIM}upgrades${C_OFF}\n" "$UP_TOTAL"
printf "    ${C_GREEN}✓${C_OFF} ${C_DIM}%-12s${C_OFF}${C_FG}%2d${C_OFF}    ${C_BLUE}●${C_OFF} ${C_DIM}%-9s${C_OFF}${C_FG}%2d${C_OFF}    ${C_VIOLET}◆${C_OFF} ${C_DIM}%-10s${C_OFF}${C_FG}%2d${C_OFF}    ${C_YELLOW}★${C_OFF} ${C_DIM}%-12s${C_OFF}${C_FG}%2d${C_OFF}\n" \
    "no-brainer" $NB "normal" $NM "profound" $PR "outlandish" $OL
echo
```

If `figlet` is missing, the title falls back to plain "Claude Critic" — the rest of the card still renders. If `python3` is missing, the canon-by-category line silently disappears (the `CANON_BUCKETS` variable is empty); the count line above remains.

## Step 2 — Pop the interactive picker

Immediately after the card prints, invoke `AskUserQuestion` with this single question. Do not write any text between the card and the picker.

- header: `Path`
- question: `What now?`
- multiSelect: false
- options:
    - **Start a design review** — *Describe a hard design question; the stack runs the full 12-step workflow.*
    - **Quick take** — *Short one-paragraph answer. Bypasses the workflow.*
    - **Knowledge question** — *Ask about a concept (e.g. "what does the CAP theorem say?"). Answered from canon, no workflow.*
    - **Just exploring** — *Dismiss this menu.*

## Step 3 — One-line follow-up

Based on the picker's answer, print exactly one line and stop. No closing remarks, no "let me know if…", no chain into another skill.

- **Start a design review** → *Describe the question now — the orchestrator will route the workflow.*
- **Quick take** → *Type your question prefixed with `quick take:`.*
- **Knowledge question** → *Ask the knowledge question now — answered from canon.*
- **Just exploring** → (print nothing — silent dismiss)

## Constraints

- **No prose before the card.** Don't introduce it. The card introduces itself.
- **No persona, no agreeability tax.** No "great question", no "happy to help".
- **One-shot.** Do not chain into `session-bootstrap` or any other skill — print the one follow-up line and stop. The user types the next thing themselves.
- **No path discipline violations.** This skill writes no markdown links and no paths in its output, so the rule is automatically satisfied.

## When `/explain` is the wrong call

Skip the card and picker entirely if:

- The user is mid-session — a [.claude/session-artifacts/](.claude/session-artifacts/)`<id>/` directory is being actively populated. Ask whether they meant to continue.
- The user asked a specific design question. Route through the 12-step workflow per [CLAUDE.md](CLAUDE.md), not orientation.
- The user asked a pure factual question. Route through `canon-librarian`, not orientation.
