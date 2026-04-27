# Canon-librarian raw return

## Corpus coverage
Partial. Strong on R&D-portfolio framing (Heilmeier, Anthropic, March-stub) and on backup-vs-archive discipline (Google SRE). Thin on RFC/ADR-lifecycle vocabulary specifically (no "superseded" pattern source like Nygard's ADR essay or IETF RFC process is ingested). Nothing in corpus on Hickey's hammock-driven development. No Chesterton's-fence treatment, no Ousterhout, no Brooks.

## Supporting passages

1. **Heilmeier, "The Heilmeier Catechism" (DARPA, n.d., fetched 2026-04-27)**, [source.txt](canon/corpus/heilmeier-catechism/source.txt) §The Catechism
   > "What are the risks? How much will it cost? How long will it take? What are the mid-term and final 'exams' to check for success?"

   Relevance: An R&D proposal that cannot answer "what are the mid-term and final exams" is, by Heilmeier's own discipline, not a proposal — it is a wish. Option (c)'s **resume condition** is the Heilmeier "exam" formalized; option (b) without a stated reason is the same proposal failing the catechism a second time silently.

2. **Anthropic, "Core Views on AI Safety" (2023)**, [source.txt](canon/corpus/anthropic-core-views-on-ai-safety/source.txt) §Taking a Portfolio Approach
   > "We believe in this kind of 'portfolio approach' to AI safety research. Rather than betting on a single possible scenario… We anticipate that our approach and resource allocation will rapidly adjust as more information about the kind of scenario we are in becomes available."

   Relevance: A portfolio explicitly *expects* re-allocation as evidence arrives. Parking with a resume condition (c) and naming-as-superseded with pointer to the moved resource (b) are both portfolio-coherent moves. Restoring the resource (a) without re-evaluating the proposals against current evidence is the portfolio anti-pattern: re-acting on stale priors.

3. **March, "Exploration and Exploitation in Organizational Learning" (1991)**, *stub entry; full text not ingested* — see [README.md](canon/corpus/march-exploration-exploitation-1991/README.md).

   Per the entry's own framing: *adaptive processes, by refining exploitation more rapidly than exploration, are likely to become effective in the short run but self-destructive in the long run*. The librarian does not quote March directly here; the abstract framing is recorded in the README, not lifted from the paper.

   Relevance: "Honest negation" *is* a counter-pressure against the gradient toward exploitation — i.e., against quietly resurrecting work that the organization has already declined to ship. (a) is the exploitation move (re-use the artifact you already have); (c) keeps the option open without re-anchoring.

## Contradicting or complicating passages

1. **Beedle/Brand/Cunningham et al. — Google SRE Book, ed. Beyer/Jones/Petoff/Murphy (2016)**, [source.txt](canon/corpus/google-sre-book/source.txt) §Backups Versus Archives (ch. 26)
   > "The most important difference between backups and archives is that backups can be loaded back into an application, while archives cannot. Therefore, backups and archives have quite differing use cases… No one really wants to make backups; what people really want are restores."

   Why this complicates the framing: This is the **strongest in-corpus argument for option (a)**. A side branch that a proposal still references is, in SRE's vocabulary, a *backup* (load-bearing, must restore quickly), not an *archive* (audit-only). If the resource is genuinely needed by live proposals, leaving it on a side branch is mis-classified storage — the side branch is being asked to do backup duty while having archive ergonomics. Option (a) isn't sentimentality; it's correcting a storage-tier mistake. Inversely, if the proposals truly don't need the resource, then (b)/(c) should be paired with a positive declaration that the side branch is now an archive — not a deferred backup.

2. **Beyer et al., Google SRE Book (2016)**, [source.txt](canon/corpus/google-sre-book/source.txt) §Branching (ch. 23)
   > "All code is checked into the main branch of the source code tree (mainline). However, most major projects don't release directly from the mainline. Instead, we branch from the mainline at a specific revision and never merge changes from the branch back into the mainline."

   Why this complicates: Google's branch policy treats **branches as one-way exits, not reservoirs**. A "preserved on a side branch" resource that is still being referenced from main is the explicit anti-pattern — branches in this discipline don't merge back. This pushes against (c)'s implicit assumption that the side branch is a stable, queryable home. Either the work belongs on main (a), or it is genuinely killed and the references on main must be cut (b) — the parked-state (c) is the position SRE branching policy refuses to recognize. This is a direct argument against the operator's lean.

3. **Anthropic, "Core Views on AI Safety" (2023)**, [source.txt](canon/corpus/anthropic-core-views-on-ai-safety/source.txt) §Portfolio
   > "We anticipate that our approach and resource allocation will rapidly adjust as more information about the kind of scenario we are in becomes available."

   Why this complicates: The portfolio passage cuts both ways — it argues *against* (d) as well. "Rapidly adjust" is incompatible with locking in a general dependency-contract rule retroactively from a sample size of two. (d) is the premature-standardization risk: a structured field added before the lab knows whether out-of-main references are a recurring shape or a one-time accident. The corpus does not contain Chesterton's fence or Ousterhout directly, but the portfolio principle — keep allocation cheap to revise — gives the same answer.

## Gaps

- **No ADR/RFC lifecycle source ingested.** Nygard's "Documenting Architecture Decisions" (origin of the "superseded by" status) is not in the corpus. IETF RFC 2026 (the "rejected/historic/obsolete" lifecycle) is not in the corpus. The "named-superseded" pattern in (b) cannot be cited to its primary source from this corpus — only inferred.
- **No Hickey "Hammock-Driven Development".** The "decide as late as possible" school is not represented; the tension the operator named between deferral and honest-negation cannot be settled from canon.
- **No Chesterton's fence / Ousterhout / Brooks.** "When to fix one instance vs. write a rule" — directly relevant to (d) — has no primary source in corpus. The argument against premature standardization above is inferred from the Anthropic portfolio passage, not from a refactoring/design canon source.
- **No corpus treatment of "kill criteria" as a named discipline** (Stage-Gate, DARPA program-manager terminations). Heilmeier gives the catechism but not the kill rule. The "honest negation" doctrine the operator cites has no in-corpus primary source — it is the operator's own term.
- **Staleness flag.** The two non-Anthropic foundational sources here are 1991 (March) and 2016 (SRE Book). The portfolio and exploration/exploitation framings are still current; the SRE branching-policy passage predates widespread trunk-based-development orthodoxy and modern monorepo tooling, but the *backup-vs-archive* distinction is not stale — it's a definitional argument, not a tooling claim.
