# Critique — product lens v2 — ark-mono phantom fixture

## 1. User-visible consequence

The day this ships, an operator-as-user opens [CLAUDE.md](CLAUDE.md) and sees `2026-04-26-format-only-state-transition-gate` rendered as the example session id — a real, on-disk, navigable directory. The "this section is unfinished" cognitive-stub signal from loop 1 is gone. A new user-visible artifact appears: [`tests/regression/EXEMPLAR-CONTRACT.md`](tests/regression/EXEMPLAR-CONTRACT.md), which a future agent following a citation from item 5 lands on directly. The contract self-declares as out-of-coverage on its own coverage rule. Right product affordance: a doc that declares its own provisional status is honest.

The punch-list goes from 13 rows with item 5 open to **13 rows with item 5 closed**. No 5b. Strictly better repo-health read.

## 2. Commitments implied

The contract document, once committed, becomes a **de facto template for all future exemplars** — same commitment named in loop 1, but now *visible* and *named* rather than implied by a punch-list row. Visible-and-named is the better property.

The substituted slug becomes citation-load-bearing for two canonical docs. v2 acknowledges this risk; re-citation cost low. Accepted.

The "real slugs only" rule is a new contract on every future CLAUDE.md edit. Cheap to honor; named.

## 3. Migration burden

- **Future agents reading CLAUDE.md**: real slug, real artifact. Strictly better than v1.
- **Operator authoring future exemplars**: must conform to the contract. Five rules to internalize, but bounded and located.
- **Items 6–13 in the punch-list**: no precedent set, because no 5b is created. The bimodal-item question from loop 1 §3 is moot. Resolved.
- **Future agents amending CLAUDE.md's step list**: owe a regression-discipline review per the mtime gate. New burden, but the *correct* burden.

## 4. Product affordances

**Better:**
- Doc-correctness bug closed today; no placeholder anywhere.
- Distiller-step gap is named in the contract and the offending test is flagged on its own page — test no longer silently lies about coverage (loop 1 §5 second frame objection).
- Single citation target for "what does an exemplar look like."
- Punch-list shrinks net.

**Worse:**
- Contract exists *without a successful run behind it* — ceremony-without-baseline risk. Honest, but real.
- mtime forcing function is observable only to operators who know to look. v2 acknowledges and stages a check-script as follow-up. Closer to convention than control.

## 5. Frame-level note

v2 inverted the surface hierarchy correctly: CLAUDE.md is now the primary surface; the contract is the secondary surface where substantive work lives. Loop 1 §5 addressed.

One residual concern: v2's "real slugs only" rule and the mtime-forcing-function are both **doc-enforced controls on a doc-discipline regime**. The CLAUDE.md rule is encountered on every session start (good). The mtime rule is encountered only by an operator who notices file metadata (weak). v2 names this and stages a script. I accept the staging — product surface "rule visible at point of use" is at least partially achieved.

The norm-setting risk from loop 1 — substituting a real slug normalizes "any plausible-looking slug is fine" — is mitigated by step 3's explicit rule. Norm being set is "real slugs are mandatory; fabrication is a defect." Stronger norm than v1's "placeholders are tolerated as honesty signals."

## 6. Verdict

**approve.**

Would change verdict if, on authoring the contract, any of its five sections balloon past assumed scope — at that point flip back toward a split, but with the contract as the home rather than a new punch-list row.
