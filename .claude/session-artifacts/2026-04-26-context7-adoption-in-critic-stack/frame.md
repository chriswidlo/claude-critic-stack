# Frame

## Revision 1

### User's implicit framing
"Context7 is hot; this repo runs on LLM agents; therefore we should evaluate adopting it." The optimization hidden in this framing is **capability accretion** — assume the new capability is good, debate the integration shape.

### What the user is implicitly optimizing for
Two things, in tension:
1. **Capability completeness** — don't leave value on the table when a design question is library-specific.
2. **Discipline preservation** — don't weaken the anti-anchoring mechanisms (canon-first, distillation, frame-challenge) that justify the stack's existence.

### Alternative framing the user did not pose
**"What is the actual base rate of design questions routed through this stack that are bottlenecked on missing library-API knowledge?"**

This reframe is biased by the classifier's `extend` default but pushes against it. If that base rate is low (estimate: design questions in critic-stack are about *patterns, tradeoffs, invariants* — not API surfaces — so the rate is plausibly <10%), then *every* adoption shape (B/C/D/E) is solving a problem the system rarely has. The right answer collapses to A (do nothing) or E (out-of-band Skill) and the integration discussion is moot.

A second alternative: **"Is Context7 a category mismatch?"** Context7's value is in the *coding* loop (write code → hit wrong API → fix). The critic-stack's loop is *evaluative* (read design → critique → propose). The two loops have different failure modes. Pattern-matching from "AI dev tool" to "this AI repo" may be the actual error.

### Frame I am committing to for steps 3–11
**Primary:** "Is the marginal anti-anchoring cost of injecting library docs into this stack greater or less than the marginal value to design questions, given the stack's actual question distribution?"

**Sub-question:** "If the answer is 'sometimes yes,' what is the *minimum-discipline-cost* integration shape?"

This frame intentionally privileges discipline preservation over capability accretion, because the stack's whole reason for existing is the discipline. If the discipline is fungible, the stack is fungible.

### Honest friction with the user's framing
The user phrased this as an upgrade question ("on top of what you did here … add it as an upgrade"). That phrasing presupposes adoption. The reframe explicitly puts non-adoption (shape A) back on the table as the default, and adoption shapes have to earn it.
