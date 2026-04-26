# Architecture critique — verdict: rework

Persisted by orchestrator from inline return (critic agents lack Write tool — known stack limitation).

## Verdict
rework

## Lens-specific critique

**Three ports as cut do not match the actual coupling shape.** The candidate names ports as (read, write, promotion) but they are not orthogonal: `promotion` is also a read (selecting candidates) followed by a write (into a session-artifact directory), and the read-port specification ("queries are by `discipline`, `type`, `maturity`, or `tag`") embeds the locking-dimension vocabulary directly into the port surface. The port is not a port — it is a leak. Any change to the maturity ladder names or document-type set is by definition a port-breaking change. Cite: locking dimension 4, paragraph "Read port (workflow → lab)."

**Curator-as-sole-writer is unenforceable.** Locking dimension 4 says "Only the `lab-curator` agent... writes new entries. Direct writes from the orchestrator or other agents are forbidden." Tradeoffs immediately concedes: "write port can begin with manual operator writes (no curator) for the first ~10 entries." The architectural commitment is to single-writer; the operational reality is two writers with no merge protocol, no entry-id allocation rule, and no rule for `INDEX.md` line conflicts. Lost-update bug at scale ≥10.

**`lab/INDEX.md` is unspecified.** Named twice in the candidate as the index of all entries, but no specification of who owns it, how it is regenerated, whether it is hand-edited or derived. INDEX.md is the single mutable shared resource across every write path. Same shape as a global mutable singleton: works at N=4 and breaks somewhere between N=20 and N=100.

**Cross-reference vocabulary collapses in practice.** The `refutes` vs `supersedes` distinction is presented as load-bearing, but real entries will carry `supersedes + builds_on` together, or `refutes + supersedes` together. The candidate offers no semantics for compound edges. `relates_to` is `builds_on` with the dependency claim removed — junk-drawer.

**`killed` as terminal-and-reachable-from-anywhere is semantically flat.** A `killed` reached from `integrated` is semantically different from `killed` reached from `raw`: one is a rollback of a shipped capability with downstream `builds_on` dependents, the other is triage rejection. Candidate flattens these. Dependents of an `integrated`-then-`killed` entry point at a tombstone with no specified semantics.

**Type/maturity covariance.** `adr` cannot exist below `integrated` by its own definition. `killed-idea` cannot exist below `tested`. So two of seven types do not span the five-state ladder; the (type × state) matrix has structural holes the candidate does not name. Query "show me all `articulated` entries" silently excludes whole types.

## Weakest link

`lab/INDEX.md` as an unspecified, multi-writer, hand-or-derived shared mutable index. Every port mentions it; no port owns it. At N=4 it is fine; at the candidate's design-scale it is the deadlock point.

## Invariants at risk

1. Single-writer invariant on lab entries — claimed by write-port, immediately violated by manual-writes mitigation.
2. Cross-reference target stability — `builds_on: [path/to/entry.md]` uses paths as IDs, but reversible-dimension-2 (naming) and reversible-dimension-1 (subfolders) both change paths. Every reversible dimension touching paths breaks every cross-reference simultaneously.
3. Monotonic forward promotion — claimed for the ladder, but `killed` from `integrated` is not monotonic, and reversible promotion criteria mean prior promotions sit under different semantics.
4. Type-singleton invariant — assumes one type per entry; not stated, no resolution for cross-type entries.
5. Discipline-tag referential integrity — discipline tags reference MODULES.md but no validation enforces that an entry's discipline is in the canonical list.

## Coupling and direction concerns

Dependency direction is **inverted relative to volatility**. The lab is supposed to be volatile; the workflow and MODULES.md stable. But the candidate makes the lab depend on MODULES.md by reference at read-time, and makes workflow agents depend on the lab's frontmatter schema. Bidirectional, with the volatile side more volatile than the stable side.

Also: curator depends on lab schema; orchestrator depends on curator (Step 14); curator at write-time may need to read existing entries (to set `supersedes`), depending on the read-port. So curator depends on the same field names it is responsible for writing. Schema migration must atomically update curator and entries — no intermediate state allowed.

Promotion port (lab → workflow) writes into `.claude/session-artifacts/`, governed by the workflow's session-id convention. So lab depends on workflow's session-id allocation. Mutual coupling, not directional.

## Frame-level objection

**The lab is being designed as a peer module to the workflow when it is structurally a capability-overlay on `.claude/session-artifacts/`.** Every "lab entry" is in form a session-artifact that has outlived its session. The (objective + output + boundary) triples for the seven types are exactly what the workflow already produces — `position-paper` is what `frame.md` becomes when promoted; `rfc` is what a `candidate.md` post-synthesis becomes; `adr` is what a `decision-log.md` entry becomes when extracted. The candidate's own self-application proves this: the lab entry *is* a promoted session artifact.

If that is the actual structure, then `lab/` should not be a peer to `.claude/` with its own protocols, schema, and curator — it should be a *promotion target* with the same structure as session-artifact directories, governed by the same conventions, with a single promotion rule: when a session artifact is judged worth keeping, it moves (or is hard-linked) into `lab/` with no schema transformation. Seven document types, maturity ladder, and cross-reference vocabulary all become *views* over an existing primitive instead of new primitives. Locking-dimension count drops from 4 to 1 (the promotion rule); integration protocol drops from 3 ports to 1 (the promote operation).

The candidate did not consider this because the scope-map's `subsume` of `exemplars/` was treated as a deletion-cost question, not as evidence that the existing primitive (session-artifact-promotion) is the lab's actual generic. The frame-challenger surfaced the retrofit frame but did not push it one step further: the prior corpus already has a structure (session-artifact form), and the lab should retrofit that structure rather than coining seven new types.

## Architectural alternatives ignored

1. **Lab as a promoted-session-artifact view.** One locking primitive (promotion rule); existing session-artifact form is the entry form; types become tags or filename suffixes.
2. **Lab as a query-only index over distributed entries.** Entries live where they were born (session-artifacts, plans, regression, pages); lab contains only INDEX.md and a query agent. No write-port, no curator-as-monopoly, no path-stability invariant.
3. **Lab as an event log with materialized views.** Each lab event (created, matured, refuted, superseded, killed) appended to a single chronological file; types and states reconstituted by replay.

## What would make this approve

Three concrete deltas:

1. **Specify `INDEX.md` ownership and regeneration semantics.**
2. **Make cross-reference targets stable IDs (slugs), not paths.** `builds_on: [<slug>]` with INDEX mapping slug → current path.
3. **Resolve type × maturity covariance.** Either name valid (type, state) pairs as a sparse matrix, or admit the ladder is type-conditional.

If those three land, the architectural objections collapse to the frame-level objection alone, and the frame-level objection becomes a question for the operator (peer module vs. capability-overlay). Verdict moves to approve.
