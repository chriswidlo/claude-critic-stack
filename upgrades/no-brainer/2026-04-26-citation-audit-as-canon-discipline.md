# Citation-audit as a `canon-librarian` discipline

| Field | Value |
|---|---|
| 📌 **title** | Citation-audit as a `canon-librarian` discipline |
| 🎯 **tier** | ✅ no-brainer |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | The operator's opening retrospective: *"Outside-view cited very specific numbers (78–94% citation accuracy, 3–13% fabricated URLs from arXiv 2601.09688, 2601.22984). I cannot confirm those papers exist or those numbers are correct from inside this session. The whole edifice rests on a WebSearch → subagent → distillation → me chain, and any link could be hallucinated. I treated those numbers as load-bearing without flagging the audit gap."* The librarian and outside-view return citations the orchestrator treats as evidence; nothing verifies they exist. |
| 💡 **essence** | Every cited source returned by `canon-librarian` and `outside-view` should carry one of three explicit confidence markers: `verified` (the source exists in canon/corpus/ or has been fetched in this session), `asserted` (the source is named but unverified — the agent has not confirmed it exists), or `cached` (cited from training data without verification). Currently every citation is implicitly `asserted` and the orchestrator treats them as if `verified`. |
| 🚀 **upgrade** | Citations become auditable. When outside-view returns "78–94% per Smith et al. 2023, arXiv 2301.09234" the orchestrator can see whether that's a verified source (read from canon/corpus/), an asserted-but-unverified one (the agent named it from training memory), or cached. Hallucinated paper IDs become visible at the citation site, not after the fact. The chain of evidence the orchestrator builds on becomes calibrated to source reliability. |
| 🏷️ **tags** | retrieval, canon, citation, audit, verification, hallucination |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The format change](#the-format-change)
- [Why this is no-brainer](#why-this-is-no-brainer)
- [Pairs naturally with the epistemic critic lens](#pairs-naturally-with-the-epistemic-critic-lens)

## The format change

Add to `canon-librarian.md` and `outside-view.md` instructions, in the output-format section:

> Every cited source MUST carry one of three confidence markers, attached to the citation:
> 
> - **`verified`** — the source has been confirmed to exist via canon/corpus/ inspection or live WebFetch in this session. The agent has touched the source.
> - **`asserted`** — the source is named (with title, author, date, identifier) but has not been verified in this session. The agent is asserting from training memory without confirmation.
> - **`cached`** — the source is referenced loosely, without a specific identifier; the citation is paraphrasing what the agent recalls without claiming a specific paper or URL.
> 
> Format: `[Author, Title (Year), <verified|asserted|cached>]`. Numerical claims (e.g., "78%") that depend on a source must inherit the source's marker explicitly.

The librarian's existing canon-grounded retrievals are by definition `verified`. Web-fetched results are `verified` if fetched in this session, `cached` if from training. Outside-view's web-confirmed sources are `verified`; recalled-from-training citations are `asserted` or `cached` depending on specificity.

## Why this is no-brainer

The change is text in two agent instruction files. No new tooling, no new agents, no workflow restructure. The discipline forces honesty in the agents' own writing rather than asking the orchestrator to second-guess every citation.

The cost is small (two file edits, ~10 minutes). The value is uncontroversial: the operator's retrospective named hallucinated arXiv IDs as a load-bearing audit gap. Adding the markers makes that gap visible at the source.

## Pairs naturally with the epistemic critic lens

The proposed `critic-epistemic` lens (a different upgrade entry, currently not yet captured but referenced elsewhere) would be the panel-level enforcement of this discipline. Lens reads citations in the candidate, checks confidence markers, flags entries where the candidate treats `asserted` citations as load-bearing without acknowledgment.

The two upgrades — librarian/outside-view discipline + epistemic lens — together close the audit chain. Either alone is a partial fix; together they catch the same class of bug at two layers.

This entry is the upstream half. The downstream half (epistemic lens) is itself an outlandish-leaning upgrade because the lens prompt design is non-trivial; the librarian discipline is the no-brainer that should land first.
