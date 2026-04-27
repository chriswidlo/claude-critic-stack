# Product-lens critique — path-discipline regime (loop 1)

## Verdict: rework

## Frame-level objection

The candidate frames this as "preserve the rule, add a gate." From a product lens, the decision is about what the repo's authoring contract says to its two users — operator and agent — about the consequences of writing a path. Today the contract is: "we ask politely; nothing breaks." The candidate changes the contract to: **"writing the wrong path-style halts the workflow."** That is a *contract change*, not an enforcement upgrade. Contract changes deserve a contract-change framing: who agreed, what the SLA is on rejection-message quality, what the rollback is when the hook itself is broken. **The candidate treats the hook as infrastructure; it is the new product surface, and the candidate has not drafted its UX.**

Sub-objection: the two users are not symmetric. The operator can read a rejection and reason about it; an agent has a fixed context window and may simply re-emit the same write. Assumption 3 names this risk and defers it to the 14-day audit. A product that ships with "we'll find out in two weeks if half our users can use it" is shipped under-tested.

## User-visible consequence

**Operator's first `/upgrade` after this ships will be interrupted by a hook rejection.** Most likely scenario: operator dictates a new entry in a deep subdir; slash-command flow reaches its Write step; `PostToolUse` hook fires and rejects the link form the model naturally produced. The "instant capture" property of `/upgrade` — its core product affordance — degrades from "speak, captured" to "speak, captured, rejected, retry, maybe captured." That is a P99-on-checkout class regression on the most operator-facing workflow in the repo.

Secondary visible consequence: **the rejection message's quality IS the product.** The candidate names `bin/check-path-discipline.sh` but specifies nothing about rejection text. If the message is `regex match on \]\(\.\./`, the operator (and the agent trying to self-correct) gets no actionable signal. The candidate explicitly defers "the exact bash pattern" as "implementation detail; not a frame issue." That is wrong from a product lens — **the rejection text is the entire UX of the gate**.

## Commitments implied (not fairly disclosed)

Once shipped, the candidate locks the operator into:
- A bash script in [`bin/`](bin/) kept in sync with every future authoring surface.
- Three agent-prompt clauses that drift independently. A fourth Write-capable agent later requires remembering to patch its prompt.
- A 14-day audit cadence that the candidate itself flags as fragile while load-bearing on it. **Disclosed-and-undermined in the same document.**
- The rejection-message contract. Once agents learn to self-correct on a particular string, changing that string breaks them. The string is not even drafted yet.

These are line items in the tradeoff table, not framed as ongoing obligations. The operator infers a one-time cost; the actual commitment is a maintenance surface.

## Migration burden

Candidate says "Sweep 7 active-surface violator files into compliance" in one bullet. Does not say:
- **Per-file edit count.** [`upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md`](upgrades/no-brainer/2026-04-26-critics-get-write-tool/README.md) alone has ~10 link sites; six other READMEs unquantified. Plausibly 30–70 link rewrites, not 7.
- **One PR or N PRs.** Silent. One huge PR or N small ones; each has different rollback semantics.
- **Who does the rewrite.** Operator? Agent? If agent, it runs *under the same hook it is trying to satisfy* — first-write-rejection is the median outcome.
- **The LEDGER row.** Step 5 names it; punch-list item 10 also covers it. Two systems claim authority over one fix.

## Product affordances better / worse

**Better:**
- Grep stability holds (preserved, not improved).
- New-author onboarding has hard signal instead of soft norm.

**Worse:**
- `/upgrade` instant-capture: degraded.
- Editor click-navigation from subdirs: explicitly accepted as lost. Mitigated "by file-tree + grep" — theoretical mitigation; operator who clicks links in Obsidian is the user this prunes.
- Critic-panel writes (this critique): candidate excludes session-artifacts but hasn't specified how the hook distinguishes path-globs at the boundary.

## Honesty meta-challenge response is not falsification

Frame-challenger's honesty meta-challenge is the load-bearing concern. Candidate's response — *"the signal that it isn't post-hoc rationalization is that I made the rule harder on myself"* — is **not evidence**. Self-imposed friction is *consistent* with rationalization (sunk-cost reinforcement). When the most rule-aware author in the system violates the rule on first contact with a new surface, **the rule has failed a usability test**, and the right response is to redesign the surface, not to add enforcement. Option D (move clause 2 out of CLAUDE.md, distribute to four authoring surfaces) is the design-response; Option A modified is the enforcement-response. Candidate chose enforcement and dismissed Option D in two sentences.

## What flips the verdict to approve

The candidate specifies:
- (a) the exact rejection-message text and how an agent is expected to recover from it,
- (b) a one-PR-or-N decision on the migration with per-file link-site counts,
- (c) a rollback path if the 14-day audit comes back red — including who turns the hook off and how.

Without those, this ships a contract change with no UX spec.
