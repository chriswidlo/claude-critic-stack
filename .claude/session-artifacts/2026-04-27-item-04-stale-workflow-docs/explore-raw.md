# Documentation Surface Area Exploration
## Session: 2026-04-27-item-04-stale-workflow-docs

### 1. References to `workflows/architecture-review.md`

**Single reference found:**
- [README.md](../../../README.md) line 29: "See `workflows/architecture-review.md` for the full routing."

This is the only place in the repo that directly links to the file. No other documents, prompts, agent instructions, or config files reference it.

---

### 2. References to singular `critic` agent

**None found.** The stale workflow file itself is the only location that references an agent named `critic` (singular, without a suffix).

The current live system names only:
- `critic-architecture`
- `critic-operations`
- `critic-product`

Zero other prose, prompts, or agent docs reference a bare `critic` agent. The old workflow is the sole location using the singular name.

---

### 3. README.md claims contradicting the current architecture

**Lines 7–13** describe the system as "three things":

```
1. A critic subagent with explicit authority to reject...
2. A canon librarian subagent that retrieves...
3. An outside-view subagent that forces reference-class forecasting...
```

This is **outdated framing**. It conflicts with the 12-step workflow and 10-agent architecture defined in [CLAUDE.md](../../../CLAUDE.md) (steps 1–12, lines 18–99). The current system includes:

- `requirement-classifier` (step 1)
- `outside-view` (step 3)
- `canon-librarian` (step 3)
- `scope-mapper` (step 7)
- `frame-challenger` (step 8)
- `critic-architecture`, `critic-operations`, `critic-product` (step 10)
- `subagent-distiller` (step 6)
- `canon-refresher` (optional, Routines-scheduled)

**Line 29** claims the workflow is defined in `workflows/architecture-review.md`, which it is not — the real workflow is in [CLAUDE.md](../../../CLAUDE.md) steps 18–99.

---

### 4. Other top-level documentation that might describe workflow shape

**Top-level docs present:**
- [README.md](../../../README.md) — main entry point, currently has stale framing
- [CLAUDE.md](../../../CLAUDE.md) — authoritative workflow definition; clearly describes 12 steps and agent roster
- `.claude/session-artifacts/README.md` — describes artifact structure for 12-step workflow; accurate
- No `CONTRIBUTING.md`, `AGENTS.md`, or `docs/` directory at repo root

**Additional docs referencing workflow or agents:**
- [`.claude/agents/requirement-classifier.md`](./.claude/agents/requirement-classifier.md) — defines an agent
- [`.claude/agents/frame-challenger.md`](./.claude/agents/frame-challenger.md) — defines an agent
- Multiple session-artifact directories in `.claude/session-artifacts/` record executed workflows

None of these contradict the 12-step / 10-agent architecture. The surface-level breakage is confined to the README and the stale `workflows/architecture-review.md` file.

---

### 5. Contents of `workflows/` directory

Current structure:
```
workflows/
└── architecture-review.md     (3421 bytes, 67 lines)
```

**Finding: The directory contains only the one file.** Deleting `architecture-review.md` would leave the directory empty. The `workflows/` directory itself could be removed (or kept as a placeholder if you anticipate future workflow files).

---

### 6. References to `Phase 1`, `Phase-1`, or `"three subagents"`

**One reference found:**
- [`.claude/session-artifacts/README.md`](../../../.claude/session-artifacts/README.md) line 58: "Phase-2 upgrade" (not Phase-1)

This is a historical marker explaining a past upgrade; it does not propagate the outdated three-subagent framing. It does not describe the current shape as "three subagents."

**Negative finding:** No other prose in the repo uses the old "three subagents" framing or references Phase 1. The README's shorthand is isolated.

---

## Summary

| Question | Finding |
|----------|---------|
| **1. References to deleted file** | 1 reference in README.md line 29 |
| **2. Singular `critic` in live docs** | 0 references; singular `critic` only in stale workflow file |
| **3. README.md outdated claims** | Lines 7–13 describe wrong shape; line 29 links to stale file |
| **4. Other docs needing updates** | Only `.claude/session-artifacts/README.md` (accurate; no changes needed) |
| **5. Workflows/ directory empty after delete** | Yes; only contains the one file |
| **6. "Phase 1" or "three subagents" prose** | Only one "Phase-2" historical ref in session-artifacts README; no stale framing elsewhere |

**Confidence: High.** All references are from a full grep-r across the repo, excluding `.git/`.

