# Canon retrieval — residual references to deleted artifacts in surrounding prose

## Corpus coverage
**Thin / partial.** The canon contains classic refactoring and legacy-code references that bear directly on stale comments and broken-windows tension — but those entries (Fowler *Refactoring* 2018, Feathers *Working Effectively with Legacy Code* 2004, Beck *TDD by Example* 2002) are **stub entries** in this corpus: citation-only, full text not ingested. Quotes from those works cannot be produced honestly from the corpus.

The corpus has **no entries** on:
- The IETF / RFC governance literature on deleted/obsoleted RFCs
- Python PEP process for withdrawn/superseded PEPs
- Rust RFC process for closed/superseded RFCs
- The architectural-decision-record (ADR) literature (Nygard's 2011 ADR blog post, Tyree & Akerman 2005, ThoughtWorks/MADR templates)
- Documentation-as-code style guides (Google developer docs style, Diátaxis, Write the Docs)
- Any direct treatment of "silent scope-shrink" — where a deleted referent quietly narrows a still-standing claim

These are real gaps. Do not paper over them.

The corpus *does* have full-text entries that bear obliquely on the question — postmortem culture (Google SRE 2016) and context curation / pruning (Anthropic *Effective Context Engineering* 2025). I'll surface those, with the caveat that they are adjacent, not central.

---

## Supporting passages (cleanup-favoring)

### 1. Anthropic, *Effective Context Engineering for AI Agents* (2025) — on pruning stale referents

> "Despite their speed and ability to manage larger and larger volumes of data, we've observed that LLMs, like humans, lose focus or experience confusion at a certain point. Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."

> "Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM."

> "An example of low-hanging superfluous content is clearing tool calls and results — once a tool has been called deep in the message history, why would the agent need to see the raw result again?"

**Relevance.** A direct argument that *un-pruned references to no-longer-relevant artifacts impose a real cost* on a downstream reader (here, an LLM; by analogy, a human navigating prose). When a doc names a deleted artifact, the named referent is dead context — it competes for attention with live content. This is the cleanup-favoring case in its strongest contemporary form: leaving residual references is not neutral.

### 2. Fowler, *Refactoring* (2018, 2nd ed.) — STUB

**Citation only.** Full text not ingested in this corpus. The book is the canonical source for "comments are a deodorant for bad code" / "if a comment names code that no longer exists, delete the comment as part of the refactor" / behavior-preserving small steps. **Do not invent the quote.** If the team needs the exact passage, retrieve from the book directly (Chapter 2 on Bad Smells; "Comments" smell).

### 3. Feathers, *Working Effectively with Legacy Code* (2004) — STUB

**Citation only.** Full text not ingested. Feathers' "scratch refactoring" and "characterization tests" frame is what the question is gesturing at: when you delete a thing, the surrounding scaffolding (tests, comments, prose claims) needs the same treatment as the deletion itself, or you've created a *seam without a contract*. **Do not invent the quote.**

### 4. Beck, *Test-Driven Development: By Example* (2002) — STUB

**Citation only.** Full text not ingested. Beck's red-green-**refactor** loop puts cleanup *inside* the unit of change — you don't ship the green without the refactor — which is the strongest precedent for "clean the prose in the same commit as the deletion." **Do not invent the quote.**

---

## Contradicting / complicating passages (the "leave the trail" position)

### 5. Google SRE Book (2016), Ch. 15 *Postmortem Culture: Learning from Failure*

> "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring."

> "Once those involved are satisfied with the document and its action items, the postmortem is added to a team or organization repository of past incidents. Transparent sharing makes it easier for others to find and learn from the postmortem."

And from the appendix-level guidance ("Keep a History of Outages"):

> "There is no better way to learn than to document what has broken in the past. History is about learning from everyone's mistakes. Be thorough, be honest, but most of all, ask hard questions."

**Why this complicates the framing.** SRE's whole stance on history is anti-cleanup: the *trail* — including dead references, scars, "we used to do X and stopped because Y" — is the artifact. Aggressively rewriting prose to remove every mention of a deleted thing erases the institutional learning the postmortem culture is designed to preserve. A doc that says "X and Y stay in sync — Y was removed in incident I-2024-07; see postmortem" is *more* useful than a doc that quietly says "X stays in sync" with the second clause silently amputated. The first invites a reader to learn from the deletion; the second hides that a deletion happened.

This is the strongest in-corpus counterweight to the cleanup-favoring frame, and it generalizes: prose is partly a historical record, not just a current spec. If you treat documentation purely as a spec, you optimize for cleanup; if you treat it partly as institutional memory, you optimize for *legible scars*.

### 6. Anthropic, *Effective Context Engineering* (2025) — the same source, complicating itself

> "The art of compaction lies in the selection of what to keep versus what to discard, as overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later."

**Why this complicates the framing.** Even the cleanup-favoring source flags that aggressive pruning has a cost: signal whose importance is only legible *later* gets thrown away. Applied to the question: a residual reference to a deleted artifact may be the only surviving trace of *why* the artifact existed; deleting that trace closes off future archaeology. The sentence "the doc mentions Y, and Y was deleted three months ago in PR #842" is itself a piece of subtle context.

---

## Sub-questions the corpus does not answer

The user's question has five sub-parts. Honest gap accounting:

1. **Stale-comment problem (Fowler / Code Complete / Beck).** Corpus has the citations but **not** the text. Cannot quote. The literature exists; this corpus has not ingested it.

2. **Broken-windows / boy-scout-rule tension.** **No corpus coverage.** Pragmatic Programmer (Hunt & Thomas), the original "broken windows" software metaphor (Martin's *Clean Code*), and Beck's "leave the campsite cleaner" are not in the corpus in any form — not even as stubs. This is a real gap.

3. **Silent scope-shrink in documentation cleanups.** **No corpus coverage in either direction.** I am not aware of a named treatment of this specific failure mode in the corpus or in the broader literature surfaced by adjacent entries. The closest in-corpus analog is the Anthropic compaction warning (passage 6) — but that is about LLM context, not human prose. Treat this as a potentially novel observation worth naming explicitly rather than expecting prior literature to back it up.

4. **RFC-style governance (IETF / PEP / Rust RFC) handling of deleted/superseded documents.** **No corpus coverage.** The actual practice is well-known outside the corpus (IETF RFCs are immutable and superseded via "Obsoletes:" / "Updates:" headers; PEPs use Status: Withdrawn / Superseded / Final; Rust RFCs are closed but the file is preserved with a note) — but none of those process docs are in the corpus. The orchestrator should not pretend otherwise.

5. **ADR literature (Nygard 2011, MADR, ThoughtWorks).** **No corpus coverage.** The ADR pattern's standard answer ("supersede, don't delete; link the new ADR to the old; mark the old as Superseded-by") is well-established but not present in this corpus. Real gap.

---

## Staleness flags

- The most-recent in-corpus passage on this topic (Anthropic 2025) is current.
- The SRE Book (2016) is ~10 years old; the postmortem-as-institutional-memory thesis has held up well, so staleness risk is low.
- The stub entries (Fowler 2018, Feathers 2004, Beck 2002) — staleness depends on whether the team treats the question as one where consensus has shifted. On comments-naming-deleted-code, consensus is very stable: clean them up. On the broader question of how much history to preserve in prose, consensus is *not* stable — the rise of git-as-history, ADRs, and "documentation as code" has shifted opinions. Reader should not assume 2002–2018 advice on prose maintenance is current.

---

## One-line summary for the orchestrator

The corpus has the **citations** for the cleanup-favoring side of this question but not the **text**; it has **full text** for the leave-the-trail counterweight (SRE postmortem culture) and for a contemporary nuance (Anthropic on compaction-cost). The user's sub-questions on RFCs, ADRs, and silent scope-shrink are **genuine corpus gaps** — the answer should name them, not paper over them.
