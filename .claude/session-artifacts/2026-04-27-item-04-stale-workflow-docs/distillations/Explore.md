## Source agent
Explore

## Invocation summary
Orchestrator asked Explore to map the documentation surface area touching the stale `workflows/architecture-review.md` file: who links to it, where the singular `critic` agent name still appears, what other docs carry outdated framing, and whether the `workflows/` directory has any other content. Explore returned a six-section grep-based survey.

## Direct facts
1. [README.md line 29] The string `See \`workflows/architecture-review.md\` for the full routing.` is the only direct reference to the stale workflow file in the repo. (confidence: direct)
2. [Explore grep across repo] Zero documents, prompts, agent instructions, or config files outside `workflows/architecture-review.md` itself reference a bare singular `critic` agent. (confidence: direct)
3. [README.md lines 7–13] The README describes the system as "three things": a critic subagent, a canon librarian subagent, and an outside-view subagent. (confidence: direct)
4. [[CLAUDE.md](../../../../CLAUDE.md)] The authoritative workflow definition lists 12 steps and 10 agents (`requirement-classifier`, `outside-view`, `canon-librarian`, `scope-mapper`, `frame-challenger`, `critic-architecture`, `critic-operations`, `critic-product`, `subagent-distiller`, `canon-refresher`). (confidence: direct)
5. [Explore directory listing] `workflows/` contains exactly one file: `architecture-review.md` (3421 bytes, 67 lines). Deletion would leave the directory empty. (confidence: direct)
6. [Explore grep] No `CONTRIBUTING.md`, `AGENTS.md`, or `docs/` directory exists at the repo root. (confidence: direct)
7. [`.claude/session-artifacts/README.md` line 58] Contains the phrase "Phase-2 upgrade" — a historical marker, not the outdated three-subagent framing. (confidence: direct)
8. [Explore grep] No other prose in the repo uses "three subagents" framing or references "Phase 1" / "Phase-1". (confidence: direct — negative finding from full grep)
9. [Explore grep] `.claude/session-artifacts/README.md` describes the artifact structure for the 12-step workflow and is accurate (no contradictions found). (confidence: direct)

## Inferred claims
1. [Explore] README.md lines 7–13 framing conflicts with the 12-step / 10-agent architecture in CLAUDE.md. (confidence: inferred — based on direct comparison of two texts)
2. [Explore] README.md line 29's claim that the workflow lives in `workflows/architecture-review.md` is false; the real workflow is in CLAUDE.md. (confidence: inferred)
3. [Explore] Surface-level breakage from the stale framing is confined to README.md and the stale workflow file itself; no other doc propagates it. (confidence: inferred — supported by exhaustive grep)
4. [Explore] The `workflows/` directory could be deleted entirely or retained as a placeholder for future workflow docs. (confidence: inferred — judgment call, not a fact)

## Authority-framed claims
None. Explore did not invoke or ventriloquize any external authority; all claims are grounded in repo-internal grep results.

## Contradictions surfaced
- **README.md vs CLAUDE.md on system shape.** README says "three subagents: critic, canon librarian, outside-view." CLAUDE.md says 12 steps, 10 named agents, with the singular `critic` replaced by a three-lens panel (`critic-architecture`, `critic-operations`, `critic-product`).
- **README.md vs filesystem on workflow location.** README line 29 points to `workflows/architecture-review.md` as the routing source. CLAUDE.md is the actual routing source; the pointed-to file is stale.

## Subagent's own verdict (verbatim)
"Confidence: High. All references are from a full grep-r across the repo, excluding `.git/`."

## Gaps the subagent missed
- Did not check whether any agent definitions under `.claude/agents/*.md` internally reference the singular `critic` (only checked top-level prose). A full read of each agent file would confirm.
- Did not check whether `prompts/` directory contents reference the stale workflow file or singular `critic` framing.
- Did not check whether any upgrade entries or canon entries reference the stale workflow file or three-subagent framing.
- Did not enumerate what specific edits to README.md would bring it into alignment (out of scope for Explore, but the orchestrator will need this for the generator step).
- Did not assess whether deleting `workflows/architecture-review.md` could break any external link (e.g., a canon entry, a session artifact, or an external bookmark) — only checked internal references.

## Token budget
~620 tokens.
