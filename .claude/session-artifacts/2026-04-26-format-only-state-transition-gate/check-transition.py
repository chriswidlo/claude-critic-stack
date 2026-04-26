#!/usr/bin/env python3
"""
Upgrade-transition gate — SPIKE (not productionized).

Reads the schema table from upgrades/README.md, finds an entry's current state
(rightmost filled-in cell in the state table), and warns if the entry body is
missing the required element for the requested new state.

Spike scope:
- One regex per state (no AND across requirements).
- No --apply flag (deferred until git strategy lands).
- No git operations.
- README path hardcoded.
- Warning-only; never writes to entries.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
README = REPO / "upgrades" / "README.md"

STATES = [
    "🌱 created", "🔬 spiked", "📋 prepared", "✅ accepted",
    "⚙️ run-through-repo", "🔨 implemented", "💎 value-proved", "🏁 completed",
]


def parse_schema(readme_text: str) -> dict | None:
    section = re.search(
        r"### Required body elements per state.*?\n(\| State \|[^\n]+\n)((?:\|[^\n]+\n)+)",
        readme_text, re.DOTALL,
    )
    if not section:
        return None
    body = section.group(2).strip().split("\n")
    schema = {}
    for row in body:
        if not row.startswith("|") or "---" in row:
            continue
        # Split on `|` but not on escaped `\|` (markdown table convention).
        parts = re.split(r"(?<!\\)\|", row)[1:-1]
        cols = [c.strip().replace(r"\|", "|") for c in parts]
        if len(cols) < 3:
            continue
        state, element, regex_cell = cols[0], cols[1], cols[2]
        m = re.search(r"`([^`]+)`", regex_cell)
        if not m:
            continue
        schema[state] = {"element": element, "regex": m.group(1)}
    return schema


def find_current_state(entry_text: str):
    lines = entry_text.split("\n")
    for i, line in enumerate(lines):
        if "🌱 created" in line and "🏁 completed" in line and i + 2 < len(lines):
            date_row = lines[i + 2]
            cells = [c.strip() for c in date_row.split("|")[1:-1]]
            if len(cells) == len(STATES):
                rightmost = "🌱 created"
                for state, cell in zip(STATES, cells):
                    if cell and cell != "—":
                        rightmost = state
                return rightmost, cells
    return None, None


def check(entry_path: str, requested_state: str) -> int:
    t0 = time.time()
    schema = parse_schema(README.read_text())
    if not schema:
        print(f"ERROR: could not parse schema table from {README}")
        return 1
    if requested_state not in schema:
        print(f"ERROR: '{requested_state}' is not a state with required elements.")
        print(f"Schema covers: {list(schema.keys())}")
        return 1
    entry = Path(entry_path)
    if not entry.exists():
        print(f"ERROR: entry not found: {entry}")
        return 1
    entry_text = entry.read_text()

    current_state, cells = find_current_state(entry_text)
    if current_state is None:
        print(f"ERROR: could not find state table in {entry}")
        return 1

    rule = schema[requested_state]
    pattern = re.compile(rule["regex"], re.IGNORECASE | re.MULTILINE)
    match = pattern.search(entry_text)
    elapsed = (time.time() - t0) * 1000

    print(f"Entry:                    {entry}")
    print(f"Current state (detected): {current_state}")
    print(f"  raw row:                {' | '.join(cells)}")
    print(f"Requested advance to:     {requested_state}")
    print()
    print(f"Schema for {requested_state} (from upgrades/README.md):")
    print(f"  element: {rule['element']}")
    print(f"  regex:   {rule['regex']}")
    print()
    if match:
        line_num = entry_text[:match.start()].count("\n") + 1
        snippet = match.group(0).strip()[:80]
        print(f"  ✓ matched at line {line_num}: {snippet!r}")
        print()
        print("All required elements present.")
        print(f"Suggested edit: in the state table, replace '—' under '{requested_state}'")
        print(f"with today's date ({time.strftime('%Y-%m-%d')}).")
        print()
        print(f"(check ran in {elapsed:.0f}ms)")
        return 0
    print("  ✗ not found")
    print()
    print(f"Missing 1 required element. Lab contract says {requested_state}")
    print(f"entries should contain: {rule['element']}")
    print()
    print("Advance is allowed — the lifecycle is descriptive, not prescriptive —")
    print("but this gate is flagging the gap so you can decide whether to fix the")
    print("entry or proceed anyway.")
    print()
    print(f"(check ran in {elapsed:.0f}ms)")
    return 2


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <entry-path> '<new-state>'")
        print(f"Example: {sys.argv[0]} upgrades/no-brainer/2026-04-26-rnd-lab.md '💎 value-proved'")
        sys.exit(1)
    sys.exit(check(sys.argv[1], sys.argv[2]))
