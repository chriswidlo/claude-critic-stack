# Distillation — canon-librarian

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage on "should critics get the Write tool" — i.e., per-lens verdict files vs. orchestrator-transcribed aggregate. Librarian returned 8 supporting passages, 6 contradicting/complicating passages, and 6 named gaps. Coverage declared **partial**.

## Direct facts (verified passages, body present)

1. [Anthropic, "Multi-agent research system" 2025, Appendix] Subagents writing directly to filesystem and passing lightweight references back "prevents information loss during multi-stage processing and reduces token overhead from copying large outputs through conversation history." (confidence: direct)
2. [Anthropic, "Effective context engineering" 2025, §Sub-agent architectures] Subagents "return only a condensed, distilled summary of their work (often 1,000-2,000 tokens)." (confidence: direct)
3. [Anthropic, "Effective context engineering" 2025, §JIT retrieval] Just-in-time agents "maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime." (confidence: direct)
4. [Anthropic, "Building Effective Agents" 2024, §Voting] Voting pattern: "Reviewing a piece of code for vulnerabilities, where several different prompts review and flag the code if they find a problem." (confidence: direct)
5. [Google SRE 2016, Ch. 15] "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions." (confidence: direct)
6. [Google SRE 2016, Ch. 15] Postmortems use "real-time collaboration" on a single doc with "open commenting/annotation system" — *one* shared document, not N sibling files. (confidence: direct)
7. [Google SRE 2016, Ch. 7] Admin Server pattern: "ACL-driven, RPC-based" with "no one could install or modify a server without an audit trail" and per-RPC logging of requestor, parameters, results. (confidence: direct)
8. [Google SRE 2016, Ch. 8] Audit trails are "archived with other build artifacts" — generated alongside work, not transcribed after. (confidence: direct)
9. [Anthropic, "Effective context engineering" 2025, §Tools] "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use." (confidence: direct)
10. [Google SRE 2016, Ch. 6] "Maintaining distinct systems with clear, simple, loosely coupled points of integration is a better strategy." (confidence: direct)
11. [Anthropic, "Building Effective Agents" 2024, §Summary] Three core principles: "Maintain simplicity… Prioritize transparency… Carefully craft your agent-computer interface (ACI)." (confidence: direct)
12. [Anthropic, "Building Effective Agents" 2024, Appendix 2] Poka-yoke example: SWE-bench tools "changed… to always require absolute filepaths—and we found that the model used this method flawsly [sic]." (confidence: direct)
13. [Google SRE 2016, Ch. 15] "An unreviewed postmortem might as well never have existed"; aggregation tools "help us identify common themes and areas for improvement across product boundaries." (confidence: direct)

## Inferred claims (librarian's synthesis on top of passages)

1. [canon-librarian] Current critic design (orchestrator transcribes prose verdicts) is "exactly the anti-pattern" the game-of-telephone passage warns against. (confidence: inferred)
2. [canon-librarian] Voting/minority-veto "doesn't survive aggregation through a single transcribing voice" — structural argument for per-voter persistence. (confidence: inferred)
3. [canon-librarian] A critic's `Write` grant should be path-scoped to `critiques/<lens>.md`, harness-enforced, not prompt-instructed. (confidence: inferred)
4. [canon-librarian] Per-lens files cleanly separate "lens was wrong" from "transcription was wrong" — two distinct failure modes. (confidence: inferred)
5. [canon-librarian] Adding `Write` to a critic that previously had Read/WebFetch/WebSearch is tool-set expansion and risks decision dilution (where to write? edit prior verdicts?). (confidence: inferred)
6. [canon-librarian] SRE pattern would suggest *one* shared `critiques.md` with section headers per lens, not N sibling files — proposal's "drop the aggregate" arm runs against this. (confidence: inferred)
7. [canon-librarian] Per-lens write surfaces should be schema-validated, not free-form Markdown the critic invents. (confidence: inferred)
8. [canon-librarian] Strict simplicity reading: prove transcription loss is real with examples before adding mechanism — "game of telephone" is suggestive, not specific. (confidence: inferred)
9. [canon-librarian] Dropping the aggregate entirely loses cross-lens pattern recognition; thin verdict-index is the SRE-aligned choice. (confidence: inferred)

## Authority-framed claims
None. The librarian quoted sources directly with section citations and did not ventriloquize. All "X argues" framings are backed by an inline quote from X.

## Contradictions surfaced (load-bearing — preserve sharp edges)

- **Per-lens isolation vs. one shared doc.** Anthropic multi-agent (#1 supporting: subagents write own artifacts, lightweight refs back) **vs.** Google SRE Ch. 15 (#2 contradicting: postmortems are *one* shared doc with annotation, not N sibling files).
- **Filesystem-artifact endorsement vs. tool-bloat warning.** Anthropic "filesystem to minimize telephone" (#1 supporting) **vs.** Anthropic "bloated tool sets are a top failure mode" (#1 contradicting) — both from the same publisher, same era.
- **Drop-the-aggregate vs. keep-the-aggregate.** JIT/lightweight-index argument (#3 supporting) **vs.** SRE "unreviewed postmortem might as well never have existed" + aggregation tools value (#6 contradicting).
- **Add mechanism vs. maintain simplicity.** Game-of-telephone fix (#1 supporting) **vs.** "maintain simplicity" + demand evidence of actual loss (#4 contradicting).
- **Loose coupling supports per-lens isolation, but warns against scope-creep.** Ch. 6 (#3 contradicting) cuts both ways: yes to separate files, no to free-form content drift.

## Subagent's own verdict (verbatim)
"**Partial.** Strong coverage on multi-agent artifact patterns, tool-permission discipline, and audit/postmortem authorship from Anthropic engineering essays + Google SRE. Thin coverage on single-writer-vs-multi-writer file patterns at the OS/build-system level (no Helland body text — stub; no Hohpe EIP body retrieved here). No canon entry directly addresses 'review-of-review' / self-modifying review systems — that's a real gap."

## Gaps the subagent missed
The librarian itself enumerated 6 gaps; orchestrator should treat these as known unknowns rather than re-invoke:
1. Self-modifying review systems / review-of-review (canon-silent).
2. Single-writer vs. multi-writer at OS/build-system level (Helland is stub — do not fabricate).
3. Path-restricted Write as a primitive in LLM harnesses (closest analogue is SRE Admin Server, not LLM-specific).
4. Aggregator/index "earns its keep" heuristics (no canonical treatment).
5. Empirical paraphrase loss in LLM orchestrator-to-subagent flows (only the suggestive "telephone" passage; no data).
6. Sources flagged abstract-only or stub: Helland 2007, Chen et al. "Devil's Advocate" 2024, Shinn et al. "Reflexion" 2023 — librarian correctly did not quote bodies.

Additional gaps the orchestrator may want named that the librarian did not call out:
- No passage on **failure-mode of per-lens artifacts going stale** (what happens when one lens's file is from a prior revision and others are fresh?).
- No passage on **append-only vs. overwrite semantics** in multi-author critique artifacts.

## Token budget
~950 tokens.
