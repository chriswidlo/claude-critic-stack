# Author attribution for community plugins

| Field | Value |
|---|---|
| 📌 **title** | Author attribution for community plugins |
| 🎯 **tier** | 🌿 normal |
| 👤 **author** | collaborative |
| 📅 **created** | 2026-04-26 |
| ⚡ **catalyst** | Session `2026-04-26-karpathy-skills-adoption`. The outside-view distillation said: *"if the marketplace plugin is from a recognized authority, the verdict flips from 15–25% durable to 50–70% durable."* The plugin in question (forrestchang/andrej-karpathy-skills) bundles content authored by Andrej Karpathy and packaged by a third party. The workflow never disambiguated whose authority is the relevant authority — the *content* author (Karpathy, recognized in LLM/coding circles) or the *plugin packager* (forrestchang, no public track record on Claude Code conventions). The verdict-pivot was left dangling. |
| 💡 **essence** | Community plugins typically have at least two authors: the content originator and the packager. Their authorities are different — sometimes orthogonal. The reference-class forecaster currently treats "the plugin's author" as one entity. For community-distributed content where someone else's words are bundled by someone else's plugin, this collapses two distinct credibility signals into one. |
| 🚀 **upgrade** | The outside-view subagent's contract should ask, when forecasting community-plugin adoption: *"who authored the content, and who packaged the distribution? Are they the same entity? If different, which authority is load-bearing for this decision?"* Two-attribution disambiguation, written once into the contract, applied every time a community plugin shows up. |
| 🏷️ **tags** | outside-view, community-plugins, attribution, reference-class |

| 🌱 created | 🔬 spiked | 📋 prepared | ✅ accepted | ⚙️ run-through-repo | 🔨 implemented | 💎 value-proved | 🏁 completed |
|---|---|---|---|---|---|---|---|
| 2026-04-26 | — | — | — | — | — | — | — |

## Table of contents

- [The two-author pattern](#the-two-author-pattern)
- [Why authority asymmetry matters](#why-authority-asymmetry-matters)
- [The contract addition](#the-contract-addition)
- [Where the model breaks down](#where-the-model-breaks-down)

## The two-author pattern

Modern community plugins frequently look like:
- **Content origin:** an author with domain authority (a tweet, a blog post, a paper, a published opinion).
- **Packaging:** a different author who turns the content into installable form (a marketplace plugin, a CLI tool, an extension).

The two are often not the same entity, often have different track records, and often have different incentives. A high-authority content originator with an unknown packager produces a different adoption profile than a low-authority content originator with a major-platform packager (Anthropic, Microsoft) doing the distribution.

The karpathy plugin is one example. There are many others: dotfile repos that wrap published shell-config patterns; npm packages that wrap algorithms from research papers; AI-prompt collections that bundle paid-newsletter content. In each case, the credibility signal is split.

## Why authority asymmetry matters

The outside-view forecaster's contradicting reference class ("canonical-from-authority" — 50–70% durable) hinges on author authority. If "author" is collapsed to one entity, the forecast resolves to whichever authority is most visible. In the karpathy session, the visible name was Karpathy (high authority), and the implied verdict-flip was nearly invoked — except that the *packager's* authority (no track record) is what determines distribution-channel reliability, maintenance follow-through, version-bump discipline.

The two authorities answer different questions:
- **Content authority** answers: *is this content worth listening to?*
- **Packaging authority** answers: *will this distribution channel be maintained, version-stable, and not abandoned?*

A high-content / low-packaging plugin is a fork-and-internalize candidate (take the words, drop the channel). A low-content / high-packaging plugin is a fashionable nothing. A high/high is the canonical-class case. A low/low is an obvious skip.

## The contract addition

Append to `outside-view.md`'s contract, in the section that handles community plugins:

> When forecasting adoption for a community-distributed artifact, identify both:
> 1. **Content origin** — the entity that authored the substantive content being bundled (regardless of who repackaged it).
> 2. **Packaging entity** — the entity responsible for the distribution channel (the plugin author, the marketplace owner, the maintainer of the install path).
>
> If they are the same entity, proceed normally — the plugin's authority equals the entity's authority.
>
> If they are different, treat the two authorities separately. Estimate the reference class for content authority (does the content move behavior under the assumption it is read?) and for packaging authority (does the channel deliver the content reliably, with maintenance, with version stability?). Surface both estimates in the forecast. Do not collapse to a single "the plugin's author" judgment.

This adds maybe 50 tokens to the forecaster's output and one extra disambiguation step. It is cheap and the failure mode it prevents is a real one — choosing adoption based on the wrong authority's reputation.

## Where the model breaks down

There are edge cases:
- The packager *is* the maintainer of the content's official distribution (Anthropic packaging Anthropic content). Then there is one authority, even if the surface looks like two.
- The content is so old / so well-known that "content author" is mythological (a tweet from 2026 has clear authorship; a "wisdom from the Unix philosophy" snippet does not). Authority for the content collapses to "field consensus."
- The plugin is a wrapper for an officially-supported convention (eslint-config-airbnb wrapping the Airbnb style guide). The content authority is Airbnb-the-organization; the packager is whoever ships the npm package; both can be high.

These are edge cases worth noting in the contract, not reasons to drop the disambiguation.
