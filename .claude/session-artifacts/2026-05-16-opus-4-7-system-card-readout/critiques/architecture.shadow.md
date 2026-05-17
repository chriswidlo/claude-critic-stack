# Critique — Architecture lens (shadow)

Lane: Sonnet shadow (`critic-architecture-shadow`). Voice, not vote. v2 — post-rework review.

## v1 recap

v1 verdict: `rework`. Two specific items: (1) R2/R3 dependency direction unnamed; (2) stubs absent for F6/F7 in target files. Plus: `subagent-distiller` no-change row failed the frame-challenger's "still works" prohibition.

## v2 assessment

All three rework items addressed and verified against landed text:

**R2/R3 asymmetric dependency direction.** [CLAUDE.md](CLAUDE.md) "Things you must not do" now contains: *"This rule is the invariant; the corresponding implementation lives in outside-view.md ... The rule is enforceable independently of the agent clause."* The [.claude/agents/outside-view.md](.claude/agents/outside-view.md) "Recognized anchor risks" section carries the co-falsifier back-link. Direction is explicit and parent-child, not symmetric peer. v1 objection resolved.

**F6/F7 stubs in target files.** Per repo-changeset.md, HTML comments landed in [.claude/agents/canon-librarian.md](.claude/agents/canon-librarian.md) and [.claude/agents/canon-refresher.md](.claude/agents/canon-refresher.md). Session-id stamp is grep-discoverable. v1 objection resolved.

**`subagent-distiller` no-change row.** v2 strips the "no 4.7 finding implies no change" reasoning and replaces it with a behavioral falsifier ("re-evaluate if distillations lose critical authority-framed-claim flags"). The "still works" claim is gone. v1 objection resolved.

**F2 fail-safe at the right layer.** R5 in CLAUDE.md operates at the comparator-enum layer (halts on `unavailable`), not at the lens-verdict-file layer where the v1 confusion lived. Retirement trigger is named. v1 objection resolved.

## Residual concern (shadow voice, not veto)

**The F2 fail-safe conflates "safety-flavored session" with a concept the orchestrator has no formalized classifier for.** The rule defines "safety-flavored" as *"involves AI-safety affordances (alignment, deception, evaluation, sabotage, or capability-evaluation reasoning)."* This is prose definition applied at orchestrator judgment, not a step-1 classifier output. The requirement-classifier labels are: new / replace / extend / migrate / refactor / investigation. None maps to "safety-flavored." The fail-safe therefore fires — or doesn't — based on unstructured orchestrator discretion, not a deterministic gate. Same structural gap as the original F2 hand-off at the wrong layer, one level up. Bounded because the fail-safe's blast radius is conservative (halts on uncertainty), but the symmetry is uncomfortable.

This concern does not flip the verdict.

## Verdict

**approve**.

Flip condition: if the requirement-classifier is extended with a "safety-flavored" label and the F2 fail-safe rule is updated to reference that classifier output rather than prose, the structural gap closes — improvement, not precondition.
