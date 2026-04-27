# Candidate recommendation v2 — folder-shape depth bug fix (item 2)

**Rewrite of [candidate.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/candidate.md) after critic-panel rework.** Addresses architecture, operations, and product flip-to-approve conditions from [critiques.md](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/critiques.md). Lens objections in hand, not defended.

## Position (revised)

**Ship a script — not 27 hand-edits — that performs the rewrite, runs a resolution check, and is the verification artifact for both item 1 and item 2. Bundle items 2 + 3 in one commit only if the script can act on both edit classes; otherwise keep them as two commits in one PR. Wait for item 1 to commit. Do NOT mutate the punch-list with new entries; surface r-and-d-lab-thesis as a one-line note in the commit message and let the operator decide where to file it.**

The work is:

1. **Wait for item 1** to commit (CLAUDE.md updated, `.claude/commands/upgrade.md` updated). Architecture's "direction is wrong way" objection stands; addressing it would require an item-2 ship under Option B's literal form to pressure item 1, which the candidate-v1 already declined and the v2 still declines on the grounds the operator has not asked for that demonstration.

2. **Author `bin/check-path-discipline.sh`** with three modes (so it serves item 1's CI need, item 2's pre-commit check, and the inbound-link audit architecture flagged):
   - `--style` — grep for residual `\.\./\.\.` chains and bare absolute / `~/`-prefixed paths in non-session-artifact markdown. (Architecture invariant 1 + 5; operations observability gap.)
   - `--resolve <files...>` — for each markdown link in the named files, resolve the target relative to repo root under Option A and verify the file exists in HEAD. (Architecture invariant 1 — the missing "resolution" half. Operations §1 — typo detection.)
   - `--inbound <files...>` — grep the rest of the repo (excluding `.claude/session-artifacts/`) for inbound links to the named files; report the set so the rewriter can verify anchor stability. (Architecture invariant 2 — anchor stability; invariant 5 — inbound-link audit.)
   
   This is the **shared verification regex / contract** architecture invariant 5 named. It also satisfies operations §observability-gap and §coupling-objection by giving item 2 a verification regime that does not depend on item 1 committing.

3. **Author `bin/rewrite-folder-shape-links.sh`** (or a `sed` invocation captured in the commit message) that produces the 27 rewrites mechanically given a target file and a known set of `(broken-form → correct-form)` rules. (Architecture alternative §1 — deterministic diff; operations §cost-at-failure — eliminates the 1-2-typo expectation.)

4. **Run the rewriter on the two punch-list-named files** for item 2's edit class (depth fix); run it on the same two files plus `living-poweruser-knowledge-module/README.md` for item 3's edit class (flat-shape → folder-shape). Two commits if the edit classes diverge in script logic; one commit if both are expressible as the same `(pattern → replacement)` table.

5. **Run `bin/check-path-discipline.sh --resolve` on the edited files** before commit. Fail-closed: any unresolvable link blocks the commit. (Architecture flip-condition (b); operations flip-condition (a).)

6. **Run `bin/check-path-discipline.sh --inbound` on the edited files** before commit. Report the count of inbound references to the operator. If non-zero, manually verify anchor stability for any `#fragment` references. (Architecture invariant 2.)

7. **In the commit message:**
   - Name items 2 and 3 closed.
   - State explicitly: *"Bundling-by-colocation is a one-time exception for items 2+3, not precedent for items 6 or 7."* (Product flip-condition (b).)
   - Surface the r-and-d-lab-thesis mixed file as: *"Out-of-scope finding: [`upgrades/profound/2026-04-27-r-and-d-lab-thesis/README.md`](upgrades/profound/2026-04-27-r-and-d-lab-thesis/README.md) has mixed `../../` and `../../../` depths. Operator's call whether to file as a new punch-list item or address inline in a future sweep."* (Product flip-condition (a) — defer without mutating the punch-list.)
   - Reference [`.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/`](.claude/session-artifacts/2026-04-27-folder-shape-depth-bug-fix/).

## What v2 changes vs. v1

| Aspect | v1 | v2 | Lens addressed |
|---|---|---|---|
| Edit method | 27 hand edits | Mechanical rewrite via committed script | architecture §alternative 1, operations §cost-at-failure |
| Verification | Single-sided grep | Resolution check + inbound audit | architecture §weakest-link + invariant 1, 2, 5; operations §1 + §observability |
| `bin/check-path-discipline.sh` ownership | Routed to item 1 | Authored under item 2, consumed by item 1 | architecture §alternative 2; operations §coupling |
| R-and-d-lab-thesis disposition | New punch-list entry appended | Surfaced in commit message; operator decides where | product §commitments §model-change, §flip-condition (a) |
| Bundling precedent | Implicit | Explicit one-time-exception note in commit message and punch-list line | product §flip-condition (b) |
| Inbound-link audit | Not done | `--inbound` mode of the script | architecture invariant 1, 2 |
| Item 1 dependency | "Wait" + assumption #1 | Same wait, but verification regime is no longer coupled to item 1 | operations §coupling |

## What v2 does NOT change

- Still waits for item 1 to commit. Architecture's "direction is wrong way" objection stands; the candidate does not invert the dependency. Reason: inverting requires the operator to request the "demonstrate cost of B" experiment, which they have not asked for.
- Still does not extend to r-and-d-lab-thesis or any other Explore-discovered file. Frame-challenger and product lens both endorse this restraint.
- Still does not touch session-artifact files. The 7 broken-by-policy occurrences remain. Operations §frame-objection-2 (broken-by-policy is still broken at click-time) is acknowledged but not actioned, on the grounds that overriding the sanctity rule is operator territory.
- Still does not modify `.claude/commands/upgrade.md`. That is item 1's plan §Step 2.

