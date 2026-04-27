## Source agent
canon-librarian

## Invocation summary
Orchestrator asked the librarian for corpus passages relevant to handling temporary/side-branch resources that paused-but-live upgrade proposals depend on (options a/restore, b/name-as-superseded, c/park-with-resume-condition, d/codify-rule). Librarian returned `coverage: partial` with 3 supporting and 3 contradicting/complicating passages, plus an explicit gaps list.

## Direct facts
1. [Heilmeier, DARPA, n.d., fetched 2026-04-27, §The Catechism] The catechism includes the questions: "What are the risks? How much will it cost? How long will it take? What are the mid-term and final 'exams' to check for success?" (confidence: direct)
2. [Anthropic, "Core Views on AI Safety" 2023, §Portfolio] "We believe in this kind of 'portfolio approach' to AI safety research… We anticipate that our approach and resource allocation will rapidly adjust as more information about the kind of scenario we are in becomes available." (confidence: direct)
3. [Google SRE Book 2016, ch. 26 §Backups Versus Archives] "The most important difference between backups and archives is that backups can be loaded back into an application, while archives cannot… No one really wants to make backups; what people really want are restores." (confidence: direct)
4. [Google SRE Book 2016, ch. 23 §Branching] "All code is checked into the main branch… most major projects don't release directly from the mainline. Instead, we branch from the mainline at a specific revision and never merge changes from the branch back into the mainline." (confidence: direct)
5. [March 1991 entry] March's "Exploration and Exploitation" is a stub; full text not ingested. The librarian did not quote March directly. (confidence: direct)

## Inferred claims
1. [canon-librarian] Option (c)'s resume condition is a Heilmeier-style "exam" formalized; option (b) without a stated reason fails the catechism silently. (confidence: inferred)
2. [canon-librarian] Both (b) and (c) are portfolio-coherent moves under Anthropic's framing; (a) without re-evaluation against current evidence is the portfolio anti-pattern of acting on stale priors. (confidence: inferred)
3. [canon-librarian] Under SRE's vocabulary, a side-branch resource that live proposals still reference is functionally a *backup* (load-bearing) being given *archive* ergonomics — a storage-tier mistake that (a) corrects. (confidence: inferred)
4. [canon-librarian] Google's branching policy treats branches as one-way exits, not reservoirs; this directly cuts against (c)'s assumption that a side branch is a stable queryable home. (confidence: inferred)
5. [canon-librarian] The Anthropic "rapidly adjust" passage cuts against (d) too: codifying a general dependency-contract rule retroactively from n=2 is premature standardization. (confidence: inferred)
6. [canon-librarian] "Honest negation" is a counter-pressure against the exploitation gradient; (a) is the exploitation move, (c) keeps the option open without re-anchoring. (Inferred from March stub framing, not from March's text.) (confidence: inferred)

## Authority-framed claims
1. "by Heilmeier's own discipline, not a proposal — it is a wish" — underlying claim: a proposal lacking mid-term/final exams is disqualified. Quote present in output: yes (catechism line). Confidence: direct (the catechism), inferred (the disqualification framing).
2. March's framing that "adaptive processes, by refining exploitation more rapidly than exploration, are likely to become effective in the short run but self-destructive in the long run" — underlying claim attributed to March 1991. Quote present in output: no (librarian flags this as the README's own framing, not lifted from the paper). Confidence: unsupported (as a March quote); the librarian was honest that it was paraphrased from the stub README.

## Contradictions surfaced
- Anthropic portfolio (supporting #2) used to justify (b)/(c) over (a) vs Anthropic portfolio (complicating #3) used against (d) — same passage, opposing inferences depending on which option is being evaluated. Not internally contradictory but doubles as both blade and shield.
- SRE backup-vs-archive (complicating #1, pro-(a) "correct the storage tier") vs SRE branching policy (complicating #2, anti-(c) "branches don't merge back, so either main or killed"). Both push against (c) but for different reasons; backup-vs-archive can be read as pro-(a) while branching policy is read as pro-(a)-or-(b) but anti-(c).
- Heilmeier/Anthropic supporting frame (favors (c) with explicit resume condition) vs SRE branching policy (rejects parked-state (c) as the unrecognized position). Direct disagreement on whether (c) is a legitimate portfolio move or a category error.

## Subagent's own verdict (verbatim)
"Partial. Strong on R&D-portfolio framing (Heilmeier, Anthropic, March-stub) and on backup-vs-archive discipline (Google SRE). Thin on RFC/ADR-lifecycle vocabulary specifically… Nothing in corpus on Hickey's hammock-driven development. No Chesterton's-fence treatment, no Ousterhout, no Brooks."

## Gaps the subagent missed
- The librarian flagged its own gaps thoroughly (ADR/RFC lifecycle, Hickey, Chesterton's fence, Ousterhout, Brooks, "kill criteria" as named discipline). No additional gaps detected by the distiller.
- One latent gap the librarian did not name: no corpus source on **reversibility-of-decisions** (Bezos one-way/two-way doors). The (a) vs (b) choice is partly a reversibility question and the corpus apparently has no primary source for it.
- Staleness flag is acknowledged but the librarian does not address whether modern trunk-based-development literature (post-2016) would re-rule on the SRE branching passage. Worth flagging if the orchestrator is going to lean on §Branching as anti-(c).

## Token budget
~720 tokens
