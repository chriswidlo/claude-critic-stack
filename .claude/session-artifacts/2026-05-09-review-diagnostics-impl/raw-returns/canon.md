# canon-librarian raw return

## Corpus coverage

Partial — the highest-relevance primary sources for this question (Nygard *Release It!* on instrumentation/internals, March 1991 on exploration/exploitation, Feathers on coupling to internals/seams) are all present in inventory but **stub** entries with no ingested body. They cannot be quoted. The Anthropic engineering essays (multi-agent system, building effective agents, context engineering), Google SRE Book Ch.6, and the Heilmeier Catechism are full-body and supply solid coverage of the observability/agent-debugging dimension. Coverage on the *self-measurement / dogfooding-as-confounder* question is **none** in canon — March 1991 is the closest match and is a stub.

## Stub / fetch-blocked entries that are best match for parts of this question

1. **Michael Nygard, *Release It! Design and Deploy Production-Ready Software (2nd Edition)* (2018), ISBN 978-1680502398.** Status: stub, paywalled-no-open-edition. From [canon/corpus/nygard-release-it/citation.yaml](../../../../canon/corpus/nygard-release-it/citation.yaml): "Circuit breaker, bulkhead, steady-state, and other stability patterns originate here." Canonical source on production instrumentation tradeoffs and steady-state / decay tail of operational tooling. *Not ingested.*
2. **Michael Feathers, *Working Effectively with Legacy Code* (2004), ISBN 978-0131177055.** Status: stub. From [canon/corpus/feathers-legacy-code/citation.yaml](../../../../canon/corpus/feathers-legacy-code/citation.yaml): "Introduces the 'seam' concept and characterization tests." Canonical on coupling to internals / hidden seams. *Not ingested.*
3. **James G. March, "Exploration and Exploitation in Organizational Learning," *Organization Science* 2(1): 71–87 (1991).** Status: stub (pdf-manual). From [canon/corpus/march-exploration-exploitation-1991/README.md](../../../../canon/corpus/march-exploration-exploitation-1991/README.md): "adaptive processes, by refining exploitation more rapidly than exploration, are likely to become effective in the short run but self-destructive in the long run." Load-bearing reference for survival × use base-rate question. *Not ingested.*

## Supporting passages

1. **Anthropic, "How we built our multi-agent research system" (2025), §Production reliability and engineering challenges.**
   > "Agents make dynamic decisions and are non-deterministic between runs, even with identical prompts. This makes debugging harder. … Adding full production tracing let us diagnose why agents failed and fix issues systematically. Beyond standard observability, we monitor agent decision patterns and interaction structures—all without monitoring the contents of individual conversations, to maintain user privacy. This high-level observability helped us diagnose root causes, discover unexpected behaviors, and fix common failures."

   Relevance: Direct support for the upgrade entry's frame — diagnostic visibility into multi-agent runs is necessary, and *structural* monitoring (decision patterns, interaction structures) is achievable without reading conversation contents (a published precedent for the AI-blindness claim).

2. **Anthropic, "How we built our multi-agent research system" (2025), §Conclusion.**
   > "When building AI agents, the last mile often becomes most of the journey. Codebases that work on developer machines require significant engineering to become reliable production systems. The compound nature of errors in agentic systems means that minor issues for traditional software can derail agents entirely."

   Relevance: Validates running an adversarial review on a v1 implementation rather than treating "shipped" as terminal.

3. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 6 §The Four Golden Signals.**
   > "The four golden signals of monitoring are latency, traffic, errors, and saturation. If you can only measure four metrics of your user-facing system, focus on these four."

   Relevance: Map onto the workflow: duration ≈ latency, agent-calls ≈ traffic, verdicts ≈ errors, tokens ≈ saturation. The shipped layer covers all four primitives, which is meaningful evidence that v1 instrument-fit is at least *minimally* canonical.

4. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 6 §Worrying About Your Tail.**
   > "When building a monitoring system from scratch, it's tempting to design a system based upon the mean of some quantity: the mean latency, the mean CPU usage of your nodes, or the mean fullness of your databases. … If you run a web service with an average latency of 100 ms at 1,000 requests per second, 1% of requests might easily take 5 seconds. … The simplest way to differentiate between a slow average and a very slow 'tail' of requests is to collect request counts bucketed by latencies (suitable for rendering a histogram), rather than actual latencies."

   Relevance: Bears directly on the instrument-fit reframe. The shipped layer captures `duration_seconds` (a single mean-like number) without per-step or per-phase distribution. Canon is unambiguous that single-number aggregates obscure the failure modes the operator will actually want to debug — the "where did the 10 minutes go" question is not answerable from the v1 instrument by design.

