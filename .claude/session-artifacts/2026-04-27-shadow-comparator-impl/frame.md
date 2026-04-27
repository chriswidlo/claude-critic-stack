# Frame — shadow comparator

## User's framing

"Add a shadow lane to the critic panel so we can detect correlated error."

This frames the problem as an *addition* to an existing system. It treats the panel as the unit of analysis and shadow comparison as a feature of that unit.

## Revision 1 — orchestrator's reframe

The deeper question is: **how do we measure correlated error in our adversarial review system at all?** The shadow-comparator pattern is one instrument for that measurement; it is not the only one and not necessarily the best one.

Implicit optimization in the user's framing: *preserve Opus authority on every lens.* The shadow is a "voice, not a vote." This optimizes for not-degrading-quality, which is a defensive frame.

Alternative optimization: *maximize the disagreement signal, even at the cost of lens authority.* Under this frame, you would intentionally pin different lenses to different models, accept some loss of per-lens quality in exchange for genuine triangulation, and use the panel itself as a research instrument.

The chosen frame for this implementation is the user's defensive frame — preserve authority — because the cost of degrading any one lens's quality on a high-stakes review is plausibly higher than the value of cleaner triangulation. But the alternative is real and should reappear in the open-questions section of the entry.

## What honesty requires

The user's framing is *not* weak in this case. It is conservative-but-honest: it acknowledges Opus is the authoritative reviewer and shadows are signal-only. The reframe doesn't dismiss it; it surfaces what the framing trades away (depth of triangulation) for what it preserves (per-lens quality).
