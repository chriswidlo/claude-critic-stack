# Workflow: architecture review

The default routing when a user brings a design question to this stack. The `CLAUDE.md` at the stack root tells Claude to follow this.

## Steps

### Step 0 — Triage
Decide whether this is a *decision* question or a *factual* question.

- **Factual** ("what does paper X say about Y", "what is the definition of Z") → route directly to `canon-librarian`. Skip the rest.
- **Decision** ("should we", "how should we", "is this the right way to") → run the full workflow below.

If ambiguous, ask the user which they want. Do not guess.

### Step 1 — Reframe
Restate the question in at least one framing the user did not use. Name:
- What the user appears to be optimizing for
- At least one alternative thing they might want to optimize for instead
- Whether this reframing changes the likely answer

Present the reframe to the user. Proceed even if they don't respond — the reframe is for the record and for the agents downstream.

### Step 2 — Outside view (parallel with step 3)
Invoke `outside-view` with the question and the user's stated constraints.

### Step 3 — Canon retrieval (parallel with step 2)
Invoke `canon-librarian` with the question.

*Run steps 2 and 3 in parallel via the Agent tool — they are independent.*

### Step 4 — Candidate recommendation
*You* (the main Claude) produce a candidate recommendation, drawing on:
- The reframe from step 1
- The outside-view forecast from step 2
- The canon retrieval from step 3

Structure the recommendation as:
- **Position:** one sentence.
- **Tradeoffs accepted:** what this recommendation gives up, and why that's acceptable.
- **Assumptions:** at least three things this depends on being true.
- **Conditions for rejection:** at least three things that, if true, would flip the recommendation.

### Step 5 — Critic
Invoke `critic` with the full candidate recommendation from step 4, the outside-view output, and the canon retrieval.

### Step 6 — Rewrite if needed
If the critic returned **reject** or **rework**, do not argue. Rewrite the recommendation incorporating the critic's points. If you believe the critic is wrong on a specific point, say so explicitly and state why — but default to updating.

Optionally re-invoke the critic on the rewrite. Stop when verdict is **approve** or when further iteration is producing diminishing returns (usually 2 rounds).

### Step 7 — Synthesis to user
Present to the user, in this order:
1. **The reframe** from step 1.
2. **The outside-view verdict** — reference class, base rate, position, typical failure mode.
3. **Canon passages** — supporting *and* contradicting, as returned.
4. **Your post-critique recommendation** — explicitly labeled as post-critique.
5. **Named uncertainties** — at least three things you don't know that would change the answer.
6. **The cheapest experiment** that would reduce the biggest uncertainty.

Do not collapse these into a single flowing paragraph. The user benefits from seeing each frame separately — the structure is part of the output.

## When to deviate

- User says "quick take" → skip to a compressed version of step 4 only, flag that you're bypassing the structure.
- User is exploring, not deciding → run reframe and canon only; skip critic (critique during exploration suppresses useful bad ideas).
- User asks for implementation, not design → this is the wrong stack; tell them so.