## Tradeoffs (revised)

| What we get | What we give up |
|---|---|
| Mechanical rewrite + resolution check eliminates the 1-2 typo expectation. | Authoring the script costs more than 27 hand edits; one-time investment. |
| Verification regime (`bin/check-path-discipline.sh`) is shared with item 1, eliminating the protocol-surface drift architecture flagged. | Item 1's plan §Step 6 needs to be updated to consume the script rather than author its own. (Coordination cost between two plans, but in writing.) |
| Inbound-link audit catches anchor-stability issues before commit. | Adds a step the operator must acknowledge (the audit report). |
| Punch-list contract preserved — no new entries appended by an agent. | R-and-d-lab-thesis finding lives in commit message rather than a tracked location; risk of being forgotten. |
| Bundling-by-colocation explicitly disclaimed; items 6 and 7 cannot pull on this precedent. | Disclaimer is text in a commit message; not enforced mechanically. |
| Rewriter script becomes a reusable artifact for any future folder reshape. | The next reshape may have different edit-class semantics; the script may need extension, not a free reuse. |

## Named assumptions (any of which would flip the recommendation)

1. **Item 1 will commit Option A within the same operator session.** Unchanged from v1. If item 1 stalls, recommendation flips per v1 §assumption-1.

2. **The rewrite is expressible as a deterministic `(pattern → replacement)` table.** This is the v2-specific assumption. If any of the 27 rewrites requires human judgment (e.g., a link whose intended target is ambiguous between two existing files), the script approach degrades to "script + manual exceptions," which reintroduces the typo risk and the verification weakness. Per Explore §wrong-target-but-exists, the 4 `../../README.md` links resolve to `upgrades/README.md` but were intended for repo `README.md` — these are the candidate ambiguous cases. The script must encode the intended target explicitly per-link, not infer from depth alone. If even one link cannot be deterministically rewritten, that link gets hand-edited under the resolution check; the script approach absorbs the exception.

3. **Authoring `bin/check-path-discipline.sh` is in scope.** v2 ships the script with item 2; item 1's plan §Step 6 explicitly named it as *optional, defer if scope creeps*. v2 reverses that: the script is required because operations and architecture both flagged its absence. This means item 2's diff includes a new `bin/` artifact in addition to the three README edits. If the operator considers that scope creep, the recommendation flips to "ship the resolution check as an inline shell snippet captured in the commit message and accept the loss of reuse."

## Named ways v2 could be wrong

- **The script is more code than 27 link edits.** A bug in the script silently corrupts all 27 rewrites at once, where a typo in a hand edit is one wrong link. Operations would prefer atomic per-line risk over script-class risk; v2 trades it. Mitigation: the resolution check catches the script's failures at the same time it would catch a hand-edit typo, so the net failure surface is no larger — but it is differently shaped.
- **Item 1's plan §Step 6 is now coupled to item 2.** v1 separated them on Release-Simplicity grounds; v2 couples them on shared-contract grounds. If item 1's plan author chooses to write their own script anyway, the coupling produces the protocol-drift architecture warned against. Mitigation: v2's write-up is precise enough that item 1 can reference it; if it does not, the orchestrator must surface the coupling at synthesis time.
- **The "out-of-scope finding" in commit message** may be insufficient — the operator may not see it weeks later when triaging the punch-list. Product wanted r-and-d-lab-thesis "either included or genuinely deferred"; v2 picks "genuinely deferred" but the deferral surface is weak. The alternative (include in sweep) was reconsidered: it loses the punch-list-as-finite-contract property in a different way (an agent extends scope beyond what the human authored).

## Cheapest experiment that would reduce the biggest uncertainty

Same as v1 §experiment: **ask the operator directly whether item 1's option-A recommendation is acceptable and can commit before item 2.** v2 adds a second-cheapest: **draft the `(pattern → replacement)` table from Explore.md's per-line tables and surface it for operator review *before* writing the script.** If the table is fully deterministic, assumption #2 holds and the script approach proceeds. If 1-2 entries require human judgment, v2 degrades gracefully to "script + manual exceptions" and the operator knows the failure shape before any code is written.

## Done when (revised)

- Item 1 is committed (CLAUDE.md and `/upgrade` updated per its plan §Steps 1-2).
- `bin/check-path-discipline.sh` exists and runs in three modes (`--style`, `--resolve`, `--inbound`). Item 1's plan §Step 6 is updated to consume this script rather than author its own.
- Three files are edited: `critics-get-write-tool/README.md`, `workflow-docs-scattered-and-stale/README.md`, `living-poweruser-knowledge-module/README.md`.
- `bin/check-path-discipline.sh --resolve` returns clean for the three files.
- `bin/check-path-discipline.sh --inbound` was run; the report was reviewed; any anchor instabilities were addressed.
- Punch-list is updated: items 2 and 3 marked `✅ done <YYYY-MM-DD>`. **No new entries appended.**
- Commit message names items 2 and 3 closed, declares bundling as one-time exception, surfaces r-and-d-lab-thesis as out-of-scope finding, and references the session-artifact dir.
