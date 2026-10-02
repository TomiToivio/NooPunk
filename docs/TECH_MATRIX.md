# NoöPunk regional technology matrix

> **Canonical data:** [`data/world/tech_matrix.json`](../data/world/tech_matrix.json).
> This document explains the model; it does not restate the numbers.
>
> **Status:** author-specified regional worldbuilding (issue #58). The regional
> sketches are NoöPunk extrapolation over real present-day actors. References to
> current countries, companies and organisations are **speculative setting
> elements, not claims about the real world**.
>
> This document defines **no rules**. AGENTS.md §4 keeps equipment statistics,
> economy, vehicles and detailed simulation mechanics unresolved, and nothing here
> overrides that.

## 1. The design decision

NoöPunk has **no global technology level**.

The question the setting answers is not "is this Cyberpunk 2020 or Eclipse Phase?"
but "what did different ideological responses to the AI / AGI paradigm shift
produce?" The answer is that they produced **several incompatible futures
occupying the same planet**, and technology is therefore a product of ideological
struggle, political economy, catastrophe, culture and infrastructure rather than of
elapsed time.

The canonical statement:

> **NoöPunk should not choose between Cyberpunk and Eclipse Phase. It should
> contain both, because different ideological responses to the paradigm shift
> produced different futures.**

### The anti-ranking rule

This is the part easiest to get wrong, so it is enforced by a test:

> **Every technological regime gains some capabilities and creates different
> vulnerabilities.**

There is deliberately **no scalar technology score** and no ordering of regions by
"advancedness". A region that leads in AI autonomy may be unable to feed itself. A
region with banned autonomous systems may be the only one whose infrastructure still
works. Reducing a profile to "how advanced is this region" defeats the design.

## 2. How to read a profile

A region's profile assigns a **value on each of thirteen dimensions**. Each
dimension is an ordered scale, not a number:

| Dimension | Scale |
|---|---|
| AI autonomy | `banned → regulated → ubiquitous → superintelligent` |
| Robotics | `scarce → industrial → ubiquitous` |
| Cybernetics | `medical → consumer → transhuman` |
| BCI | `assistive → universal → collective` |
| Biotech | `contemporary → regenerative → posthuman` |
| Virtuality | `screens → ar → full_sensory → substrate_independent` |
| Space | `earthbound → orbital → interplanetary` |
| Energy | `constrained → abundant → near_post_scarcity` |
| Manufacturing | `centralized → fablabs → molecular_autonomous` |
| Psionics | `fringe → reproducible → industrialized` |
| Noösphere | `cultural_metaphor → measurable → infrastructural` |
| Governance | `nation_state → platform_state → cybernetic_post_state` |
| Ecology | `collapse → adaptation → restoration` |

Two rules govern reading them:

1. **A dimension may be unassigned.** Where the author has not specified a region's
   position, the value is `null` and stays `null`. A blank is a blank, not a
   placeholder to fill in with a genre convention.
2. **A profile may be internally uneven.** The United States profile is *bimodal*:
   elite and corporate zones sit at the top of several scales while the devastated
   interior is salvage economy. Reading it as one uniformly high profile is the
   misreading the matrix exists to prevent — which is why the file marks it
   `$profile_bimodal`.

### The posture is not the whole ideology

A region's `posture` (accelerationist / AI-critical / doomer / hybrid) summarises its
response to the **AI shift specifically**. It is not the region's position on every
paradigm shift, and it is deliberately not the same vocabulary as
[`ideology.json`](WORLD_IDEOLOGY.md)'s per-shift `position_kinds`. A region can be AI
critical and still pro-psionics; that is a normal combination, not an inconsistency.

## 3. The regions

Seven sketches, each with a posture, a profile, and an explicit **gains /
vulnerabilities** pair.

### United States — failed accelerationist superpower

Went full Accelerationist and suffered **both** rogue-AGI catastrophes. The result is
the clearest instance of the setting's central contrast: **maximum technological
capability plus minimum social stability**. The corporations that built the old
accelerationist order survive better than the state does, and run orbital
infrastructure, enclaves, AI systems, logistics and security.

*Reading:* Eclipse Phase inside elite and corporate zones, post-apocalyptic salvage
elsewhere.

### European Federation — AI-critical welfare cybernetics

Deliberately slowed or regulated some AGI and automation trajectories, so it looks
conservative beside the surviving US corporate zones while remaining politically
coherent, egalitarian, infrastructure-rich and ecologically healthier. Universal
public BCI, privacy-preserving digital identity, public AI, democratic cybernetics,
cooperative automation, biosphere restoration.

The open question stands **unresolved**:

> Is the European Federation actually technologically behind, or has it optimised
> for robustness, ecological sustainability and human autonomy rather than raw
> capability?

*Reading:* Cyberpunk+ with selective transhumanism, and socially far more functional.

### China — closed post-AGI synthesis

Experienced its own rogue-AGI crisis and became much more closed. Outside observers
do not understand the resulting system, and the profile **records that opacity
rather than resolving it**: five dimensions are left unassigned because the author's
sketch does not assign them, and the stated values are a synthesis to be discovered,
not an observed capability.

Possible synthesis: Taoism, Maoism, cybernetics, cyborgism, collective intelligence,
state planning, noöspheric ideas — with collective BCIs, state-scale cognitive
systems, cybernetic communes and post-individual identity systems.

*Reading:* unknown; possibly extremely advanced but opaque.

### Russia — post-defeat civil war

Fragmented after military defeat by federal European armies: EU-aligned west,
Chinese-aligned east, and autonomous, military, nationalist, criminal, corporate and
local formations between. A theatre for proxy warfare, abandoned military AI,
smuggling, experimental governance and black-market cybernetics.

Note that its governance value is **nominal** — no single authority holds the
territory, so `platform_state` describes competing platform-like formations rather
than one state.

*Reading:* uneven military cyberpunk plus salvage society.

### Middle East — Butlerian Jihad

A broad rejection of autonomous machine intelligence, which **does not mean
technological backwardness**. Development diverges into human-controlled
computation, hardened analog systems, biotech, religious cybernetics, non-AI expert
systems, anti-machine warfare, cognition enhancement, and psionics and noöspheric
practice.

Its comparative advantage is structural: regions that never depended on autonomous
systems **cannot suffer the class of catastrophe that destroyed the United States.**

#### The jinn question

The noöspheric paradigm may radically alter the interpretation of **djinn / jinn**.
This is `in_world_unknown` and stays that way: NoöPunk does not settle whether such
entities are independent NHI, psychological entities, panpsychic structures,
interdimensional beings, collective thoughtforms, or something else entirely. The
file lists the candidate readings precisely so that no later session picks one.

### India — noöspheric renaissance

The paradigm shift arrives as **continuity rather than crisis**, because many of the
new discoveries can be interpreted through existing philosophical and religious
traditions while old worldviews elsewhere enter crisis. Consciousness research,
panpsychism, idealism, quantum cognition, meditation technologies, nervous-system
engineering, psionics, post-materialist science and noöspheric institutions.

*Reading:* Eclipse Phase-level in selected consciousness, aerospace and biotech
domains, culturally distinct from Western transhumanism.

Two playful reinterpretations are recorded as extrapolation, not as claims about the
traditions: **Siddhis** as advanced psionic capabilities or technologies, and
**Vimanas** as advanced aerospace or anomalous propulsion systems.

> **Ganesh has returned.**

That statement is `in_world_unknown`. A literal divine manifestation, an AI or NHI, a
collective noöspheric entity, a cultural-symbolic event, and something stranger all
remain open, and the file says so.

### Sub-Saharan Africa — unexpectedly healthy future

Deliberately **not** the standard cyberpunk ruined extraction zone. It may be one of
the healthier macro-regions, for structural reasons: less dependence on legacy
infrastructure that failed elsewhere, younger populations, decentralised energy,
mobile-first institutions, distributed manufacturing, less exposure to some AGI
catastrophes, cooperative and commons-based development, leapfrogging of centralised
industrial systems, locally adapted AI and cybernetic systems, climate adaptation,
pan-African political integration, and new cultural confidence.

Its profile records **low robotics and no orbital presence plainly**, rather than
treating them as deficits: its advantages are distributed resilience and local
fabrication, not peak capability in every dimension.

*Reading:* heterogeneous, resilient, decentralised, and often healthier than richer
regions.

## 4. The two rogue-AGI catastrophes

The issue specifies **two** events where `TIMELINE.md` previously carried one:

| | Event | Severity | Resolution |
|---|---|---|---|
| 1 | First Rogue AGI Holocaust | contained | defeated by conventional military means |
| 2 | Second Rogue AGI Holocaust | continental | required large-scale EMP attacks, including nuclear EMP |

The first was the **proof of possibility** and was nonetheless read as a containment
success, so it did not change the accelerationist course. The second devastated much
of the continental United States and left a fragmented failed state.

Company attributions are **setting fiction about a fictional future event**, recorded
as such in the file, not claims about the real companies.

## 5. Gameplay consequences

Guidance for scenario design, not mechanics.

> **Travelling between regions should feel like moving between different science
> fiction genres.**

- an EU character enters a US orbital corporate enclave and experiences capability
  shock;
- a US corporate transhuman enters rural Europe and is surprised by the *absence* of
  omnipresent autonomous AI;
- Chinese systems appear incomprehensible because they rest on different assumptions
  about individuality;
- Indian psionic technology outperforms Western cybernetics in entirely different
  domains;
- African distributed systems survive catastrophes that destroy sophisticated
  centralised ones;
- Butlerian regions may be almost impossible for autonomous AI characters to enter.

The tonal registers available **inside one coherent world** include cyberpunk,
post-cyberpunk, solarpunk, post-apocalypse, transhumanism, posthumanism, weird
fiction, space opera, and noöspheric / psionic science fiction.

## 6. What this does not define

The issue's own open questions that remain **author decisions**, and are deliberately
not answered here:

- the approximate era and any exact date (AGENTS.md §6: still 20XX);
- which technologies are globally mature as opposed to region-specific;
- which regions reach Eclipse Phase-like capability in which sectors;
- the detailed internal politics of any region;
- any numeric technology score, tech-level modifier, equipment availability table or
  economy.

A dimension the author has not assigned stays `null` in the data and is reported as
unassigned rather than filled. Where a region's sketch is an extrapolation beyond the
author's text, the entry carries `$example` so it can be cut.

## 7. Related documents

- [`TIMELINE.md`](../TIMELINE.md) — the dated sequence, including the supersession of
  the single rogue-AGI entry.
- [`data/world/ideology.json`](../data/world/ideology.json) — the multi-axis
  ideological model. Positions on different paradigm shifts are separable; a
  regional tech posture is not a substitute for it.
- [`docs/WORLD_IDEOLOGY.md`](WORLD_IDEOLOGY.md) — the human-readable companion to the
  ideology model.
- [`docs/WRITING_STYLE_AND_MODELING.md`](WRITING_STYLE_AND_MODELING.md) §4 — the
  epistemic-status vocabulary used to mark setting fiction as extrapolation.