5. **Anthropic, "How we built our multi-agent research system" (2025), §Effective evaluation of agents.**
   > "Start evaluating immediately with small samples. … We started with a set of about 20 queries representing real usage patterns. … However, it's best to start with small-scale testing right away with a few examples, rather than delaying until you can build more thorough evals."

   Relevance: Some support for shipping a 75% instrument now and iterating, *if* the operator runs ≥20 representative sessions. The shipped layer has a sample of one (the dogfooding session). That gap maps onto the dogfooding-as-confounder concern.

## Contradicting / complicating passages

1. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 6 §As Simple as Possible, No Simpler.**
   > "Like all software systems, monitoring can become so complex that it's fragile, complicated to change, and a maintenance burden. … Data collection, aggregation, and alerting configuration that is rarely exercised (e.g., less than once a quarter for some SRE teams) should be up for removal. Signals that are collected, but not exposed in any prebaked dashboard nor used by any alert, are candidates for removal."

   Why this complicates the framing: **Canon contradiction to the SOTA wishlist.** The instrument-fit reframe pulls toward more instrumentation; canon pulls the other way: signals not viewed regularly should be *removed*. A reviewer treating "missing data" as a defect is exactly the failure mode SRE Ch.6 warns against.

2. **Google SRE team, *Site Reliability Engineering* (2016), Ch. 6 §As Simple as Possible.**
   > "It can be tempting to combine monitoring with other aspects of inspecting complex systems… As in many other aspects of software engineering, maintaining distinct systems with clear, simple, loosely coupled points of integration is a better strategy (for example, using web APIs for pulling summary data in a format that can remain constant over an extended period of time)."

   Why this complicates: The shipped layer **violates the loosely-coupled principle directly** — it walks an undocumented internal subagent JSONL layout. SRE explicitly recommends *integrating against formats that can remain constant over an extended period*. Canon says the parser should not exist in its current form; it should call a stable API. The upgrade entry's open question 5 is, per canon, the load-bearing question, not a footnote.

3. **Anthropic, "Building Effective Agents" (2024), §When (and when not) to use agents / Summary.**
   > "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. … Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."

   Why this complicates: A *minor* contradiction to the instrument-fit reframe. Anthropic argues ship the simplest thing, iterate, add complexity only when justified by observed failure. Under this lens, the v1 layer's gap on per-step duration is *correct minimalism*, not a defect; the panel should require evidence of operator pain before queuing per-phase timing.

4. **Anthropic, "Effective context engineering for AI agents" (2025), §Sub-agent architectures.**
   > "Sub-agent architectures provide another way around context limitations. … Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."

   Why this complicates: Names the architectural reason subagent transcripts are stored separately. *Partially defends* the parser's per-subagent file walk (matches architectural intent), but reinforces the SRE point: the layout is a load-bearing detail of the host runtime that the host owner controls.

5. **George Heilmeier (DARPA), "The Heilmeier Catechism" (1975).**
   > "What are the mid-term and final 'exams' to check for success?"

   Why this complicates: Direct objection to the upgrade entry's lifecycle row showing `value-proved: —` and `completed: —`. Heilmeier's catechism makes the absence of a stated success exam a frame-level defect — the implementation shipped without naming the exam that would distinguish "this layer earns its maintenance cost" from "this layer was a sunk-cost monument."

## Gaps

- **Self-measurement / dogfooding traps.** No full-body canon source. March 1991 is the closest match in inventory and is a stub. The dogfooding-as-confounder reframe is largely unsupported by canon and should be marked as such in synthesis.
- **Coupling to internals / Hyrum's Law.** Feathers (stub) and Nygard (stub) are the relevant authors; neither ingested. The "undocumented layout" concern is well-supported by the SRE loosely-coupled-integration principle but lacks a Hyrum's-Law-class canonical statement.
- **Ships-then-decays maintenance tails for instrumentation.** Nygard would be the source; not ingested. SRE Ch.6 §As Simple as Possible covers the forward-looking pruning principle but not the longitudinal decay pattern.
- **Survival × use base rate for internal tooling.** No canon coverage. Must come from outside-view's WebSearch tier, not canon.
- **"Convention-enforced invariants" defense.** No canon source surfaced. Canon-side material is only the SRE simplicity argument, which is silent on whether convention review at every edit is a sufficient substitute for structural enforcement.
