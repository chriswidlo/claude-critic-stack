# Exploration Report — Critic Independence vs. Target-Repo Read Access

**Session id:** 2026-05-09-critic-independence-vs-target-repo-read-access

**Scope:** Complete audit of critic agent definitions, workflow orchestration, skills routing, and evidence of target-repo influence on the critic panel.

---

## 1. CRITIC AGENT DEFINITIONS — Tool Permissions and Input Constraints

### 1.1 The Three Opus Lenses

All three critic agents have **identical frontmatter and tool grants**:

**File:** [`.claude/agents/critic-architecture.md`](./.claude/agents/critic-architecture.md) (lines 1-5)
- **Tools:** `Read, WebFetch, WebSearch` (line 4)
- **Model:** Opus (inherited from orchestrator; no `model:` field pinned)
- **Inputs mentioned:** None in frontmatter; body references "the candidate" (line 9)
- **Output constraint:** Verdict at line 42, structured with 6 required sections (lines 20-42)
- **Target-repo prohibition:** Lines 44-50 explicitly list "Things you must not do" — no mention of target-repo access being forbidden or permitted

**File:** [`.claude/agents/critic-operations.md`](./.claude/agents/critic-operations.md) (lines 1-5)
- **Tools:** `Read, WebFetch, WebSearch` (line 4)
- **Model:** Opus (inherited)
- **Inputs mentioned:** None; body references "the candidate" (line 9)
- **Output constraint:** Verdict at line 47, structured with 7 required sections (lines 19-47)
- **Target-repo prohibition:** Same pattern as architecture (lines 49-54)

**File:** [`.claude/agents/critic-product.md`](./.claude/agents/critic-product.md) (lines 1-5)
- **Tools:** `Read, WebFetch, WebSearch` (line 4)
- **Model:** Opus (inherited)
- **Inputs mentioned:** None; body references "the candidate" (line 9)
- **Output constraint:** Verdict at line 42, structured with 6 required sections (lines 18-42)
- **Target-repo prohibition:** Same pattern (lines 44-49)

