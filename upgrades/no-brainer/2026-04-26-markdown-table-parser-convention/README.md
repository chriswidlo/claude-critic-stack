# Markdown-table parser convention for repo scripts (`\|` escapes)

| Field | Value |
|---|---|
| 📌 **title** | Markdown-table parser convention for repo scripts (`\|` escapes) |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | ai |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Spike of the format-only state-transition gate ran a Python script that parsed a markdown table from `upgrades/README.md`. The naive `split("|")` shredded any row whose regex column contained `\|` (escaped pipe — the markdown-table convention for embedding a literal pipe inside a cell). On first run, 5 of 7 schema rows were silently dropped. Caught immediately because the script reported `Schema covers: ['✅ accepted', '⚙️ run-through-repo']` — only the two rows whose regex contained no pipes survived. |
| 💡 **essence** | Any script in this repo that parses markdown tables must split on `(?<!\\)\|` (negative lookbehind: pipe not preceded by backslash), then `replace(r"\|", "|")` to restore literal pipes inside cells. This is a five-line pattern that should land in any future repo script + a one-paragraph note in whichever doc captures repo scripting conventions (`GIT.md`? `MODULES.md`? open question). |
| 🚀 **upgrade** | The next script-writer doesn't repeat the bug. The lab's convention of putting regexes (which contain `|` for alternation) inside markdown tables remains viable — without the convention, every script-writer has to rediscover that `\|` escapes break naive parsers, debug it, fix it, and probably break a different way. |
| 🏷️ **tags** | scripting, markdown, parsing, conventions, lab-hygiene |
| 🔗 **relates_to** | 2026-04-26-format-only-state-transition-gate |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The pattern](#the-pattern)
- [Why this is convention-worth, not just a code comment](#why-this-is-convention-worth-not-just-a-code-comment)
- [Where it should be documented](#where-it-should-be-documented)
- [Why no-brainer](#why-no-brainer)

## The pattern

```python
import re

def parse_markdown_table_row(row: str) -> list[str]:
    """Split a markdown table row on |, respecting \\| escapes."""
    # Negative lookbehind: split on | not preceded by backslash.
    parts = re.split(r"(?<!\\)\|", row)
    # First and last cells are empty (rows start and end with |).
    parts = parts[1:-1]
    # Restore literal pipes inside cells.
    return [c.strip().replace(r"\|", "|") for c in parts]
```

In bash/awk: harder. Use the Python pattern, or accept that the table cannot contain `\|` escapes.

## Why this is convention-worth, not just a code comment

The lab has already established that schema/config tables go in markdown (the `upgrades/README.md` schema table is the load-bearing example). Markdown tables that contain regexes will routinely have `|` characters that need escaping. So the failure mode is structural to the lab's chosen pattern, not incidental.

Without a convention, every future script that parses one of these tables either (a) forces regexes to be pipe-free (cripples the schema), (b) silently drops rows (the spike's failure), or (c) re-discovers the pattern through debugging (slow). With a convention, the pattern is import-and-forget.

## Where it should be documented

Three candidate homes, in order of preference:

1. **A future `MODULES.md` entry under "harness / scripting conventions."** Best fit if/when the constitutional-layer entry (LEDGER #4) lands.
2. **A future `GIT.md`** (LEDGER #16) under "scripts that operate on tracked files."
3. **A `bin/README.md`** if/when this repo grows a `bin/` directory of utility scripts.

Until any of those lands, this upgrade entry is the canonical reference. When MODULES.md or GIT.md lands, this entry should be linked from there and possibly subsumed.

## Why no-brainer

- The pattern is five lines.
- The damage of not having it (silent row dropout — the spike's exact failure mode) is real and was witnessed.
- Documentation can be a single paragraph in whatever convention doc lands first.
- Total work: ~10 minutes to add a paragraph + the helper function snippet wherever it goes.
