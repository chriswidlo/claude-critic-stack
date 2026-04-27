# Frame challenges — shadow comparator

## Alternative frame

**The panel should not exist.** A single Opus critic that explicitly cycles through the architecture / operations / product lenses inside one prompt is cheaper, equally correlated, and simpler. The three-lens design's value is style-diversity, not model-diversity; the shadow proposal admits this by adding diversity at the model layer. If model-diversity is the missing ingredient, lens-multiplication was never the right axis.

Under this frame, the right move is: collapse the three lenses to one Opus critic with explicit lens-cycling, then add an actual cross-family shadow at the critic level (one Opus, one Llama or Gemini). Total cost: 2 invocations instead of 6. Triangulation: genuine.

## Condition under which the current frame is wrong

If the disagreement-rate between an Opus-architecture-lens verdict and a Sonnet-architecture-lens verdict is below ~5% on a sample of 20+ real candidates, the same-family shadow is performative diversity — adds cost, adds no signal. The current frame (preserve three lenses, add same-family shadow) collapses.

The cheapest experiment to settle this: run the next 20 critic-panel sessions with `SHADOW_PANEL=1`, log the comparator's `agree | partial-agree | disagree` per lens, and compute the disagreement rate. If <5%, the proposal failed value-proof and the entry stays at 🩺/🔖 without ever reaching 💎 value-proved.

## Challenge to a preserved primitive

The scope-map preserves `frame-challenger` unchanged. That preservation is suspect. If the panel's value is triangulation, the frame-challenger's role (devil's-advocate on the frame, single-agent, single-model) is also correlated-by-default. Why doesn't `frame-challenger` get a shadow too? Either because its output is more robust to model variance (a claim with no evidence), or because the proposal stops short of where its own logic leads. Worth flagging in the next iteration.

## What the challenger declines

The challenger does not assert "do nothing." Doing nothing — leaving the panel correlated by default and never measuring — is the worst option, because it leaves the proposal's own claim (correlated blind spots exist) untestable. Some shadow is better than none, even if same-family.
