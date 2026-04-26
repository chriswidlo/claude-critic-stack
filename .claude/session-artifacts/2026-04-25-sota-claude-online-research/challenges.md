# Frame Challenges

## Frame as given

The orchestrator's working frame is: *"the minimum architecture that gives a single user defensible research output, with citation verification as the hard gate."* The optimization target is auditability per claim; the verb is **compose** (Claude-Code-native primitives + a hosted engine treated as untrusted high-recall input + a CitationAgent re-fetch loop). The frame implicitly treats fragmentation across vendors as a problem to be neutralized by owning the verification layer locally.

## Alternative frame

Reframe as **"choose a research counterparty, not an architecture."** The frame the orchestrator did not use: online research output is a *contract* between the user and a producer, and the producer is either (a) a vendor (Anthropic Research, OpenAI DR), (b) the user themselves with the LLM as instrument, or (c) a domain expert the LLM helps the user reach. Once you pick the counterparty, the architecture follows mechanically; if you pick the architecture first you commit to "user as quality engineer" before knowing whether they have the time, the calibration, or the consequence-tolerance to play that role. The verb shifts from *compose* to *delegate-with-recourse*: the design question becomes **what is my recourse when the output is wrong**, not **what tool do I bolt on to make it less wrong**.

## Condition under which the current frame is wrong

The current frame is wrong if the user's downstream decision is reversible and low-stakes (e.g., choosing what to read this week, scoping a side project) — at that consequence level the cost of running CitationAgent + critic-panel + version-pinning exceeds the cost of acting on a 10%-wrong hosted answer and noticing within a day, and the auditability optimization becomes pure ceremony.

## Challenges to scope-map preservations

- **B1/B2 (WebSearch + WebFetch) preserved as the auditable retrieval path.** The stated reason is "hosted engines are opaque, the verifier needs something to re-fetch against." The reason is weak because *the verifier re-fetches the URLs the hosted engine already returned* — so the auditable path is the hosted engine's citation list, not WebSearch/WebFetch as independent retrieval. Preserving B1/B2 as if they are an alternative retrieval path conflates "verify what the engine cited" with "do the search ourselves," and biases the downstream answer toward **redundant retrieval that doubles cost without changing the citation set**.

- **B3 (subagents) preserved on the 80%-of-variance-from-token-budget claim.** That claim is from the same Anthropic essay that the canon-librarian flagged as the source-diversity contradiction; preserving subagents on its strength bakes Anthropic's preferred architecture in. The reason is weak because token-budget-as-explanation predicts that *any* method of spending more tokens (longer single-agent runs, deeper Reflexion loops, larger context windows) would do equally well — but the preservation specifically locks in fan-out. Bias: **multi-agent theater**, where parallelism is the aesthetic even when a longer single-agent run with the same token budget would be cheaper to debug.

- **B8 (Routines) preserved to address refresh half-life.** The reason is weak because the frame named refresh half-life as a *user* concern, not a system concern — a monthly routine refreshes the canon, but the user still has to read the refresh and decide whether to re-architect. Preserving Routines bakes in the assumption that the user wants a long-lived system rather than a one-shot answer they discard. Bias: **infrastructure-for-a-user-who-may-not-return**, building a refresh loop for a question that may have been situational.

- **D1 + D2 (5-axis rubric + CitationAgent) preserved as the dominant lifter.** This is the load-bearing preservation and the most dangerous. The stated reason is "outside-view names the citation verifier as the single dominant lifter above base rate." That reason is weak in three specific ways: (i) the outside-view's effectiveness number for the verifier is *unquantified* (its own gap #3), so "dominant lifter" is conjecture; (ii) the rubric and CitationAgent are both Anthropic-authored, evaluated on Anthropic's own internal eval — there is no third-party replication; (iii) the verifier checks **groundedness of cited URLs**, not **whether the cited URL actually supports the claim** — a URL can be reachable, on-topic, and still misquoted or cherry-picked. Bias: **false-confidence-via-green-checkmark**, where a passing verifier signals trustworthiness the verifier did not actually establish, and the user lowers their own scrutiny in proportion.

## The citation-verifier as false god

Beyond the preservation challenge: the hard-gate decision itself deserves a frame-level objection. A verifier that re-fetches URLs and scores groundedness is solving the *easy half* of citation hallucination (does the URL exist and roughly match) and leaving the *hard half* untouched (does the source actually say what the agent claims it says, in context, without omission). If the verifier is itself an LLM call, it hallucinates at a rate correlated with the original agent — same model family, same blind spots — so the gate's failure modes are not independent of the producer's failure modes. The hard-gate framing assumes verifier errors are uncorrelated with producer errors; if they are correlated, the gate is **theatre that licenses higher producer trust without earning it**, and the user is worse off than with no gate plus explicit "this is unverified" framing.

## Challenge to the classifier label

N/A for substantive re-classification, but worth flagging: the classifier labeled this *investigation* with research-theater as the named bias. The current composition (slash command + hooks + verifier + Routines) has quietly drifted toward a *new-build* answer — seven primitives wired together, a refresh loop, a decision-quality wrapper. If the label is taken seriously, the right artifact is a one-page decision memo, not an architecture. The drift from "investigation" to "build" is itself the research-theater the classifier warned about.

## The strongest case for the boring answer (hosted-only)

**"Just use Anthropic Research or OpenAI Deep Research, accept 5–15% error, move on."** This is correct for the user whose decisions are (a) reversible within a week, (b) cross-checked by another human before consequence, (c) about exploration rather than commitment, and (d) high-volume enough that per-query overhead matters. For this user — call them the *scout* — the hosted engine is at base rate by construction (outside-view), the 5–15% error is detectable on the second read, and every minute spent on CitationAgent is a minute not spent reading more sources. The composition the scope-map proposes is *malpractice* for this user: it converts a 30-second query into a 10-minute pipeline run for an error reduction the user could not measure.

## The strongest case for the opposite boring answer (human-as-researcher)

**"Agentic web research is fundamentally low-ceiling — Devil's Advocate hits 23.5% on WebArena; the right answer is human-in-the-loop with the LLM as literature scout, not autonomous researcher."** This is correct for the user whose output is (a) load-bearing for an irreversible decision, (b) going to be read by adversaries (regulators, reviewers, opposing counsel, a board), (c) in a domain where the user has enough expertise to recognize a wrong answer but not enough time to find the right one unaided, and (d) where being wrong is more expensive than being slow. For this user — call them the *principal* — the autonomous-pipeline framing is a category error: the LLM's role is to surface candidate sources, summarize them faithfully, and *stop*, while the user does the judgment work that no verifier can do (does this source say what the agent claims, in context, without omission). The composition the scope-map proposes is *also malpractice* for this user, because the green checkmark from CitationAgent will be cited by the user as evidence of rigor it did not establish.

The middle case the scope-map serves — defensible-output-for-a-single-user-who-is-not-quite-a-principal — may be a real user, but the frame-challenger's job is to note that *this middle is narrower than the frame implies*, and most actual users fall to one side or the other.

## Frame-level objection the orchestrator should carry forward

**The composition optimizes auditability for a user whose consequence-tolerance has not been established; if the user is a scout, the composition is overhead, and if the user is a principal, the verifier's green checkmark is false confidence — the generator must name which user this is for, or the recommendation is unfalsifiable.**
