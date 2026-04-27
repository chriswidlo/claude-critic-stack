# Frame

## Revision 1

### How the user framed it

*"Pick A, B, or C — three options for what to do about the path-discipline rule that has a misworded reason and a 50/50 compliance split."*

The framing is **decision-among-three-presented-options**, biased toward A (presented as conservative, name-checked as "keep clauses 1-5"). The plan document the user wrote leans recommendation toward A.

### What the user is implicitly optimising for

**System legibility for AI readers across time.** The rule was added in commit `5108ed3` alongside the decision to track session artifacts longitudinally. The shared motivation is *make reasoning visible to a human (or AI) reading the repo six months from now without leaking machine-specific paths*. Repo-root style serves that — same token regardless of where a reference lives, no usernames in committed history.

The user's secondary optimisation is **adoption discipline** — they noticed the drift and want to stop it. The plan recommends a slash-command patch as the structural fix.

### Reframe — what else this question could be optimising

**Frame R1.1 — Authoring ergonomics for whoever writes most.**
If the dominant authoring agent is a Claude session (or me) operating from a deep subdir, the "natural" output is file-relative `../` chains. Every rule that fights the natural output is friction that erodes. Reframed: *"who actually writes the most paths, and which style minimises their cognitive overhead per write?"* Under this frame, the answer leans Option B: stop fighting the medium.

**Frame R1.2 — What does the repo *export* (read by external eyes), vs. what does it *use* internally?**
External readers (GitHub web view, prospective contributors) want links that click. Internal readers (the orchestrator agent reading session artifacts) want stable text addresses for grep. These are different audiences with different optima. The current rule treats them as one. Reframed: *"split the rule by surface — public READMEs use one style, internal artifacts use another."* That's a fourth option the user did not name.

**Frame R1.3 — The rule is a symptom of a missing tool.**
The drift exists because there's no automated check at write-time. If a `bin/check-path-discipline.sh` ran in pre-commit, the style choice would become invisible to the author — they'd be told their links are wrong and fix them, regardless of which style was canonical. Reframed: *"the meta-decision is whether to enforce by prose or by tool. Once enforcement is tool-shaped, the style choice matters less."*

### What the user is *not* asking

- "Should the rule exist at all?" — taken as settled by commit `5108ed3`. But step 8 (frame-challenger) should test that.
- "Is grep-stability worth the editor-clickability cost?" — the user assumes yes and recommends A on that basis. The cost has not been quantified.
- "Are there compliance asymmetries — files where the cost of fixing differs?" — the plan treats the 6 drifted READMEs as uniformly fixable. Not verified.

### The honest friction (what I would push back on if not being polite)

The user's plan recommends **Option A** with confidence "medium" and names three signals that would flip them to B. The recommendation is well-reasoned but **may be over-determined by attachment to the existing rule** — option B is presented with `❌` markers on every tradeoff and `✅` markers on only two. That's an uneven presentation. The frame-challenger should test whether B's case has been steelmanned.

Also: the 9-vs-9 split is described as "drift," but it could equally be described as "the rule lost democratic legitimacy among recent authors." Calling it drift presumes the rule is right and authors are wrong. The reverse framing — *the rule is too costly to follow and authors are voting with their fingers* — deserves equal airtime.

### Frame this session will operate under (Revision 1, superseded — see Revision 2)

**Reframed question:** *"Given that the path-discipline rule was added for grep-stability + privacy, and that the 9-vs-9 compliance split signals adoption failure, decide whether the right move is to (i) preserve the rule and fix its enforcement substrate, (ii) replace the rule with one authors will follow naturally, (iii) split the rule by surface, or (iv) replace prose enforcement with tooling enforcement — and verify the choice doesn't degrade the longitudinal-record property the rule was added to protect."*

This is the operator's question with one extra option (R1.2) and one extra lens (R1.3) added.

---

## Revision 2

### What loop 1 surfaced

All three critic lenses returned `rework`, all at frame level, with convergent shape:

- Architecture: this is a **gate-substrate** decision, not a path-style decision. The first hook becomes the template for every future gate.
- Operations: this is a **change-management** decision against a live, self-modifying authoring loop, not a compliance decision.
- Product: this is a **contract** decision between the repo and its two users (operator + agents), not a tooling decision.

The candidate (loop-1 Option A modified) was solving the wrong problem at the wrong altitude. Treating "what enforces clause 2" as the question scoped the candidate to a specific hook + specific exclusion list + specific 14-day audit, when the actual decision shape is *what kind of policy substrate this stack supports, with path-style as the first instance*.

### Revised frame

**The decision is: what is the gate-substrate of this stack, and what is the contract its first instance establishes between the workflow runtime, the operator, and AI agents?** Path-discipline is the inaugural gate — its design sets the precedent for every gate to come (privacy, citation, secret-scan, output-shape, immutability).

This reframe collapses Options A/B/C/D from the operator's plan into a sub-question. The primary question is *substrate*; clause-2 enforcement is a *use case* of the substrate.

### What this frame requires the candidate to address

1. **A named gate-substrate primitive.** Not "a hook" — a *kind of thing* (gate-substrate) of which this is the first instance. Spec: input contract (what does the gate read?), output contract (what verdicts can it return?), failure contract (what does the workflow do when a gate denies?), bypass contract (how does the operator override?), telemetry contract (what does the gate log?).
2. **Per-file or per-section policy declaration**, not directory-prefix exclusion. So the substrate generalises beyond clause 2.
3. **Two-user contract.** Operator-facing UX (rejection message, override path) and agent-facing UX (rejection signal that an agent can self-correct against). Both first-class.
4. **Rollout discipline as part of the substrate.** Warn-only mode → blocking mode is part of how *every* gate ships, not a special case.
5. **A control loop, not just a measurement.** The 14-day audit is a measurement; the substrate must specify what fires automatically when measurement crosses threshold.
6. **Honest treatment of Option D.** Move clause 2 prose out of CLAUDE.md and into the four authoring surfaces; let the gate-substrate enforce the same intent mechanically. The two are complements, not alternatives.

### What this frame still preserves from Revision 1

- Privacy clauses (1, 3, 4, 5) of the rule — uncontested across all loops.
- The longitudinal-record contract from commit `5108ed3` — session artifacts immune from style sweeps.
- The empirical signal from Explore: 100% of post-rule violations are in agent-authored content with no prompt-level path instruction.
- The base-rate concern from outside-view: solo-maintainer rules without mechanical gates decay.

### What's at risk under the new frame

The reframe broadens the question. There's a real chance the substrate spec is too big to settle in one workflow run. The candidate should explicitly name what is in scope for *this* decision and what is deferred to a follow-up that designs the substrate proper. A candidate that tries to ship the full substrate is over-reach; one that ships a clause-2 fix without naming the substrate at all repeats the loop-1 mistake.

### Frame for loop 2 (current)

**Decide the smallest concrete action on path-discipline that (a) does not trap the repo into a substrate-by-precedent it hasn't designed, (b) preserves the privacy + grep-stability properties currently working, (c) addresses the 9-vs-9 compliance gap with a mechanism that survives base-rate scrutiny, and (d) names what would have to be true for a future gate-substrate decision to overturn this one.**

Translation: don't ship the gate. Ship something smaller, name the gate as a follow-up, and instrument the small thing so the substrate decision has data when it happens.
