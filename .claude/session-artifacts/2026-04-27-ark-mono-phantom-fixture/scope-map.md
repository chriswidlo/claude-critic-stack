# Scope map — ark-mono phantom fixture resolution

The requirement is a three-way option choice, not a single new capability. Each option touches the seven primitives differently. Where the relationship is option-dependent, the table records the relationship under each option in the rationale column and assigns the label that holds across the option set the user is most likely to pick. Preservation is flagged explicitly.

## Existing primitives touched

| primitive | source (where it was named) | relationship | one-line rationale |
|-----------|-----------------------------|--------------|--------------------|
| Regression-test artifact at [ark-mono-connector-routing.md](tests/regression/ark-mono-connector-routing.md) (7 acceptance criteria) | user prose; canon-librarian (SRE Ch.17 supports running it) | extend | Option (a) consumes it as input and produces the artifacts it specifies; (b) and (c) leave it intact and unrun. In all three options the file persists; (a) merely activates it. |
| Exemplars directory contract at [.claude/session-artifacts/exemplars/.keep](.claude/session-artifacts/exemplars/.keep) and its "Promotion to exemplar" mechanism | user prose; regression-test artifact | extend | (a) exercises the promotion path for the first time, populating the directory. (b)/(c) leave the directory empty but the contract intact. No option deletes or rewrites the contract. |
| Example slug in [CLAUDE.md line 20](CLAUDE.md) (`2026-04-24-ark-mono-connector-routing`) | user prose | replace | All three options rewrite the slug. (a) replaces with the real promoted directory name; (b) replaces with an existing real session; (c) replaces with any consistent slug. The current value is a phantom and must go regardless of frame. |
| Example slug in [.claude/session-artifacts/README.md line 23](.claude/session-artifacts/README.md) (`2026-04-24-connector-routing-ark-mono`) | user prose | replace | Same as above; the word-order divergence between the two files is the immediate defect. Every option replaces this token. |
| `.gitignore` allowlist rule `!.claude/session-artifacts/exemplars/` | user prose | extend | (a) makes the rule load-bearing for the first time by adding tracked content under that path. (b)/(c) leave it dormant. No option modifies the rule itself. |
| Session-artifacts immutability norm ([README](.claude/session-artifacts/README.md)) | user prose | preserve | All three options are forward-only: (a) writes a new session-artifact and a new exemplar copy; (b)/(c) edit only the doc citations, not historical artifacts. Preservation is the user's stated norm and is the reason option (a) goes through promotion rather than rewriting an existing artifact in place. |
| 12-step workflow itself ([CLAUDE.md](CLAUDE.md)) | user prose | conflict (option-a only) | If (a) is chosen, running the workflow against the regression scenario may produce output that does not match the seven acceptance criteria. That is a primitive conflict between the workflow and the test. (b) and (c) do not invoke the workflow against this scenario, so no conflict arises. See `## Requires decision`. |
| Cleanup punch-list ordering ([2026-04-27-repo-cleanup-punch-list.md](plans/2026-04-27-repo-cleanup-punch-list.md)) — items 6–13 follow this one | user prose | extend | (a) closes item 5 in place. (b) closes item 5 in place with a substitution. (c) closes the doc-divergence half of item 5 and inserts a new dated item; the punch-list grows by one. None of the options reorder items 6–13. |

## Deletion cost (for subsume/replace rows)

- **`CLAUDE.md` line 20 example slug** (`2026-04-24-ark-mono-connector-routing`): callers = one (the prose at line 20 itself); data migrations = none; config surface = none. Cost is purely textual. Risk: if any external doc, agent prompt, or workflow has memorized this exact slug as a reference, it breaks. A repo-wide search for the literal string is the cheap mitigation.
- **`.claude/session-artifacts/README.md` line 23 example slug** (`2026-04-24-connector-routing-ark-mono`): callers = one; data migrations = none; config surface = none. Same shape as above. The two replacements must agree on the new slug or the divergence reappears under a new name.

## Requires decision (conflicts)

- **12-step workflow vs. regression-test acceptance criteria** (option-a only): the workflow is generative and the test is prescriptive. If the user picks (a), the workflow may emit a synthesis whose shape does not match what the test's seven criteria expect (e.g., section names, artifact ordering, decision-log presence). The conflict cannot be resolved before the run; it is a property of running the workflow against a test that was authored before the current workflow shape stabilized. Decision the user has not made: *if the workflow output diverges from the test, does the test get amended (test was wrong) or does the synthesis get rewritten (workflow drift)?* This is upstream of option (a) and should be answered before (a) is selected.

## Preserved primitives with stated reason (non-default)

- **Session-artifacts immutability norm**: preserved because it is the user's explicitly written norm in the README ("artifacts are historical record, do not rewrite") and because all three candidate options can be executed without violating it. The frame-challenger (step 8) is required to challenge this preservation — specifically, to ask whether option (a)'s "promotion to exemplar" step is itself a soft violation (copying a session-artifact into a new location with a new name, even if the original is left intact, may amount to a rewrite under a different filename).

## Primitives the distillations did not name but the query implies

- The naming convention for session-artifact slugs (date + short slug). All three options pick a slug; none of the options state which convention governs the pick. If (b) is chosen, the substituted slug already conforms; if (a) is chosen, the promoted slug inherits from the session id; if (c) is chosen, "any consistent slug" is under-specified and could regress to phantom-shape.
- The relationship between `tests/regression/` as a directory and the exemplars directory. The regression test references promotion into exemplars but the two directories have no enforced lifecycle link. Option (a) creates the first instance of that link in practice; whether future regression tests follow the same pattern is unspecified.
- Whether "cleanup punch-list" items are themselves subject to the 12-step workflow. The current item is being routed through the workflow; items 6–13 may or may not be. This is a meta-primitive (workflow-applicability rule) the distillations did not surface.
