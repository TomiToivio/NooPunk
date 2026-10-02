# The regional technology matrix

> **Status:** author-specified worldbuilding (issue #58), expanded into a
> machine-readable matrix. **Setting fiction.** References to current countries,
> companies and organisations are speculative setting elements, not claims about the
> real world.
>
> The canonical artefact is [`data/world/tech_matrix.json`](../data/world/tech_matrix.json).
> This document explains it. Where the two disagree, the JSON is authoritative.
>
> All dates in the setting are written **20XX** (`AGENTS.md` §6). This matrix assigns
> no year to any region or event.

## 1. The design rule

NoöPunk has **no single global technology level**. Technology is uneven because
different societies responded differently to the AI/AGI paradigm shift, so the
technological landscape is a product of ideological struggle, political economy,
catastrophe, culture and infrastructure.

The point is not that some regions are ahead and others behind:

> **Every technological regime gains some capabilities and creates different
> vulnerabilities.**

A player travelling between regions should feel they are moving between different
science-fiction genres — cyberpunk, post-cyberpunk, solarpunk, post-apocalypse,
transhumanism, posthumanism, weird fiction, space opera and Noöspheric/psionic
science fiction — inside one coherent world.

The issue's own summary: *"NoöPunk should not choose between Cyberpunk and Eclipse
Phase. It should contain both."*

## 2. How to read a profile

Each region carries a `posture` (its ideological response) and a `profile` giving a
value per **dimension**, or `unassigned`.

Thirteen dimensions, each an **open ordered ladder** rather than a number:

| Dimension | Ladder |
|---|---|
| AI autonomy | banned → regulated → ubiquitous → superintelligent |
| Robotics | scarce → industrial → ubiquitous |
| Cybernetics | medical → consumer → transhuman |
| BCI | assistive → universal → collective |
| Biotech | contemporary → regenerative → posthuman |
| Virtuality | screens → AR → full sensory → substrate-independent |
| Space | Earthbound → orbital → interplanetary |
| Energy | constrained → abundant → near-post-scarcity |
| Manufacturing | centralized → fablabs → molecular/autonomous |
| Psionics | fringe → reproducible → industrialized |
| Noösphere | cultural metaphor → measurable → infrastructural |
| Governance | nation-state → platform-state → cybernetic/post-state |
| Ecology | collapse → adaptation → restoration |

Two rules make this readable rather than a ranking:

- **The ladders are not commensurable.** `banned` AI autonomy is not "less
  technology" than `superintelligent`; a Butlerian region is described by the issue
  as highly advanced along other routes. Comparing values across different dimensions
  is meaningless by construction.
- **There is deliberately no numeric tech score and no derived modifier.** Same
  boundary `data/world/ideology.json` draws for ideology ("no numeric ideology
  score"). A single scalar would collapse the incomparability the setting depends on.

## 3. Epistemic status of every cell

This is lore, so `AGENTS.md` §1 applies: author intent is canon and agents must not
fill gaps. Each cell therefore records where it came from, using
[`WRITING_STYLE_AND_MODELING.md`](WRITING_STYLE_AND_MODELING.md) §4's levels:

| Cell state | Meaning |
|---|---|
| **stated** | issue #58's own text supports the value |
| **$example: true** | extrapolated from a qualitative sentence in the issue; cuttable |
| **unassigned** | the issue does not say, so nothing is asserted |

**49 of the 91 dimension × region cells are unassigned; 42 carry a value.** No cell
was invented to make a profile look complete.

## 4. Regions

### United States — failed accelerationist superpower

**Posture:** accelerationist. Two rogue-AGI catastrophes, the second requiring
large-scale EMP attacks including nuclear EMP. The surviving US is a fragmented
failed state.

The issue's own framing is a genre split held in one territory: *Mad Max* wasteland
and dead infrastructure on one side, extreme libertarian cyberpunk enclave
capitalism, orbital cities, corporate sovereignty and high-end transhumanism on the
other.

> **Maximum technological capability + minimum social stability.**

Corporate blocs descending from real companies operate orbital infrastructure,
enclaves, communications, AI systems and security. They are recorded as **setting
fiction** and as antecedents only — no corporation is characterised, given territory
or assigned capability.

**Gains:** the setting's maximum capability; elite zones at Eclipse Phase level.
**Vulnerabilities:** failed state, devastated interior, abandoned autonomous
infrastructure nobody controls, capability concentrated in enclaves.

### European Federation — AI Critical welfare cybernetics

**Posture:** AI Critical. Deliberately slowed or regulated some AGI/automation
trajectories, and so *appears* conservative beside the surviving US corporate zones.

Strengths the issue names: universal public BCI infrastructure, privacy-preserving
digital identity, public AI, democratic cybernetics, ecological engineering,
renewable energy, advanced healthcare, public transport, cooperative automation,
biosphere restoration.

**Gains:** politically coherent, stable, relatively egalitarian, ecologically
healthier. **Vulnerabilities:** the apparent lag is partly real and partly chosen;
restricted AI autonomy may cost capability where autonomy is decisive; institutional
coherence is itself the load-bearing dependency.

> **Left open, per the issue:** is the EU actually behind, or has it optimised for
> robustness, ecological sustainability and human autonomy rather than raw capability?

### China — closed post-AGI synthesis

**Posture:** opaque. A rogue-AGI crisis of its own, then closure; outside observers do
not understand the resulting system.

Possible synthesis the issue names: Taoism, Maoism, cybernetics, cyborgism,
collective intelligence, state planning, Noöspheric ideas — and technologies fitting
neither "AI" nor "human" as Western categories frame them: collective BCIs,
state-scale cognitive systems, human-machine planning assemblages, cybernetic
communes, post-individual identity systems.

**This profile is deliberately sparse.** Most of its cells are `unassigned`, because
the issue describes these as concepts China *may* have developed. **Filling them in
would destroy the setting effect the issue asks for.** The mystery is the canon.

### Russia — post-defeat fragmentation

**Posture:** fragmented after military defeat by federal European armies. Western
regions hold EU-aligned or EU-supported factions; eastern regions Chinese-aligned or
supported; between them, autonomous, military, nationalist, criminal, corporate and
local formations.

**Gains:** a sanctuary and marketplace for experimental governance; autonomous
weapons, mercenary factions and abandoned military AI available to whoever can pay or
take them; black-market cybernetics.
**Vulnerabilities:** fragmentation, ruined nuclear/industrial infrastructure, no
central authority able to restrain autonomous systems.

### Middle East — Butlerian Jihad

**Posture:** a broad Butlerian Jihad against autonomous machine intelligence. The
issue is explicit that this does **not** mean the region is technologically backward;
development diverges instead into human-controlled computation, hardened analog
systems, biotech, religious cybernetics, non-AI expert systems, anti-machine warfare,
cognition enhancement, and psionics and Noöspheric practice.

**The jinn question is IN-WORLD UNKNOWN.** The issue asks whether entities encountered
through psionics, altered states, quantum consciousness or the Noösphere correspond to
older traditions concerning jinn, and asks to keep it ambiguous. Candidate readings —
independent NHI, psychological entities, panpsychic structures, interdimensional
beings, collective thoughtforms, or something else — are listed and **none is
selected**. Per §4 that refusal is first-class canon: a later contributor must not
resolve it.

### India — Noöspheric renaissance

**Posture:** India becomes a major cultural and intellectual superpower, and the
paradigm shift is less culturally destructive because existing philosophical and
religious traditions can absorb it. Consciousness research, panpsychism, idealism,
quantum cognition, advanced meditation technologies, psionics, BCI/nervous-system
engineering, post-materialist science, Noöspheric institutions.

The issue playfully reframes old concepts as names for technologies: **Siddhis** as
advanced psionic capabilities or technologies, **Vimanas** as advanced aerospace or
anomalous propulsion systems. Recorded as the author's framing, with no mechanism
attached.

**"Ganesh has returned" is left open** — literal divine manifestation, AI/NHI,
collective Noöspheric entity, cultural-symbolic event, or something stranger.
IN-WORLD UNKNOWN; not decided here.

### Sub-Saharan Africa — unexpectedly healthy future

**Posture:** decentralised commons. The issue deliberately rejects the "ruined
extraction zone" trope and makes this possibly one of the healthier macro-regions:
younger populations, decentralised energy, mobile-first institutions, distributed
manufacturing, less exposure to some AGI catastrophes, cooperative/commons-based
development, leapfrogging centralised industry, locally adapted AI, climate
adaptation, pan-African political integration. Solar abundance, local fabrication,
open-source technology, cooperative ownership, mesh networks, human-scale urbanism,
selective cybernetics.

Its vulnerabilities are therefore **not material ruin — they are the costs of
decentralisation**: less concentrated capability, and heterogeneity as a coordination
burden.

## 5. The two catastrophes, and the timeline supersession

The issue specifies **two** US rogue-AGI catastrophes:

1. **First — contained.** Defeated with conventional military means; the first major
   proof that AGI catastrophe was possible.
2. **Second — severe.** Required large-scale EMP attacks, including nuclear EMP; much
   of the continental United States was devastated.

`TIMELINE.md` currently records **one**. `data/world/tech_matrix.json` therefore
carries an explicit `supersedes` block naming the target section and the reason,
rather than silently rewriting a timeline fact. The existing entry's phrase
"concentrated primarily in the United States" remains true under the two-event
reading, so the change is additive where it can be.

The real company names the issue attaches to these events are marked **setting
fiction**. NoöPunk asserts nothing about any real organisation's safety record,
conduct or capability.

## 6. Gameplay consequences (narrative guidance, not rules)

The issue asks that regional difference matter mechanically: travelling between
regions should feel like moving between genres. Examples it gives:

- an EU character entering a US orbital corporate enclave: massive capability shock;
- a US corporate transhuman in rural Europe: surprised by the *absence* of
  omnipresent autonomous AI;
- Chinese systems appearing incomprehensible because they rest on different
  assumptions about individuality;
- Indian psionic technology outperforming Western cybernetics in different domains;
- African distributed systems surviving catastrophes that destroy centralised ones;
- Butlerian regions being nearly impossible for autonomous AI characters to enter.

**These produce no rules here.** `AGENTS.md` §4 keeps equipment statistics, economy,
vehicles and detailed simulation mechanics unresolved, so this section is scenario and
narrative guidance only — no modifiers, no point costs, no travel mechanics.

One interface the matrix does imply, for whoever implements it later: a region's
posture should **refuse** an action that contradicts it rather than penalise it. An
autonomous AI in a Butlerian region is refused by the region, not rolled at a penalty
— the same shape the rules layer already uses for an absent system, so a refusal can
never be misread as a failed attempt.

## 7. What this document does not do

- **It does not answer the issue's open questions.** The approximate era, which
  technologies are globally mature, which are region-specific, which areas reach
  Eclipse Phase-like capability and which stay near Cyberpunk 2020/RED — all are
  author decisions, listed under `open_questions_unassigned` in the JSON.
- **It does not invent organisations, places or events.** No megacorp is named,
  territoried or given capability; the issue's one-line antecedents stay one-line.
- **It does not resolve the open metaphysical readings** — the jinn, Ganesh, or the
  status of Vimana-style propulsion. Those are IN-WORLD UNKNOWN by the issue's own
  instruction.
- **It defines no mechanics.**

## See also

- [`data/world/tech_matrix.json`](../data/world/tech_matrix.json) — the canonical matrix
- [`WORLD_IDEOLOGY.md`](WORLD_IDEOLOGY.md) — the ideological model these postures reference
- [`THEMES_IDEOLOGY_AND_PARADIGM_SHIFTS.md`](THEMES_IDEOLOGY_AND_PARADIGM_SHIFTS.md) — the paradigm-shift grammar
- [`TIMELINE.md`](../TIMELINE.md) — the scenario the catastrophes belong to
- [`WRITING_STYLE_AND_MODELING.md`](WRITING_STYLE_AND_MODELING.md) — the epistemic-status vocabulary used above
