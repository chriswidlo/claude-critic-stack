# Distillation — canon-librarian

## Source agent
canon-librarian

## Invocation summary
Orchestrator asked for canon coverage of "residual references to deleted artifacts in surrounding prose" — stale comments, broken-windows tension, silent scope-shrink, RFC/PEP/ADR governance of superseded documents. Librarian returned a thin/partial coverage verdict with two oblique full-text passages (Anthropic 2025 context-engineering, Google SRE 2016 postmortems) and three stubs (Fowler, Feathers, Beck) it explicitly refused to ventriloquize.

## Direct facts

1. [Anthropic 2025, *Effective Context Engineering for AI Agents*] "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases" — the "context rot" claim. (confidence: direct)
2. [Anthropic 2025] "Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM." (confidence: direct)
3. [Anthropic 2025] Tool-call results deep in message history are flagged as "low-hanging superfluous content" once consumed. (confidence: direct)
4. [Anthropic 2025] "overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later" — same source self-complicating. (confidence: direct)
5. [Google SRE Book 2016, Ch. 15] A postmortem is defined as "a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring." (confidence: direct)
6. [Google SRE 2016, Ch. 15] Postmortems are added to a team/org repository so that "Transparent sharing makes it easier for others to find and learn from the postmortem." (confidence: direct)
7. [Google SRE 2016, "Keep a History of Outages"] "There is no better way to learn than to document what has broken in the past." (confidence: direct)
8. [canon-librarian] Fowler *Refactoring* (2018), Feathers *Working Effectively with Legacy Code* (2004), and Beck *TDD by Example* (2002) are present in the corpus as **citation-only stubs**; full text not ingested; librarian refused to invent quotes. (confidence: direct — meta-fact about corpus state)
9. [canon-librarian] Corpus has **no entries** on: IETF/RFC governance of obsoleted RFCs, PEP withdrawn/superseded process, Rust RFC closure conventions, ADR literature (Nygard 2011, Tyree & Akerman 2005, MADR), documentation-as-code style guides (Diátaxis, Google docs style, Write the Docs), or any direct treatment of "silent scope-shrink." (confidence: direct — explicit gap declaration)
10. [canon-librarian] Pragmatic Programmer broken-windows metaphor and Beck's "leave the campsite cleaner" are **not in the corpus, not even as stubs**. (confidence: direct)

## Inferred claims

1. [canon-librarian] Un-pruned references to no-longer-relevant artifacts impose a real cost on a downstream reader — by analogy from LLM context rot to human prose navigation. (confidence: inferred — librarian's own analogy from Anthropic passage to human readers)
2. [canon-librarian] SRE postmortem culture generalizes to a stance that "prose is partly a historical record, not just a current spec," which counterweights the cleanup-favoring frame. (confidence: inferred — extrapolation from postmortem-repository practice to general doc maintenance)
3. [canon-librarian] A residual reference to a deleted artifact "may be the only surviving trace of *why* the artifact existed"; deleting it forecloses future archaeology. (confidence: inferred — librarian's application of Anthropic compaction-cost passage to the question)
4. [canon-librarian] Silent scope-shrink (a deleted referent quietly narrowing a still-standing claim) may be a **novel observation** without prior literature backing in or near the corpus. (confidence: inferred — librarian explicitly flags as not-found, suggests treating as novel)
5. [canon-librarian] On "comments naming deleted code, clean them up" the consensus is stable; on "how much history to preserve in prose," consensus is **not** stable — git-as-history, ADRs, and docs-as-code have shifted opinion. (confidence: inferred — staleness commentary, not a quoted claim)

## Authority-framed claims

1. "Fowler's canonical position: 'comments are a deodorant for bad code' / delete the comment as part of the refactor." — underlying claim: Fowler advocates deleting comments that name code that no longer exists. Quote present in output: **no** (stub; librarian explicitly refused to produce the quote). Confidence: **unsupported** in this corpus.
2. "Feathers' 'scratch refactoring' / 'characterization tests' frame: surrounding scaffolding needs the same treatment as the deletion." — underlying claim: deletion without cleaning surrounding artifacts creates a "seam without a contract." Quote present: **no** (stub). Confidence: **unsupported** in this corpus.
3. "Beck's red-green-refactor loop puts cleanup *inside* the unit of change." — underlying claim: cleanup belongs in the same commit as the deletion. Quote present: **no** (stub). Confidence: **unsupported** in this corpus.
4. "ADR pattern's standard answer: supersede, don't delete; link new to old; mark old as Superseded-by." — underlying claim: governance literature recommends preservation-with-pointer over deletion. Quote present: **no** (no ADR entries in corpus at all). Confidence: **unsupported** in this corpus (librarian flags as well-known outside the corpus but not retrievable from it).
5. "IETF RFCs are immutable and superseded via 'Obsoletes:' / 'Updates:' headers; PEPs use Status: Withdrawn/Superseded; Rust RFCs are closed but file is preserved with a note." — underlying claim: governance norms favor preserve-and-mark over delete. Quote present: **no**. Confidence: **unsupported** in this corpus.

## Contradictions surfaced

- **Cleanup-favoring (Anthropic 2025, primary read):** unpruned dead referents impose a recall/attention cost; pruning is not neutral — leaving residue is a tax.
  vs.
- **Leave-the-trail (Google SRE 2016 + Anthropic 2025 self-complication):** the trail (including dead references and "we used to do X, stopped because Y") is itself the artifact; aggressive pruning erases institutional memory and discards subtle context whose importance only becomes legible later.

These are **not reconciled** in the librarian's output and should not be collapsed downstream. The cleanup-favoring side is also **stub-heavy** in this corpus (its strongest exponents — Fowler, Feathers, Beck — are unquotable here); the leave-the-trail side has a directly quotable full-text source (SRE 2016).

## Subagent's own verdict (verbatim)

"**Thin / partial.**" (Corpus coverage line.) Plus the one-line summary: "The corpus has the **citations** for the cleanup-favoring side of this question but not the **text**; it has **full text** for the leave-the-trail counterweight (SRE postmortem culture) and for a contemporary nuance (Anthropic on compaction-cost). The user's sub-questions on RFCs, ADRs, and silent scope-shrink are **genuine corpus gaps** — the answer should name them, not paper over them."

## Gaps the subagent missed

- The librarian named the gaps cleanly (RFC/PEP/Rust governance, ADR literature, broken-windows/boy-scout-rule, silent scope-shrink, Fowler/Feathers/Beck full text). It did **not** propose canon-refresher targets to close these gaps — the orchestrator may want to flag these for a future canon-refresher pass, particularly Nygard's ADR post and a docs-as-code style guide (Diátaxis), since both are directly on-topic and freely retrievable.
- No treatment of the *commit-message-and-PR-as-trail* alternative — i.e., the position that git history (not prose) is the right place for "we used to mention Y." This is a third frame (neither cleanup-the-prose nor leave-the-trail-in-prose) that the librarian did not surface and that may resolve the contradiction by relocating the trail.
- No quantitative or empirical reference-class data on doc-rot or stale-reference incidence; this is properly an outside-view question, but the librarian did not flag the handoff.

## Token budget
~880 tokens.
