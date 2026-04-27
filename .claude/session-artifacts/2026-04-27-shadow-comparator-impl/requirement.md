# Requirement classification — shadow comparator implementation

Driving entry: [upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md](upgrades/profound/2026-04-26-critic-panel-correlated-by-default/README.md)

## Primary label

**`extend`** — extend the existing critic-panel primitive with a shadow lane and comparator. The three Opus lenses stay; new agents are siblings, not replacements.

## Default frame for `extend`

The `extend` label biases toward "minimum-viable addition without disturbing existing surfaces." That bias is useful for keeping change scope tight, but risks under-counting the case for a deeper redesign of the panel as ensemble triangulation rather than three named lenses.

## Frame bias to surface explicitly

`extend` makes the implementation *additive*, which means the existing panel's three-lens framing becomes load-bearing for any new layer to fit underneath. If the right answer is "redesign the panel from scratch as N variable lenses with a comparator", the `extend` framing will not generate it.

## Alternative classification

**`replace`** — replace the three-lens panel with an N-by-M matrix (lenses × models) and a comparator that aggregates. Reframes the panel as ensemble triangulation. More disruptive but possibly correct if same-family-correlation turns out to be the dominant failure mode.

The orchestrator chose `extend` for this pass; if the spike-data on disagreement rates comes back below ~5%, revisit and consider `replace`.