**Finding:** Critics are given no explicit instructions about target-repo access. They are told to review "the candidate" (the orchestrator's generated recommendation from step 9). No prohibitions exist in the agent files themselves.

### 1.2 The Three Sonnet Shadow Variants

**Files:**
- [`.claude/agents/critic-architecture-shadow.md`](./.claude/agents/critic-architecture-shadow.md)
- [`.claude/agents/critic-operations-shadow.md`](./.claude/agents/critic-operations-shadow.md)
- [`.claude/agents/critic-product-shadow.md`](./.claude/agents/critic-product-shadow.md)

All three shadows are **functionally identical to their Opus counterparts** with exactly two modifications:

1. **Frontmatter `model:` pinning** (lines 3-5 of each):
   - `model: sonnet` explicitly pins the Sonnet model
   - Example from [critic-architecture-shadow.md](./.claude/agents/critic-architecture-shadow.md): "You are pinned to Sonnet (not Opus) via the `model:` frontmatter field" (line 11)

2. **Output path redirection** (lines 8-9 of each):
   - Opus writes to `critiques/<lens>.md`
   - Shadow writes to `critiques/<lens>.shadow.md`
   - Example: "Write your verdict to `critiques/architecture.shadow.md`, not `critiques/architecture.md`" (critic-architecture-shadow.md line 42)

**Tools:** Same as Opus (`Read, WebFetch, WebSearch` per line 5 of each shadow)

**Critical constraint** (critic-architecture-shadow.md lines 37-40): "Do not coordinate with the Opus lane — you are the shadow precisely because you reason independently." This is a **coordination constraint**, not a **target-repo constraint**. Nothing in the shadow variants forbids or mentions target-repo access.

### 1.3 The Comparator (Triangulation Meta-Lens)

**File:** [`.claude/agents/critic-comparator.md`](./.claude/agents/critic-comparator.md) (lines 1-77)

**Tools:** `Read, Write` only (line 4) — **notably does not have WebFetch, WebSearch, or any tool to reach outside the repo**

**Inputs:** Reads both Opus and Sonnet verdict files from disk:
- Lines 17-25: "For each lens in `{architecture, operations, product}`: `critiques/<lens>.md` — Opus lane verdict; `critiques/<lens>.shadow.md` — Sonnet shadow lane verdict"

**Prohibitions** (lines 59-66):
- Line 66: "Do not WebSearch. You compare two on-disk files; that is the entire job."

**Critical finding:** Comparator does **not** have access to target-repo (no Read scope beyond repo, no WebFetch, no WebSearch). It only reads the verdicts the two lanes produced.

### 1.4 Summary of Tool Permissions

| Agent | Read | Write | WebFetch | WebSearch | Grep | Glob | Target-repo access implied? |
|---|---|---|---|---|---|---|---|
| critic-architecture | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | No explicit mention |
| critic-operations | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | No explicit mention |
| critic-product | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | No explicit mention |
| critic-architecture-shadow | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | No explicit mention |
| critic-operations-shadow | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | No explicit mention |
| critic-product-shadow | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | No explicit mention |
| critic-comparator | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | No, explicitly forbidden (line 66) |

---

## 2. WORKFLOW ORCHESTRATION — Where Target-Repo Content Enters Critic Context

### 2.1 The 12-Step Workflow Definition (CLAUDE.md)

**File:** [CLAUDE.md](./CLAUDE.md) (top-level, lines 1-132)

**Critical preamble** (lines 1-5):
> "You are running inside an adversarial-review stack. The working directory is **deliberately not a target codebase**. Do not look for one. Do not ask to see one. Do not suggest exploring the filesystem."

**Step 3–5 (Parallel gather)** (lines 28-31):
```
- `outside-view` — reference-class forecast; must consult canon first
- `canon-librarian` — corpus retrieval
- `Explore` — **only** if the user has provided repository context or named a target codebase. Otherwise skip.
```

**Key finding:** "Explore" is **not a named agent** but rather a **manual orchestration step**. The orchestrator performs it when a target-repo is in scope.

### 2.2 What "Explore" Actually Is (From Session Artifact Evidence)

**Evidence source:** [.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md](./.claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md) (lines 1-52)

The distiller summarizes an Explore invocation as:
- **Line 5:** "Orchestrator asked Explore to map the current repo state relevant to [the question]"
- **Line 14:** "Explore is used to fetch repo-grounded facts" (inferred from distillation pattern)

The Explore step is **orchestrator-conducted target-repo reading**, not an agent invocation. The orchestrator:
1. Reads the target-repo (if provided)
2. Compiles findings into a `distillations/explore.md` artifact
3. This artifact then feeds into step 7 (scope-mapper) and step 8 (frame-challenger)

**Does Explore output reach critics directly?** No. Per CLAUDE.md line 33: "After this step, the orchestrator reads **only** the distillations going forward; raw subagent output stays on disk."

Step 10 (critic-panel) consumes:
- The candidate recommendation (from step 9)
- Implicitly: question.md, frame.md (current revision), scope-map.md, challenges.md
- NOT explicitly: the Explore distillation

### 2.3 How Target-Repo Path Flows Through the Workflow (critique-prep and critique-start)

**Files involved:**
- [`.claude/skills/critique-prep/SKILL.md`](./.claude/skills/critique-prep/SKILL.md)
- [`.claude/skills/critique-start/SKILL.md`](./.claude/skills/critique-start/SKILL.md)

**What critique-prep does** (lines 6-136):

**Lines 60-67 (Validate target repo):**
Asks the user for one of:
- Absolute path on disk (verified with `test -d "<path>/.git"`)
- Git remote URL only ("remote-info-only" mode)
- None ("prompt-only" mode)

**Lines 60-63 (Grounding strategy):**
If target mode ≠ none, asks for strategy:
- `full-explore` — multi-agent deep read
- `user-named-subset` — specific paths
- `follow-AI-docs` — read target's CLAUDE.md, AGENTS.md, etc.
- `custom` — free-form

**Lines 120-121 (What goes on disk):**
> "Write `.local/target-path` only in local-path mode. A single line, the absolute path, no extra content. This file is gitignored — it never enters git history."

**Lines 115-118 (.gitignore rule):**
Ensure `.claude/session-artifacts/*/.local/` is in .gitignore.

**What critique-start does** (lines 23-42):

**Lines 23-26 (Source the target path):**
```
- Read `.claude/session-artifacts/<id>/.local/target-path`.
- Hold the absolute path in this session's working memory only
  — treat it as the value of `$CRITIC_TARGET` for any subagent prompt.
- Never echo it into a committed artifact.
```

**Lines 38-42 (Path-rewrite reminder):**
```
Whenever you compose a prompt for an agent that may read from `$CRITIC_TARGET`
(Explore in step 5, scope-mapper in step 7, critics in step 10 if they verify facts),
include this sentence verbatim in the prompt:

> Any absolute path under `$CRITIC_TARGET` must appear in your output as `<target>/...`.
  The absolute path is machine-specific; the `<target>/` token is what gets recorded in artifacts.
```

**Critical finding:** critique-start's instructions say "critics in step 10 **if they verify facts**" (line 38). This is a **conditional permission to pass target-repo to critics**, not a mandate.

### 2.4 What Actually Gets Passed to Critics (Step 10 Invocation)

**From CLAUDE.md line 43-48:**
```
10. **Critic-panel.** Invoke the three critic lenses in parallel (single message, three Agent calls):
    - `critic-architecture`
    - `critic-operations`
    - `critic-product`

    Aggregate verdicts into `critiques.md`.
```

**What is NOT in these instructions:**
- No mention of passing `$CRITIC_TARGET` to critics
- No mention of passing session-id
- No mention of passing inputs.md or question.md
- No mention of passing Explore distillation

**What critics implicitly receive:**
- The candidate recommendation (from step 9), passed as the main prompt input
- Presumably: the question.md (what the design question was) — implied by the need to judge "does this candidate address the question?"

**Critical ambiguity:** CLAUDE.md step 10 does not specify the exact prompt structure sent to critics. The skill instructions (critique-start line 38) *mention* the possibility of passing target-repo to critics, but the main workflow does not mandate it.

---

## 3. SKILLS THAT ROUTE TARGET-REPO CONTENT FORWARD

### 3.1 critique-prep Skill

**File:** [`.claude/skills/critique-prep/SKILL.md`](./.claude/skills/critique-prep/SKILL.md)

**Key actions:**
- Lines 37-47: Collects design doc, target-repo path, and grounding strategy
- Lines 67-68: Mints session-artifacts/<id>/.local/ and writes `.local/target-path`
- Lines 69-85: Writes question.md with the design doc body
- Lines 87-118: Writes inputs.md with target identifier, mode, and grounding strategy

**What targets becomes:**
- **question.md** — design doc body, no target-repo references (lines 73-85)
- **inputs.md** — target identifier (URL or name, never absolute path), grounding strategy (lines 87-118)
- **.local/target-path** — absolute path, gitignored, for the orchestrator's session-memory only (line 120)

**Pattern:** Target-repo is **decoupled into three artifacts**: design question (absolute), metadata (URL/name), and session-memory (absolute path).

### 3.2 critique-start Skill

**File:** [`.claude/skills/critique-start/SKILL.md`](./.claude/skills/critique-start/SKILL.md)

**Key actions:**
- Lines 16-20: Resolves session id and reads inputs.md
- Lines 23-26: Reads `.local/target-path` into `$CRITIC_TARGET` session-memory variable
- Lines 38-42: **Conditions pass to downstream agents** — "agents that **may read from** `$CRITIC_TARGET`"

**The conditional list:** "Explore in step 5, scope-mapper in step 7, critics in step 10 **if they verify facts**"

**Finding:** Critics are on the **conditional** list, not a mandatory pass-through. The skill leaves the decision to the orchestrator at step 10 invocation time.

### 3.3 No Other Skills Reference Target-Repo

Checked: explain, session-bootstrap, ledger-render, path-check. None of them mention or route target-repo content.

---

## 4. EXISTING SESSION ARTIFACTS — Evidence of Target-Repo Influence in Critiques

**No sessions in this repo have yet used critique-prep + critique-start**, so there are no existing critiques that received target-repo context.

However, **prior sessions do show critiques referencing external design context**:

### 4.1 Sample Critique (Prompt-Only, No Target-Repo)

**Session:** [2026-04-26-format-only-state-transition-gate](./.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/)

This session had no target-repo (the question was about the upgrades-lab itself, i.e., the claude-critic-stack repo, which is the harness not a target).

**File:** [critiques/architecture.md](./.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/critiques/architecture.md)

**Evidence of what critics actually read:**
- Line 5: "the audit script's grep schema *is* the per-state transition schema" — this refers to **the candidate recommendation** (see candidate.md in same session)
- Lines 10-11: "README prose semantics + bash grep patterns" — these come from the **question.md / candidate**, not from target-repo
- Lines 14-17: Specific invariants named (rightmost-filled-column, body-section presence, etc.) — all from the **candidate's proposed mechanics**, not target-repo

**Product critic same session** ([critiques/product.md](./.claude/session-artifacts/2026-04-26-format-only-state-transition-gate/critiques/product.md)):
- Lines 7-9: "Day 1 of Phase 0: operator gains a script... **nothing has happened**. The thing the operator asked for does not exist." — references **question.md** intent, not target-repo
- Lines 20-22: "22 historical entries' state tables retroactively 'incorrectly produced'" — references **the candidate's design**, not a read of the target

**Finding:** Even without explicit target-repo access, critics reference **the design context from question.md and candidate.md**. They do not reference target-repo content, but they also do not forbid it.

---

## 5. THE SHADOW COMPARATOR AND DECORRELATION PRIMITIVES

### 5.1 What The Shadow Comparator Already Addresses

**File:** [`.claude/agents/critic-comparator.md`](./.claude/agents/critic-comparator.md)

**Type of correlation it measures:** **Model-family correlated blindness**

- Lines 11-12: "You compare the Opus lane and the Sonnet shadow lane for each critic lens."
- Lines 31-37: Defined agreement classes: `agree | partial-agree | disagree | unavailable`
- Lines 52-56: Specific definitions of each class (e.g., "disagree" = verdict labels two notches apart)

**Upgrade that implemented this:** [upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md](./upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md) (lines 1-150)

**From the upgrade's problem statement** (lines 32-36):
> "The critic panel runs three lenses (architecture, operations, product) on Opus by default. All three frontmatter files pin a model — all inherit Opus from the orchestrator. So three lenses on the same candidate become Opus reading itself three times."

**From the shadow-comparator concrete sketch** (lines 46-54):
```
- Each critic agent stays on Opus by default.
- Behind env var `SHADOW_PANEL=1`, each lens fires twice in parallel: Opus + Sonnet (same prompt, same candidate).
- New agent `critic-comparator` reads both, writes `critiques/<lens>.comparison.md`.
```

### 5.2 What Decorrelation The Stack Does NOT Address Yet

**The assumption buried in the comparator:** Both Opus and Sonnet **read the same candidate recommendation**. If the candidate itself embeds target-repo narrative (quotes from the target, shaped by target-repo constraints), then:
- Opus and Sonnet will *both* see that narrative
- Their disagreement will be **bounded by shared exposure to target-repo framing**
- This is a **new source of correlation the comparator does not measure**

**Evidence:** From the same upgrade (lines 11-12):
> "None of the three frontmatter files pin a model — all inherit Opus from the orchestrator. So three lenses on the same candidate become Opus reading itself three times."

The upgrade fixes "three lenses on the same model," but does **not** address "three lenses reading the same candidate that was shaped by target-repo constraints."

---

## 6. THE "CRITICS GET WRITE TOOL" CHANGE

### 6.1 What Was Changed

**File:** [upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md](./upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md)

**Status:** PAUSED — not implemented. (Line 3: "⏸️ **PAUSED — 2026-04-27.**")

**Proposed change** (lines 39-44):
- Add `Write` to each of the three critics' `tools:` line
- Add one sentence to each critic's body instructing them to write their verdict to `critiques/<lens>.md`
- Update CLAUDE.md step 10 to reflect that critics now persist their own verdicts

**Why paused:** Lines 3-4: "Loop 1 produced a convergent veto across all three lenses... Loop 2's revised candidate v2-C also returned 3× rework."

**Impact on this question:** The Write change does **not affect target-repo access**. It only changes who persists the verdict (critic directly vs. orchestrator transcription). The question of "can critics read target-repo?" is orthogonal.

---

## 7. ANYTHING SUSPICIOUS OR INDIRECT

### 7.1 Session-id and Question.md Leakage

**Potential vector:** If the orchestrator passes question.md to critics, and question.md mentions the target-repo context, then critics indirectly receive target-repo framing without explicit Read access.

**Evidence from question.md structure** (question.md template from CLAUDE.md):
```markdown
# Question under review
<design doc body verbatim>

## Constraints / context
- Target repo: <identifier>
- Grounding strategy: <strategy>
```

If question.md explicitly names the target-repo identifier (URL or name), and the orchestrator passes this to critics, then critics know:
1. **That a target-repo exists** (presence signal)
2. **What it is** (identifier, not absolute path)
3. **What grounding strategy was chosen** (full-explore, user-named-subset, follow-AI-docs, etc.)

This is **not the same as reading the target-repo content**, but it **shapes critic priors about what the question is about**.

**Finding:** question.md may carry target-repo metadata even though it does not contain target-repo content. Critics receiving question.md would see this metadata.

### 7.2 Settings.json and Hooks

**File:** [`.claude/settings.json`](./.claude/settings.json)

Permits:
- `Read(//Users/krzys/Development/Projects/claude-critic-stack/**)`
- `Glob(//Users/krzys/Development/Projects/claude-critic-stack/**)`
- `Grep(//Users/krzys/Development/Projects/claude-critic-stack/**)`

**Does NOT explicitly permit Reading outside this repo.**

**However:** The question-is settings.json scoped to this repo only, or is this a project-level override? If the user has a global settings.json that permits broader Read, critics could theoretically read target-repo files via Read tool.

**Status of hook enforcement:** Line 11 of settings.json file: `"hooks"` section does not exist. So there are **no runtime hooks enforcing path discipline on critics' Read calls**.

**Finding:** If a global settings.json permitted broader Read, critics could technically read target-repo files, and the only protection would be agent-side instruction (the path-rewrite reminder from critique-start line 38-42).

### 7.3 WebFetch and WebSearch as Backdoor

**Question:** Can critics use WebFetch / WebSearch to reach target-repo content indirectly?

**Answer:** Only if the target-repo is public on GitHub / accessible via web, and the critic decides to fetch it. This is **not a backdoor but a loophole**. The agent instructions do not forbid it.

**Evidence:** Neither critic-architecture.md, nor critic-operations.md, nor critic-product.md contain any instruction against WebFetch-ing the target-repo if its URL is mentioned in the candidate.

**Finding:** If the candidate recommendation mentions a GitHub URL and says "see this repo for details," a critic could fetch it via WebFetch. This is probably unintended but not explicitly prevented.

---

## 8. THE CURRENT DEPTH OF TARGET-REPO INFLUENCE — Summary

### Layer 1: Question & Frame (Steps 1-2)
- **Input:** question.md (design doc body + optional target-repo identifier in metadata)
- **Outputs:** requirement.md, frame.md
- **Target-repo content?** No. Metadata only if in question.md.
- **Does it reach critics?** Unknown — depends on step 10 invocation spec (not in CLAUDE.md).

### Layer 2: Subagent Gather (Steps 3-5)
- **Input:** question.md, scope from critique-prep (if used), target-repo path via `$CRITIC_TARGET` (session-memory only)
- **Outputs:** distillations/outside-view.md, distillations/canon-librarian.md, distillations/explore.md
- **Target-repo content?** Yes, via Explore step (orchestrator manually reads target).
- **Does it reach critics?** No — distillations are read-only by orchestrator; CLAUDE.md line 33 forbids re-reading raw subagent output.

### Layer 3: Scope-Map & Frame-Challenge (Steps 7-8)
- **Input:** question.md, distillations from step 6, target-repo path (for scope-mapper per critique-start line 38), candidate (not yet, but for reference)
- **Outputs:** scope-map.md, challenges.md
- **Target-repo content?** Yes, implicitly — scope-mapper may read target to understand existing primitives.
- **Does it reach critics?** Indirectly — scope-map.md and challenges.md are read by the generator (step 9) but NOT explicitly by critics per CLAUDE.md.

### Layer 4: Generator (Step 9)
- **Input:** scope-map.md, challenges.md, all prior artifacts, possibly target-repo (if orchestrator references it in generator prompts)
- **Outputs:** candidate.md
- **Target-repo content?** Possibly — the candidate may be shaped by target-repo constraints, but the artifact itself uses `<target>/...` token, not absolute paths.
- **Does it reach critics?** Yes, directly — critics review the candidate.

### Layer 5: Critic-Panel (Step 10)
- **Input:** candidate.md, implicitly question.md (unknown), possibly scope-map.md / challenges.md (unknown)
- **Outputs:** critiques/architecture.md, critiques/operations.md, critiques/product.md
- **Target-repo read access?** No explicit permission. They have `Read, WebFetch, WebSearch` but not targeted at `$CRITIC_TARGET`.
- **Target-repo *indirect* exposure?** Yes, if:
  - candidate.md mentions target-repo identifiers or constraints
  - question.md is passed and mentions target-repo metadata
  - critic uses WebFetch to fetch a GitHub URL mentioned in the candidate

---

## 9. LOAD-BEARING CONTRACTS AND RISK BOUNDARIES

### 9.1 Path Discipline as Stated (CLAUDE.md lines 7-17)

```
**NEVER** write absolute filesystem paths or `~/`-prefixed paths in **any** artifact
in this repo — not in CLAUDE.md, README.md, agents, prompts, workflows, upgrades,
session artifacts, plans, temporary notes, anywhere.
```

**What this protects:**
- Privacy (no `/Users/<username>` in git history)
- Portability (repo works across machines)
- Stability (stable grep targets across moves)

**What it does NOT protect:**
- Against model priors shaped by target-repo context
- Against indirect exposure via question.md metadata
- Against critic-authored inference based on target-repo narrative in the candidate

### 9.2 The "Deliberately Not a Target Codebase" Disclaimer (CLAUDE.md line 3)

```
You are running inside an adversarial-review stack. The working directory is
**deliberately not a target codebase**. Do not look for one.
```

**What this protects:** Against agents accidentally exploring the working directory as if it were the system under review.

**What it does NOT protect:** Against intentional, structured passing of target-repo context via question.md, candidate.md, or explicit `$CRITIC_TARGET` prompts.

---

## 10. ACTUAL vs. DESIGNED INDEPENDENCE

### Current State (Opus-Sonnet Triangulation Only)

- **Designed independence:** Three lenses on different aspects (architecture / operations / product)
- **Actual independence:** All three on Opus; shadow comparator measures model-family correlation, not lens/target-repo correlation
- **Critic exposure to target-repo:** Permitted indirectly via candidate.md, question.md metadata, and WebFetch; not explicitly via dedicated `$CRITIC_TARGET` prompts

### If Target-Repo Becomes Explicit (e.g., Future Feature)

If a future step adds "`$CRITIC_TARGET` to critic prompts" explicitly, then:
- All three critics would read the **same target-repo content**
- Shadow comparator would still measure Opus-Sonnet disagreement
- But **both Opus and Sonnet would be primed by the same target-repo narrative**
- This is a **new source of correlation** not currently measured

---

## 11. APPENDIX — File-by-File Citation Index

### Agent Definitions
- Critic-architecture.md (lines 1-57)
  - Tool grant: line 4
  - "Things you must not do": lines 44-56
  
- Critic-operations.md (lines 1-61)
  - Tool grant: line 4
  - "Things you must not do": lines 49-61

- Critic-product.md (lines 1-56)
  - Tool grant: line 4
  - "Things you must not do": lines 44-49

- Critic-architecture-shadow.md (lines 1-47)
  - Model pinning: line 4
  - Output path: lines 8-9, 42
  - Coordination constraint: lines 37-40

- Critic-operations-shadow.md (lines 1-48)
  - Model pinning: line 4
  - Output path: lines 8-9, 43
  - Coordination constraint: lines 37-40

- Critic-product-shadow.md (lines 1-47)
  - Model pinning: line 4
  - Output path: lines 8-9, 42
  - Coordination constraint: lines 37-40

- Critic-comparator.md (lines 1-77)
  - Tool grant: line 4 (Read, Write only)
  - WebSearch prohibition: line 66
  - Inputs: lines 17-25

### Workflow Orchestration
- CLAUDE.md (lines 1-132)
  - Preamble disclaimer: lines 1-5
  - Step 3-5 (Parallel gather): lines 28-31
  - Step 10 (Critic-panel): lines 43-60

### Skills
- critique-prep/SKILL.md (lines 1-144)
  - Target-repo modes: lines 37-40
  - Grounding strategy: lines 44-46
  - .local/target-path: line 120
  - inputs.md format: lines 87-118

- critique-start/SKILL.md (lines 1-57)
  - Session resolution: lines 16-20
  - Target-path sourcing: lines 23-26
  - Conditional pass to agents: lines 38-42

### Session Artifacts
- .claude/session-artifacts/README.md (lines 1-165)
  - Artifact tree: lines 7-20
  - .gitignore choice: lines 158-164

- .claude/session-artifacts/2026-04-27-critics-get-write-tool-impl/distillations/Explore.md (lines 1-52)
  - What Explore does: lines 4-5
  - Evidence of critic-artifact reading: lines 9-14

### Upgrades
- upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md (lines 1-193)
  - Paused status: line 3
  - Run-through-repo outcome: lines 109-132

- upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md (lines 1-150)
  - Problem statement: lines 32-36
  - Sonnet shadow sketch: lines 46-54
  - Implementation plan: lines 78-94

---

## TRUNCATION NOTE

This report reads all critic agent files, CLAUDE.md, critique-prep/critique-start skills, and representative session artifacts. Skipped (low-priority for this question):
- Full contents of all 20+ session-artifacts directories (spot-checked 3)
- All other skills (explain, session-bootstrap, ledger-render, path-check) — none mention target-repo
- Detailed review of upgrades/ entries not related to critics or target-repo routing
- Global settings.json or user .claude/ configuration (outside repo scope)

